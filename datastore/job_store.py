from langchain_community.document_loaders import (
    DirectoryLoader,
    UnstructuredMarkdownLoader,
)
from langchain_core.documents import Document

from datastore.job_model import JobModel

def enumerateJobs() -> list[JobModel]:
     # load documents
        loader = DirectoryLoader(
            "./datastore/jobs", glob="**/*.md", loader_cls=UnstructuredMarkdownLoader
        )
        documents = loader.load()

        for document in documents:
            arr = document.page_content.split('\n')
            print(arr[1])

        return documents
