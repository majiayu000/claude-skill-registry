---
name: headless-mode
description: Guide for using Claude Code programmatically via CLI flags and SDKs. Use for automation, CI/CD pipelines, scripting, and building tools on top of Claude Code. Covers --print mode, output formats, session management, and SDK integration.
allowed-tools: ["Read", "Write", "Bash", "Glob"]
---

# Headless Mode

Run Claude Code programmatically for automation, CI/CD, and scripting.

## Quick Reference

| Mode | Command | Use Case |
|------|---------|----------|
| CLI (simple) | `claude -p "prompt"` | One-shot tasks, scripts |
| CLI (structured) | `claude -p "prompt" --output-format json` | Parsing responses |
| TypeScript SDK | `@anthropic-ai/claude-code` | Full programmatic control |
| Python SDK | `claude-code-sdk` | Python automation |

## Core Concept

The `-p` (or `--print`) flag runs Claude Code non-interactively. All CLI options work with `-p`, enabling automated workflows without human interaction.

```bash
claude -p "Explain what this project does"
```

## Essential Flags

| Flag | Purpose | Example |
|------|---------|---------|
| `-p`, `--print` | Run non-interactively | `claude -p "query"` |
| `--output-format` | Response format | `json`, `stream-json`, `text` |
| `--allowedTools` | Auto-approve tools | `"Bash,Read,Edit"` |
| `--max-turns` | Limit agent turns | `--max-turns 5` |
| `--continue` | Continue last session | `claude -p "..." --continue` |
| `--resume` | Resume specific session | `--resume $SESSION_ID` |

## Output Formats

### Text (Default)

Plain text output for simple tasks:

```bash
claude -p "Summarize auth.py"
```

### JSON (Structured)

Get metadata with response:

```bash
claude -p "Analyze this code" --output-format json
```

Returns:
```json
{
  "result": "Analysis text...",
  "session_id": "abc123",
  "usage": { "input_tokens": 100, "output_tokens": 50 }
}
```

### Stream JSON (Real-time)

Newline-delimited JSON for streaming:

```bash
claude -p "Generate report" --output-format stream-json
```

## Tool Auto-Approval

### Basic Approval

Allow specific tools without prompting:

```bash
claude -p "Fix the failing tests" --allowedTools "Bash,Read,Edit"
```

### Granular Bash Commands

Restrict to specific bash patterns:

```bash
claude -p "Create a commit for staged changes" \
  --allowedTools "Bash(git diff:*),Bash(git log:*),Bash(git commit:*)"
```

### Skip All Permissions (Dangerous)

Use only in trusted, sandboxed environments:

```bash
claude -p "Deploy to staging" --dangerously-skip-permissions
```

## Session Management

### Continue Last Session

```bash
claude -p "Review this codebase"
claude -p "Focus on the database layer" --continue
claude -p "Summarize findings" --continue
```

### Resume Specific Session

```bash
# Capture session ID
session_id=$(claude -p "Start review" --output-format json | jq -r '.session_id')

# Later: resume that session
claude -p "Continue the review" --resume "$session_id"
```

### Fork a Session

Create a new branch from an existing session:

```bash
claude -p "Try alternative approach" --resume $SESSION_ID --fork-session
```

## System Prompt Customization

### Append Instructions

Keep default behavior, add context:

```bash
claude -p "Review this PR" \
  --append-system-prompt "Focus on security vulnerabilities"
```

### Replace System Prompt

Full control over Claude's behavior:

```bash
claude -p "Analyze code" \
  --system-prompt "You are a security auditor. Only report vulnerabilities."
```

### Load from File

```bash
claude -p "Review code" --system-prompt-file ./prompts/security-review.txt
```

## Structured Output (JSON Schema)

Force output to match a schema:

```bash
claude -p "Extract function names from utils.py" \
  --output-format json \
  --json-schema '{"type":"object","properties":{"functions":{"type":"array","items":{"type":"string"}}},"required":["functions"]}'
```

Response includes `structured_output` field:

```json
{
  "result": "...",
  "structured_output": {
    "functions": ["parseDate", "formatCurrency", "validateEmail"]
  }
}
```

## Common Patterns

### Code Review

```bash
gh pr diff "$PR_NUMBER" | claude -p \
  "Review this PR for bugs and improvements" \
  --output-format json
```

### Test Fixing

```bash
claude -p "Run tests and fix failures" \
  --allowedTools "Bash,Read,Edit" \
  --max-turns 10
```

### Documentation Generation

```bash
claude -p "Generate API documentation for src/api/" \
  --allowedTools "Read,Glob,Grep,Write"
```

### Batch Processing

```bash
for file in src/*.ts; do
  claude -p "Add JSDoc comments to $file" \
    --allowedTools "Read,Edit"
done
```

## Key Differences from Interactive Mode

| Feature | Interactive | Headless (`-p`) |
|---------|-------------|-----------------|
| Slash commands | Available | Not available |
| Permission prompts | Interactive | Auto-approve or skip |
| Output | Formatted | Raw text/JSON |
| Session | Persistent | One-shot (unless --continue) |

## Reference Files

| File | Contents |
|------|----------|
| [CLI-FLAGS.md](./CLI-FLAGS.md) | Complete CLI flag reference |
| [SDK.md](./SDK.md) | TypeScript and Python SDK usage |
| [EXAMPLES.md](./EXAMPLES.md) | Practical automation examples |

## Troubleshooting

### No Output

Check if Claude is waiting for permission:
```bash
claude -p "query" --verbose
```

Add `--allowedTools` or `--dangerously-skip-permissions`.

### JSON Parsing Errors

Use `jq` to extract fields:
```bash
claude -p "query" --output-format json | jq -r '.result'
```

### Session Not Found

Sessions are directory-specific. Run from the same directory or use `--session-id` with a UUID.

## Best Practices

1. **Use JSON output** for automation - easier to parse
2. **Limit tools** to only what's needed - security first
3. **Set max-turns** for predictable execution time
4. **Capture session IDs** for multi-turn workflows
5. **Use --append-system-prompt** to add context without losing defaults
