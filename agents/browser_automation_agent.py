import os
import sys
import subprocess
from langgraph.prebuilt import create_react_agent

def browser_automation_agent_main(user_query: str, timeout: int = 60) -> str:
    """
    Invoke the standalone script as a subprocess and stream progress.
    """
    script_path = os.path.join(os.path.dirname(__file__), "browser_agent.py")
    cmd = [sys.executable, script_path, user_query]
    # Launch with UTF-8 encoding and replace errors to avoid UnicodeEncodeError
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding='utf-8',
        errors='replace',
        bufsize=1
    )
    full_output = []
    try:
        for line in proc.stdout:
            # Stream each progress line back to caller
            print(line.strip(), flush=True)
            full_output.append(line)
        proc.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        proc.kill()
        return f"Error: browser automation timed out after {timeout} seconds."
    except subprocess.CalledProcessError as e:
        return f"Error: browser automation failed with exit code {e.returncode}: {e.stderr.strip()}"
    return "".join(full_output).strip()



# 8) Create React-style browser automation agent
browser_automation_agent = create_react_agent(
    model="openai:gpt-4.1",
    tools=[browser_automation_agent_main],
    prompt=(
        "You are a browser automation agent.\n\n"
        "INSTRUCTIONS:\n"
        "- Assist ONLY with web browsing tasks\n"
        "- After you're done, respond with results only."
    ),
    name="browser_automation_agent",
)