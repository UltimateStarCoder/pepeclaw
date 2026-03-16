from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools.file import FileTools
from dotenv import load_dotenv

from config import db, memory_manager

load_dotenv()

file_agent = Agent(
    id="file-agent",
    name="File Agent",
    model=Claude(id="claude-sonnet-4-5"),
    instructions=["You are a file management assistant. Read, write, search, and organize files."],
    tools=[
        FileTools(
            enable_read_file=True,
            enable_read_file_chunk=True,
            enable_save_file=True,
            enable_search_files=True,
            enable_list_files=True,
        ),
    ],
    db=db,
    memory_manager=memory_manager,
    enable_agentic_memory=True,
    add_history_to_context=True,
    update_memory_on_run=True,
    markdown=True,
)
