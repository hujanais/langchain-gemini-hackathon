import os
from dotenv import load_dotenv
import pandas as pd

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


class RecruiterAgent:
    def __init__(self):
        apiKey = os.environ["GOOGLE_API_KEY"]
        self.llm = ChatGoogleGenerativeAI(
            model="models/gemini-1.0-pro-001", google_api_key=apiKey, temperature=0.2
        )
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        self.db = None
        self.chain = None

    def enumerateJobs(self):
        # TODO: get the list of jobs from the folder for now.  
        # the url is not saved but we can get it from the military-job website
        jobs = [
            {"title": "job-1", "link": "http://job1.mil"},
            {"title": "job-2", "link": "http://job2.mil"},
            {"title": "job-3", "link": "http://job3.mil"},
        ]

    def analyzeJob(jobId: str) -> list:
        # analyze the job against pool of candidates
        return []

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
