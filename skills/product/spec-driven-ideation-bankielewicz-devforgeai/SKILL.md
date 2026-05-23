---
name: spec-driven-ideation
description: >
  Transform business ideas into structured requirements through guided discovery
  with structural anti-skip enforcement (Execute-Verify-Gate pattern). Applies
  per-phase reference loading, checkpoint persistence, and artifact verification
  to every step of the 7-phase ideation process. Prevents token optimization bias
  through lean orchestration. Use when users say "I have a business idea",
  "help me define requirements", "let's explore what to build", or runs /ideate.
  Do NOT use when user wants to brainstorm a vague problem (use spec-driven-brainstorming)
  or wants a business plan directly (use planning-business).
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
  - Task
  - Skill
model: claude-opus-4-6
effort: High
version: "1.0.0"
topics: requirements, ideation, discovery, spec-driven, anti-skip, elicitation
---

# Spec-Driven Ideation

Transform business ideas into structured, actionable requirements through guided interactive questioning with structural anti-skip enforcement.

**Output:** `devforgeai/specs/requirements/{project-name}-requirements.md` (YAML per F4 schema)
**Feeds Into:** `/create-epic` command for epic generation, `/create-context` for architecture

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

This skill enforces 4 independent anti-skip layers. ALL FOUR must fail for a step to be skipped:

1. **Per-phase reference loading** - Each phase loads its reference file fresh via `Read()`. NOT consolidated. Prevents "already covered" rationalization.
2. **Checkpoint-based state tracking** - Phase completion verified by checking checkpoint JSON data keys and `current_phase` field.
3. **Artifact verification** - Checkpoint JSON existence checked via `Glob()`, output document verified on disk.
4. **Step registry with question completion** - Each phase has minimum question counts and required data keys. Phase exit criteria checked before proceeding.

**Execute-Verify-Record Pattern:** Every mandatory step in every phase file has three parts:
- **EXECUTE:** The exact AskUserQuestion call, Task call, or Write call to perform
- **VERIFY:** How to confirm the action happened (user response non-empty, file exists, data key populated)
- **RECORD:** Update checkpoint JSON with captured data; increment question counter

**Token Optimization Bias is PROHIBITED.** Do not skip, compress, or shortcut any step. Every phase step exists because a previous failure proved it necessary.

---

## Parameter Extraction

Extract from conversation context:

| Parameter | Source | Default |
|-----------|--------|---------|
| `$BUSINESS_IDEA` | Text from `/ideate` command or `<business-idea>` XML | null (will ask in Phase 02) |
| `$BRAINSTORM_FILE` | `<brainstorm-file>` XML element from /ideate | null (no brainstorm input) |
| `$PROJECT_MODE` | `<project-mode>` XML element from /ideate | "auto-detect" |
| `$RESUME_ID` | `--resume IDEATION-NNN` argument | null (new session) |
| `$MODE` | Derived from above | "new" or "resume" |

---

## Phase 00: Initialization [INLINE - Bootstraps State]

This phase runs inline because it creates the state that all other phases depend on.

### Step 0.1: Parse Arguments

```
IF conversation contains "--resume IDEATION-":
  Extract IDEATION_ID from argument
  MODE = "resume"
ELSE IF conversation contains "<ideation-context>":
  Extract BUSINESS_IDEA from <business-idea> element
  Extract BRAINSTORM_FILE from <brainstorm-file> element
  Extract PROJECT_MODE from <project-mode> element
  MODE = "new"
ELSE IF conversation contains business idea text after /ideate:
  BUSINESS_IDEA = extracted text
  MODE = "new"
ELSE:
  MODE = "new"
  BUSINESS_IDEA = null
```

### Step 0.2: Handle Resume Mode

```
IF MODE == "resume":
  checkpoint_results = Glob(pattern="devforgeai/specs/ideation/${IDEATION_ID}.checkpoint.json")

  IF found:
    Read(file_path="devforgeai/specs/ideation/${IDEATION_ID}.checkpoint.json")
    Restore session state from checkpoint
    CURRENT_PHASE = checkpoint.progress.current_phase
    Display: "Resuming ${IDEATION_ID} from Phase ${CURRENT_PHASE}"
    GOTO Phase Orchestration Loop at CURRENT_PHASE
  ELSE:
    Display: "No checkpoint found for ${IDEATION_ID}."
    AskUserQuestion:
      Question: "No checkpoint found. What would you like to do?"
      Header: "Resume"
      Options:
        - label: "Start a new ideation session"
          description: "Begin fresh session"
        - label: "Check for completed requirements"
          description: "Look for existing requirements files"
    IF "Start new": MODE = "new", continue below
    IF "Check completed": Glob for existing requirements files, display results
```

