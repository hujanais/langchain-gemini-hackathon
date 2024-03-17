import pandas as pd
import streamlit as st

from agents.obsolete.agent import Agent
from agents.tool_agent import ToolAgent

if __name__ == "__main__":
    agent = Agent()
    agent.crawlJobs()
    agent.buildChain()
    agent.uploadResume2()

    while True:
        user_input = input(">> ")
        if user_input.lower() == "bye":
            print("LLM: Goodbye")
            break

        if user_input is not None:
            resp = agent.chat(user_input)
            print(resp)