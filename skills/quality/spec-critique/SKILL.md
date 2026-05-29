---
name: spec-critique
description: 'Self-critique specification documents using extended thinking. Use when a spec is complete and needs validation before implementation.'
version: 1.0.0
model: opus
extended_thinking: true
invoked_by: both
user_invocable: true
tools: [Read, Write, Edit, Glob, Grep]
best_practices:
  - Use extended thinking for deep analysis
  - Compare spec against requirements and research
  - Fix issues directly, don't just report
error_handling: graceful
streaming: supported
source: auto-claude
---

# Specification Critique Skill

## Overview

Critically review specification documents for accuracy, completeness, and feasibility. Use extended thinking to find issues BEFORE implementation begins.

**Core principle:** Use extended thinking (deep analysis). Find problems BEFORE implementation.

## When to Use

**Always:**

- After spec writing is complete
- Before implementation planning begins
- When spec involves external integrations
- For complex features with multiple components

**Exceptions:**

- Simple specs for trivial changes
- Specs already reviewed by another agent

## The Iron Law

```
NO IMPLEMENTATION WITHOUT SPEC CRITIQUE FOR COMPLEX TASKS
```

Complex tasks (external integrations, multi-service changes) must have spec critique.

## Inputs Required

Before critiquing, ensure you have:

1. **spec.md** - The specification to critique
2. **Requirements document** - Original user requirements
3. **Project context** - Tech stack, patterns

## Workflow

### Phase 1: Load All Context

```bash
# Read the spec
cat .claude/context/specs/[task-name]-spec.md

# Read original requirements
cat .claude/context/requirements/[task-name].md

# Read project context
cat .claude/context/tech-stack.md
```

Understand:

- What the spec claims
- What the user originally requested
- What patterns exist in the codebase

### Phase 2: Deep Analysis (USE EXTENDED THINKING)

**CRITICAL**: Use extended thinking for this phase. Think deeply about:

#### Technical Accuracy

Compare spec against requirements and codebase:

- **Package names**: Does spec use correct package names?
- **Import statements**: Do imports match API patterns?
- **API calls**: Do function signatures match documentation?
- **Configuration**: Are env vars and config options correct?

**Check for common spec errors:**

- Wrong package name (e.g., "react-query" vs "@tanstack/react-query")
- Outdated API patterns (e.g., using deprecated functions)
- Incorrect function signatures (e.g., wrong parameter order)
- Missing required configuration (e.g., missing env vars)

Flag any mismatches.

#### Completeness

Check against requirements:

- **All requirements covered?** - Each requirement should have implementation details
- **All acceptance criteria testable?** - Each criterion should be verifiable
- **Edge cases handled?** - Error conditions, empty states, timeouts
- **Integration points clear?** - How components connect

Flag any gaps.

#### Consistency

Check within spec:

- **Package names consistent** - Same name used everywhere
- **File paths consistent** - No conflicting paths
- **Patterns consistent** - Same style throughout
- **Terminology consistent** - Same terms for same concepts

Flag any inconsistencies.

#### Feasibility

Check practicality:

- **Dependencies available?** - All packages exist and are maintained
- **Infrastructure realistic?** - Setup will work
- **Implementation order logical?** - Dependencies before dependents
- **Scope appropriate?** - Not over-engineered, not under-specified

Flag any concerns.

#### Requirements Alignment

Cross-reference with requirements:

- **Verified information used?** - Spec should use researched facts
- **Unverified claims flagged?** - Any assumptions marked clearly
- **Gotchas addressed?** - Known issues handled
- **Recommendations followed?** - Requirements suggestions incorporated

Flag any divergences.

### Phase 3: Catalog Issues

Create a list of all issues found:

```markdown
## Issues Found

### 1. [SEVERITY: HIGH] Package name incorrect

- **Spec says**: "[incorrect]"
- **Should be**: "[correct]"
- **Location**: Line 45, Requirements section

### 2. [SEVERITY: MEDIUM] Missing edge case

- **Requirement**: "Handle connection failures"
- **Spec**: No error handling specified
- **Location**: Implementation Notes section

### 3. [SEVERITY: LOW] Inconsistent terminology

- **Issue**: Uses both "memory" and "episode" for same concept
- **Location**: Throughout document
```

