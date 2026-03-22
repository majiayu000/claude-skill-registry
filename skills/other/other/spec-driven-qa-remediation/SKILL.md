---
name: spec-driven-qa-remediation
description: >
  Process QA gap files and create remediation user stories with structural anti-skip
  enforcement (Execute-Verify-Gate pattern at every step). Applies per-phase reference
  loading, checkpoint persistence, and binary CLI gate enforcement to every step of the
  7-phase QA remediation process. Prevents token optimization bias through lean orchestration,
  fresh-context subagent delegation, and artifact verification. Use when converting QA
  findings into actionable development work, processing imported QA reports, or
  systematically addressing accumulated technical debt from gap files. Always use this
  skill when the user runs /review-qa-reports or mentions QA gap remediation, gap-to-story
  conversion, or technical debt from QA reports.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
  - Task
  - Skill
  - Bash(devforgeai-validate:*)
model: claude-opus-4-6
effort: High
---

# Spec-Driven QA Remediation

Process QA gap files and create remediation user stories through strict 7-phase workflow with gap discovery, deduplication, prioritization, batch story creation, report generation, and technical debt integration.

**Context files are THE LAW:** tech-stack.md, source-tree.md, dependencies.md, coding-standards.md, architecture-constraints.md, anti-patterns.md

**If ambiguous or conflicts detected: HALT and use AskUserQuestion**

---

## Execution Model

This skill expands inline. After invocation, execute Phase State Initialization immediately. Do not wait passively, ask permission, or offer execution options.

**Self-Check (if ANY box is true = VIOLATION):**

- [ ] Stopping to ask about token budget
- [ ] Stopping to offer execution options
- [ ] Waiting passively for results
- [ ] Asking "should I execute this?"
- [ ] Skipping a phase because it "seems simple"
- [ ] Combining multiple phases into one
- [ ] Summarizing instead of loading a reference file
- [ ] Skipping verification because "I already know the result"

**IF any box checked:** EXECUTION MODEL VIOLATION. Go directly to Phase State Initialization now.

---

## Anti-Skip Enforcement Contract

This skill enforces 4 independent anti-skip layers. ALL FOUR must fail for a step to be skipped:

1. **Fresh-context subagent execution** — Story creation runs in isolated context via spec-driven-stories skill invocation
2. **Binary CLI gates** — `devforgeai-validate phase-check/phase-complete/phase-record --workflow=qa-remediation` (compiled, cannot be forged by LLM)
3. **Hook enforcement** — Shell scripts in `.claude/hooks/` run outside LLM control
4. **Step registry + artifact verification** — `.claude/hooks/phase-steps-registry.json` tracks every mandatory step

**Execute-Verify-Record Pattern:** Every mandatory step in every phase file has three parts:
- **EXECUTE:** The exact action to perform
- **VERIFY:** How to confirm the action happened (Glob, Grep, exit code, Task result)
- **RECORD:** CLI command to record completion (`devforgeai-validate phase-record`)

**Token Optimization Bias is PROHIBITED.** Do not skip, compress, or shortcut any step. Every phase step exists because a previous failure proved it necessary.

---

## Purpose

Convert QA gap findings (coverage gaps, anti-pattern violations, code quality issues, deferral problems) into actionable user stories, eliminating technical debt through structured remediation.

### When to Use

- After QA validation produces gap files (`*-gaps.json`)
- When importing QA reports from external projects
- When systematically addressing accumulated technical debt
- When gaps need to be converted to trackable stories

### Philosophy

**"Every gap tracked. Every story actionable. Every phase executed."**

---

## Parameter Extraction

Extract all parameters from `$ARGUMENTS` provided by the `/review-qa-reports` command.

**Skills cannot accept runtime parameters.** All information extracted from conversation context (command arguments, explicit statements, or file references).

