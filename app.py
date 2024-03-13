import os
from dotenv import load_dotenv

load_dotenv()
from operator import itemgetter

from classes.qa_memory import QAMemory

import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
import PyPDF2 as pdf

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

import streamlit as st


class GeminiRag:
    def __init__(self):
        apiKey = os.environ["GOOGLE_API_KEY"]
        self.llm = ChatGoogleGenerativeAI(
            model="models/gemini-1.0-pro-001", google_api_key=apiKey, temperature=0.2
        )
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        self.resume = ""
        self.memory = QAMemory(3)
        self.db = None

    def uploadResume2(self, uploaded_file):
        reader = pdf.PdfReader(uploaded_file)
        self.resume = ""
        for page in range(len(reader.pages)):
            page = reader.pages[page]
            self.resume += str(page.extract_text())

        print(self.resume)


    def uploadResume(self):
        # load resume
        reader = pdf.PdfReader(
            "./resumes/Communications Electronics Technician-Resume Sample.pdf"
        )
        self.resume = ""
        for page in range(len(reader.pages)):
            page = reader.pages[page]
            self.resume += str(page.extract_text())

        print(self.resume)

    def crawlJobs(self):
        self.uploadResume()

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

    def chat(self, question: str):
        # Prompt Template
        template = """You are a friendly and useful assistant to help with searching and summarizing military jobs.  You will also be able to analyze the candidate's resume.  Reply with Markdown syntax.
        You are not only an experience recruiter but also one that is very encouraging and generously identifying appropriate jobs for the candidate.

        Answer questions based only on the following:
        context: {context}
        resume: {resume}

        Current conversation:
        {history}
        Question: {question}
        """
        prompt = ChatPromptTemplate.from_template(template)

        retriever = self.db.as_retriever()

        # Build the langchain
        chain = (
            {
                "context": itemgetter("question") | retriever,
                "question": itemgetter("question"),
                "resume": itemgetter("resume"),
                "history": itemgetter("history"),
            }
            | prompt
            | self.llm
            | StrOutputParser()
        )

        try:
            result = chain.invoke(
                {
                    "question": question,
                    "resume": self.resume,
                    "history": self.memory.getHistory(),
                }
            )

            # update the conversation history
            self.memory.add(question, result)

        except Exception as error:
            return error

        return result


# if __name__ == "__main__":
#     geminiRag = GeminiRag()
#     geminiRag.crawlJobs()

#     while True:
#         user_input = input(">> ")
#         if user_input.lower() == "bye":
#             print("LLM: Goodbye")
#             break

#         if user_input is not None:
#             resp = geminiRag.chat(user_input)
#             print(resp)

if __name__ == "__main__":
    st.markdown("### Welcome to the Military Job Bank 🛡️💼")

    geminiRag = GeminiRag()
    geminiRag.crawlJobs()

    # build sidebar
    with st.sidebar:
        input_text = st.text_area("Job Description: ", key="input")
        uploaded_file = st.file_uploader("Upload your resume(PDF)...", type=["pdf"])
        submit_resume = st.button("Upload")

        if submit_resume:
            geminiRag.uploadResume()
            # geminiRag.uploadResume2(uploaded_file)

    # initialize session state
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "How can I help you?"}
        ]

    # clear conversation button
    if st.button("Clear"):
        st.session_state.clear()

    # Display or clear chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # chat input
    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = geminiRag.chat(prompt)
                print(response)
                placeholder = st.empty()
                full_response = ""
                for item in response:
                    full_response += item
                    placeholder.markdown(full_response)
                placeholder.markdown(full_response)

        message = {"role": "assistant", "content": full_response}
        st.session_state.messages.append(message)
