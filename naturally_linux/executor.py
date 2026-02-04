"""Command execution helpers."""

import subprocess
from typing import Tuple


def run_command(command: str) -> Tuple[str, str, int]:
    """
    Execute a shell command and return (stdout, stderr, returncode).

    TODO:
    - Consider a safer execution strategy (no shell, explicit args).
    - Add timeouts and resource limits.
    """

    result = subprocess.run(
        command,
        shell=True,
        text=True,
        capture_output=True,
    )

    return result.stdout, result.stderr, result.returncode