| Argument | Variable | Default | Description |
|----------|----------|---------|-------------|
| `--source` | `$SOURCE` | `local` | Gap file source: `local`, `imports`, `all` |
| `--min-severity` | `$MIN_SEVERITY` | From config | Filter threshold: `CRITICAL`, `HIGH`, `MEDIUM`, `LOW` |
| `--epic` | `$EPIC_ID` | null | Associate created stories with epic |
| `--dry-run` | `$DRY_RUN` | false | Preview gaps without creating stories |
| `--add-to-debt` | `$ADD_TO_DEBT` | false | Auto-add deferred gaps to debt register (skip confirmation) |
| `--create-stories` | `$CREATE_STORIES` | false | Auto-create remediation stories (skip confirmation) |
| `--blocking-only` | `$BLOCKING_ONLY` | false | Show only blocking gaps, hide advisory |

**Flag Routing Context:**
- `$ADD_TO_DEBT=true` → Phase 07 skips confirmation prompt
- `$CREATE_STORIES=true` → Phase 05 uses batch mode without prompts

**Combined Flag Operation (`--add-to-debt --create-stories`):**
When BOTH flags are present, stories are created first, then debt entries are added:
1. Phase 05 executes before Phase 07 (stories created first)
2. Phase 07 executes SECOND (gaps added to debt register)
3. Debt entries have Follow-up field pre-populated with created STORY-XXX IDs

## Command Integration

| Context Marker | Set By | Description |
|----------------|--------|-------------|
| `$ARGUMENTS` | /review-qa-reports | Raw command arguments string |
| `$SESSION_ID` | Phase State Init | Generated session identifier |

---

## Phase State Initialization [MANDATORY FIRST]

```bash
source .venv/bin/activate && devforgeai-validate phase-init ${SESSION_ID} --workflow=qa-remediation --project-root=. 2>&1
```

Generate `$SESSION_ID` from timestamp: `qa-rem-{YYYYMMDD-HHmmss}`

| Exit Code | Meaning | Action |
|-----------|---------|--------|
| 0 | New workflow | State file created. Set CURRENT_PHASE = "01". |
| 1 | Existing workflow | Resume. Run `devforgeai-validate phase-status ${SESSION_ID} --workflow=qa-remediation` to get CURRENT_PHASE. |
| 2 | Invalid session ID | HALT. |
| 127 | CLI not installed | Continue without enforcement (backward compatibility). |

**Resume Detection:**
```
Glob(pattern="devforgeai/workflows/checkpoints/qa-remediation-*.checkpoint.json")

IF checkpoint found:
  Read(file_path=checkpoint_path)
  AskUserQuestion:
    Question: "Found existing QA remediation session. Resume or start fresh?"
    Options:
      - label: "Resume session"
      - label: "Start fresh"

  IF "Resume":
    Restore state from checkpoint
    $CURRENT_PHASE = checkpoint.progress.current_phase
  ELSE:
    Delete checkpoint, set CURRENT_PHASE = "01"
ELSE:
  Set CURRENT_PHASE = "01"
```

---

## Phase Orchestration Loop

```
FOR phase_num in [01, 02, 03, 04, 05, 06, 07]:
    phase_id = phase_num

    IF $DRY_RUN == true AND phase_id > 04:
        SKIP remaining phases (dry-run exits after Phase 04)
        BREAK

    1. ENTRY GATE: devforgeai-validate phase-check ${SESSION_ID} --workflow=qa-remediation --from={prev} --to={phase_id} --project-root=.
       IF exit != 0: HALT

    2. LOAD: Read(file_path=".claude/skills/spec-driven-qa-remediation/phases/{phase_files[phase_id]}")
       Load FRESH - do NOT rely on memory of previous reads

    3. EXECUTE: Follow every step in the phase file (EXECUTE-VERIFY-RECORD triplets)
       - Each step's EXECUTE instruction tells you exactly what to do
       - Each step's VERIFY instruction tells you how to confirm it happened
       - Each step's RECORD instruction tells you what CLI command to call

    4. RECORD: devforgeai-validate phase-record ${SESSION_ID} --workflow=qa-remediation --phase={phase_id} --project-root=.

    5. EXIT GATE: devforgeai-validate phase-complete ${SESSION_ID} --workflow=qa-remediation --phase={phase_id} --checkpoint-passed --project-root=.
       IF exit != 0: HALT
```

