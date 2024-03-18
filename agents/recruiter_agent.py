import os
from dotenv import load_dotenv
import pandas as pd

from agents.fiass_utility import FiassUtility
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
            model="models/gemini-1.0-pro-001", google_api_key=apiKey, temperature=0.2
        )
        # self.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        self.embeddings = GPT4AllEmbeddings()
        self.db = None
        self.chain = None
        self.analyzer_chain = None
        self.jobs: list[JobModel] = jobDataStore.getAllJobs()

        self.crawlResumes()
        self.buildPromptTemplate()
        self.buildAnalyzerPromptTemplate()

    # return list of job titles
    def enumerateJobs(self) -> list[str]:
        job_titles = list(map(lambda x: x.document, self.jobs))
        return job_titles

    def crawlResumes(self):
        resumes = resumeDataStore.getResumes()
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
        self.db = FAISS.from_documents(documents, self.embeddings)

        print("embeddings completed...")

    def buildAnalyzerPromptTemplate(self):
        self.memory = QAMemory(3)
        self.analyzer_chain = None

        # Prompt Template
        template = """You are an experienced military recruiter that is skilled at analyzing jobs and to find candidates that are suitable using their resumes.
            Given the following job:
            job: {job}
            
            Find and rate candidates from the following candidate list only:
            context: {context}

            Question: {question}
            """

        prompt = ChatPromptTemplate.from_template(template)

        retriever = self.db.as_retriever()

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
            template = """You are an experienced military recruiter that is skilled at analyzing jobs and to find candidates that are suitable using their resumes.
            
            Answer questions based only on the following candidate resumes:
            context: {context}

            Current conversation:
            {history}
            Question: {question}
            """
            prompt = ChatPromptTemplate.from_template(template)

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

            print("recruiter agent prompt-template initialized...")

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

    def analyze(self, job: str, question: str):
        try:
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