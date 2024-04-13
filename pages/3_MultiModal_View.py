import streamlit as st
import requests
from PIL import Image
from io import BytesIO

from agents.multimodal_agent import MultiModalAgent

agent = MultiModalAgent()

st.markdown("### Multimodal LLM")

image_url = st.text_input(label='Image URL', value='https://picsum.photos/200')
txt_query = st.text_input('User input', placeholder="Describe this image vividly to someone who is visually impared?")

if (txt_query):
    print(txt_query)

if txt_query:
    if image_url:
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))
        st.image(img)
        resp = agent.multimodal_chat(txt_query, img)
        st.markdown(resp)