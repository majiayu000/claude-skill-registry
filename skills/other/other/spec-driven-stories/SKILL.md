---
name: spec-driven-stories
description: >
  Create user stories with acceptance criteria, technical specifications, and UI
  specifications through an 8-phase workflow with structural anti-skip enforcement.
  Prevents token optimization bias through per-phase reference loading, checkpoint
  persistence, Execute-Verify-Record enforcement, and artifact verification. Use when
  transforming feature descriptions into structured stories, generating stories from
  epic features, or creating follow-up stories for deferred work. Supports CRUD,
  authentication, workflow, and reporting story types with complete technical and UI
  specifications.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Task
  - AskUserQuestion
  - Skill
model: claude-opus-4-6
effort: High
---

# Spec-Driven Stories

Create comprehensive, implementation-ready user stories through an 8-phase workflow with structural anti-skip enforcement.

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
4. **Artifact verification** - Checkpoint JSON existence checked via `Glob()`, story files verified on disk, epic/sprint entries verified via `Grep()`.

**Execute-Verify-Record Pattern:** Every mandatory step in every phase file has three parts:
- **EXECUTE:** The exact action to perform (Read, Write, AskUserQuestion, Task, Grep, Glob)
- **VERIFY:** How to confirm the action happened (file exists, content contains expected text, data key populated)
- **RECORD:** Update checkpoint JSON with captured data; call `devforgeai-validate phase-record`

**Token Optimization Bias is PROHIBITED.** Do not skip, compress, or shortcut any step. Every phase step exists because a previous failure proved it necessary.

---

## Story Template Versions

**Current Version:** 2.8 (as of 2026-02-04)

| Version | Date | Change | Reference |
|---------|------|--------|-----------|
| v2.8 | 2026-02-04 | Advisory story fields (`advisory`, `source_gap`, `source_story`) | STORY-348, EPIC-054 |
| v2.1 | 2025-01-21 | AC header format: `### 1. [ ]` to `### AC#1:` | RCA-012 |
| v2.0 | 2025-10-30 | Structured YAML `technical_specification` block | RCA-006 |
| v1.0 | Initial | Original template (legacy, still supported) | -- |

**Format Specification:** `devforgeai/specs/STRUCTURED-FORMAT-SPECIFICATION.md` (loaded in Phase 03)

**Migration Script (v2.0 to v2.1):** `scripts/migrate-ac-headers.sh`

**Backward Compatibility:** All versions (v1.0, v2.0, v2.1, v2.8) supported. Migration is optional.

**Template Location:** `assets/templates/story-template.md` (loaded in Phase 05)

---

## When to Use This Skill

### Trigger Scenarios

- User runs `/create-story [feature-description]` command
- `/create-stories-from-rca` decomposes RCA recommendations into stories
- devforgeai-orchestration decomposes epic features into stories
- spec-driven-dev creates tracking stories for deferred DoD items
- Sprint planning requires story generation
- Manual invocation: `Skill(command="spec-driven-stories")`

### When NOT to Use

- Epic creation (use devforgeai-orchestration epic mode instead)
- Sprint planning (use devforgeai-orchestration sprint mode instead)
- Story already exists (use Edit tool to modify existing story)

---

## Batch Mode Support

**Batch mode triggered when:**
- Context marker `**Batch Mode:** true` present in conversation

**Batch mode behavior:**
- **Phase 01 modified:** Skip interactive questions, extract metadata from context markers
- **Phases 02-07:** Execute normally (requirements, tech spec, UI spec, file creation, linking, validation)
- **Phase 08 modified:** Skip next action AskUserQuestion, return immediately to batch loop

**Required context markers for batch mode:**
```
**Story ID:** STORY-009
**Epic ID:** EPIC-001
**Feature Number:** 1.1
**Feature Name:** User Registration Form
**Feature Description:** Implement user registration form with email validation...
**Priority:** High
**Points:** 5
**Type:** feature
**Sprint:** Sprint-1
**Batch Mode:** true
**Batch Index:** 0
```

**When batch mode detected:**
1. Extract all metadata from conversation context
2. Validate all required markers present (Story ID, Epic ID, Feature Description, Priority, Points, Type, Sprint)
3. Skip Phase 01 interactive questions (epic/sprint/priority/points/type selection)
4. Use provided values instead of asking user
5. Execute Phases 02-07 normally (full story generation)
6. Skip Phase 08 next action question (batch loop handles this)
7. Return control to command for next feature in batch

**Fallback:** If required markers missing, switch to interactive mode and ask questions

**See `references/story-discovery.md` for batch mode detection and metadata extraction logic.** (loaded in Phase 01)

---

## Parameter Extraction

