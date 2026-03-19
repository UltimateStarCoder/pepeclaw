from pathlib import Path

from agno.agent import Agent
from agno.tools.file_generation import FileGenerationTools

from config import db, image_model, learning_machine
filegen_agent = Agent(
    id="filegen-agent",
    name="File Generation Agent",
    model=image_model,
    instructions=[
        "You are a file generation assistant.",
        "Create files in various formats when requested.",
        "Provide meaningful content and appropriate filenames.",
    ],
    tools=[FileGenerationTools(output_directory=Path("tmp/generated"))],
    db=db,
    learning=learning_machine,
    add_history_to_context=True,
    add_learnings_to_context=True,
    markdown=True,
)
