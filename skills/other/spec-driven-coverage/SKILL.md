---
name: spec-driven-coverage
description: >
  Validate epic-to-story coverage with gap detection and batch story creation using
  structural anti-skip enforcement. Implements 6 phases of the DevForgeAI coverage
  workflow using the Execute-Verify-Gate pattern at every step. Designed to prevent
  token optimization bias through lean orchestration, fresh-context subagent delegation,
  and binary CLI gate enforcement. Detects coverage gaps between epics and stories,
  generates visual coverage reports, and orchestrates batch story creation with failure
  isolation. Use when validating epic coverage, detecting story gaps, or batch-creating
  stories for uncovered features. Always use this skill when the user runs
  /validate-epic-coverage or /create-missing-stories.
allowed-tools:
  - Read
  - Glob
  - Grep
  - AskUserQuestion
  - Task
  - Bash(devforgeai/traceability/gap-detector.sh:*)
  - Bash(devforgeai/epic-coverage/generate-report.sh:*)
  - Bash(devforgeai-validate:*)
  - Skill
model: opus
effort: Medium
---

# Spec-Driven Coverage Validation

Validate epic-to-story coverage gaps and orchestrate batch story creation through a strict 6-phase workflow with structural anti-skip enforcement.

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
- [ ] Skipping a phase because "it seems simple"
- [ ] Summarizing instead of loading a reference file

**IF any box checked:** EXECUTION MODEL VIOLATION. Go directly to Phase State Initialization now.

---

## Anti-Skip Enforcement Contract

This skill enforces 4 independent anti-skip layers. ALL FOUR must fail for a step to be skipped:

1. **Per-phase reference loading** — Each phase loads its reference files FRESH via Read() (not consolidated from memory)
2. **Binary CLI gates** — `devforgeai-validate phase-check/phase-complete/phase-record` (compiled binary, cannot be forged by LLM)
3. **Checkpoint-based state tracking** — Phase state JSON tracks current_phase, phases_completed, active_phases
4. **Artifact verification** — Phase state file verified via Glob(), outputs verified on disk via Grep()

**Execute-Verify-Gate Pattern:** Every mandatory step in every phase file has three parts:
- **EXECUTE:** The exact action to perform (Read, Glob, Grep, Bash, Task, Skill)
- **VERIFY:** How to confirm the action happened (file exists, content matches, exit code, data key populated)
- **RECORD:** CLI command to record completion (`devforgeai-validate phase-record`)

**Token Optimization Bias is PROHIBITED.** Do not skip, compress, or shortcut any step. Every phase step exists because a previous failure proved it necessary. (Reference: RCA-001, RCA-002, STORY-457)

---

## Validation Modes

Three modes determine which phases execute. The mode is set by the invoking command via context markers.

| Mode | Phases Executed | Purpose |
|------|----------------|---------|
| `validate` | 00 → 01 → 02 → 03 | Gap detection + coverage report + display formatting |
| `detect` | 00 → 01 | Gap detection only, return structured data |
| `create` | 00 → 01 → 04 → 05 | Batch story creation from gaps + completion summary |

---

## Phase State Initialization

Before any phase executes, initialize phase state tracking.

**EXECUTE:**
```
Bash(command="devforgeai-validate phase-init ${IDENTIFIER} --workflow=coverage --project-root=. 2>&1")
```

Where `${IDENTIFIER}` is `${EPIC_ID}` (e.g., `EPIC-015`) or `COVERAGE-ALL` for all-epics mode.

**VERIFY:** Exit code 0 or 2 (exit code 2 = identifier format not recognized, proceed with backward compatibility).

**If exit code 127:** CLI not installed. Continue without CLI gates but execute ALL phases and steps regardless.

---

## Phase Orchestration

Determine active phases from the mode, then execute each in sequence:

```
active_phases = MODE_ROUTES[mode]
  validate: ["00", "01", "02", "03"]
  detect:   ["00", "01"]
  create:   ["00", "01", "04", "05"]

FOR phase_num in active_phases:
  1. ENTRY GATE: Verify previous phase completed (check phase state or first phase)
  2. LOAD: Read(file_path="src/claude/skills/spec-driven-coverage/phases/phase-{phase_num}-{name}.md")
     - If Read fails, try: Read(file_path=".claude/skills/spec-driven-coverage/phases/phase-{phase_num}-{name}.md")
  3. EXECUTE: Follow ALL EVG triplets in the phase file — no skipping
  4. RECORD: devforgeai-validate phase-record ${IDENTIFIER} --phase={phase_num} --project-root=. 2>&1
  5. EXIT GATE: Verify phase artifacts exist before proceeding
```

