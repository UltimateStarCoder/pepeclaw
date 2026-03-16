from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools.shell import ShellTools
from dotenv import load_dotenv

load_dotenv()

shell_agent = Agent(
    id="shell-agent",
    name="Shell Agent",
    model=Claude(id="claude-sonnet-4-5"),
    instructions=["You are a shell command assistant. Execute shell commands to help with system tasks."],
    tools=[ShellTools()],
    markdown=True,
)
