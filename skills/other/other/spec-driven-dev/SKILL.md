---
name: spec-driven-dev
description: >
  Implements user stories through spec-driven TDD workflow (Red-Green-Refactor) with
  structural anti-skip enforcement. Replicates all 12 phases of the DevForgeAI development
  workflow using the Execute-Verify-Gate pattern at every step. Designed to prevent token
  optimization bias through lean orchestration, fresh-context subagent delegation, and
  binary CLI gate enforcement. Use when developing features from story specifications,
  building code that must comply with context files, or running TDD workflows.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
  - Task
  - Bash(git:*)
  - Bash(npm:*)
  - Bash(pytest:*)
  - Bash(dotnet:*)
  - Bash(cargo:*)
  - Bash(mvn:*)
  - Bash(gradle:*)
  - Bash(python:*)
  - Skill
model: claude-opus-4-6
effort: High
---

# Spec-Driven Development

Implement user stories using strict TDD (Red-Green-Refactor) while enforcing all 6 context file constraints.

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

**IF any box checked:** EXECUTION MODEL VIOLATION. Go directly to Phase State Initialization now.

---

## Anti-Skip Enforcement Contract

This skill enforces 4 independent anti-skip layers. ALL FOUR must fail for a step to be skipped:

1. **Fresh-context subagent execution** - Subagents run in isolated context without accumulated bias
2. **Binary CLI gates** - Compiled Rust in `src/commands/phase.rs`, cannot be forged by LLM
3. **Hook enforcement** - Shell scripts in `.claude/hooks/` run outside LLM control
4. **Step registry + artifact verification** - `.claude/hooks/phase-steps-registry.json` tracks every mandatory step

**Execute-Verify-Gate Pattern:** Every mandatory step in every phase file has three parts:
- **EXECUTE:** The exact action to perform
- **VERIFY:** How to confirm the action happened (Glob, Grep, exit code, Task result)
- **RECORD:** CLI command to record completion (`devforgeai-validate phase-record`)

**Token Optimization Bias is PROHIBITED.** Do not skip, compress, or shortcut any step. Every phase step exists because a previous failure proved it necessary. (Reference: RCA-001, RCA-002)

---

## Parameter Extraction

Extract story ID from conversation context. See `references/parameter-extraction.md` for the extraction algorithm.

## Command Integration

| Context Marker | Set By | Description |
|----------------|--------|-------------|
| `$STORY_ID` | /dev, /resume-dev | Story identifier (STORY-NNN) |
| `$FORCE_FLAG` | /dev | Bypass dependency checks |
| `$REMEDIATION_MODE` | /dev | `--fix` flag or auto-detected from gaps.json |
| `$GAPS_AUTO_DETECTED` | /dev | True if gaps.json auto-detected |
| `$IGNORE_DEBT_FLAG` | /dev | Override technical debt threshold |
| `$RESUME_MODE` | /resume-dev | "manual" or "auto" |
| `$PHASE_NUM` | /resume-dev | Phase number to resume from |

---

## Phase State Initialization [MANDATORY FIRST]

```bash
devforgeai-validate phase-init ${STORY_ID} --project-root=.
```

| Exit Code | Meaning | Action |
|-----------|---------|--------|
| 0 | New workflow | State file created. Set CURRENT_PHASE = "01". |
| 1 | Existing workflow | Resume. Run `devforgeai-validate phase-status ${STORY_ID}` to get CURRENT_PHASE. |
| 2 | Invalid story ID | HALT. Must match STORY-XXX pattern. |
| 127 | CLI not installed | Continue without enforcement (backward compatibility). |

**Iteration counter:** `iteration_count = 1`, `max_iterations = 5`. If resuming, read from phase-state.json.

---

## Phase Orchestration Loop

```
FOR phase_num in range(CURRENT_PHASE, 11):
    phase_id = format(phase_num)

    1. ENTRY GATE: devforgeai-validate phase-check ${STORY_ID} --from={prev} --to={phase_id}
       IF exit != 0: HALT

    2. LOAD: Read(file_path="phases/{phase_files[phase_id]}")

    3. EXECUTE: Follow every step in the phase file (EXECUTE-VERIFY-GATE triplets)
       - Each step's EXECUTE instruction tells you exactly what to do
       - Each step's VERIFY instruction tells you how to confirm it happened
       - Each step's RECORD instruction tells you what CLI command to call

    4. RECORD: devforgeai-validate phase-record ${STORY_ID} --phase={phase_id} --subagent={name}

    5. EXIT GATE: devforgeai-validate phase-complete ${STORY_ID} --phase={phase_id} --checkpoint-passed
       IF exit != 0: HALT
```

| Phase | Name | File |
|-------|------|------|
| 01 | Pre-Flight Validation | `phases/phase-01-preflight.md` |
| 02 | Test-First (Red) | `phases/phase-02-test-first.md` |
| 03 | Implementation (Green) | `phases/phase-03-implementation.md` |
| 04 | Refactoring | `phases/phase-04-refactoring.md` |
| 4.5 | AC Verification (Post-Refactor) | `phases/phase-04.5-ac-verification.md` |
| 05 | Integration Testing | `phases/phase-05-integration.md` |
| 5.5 | AC Verification (Post-Integration) | `phases/phase-05.5-ac-verification.md` |
| 06 | Deferral Challenge | `phases/phase-06-deferral.md` |
| 07 | DoD Update | `phases/phase-07-dod-update.md` |
| 08 | Git Workflow | `phases/phase-08-git-workflow.md` |
| 09 | Feedback Hook | `phases/phase-09-feedback.md` |
| 10 | Result Interpretation | `phases/phase-10-result.md` |