### Step 0.3: Brainstorm Context Detection

```
IF BRAINSTORM_FILE is not null and BRAINSTORM_FILE != "none":
  # Validate brainstorm file exists
  brainstorm_exists = Glob(pattern=BRAINSTORM_FILE)
  IF found:
    Read(file_path=BRAINSTORM_FILE)

    # Schema validation
    Read(file_path=".claude/skills/devforgeai-orchestration/references/skill-output-schemas.yaml")
    validation_result = validate_brainstorm_schema(brainstorm_content)

    IF validation_result == "FAILED":
      HALT: "Brainstorm schema validation failed."
    IF validation_result == "WARN":
      Display: "Brainstorm validation passed with warnings (legacy document)"
    IF validation_result == "PASSED":
      Display: "Brainstorm validation passed"

    # Pre-populate session from brainstorm
    session.brainstorm_input = {
      brainstorm_id: extract brainstorm ID from file,
      confidence_level: extract confidence from file,
      pre_populated_fields: [problem_statement, user_personas, constraints, must_haves]
    }
    session.problem_statement = brainstorm.problem_statement
    session.user_personas = brainstorm.user_personas
    session.constraints = brainstorm.hard_constraints
    session.must_have_requirements = brainstorm.must_have_capabilities
  ELSE:
    Display: "Brainstorm file not found. Starting fresh."
    BRAINSTORM_FILE = null
```

### Step 0.4: Generate Session ID (New Session)

```
IF MODE == "new":
  # Scan for highest existing ID
  Glob(pattern="devforgeai/specs/ideation/IDEATION-*.checkpoint.json")
  Glob(pattern="devforgeai/specs/requirements/*-requirements.md")

  # Extract highest NNN, increment
  IDEATION_ID = "IDEATION-{NNN+1}" (zero-padded to 3 digits minimum)

  # Ensure output directories exist
  Glob(pattern="devforgeai/specs/ideation/.gitkeep")
  IF not found: Write(file_path="devforgeai/specs/ideation/.gitkeep", content="")
```

### Step 0.5: Create Initial Checkpoint

```
checkpoint = {
  "checkpoint_version": "2.0",
  "session_id": IDEATION_ID,
  "created_at": "current ISO 8601 timestamp",
  "updated_at": "current ISO 8601 timestamp",
  "status": "in_progress",
  "business_idea": BUSINESS_IDEA,
  "project_mode": PROJECT_MODE or "auto-detect",
  "brainstorm_input": {
    "brainstorm_id": session.brainstorm_input.brainstorm_id or null,
    "confidence_level": session.brainstorm_input.confidence_level or null,
    "pre_populated_fields": session.brainstorm_input.pre_populated_fields or []
  },
  "progress": {
    "current_phase": 0,
    "phases_completed": [],
    "completion_percentage": 0,
    "total_questions_asked": 0
  },
  "phases": {},
  "completed_outputs": {
    "project_type": null,
    "problem_statement": BUSINESS_IDEA or null,
    "user_types": [],
    "personas": [],
    "business_goals": [],
    "scope_boundaries": {},
    "complexity_assessment": null,
    "functional_requirements": [],
    "nfr_requirements": [],
    "data_entities": [],
    "integrations": [],
    "adr_prerequisites": [],
    "requirements_file_path": null,
    "validation_status": null,
    "next_action": null
  }
}

Write(file_path="devforgeai/specs/ideation/${IDEATION_ID}.checkpoint.json", content=checkpoint)
```

VERIFY: `Glob(pattern="devforgeai/specs/ideation/${IDEATION_ID}.checkpoint.json")`
IF not found: HALT -- "Initial checkpoint was NOT created."

### Step 0.6: Display Session Banner

```
Display:
"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  DevForgeAI Ideation Session
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Session: ${IDEATION_ID}
Mode: ${MODE == 'resume' ? 'Resumed' : 'New Ideation'}
Business Idea: ${BUSINESS_IDEA || 'To be discovered in Phase 2'}
Brainstorm Input: ${BRAINSTORM_FILE || 'None'}
Project Mode: ${PROJECT_MODE || 'Auto-detect'}

Phases: 7 (Pre-Flight > Discovery > Elicitation > Compliance > Artifacts > Validation > Handoff)
Estimated Duration: 30-90 minutes
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
```

Set CURRENT_PHASE = 1.

---

## Phase Orchestration Loop

