from agno.agent import Agent
from agno.models.anthropic import Claude
from dotenv import load_dotenv

from config import db, memory_manager
from tools.auth import create_oauth_mcp_tools

load_dotenv()

expo_mcp_tools = create_oauth_mcp_tools(
    url="https://mcp.expo.dev/mcp",
    cache_key="expo",
    client_name="Pepeclaw",
)

expo_mcp_agents = Agent(
    id="expo-agent",
    name="Expo Agent",
    model=Claude(id="claude-sonnet-4-5"),
    instructions=["You are a helpful Expo MCP agent assistant."],
    tools=[expo_mcp_tools],
    db=db,
    memory_manager=memory_manager,
    enable_agentic_memory=True,
    add_history_to_context=True,
    update_memory_on_run=True,
    markdown=True,
)
