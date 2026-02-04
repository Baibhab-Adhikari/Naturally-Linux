# Naturally Linux

Naturally Linux is a command-line tool that turns natural-language requests into safe, reviewable Linux shell commands. It shows you the proposed command, explains what it does, and runs it only after confirmation.

## Features

- Natural-language → shell command generation
- Command preview and explanation
- Safety checks before execution
- Confirmation before running commands

## Install

```
pip install naturally-linux
```

## Setup

Set your Groq API key:

```
export GROQ_API_KEY="your-key"
```

## Usage

Generate and run a command:

```
naturally-linux run "list files larger than 10MB"
```

Preview with explanation only:

```
naturally-linux run "list files larger than 10MB" --dry-run
```

## License

MIT
