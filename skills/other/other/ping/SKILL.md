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

```powershell
ping $ARGUMENTS
```

## Examples

- `/ping gemini`
- `/ping codex`
- `/ping claude`