### Phase 4: Fix Issues

For each issue found, fix it directly in the spec:

**For each fix**:

1. Make the change in spec
2. Verify the change was applied
3. Document what was changed

### Phase 5: Create Critique Report

```markdown
# Spec Critique Report

**Spec**: [spec-name]
**Date**: [timestamp]

## Summary

| Category               | Status    | Issues  |
| ---------------------- | --------- | ------- |
| Technical Accuracy     | PASS/FAIL | [count] |
| Completeness           | PASS/FAIL | [count] |
| Consistency            | PASS/FAIL | [count] |
| Feasibility            | PASS/FAIL | [count] |
| Requirements Alignment | PASS/FAIL | [count] |

## Issues Found and Fixed

### High Severity

1. [Issue] - FIXED: [what was changed]

### Medium Severity

1. [Issue] - FIXED: [what was changed]

### Low Severity

1. [Issue] - FIXED: [what was changed]

## No Issues Found (if applicable)

Spec is well-written with no significant issues found.

## Confidence Level

[HIGH/MEDIUM/LOW]

## Recommendations

- [Any remaining concerns or suggestions]
```

### Phase 6: Verify Fixes

After making changes:

```bash
# Verify spec is still valid markdown
head -50 .claude/context/specs/[task-name]-spec.md

# Check key sections exist
grep -E "^##? Overview" spec.md
grep -E "^##? Requirements" spec.md
grep -E "^##? Success Criteria" spec.md
```

## Severity Guidelines

**HIGH** - Will cause implementation failure:

- Wrong package names
- Incorrect API signatures
- Missing critical requirements
- Invalid configuration

**MEDIUM** - May cause issues:

- Missing edge cases
- Incomplete error handling
- Unclear integration points
- Inconsistent patterns

**LOW** - Minor improvements:

- Terminology inconsistencies
- Documentation gaps
- Style issues
- Minor optimizations

## Category Definitions

- **Accuracy**: Technical correctness (packages, APIs, config)
- **Completeness**: Coverage of requirements and edge cases
- **Consistency**: Internal coherence of the document
- **Feasibility**: Practical implementability
- **Alignment**: Match with original requirements

## Verification Checklist

Before completing spec critique:

- [ ] All sections analyzed with extended thinking
- [ ] Technical accuracy verified
- [ ] Completeness checked against requirements
- [ ] Consistency verified throughout spec
- [ ] Feasibility assessed
- [ ] All issues cataloged with severity
- [ ] All high/medium issues fixed
- [ ] Critique report created
- [ ] Spec still valid after fixes

## Extended Thinking Prompt

When analyzing, think through:

> "Looking at this spec, I need to deeply analyze it against the requirements...
>
> First, let me check all package names. The requirements mention [X], but the spec says [Y]. This is a mismatch that needs fixing.
>
> Next, looking at the API patterns. The requirements show initialization requires [steps], but the spec shows [different steps]. Another issue.
>
> For completeness, the requirements mention [X, Y, Z]. The spec covers X and Y but I don't see Z addressed anywhere. This is a gap.
>
> Looking at consistency, I notice '[term1]' and '[term2]' used interchangeably. Should standardize on one term.
>
> For feasibility, the setup seems correct. The configuration matches.
>
> Overall, I found [N] issues that need fixing before this spec is ready for implementation."

## Common Mistakes

### Surface-Level Review

**Why it's wrong:** Skimming misses critical issues.

**Do this instead:** Use extended thinking. Analyze each section deeply.

### Reporting Without Fixing

**Why it's wrong:** Just listing issues doesn't improve the spec.

**Do this instead:** Fix issues directly. Make the spec better.

## Integration with Other Skills

This skill works well with:

- **spec-writing**: Provides the spec to critique
- **complexity-assessment**: Helps determine if critique is needed
- **debugging**: Use if spec critique reveals code issues

## Memory Protocol

**Before starting:**
Read `.claude/context/memory/learnings.md`

**After completing:**

- New pattern -> `.claude/context/memory/learnings.md`
- Issue found -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: If it's not in memory, it didn't happen.
