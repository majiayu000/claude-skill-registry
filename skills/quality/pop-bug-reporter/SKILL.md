---
name: bug-reporter
description: Capture bug context, generate reports, and optionally create GitHub issues or share patterns
---

# Bug Reporter

Capture and report bugs with automatic context gathering, local logging, GitHub issue creation, and pattern sharing.

## When to Use

- User reports a bug or issue with `/popkit:bug`
- Agent encounters repeated errors or gets stuck
- Need to document an issue for later investigation
- Want to share a bug pattern with the collective

## Input

User provides:

- Bug description
- Optional flags: `--issue`, `--share`, `--verbose`, `--no-context`
- Or subcommands: `list`, `view <id>`, `clear`

## Process

### 1. Parse Request

Determine the action:

- Default: Report new bug
- `list`: List logged bugs
- `view`: View specific bug
- `clear`: Clear logs

### 2. Capture Context (for new bug)

Gather automatic context using `hooks/utils/bug_context.py`:

```python
from bug_context import BugContextCapture, format_bug_report, format_github_issue

capture = BugContextCapture()
ctx = capture.capture(
    description=user_description,
    recent_tools=recent_tool_calls,
    agent_state=current_agent_state
)
```

Context includes:

- Recent tool calls (last 10)
- Files touched
- Error messages detected
- Agent progress and current task
- Project type (language, framework)
- Git status (branch, uncommitted changes)
- Stuck patterns (same file edited 3+ times, build failures)

### 3. Generate Report

Format the bug report:

```
Bug Report
==========
ID: bug-2024-12-04-abc123
Time: 2024-12-04T10:30:00Z

Description: Agent got stuck on OAuth flow

Context:
  Language: TypeScript
  Framework: Next.js
  Branch: feature/oauth
  Uncommitted: 3 files

Recent Actions:
  1. Edit src/auth/oauth.ts
  2. Bash: npm run build (failed)
  3. Edit src/auth/oauth.ts (same file, 2nd time)

Errors Detected:
  [TypeError] Cannot read property 'token' of undefined

Stuck Patterns:
  - Same file edited 3 times: oauth.ts
  - Build command failed

Suggested Actions:
  - Consider stepping back and reviewing the approach
  - Check for null/undefined values
```

### 4. Output Actions

Based on flags:

**Default** - Log locally:

```python
file_path = capture.save(ctx)
print(f"Logged to: {file_path}")
```

**--issue** - Create GitHub issue:

```python
issue_body = format_github_issue(ctx)
# Use gh issue create with formatted body
```

**--share** - Share to collective (Pro/Team):

```python
# Anonymize pattern
# Upload to collective learning database
```

### 5. Confirm to User

Show:

- Bug ID
- Actions taken (logged, issue created, shared)
- Link to issue if created

## Subcommand Handlers

### list

```python
bugs = capture.list_bugs(limit=10)
# Format as table with ID, date, description
```

### view

```python
ctx = capture.get_bug(bug_id)
if ctx:
    print(format_bug_report(ctx, verbose=True))
```

### clear

```python
cleared = capture.clear_bugs(before=date, bug_id=id)
print(f"Cleared {cleared} bug reports")
```

## Anonymization for Sharing

When `--share` is used, anonymize before uploading:

| Original                      | Anonymized              |
| ----------------------------- | ----------------------- |
| `<project>/src/auth/oauth.ts` | `auth module`           |
| `handleTokenRefresh()`        | `token refresh handler` |
| API keys, secrets             | `[REDACTED]`            |
| Variable names                | Generic terms           |

```python
def anonymize_pattern(ctx: BugContext) -> Dict:
    return {
        "trigger": abstract_error(ctx.errors[0] if ctx.errors else None),
        "context": {
            "language": ctx.project.language,
            "framework": ctx.project.framework,
            "error_type": ctx.errors[0].error_type if ctx.errors else None
        },
        "stuck_patterns": ctx.stuck_patterns,
        "suggested_actions": ctx.suggested_actions
    }
```

## Example Flows

### Report Bug (Default)

```
User: /popkit:bug "Agent can't find the right file"

[Capturing context...]
- Recent tools: 8 calls
- Files touched: 4
- Errors: 1 (ENOENT)
- Git: feature/search branch

Bug Report
==========
ID: bug-2024-12-04-def456
...

Logged to: .claude/bugs/bug-2024-12-04-def456.json
```

### Create GitHub Issue

```
User: /popkit:bug "Tests failing after refactor" --issue

[Capturing context...]
[Creating GitHub issue...]

Bug Report Created
==================
ID: bug-2024-12-04-ghi789
GitHub Issue: #123
URL: https://github.com/user/repo/issues/123

Logged locally and issue created.
```

### Share Pattern

```
User: /popkit:bug "OAuth token refresh failing" --share

[Capturing context...]
[Anonymizing pattern...]
[Uploading to collective...]

Bug Report
==========
ID: bug-2024-12-04-jkl012
Pattern shared: Yes (anonymized)
Collective ID: pattern-abc123

Thank you for contributing to the collective learning database!
```

## Integration Points

| Component                        | Purpose                        |
| -------------------------------- | ------------------------------ |
| `hooks/utils/bug_context.py`     | Context capture and formatting |
| `.claude/bugs/`                  | Local bug storage              |
| `power-mode/insight_embedder.py` | Pattern sharing                |
| `gh issue create`                | GitHub issue creation          |

## Output Style

Use a clear, structured format:

- Show bug ID prominently
- List context in organized sections
- Highlight errors and stuck patterns
- Provide actionable suggestions
- Confirm what actions were taken
