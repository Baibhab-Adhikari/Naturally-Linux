"""Config helpers for Naturally Linux."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Optional


CONFIG_DIR_NAME = "naturally-linux"
CONFIG_FILE_NAME = "config.json"


def _config_dir() -> Path:
    base_dir = os.environ.get("XDG_CONFIG_HOME")
    if base_dir:
        return Path(base_dir) / CONFIG_DIR_NAME
    return Path.home() / ".config" / CONFIG_DIR_NAME


def _config_path() -> Path:
    return _config_dir() / CONFIG_FILE_NAME


def _ensure_config_dir() -> Path:
    config_dir = _config_dir()
    config_dir.mkdir(parents=True, exist_ok=True)
    try:
        os.chmod(config_dir, 0o700)
    except OSError:
        pass
    return config_dir


def load_config() -> dict:
    path = _config_path()
    if not path.exists():
        return {}
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError):
        return {}


def save_config(data: dict) -> None:
    _ensure_config_dir()
    path = _config_path()
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)


def get_api_key() -> Optional[str]:
    env_key = os.environ.get("GROQ_API_KEY")
    if env_key:
        return env_key
    config = load_config()
    return config.get("groq_api_key")


def set_api_key(value: str) -> None:
    config = load_config()
    config["groq_api_key"] = value
    save_config(config)


def delete_api_key() -> bool:
    config = load_config()
    if "groq_api_key" not in config:
        return False
    config.pop("groq_api_key", None)
    save_config(config)
    return True


def config_path() -> Path:
    return _config_path()
