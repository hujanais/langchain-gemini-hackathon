from typing import Optional, Type
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
import PyPDF2 as pdf

class RequestBody(BaseModel):
    query: str = Field(description='query')

class ResumeTool(BaseTool):
    name = "resume_tool"
    description = "Use when you need to query the candidate's resume"
    args_schema: Type[BaseModel] = RequestBody
    return_direct = True

    def _run(
        self, 
        query: str, 
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        reader = pdf.PdfReader(
            "../../resumes/Communications Electronics Technician-Resume Sample.pdf"
        )
        resume = ""
        for page in range(len(reader.pages)):
            page = reader.pages[page]
            resume += str(page.extract_text())

        return resume
        # return 'I am sorry but I do not have your resume.  Please update a copy'

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")
