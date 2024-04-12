import streamlit as st
import requests
from PIL import Image
from io import BytesIO

from agents.multimodal_agent import MultiModalAgent

agent = MultiModalAgent()

st.markdown("### Multimodal LLM")

image_url = st.text_input(label='Image URL', value='https://picsum.photos/200')
btn_submit = st.button('Analyze')

if btn_submit:
    if image_url:
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))
        st.image(img)
        resp = agent.multimodal_chat(img)
        st.markdown(resp)