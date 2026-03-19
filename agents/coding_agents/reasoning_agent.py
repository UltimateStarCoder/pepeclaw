from agno.agent import Agent
from agno.tools.reasoning import ReasoningTools

from config import db, learning_machine, reasoning_model
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
    learning=learning_machine,
    add_history_to_context=True,
    add_learnings_to_context=True,
    markdown=True,
)
