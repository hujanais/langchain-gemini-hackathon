import streamlit as st

from agents.recruiter_agent import RecruiterAgent


def recruiter_page(agent: RecruiterAgent):
    st.markdown("### Recruiter View")

    option = st.selectbox(
        "Select job",
        (
            "14 AIR DEFENSE ARTILLERY OFFICER",
            "14G AIR DEFENSE BATTLE MANAGEMENT SYSTEM OPERATOR",
            "17B CYBER AND ELECTRONIC WARFARE OFFICER",
            "25D TELECOMMUNICATIONS OPERATOR-MAINTAINER",
            "170A CYBER OPERATIONS TECHNICIAN",
        ),
    )

    if option:
        st.markdown(f"Analyzing {option}")

        candidates = [
            {
                "id": "123",
                "name": "candidate-1",
                "rating": "5",
            },
            {
                "id": "123",
                "name": "candidate-1",
                "rating": "5",
            },
            {
                "id": "123",
                "name": "candidate-1",
                "rating": "5",
                "summary": "highlight special attributes",
            },
            {
                "id": "123",
                "name": "candidate-1",
                "rating": "5",
            },
        ]

        st.table(candidates)