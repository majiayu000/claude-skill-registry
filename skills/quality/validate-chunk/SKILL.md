---
name: validate-chunk
description: "Enforcement layer for chunk and story validation. Invokes the chunk-validator agent (haiku), enforces the verdict, routes failures to refine-chunk or test-fix, captures CLI learnings. The orchestrator invokes this skill — never the agent directly."
version: 4.0.0
allowed-tools: ["Read", "Bash", "Glob", "Grep", "Task", "Skill"]
---

# Validate Chunk Skill

You are the **enforcement layer** — the single gateway between the orchestrator and validation. You invoke the chunk-validator agent, enforce the verdict, route failures, and capture learnings. The orchestrator never interprets raw validation output — it only sees your structured result.

## CRITICAL: FAILED Means FAILED

⛔ **A FAILED verdict is NEVER overridden.** You do not:
- Dismiss test failures as "unrelated to this story"
- Skip re-validation because "the fix is obvious"
- Let the orchestrator proceed past a FAILED result

**WARN means WARN — not a failure.** Warnings are informational on non-final chunks. They appear in the report but do NOT trigger refine-chunk routing. The agent promotes WARNs to FAILs on the final chunk automatically.

**ALL tests must pass before a chunk or story completes. No exceptions.**

## When This Activates

- Orchestrator invokes after implementer completes a chunk (per-chunk mode)
- Orchestrator invokes after all chunks complete (story-final mode)
- User asks to "validate", "check", "verify" (manual mode — same behavior)

## Orchestrator Context

The orchestrator passes enriched args with labeled fields:

- `CHUNK:` "N/total: chunk title" — which chunk to validate
- `FILES_CHANGED:` comma-separated paths — files the chunk touched
- `PM:` package manager (pnpm/npm/yarn/bun)
- `PROJECT_ROOT:` absolute path to the project
- `STORY_FILE:` absolute path to the story markdown file
- `MODE:` "per-chunk" (default) or "story-final"

**Fallback:** Args may be just a file path. Detect mode and gather context from state files.

## Phase 1: Invoke Validation Agent

Launch the **chunk-validator** agent using the Task tool. The agent runs quality checks and returns a structured report.

```
Task tool:
  subagent_type: "craft:chunk-validator"
  model: "haiku"
  description: "Validate chunk [CHUNK]"
  prompt: "Run validation checks on this project.

    CHUNK: [CHUNK value]
    FILES_CHANGED: [FILES_CHANGED value]
    PROJECT_ROOT: [PROJECT_ROOT value]
    PM: [PM value]
    STORY_FILE: [STORY_FILE value]
    MODE: per-chunk
    PLUGIN_ROOT: [resolved ${CLAUDE_PLUGIN_ROOT} - the subagent cannot resolve the variable itself]"
```

**For story-final mode**, set CHUNK to "final":

```
Task tool:
  subagent_type: "craft:chunk-validator"
  model: "haiku"
  description: "Validate story-final"
  prompt: "Run story-final validation checks on this project.

    CHUNK: final
    FILES_CHANGED: [all files in story, or empty]
    PROJECT_ROOT: [PROJECT_ROOT value]
    PM: [PM value]
    STORY_FILE: [STORY_FILE value]
    MODE: story-final
    PLUGIN_ROOT: [resolved ${CLAUDE_PLUGIN_ROOT} - the subagent cannot resolve the variable itself]"
```

**NEVER use `run_in_background: true`.** Validation must run synchronously — wait for the agent to complete.

## Phase 2: Parse Output

The agent outputs structured markdown. Parse these fields:

| Field | Format | Example |
|-------|--------|---------|
| Status | `**Status:** PASSED\|FAILED\|PARTIAL` | `**Status:** FAILED` |
| Chunk | `**Chunk:** [value]` | `**Chunk:** 2/4: API routes` |
| Mode | `**Mode:** per-chunk\|story-final` | `**Mode:** per-chunk` |
| Fix count | `**Fix count:** N` | `**Fix count:** 0` |
| Errors | `**Errors:**` section with structured error blocks | See below |
| Warnings | `**Warnings:**` section with structured warning blocks | See below |

**Error block format** (may have multiple):
```
- **Check:** [check name]
- **Type:** [type-error|lint-error|build-error|test-failure|verified-gate-error]
- **File:** [file path]
- **Line:** [line number or -]
- **Message:** [error message]
- **Pattern:** [generalized pattern]
```

