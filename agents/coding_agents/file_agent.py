from agno.agent import Agent
from agno.tools.file import FileTools

from config import db, default_model, memory_manager
file_agent = Agent(
    id="file-agent",
    name="File Agent",
    model=default_model,
    instructions=[
        "You are a file management assistant. Read, write, search, and organize files.",
        "After saving files, verify the content was written correctly by reading it back.",
    ],
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
