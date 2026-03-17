from agno.team import Team

from agents.coding_agents.reasoning_agent import reasoning_agent
from config import db, reasoning_model
from agents.mcp_agents.agno_mcp_agents import agno_mcp_agents
from agents.mcp_agents.clerk_mcp_agents import clerk_mcp_agents
from agents.mcp_agents.livekit_mcp_agents import livekit_mcp_agents

docs_team = Team(
    id="docs-team",
    name="Docs Team",
    description="A team that looks up documentation and answers questions.",
    model=reasoning_model,
    members=[agno_mcp_agents, clerk_mcp_agents, livekit_mcp_agents, reasoning_agent],
    instructions=[
        "You are the lead of a documentation research team.",
        "Delegate Agno framework questions to the Agno Agent.",
        "Delegate Clerk auth questions to the Clerk Agent.",
        "Delegate LiveKit real-time voice, video, and agents questions to the LiveKit Agent.",
        "Use the Reasoning Agent to analyze and synthesize findings.",
    ],
    show_members_responses=True,
    markdown=True,
    db=db,
)
