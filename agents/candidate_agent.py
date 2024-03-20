import os
from dotenv import load_dotenv

from agents.prompt_templates.de import get_DE_candidate_no_resume_template, get_DE_candidate_with_resume_template
from agents.prompt_templates.us import get_US_candidate_no_resume_template
from datastore.job_store import JobDataStore
from agents.fiass_utility import FiassUtility

load_dotenv()
from operator import itemgetter

from agents.qa_memory import QAMemory

import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.embeddings import GPT4AllEmbeddings
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

jobDataStore = JobDataStore()

class CandidateAgent:
    def __init__(self):
        print("ctor CandidateAgent")
        apiKey = os.environ["GOOGLE_API_KEY"]
        self.llm = ChatGoogleGenerativeAI(
            model="models/gemini-1.0-pro-001", google_api_key=apiKey, temperature=0
        )
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        # self.embeddings = GPT4AllEmbeddings()
        self.memory = QAMemory(3)
        self.db = None
        self.chain = None
        self.list_of_jobs = []

        self.loadAllDocs()

    def initialize_no_resume(self):
        self.memory = QAMemory(3)
        self.chain = None

        # Prompt Template
        template = get_DE_candidate_no_resume_template()

        prompt = ChatPromptTemplate.from_template(template)
        prompt = prompt.partial(
            list_of_jobs=self.list_of_jobs
        )

        retriever = self.db.as_retriever()

        # Build the langchain
        self.chain = (
            {
                "context": itemgetter("question") | retriever,
                "question": itemgetter("question"),
                "history": itemgetter("history"),
            }
            | prompt
            | self.llm
            | StrOutputParser()
        )

        print("initialize_with_no_resume completed...")

    def initialize_with_resume(self, uploaded_resume):
        self.memory = QAMemory(3)
        self.chain = None

        # read in the resume in pdf format
        # reader = pdf.PdfReader(uploaded_resume)
        # resume = "** Candidate's Resume **"
        # for page in range(len(reader.pages)):
        #     page = reader.pages[page]
        #     resume += str(page.extract_text())

        # read in the resume in markdown format
        resume = "** Candidate's Resume **"
        resume += uploaded_resume.getvalue().decode('utf-8')

        # Prompt Template
        template = get_DE_candidate_with_resume_template()

        prompt = ChatPromptTemplate.from_template(template)
        prompt = prompt.partial(
            list_of_jobs=self.list_of_jobs,
            resume=resume
        )

        retriever = self.db.as_retriever()

        # Build the langchain
        self.chain = (
            {
                "context": itemgetter("question") | retriever,
                "question": itemgetter("question"),
                "history": itemgetter("history"),
            }
            | prompt
            | self.llm
            | StrOutputParser()
        )

        print("initialize_with_resume completed...")

    def loadAllDocs(self):
        jobs = jobDataStore.getAllDocs()
        pages = list(map(lambda x: x.document, jobs))
        self.list_of_jobs = ', '.join(list(map(lambda x: x.title, jobs)))

        # Extract page_content from each page
        page_texts = [page.page_content for page in pages]

        # Option #1. manual splitting by page.  this seems to be better to keep maintain
        # context of each job description
        documents = []
        for page_text in page_texts:
            documents.append(Document(page_content=page_text))

        # Option #2. split text into chunks
        # text_splitter = RecursiveCharacterTextSplitter()
        # documents = text_splitter.create_documents(page_texts)

        # perform embeddings
        self.db = FAISS.from_documents(documents, self.embeddings)

        print("embeddings completed...")

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
