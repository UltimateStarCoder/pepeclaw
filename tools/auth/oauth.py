import asyncio
import json
import webbrowser
from datetime import timedelta
from pathlib import Path
from typing import Optional

import httpx
from aiohttp import web
from mcp.client.auth import OAuthClientProvider, TokenStorage
from mcp.shared.auth import OAuthClientInformationFull, OAuthClientMetadata, OAuthToken
from pydantic import AnyUrl

from agno.tools.mcp import MCPTools, StreamableHTTPClientParams

TOKEN_CACHE_DIR = Path.home() / ".pepeclaw" / "tokens"


class FileTokenStorage(TokenStorage):
    """Persists OAuth tokens and client info to disk for reuse across sessions."""

    def __init__(self, cache_path: Path):
        self.token_file = cache_path / "tokens.json"
        self.client_file = cache_path / "client_info.json"
        cache_path.mkdir(parents=True, exist_ok=True)

    async def get_tokens(self) -> Optional[OAuthToken]:
        if self.token_file.exists():
            data = json.loads(self.token_file.read_text())
            return OAuthToken(**data)
        return None

    async def set_tokens(self, tokens: OAuthToken) -> None:
        self.token_file.write_text(tokens.model_dump_json())

    async def get_client_info(self) -> Optional[OAuthClientInformationFull]:
        if self.client_file.exists():
            data = json.loads(self.client_file.read_text())
            return OAuthClientInformationFull(**data)
        return None

    async def set_client_info(self, client_info: OAuthClientInformationFull) -> None:
        self.client_file.write_text(client_info.model_dump_json())


async def _run_oauth_flow(
    server_url: str,
    storage: FileTokenStorage,
    client_name: str = "Pepeclaw",
    callback_port: int = 3000,
) -> str:
    """Run the OAuth flow: open browser, receive callback, return access token."""

    auth_code_future: asyncio.Future[tuple[str, Optional[str]]] = (
        asyncio.get_event_loop().create_future()
    )

    async def handle_callback(request: web.Request) -> web.Response:
        code = request.query.get("code")
        state = request.query.get("state")
        if code:
            if not auth_code_future.done():
                auth_code_future.set_result((code, state))
            return web.Response(
                text="<html><body><h2>Authentication successful!</h2>"
                "<p>You can close this tab.</p></body></html>",
                content_type="text/html",
            )
        error = request.query.get("error", "unknown error")
        if not auth_code_future.done():
            auth_code_future.set_exception(RuntimeError(f"OAuth error: {error}"))
        return web.Response(text=f"OAuth error: {error}", status=400)

    async def oauth_callback_handler() -> tuple[str, Optional[str]]:
        return await auth_code_future

    callback_url = f"http://localhost:{callback_port}/callback"

    app = web.Application()
    app.router.add_get("/callback", handle_callback)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "localhost", callback_port)
    await site.start()

    try:
        oauth_provider = OAuthClientProvider(
            server_url=server_url,
            client_metadata=OAuthClientMetadata(
                client_name=client_name,
                redirect_uris=[AnyUrl(callback_url)],
                grant_types=["authorization_code", "refresh_token"],
                response_types=["code"],
            ),
            storage=storage,
            redirect_handler=_open_browser,
            callback_handler=oauth_callback_handler,
        )

        async with httpx.AsyncClient(auth=oauth_provider, follow_redirects=True) as client:
            await client.post(
                server_url,
                content=b'{"jsonrpc":"2.0","method":"initialize","id":1}',
                headers={"Content-Type": "application/json"},
            )

        tokens = await storage.get_tokens()
        if not tokens:
            raise RuntimeError("OAuth flow completed but no tokens were stored")
        return tokens.access_token

    finally:
        await runner.cleanup()


async def _open_browser(url: str) -> None:
    print(f"\nOpening browser for authentication...\n  {url}\n")
    webbrowser.open(url)


async def _validate_token(server_url: str, token: str) -> bool:
    """Check if a cached token is still valid by making a test request."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                server_url,
                content=b'{"jsonrpc":"2.0","method":"initialize","id":1}',
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {token}",
                },
                timeout=10,
            )
            return response.status_code != 401
    except Exception:
        # Network errors shouldn't invalidate the token — let the actual connection handle it
        return True


async def get_oauth_token(
    server_url: str,
    cache_key: str,
    client_name: str = "Pepeclaw",
    callback_port: int = 3000,
    force_refresh: bool = False,
) -> str:
    """Get an OAuth token, using cached token if available.

    Validates cached tokens before returning them. If the token has expired,
    the cache is cleared and the browser-based OAuth flow is re-triggered
    automatically.

    Args:
        server_url: The MCP server URL.
        cache_key: Unique key for caching tokens (e.g., "expo").
        client_name: OAuth client name shown during authorization.
        callback_port: Local port for the OAuth callback server.
        force_refresh: If True, ignore cached token and re-authenticate.
    """
    cache_path = TOKEN_CACHE_DIR / cache_key
    storage = FileTokenStorage(cache_path)

    if not force_refresh:
        tokens = await storage.get_tokens()
        if tokens:
            if await _validate_token(server_url, tokens.access_token):
                return tokens.access_token
            print(f"\n[pepeclaw] Cached token for '{cache_key}' expired. Re-authenticating...")

    return await _run_oauth_flow(
        server_url=server_url,
        storage=storage,
        client_name=client_name,
        callback_port=callback_port,
    )


def create_oauth_mcp_tools(
    url: str,
    cache_key: str,
    client_name: str = "Pepeclaw",
    callback_port: int = 3000,
    add_instructions: bool = True,
    timeout: float = 30,
    sse_read_timeout: float = 300,
) -> MCPTools:
    """Create MCPTools with OAuth authentication.

    On first use, opens a browser for the user to authenticate.
    Tokens are cached to disk at ~/.pepeclaw/tokens/{cache_key}/.

    Args:
        url: The MCP server URL.
        cache_key: Unique key for caching tokens (e.g., "expo").
        client_name: OAuth client name shown during authorization.
        callback_port: Local port for the OAuth callback server.
        add_instructions: Whether to inject tool instructions into the system prompt.
        timeout: Connection timeout in seconds.
        sse_read_timeout: SSE read timeout in seconds.
    """
    token = asyncio.run(
        get_oauth_token(
            server_url=url,
            cache_key=cache_key,
            client_name=client_name,
            callback_port=callback_port,
        )
    )

    server_params = StreamableHTTPClientParams(
        url=url,
        headers={"Authorization": f"Bearer {token}"},
        timeout=timedelta(seconds=timeout),
        sse_read_timeout=timedelta(seconds=sse_read_timeout),
    )

    return MCPTools(
        server_params=server_params,
        transport="streamable-http",
        add_instructions=add_instructions,
    )
