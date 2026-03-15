from os import getenv

from agno.tools.mcp import MCPTools, StreamableHTTPClientParams


def create_static_mcp_tools(
    url: str,
    token_env_var: str,
    extra_headers: dict | None = None,
    add_instructions: bool = True,
    timeout: float = 30,
    sse_read_timeout: float = 300,
) -> MCPTools:
    """Create MCPTools with static auth headers from an environment variable.

    Args:
        url: The MCP server URL.
        token_env_var: Name of the env var holding the Bearer token.
        extra_headers: Additional headers to include in requests.
        add_instructions: Whether to inject tool instructions into the system prompt.
        timeout: Connection timeout in seconds.
        sse_read_timeout: SSE read timeout in seconds.
    """
    token = getenv(token_env_var)
    if not token:
        raise ValueError(f"Environment variable '{token_env_var}' is not set")

    headers = {"Authorization": f"Bearer {token}"}
    if extra_headers:
        headers.update(extra_headers)

    server_params = StreamableHTTPClientParams(
        url=url,
        headers=headers,
        timeout=timeout,
        sse_read_timeout=sse_read_timeout,
    )

    return MCPTools(
        server_params=server_params,
        transport="streamable-http",
        add_instructions=add_instructions,
    )