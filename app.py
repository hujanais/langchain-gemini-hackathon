from agents.candidate_agent import CandidateAgent
from agents.recruiter_agent import RecruiterAgent
from datastore.job_store import JobDataStore
from datastore.resume_store import ResumeDataStore

if __name__ == "__main__":
    # agent = CandidateAgent()
    # agent.initialize_no_resume()
    
    # while True:
    #     user_input = input(">> ")
    #     if user_input.lower() == "bye":
    #         print("LLM: Goodbye")
    #         break

    #     if user_input is not None:
    #         resp = agent.chat(user_input)
    #         print(resp)

    agent = RecruiterAgent()

    # job_titles = list(map(lambda x: x.title, jobs))
    # print(job_titles)

    while True:
        user_input = input(">> ")
        if user_input.lower() == "bye":
            print("LLM: Goodbye")
            break

        if user_input is not None:
            resp = agent.chat(user_input)
            print(resp)    
