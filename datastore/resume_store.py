import os
from langchain_core.documents import Document
from langchain_community.document_loaders import (
    DirectoryLoader,
    UnstructuredMarkdownLoader,
)

import PyPDF2
from datastore.resume_model import ResumeModel

class ResumeDataStore:
                
    def getResumes(self) -> list[ResumeModel]:
        resumeArr = [
            ['Jose Gonzales', './datastore/resumes/jose_gonzales.pdf'],
            ['Michelle Adams', './datastore/resumes/michelle_adams.pdf'],
            ['William Bradford', './datastore/resumes/william_bradford.pdf'],
            ['Suzanne Davis', './datastore/resumes/suzanne_davis.pdf'],
            ['Heather Cox', './datastore/resumes/heather_cox.pdf']
        ]

        # enumerate all resumes
        resumes: list[ResumeModel] = []
        for pair in resumeArr:
            reader = PyPDF2.PdfReader(pair[1])
            resumeText = ''
            for page in reader.pages:
                resumeText += page.extract_text()

            resumes.append(ResumeModel(name=pair[0], resume=Document(page_content=resumeText)))

        return resumes
    
    def getDEResumes(self) -> list[ResumeModel]:
        resumeArr = [
            ['Jana Muller', './datastore/de_resumes/jana_muller.md'],
            ['Karl Schmidt', './datastore/de_resumes/karl_schmidt.md'],
            ['Luca Fischer', './datastore/de_resumes/luca_fischer.md'],
            ['Lucas Becker', './datastore/de_resumes/lucas_becker.md'],
            ['Markus Weber', './datastore/de_resumes/markus_weber.md'],
        ]

        # enumerate all resumes
        resumes: list[ResumeModel] = []
        for pair in resumeArr:
            reader = UnstructuredMarkdownLoader(pair[1])
            document = reader.load()
            resumes.append(ResumeModel(name=pair[0], resume=document[0]))

        return resumes