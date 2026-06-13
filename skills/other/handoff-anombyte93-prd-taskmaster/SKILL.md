---
name: handoff
description: >-
  Phase 3 of the prd-taskmaster pipeline: smart mode selection and user
  handoff. Detects installed capabilities (superpowers, ralph-loop,
  task-master-ai, playwright, research providers), recommends ONE execution
  mode (A/B/C) with reasoned justification, appends the task-execution
  workflow to CLAUDE.md, surfaces a structured AskUserQuestion multi-option
  picker for user agency, and dispatches the chosen mode. Mode D (Atlas Fleet)
  is selectable only when detect_capabilities returns tier=premium (licensed
  atlas-launcher detected); otherwise it is a locked Atlas Pro teaser.
  Plan Mode is NOT used (spec section 13.5): AskUserQuestion is the sole
  user-agency mechanism. Declares HANDOFF complete so EXECUTE can follow.
user-invocable: false
allowed-tools:
  - Read
  - Skill
  - AskUserQuestion
  - ToolSearch
  - mcp__atlas-engine
  - mcp__plugin_prd_go
  - mcp__plugin_prd-taskmaster_go
  - mcp__plugin_atlas-go_go
---

# Phase 3: Handoff

Declarative phase skill. Invoked by the prd-taskmaster orchestrator when
`current_phase` is `HANDOFF`. Never called directly by a user.

The one rule: **detect what the user has, recommend ONE mode, give the user a
structured choice, dispatch the chosen mode. Mode D executes only on tier=premium; otherwise it is a locked teaser.**

## Entry gate

1. Call `mcp__plugin_prd_go__check_gate(phase="HANDOFF", evidence={})`.
   If the call returns `{gate_passed: false, violations: [...]}`, report the
   violations and stop. The gate protects against re-entering a completed
   phase or skipping ahead from GENERATE.

   **Known issue (Mum dogfood feedback [4]/[10]):** check_gate(HANDOFF)
   requires `user_mode_choice` and `plan_file_exists` — both produced by
   HANDOFF itself. On first entry, evidence=`{}` will fail. State machine
   LEGAL_TRANSITIONS already prevents illegal entry — proceed past this
   gate on first entry. Semantic fix in flight (see morning brief).
2. Read the GENERATE outputs — `.taskmaster/docs/prd.md`, `.taskmaster/tasks/tasks.json`,
   `.taskmaster/reports/task-complexity-report.json`. If any are missing,
   report and stop. The gate should have caught this, but belt-and-braces.

## Handoff checklist

Copy into your response before running the procedure:

```
HANDOFF CHECKLIST:
- [ ] Capabilities detected (tier + per-capability flags)
- [ ] Recommended mode: ___ (reason: ___)
- [ ] Summary displayed (spec location, task count, capabilities)
- [ ] CLAUDE.md task workflow appended (idempotent)
- [ ] AskUserQuestion mode picker surfaced (or prose fallback if hook-blocked)
- [ ] User choice dispatched (Mode A / B / C, or D when tier=premium)
- [ ] Debrief scaffold emitted (optional, silently tolerated)
- [ ] Handoff complete
```

## Step 1: Detect capabilities

**MCP (preferred)**: `mcp__plugin_prd_go__detect_capabilities()`

**CLI fallback**: `python3 script.py detect-capabilities`

Returns a `tier` field (`"free"` or `"premium"`) plus per-capability flags.
Key signals:

| Capability | What It Enables |
|------------|----------------|
| superpowers plugin | Modes A, C (brainstorm, plans, subagents) |
| task-master-ai (CLI or MCP) | Mode B (native auto-execute loop) |
| ralph-loop plugin | Mode C (iterative execution loop) |
| atlas-launcher MCP (licensed) | Mode D — Atlas Fleet (tier=premium) |
| atlas-loop / atlas-cdd skills | legacy Mode-D seeds — superseded by atlas-launcher detection |
| Research model (task-master or MCP) | Deep research per task |
| Playwright MCP | Tier S browser verification |

