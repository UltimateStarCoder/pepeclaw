import asyncio
import shutil
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(
    name="pepeclaw",
    help="Pepeclaw — Multi-agent system powered by Agno and MCP. Config: ~/.pepeclaw/.env",
    no_args_is_help=True,
)
auth_app = typer.Typer(help="Manage OAuth authentication tokens.")
app.add_typer(auth_app, name="auth")

console = Console()

# ─────────────────────────────────────────────────────────────────
# Registry — maps names to agent/team imports
# ─────────────────────────────────────────────────────────────────

AGENTS = {
    "coding": "agents.coding_agents.coding_agent:coding_agent",
    "python": "agents.coding_agents.python_agent:python_agent",
    "shell": "agents.coding_agents.shell_agent:shell_agent",
    "file": "agents.coding_agents.file_agent:file_agent",
    "filegen": "agents.coding_agents.filegen_agent:filegen_agent",
    "reasoning": "agents.coding_agents.reasoning_agent:reasoning_agent",
    "agno": "agents.mcp_agents.agno_mcp_agents:agno_mcp_agents",
    "clerk": "agents.mcp_agents.clerk_mcp_agents:clerk_mcp_agents",
    "convex": "agents.mcp_agents.convex_mcp_agents:convex_mcp_agents",
    "expo": "agents.mcp_agents.expo_mcp_agents:expo_mcp_agents",
    "stripe": "agents.mcp_agents.stripe_mcp_agents:stripe_mcp_agents",
}

TEAMS = {
    "dev": "teams.dev_team:dev_team",
    "docs": "teams.docs_team:docs_team",
    "deploy": "teams.deploy_team:deploy_team",
    "payments": "teams.payments_team:payments_team",
    "fullstack": "teams.fullstack_team:fullstack_team",
}

PEPECLAW_HOME = Path.home() / ".pepeclaw"
TOKEN_CACHE_DIR = PEPECLAW_HOME / "tokens"
GLOBAL_ENV_FILE = PEPECLAW_HOME / ".env"

ENV_TEMPLATE = """\
# Pepeclaw Configuration
# ─────────────────────────────────────────────────────────────────
# This file is loaded automatically by pepeclaw.
# Set your API keys here to use them from anywhere.

# Anthropic (required)
ANTHROPIC_API_KEY=

# OpenAI (optional)
OPENAI_API_KEY=

# Google Vertex AI (optional)
# GOOGLE_GENAI_USE_VERTEXAI=true
# GOOGLE_CLOUD_PROJECT=your-project-id
# GOOGLE_CLOUD_LOCATION=us-central1
"""


def _load(path: str):
    """Dynamically import an agent or team from a module:attribute string."""
    module_path, attr_name = path.rsplit(":", 1)
    import importlib
    module = importlib.import_module(module_path)
    return getattr(module, attr_name)


# ─────────────────────────────────────────────────────────────────
# pepeclaw init
# ─────────────────────────────────────────────────────────────────

@app.command()
def init():
    """Set up pepeclaw config at ~/.pepeclaw/.env with your API keys."""
    PEPECLAW_HOME.mkdir(parents=True, exist_ok=True)

    if GLOBAL_ENV_FILE.exists():
        console.print(f"[yellow]Config already exists at {GLOBAL_ENV_FILE}[/yellow]")
        overwrite = typer.confirm("Overwrite?", default=False)
        if not overwrite:
            console.print("[dim]Skipped.[/dim]")
            raise typer.Exit()

    GLOBAL_ENV_FILE.write_text(ENV_TEMPLATE)
    console.print(f"\n[green]Created config at {GLOBAL_ENV_FILE}[/green]")
    console.print("[dim]Edit the file to add your API keys, then run pepeclaw serve.[/dim]\n")


# ─────────────────────────────────────────────────────────────────
# pepeclaw serve
# ─────────────────────────────────────────────────────────────────

@app.command()
def serve(
    host: str = typer.Option("localhost", help="Host to bind to."),
    port: int = typer.Option(7777, help="Port to bind to."),
):
    """Start the Pepeclaw AgentOS server."""
    from main import agent_os, app as asgi_app  # noqa: F811

    console.print(f"\n[bold green]Starting Pepeclaw AgentOS on {host}:{port}[/bold green]\n")
    agent_os.serve(app="main:app", host=host, port=port)


# ─────────────────────────────────────────────────────────────────
# pepeclaw list
# ─────────────────────────────────────────────────────────────────

@app.command(name="list")
def list_all():
    """List all available agents and teams."""
    table = Table(title="Pepeclaw Agents", show_lines=True)
    table.add_column("Name", style="cyan")
    table.add_column("Type", style="green")
    table.add_column("ID")

    for name, path in AGENTS.items():
        agent = _load(path)
        table.add_row(name, "agent", agent.id)

    console.print(table)
    console.print()

    table = Table(title="Pepeclaw Teams", show_lines=True)
    table.add_column("Name", style="cyan")
    table.add_column("Type", style="green")
    table.add_column("ID")
    table.add_column("Members", style="dim")

    for name, path in TEAMS.items():
        team = _load(path)
        members = ", ".join(m.name for m in team.members)
        table.add_row(name, "team", team.id, members)

    console.print(table)


# ─────────────────────────────────────────────────────────────────
# pepeclaw chat
# ─────────────────────────────────────────────────────────────────

