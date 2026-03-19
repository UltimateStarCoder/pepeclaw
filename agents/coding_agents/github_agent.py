import subprocess

from agno.agent import Agent
from agno.tools.github import GithubTools

from config import db, default_model, learning_machine


def _get_gh_token() -> str:
    """Get GitHub token from gh CLI auth (no env var needed)."""
    try:
        result = subprocess.run(
            ["gh", "auth", "token"], capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return ""


_gh_token = _get_gh_token()

try:
    github_tools = GithubTools(access_token=_gh_token) if _gh_token else None
except (ValueError, Exception):
    github_tools = None

github_agent = Agent(
    id="github-agent",
    name="GitHub Agent",
    model=default_model,
    instructions=[
        "You are a GitHub assistant. Manage repositories, issues, pull requests, and branches.",
        "When creating issues or PRs, write clear titles and descriptions.",
        "When reviewing PRs, examine the changes and provide constructive feedback.",
        "If GitHub tools are unavailable, tell the user to run: pepeclaw auth login github",
    ],
    tools=[github_tools] if github_tools else [],
    db=db,
    learning=learning_machine,
    add_history_to_context=True,
    add_learnings_to_context=True,
    markdown=True,
)
