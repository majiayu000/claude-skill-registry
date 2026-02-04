---
name: gemini-cli
description: Google Gemini CLI fundamentals for code analysis, review, and validation. Use when (1) executing gemini commands for code review/analysis, (2) configuring models (gemini-3-flash-preview (default)/gemini-3-pro-preview (complex only)), output formats (text/json/stream-json), or sandbox modes, (3) managing Gemini sessions with /chat save/resume, (4) integrating Gemini into automation scripts and CI/CD pipelines. Do NOT use for orchestration patterns (use gemini-claude-loop instead).
---

# Gemini CLI Skill

## ⚠️ Environment Notice

| Environment | Command Format |
|-------------|----------------|
| Interactive terminal | `gemini` (enters interactive mode) |
| **Claude Code / CI** | `gemini -p "prompt"` (headless mode) |
| **Scripting with JSON** | `gemini -p "prompt" --output-format json` |
| **Stdin input** | `echo "prompt" \| gemini` or `cat file \| gemini -p "analyze"` |

**Non-TTY environments** (Claude Code, CI pipelines) require `-p` flag or stdin input.

## Quick Start

### Headless Mode (Claude Code/CI)
```bash
# Basic review
gemini -p "Review this code for bugs"

# With JSON output for parsing
gemini -p "Analyze this code" --output-format json

# With specific model and directories
gemini -m gemini-3-flash-preview --include-directories ./src,./lib -p "Code analysis"

# Stdin input with prompt
cat src/auth.py | gemini -p "Review for security issues"
```

### JSON Output Parsing
```bash
result=$(gemini -p "Query" --output-format json)
response=$(echo "$result" | jq -r '.response')
```

## Reference Documentation

- **[Commands Reference](references/commands.md)** - Slash commands, @ commands, shell mode
- **[Options Reference](references/options.md)** - Models, output formats, directories, JSON schema
- **[Examples](references/examples.md)** - Code review, CI/CD integration, automation scripts

## Available Models

| Model | Description | Best For |
|-------|-------------|----------|
| `gemini-3-flash-preview` | Fast and efficient (DEFAULT) | Standard reviews, batch operations, general use |
| `gemini-3-pro-preview` | Flagship model | Complex architecture analysis, security audits only |

## Output Formats

| Format | Description | Use Case |
|--------|-------------|----------|
| (default) | Human-readable text | Terminal output |
| `json` | Structured with stats | Script parsing, automation |
| `stream-json` | JSONL events | Real-time monitoring |

### JSON Response Structure
> Full schema: See [Options Reference](references/options.md#json-response-schema)

Key fields: `response` (string), `stats` (object), `error` (optional object)

## Key Options

| Option | Alias | Description |
|--------|-------|-------------|
| `--prompt` | `-p` | Run in headless mode with prompt |
| `--model` | `-m` | Model selection |
| `--output-format` | | Output format (`json`, `stream-json`) |
| `--include-directories` | | Additional context directories (comma-separated) |
| `--yolo` | `-y` | Auto-approve all actions |
| `--sandbox` | `-s` | Sandbox mode (`restrictive`) |
| `--approval-mode` | | Set approval mode (`auto_edit`) |

## Common Patterns

> **Full examples**: See [Examples](references/examples.md) for detailed patterns

### Essential Patterns
```bash
# Code review with output
cat src/auth.py | gemini -p "Review for security issues" > review.txt

# JSON output with jq parsing
result=$(gemini -p "Query" --output-format json)
echo "$result" | jq -r '.response'

# Cross-directory analysis
gemini --include-directories ./backend,./frontend -p "Review API integration"
```

## Timeout Configuration

| Task Type | Recommended Timeout | Claude Code Tool |
|-----------|---------------------|------------------|
| Quick checks | 2 minutes | `timeout: 120000` |
| Standard review | 5 minutes | `timeout: 300000` |
| Deep analysis | **10 minutes** | `timeout: 600000` |

**Recommendation**: Use `timeout: 600000` for complex analysis with `gemini-3-pro-preview`.

## Error Handling

> **Detailed error handling patterns**: See [Examples](references/examples.md#error-handling)

| Error | Cause | Solution |
|-------|-------|----------|
| No output | Missing `-p` flag | Use `gemini -p "prompt"` |
| Empty response | No stdin/prompt | Provide via `-p` or stdin |
| Exit code `1` | General error | Check JSON `.error` field |
| Context too large | Too many files | Use specific paths |
| Permission denied | Sandbox restrictions | Use `--yolo` carefully |

## Best Practices

1. **Use `-p` flag** in Claude Code and CI environments
2. **Use `--output-format json`** for script parsing
3. **Parse with `jq`** for reliable extraction
4. **Check `.error`** in JSON response for error handling
5. **Use `--include-directories`** for multi-directory context
6. **Match model to task**: `gemini-3-flash-preview` for most tasks, `gemini-3-pro-preview` only for complex architecture/security
7. **Set 10-minute timeout** for deep analysis (`timeout: 600000`)
