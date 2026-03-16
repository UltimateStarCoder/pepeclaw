from pathlib import Path

from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools.python import PythonTools
from dotenv import load_dotenv

load_dotenv()

python_agent = Agent(
    id="python-agent",
    name="Python Agent",
    model=Claude(id="claude-sonnet-4-5"),
    instructions=["You are a Python coding assistant. Write and execute Python code to solve problems."],
    tools=[
        PythonTools(
            base_dir=Path("tmp/python"),
            exclude_tools=["pip_install_package", "uv_pip_install_package"],
        ),
    ],
    markdown=True,
)
