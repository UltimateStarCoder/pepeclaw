from agno.agent import Agent
from agno.tools.shell import ShellTools

from config import db, default_model, memory_manager
shell_agent = Agent(
    id="shell-agent",
    name="Shell Agent",
    model=default_model,
    instructions=["You are a shell command assistant. Execute shell commands to help with system tasks."],
    tools=[ShellTools()],
    db=db,
    memory_manager=memory_manager,
    enable_agentic_memory=True,
    add_history_to_context=True,
    update_memory_on_run=True,
    markdown=True,
)
