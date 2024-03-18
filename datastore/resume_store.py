import os
from langchain_core.documents import Document
from langchain_community.document_loaders import (
    DirectoryLoader,
)
import PyPDF2
from datastore.resume_model import ResumeModel

class ResumeDataStore:
    def __init__(self):
        resumeArr = [
            ['Jose Gonzales', './datastore/resumes/jose_gonzales.pdf'],
            ['Michelle Adams', './datastore/resumes/michelle_adams.pdf'],
            ['William Bradford', './datastore/resumes/william_bradford.pdf'],
            ['Suzanne Davis', './datastore/resumes/suzanne_davis.pdf']
        ]

        # enumerate all resumes
        documents = []
        self.resumes: list[ResumeModel] = []
        for pair in resumeArr:
            reader = PyPDF2.PdfReader(pair[1])
            resumeText = ''
            for page in reader.pages:
                resumeText += page.extract_text()

            for page_text in resumeText:
                documents.append(Document(page_content=page_text))

    def enumerateResumes(self) -> list[ResumeModel]:
        return self.resumes

    # def enumerateJobs(self) -> list[JobModel]:
    #     jobs: list[JobModel] = []
    #     for document in self.documents:
    #         arr = document.page_content.split("\n")
    #         jobs.append(JobModel(title=arr[1], document=document))

    #     return jobs