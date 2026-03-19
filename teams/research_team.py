from agno.team import Team

from agents.coding_agents.learning_agent import learning_agent
from agents.coding_agents.calculator_agent import calculator_agent
from agents.coding_agents.reasoning_agent import reasoning_agent
from agents.mcp_agents.agno_mcp_agents import agno_mcp_agents
from config import db, reasoning_model

research_team = Team(
    id="research-team",
    name="Research Team",
    description="A team for deep analysis, knowledge synthesis, and learning.",
    model=reasoning_model,
    members=[learning_agent, reasoning_agent, calculator_agent, agno_mcp_agents],
    instructions=[
        "You are the lead of a research and analysis team.",
        "Delegate deep analysis and structured thinking to the Reasoning Agent.",
        "Use the Learning Agent for tasks that benefit from accumulated knowledge and user context.",
        "Use the Agno Agent for Agno framework documentation and best practices.",
        "Delegate math calculations and numerical analysis to the Calculator Agent.",
        "Synthesize findings from multiple agents into clear, actionable insights.",
    ],
    show_members_responses=True,
    markdown=True,
    db=db,
)
