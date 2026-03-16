from agno.team import Team

from agents.coding_agents.filegen_agent import filegen_agent
from config import db, reasoning_model
from agents.mcp_agents.stripe_mcp_agents import stripe_mcp_agents

payments_team = Team(
    id="payments-team",
    name="Payments Team",
    description="A team that handles Stripe operations and generates reports.",
    model=reasoning_model,
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