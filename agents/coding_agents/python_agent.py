from pathlib import Path

from agno.agent import Agent
from agno.tools.python import PythonTools
from dotenv import load_dotenv

from config import db, default_model, memory_manager

load_dotenv()

python_agent = Agent(
    id="python-agent",
    name="Python Agent",
    model=default_model,
    instructions=["You are a Python coding assistant. Write and execute Python code to solve problems."],
    tools=[
        PythonTools(
            base_dir=Path("tmp/python"),
            exclude_tools=["pip_install_package", "uv_pip_install_package"],
        ),
    ],
    db=db,
    memory_manager=memory_manager,
    enable_agentic_memory=True,
    add_history_to_context=True,
    update_memory_on_run=True,
    markdown=True,
)
