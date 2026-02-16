# Safety

Naturally Linux applies a basic safety filter before running commands. This reduces the chance of accidental destructive actions.

## Current behavior

The tool flags commands containing patterns like:

- `rm -rf`
- `mkfs`
- `dd if=`
- Fork bombs like `:(){`
- `shutdown` or `reboot`

If a command is flagged, you will be warned with the reason and asked to confirm explicitly.

## Heuristic warnings

The CLI also warns about potentially expensive or system-wide operations, such as:

- Root-level scans like `find /`
- Recursive scans across `/`
- Commands using `sudo`

When detected, the CLI will display a risk level and require explicit confirmation.

## Limitations

This is a simple substring-based check. It can miss risky commands or flag safe ones. Always review the proposed command.

## Planned improvements

- Regex-based rules
- Allow/deny lists by environment
- Context-aware risk analysis
- Structured command parsing
