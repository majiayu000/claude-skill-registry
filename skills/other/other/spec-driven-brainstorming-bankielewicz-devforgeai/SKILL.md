---
name: spec-driven-brainstorming
description: >
  Interactive question-driven discovery skill that transforms vague business problems
  into structured AI-consumable documents. Applies structural anti-skip enforcement
  (Execute-Verify-Gate pattern) to every step of the 8-phase brainstorming process.
  Prevents token optimization bias through lean orchestration, per-phase reference
  loading, and artifact verification. Use when user says "brainstorm", wants to
  explore a vague business problem, needs stakeholder analysis, or runs /brainstorm.
  Do NOT use when user has structured requirements (use spec-driven-ideation) or
  wants a business plan directly (use planning-business).
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
topics: brainstorm, discovery, business analysis, ideation, stakeholder, problem exploration, anti-skip
---

# Discovering Problems

Transform vague business problems into structured, AI-consumable discovery documents through guided interactive questioning.

**Output:** `devforgeai/specs/brainstorms/BRAINSTORM-{NNN}-{short-name}.brainstorm.md`
**Feeds Into:** `/ideate` command for formal requirements generation

---

## Execution Model

This skill expands inline. After invocation, execute Phase 00 Initialization immediately. Do not wait passively, ask permission, or offer execution options.

**Self-Check (if ANY box is true = VIOLATION):**

- [ ] Stopping to ask about token budget
- [ ] Stopping to offer execution options
- [ ] Waiting passively for user to say "go"
- [ ] Asking "should I execute this?"
- [ ] Skipping a phase because it "seems simple"

**IF any box checked:** EXECUTION MODEL VIOLATION. Go directly to Phase 00 Initialization now.

---

## Anti-Skip Enforcement Contract

This skill enforces 4 independent anti-skip layers. ALL FOUR must fail for a step to be skipped:

1. **Per-phase reference loading** - Each phase loads its reference file fresh via `Read()`. NOT consolidated. Prevents "already covered" rationalization.
2. **Checkpoint-based state tracking** - Phase completion verified by checking checkpoint JSON data keys and `current_phase` field.
3. **Artifact verification** - Checkpoint JSON existence checked via `Glob()`, output document verified on disk.
4. **Step registry with question completion** - Each phase has minimum question counts and required data keys. Phase exit criteria checked before proceeding.

**Execute-Verify-Gate Pattern:** Every mandatory step in every phase file has three parts:
- **EXECUTE:** The exact AskUserQuestion call, Task call, or Write call to perform
- **VERIFY:** How to confirm the action happened (user response non-empty, file exists, data key populated)
- **RECORD:** Update checkpoint JSON with captured data; increment question counter

**Token Optimization Bias is PROHIBITED.** Do not skip, compress, or shortcut any step. Every phase step exists because a previous failure proved it necessary.

---

## Parameter Extraction

Extract from conversation context:

| Parameter | Source | Default |
|-----------|--------|---------|
| `$TOPIC` | Text after `/brainstorm` command | null (will ask in Phase 01) |
| `$RESUME_ID` | `--resume BRAINSTORM-NNN` argument | null (new session) |
| `$MODE` | Derived from above | "new" or "resume" |

---

## Phase 00: Initialization [INLINE - Bootstraps State]

This phase runs inline because it creates the state that all other phases depend on.

### Step 0.1: Parse Arguments

```
IF conversation contains "--resume BRAINSTORM-":
  Extract BRAINSTORM_ID from argument
  MODE = "resume"
ELSE IF conversation contains topic text after /brainstorm:
  TOPIC = extracted text
  MODE = "new"
ELSE:
  MODE = "new"
  TOPIC = null
```

### Step 0.2: Handle Resume Mode

```
IF MODE == "resume":
  checkpoint_path = "devforgeai/specs/brainstorms/${BRAINSTORM_ID}.checkpoint.json"
  Glob(pattern=checkpoint_path)

  IF found:
    Read(file_path=checkpoint_path)
    Restore session state from checkpoint
    CURRENT_PHASE = checkpoint.progress.current_phase
    Display: "Resuming ${BRAINSTORM_ID} from Phase ${CURRENT_PHASE}"
    GOTO Phase Orchestration Loop at CURRENT_PHASE
  ELSE:
    Display: "No checkpoint found for ${BRAINSTORM_ID}."
    AskUserQuestion:
      Question: "No checkpoint found. What would you like to do?"
      Header: "Resume"
      Options:
        - label: "Start a new brainstorm"
          description: "Begin fresh session"
        - label: "Check for completed document"
          description: "Look for existing brainstorm output"
    IF "Start new": MODE = "new", continue below
    IF "Check completed": Glob for existing .brainstorm.md files, display results
```

### Step 0.3: Generate Brainstorm ID (New Session)

```
IF MODE == "new":
  # Scan for highest existing ID
  Glob(pattern="devforgeai/specs/brainstorms/BRAINSTORM-*.brainstorm.md")
  Glob(pattern="devforgeai/specs/brainstorms/BRAINSTORM-*.checkpoint.json")

  # Extract highest NNN, increment
  BRAINSTORM_ID = "BRAINSTORM-{NNN+1}" (zero-padded to 3 digits minimum)

  # Ensure output directory exists
  Glob(pattern="devforgeai/specs/brainstorms/.gitkeep")
  IF not found: Create directory structure
```

