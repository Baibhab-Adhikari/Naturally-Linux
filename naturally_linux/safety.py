"""Safety checks for generated shell commands."""

from typing import Iterable


def _dangerous_patterns() -> Iterable[str]:
    """
    Return a small blacklist of patterns that should require explicit approval.

    TODO:
    - Replace with a richer ruleset (regex, parsing, allow/deny lists).
    - Add OS-specific checks and context-aware risk assessment.
    """

    return [
        "rm -rf",  # recursive delete
        "mkfs",    # format filesystem
        "dd if=",  # raw disk writes
        ":(){",    # fork bomb
        "shutdown",
        "reboot",
    ]


def is_safe_command(command: str) -> bool:
    """Return True if the command appears safe, False otherwise."""

    lowered = command.lower()
    return not any(pattern in lowered for pattern in _dangerous_patterns())
