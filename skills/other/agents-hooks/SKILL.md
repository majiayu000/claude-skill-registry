---
name: agents-hooks
description: Event-driven hooks for AI coding agents. Use when automating Claude Code or Codex CLI with stdin JSON and decision-control responses.
---

# Claude Code Hooks — Meta Reference

This skill provides the definitive reference for creating Claude Code hooks. Use this when building automation that triggers on Claude Code events.

---

## When to Use This Skill

- Building event-driven automation for Claude Code
- Creating PreToolUse guards to block dangerous commands
- Implementing PostToolUse formatters, linters, or auditors
- Adding Stop hooks for testing or notifications
- Setting up SessionStart/SessionEnd for environment management
- Integrating Claude Code with CI/CD pipelines (headless mode)

---

## Quick Reference

| Event | Trigger | Use Case |
|-------|---------|----------|
| `SessionStart` | Session begins/resumes | Initialize environment |
| `UserPromptSubmit` | User submits prompt | Preprocess/validate input |
| `PreToolUse` | Before tool execution | Validate, block dangerous commands |
| `PermissionRequest` | Permission dialog shown | Auto-allow/deny permissions |
| `PostToolUse` | After tool succeeds | Format, audit, notify |
| `PostToolUseFailure` | After tool fails | Capture failures, add guidance |
| `SubagentStart` | Subagent spawns | Inspect subagent metadata |
| `Stop` | When Claude finishes | Run tests, summarize |
| `SubagentStop` | Subagent finishes | Verify subagent completion |
| `Notification` | On notifications | Alert integrations |
| `PreCompact` | Before context compaction | Preserve critical context |
| `Setup` | `--init`/`--maintenance` | Initialize repo/env |
| `SessionEnd` | Session ends | Cleanup, save state |
## Hook Structure

```text
.claude/hooks/
├── pre-tool-validate.sh
├── post-tool-format.sh
├── post-tool-audit.sh
├── stop-run-tests.sh
└── session-start-init.sh
```
---

## Configuration

### settings.json

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/post-tool-format.sh"
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/pre-tool-validate.sh"
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/stop-run-tests.sh"
          }
        ]
      }
    ]
  }
}
```

---

## Execution Model (Jan 2026)

- Hooks receive a JSON payload via stdin (treat it as untrusted input) and run with your user permissions (outside the Bash tool sandbox).
- Default timeout is 60s per hook command; all matching hooks run in parallel; identical commands are deduplicated.

### Hook Input (stdin)

```json
{
  "hook_event_name": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": {
    "command": "ls -la"
  }
}
```

### Environment Variables (shell)

| Variable | Description |
|----------|-------------|
| `CLAUDE_PROJECT_DIR` | Absolute project root where Claude Code started |
| `CLAUDE_PLUGIN_ROOT` | Plugin root (plugin hooks only) |
| `CLAUDE_CODE_REMOTE` | `"true"` in remote/web environments; empty/local otherwise |
| `CLAUDE_ENV_FILE` | File path to persist `export ...` lines (available in SessionStart; check docs for Setup support) |

---

## Exit Codes

| Code | Meaning | Notes |
|------|---------|------|
| `0` | Success | JSON written to stdout is parsed for structured control |
| `2` | Blocking error | `stderr` becomes the message; JSON in stdout is ignored |
| Other | Non-blocking error | Execution continues; `stderr` is visible in verbose mode |

Stdout injection note: for `UserPromptSubmit`, `SessionStart`, and `Setup`, non-JSON stdout (exit 0) is injected into Claude’s context; most other events show stdout only in verbose mode.

---

## Decision Control + Input Modification (v2.0.10+)

PreToolUse hooks can allow/deny/ask and optionally modify the tool input via `updatedInput`.

### Hook Output Schema

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "permissionDecisionReason": "Reason shown to user (and to Claude on deny)",
    "updatedInput": { "command": "echo 'modified'" },
    "additionalContext": "Extra context added before tool runs"
  }
}
```

Note: older `decision`/`reason` fields are deprecated; prefer the `hookSpecificOutput.*` fields.

See [hook-templates.md](references/hook-templates.md) for full examples: redirect sensitive file edits to `/dev/null` and strip `.env` files from `git add` commands.

---

## Prompt-Based Hooks

For complex decisions, use LLM-evaluated hooks (`type: "prompt"`) instead of bash scripts. They are most useful for `Stop` and `SubagentStop` decisions.

