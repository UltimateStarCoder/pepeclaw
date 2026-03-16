from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools.mcp import MCPTools
from dotenv import load_dotenv

load_dotenv()

convex_mcp_tools = MCPTools(
    command="npx -y convex@latest mcp start",
    add_instructions=True,
)

convex_mcp_agents = Agent(
    id="convex-agent",
    name="Convex Agent",
    model=Claude(id="claude-sonnet-4-5"),
    instructions=["You are a helpful Convex MCP agent assistant."],
    tools=[convex_mcp_tools],
    markdown=True,
)
