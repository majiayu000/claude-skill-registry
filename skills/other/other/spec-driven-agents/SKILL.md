---
name: spec-driven-agents
description: >
  Create DevForgeAI-aware Claude Code subagents with structural anti-skip enforcement
  (Execute-Verify-Record pattern) across all 6 phases. Prevents token optimization bias
  through lean orchestration, per-phase reference loading, checkpoint persistence, and
  artifact verification. Use when user runs /create-agent command, requests custom
  subagent creation with framework integration, or says "create a subagent" or
  "generate an agent". Supports guided, template, domain, and custom spec modes.
  Do NOT use for skill creation (use skill-creator) or command creation (use manual workflow).
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
version: "1.0.0"
topics: agents, subagents, generation, DevForgeAI, anti-skip enforcement, framework compliance
---

# Creating Agents

Create DevForgeAI-aware Claude Code subagents through guided specification with framework compliance validation.

**Output:** `.claude/agents/{name}.md` (subagent file) + optional reference file
**Invoked by:** `/create-agent` command
**Delegates to:** `agent-generator` subagent v2.0

---

## Execution Model

This skill expands inline. After invocation, execute Phase 00 Initialization immediately. Do not wait passively, ask permission, or offer execution options.

**Self-Check (if ANY box is true = VIOLATION):**

- [ ] Stopping to ask about token budget
- [ ] Stopping to offer execution options
- [ ] Waiting passively for user to say "go"
- [ ] Asking "should I execute this?"
- [ ] Skipping a phase because it "seems simple"
- [ ] Skipping reference loading because "already covered"
- [ ] Generating agent file without completing Phase 05 validation

**IF any box checked:** EXECUTION MODEL VIOLATION. Go directly to Phase 00 Initialization now.

---

## Anti-Skip Enforcement Contract

This skill enforces 4 independent anti-skip layers. ALL FOUR must fail for a step to be skipped:

1. **Per-phase reference loading** - Each phase loads its reference file fresh via `Read()`. NOT consolidated. Prevents "already covered" rationalization.
2. **Checkpoint-based state tracking** - Phase completion verified by checking checkpoint JSON data keys and `current_phase` field.
3. **Artifact verification** - Checkpoint JSON existence checked via `Glob()`, generated files verified on disk.
4. **Step registry with data key completion** - Each phase has minimum step counts and required data keys. Phase exit criteria checked before proceeding.

**Execute-Verify-Record Pattern:** Every mandatory step in every phase file has three parts:
- **EXECUTE:** The exact Read, Write, AskUserQuestion, or Task call to perform
- **VERIFY:** How to confirm the action happened (file exists, data key populated, response non-empty)
- **RECORD:** Update checkpoint JSON with captured data

**Token Optimization Bias is PROHIBITED.** Do not skip, compress, or shortcut any step. Every phase step exists because a previous failure proved it necessary.

---

## Parameter Extraction

Extract from conversation context:

| Parameter | Source | Default |
|-----------|--------|---------|
| `$NAME` | First argument after `/create-agent` | null (will ask in Phase 02) |
| `$MODE` | `--template=`, `--domain=`, `--spec=`, or guided | "guided" |
| `$TEMPLATE` | Value from `--template=` flag | null |
| `$DOMAIN` | Value from `--domain=` flag | null |
| `$SPEC_FILE` | Value from `--spec=` flag | null |
| `$RESUME_ID` | `--resume AGENT-NNN` argument | null (new session) |

---

## Phase 00: Initialization [INLINE - Bootstraps State]

This phase runs inline because it creates the state that all other phases depend on.

### Step 0.1: Parse Arguments

```
IF conversation contains "--resume AGENT-":
  Extract AGENT_ID from argument
  MODE = "resume"
ELSE:
  MODE = "new"
  Extract $NAME, $MODE, $TEMPLATE, $DOMAIN, $SPEC_FILE from conversation markers
```

### Step 0.2: Handle Resume Mode

