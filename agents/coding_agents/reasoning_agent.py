from agno.agent import Agent
from agno.tools.reasoning import ReasoningTools
from dotenv import load_dotenv

from config import db, memory_manager, reasoning_model

load_dotenv()

reasoning_agent = Agent(
    id="reasoning-agent",
    name="Reasoning Agent",
    model=reasoning_model,
    instructions=[
        "You are a reasoning and debugging assistant.",
        "Break down complex problems into steps.",
        "State assumptions, evaluate evidence, and draw well-justified conclusions.",
    ],
    tools=[
        ReasoningTools(
            enable_think=True,
            enable_analyze=True,
            add_instructions=True,
            add_few_shot=True,
        ),
    ],
    db=db,
    memory_manager=memory_manager,
    enable_agentic_memory=True,
    add_history_to_context=True,
    update_memory_on_run=True,
    markdown=True,
)
