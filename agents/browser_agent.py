import os
import sys
import subprocess
import asyncio
from browser_use.browser import BrowserProfile, BrowserSession
from browser_use import Agent
from langchain_openai.chat_models import ChatOpenAI

# Ensure UTF-8 output in Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')


def create_event_loop():
    """
    Create and set a fresh asyncio event loop for this process.
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop


async def browser_automation(user_query: str) -> str:
    """Run browser automation and return text response."""
    browser_profile = BrowserProfile(headless=True)
    browser_session = BrowserSession(browser_profile=browser_profile)
    try:
        agent = Agent(
            task=user_query,
            browser_session=browser_session,
            tool_calling_method="function_calling",
            llm=ChatOpenAI(model="gpt-4.1")
        )
        result = await agent.run(max_steps=10)
        text_response = ''
        for action in result.action_results():
            content = action.extracted_content or ''
            # emit a progress line
            print(f"[BrowserAgent Progress] {content}", flush=True)
            text_response += content + "\n"
        return text_response.strip()
    finally:
        await browser_session.close()


if __name__ == '__main__':
    # Ensure UTF-8 output in this standalone script too
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')

    if len(sys.argv) != 2:
        print("Usage: python browser_agent.py \"<user query>\"")
        sys.exit(1)

    query = sys.argv[1]
    create_event_loop()
    response = asyncio.get_event_loop().run_until_complete(browser_automation(query))
    print(response, flush=True)
