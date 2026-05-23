---
name: spec-driven-analytics
description: >
  Orchestrate session data mining operations through a 7-phase workflow with structural
  anti-skip enforcement. Analyzes Claude Code history.jsonl files and workflow artifacts
  to deliver formatted, actionable analytics for workflow patterns, errors, decisions,
  and command sequences. Prevents token optimization bias through per-phase reference
  loading, checkpoint persistence, Execute-Verify-Record enforcement, and artifact
  verification. Use when analyzing session data, extracting workflow patterns, investigating
  error trends, or reviewing development decisions. Always use this skill when the user
  runs /analytics or mentions session analytics, workflow patterns, error mining, decision
  archive, or command sequence analysis.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
  - Task
model: claude-opus-4-6
effort: High
---

# Spec-Driven Analytics

Orchestrate session data mining operations through the session-miner subagent to deliver formatted, actionable analytics from Claude Code session history, with 4-layer structural anti-skip enforcement.

**Context files are THE LAW:** tech-stack.md, source-tree.md, dependencies.md, coding-standards.md, architecture-constraints.md, anti-patterns.md

**If ambiguous or conflicts detected: HALT and use AskUserQuestion**

---

## Execution Model

This skill expands inline. After invocation, execute Phase 00 Initialization immediately. Do not wait passively, ask permission, or offer execution options.

**Self-Check (if ANY box is true = VIOLATION):**

- [ ] Stopping to ask about token budget
- [ ] Stopping to offer execution options
- [ ] Waiting passively for user to say "go"
- [ ] Asking "should I execute this?"
- [ ] Skipping a phase because it "seems simple"
- [ ] Combining multiple phases into one
- [ ] Summarizing instead of loading a reference file
- [ ] Skipping verification because "I already wrote the file"

**IF any box checked:** EXECUTION MODEL VIOLATION. Go directly to Phase 00 Initialization now.

---

## Anti-Skip Enforcement Contract

This skill enforces 4 independent anti-skip layers. ALL FOUR must fail for a step to be skipped:

1. **Per-phase reference loading** - Each phase loads its reference files fresh via `Read()`. NOT consolidated. Prevents "already covered" rationalization.
2. **Binary CLI gates** - `devforgeai-validate phase-check/phase-complete` at phase boundaries. Cannot be forged by LLM.
3. **Checkpoint-based state tracking** - Phase completion verified by checking checkpoint JSON data keys and `current_phase` field.
4. **Artifact verification** - Checkpoint JSON existence checked via `Glob()`, cache files verified on disk, output verified via `Grep()`.

**Execute-Verify-Record Pattern:** Every mandatory step in every phase file has three parts:
- **EXECUTE:** The exact action to perform (Read, Write, Task, Glob, Grep, AskUserQuestion)
- **VERIFY:** How to confirm the action happened (file exists, content contains expected text, data key populated)
- **RECORD:** Update checkpoint JSON with captured data; call `devforgeai-validate phase-record`

**Token Optimization Bias is PROHIBITED.** Do not skip, compress, or shortcut any step. Every phase step exists because a previous failure proved it necessary.

---

## Purpose

This skill serves as the **analytics orchestration layer** for DevForgeAI. It coordinates the session-miner subagent to extract patterns from Claude Code history.jsonl files and presents formatted, actionable analytics.

### Core Philosophy

**"Mine Once, Reference Forever"** - Extract session patterns into cached analytics that survive context window clears and are queryable across sessions.

**"Evidence-Based Optimization"** - All workflow recommendations are backed by empirical session data, not speculation.

**"Data Compounds Over Time"** - Analytics cache grows with each query, related patterns are cross-referenced, and staleness tracking ensures freshness.

---

## When to Use This Skill

### Trigger Scenarios

- Analyzing workflow patterns and execution frequencies
- Mining error patterns and failure points from session history
- Surfacing architectural and implementation decisions
- Deep analysis of a specific story's development history
- Identifying high-frequency command sequences for optimization
- User runs `/analytics` command
- User mentions session analytics, workflow patterns, or error mining

### When NOT to Use

- Capturing feedback (use spec-driven-feedback)
- Searching chat history (use /chat-search)
- Root cause analysis of specific failures (use spec-driven-rca)

---

## Parameter Extraction

Extract from command arguments:

