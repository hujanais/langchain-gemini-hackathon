import streamlit as st

from agents.recruiter_agent import RecruiterAgent
from datastore.job_store import JobDataStore

def recruiter_page(agent: RecruiterAgent):
    st.markdown("### Recruiter View")

    jobs = JobDataStore().getAllJobs()
    job_titles = list(map(lambda x: x.title, jobs))

    option = st.selectbox(
        "Select job",
        job_titles,
    )

    if option:
        st.markdown(f"Analyzing {option}")

        candidates = [
            {
                "name": "candidate-1",
                "rating": "5",
                "comments": "good mechanical experience",
            },
            {
                "name": "candidate-1",
                "rating": "5",
                "comments": "good mechanical experience",
            },
            {
                "name": "candidate-1",
                "rating": "5",
                "comments": "good mechanical experience",
            },
            {
                "name": "candidate-1",
                "rating": "5",
                "comments": "good mechanical experience",
            },
            {
                "name": "candidate-1",
                "rating": "5",
                "comments": "good mechanical experience",
            },
        ]

        st.table(candidates)
