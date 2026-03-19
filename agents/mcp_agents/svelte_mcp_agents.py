from agno.agent import Agent
from agno.tools.mcp import MCPTools

from config import db, default_model, learning_machine

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
    learning=learning_machine,
    add_history_to_context=True,
    add_learnings_to_context=True,
    markdown=True,
)
