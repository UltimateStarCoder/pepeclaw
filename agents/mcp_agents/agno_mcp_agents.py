from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools.mcp import MCPTools
from dotenv import load_dotenv

load_dotenv()

agno_mcp_tools = MCPTools(
    transport="streamable-http",
    url="https://docs.agno.com/mcp",
    add_instructions=True,
)

agno_mcp_agents = Agent(
    id="agno-agent",
    name="Agno Agent",
    model=Claude(id="claude-sonnet-4-5"),
    instructions=["You are a helpful agno mcp agent assistant."],
    tools=[agno_mcp_tools],
    markdown=True,
)