**CRITICAL:** Execute EVERY step in EVERY active phase. The mode router only controls WHICH phases run — within each phase, ALL steps are mandatory.

---

## Phase Index

| Phase | File | Name | Required Subagents |
|-------|------|------|--------------------|
| 00 | `phases/phase-00-initialization.md` | Initialization | None |
| 01 | `phases/phase-01-gap-detection.md` | Gap Detection | None |
| 02 | `phases/phase-02-coverage-report.md` | Coverage Report | None |
| 03 | `phases/phase-03-display-formatting.md` | Display Formatting | epic-coverage-result-interpreter |
| 04 | `phases/phase-04-batch-creation.md` | Batch Story Creation | None (delegates to spec-driven-stories) |
| 05 | `phases/phase-05-completion-summary.md` | Completion Summary | epic-coverage-result-interpreter |

---

## Command Integration

This skill is invoked by two commands with context markers:

### /validate-epic-coverage context markers:
```
**Epic ID:** ${EPIC_ID} (or "all")
**Mode:** validate
**Prompt Mode:** interactive | quiet | ci
```

### /create-missing-stories context markers:
```
**Epic ID:** ${EPIC_ID}
**Mode:** detect (first invocation) OR create (second invocation)
**Sprint:** ${SPRINT}
**Priority:** ${PRIORITY}
**Points:** ${POINTS}
**Individual Priority:** true | false
**Individual Points:** true | false
**Batch Mode:** true
**Batch Total:** ${gap_count}
**Created From:** /create-missing-stories
```

---

## Business Rules

| ID | Rule | Enforcement Phase | Reference |
|----|------|-------------------|-----------|
| BR-001 | Epic ID: case-insensitive, normalized to EPIC-NNN | Phase 00 | `references/business-rules.md` |
| BR-002 | Coverage: only stories with status >= Dev Complete count | Phase 01 | `references/business-rules.md` |
| BR-003 | Shell-safe escaping for feature descriptions in commands | Phase 03 | `references/business-rules.md` |
| BR-004 | Batch failure isolation: item N failure does not affect item N+1 | Phase 04 | `references/business-rules.md` |

---

## Performance Targets

- Single epic validation: < 500ms
- All epics (20 epics, 200 stories): < 3 seconds
- Batch story creation: ~3 seconds per story
- Batch of 10 stories: < 30 seconds total

---

## Reference Files Index

Each phase loads only its required references. No consolidated loading.

| Reference | Loaded By | Purpose |
|-----------|-----------|---------|
| `references/shared-protocols.md` | Phase 00 | EVG pattern documentation, self-check violations |
| `references/parameter-extraction.md` | Phase 00 | Context marker extraction rules |
| `references/business-rules.md` | Phase 00, 01, 03, 04 | BR-001 through BR-004 definitions |
| `references/gap-detector-integration.md` | Phase 01 | Shell script invocation documentation |
| `references/story-quality-gates.md` | Phase 04 | RCA-020 evidence verification requirements |

---

## Success Criteria

| Mode | Success Condition |
|------|-------------------|
| `validate` | Gap data collected, coverage report generated, display formatted via subagent |
| `detect` | Structured gap data returned (JSON-compatible object with total_features, covered_features, missing_features, coverage_percentage) |
| `create` | All gaps processed (success or isolated failure), completion summary displayed |

---

## Change Log

| Date | Story | Change |
|------|-------|--------|
| 2026-03-18 | — | Created — migrated from validating-epic-coverage with EVG anti-skip enforcement |
| 2026-02-20 | STORY-457 | Original skill created (validating-epic-coverage) |

---

**Created:** 2026-03-18
**Migrated from:** validating-epic-coverage (STORY-457)
**Pattern:** Spec-driven skill with Execute-Verify-Gate anti-skip enforcement
**Predecessor ADR:** ADR-020 (Structural Changes Authorization)
