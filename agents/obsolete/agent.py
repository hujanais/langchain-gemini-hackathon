import os
from dotenv import load_dotenv

from agents.fiass_utility import FiassUtility

load_dotenv()
from operator import itemgetter

from agents.qa_memory import QAMemory

import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
import PyPDF2 as pdf
from langchain_community.document_loaders import PyPDFLoader

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_community.document_loaders import (
    DirectoryLoader,
    UnstructuredMarkdownLoader,
)

from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

class Agent:
    def __init__(self):
        apiKey = os.environ["GOOGLE_API_KEY"]
        self.llm = ChatGoogleGenerativeAI(
            model="models/gemini-1.0-pro-001", google_api_key=apiKey, temperature=0.2
        )
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        self.memory = QAMemory(3)
        self.db = None 
        self.resumeEmbedding = None
        self.chain = None

    def buildChain(self):
        # Prompt Template
        template = """You are a friendly and useful assistant to help with searching and summarizing military jobs.  You will also be able to analyze the candidate's resume.
        You are not only an experience recruiter but also one that is very encouraging and generously identifying appropriate jobs for the candidate.  You will reply concisely in a conversational manner.

        Answer questions based only on the following:
        context: {context}

        Current conversation:
        {history}
        Candidate's resume: {resume}
        Question: {question}
        """
        prompt = ChatPromptTemplate.from_template(template)

        retriever = self.db.as_retriever()
        resume_retriever = self.resumeEmbedding.as_retriever()

        # Build the langchain
        self.chain = (
            {
                "context": itemgetter("question") | retriever,
                "question": itemgetter("question"),
                "resume": itemgetter("question") | resume_retriever,
                "history": itemgetter("history"),
            }
            | prompt
            | self.llm
            | StrOutputParser()
        )

        print('conversation chain complete...');

    def uploadResume(self, uploaded_file):
        reader = pdf.PdfReader(uploaded_file)
        resume = "** Candidate's Resume **"
        for page in range(len(reader.pages)):
            page = reader.pages[page]
            resume += str(page.extract_text())

        self.resumeEmbedding = FAISS.from_documents([Document(page_content=resume)], self.embeddings)

    def uploadResume2(self):
        loader = PyPDFLoader("./resumes/Aerospace-Engineer-Resume-Sample.pdf")
        documents = loader.load()
        documents[0].page_content = "**Candidate Resume**" + documents[0].page_content
        print(documents[0].page_content)
        # resume = "** Candidate's Resume **"
        # for page in range(len(reader.pages)):
        #     page = reader.pages[page]
        #     resume += str(page.extract_text())

        self.resumeEmbedding = FAISS.from_documents(documents, self.embeddings)

    def crawlJobs(self):
        # load documents
        loader = DirectoryLoader(
            "./documents", glob="**/*.md", loader_cls=UnstructuredMarkdownLoader
        )
        pages = loader.load()

        # Extract text content from each page
        page_texts = [page.page_content for page in pages]

        # Option #1. manual splitting by page
        documents = []
        for page_text in page_texts:
            documents.append(Document(page_content=page_text))

        # Option #2. split text into chunks
        # text_splitter = RecursiveCharacterTextSplitter()
        # documents = text_splitter.create_documents(page_texts)

        # perform embeddings
        self.db = FAISS.from_documents(documents, self.embeddings)

        resumes = [Document(page_content="Resume not found")]
        self.resumeEmbedding = FAISS.from_documents(resumes, self.embeddings)

        print('embeddings completed...')

    def chat(self, question: str):
        try:
            result = self.chain.invoke(
                {
                    "question": question,
                    "history": self.memory.getHistory(),
                }
            )

            # update the conversation history
            self.memory.add(question, result)
            return result
        except Exception as err:
            return err