@app.command()
def chat(
    name: str = typer.Argument(help="Agent or team name (e.g., 'coding', 'fullstack')."),
    user_id: str = typer.Option("cli-user", help="User ID for memory/session."),
):
    """Chat with a specific agent or team in the terminal."""
    if name in AGENTS:
        target = _load(AGENTS[name])
        kind = "agent"
    elif name in TEAMS:
        target = _load(TEAMS[name])
        kind = "team"
    else:
        console.print(f"[red]Unknown agent or team: '{name}'[/red]")
        console.print(f"Available: {', '.join(list(AGENTS) + list(TEAMS))}")
        raise typer.Exit(1)

    console.print(f"\n[bold]Chatting with {target.name} ({kind})[/bold]")
    console.print("[dim]Type 'exit' or 'quit' to end the conversation.[/dim]\n")

    async def _chat_loop():
        while True:
            try:
                message = console.input("[bold cyan]You:[/bold cyan] ")
            except (EOFError, KeyboardInterrupt):
                break

            if message.strip().lower() in ("exit", "quit", "q"):
                break

            if not message.strip():
                continue

            await target.aprint_response(message, user_id=user_id, stream=True)
            console.print()

    asyncio.run(_chat_loop())
    console.print("\n[dim]Goodbye![/dim]")


# ─────────────────────────────────────────────────────────────────
# pepeclaw auth login
# ─────────────────────────────────────────────────────────────────

@auth_app.command(name="login")
def auth_login(
    service: str = typer.Argument(help="Service to authenticate with (e.g., 'expo', 'stripe')."),
):
    """Authenticate with an OAuth-protected MCP service."""
    from tools.auth.oauth import get_oauth_token

    urls = {
        "expo": "https://mcp.expo.dev/mcp",
        "stripe": "https://mcp.stripe.com",
    }

    if service not in urls:
        console.print(f"[red]Unknown service: '{service}'[/red]")
        console.print(f"Available: {', '.join(urls)}")
        raise typer.Exit(1)

    console.print(f"\n[bold]Authenticating with {service}...[/bold]\n")

    token = asyncio.run(
        get_oauth_token(
            server_url=urls[service],
            cache_key=service,
            client_name="Pepeclaw",
            force_refresh=True,
        )
    )

    console.print(f"[green]Authenticated with {service}.[/green]")
    console.print(f"[dim]Token cached at ~/.pepeclaw/tokens/{service}/[/dim]\n")


# ─────────────────────────────────────────────────────────────────
# pepeclaw auth clear
# ─────────────────────────────────────────────────────────────────

@auth_app.command(name="clear")
def auth_clear(
    service: Optional[str] = typer.Argument(None, help="Service to clear tokens for. Omit to clear all."),
):
    """Clear cached OAuth tokens."""
    if service:
        target = TOKEN_CACHE_DIR / service
        if target.exists():
            shutil.rmtree(target)
            console.print(f"[green]Cleared tokens for {service}.[/green]")
        else:
            console.print(f"[yellow]No cached tokens found for {service}.[/yellow]")
    else:
        if TOKEN_CACHE_DIR.exists():
            shutil.rmtree(TOKEN_CACHE_DIR)
            console.print("[green]Cleared all cached tokens.[/green]")
        else:
            console.print("[yellow]No cached tokens found.[/yellow]")


# ─────────────────────────────────────────────────────────────────
# pepeclaw auth status
# ─────────────────────────────────────────────────────────────────

@auth_app.command(name="status")
def auth_status():
    """Show which services have cached tokens."""
    if not TOKEN_CACHE_DIR.exists():
        console.print("[yellow]No cached tokens.[/yellow]")
        return

    services = [d.name for d in TOKEN_CACHE_DIR.iterdir() if d.is_dir()]
    if not services:
        console.print("[yellow]No cached tokens.[/yellow]")
        return

    table = Table(title="Cached OAuth Tokens")
    table.add_column("Service", style="cyan")
    table.add_column("Token File", style="green")

    for svc in sorted(services):
        token_file = TOKEN_CACHE_DIR / svc / "tokens.json"
        status = "present" if token_file.exists() else "missing"
        table.add_row(svc, status)

    console.print(table)


# ─────────────────────────────────────────────────────────────────
# pepeclaw reset
# ─────────────────────────────────────────────────────────────────

@app.command()
def reset(
    memory: bool = typer.Option(False, "--memory", "-m", help="Clear agent memory database."),
    tokens: bool = typer.Option(False, "--tokens", "-t", help="Clear cached OAuth tokens."),
    generated: bool = typer.Option(False, "--generated", "-g", help="Clear generated files."),
    all_: bool = typer.Option(False, "--all", "-a", help="Clear everything."),
):
    """Clear memory, tokens, and/or generated files."""
    if not any([memory, tokens, generated, all_]):
        console.print("[yellow]Specify what to reset: --memory, --tokens, --generated, or --all[/yellow]")
        raise typer.Exit(1)

    if all_ or memory:
        db_path = Path("tmp/pepeclaw.db")
        if db_path.exists():
            db_path.unlink()
            console.print("[green]Cleared agent memory database.[/green]")
        else:
            console.print("[yellow]No memory database found.[/yellow]")

    if all_ or tokens:
        if TOKEN_CACHE_DIR.exists():
            shutil.rmtree(TOKEN_CACHE_DIR)
            console.print("[green]Cleared all OAuth tokens.[/green]")
        else:
            console.print("[yellow]No cached tokens found.[/yellow]")

    if all_ or generated:
        gen_path = Path("tmp/generated")
        if gen_path.exists():
            shutil.rmtree(gen_path)
            gen_path.mkdir(parents=True)
            console.print("[green]Cleared generated files.[/green]")
        else:
            console.print("[yellow]No generated files found.[/yellow]")


# ─────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app()
