---
name: quality-audit
description: >-
  Meta-skill for auditing and validating skill quality. Use when reviewing
  skills for consistency, completeness, accuracy, and adherence to standards.
  Provides structured rubrics, scoring frameworks, and actionable recommendations.
author: cortex team
version: 1.0.0
license: MIT
tags: [meta, quality, validation, review, standards]
created: 2026-01-05
updated: 2026-01-05
triggers:
  - audit skill
  - review skill quality
  - validate skill
  - skill quality check
  - rubric assessment
dependencies:
  skills: []
  tools: []
token_estimate: ~2000
---

# Quality Audit Skill

Systematic framework for evaluating skill quality across four dimensions: **Clarity**, **Completeness**, **Accuracy**, and **Usefulness**.

## When to Use This Skill

- Reviewing a new skill before adding to the registry
- Auditing existing skills for quality improvements
- Creating quality rubrics for skill validation
- Standardizing skill quality across the library
- Preparing skills for production use

## Core Principles

### The Four Quality Dimensions

| Dimension | Weight | Focus |
|-----------|--------|-------|
| **Clarity** | 25% | Structure, readability, progressive disclosure |
| **Completeness** | 25% | Coverage, examples, edge cases, anti-patterns |
| **Accuracy** | 30% | Correctness, best practices, security |
| **Usefulness** | 20% | Real-world applicability, production-readiness |

### Scoring Scale (1-5)

| Score | Label | Meaning |
|-------|-------|---------|
| 1 | Unacceptable | Fundamentally broken, dangerous, or unusable |
| 2 | Needs Work | Major issues requiring significant revision |
| 3 | Acceptable | Meets minimum standards, functional |
| 4 | Good | High quality, minor improvements possible |
| 5 | Excellent | Exemplary, production-ready, best-in-class |

### Passing Criteria

- **Minimum**: 3.0 weighted average (acceptable)
- **Target**: 4.0 weighted average (good)
- **Exceptional**: 4.5+ weighted average (excellent)
- **Blocking**: Accuracy must be ≥3.0 (no dangerous advice)

## Audit Workflow

### Phase 1: Structure Check

```yaml
checklist:
  structure:
    - [ ] Has valid YAML frontmatter
    - [ ] Contains required metadata (name, description)
    - [ ] Follows progressive disclosure (Tier 1 → 2 → 3)
    - [ ] Sections are logically ordered
    - [ ] Token estimate is reasonable (<5000 for core)
```

### Phase 2: Content Evaluation

```yaml
checklist:
  content:
    - [ ] "When to Use" section is clear
    - [ ] Core principles are well-defined
    - [ ] Code examples are complete and runnable
    - [ ] Anti-patterns are documented
    - [ ] Troubleshooting guidance exists
```

### Phase 3: Dimension Scoring

For each dimension, evaluate against specific criteria:

**Clarity Criteria:**
- Well-organized sections with logical flow
- Concise explanations without jargon overload
- Code examples are readable and well-commented
- Progressive disclosure from simple to complex

**Completeness Criteria:**
- Covers core concepts thoroughly
- Includes edge cases and error handling
- Provides both do's and don'ts
- Has working examples for main use cases

**Accuracy Criteria:**
- Code examples compile/run without errors
- Follows current best practices (not deprecated)
- Security considerations are correct
- Performance claims are verifiable

**Usefulness Criteria:**
- Examples solve real-world problems
- Can be applied immediately
- Scales to production use cases
- Includes troubleshooting guidance

### Phase 4: Report Generation

```markdown
## Audit Report: {skill_name}

**Date**: {date}
**Auditor**: {auditor}
**Status**: {PASS|FAIL|NEEDS_REVIEW}

### Scores

| Dimension | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Clarity | {x}/5 | 25% | {x*0.25} |
| Completeness | {x}/5 | 25% | {x*0.25} |
| Accuracy | {x}/5 | 30% | {x*0.30} |
| Usefulness | {x}/5 | 20% | {x*0.20} |
| **Total** | | | **{sum}/5** |

### Issues Found

- [CRITICAL] {issue description}
- [MAJOR] {issue description}
- [MINOR] {issue description}

### Recommendations

1. {actionable recommendation}
2. {actionable recommendation}
```

## Implementation Patterns

### Pattern 1: Quick Audit (5-minute review)

Use for rapid assessment of skill quality:

```bash
# Run automated structure checks
cortex skills audit <skill-name> --quick

# Output: Pass/Fail with basic metrics
```

