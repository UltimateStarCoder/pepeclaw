from agno.models.anthropic import Claude
from agno.team import Team

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
from agents.mcp_agents.stripe_mcp_agents import stripe_mcp_agents

fullstack_team = Team(
    id="fullstack-team",
    name="Full Stack Team",
    description="A team of all agents orchestrated to handle any task.",
    model=Claude(id="claude-sonnet-4-5"),
    members=[
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
        stripe_mcp_agents,
    ],
    instructions=[
        "You are the lead architect of a full stack team.",
        "Delegate coding tasks to the appropriate coding agent.",
        "Delegate documentation lookups to the Agno or Clerk agent.",
        "Delegate deployments to the Expo or Convex agent.",
        "Delegate payments to the Stripe agent.",
        "Use the Reasoning Agent for planning and complex problem solving.",
        "Use the File Generation Agent for creating reports and documents.",
    ],
    show_members_responses=True,
    markdown=True,
)
