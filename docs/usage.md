# Usage

## Generate and run a command

```bash
naturally-linux "find files modified today"
```

The CLI will:

1. Generate a command from your prompt
2. Perform a safety check
3. Show the proposed command
4. Ask for confirmation
5. Execute and display output

## Dry run

Use `--dry-run` to preview the command and receive an explanation without running it:

```bash
naturally-linux "list directories" --dry-run
```

You can still choose to execute after reviewing the explanation.

## Auto-approve

Skip confirmation with `--yes`:

```bash
naturally-linux "list files" --yes
```

Use this carefully. It bypasses the confirmation prompt.