| Argument | Variable | Description |
|----------|----------|-------------|
| First positional arg | `$QUERY_TYPE` | Query type: dashboard, workflows, errors, decisions, story, command-patterns |
| `STORY-NNN` | `$STORY_ID` | Story ID for story-specific queries |
| `--force` | `$FORCE_REFRESH` | Force cache refresh (bypass TTL) |
| `--days N` | `$DAYS_LIMIT` | Limit to last N days of data |
| `--resume ANALYTICS-NNN` | `$RESUME_ID` | Resume existing analytics session |
| `--help` | `$HELP_MODE` | Display help and exit |
| `"search string"` | `$QUERY_PARAM` | Search string for decisions query |

**Default:** If no arguments, `$QUERY_TYPE = "dashboard"`

---

## State Persistence

- **Checkpoint:** `devforgeai/workflows/${ANALYTICS_ID}-phase-state.json`
- **References:** `references/` (self-contained within this skill)
- **Templates:** `assets/templates/` (self-contained within this skill)
- **Cache Output:** `devforgeai/cache/analytics/`

---

## Phase 00: Initialization [INLINE - Bootstraps State]

This phase runs inline because it creates the state that all other phases depend on. It CANNOT be skipped.

### Step 0.1: Parse Arguments

Extract arguments from command invocation. Determine mode:

```
IF args contain "--help" or "-h":
  Read("src/claude/skills/spec-driven-analytics/references/analytics-help.md")
  Display help content
  EXIT skill

IF args contain "--resume ANALYTICS-NNN":
  mode = "resume"
  RESUME_ID = extract_id(args)
  GOTO Step 0.2 (Resume Detection)

# Parse query type
QUERY_TYPE = first_positional_arg OR "dashboard"
VALID_TYPES = ["dashboard", "workflows", "errors", "decisions", "story", "command-patterns"]

IF QUERY_TYPE not in VALID_TYPES:
  Display error: "Invalid query type: '{QUERY_TYPE}'"
  Display: "Valid types: dashboard, workflows, errors, decisions, story, command-patterns"
  HALT

# Parse optional parameters
STORY_ID = extract_story_id(args)  # Required if QUERY_TYPE == "story"
FORCE_REFRESH = "--force" in args
DAYS_LIMIT = extract_days(args)    # Default: null (all data)
QUERY_PARAM = extract_quoted_string(args)  # For decisions query

IF QUERY_TYPE == "story" AND STORY_ID is null:
  Display error: "Story query requires a STORY-ID parameter"
  Display: "Usage: /analytics story STORY-XXX"
  HALT
```

### Step 0.2: Resume Detection

```
IF mode == "resume":
  checkpoint_file = Glob(pattern=f"devforgeai/workflows/{RESUME_ID}-phase-state.json")
  IF checkpoint_file found:
    Read the checkpoint file
    Restore state from checkpoint
    Set CURRENT_PHASE from checkpoint.progress.current_phase
    GOTO Phase Orchestration Loop at CURRENT_PHASE
  ELSE:
    HALT -- "Analytics session {RESUME_ID} not found"

# Check for existing in-progress checkpoint (new mode)
existing_checkpoints = Glob(pattern="devforgeai/workflows/ANALYTICS-*-phase-state.json")
IF existing_checkpoints with status "in_progress":
  AskUserQuestion:
    Question: "Found existing analytics session in progress. Resume or start fresh?"
    Header: "Resume"
    Options:
      - label: "Resume session"
        description: "Continue from last checkpoint"
      - label: "Start fresh"
        description: "Begin new analytics session"
  IF "Resume": Restore state, GOTO Phase Orchestration Loop at CURRENT_PHASE
```

### Step 0.3: Generate Analytics ID

```
existing_files = Glob("devforgeai/workflows/ANALYTICS-*-phase-state.json")

# Extract date-based IDs (gap-aware)
today = current_date_YYYY_MM_DD
today_checkpoints = [f for f in existing_files if today in f]
next_seq = len(today_checkpoints) + 1

ANALYTICS_ID = f"ANALYTICS-{today}-{next_seq:03d}"
```

### Step 0.4: CLI Initialization

```bash
source .venv/bin/activate && devforgeai-validate phase-init ${ANALYTICS_ID} --workflow=analytics --project-root=. 2>&1
```

| Exit Code | Meaning | Action |
|-----------|---------|--------|
| 0 | New workflow | State file created. Set CURRENT_PHASE = "01". |
| 1 | Existing workflow | Resume. Run `devforgeai-validate phase-status ${ANALYTICS_ID} --workflow=analytics` to get CURRENT_PHASE. |
| 2 | Invalid ID | HALT. Must match ANALYTICS-YYYY-MM-DD-NNN pattern. |
| 127 | CLI not installed | Continue without CLI enforcement (backward compatibility). |

