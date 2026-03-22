---
name: spec-driven-qa
description: >
  Validates code quality through spec-driven QA validation with structural anti-skip
  enforcement. Replicates all 6 phases of the DevForgeAI QA workflow using the
  Execute-Verify-Gate pattern at every step. Designed to prevent token optimization
  bias through lean orchestration, fresh-context subagent delegation, and binary CLI
  gate enforcement. Enforces test coverage (95%/85%/80% strict thresholds), detects
  anti-patterns, validates spec compliance, and analyzes code quality metrics. Use when
  validating implementations, ensuring quality standards, or preparing for release.
  Always use this skill when the user runs /qa or mentions QA validation, quality checks,
  or coverage analysis.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
  - Task
  - Bash(devforgeai-validate:*)
  - Bash(git:*)
  - Bash(pytest:*)
  - Bash(dotnet:*)
  - Bash(cargo:*)
  - Bash(npm:*)
  - Bash(python:*)
  - Bash(radon:*)
  - Bash(npx:*)
  - Bash(mvn:*)
  - Bash(go:*)
  - Skill
model: opus
effort: High
---

# Spec-Driven QA Validation

Validate story implementations through strict 6-phase QA workflow while enforcing coverage thresholds, anti-pattern detection, and spec compliance.

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
2. **Binary CLI gates** - `devforgeai-validate phase-check/phase-complete/phase-record` (compiled Rust, cannot be forged by LLM)
3. **Hook enforcement** - Shell scripts in `.claude/hooks/` run outside LLM control
4. **Step registry + artifact verification** - `.claude/hooks/phase-steps-registry.json` tracks every mandatory step

**Execute-Verify-Gate Pattern:** Every mandatory step in every phase file has three parts:
- **EXECUTE:** The exact action to perform
- **VERIFY:** How to confirm the action happened (Glob, Grep, exit code, Task result)
- **RECORD:** CLI command to record completion (`devforgeai-validate phase-record`)

**Token Optimization Bias is PROHIBITED.** Do not skip, compress, or shortcut any step. Every phase step exists because a previous failure proved it necessary. (Reference: RCA-001, RCA-002)

---

## Validation Modes

### Light (~10K tokens, 2-3 min)
- Build/syntax checks
- Test execution (100% pass required)
- Critical anti-patterns only
- Deferral validation (if deferrals exist)

### Deep (~35K tokens, 8-12 min)
- Complete coverage analysis (95%/85%/80% thresholds -- ADR-010, non-negotiable)
- Comprehensive anti-pattern detection
- Full spec compliance (AC, API, NFRs)
- Code quality metrics
- Security scanning (OWASP Top 10)
- Deferral validation (if deferrals exist)

---

## Parameter Extraction

Extract story ID and mode from conversation context. See `.claude/skills/spec-driven-qa/references/parameter-extraction.md` for the extraction algorithm.

Extraction methods: YAML frontmatter, file reference, explicit statement, status inference.
Default mode: deep (if unable to determine).

## Command Integration

| Context Marker | Set By | Description |
|----------------|--------|-------------|
| `$STORY_ID` | /qa | Story identifier (STORY-NNN) |
| `$MODE` | /qa | Validation mode (light/deep/auto) |

---

## Phase State Initialization [MANDATORY FIRST]

```bash
devforgeai-validate phase-init ${STORY_ID} --workflow=qa --project-root=.
```

| Exit Code | Meaning | Action |
|-----------|---------|--------|
| 0 | New workflow | State file created. Set CURRENT_PHASE = "01". |
| 1 | Existing workflow | Resume. Run `devforgeai-validate phase-status ${STORY_ID} --workflow=qa` to get CURRENT_PHASE. |
| 2 | Invalid story ID | HALT. Must match STORY-XXX pattern. |
| 127 | CLI not installed | Continue without enforcement (backward compatibility). |

---

## Phase Orchestration Loop

```
FOR phase_num in [01, 02, 03, 04, 05, 06]:
    phase_id = phase_num

    1. ENTRY GATE: devforgeai-validate phase-check ${STORY_ID} --workflow=qa --from={prev} --to={phase_id} --project-root=.
       IF exit != 0: HALT

    2. LOAD: Read(file_path=".claude/skills/spec-driven-qa/phases/{phase_files[phase_id]}")

    3. EXECUTE: Follow every step in the phase file (EXECUTE-VERIFY-GATE triplets)
       - Each step's EXECUTE instruction tells you exactly what to do
       - Each step's VERIFY instruction tells you how to confirm it happened
       - Each step's RECORD instruction tells you what CLI command to call

    4. RECORD: devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase={phase_id} --project-root=.

    5. EXIT GATE: devforgeai-validate phase-complete ${STORY_ID} --workflow=qa --phase={phase_id} --checkpoint-passed --project-root=.
       IF exit != 0: HALT
```

