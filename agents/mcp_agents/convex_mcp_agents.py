from agno.agent import Agent
from agno.tools.mcp import MCPTools

from config import db, default_model, learning_machine
convex_mcp_tools = MCPTools(
    command="npx -y convex@latest mcp start --project-dir .",
    timeout_seconds=60,
    add_instructions=True,
)

convex_mcp_agents = Agent(
    id="convex-agent",
    name="Convex Agent",
    model=default_model,
    instructions=["You are a helpful Convex MCP agent assistant."],
    tools=[convex_mcp_tools],
    db=db,
    learning=learning_machine,
    add_history_to_context=True,
    add_learnings_to_context=True,
    markdown=True,
)
