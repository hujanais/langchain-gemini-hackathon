import streamlit as st

from agents.recruiter_agent import RecruiterAgent
from datastore.job_store import JobDataStore

def recruiter_page(agent: RecruiterAgent):
    st.markdown("### Recruiter View")

    jobs = JobDataStore().getAllJobs()
    job_titles = list(map(lambda x: x.title, jobs))
    
    # Create a dictionary mapping job titles to job objects
    job_dict = {job.title: job for job in jobs}

    selectedJobTitle = st.selectbox(
        "Select job",
        job_titles,
    )

    btn_analyze = st.button('Analyze')

    if btn_analyze:
        st.markdown(f"Analyzing {selectedJobTitle}")
        selectedJob = job_dict[selectedJobTitle]
        resp = agent.analyze(job=selectedJob)
        st.markdown(resp)