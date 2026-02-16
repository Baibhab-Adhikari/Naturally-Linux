# Naturally Linux

Naturally Linux is a command-line tool that turns natural-language requests into safe, reviewable Linux shell commands. It shows you the proposed command, explains what it does, and runs it only after confirmation.

## Features

- Natural-language → shell command generation
- Command preview and explanation
- Safety checks before execution
- Confirmation before running commands

## Install (recommended)

Install the UV package manager, then install the CLI system-wide:

```
curl -LsSf https://astral.sh/uv/install.sh | sh
uv tool install naturally-linux
```

Alternative (pip):

```
pip install naturally-linux
```

## Setup

Store your Groq API key (recommended):

```
naturally-linux config set-key YOUR_GROQ_API_KEY
```

Or set it via environment variable:

```
export GROQ_API_KEY="your-key"
```

## Usage

Generate and run a command:

```
naturally-linux "list files larger than 10MB"
```

Preview with explanation only:

```
naturally-linux "list files larger than 10MB" --dry-run
```

Set a timeout (seconds):

```
naturally-linux "scan logs" --timeout 10
```

Manage API key:

```
naturally-linux config show
naturally-linux config delete
```

## License

MIT
