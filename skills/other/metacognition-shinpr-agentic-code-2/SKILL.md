---
name: metacognition
description: "Validates approach and checks assumptions before/after tasks. Use when: starting work, encountering errors, or switching phases."
---

# Metacognition Protocol

## Purpose

Self-assessment checkpoints.

## When to Apply [MANDATORY CHECKPOINTS]

**BLOCKING METACOGNITION REQUIRED at:**
- [CHECKPOINT] Task type changes → CANNOT proceed without assessment
- [CHECKPOINT] After completing ANY task from Work Plan document → MUST evaluate before next task
- [CHECKPOINT] When encountering error or unexpected result → ASSESS approach immediately
- [CHECKPOINT] Before writing first line of new feature → VALIDATE approach first
- [CHECKPOINT] When switching between major phases → CONFIRM all gates passed

**ENFORCEMENT**: Skipping metacognition = CRITICAL VIOLATION

## Assessment Questions

### 1. Task Understanding

- What is the fundamental goal?
- Am I solving the root cause or symptom?
- Do I have all necessary information?
- Are success criteria clear and measurable?
- What are the known unknowns at this point?

### 2. Current State

- What rules are currently loaded?
- Which rules are actually being used?
- What assumptions am I making?
- What could go wrong?

### 3. Approach Validation

- Is my approach the simplest solution?
- Am I following established patterns?
- Have I considered alternatives?
- Is this maintainable long-term?
- What would make me reverse this decision? (Kill criteria)

## Rule Selection Guide

### By Task Type

| Task Type | Essential Rules | Optional Rules |
|-----------|----------------|----------------|
| **Implementation** | language/rules.md, ai-development-guide.md | architecture patterns |
| **Bug Fix** | ai-development-guide.md | debugging patterns |
| **Design** | documentation-criteria.md | architecture patterns |
| **Testing** | language/testing.md | coverage strategies |
| **Refactoring** | ai-development-guide.md | design patterns |

### Loading Strategy

**Immediate needs**: Load only what's required now
**Progressive loading**: Add rules as specific needs arise
**Cleanup**: Unload rules after task completion

Note: Context management is user's responsibility. Ask for guidance if unsure.

## Common Decision Points

### When Starting Work [BLOCKING CHECKLIST]
☐ [MUST VERIFY] Task type and scale documented with evidence
☐ [MUST VERIFY] Required rules LOADED and file paths listed
☐ [MUST VERIFY] Success criteria MEASURABLE and specific
☐ [MUST VERIFY] Approach validated against existing patterns

**GATE: CANNOT start coding if ANY unchecked**

### During Execution [PROGRESS GATES]
☐ [VERIFY] Following Work Plan from `docs/plans/`
☐ [VERIFY] Making measurable progress (list completed items)
☐ [EVALUATE] Additional rules needed? (load IMMEDIATELY if yes)
☐ [EVALUATE] Blocked for >10 minutes? (MUST ask for help)

**Dynamic Rule Loading Triggers:**
- Same error occurs 2+ times → Load `ai-development-guide.md` for debugging patterns
- "Performance" mentioned in requirements → Load optimization rules if available
- "Security" mentioned in requirements → Load security guidelines if available
- External API/service integration needed → Load integration patterns if available

**ENFORCEMENT: If progress stalled → MANDATORY metacognition**

### After Completion [EXIT GATES]
☐ [VERIFIED] ALL completion criteria met with evidence
☐ [VERIFIED] Code quality metrics passed (lint, test, build)
☐ [VERIFIED] Documentation updated (if applicable)
☐ [RECORDED] What worked/failed for next iteration

**GATE: CANNOT mark complete without ALL verified**

## Anti-Pattern Recognition

| Pattern | Signs | Correction |
|---------|-------|------------|
| **Over-engineering** | Complex solution for simple problem | Simplify approach |
| **Under-planning** | Jumping into code too quickly | Step back, plan first |
| **Tunnel vision** | Ignoring alternatives | Consider other approaches |
| **Quality debt** | Skipping tests or docs | Complete properly |
| **Context bloat** | Loading unnecessary rules | Load only essentials |

## Error Recovery

When stuck:
1. Identify what's blocking progress
2. Check if it's a knowledge gap or logic error
3. Review loaded rules for guidance
4. Consider simpler approach
5. Ask user for clarification

**ERROR HANDLING PROTOCOL:**

When encountering an error or blocker:
- [IMMEDIATE] Execute metacognition assessment
- [SEARCH] Look for similar patterns in codebase
- [RE-READ] Relevant rule files for guidance
- [EVALUATE] Can I solve this with available information?

If unable to resolve:
- [DOCUMENT] Exact error message and context
- [EXPLAIN] What was attempted and why it failed
- [REQUEST] User guidance with specific questions

**PRINCIPLE: Ask for help when genuinely stuck, not after arbitrary attempt count**

## Learning from Experience

Track:
- What worked well
- What caused delays
- Which rules were helpful
- What patterns emerged
- What to do differently

## Guidelines

- **Be honest**: Acknowledge when uncertain
- **Be systematic**: Follow structured approach
- **Be efficient**: Don't overthink simple tasks
- **Be thorough**: Don't skip important steps
- **Be adaptive**: Adjust approach based on feedback

## Notes

Remember:
- Metacognition prevents costly mistakes
- Regular reflection improves quality
- It's okay to pause and think
- Ask for help when genuinely stuck
- Perfect is the enemy of good
