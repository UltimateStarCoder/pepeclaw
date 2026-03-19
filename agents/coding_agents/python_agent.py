from pathlib import Path

from agno.agent import Agent
from agno.tools.python import PythonTools

from config import db, default_model, learning_machine
python_agent = Agent(
    id="python-agent",
    name="Python Agent",
    model=default_model,
    instructions=[
        "You are a Python coding assistant. Write and execute Python code to solve problems.",
        "After writing or modifying Python code, check for syntax errors and type issues. Run lint checks if a linter config is present in the project.",
    ],
    tools=[
        PythonTools(
            base_dir=Path("tmp/python"),
            exclude_tools=["pip_install_package", "uv_pip_install_package"],
        ),
    ],
    db=db,
    learning=learning_machine,
    add_history_to_context=True,
    add_learnings_to_context=True,
    markdown=True,
)