| Phase | Name | File |
|-------|------|------|
| 01 | Setup | `phases/phase-01-setup.md` |
| 02 | Validation | `phases/phase-02-validation.md` |
| 03 | Diff Regression Detection | `phases/phase-03-diff-regression.md` |
| 04 | Analysis | `phases/phase-04-analysis.md` |
| 05 | Reporting | `phases/phase-05-reporting.md` |
| 06 | Cleanup | `phases/phase-06-cleanup.md` |

---

## Required Subagents Per Phase

| Phase | Required Subagents | Enforcement |
|-------|-------------------|-------------|
| 01 | (none) | N/A |
| 02 | (none) | N/A |
| 03 | (none) | N/A |
| 04 | anti-pattern-scanner, test-automator, code-reviewer, security-auditor | BLOCKING (adaptive per story type) |
| 04 | deferral-validator (if deferrals) | CONDITIONAL |
| 04 | diagnostic-analyst (if failures) | CONDITIONAL |
| 05 | qa-result-interpreter | BLOCKING |
| 06 | (none) | N/A |

**Deviation Protocol:** Any skip requires explicit user consent via AskUserQuestion.

---

## Definition of Done Protocol

Deferral validation CANNOT be skipped (RCA-007). Deferred DoD items require user approval, story/ADR references, and deferral-validator subagent validation.

Load protocol details when needed:
```
Read(file_path=".claude/skills/spec-driven-qa/references/dod-protocol.md")
```

---

## State Persistence

**Location:** `devforgeai/workflows/${STORY_ID}-qa-phase-state.json`

---

## Workflow Completion Validation

```
IF completed_count < 6: HALT "WORKFLOW INCOMPLETE - {completed_count}/6 phases"
IF completed_count == 6: "All 6 phases completed - QA workflow validation passed"
```

---

## Success Criteria

**Light:** Build passes, tests pass, no CRITICAL, deferrals valid, <10K tokens
**Deep:** Coverage thresholds met, no CRITICAL/HIGH, spec compliant, quality acceptable, deferrals valid, status="QA Approved", <35K tokens

---

## Reference Files Index

**Local references** (loaded per-phase on demand, NOT consolidated):

| Phase | Reference Files (load via Read from .claude/skills/spec-driven-qa/references/) |
|-------|-----------------------------------------------------------------------------|
| 01 | `parameter-extraction.md`, `phase-0-setup-workflow.md`, `test-isolation-service.md`, `parallel-validation.md` |
| 02 | `traceability-validation-algorithm.md`, `coverage-analysis.md` |
| 03 | `diff-regression-detection.md`, `test-tampering-heuristics.md` |
| 04 | `anti-pattern-detection.md`, `parallel-validation.md`, `spec-compliance-validation.md`, `code-quality-workflow.md`, `dod-protocol.md` |
| 05 | `qa-result-formatting-guide.md`, `phase-3-reporting-workflow.md`, `story-update-workflow.md` |
| 06 | `phase-4-cleanup-workflow.md`, `feedback-hooks-workflow.md` |

**Assets:**
- `.claude/skills/spec-driven-qa/assets/config/coverage-thresholds.md`
- `.claude/skills/spec-driven-qa/assets/language-smoke-tests.yaml`
- `.claude/skills/spec-driven-qa/assets/templates/qa-report-template.md`
- `.claude/skills/spec-driven-qa/assets/traceability-report-template.md`

**Automation Scripts:**
- `.claude/skills/spec-driven-qa/scripts/generate_coverage_report.py`
- `.claude/skills/spec-driven-qa/scripts/detect_duplicates.py`
- `.claude/skills/spec-driven-qa/scripts/analyze_complexity.py`
- `.claude/skills/spec-driven-qa/scripts/security_scan.py`
- `.claude/skills/spec-driven-qa/scripts/validate_spec_compliance.py`
- `.claude/skills/spec-driven-qa/scripts/generate_test_stubs.py`
