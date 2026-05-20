---
# VERSION: 2.88.0
name: ask-questions-if-underspecified
description: "Ask clarifying questions when requirements are underspecified"
user-invocable: true
---

# Skill: Ask Questions If Underspecified

## v2.88 Key Changes (MODEL-AGNOSTIC)

- **Model-agnostic**: Uses model configured in `~/.claude/settings.json` or CLI/env vars
- **No flags required**: Works with the configured default model
- **Flexible**: Works with GLM-5, Claude, Minimax, or any configured model
- **Settings-driven**: Model selection via `ANTHROPIC_DEFAULT_*_MODEL` env vars

**ultrathink** - Take a deep breath. We're not here to write code. We're here to make a dent in the universe.

## The Vision
Clarity is the foundation of inevitable solutions. Every question should narrow the path to truth.

## Your Work, Step by Step
1. **Analyze requirements**: Identify missing inputs and ambiguities.
2. **Separate MUST vs NICE**: Block on essentials, assume the rest.
3. **Ask precisely**: Short, concrete questions with defaults.
4. **Confirm understanding**: Summarize before proceeding.

## Ultrathink Principles in Practice
- **Think Different**: Question hidden assumptions.
- **Obsess Over Details**: Align questions with real constraints.
- **Plan Like Da Vinci**: Build the question set before asking.
- **Craft, Don't Code**: Precision over volume.
- **Iterate Relentlessly**: Refine questions as context evolves.
- **Simplify Ruthlessly**: Ask only what matters.

## Purpose
Ensure task clarity BEFORE implementation by identifying ambiguities.

## When to Use
- ANY new task or feature request
- Complex modifications
- Unclear requirements

## Process

### 1. Analyze Requirements
Identify:
- Missing technical details
- Unclear scope boundaries
- Ambiguous terminology
- Unstated assumptions

### 2. Categorize Questions

#### MUST_HAVE (Blocking)
Questions that BLOCK implementation until answered:
- Critical architecture decisions
- Security requirements
- Data model choices
- Integration points

#### NICE_TO_HAVE (Assumptions)
Questions where you can make reasonable assumptions:
- UI/UX preferences
- Performance targets
- Edge case handling

### 3. Output Format

```markdown
## 🔍 Clarification Needed

### MUST_HAVE (Please answer before I proceed):
1. [Critical question 1]
2. [Critical question 2]

### NICE_TO_HAVE (I'll assume these if not specified):
- [Optional question] → I'll assume: [default value]
- [Optional question] → I'll assume: [default value]

### My Understanding:
[Summarize what you understand so far]
```

### 4. Wait for Answers
DO NOT proceed with implementation until MUST_HAVE questions are answered.

## Examples

### Good Clarification
```
MUST_HAVE:
1. Should auth support both email/password AND OAuth providers?
2. What's the session timeout requirement?

NICE_TO_HAVE:
- Rate limiting? → I'll assume: 100 req/min
- Password complexity? → I'll assume: min 8 chars, 1 number, 1 special
```

### Bad (Too Vague)
```
What do you want?
Can you give more details?
```
