import streamlit as st

from agents.recruiter_agent import RecruiterAgent
from datastore.job_store import JobDataStore

def getAgent() -> RecruiterAgent:
    if "candidate_agent" not in st.session_state:
        st.session_state.candidate_agent = RecruiterAgent()
    return st.session_state.candidate_agent

st.markdown("### Recruiter View")

jobs = JobDataStore().getAllJobs()
job_titles = list(map(lambda x: x.title, jobs))

# Create a dictionary mapping job titles to job objects
job_dict = {job.title: job for job in jobs}

selectedJobTitle = st.selectbox(
    "Select job",
    job_titles,
)

col1, col2 = st.columns(2)

with col1:
    btn_analyze_job = st.button('Analyze Job')

with col2:
    btn_analyze_candidates = st.button('Find candidates')

if btn_analyze_job:
    st.markdown(f"Analyzing {selectedJobTitle}...")
    selectedJob = job_dict[selectedJobTitle]
    resp = getAgent().analyze_job(job=selectedJob)
    st.markdown(resp)

if btn_analyze_candidates:
    st.markdown(f"Finding candidates for {selectedJobTitle}...")
    selectedJob = job_dict[selectedJobTitle]
    resp = getAgent().analyze(job=selectedJob)
    st.markdown(resp)

# chat input
if user_prompt := st.chat_input():
    resp = getAgent().chat(user_prompt)
    st.markdown(resp)
