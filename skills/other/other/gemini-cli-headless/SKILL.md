---
name: mastering-gemini-cli
description: Build headless automation and agentic workflows with Google's Gemini CLI. Covers approval modes (default, auto_edit, yolo), file permission model, Edit vs WriteFile tool selection, smartEdit configuration, GEMINI.md context files, settings.json hierarchy, and MCP server integration. Use when building CI/CD pipelines with Gemini, debugging "0 occurrences found" edit failures, configuring --approval-mode for automation, creating long-running agents with --resume, or integrating external services via Model Context Protocol.
---

# Gemini CLI Agentic Systems

Build headless automation with Google's Gemini CLI.

> **Compatibility:** Gemini CLI 1.x. Features may differ in future versions.

## Quick Start

```bash
# Basic headless invocation
gemini -p "Refactor auth.js to use async/await" --approval-mode auto_edit

# Pipe input for context
git diff --staged | gemini -p "Generate semantic commit message"

# JSON output for scripts
gemini -p "List TODOs in src/" --output-format json --include-directories src
```

## Headless Checklist

Before any automation task:

```
- [ ] Set --approval-mode (auto_edit or yolo)
- [ ] Enable smartEdit in .gemini/settings.json
- [ ] Scope file access with --include-directories
- [ ] Choose output format (json for parsing)
- [ ] Add --resume for multi-step workflows
```

## Approval Mode Decision

| Mode | Command | File Ops | Shell Cmds | Use When |
|------|---------|----------|------------|----------|
| default | (none) | ❌ Prompts | ❌ Prompts | Interactive only |
| auto_edit | `--approval-mode auto_edit` | ✅ Auto | ❌ Prompts | Code refactoring |
| yolo | `--approval-mode yolo` | ✅ Auto | ✅ Auto | Sandboxed CI/CD |

**Rule:** Never use `yolo` outside containers or ephemeral environments.

### Least Privilege Pattern

Restrict capabilities with `--allowed-tools`:

```bash
# Documentation agent: read + write only, no shell
gemini -p "Update README from source" \
  --approval-mode yolo \
  --allowed-tools "ReadFile,WriteFile"

# Analysis agent: read only
gemini -p "Find security issues in src/" \
  --approval-mode auto_edit \
  --allowed-tools "ReadFile"
```

## Tool Selection

| Task | Tool | Rationale |
|------|------|-----------|
| Create new file | WriteFile | No existing content |
| Rewrite small file (<50 lines) | WriteFile | Simpler than surgical edit |
| Modify existing code | Edit | Preserves unrelated content |
| Fix specific function | Edit | Surgical precision |

### Edit Tool Reliability

The Edit tool uses exact string matching. Common failure:

```
Error: 0 occurrences found for old_string
```

**Cause:** Model hallucinated whitespace, tabs, or characters.

**Fix:** Enable smartEdit (fuzzy matching):

```json
// .gemini/settings.json
{
  "useSmartEdit": true
}
```

See [tools.md](references/tools.md) for detailed patterns.

## File Access Model

Gemini uses **explicit consent**—agent sees only referenced files.

### Expanding Visibility

```bash
# Single directory
--include-directories src

# Multiple directories
--include-directories src --include-directories lib

# Current directory (careful with token budget)
--include-all-files
```

**Token budget warning:** Including thousands of files degrades reasoning. Be selective.

See [permission-model.md](references/permission-model.md) for security details.

## Context Configuration

### GEMINI.md (Agent Instructions)

Create `./GEMINI.md` in project root:

```markdown
# Project Context

You are a Senior Engineer working on this Node.js API.

## Constraints
- Use TypeScript strict mode
- Never modify test fixtures
- Log all file changes to session_log.md

## Style
- 2 spaces indentation
- Single quotes for strings
```

Import external docs with `@file`:

```markdown
@./docs/api-schema.md
@./docs/coding-standards.md
```

### settings.json Hierarchy

```
Precedence (lowest → highest):
1. Defaults
2. ~/.gemini/settings.json (user)
3. .gemini/settings.json (project)
4. Environment variables
5. Command-line flags
```

See [context-hierarchy.md](references/context-hierarchy.md) for full reference.

## Session Persistence

Headless sessions are ephemeral by default. For multi-step workflows:

```bash
# First invocation
gemini -p "Analyze codebase structure" --output-format json > analysis.json

# Resume with previous context
gemini -p "Now refactor based on analysis" --resume latest

# Resume specific session
gemini -p "Continue refactoring" --resume abc123-uuid
```

## Output Formats

| Format | Flag | Use Case |
|--------|------|----------|
| text | (default) | Human reading |
| json | `--output-format json` | Script parsing |
| stream-json | `--output-format stream-json` | Real-time dashboards |

### Parsing JSON Output

```bash
# Extract final answer
gemini -p "List files" --output-format json | jq '.response'

# Check if tool was called
gemini -p "Edit file" --output-format json | jq '.tool_calls'
```

## MCP Integration

Extend agent to external services (GitHub, Postgres, Slack).

```json
// .gemini/settings.json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"]
    }
  }
}
```

See [mcp-integration.md](references/mcp-integration.md) for server configs.

## Debugging

```bash
# Verbose output showing Client ↔ Core traffic
gemini -p "Edit file" --debug

# Check what model proposed
gemini -p "Edit file" --debug 2>&1 | grep "old_string"
```

### Session Logging Pattern

Instruct agent via GEMINI.md:

```markdown
## Logging
After every action, append timestamped summary to session_log.md
```

## Common Mistakes

| Mistake | Symptom | Fix |
|---------|---------|-----|
| No approval mode | Script hangs forever | Add `--approval-mode auto_edit` |
| smartEdit disabled | Edit fails repeatedly | Enable in .gemini/settings.json |
| yolo on host machine | Security risk | Use containers only |
| No --include-directories | Agent can't find files | Scope visibility explicitly |
| Interactive shell commands | Script hangs on prompts | Use non-interactive flags (-y) |

## Common Patterns

### Git Commit Agent

```bash
git diff --staged | gemini -p "Generate semantic commit message. Output only the message, no explanation."
# Output: feat(auth): add JWT refresh token rotation
```

### Linter Auto-Fix

```bash
npm run lint 2>&1 | gemini -p "Fix these lint errors" \
  --approval-mode auto_edit \
  --include-directories src
# Agent reads errors, edits files, outputs: "Fixed 3 files: auth.js, utils.js, api.js"
```

### Test Generator

```bash
gemini -p "Generate Jest tests for src/utils.js" \
  --approval-mode auto_edit \
  --include-directories src
```

## When Not to Use This Skill

- Interactive chat with Gemini (use default mode)
- Non-Gemini LLM CLIs (different flag syntax)
- Gemini API direct integration (this is CLI-specific)
- Web-based Gemini interfaces

## Reference Files

- [flags.md](references/flags.md) — Complete flag reference
- [permission-model.md](references/permission-model.md) — Consent model + approval modes
- [context-hierarchy.md](references/context-hierarchy.md) — GEMINI.md + settings.json
- [tools.md](references/tools.md) — ReadFile, Edit, WriteFile, RunShell
- [mcp-integration.md](references/mcp-integration.md) — External service integration

## Assets

- [GEMINI-template.md](assets/GEMINI-template.md) — Starter context file
- [settings-template.json](assets/settings-template.json) — Minimal config with smartEdit
- [headless-wrapper.sh](assets/headless-wrapper.sh) — Shell script template

## Scripts

- [validate-setup.sh](scripts/validate-setup.sh) — Verify configuration before deployment
