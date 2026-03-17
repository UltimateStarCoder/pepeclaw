from agno.agent import Agent
from agno.tools.mcp import MCPTools

from config import db, default_model, memory_manager

svelte_mcp_tools = MCPTools(
    transport="streamable-http",
    url="https://mcp.svelte.dev/mcp",
    add_instructions=True,
)

svelte_mcp_agents = Agent(
    id="svelte-agent",
    name="Svelte Agent",
    model=default_model,
    instructions=["You are a helpful Svelte MCP agent assistant."],
    tools=[svelte_mcp_tools],
    db=db,
    memory_manager=memory_manager,
    enable_agentic_memory=True,
    add_history_to_context=True,
    update_memory_on_run=True,
    markdown=True,
)
