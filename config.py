from agno.db.sqlite import SqliteDb
from agno.memory import MemoryManager
from agno.models.anthropic import Claude
from agno.models.google import Gemini

db = SqliteDb(db_file="tmp/pepeclaw.db")

# Task-specific models
# ────────────────────────────────────────────────
# Anthropic
#   Opus 4.6:   complex reasoning, large codebases, deep analysis
#   Sonnet 4.5: fast workhorse for day-to-day coding and general tasks
#   Haiku 4.5:  fastest, cheapest — simple tasks and high-volume processing
# Google
#   Gemini Flash: fast, cheap, good for file generation and simple tasks
# ────────────────────────────────────────────────
default_model = Claude(id="claude-sonnet-4-5")
reasoning_model = Claude(id="claude-opus-4-6")
fast_model = Claude(id="claude-haiku-4-5-20251001")
flash_model = Gemini(id="gemini-2.0-flash")

memory_manager = MemoryManager(
    model=fast_model,
    db=db,
)