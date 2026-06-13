---
name: generate
description: >-
  Phase 2 of the prd-taskmaster pipeline: spec generation and task parsing.
  Loads a template (comprehensive|minimal), fills it with DISCOVER-phase
  constraints and answers, validates the spec (placeholders_found, grade
  thresholds), parses the PRD into tasks via task-master, runs TaskMaster's
  native complexity analysis, and expands every task into verifiable subtasks.
  Autonomous-safe. Declares GENERATE complete so HANDOFF can follow.
user-invocable: false
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Skill
  - ToolSearch
  - mcp__atlas-engine
  - mcp__plugin_prd_go
  - mcp__plugin_prd-taskmaster_go
  - mcp__plugin_atlas-go_go
---

# Phase 2: Generate

Declarative phase skill. Invoked by the prd-taskmaster orchestrator when
`current_phase` is `GENERATE`. Never called directly by a user.

The one rule: **generate the spec, validate it catches placeholders, parse it
into tasks, expand every task into subtasks. Quality over speed.**

## Entry gate

1. Call `mcp__plugin_prd_go__check_gate(phase="GENERATE", evidence={})`.
   If the call returns `{gate_passed: false, violations: [...]}`, report the
   violations and stop. The gate protects against re-entering a completed
   phase or skipping ahead from DISCOVER.

   **Known issue (Mum dogfood feedback [10] — WORST):** check_gate(GENERATE)
   currently checks `task_count > 0`, `subtask_coverage >= 1.0`, and
   `validation_grade in (EXCELLENT, GOOD)` — all of which are GENERATE's
   OWN OUTPUTS, not entry preconditions. First-time entry deadlocks. State
   machine LEGAL_TRANSITIONS already prevents illegal entry — proceed past
   this gate on first entry. Semantic fix in flight (see morning brief).
2. Read the DISCOVER output (discovery summary + `CONSTRAINTS CAPTURED` block
   + scale classification). If any of these are missing, report and stop — the
   gate should have caught this, but belt-and-braces.

## Generate checklist

Copy into your response before running the procedure:

```
GENERATE CHECKLIST:
- [ ] Template loaded (comprehensive|minimal)
- [ ] Spec written with discovery answers (no bare placeholders remaining)
- [ ] CONSTRAINT CHECK: every DISCOVER constraint appears in the spec
- [ ] SCOPE CHECK: task count matches scale (Solo 8-12, Team 12-20, Enterprise 20-30)
- [ ] Validation score: ___ / ___ (grade: ___)
- [ ] placeholders_found: ___ (bare placeholders = 0 required)
- [ ] Warnings addressed or acknowledged
- [ ] Tasks parsed: ___ tasks created
- [ ] Complexity analyzed via TaskMaster: Y/N
- [ ] All tasks expanded into subtasks: Y/N
```

## Step 1: Choose and load template

Decide based on discovery depth:

- **Comprehensive**: 4+ detailed answers, complex project, Team / Enterprise scale
- **Minimal**: thin answers, user wants speed, Solo scale

**MCP (preferred)**: `mcp__plugin_prd_go__load_template(type="comprehensive")`

**CLI fallback**: `python3 script.py load-template --type comprehensive`

The template is the canonical shape — do not invent your own. If the template
load fails, report and stop. Do not paper over with a home-rolled skeleton.

## Step 2: Generate spec at `.taskmaster/docs/prd.md`

Fill the template with discovery answers. AI judgment required:

- Replace ALL placeholders with actual content pulled from DISCOVER.
- Expand with project-specific details — do not leave template prose verbatim.
- Add technical depth proportional to what the user provided in discovery.
- Generate domain-appropriate sections (pentest = threat model, app = user
  stories, business = success metrics, learning = assessment criteria).
- Document assumptions where discovery was thin — explicitly, not silently.

### CONSTRAINT CHECK (MANDATORY)

