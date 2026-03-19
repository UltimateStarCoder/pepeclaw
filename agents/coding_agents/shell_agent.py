from agno.agent import Agent
from agno.tools.shell import ShellTools

from config import db, default_model, learning_machine
shell_agent = Agent(
    id="shell-agent",
    name="Shell Agent",
    model=default_model,
    instructions=["You are a shell command assistant. Execute shell commands to help with system tasks."],
    tools=[ShellTools()],
    db=db,
    learning=learning_machine,
    add_history_to_context=True,
    add_learnings_to_context=True,
    markdown=True,
)
