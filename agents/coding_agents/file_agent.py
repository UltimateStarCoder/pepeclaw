from agno.agent import Agent
from agno.tools.file import FileTools

from config import db, default_model, learning_machine
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
    learning=learning_machine,
    add_history_to_context=True,
    add_learnings_to_context=True,
    markdown=True,
)