**Quick Audit Checks:**
1. YAML frontmatter valid?
2. Required sections present?
3. Code blocks have language tags?
4. No TODO/FIXME markers?
5. Token count reasonable?

### Pattern 2: Full Audit (15-30 minute review)

Comprehensive evaluation with human review:

```bash
# Generate full audit report
cortex skills audit <skill-name> --full

# Interactive mode for scoring
cortex skills audit <skill-name> --interactive
```

**Full Audit Process:**
1. Run automated checks
2. Read through content manually
3. Test code examples
4. Score each dimension
5. Document issues and recommendations
6. Generate report

### Pattern 3: Comparative Audit

Compare skill against reference implementation:

```bash
# Compare against template-skill-enhanced
cortex skills audit <skill-name> --compare template-skill-enhanced
```

### Pattern 4: Batch Audit

Audit multiple skills for registry health:

```bash
# Audit all skills in a category
cortex skills audit --category security

# Audit skills below threshold
cortex skills audit --below-score 3.5
```

## CLI Commands

```bash
# Basic audit
cortex skills audit <skill-name>

# Options
  --quick           Quick structural check only
  --full            Full audit with all dimensions
  --interactive     Interactive scoring mode
  --output FILE     Write report to file
  --format FORMAT   Output format (markdown|json|yaml)
  --compare SKILL   Compare against reference skill
  --fix             Auto-fix simple issues (formatting)
```

## Creating Custom Rubrics

Skills can define custom rubrics in `validation/rubric.yaml`:

```yaml
# validation/rubric.yaml
version: "1.0.0"
skill_name: my-skill

dimensions:
  clarity:
    weight: 25
    criteria:
      - "API examples use realistic data"
      - "Error handling is shown for each operation"
  completeness:
    weight: 25
    criteria:
      - "Covers all HTTP methods"
      - "Includes pagination patterns"
  accuracy:
    weight: 30
    criteria:
      - "Follows REST conventions"
      - "Security headers documented"
  usefulness:
    weight: 20
    criteria:
      - "Examples work with common frameworks"

passing_criteria:
  minimum_score: 3.5  # Higher bar for this skill
  required_dimensions:
    - accuracy
    - completeness
```

## Best Practices

### Do

- **Be specific** - "Line 45: SQL query vulnerable to injection" not "has security issues"
- **Be actionable** - Include how to fix each issue
- **Be fair** - Use the same standards consistently
- **Document evidence** - Quote specific content for each score
- **Prioritize** - Critical issues first, suggestions last

### Don't

- Score based on personal style preferences
- Mark deprecated patterns without suggesting alternatives
- Fail skills for missing optional sections
- Ignore security issues regardless of other scores
- Rush through audits for complex skills

## Anti-Patterns

### The Rubber Stamp

**Problem**: Approving skills without thorough review
**Why it's bad**: Low-quality skills erode trust in the library
**Fix**: Use the full audit checklist, test code examples

### The Perfectionist Block

**Problem**: Failing skills for minor issues
**Why it's bad**: Prevents useful skills from being available
**Fix**: Distinguish between blocking issues and suggestions

### Score Inflation

**Problem**: Giving high scores without justification
**Why it's bad**: Makes scores meaningless
**Fix**: Document specific evidence for each score

## Integration with CI/CD

```yaml
# .github/workflows/skill-quality.yml
name: Skill Quality Gate

on:
  pull_request:
    paths:
      - 'skills/**'

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install cortex
        run: pip install cortex
      - name: Audit changed skills
        run: |
          for skill in $(git diff --name-only HEAD~1 | grep 'skills/' | cut -d'/' -f2 | uniq); do
            cortex skills audit "$skill" --quick --fail-under 3.0
          done
```

## Troubleshooting

### "Audit fails but skill looks fine"

1. Check YAML frontmatter syntax
2. Verify all required sections exist
3. Ensure code blocks have language tags
4. Check for hidden characters (copy/paste issues)

### "Scores seem inconsistent"

1. Review the scoring guide for each dimension
2. Calibrate by auditing template-skill-enhanced first
3. Use --interactive mode for clearer criteria

## External Resources

- [Skill Template Reference](../template-skill-enhanced/SKILL.md)
- [Rubric Schema](../rubric.schema.yaml)
- [Skill Creator Guide](../skill-creator/SKILL.md)

## Changelog

### 1.0.0 (2026-01-05)
- Initial release
- Four-dimension scoring framework
- CLI integration
- CI/CD workflow example
