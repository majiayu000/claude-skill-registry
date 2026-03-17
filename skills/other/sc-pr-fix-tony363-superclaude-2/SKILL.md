---
name: sc-pr-fix
description: Create PR and iteratively fix CI failures with interactive confirmation. Automates branch creation, commit, push, PR creation, and CI monitoring until all checks pass.
---

# PR Fix Skill

Create pull requests and interactively fix CI check failures until all pass.

## Quick Start

```bash
# Create PR from current changes
/sc:pr-fix "fix: resolve test failures" --branch fix/tests

# Dry run to preview
/sc:pr-fix "feat: new feature" --dry-run

# With custom PR details
/sc:pr-fix "chore: update deps" --title "Update dependencies" --body "Monthly update"

# Auto-fix low-risk issues
/sc:pr-fix "fix: lint errors" --auto-fix
```

## Behavioral Flow

1. **Validate** - Check git state, ensure changes exist
2. **Branch** - Create and checkout new branch
3. **Commit** - Stage all changes and commit with provided message
4. **Push** - Push branch to origin
5. **PR Create** - Create pull request via `gh` CLI
6. **Monitor** - Poll CI status at configured interval
7. **Fix Loop** - For each failing check:
   - Parse failure logs
   - Propose fix (with PAL MCP assistance for complex issues)
   - **Prompt user for confirmation** (interactive mode)
   - Apply fix and push
   - Re-monitor checks
8. **Complete** - All checks pass or max attempts reached

## Flags

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--branch` | string | auto | New branch name (auto: `pr-fix/<timestamp>`) |
| `--base` | string | `main` | Target branch for PR |
| `--title` | string | commit msg | PR title |
| `--body` | string | auto | PR description body |
| `--dry-run` | bool | false | Preview operations without executing |
| `--auto-fix` | bool | false | Auto-apply low-risk fixes, prompt only for high-risk |
| `--max-fix-attempts` | int | 5 | Max CI fix iterations (hard cap: 5) |
| `--poll-interval` | int | 30 | Seconds between CI status checks |
| `--no-push` | bool | false | Create branch and commit but do not push/PR |

## Interactive Mode

By default, the skill prompts before each fix:

```
================================================================================
CI Check Failed: build (lint)                                   Attempt 2 of 5
================================================================================

Error Summary:
  - src/component.ts:42:15 - Missing semicolon (semi)
  - src/utils.ts:18:1 - Unexpected console statement (no-console)

Proposed Fix:
  1. Add semicolon at src/component.ts:42
  2. Remove console.log at src/utils.ts:18

Risk Level: LOW (auto-fixable lint errors)

--------------------------------------------------------------------------------
[A]pply fix  [S]kip this check  [V]iew full log  [Q]uit
>
```

Use `--auto-fix` to skip prompts for low-risk fixes (lint, formatting).
High-risk fixes (test changes, security, core logic) always prompt.

## Risk Classification

| Level | Examples | Behavior |
|-------|----------|----------|
| LOW | Lint errors, formatting, whitespace | Auto-fix if `--auto-fix` |
| MEDIUM | Test updates, documentation | Always prompt |
| HIGH | Core logic, security, API changes | Always prompt + PAL review |

## Evidence Requirements

This skill requires evidence of successful operations:
- Git operations must succeed (branch created, pushed)
- PR creation must return valid PR URL
- CI status must be retrievable via `gh` CLI
- Fix attempts must show file diffs

## Tool Coordination

- **Bash** - Git and `gh` CLI execution
- **Read** - Analyze failure logs and source code
- **Edit** - Apply fixes to source files
- **AskUserQuestion** - Interactive prompts for fix confirmation
- **PAL MCP debug** - Diagnose complex CI failures
- **PAL MCP codereview** - Validate fix quality before applying

## MCP Integration

- **PAL MCP debug** - Root cause analysis for CI failures
- **PAL MCP codereview** - Review proposed fixes before applying

## Safety Mechanisms

1. **Hard cap**: Maximum 5 fix iterations (cannot be overridden)
2. **Stagnation detection**: Same error 3 consecutive times = abort
3. **Oscillation detection**: Fix-revert-fix pattern = abort
4. **Interactive confirmation**: All structural changes require approval
5. **Never skip checks**: Must fix or explicitly abort - no skipping
6. **Backup branch**: Creates `backup/<branch>-<timestamp>` before starting

## CI Status Polling

The skill polls GitHub Actions check status using:

```bash
gh pr checks <pr_number> --json name,state,conclusion,url
```

Poll behavior:
- Initial wait: 10 seconds after push (allow CI to start)
- Poll interval: `--poll-interval` seconds (default: 30)
- Timeout: 10 minutes for checks to complete
- Handles pending, queued, in_progress, and completed states

## Failure Log Parsing

Supported CI output formats:
- ESLint/TSLint JSON format
- pytest output with tracebacks
- ruff/flake8 format
- Jest/Vitest output format
- Generic error patterns (`error:`, `ERROR`, `failed`)
- GitHub Actions annotations

## Examples

### Basic PR Creation with Fix Loop

```bash
/sc:pr-fix "fix: resolve ESLint errors"
```

Output:
```
Creating branch: pr-fix/20240115-143022
Committing: fix: resolve ESLint errors
Pushing to origin...
Creating PR #42: fix: resolve ESLint errors

