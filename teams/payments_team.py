from agno.models.anthropic import Claude
from agno.team import Team

from agents.coding_agents.filegen_agent import filegen_agent
from config import db
from agents.mcp_agents.stripe_mcp_agents import stripe_mcp_agents

payments_team = Team(
    id="payments-team",
    name="Payments Team",
    description="A team that handles Stripe operations and generates reports.",
    model=Claude(id="claude-sonnet-4-5"),
    members=[stripe_mcp_agents, filegen_agent],
    instructions=[
        "You are the lead of a payments and billing team.",
        "Delegate Stripe operations to the Stripe Agent.",
        "Delegate report and invoice generation to the File Generation Agent.",
    ],
    show_members_responses=True,
    markdown=True,
    db=db,
)