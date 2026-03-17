---
name: ping
description: Test connectivity with AI provider (gemini/codex/opencode/droid/claude).
metadata:
  short-description: Test AI provider connectivity
---

# Ping AI Provider

Test connectivity with specified AI provider.

## Usage

The first argument must be the provider name:
- `gemini` - Test Gemini
- `codex` - Test Codex
- `opencode` - Test OpenCode
- `droid` - Test Droid
- `claude` - Test Claude

## Execution (MANDATORY)

**Windows Native - use ccb-ping to avoid conflict with system ping:**
```
Bash(ccb-ping $PROVIDER)
```

**Linux/macOS/WSL:**
```
Bash(ping $PROVIDER)
```

IMPORTANT: On Windows, the system `PING.EXE` takes priority. Use `ccb-ping` wrapper instead.

## Examples

- `/ping gemini`
- `/ping codex`
- `/ping claude`
