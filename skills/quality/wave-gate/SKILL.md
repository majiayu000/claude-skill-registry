---
name: wave-gate
version: "2.1.0"
description: "Run after wave implementation complete. Executes test + spec-check + review gate sequence. Usage: /wave-gate"
---

# Wave Gate - Test, Spec & Review Sequence

Executes the gate sequence after all wave tasks reach "implemented". Verifies test evidence, checks spec alignment, spawns code reviewers, and advances waves.

**Run this after SubagentStop hook outputs "Wave N implementation complete".**

**Important:** State file writes via Bash are blocked by `guard-state-file.sh`. All state mutations happen through SubagentStop hooks and whitelisted helper scripts. Read access (jq, cat) is allowed.

---

## Sequence

### Step 1: Verify State

```bash
jq '{wave: .current_wave, impl_complete: .wave_gates[.current_wave | tostring].impl_complete}' .claude/state/active_task_graph.json
```

Abort if `impl_complete != true`.

### Step 2: Verify Test Evidence

Test evidence is set **automatically** by the `update-task-status.sh` SubagentStop hook when implementation agents complete. It extracts pass markers (Maven, Node, Vitest, pytest) from agent transcripts and stores per-task `tests_passed` + `test_evidence`.

**Check evidence status (read-only):**
```bash
bash ~/.claude/hooks/helpers/mark-tests-passed.sh
```

This prints per-task evidence status. Exit 0 = all tasks have evidence, exit 1 = missing.

**If evidence missing** → re-spawn the implementation agent for that task. The agent MUST run tests and the SubagentStop hook must see pass markers in the transcript.

**New test verification:** The `verify-new-tests.sh` SubagentStop hook also checks that agents wrote NEW test methods (not just reran existing). It diffs against the per-task `start_sha` baseline (set by PreToolUse hook) to scope detection to each task's changes. Both `tests_passed` and `new_tests_written` must be true for the wave gate to pass.

**Do NOT manually run tests or set test flags.** The guard hook blocks direct state file writes. Evidence can only come from agent execution → SubagentStop hook extraction.

### Step 3: Spawn Verification (Parallel)

Spawn **spec-check AND code reviewers** in a single message with multiple Task calls.

**Get wave info:**
```bash
WAVE=$(jq -r '.current_wave' .claude/state/active_task_graph.json)
TASKS=$(jq -r ".tasks[] | select(.wave == $WAVE) | .id" .claude/state/active_task_graph.json | tr '\n' ',')
```

**Get wave changes:**
```bash
BASE=$(git rev-parse --abbrev-ref origin/HEAD 2>/dev/null | sed 's|origin/||' || echo "main")
git diff --name-only $BASE...HEAD
```

**Get tasks needing review:**
```bash
jq -r ".tasks[] | select(.wave == $WAVE) | select(.review_status == \"pending\" or .review_status == \"blocked\") | .id" .claude/state/active_task_graph.json
```

**Spawn ALL in parallel (single message, multiple Task calls):**

1. **Spec-check invoker** (always, once per wave):
```markdown
## Spec Alignment Check
**Wave:** {wave}
**Tasks:** {task_ids}

Invoke /spec-check to verify implementation aligns with specification.
Output format required:
- SPEC_CHECK_WAVE: {wave}
- CRITICAL/HIGH/MEDIUM findings
- SPEC_CHECK_CRITICAL_COUNT: N
- SPEC_CHECK_VERDICT: PASSED | BLOCKED
```

2. **Review invoker per task** (for each task needing review):
```markdown
## Task: {task_id}
**Description:** {task description}

Files: {comma-separated files relevant to this task}
Task: {task_id}

Call: Skill(skill: "review-pr", args: "--files {files} --task {task_id}")
```

**What happens automatically on completion:**

| Agent | SubagentStop Hook | Effect |
|-------|-------------------|--------|
| spec-check-invoker | `store-spec-check-findings.sh` | Sets `spec_check.critical_count`, `spec_check.verdict` |
| review-invoker | `store-reviewer-findings.sh` | Sets `review_status` per task |

