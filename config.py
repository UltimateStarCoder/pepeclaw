from agno.db.sqlite import SqliteDb
from agno.memory import MemoryManager
from agno.models.anthropic import Claude

db = SqliteDb(db_file="tmp/pepeclaw.db")

memory_manager = MemoryManager(
    model=Claude(id="claude-sonnet-4-5"),
    db=db,
)
