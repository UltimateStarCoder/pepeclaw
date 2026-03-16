from agno.agent import Agent
from agno.models.anthropic import Claude
from dotenv import load_dotenv

from config import db, memory_manager
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
    db=db,
    memory_manager=memory_manager,
    enable_agentic_memory=True,
    add_history_to_context=True,
    update_memory_on_run=True,
    markdown=True,
)