Verify EVERY constraint from the DISCOVER phase `CONSTRAINTS CAPTURED` block
appears in the spec. If "must use Python" was a constraint, the spec MUST
reference Python. Missing constraints = spec bug.

Emit the check explicitly:

```
CONSTRAINT CHECK:
- Tech stack (Python): FOUND in spec section "Technical Stack"
- Timeline (MVP in 2 weeks): FOUND in spec section "Milestones"
- ...
```

Every constraint must be marked FOUND. If any are MISSING, loop back and
fix the spec before proceeding.

### SCOPE CHECK (MANDATORY)

Use the scale classification from DISCOVER to set task count range:

| Scale      | Task Count | Subtask Depth    |
|------------|-----------|------------------|
| Solo       | 8–12      | 2–3 subtasks each |
| Team       | 12–20     | 3–5 subtasks each |
| Enterprise | 20–30     | 5–8 subtasks each |

If DISCOVER classified the project as Team but the spec implies 30 tasks,
that's a scope bug — narrow the spec or re-classify explicitly.

### Domain-neutral vocabulary

When the domain is unclear, default to neutral terms:

| Software term | Neutral equivalent | When to use neutral |
|---------------|-------------------|---------------------|
| tests         | verification criteria | pentest, business, learning |
| code          | deliverable        | business, learning |
| deploy        | execute / deliver  | business, learning |
| repo          | workspace          | non-software |
| PR            | output / submission | non-software |

If the domain IS software, use software terms. Neutral terms are for
non-software goals.

### Deferred decisions — the `reason:` convention

Every `[placeholder]`, `{{variable}}`, `[TBD]`, `[TODO]` must be either:

(a) Replaced with real content,
(b) Removed entirely, or
(c) **Paired with a `reason:` explanation** on the same line or the next line
    documenting why the decision is deferred.

Per the v4 spec: placeholders with `reason:` attribution are allowed and
surfaced in the validation output as `deferred_decisions`. A bare placeholder
is a validation failure; an attributed one is a known deferred decision with
accountability.

Examples:

```
# BAD — bare placeholder, fails validation:
Target latency: {{TBD}}

# GOOD — attributed, appears in deferred_decisions:
Target latency: {{TBD}} reason: awaiting load-test results scheduled 2026-04-20
```

Write the final spec to `.taskmaster/docs/prd.md`. This is the canonical
path — downstream tools read from here.

## Step 3: Validate spec quality

**MCP (preferred)**: `mcp__plugin_prd_go__validate_prd(input_path=".taskmaster/docs/prd.md")`

**CLI fallback**: `python3 script.py validate-prd --input .taskmaster/docs/prd.md`

Returns: `score`, `grade`, `checks`, `warnings`, `placeholders_found`.

**Optional AI-augmented review** (opt-in): pass `--ai` (CLI) or `ai=True` (MCP)
to additionally invoke TaskMaster's configured main model for a holistic
quality review. The deterministic regex checks always run first — AI review
is additive, never a replacement.

**Grading thresholds:**

- EXCELLENT: 91%+
- GOOD: 83–90%
- ACCEPTABLE: 75–82%
- NEEDS_WORK: <75%

**Decision rules:**

- If `placeholders_found > 0` (bare placeholders, not `reason:`-attributed):
  fix before proceeding. No exceptions.
- If grade is NEEDS_WORK: offer auto-fix or proceed-with-risk — do not silently
  advance. Surface the decision.
- If grade is ACCEPTABLE or better AND placeholders_found == 0: proceed to
  Step 4.

## Step 4: Parse tasks via backend

Calculate task count first:

**MCP**: `mcp__plugin_prd_go__calc_tasks(requirements_count=<count>)`

**CLI**: `python3 script.py calc-tasks --requirements <count>`

Then parse through the normative backend operation:

**backend op parse-prd**: `python3 script.py parse-prd --input .taskmaster/docs/prd.md --num-tasks <recommended>`

