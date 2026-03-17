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
        "Delegate coding tasks to the Coding Agent for general file ops and shell commands.",
        "Delegate Python execution to the Python Agent.",
        "Delegate shell commands to the Shell Agent.",
        "Delegate file read/write/search to the File Agent.",
        "Use the Reasoning Agent for debugging and complex problem analysis.",
        "Delegate Svelte and SvelteKit code analysis, autofixing, and playground links to the Svelte Agent.",
    ],
    show_members_responses=True,
    markdown=True,
    db=db,
)
