from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.os import AgentOS
from dotenv import load_dotenv

from tools import create_oauth_mcp_tools

load_dotenv()

# Expo MCP requires OAuth — authenticates via browser on first use,
# then caches token to ~/.pepeclaw/tokens/expo/
expo_mcp_tools = create_oauth_mcp_tools(
    url="https://mcp.expo.dev/mcp",
    cache_key="expo",
    client_name="Pepeclaw",
)

# Create an Expo MCP-enabled agent
expo_mcp_agents = Agent(
    id="expo-agent",
    name="Expo Agent",
    model=Claude(id="claude-sonnet-4-5"),
    instructions=["You are a helpful Expo MCP agent assistant."],
    tools=[expo_mcp_tools],
    markdown=True,
)


if __name__ == "__main__":
    # AgentOS manages MCP lifespan
    agent_os = AgentOS(
        description="AgentOS with Expo MCP Tools",
        agents=[expo_mcp_agents],
    )

    app = agent_os.get_app()
    # Don't use reload=True with MCP tools to avoid lifespan issues
    agent_os.serve(app=app)
