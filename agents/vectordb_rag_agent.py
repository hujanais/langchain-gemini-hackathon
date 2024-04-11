import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_text_splitters import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter,
)

load_dotenv()

from langchain.retrievers import ParentDocumentRetriever
from langchain.storage import InMemoryStore
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import TextLoader
from langchain.chains import RetrievalQA
from langchain_community.llms import OpenAI

class VectorDbRagAgent:
    def __init__(self):
        apiKey = os.environ["GOOGLE_API_KEY"]
        self.llm = ChatGoogleGenerativeAI(
            model="models/gemini-pro", google_api_key=apiKey, temperature=0,
            convert_system_message_to_human=True
        )
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

        # apiKey = os.environ["OPENAI_KEY"]
        # self.llm = OpenAI(openai_api_key=apiKey, temperature=0)
        # embeddings = OpenAIEmbeddings(api_key=apiKey)

        loaders = [
            TextLoader(
                "./datastore/samples/langchain_blog_posts/blog.langchain.dev_announcing-langsmith_.txt"
            ),
            TextLoader(
                "./datastore/samples/langchain_blog_posts/blog.langchain.dev_benchmarking-question-answering-over-csv-data_.txt"
            ),
        ]

        # loader = TextLoader("./datastore/samples/state_of_the_union.txt")
        # documents = loader.load()

        self.docs = []
        for loader in loaders:
            self.docs.extend(loader.load())

        self.small_chunks_retriever()
        # self.full_chunks_retriever()

    def small_chunks_retriever(self):
        # This text splitter is used to create the child documents
        child_splitter = RecursiveCharacterTextSplitter(chunk_size=400)

        # The vectorstore to use to index the child chunks
        vectorstore = Chroma(
            collection_name="full_documents", embedding_function=self.embeddings
        )

        # The storage layer for the parent documents
        store = InMemoryStore()

        small_chunk_retriever = ParentDocumentRetriever(
            vectorstore=vectorstore,
            docstore=store,
            child_splitter=child_splitter,
        )
        small_chunk_retriever.add_documents(self.docs, ids=None)

        sub_docs = vectorstore.similarity_search("what is langsmith?", k=2)
        print(sub_docs[0].page_content)
        print("#######################")
        retrieved_docs = small_chunk_retriever.get_relevant_documents("what is langsmith?")
        # print(retrieved_docs[0].page_content)

        qa = RetrievalQA.from_chain_type(llm=self.llm,
                                 chain_type="stuff",
                                 retriever=small_chunk_retriever)
        
        print(qa.invoke('what is langsmith?'))

    def full_chunks_retriever(self):
       # This text splitter is used to create the parent documents - The big chunks
        parent_splitter = RecursiveCharacterTextSplitter(chunk_size=2000)

        # This text splitter is used to create the child documents - The small chunks
        # It should create documents smaller than the parent
        child_splitter = RecursiveCharacterTextSplitter(chunk_size=400)

        # The vectorstore to use to index the child chunks
        vectorstore = Chroma(collection_name="split_parents", embedding_function=self.embeddings) #OpenAIEmbeddings()

        # The storage layer for the parent documents
        store = InMemoryStore() 

        big_chunks_retriever = ParentDocumentRetriever(
            vectorstore=vectorstore,
            docstore=store,
            child_splitter=child_splitter,
            parent_splitter=parent_splitter,
        )

        big_chunks_retriever.add_documents(self.docs)

        qa = RetrievalQA.from_chain_type(llm=self.llm,
                                 chain_type="stuff",
                                 retriever=big_chunks_retriever)
        
        print(qa.invoke('what is langsmith?'))

    def run(self, query: str) -> str:
        docs = self.retriever.invoke(query)
        for document in docs:
            print(document.page_content)
            print(document.metadata)
            print()

        return "docs"