**TaskMaster backend direct methods** (only when explicitly operating that backend):
- **MCP**: `mcp__task-master-ai__parse_prd(input=".taskmaster/docs/prd.md", numTasks=<recommended>)`
- **MCP fallback**: `mcp__plugin_prd_go__tm_parse_prd(input_path=".taskmaster/docs/prd.md", num_tasks=<recommended>)`
- **CLI**: `task-master parse-prd --input .taskmaster/docs/prd.md --num-tasks <recommended>`

The backend operation writes to `.taskmaster/tasks/tasks.json`. Verify the file exists
and contains the expected number of tasks before continuing.

## Step 5: Rate complexity via backend

Use the normative backend operation instead of home-rolled classification:

**backend op rate**: `python3 script.py rate`

**TaskMaster backend direct methods** (only when explicitly operating that backend):
- **MCP**: `mcp__task-master-ai__analyze_complexity` (analyzes all tasks)
- **MCP fallback**: `mcp__plugin_prd_go__tm_analyze_complexity` (wraps the CLI)
- **CLI**: `task-master analyze-complexity`

**Important — output location**: the TaskMasterBackend internal
`analyze-complexity` step does NOT emit JSON to stdout. It writes structured
analysis to
`.taskmaster/reports/task-complexity-report.json` and prints a human-readable
table to stdout. To read the structured result, read the report file:

```bash
cat .taskmaster/reports/task-complexity-report.json | jq .
```

Do not try to parse the stdout table — it's colour-coded ASCII and will break
consumers. TaskMaster's built-in analysis is more accurate than anything
hand-rolled because it has full context of the task graph and dependencies.

## Step 6: Expand tasks into subtasks (MANDATORY)

Every task MUST be expanded into subtasks before HANDOFF. Subtasks are
verifiable checkpoints — without them, tasks are black boxes that either
pass or fail with no intermediate proof.

### Use backend op expand, NOT bare per-id parallel calls

Per-id parallel calls (e.g. `task-master expand --id=1 & task-master expand
--id=2 &`) hit a non-atomic read-modify-write race on
`.taskmaster/tasks/tasks.json`: every parallel writer reads the same starting
snapshot, adds its own subtasks, and writes the whole file back. The last
writer wins and earlier writes are silently lost — the AI call reports
success, the subtasks were generated, but they never landed on disk.
Detected in the v4 Shade dogfood 2026-04-13.

**backend op expand** is the correct path:

```bash
python3 script.py expand
```

The backend operation chooses the correct implementation. Its
TaskMasterBackend.expand internals may use serial native expansion,
`tm-parallel`, or the TaskMaster backend direct methods below. The native/agent
path uses agent-parallel planning and atomic apply when direct native API
expansion is unavailable.

**TaskMaster backend direct methods** (only when explicitly operating that backend):

```bash
# Preferred: research-enriched expansion (when a research provider is configured)
task-master expand --all --research

# Fallback: structural-only (still valuable; always available)
task-master expand --all
```

**MCP note on `expand_task`**: task-master's MCP currently exposes
`expand_task(id=...)` per-task only. Do NOT call `expand_task` in parallel
across IDs — same race, same data loss. If you must use the MCP, call
`expand_task` serially for every task, or shell out to
`task-master expand --all` via Bash.

### Patience under slow providers

Under `claude-code` (Claude Max rate-limited) or local `ollama`, `--all`
can run for 5–15 minutes on a 12-task project. Do NOT time out aggressively.
Use `.taskmaster/tasks/tasks.json` mtime as the liveness signal:

- **mtime updated within last 60s** → work is landing, keep waiting
- **mtime stale for 120s+** → investigate (rate limit, provider crash, network)
- **Never conclude STUCK from a single capture** — always compare two
  snapshots 30–60s apart

### Verify coverage (read tasks.json DIRECTLY, not `task-master list`)

