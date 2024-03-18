from langchain_community.document_loaders import (
    DirectoryLoader,
    UnstructuredMarkdownLoader,
)
from langchain_core.documents import Document

from datastore.job_model import JobModel

class JobDataStore:
    def __init__(self):
        loader = DirectoryLoader(
            "./datastore/jobs", glob="**/*.md", loader_cls=UnstructuredMarkdownLoader
        )

        self.documents = loader.load()

    def enumerateJobs(self) -> list[JobModel]:
        jobs: list[JobModel] = []
        for document in self.documents:
            arr = document.page_content.split("\n")
            jobs.append(JobModel(title=arr[1], document=document))

        return jobs
