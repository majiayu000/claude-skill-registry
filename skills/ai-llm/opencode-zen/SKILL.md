---
name: opencode-zen
description: Invoke the 'opencode' CLI in headless mode for AI-powered code analysis, reviews, and second opinions. Use when you need a different AI perspective, the user mentions opencode, or requests batch code analysis.
allowed-tools: Bash(opencode:*), Read, Write, Grep, Glob
---

# Opencode CLI Skill

## Overview

This skill enables invocation of the `opencode` CLI in headless mode for automated AI analysis, code reviews, and generating insights without launching the TUI.

Use opencode for:
- Second opinions on code or architecture
- Batch analysis of multiple files
- Alternative AI perspectives (different model families)
- Scenarios where the user explicitly requests opencode

## Available Providers

Check current providers with `opencode models`. Common options:

| Provider | Models | Notes |
|----|----|----|
| `groq/*` | qwen-qwq-32b, llama-3.3-70b-versatile, deepseek-r1-distill-llama-70b | Fast inference via Groq |
| `opencode/*` | big-pickle, gpt-5-nano, grok-code | Opencode's hosted models |

**Note**: The `opencode-zen` alias referenced in examples is a custom provider configuration. Until configured, substitute with an available model (e.g., `groq/qwen-qwq-32b`).

## Instructions

### Basic Headless Invocation

```bash
# Basic prompt (uses default model)
opencode run "Your prompt here"

# With specific model
opencode run -m groq/qwen-qwq-32b "Your prompt here"

# With file context
opencode run -m groq/llama-3.3-70b-versatile "Analyze this file" -f src/main.rs

# Multiple files
opencode run "Compare these two implementations" -f src/v1.rs -f src/v2.rs
```

### Output Control

```bash
# JSON output for parsing
opencode run "Your prompt" --format json

# Save output to file
opencode run "Your prompt" > output.txt

# Show logs for debugging
opencode run "Your prompt" --print-logs
```

### Configuration Options

| Option | Description | Example |
|----|----|----|
| `run [message]` | Execute in headless mode | `opencode run "Analyze this"` |
| `-m, --model` | Specify provider/model | `-m groq/qwen-qwq-32b` |
| `-f, --file` | Attach file(s) to context | `-f file.py -f test.py` |
| `--format` | Output format (default, json) | `--format json` |
| `--print-logs` | Print logs to stderr | `--print-logs` |
| `-s, --session` | Continue a specific session | `-s <session-id>` |
| `-c, --continue` | Continue last session | `-c` |
| `--agent` | Use a specific agent | `--agent code-review` |

## Examples

### Example 1: Code Review

```bash
# Get a second opinion on a module
opencode run -m groq/qwen-qwq-32b \
  "Review this code for bugs, performance issues, and maintainability. Be critical." \
  -f boundary/commands.ss \
  > docs/peer-review/opencode-commands-review.md
```

### Example 2: Batch Analysis

```bash
# Analyze multiple files for potential issues
for file in core/base/*.ss; do
    echo "Analyzing $file..."
    opencode run -m groq/llama-3.3-70b-versatile \
      "Check for: 1) potential runtime errors, 2) missing edge cases, 3) unclear logic" \
      -f "$file" --format json >> reports/core-base-audit.json
done
```

### Example 3: Tech Debt Report

```bash
# Comprehensive tech debt assessment
opencode run -m groq/deepseek-r1-distill-llama-70b \
  "Analyze this codebase for technical debt. Identify: duplicated code, missing tests, complex functions, outdated patterns. Prioritize by impact." \
  -f core/types/*.ss \
  > reports/opencode-tech-debt-types.md
```

### Example 4: Architecture Review

```bash
# Get architectural feedback
opencode run -m groq/qwen-qwq-32b \
  "Review this module's architecture. What are the design trade-offs? What would you change?" \
  -f core/lang/eval.ss -f core/lang/compile.ss \
  > reports/lang-architecture-review.md
```

### Example 5: Multi-turn Session

```bash
# Start a session
opencode run -m groq/qwen-qwq-32b "Explain the type inference algorithm" -f core/types/infer.ss

# Continue the conversation
opencode run -c "What are the edge cases I should test?"

# Or by session ID
opencode run -s abc123 "Show me example inputs that would fail"
```

## Best Practices

1. **Model Selection**: Use `groq/*` models for speed, `opencode/*` for variety
2. **Use JSON for Scripts**: `--format json` for any automated processing
3. **File Context**: Always use `-f` rather than piping file contents for better context handling
4. **Session Continuity**: Use `-c` or `-s` for follow-up questions
5. **Parallel Execution**: Run multiple `opencode run` commands in parallel for batch work (they're stateless unless using sessions)

## Piping and Composition

```bash
# Analyze command output
opencode run "Explain these test failures" -f <(npm test 2>&1 | tail -50)

# Chain with jq for JSON processing
opencode run "List all functions" -f src/utils.ts --format json | jq -r '.response'

# Use heredoc for complex prompts
opencode run -m groq/qwen-qwq-32b << 'EOF'
Review this code with focus on:
1. Security vulnerabilities
2. Performance bottlenecks
3. Code clarity
EOF
```

## Integration with The Fold

When using opencode within The Fold:

1. **Second Opinions**: Use for architectural reviews alongside Gemini - different model families catch different issues
2. **Document Results**: Save valuable insights to `docs/peer-review/` or `reports/`
3. **Forum Integration**: Post summaries via `(msg 'engineering ...)` for team visibility
4. **Batch Workflows**: Use in maintenance scripts for periodic code health checks

## Comparison with Gemini CLI

| Feature | opencode | gemini |
|----|----|----|
| Headless flag | `run` subcommand | `-p` flag |
| File context | `-f file.ss` | `--include-directories dir` |
| Model selection | `-m provider/model` | `-m model-name` |
| JSON output | `--format json` | `--output-format json` |
| Sessions | `-s <id>` or `-c` | N/A |

Both tools are useful for different perspectives - use them together for comprehensive review coverage.
