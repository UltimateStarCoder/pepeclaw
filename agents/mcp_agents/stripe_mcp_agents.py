from agno.agent import Agent
from agno.models.anthropic import Claude
from dotenv import load_dotenv

from tools.auth import create_static_mcp_tools

load_dotenv()

stripe_mcp_tools = create_static_mcp_tools(
    url="https://mcp.stripe.com",
    token_env_var="STRIPE_SECRET_KEY",
)

stripe_mcp_agents = Agent(
    id="stripe-agent",
    name="Stripe Agent",
    model=Claude(id="claude-sonnet-4-5"),
    instructions=[
        "You are a Stripe operations assistant.",
        "Create and manage Stripe objects like customers, products, prices, and payment links.",
        "Execute steps sequentially if a request involves multiple actions.",
    ],
    tools=[stripe_mcp_tools],
    markdown=True,
)
