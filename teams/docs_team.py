from agno.team import Team

from config import db, reasoning_model
from agents.mcp_agents.agno_mcp_agents import agno_mcp_agents
from agents.mcp_agents.clerk_mcp_agents import clerk_mcp_agents
from agents.mcp_agents.convex_auth_mcp_agents import convex_auth_mcp_agents
from agents.mcp_agents.livekit_mcp_agents import livekit_mcp_agents
from agents.mcp_agents.svelte_mcp_agents import svelte_mcp_agents

docs_team = Team(
    id="docs-team",
    name="Docs Team",
    description="A team that looks up documentation and answers questions.",
    model=reasoning_model,
    members=[agno_mcp_agents, clerk_mcp_agents, convex_auth_mcp_agents, livekit_mcp_agents, svelte_mcp_agents],
    instructions=[
        "You are the lead of a documentation research team.",
        "Delegate Agno framework questions to the Agno Agent.",
        "Delegate Clerk auth questions to the Clerk Agent.",
        "Delegate Convex Auth questions to the Convex Auth Agent.",
        "Delegate LiveKit real-time voice, video, and agents questions to the LiveKit Agent.",
        "Delegate Svelte and SvelteKit questions to the Svelte Agent.",
    ],
    show_members_responses=True,
    markdown=True,
    db=db,
)
