import pandas as pd
import streamlit as st
from agents.candidate_agent import CandidateAgent

def getAgent() -> CandidateAgent:
    if "candidate_agent" not in st.session_state:
        st.session_state.candidate_agent = CandidateAgent()
        st.session_state.candidate_agent.initialize_no_resume()
    return st.session_state.candidate_agent

# initialize session states
st.session_state.title = "### Candidate View - No Resume - !!!CHATGPT!!!"

# build sidebar
with st.sidebar:
    uploaded_file = st.file_uploader("Upload your resume(md)...", type=["md"])
    submit_resume = st.button("Upload")

    if submit_resume and uploaded_file is not None:
        getAgent().initialize_with_resume(uploaded_file)
        prompt = "I have uploaded my resume.  Please confirm my name and email.  Reply with Welcome my name and then show other details"
        response = getAgent().chat(prompt)
        full_response = ""
        for item in response:
            full_response += item
        message = {"role": "assistant", "content": full_response}
        st.session_state.title = "### Candidate View - With Resume - !!!CHATGPT!!!"
        st.session_state.messages.append(message)

if st.session_state.title:
    st.markdown(st.session_state.title)

# initialize session state
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Welcome to the Bundeswehr career website.  Would you like to start by uploading your resume?"}
    ]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# chat input
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# listen for message changes
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = getAgent().chat(prompt)
                placeholder = st.empty()
                full_response = ""
                for item in response:
                    full_response += item
                    placeholder.markdown(full_response)
                placeholder.markdown(full_response)
            except Exception as err:
                placeholder.markdown(f"I am sorry.  There was an error. {err}")

    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)
