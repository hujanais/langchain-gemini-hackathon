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
            model="models/gemini-pro", google_api_key=apiKey, temperature=0.1
        )
        
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        self.resumeDb = None
        self.jobDb = None
        self.chain = None
        self.analyzer_chain = None
        self.memory = QAMemory(3)
        self.memory = QAMemory(3)

        self.loadResumes()
        self.loadJobs()
        self.buildPromptTemplate()
        self.buildAnalyzerPromptTemplate()

    def loadJobs(self):
        jobs = jobDataStore.getAllJobs()
        pages = list(map(lambda x: x.document, jobs))
        self.list_of_jobs = ', '.join(list(map(lambda x: x.title, jobs)))

        # Extract page_content from each page
        page_texts = [page.page_content for page in pages]

        # Option #1. manual splitting by page.  this seems to be better to keep maintain
        # context of each job description
        documents = []
        for page_text in page_texts:
            documents.append(Document(page_content=page_text))

        print(len(documents))

        # Option #2. split text into chunks
        # text_splitter = RecursiveCharacterTextSplitter()
        # documents = text_splitter.create_documents(page_texts)

        # perform embeddings
        self.jobDb = FAISS.from_documents(documents, self.embeddings)

    def loadResumes(self):
        resumes = resumeDataStore.getDEResumes()
        pages = list(map(lambda x: x.resume, resumes))
        self.list_of_resumes = ', '.join(list(map(lambda x: x.name, resumes)))

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
        self.resumeDb = FAISS.from_documents(documents, self.embeddings)

        print("embeddings completed...")

    def buildAnalyzerPromptTemplate(self):
        self.memory = QAMemory(3)
        self.analyzer_chain = None

        # Prompt Template
        template = """You are an experienced recruiter that knows everything about the Bundeswehr and that is skilled at analyzing jobs and finding candidates that are suitable based on their resumes.  You will first analyze the important
        aspects of the job and then go through the list of all candidates.  For each candidate, you wil then analyze the candidate's interest, experience, training and educational background to build your match.  You shall consider 'candidate' and 'resume' as interchangeable terms.

            Your answer is based on the job and resumes which you have full access:
            job: {job}
            context: {resumes}

            Question: {question}
            """

        prompt = ChatPromptTemplate.from_template(template)

        retriever = self.resumeDb.as_retriever()

        # Build the langchain
        self.analyzer_chain = (
            {
                "resumes": itemgetter("question") | retriever,
                "job": itemgetter("job"),
                "question": itemgetter("question")
            }
            | prompt
            | self.llm
            | StrOutputParser()
        )

        print("recruiter agent analyzer-template initialized...")

    def buildPromptTemplate(self):
            self.memory = QAMemory(3)
            self.chain = None

            # Prompt Template
            template = """You are an experienced recruiter that knows everything about the Bundeswehr.  You can analyze the candidate's resume against a selected job description.
            When referring to either a candidate or a resume, feel free to use either word as appropriate to convey the same meaning.

            Answer questions based only on the following:
            List of all job openings: [{list_of_jobs}]
            List of all resumes: [{list_of_resumes}]
            job: {job}
            context: {resumes}

            Current conversation:
            {history}
            Question: {question}

            Reply with Markdown syntax.

            """
            prompt = ChatPromptTemplate.from_template(template, kwargs={"k":100})
            prompt = prompt.partial(
                list_of_jobs=self.list_of_jobs,
                list_of_resumes=self.list_of_resumes
            )

            retriever = self.resumeDb.as_retriever()
            jobsRetriever = self.jobDb.as_retriever()

            # Build the langchain
            self.chain = (
                {
                    "resumes": itemgetter("question") | retriever,
                    "job": itemgetter("question") | jobsRetriever,
                    "question": itemgetter("question"),
                    "history": itemgetter("history")
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
                    "history": self.memory.getHistory()
                }
            )

            # update the conversation history
            self.memory.add(question, result)
            return result

        except Exception as err:
            return err

    def analyze_job(self, job: JobModel):
        print('analyze_job', job.title)
        try:
            question = """Please analyze the job description and list the important skills."""

            result = self.analyzer_chain.invoke(
                {
                    "question": question,
                    "job": job.document
                }
            )

            # update the conversation history
            # self.memory.add(question, result)
            return result
        except Exception as err:
            return err 
        
    def analyze(self, job: JobModel):
        print('find_candidates', job.title)
        try:
            question = """Please analyze each candidate's resume and generate a suitability percentage based on the candidate's interest, relevant skills, experience and educational background based on the job description.
                Please sort candidates by descending order of percentage"""

            result = self.analyzer_chain.invoke(
                {
                    "question": question,
                    "job": job.document
                }
            )

            # update the conversation history
            # self.memory.add(question, result)
            return result
        except Exception as err:
            return err 