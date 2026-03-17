---
name: using-claude-code-cli
description: |
  Invoke Claude Code CLI from Python orchestrators and shell scripts. Use when asked to
  "spawn claude as subprocess", "automate claude cli", "run claude headless",
  "configure --allowedTools", "set up claude hooks", or "parallel claude invocation".
  Covers permissions, directory access (--add-dir), hooks, sandbox mode, and async patterns.
license: MIT
allowed-tools:
  - Read
  - Bash
triggers:
  - claude cli
  - claude subprocess
  - claude permissions
  - --allowedTools
  - --add-dir
  - --settings
  - claude automation
  - spawn claude
  - claude orchestration
  - headless claude
  - parallel agents
metadata:
  version: 1.1.0
  category: cli-automation
  author: Book Generator v2 Project
  tags:
    - cli
    - automation
    - subprocess
    - permissions
    - hooks
---

# Using Claude Code CLI

Patterns for programmatically invoking Claude Code CLI from orchestrators, scripts, and automation pipelines.

## Contents

- [Quick Start Checklist](#quick-start-checklist)
- [Essential Commands](#essential-commands)
- [Core CLI Flags](#core-cli-flags)
- [Sandbox Mode](#sandbox-mode)
- [Validation](#validation)
- [Troubleshooting](#troubleshooting)
- [When Not to Use](#when-not-to-use)

## Quick Start Checklist

Copy and track as you work:

```
CLI Automation Setup:
- [ ] 1. Identify required tools, add to --allowedTools
- [ ] 2. List directories Claude needs, add to --add-dir
- [ ] 3. Choose pattern: sync, async, or parallel (see references/)
- [ ] 4. Configure hooks if logging/monitoring needed
- [ ] 5. Enable sandbox mode for untrusted operations
- [ ] 6. Add fallback strategy if using OpenCode backup
- [ ] 7. Test with simple prompt before full automation
- [ ] 8. Validate setup (see Validation section)
```

## Essential Commands

**Minimal automation:**
```bash
claude -p "Your prompt" --allowedTools Write Read Edit --max-turns 5
```

**Full automation:**
```bash
claude \
  --model sonnet \
  --add-dir /path/to/skills \
  --add-dir /path/to/templates \
  --allowedTools Write Read Edit Bash Task \
  --output-format json \
  -p "Your automation prompt"
```

**With settings JSON:**
```bash
claude --settings '{"hooks":{},"sandbox":{"enabled":true}}' -p "prompt"
```

## Core CLI Flags

| Flag | Purpose | Example |
|------|---------|---------|
| `-p` | Non-interactive mode (required) | `claude -p "query"` |
| `--allowedTools` | Pre-approve tools | `--allowedTools Write Read Bash` |
| `--add-dir` | Grant directory access | `--add-dir ../lib` |
| `--settings` | Pass hooks/permissions JSON | `--settings ./settings.json` |
| `--model` | Select model | `--model sonnet` |
| `--output-format` | Output: text, json, stream-json | `--output-format json` |
| `--max-turns` | Limit agentic turns | `--max-turns 5` |

**Recommended tools for automation:**
- Core: `Write`, `Read`, `Edit`, `Glob`, `Grep`, `LS`
- Automation: `Bash`, `Task`, `Skill`
- Web: `WebFetch`, `WebSearch`

**MCP tools require full path:**
```bash
--allowedTools "mcp__perplexity-ask__perplexity_ask"
--allowedTools "mcp__context7__get-library-docs"
```

See [references/cli-reference.md](references/cli-reference.md) for complete flag documentation.

## Sandbox Mode

Enable sandbox for safe file operations:

**Via settings JSON:**
```bash
claude --settings '{"sandbox":{"enabled":true,"autoAllowBashIfSandboxed":true}}' -p "prompt"
```

**Via stdin (pass /sandbox before prompt):**
```python
stdin_content = "/sandbox\nYour actual prompt"
subprocess.run(["claude", "-p"], input=stdin_content, text=True)
```

See [references/hooks-examples.md](references/hooks-examples.md) for full sandbox options.

## Validation

Before full automation, verify setup works:

```bash
# 1. Test tool pre-approval (should complete without prompts)
claude -p "Create file test.txt with 'hello'" --allowedTools Write

# 2. Test directory access
claude -p "List files in /path/to/dir" --add-dir /path/to/dir --allowedTools LS

# 3. Test JSON output
claude -p "Return {\"status\": \"ok\"}" --output-format json | jq .

# 4. Test hooks (check log file after)
claude --settings '{"hooks":{...}}' -p "Simple task" --allowedTools Read
```

If any step fails, see [Troubleshooting](#troubleshooting).

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Permission prompts appearing | Verify tool names match exactly (case-sensitive); MCP tools need full path |
| Hooks not firing | Check script is executable (`chmod +x`), has shebang, timeout not exceeded |
| Subprocess hangs | Add timeout; check if waiting for permission (missing --allowedTools) |
| Working directory issues | Use absolute paths in --add-dir; set cwd in subprocess |
| JSON parse errors | Use --output-format json; see [json-extraction.md](references/json-extraction.md) |

## When Not to Use

This skill is for **subprocess invocation**. Do not use for:
- Interactive Claude sessions (use Claude directly)
- API integration (use Claude SDK/API)
- MCP server setup (use `claude mcp` command)

## Reference Files

| File | Contents |
|------|----------|
| [cli-reference.md](references/cli-reference.md) | Complete CLI commands and flags |
| [subprocess-patterns.md](references/subprocess-patterns.md) | Python sync/async/parallel patterns |
| [hooks-examples.md](references/hooks-examples.md) | Hook scripts and settings JSON |
| [json-extraction.md](references/json-extraction.md) | Parsing JSON from CLI output |
| [orchestrator_example.py](references/orchestrator_example.py) | Complete Python orchestrator class |

## OpenCode CLI Fallback

When using OpenCode as fallback, note key differences:

| Feature | Claude CLI | OpenCode CLI |
|---------|------------|--------------|
| Headless | `claude -p "prompt"` | `opencode run "prompt"` |
| Model | `--model sonnet` | `--model provider/model` |
| Settings | `--settings JSON` | Not supported |
| Add dirs | `--add-dir /path` | Not supported |

**Try-Claude-then-OpenCode pattern:**
```python
import subprocess

def invoke_with_fallback(prompt: str, timeout: int = 300) -> str:
    """Try Claude CLI first, fall back to OpenCode on failure."""
    try:
        result = subprocess.run(
            ["claude", "-p", prompt, "--allowedTools", "Write", "Read"],
            capture_output=True, text=True, timeout=timeout
        )
        if result.returncode == 0:
            return result.stdout
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass  # Fall through to OpenCode

    result = subprocess.run(
        ["opencode", "run", prompt],
        capture_output=True, text=True, timeout=timeout
    )
    return result.stdout
```

See [subprocess-patterns.md](references/subprocess-patterns.md) for advanced patterns.