**Warning block format** (may have multiple):
```
- **Check:** [check name]
- **Type:** [lint-warning|any-type-warning|token-warning|verified-gate-warning|rot-warning]
- **File:** [file path]
- **Line:** [line number or -]
- **Message:** [warning message]
```

## Phase 3 and Phase 4: Independent Concerns

Phase 3 (verdict routing) and Phase 4 (CLI error detection) run independently - order doesn't matter. Phase 4 never changes the verdict. Phase 5 (event emission) always runs last.

## Phase 3: Enforce Verdict and Route

### If PASSED

**Gate reconcile beat (both per-chunk branches):** Read `${CLAUDE_PLUGIN_ROOT}/commands/references/gate-reconcile.md` and run it inline (NOT via the Skill tool) BEFORE complete-chunk.sh. Steady state (Gates row `full coverage`, no rot-warnings) exits silently; an uncovered undecided signal gets the offer AskUserQuestion (accept wires it; decline is risk-confirmed then permanently silent; no answer stays pending for the next attended PASS). Never fires on FAILED.

Per-chunk mode (non-final):
- Run complete-chunk.sh: `bash ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/complete-chunk.sh`
- Emit validation event (Phase 5)
- **Write a continuation breadcrumb** before outputting the summary. This protects the "continue to next chunk" step - if the agent stops after outputting the summary, the Stop hook catches it:
```bash
cat > "${CRAFT_PROJECT_ROOT:-.}/.craft/.continuation" << CRUMB
ACTION: Continue implementation loop - checkpoint, then implementer for next chunk, then validate-chunk
SKILL: craft:craft-story-implement
ARGS: Continue from chunk ${CHUNK} - next chunk ready
WRITTEN_BY: validate-chunk
TIMESTAMP: $(date -u +%Y-%m-%dT%H:%M:%S)
CRUMB
```
- Output validation summary with `>>> NEXT ACTION:` directive, then execute it immediately
- The breadcrumb is cleaned up at the START of the next validation cycle (not this one)

Per-chunk mode (final chunk):
- Run complete-chunk.sh: `bash ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/complete-chunk.sh`
- Emit validation event (Phase 5)
- Write continuation breadcrumb for story-final validation
- Output summary directing to story-final, then execute immediately

Story-final mode:
- Clean up any OLD breadcrumb: `rm -f "${CRAFT_PROJECT_ROOT:-.}/.craft/.continuation"`
- Emit validation event (Phase 5)
- **Write a NEW continuation breadcrumb** for the Step 5 completion flow. This is the most critical breadcrumb in the chain - without it, the orchestrator stops after story-final passes and never runs self-critique or complete-story.sh:
```bash
cat > "${CRAFT_PROJECT_ROOT:-.}/.craft/.continuation" << CRUMB
ACTION: Story-final PASSED. Continue Step 5 of craft-story-implement: Self-Critique, Usage Summary, Learnings, Spark Verification, then run complete-story.sh. DO NOT STOP until complete-story.sh has run.
SKILL: craft:craft-story-implement
ARGS: STORY_FINAL_PASSED — Continue Step 5 completion flow. Run self-critique, usage summary, learnings check, spark verification, then complete-story.sh.
WRITTEN_BY: validate-chunk (story-final)
TIMESTAMP: $(date -u +%Y-%m-%dT%H:%M:%S)
CRUMB
```
- Output validation summary, then immediately proceed to Step 5 in the orchestrator flow

### If FAILED — Validate-Fix-Revalidate Loop

⛔ **This is an internal loop. Do NOT hand back to the orchestrator between fix and re-validation.** The loop runs entirely within this skill invocation - no turn boundaries, no breadcrumbs, no stop opportunities. This eliminates the chain break where the worker stalls after refine-chunk returns.

**Initialize `REFINE_COUNT=0` at the start of each chunk validation cycle.**

```
VALIDATE-FIX-REVALIDATE LOOP:

  1. Parse error types from agent output
  2. Route to fix skill (test-fix or refine-chunk)
  3. Fix skill returns
  4. Re-invoke chunk-validator agent (Phase 1) immediately
  5. Parse new output (Phase 2)
  6. If PASSED → exit loop, continue to PASSED path
  7. If FAILED → check REFINE_COUNT, loop back to step 2
  8. If REFINE_COUNT >= 4 → exit loop, escalate
```

### Step 1: Classify Errors

Parse the `**Type:**` field from each error in the `**Errors:**` section.

