from agno.team import Team

from agents.coding_agents.coding_agent import coding_agent
from agents.coding_agents.file_agent import file_agent
from agents.coding_agents.filegen_agent import filegen_agent
from agents.coding_agents.learning_agent import learning_agent
from agents.coding_agents.python_agent import python_agent
from agents.coding_agents.reasoning_agent import reasoning_agent
from agents.coding_agents.shell_agent import shell_agent
from agents.coding_agents.github_agent import github_agent
from config import db, reasoning_model

code_team = Team(
    id="code-team",
    name="Code Team",
    description="A team that builds, debugs, and generates code and files.",
    model=reasoning_model,
    members=[coding_agent, python_agent, shell_agent, file_agent, filegen_agent, reasoning_agent, learning_agent, github_agent],
    instructions=[
        "You are the lead developer of a coding team.",
        "Delegate general code tasks (read, write, edit, shell) to the Coding Agent.",
        "Delegate Python execution to the Python Agent.",
        "Delegate shell commands and system tasks to the Shell Agent.",
        "Delegate file management (read, write, search) to the File Agent.",
        "Delegate file and image generation to the File Generation Agent.",
        "Delegate complex reasoning, debugging, and analysis to the Reasoning Agent.",
        "Use the Learning Agent for tasks that benefit from accumulated project knowledge and user context.",
        "Delegate GitHub operations (repos, issues, PRs, branches) to the GitHub Agent.",
        "After any code modification, ensure lint and type checks pass before considering the task complete.",
    ],
    show_members_responses=True,
    markdown=True,
    db=db,
)
