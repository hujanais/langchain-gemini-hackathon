import pandas as pd
import streamlit as st

from agents.obsolete.agent import Agent

def initializeAgent() -> Agent:
    if "agent" not in st.session_state:
        st.session_state.agent = Agent()
        st.session_state.agent.crawlJobs()
        st.session_state.agent.buildChain()

    return st.session_state.agent


if __name__ == "__main__":
    agent = initializeAgent()

    st.markdown("### Welcome to the Military Job Bank 🛡️💼")

    # build sidebar
    with st.sidebar:
        uploaded_file = st.file_uploader("Upload your resume(PDF)...", type=["pdf"])
        submit_resume = st.button("Upload")

        if submit_resume:
            agent.uploadResume(uploaded_file)

    # initialize session state
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "How can I help you?"}
        ]

    # clear conversation button
    if st.button("Clear"):
        st.session_state.clear()

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
                    response = agent.chat(prompt)
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

    # awesome table
    sample_data = [
        {
            "title": "123",
            "branch": "air-force",
            "description": "description",
            "link": "www.google.com",
        },
        {
            "title": "123",
            "branch": "air-force",
            "description": "description",
            "link": "www.google.com",
        },
        {
            "title": "123",
            "branch": "air-force",
            "description": "description",
            "link": "www.google.com",
        },
        {
            "title": "123",
            "branch": "air-force",
            "description": "description",
            "link": "www.google.com",
        },
        {
            "title": "123",
            "branch": "air-force",
            "description": "description",
            "link": "www.google.com",
        },
        {
            "title": "123",
            "branch": "air-force",
            "description": "description",
            "link": "www.google.com",
        },
        {
            "title": "123",
            "branch": "air-force",
            "description": "description",
            "link": "www.google.com",
        },
    ]

    st.table(sample_data)