`task-master list --format json` has been observed to return a different
top-level schema from `tasks.json`, causing consumers to report 0/N
coverage even when all tasks have subtasks on disk (v4 dogfood LEARNING
#15). Always read the canonical file directly:

```bash
python3 -c "
import json
d = json.load(open('.taskmaster/tasks/tasks.json'))
# tasks.json is tag-grouped (master, defaults, feature branches) — walk all tags
all_tasks = []
if 'master' in d and isinstance(d['master'], dict):
    all_tasks = d['master'].get('tasks', [])
elif 'tasks' in d:
    all_tasks = d['tasks']
else:
    for v in d.values():
        if isinstance(v, dict) and 'tasks' in v:
            all_tasks.extend(v['tasks'])

counts = [len(t.get('subtasks', [])) for t in all_tasks]
covered = sum(1 for c in counts if c > 0)
total = len(all_tasks)
no_subs = [t['id'] for t in all_tasks if not t.get('subtasks')]

if no_subs:
    print(f'WARNING: {covered}/{total} tasks expanded. Missing: {no_subs}. Re-run backend op expand.')
else:
    print(f'OK: All {total} tasks expanded ({sum(counts)} subtasks total).')
"
```

### Idempotent recovery

If any task still shows 0 subtasks after `--all` completes (rate-limit hiccup,
provider timeout, partial run), re-run the same command:

```bash
python3 script.py expand
```

The backend operation only re-expands tasks that are still in `pending` state
with 0 subtasks, so a second invocation is safe and recovers gracefully. Do NOT
work around it with parallel per-id calls — that is the exact pattern that
causes silent data loss.

## Evidence gate

**Gate: spec validation grade is ACCEPTABLE+ AND placeholders_found == 0 AND
tasks parsed AND complexity analyzed AND all tasks have subtasks in
`.taskmaster/tasks/tasks.json`.**

Emit a compact one-block status:

```
Generate:
  spec: .taskmaster/docs/prd.md (grade: <grade>, score: <n>/<total>)
  placeholders_found: <n> (bare), <m> deferred_decisions
  tasks parsed: <n>
  complexity report: .taskmaster/reports/task-complexity-report.json
  subtask coverage: <n>/<n> tasks expanded (<total> subtasks)
```

## Exit gate

After the evidence gate passes:

1. Call `mcp__plugin_prd_go__advance_phase(expected_current="GENERATE", target="HANDOFF", evidence={"validation_grade": "<EXCELLENT|GOOD|ACCEPTABLE>", "task_count": <int>, "subtask_coverage": <float 0-1>, "placeholders_found": <int>})`.
   The call atomically transitions `pipeline.json` from GENERATE to HANDOFF.
   The `expected_current` field is the compare-and-swap guard;
   `evidence` is stored under `phase_evidence[HANDOFF]` for audit.
2. Return control to the orchestrator (`prd-taskmaster` skill). Do NOT invoke
   HANDOFF directly — the orchestrator re-reads `current_phase` and routes.

## Red flags (stop and report, do not paper over)

- "The validation says placeholders_found=3 but the content reads fine —
  I'll advance anyway" → NO. Bare placeholders are a hard fail. Fix or
  attribute with `reason:`.
- "`task-master expand --all` is slow, let me run `expand_task` in parallel
  across IDs to speed it up" → NO. That is the exact race that silently
  drops subtasks. Serial `--all` or serial per-id only.
- "A constraint from DISCOVER isn't in the spec — I'll add it to the
  handoff note instead" → NO. Constraints live in the spec. Fix the spec.
- "Complexity analyze output looked odd, I'll skip reading the JSON report"
  → NO. Read `.taskmaster/reports/task-complexity-report.json` directly;
  the stdout table is decoration.
- "I can call advance_phase without check_gate" → NO. Gate first, always.
- "The template prose is close enough, I'll ship it verbatim" → NO. The
  template is a shape, not content. Fill every section with project-specific
  material.

## Non-exits

This skill does not use explicit process termination. A hard block reports
the reason and returns control to the orchestrator; the orchestrator decides
whether to surface to the user.
