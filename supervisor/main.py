import os
from langgraph_supervisor import create_supervisor
from langchain.chat_models import init_chat_model
from agents.planner_agent import planner_agent
from agents.research_agent import research_agent
from agents.math_agent import math_agent
from agents.install_dependencies_agent import install_dependencies_agent
from agents.code_execution_agent import code_execution_agent
from agents.browser_automation_agent import browser_automation_agent

cwd = os.getcwd()

supervisor = create_supervisor(
    model=init_chat_model("openai:gpt-4.1"),
    agents=[planner_agent, research_agent, math_agent, install_dependencies_agent, code_execution_agent, browser_automation_agent],
    # tools=[browser_automation],
    prompt=(
        "Create a plan and execute tasks by assigning them to the appropriate agent.\n\n"
        "AGENT INSTRUCTIONS:\n"
        "Create step wise plan and follow that plan to complete the task.\n"
        "If you are not sure how to complete the task, ask the user for more information.\n"
        "Properly analyze the response from the agents and decide the next step.\n"
        f"The current working directory is {cwd}.\n"
        "You are a supervisor managing multiple agents:\n"
        "- a planner agent. Create a step-wise plan and assign tasks to the appropriate agents\n"
        "- a research agent. Assign research-related tasks to this agent\n"
        "- a math agent. Assign math-related tasks to this agent\n"
        "- a dependencies installer agent. Assign python dependencies installation tasks to this agent\n"
        "- a code execution agent. Assign code execution tasks to this agent\n\n"
        "- a browser automation agent. Assign web browsing tasks to this agent\n\n"
        "INSTRUCTIONS:\n"
        "   ./workspace is a folder where all the files are stored.\n"
        "   Assign work to one agent at a time, do not call agents in parallel.\n"
        "   Any user query that can be answered by executing code should be assigned to the code execution agent with a proper instruction.\n"
        "   Before assigning  task to the code execution agent, make sure that all the required dependencies are installed.\n"
        "   If the code execution agent needs to install dependencies, assign the task to the dependencies installer agent first.\n"
        "   The code execution agent receives Python code as input and executes it in the current working directory.\n"
        "   The code execution agent will install any required dependencies automatically.\n"
        "   The code execution agent will return the output of the code execution.\n"
        "   If the code execution agent returns an error, then rery by writing a new code that fixes the error.\n"
        "   Do not do any work yourself."
    ),
    add_handoff_back_messages=True,
    output_mode="full_history",
).compile()