Extract from conversation context markers set by invoking command:

| Context Marker | Set By | Description |
|----------------|--------|-------------|
| `$MODE` | `/create-story` | SINGLE_STORY or EPIC_BATCH |
| `$EPIC_ID` | `/create-story` | EPIC-NNN identifier |
| `$FEATURE_DESCRIPTION` | `/create-story` | Feature description text |
| `$STORY_ID` | batch mode | STORY-NNN identifier |
| `$FEATURE_NUMBER` | batch mode | Feature number (e.g., 1.1) |
| `$FEATURE_NAME` | batch mode | Feature name |
| `$PRIORITY` | batch mode | High/Medium/Low |
| `$POINTS` | batch mode | Story points |
| `$TYPE` | batch mode | feature/bug/refactor/documentation |
| `$SPRINT` | batch mode | Sprint-N identifier |
| `$BATCH_MODE` | batch mode | true/false |
| `$BATCH_INDEX` | batch mode | 0-based index |

---

## Command Integration

These commands delegate to this skill. When invoked via a command, context markers are already set.

| Command | Purpose | Markers Set |
|---------|---------|-------------|
| `/create-story` | Create single story or batch from epic | Mode, Epic ID or Feature Description |
| `/create-stories-from-rca` | Create stories from RCA recommendations | Mode, Story metadata from RCA |

---

## State Persistence

- **Checkpoint:** `devforgeai/workflows/checkpoints/${SESSION_ID}.checkpoint.json`
- **References:** `references/` (self-contained within this skill)
- **Contracts:** `contracts/` (self-contained within this skill)
- **Templates:** `assets/templates/` (self-contained within this skill)
- **Scripts:** `scripts/` (self-contained within this skill)

---

## Phase 00: Initialization [INLINE - Bootstraps State]

This phase runs inline because it creates the state that all other phases depend on. It CANNOT be skipped.

### Step 0.1: Parse Arguments

Extract all context markers from the Parameter Extraction table above. Defaults: `$MODE` = "SINGLE_STORY", `$TYPE` = "feature", `$BATCH_MODE` = false. All other markers default to null if not present.

### Step 0.2: Resume Detection

```
Glob(pattern="devforgeai/workflows/checkpoints/SC-*.checkpoint.json")

IF matching checkpoint found with status "in_progress":
  Read the checkpoint file
  AskUserQuestion:
    Question: "Found existing story creation session. Resume or start fresh?"
    Header: "Resume"
    Options:
      - label: "Resume session"
        description: "Continue from last checkpoint"
      - label: "Start fresh"
        description: "Begin new story creation session"
  IF "Resume": Restore state, GOTO Phase Orchestration Loop at CURRENT_PHASE
ELSE:
  Continue to Step 0.3
```

### Step 0.3: Generate Session ID

```
# Scan for highest existing SC-YYYY-MM-DD-### in checkpoints directory (gap-aware)
checkpoint_files = Glob(pattern="devforgeai/workflows/checkpoints/SC-*.checkpoint.json")

IF checkpoint_files found:
  Extract highest ### for today's date
  SESSION_ID = "SC-{YYYY-MM-DD}-{###+1}" (zero-padded to 3 digits)
ELSE:
  SESSION_ID = "SC-{YYYY-MM-DD}-001"
```

### Step 0.4: CLI Initialization

```bash
source .venv/bin/activate && devforgeai-validate phase-init ${SESSION_ID} --workflow=stories --project-root=. 2>&1
```

| Exit Code | Meaning | Action |
|-----------|---------|--------|
| 0 | New workflow | State file created. Set CURRENT_PHASE = "01". |
| 1 | Existing workflow | Resume. Run `devforgeai-validate phase-status ${SESSION_ID} --workflow=stories` to get CURRENT_PHASE. |
| 2 | Invalid session ID | HALT. Must match SC-YYYY-MM-DD-NNN pattern. |
| 127 | CLI not installed | Continue without CLI enforcement (backward compatibility). |

### Step 0.5: Create Initial Checkpoint

```json
{
  "checkpoint_version": "1.0",
  "session_id": "SC-YYYY-MM-DD-NNN",
  "workflow": "stories",
  "created_at": "ISO 8601",
  "updated_at": "ISO 8601",
  "status": "in_progress",
  "input": {
    "mode": "$MODE",
    "epic_id": "$EPIC_ID or null",
    "feature_description": "$FEATURE_DESCRIPTION or null",
    "story_id": "null (generated in Phase 01)",
    "batch_mode": "$BATCH_MODE or false",
    "batch_index": "$BATCH_INDEX or null"
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
    "06": { "status": "pending", "steps_completed": [] },
    "07": { "status": "pending", "steps_completed": [] },
    "08": { "status": "pending", "steps_completed": [] }
  },
  "output": {
    "story_id": null,
    "story_file_path": null,
    "epic_linked": false,
    "sprint_linked": false,
    "validation_passed": false,
    "error": null
  }
}
```

