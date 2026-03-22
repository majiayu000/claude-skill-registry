---
name: spec-driven-rca
description: >
  Unified root cause analysis with 4-layer anti-skip enforcement for both tactical
  (dev workflow diagnosis) and strategic (5 Whys RCA documents) modes. Tactical mode
  auto-triggers after 2-3 failed fix attempts during TDD, returning fix prescriptions.
  Strategic mode invoked via /rca command, producing self-contained RCA documents with
  5 Whys analysis, evidence collection, and actionable recommendations. Uses
  Execute-Verify-Record pattern at every step to prevent token optimization bias.
  Use this skill whenever root cause analysis is needed — after repeated test failures,
  integration failures, QA violations, framework breakdowns, workflow violations,
  or when the user runs /rca. Also use when the diagnosis-before-fix rule triggers
  after 3+ consecutive fix attempts on the same error.
metadata:
  author: DevForgeAI
  version: "2.0.0"
  category: quality-assurance
  agent-skills-spec-version: "1.0"
  last-updated: "2026-03-18"
  migrated-from: root-cause-diagnosis v1.0.0 + devforgeai-rca v1.0.0
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - AskUserQuestion
  - Task
  - Bash(devforgeai-validate:*)
  - Bash(git:*)
model: opus
effort: High
---

# Spec-Driven RCA

Unified root cause analysis for the DevForgeAI framework. Operates in two modes:

- **Tactical:** Fast diagnosis during dev workflow after repeated fix failures. Returns fix prescriptions. (Phases 00-03)
- **Strategic:** Full 5 Whys RCA for framework breakdowns. Creates self-contained RCA documents. (Phases 00-02, 04-08)

**Core Principle:** Understanding WHY a failure occurred is mandatory before attempting HOW to fix it. Every step in this skill exists because a previous failure proved it necessary.

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
- [ ] Skipping verification because "I already know the answer"
- [ ] Attempting fixes before Phase 02 Investigation completes
- [ ] Guessing at root causes without evidence

**IF any box checked:** EXECUTION MODEL VIOLATION. Go directly to Phase State Initialization now.

---

## Anti-Skip Enforcement Contract

This skill enforces 4 independent anti-skip layers. ALL FOUR must fail for a step to be skipped:

1. **Fresh-context subagent execution** — diagnostic-analyst subagent in Phase 02 runs in isolated read-only context, preventing accidental state mutation during investigation
2. **Binary CLI gates** — `devforgeai-validate` commands enforce phase state transitions; cannot be forged by LLM
3. **Hook enforcement** — Shell scripts in `.claude/hooks/` run outside LLM control
4. **Step registry + artifact verification** — Glob/Grep confirmation after every step, not trust-based

**Execute-Verify-Record Pattern:** Every mandatory step in every phase file has three parts:
- **EXECUTE:** The exact action to perform
- **VERIFY:** How to confirm the action happened (Glob, Grep, exit code)
- **RECORD:** CLI command to record completion (`devforgeai-validate phase-record`)

**Token Optimization Bias is PROHIBITED.** Do not skip, compress, or shortcut any step. Every phase step exists because a previous failure proved it necessary.

---

## Validation Modes

This skill operates in two modes, determined during Phase 00 Initialization.

### Tactical Mode (Dev Workflow Diagnosis)

**When:** Auto-triggered during dev workflow after 2-3 failed fix attempts on the same error. Also triggered when diagnosis-before-fix rule fires.

**Phase Route:** `00 → 01 → 02 → 03 → END`

**Output:** Fix prescriptions returned to invoking workflow phase for execution.

**Context Markers (set by dev workflow):**
- `**Mode:** tactical`
- `**Fix Attempts:** {count}`
- `**Phase:** {Green|Integration|QA}`
- `**Story ID:** {STORY-NNN}`
- `**Error:** {error message}`

### Strategic Mode (Full RCA Document)

**When:** Invoked via `/rca` command or manually for framework breakdowns.

**Phase Route:** `00 → 01 → 02 → 04 → 05 → 06 → 07 → 08 → END`

**Output:** Self-contained RCA document in `devforgeai/RCA/RCA-{NNN}-{slug}.md`

**Context Markers (set by /rca command):**
- `**Mode:** strategic` (or absent — defaults to strategic)
- `**Issue Description:** {text}`
- `**Severity:** {CRITICAL|HIGH|MEDIUM|LOW|infer}`
- `**Command:** rca`

### Mode Detection Priority