Monitoring CI checks...
  - lint: pending
  - test: pending

[30s later]
  - lint: failed
  - test: passed

Parsing lint failures...
Found 2 errors in 1 file.

================================================================================
CI Check Failed: lint                                           Attempt 1 of 5
================================================================================
...
[A]pply fix  [S]kip  [V]iew log  [Q]uit
> a

Applying fix...
Pushing fix commit...
Monitoring CI checks...
  - lint: passed
  - test: passed

All checks passed! PR #42 is ready for review.
PR URL: https://github.com/owner/repo/pull/42
```

### Feature PR with Details

```bash
/sc:pr-fix "feat: add user dashboard" \
  --branch feat/user-dashboard \
  --title "Add User Dashboard Component" \
  --body "Implements user dashboard as per spec #42"
```

### Preview Mode

```bash
/sc:pr-fix "refactor: cleanup utils" --dry-run
```

Output:
```
[DRY RUN] Would execute:
  1. git checkout -b pr-fix/20240115-143022
  2. git add -A
  3. git commit -m "refactor: cleanup utils"
  4. git push -u origin pr-fix/20240115-143022
  5. gh pr create --base main --title "refactor: cleanup utils"
  6. Monitor CI and fix failures interactively

No changes made.
```

### Auto-Fix Low-Risk Issues

```bash
/sc:pr-fix "fix: formatting" --auto-fix
```

With `--auto-fix`, LOW risk fixes (lint, formatting) are applied automatically.
MEDIUM and HIGH risk fixes still prompt for confirmation.

## Termination Conditions

The fix loop terminates when:

| Condition | Exit Status | Message |
|-----------|-------------|---------|
| All checks pass | SUCCESS | "All checks passed! PR ready for review." |
| Max attempts (5) | FAILED | "Max fix attempts reached. Manual intervention required." |
| Stagnation (3x same error) | FAILED | "Same error persists after 3 attempts. Aborting." |
| User quits | ABORTED | "Fix loop aborted by user." |
| CI timeout | TIMEOUT | "CI checks did not complete within timeout." |

## Commit Message Format

Fix commits follow Conventional Commits:

```
fix(ci): resolve <check_name> failures

- <description of fix 1>
- <description of fix 2>

Automated fix by sc-pr-fix skill
```

## Scripts

This skill uses Python helper scripts in `scripts/`:

- `check_pr_status.py` - Poll PR check status via `gh pr checks`
- `parse_check_failures.py` - Parse CI failure logs to extract errors
- `fix_orchestrator.py` - Coordinate fix loop with safety mechanisms

## Error Handling

| Scenario | Behavior |
|----------|----------|
| No git repo | Exit with error message |
| Dirty working tree | Prompt: stash, commit, or abort |
| Branch already exists | Prompt for different name |
| Push fails | Check permissions, offer retry |
| PR creation fails | Show `gh` CLI error, suggest manual |
| CI timeout | Report status, offer to continue monitoring |
| Parse failure | Fall back to raw log display |
| Fix application fails | Increment attempt counter, continue loop |
| User aborts | Clean exit with status summary |
