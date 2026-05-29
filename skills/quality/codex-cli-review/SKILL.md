---
name: codex-cli-review
description: Use Codex CLI (not MCP) to review uncommitted changes. Codex explores the codebase independently with full disk read access.
allowed-tools: Bash(bash:*), Read, Grep, Glob
context: fork
---

# Codex CLI Review Skill

## Trigger

- Keywords: codex cli review, cli review, script review

## When to Use

- Need Codex to independently explore the entire project (full disk read)
- Don't need MCP's context persistence feature
- Want to use Codex CLI's native review format

## When NOT to Use

- Need iterative review (use `/codex-review-fast --continue`)
- Need to follow up with Codex (use MCP version)
- Only want to see diff without waiting for Codex exploration (use `/codex-review-fast`)

## Difference from MCP Version

| Feature             | CLI Version (this skill) | MCP Version           |
| ------------------- | ------------------------ | --------------------- |
| Independent explore | Full disk read           | Needs explicit instruction |
| Context persistence | None                     | threadId              |
| Iterative review    | Each run independent     | --continue            |
| Format              | Codex native format      | Custom prompt format  |
| Execution method    | Script invocation        | MCP tool invocation   |

## Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│ Step 1: Check Changes                                           │
├─────────────────────────────────────────────────────────────────┤
│ git status --porcelain                                          │
│ No changes -> Early exit                                        │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ Step 2: Execute Codex CLI                                       │
├─────────────────────────────────────────────────────────────────┤
│ codex review --uncommitted                                      │
│   -c 'sandbox_permissions=["disk-full-read-access"]'            │
│                                                                 │
│ Codex will independently:                                       │
│ - Read changed files                                            │
│ - Explore related dependencies                                  │
│ - Check existing tests                                          │
│ - Understand project structure                                  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ Step 3: Output Review Results                                   │
├─────────────────────────────────────────────────────────────────┤
│ Codex native format:                                            │
│ - Summary                                                       │
│ - Issues (Critical/Major/Minor/Suggestion)                      │
│ - Recommendations                                               │
└─────────────────────────────────────────────────────────────────┘
```

## Script

```bash
bash skills/codex-cli-review/scripts/review.sh [options]
```

### Options

| Parameter           | Description                |
| ------------------- | -------------------------- |
| `--base <branch>`   | Compare with specified branch |
| `--title "<text>"`  | Set review title           |
| `--prompt "<text>"` | Custom review instructions |

### I/O Contract

**Input:**

- Git working directory with changes

**Output:**

- Codex review report (stdout)
- Exit code: 0 = success, non-0 = failure

## Verification

- [ ] Script executes without errors
- [ ] Codex explored the project (file references visible in output)
- [ ] Output includes issue classification

## Examples

```bash
# Review uncommitted changes
/codex-cli-review

# Compare with main branch
/codex-cli-review --base main

# With title
/codex-cli-review --title "Feature: User Auth"

# Custom review instructions
/codex-cli-review --prompt "Focus on security and performance"
```

## Related

| Command/Skill          | Difference                           |
| ---------------------- | ------------------------------------ |
| `/codex-review-fast`   | MCP version, supports iterative review |
| `/codex-review`        | MCP version, includes lint + build   |
| `/codex-review-branch` | MCP version, reviews entire branch   |
