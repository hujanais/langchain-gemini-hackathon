import streamlit as st
import requests
from PIL import Image
from io import BytesIO

from agents.multimodal_agent import MultiModalAgent

if "agent" not in st.session_state:
    st.session_state.agent = MultiModalAgent()
if "image" not in st.session_state:
    st.session_state.image = None

st.markdown("### Multimodal LLM")

col1, col2 = st.columns([4,1])
with col1:
    image_url = st.text_input(label='Image URL', value='https://picsum.photos/200')
with col2:
    btn_image =  st.button('Load image')

txt_query = st.text_input('User input', placeholder="Describe this image vividly to someone who is visually impared?")

if btn_image:
    response = requests.get(image_url)
    st.session_state.image = Image.open(BytesIO(response.content))

if st.session_state.image:
    st.image(st.session_state.image)

if txt_query and st.session_state.image:
    resp = st.session_state.agent.multimodal_chat(txt_query, st.session_state.image)
    st.markdown(resp)