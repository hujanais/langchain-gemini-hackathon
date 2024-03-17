import streamlit as st

from classes.candidate_agent import CandidateAgent

def candidate_page(agent: CandidateAgent):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("Candidate View")
    with col2:
        # clear conversation button
        if st.button("Clear"):
            st.session_state.clear()
    with col3:
        st.write('Hello, *World!* :sunglasses:')

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

    # show job table
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