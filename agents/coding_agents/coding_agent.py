from agno.agent import Agent
from agno.tools.coding import CodingTools

from config import db, default_model, memory_manager
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
    memory_manager=memory_manager,
    enable_agentic_memory=True,
    add_history_to_context=True,
    update_memory_on_run=True,
    markdown=True,
)