**File-to-task mapping algorithm (for reviewers):**
1. Get task description keywords (e.g., "JWT service" → jwt, token, auth)
2. Filter wave changes to files matching keywords or parent directories
3. If <3 files match, include all wave changes for that task
4. If ambiguous, prefer over-inclusion (review more rather than miss files)

### Step 4: Post GH Comment

After all verification agents complete, read status and post summary:

```bash
gh issue comment {ISSUE} --body "$(cat <<'EOF'
## Wave {N} Verification

### Spec Alignment
**Status:** {PASSED | BLOCKED}
{if blocked: list critical findings}

### Code Review

#### T1: {description}
**Status:** PASSED | BLOCKED - {N} critical findings
- {findings list}

#### T2: {description}
...

---
**Wave Status:** PASSED - Ready to advance | BLOCKED - fix issues
EOF
)"
```

**If GH comment fails** (rate limit, auth, network):
- Log summary to `.claude/state/wave-{N}-review.md` as fallback
- Proceed with gate logic - don't block on comment failure
- Retry comment post after gate decision

### Step 5: Advance

Call `complete-wave-gate.sh` — it handles ALL verification and advancement:

```bash
bash ~/.claude/hooks/helpers/complete-wave-gate.sh
```

The helper performs **five checks** before advancing:
1. **Per-task test evidence** — all wave tasks must have `tests_passed == true`
2. **New tests written** — all wave tasks must have `new_tests_written == true`
3. **Spec alignment** — `spec_check.critical_count == 0`
4. **Per-task review status** — all wave tasks must have `review_status != "pending"`
5. **No critical findings** — code review `critical_findings` count must be 0

If any check fails, the helper exits with error and the wave does NOT advance. Fix the issue and re-run `/wave-gate`.

On success: marks tasks "completed", updates GH issue checkboxes, advances to next wave.

---

## Re-run After Fixes

When issues fixed, run `/wave-gate` again. It will:
- Skip test verification if evidence already present
- Re-run spec-check (always runs, overwrites previous)
- Re-review ONLY tasks with `review_status == "blocked"`
- Advance when all clear

---

## Handling Failures

### Spec-Check Failures

| Symptom | Cause | Recovery |
|---------|-------|----------|
| No SPEC_CHECK_CRITICAL_COUNT | Output malformed | Re-spawn spec-check-invoker |
| spec_check.verdict missing | Hook parse failed | Check hook output, re-spawn |
| CRITICAL findings | Spec drift detected | Fix drift, re-run /wave-gate |

**Debugging:**
```bash
# Check spec-check status
jq '.spec_check' .claude/state/active_task_graph.json
```

### Review Failures

| Symptom | Cause | Recovery |
|---------|-------|----------|
| No output from reviewer | Agent crashed/timed out | Re-spawn that specific reviewer |
| Malformed output | Skill parsing issue | Re-spawn with explicit format reminder |
| review_status still "pending" | Hook didn't fire/parse | Check hook output, re-spawn reviewer |

**Debugging:**
```bash
# Check per-task review status
jq '.tasks[] | {id, review_status, tests_passed}' .claude/state/active_task_graph.json

# Check wave tasks
WAVE=$(jq -r '.current_wave' .claude/state/active_task_graph.json)
jq -r ".tasks[] | select(.wave == $WAVE) | .id" .claude/state/active_task_graph.json
```

---

## Constraints

- MUST spawn spec-check AND reviewers in parallel (single message)
- MUST use `spec-check-invoker` agent for spec alignment
- MUST use `review-invoker` agent with `--files` and `--task` args
- MUST post GH comment before advancing
- NEVER advance if spec-check has critical findings
- NEVER advance if code review has critical findings
- NEVER manually write to state file (guard hook blocks it)
- All status comes from SubagentStop hooks — cannot be set manually
- `complete-wave-gate.sh` is the ONLY path to advance waves
