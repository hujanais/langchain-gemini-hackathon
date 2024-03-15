import streamlit as st

from classes.agent import Agent

# if __name__ == "__main__":
#     agent = Agent()
#     agent.crawlJobs()
#     agent.buildChain()

#     while True:
#         user_input = input(">> ")
#         if user_input.lower() == "bye":
#             print("LLM: Goodbye")
#             break

#         if user_input is not None:
#             resp = agent.chat(user_input)
#             print(resp)

def initializeAgent() -> Agent:
    if 'agent' not in st.session_state:
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
            # agent.uploadResume()
            agent.uploadResume2(uploaded_file)

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
