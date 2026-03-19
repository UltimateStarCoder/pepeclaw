from agno.agent import Agent
from agno.tools.coding import CodingTools

from config import db, default_model, learning_machine
coding_agent = Agent(
    id="coding-agent",
    name="Coding Agent",
    model=default_model,
    instructions=[
        "You are a coding assistant. Read, write, edit files and run shell commands to solve coding tasks.",
        "After writing or modifying code, run the project's lint and type-check commands to verify correctness. Fix any errors before reporting the task as complete.",
    ],
    tools=[CodingTools()],
    db=db,
    learning=learning_machine,
    add_history_to_context=True,
    add_learnings_to_context=True,
    markdown=True,
)