```
IF MODE == "resume":
  checkpoint_path = "devforgeai/workflows/agent-creation/${AGENT_ID}.checkpoint.json"
  Glob(pattern=checkpoint_path)

  IF found:
    Read(file_path=checkpoint_path)
    Restore session state from checkpoint
    CURRENT_PHASE = checkpoint.progress.current_phase
    Display: "Resuming ${AGENT_ID} from Phase ${CURRENT_PHASE}"
    GOTO Phase Orchestration Loop at CURRENT_PHASE
  ELSE:
    Display: "No checkpoint found for ${AGENT_ID}."
    AskUserQuestion:
      Question: "No checkpoint found. What would you like to do?"
      Header: "Resume"
      Options:
        - label: "Start a new agent creation"
          description: "Begin fresh session"
        - label: "Cancel"
          description: "Exit without action"
    IF "Start new": MODE = "new", continue below
    IF "Cancel": EXIT skill
```

### Step 0.3: Generate Session ID (New Session)

```
IF MODE == "new":
  # Scan for highest existing ID
  Glob(pattern="devforgeai/workflows/agent-creation/AGENT-*.checkpoint.json")

  # Extract highest NNN, increment
  AGENT_ID = "AGENT-{NNN+1}" (zero-padded to 3 digits minimum)

  # Ensure output directory exists
  Glob(pattern="devforgeai/workflows/agent-creation/.gitkeep")
  IF not found: Create directory structure
```

### Step 0.4: Create Initial Checkpoint

```
checkpoint = {
  "checkpoint_version": "1.0",
  "session_id": AGENT_ID,
  "created_at": "current timestamp",
  "status": "in_progress",
  "progress": {
    "current_phase": 0,
    "phases_completed": [],
    "completion_percentage": 0
  },
  "parameters": {
    "agent_name": $NAME,
    "creation_mode": $MODE,
    "domain": $DOMAIN,
    "template_name": $TEMPLATE,
    "spec_file": $SPEC_FILE
  },
  "framework_context": {
    "references_loaded": [],
    "context_files_required": []
  },
  "specification": {
    "name": null,
    "purpose": null,
    "domain": null,
    "tools": [],
    "model": null,
    "responsibilities": [],
    "integration_skills": [],
    "context_files": []
  },
  "generation": {
    "generated_files": {},
    "validation_results": null,
    "reference_file_needed": false
  },
  "phases": {
    "01": { "status": "pending", "steps_completed": [] },
    "02": { "status": "pending", "steps_completed": [], "questions_answered": 0 },
    "03": { "status": "pending", "steps_completed": [] },
    "04": { "status": "pending", "steps_completed": [] },
    "05": { "status": "pending", "steps_completed": [] },
    "06": { "status": "pending", "steps_completed": [] }
  }
}

Write(file_path="devforgeai/workflows/agent-creation/${AGENT_ID}.checkpoint.json", content=checkpoint)
```

VERIFY: `Glob(pattern="devforgeai/workflows/agent-creation/${AGENT_ID}.checkpoint.json")`
IF not found: HALT -- "Initial checkpoint was NOT created."

### Step 0.5: Display Session Banner

```
Display:
"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  DevForgeAI Agent Creation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Session: ${AGENT_ID}
Mode: ${MODE}
Agent Name: ${NAME || 'To be determined in Phase 2'}

Phases: 6 (Context > Requirements > Specification > Generation > Validation > Handoff)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
```

Set CURRENT_PHASE = 1.

---

## Phase Orchestration Loop

