from agno.team import Team

from agents.coding_agents.docker_agent import docker_agent
from agents.coding_agents.shell_agent import shell_agent
from config import db, reasoning_model
from agents.mcp_agents.convex_mcp_agents import convex_mcp_agents
from agents.mcp_agents.expo_mcp_agents import expo_mcp_agents

deploy_team = Team(
    id="deploy-team",
    name="Deploy Team",
    description="A team that deploys and manages applications.",
    model=reasoning_model,
    members=[shell_agent, docker_agent, expo_mcp_agents, convex_mcp_agents],
    instructions=[
        "You are the lead of a deployment team.",
        "Delegate Expo/React Native tasks to the Expo Agent.",
        "Delegate Convex backend tasks to the Convex Agent.",
        "Delegate Docker container management to the Docker Agent.",
        "Use the Shell Agent for running deploy scripts and system commands.",
    ],
    show_members_responses=True,
    markdown=True,
    db=db,
)