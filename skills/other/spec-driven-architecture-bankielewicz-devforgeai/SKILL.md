---
name: spec-driven-architecture
description: >
  Creates immutable context files and architecture documentation through spec-driven
  workflow with structural anti-skip enforcement. Replicates all 11 phases of the
  DevForgeAI architecture workflow using the Execute-Verify-Gate pattern at every step.
  Designed to prevent token optimization bias through lean orchestration, fresh-context
  subagent delegation, and artifact verification. Use when creating context files,
  making technology decisions, establishing project structure, or creating epics.
  Always use this skill when the user runs /create-context or /create-epic.
  Do NOT use when user wants spec-driven development (use spec-driven-dev)
  or QA validation (use spec-driven-qa).
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
  - Task
  - Bash(git:*)
  - Bash(devforgeai-validate:*)
  - WebFetch
  - Skill
model: claude-opus-4-6
effort: High
---

# Spec-Driven Architecture

Create immutable context files and architecture documentation that prevents technical debt through explicit constraints that all DevForgeAI agents must enforce.

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

**IF any box checked:** EXECUTION MODEL VIOLATION. Go directly to Phase 00 Initialization now.

---

## Anti-Skip Enforcement Contract

This skill enforces 3 independent anti-skip layers. ALL THREE must fail for a step to be skipped:

1. **Per-phase fresh reference loading** - Each phase loads its reference file fresh via `Read()`. NOT consolidated. Prevents "already covered" rationalization.
2. **Checkpoint-based state tracking** - Phase completion verified by checking checkpoint JSON data keys and `current_phase` field.
3. **Artifact verification** - Checkpoint JSON existence checked via `Glob()`, output files verified on disk after every Write.

**Note:** Binary CLI gate enforcement (Layer 4) deferred to future story — requires extending `STORY_ID_PATTERN` in phase_state.py to accept `ARCH-` prefix.

**Execute-Verify-Record Pattern:** Every mandatory step in every phase file has three parts:
- **EXECUTE:** The exact action to perform (Read, Write, AskUserQuestion, Task, Glob, Grep)
- **VERIFY:** How to confirm the action happened (file exists, data key populated, user response non-empty)
- **RECORD:** Update checkpoint JSON with captured data; verify write via Glob

**Token Optimization Bias is PROHIBITED.** Do not skip, compress, or shortcut any step. Every phase step exists because a previous failure proved it necessary.

---

## Parameter Extraction

Extract from conversation context:

| Parameter | Source | Default |
|-----------|--------|---------|
| `$PROJECT_NAME` | `/create-context` argument or directory name | Current directory name |
| `$COMMAND_MODE` | `/create-context` → "context-creation", `/create-epic` → "epic-creation" | "context-creation" |
| `$EPIC_NAME` | `/create-epic` argument | null |
| `$OVERWRITE_MODE` | Set by `/create-context` pre-flight (overwrite/merge/null) | null |

---

## Command Integration

| Context Marker | Set By | Description |
|----------------|--------|-------------|
| `$PROJECT_NAME` | /create-context | Project identifier |
| `$COMMAND_MODE` | /create-context, /create-epic | "context-creation" or "epic-creation" |
| `$EPIC_NAME` | /create-epic | Epic name (10-100 chars) |
| `$OVERWRITE_MODE` | /create-context | "overwrite", "merge", or null |

---

## Phase 00: Initialization [INLINE — Bootstraps State]

This phase runs inline because it creates the state that all other phases depend on.

### Step 0.1: Parse Arguments

```
IF conversation contains "<epic-name>":
  COMMAND_MODE = "epic-creation"
  EPIC_NAME = extracted value
ELSE:
  COMMAND_MODE = "context-creation"
  EPIC_NAME = null

IF conversation contains project name after /create-context:
  PROJECT_NAME = extracted value
ELSE:
  PROJECT_NAME = current directory name (from CWD)

IF conversation contains overwrite/merge decision:
  OVERWRITE_MODE = extracted value
ELSE:
  OVERWRITE_MODE = null
```

### Step 0.2: Generate Architecture ID

```
ARCH_ID = "ARCH-" + current timestamp (YYYYMMDD-HHMMSS)
Example: ARCH-20260316-143000
```

### Step 0.3: Create Checkpoint File

```
checkpoint = {
  "checkpoint_version": "1.0",
  "arch_id": ARCH_ID,
  "project_name": PROJECT_NAME,
  "command_mode": COMMAND_MODE,
  "created_at": ISO 8601 timestamp,
  "progress": {
    "current_phase": 1,
    "phases_completed": [],
    "phases_skipped": [],
    "total_phases": 11
  },
  "phases": {
    "01": {"status": "pending"},
    "02": {"status": "pending", "files_created": [], "files_verified": false},
    "03": {"status": "pending", "adrs_created": []},
    "04": {"status": "pending"},
    "05": {"status": "pending"},
    "06": {"status": "pending"},
    "07": {"status": "pending"},
    "08": {"status": "pending"},
    "09": {"status": "pending"},
    "10": {"status": "pending"},
    "11": {"status": "pending"}
  },
  "context_markers": {
    "overwrite_mode": OVERWRITE_MODE,
    "epic_name": EPIC_NAME
  }
}

Write(file_path="devforgeai/workflows/${ARCH_ID}-arch-checkpoint.json", content=JSON.stringify(checkpoint))
```

