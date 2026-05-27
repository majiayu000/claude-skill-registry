---
name: dialogue-assess-framing
description: Assess problem framing quality before proceeding with implementation. Captures whether the problem is well-defined per Naur's theory-building principles. Triggers on "assess framing", "check problem framing", "framing assessment", "is the problem well-defined".
allowed-tools: Bash, AskUserQuestion
---

# Dialogue: Problem Framing Assessment

Assess whether a problem is sufficiently well-framed to proceed with implementation. This is a foundational checkpoint that validates understanding before committing to a solution approach.

## Framework Grounding

This skill operationalises:
- **Naur (1985)**: Theory-building—the problem must be understood before solutions are meaningful
- **Phase transitions**: Quality of Phase 1→2 transition depends on problem clarity
- **STS Theory**: Shared understanding is prerequisite for effective collaboration

## Why This Matters

Proceeding with unclear problem framing leads to:
- Wasted effort on wrong solutions
- Scope creep from undefined boundaries
- Unvalidated assumptions causing rework
- Stakeholder misalignment discovered late

**The framework strongly encourages completing this assessment before Phase 2 work.**

## When to Use

Use this skill:
- Before starting implementation work on a new feature/task
- At Phase 1→2 transition points
- When revisiting scope after significant requirement changes
- As input to phase readiness assessment (`dialogue-assess-phase`)

## Problem Framing Checklist

The assessment covers 6 foundational elements:

| Element | Question | Why It Matters |
|---------|----------|----------------|
| `problem_stated` | Is the problem explicitly stated? | Can't solve what isn't named |
| `scope_bounded` | Are scope boundaries defined? | Prevents creep, enables estimation |
| `success_criteria` | Are success criteria measurable? | Defines "done", enables validation |
| `constraints_identified` | Are constraints documented? | Shapes solution space |
| `assumptions_explicit` | Are key assumptions stated? | Enables validation, reduces risk |
| `stakeholders_identified` | Are affected stakeholders identified? | Ensures appropriate input/review |

## How to Assess Problem Framing

### Option 1: Interactive Collection (Recommended)

Ask the user the following questions using AskUserQuestion. Frame this as a problem framing checkpoint.

For each element, ask:
1. Is the problem explicitly stated? (yes/no)
2. Are scope boundaries defined? (yes/no)
3. Are success criteria measurable? (yes/no)
4. Are constraints documented? (yes/no)
5. Are key assumptions stated? (yes/no)
6. Are affected stakeholders identified? (yes/no)

Then ask:
7. Overall confidence in problem framing (1-5)
8. Any gaps or concerns identified? (optional free text)

### Option 2: Direct Script Invocation

If you already have the responses:

```bash
${CLAUDE_PLUGIN_ROOT}/skills/dialogue-assess-framing/scripts/log-assess-framing.sh \
  <assessor> \
  <problem_stated> <scope_bounded> <success_criteria> \
  <constraints_identified> <assumptions_explicit> <stakeholders_identified> \
  <confidence> \
  [phase] [task_ref] [gaps_identified]
```

### Parameters

| Parameter | Values | Description |
|-----------|--------|-------------|
| `assessor` | `ai:claude` or `human:<id>` | Who performed the assessment |
| `problem_stated` | `true` or `false` | Problem is explicitly stated |
| `scope_bounded` | `true` or `false` | Scope boundaries are defined |
| `success_criteria` | `true` or `false` | Success criteria are measurable |
| `constraints_identified` | `true` or `false` | Constraints are documented |
| `assumptions_explicit` | `true` or `false` | Key assumptions are stated |
| `stakeholders_identified` | `true` or `false` | Affected stakeholders identified |
| `confidence` | `1-5` | Overall confidence in framing |
| `phase` | `1-7` (optional) | Current SDLC phase |
| `task_ref` | string (optional) | Task reference (e.g., "FW-023") |
| `gaps_identified` | string (optional) | Any gaps or concerns noted |
| `context` | string (optional) | Situational context |
| `tags` | string (optional) | Comma-separated categorisation tags |

## Interpreting Results

### Readiness Indicators

| True Count | Confidence | Interpretation |
|------------|------------|----------------|
| 6/6 | 4-5 | Well-framed, proceed with confidence |
| 5-6/6 | 3-4 | Mostly framed, note gaps before proceeding |
| 3-4/6 | 2-3 | Gaps present, address before major work |
| 0-2/6 | 1-2 | Poorly framed, return to problem definition |

### Critical Elements

Some elements are more critical than others:

- **problem_stated**: Foundational—if false, stop and define the problem
- **success_criteria**: Essential for knowing when you're done
- **assumptions_explicit**: High-risk if false—hidden assumptions cause rework

### Recommended Actions by Score

| Confirmed | Confidence | Recommendation | Action |
|-----------|------------|----------------|--------|
| 6/6 | 4-5 | PROCEED | Proceed to implementation |
| 5-6/6 | 3-4 | PROCEED_WITH_CAUTION | Document gaps, proceed with caution |
| 4-6/6 | 2-3 | ADDRESS_GAPS | Address gaps before significant work |
| <4/6 | <2 | RETURN_TO_DEFINITION | Return to problem definition phase |

**Note**: Both confirmed count AND confidence must meet thresholds.

## Example Interactive Flow

```
AI: Before we proceed with implementation, let me run a problem framing check.
    This ensures we have a solid foundation.

[Uses AskUserQuestion with the 6 checklist items + confidence + gaps]

AI: Thanks! Let me log that assessment.

[Invokes log-assess-framing.sh with collected responses]

AI: Problem framing assessment logged as ASSESS-20260122-143000.
    Score: 5/6 elements confirmed, confidence 4/5
    Gap: Constraints not yet documented

    Recommendation: Document known constraints before proceeding.
    This is a minor gap—you can proceed with caution while addressing it.
```

## Example Direct Invocation

```bash
${CLAUDE_PLUGIN_ROOT}/skills/dialogue-assess-framing/scripts/log-assess-framing.sh \
  "human:pidster" \
  true true true false true true \
  4 \
  2 \
  "FW-023" \
  "Constraints around performance requirements not yet documented"
```

## Output

The script returns the generated assessment ID (e.g., `ASSESS-20260122-143000`).

The assessment is stored in `.dialogue/logs/assessments/` and creates:
- Assessment YAML file
- Context graph node (ARTIFACT with artifact_type: ASSESSMENT)
- CREATED edge from assessor to assessment
- ASSESSES edge to task (if task_ref provided)

## Integration with Phase Readiness

This assessment is a key input to `dialogue-assess-phase`. When assessing phase readiness:
- If no problem framing assessment exists, the phase readiness skill will flag this
- Recent framing assessments (within current phase) are considered
- Low framing scores reduce overall phase readiness

## Schema Reference

See [Assessment Schema](../dialogue-daily-check/schema.md) for the complete PROBLEM_FRAMING response schema and validation rules.
