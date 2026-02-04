# Install

## Requirements

- Python 3.13+
- A Groq API key

## Install with UV (recommended)

Install UV (by Astral) and then install the CLI system-wide. See the official UV docs: [UV by Astral](https://docs.astral.sh/uv/)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv tool install naturally-linux
```

## Install from PyPI (pip)

```bash
pip install naturally-linux
```

## Set the API key

Set the Groq API key as an environment variable:

```bash
export GROQ_API_KEY="your-key"
```

You can add this to your shell profile (e.g., `~/.zshrc`).

## Verify

```bash
naturally-linux --help
```