### Step 0.5: Create Initial Checkpoint

```json
{
  "checkpoint_version": "1.0",
  "analytics_id": "${ANALYTICS_ID}",
  "workflow": "analytics",
  "created_at": "ISO 8601",
  "updated_at": "ISO 8601",
  "status": "in_progress",
  "input": {
    "query_type": "${QUERY_TYPE}",
    "story_id": "${STORY_ID}",
    "force_refresh": false,
    "days_limit": null,
    "query_param": null
  },
  "progress": {
    "current_phase": 0,
    "phases_completed": [],
    "total_steps_completed": 0
  },
  "phases": {
    "01": { "status": "pending", "steps_completed": [] },
    "02": { "status": "pending", "steps_completed": [] },
    "03": { "status": "pending", "steps_completed": [] },
    "04": { "status": "pending", "steps_completed": [] },
    "05": { "status": "pending", "steps_completed": [] },
    "06": { "status": "pending", "steps_completed": [] }
  },
  "cache": {
    "cache_key": null,
    "cache_hit": false,
    "cache_path": null
  },
  "output": {
    "raw_entries": null,
    "aggregated_results": null,
    "formatted_output": null,
    "error": null
  }
}
```

Write to `devforgeai/workflows/${ANALYTICS_ID}-phase-state.json`

**VERIFY:** `Glob(pattern="devforgeai/workflows/${ANALYTICS_ID}-phase-state.json")`
IF not found: HALT -- "Initial checkpoint was NOT created."

### Step 0.6: Display Session Banner

```
Display:
"------------------------------------------------------------
  DevForgeAI Analytics Session
------------------------------------------------------------

Analytics ID: ${ANALYTICS_ID}
Query Type:   ${QUERY_TYPE}
Story ID:     ${STORY_ID || 'N/A'}
Force Refresh: ${FORCE_REFRESH}
Days Limit:   ${DAYS_LIMIT || 'All data'}

Phases: 7 (Initialization > Cache Management > Query Orchestration > Result Aggregation > Output Formatting > Display & Delivery > Completion)
------------------------------------------------------------"
```

### Step 0.7: Checkpoint Path Verification

```
Glob(pattern="devforgeai/workflows/${ANALYTICS_ID}-phase-state.json")
IF not found: HALT -- "Checkpoint file missing after Step 0.6"
```

Set CURRENT_PHASE = 1.

---

## Phase Orchestration Loop

```
phase_slugs = {
    1: "cache-management",
    2: "query-orchestration",
    3: "result-aggregation",
    4: "output-formatting",
    5: "display-delivery",
    6: "completion-summary"
}

FOR phase_num in range(CURRENT_PHASE, 7):  # Phases 01-06
    phase_id = f"{phase_num:02d}"
    slug = phase_slugs[phase_num]

    1. ENTRY GATE: devforgeai-validate phase-check ${ANALYTICS_ID} --workflow=analytics --from={prev_phase} --to={phase_id} --project-root=.
       IF exit != 0 AND exit != 127: HALT

    2. LOAD: Read(file_path=f"src/claude/skills/spec-driven-analytics/phases/phase-{phase_id}-{slug}.md")
       Load the phase file FRESH. Do NOT skip this step. Do NOT rely on memory of previous reads.

    3. REFERENCE: Read the phase's reference files as specified in the phase Contract section.
       References are in references/ (self-contained within this skill).
       Load ALL listed references. Do not skip any.

    4. EXECUTE: Follow EVERY step in the phase file using EXECUTE-VERIFY-RECORD triplets.

    5. EXIT GATE: devforgeai-validate phase-complete ${ANALYTICS_ID} --workflow=analytics --phase={phase_id} --checkpoint-passed --project-root=.
       IF exit != 0 AND exit != 127: HALT

    6. CHECKPOINT: Update checkpoint JSON with phase completion.
       Write updated checkpoint to disk.
       Verify write via Glob().

    # CACHE HIT SHORT-CIRCUIT: If Phase 01 sets CACHE_HIT=true, skip Phases 02-04 and jump to Phase 05.
    IF phase_num == 1 AND CACHE_HIT == true:
       Set CURRENT_PHASE = 5
       CONTINUE to Phase 05 (Display & Delivery)
```

---

## Phase Table