```
IF context contains "**Mode:** tactical" OR "**Fix Attempts:**":
    MODE = tactical
    ACTIVE_PHASES = [00, 01, 02, 03]
ELIF context contains "**Mode:** strategic" OR "**Issue Description:**" OR "**Command:** rca":
    MODE = strategic
    ACTIVE_PHASES = [00, 01, 02, 04, 05, 06, 07, 08]
ELSE:
    AskUserQuestion:
        Question: "This skill supports two modes. Which do you need?"
        Header: "RCA Mode"
        Options:
            - label: "Tactical — Quick diagnosis for dev workflow failures"
              description: "Returns fix prescriptions. Use when tests keep failing during /dev."
            - label: "Strategic — Full RCA with 5 Whys analysis"
              description: "Creates self-contained RCA document. Use for framework breakdowns."
        multiSelect: false
    MODE = user selection
    ACTIVE_PHASES = tactical ? [00,01,02,03] : [00,01,02,04,05,06,07,08]
```

---

## Parameter Extraction

Extract parameters from conversation context markers. See `references/parameter-extraction.md` for the complete extraction algorithm for both modes.

---

## Phase State Initialization [MANDATORY FIRST]

Derive SESSION_ID from mode and context:

```
IF MODE == tactical:
    SESSION_ID = "DIAG-" + STORY_ID
    # Example: "DIAG-STORY-127"
ELIF MODE == strategic:
    SESSION_ID = "RCA-" + rca_number
    # Example: "RCA-031"
```

```bash
devforgeai-validate phase-init ${SESSION_ID} --workflow=rca --project-root=.
```

| Exit Code | Meaning | Action |
|-----------|---------|--------|
| 0 | New workflow | State file created. Set CURRENT_PHASE = "00". |
| 1 | Existing workflow | Resume. Check checkpoint file for CURRENT_PHASE. |
| 2 | Invalid session ID | HALT. Verify parameters. |
| 127 | CLI not installed | Continue without enforcement (backward compatibility). |

**Resume Detection:** If resuming, read checkpoint:
```
Read(file_path="devforgeai/temp/.rca-checkpoint-${SESSION_ID}.yaml")
```
Extract `current_phase` and `phase_completion` to determine where to resume.

---

## Phase Orchestration Loop

```
FOR phase_num in ACTIVE_PHASES:
    phase_id = format(phase_num, "02d")

    1. ENTRY GATE: devforgeai-validate phase-check ${SESSION_ID} --workflow=rca --from={prev} --to={phase_id}
       IF exit != 0: HALT

    2. LOAD: Read(file_path=".claude/skills/spec-driven-rca/phases/{phase_files[phase_id]}")

    3. EXECUTE: Follow every step in the phase file (EXECUTE-VERIFY-RECORD triplets)
       - Each step's EXECUTE instruction tells you exactly what to do
       - Each step's VERIFY instruction tells you how to confirm it happened
       - Each step's RECORD instruction tells you what CLI command to call

    4. RECORD: devforgeai-validate phase-record ${SESSION_ID} --workflow=rca --phase={phase_id}

    5. EXIT GATE: devforgeai-validate phase-complete ${SESSION_ID} --workflow=rca --phase={phase_id} --checkpoint-passed
       IF exit != 0: HALT
```

---

## Phase Index

| Phase | Name | Tactical | Strategic | File | Required Subagents |
|-------|------|----------|-----------|------|--------------------|
| 00 | Initialization | Yes | Yes | `phases/phase-00-initialization.md` | None |
| 01 | Capture | Yes | Yes | `phases/phase-01-capture.md` | None |
| 02 | Investigation | Yes | Yes | `phases/phase-02-investigation.md` | diagnostic-analyst |
| 03 | Prescription | Yes | No | `phases/phase-03-prescription.md` | None |
| 04 | Evidence Organization | No | Yes | `phases/phase-04-evidence-organization.md` | None |
| 05 | Recommendation Generation | No | Yes | `phases/phase-05-recommendation-generation.md` | None |
| 06 | RCA Document Creation | No | Yes | `phases/phase-06-document-creation.md` | None |
| 07 | Validation & Self-Check | No | Yes | `phases/phase-07-validation.md` | None |
| 08 | Completion & Pipeline | No | Yes | `phases/phase-08-completion.md` | None |

---

## HALT: NO FIX ATTEMPTS UNTIL Phase 02 COMPLETES

This is a blocking requirement for BOTH modes. Any code changes, edits, or operations targeting production or test files are FORBIDDEN until the investigation phase produces a report. Violation of this rule constitutes shotgun debugging and invalidates the diagnosis.

If prior fix attempts >= 3 without completing Phase 02, escalate to user:
```
AskUserQuestion: "{count} fix attempts have failed without diagnosis.
Systematic investigation is required. Proceed with full diagnosis? [Y/n]"
```

---

## Escalation Protocol (Tactical Mode)

### 3-Attempt Escalation Rule

| Attempt | Action |
|---------|--------|
| 1-2 | Normal fix-test cycle (no diagnosis needed) |
| 3 | HALT. Invoke full spec-driven-rca skill in tactical mode |
| 4 | If diagnosis prescription fails, try next hypothesis |
| 5 | HALT. Escalate to user via AskUserQuestion |

