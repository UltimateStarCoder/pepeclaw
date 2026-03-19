from agno.agent import Agent
from agno.tools.mcp import MCPTools

from config import db, default_model, learning_machine

livekit_mcp_tools = MCPTools(
    transport="streamable-http",
    url="https://docs.livekit.io/mcp",
    add_instructions=True,
)

livekit_mcp_agents = Agent(
    id="livekit-agent",
    name="LiveKit Agent",
    model=default_model,
    instructions=["You are a helpful LiveKit MCP agent assistant."],
    tools=[livekit_mcp_tools],
    db=db,
    learning=learning_machine,
    add_history_to_context=True,
    add_learnings_to_context=True,
    markdown=True,
)