| Phase | Name | File |
|-------|------|------|
| 01 | Pre-Flight Validation | `phases/phase-01-preflight.md` |
| 02 | Discovery & Parsing | `phases/phase-02-discovery-parsing.md` |
| 03 | Aggregation & Prioritization | `phases/phase-03-aggregation-prioritization.md` |
| 04 | Interactive Selection | `phases/phase-04-interactive-selection.md` |
| 05 | Batch Story Creation | `phases/phase-05-batch-story-creation.md` |
| 06 | Source Report Update | `phases/phase-06-source-report-update.md` |
| 07 | Technical Debt Integration | `phases/phase-07-technical-debt-integration.md` |

---

## Required Subagents Per Phase

| Phase | Required Subagents | Enforcement |
|-------|-------------------|-------------|
| 01 | (none) | N/A |
| 02 | (none) | N/A |
| 03 | (none) | N/A |
| 04 | (none) | N/A |
| 05 | spec-driven-stories (Skill) | BLOCKING |
| 06 | (none) | N/A |
| 07 | technical-debt-analyzer | CONDITIONAL (config-driven) |

**Deviation Protocol:** Any skip requires explicit user consent via AskUserQuestion.

---

## Phase Summaries

Each phase is fully specified in its own file under `phases/`. The summaries below provide orientation; the phase files are the source of truth.

### Phase 01: Pre-Flight Validation (6 steps)

Validate project root, load configuration from `devforgeai/config/qa-remediation.yaml`, parse 7 arguments, validate flag dependencies, verify source paths exist, create checkpoint.

**Reference:** None (inline bootstrap)
**Key Outputs:** `$CONFIG`, `$SOURCE`, `$MIN_SEVERITY`, `$EPIC_ID`, `$DRY_RUN`, `$ADD_TO_DEBT`, `$CREATE_STORIES`, `$BLOCKING_ONLY`, `$GAP_PATHS`

### Phase 02: Discovery & Parsing (5 steps)

Glob gap files from configured sources, parse JSON structure, validate required fields per gap type (coverage_gaps, anti_pattern_violations, code_quality_violations, deferral_issues), handle backward compatibility for missing `blocking` field (defaults to true), build unified normalized gap list.

**Reference:** `references/gap-discovery-workflow.md`
**Key Outputs:** `$GAP_FILES`, `$ALL_GAPS`, `$FILES_PROCESSED`, `$TOTAL_GAPS`

### Phase 03: Aggregation & Prioritization (6 steps)

Deduplicate gaps by file+type+description key, calculate priority scores using severity weights (CRITICAL:100, HIGH:75, MEDIUM:50, LOW:25) plus type modifiers (deferral:+25, security:+15, Business Logic coverage:+10), filter by `$MIN_SEVERITY` threshold, apply `--blocking-only` filter (AND logic with severity), sort by score descending.

**Reference:** `references/gap-aggregation-algorithm.md`
**Key Outputs:** `$UNIQUE_GAPS`, `$FILTERED_GAPS`, `$DEFERRED_GAPS`, `$ADVISORY_HIDDEN_COUNT`

### Phase 04: Interactive Selection (4 steps)

Display gap summary table with [R] (blocking) and [Y] (advisory) indicators, show statistics summary, handle dry-run exit (display and EXIT — no further phases), present AskUserQuestion with selection options (all, CRITICAL only, CRITICAL+HIGH, cancel).

**Reference:** None (user interaction phase)
**Key Outputs:** `$SELECTED_GAPS`, `$SELECTION_COUNT`

**Dry-Run Exit:** If `$DRY_RUN == true`, display summary and EXIT skill. Phases 05-07 are NOT executed.

### Phase 05: Batch Story Creation (7 steps)

Initialize tracking arrays, determine next story ID, generate story context markers per gap (with advisory story naming per STORY-348), invoke `spec-driven-stories` skill in batch mode for each gap, handle `--create-stories` auto-mode (skip confirmation), track created/failed stories with failure isolation, display batch completion summary.

**Reference:** `references/gap-to-story-mapping.md`
**Key Outputs:** `$CREATED_STORIES`, `$FAILED_STORIES`, `$STORIES_CREATED_COUNT`, `$BLOCKING_STORIES_COUNT`, `$ADVISORY_STORIES_COUNT`, `$STORY_ID_MAP`

### Phase 06: Source Report Update (4 steps)