Write to `devforgeai/workflows/checkpoints/${SESSION_ID}.checkpoint.json`

**VERIFY:** `Glob(pattern="devforgeai/workflows/checkpoints/${SESSION_ID}.checkpoint.json")`
IF not found: HALT -- "Initial checkpoint was NOT created."

### Step 0.6: Display Session Banner

```
Display:
"------------------------------------------------------------
  DevForgeAI Story Creation Session
------------------------------------------------------------

Session: ${SESSION_ID}
Mode: ${MODE}
Epic: ${EPIC_ID || 'None'}
Feature: ${FEATURE_DESCRIPTION || 'None provided'}
Batch: ${BATCH_MODE || false}

Phases: 8 (Discovery > Requirements > Tech Spec > UI Spec > File Creation > Linking > Validation > Completion)
------------------------------------------------------------"
```

Set CURRENT_PHASE = 1.

---

## Phase Orchestration Loop

```
FOR phase_num in range(CURRENT_PHASE, 9):  # Phases 01-08

    1. ENTRY GATE: devforgeai-validate phase-check ${SESSION_ID} --workflow=stories --from={prev} --to={phase_id} --project-root=.
       IF exit != 0 AND exit != 127: HALT

    2. LOAD: Read(file_path="src/claude/skills/spec-driven-stories/phases/{phase_files[phase_num]}")
       Load the phase file FRESH. Do NOT skip this step. Do NOT rely on memory of previous reads.

    3. REFERENCE: Read the phase's reference files as specified in the phase Contract section.
       References are in references/ (self-contained within this skill).
       Load ALL listed references. Do not skip any.

    4. EXECUTE: Follow EVERY step in the phase file using EXECUTE-VERIFY-RECORD triplets.

    5. EXIT GATE: devforgeai-validate phase-complete ${SESSION_ID} --workflow=stories --phase={phase_id} --checkpoint-passed --project-root=.
       IF exit != 0 AND exit != 127: HALT

    6. CHECKPOINT: Update checkpoint JSON with phase completion.
       Write updated checkpoint to disk.
       Verify write via Glob().
```

---

## Phase Table

| Phase | Name | File | Steps | Required Subagents |
|-------|------|------|-------|--------------------|
| 00 | Initialization | (inline above) | 6 | none |
| 01 | Story Discovery & Context | `phases/phase-01-story-discovery.md` | 6 | none |
| 02 | Requirements Analysis | `phases/phase-02-requirements-analysis.md` | 4 | story-requirements-analyst (BLOCKING) |
| 03 | Technical Specification | `phases/phase-03-technical-specification.md` | 5 | api-designer (CONDITIONAL) |
| 04 | UI Specification | `phases/phase-04-ui-specification.md` | 3 | none |
| 05 | Story File Creation | `phases/phase-05-story-file-creation.md` | 5 | none |
| 06 | Epic/Sprint Linking | `phases/phase-06-epic-sprint-linking.md` | 3 | none |
| 07 | Self-Validation | `phases/phase-07-self-validation.md` | 4 | none |
| 08 | Completion Report | `phases/phase-08-completion-report.md` | 3 | none |

---

## Required Subagents Per Phase

| Phase | Subagent | Enforcement |
|-------|----------|-------------|
| 02 | story-requirements-analyst | BLOCKING - Must invoke and use output |
| 03 | api-designer | CONDITIONAL - Only if API endpoints detected |

**All other phases:** No subagents required. Direct tool calls (Read, Write, Glob, Grep, AskUserQuestion).

---

## Subagent Coordination

This skill delegates specialized tasks to subagents:

- **story-requirements-analyst** (Phase 02) - Generates user story and acceptance criteria from feature description. BLOCKING: Phase 02 cannot complete without subagent output. The subagent produces the user story (As a/I want/So that), 3+ acceptance criteria (Given/When/Then), edge cases, and non-functional requirements.
- **api-designer** (Phase 03, conditional) - Designs API contracts when endpoints are detected in the requirements. CONDITIONAL: Only invoked when Phase 02 output contains API-related acceptance criteria or when the feature description implies REST/GraphQL endpoints.

**Subagent contracts (loaded per-phase, not upfront):**
- `contracts/requirements-analyst-contract.yaml` (loaded in Phase 02)
- `contracts/api-designer-contract.yaml` (loaded in Phase 03, conditional)

---

## Integration Points

