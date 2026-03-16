from agno.agent import Agent
from agno.models.anthropic import Claude
from dotenv import load_dotenv

from tools.auth import create_oauth_mcp_tools

load_dotenv()

stripe_mcp_tools = create_oauth_mcp_tools(
    url="https://mcp.stripe.com",
    cache_key="stripe",
    client_name="Pepeclaw",
)

stripe_mcp_agents = Agent(
    id="stripe-agent",
    name="Stripe Agent",
    model=Claude(id="claude-sonnet-4-5"),
    instructions=["You are a helpful Stripe MCP agent assistant."],
    tools=[stripe_mcp_tools],
    markdown=True,
)
