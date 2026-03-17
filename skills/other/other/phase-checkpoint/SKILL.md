---
name: phase-checkpoint
description: Run checkpoint criteria after completing a phase. Use after /phase-start completes all tasks to verify quality gates before proceeding.
argument-hint: [phase-number]
allowed-tools: Bash, Read, Edit, Glob, Grep, Task, AskUserQuestion, WebFetch, WebSearch
---

Phase $1 is complete. Run the checkpoint criteria from EXECUTION_PLAN.md.

**AUTONOMY RULE:** Never invoke skills via the Skill tool mid-checkpoint — it creates
a turn boundary that breaks procedural flow. Use the **Task tool** (subagent) for any
delegated work. Do NOT use AskUserQuestion during the checkpoint — it pauses the
auto-advance chain. If something is ambiguous, use a deterministic default and report it.

## Workflow

Copy this checklist and track progress:

```
Phase Checkpoint Progress:
- [ ] Step 1: Context detection
- [ ] Step 2: Tool availability & config
- [ ] Step 3: Local verification (automated, optional, manual)
- [ ] Step 4: Cross-model review (Codex)
- [ ] Step 5: Production verification
- [ ] Step 6: State update
- [ ] Step 7: Generate report
- [ ] Step 8: Auto-advance check
```

## Step 1: Context Detection

Determine working context:

1. If CWD matches `*/features/*`:
   - PROJECT_ROOT = parent of parent of CWD
   - MODE = "feature"
2. Otherwise:
   - PROJECT_ROOT = current working directory
   - MODE = "greenfield"

**Directory Guard:** Confirm `EXECUTION_PLAN.md` exists. If not, STOP and tell user to `cd` into their project directory.

**Context Check:** If context is below 40% remaining, run `/compact` first.

## Step 2: Tool Availability & Config

Check which optional tools are available:

| Tool | Check Method | Fallback |
|------|--------------|----------|
| ExecuteAutomation Playwright | Check for `mcp__playwright__*` | Next in chain |
| Browser MCP | Check for `mcp__browsermcp__*` | Next in chain |
| Chrome DevTools MCP | `mcp__chrome-devtools__list_pages` | Manual verification |
| code-simplifier | Check if agent type available | Skip |
| Codex CLI | `codex --version` | Skip cross-model review |

**Browser fallback chain:** ExecuteAutomation → Browser MCP → Microsoft Playwright → Chrome DevTools → Manual

Read `.claude/verification-config.json` from PROJECT_ROOT. If missing entirely, run `/configure-verification`. Omitted keys mean those checks are not configured — skip them rather than blocking.

Read `.claude/settings.local.json` for cross-model review config:
```json
{
  "codexReview": {
    "enabled": true,
    "triggerOn": ["phase-checkpoint"]
  }
}
```

If `codexReview` is not configured, default to `enabled: true` when Codex CLI is available.

## Step 3: Local Verification (Must Pass First)

**IMPORTANT**: All local verification must pass before production verification.

See [VERIFICATION.md](VERIFICATION.md) for detailed check procedures.

### Automated Checks

Run these using commands from verification-config (skip any that are not configured):
1. Tests (`commands.test`) — skip if not in config
2. Type Checking (`commands.typecheck`) — skip if not in config
3. Linting (`commands.lint`) — skip if not in config
4. Build (`commands.build`) — skip if not in config
5. Mutation Tests (`commands.mutation_test`) — skip if not in config
6. Dev Server (`devServer.command`) — skip if not in config
7. Security Scan
8. Code Quality Metrics

If `commands.mutation_test` is configured, treat failures as a local verification
failure (it is part of the quality gate).

### Optional Checks

- Code Simplification (if code-simplifier available)
- Browser Verification (if browser tools available)
- Technical Debt Check (if skill exists)

### Manual Verification

1. Extract manual items from "Phase $1 Checkpoint" in EXECUTION_PLAN.md
2. Attempt automation using auto-verify skill (via Task tool, not Skill tool)
3. Classify remaining items:
   - `MANUAL:DEFER` → enqueue to deferred review queue (see [DEFERRED_QUEUE.md](DEFERRED_QUEUE.md))
   - `MANUAL` (blocking) → stop checkpoint and stop auto-advance
4. If blocking items exist: report them in the checkpoint output and stop.
   Do NOT use AskUserQuestion — just list the items and halt auto-advance.
5. If only deferred items: continue, report queue status
6. Update checkboxes in EXECUTION_PLAN.md

For external integrations, follow [DOCS_PROTOCOL.md](DOCS_PROTOCOL.md) to fetch latest documentation.

## Step 4: Cross-Model Review (Codex)