### Escalation Message Template

After attempt 5 (or after all hypotheses exhausted):
```
AskUserQuestion: "Persistent failure after diagnosis and {N} fix attempts.

Error: {error_message}
Diagnosis: {top_hypothesis}
Attempts: {fix_attempt_count}

Options:
1. Provide additional context or hints
2. Skip this acceptance criterion (requires justification)
3. Pause and investigate manually"
```

---

## State Persistence

**Phase State:** `devforgeai/workflows/${SESSION_ID}-rca-phase-state.json`
**Session Memory:** `.claude/memory/sessions/${SESSION_ID}-rca-session.md`
**Checkpoint:** `devforgeai/temp/.rca-checkpoint-${SESSION_ID}.yaml`

---

## Reference Files (Progressive Loading)

References are loaded on-demand by each phase. Do NOT pre-load all references.

| Phase | Reference File | Purpose |
|-------|---------------|---------|
| 00 | `references/parameter-extraction.md` | Context marker extraction for both modes |
| 01 (strategic) | `references/framework-integration-points.md` | Determine which files to read |
| 02 (tactical) | `references/investigation-patterns.md` | 6 failure category taxonomy |
| 02 (strategic) | `references/5-whys-methodology.md` | How to perform effective 5 Whys |
| 04 | `references/evidence-collection-guide.md` | Evidence quality criteria |
| 05 | `references/recommendation-framework.md` | Priority criteria, implementation details |
| 06 | `references/rca-writing-guide.md` | RCA document standards |
| — | `references/workflow-integration.md` | Dev workflow integration hooks (external consumers) |
| — | `references/rca-help.md` | Command help and examples |

## Asset Templates (Strategic Mode)

| Asset | Purpose |
|-------|---------|
| `assets/5-whys-template.md` | 5 Whys section template for RCA document |
| `assets/evidence-section-template.md` | Evidence organization template |
| `assets/rca-document-template.md` | Full RCA document template |
| `assets/recommendation-template.md` | Recommendation subsection template |

---

## Integration with DevForgeAI Framework

### Invoked By

**Commands:**
- `/rca` slash command (strategic mode, primary invocation)

**Automatic Triggers (tactical mode):**
- `diagnosis-before-fix` rule after 3+ failed fix attempts
- spec-driven-dev Phase 03 (Green) after 2+ test failures
- spec-driven-dev Phase 05 (Integration) on non-environment failures
- spec-driven-qa Phase 02 (Deep Analysis) on CRITICAL/HIGH violations

**Manual Invocation:**
```
**Mode:** tactical
**Story ID:** STORY-NNN
**Error:** {error message}
**Fix Attempts:** {count}

Skill(command="spec-driven-rca")
```

### Subagents

| Subagent | Role | Phase | Required |
|----------|------|-------|----------|
| diagnostic-analyst | Read-only spec drift detection against 6 context files | Phase 02 | Yes (both modes) |

### Related Skills

- spec-driven-dev (triggers tactical mode on test failures)
- spec-driven-qa (triggers tactical mode on validation failures)
- spec-driven-stories (consumes RCA recommendations via /create-stories-from-rca)

---

## Workflow Completion Validation

```
IF MODE == tactical:
    IF completed_phases < 4: HALT "WORKFLOW INCOMPLETE - {count}/4 phases"
    IF completed_phases == 4: "Tactical diagnosis complete - returning prescription"

IF MODE == strategic:
    IF completed_phases < 8: HALT "WORKFLOW INCOMPLETE - {count}/8 phases"
    IF completed_phases == 8: "Strategic RCA complete - document created"
```

---

## Success Criteria

### Tactical Mode
- [ ] All 4 phases executed in order (00 → 01 → 02 → 03)
- [ ] No fix attempts before Phase 02 completion
- [ ] diagnostic-analyst subagent invoked in Phase 02
- [ ] At least one hypothesis with confidence >= 0.5
- [ ] Prescription includes specific file paths and actions
- [ ] Prescription returned to invoking workflow

### Strategic Mode
- [ ] All 8 phases executed in order (00 → 01 → 02 → 04 → 05 → 06 → 07 → 08)
- [ ] diagnostic-analyst subagent invoked in Phase 02
- [ ] 5 Whys complete with evidence
- [ ] Root cause validated (4 criteria)
- [ ] RCA document created at `devforgeai/RCA/RCA-{NNN}-{slug}.md`
- [ ] 3+ recommendations with exact implementation details
- [ ] Self-containedness check passed
- [ ] Completion report displayed

---

## Change Log

| Version | Date | Change |
|---------|------|--------|
| 2.0.0 | 2026-03-18 | Initial creation. Merged root-cause-diagnosis v1.0.0 (tactical 4-phase) and devforgeai-rca v1.0.0 (strategic 8-phase) into unified spec-driven skill with Execute-Verify-Record anti-skip enforcement. |
