---
name: gemini
description: Run Google Gemini CLI as a subagent for second opinions, code reviews, and questions. Use when you want a different AI model's perspective.
---

# Gemini Subagent

Run Google Gemini CLI for second opinions and external reviews.

## Availability Check

Before using Gemini, verify it's installed:

```bash
which gemini >/dev/null 2>&1 || echo "GEMINI_NOT_INSTALLED"
```

If not installed, inform the user: "Gemini CLI is not installed. Skipping Gemini review."

## API Key

Gemini requires `GEMINI_API_KEY` in the environment. Load it from the `.env` file in the current working directory (the folder your current agent session is running from):

```bash
GEMINI_API_KEY=$(grep '^GEMINI_API_KEY=' .env 2>/dev/null | cut -d= -f2-)
export GEMINI_API_KEY
```

If `.env` doesn't exist or doesn't contain `GEMINI_API_KEY`, inform the user: "GEMINI_API_KEY not found in .env file."

## Execution Pattern

```bash
GEMINI_API_KEY=$(grep '^GEMINI_API_KEY=' .env 2>/dev/null | cut -d= -f2-) gemini -p "$PROMPT" --yolo 2>&1
```

### Flags

| Flag | Purpose |
|------|---------|
| `-p` / `--prompt` | Non-interactive mode with direct prompt |
| `--yolo` | Auto-approve all tool calls without prompts |
| `2>&1` | Capture both stdout and stderr |

### Timeout

Gemini can take several minutes for complex prompts. Use 15 minute timeout:

```bash
timeout 900 gemini -p "$PROMPT" --yolo 2>&1
```

## Usage Examples

### Simple Question

```bash
timeout 900 gemini -p "What are the tradeoffs between Redis and Memcached for session storage?" --yolo 2>&1
```

### Code Review

```bash
DIFF=$(git diff main...HEAD)
timeout 900 gemini -p "Review this diff for issues:

$DIFF

List concerns with severity (blocking/important/nice-to-have)." --yolo 2>&1
```

### With Working Directory

Gemini runs in current directory by default. Change directory before running:

```bash
cd /path/to/repo && timeout 900 gemini -p "Analyze the architecture of this codebase" --yolo 2>&1
```

### GitHub PR Review

Gemini has access to `gh` CLI when tools are enabled. Pass the PR URL and let it fetch the diff:

```bash
timeout 900 gemini -p "Review this PR: https://github.com/owner/repo/pull/123

Use gh CLI to get the diff and review for issues." --yolo 2>&1
```

## Notes

- Gemini provides a different perspective from Claude and Codex
- Each call is stateless - no conversation continuity
- `--yolo` mode auto-approves tool use (shell commands, file reads, etc.)
- API costs apply per call
