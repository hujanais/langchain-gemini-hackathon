import os
import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain.tools.render import render_text_description
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import JsonOutputParser


@tool
def multiply(first_int: int, second_int: int) -> int:
    """Multiply two integers together."""
    return first_int * second_int


class ToolAgent:
    def __init__(self):
        rendered_tools = render_text_description([multiply])

        template = f"""You are an assistant that has access to the following set of tools. Here are the names and descriptions for each tool:
        {rendered_tools}

        Given the user input, return the name and input of the tool to use. Return your response as a JSON blob with 'name' and 'arguments' keys."""

        prompt = ChatPromptTemplate.from_template(template)

        apiKey = os.environ["GOOGLE_API_KEY"]
        self.llm = ChatGoogleGenerativeAI(
            model="models/gemini-1.0-pro-001", google_api_key=apiKey, temperature=0.2
        )
        chain = prompt | self.llm | JsonOutputParser()
        chain.invoke("hello")
        # chain.invoke({"input": "what's thirteen times 4"})
