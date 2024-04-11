import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
load_dotenv()

from langchain.schema import Document
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.chains.query_constructor.base import AttributeInfo

class SelfQueryRagAgent:
    def __init__(self):
        apiKey = os.environ["GOOGLE_API_KEY"]
        self.llm = ChatGoogleGenerativeAI(
            model="models/gemini-pro", google_api_key=apiKey, temperature=0
        )
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

        # apiKey = os.environ["OPENAI_KEY"]
        # self.llm = OpenAI(openai_api_key=apiKey, temperature=0)
        # self.embeddings = OpenAIEmbeddings(api_key=apiKey)

        docs = [
            Document(
                page_content="Complex, layered, rich red with dark fruit flavors",
                metadata={
                    "name": "Opus One",
                    "year": 2018,
                    "rating": 96,
                    "grape": "Cabernet Sauvignon",
                    "color": "red",
                    "country": "USA",
                },
            ),
            Document(
                page_content="Luxurious, sweet wine with flavors of honey, apricot, and peach",
                metadata={
                    "name": "Château d'Yquem",
                    "year": 2015,
                    "rating": 98,
                    "grape": "Sémillon",
                    "color": "white",
                    "country": "France",
                },
            ),
            Document(
                page_content="Full-bodied red with notes of black fruit and spice",
                metadata={
                    "name": "Penfolds Grange",
                    "year": 2017,
                    "rating": 97,
                    "grape": "Shiraz",
                    "color": "red",
                    "country": "Australia",
                },
            ),
            Document(
                page_content="Elegant, balanced red with herbal and berry nuances",
                metadata={
                    "name": "Sassicaia",
                    "year": 2016,
                    "rating": 95,
                    "grape": "Cabernet Franc",
                    "color": "red",
                    "country": "Italy",
                },
            ),
            Document(
                page_content="Highly sought-after Pinot Noir with red fruit and earthy notes",
                metadata={
                    "name": "Domaine de la Romanée-Conti",
                    "year": 2018,
                    "rating": 100,
                    "grape": "Pinot Noir",
                    "color": "red",
                    "country": "France",
                },
            ),
            Document(
                page_content="Crisp white with tropical fruit and citrus flavors",
                metadata={
                    "name": "Cloudy Bay",
                    "year": 2021,
                    "rating": 92,
                    "grape": "Sauvignon Blanc",
                    "color": "white",
                    "country": "New Zealand",
                },
            ),
            Document(
                page_content="Rich, complex Champagne with notes of brioche and citrus",
                metadata={
                    "name": "Krug Grande Cuvée",
                    "year": 2010,
                    "rating": 93,
                    "grape": "Chardonnay blend",
                    "color": "sparkling",
                    "country": "New Zealand",
                },
            ),
            Document(
                page_content="Intense, dark fruit flavors with hints of chocolate",
                metadata={
                    "name": "Caymus Special Selection",
                    "year": 2018,
                    "rating": 96,
                    "grape": "Cabernet Sauvignon",
                    "color": "red",
                    "country": "USA",
                },
            ),
            Document(
                page_content="Exotic, aromatic white with stone fruit and floral notes",
                metadata={
                    "name": "Jermann Vintage Tunina",
                    "year": 2020,
                    "rating": 91,
                    "grape": "Sauvignon Blanc blend",
                    "color": "white",
                    "country": "Italy",
                },
            ),
        ]
        vectorstore = Chroma.from_documents(docs, self.embeddings)

        metadata_field_info = [
            AttributeInfo(
                name="grape",
                description="The grape used to make the wine",
                type="string or list[string]",
            ),
            AttributeInfo(
                name="name",
                description="The name of the wine",
                type="string or list[string]",
            ),
            AttributeInfo(
                name="color",
                description="The color of the wine",
                type="string or list[string]",
            ),
            AttributeInfo(
                name="year",
                description="The year the wine was released",
                type="integer",
            ),
            AttributeInfo(
                name="country",
                description="The name of the country the wine comes from",
                type="string",
            ),
            AttributeInfo(
                name="rating",
                description="The Robert Parker rating for the wine 0-100",
                type="integer",  # float
            ),
        ]
        document_content_description = "Brief description of the wine"

        self.retriever = SelfQueryRetriever.from_llm(
            self.llm,
            vectorstore,
            document_content_description,
            metadata_field_info,
            verbose=True
        )

    def run(self, query: str) -> str:
        docs = self.retriever.invoke(query)
        for document in docs:
            print(document.page_content)
            print(document.metadata)

        return docs