**Mixed error types:** If the output contains BOTH `test-failure` AND non-test errors (type-error, lint-error, build-error), route to **refine-chunk first**. The reasoning: type/build errors often cause test failures as a side effect, so fixing the code errors first may resolve the tests too. If tests still fail after refine-chunk, the next loop iteration will route to test-fix.

### Step 2: Invoke Fix Skill

**Test failures** (`Type: test-failure` only, no other error types):

→ **INVOKE `craft:test-fix` using the Skill tool** with args:
```
"[STORY_FILE] — Chunk [CHUNK]. Test failures detected.
  CHUNK: [CHUNK value]
  CHUNK_GOAL: [goal from chunk spec]
  FAILING_TESTS: [File and Message from error block]
  ERRORS: [full error block text]
  FILES_CHANGED: [FILES_CHANGED value]"
```

After test-fix returns:
1. If verdict is "Test stale": test-fix updated the test. Continue to Step 3 (re-validate). Do NOT increment REFINE_COUNT.
2. If verdict is "Code wrong" or "Compile error": increment REFINE_COUNT, re-invoke refine-chunk (switch to the non-test path below).
3. If verdict is "Ambiguous": user decides, then route accordingly.

**All other failures** (`Type: type-error`, `lint-error`, `build-error`):

→ Increment `REFINE_COUNT`

→ **INVOKE `craft:refine-chunk` using the Skill tool** with args:
```
"[STORY_FILE] — Chunk [CHUNK]. Validation errors need fixing.
  CHUNK: [CHUNK value]
  ERRORS: [full Errors section from agent output]
  FILES_CHANGED: [FILES_CHANGED value]
  REFINE_COUNT: [current count]"
```

### Step 3: Re-validate Immediately (NO turn boundary)

⛔ **After the fix skill returns, re-invoke the chunk-validator agent IMMEDIATELY.** Do not output a summary. Do not stop. Do not write a breadcrumb. Go directly back to Phase 1.

```
[Fix skill returns with ">>> HAND BACK TO validate-chunk"]
  → Immediately invoke chunk-validator agent (Phase 1)
  → Parse output (Phase 2)
  → Check verdict:
      PASSED → exit loop, go to PASSED path above
      FAILED → check escalation, then loop back to Step 2
```

**This is the critical fix.** The old pattern wrote a breadcrumb and hoped the agent would continue after the fix skill returned. That failed 100% of the time in practice - the worker treated the stop-hook's BLOCKED message as informational and sat at the prompt. By looping internally, there is no turn boundary for the worker to stall at.

### Step 4: Escalation Check (before each loop iteration)

Check REFINE_COUNT before routing to the next fix:

- `REFINE_COUNT >= 2`: Flag for mandatory learnings capture. In an interactive (default) run, ask the user. In an autonomous run (RUN_MODE=autonomous), try a different approach. **Continue the loop.**
- `REFINE_COUNT >= 4`: **Exit the loop.** Clean up any breadcrumb: `rm -f "${CRAFT_PROJECT_ROOT:-.}/.craft/.continuation"`. Stop. Offer rollback.

**Before any rollback, salvage partial work:**

Use **Read** on `$CHECKPOINT_FILE` → parse the `git_ref:` value → `CHECKPOINT_REF`

Then run the salvage script with that value:
```bash
SALVAGE_PATH=$(${CLAUDE_PLUGIN_ROOT}/hooks/scripts/salvage-partial-work.sh \
  "$CHECKPOINT_REF" "[story-name]" [chunk_number] "${CRAFT_PROJECT_ROOT:-.}")
```

**Log the failure:**
```bash
${CLAUDE_PLUGIN_ROOT}/hooks/scripts/append-recovery-log.sh \
  "${CRAFT_PROJECT_ROOT:-.}" "[story-name]" [chunk_number] \
  "[failure_type]" "$SALVAGE_PATH" "$CHECKPOINT_REF" "[error_details]"
```

### Loop Output

Output a single summary after the loop exits (not per-iteration):

```
## Validation Loop: [PASSED after N refines | ESCALATED at REFINE_COUNT N] - Chunk [N/total: title]

Iterations:
1. FAILED (type-error: missing @types/pg) → refine-chunk → fixed
2. FAILED (lint-error: next-env.d.ts) → refine-chunk → fixed
3. PASSED ✓

REFINE_COUNT: [final count]
[If REFINE_COUNT >= 2: "⚠ Flagged for mandatory learnings capture"]
```

### If PARTIAL (warnings only)