Update LOCAL gap files with `implemented_in` and `remediation_date` fields (imported files are read-only), generate enhancement report from template at `devforgeai/qa/enhancement-reports/{date}-enhancement-report.md`, invoke optional post-qa-remediation hook.

**Reference:** `references/report-update-protocol.md`
**Key Outputs:** `$REPORTS_UPDATED`, `$ENHANCEMENT_REPORT_PATH`

### Phase 07: Technical Debt Integration (8 steps)

Check config for auto-add setting, read current debt register, generate formatted debt entries for `$DEFERRED_GAPS`, append to register under "## Open Debt Items" section, update statistics, handle `--add-to-debt` auto-mode (skip confirmation, pre-populate Follow-up with story IDs from Phase 05), invoke optional technical-debt-analyzer subagent.

**Reference:** `references/technical-debt-update.md`
**Key Outputs:** `$DEBT_ENTRIES_ADDED`, `$REGISTER_UPDATED`

---

## State Persistence

**Checkpoint Location:** `devforgeai/workflows/checkpoints/qa-remediation-${SESSION_ID}.checkpoint.json`

```json
{
  "checkpoint_version": "1.0",
  "session_id": "${SESSION_ID}",
  "workflow": "qa-remediation",
  "created_at": "ISO 8601 timestamp",
  "updated_at": "ISO 8601 timestamp",
  "status": "in_progress|completed|paused",

  "input": {
    "source": "${SOURCE}",
    "min_severity": "${MIN_SEVERITY}",
    "epic_id": "${EPIC_ID}",
    "dry_run": false,
    "add_to_debt": false,
    "create_stories": false,
    "blocking_only": false
  },

  "progress": {
    "current_phase": 1,
    "phases_completed": [],
    "phases_skipped": [],
    "total_steps_completed": 0
  },

  "phases": {
    "01": { "status": "pending", "steps_completed": [] },
    "02": { "status": "pending", "steps_completed": [] },
    "03": { "status": "pending", "steps_completed": [] },
    "04": { "status": "pending", "steps_completed": [] },
    "05": { "status": "pending", "steps_completed": [] },
    "06": { "status": "pending", "steps_completed": [] },
    "07": { "status": "pending", "steps_completed": [] }
  },

  "output": {
    "gap_files_processed": 0,
    "total_gaps": 0,
    "stories_created": 0,
    "debt_entries_added": 0,
    "enhancement_report_path": null,
    "error": null
  }
}
```

---

## Workflow Completion Validation

```
expected_phases = 7  (or 4 if $DRY_RUN)
IF completed_count < expected_phases: HALT "WORKFLOW INCOMPLETE - {completed_count}/{expected_phases} phases"
IF completed_count == expected_phases: "All {expected_phases} phases completed - QA Remediation workflow passed"
```

---

## Final Summary Display

After all phases complete (or after Phase 04 in dry-run mode), display:

```
┌────────────────────────────────────────────────────────────────────────────┐
│                    QA Gap Remediation Complete                              │
├────────────────────────────────────────────────────────────────────────────┤
│ Gap Files Processed:     {$FILES_PROCESSED}                                 │
│ Total Gaps Found:        {$TOTAL_GAPS}                                      │
│   Blocking Gaps:         {$BLOCKING_GAPS_COUNT}                             │
│   Advisory Gaps:         {$ADVISORY_GAPS_COUNT}                             │
│ Gaps Selected:           {$SELECTION_COUNT}                                 │
│ Stories Created:         {$STORIES_CREATED_COUNT}                           │
│   Blocking Stories:      {$BLOCKING_STORIES_COUNT}                          │
│   Advisory Stories:      {$ADVISORY_STORIES_COUNT}                          │
│ Stories Failed:          {count of $FAILED_STORIES}                         │
│ Gaps Deferred to Debt:   {$DEBT_ENTRIES_ADDED}                              │
│ Advisory Gaps Hidden:    {$ADVISORY_HIDDEN_COUNT}                           │
├────────────────────────────────────────────────────────────────────────────┤
│ Enhancement Report: {$ENHANCEMENT_REPORT_PATH}                              │
│ Technical Debt Register: devforgeai/technical-debt-register.md              │
└────────────────────────────────────────────────────────────────────────────┘

Validation: Total Gaps = Blocking Gaps + Advisory Gaps

IF $BLOCKING_ONLY == true:
  "--blocking-only filter active ({$ADVISORY_HIDDEN_COUNT} advisory gaps hidden)"

Next Steps:
1. Review created stories in devforgeai/specs/Stories/
2. Assign stories to sprint via /create-sprint
3. Review deferred gaps in technical-debt-register.md
4. Re-run with --min-severity LOW to address deferred gaps
```

