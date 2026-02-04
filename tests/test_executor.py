"""Tests for command execution."""

from naturally_linux.executor import run_command


def test_run_command_echo():
    stdout, stderr, returncode = run_command("echo hello")
    assert returncode == 0
    assert "hello" in stdout
    assert stderr == ""
