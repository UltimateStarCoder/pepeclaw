from agno.agent import Agent

from config import db, default_model, learning_machine
from tools.auth import create_oauth_mcp_tools
stripe_mcp_tools = create_oauth_mcp_tools(
    url="https://mcp.stripe.com",
    cache_key="stripe",
    client_name="Pepeclaw",
)

stripe_mcp_agents = Agent(
    id="stripe-agent",
    name="Stripe Agent",
    model=default_model,
    instructions=["You are a helpful Stripe MCP agent assistant."],
    tools=[stripe_mcp_tools],
    db=db,
    learning=learning_machine,
    add_history_to_context=True,
    add_learnings_to_context=True,
    markdown=True,
)
