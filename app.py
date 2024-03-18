from agents.candidate_agent import CandidateAgent

if __name__ == "__main__":
    agent = CandidateAgent()
    agent.initialize_no_resume()

    while True:
        user_input = input(">> ")
        if user_input.lower() == "bye":
            print("LLM: Goodbye")
            break

        if user_input is not None:
            resp = agent.chat(user_input)
            print(resp)