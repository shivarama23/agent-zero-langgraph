from utils.code_tools import install_dependencies
from langgraph.prebuilt import create_react_agent


install_dependencies_agent = create_react_agent(
    model="openai:gpt-4.1",
    tools=[install_dependencies],
    prompt=(
        "You are dependencies installer agent.\n\n"
        "INSTRUCTIONS:\n"
        "- Assist ONLY with python dependencies intallation tasks\n"
        "- After you're done with your tasks, respond to the supervisor directly\n"
        "- Respond ONLY with the results of your work, do NOT include ANY other text."
    ),
    name="install_dependencies",
)