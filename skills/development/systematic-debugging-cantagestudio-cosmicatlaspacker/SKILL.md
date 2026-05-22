---
name: systematic-debugging
description: "[Debug] Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes - four-phase framework (root cause investigation, pattern analysis, hypothesis testing, implementation) that ensures understanding before attempting solutions. (project)"
---

# Systematic Debugging

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

## The Four Phases

### Phase 1: Root Cause Investigation
1. Read Error Messages Carefully
2. Reproduce Consistently
3. Check Recent Changes
4. Gather Evidence in Multi-Component Systems
5. Trace Data Flow

### Phase 2: Pattern Analysis
1. Find Working Examples
2. Compare Against References
3. Identify Differences
4. Understand Dependencies

### Phase 3: Hypothesis and Testing
1. Form Single Hypothesis
2. Test Minimally
3. Verify Before Continuing

### Phase 4: Implementation
1. Create Failing Test Case
2. Implement Single Fix
3. Verify Fix
4. If 3+ Fixes Failed: Question Architecture

## Red Flags - STOP and Follow Process

- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "I don't fully understand but this might work"
- Proposing solutions before tracing data flow

## Quick Reference

| Phase | Key Activities | Success Criteria |
|-------|---------------|------------------|
| 1. Root Cause | Read errors, reproduce, check changes | Understand WHAT and WHY |
| 2. Pattern | Find working examples, compare | Identify differences |
| 3. Hypothesis | Form theory, test minimally | Confirmed or new hypothesis |
| 4. Implementation | Create test, fix, verify | Bug resolved, tests pass |