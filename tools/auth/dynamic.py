from os import getenv
from typing import TYPE_CHECKING, Optional

from agno.run import RunContext
from agno.tools.mcp import MCPTools

if TYPE_CHECKING:
    from agno.agent import Agent
    from agno.team import Team


def create_dynamic_mcp_tools(
    url: str,
    token_metadata_key: str = "api_token",
    token_env_var: str | None = None,
    extra_headers: dict | None = None,
    add_instructions: bool = True,
) -> MCPTools:
    """Create MCPTools with dynamic auth headers derived from RunContext.

    Headers are generated per-request, pulling the token from
    RunContext.metadata[token_metadata_key]. If no token is found in
    metadata, falls back to the env var specified by token_env_var.

    Args:
        url: The MCP server URL.
        token_metadata_key: Key in RunContext.metadata holding the Bearer token.
        token_env_var: Fallback env var name if no token is found in metadata.
        extra_headers: Additional static headers to include in every request.
        add_instructions: Whether to inject tool instructions into the system prompt.
    """

    def header_provider(
        run_context: RunContext,
        agent: Optional["Agent"] = None,
        team: Optional["Team"] = None,
    ) -> dict:
        token = (
            run_context.metadata.get(token_metadata_key)
            if run_context.metadata
            else None
        )

        if not token and token_env_var:
            token = getenv(token_env_var)

        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        if run_context.user_id:
            headers["X-User-ID"] = run_context.user_id
        if run_context.session_id:
            headers["X-Session-ID"] = run_context.session_id
        if extra_headers:
            headers.update(extra_headers)

        return headers

    return MCPTools(
        url=url,
        transport="streamable-http",
        header_provider=header_provider,
        add_instructions=add_instructions,
    )
