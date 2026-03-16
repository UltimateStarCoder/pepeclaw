from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools.shell import ShellTools
from dotenv import load_dotenv

from config import db, memory_manager

load_dotenv()

shell_agent = Agent(
    id="shell-agent",
    name="Shell Agent",
    model=Claude(id="claude-sonnet-4-5"),
    instructions=["You are a shell command assistant. Execute shell commands to help with system tasks."],
    tools=[ShellTools()],
    db=db,
    memory_manager=memory_manager,
    enable_agentic_memory=True,
    add_history_to_context=True,
    update_memory_on_run=True,
    markdown=True,
)
