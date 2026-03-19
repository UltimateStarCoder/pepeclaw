# pepeclaw

Multi-agent system built with [Agno](https://github.com/agno-agi/agno) and MCP (Model Context Protocol).

18 agents, 6 teams, 3 auth methods, 3 AI providers, Learning Machine, and a CLI.

## Project Structure

```text
pepeclaw/
├── agents/
│   ├── coding_agents/
│   │   ├── coding_agent.py         # All-in-one: file ops, shell, grep, find
│   │   ├── python_agent.py         # Write & execute Python
│   │   ├── shell_agent.py          # Shell commands
│   │   ├── file_agent.py           # Read, write, search files
│   │   ├── filegen_agent.py        # Generate files & images
│   │   ├── reasoning_agent.py      # Structured thinking & debugging
│   │   ├── learning_agent.py       # Adaptive learning with full Learning Machine
│   │   ├── github_agent.py         # GitHub repos, issues, PRs, branches
│   │   ├── calculator_agent.py     # Math operations & numerical analysis
│   │   └── docker_agent.py         # Docker container management
│   └── mcp_agents/
│       ├── agno_mcp_agents.py      # Agno docs (public, no auth)
│       ├── clerk_mcp_agents.py     # Clerk auth (public, no auth)
│       ├── convex_mcp_agents.py    # Convex backend (stdio)
│       ├── convex_auth_mcp_agents.py # Convex Auth specialist (stdio)
│       ├── expo_mcp_agents.py      # Expo (OAuth)
│       ├── livekit_mcp_agents.py   # LiveKit docs (public, no auth)
│       ├── svelte_mcp_agents.py    # Svelte/SvelteKit docs (public, no auth)
│       └── stripe_mcp_agents.py    # Stripe (OAuth + refresh tokens)
├── teams/
│   ├── code_team.py                # Coding, Python, Shell, File, Filegen, Reasoning, Learning, GitHub
│   ├── docs_team.py                # Agno, Clerk, Convex Auth, LiveKit, Svelte
│   ├── deploy_team.py              # Shell, Docker, Expo, Convex
│   ├── payments_team.py            # Stripe, File Generation
│   ├── research_team.py            # Learning, Reasoning, Calculator, Agno
│   └── fullstack_team.py           # Code, Docs, Deploy, Payments, Research sub-teams
├── tools/
│   └── auth/
│       ├── static.py               # Static auth — env var token
│       ├── dynamic.py              # Dynamic auth — per-request tokens
│       └── oauth.py                # OAuth — browser flow + refresh tokens + caching
├── config.py                       # Models, database, Learning Machine
├── cli.py                          # CLI entry point (uses Agno's built-in acli_app)
├── main.py                         # AgentOS server
├── pyproject.toml
└── .env                            # API keys (not committed)
```

## Installation

### From GitHub

```bash
uv pip install git+https://github.com/UltimateStarCoder/pepeclaw.git
```

### From source

```bash
git clone https://github.com/UltimateStarCoder/pepeclaw.git
cd pepeclaw
uv sync
```

### Global CLI

Install pepeclaw as a global command available in any terminal:

```bash
# Editable — links to source, changes take effect immediately (recommended for development)
uv tool install --editable .

# Standard — snapshot copy, stable but needs reinstall after source changes
uv tool install .
```

This adds `pepeclaw` to your PATH (`~/.local/bin/`). Run `pepeclaw` from any directory.

To uninstall:

```bash
uv tool uninstall pepeclaw
```

## Setup

```bash
# Generate config file with API key template
pepeclaw init
```

This creates `~/.pepeclaw/.env` — edit it to add your API keys. This file is loaded automatically so you can run `pepeclaw` from anywhere.

### Environment Variables

pepeclaw looks for API keys in this order:

1. **Local `.env`** — in the current working directory
2. **Global `~/.pepeclaw/.env`** — created by `pepeclaw init`
3. **Shell environment** — exported variables

```env
# Required
ANTHROPIC_API_KEY=sk-ant-...

# Optional — enable more models and services
OPENAI_API_KEY=sk-...

# Google Vertex AI (for Gemini models)
# GOOGLE_GENAI_USE_VERTEXAI=true
# GOOGLE_CLOUD_PROJECT=your-project-id
# GOOGLE_CLOUD_LOCATION=us-central1
```

## CLI

```bash
# First-time setup
pepeclaw init

# Start AgentOS server
pepeclaw serve
pepeclaw serve --port 8000

# List all agents and teams
pepeclaw list

# Chat with an agent or team
pepeclaw chat coding
pepeclaw chat fullstack
pepeclaw chat stripe --user-id me
pepeclaw chat fullstack --session <id>  # Resume a previous session
pepeclaw chat coding --no-stream        # Disable streaming
pepeclaw chat coding --no-markdown      # Disable markdown formatting

# Manage chat sessions
pepeclaw sessions list
pepeclaw sessions list --user-id me
pepeclaw sessions clear <session-id>
pepeclaw sessions clear --all

# Manage authentication
pepeclaw auth login expo       # OAuth browser flow
pepeclaw auth login stripe     # OAuth browser flow
pepeclaw auth login github     # GitHub CLI auth (gh auth login)
pepeclaw auth status
pepeclaw auth clear
pepeclaw auth clear expo

# Reset data
pepeclaw reset --learning       # Clear learning data only (profiles, memory, entities, decisions)
pepeclaw reset --sessions       # Clear chat sessions only
pepeclaw reset --tokens         # Clear OAuth tokens
pepeclaw reset --generated      # Clear generated files
pepeclaw reset --db             # Delete entire database (learning + sessions + everything)
pepeclaw reset --all            # Clear everything (db + tokens + generated)
```

## Teams

```text
fullstack
├── code:     coding, python, shell, file, filegen, reasoning, learning, github
├── docs:     agno, clerk, convex-auth, livekit, svelte
├── deploy:   shell, docker, expo, convex
├── payments: stripe, filegen
└── research: learning, reasoning, calculator, agno
```

## Models

All models are configured in `config.py`. Change a role assignment once, and every agent using that role updates automatically.

| Role | Model | Used by |
| ---- | ----- | ------- |
| `default_model` | Claude Sonnet 4.6 | All coding and MCP agents |
| `reasoning_model` | Claude Opus 4.6 | Reasoning Agent, all team leaders |
| `fast_model` | GPT-5 Nano | Learning Machine extraction (high volume, cheap) |
| `image_model` | Gemini 2.5 Flash Image | File Generation Agent |

Additional models available in config: Claude Haiku, GPT-5.4, GPT-5.4 Pro, GPT-5 Mini, GPT-5.3 Codex, GPT Image 1.5, o3, Gemini 3.1 Pro, Gemini 3 Flash (preview), Gemini 2.5 Flash, Gemini 2.5 Flash Lite.

## Learning Machine

All agents use Agno's Learning Machine for persistent, cross-session learning. When one agent learns something about a user or project, every other agent can access it.

Configured in `config.py` with 6 stores:

| Store | Purpose |
| ----- | ------- |
| `user_profile` | Structured user data (role, preferences, coding style) |
| `user_memory` | Unstructured observations per user |
| `session_context` | Goals, plans, and progress per session (planning enabled) |
| `entity_memory` | Knowledge graph of project entities and relationships |
| `learned_knowledge` | Reusable insights and patterns across all interactions |
| `decision_log` | Technical decisions with rationale and outcomes |

Extraction runs on `fast_model` (GPT-5 Nano) to keep costs low. Data persists in `tmp/pepeclaw.db`.

## Auth Methods

Three approaches for authenticating with MCP servers, plus GitHub CLI auth.

### OAuth (Expo, Stripe)

Browser-based OAuth 2.0 flow with file-based token caching at `~/.pepeclaw/tokens/`. Supports automatic refresh tokens — Stripe tokens refresh silently without reopening the browser.

```python
from tools.auth import create_oauth_mcp_tools

mcp_tools = create_oauth_mcp_tools(
    url="https://mcp.expo.dev/mcp",
    cache_key="expo",
)
```

### GitHub CLI

Piggybacks on existing `gh auth login` — no env var or OAuth flow needed.

```bash
pepeclaw auth login github
```

### Static Auth

One token from an env var, set at startup.

```python
from tools.auth import create_static_mcp_tools

mcp_tools = create_static_mcp_tools(
    url="https://example.com/mcp",
    token_env_var="MY_API_KEY",
)
```

### Dynamic Auth

Per-request tokens from `RunContext.metadata`, with env var fallback.

```python
from tools.auth import create_dynamic_mcp_tools

mcp_tools = create_dynamic_mcp_tools(
    url="https://example.com/mcp",
    token_metadata_key="api_token",
    token_env_var="FALLBACK_TOKEN",
)

# Each request can use a different token
await agent.arun("do something", metadata={"api_token": "user-token"})
```

## Dependencies

- [agno](https://github.com/agno-agi/agno) — agent framework with Learning Machine
- [anthropic](https://github.com/anthropics/anthropic-sdk-python) — Claude models
- [openai](https://github.com/openai/openai-python) — GPT models
- [google-genai](https://github.com/googleapis/python-genai) — Gemini models (Vertex AI)
- [mcp](https://github.com/modelcontextprotocol/python-sdk) — Model Context Protocol
- [aiohttp](https://github.com/aio-libs/aiohttp) — OAuth callback server
- [pygithub](https://github.com/PyGithub/PyGithub) — GitHub API
- [docker](https://github.com/docker/docker-py) — Docker SDK
