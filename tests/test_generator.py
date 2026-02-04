"""Tests for command generator."""

from types import SimpleNamespace

import naturally_linux.generator as generator


class _FakeGroq:
    """Minimal fake Groq client for tests."""

    def __init__(self, api_key: str):
        self.api_key = api_key

    class chat:
        class completions:
            @staticmethod
            def create(*_args, **_kwargs):
                return SimpleNamespace(
                    choices=[
                        SimpleNamespace(
                            message=SimpleNamespace(content="ls -la")
                        )
                    ]
                )


def test_generate_command_returns_string(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "test-key")
    monkeypatch.setattr(generator, "Groq", _FakeGroq)

    result = generator.generate_command("list files")
    assert isinstance(result, str)
    assert result == "ls -la"
