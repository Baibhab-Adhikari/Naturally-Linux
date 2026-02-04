# Naturally Linux

Naturally Linux is a command-line tool that converts natural-language requests into safe, reviewable Linux shell commands. It previews the generated command, explains what it does, and executes only after confirmation.

## Why it exists

Shell commands can be terse and easy to misremember. Naturally Linux lets you describe tasks in plain English and translates them into commands you can review and run.

## Key features

- Natural-language → shell command generation
- Command preview and explanation
- Safety checks for potentially destructive operations
- Confirmation before execution

## Quick start

```bash
pip install naturally-linux
export GROQ_API_KEY="your-key"

naturally-linux "list files larger than 10MB"
```

For a dry-run with explanation only:

```bash
naturally-linux "list files larger than 10MB" --dry-run
```