**Invoked by:**
- `/create-story` command (user-initiated)
- `/create-stories-from-rca` command (RCA recommendation decomposition)
- devforgeai-orchestration skill (epic/sprint decomposition)
- spec-driven-dev skill (deferred work tracking)

**Provides output to:**
- spec-driven-ui (AC to UI requirements)
- spec-driven-dev (AC to test generation)
- spec-driven-qa (AC to validation targets)

**See `references/integration-guide.md` for complete integration patterns.** (loaded on-demand, not upfront)

---

## Workflow Completion Validation

```
completed_count = len(checkpoint.progress.phases_completed)
IF completed_count < 8:
    HALT "WORKFLOW INCOMPLETE - {completed_count}/8 phases completed"
IF completed_count == 8:
    Display "All 8 phases completed - Workflow validation passed"
    Update checkpoint status to "completed"
```

---

## Success Criteria

Complete story generated with:
- [ ] Valid story ID (STORY-NNN format)
- [ ] User story (As a/I want/So that)
- [ ] 3+ acceptance criteria (Given/When/Then)
- [ ] Technical specification (complete)
- [ ] UI specification (if applicable)
- [ ] Non-functional requirements (measurable)
- [ ] Edge cases documented
- [ ] Definition of Done (checkboxes)
- [ ] File written to devforgeai/specs/Stories/
- [ ] Epic/sprint updated (if applicable)
- [ ] Self-validation passed
- [ ] Token usage <90K (isolated context)

---

## Reference Files Inventory

Load these on-demand during workflow execution:

### Phase Files (8 files in `phases/`)

| Phase File | Primary Reference (in `references/`) | Additional References |
|------------|--------------------------------------|----------------------|
| `phase-01-story-discovery.md` | `story-discovery.md` | `user-input-integration-guide.md`, `story-type-classification.md` |
| `phase-02-requirements-analysis.md` | `requirements-analysis.md` | `acceptance-criteria-patterns.md` |
| `phase-03-technical-specification.md` | `technical-specification-creation.md` | `technical-specification-guide.md` |
| `phase-04-ui-specification.md` | `ui-specification-creation.md` | `ui-specification-guide.md` |
| `phase-05-story-file-creation.md` | `story-file-creation.md` | `story-structure-guide.md`, `story-examples.md` |
| `phase-06-epic-sprint-linking.md` | `epic-sprint-linking.md` | -- |
| `phase-07-self-validation.md` | `story-validation-workflow.md` | `validation-checklists.md`, `context-validation.md` |
| `phase-08-completion-report.md` | `completion-report.md` | -- |

### Supporting Guides (8 files in `references/`)
- **acceptance-criteria-patterns.md** - Given/When/Then templates by domain
- **story-examples.md** - 4 complete story examples (CRUD, auth, workflow, reporting)
- **story-structure-guide.md** - YAML frontmatter, section formatting rules
- **technical-specification-guide.md** - API contract patterns, data modeling
- **ui-specification-guide.md** - Component design, ASCII mockups, accessibility
- **validation-checklists.md** - Quality validation procedures
- **user-input-integration-guide.md** - User input guidance integration
- **story-type-classification.md** - Story type enum, phase skip matrix

### Workflow & Error References (4 files in `references/`)
- **error-handling.md** - Error recovery procedures across all phases
- **integration-guide.md** - Skill integration patterns and downstream consumers
- **batch-mode-configuration.md** - Batch processing detection and metadata
- **custody-chain-workflow.md** - Provenance chain tracking

### Additional References (4 files in `references/`)
- **context-validation.md** - Context file constraint validation
- **gap-to-story-conversion.md** - Gap ID to story conversion logic
- **parameter-extraction.md** - Context marker parsing and validation
- **checkpoint-schema.md** - Checkpoint JSON schema and update protocol

### Contracts (2 YAML files)
- **contracts/requirements-analyst-contract.yaml** - story-requirements-analyst interface
- **contracts/api-designer-contract.yaml** - api-designer interface

### Assets (1 template)
- **assets/templates/story-template.md** - Base story template (YAML + markdown)

**Total:** 8 phase files + 24 reference files + 2 contracts + 1 template = 35 files

---

## Best Practices

**Top 5 practices for story creation:**

1. **Provide clear feature description** - Minimum 10 words, specific WHO/WHAT
2. **Associate with epic when possible** - Enables traceability and feature tracking
3. **Ensure AC are testable** - All criteria must be verifiable (Given/When/Then)
4. **Include UI specs for frontend work** - Mockups prevent implementation ambiguity
5. **Trust self-validation** - Phase 07 auto-corrects common issues, high quality output

**See phase-specific reference files for detailed best practices.**