---

## Success Criteria

| Criterion | Validation |
|-----------|------------|
| Gap files discovered | `$FILES_PROCESSED > 0` |
| Gaps parsed | `$TOTAL_GAPS > 0` |
| Selection completed | User made selection or dry-run completed |
| Stories created | `$STORIES_CREATED_COUNT >= 0` |
| Source reports updated | Local files have `implemented_in` field |
| Debt register updated | Deferred gaps added (if any) |
| Enhancement report generated | File exists at `$ENHANCEMENT_REPORT_PATH` |
| Blocking vs advisory distinction | Correct counting per gap `blocking` field |

---

## Error Handling

### HALT Conditions

| Condition | Action |
|-----------|--------|
| Project root invalid | HALT with navigation instructions |
| Config file missing | HALT with creation instructions |
| No gap files found | HALT with generation/import guidance |
| User cancels selection | EXIT gracefully with message |

### Continue Conditions (Failure Isolation)

| Condition | Action |
|-----------|--------|
| Individual story creation fails | Log error, continue to next gap |
| Gap file update fails (imports) | Skip update (imports are read-only) |
| Debt register update fails | Log warning, continue with summary |

---

## Reference Files

| Reference | Phase | Purpose |
|-----------|-------|---------|
| `references/gap-discovery-workflow.md` | 02 | Detailed gap file parsing algorithm |
| `references/gap-aggregation-algorithm.md` | 03 | Scoring, deduplication, and filtering |
| `references/gap-to-story-mapping.md` | 05 | Story context marker generation rules |
| `references/report-update-protocol.md` | 06 | Gap file update and report generation |
| `references/technical-debt-update.md` | 07 | Debt register entry format and update |

## Template Files

| Template | Phase | Purpose |
|----------|-------|---------|
| `assets/templates/enhancement-report-template.md` | 06 | Enhancement report markdown template |
| `assets/templates/import-metadata-template.yaml` | 02 | Import metadata schema |

---

## Related Components

| Component | Relationship |
|-----------|--------------|
| `/review-qa-reports` command | Invokes this skill |
| `spec-driven-stories` skill | Batch mode story creation (Phase 05) |
| `spec-driven-qa` skill | Produces gap files consumed by this skill |
| `technical-debt-analyzer` subagent | Optional debt analysis (Phase 07) |
| `devforgeai/config/qa-remediation.yaml` | Runtime configuration |
| `devforgeai/technical-debt-register.md` | Deferred gap tracking |
| `devforgeai/qa/reports/` | Local gap file source |
| `devforgeai/qa/imports/` | External project gap imports |
| `devforgeai/qa/enhancement-reports/` | Generated report output |

---

## Configuration

Runtime settings in `devforgeai/config/qa-remediation.yaml`:

| Setting | Default | Description |
|---------|---------|-------------|
| `sources.local` | `devforgeai/qa/reports/*-gaps.json` | Local gap file glob |
| `sources.imports` | `devforgeai/qa/imports/**/*-gaps.json` | Import gap file glob |
| `severity_weights.CRITICAL` | 100 | Scoring weight |
| `severity_weights.HIGH` | 75 | Scoring weight |
| `severity_weights.MEDIUM` | 50 | Scoring weight |
| `severity_weights.LOW` | 25 | Scoring weight |
| `defaults.min_severity` | MEDIUM | Default severity filter |
| `defaults.sprint` | Backlog | Default sprint for stories |
| `technical_debt.register_path` | `devforgeai/technical-debt-register.md` | Debt register location |
| `technical_debt.auto_add_skipped` | true | Auto-add deferred gaps |
| `technical_debt.invoke_analyzer` | false | Run debt analyzer subagent |
| `batch_mode.continue_on_failure` | true | Continue if story fails |
| `batch_mode.max_stories_per_run` | 20 | Safety limit |
