from agno.agent import Agent
from agno.tools.mcp import MCPTools

from config import db, default_model, memory_manager
agno_mcp_tools = MCPTools(
    transport="streamable-http",
    url="https://docs.agno.com/mcp",
    add_instructions=True,
)

agno_mcp_agents = Agent(
    id="agno-agent",
    name="Agno Agent",
    model=default_model,
    instructions=["You are a helpful agno mcp agent assistant."],
    tools=[agno_mcp_tools],
    db=db,
    memory_manager=memory_manager,
    enable_agentic_memory=True,
    add_history_to_context=True,
    update_memory_on_run=True,
    markdown=True,
)