**Final chunk override:** If PARTIAL on the final chunk (N/N) and the agent didn't promote warnings to failures, treat as FAILED and route to refine-chunk. The agent is supposed to promote warnings on the final chunk, but validate-chunk enforces this as a safety net. Pass the warnings as errors to refine-chunk with a note that these are promoted warnings.

**Non-final chunks:** Warnings are non-blocking - do NOT trigger refine-chunk.
- Run complete-chunk.sh: `bash ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/complete-chunk.sh`
- Emit validation event (Phase 5)
- Write continuation breadcrumb (same as PASSED path - protects against agent stopping)
- Output validation summary with warnings noted, then continue to next chunk

## Phase 4: CLI Error Detection and Learning Capture

When the agent's output contains patterns indicating CLI/infrastructure errors rather than code errors, capture them as learnings.

**Detection patterns** (check agent output for these):
- `Unknown option` or `unknown option` — wrong flag passed to a tool
- `missing script` or `Missing script` — package.json script not configured
- `command not found` or `not found` — tool not installed
- `ENOENT` — file or directory missing
- `permission denied` — filesystem permission issue
- `Cannot find module` in a non-test context — missing dependency

**When detected, write to `.craft/.learnings.yaml`:**
```yaml
enforcements:
  - pattern: "[generalized pattern, e.g., 'typecheck script must exist in package.json']"
    evidence:
      - source: cli_error
        quote: "[the raw error message]"
        story: "[current story name]"
        date: [today's date]
    occurrences: 1
    status: pending
    type: infrastructure
```

Read the existing `.learnings.yaml` first. If the pattern already exists, increment `occurrences` and add evidence. If the file does not exist, create it.

**CLI errors do NOT change the verdict.** The agent's Status field is the source of truth. CLI errors are captured for future prevention, not for re-routing.

## Phase 5: Emit Validation Event

After processing the agent's result (regardless of verdict), emit a validation event if STORY_FILE was provided:

```bash
CYCLE_DIR=$(dirname "$(dirname "$STORY_FILE")")
STORY_NAME=$(basename "$STORY_FILE" .md)
EVENTS_DIR="${CYCLE_DIR}/.events"

bash ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/append-event.sh \
  "$EVENTS_DIR" "validation_completed" "$STORY_NAME" \
  result="[STATUS]" chunk="[CHUNK]"
```

This runs after Phase 3 (routing) and Phase 4 (learnings). Every validation — PASSED, PARTIAL, or FAILED — gets logged.

## Output Format

Output a structured summary, then **immediately execute the next action.** You ARE the orchestrator - outputting a directive and stopping is the bug that breadcrumbs exist to catch.

**Template** (adapt header and NEXT ACTION based on context):
```
## Validation: [PASSED|PASSED (warnings)|FAILED] - [Chunk N/total: title | (story-final)]

[Table from agent output]
[If warnings: list them as "Warnings (non-blocking, enforced on final chunk): ..."]
[If FAILED: "Routing: [Type] -> invoking [test-fix|refine-chunk]"]

>>> NEXT ACTION: [see below]
```

**NEXT ACTION by scenario:**
- **Per-chunk PASSED (not final):** Continue Step 4 loop - checkpoint, implementer for chunk [N+1], validate-chunk
- **Per-chunk PASSED (final chunk):** Proceed to Step 5: Story Completion - invoke story-final validation
- **Story-final PASSED:** Continue Step 5 - Self-Critique, Usage Summary, complete-story.sh
- **FAILED:** Invoke [test-fix|refine-chunk], then re-validate this chunk
- **Escalation (REFINE_COUNT >= 4):** No NEXT ACTION - stop, salvage, offer rollback

## Remember

- **FAILED means FAILED.** No overrides. No dismissals.
- **WARN means WARN.** Non-blocking on non-final chunks. The agent promotes to FAIL on final chunk.
- **Route, don't fix.** Parse errors, invoke the right skill. Don't attempt fixes yourself.
- **The fix loop is internal.** After refine-chunk or test-fix returns, re-invoke the validator agent immediately within this skill. No turn boundaries, no breadcrumbs, no hand-back. The loop exits on PASS or REFINE_COUNT >= 4.
- **REFINE_COUNT persists across the loop.** It is initialized once at the start and incremented each iteration. It never resets within a chunk validation cycle.
- **Always continue.** After outputting the summary, execute the next action. Breadcrumbs protect the PASSED path (continue to next chunk), not the fix loop.
