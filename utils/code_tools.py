import subprocess
import os
import uuid

WORKSPACE = "./workspace"
CODE_WORKSPACE = "./code"
os.makedirs(WORKSPACE, exist_ok=True)

class PythonExecutor:
    def execute_code(self, code: str) -> str:
        if not code.strip():
            return "[No code provided]"
        filename = os.path.join(CODE_WORKSPACE, f"user_code_{uuid.uuid4().hex[:8]}.py")
        with open(filename, "w") as f:
            f.write(code)

        try:
            result = subprocess.run(["python", filename], capture_output=True, text=True, timeout=100)
            return result.stdout.strip() or result.stderr.strip() or "[No output]"
        except subprocess.TimeoutExpired:
            return "[Code execution timed out]"

def execute_python_code(code: str) -> str:
    """
    Execute Python code and return the output.
    """
    print("[Executing code...]\n[Code to execute: {code}]")
    return PythonExecutor().execute_code(code)

def install_dependencies(modules: list[str]) -> str:
    """
    Install Python dependencies using pip.
    """
    if not modules:
        return "[No dependencies to install]"
    try:
        result = subprocess.run(["pip", "install", *modules], check=True, capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"[Error installing packages: {e.stderr.strip()}]"
