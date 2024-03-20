import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import pandas as pd

from agents.fiass_utility import FiassUtility
from agents.prompt_templates.de import get_DE_recruiter_template
from datastore.job_model import JobModel
from datastore.job_store import JobDataStore
from datastore.resume_store import ResumeDataStore

load_dotenv()
from operator import itemgetter

from agents.qa_memory import QAMemory

import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_community.document_loaders import PyPDFLoader

from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

jobDataStore = JobDataStore()
resumeDataStore = ResumeDataStore()

class RecruiterAgent:
    def __init__(self):
        apiKey = os.environ["GOOGLE_API_KEY"]
        self.llm = ChatGoogleGenerativeAI(
            model="models/gemini-1.0-pro-001", google_api_key=apiKey, temperature=0.1
        )

        # apiKey = os.environ["OPENAI_KEY"]
        # self.llm = ChatOpenAI(openai_api_key=apiKey, model_name="gpt-3.5-turbo", temperature=0)
        
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        # self.embeddings = GPT4AllEmbeddings()
        self.resumedb = None
        self.chain = None
        self.analyzer_chain = None
        self.jobs: list[JobModel] = jobDataStore.getAllJobs()

        self.crawlResumes()
        # self.buildPromptTemplate()
        self.buildAnalyzerPromptTemplate()

    # return list of job titles
    def enumerateJobs(self) -> list[str]:
        job_titles = list(map(lambda x: x.document, self.jobs))
        return job_titles

    def crawlResumes(self):
        resumes = resumeDataStore.getDEResumes()
        pages = list(map(lambda x: x.resume, resumes))

        # Extract page_content from each page
        page_texts = [page.page_content for page in pages]

        # Option #1. manual splitting by page.
        documents = []
        for page_text in page_texts:
            documents.append(Document(page_content=page_text))

        # # Option #2. split text into chunks
        # # text_splitter = RecursiveCharacterTextSplitter()
        # # documents = text_splitter.create_documents(page_texts)

        # perform embeddings
        self.resumedb = FAISS.from_documents(documents, self.embeddings)

        print("embeddings completed...")

    def buildAnalyzerPromptTemplate(self):
        self.memory = QAMemory(3)
        self.analyzer_chain = None

        # Prompt Template
        template = get_DE_recruiter_template()

        prompt = ChatPromptTemplate.from_template(template)

        retriever = self.resumedb.as_retriever()

        # Build the langchain
        self.analyzer_chain = (
            {
                "context": itemgetter("question") | retriever,
                "job": itemgetter("job"),
                "question": itemgetter("question")
            }
            | prompt
            | self.llm
            | StrOutputParser()
        )

        print("recruiter agent prompt-template initialized...")

    def buildPromptTemplate(self):
            self.memory = QAMemory(3)
            self.chain = None

            # Prompt Template
            template = """You are an experienced recruiter that knows everything about the Bundeswehr.  You can analyze the candidate's resume against a selected job description.
                Reply with Markdown syntax.
            
            Answer questions based only on the following:
            context: {context}
            job: itemgetter("job"),
            Question: {question}
            """
            prompt = ChatPromptTemplate.from_template(template)

            retriever = self.resumedb.as_retriever()

            # Build the langchain
            self.chain = (
                {
                    "context": itemgetter("question") | retriever,
                    "job": itemgetter("job"),
                    "question": itemgetter("question")
                }
                | prompt
                | self.llm
                | StrOutputParser()
            )

            print("recruiter agent prompt-template initialized...")

    def chat(self, question: str, jobDescription: str):
        try:
            result = self.chain.invoke(
                {
                    "question": question,
                    "job": jobDescription
                }
            )

            # update the conversation history
            self.memory.add(question, result)
            return result
        except Exception as err:
            return err

    def analyze(self, job: str):
        try:
            question = """Please analyze each candidate's resume and generate a suitability percentage based on the candidate's interest, relevant skills, experience and educational background based on the job description.
                Please sort candidates by descending order of percentage"""

            result = self.analyzer_chain.invoke(
                {
                    "question": question,
                    "job": job
                }
            )

            # update the conversation history
            self.memory.add(question, result)
            return result
        except Exception as err:
            return err 