---
name: codex
description: Hand off a task to Codex CLI for autonomous execution. Use when a task would benefit from a capable subagent to implement, fix, investigate, or review code. Codex has full codebase access and can make changes.
argument-hint: <task description> [--model <model>] [--sandbox <mode>]
disable-model-invocation: false
allowed-tools: Bash(codex:*), Bash(git:*), Bash(pwd:*), Bash(mkdir:*), Bash(cat:*), Bash(head:*), Bash(tail:*), Bash(wc:*), Read, Grep, Glob
---

# Codex Subagent

Session ID: ${CLAUDE_SESSION_ID}
Output: `~/.claude/codex/${CLAUDE_SESSION_ID}/`

## Arguments

Task: $ARGUMENTS

**Optional flags** (only if user explicitly requests):
- `--model <model>`: `gpt-5.2-codex` (default), `gpt-5.2`, `gpt-5-mini`, `o3`
- `--sandbox <mode>`: `read-only`, `workspace-write`, `danger-full-access`

Omit flags to use user's config defaults.

## Context Depth

**Minimal**: Specific file/function → git state only
**Medium**: Feature/multi-file → add recent changes
**Full**: Investigation/unclear → add session summary

## Gather Context

**Always:**
```bash
pwd && git rev-parse --show-toplevel 2>/dev/null || echo "Not a git repo"
git branch --show-current 2>/dev/null && git status --short 2>/dev/null | head -20
```

**Medium/Full:**
```bash
git diff --stat 2>/dev/null | tail -20
git log --oneline -5 --since="4 hours ago" 2>/dev/null
```

**Full only:** Session summary (work done, decisions, blockers)

## Prompt Structure

Use CTCO format (Context → Task → Constraints → Output):

```
<context>
Working directory: {cwd}
Repository: {repo_name}
Branch: {branch}
{git_status}
{recent_changes if medium/full}
{session_summary if full}
</context>

<task>
{task from arguments}
</task>

<constraints>
- Implement EXACTLY what is requested
- Read files before changing
- Run tests/linters to validate
- State interpretation if ambiguous
</constraints>

<output>
Summary (≤5 bullets):
- **What changed**: Files and changes
- **Where**: file:line references
- **Validation**: Tests/linters run
- **Risks**: Edge cases to watch
- **Next steps**: Follow-up or "None"
</output>
```

## Execute

Setup:
```bash
mkdir -p ~/.claude/codex/${CLAUDE_SESSION_ID}
git rev-parse --show-toplevel 2>/dev/null && IN_GIT=true || IN_GIT=false
```

Run:
```bash
codex exec --json \
  -o ~/.claude/codex/${CLAUDE_SESSION_ID}/summary-{timestamp}.txt \
  {--skip-git-repo-check if not in git} \
  {--full-auto OR --sandbox <mode>} \
  {-m <model> if requested} \
  - <<'CODEX_PROMPT'
{prompt}
CODEX_PROMPT > ~/.claude/codex/${CLAUDE_SESSION_ID}/progress-{timestamp}.jsonl
```

**Flags:**
- Not in git: add `--skip-git-repo-check`
- Default: `--full-auto` (workspace-write + auto-approval)
- User-requested: `--sandbox <mode>` or `-m <model>`

### Background vs Foreground

**Background tasks** (>30 seconds expected):
- Multi-file changes, investigations, tests, feature work
- Use `run_in_background: true` → returns `task_id`

**Foreground tasks** (<30 seconds):
- Single-line fixes, simple queries

### Monitoring Background Tasks

**Token-efficient approach:**
1. Use `TaskOutput(task_id, block=true)` to wait for completion
2. Ignore TaskOutput's content (stdout redirected to progress file)
3. Read summary file directly: `cat ~/.claude/codex/${CLAUDE_SESSION_ID}/summary-*.txt`

The summary file contains only Codex's final message (token-efficient).

**Progress checks** (if needed before completion):
- `TaskOutput(task_id, block=false)` - check if still running
- `tail -n 3 ~/.claude/codex/${CLAUDE_SESSION_ID}/progress-*.jsonl` - last 3 events only

**Do NOT** read entire progress files or use `tail -f`.

## Report Result

Read summary:
```bash
cat ~/.claude/codex/${CLAUDE_SESSION_ID}/summary-*.txt
```

Report format (≤5 bullets):
```
**Status:** {success/error/partial}
**Changed:** {files and changes}
**Validation:** {tests/linters}
**Risks:** {if any}
**Next:** {follow-up or "None"}
```

## Examples

```bash
# Simple fix
/codex fix the null pointer in utils/parser.ts line 42

# Feature work
/codex add rate limiting to the /api/submit endpoint

# Investigation (background)
/codex investigate why the CI build fails on arm64

# Model override
/codex --model o3 design a caching strategy

# Read-only
/codex --sandbox read-only review the auth implementation
```
