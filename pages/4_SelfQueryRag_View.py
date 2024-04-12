import streamlit as st

from agents.self_query_rag_agent import SelfQueryRagAgent

def getAgent() -> SelfQueryRagAgent:
    if "agent" not in st.session_state:
        st.session_state.agent = SelfQueryRagAgent()
    return st.session_state.agent

st.markdown("#### Self-Querying RAG")
st.markdown("##### Search wines")

txt_query = st.text_input(label='Query', placeholder='Show me fruity Italian wines after the year 2010')

if txt_query:
    documents = getAgent().run(txt_query)
    markdown_text = ''
    for doc in documents:
        title = doc.page_content
        metadata = doc.metadata

        markdown_text += f"""
            Wine Description: {title}

            ``` {metadata} ```
        """

    st.markdown(markdown_text)