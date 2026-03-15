from agno.agent import Agent
from agno.os import AgentOS
from agno.tools.mcp import MCPTools
from dotenv import load_dotenv

load_dotenv()

# Create an MCPTools instance
mcp_tools = MCPTools(
    transport="streamable-http",
    url="https://docs.agno.com/mcp"
)

# Create an MCP-enabled agent
agno_mcp_agents = Agent(
    id="agno-agent",
    name="Agno Agent",
    tools=[mcp_tools],
)


if __name__ == "__main__":
    # AgentOS manages MCP lifespan
    agent_os = AgentOS(
        description="AgentOS with MCP Tools",
        agents=[agno_mcp_agents],
    )

    app = agent_os.get_app()
    # Don't use reload=True with MCP tools to avoid lifespan issues
    agent_os.serve(app="mcp_tools_example:app")