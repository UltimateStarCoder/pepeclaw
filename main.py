from agno.os import AgentOS
from dotenv import load_dotenv

from agents.coding_agents.coding_agent import coding_agent
from agents.coding_agents.file_agent import file_agent
from agents.coding_agents.filegen_agent import filegen_agent
from agents.coding_agents.python_agent import python_agent
from agents.coding_agents.reasoning_agent import reasoning_agent
from agents.coding_agents.shell_agent import shell_agent
from agents.mcp_agents.agno_mcp_agents import agno_mcp_agents
from agents.mcp_agents.clerk_mcp_agents import clerk_mcp_agents
from agents.mcp_agents.convex_mcp_agents import convex_mcp_agents
from agents.mcp_agents.expo_mcp_agents import expo_mcp_agents

load_dotenv()

agent_os = AgentOS(
    description="Pepeclaw AgentOS",
    agents=[
        # Coding agents
        coding_agent,
        python_agent,
        shell_agent,
        file_agent,
        filegen_agent,
        reasoning_agent,
        # MCP agents
        agno_mcp_agents,
        clerk_mcp_agents,
        convex_mcp_agents,
        expo_mcp_agents,
    ],
)

app = agent_os.get_app()

if __name__ == "__main__":
    # Don't use reload=True with MCP tools to avoid lifespan issues
    agent_os.serve(app="main:app")
