# pepeclaw

Multi-agent system built with [Agno](https://github.com/agno-agi/agno) and MCP (Model Context Protocol).

## Project Structure

```
pepeclaw/
├── agents/
│   └── mcp_agents/
│       ├── agno_mcp_agents.py    # Agno docs MCP agent (public, no auth)
│       └── expo_mcp_agents.py    # Expo MCP agent (OAuth)
├── tools/
│   ├── __init__.py
│   ├── static_auth.py            # Static auth — one token for all requests
│   ├── dynamic_auth.py           # Dynamic auth — per-request tokens
│   └── oauth_auth.py             # OAuth auth — browser flow with token caching
├── main.py                       # Runs all agents via AgentOS
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

## Running

```bash
uv run python main.py
```

This starts AgentOS on `http://localhost:7777` with all agents. On first run, the Expo agent will open your browser for OAuth authentication.

## Auth Tools

pepeclaw provides three reusable tools for authenticating with MCP servers.

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

### OAuth Auth

Full OAuth 2.0 flow with browser-based authentication and file-based token caching.

```python
from tools import create_oauth_mcp_tools

mcp_tools = create_oauth_mcp_tools(
    url="https://mcp.expo.dev/mcp",
    cache_key="expo",
    client_name="Pepeclaw",
)
```

On first use, opens a browser for the user to authenticate. Tokens are cached to `~/.pepeclaw/tokens/{cache_key}/` and reused automatically on subsequent runs.

Best for: MCP servers that require OAuth (e.g., Expo), where a simple API key isn't sufficient.

## Agents

### Agno MCP Agent

Connects to the public Agno docs MCP server. No authentication required.

### Expo MCP Agent

Connects to Expo's MCP server via OAuth. On first run, opens a browser for authentication. Tokens are cached for subsequent runs.

## Dependencies

- [agno](https://github.com/agno-agi/agno) — agent framework
- [anthropic](https://github.com/anthropics/anthropic-sdk-python) — Claude models
- [mcp](https://github.com/modelcontextprotocol/python-sdk) — Model Context Protocol
- [aiohttp](https://github.com/aio-libs/aiohttp) — OAuth callback server
