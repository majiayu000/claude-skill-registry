---
name: intent-first
description: Clarify user intent before executing tasks. Use when requests are vague, ambiguous, or could be interpreted multiple ways. Helps prevent wasted effort from misunderstanding.
---

# Intent-First: Clarify Before You Execute

## Purpose

Transform vague requests into clear, actionable specifications before starting work.

## When to Use

- User request is ambiguous or could mean multiple things
- Task scope is unclear
- Success criteria are not defined
- You're about to start significant work

## The Intent Clarification Framework

### Step 1: Identify the Intent Type

| Type | Signal Words | Example |
|------|-------------|---------|
| **Create** | make, build, write, generate | "Make a report" |
| **Modify** | change, update, fix, improve | "Fix this code" |
| **Analyze** | review, check, find, understand | "Review this design" |
| **Decide** | should I, which is better, compare | "Should I use X or Y?" |
| **Learn** | explain, how does, what is | "How does this work?" |

### Step 2: Ask the 5 Clarifying Questions

Not all questions apply to every request. Select the relevant ones:

#### 1. PURPOSE (Why)
> "What problem are you trying to solve?" or "Who will use this and for what?"

#### 2. SCOPE (What)
> "What should be included? What should NOT be included?"

#### 3. FORMAT (How)
> "What format do you expect? (bullet points, prose, code, diagram)"

#### 4. CONSTRAINTS (Limits)
> "Any constraints? (time, length, technology, style)"

#### 5. SUCCESS (Done)
> "How will you know this is successful?"

### Step 3: Confirm Understanding

Before proceeding, summarize:

```
I understand you want to:
- [Action]: [specific task]
- [Purpose]: [why this matters]
- [Output]: [expected deliverable]
- [Constraints]: [limitations to respect]

Shall I proceed?
```

## Examples

### Vague Request
> "Help me with my presentation"

### Clarified Intent
```
I understand you want to:
- Action: Improve/create presentation slides
- Purpose: [Need to ask - what's the presentation for?]
- Output: [Need to ask - slides? script? both?]
- Constraints: [Need to ask - time limit? audience?]

Let me ask:
1. What is the presentation about and who is the audience?
2. Do you have existing slides to improve, or starting from scratch?
3. What do you need help with - content, structure, or visuals?
```

## Anti-Patterns

| Don't Do This | Do This Instead |
|---------------|-----------------|
| Start working immediately on vague requests | Pause and clarify first |
| Ask all 5 questions every time | Select relevant questions only |
| Make assumptions silently | State assumptions and confirm |
| Over-clarify simple requests | Use judgment on when to clarify |

## Quick Decision: When to Skip Clarification

Skip if ALL are true:
- [ ] Request is specific and unambiguous
- [ ] Scope is clearly bounded
- [ ] Failure cost is low (easy to redo)
- [ ] You have high confidence in understanding

## Integration with Other Skills

After clarifying intent:
- Use **delegation-triggers** to decide who should execute
- Use **skill-activator** to find relevant skills for the task
