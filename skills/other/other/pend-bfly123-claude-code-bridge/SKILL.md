---
name: pend
description: View latest reply from AI provider (gemini/codex/opencode/droid/claude).
metadata:
  short-description: View latest AI provider reply
---

# Pend - View Latest Reply

View the latest reply from specified AI provider.

## Usage

The first argument must be the provider name:
- `gemini` - View Gemini reply
- `codex` - View Codex reply
- `opencode` - View OpenCode reply
- `droid` - View Droid reply
- `claude` - View Claude reply

Optional: Add a number N to show the latest N conversations.

## Execution (MANDATORY)

```bash
pend $ARGUMENTS
```

## Examples

- `/pend gemini`
- `/pend codex 3`
- `/pend claude`
