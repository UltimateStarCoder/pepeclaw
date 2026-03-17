# pepeclaw

Multi-agent system built with [Agno](https://github.com/agno-agi/agno) and MCP (Model Context Protocol).

12 agents, 5 teams, 3 auth tools, 3 AI providers, shared memory, and a CLI.

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
│   │   └── reasoning_agent.py      # Structured thinking & debugging
│   └── mcp_agents/
│       ├── agno_mcp_agents.py      # Agno docs (public, no auth)
│       ├── clerk_mcp_agents.py     # Clerk auth (public, no auth)
│       ├── convex_mcp_agents.py    # Convex backend (stdio)
│       ├── expo_mcp_agents.py      # Expo (OAuth)
│       ├── livekit_mcp_agents.py   # LiveKit docs (public, no auth)
│       └── stripe_mcp_agents.py    # Stripe (OAuth)
├── teams/
│   ├── dev_team.py                 # Coding, Python, Shell, File, Reasoning
│   ├── docs_team.py                # Agno, Clerk, Expo, LiveKit, Reasoning
│   ├── deploy_team.py              # Shell, Expo, Convex
│   ├── payments_team.py            # Stripe, File Generation
│   └── fullstack_team.py           # All 12 agents
├── tools/
│   └── auth/
│       ├── static.py               # Static auth — env var token
│       ├── dynamic.py              # Dynamic auth — per-request tokens
│       └── oauth.py                # OAuth — browser flow + token caching
├── config.py                       # Models, database, memory manager
├── cli.py                          # CLI entry point
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
uv tool install --from . --editable .

# Standard — snapshot copy, stable but needs reinstall after source changes
uv tool install --from .
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

# Manage OAuth tokens
pepeclaw auth login expo
pepeclaw auth login stripe
pepeclaw auth status
pepeclaw auth clear
pepeclaw auth clear expo

# Reset data
pepeclaw reset --memory         # Clear agent memory database
pepeclaw reset --tokens         # Clear OAuth tokens
pepeclaw reset --generated      # Clear generated files
pepeclaw reset --all            # Clear everything
```

## Models

All models are configured in `config.py`. Change a role assignment once, and every agent using that role updates automatically.

| Role | Model | Used by |
| ---- | ----- | ------- |
| `default_model` | Claude Sonnet 4.5 | All coding & MCP agents |
| `reasoning_model` | Claude Opus 4.6 | Reasoning Agent, all team leaders |
| `fast_model` | GPT-5 Nano | Memory Manager |
| `image_model` | Gemini Flash Image | File Generation Agent |

Additional models available in config: GPT-5.4, GPT-5.4 Pro, GPT-5 Mini, GPT-5.3 Codex, o3, Gemini 3.1 Pro, Gemini 3 Flash, Gemini 2.5 Flash.

## Auth Tools

Three reusable tools for authenticating with MCP servers.

### Static Auth

One token from an env var, set at startup. Same token for every request.

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

Token priority: `metadata[key]` > env var > no auth header.

### OAuth Auth

Browser-based OAuth 2.0 flow with file-based token caching at `~/.pepeclaw/tokens/`.

```python
from tools.auth import create_oauth_mcp_tools

mcp_tools = create_oauth_mcp_tools(
    url="https://mcp.expo.dev/mcp",
    cache_key="expo",
)
```

## Shared Memory

All agents share a SQLite database (`tmp/pepeclaw.db`) for memory persistence. When one agent learns something about a user, all other agents can access it. Configured via `config.py`.

## Dependencies

- [agno](https://github.com/agno-agi/agno) — agent framework
- [anthropic](https://github.com/anthropics/anthropic-sdk-python) — Claude models
- [openai](https://github.com/openai/openai-python) — GPT models
- [google-genai](https://github.com/googleapis/python-genai) — Gemini models (Vertex AI)
- [mcp](https://github.com/modelcontextprotocol/python-sdk) — Model Context Protocol
- [aiohttp](https://github.com/aio-libs/aiohttp) — OAuth callback server
