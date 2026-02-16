"""Safety checks for generated shell commands."""

from __future__ import annotations

import re
from typing import Iterable, List, Tuple


_DANGEROUS_RULES: List[Tuple[str, str]] = [
    ("rm -rf", "Recursive delete detected"),
    ("mkfs", "Filesystem format detected"),
    ("dd if=", "Raw disk write detected"),
    (":(){", "Fork bomb pattern detected"),
    ("shutdown", "System shutdown detected"),
    ("reboot", "System reboot detected"),
]

_HEURISTIC_RULES: List[Tuple[re.Pattern[str], str, str]] = [
    (re.compile(r"\bfind\s+/\b"), "Command scans from filesystem root", "HIGH"),
    (re.compile(r"\bdu\s+-a\s+/\b"), "Disk usage across filesystem root", "HIGH"),
    (re.compile(r"\b(sudo)\b"), "Command requires elevated privileges", "MEDIUM"),
    (re.compile(r"\b/\b.*-R\b"), "Recursive operation across root", "HIGH"),
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


def heuristic_warnings(command: str) -> List[Tuple[str, str]]:
    warnings: List[Tuple[str, str]] = []
    for regex, message, level in _HEURISTIC_RULES:
        if regex.search(command):
            warnings.append((message, level))
    return warnings


def heuristic_risk_level(warnings: List[Tuple[str, str]]) -> str:
    if not warnings:
        return "LOW"
    if any(level == "HIGH" for _, level in warnings):
        return "HIGH"
    return "MEDIUM"
