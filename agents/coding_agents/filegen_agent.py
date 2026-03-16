from pathlib import Path

from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools.file_generation import FileGenerationTools
from dotenv import load_dotenv

load_dotenv()

filegen_agent = Agent(
    id="filegen-agent",
    name="File Generation Agent",
    model=Claude(id="claude-sonnet-4-5"),
    instructions=[
        "You are a file generation assistant.",
        "Create files in various formats when requested.",
        "Provide meaningful content and appropriate filenames.",
    ],
    tools=[FileGenerationTools(output_directory=Path("tmp/generated"))],
    markdown=True,
)