### Step 0.4: Create Initial Checkpoint

```
checkpoint = {
  "checkpoint_version": "1.0",
  "brainstorm_id": BRAINSTORM_ID,
  "session_number": 1,
  "created_at": "current timestamp",
  "status": "in_progress",
  "progress": {
    "current_phase": 0,
    "phases_completed": [],
    "completion_percentage": 0
  },
  "completed_outputs": {},
  "topic": TOPIC
}

Write(file_path="devforgeai/specs/brainstorms/${BRAINSTORM_ID}.checkpoint.json", content=checkpoint)
```

VERIFY: `Glob(pattern="devforgeai/specs/brainstorms/${BRAINSTORM_ID}.checkpoint.json")`
IF not found: HALT -- "Initial checkpoint was NOT created."

### Step 0.5: Display Session Banner

```
Display:
"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  DevForgeAI Discovery Session
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Session: ${BRAINSTORM_ID}
Mode: New Discovery
Topic: ${TOPIC || 'To be discovered in Phase 1'}

Phases: 7 (Stakeholders > Problem > Opportunities > Constraints > Hypotheses > Priorities > Synthesis)
Estimated Duration: 20-45 minutes
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
```

Set CURRENT_PHASE = 1.

---

## Phase Orchestration Loop

```
FOR phase_num in range(CURRENT_PHASE, 8):  # Phases 01-07

    1. LOAD: Read(file_path=".claude/skills/spec-driven-brainstorming/phases/{phase_files[phase_num]}")
       Load the phase file FRESH. Do NOT rely on memory of previous reads.

    2. REFERENCE: Read the phase's reference file as specified in the phase Contract section.
       Each phase references a file in .claude/skills/spec-driven-brainstorming/references/.

    3. EXECUTE: Follow EVERY step in the phase file using EXECUTE-VERIFY-RECORD triplets.
       - Each step's EXECUTE tells you exactly what AskUserQuestion to call
       - Each step's VERIFY tells you how to confirm the data was captured
       - Each step's RECORD tells you how to update the checkpoint

    4. EXIT CRITERIA: Verify ALL phase exit criteria are met before proceeding.
       IF any required data key is null or empty: HALT.

    5. CHECKPOINT: Update checkpoint JSON with phase completion.
       Write updated checkpoint to disk.

    6. CONTEXT CHECK: If estimated context > 70%, offer save-and-resume via AskUserQuestion.
       IF user chooses "Save and resume later":
         Write final checkpoint, display resume command, EXIT skill.
```

---

## Phase Table

| Phase | Name | File | Min Questions | Required Data |
|-------|------|------|---------------|---------------|
| 00 | Initialization | (inline above) | 0 | brainstorm_id, checkpoint on disk |
| 01 | Stakeholder Discovery | `phases/phase-01-stakeholder-discovery.md` | 5 | stakeholders.primary[>=1], goals, concerns |
| 02 | Problem Exploration | `phases/phase-02-problem-exploration.md` | 5 | problem_statement, root_causes[>=1], pain_points[>=1] |
| 03 | Opportunity Mapping | `phases/phase-03-opportunity-mapping.md` | 3 | opportunities[>=1], ideal_state |
| 04 | Constraint Discovery | `phases/phase-04-constraint-discovery.md` | 3 | constraints.budget, constraints.timeline |
| 05 | Hypothesis Formation | `phases/phase-05-hypothesis-formation.md` | 2 | hypotheses[>=1] |
| 06 | Prioritization | `phases/phase-06-prioritization.md` | 2 | prioritization.must_have[>=1] |
| 07 | Handoff Synthesis | `phases/phase-07-synthesis.md` | 0 | output_file_path (file exists on disk) |

---

## Required Subagents

| Phase | Subagent | Enforcement |
|-------|----------|-------------|
| 01 | stakeholder-analyst | OPTIONAL (enhances analysis, not blocking) |
| 03 | internet-sleuth | CONDITIONAL (user opts in to market research) |

---

## State Persistence

- **Checkpoint:** `devforgeai/specs/brainstorms/${BRAINSTORM_ID}.checkpoint.json`
- **Output:** `devforgeai/specs/brainstorms/${BRAINSTORM_ID}-${short_name}.brainstorm.md`
- **Templates:** `.claude/skills/spec-driven-brainstorming/assets/templates/` (loaded via Read, not duplicated)

---

## Workflow Completion Validation

```
IF phases_completed < 7: HALT "WORKFLOW INCOMPLETE - {completed_count}/7 phases"
IF output_file not on disk (Glob returns empty): HALT "Output document not generated"
IF checkpoint still exists: Delete checkpoint (session complete)
```

---

## Error Handling

Load error recovery patterns from: `.claude/skills/spec-driven-brainstorming/references/error-handling.md`

**Graceful Degradation Priority:**
1. User answers (highest - never lose)
2. Problem statement
3. Stakeholder map
4. Constraints
5. Priorities
6. Market research (lowest - can skip)

---

## Success Criteria

- All 7 phases executed (no skipping)
- Output document exists on disk with all sections
- User validated output accuracy
- Checkpoint deleted after successful completion
- Next steps displayed to user
