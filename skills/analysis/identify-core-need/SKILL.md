---
name: identify-core-need
description: This skill should be used when the user asks to "identify core need",
  "clarify requirements", "extract user intent", "validate distinctions", or when
  starting any research or analysis task that requires understanding what the user
  actually needs before proceeding.
version: 1.0.0
---

# Identify Core Need

Extract the fundamental requirement from user requests before any research or implementation.

## Purpose

Transform ambiguous or complex user requests into clear, actionable core needs with validated distinctions. Filter noise before it reaches the user.

## Flow

```
User Request
    │
    ├─ If ambiguous → AskUserQuestion to clarify
    │
    ▼
Apply Behavioral Principles + Validation Log
    │
    ▼
Core Need Output: action + target + triggers + validated distinctions
```

## When to Use

- Before any research phase
- Before generating configurations or code
- When user request has multiple interpretations
- When starting analysis that could go in multiple directions

## Process

**Read and follow `references/process.md` for the complete workflow.**

The process includes:

1. **Clarify User Request**: Use AskUserQuestion if ambiguous
2. **Apply Behavioral Principles**: Focus on practical, no artificial distinctions
3. **Validate Distinctions**: Ask "If I omit this, does it change what user must DO?"
4. **Document in Validation Log**: All evaluations must be logged
5. **Extract Core Need**: action + target + triggers + success criteria

## Key Behavioral Principles

| Principle | Application |
|-----------|-------------|
| FOCUS ON PRACTICAL | Address real objective directly |
| VALIDATE COMPARISONS | Each distinction must be relevant and correct |
| NO ARTIFICIAL DISTINCTIONS | Omit implementation details that don't change action |
| SIMPLICITY > COMPLEXITY | Simple solution without elaboration |
| VALIDATION QUESTION | "Does this change what user must DO?" |

## Output Structure

The mandatory output includes:
- Core Need (action, target, triggers, success criteria)
- Validation Log (minimum 3 evaluations)
- Actionable Distinctions (≤3 items)
- Context Discarded (minimum 2 items)
- Clarifications Made

## Validation Checkpoints

Before proceeding, verify:
- User request is clear
- Minimum 3 distinctions evaluated
- Each included distinction has justification
- Context Discarded has minimum 2 items
- Actionable Distinctions has ≤3 items

## Reference Files

| Need | Reference |
|------|-----------|
| Complete process with examples | `references/process.md` |