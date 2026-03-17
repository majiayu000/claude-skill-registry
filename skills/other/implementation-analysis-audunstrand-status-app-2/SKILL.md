---
name: Lightweight Implementation Analysis Protocol
description: This skill should be used when fixing bugs, implementing features, debugging issues, or making code changes. Ensures understanding of code flow before implementation by: (1) Tracing execution path with specific file:line references, (2) Creating lightweight text diagrams showing class.method() flows, (3) Verifying understanding with user. Prevents wasted effort from assumptions or guessing. Triggers when users request: bug fixes, feature implementations, refactoring, TDD cycles, debugging, code analysis.
---

# GitHub Copilot Skill: implementation-analysis

> **Note:** This skill has been adapted from [claude-skillz](https://github.com/NTCoding/claude-skillz) 
> for use with GitHub Copilot Agent Skills.

---

# Lightweight Implementation Analysis Protocol

Quick understanding before implementation - **just enough to guide TDD, no more**.

## When This Activates

Before creating implementation plans, fix plans, or TDD cycles for bugs/features.

## The Protocol (3 Quick Steps)

### 1. Trace the Flow

Answer these:
- Which event/request triggers this?
- Which file:line handles it?
- Where does the error occur (file:line)?

### 2. Quick Diagram

Simple class.method() flow with relevant data:

```
Event: EventName
  ↓ (contains: relevant fields)
Class.method() [file:line]
  ↓ (what it does)
Class.method() [file:line] ← 💥 Error here
  ↓
Result: What happens
```

**Keep it short** - 5-10 lines max.

### 3. Verify

Ask: "Here's the flow: [diagram]. Correct?"

Wait for confirmation, then proceed.

## Example

```
Problem: Email validation failing

Event: user.email.updated
  ↓ (email: "invalid@")
UpdateUserEmailHandler.execute() [line 281]
  ↓ (validates email format)
EmailValidator.parse() [line 289] ← 💥 Throws ValidationError
  ↓
Result: Error response

Current: Throws
Should: Use safeParse(), return validation error
```

## Rules

- **Keep it lightweight** - This isn't detailed planning, just enough to know what to test
- **Be specific** - File:line, not abstractions
- **Get confirmation** - Don't proceed without it
- **Skip for trivial changes** - Typos, formatting, docs

## Anti-Pattern

❌ **WRONG**: "I'll fix the validation. Here's my plan..."
✅ **RIGHT**: "Let me trace where the error occurs... [diagram]. Correct?"
