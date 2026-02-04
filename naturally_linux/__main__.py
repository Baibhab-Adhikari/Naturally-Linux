"""Run the Typer app with python -m naturally_linux."""

from .cli import app


def main() -> None:
    # Ensure help shows the intended CLI name when invoked via python -m.
    app(prog_name="naturally-linux")


if __name__ == "__main__":
    main()
