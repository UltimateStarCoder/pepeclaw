from agno.agent import Agent
from agno.tools.mcp import MCPTools

from config import db, default_model, memory_manager

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
    memory_manager=memory_manager,
    enable_agentic_memory=True,
    add_history_to_context=True,
    update_memory_on_run=True,
    markdown=True,
)
