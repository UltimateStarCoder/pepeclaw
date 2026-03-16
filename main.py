from agno.os import AgentOS
from dotenv import load_dotenv

from agents.mcp_agents.agno_mcp_agents import agno_mcp_agents
from agents.mcp_agents.expo_mcp_agents import expo_mcp_agents

load_dotenv()


def main():
    agent_os = AgentOS(
        description="Pepeclaw AgentOS",
        agents=[agno_mcp_agents, expo_mcp_agents],
    )

    app = agent_os.get_app()
    # Don't use reload=True with MCP tools to avoid lifespan issues
    agent_os.serve(app=app)


if __name__ == "__main__":
    main()
