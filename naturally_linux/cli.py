"""Typer CLI entrypoint for Naturally Linux."""

from __future__ import annotations

from contextlib import contextmanager
from typing import Optional

import typer
from rich.console import Console
from typer.core import TyperGroup

from .config import config_path, delete_api_key, get_api_key, set_api_key
from .executor import run_command
from .generator import explain_command, generate_command
from .safety import heuristic_risk_level, heuristic_warnings, unsafe_reasons


class DefaultGroup(TyperGroup):
    """Treat unknown commands as the default 'run' command."""
    default_cmd_name = "run"

    def parse_args(self, ctx, args):
        if args and args[0] not in self.commands:
            args.insert(0, self.default_cmd_name)
        return super().parse_args(ctx, args)


# Create the Typer app instance.
app = typer.Typer(
    cls=DefaultGroup,
    help="Naturally Linux: translate natural language into safe Linux commands.",
    epilog=(
        "Examples:\n"
        "  naturally-linux \"list files in this folder\"\n\n"
        "  naturally-linux \"find files larger than 10MB\" --dry-run\n\n"
        "  naturally-linux config set-key YOUR_GROQ_API_KEY\n\n"
        "Commands:\n\n"
        "  config set-key   Store Groq API key\n\n"
        "  config show      Show stored API key (masked)\n\n"
        "  config delete    Remove stored API key\n\n"
        "Notes:\n\n"
        "  Set GROQ_API_KEY or use the config commands to store it."
    ),
    context_settings={"allow_extra_args": True},
)
config_app = typer.Typer(help="Manage Naturally Linux configuration.")

app.add_typer(config_app, name="config")

console = Console()


@contextmanager
def spinner(message: str):
    if not console.is_terminal:
        yield
        return

    with console.status(message):
        yield


def _print_heuristics(command: str) -> str:
    warnings = heuristic_warnings(command)
    risk_level = heuristic_risk_level(warnings)
    typer.secho(f"\nHeuristic risk: {risk_level}", fg=typer.colors.MAGENTA)
    for message, level in warnings:
        typer.secho(f"- {message} ({level})", fg=typer.colors.MAGENTA)
    return risk_level


@config_app.command("set-key")
def config_set_key(
    api_key: str = typer.Argument(..., help="Groq API key to store locally."),
):
    """Store the Groq API key in the user config file."""

    set_api_key(api_key)
    typer.echo(f"Saved API key to {config_path()}")


@config_app.command("show")
def config_show_key():
    """Show whether an API key is configured (masked if present)."""

    api_key = get_api_key()
    if api_key:
        masked = api_key[:4] + "..." + api_key[-4:]
        typer.echo(f"GROQ_API_KEY: {masked}")
        return
    typer.echo("No API key configured.")


@config_app.command("delete")
def config_delete_key():
    """Delete the stored API key from the config file."""

    if delete_api_key():
        typer.echo("API key removed.")
    else:
        typer.echo("No API key found to delete.")


def _handle_prompt(
    prompt: str,
    auto_approve: bool,
    dry_run: bool,
    timeout: float,
) -> None:
    """Core handler for the natural-language prompt."""

    try:
        with spinner("Generating command"):
            command = generate_command(prompt)
    except RuntimeError as exc:
        typer.secho(str(exc), fg=typer.colors.YELLOW)
        raise typer.Exit(code=1)

    typer.secho("Proposed command:", fg=typer.colors.CYAN)
    typer.echo(command)

    reasons = unsafe_reasons(command)
    if reasons:
        typer.secho("Potentially unsafe command detected:",
                    fg=typer.colors.RED)
        for reason in reasons:
            typer.secho(f"- {reason}", fg=typer.colors.RED)
        if not auto_approve and not typer.confirm("Proceed anyway?", default=False):
            raise typer.Abort()

    warnings = heuristic_warnings(command)
    if warnings:
        typer.secho(
            "\nThis command may scan the entire filesystem or require privileges.",
            fg=typer.colors.MAGENTA,
        )
        for message, level in warnings:
            typer.secho(f"- {message} ({level})", fg=typer.colors.MAGENTA)
        if not typer.confirm("Proceed anyway?", default=False):
            raise typer.Abort()

    if dry_run:
        try:
            with spinner("Explaining command"):
                explanation = explain_command(command)
            if explanation:
                typer.secho("\nExplanation:", fg=typer.colors.GREEN)
                typer.echo(explanation)
        except RuntimeError as exc:
            typer.secho(str(exc), fg=typer.colors.YELLOW)

        safety_label = "SAFE" if not reasons else "UNSAFE"
        safety_color = typer.colors.GREEN if safety_label == "SAFE" else typer.colors.RED
        typer.secho(f"\nSafety check: {safety_label}", fg=safety_color)

        _print_heuristics(command)

        executed = False
        returncode: Optional[int] = None
        if auto_approve or typer.confirm("Run this command now?", default=False):
            stdout, stderr, returncode = run_command(
                command, timeout_seconds=timeout)

            executed = True

            if stdout:
                typer.echo(stdout)

            if stderr:
                typer.secho(stderr, fg=typer.colors.YELLOW)

            if returncode != 0:
                raise typer.Exit(code=returncode)

        if executed:
            return

        typer.secho(
            "\nDry run mode — command not executed.",
            fg=typer.colors.YELLOW,
        )
        return

    if not auto_approve and not typer.confirm("Run this command?", default=False):
        raise typer.Abort()

    stdout, stderr, returncode = run_command(command, timeout_seconds=timeout)

    if stdout:
        typer.echo(stdout)

    if stderr:
        typer.secho(stderr, fg=typer.colors.YELLOW)

    if returncode != 0:
        raise typer.Exit(code=returncode)


@app.command(hidden=True, name="run")
def run(
    prompt: str = typer.Argument(...,
                                 help="Natural language task description."),
    auto_approve: bool = typer.Option(
        False, "--yes", "-y", help="Skip confirmation prompts and execute immediately."
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Show explanation and safety verdict without executing."
    ),
    timeout: float = typer.Option(
        15.0, "--timeout", help="Execution timeout in seconds (default: 15)."
    ),
):
    """Hidden default command used for prompt execution."""
    _handle_prompt(prompt, auto_approve, dry_run, timeout)

# Remove or keep the @app.callback if you want, but it’s no longer required.
