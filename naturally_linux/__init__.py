"""Naturally Linux package initializer."""

# Expose the Typer app at package level if needed by external callers.
from .cli import app  # noqa: F401
