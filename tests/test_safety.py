"""Tests for safety checks."""

from naturally_linux.safety import is_safe_command


def test_is_safe_command_allows_benign():
    assert is_safe_command("ls -la") is True


def test_is_safe_command_blocks_dangerous():
    assert is_safe_command("rm -rf /") is False
