from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools.mcp import MCPTools
from dotenv import load_dotenv

load_dotenv()

clerk_mcp_tools = MCPTools(
    transport="streamable-http",
    url="https://mcp.clerk.com/mcp",
    add_instructions=True,
)

clerk_mcp_agents = Agent(
    id="clerk-agent",
    name="Clerk Agent",
    model=Claude(id="claude-sonnet-4-5"),
    instructions=["You are a helpful Clerk MCP agent assistant."],
    tools=[clerk_mcp_tools],
    markdown=True,
)
