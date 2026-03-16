from pathlib import Path

from agno.agent import Agent
from agno.tools.file_generation import FileGenerationTools
from dotenv import load_dotenv

from config import db, image_model, memory_manager

load_dotenv()

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
    memory_manager=memory_manager,
    enable_agentic_memory=True,
    add_history_to_context=True,
    update_memory_on_run=True,
    markdown=True,
)
