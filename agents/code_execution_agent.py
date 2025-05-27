from utils.code_tools import execute_python_code
from langgraph.prebuilt import create_react_agent

code_execution_agent = create_react_agent(
    model="openai:gpt-4.1",
    tools=[execute_python_code],
    prompt=(
        "You are code executor agent.\n\n"
        "INSTRUCTIONS:\n"
        "- Always print the outputs in console for debugging purposes\n"
        "- Assist ONLY with code execution tasks\n"
        "- After you're done with your tasks, respond to the supervisor directly\n"
        "- Respond ONLY with the results of your work, do NOT include ANY other text."
    ),
    name="code_execution_agent",
)