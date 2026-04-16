---
name: benchmark
description: Compare Claude Code output with full config vs minimal config using standardized tasks per stack.
---

# Benchmark

Compare the effectiveness of a project's full dotforge configuration against a minimal baseline by executing the same standardized task in two isolated worktrees.

**Cost warning:** Each benchmark runs Claude Code twice (full + minimal). Use sparingly and only after Fases 0-2 are working.

## Prerequisites

- Project must have `.claude/settings.json` and `CLAUDE.md`
- Project must be a git repository with a clean working tree
- Task definitions must exist in `$DOTFORGE_DIR/tests/benchmark-tasks/`

## Step 1: Select task

1. Detect project stacks from `.claude/.forge-manifest.json` or infer from project files
2. Load matching task from `$DOTFORGE_DIR/tests/benchmark-tasks/{stack}.yml`
3. If multiple stacks match, let user choose or run the first match
4. If no stack matches, use `generic.yml`

Display:
```
═══ BENCHMARK SETUP ═══
Project: {{name}}
Stack detected: {{stack}}
Task: {{task title}}
Description: {{task description}}

⚠ This will run Claude Code twice in isolated worktrees.
Proceed? (yes/no)
```

## Step 2: Prepare worktrees

Create two git worktrees from the current HEAD:

1. **Full config** — `git worktree add /tmp/bench-full-{{slug}} HEAD`
   - Copy entire `.claude/` directory as-is
   - Copy `CLAUDE.md` as-is

2. **Minimal config** — `git worktree add /tmp/bench-minimal-{{slug}} HEAD`
   - Create minimal `CLAUDE.md` with only project name and "Build & Test" section
   - Create minimal `.claude/settings.json` with only `allowedTools` (no hooks, no deny list)
   - No `.claude/rules/`, no hooks, no agents

## Step 3: Execute task

For each worktree, run the task prompt using Claude Code in non-interactive mode:

```bash
cd /tmp/bench-full-{{slug}}
claude --print "{{task prompt}}" --allowedTools "Bash,Read,Write,Edit,Glob,Grep"
```

Same for minimal worktree.

Capture for each run:
- **files_created**: count of new files (git diff --name-only --diff-filter=A)
- **files_modified**: count of modified files
- **tests_passing**: run the test command from task definition, count pass/fail
- **lint_issues**: run lint command from task definition, count issues
- **errors**: grep stderr for error patterns
- **has_test**: boolean — did Claude create a test file?

## Step 4: Compare and report

```
═══ BENCHMARK RESULTS — {{project}} ═══
Task: {{task title}}
Stack: {{stack}}
Date: {{YYYY-MM-DD}}

                   Full Config    Minimal Config    Delta
Files created:         {{N}}          {{N}}          {{+/-N}}
Tests created:         {{yes/no}}     {{yes/no}}     —
Tests passing:         {{N/M}}        {{N/M}}        {{+/-N}}
Lint issues:           {{N}}          {{N}}          {{+/-N}}
Errors:                {{N}}          {{N}}          {{+/-N}}

── ANALYSIS ──
{{if full is better across metrics:
  "Full config prevented {{N}} lint issues and {{N}} errors.
   ROI: rules + hooks justified for this project."}}
{{if similar:
  "Minimal difference detected. Consider simplifying configuration
   or running /forge rule-check to identify inert rules."}}
{{if minimal is better:
  "⚠ Full config may be adding overhead without benefit.
   Review rules for contradictions or excessive constraints."}}
```

## Step 5: Cleanup

1. Remove worktrees: `git worktree remove /tmp/bench-full-{{slug}}` and minimal
2. Optionally save results to `~/.claude/metrics/{{slug}}/benchmark-{{date}}.json`

Results JSON schema:
```json
{
  "project": "{{slug}}",
  "date": "{{YYYY-MM-DD}}",
  "stack": "{{stack}}",
  "task": "{{task id}}",
  "full": {
    "files_created": 0,
    "tests_passing": 0,
    "lint_issues": 0,
    "errors": 0,
    "has_test": false
  },
  "minimal": {
    "files_created": 0,
    "tests_passing": 0,
    "lint_issues": 0,
    "errors": 0,
    "has_test": false
  }
}
```

## Important constraints

- NEVER run benchmark automatically — always require explicit user confirmation
- NEVER push or commit from worktrees — they are disposable
- If Claude Code execution fails in either worktree, report the failure and still show partial results
- Timeout each run at 5 minutes — if Claude hasn't finished, capture partial state
- Clean up worktrees even on failure
