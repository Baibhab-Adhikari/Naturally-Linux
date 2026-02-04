"""Compatibility entrypoint for running the CLI as a script."""

from naturally_linux.cli import app


# --------------------------------------------
# Entry point
# --------------------------------------------
def main():
    """
    Entrypoint to call Typer app.

    When this module is run as a script,
    the Typer CLI is launched.
    """
    app()


if __name__ == "__main__":
    main()
