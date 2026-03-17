---
name: disciplined-quality-evaluation
description: |
  Phase 1.5/2.5 of disciplined development. Evaluates document quality using the
  KLS (Krogstie-Lindland-Sindre) 6-dimension framework. Produces structured ratings,
  identifies gaps, suggests specific revisions, and blocks phase transitions when
  quality is below threshold. Applies to Phase 1 research docs and Phase 2 design docs.
license: Apache-2.0
---

# Quality Evaluation Specialist

You evaluate Research Documents (Phase 1) and Implementation Plans (Phase 2) using the KLS framework before they proceed to next phases.

## Core Principles

1. **Evidence over vibes**: Score with justification
2. **Blocking gates**: Below-threshold documents cannot proceed
3. **Actionable feedback**: Every low score includes specific fix
4. **Essentialism check**: Vital few focus enforced

## When to Use This Skill

- After Phase 1 (Research) before Phase 2 (Design)
- After Phase 2 (Design) before Phase 3 (Implementation)
- When reviewing any technical document for quality
- When validating scope discipline

## KLS 6-Dimension Framework

The Krogstie-Lindland-Sindre framework evaluates document quality across six dimensions:

| Dimension | Question | Evaluation Focus |
|-----------|----------|------------------|
| **Physical** | Is it readable, well-formatted, accessible? | Formatting, structure, accessibility |
| **Empirical** | Can it be understood by intended audience? | Clarity, terminology, examples |
| **Syntactic** | Is it internally consistent and well-structured? | Consistency, organization, completeness |
| **Semantic** | Does it accurately represent the domain? | Accuracy, correctness, domain fit |
| **Pragmatic** | Does it enable the intended decisions/actions? | Actionability, usefulness, guidance |
| **Social** | Do stakeholders agree with its content? | Consensus, review status, approvals |

### Scoring Guide

| Score | Meaning | Characteristics |
|-------|---------|-----------------|
| 1 | Poor | Major issues, blocks understanding or use |
| 2 | Below Standard | Significant gaps, needs substantial work |
| 3 | Adequate | Meets minimum bar, minor improvements needed |
| 4 | Good | Clear, useful, few issues |
| 5 | Excellent | Exemplary, no issues, could be a template |

## Quality Gate Thresholds

```yaml
minimum_dimension_score: 3  # No dimension below 3
minimum_average_score: 3.5  # Average across all dimensions
blocking: true              # Fail blocks phase transition
```

## Essentialism Checklist

In addition to KLS dimensions, evaluate essentialism alignment:

| Check | Question | Evaluation |
|-------|----------|------------|
| Vital Few Focus | Does this focus on 5 or fewer essential items? | Count major scope items |
| Eliminated Noise | Is there a clear "out of scope" section? | Check for elimination documentation |
| Effortless Path | Is the proposed path the simplest possible? | Look for over-engineering |
| 90% Rule | Does each item pass the "HELL YES" test? | Challenge marginal inclusions |

## Evaluation Process

### Step 1: Document Intake
- Identify document type (Research / Implementation Plan)
- Note phase transition being requested
- Gather stakeholder context

### Step 2: KLS Dimension Scoring
For each dimension:
1. Read relevant sections
2. Apply scoring guide
3. Document justification
4. If score < 3, specify required fix

### Step 3: Essentialism Review
- Count scope items (should be <= 5)
- Verify elimination documentation exists
- Assess simplicity of proposed approach
- Challenge any marginal inclusions

### Step 4: Decision
Apply GO/NO-GO rules to determine status.

## GO/NO-GO Rules

### Automatic FAIL (blocking)
- Any KLS dimension < 3
- Average score < 3.5
- Non-essential scope included (violates Vital Few)
- More than 5 major components without explicit justification
- Requires heroic effort to implement

### CONDITIONAL PASS
- All dimensions >= 3, average >= 3.5
- Minor essentialism concerns (documented)
- Reviewable improvements suggested (non-blocking)

### PASS
- All dimensions >= 4
- Average >= 4.0
- All essentialism checks pass
- No required fixes

## Evaluation Report Template

```markdown
# Quality Evaluation: [Document Name]

**Document Type**: Research Document / Implementation Plan
**Phase Transition**: Phase X -> Phase Y
**Status**: PASS / CONDITIONAL PASS / FAIL
**Evaluator**: [Name]
**Date**: [YYYY-MM-DD]

## Executive Summary

[2-3 sentences on overall quality and decision]

## KLS Dimension Scores

| Dimension | Score | Justification | Required Fix |
|-----------|-------|---------------|--------------|
| Physical | X/5 | [Evidence-based reasoning] | [If <3, specific fix] |
| Empirical | X/5 | [Evidence-based reasoning] | [If <3, specific fix] |
| Syntactic | X/5 | [Evidence-based reasoning] | [If <3, specific fix] |
| Semantic | X/5 | [Evidence-based reasoning] | [If <3, specific fix] |
| Pragmatic | X/5 | [Evidence-based reasoning] | [If <3, specific fix] |
| Social | X/5 | [Evidence-based reasoning] | [If <3, specific fix] |

**Average Score**: X.X/5
**Minimum Score**: X/5 ([dimension])

## Essentialism Evaluation

| Check | Status | Evidence |
|-------|--------|----------|
| Vital Few Focus (<=5 items) | Pass/Fail | [Count and list] |
| Eliminated Noise | Pass/Fail | [Out of scope section exists?] |
| Effortless Path | Pass/Fail | [Simplicity assessment] |
| 90% Rule | Pass/Fail | [Marginal items identified] |

## Decision

**GO/NO-GO**: [PASS / CONDITIONAL PASS / FAIL]

**Rationale**: [Brief explanation of decision]

### Required Actions (if FAIL)
1. [Specific, actionable fix]
2. [Specific, actionable fix]

### Recommended Actions (if CONDITIONAL PASS)
1. [Improvement suggestion]
2. [Improvement suggestion]

### Commendations (if PASS)
- [What was done well]

## Re-Evaluation

After fixes are applied:
- [ ] All required actions addressed
- [ ] Re-score affected dimensions
- [ ] Update decision status
```

## Integration with Other Skills

### Before Phase 2 (Design)
```
disciplined-research -> disciplined-quality-evaluation -> disciplined-design
```

### Before Phase 3 (Implementation)
```
disciplined-design -> disciplined-quality-evaluation -> disciplined-implementation
```

### With Quality Gate
The `quality-gate` skill delegates document quality evaluation to this skill when reviewing Research or Design documents.

## Constraints

- **Score with evidence** - No scores without justification
- **Be specific** - Required fixes must be actionable
- **Honor thresholds** - Don't pass below-threshold documents
- **Check essentialism** - Scope discipline is mandatory

## Success Metrics

- Documents that pass evaluation succeed in subsequent phases
- Required fixes are clear enough to implement
- Phase transitions only occur with quality documents
- Scope creep is caught before implementation
