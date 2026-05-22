---
name: agent-ops-implementation
description: "Implement only after a validated/approved plan. Use for coding: small diffs, frequent tests, no refactors, stop on ambiguity."
category: core
invokes: [agent-ops-state, agent-ops-validation, agent-ops-testing, agent-ops-git, agent-ops-tasks, agent-ops-debugging]
invoked_by: []
state_files:
  read: [constitution.md, baseline.md, focus.md, issues/*.md, issues/references/*]
  write: [focus.md, issues/*.md]
---

# Implementation workflow

**Works with or without `aoc` CLI installed.** Issue tracking can be done via direct file editing.

## Build/Test Commands (from constitution)

Implementation uses project-specific commands from **constitution.md**:

```bash
# Read actual commands from .agent/constitution.md
build: uv run python -m build     # or: npm run build
lint: uv run ruff check .         # or: npm run lint  
test: uv run pytest               # or: npm run test
format: uv run ruff format .      # or: npm run format
```

## Issue Tracking (File-Based — Default)

| Operation | How to Do It |
|-----------|--------------|
| Start work | Edit issue in `.agent/issues/{priority}.md`: set `status: in_progress` |
| Add log entry | Append to issue's `### Log` section: `- YYYY-MM-DD: Completed step 1` |
| Create follow-up | Append new issue to appropriate priority file |
| Complete issue | Set `status: done`, add log entry, move to `history.md` |

### Example Implementation Flow (File-Based)

1. Edit issue in `.agent/issues/{priority}.md` — set `status: in_progress`
2. Update `.agent/focus.md` — "Implementing {ISSUE-ID}"
3. Run tests after each change (from constitution)
4. Edit issue — add log entry for progress
5. When done, set `status: done`, add final log entry, move to `history.md`

## CLI Integration (when aoc is available)

When `aoc` CLI is detected in `.agent/tools.json`, these commands provide convenience shortcuts:

| Operation | Command |
|-----------|---------|
| Start work | `aoc issues update <ID> --status in-progress` |
| Add log entry | `aoc issues update <ID> --log "Completed step 1"` |
| Create follow-up | `aoc issues create --type CHORE --title "..."` |
| Complete issue | `aoc issues close <ID> --log "Done"` |

## Preconditions
- Constitution is confirmed.
- Baseline exists.
- Final plan exists and is approved (or stop and ask for approval).
- Work is tracked as an issue (or create one before starting).
- **Implementation details file exists** (from planning phase) — check `.agent/issues/references/{ISSUE-ID}-impl-plan.md`

## Using Implementation Details

**Before starting implementation, check for implementation details:**

1. Look for `.agent/issues/references/{ISSUE-ID}-impl-plan.md`
2. If exists, use it as the primary implementation guide:
   - Follow the detailed code snippets (extensive level)
   - Reference function signatures (normal level)
   - Use file list and approach (low level)
3. If not exists, proceed with plan only (but consider generating details first)

**During implementation, reference the details file for:**
- Exact function signatures to implement
- Edge cases to handle
- Error scenarios to cover
- Test cases to write

## Issue Tracking During Implementation

1) **Reference the issue** being worked on:
   - Update issue status to `in_progress`
   - Note in focus.md: "Implementing {ISSUE-ID}"

2) **Track deferred work**:
   - If you notice something that needs fixing but is out of scope:
   - Create a new issue, don't fix it now
   - Add to current issue's notes: "Related: {NEW-ISSUE-ID}"

## Procedure
1) Implement in small steps (reviewable diffs).
2) After each step:
   - run the smallest reliable test subset
   - update focus
3) **Log file creations** (see File Audit Trail below)
4) If ambiguity appears:
   - stop and ask; do not guess
5) Avoid refactors:
   - if a refactor seems necessary, create an issue + ask permission before doing it.
6) End-of-implementation:
   - run full test suite (or constitution-defined test command)
   - prepare for critical review skill.

## File Audit Trail

**When creating files OUTSIDE `.agent/`, log them for audit purposes.**

This enables `agent-ops-selective-copy` to identify agent-created files when preparing clean PR branches.

### What to Log
- Files created in `src/`, `tests/`, `docs/`, etc.
- Configuration files added to project root
- Any file the user didn't explicitly create themselves

### What NOT to Log
- Files inside `.agent/` (already excluded by convention)
- Files inside `.github/skills/`, `.github/prompts/`, `.github/agents/` (already excluded)
- Temporary files that will be deleted

### Log Format

Append to `.agent/log/created-files.log`:
```
{ISO-timestamp} {action} {relative-path}
```

Actions: `CREATE`, `MODIFY`, `DELETE`

### Logging Commands

**PowerShell:**
```powershell
$timestamp = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
Add-Content -Path ".agent/log/created-files.log" -Value "$timestamp CREATE src/new-file.py"
```

**Bash:**
```bash
echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) CREATE src/new-file.py" >> .agent/log/created-files.log
```

### Example Flow

When implementing a feature that creates `src/utils/helper.py`:

1. Create the file
2. Log it: `2026-01-20T10:15:32Z CREATE src/utils/helper.py`
3. Continue with tests

## Handling Unexpected Failures

**If tests fail unexpectedly during implementation, invoke `agent-ops-debugging`:**

1. **Don't guess** — use systematic debugging process
2. **Isolate** — is this from your changes or pre-existing?
3. **Diagnose** — form hypothesis, test it
4. **Decide**:
   - If your change caused it → fix before continuing
   - If pre-existing → document, create issue, continue
   - If unclear → escalate to user

```
⚠️ Test failure during implementation step {N}.

Debugging analysis:
- Hypothesis: {what you think caused it}
- Evidence: {what you found}

Options:
1. Fix and continue (my change caused this)
2. Create issue and continue (pre-existing)
3. Need help investigating
```

## Issue Discovery After Implementation

**After implementation complete, invoke `agent-ops-tasks` discovery procedure:**

1) **Collect follow-up items discovered during implementation:**
   - TODOs left in code → `CHORE` issues
   - Edge cases to handle later → `BUG` or `ENH` issues
   - Tests to add → `TEST` issues
   - Documentation needed → `DOCS` issues
   - Related improvements noticed → `ENH` or `REFAC` issues

2) **Present to user:**
   ```
   📋 Implementation complete for {ISSUE-ID}. Found {N} follow-up items:
   
   - [TEST] Add edge case tests for empty input
   - [DOCS] Document new API endpoint
   - [ENH] Consider caching for performance
   
   Create issues for these? [A]ll / [S]elect / [N]one
   ```

3) **Update original issue:**
   - Status: `done` (or `blocked` if follow-ups are required)
   - Log: "YYYY-MM-DD: Implementation complete, {N} follow-up issues created"

4) **After creating issues:**
   ```
   Created {N} follow-up issues. What's next?
   
   1. Run critical review on changes
   2. Start next priority issue
   3. Work on follow-up item ({ISSUE-ID})
   4. Mark original issue done and commit
   ```

## Low Confidence Hard Stop (MANDATORY)

**When confidence is LOW, implementation MUST stop after EACH issue for human review.**

This is non-negotiable. Low confidence means high uncertainty — human oversight is critical.

### Hard Stop Trigger

After completing implementation of a LOW confidence issue:

1. **DO NOT** proceed to next issue automatically
2. **DO NOT** batch multiple issues
3. **MUST** present hard stop checkpoint

### Hard Stop Checkpoint Template

```
🛑 LOW CONFIDENCE HARD STOP — Human Review Required

## Implementation Complete: {ISSUE-ID}

### Changes Made
- {file1}: {description of change}
- {file2}: {description of change}

### Tests Executed
- Test command: {command from constitution}
- Result: {PASS/FAIL} ({N} tests, {coverage}% coverage)
- New tests added: {count}

### Coverage Analysis
- Lines changed: {N}
- Lines covered by tests: {N} ({percentage}%)
- Branches covered: {N} ({percentage}%)

### Implementation Details Reference
- Spec file: {path to impl-plan.md}
- Adherence: {followed spec / deviated because...}

### Questions for Reviewer
1. {Any uncertainties encountered}
2. {Any assumptions made}

---

⏸️ WAITING FOR HUMAN APPROVAL

Please review the changes and respond:
- [A]pprove — continue to next issue or critical review
- [R]equest changes — specify what needs modification
- [D]iscuss — need clarification before deciding
```

### After Human Approval

Only after explicit human approval:

1. Update issue status to `done` (or `needs-changes` if requested)
2. Log the approval in issue notes
3. Proceed to critical review OR next issue (human's choice)

### Batch Size Enforcement

| Confidence | Issues per Iteration | Hard Stop |
|------------|---------------------|------------|
| LOW | 1 (hard limit) | After each issue |
| NORMAL | Up to 3 | Soft stop (ask, continue) |
| HIGH | Up to 5 | Minimal (report only) |

**For LOW confidence, batch size is ALWAYS 1.** The agent must not group issues.