**VERIFY:** `Glob(pattern="devforgeai/workflows/${ARCH_ID}-arch-checkpoint.json")` returns exactly 1 file.

### Step 0.4: Display Initialization

```
Display:
  "Architecture Workflow Initialized"
  "ID: ${ARCH_ID}"
  "Mode: ${COMMAND_MODE}"
  "Project: ${PROJECT_NAME}"
  "Phases: 11 (3 conditional)"
```

**GOTO Phase Orchestration Loop at Phase 01.**

---

## Phase Orchestration Loop

For each phase from CURRENT_PHASE to 11:

1. **LOAD PHASE:** `Read(file_path=".claude/skills/spec-driven-architecture/phases/{phase_file}")` — Read the phase file FRESH. Do NOT skip this step.

2. **LOAD REFERENCES:** Each phase file specifies which references to load from `.claude/skills/spec-driven-architecture/`. Load them ALL via Read(). Do NOT skip or summarize.

3. **EXECUTE STEPS:** Follow EVERY step's EXECUTE-VERIFY-RECORD triplet in the phase file. Execute them IN ORDER. Do NOT compress or skip steps.

4. **EXIT CRITERIA:** Verify ALL mandatory exit conditions listed in the phase file before proceeding.

5. **UPDATE CHECKPOINT:** Update `phases[phase_id].status = "completed"`, add to `phases_completed`, advance `current_phase`.

6. **VERIFY CHECKPOINT:** `Read(file_path="devforgeai/workflows/${ARCH_ID}-arch-checkpoint.json")` — Confirm the update persisted.

7. **DISPLAY TRANSITION:** Show phase completion and next phase name.

---

## Phase Table

| Phase | Name | File | Conditional | Subagents |
|-------|------|------|-------------|-----------|
| 01 | Context Discovery | `phases/phase-01-context-discovery.md` | No | — |
| 02 | Context File Creation | `phases/phase-02-context-creation.md` | No | internet-sleuth (conditional) |
| 03 | ADR Creation | `phases/phase-03-adr-creation.md` | No | — |
| 04 | Technical Specifications | `phases/phase-04-tech-specs.md` | **Yes** (skip if scope too small) | — |
| 05 | Spec Validation | `phases/phase-05-spec-validation.md` | No | **context-validator** |
| 06 | Prompt Alignment | `phases/phase-06-prompt-alignment.md` | No | **alignment-auditor** |
| 07 | Domain Reference Generation | `phases/phase-07-domain-references.md` | No | — |
| 08 | Architecture Review | `phases/phase-08-architecture-review.md` | No | **architect-reviewer** |
| 09 | Design System Generation | `phases/phase-09-design-system.md` | **Yes** (UI projects only) | — |
| 10 | Post-Creation Validation | `phases/phase-10-validation-report.md` | No | — |
| 11 | Epic Creation | `phases/phase-11-epic-creation.md` | **Yes** (/create-epic only) | **requirements-analyst**, **architect-reviewer** |

**Conditional Phase Handling:**
- Phase 04: Ask user via AskUserQuestion. If skip → mark `phases_skipped`, advance.
- Phase 09: Auto-detect from tech-stack.md. If no UI framework → mark `phases_skipped`, advance.
- Phase 11: Check `$COMMAND_MODE`. If "context-creation" → mark `phases_skipped`, advance.

---

## State Persistence

- **Checkpoint:** `devforgeai/workflows/${ARCH_ID}-arch-checkpoint.json`
- **Updated:** After every phase completion
- **Verified:** Via `Glob()` after every write
- **Resume:** Read checkpoint, set `CURRENT_PHASE` from `progress.current_phase`, resume loop

---

## Workflow Completion Validation

```
required_phases = phases_completed + phases_skipped
IF len(required_phases) < 11:
    HALT "WORKFLOW INCOMPLETE — ${len(required_phases)}/11 phases accounted for"
    Display missing phases

IF COMMAND_MODE == "context-creation":
    Verify: Glob("devforgeai/specs/context/*.md") returns >= 6 files
    Verify: Glob("devforgeai/specs/adrs/ADR-*.md") returns >= 1 file

IF COMMAND_MODE == "epic-creation":
    Verify: Glob("devforgeai/specs/Epics/EPIC-*.epic.md") returns new epic file
```

---

## Success Criteria

- All 6 required context files exist in `devforgeai/specs/context/`
- Optional design-system.md created if UI project detected
- Context files non-empty (no TODO/TBD/[FILL IN] placeholders)
- At least 1 ADR created (initial architecture decision)
- All ambiguities resolved via AskUserQuestion
- Architecture review passed (Phase 08)
- Post-creation validation passed (Phase 10)
- Ready for story planning via `/create-epic`, `/create-sprint`, `/dev`

---

## Deviation Protocol

If you need to deviate from ANY phase step:
1. HALT immediately
2. Use AskUserQuestion to explain the deviation and get user consent
3. Only proceed with explicit user approval
4. Record the deviation in the checkpoint under `deviations` key

**Without user consent, no deviation is permitted.**