```
FOR phase_num in range(CURRENT_PHASE, 8):  # Phases 01-07

    1. LOAD: Read(file_path=".claude/skills/spec-driven-ideation/phases/{phase_files[phase_num]}")
       Load the phase file FRESH. Do NOT rely on memory of previous reads.

    2. REFERENCE: Read the phase's reference files as specified in the phase Contract section.
       Each phase references files in .claude/skills/spec-driven-ideation/references/.
       Load ALL listed references. Do not skip any.

    3. EXECUTE: Follow EVERY step in the phase file using EXECUTE-VERIFY-RECORD triplets.
       - Each step's EXECUTE tells you exactly what AskUserQuestion to call or action to take
       - Each step's VERIFY tells you how to confirm the data was captured
       - Each step's RECORD tells you how to update the checkpoint

    4. EXIT CRITERIA: Verify ALL phase exit criteria are met before proceeding.
       IF any required data key is null or empty: HALT.
       IF questions_answered < minimum_questions: HALT.

    5. CHECKPOINT: Update checkpoint JSON with phase completion.
       Write updated checkpoint to disk.
       Verify write via Glob().

    6. CONTEXT CHECK: If estimated context > 70%, offer save-and-resume via AskUserQuestion.
       IF user chooses "Save and resume later":
         Write final checkpoint, display resume command, EXIT skill.
         Display: "Run /ideate --resume ${IDEATION_ID} to continue."
```

---

## Phase Table

| Phase | Name | File | Min Qs | Required Data |
|-------|------|------|--------|---------------|
| 00 | Initialization | (inline above) | 0-1 | session_id, checkpoint on disk |
| 01 | Pre-Flight & Context Detection | `phases/phase-01-preflight.md` | 0-3 | project_type, user_input_patterns_loaded |
| 02 | Discovery & Problem Understanding | `phases/phase-02-discovery.md` | 5 | problem_statement, user_types[>=1], business_goals[>=1], scope_boundaries |
| 03 | Requirements Elicitation | `phases/phase-03-elicitation.md` | 10 | functional_requirements[>=5], nfr_requirements[>=1], data_entities[>=1] |
| 04 | Constitutional Compliance | `phases/phase-04-compliance.md` | 0 | compliance_checked=true, adr_prerequisites (list) |
| 05 | Artifact Generation | `phases/phase-05-artifacts.md` | 0-2 | requirements_file_path (non-null, file on disk, F4 fields present) |
| 06 | Self-Validation | `phases/phase-06-validation.md` | 0-1 | validation_status in [PASSED, PASSED_WITH_WARNINGS] |
| 07 | Completion & Handoff | `phases/phase-07-handoff.md` | 1-3 | completion_summary_displayed=true, next_action_determined=true |

---

## Required Subagents

| Phase | Subagent | Enforcement |
|-------|----------|-------------|
| 01 | internet-sleuth | CONDITIONAL (if user opts for market research enrichment) |
| 04 | context-validator | CONDITIONAL (if context files exist for brownfield check) |

---

## State Persistence

- **Checkpoint:** `devforgeai/specs/ideation/${IDEATION_ID}.checkpoint.json`
- **Output:** `devforgeai/specs/requirements/{project-name}-requirements.md`
- **References:** `.claude/skills/spec-driven-ideation/references/` (shared read, not duplicated)
- **Templates:** `.claude/skills/spec-driven-ideation/assets/templates/` (shared read)
- **Scripts:** `.claude/skills/spec-driven-ideation/scripts/` (shared read)

---

## Workflow Completion Validation

```
IF phases_completed < 7: HALT "WORKFLOW INCOMPLETE - {completed_count}/7 phases"
IF requirements_file not on disk (Glob returns empty): HALT "Requirements document not generated"
IF validation_status not in [PASSED, PASSED_WITH_WARNINGS]: HALT "Validation did not pass"
IF checkpoint still exists: Mark checkpoint status = "complete"
```

---

## Error Handling

Load error recovery patterns from: `.claude/skills/spec-driven-ideation/references/error-handling-index.md`

**Error Type Files (load on-demand):**
1. `error-type-1-incomplete-answers.md` - Vague/incomplete user responses
2. `error-type-2-artifact-failures.md` - File write/permission errors
3. `error-type-3-complexity-errors.md` - Complexity assessment errors
4. `error-type-4-validation-failures.md` - Quality validation issues
5. `error-type-5-constraint-conflicts.md` - Brownfield constraint conflicts
6. `error-type-6-directory-issues.md` - Directory structure issues

**Graceful Degradation Priority:**
1. User answers (highest - never lose)
2. Problem statement
3. Functional requirements
4. Non-functional requirements
5. Data entities
6. Integrations (lowest - can be discovered later)

---

## Success Criteria

- All 7 phases executed (no skipping)
- requirements.md exists on disk with all F4 schema sections
- Validation passed (PASSED or PASSED_WITH_WARNINGS)
- User validated requirements accuracy
- Checkpoint marked as complete
- Next steps displayed to user
