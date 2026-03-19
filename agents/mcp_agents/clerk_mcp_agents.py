from agno.agent import Agent
from agno.tools.mcp import MCPTools

from config import db, default_model, learning_machine
clerk_mcp_tools = MCPTools(
    transport="streamable-http",
    url="https://mcp.clerk.com/mcp",
    add_instructions=True,
)

clerk_mcp_agents = Agent(
    id="clerk-agent",
    name="Clerk Agent",
    model=default_model,
    instructions=["You are a helpful Clerk MCP agent assistant."],
    tools=[clerk_mcp_tools],
    db=db,
    learning=learning_machine,
    add_history_to_context=True,
    add_learnings_to_context=True,
    markdown=True,
)
