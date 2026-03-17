---
name: gpt-delegation
description: Use when blocked, stuck, or needing fresh perspective. Consults GPT experts via Codex CLI with graceful fallback.
---

# SKILL: GPT Delegation

> **Purpose**: Intelligent Codex/GPT consultation for complex problems, escalation when stuck

---

## Quick Start

### When to Use

- After 2+ failed attempts on same issue
- Architecture decisions needed
- Security concerns
- Ambiguous requirements
- Plan review for large plans (5+ SCs)
- **Proactive consultation**: Before asking user when confidence < 0.5 (see rubric below)

### Quick Reference

```bash
# Graceful fallback + delegation (see CRITICAL WARNING below for valid parameters)
if ! command -v codex &> /dev/null; then
  echo "Warning: Codex CLI not installed - falling back to Claude-only analysis"
  return 0
fi
codex exec -m gpt-5.2 -s workspace-write -c reasoning_effort=medium --json "TASK: [goal]
EXPECTED: [outcome], CONTEXT: [attempts, errors, iteration], MUST: Analyze failures, fresh approach, report files"
```

## Core Concepts

### Graceful Fallback (CRITICAL)

**MANDATORY**: All GPT delegation points MUST include graceful fallback.

```bash
if ! command -v codex &> /dev/null; then
  echo "Warning: Codex CLI not installed - falling back to Claude-only analysis"
  return 0  # NOT an error, continue with Claude
fi
```

**Key Points**:
- Graceful fallback is **NOT** an error
- Log warning message
- Return success (exit 0) to allow continuation
- Continue with Claude agents

### CRITICAL WARNING: Codex CLI Parameters (READ CAREFULLY)

**MANDATORY: Use EXACT values below - NO variations allowed**

**Valid -s modes**: `read-only` | `workspace-write` | `danger-full-access`
**FORBIDDEN**: `workspace-read`, `read-write`, `write` (Claude often creates invalid combinations)
**Valid -c value**: `reasoning_effort=medium` ONLY (NOT high/low)
**Required**: `-m gpt-5.2 --json "PROMPT"`

### Delegation Triggers

| Trigger | Expert | Mode | When to Delegate |
|---------|--------|------|------------------|
| 2+ failed attempts | Architect | workspace-write | Progressive escalation |
| Stuck on task | Architect | workspace-write | Fresh perspective |
| Architecture decision | Architect | read-only | Design guidance |
| Security concern | Security Analyst | read-only | Vulnerability assessment |
| Ambiguous plan | Scope Analyst | read-only | Requirements clarification |
| Large plan (5+ SCs) | Plan Reviewer | read-only | Plan validation |

### Confidence Score Rubric (Centralized)

**Formula**:
```
confidence = 1.0 - (architecture_keywords * 0.3) - (multiple_approaches * 0.2) - (uncertainty_markers * 0.2)
```

**Scale**: 0.0 - 1.0

**Thresholds**:
- 0.9-1.0: Proceed autonomously
- 0.5-0.9: Consider consultation
- < 0.5: **MUST consult GPT** (proactive)

**Detection Patterns**:
- Architecture: architecture, tradeoff, design, scalability, pattern, choice
- Multiple approaches: could, might, option A/B, either
- Uncertainty: not sure, unclear, depends

### Progressive Escalation

**Principle**: Delegate ONLY after 2nd failure, not first

```
Attempt 1 (Claude) → Fail
     ↓
Attempt 2 (Claude) → Fail
     ↓
Attempt 3 (GPT Architect) → Success
```

## Expert Mapping

| Expert | Purpose | When | Mode | Output |
|--------|---------|------|------|--------|
| **Architect** | Fresh perspective on implementation | 2+ failures, stuck, architecture | workspace-write | Root cause, fresh approach, files modified |
| **Security Analyst** | Vulnerability assessment | Security concerns, auth, sensitive data | read-only | OWASP findings, severity, fixes |
| **Plan Reviewer** | Plan validation | 5+ SCs, complex deps, high-risk | read-only | Quality (1-10), clarity, feasibility, risks |
| **Scope Analyst** | Requirements clarification | Ambiguous requirements, edge cases | read-only | Ambiguities, assumptions, acceptance criteria |
| **Code Reviewer** | Code quality assessment | Explicit review, quality concerns | read-only | Quality issues, violations, refactoring |

## Integration Pattern

### Coder Teammate (Ralph Loop)

**Pattern**: Teammate calls GPT directly when blocked, shares results with Team Lead and other teammates via Message.

```bash
# After 2nd failure in Ralph Loop
if [ $iteration -ge 2 ] && [ $TEST_RESULT -ne 0 ]; then
  PROMPT="TASK: Fix failing test ${TEST_NAME}
  EXPECTED OUTCOME: All tests pass
  CONTEXT: Previous attempts: ${ATTEMPT_SUMMARY}, Errors: $(cat /tmp/test.log | tail -20)"
  codex exec -m gpt-5.2 -s workspace-write -c reasoning_effort=medium --json "$PROMPT"

  # Share GPT recommendations with Team Lead
  echo "Message to Team Lead: GPT Architect provided recommendations. Applying fixes..."
fi
```

**Key Points**:
- Teammate calls codex directly (no Team Lead relay needed)
- Teammate shares GPT results via Message tool
- Team Lead coordinates but doesn't implement

### /00_plan Command

```bash
# Large plan review
if [ $(echo "$PLAN" | grep -c "SC-") -ge 5 ]; then
  PROMPT="Review plan: $PLAN (Clarity, Completeness, Feasibility, Dependencies, Risks)"
  codex exec -m gpt-5.2 -s read-only -c reasoning_effort=medium --json "$PROMPT"
fi
```

## Troubleshooting

### Codex CLI Not Installed

**Symptom**: Warning message about Codex CLI not installed

**Solution**: Expected behavior. Skill gracefully falls back to Claude-only analysis.

### Delegation Not Triggering

**Causes**: 1) Trigger not met (< 2 failures) 2) Skill not loaded 3) Codex check failing

**Debug**: Check `echo $iteration`, verify `grep -r "gpt-delegation" .claude/skills/`, test `command -v codex`

### GPT Returns Same Approach

**Solution**: Document previous attempts clearly with errors and stack traces.

## Best Practices

- **Always include graceful fallback**: Codex CLI may not be installed
- **Document previous attempts clearly**: Include errors, stack traces, code snippets
- **Specify expected outcome**: What does success look like?
- **Use appropriate mode**: workspace-write for code changes, read-only for analysis
- **Parse output carefully**: GPT output format may vary
- **Verify suggestions**: Don't blindly apply GPT recommendations

## Further Reading

**Internal**: @.claude/skills/gpt-delegation/REFERENCE.md - Complete prompt templates, integration examples, troubleshooting | @.claude/skills/ralph-loop/SKILL.md - Ralph Loop integration with GPT delegation

**External**: [Codex Documentation](https://github.com/example/codex)
