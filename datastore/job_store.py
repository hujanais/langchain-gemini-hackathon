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

        self.jobs = loader.load()

        loader = DirectoryLoader(
            "./datastore/docs", glob="**/*.md", loader_cls=UnstructuredMarkdownLoader
        )

        self.documents = self.jobs + loader.load()

    def getAllDocs(self) -> list[JobModel]:
        allDocs: list[JobModel] = []
        for document in self.documents:
            arr = document.page_content.split("\n")
            allDocs.append(JobModel(title=arr[1], document=document))

        return allDocs

    def getAllJobs(self) -> list[JobModel]:
        jobs: list[JobModel] = []
        for document in self.jobs:
            arr = document.page_content.split("\n")
            jobs.append(JobModel(title=arr[1], document=document))

        return jobs
