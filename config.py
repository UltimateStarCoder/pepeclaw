from agno.db.sqlite import SqliteDb
from agno.memory import MemoryManager
from agno.models.anthropic import Claude
from agno.models.google import Gemini
from agno.models.openai import OpenAIResponses

db = SqliteDb(db_file="tmp/pepeclaw.db")

# Vertex AI config — set these env vars:
#   GOOGLE_GENAI_USE_VERTEXAI=true
#   GOOGLE_CLOUD_PROJECT=your-project-id
#   GOOGLE_CLOUD_LOCATION=us-central1
VERTEXAI = True

# Task-specific models
# ─────────────────────────────────────────────────────────────────
# Anthropic (ANTHROPIC_API_KEY)
#   Opus 4.6:   complex reasoning, large codebases, deep analysis
#   Sonnet 4.5: fast workhorse for day-to-day coding and general tasks
#   Haiku 4.5:  fastest, cheapest — simple tasks and high-volume
# OpenAI (OPENAI_API_KEY)
#   GPT-5.2:    slow but careful, large codebases, minimal-regret edits
#   GPT-4o:     fast, multimodal, balanced
#   GPT-4o Mini: cheapest OpenAI, good for simple tasks
# Google Vertex AI (GOOGLE_CLOUD_PROJECT)
#   Gemini 3.1 Pro:        reasoning, agentic workflows, 1M context
#   Gemini 3 Flash:        multimodal, coding, strong reasoning
#   Gemini 2.5 Flash:      balanced speed/intelligence, general purpose
#   Gemini 2.5 Flash-Lite: cheapest, high-volume tasks
#   Gemini Flash Image:    image generation, conversational editing
# ─────────────────────────────────────────────────────────────────

# Anthropic models
claude_opus = Claude(id="claude-opus-4-6")
claude_sonnet = Claude(id="claude-sonnet-4-5")
claude_haiku = Claude(id="claude-haiku-4-5-20251001")

# OpenAI models
gpt_5 = OpenAIResponses(id="gpt-5.2")
gpt_4o = OpenAIResponses(id="gpt-4o")
gpt_4o_mini = OpenAIResponses(id="gpt-4o-mini")

# Google Vertex AI models
gemini_pro = Gemini(id="gemini-3.1-pro", vertexai=VERTEXAI)
gemini_flash = Gemini(id="gemini-3-flash-preview", vertexai=VERTEXAI)
gemini_fast = Gemini(id="gemini-2.5-flash", vertexai=VERTEXAI)
gemini_lite = Gemini(id="gemini-2.5-flash-lite", vertexai=VERTEXAI)
gemini_image = Gemini(
    id="gemini-2.5-flash-image",
    vertexai=VERTEXAI,
    response_modalities=["Text", "Image"],
)

# Role assignments
# ─────────────────────────────────────────────────────────────────
default_model = claude_sonnet       # Day-to-day coding agents
reasoning_model = claude_opus       # Reasoning agent, team leaders
fast_model = gemini_lite            # Memory manager (high volume, cheap)
flash_model = gemini_fast           # File generation, simple tasks
image_model = gemini_image          # Image generation

memory_manager = MemoryManager(
    model=fast_model,
    db=db,
)
