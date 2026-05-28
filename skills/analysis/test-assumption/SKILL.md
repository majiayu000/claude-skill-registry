---
name: test-assumption
description: Identify hidden assumptions about users in code that could exclude or harm. A focused analysis asking "What am I assuming about the person using this?"
allowed-tools: Read, Grep, Glob
user-invocable: true
---

# Test of Assumption

A focused analysis to identify hidden assumptions about users that could exclude or harm them.

## Philosophy

Every line of code makes assumptions about who will use it. Most assumptions are invisible to the people making them because they match the developer's own experience.

> "What am I assuming about the person using this?"

This skill makes the invisible visible. Not to judge—but to **see** who we might be leaving out.

## Scope

The user may specify a file path, glob pattern, or directory. If not specified, ask what they'd like to analyze.

## Config Integration

Before starting, check for `.inclusion-config.md` in the project root.

If it exists:
1. **Read** scope decisions and acknowledged findings
2. **Skip** acknowledged findings (note them in output)
3. **Respect** scope decisions (e.g., if US-only, certain location assumptions are intentional)
4. **Note** at the top of output: "Config loaded: .inclusion-config.md"

Core dignity checks always run regardless of config.

## Process

### 1. Read and Understand

First, **read the code** to understand:
- What does this code do?
- Who sees or uses this? (developers? end users? both?)
- What's the context? (onboarding? checkout? settings?)

### 2. Identify Assumptions

Look for assumptions about users in these categories:

**Ability**
- Physical: Can use mouse, can see screen, can hear audio
- Cognitive: Can read quickly, can remember steps, understands jargon
- Technological: Has fast internet, has modern device, has webcam

**Identity**
- Gender: Binary options, gendered language, assumptions about presentation
- Age: Tech-savvy defaults, references that assume generation
- Culture: Western holidays, specific foods, cultural norms

**Circumstance**
- Economic: Has credit card, can afford premium, has bank account
- Family: Has parents, is married, has children
- Location: In US, has stable address, speaks English
- Employment: Has job, has work email, available during business hours

**Experience**
- No trauma history (showing "memories" or throwbacks)
- No grief (Mother's/Father's Day reminders)
- Positive associations (holidays are joyful)

### 3. Evaluate Each Assumption

For each assumption identified:

| Question | If Yes | If No |
|----------|--------|-------|
| Is this necessary for the feature to work? | Document why | Flag for removal |
| Could it exclude or harm someone? | Note who | Lower priority |
| Could the feature work without this assumption? | Suggest how | Document constraint |

### 4. Prioritize

**Remove** - Unnecessary and potentially harmful
**Redesign** - Can work differently to be more inclusive
**Mitigate** - Necessary but add opt-out or alternatives
**Document** - Unavoidable with clear justification

## Output Format

```markdown
## Assumption Analysis: [Target]

[1-2 sentences: What is this? Who uses it? Key finding?]

---

### Assumptions Found

| # | Assumption | Category | Who's Excluded | Priority |
|---|------------|----------|----------------|----------|
| 1 | Binary gender required | Identity | Non-binary users | Remove |
| 2 | Credit card required | Circumstance | Unbanked users | Redesign |
| 3 | Can click buttons | Ability | Keyboard users | Mitigate |

### Detailed Analysis

#### 1. [Assumption]

**Location**: `file.tsx:27`
**Category**: [Ability / Identity / Circumstance / Experience]

**Who's excluded**: [Specific user groups]

**Is it necessary?** [Yes/No with reasoning]

**Recommendation**: Remove / Redesign / Mitigate / Document

**Suggested change**:
[Specific alternative approach]

---

### Summary

**[X] assumptions found**: [breakdown by priority]

**Pattern**: [What underlying assumption connects these?]

**Priority action**: [Single most impactful change to make]
```

## The Guiding Question

When in doubt:

> "If this were my first experience with this product, and I didn't match the 'default user', would I feel welcome?"

Design for the margins. What works for users with the most constraints usually works better for everyone.
