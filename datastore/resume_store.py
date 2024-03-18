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
            ['Suzanne Davis', './datastore/resumes/suzanne_davis.pdf'],
            ['Heather Cox', './datastore/resumes/heather_cox.pdf']
        ]

        # enumerate all resumes
        self.resumes: list[ResumeModel] = []
        for pair in resumeArr:
            reader = PyPDF2.PdfReader(pair[1])
            resumeText = ''
            for page in reader.pages:
                resumeText += page.extract_text()

            self.resumes.append(ResumeModel(name=pair[0], resume=Document(page_content=resumeText)))
        
    def getResumes(self) -> list[ResumeModel]:
        return self.resumes