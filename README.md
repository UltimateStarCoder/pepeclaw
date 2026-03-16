# pepeclaw

Multi-agent system built with [Agno](https://github.com/agno-agi/agno) and MCP (Model Context Protocol).

## Project Structure

```
pepeclaw/
├── agents/
│   └── mcp-agents/
│       ├── agno-mcp-agents.py    # Agno docs MCP agent (public, no auth)
│       └── expo-mcp-agents.py    # Expo MCP agent (authenticated)
├── tools/
│   ├── __init__.py
│   ├── static_auth.py            # Static auth — one token for all requests
│   └── dynamic_auth.py           # Dynamic auth — per-request tokens
├── main.py
├── pyproject.toml
└── .env                          # API keys (not committed)
```

## Setup

```bash
# Install dependencies
uv sync

# Configure environment variables
cp .env.example .env
# Edit .env with your API keys
```

### Required Environment Variables

```
ANTHROPIC_API_KEY=sk-ant-...
```

### Optional Environment Variables

```
EXPO_TOKEN=eas_...
```

## Auth Tools

pepeclaw provides two reusable tools for authenticating with MCP servers.

### Static Auth

One token, set at startup from an environment variable. Same token for every request.

```python
from tools import create_static_mcp_tools

mcp_tools = create_static_mcp_tools(
    url="https://example.com/mcp",
    token_env_var="MY_API_KEY",
)
```

Best for: single-user agents, server-to-server calls, dev/testing.

### Dynamic Auth

Per-request tokens from `RunContext.metadata`, with env var fallback. Each request can authenticate as a different user.

```python
from tools import create_dynamic_mcp_tools

mcp_tools = create_dynamic_mcp_tools(
    url="https://example.com/mcp",
    token_metadata_key="api_token",
    token_env_var="FALLBACK_TOKEN",  # optional fallback
)
```

At runtime, pass the token in metadata:

```python
await agent.arun(
    "do something",
    user_id="user-123",
    metadata={"api_token": "user-specific-token"},
)
```

The `metadata` dictionary is part of Agno's `RunContext` — it flows through the entire request lifecycle. The dynamic auth tool reads from it to generate per-request `Authorization` headers. It also automatically attaches `X-User-ID` and `X-Session-ID` headers.

Token priority: `metadata[key]` > env var > no auth header.

Best for: multi-user/multi-tenant apps where each user has their own credentials.

## Agents

### Agno MCP Agent

Connects to the public Agno docs MCP server. No authentication required.

```bash
uv run python agents/mcp-agents/agno-mcp-agents.py
```

### Expo MCP Agent

Connects to Expo's MCP server with dynamic auth. Requires an Expo token.

```bash
uv run python agents/mcp-agents/expo-mcp-agents.py
```

## Dependencies

- [agno](https://github.com/agno-agi/agno) — agent framework
- [anthropic](https://github.com/anthropics/anthropic-sdk-python) — Claude models
- [mcp](https://github.com/modelcontextprotocol/python-sdk) — Model Context Protocol