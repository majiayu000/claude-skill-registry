---
name: codex-bridge
description: Use when user wants to ask Codex, get GPT's opinion, get a second opinion from OpenAI, compare perspectives, have Codex review code or docs, or let Codex fix/refactor/implement something.
allowed-tools: Bash(node:*), Bash(codex:*), Read, Write
user-invocable: true
model: haiku
---

# Codex Bridge

Call OpenAI's Codex CLI to get responses, reviews, or perform tasks.

## When to Use

Activate when user says:
- "Ask Codex...", "Have Codex...", "Let Codex..."
- "Get GPT's opinion on...", "What does OpenAI think..."
- "Get a second opinion on..."
- "Have Codex review...", "Let Codex fix/refactor/implement..."
- "Compare Claude vs Codex...", "Run this through Codex..."

## Quick Reference

| Flag | When | Example |
|------|------|---------|
| _(none)_ | Opinions, reviews, questions, analysis | `node "$CODEX_BRIDGE" "Review this code" --working-dir "<project>"` |
| `--full-auto` | Fix, refactor, implement, update files | `node "$CODEX_BRIDGE" "Fix errors" --full-auto --working-dir "<project>"` |
| `--model MODEL` | Override model (default: Codex default) | `node "$CODEX_BRIDGE" "Explain" --model gpt-4o --working-dir "<project>"` |
| `--json` | Bridge outputs raw JSON events (debugging) | `node "$CODEX_BRIDGE" "Analyze" --json --working-dir "<project>"` |
| `--timeout MS` | Override 20-minute default timeout | `node "$CODEX_BRIDGE" "Long task" --timeout 2400000 --working-dir "<project>"` |

## Setup

```bash
# Resolve bridge path (one command):
CODEX_BRIDGE=$(ls -1 "$HOME/.claude/plugins/cache/saurun-marketplace/saurun/"*/skills/codex-bridge/codex-bridge.mjs 2>/dev/null | head -1)
```

**CRITICAL:** Always pass `--working-dir` with the project directory. Without it, Codex runs in its install location and can't access project files.

## Decision Logic

| Mode | When |
|------|------|
| Read-only _(no flags)_ | Opinion, explanation, review, comparison, questions |
| `--full-auto` | Modify files. Trigger words: "fix", "refactor", "implement", "update", "change" |

## Handling File Reviews

When user wants Codex to review a file:
1. Read the file content with the Read tool
2. Include content in the prompt to Codex

```bash
node "$CODEX_BRIDGE" "Review this document for feasibility, risks, and suggestions:

---
[FILE CONTENT HERE]
---" --working-dir "/path/to/project"
```

## Response Format

**For opinions/reviews:**
> **Codex (OpenAI) says:**
> [response]

**For comparisons:** Provide your own analysis AND Codex's response, noting differences.

**For file modifications:** After Codex completes, show changes with `git diff`.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Omitting `--working-dir` | Codex can't read project files. Always pass it. |
| Using `--full-auto` for reviews | Read-only is safer for opinions. Only use `--full-auto` when user wants file changes. |
| Sending huge files as CLI args | Bridge handles this automatically (writes to temp file for prompts >7000 chars). |
| Forgetting prerequisites | Codex CLI must be installed (`npm install -g @openai/codex`) and authenticated (`codex login`). |

## Error Handling

If the bridge fails (exit code non-zero), check:
- Codex CLI installed: `which codex` (install: `npm install -g @openai/codex`)
- Authentication valid: `codex login`
- Working directory exists and is accessible
- Timeout: increase with `--timeout MS` (default: 1,200,000ms / 20 min)