| Phase | Name | File | Steps | Required Subagents |
|-------|------|------|-------|--------------------|
| 00 | Initialization | (inline above) | 7 | none |
| 01 | Cache Management | `phases/phase-01-cache-management.md` | 5 | none |
| 02 | Query Orchestration | `phases/phase-02-query-orchestration.md` | 5 | session-miner (BLOCKING) |
| 03 | Result Aggregation | `phases/phase-03-result-aggregation.md` | 6 | none |
| 04 | Output Formatting | `phases/phase-04-output-formatting.md` | 5 | none |
| 05 | Display & Delivery | `phases/phase-05-display-delivery.md` | 3 | none |
| 06 | Completion Summary | `phases/phase-06-completion-summary.md` | 3 | none |

---

## Required Subagents Per Phase

| Phase | Subagent | Enforcement |
|-------|----------|-------------|
| 02 | session-miner | BLOCKING - Must invoke via Task() and use output. |

**All other phases:** No subagents required. Direct tool calls (Read, Write, Glob, Grep, AskUserQuestion).

**Deviation Protocol:** Any skip requires explicit user consent via AskUserQuestion.

---

## Workflow Completion Validation

```
completed_count = len(checkpoint.progress.phases_completed)
IF completed_count < 6:
    HALT "WORKFLOW INCOMPLETE - {completed_count}/6 phases completed"
IF completed_count == 6:
    Display "All 6 phases completed - Workflow validation passed"
    Update checkpoint status to "completed"
```

---

## Success Criteria

Complete analytics query processed with:
- [ ] Valid analytics ID (ANALYTICS-YYYY-MM-DD-NNN format)
- [ ] Cache checked (hit returns immediately, miss proceeds to mining)
- [ ] session-miner subagent invoked via Task() pattern (on cache miss)
- [ ] Results aggregated, filtered, and ranked
- [ ] Output formatted as markdown with tables
- [ ] Cache mechanism operational (1-hour TTL)
- [ ] All 6 query types supported (dashboard, workflows, errors, decisions, story, command-patterns)
- [ ] Checkpoint updated to "completed"

---

## Reference Files Inventory

Load these on-demand during workflow execution:

### Phase Files (6 files in `phases/`)

| Phase File | Primary Reference (in `references/`) | Additional References |
|------------|--------------------------------------|----------------------|
| `phase-01-cache-management.md` | `cache-management.md` | -- |
| `phase-02-query-orchestration.md` | `query-configuration.md` | `session-miner-delegation.md` |
| `phase-03-result-aggregation.md` | `aggregation-pipeline.md` | -- |
| `phase-04-output-formatting.md` | `output-templates.md` | -- |
| `phase-05-display-delivery.md` | (self-contained) | -- |
| `phase-06-completion-summary.md` | (self-contained) | -- |

### Reference Files (6 files in `references/`)
- **cache-management.md** - TTL logic, cache key generation, invalidation rules, force refresh behavior
- **query-configuration.md** - 6 query type configurations, prompt templates, parameter mapping
- **session-miner-delegation.md** - Subagent invocation contract, Task() template, response schema
- **aggregation-pipeline.md** - group_by, filter_by, calculate_metrics, rank_by_relevance
- **output-templates.md** - 6 query-specific markdown templates, table schemas
- **analytics-help.md** - Help text, usage examples, error handling

### Assets (1 template)
- **assets/templates/checkpoint-template.json** - Checkpoint schema template

**Total:** 6 phase files + 6 reference files + 1 template = 13 files + SKILL.md = 14 files

---

## Error Handling

### Subagent Errors

```
IF session-miner returns error:
    Log error details to checkpoint.output.error
    Return error template with troubleshooting steps
    Do NOT cache error responses
```

### Cache Errors

```
IF cache read fails:
    Proceed without cache (CACHE_HIT=false)
    Log warning in checkpoint
```

### Empty Results

```
IF no matching sessions found:
    Return "no results" template
    Suggest query modifications via AskUserQuestion
```

---

## Best Practices

1. **Use specific query types** - Dashboard for overview, targeted queries for deep dives
2. **Use --force sparingly** - Cache exists to save time; force-refresh when data may have changed
3. **Use --days for recent analysis** - Narrow time windows produce faster, more focused results
4. **Review recommendations** - Analytics recommendations are data-driven but require human judgment
5. **Link to stories/ADRs when relevant** - Bidirectional traceability strengthens the knowledge base

**See phase-specific reference files for detailed procedures.**
