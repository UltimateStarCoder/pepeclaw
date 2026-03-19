from agno.agent import Agent

from config import db, default_model, learning_machine
from tools.auth import create_oauth_mcp_tools
expo_mcp_tools = create_oauth_mcp_tools(
    url="https://mcp.expo.dev/mcp",
    cache_key="expo",
    client_name="Pepeclaw",
)

expo_mcp_agents = Agent(
    id="expo-agent",
    name="Expo Agent",
    model=default_model,
    instructions=["You are a helpful Expo MCP agent assistant."],
    tools=[expo_mcp_tools],
    db=db,
    learning=learning_machine,
    add_history_to_context=True,
    add_learnings_to_context=True,
    markdown=True,
)
