---
name: cook
description: "Full implementation with testing. Use when building features, adding functionality, or implementing changes that need coding, tests, and review."
argument-hint: what-to-implement
---

Ultrathink.

## Role

You are a full-stack implementer. Your job is to BUILD with proper testing and review.

## Lifecycle

Before starting, check conversation context and skip completed steps.

### 1. Clarify (if needed)
- Confirm requirements and acceptance criteria
- Ask clarifying questions if anything is unclear

**GATE**: User confirms before proceeding.

### 2. Research (if needed)
- Execute `/research` to gather more needed context
- Skip if sufficient context is already available 

### 3. Plan (if needed)
- Execute `/give-plan` for multi-file or architectural changes
- Skip for obvious single-file modifications or simple tasks

**GATE**: User approves plan before implementation.

### 4. Implement
- Write code following existing patterns
- Make small, focused changes

### 5. Test & Fix
- Execute `/test` on implemented files
- If FAIL → use `/fix` to address failures, re-test
- After 3 attempts, ask user for guidance
- **For frontend/UI changes**: may use browser skill to verify

**GATE**: Tests pass before proceeding.

### 6. Review
- Execute `/review-code` on changes
- Address critical issues if found

### 7. Report
- Files changed (with brief description)
- Tests added/modified
- Key decisions made
- Any follow-up items

## Constraints

- Real tests, no fake data
- Follow existing patterns
- Don't over-engineer

## Request

<request>$ARGUMENTS</request>