```
FOR phase_num in range(CURRENT_PHASE, 7):  # Phases 01-06

    1. LOAD: Read(file_path="src/claude/skills/spec-driven-agents/phases/{phase_files[phase_num]}")
       Load the phase file FRESH. Do NOT rely on memory of previous reads.

    2. REFERENCE: Read the phase's reference file as specified in the phase Contract section.
       Each phase references a file in src/claude/skills/spec-driven-agents/references/.

    3. EXECUTE: Follow EVERY step in the phase file using EXECUTE-VERIFY-RECORD triplets.
       - Each step's EXECUTE tells you exactly what action to perform
       - Each step's VERIFY tells you how to confirm the action happened
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

| Phase | Name | File | Min Steps | Required Data |
|-------|------|------|-----------|---------------|
| 00 | Initialization | (inline above) | 5 | session_id, checkpoint on disk |
| 01 | Framework Context Loading | `phases/phase-01-framework-context.md` | 3 | references_loaded[>=3] |
| 02 | Requirements Gathering | `phases/phase-02-requirements-gathering.md` | 5 | agent_name, purpose, domain, tools, model |
| 03 | Specification Assembly | `phases/phase-03-specification-assembly.md` | 3 | spec_file on disk |
| 04 | Agent Generation | `phases/phase-04-agent-generation.md` | 2 | generated_file on disk |
| 05 | Validation | `phases/phase-05-validation.md` | 3 | validation_status, 12-point results |
| 06 | Result Processing | `phases/phase-06-result-handoff.md` | 3 | output displayed, checkpoint deleted |

---

## Required Subagents

| Phase | Subagent | Enforcement |
|-------|----------|-------------|
| 04 | agent-generator | BLOCKING (must invoke via Task, cannot generate inline) |

---

## State Persistence

- **Checkpoint:** `devforgeai/workflows/agent-creation/${AGENT_ID}.checkpoint.json`
- **Output:** `.claude/agents/{name}.md` (generated subagent)
- **Reference (if needed):** `.claude/agents/{name}/references/{name}-patterns.md`
- **Templates:** `src/claude/skills/spec-driven-agents/assets/templates/` (loaded via Read, not duplicated)

---

## Workflow Completion Validation

```
IF phases_completed < 6: HALT "WORKFLOW INCOMPLETE - {completed_count}/6 phases"
IF generated_file not on disk (Glob returns empty): HALT "Subagent file not generated"
IF validation_status != "PASS" and validation_status != "PASS WITH WARNINGS": HALT "Validation not passed"
IF checkpoint still exists: Delete checkpoint (session complete)
```

---

## Error Handling

Load error recovery patterns from: `src/claude/skills/spec-driven-agents/references/error-handling.md`

**Graceful Degradation Priority:**
1. User specification data (highest - never lose)
2. Framework context
3. Validation results
4. Reference file generation (lowest - can skip with user approval)

---

## Success Criteria

- All 6 phases executed (no skipping)
- Subagent file exists on disk with all 10 required sections
- 12-point validation passed (or PASS WITH WARNINGS acknowledged)
- Checkpoint deleted after successful completion
- Next steps displayed to user
- Integration points documented

---

## Templates

Available in `src/claude/skills/spec-driven-agents/assets/templates/`:

| Template | Domain | Purpose |
|----------|--------|---------|
| `code-reviewer-template.md` | QA | Code quality, security, best practices review |
| `test-automator-template.md` | QA | TDD test generation (unit, integration, E2E) |
| `documentation-writer-template.md` | Documentation | Technical docs, API specs, user guides |
| `deployment-coordinator-template.md` | Deployment | Infrastructure, CI/CD, release management |
| `requirements-analyst-template.md` | Architecture | User story creation, acceptance criteria |
| `skill-template.md` | Meta | Skill creation template |
| `command-template-lean-orchestration.md` | Meta | Command refactoring subagents |

---

## Integration with DevForgeAI

**This skill is invoked by:**
- `/create-agent` command (primary entry point)
- Direct invocation: `Skill(command="spec-driven-agents")`

**This skill invokes:**
- `agent-generator` subagent v2.0 (Phase 04, for actual generation)

**Created subagents work with:**
- All DevForgeAI skills (spec-driven-dev, spec-driven-qa, spec-driven-architecture, etc.)
- Claude Code workflows (official pattern compliance)
