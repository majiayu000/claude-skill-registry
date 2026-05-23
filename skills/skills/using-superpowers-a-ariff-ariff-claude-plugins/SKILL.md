---
name: using-superpowers
description: Core skill activation protocol - establishes mandatory workflows for finding and applying skills before any task
version: 1.0.0
author: Ariff
---

# Superpowers Activation Protocol

## Core Philosophy

> "If a skill exists for your task, you MUST use it. No exceptions. No rationalizations."

Skills encode proven solutions. Ignoring them means repeating solved problems.

## Mandatory First Response Protocol

Before ANY action, complete this mental checklist:

```
□ What skills might apply here?
□ Have I checked the skill registry?
□ Did I read the CURRENT version (not memory)?
□ Am I following it exactly?
```

## The Golden Rules

### 1. Skills Are Not Optional
If a relevant skill exists → USE IT.
- "This is just a simple question" → Still check for skills
- "I can do this quickly" → Skills exist because "quick" becomes complex
- "The skill is overkill" → Use it anyway

### 2. Always Announce Skill Usage
```
"I'm using [Skill Name] to [what you're doing]."
```

### 3. Checklists Require TodoWrite
If a skill has a checklist → Create todos for EACH item.
Don't work through checklists mentally. Track them.

### 4. Instructions ≠ Permission to Skip Workflows
User says "Fix X" → That's the WHAT, not the HOW.
Still follow brainstorming, TDD, verification workflows.

## Skill Categories

| Category | When to Use |
|----------|-------------|
| **Checkers** | Before assumptions, before actions |
| **Collaboration** | Planning, brainstorming, executing plans |
| **Debugging** | When something's broken |
| **Problem-Solving** | When stuck |
| **Testing** | TDD, test design |
| **Meta** | Writing/improving skills |

## Quick Dispatch

```
Starting a feature → brainstorming → writing-plans → executing-plans
Something broken → systematic-debugging or root-cause-tracing
About to assume → assumption-checker
About to modify → pre-action-verifier
Claiming done → verification-before-completion
```

## Anti-Patterns (Stop If You Think These)

| Thought | Reality |
|---------|---------|
| "I remember this skill" | Skills evolve. Read current version. |
| "This doesn't need a skill" | If skill exists, use it. |
| "Let me just do this first" | Check skills BEFORE anything. |
| "This is simple" | Simple tasks become complex. Use skills. |

## Integration with Checker Agents

Before taking action, the checker agents validate:
- `assumption-checker` → Are you guessing?
- `context-validator` → Do you have enough context?
- `intent-clarifier` → Is the request clear?
- `pre-action-verifier` → Are prerequisites met?
- `fact-checker` → Are your claims about code accurate?

These checkers are **strict mode** - they halt and ask rather than proceeding.

## Summary

1. Check for relevant skills FIRST
2. Announce you're using them
3. Follow them EXACTLY
4. Use TodoWrite for checklists
5. Verify before claiming completion