**Purpose:** Get a second opinion from a different AI model to catch blind spots.

### When This Step Runs

This step runs if ALL of these conditions are true:
- Codex CLI is available (`codex --version` succeeds)
- `codexReview.enabled` is true (or not configured, defaulting to true)
- `"phase-checkpoint"` is in `codexReview.triggerOn` (or not configured)

### Execution

**IMPORTANT — Invocation Method:** Do NOT invoke `/codex-review` via the Skill tool.
The Skill tool creates a turn boundary that breaks the checkpoint's procedural flow
and prevents auto-advance from continuing. Use the **Task tool** instead.

1. **Gather phase context:**
   ```bash
   # Identify technologies from changed files for --research flag
   # Check package.json, imports in changed files
   ```

2. **Launch Task subagent** to perform the Codex review inline:
   - `subagent_type`: `general-purpose`
   - Include in the prompt:
     - The technologies/research topics identified in step 1
     - Any focus area (e.g., `security`)
     - The base branch and model from config
   - Instruct the subagent to:
     a. Read `.claude/skills/codex-review/SKILL.md` and follow Steps 1-5
     b. Read supporting files as needed (CODEX_INVOCATION.md, PROMPT_TEMPLATE.md, EVALUATION_PRACTICES.md)
     c. Return structured JSON with `status`, `critical_issues`, `recommendations`, `positive_findings`

   The Task tool returns results to the current turn, preserving checkpoint state.

3. **Process results** from the Task subagent:

   | Codex Status | Checkpoint Action |
   |--------------|-------------------|
   | `pass` | Continue, note in report |
   | `pass_with_notes` | Auto-implement recommendations, continue |
   | `needs_attention` | Auto-implement all findings, continue |
   | `skipped` | Note unavailable, continue |
   | `error` | Note error, continue |

### Auto-Implement Findings

When Codex returns findings (`pass_with_notes` or `needs_attention`), implement
them automatically. Do NOT ask the user — this keeps the auto-advance chain flowing.

1. **Launch Task subagent** to implement all findings:
   - `subagent_type`: `general-purpose`
   - Include in the prompt:
     - All critical issues with file:line locations and suggestions
     - All recommendations with file:line locations and suggestions
     - Instruct: "Implement each fix. If a suggestion is too vague to act on
       (no specific file/line or actionable change), skip it and note why.
       Do NOT use AskUserQuestion — if anything is ambiguous, skip it.
       Do NOT create new files unless a fix explicitly requires it."
   - The subagent edits files and returns a summary of what it changed

3. **Re-run automated verification** (same commands from Step 3):
   - Tests, typecheck, lint, build — whatever is configured in verification-config
   - This confirms the fixes don't break anything

4. **Handle re-verification results:**

   | Outcome | Action |
   |---------|--------|
   | All checks pass | Commit: `git add -u && git commit -m "fix: address Codex review findings (phase $1 checkpoint)"`, note "{N} findings auto-fixed" in report |
   | Any check fails | Revert: `git checkout -- .`, note "fixes reverted — broke verification" in report, log findings to deferred queue |

   **Git safety notes:**
   - Use `git add -u` (tracked files only) — never `git add -A` which can stage untracked artifacts
   - Commit only after verification passes — no commit to undo on failure
   - `git checkout -- .` reverts working tree changes without needing `git reset --hard`
   - If pre-commit hooks fail the commit, treat as "skip auto-commit" and continue

5. **Continue to Step 5** regardless of outcome — Codex findings never block.

### Output

```
Cross-Model Review (Codex):
- Status: PASS | PASS WITH NOTES | NEEDS ATTENTION | SKIPPED
- Findings: {N} critical, {M} recommendations
- Auto-implemented: {X} fixes applied, {Y} skipped (too vague)
- Verification: PASSED | REVERTED (logged to deferred queue)
```

### Skip Conditions

Skip this step (mark as SKIPPED) if:
- Running inside Codex CLI (`$CODEX_SANDBOX` is set) — `/codex-review` detects this automatically
- Codex CLI not installed
- `codexReview.enabled` is explicitly false
- Phase has fewer than 3 tasks (trivial phase)
- `--skip-codex` flag passed to checkpoint

## Step 5: Production Verification

**BLOCKED** until all Local Verification passes.

When local passes, verify:
- Staging/production deployment
- External integrations
- Production-only manual checks

## Step 6: State Update

After checkpoint passes, update `.claude/phase-state.json`:

