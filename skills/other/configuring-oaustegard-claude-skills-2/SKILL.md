---
name: configuring
description: Universal environment variable loader for AI agent environments. Loads secrets and config from Claude.ai, Claude Code, OpenAI Codex, Jules, and standard .env files.
metadata:
  version: 2.0.0
  replaces: api-credentials, getting-env
---

# Configuring

Unified configuration management across AI coding environments. Load environment variables, secrets, and other opinionated configuration setups from any AI coding platform.

## Quick Start

```python
import sys
sys.path.insert(0, '/path/to/claude-skills')  # or wherever skills are installed
from configuring import get_env, detect_environment

# Get a variable (searches all sources automatically)
token = get_env("TURSO_TOKEN", required=True)

# With default
port = get_env("PORT", default="8080")

# What environment are we in?
env = detect_environment()  # "claude.ai", "claude-code-desktop", "codex", "jules", etc.
```

## Supported Environments

| Environment | Config Sources |
|-------------|----------------|
| **Claude.ai Projects** | `/mnt/project/*.env`, `/mnt/project/*-token.txt` |
| **Claude Code** | `~/.claude/settings.json` (`env` block), `.claude/settings.json` |
| **OpenAI Codex** | `~/.codex/config.toml`, setup script → `~/.bashrc`, `shell_snapshots/*.sh` |
| **Jules** | Environment settings UI, `.env` in repo |
| **Universal** | `os.environ`, `.env`, `.env.local` |

## API Reference

```python
# Core
get_env(key, default=None, *, required=False, validator=None) -> str | None
load_env(path) -> dict[str, str]           # Load specific file
load_all(force_reload=False) -> dict       # Load all sources

# Utilities
detect_environment() -> str                 # Current platform
mask_secret(value, show_chars=4) -> str    # Safe logging
debug_info() -> dict                        # Troubleshooting
get_loaded_sources() -> list[str]          # What was checked
```

## Credential File Formats

**`.env` files** (KEY=value):
```
TURSO_TOKEN=eyJhbGciOiJFZERTQSI...
EMBEDDING_API_KEY=sk-svcacct-...
```

**Single-value files** (`*-token.txt`, `*-key.txt`):
```
eyJhbGciOiJFZERTQSI...
```
Filename becomes key: `turso-token.txt` → `TURSO_TOKEN`

**Claude Code settings.json**:
```json
{
  "env": {
    "TURSO_TOKEN": "eyJhbGciOiJFZERTQSI..."
  }
}
```

## Priority Order

Later sources override earlier:
1. OS environment variables
2. Platform-specific sources (detected automatically)
3. `.env` files in cwd
4. OS environment variables (again - explicit exports always win)

## Debugging

```python
import sys
sys.path.insert(0, '/path/to/claude-skills')
from configuring import debug_info
print(debug_info())
# {'environment': 'claude.ai', 'sources': ['os.environ', 'claude.ai:/mnt/project/'], ...}
```

CLI:
```bash
cd /path/to/claude-skills/configuring
python scripts/getting_env.py                    # Show debug info
python scripts/getting_env.py TURSO_TOKEN        # Get specific key
```

## Migration from api-credentials / getting-env

Replace:
```python
# Old (api-credentials)
from credentials import get_anthropic_api_key
key = get_anthropic_api_key()

# Old (getting-env)
from getting_env import get_env
key = get_env("ANTHROPIC_API_KEY")

# New (configuring)
import sys
sys.path.insert(0, '/path/to/claude-skills')
from configuring import get_env
key = get_env("ANTHROPIC_API_KEY", required=True)
```
