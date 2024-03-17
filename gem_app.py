import streamlit as st

from classes.candidate_agent import CandidateAgent
from classes.agent import Agent
from pages import candidate_page, recruiter_page


# candidate-agent, recruiter-agent
def getAgent(agentName: str) -> Agent:
    if agentName == "candidate_agent":
        if "candidate_agent" not in st.session_state:
            st.session_state.candidate_agent = CandidateAgent()
            st.session_state.candidate_agent.initialize_no_resume()

        return st.session_state.candidate_agent
    elif agentName == "recruiter_agent":
        if "recruiter_agent" not in st.session_state:
            st.session_state.recruiter_agent = Agent()
            st.session_state.recruiter_agent.crawlJobs()
            st.session_state.recruiter_agent.buildChain()

        return st.session_state.recruiter_agent
    else:
        raise(f'{agentName} not found')

def main():
    selection = st.sidebar.radio("Select User Type", ("Candidate", "Recruiter"))

    if selection == "Candidate":
        agent = getAgent('candidate_agent')
        candidate_page.candidate_page(agent)

        with st.sidebar:
            uploaded_file = st.file_uploader("Upload your resume(PDF)...", type=["pdf"])
            submit_resume = st.button("Upload")

            if submit_resume:
                agent.initialize_with_resume(uploaded_file)
                st.empty()

    elif selection == "Recruiter":
        recruiter_page.recruiter_page(getAgent('recruiter_agent'))


if __name__ == "__main__":
    main()