```json
{
  "phases": [{
    "number": 1,
    "status": "CHECKPOINTED",
    "completed_at": "{ISO timestamp}",
    "checkpoint": {
      "tests_passed": true,
      "type_check_passed": true,
      "lint_passed": true,
      "security_passed": true,
      "mutation_tests_passed": true,
      "coverage_percent": 85,
      "manual_verified": true,
      "codex_review": {
        "status": "pass | pass_with_notes | needs_attention | skipped",
        "critical_issues": 0,
        "recommendations": 2,
        "auto_fixed": 2,
        "fix_skipped": 0,
        "fix_reverted": false
      }
    }
  }]
}
```

Write checkpoint report to `.claude/verification/phase-$1.md` and append to `.claude/verification-log.jsonl`.

## Step 7: Report

```
Phase $1 Checkpoint Results
===========================

Tool Availability:
- ExecuteAutomation Playwright: ✓ | ✗
- Browser MCP: ✓ | ✗
- Chrome DevTools MCP: ✓ | ✗
- code-simplifier: ✓ | ✗
- Codex CLI: ✓ | ✗

## Local Verification

Automated Checks:
- Tests: PASSED | FAILED
- Type Check: PASSED | FAILED | SKIPPED
- Linting: PASSED | FAILED | SKIPPED
- Build: PASSED | FAILED | SKIPPED
- Mutation Tests: PASSED | FAILED | SKIPPED
- Security: PASSED | FAILED

Optional Checks:
- Browser Verification: PASSED | SKIPPED
  - Target: {URL}
- Tech Debt: PASSED | NOTES | SKIPPED

Manual Checks:
- Automated: {X} items
- Blocking manual: {Y} items
- Deferred: {Z} items (queued for later review)
- Total deferred queue: {M} items across {P} phases

Local Verification: ✓ PASSED | ✗ FAILED

---

## Cross-Model Review (Codex)

Status: PASS | PASS WITH NOTES | NEEDS ATTENTION | SKIPPED
{If not skipped}
- Findings: {N} critical, {M} recommendations
- Auto-implemented: {X} fixes applied, {Y} skipped (too vague)
- Verification: PASSED | REVERTED (logged to deferred queue)
{If reverted}
- Reverted fixes logged to deferred queue for later review
{/If}
{/If}

---

## Production Verification
{items or "Blocked: Complete local verification first"}

---

Overall: Ready to proceed | Issues to address
```

## Step 8: Auto-Advance

See [AUTO_ADVANCE.md](AUTO_ADVANCE.md) for auto-advance logic.

**Summary:** If all checks pass and no blocking manual items remain, automatically invoke `/phase-prep {N+1}`. `MANUAL:DEFER` items are queued and do not block.

**Codex review and auto-advance:** Codex findings are auto-implemented inline. If fixes pass re-verification they are committed; if they fail, they are reverted and logged to the deferred queue. Either way, auto-advance is never blocked.

---

## When Checkpoint Cannot Pass

**If both local AND production verification fail:**
- Report all failures clearly, separated by category
- Do NOT suggest skipping checks
- Prioritize: Fix local failures first (they often cause production failures)
- Suggest: Run `/phase-start $1` to address failing tasks before re-running checkpoint

**If blocking manual verification items remain after auto-verify:**
- Stop the checkpoint and report which items blocked it
- Do NOT use AskUserQuestion — just halt and list the items
- The user can re-run `/phase-checkpoint $1` after manual resolution
- Note: Blocking items prevent auto-advance (this is by design)

**If verification config file is missing entirely:**
- Run `/configure-verification` to auto-detect
- Omitted keys in an existing config are intentional — skip those checks

**If auto-advance chain should stop:**
- Report: "Auto-advance stopped at Phase $1 checkpoint"
- List specific blocking items
- Provide: "Run `/phase-checkpoint $1` again after resolving issues"

**If a tool consistently fails mid-checkpoint:**
- Mark that specific check as FAILED (not SKIPPED)
- Continue with remaining checks
- Report tool failure in final summary
- Suggest troubleshooting steps for the failing tool

**If Codex review times out or errors:**
- Mark as SKIPPED with reason
- Do NOT block checkpoint progress
- Note in report: "Cross-model review unavailable: {reason}"
- Suggest: Re-run `/codex-review` manually after checkpoint if desired

**If Codex finds critical issues:**
- Auto-implement all findings (see "Auto-Implement Findings" in Step 4)
- If fixes pass re-verification, commit with `git add -u` and continue
- If fixes break re-verification, revert with `git checkout -- .` and log to deferred queue
- Continue without pausing — cross-model review never blocks
- Do NOT use AskUserQuestion — this breaks auto-advance

---

**REMINDER**: Local verification must pass before production verification. If any local check fails, stop and report — do not proceed to production checks.
