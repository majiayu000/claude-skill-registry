---
name: spec-driven-w3-compliance
description: >
  W3 compliance scanning with structural anti-skip enforcement. Detects auto-skill
  chaining violations (skills/commands that auto-invoke other skills without user approval)
  using the Execute-Verify-Record pattern at every step. Designed to prevent token
  optimization bias through lean orchestration and binary CLI gate enforcement. Scans
  subagent files, skill files, and command files for unauthorized Skill() invocations.
  Use when auditing W3 compliance, checking for auto-skill chaining violations, or
  preparing for release validation. Always use this skill when the user runs /audit-w3
  or mentions W3 compliance, skill chaining, or auto-invocation scanning.
allowed-tools:
  - Read
  - Glob
  - Grep
  - AskUserQuestion
  - Bash(devforgeai-validate:*)
model: opus
effort: High
---

# Spec-Driven W3 Compliance

Scan for W3 violations (auto-skill chaining without user control) through strict 4-phase workflow with structural anti-skip enforcement.

**W3 Definition:** Skills/commands that auto-invoke other skills without user approval, causing token overflow and violating lean orchestration principles.

**Reference:** BRAINSTORM-001 (line 85), STORY-135, ADR-020

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

1. **Fresh-context reference loading** - References loaded fresh from disk each phase, never from memory
2. **Binary CLI gates** - `devforgeai-validate phase-check/phase-complete/phase-record` (compiled Rust, cannot be forged by LLM)
3. **Hook enforcement** - Shell scripts in `.claude/hooks/` run outside LLM control
4. **Step registry + artifact verification** - `.claude/hooks/phase-steps-registry.json` tracks every mandatory step

**Execute-Verify-Record Pattern:** Every mandatory step in every phase file has three parts:
- **EXECUTE:** The exact action to perform
- **VERIFY:** How to confirm the action happened (Glob, Grep, exit code, variable state)
- **RECORD:** CLI command to record completion (`devforgeai-validate phase-record`)

**Token Optimization Bias is PROHIBITED.** Do not skip, compress, or shortcut any step. Every phase step exists because a previous failure proved it necessary. (Reference: RCA-001, RCA-002)

---

## Parameter Extraction

Extract scan parameters from command context markers set by `/audit-w3`:

| Context Marker | Set By | Default | Description |
|----------------|--------|---------|-------------|
| `$MODE` | /audit-w3 | `"normal"` | Scan mode (normal/verbose) |
| `$QUIET` | /audit-w3 | `false` | Suppress detailed output |
| `$FIX_HINTS` | /audit-w3 | `false` | Show remediation patterns |

If context markers are not found, use defaults.

---

## Phase State Initialization [MANDATORY FIRST]

```bash
devforgeai-validate phase-init W3-AUDIT --workflow=w3-compliance --project-root=.
```

| Exit Code | Meaning | Action |
|-----------|---------|--------|
| 0 | New workflow | State file created. Set CURRENT_PHASE = "01". |
| 1 | Existing workflow | Resume from last completed phase. |
| 2 | Invalid ID | HALT. |
| 127 | CLI not installed | Continue without enforcement (backward compatibility). |

---

## Phase Orchestration Loop

```
FOR phase_num in [01, 02, 03, 04]:
    phase_id = phase_num

    1. ENTRY GATE: devforgeai-validate phase-check W3-AUDIT --workflow=w3-compliance --from={prev} --to={phase_id} --project-root=.
       IF exit != 0: HALT

    2. LOAD: Read(file_path="src/claude/skills/spec-driven-w3-compliance/phases/{phase_files[phase_id]}")

    3. EXECUTE: Follow every step in the phase file (EXECUTE-VERIFY-RECORD triplets)
       - Each step's EXECUTE instruction tells you exactly what to do
       - Each step's VERIFY instruction tells you how to confirm it happened
       - Each step's RECORD instruction tells you what CLI command to call

    4. RECORD: devforgeai-validate phase-record W3-AUDIT --workflow=w3-compliance --phase={phase_id} --project-root=.

    5. EXIT GATE: devforgeai-validate phase-complete W3-AUDIT --workflow=w3-compliance --phase={phase_id} --checkpoint-passed --project-root=.
       IF exit != 0: HALT
```

| Phase | Name | File |
|-------|------|------|
| 01 | Setup | `phases/phase-01-setup.md` |
| 02 | Scanning | `phases/phase-02-scanning.md` |
| 03 | Reporting | `phases/phase-03-reporting.md` |
| 04 | Completion | `phases/phase-04-completion.md` |

---

## Required Subagents Per Phase

| Phase | Required Subagents | Enforcement |
|-------|-------------------|-------------|
| 01 | (none) | N/A |
| 02 | (none) | N/A |
| 03 | (none) | N/A |
| 04 | (none) | N/A |

This skill is read-only scanning. No subagents are required.

**Deviation Protocol:** Any skip requires explicit user consent via AskUserQuestion.

---

## Workflow Completion Validation

```
IF completed_count < 4: HALT "WORKFLOW INCOMPLETE - {completed_count}/4 phases"
IF completed_count == 4: "All 4 phases completed - W3 compliance audit passed"
```

---

## Success Criteria

- Detects subagent Skill() invocations (CRITICAL)
- Detects non-orchestration skill auto-chaining (HIGH)
- Flags missing W3 compliance documentation (MEDIUM)
- Identifies auto-invoke language patterns (INFO)
- Excludes legitimate orchestration and backup files
- CRITICAL violations return exit code 1
- Quiet mode works for release integration
- Report format matches other audit commands

---

## Reference Files Index

**Local references** (loaded per-phase on demand, NOT consolidated):

| Phase | Reference Files (load via Read from src/claude/skills/spec-driven-w3-compliance/references/) |
|-------|-------------------------------------------------------------------------------------------|
| 01 | (none -- setup uses inline logic) |
| 02 | `scanning-patterns.md`, `w3-rules.md` |
| 03 | `report-templates.md`, `w3-rules.md` |
| 04 | (none -- completion uses inline logic) |

---

## Integration Notes

**Invoked by:** /audit-w3 command
**Invokes:** None (read-only scanning)
**Output:** Display report to user, exit code for CI/CD
**W3 Compliance:** This skill does NOT auto-invoke other skills.