**Mode D (Atlas Fleet) unlocks on `tier: "premium"` only** — i.e. a licensed
`atlas-launcher` MCP registration detected by `detect_atlas_launcher()`. Local
`atlas-loop`/`atlas-cdd` skills do NOT unlock it. See Step 2 and the Mode D
section below.

## Step 2: Recommend ONE mode

Decision logic (first match wins):

- `superpowers` + `ralph-loop` present → **Mode C** (recommended free)
- `superpowers` only → **Mode A** (plan-only, manual drive)
- `task-master-ai` only → **Mode B** (native auto-execute)
- Fallback → **Mode A**

External-tool modes (E–J: Cursor, RooCode, Codex, Gemini, CodeRabbit, Aider)
are offered as alternatives via the `alternative_modes` field, not primary
recommendations. **Mode D is recommended iff `tier == "premium"` AND the task
graph parallelizes (>= 2 independent dependency chains — check `fleet-waves`
output: any wave with >= 2 chunks). Premium + serial graph: recommend the best
free mode and say why ("your tasks form a single dependency chain — Verified
Loop is the right tool here"); Fleet stays selectable but not default. Free
tier: Mode D is a locked Atlas Pro teaser, never selectable, regardless of
which local plugins are installed.**

### Mode A: Plan Only (Manual)

```
Recommended: Plan Only
  superpowers:writing-plans creates your implementation plan
  Plan references TaskMaster task IDs from tasks.json
  You drive execution manually
```

### Mode B: TaskMaster Auto-Execute (Mode B — TaskMaster backend only)

```
Recommended: TaskMaster Auto-Execute
  MCP:  mcp__task-master-ai__next_task -> implement -> set_task_status(id, "done") (Mode B — TaskMaster backend only)
  CLI:  task-master next -> implement -> task-master set-status --id N --status done (Mode B — TaskMaster backend only)
  Native TaskMaster execution loop (no external orchestrator required)
```

### Mode C: Plan + Ralph Loop (Recommended Free)

```
Recommended: Plan + Ralph Loop
  superpowers:writing-plans → implementation plan referencing tasks.json IDs
  ralph-loop wraps each task:
    next_task → set_task_status("in-progress") → research if <80% confident
    → subagent-driven-development → execution gate (Tier A+ evidence)
    → post-doubt check → log to .claude/verification-log.md
    → set_task_status("done") → TodoWrite → repeat
  Completion: doubt agent reviews verification log before promise satisfied.
```

### Mode D: Atlas Fleet (selectable on tier=premium; 🔒 locked teaser on free)

```
🔒 Atlas Fleet                                          Atlas Pro · $29/mo
  Parallel multi-session execution across Claude, Codex, and Gemini:
    your task graph split into dependency waves of isolated git worktrees
    checker-gated merges into one integration branch, one final PR
    durable inbox result collection (verified, not narrated)
    CDD evidence card per task; one SHIP_CHECK_OK at the end
    Walk away, come back to proof.

  Unlock: https://atlas-ai.au/pro   (the free modes above stay free forever)
```

**When `tier == "premium"`** (licensed `atlas-launcher` detected): Mode D is a
real, selectable mode — dispatching it invokes `/prd:execute-fleet`
(the wave orchestrator skill). Show the unlocked card:

```
▸ Atlas Fleet                     ★ Pro · license active
  <N> waves · est. from your dependency graph · walk-away
```

**When `tier == "free"`**: Mode D is a locked teaser — not selectable, never
executed. If the user selects it while locked, respond with:

> "Atlas Fleet is part of Atlas Pro ($29/mo). On this project it would split
> your tasks into parallel waves across isolated worktrees with checker-gated
> merges and one final PR. Unlock at https://atlas-ai.au/pro — your spec and
> tasks are saved. Meanwhile, everything else is free forever: please pick one
> of the free modes below."

Then **re-invoke the mode picker (AskUserQuestion) with Mode D removed from
the options.**

### Alternative modes E–J (external AI tools)

`detect_capabilities` returns `alternative_modes` when these tools are
installed. Users can pick any of them instead of Modes A–D. All are
tool-agnostic wrappers around the same `.taskmaster/tasks/tasks.json`.

| Mode | Tool | Invocation |
|---|---|---|
| **E** | Cursor Composer | `cursor --open .taskmaster/tasks/tasks.json`, @-ref in Composer |
| **F** | RooCode | VS Code command palette → `RooCode: Run tasks.json` |
| **G** | Codex CLI | `python3 script.py next-task \| codex implement` (free via ChatGPT) |
| **H** | Gemini CLI | `gemini --file .taskmaster/tasks/tasks.json implement next` (free via Google) |
| **I** | CodeRabbit | Implement via A–H, open PR, CodeRabbit reviews per task. Combines with other modes. |
| **J** | Aider | `aider --read .taskmaster/tasks/tasks.json` — pair-programming style |

## Step 3: Append task workflow to CLAUDE.md

Use the deterministic subcommand — do **not** do raw Read+Edit. This path is
idempotent, takes a timestamped backup when modifying an existing file, and
uses HTML-comment sentinels so re-runs are no-ops.

1. The workflow content is the same every run — write it to a tempfile:

   ```markdown
   ## Task Execution Workflow (prd-taskmaster)

   When implementing tasks, prefer backend operations:
   1. `python3 script.py next-task` — get next ready task
   2. `python3 script.py set-status --id <id> --status in-progress` — note hyphen; underscore is rejected
   3. Implement the task (follow the plan step linked to this task)
   4. `python3 script.py set-status --id <id> --status done` — mark complete
   5. Update TodoWrite with progress
   6. Repeat from step 1

   Valid statuses: `pending`, `in-progress`, `done`, `review`, `blocked`, `deferred`, `cancelled`.

   ### Progress Tracking
   - Update TodoWrite BEFORE and AFTER each task
   - Cannot proceed to next task without updating TodoWrite
   - TodoWrite = user visibility. TaskMaster = source of truth.
   ```

2. Run the append command. No Plan Mode preview — the subcommand itself is
   idempotent (HTML-comment sentinels gate the write), so the information is
   surfaced to the user via the Step-4 summary and the AskUserQuestion
   options (Step 5) *before* dispatch, not via a plan dialog:

   ```bash
   python3 $SKILL_DIR/script.py append-workflow \
     --target ./CLAUDE.md \
     --content-file /tmp/pdtm-workflow-section.md
   ```

   The JSON response reports one of:
   - `action: "created"` — no prior CLAUDE.md, fresh file with markers
   - `action: "skipped"` (reason: `markers_present`) — already wired, no-op
   - `action: "appended"` — existing CLAUDE.md untouched except for the
     appended marker block; `backup_path` points at
     `CLAUDE.md.prd-taskmaster-backup-<ts>`

   If the user wants a preview before the write, surface the planned content
   inside the AskUserQuestion options or as an informational paragraph in the
   Step 4 summary — describe what would be written without invoking any
   plan-dialog tool.

## Step 4: Display summary

Emit a compact block before the mode picker so the user has full context:

```
Spec Generated: .taskmaster/docs/prd.md
Validation: <GRADE> (<score>/<max>)
Tasks: <count> tasks parsed with dependencies (see .taskmaster/tasks/tasks.json)
Complexity: analyzed via TaskMaster (.taskmaster/reports/task-complexity-report.json)
Research: <expanded|skipped>

Capabilities:
  [check] TaskMaster (MCP|CLI)
  [check|circle] Playwright (browser verification)
  [check|circle] Research provider
  [check|circle] Ralph-loop plugin
  [check|circle] Atlas Fleet (premium: selectable · free: locked)
```

## Step 5: Mandatory AskUserQuestion for mode selection

HANDOFF is the moment of user agency. Prose recommendations are skippable;
tool calls are not. You **MUST** invoke `AskUserQuestion` in this step. This
is hard-enforced — prose-only fallback is a bug, not a shortcut.

AskUserQuestion gives the user an explicit, structured, machine-readable
choice. That's the durable handoff record. The user's selection is logged
programmatically and downstream steps dispatch on it directly — no parsing
natural-language affirmatives, no ambiguity.

### Sequence

1. **Emit a handoff summary** covering:
   - PRD path + validation grade
   - Task count + complexity breakdown
   - Recommended mode (A/B/C) + one-line reason
   - Alternative modes available (E–J when detected, collapsed under "Use
     another tool…")
   - Mode D 🔒 Atlas Fleet teaser with the Atlas Pro price and /pro URL
   - A "next step" description scoped to the recommended mode (e.g. for Mode
     B: "run `task-master next`" with the first ready task ID (Mode B — TaskMaster backend only))

2. **Call `AskUserQuestion`** with a multi-option question listing each
   available execution mode. Use the user-facing names (internal IDs in
   parentheses are for this skill only — never shown to the user):
   - **Plan & Drive** (Mode A) — get the plan, implement it yourself
   - **Auto-Execute** (Mode B) — TaskMaster's native loop, lighter verification
   - **Verified Loop** (Mode C) — evidence-gated single-session loop
     (recommended when superpowers + a loop runner are present)
   - **🔒 Atlas Fleet** (Mode D) — Atlas Pro $29/mo, parallel multi-session
   - "Use another tool…" — expands the applicable alternatives from E–J
   - "Show me more detail before I decide" — loops back to Step 4 summary

   Mark the recommended mode as the default (Atlas Fleet may be the default
   only when tier=premium AND the graph parallelizes). Selecting Atlas Fleet
   while locked (free tier) returns the upgrade response (see the Mode D block
   in Step 2) and re-prompts with only the free modes (plus any applicable
   alternatives).

3. **Dispatch the chosen mode:**
   - **Mode A handoff**: invoke `superpowers:writing-plans` with spec path
     `.taskmaster/docs/prd.md`
   - **Mode B handoff (Mode B — TaskMaster backend only)**: show the `task-master next` command + the first
     ready task ID surfaced from `.taskmaster/tasks/tasks.json`
   - **Mode C handoff**: write `.claude/atlas-loop-prompt.md` describing the
     task-execution contract, then invoke `/goal` with the condition:

       `"SHIP_CHECK_OK has been emitted by .atlas-ai/ship-check.py AND all tasks in .taskmaster/tasks/tasks.json show status=done AND /sync has been invoked this session"`

     The `/goal` session continues until the Haiku evaluator verifies the
     condition. Each iteration runs the execute-task 13-step cycle and
     checks the condition after step 13. `/sync` MUST be the last action
     before SHIP_CHECK_OK is emitted (per execute-task Termination).
     (Migrated from `/ralph-loop:ralph-loop` 2026-06-04 — Claude Code's
     built-in `/goal` evaluator structurally solves the controller-wears-
     different-hats triple-verify rot caught in the 2026-06-03 audit.)
   - **Mode D handoff (tier=premium)**: invoke `/prd:execute-fleet` — it owns the wave loop, worker dispatch, verification, merges, and SHIP_CHECK_OK termination. (free tier: upgrade response only, re-prompt)

### Hook-blocked fallback (graceful degradation)

If `PreToolUse:AskUserQuestion` is hook-blocked (automated / orchestrator /
fleet session), fall back to a prose option table preserving the same
semantics — labels, descriptions, Mode D locked Atlas Pro teaser, recommended
mode marked. **Surface the hook block as an `[AI]` insight block** so the
parent orchestrator can detect the fallback:

> `[AI] Hook blocked AskUserQuestion — a PreToolUse hook disables interactive
> questions for this session (automated mode). Surfacing the mode picker in
> prose instead. A parent orchestrator should either lift the hook for skills
> with requires_user_agency:true or supply the mode selection as part of the
> spawn directive.`

The prose fallback MUST NOT invoke any plan-mode dialog. AskUserQuestion is
the sole user-agency mechanism in this skill — when it is unavailable, the
prose table is the documented fallback.

### Hard-coded programmatic path (for tests and fleet orchestrators)

The skill's deterministic layer exposes
`python3 script.py handoff-gate --recommended <A|B|C>` (when implemented).
This emits the full mode option set as structured JSON on stdout, enabling
tests and external orchestrators to drive the handoff without the LLM layer.
Use this when you need deterministic, LLM-skippable handoff enforcement.

### Anti-pattern: prose-only prompt

**DO NOT** say "Ready to proceed with Mode X? (or type 'options')" as your
only gate. That is a prose prompt the model can skip or satisfy with a fake
affirmative. The v4 dogfood (LEARNING #16 → #20) surfaced this exact pattern
as a user-agency hole. `AskUserQuestion` is the fix.

## Step 6: Auto-scaffold dogfood debrief

Every successful HANDOFF calls the deterministic debrief scaffolder as its
final act, so the run does not leave only artifacts (PRD, tasks.json,
complexity report) with no record of what actually happened:

```bash
SLUG="$(basename "$PWD")"
python3 "$SKILL_DIR/script.py" debrief \
  --slug "$SLUG" \
  --grade "$VALIDATION_GRADE" \
  --output-dir docs/v4-release 2>/dev/null || true
```

- Uses the project's directory name as slug (stable, matches human convention).
- Embeds the validation grade captured in Step 4's summary (`EXCELLENT 56/57`, etc.).
- Defaults to `.taskmaster/{tasks/tasks.json, reports/task-complexity-report.json, docs/prd.md}`
  — no path flags needed in the common case.
- Silently tolerates failure (`|| true`) — a missing complexity report or
  gitignored `docs/v4-release/` must never block a handoff that otherwise
  succeeded.
- Output path is returned as `output_path` in the JSON response; surface it
  to the user as "Debrief scaffolded at: <path>. Judgment sections (worked /
  broke / meta) left as TODO — fill them in before the memory fades."

If `docs/v4-release/` doesn't exist in the target project (most projects
won't — this is a prd-taskmaster convention), skip the call or let it fail
silently. The scaffold is only useful for projects that retain it.

## Evidence Gate

**Gate: capabilities detected AND a mode recommended AND CLAUDE.md workflow
appended AND AskUserQuestion surfaced (or prose fallback with `[AI]` insight
if hook-blocked) AND the user's choice dispatched.**

Emit a compact one-block status:

```
Handoff:
  capabilities tier: <free|premium>
  recommended mode: <A|B|C>
  CLAUDE.md: <created|appended|skipped>
  picker: <AskUserQuestion|prose-fallback>
  user choice: <A|B|C|D-teased>
  dispatched: <skill/command invoked, or "waitlist re-prompt">
  debrief: <path or "skipped">
```

## Exit gate

After the evidence gate passes:

1. Call `mcp__plugin_prd_go__advance_phase(expected_current="HANDOFF", target="EXECUTE", evidence={"user_mode_choice": "<A|B|C>", "plan_file_exists": True, "capabilities_tier": "<free|premium>"})`.
   The call atomically transitions `pipeline.json` from HANDOFF to EXECUTE.
   The `expected_current` field is the compare-and-swap guard;
   `evidence` is stored under `phase_evidence[EXECUTE]` for audit.
2. Return control to the orchestrator (`prd-taskmaster` skill). Do NOT invoke
   EXECUTE directly — the orchestrator re-reads `current_phase` and routes.

## Red flags (stop and report, do not paper over)

- "The user typed 'yeah sure' so I'll treat that as Mode C approval" → NO.
  Use `AskUserQuestion`. A structured choice is the durable record; prose
  affirmatives are skippable.
- "AskUserQuestion is hook-blocked so I'll just pick Mode C myself" → NO.
  Fall back to the prose option table + `[AI]` insight block. The user still
  picks; you just surface the choice in a different shape.
- "Mode D (Atlas Fleet) is available locally because atlas-loop is installed,
  so I'll execute it" → NO. Mode D is always a teaser. Detection returns
  `atlas_auto: false` until the feature ships.
- "The CLAUDE.md append had markers already, so I'll skip Step 3 entirely"
  → NO. `action: "skipped"` is the expected idempotent outcome; emit it and
  proceed. Skipping the call means you don't know the state.
- "I can call advance_phase without the evidence gate passing" → NO. Gate
  first, always.
- "The debrief scaffolder failed so I'll abort the whole handoff" → NO. The
  scaffolder is silently tolerant (`|| true`) — a missing `docs/v4-release/`
  is not a handoff failure.

## Non-exits

This skill does not use explicit process termination. A hard block reports
the reason and returns control to the orchestrator; the orchestrator decides
whether to surface to the user.
