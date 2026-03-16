from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools.coding import CodingTools
from dotenv import load_dotenv

load_dotenv()

coding_agent = Agent(
    id="coding-agent",
    name="Coding Agent",
    model=Claude(id="claude-sonnet-4-5"),
    instructions=["You are a coding assistant. Read, write, edit files and run shell commands to solve coding tasks."],
    tools=[CodingTools()],
    markdown=True,
)
