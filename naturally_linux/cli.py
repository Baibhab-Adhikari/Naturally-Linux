"""Typer CLI entrypoint for Naturally Linux."""

import typer

from .executor import run_command
from .generator import generate_command
from .safety import is_safe_command

# Create the Typer app instance.
# This object registers and groups all CLI commands.
app = typer.Typer(
    help="Naturally Linux: run shell tasks using natural language.")


@app.command()
def run(
    prompt: str = typer.Argument(...,
                                 help="Natural language task description."),
    auto_approve: bool = typer.Option(
        False, "--yes", "-y", help="Auto-approve without confirmation."
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Preview command without executing it."
    ),
):
    """
    Convert a natural-language instruction into a shell command,
    display it, and optionally execute it.
    """

    # Step 1: Ask the generator to produce a shell command.
    command = generate_command(prompt)

    # Step 2: Run safety checks on the generated command.
    if not is_safe_command(command):
        typer.secho("Potentially unsafe command detected.",
                    fg=typer.colors.RED)
        if not auto_approve and not typer.confirm("Proceed anyway?", default=False):
            raise typer.Abort()

    # Step 3: Show the user the proposed command.
    typer.secho("Proposed command:", fg=typer.colors.CYAN)
    typer.echo(command)

    # Step 4: Stop here if the user only wants a preview.
    if dry_run:
        return

    # Step 5: Ask for confirmation unless auto-approved.
    if not auto_approve and not typer.confirm("Run this command?", default=False):
        raise typer.Abort()

    # Step 6: Execute the command and surface output.
    stdout, stderr, returncode = run_command(command)

    if stdout:
        typer.echo(stdout)

    if stderr:
        typer.secho(stderr, fg=typer.colors.YELLOW)

    if returncode != 0:
        raise typer.Exit(code=returncode)
