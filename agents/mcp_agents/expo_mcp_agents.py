from agno.agent import Agent
from agno.models.anthropic import Claude
from dotenv import load_dotenv

from tools import create_oauth_mcp_tools

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
    markdown=True,
)
