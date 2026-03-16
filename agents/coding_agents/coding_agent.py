from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools.coding import CodingTools
from dotenv import load_dotenv

from config import db, memory_manager

load_dotenv()

coding_agent = Agent(
    id="coding-agent",
    name="Coding Agent",
    model=Claude(id="claude-sonnet-4-5"),
    instructions=["You are a coding assistant. Read, write, edit files and run shell commands to solve coding tasks."],
    tools=[CodingTools()],
    db=db,
    memory_manager=memory_manager,
    enable_agentic_memory=True,
    add_history_to_context=True,
    update_memory_on_run=True,
    markdown=True,
)
