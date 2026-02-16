# Architecture

## Overview

The CLI is split into focused modules:

- `cli.py`: Typer app and command wiring
- `generator.py`: LLM inference and prompt handling
- `safety.py`: safety checks for commands
- `executor.py`: execution via `subprocess`
- `config.py`: local config storage for API key

## Flow

1. User provides a prompt
2. `generate_command()` calls Groq to produce a command
3. `unsafe_reasons()` evaluates risk
4. Command is shown to the user
5. If confirmed, `run_command()` executes it with a timeout

## Extension points

- Swap the LLM provider in `generator.py`
- Add advanced safety policies in `safety.py`
- Add stronger sandboxing in `executor.py`
