# Architecture

## Overview

The CLI is split into focused modules:

- `cli.py`: Typer app and command wiring
- `generator.py`: LLM inference and prompt handling
- `safety.py`: safety checks for commands
- `executor.py`: execution via `subprocess`

## Flow

1. User provides a prompt
2. `generate_command()` calls Groq to produce a command
3. `is_safe_command()` evaluates risk
4. Command is shown to the user
5. If confirmed, `run_command()` executes it

## Extension points

- Swap the LLM provider in `generator.py`
- Add advanced safety policies in `safety.py`
- Add timeout/sandboxing in `executor.py`
