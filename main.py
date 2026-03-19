from agno.os import AgentOS

from agents.coding_agents.coding_agent import coding_agent
from agents.coding_agents.file_agent import file_agent
from agents.coding_agents.filegen_agent import filegen_agent
from agents.coding_agents.python_agent import python_agent
from agents.coding_agents.reasoning_agent import reasoning_agent
from agents.coding_agents.learning_agent import learning_agent
from agents.coding_agents.shell_agent import shell_agent
from agents.coding_agents.github_agent import github_agent
from agents.coding_agents.calculator_agent import calculator_agent
from agents.coding_agents.docker_agent import docker_agent
from agents.mcp_agents.agno_mcp_agents import agno_mcp_agents
from agents.mcp_agents.clerk_mcp_agents import clerk_mcp_agents
from agents.mcp_agents.convex_mcp_agents import convex_mcp_agents
from agents.mcp_agents.convex_auth_mcp_agents import convex_auth_mcp_agents
from agents.mcp_agents.expo_mcp_agents import expo_mcp_agents
from agents.mcp_agents.livekit_mcp_agents import livekit_mcp_agents
from agents.mcp_agents.svelte_mcp_agents import svelte_mcp_agents
from agents.mcp_agents.stripe_mcp_agents import stripe_mcp_agents
from teams.deploy_team import deploy_team
from teams.code_team import code_team
from teams.docs_team import docs_team
from teams.fullstack_team import fullstack_team
from teams.payments_team import payments_team
from teams.research_team import research_team
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
        learning_agent,
        github_agent,
        calculator_agent,
        docker_agent,
        # MCP agents
        agno_mcp_agents,
        clerk_mcp_agents,
        convex_mcp_agents,
        convex_auth_mcp_agents,
        expo_mcp_agents,
        livekit_mcp_agents,
        svelte_mcp_agents,
        stripe_mcp_agents,
    ],
    teams=[
        code_team,
        docs_team,
        deploy_team,
        payments_team,
        research_team,
        fullstack_team,
    ],
)

app = agent_os.get_app()

if __name__ == "__main__":
    # Don't use reload=True with MCP tools to avoid lifespan issues
    agent_os.serve(app="main:app")