---

## Required Subagents Per Phase

| Phase | Required Subagents | Enforcement |
|-------|-------------------|-------------|
| 01 | git-validator, tech-stack-detector | BLOCKING |
| 02 | test-automator | BLOCKING |
| 03 | backend-architect OR frontend-developer, context-validator | BLOCKING |
| 04 | refactoring-specialist, code-reviewer | BLOCKING |
| 4.5 | ac-compliance-verifier | BLOCKING |
| 05 | integration-tester | BLOCKING |
| 5.5 | ac-compliance-verifier | BLOCKING |
| 06 | deferral-validator (if deferrals) | CONDITIONAL |
| 07 | (none) | N/A |
| 08 | (none) | N/A |
| 09 | framework-analyst | BLOCKING |
| 10 | dev-result-interpreter | BLOCKING |

**Deviation Protocol:** Any skip requires explicit user consent via AskUserQuestion. See `references/workflow-deviation-protocol.md`.

---

## Test File Immutability (RCA-046, RCA-047)

After Phase 02, test files are IMMUTABLE until Phase 05. Mismatches = HALT immediately.

**Back-to-Red Protocol:** If test bugs found in Phase 03/04: mark incomplete, return to Phase 02, re-invoke test-automator, create new snapshot, resume Phase 03.

---

## Remediation Mode

After Phase 01, if `$REMEDIATION_MODE == true`: Read `references/qa-remediation-workflow.md`, SKIP Phases 02-08, GOTO Phase 09.

## Technical Debt Override Banner

If `$DEBT_OVERRIDE_BANNER == true`, display at start of each phase:
```
[DEBT OVERRIDE ACTIVE - Proceeding with elevated debt]
```

---

## State Persistence

**Location:** `devforgeai/workflows/${STORY_ID}-phase-state.json`
**Session Memory:** `.claude/memory/sessions/${STORY_ID}-session.md`
**References:** `references/memory-file-schema.md`, `references/memory-file-operations.md`

---

## Workflow Completion Validation

```
IF completed_count < 10: HALT "WORKFLOW INCOMPLETE - {completed_count}/10 phases"
IF completed_count == 10: "All 10 phases completed - Workflow validation passed"
```

IF iteration_count >= 4: Display "Approaching limit"
IF iteration_count >= max_iterations: HALT "Maximum iterations reached"

---

## Success Criteria

- All tests pass (100% pass rate)
- Coverage meets thresholds (95%/85%/80%)
- Light QA validation passed
- No context file violations
- All AC implemented
- DoD validation passed
- Changes committed
- Story status = "Dev Complete"

---

## Treelint AST-Aware Search Integration

Phases 02-04 invoke Treelint-enabled subagents for semantic code analysis (40-80% token reduction). Automatic fallback to Grep when unavailable.

**Reference:** `references/treelint-integration.md` and `.claude/agents/references/treelint-search-patterns.md`

---

## Reference Files

### Phase Execution (phases/ directory)

| File | Phase |
|------|-------|
| phase-01-preflight.md | Pre-Flight Validation |
| phase-02-test-first.md | Test-First (TDD Red) |
| phase-03-implementation.md | Implementation (TDD Green) |
| phase-04-refactoring.md | Refactoring + Light QA |
| phase-04.5-ac-verification.md | AC Verification (Post-Refactor) |
| phase-05-integration.md | Integration Testing |
| phase-05.5-ac-verification.md | AC Verification (Post-Integration) |
| phase-06-deferral.md | Deferral Challenge |
| phase-07-dod-update.md | DoD Update |
| phase-08-git-workflow.md | Git Workflow |
| phase-09-feedback.md | Feedback Hook |
| phase-10-result.md | Result Interpretation |

### Supporting References (references/ directory)

| File | Purpose |
|------|---------|
| parameter-extraction.md | Story ID extraction algorithm |
| preflight-validation.md | Phase 01 detailed workflow |
| tdd-red-phase.md | Phase 02 detailed workflow |
| test-integrity-snapshot.md | Red-phase test checksum snapshot (STORY-502) |
| tdd-green-phase.md | Phase 03 detailed workflow |
| tdd-refactor-phase.md | Phase 04 detailed workflow |
| ac-verification-workflow.md | AC Verification for Phase 4.5/5.5 |
| ac-checklist-update-workflow.md | AC checklist update procedures |
| integration-testing.md | Phase 05 detailed workflow |
| phase-06-deferral-challenge.md | Phase 06 detailed workflow |
| dod-update-workflow.md | Phase 07 detailed workflow |
| git-workflow-conventions.md | Phase 08 detailed workflow |
| tdd-patterns.md | Comprehensive TDD guidance |
| qa-remediation-workflow.md | Remediation mode workflow |
| resume-detection.md | Resume workflow detection and pre-flight (STORY-459) |
| observation-capture.md | Inline observation schema (STORY-400) |
| workflow-deviation-protocol.md | Deviation consent protocol (RCA-019) |
| pre-phase-planning.md | Optional pre-phase planning (STORY-FEEDBACK-005) |
| phase-transition-validation.md | CLI validation call reference (STORY-153) |
| memory-file-schema.md | Memory file YAML schema (STORY-303) |
| memory-file-operations.md | Memory file read/write operations (STORY-303) |
| ambiguity-protocol.md | When to ask user questions |
| treelint-integration.md | Treelint AST-aware search setup and fallback |
| treelint-daemon-lifecycle.md | Treelint daemon start/stop management |
| treelint-dependency-query.md | Treelint dependency query patterns |
| treelint-repository-map.md | Treelint repository map generation |
