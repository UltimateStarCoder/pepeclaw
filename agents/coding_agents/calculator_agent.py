from agno.agent import Agent
from agno.tools.calculator import CalculatorTools

from config import db, default_model, learning_machine

calculator_agent = Agent(
    id="calculator-agent",
    name="Calculator Agent",
    model=default_model,
    instructions=[
        "You are a math assistant. Perform calculations, conversions, and numerical analysis.",
        "Show your work step-by-step. Use the calculator tools for precision.",
    ],
    tools=[CalculatorTools()],
    db=db,
    learning=learning_machine,
    add_history_to_context=True,
    add_learnings_to_context=True,
    markdown=True,
)
