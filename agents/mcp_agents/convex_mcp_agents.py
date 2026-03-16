from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools.mcp import MCPTools
from dotenv import load_dotenv

from config import db, memory_manager

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
    db=db,
    memory_manager=memory_manager,
    enable_agentic_memory=True,
    add_history_to_context=True,
    update_memory_on_run=True,
    markdown=True,
)
