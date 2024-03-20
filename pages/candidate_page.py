import pandas as pd
import streamlit as st

from agents.candidate_agent import CandidateAgent

def candidate_page(agent: CandidateAgent):
    # initialize session state
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "How can I help you?"}
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