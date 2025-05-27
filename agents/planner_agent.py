from langgraph.prebuilt import create_react_agent

def plan_task(task: str) -> str:
    """
    Create a step-wise plan to complete the task.
    """
    return (
        f"Plan for task '{task}':\n"
        "1. Research the topic.\n"
        "2. Perform calculations if needed.\n"
        "3. Install dependencies if required.\n"
        "4. Execute code and summarize results."
    )

planner_agent = create_react_agent(
    model="openai:gpt-4.1",
    tools=[plan_task],
    prompt=(
        "You are a planner agent.\n\n"
        "INSTRUCTIONS:\n"
        "- Create step wise plan and follow that plan to complete the task.\n"
        "- If you are not sure how to complete the task, ask the user for more information.\n"
        "- Assign tasks to the appropriate agent based on their capabilities.\n"
        "- Do not do any work yourself."
    ),
    name="planner_agent",
)