### Configuration

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Evaluate whether Claude should stop. Context JSON: $ARGUMENTS. Return {\"ok\": true} if all tasks are complete, otherwise {\"ok\": false, \"reason\": \"what remains\"}.",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

### Response Schema

- Allow: `{"ok": true}`
- Block: `{"ok": false, "reason": "Explanation shown to Claude"}`

### Combining Command and Prompt Hooks

Use command hooks for fast, deterministic checks. Use prompt hooks for nuanced decisions:

```json
{
  "Stop": [
    {
      "hooks": [
        { "type": "command", "command": ".claude/hooks/quick-check.sh" },
        { "type": "prompt", "prompt": "Verify code quality meets standards" }
      ]
    }
  ]
}
```

---

## Permission Prompt Fatigue Reduction Pattern

Use this when frequent approval dialogs slow down repeated safe workflows.

### Strategy

1. Identify repetitive, low-risk command prefixes (for example: test runners, read-only diagnostics).
2. Approve narrow prefixes instead of full commands.
3. Keep destructive or broad shells (`rm`, `git reset --hard`, generic interpreters with arbitrary input) out of auto-approval rules.
4. Re-check approved prefixes periodically; remove stale ones.

### Practical Guardrails

- Allow only task-scoped prefixes (example: `npm run test:e2e`), not unrestricted executors.
- Keep separate policy for write-outside-workspace actions.
- Pair allow-rules with deny-rules for dangerous patterns.

### Outcome

This reduces repeated permission interruptions while preserving high-safety boundaries.


## Runtime Preflight Hooks (Mandatory for Tool Reliability)

Add a lightweight runtime preflight hook when workflows depend on specific local tool versions (for example Node for JS REPL, test runners, linters).

### Preflight Responsibilities

- Verify required binaries exist.
- Verify minimum version constraints.
- Emit a clear remediation message when requirements are not met.
- Fail fast before expensive task execution starts.

### Recommended Trigger

- `SessionStart` for general runtime checks.
- `Setup` for repository bootstrap checks.

### Minimal Policy

- Keep checks deterministic and fast (<1s target).
- Do not auto-install dependencies silently in hooks.
- Print exact command the operator should run to remediate.

## Hook Templates

Copy-paste templates for the five most common hook scenarios: PreToolUse validation, PostToolUse formatting, PostToolUse security audit, Stop test runner, and SessionStart environment check.

See [references/hook-templates.md](references/hook-templates.md) for all scripts.

---

## Matchers

Matchers filter which tool triggers the hook:

- Exact match: `Write` matches only the Write tool
- Regex: `Edit|Write` or `Notebook.*`
- Match all: `*` (also works with `""` or omitted matcher)

---

## Security Best Practices

Hooks run with full user permissions outside the Bash tool sandbox. Key rules: validate all stdin input, quote every variable (`"$VAR"`), use absolute paths, never `eval` untrusted data, and set `-euo pipefail`.

See [references/hook-security.md](references/hook-security.md) for the full checklist, command injection prevention, path traversal defense, credential protection, and ShellCheck requirements.

---

## Hook Composition

### Multiple Hooks on Same Event

```json
{
  "PostToolUse": [
    {
      "matcher": "Edit|Write",
      "hooks": [
        { "type": "command", "command": ".claude/hooks/format.sh" },
        { "type": "command", "command": ".claude/hooks/audit.sh" },
        { "type": "command", "command": ".claude/hooks/notify.sh" }
      ]
    }
  ]
}
```

All matching hooks run in parallel. If you need strict ordering (format → lint → test), make one wrapper script that runs them sequentially.

---

## Debugging Hooks

```bash
# Test a PostToolUse hook manually (stdin JSON)
export CLAUDE_PROJECT_DIR="$(pwd)"
echo '{"hook_event_name":"PostToolUse","tool_name":"Edit","tool_input":{"file_path":"'"$(pwd)"'/src/app.ts"}}' \
  | bash .claude/hooks/post-tool-format.sh

# Check exit code
echo $?
```

---

## Navigation

### Resources

- [references/hook-templates.md](references/hook-templates.md) — Copy-paste hook scripts
- [references/hook-patterns.md](references/hook-patterns.md) — Common patterns
- [references/hook-security.md](references/hook-security.md) — Security guide
- [references/runtime-preflight-hooks.md](references/runtime-preflight-hooks.md) — Runtime/version preflight patterns for SessionStart and Setup
- [data/sources.json](data/sources.json) — Documentation links
- [assets/template-preflight-runtime-hook.sh](assets/template-preflight-runtime-hook.sh) — Shell hook template for runtime/tool version checks

### Related Skills

- [../agents-subagents/SKILL.md](../agents-subagents/SKILL.md) — Agent creation
- [../agents-skills/SKILL.md](../agents-skills/SKILL.md) — Skill creation
- [../ops-devops-platform/SKILL.md](../ops-devops-platform/SKILL.md) — CI/CD integration

## Fact-Checking

- Use web search/web fetch to verify current external facts, versions, pricing, deadlines, regulations, or platform behavior before final answers.
- Prefer primary sources; report source links and dates for volatile information.
- If web access is unavailable, state the limitation and mark guidance as unverified.
