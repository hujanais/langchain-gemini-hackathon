import os
from pprint import pprint
from dotenv import load_dotenv
import pandas as pd
import requests
from io import BytesIO
from matplotlib import pyplot as plt

from PIL import Image
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage


class MultiModalAgent:
    def __init__(self):
        apiKey = os.environ["GOOGLE_API_KEY"]
        self.llm = ChatGoogleGenerativeAI(
            model="models/gemini-pro-vision",
            google_api_key=apiKey,
            temperature=0.1,
        )

        self.model = genai.GenerativeModel("gemini-pro-vision")

        # for model in genai.list_models():
        #    pprint.pprint(model)

    def chat(self, question: str) -> str:
        resp = self.llm.invoke(question)
        return resp.content

    def multimodal_chat(self, query: str, image: Image) -> str:

        # response = requests.get(image_url)
        # image_data = BytesIO(response.content)

        # # Open image using PIL
        # image = Image.open(image_data)

        # # Display the image
        # plt.figure(figsize=(4, 4))
        # plt.imshow(image)
        # plt.axis('off')
        # plt.show()

        # using Google Gemini API directly
        resp = self.model.generate_content(
            [query, image]
        )
        return resp.text

        # To provide an image, pass a human message with a content field set to an array of content objects.
        # Each content object where each dict contains either an image value (type of image_url) or a text (type of text) value.
        # The value of image_url must be a base64 encoded image (e.g., data:image/png;base64,abcd124):
        # example
        # message = HumanMessage(
        #     content=[
        #         {
        #             "type": "text",
        #             "text": "Describe this image to someone who is visually impared?",
        #         },  # You can optionally provide text parts
        #         {
        #             "type": "image_url",
        #             "image_url": image_url
        #         },
        #     ]
        # )

        # model = genai.GenerativeModel("gemini-pro-vision")
        # resp = model.generate_content(["Explain the picture?",image])
        # # resp = self.llm.invoke(message)
        # print(resp)
