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
resumeDataStore = ResumeDataStore()

class RecruiterAgent:
    def __init__(self):
        apiKey = os.environ["GOOGLE_API_KEY"]
        self.llm = ChatGoogleGenerativeAI(
            model="models/gemini-1.0-pro-001", google_api_key=apiKey, temperature=0.2
        )
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        self.db = None
        self.chain = None
        self.jobs: list[JobModel] = jobDataStore.enumerateJobs()

        self.crawlResumes()

    # return list of job titles
    def enumerateJobs(self) -> list[str]:
        job_titles = list(map(lambda x: x.document, self.jobs))
        return job_titles

    def analyzeJob(jobId: str) -> list:
        # analyze the job against pool of candidates
        return []

    def crawlResumes(self):
        resumes = resumeDataStore.enumerateResumes()
        # pages = list(map(lambda x: x.document, jobs))
        # self.list_of_jobs = ', '.join(list(map(lambda x: x.title, jobs)))

        # # Extract page_content from each page
        # page_texts = [page.page_content for page in pages]

        # # Option #1. manual splitting by page.  this seems to be better to keep maintain
        # # context of each job description
        # documents = []
        # for page_text in page_texts:
        #     documents.append(Document(page_content=page_text))

        # # Option #2. split text into chunks
        # # text_splitter = RecursiveCharacterTextSplitter()
        # # documents = text_splitter.create_documents(page_texts)

        # # perform embeddings
        # self.db = FAISS.from_documents(documents, self.embeddings)

        # print("embeddings completed...")


    # def chat(self, question: str):
    #     try:
    #         result = self.chain.invoke(
    #             {
    #                 "question": question,
    #                 "history": self.memory.getHistory(),
    #             }
    #         )

    #         # update the conversation history
    #         self.memory.add(question, result)
    #         return result
    #     except Exception as err:
    #         return err
