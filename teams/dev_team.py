from agno.team import Team

from agents.coding_agents.coding_agent import coding_agent
from config import db, reasoning_model
from agents.coding_agents.file_agent import file_agent
from agents.coding_agents.python_agent import python_agent
from agents.coding_agents.reasoning_agent import reasoning_agent
from agents.coding_agents.shell_agent import shell_agent
from agents.mcp_agents.svelte_mcp_agents import svelte_mcp_agents

dev_team = Team(
    id="dev-team",
    name="Dev Team",
    description="A team that builds and debugs code.",
    model=reasoning_model,
    members=[coding_agent, python_agent, shell_agent, file_agent, reasoning_agent, svelte_mcp_agents],
    instructions=[
        "You are the lead developer of a coding team.",
        "Delegate tasks to the most appropriate agent based on the work needed.",
        "If an agent fails or can't complete a task, re-delegate to a different agent.",
        "After any code modification, ensure lint and type checks pass before considering the task complete.",
    ],
    show_members_responses=True,
    markdown=True,
    db=db,
)
