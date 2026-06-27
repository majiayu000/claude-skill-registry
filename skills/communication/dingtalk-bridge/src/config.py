#!/usr/bin/env python3
"""Configuration loader for dingtalk-bridge skill.

Priority: environment variables > config.json > defaults.

Required:
  DINGTALK_APP_KEY    or config.json "app_key"
  DINGTALK_APP_SECRET or config.json "app_secret"

Optional:
  DINGTALK_CONV_FILE  — path to conversation metadata JSON (default: <skill>/data/conv.json)
  DINGTALK_WORKDIR    — working directory for claude CLI (default: cwd)
  DINGTALK_CLAUDE_BIN — path to claude binary (default: claude)
  DINGTALK_MAX_REPLY  — max reply length in chars (default: 3000)
  DINGTALK_KEEPALIVE  — WebSocket keepalive interval in seconds (default: 20)
"""

import json
import os
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
CONFIG_FILE = SKILL_DIR / "config.json"
DEFAULT_CONV_FILE = SKILL_DIR / "data" / "conv.json"


def _load_file_config():
    if CONFIG_FILE.exists():
        return json.loads(CONFIG_FILE.read_text())
    return {}


def get(key, default=None):
    env_key = f"DINGTALK_{key.upper()}"
    val = os.environ.get(env_key)
    if val is not None:
        return val
    file_cfg = _load_file_config()
    if key in file_cfg:
        return file_cfg[key]
    return default


def require(key):
    val = get(key)
    if val is None:
        env_key = f"DINGTALK_{key.upper()}"
        raise RuntimeError(
            f"Missing required config: set {env_key} env var or add '{key}' to {CONFIG_FILE}"
        )
    return val


def app_key():
    return require("app_key")


def app_secret():
    return require("app_secret")


def conv_file():
    return Path(get("conv_file", str(DEFAULT_CONV_FILE)))


def workdir():
    return get("workdir", os.getcwd())


def claude_bin():
    return get("claude_bin", "claude")


def max_reply_len():
    return int(get("max_reply", "3000"))


def keepalive_interval():
    return int(get("keepalive", "20"))
