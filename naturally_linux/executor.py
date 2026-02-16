"""Command execution helpers."""

import subprocess
from typing import Tuple


def run_command(command: str, timeout_seconds: float = 60.0) -> Tuple[str, str, int]:
    """
    Execute a shell command and return (stdout, stderr, returncode).

    TODO:
    - Consider a safer execution strategy (no shell, explicit args).
    - Add timeouts and resource limits.
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            text=True,
            capture_output=True,
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired:
        return "", "Command timed out.", 124

    return result.stdout, result.stderr, result.returncode
