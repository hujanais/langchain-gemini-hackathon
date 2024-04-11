from agents.self_query_rag_agent import SelfQueryRagAgent
from agents.vectordb_rag_agent import VectorDbRagAgent


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

    # agent = RecruiterAgent()

    # job_titles = list(map(lambda x: x.title, jobs))
    # print(job_titles)

    # agent = SelfQueryRagAgent()
    agent = VectorDbRagAgent()

    while True:
        user_input = input(">> ")
        if user_input.lower() == "bye":
            print("LLM: Goodbye")
            break

        if user_input is not None:
            # resp = agent.chat(user_input)
            resp = agent.run(user_input)
            print(resp)    
