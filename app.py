import pandas as pd
import streamlit as st

from classes.agent import Agent
from classes.tool_agent import ToolAgent

if __name__ == "__main__":
    agent = Agent()
    agent.crawlJobs()
    agent.buildChain()

    while True:
        user_input = input(">> ")
        if user_input.lower() == "bye":
            print("LLM: Goodbye")
            break

        if user_input is not None:
            resp = agent.chat(user_input)
            print(resp)