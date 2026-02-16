"""Safety checks for generated shell commands."""

from __future__ import annotations

from typing import List, Tuple


_DANGEROUS_RULES: List[Tuple[str, str]] = [
    ("rm -rf", "Recursive delete detected"),
    ("mkfs", "Filesystem format detected"),
    ("dd if=", "Raw disk write detected"),
    (":(){", "Fork bomb pattern detected"),
    ("shutdown", "System shutdown detected"),
    ("reboot", "System reboot detected"),
]


def is_safe_command(command: str) -> bool:
    """Return True if the command appears safe, False otherwise."""

    return not unsafe_reasons(command)


def unsafe_reasons(command: str) -> List[str]:
    lowered = command.lower()
    reasons = []
    for pattern, reason in _DANGEROUS_RULES:
        if pattern in lowered:
            reasons.append(reason)
    return reasons
