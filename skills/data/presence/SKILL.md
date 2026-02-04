---
name: presence
description: Surface what needs human attention during complex AI work. Use when context is large, user seems overwhelmed, or after substantial output. Triggers on "what just happened", "summarize progress", "what do I need to know", "lost track", "overwhelmed".
model: haiku
allowed-tools: Read
---

# presence

Stay present with AI reasoning. Surface what matters when complexity hides it.

## When to Use

| Trigger | Action |
| ------- | ------ |
| Context exceeds ~50 messages | Auto-surface presence markers |
| User says "lost track", "overwhelmed" | Run full presence check |
| After substantial output (>500 lines) | Append presence summary |
| Before major decision point | Surface assumptions and uncertainties |
| User asks "what just happened" | Reconstruct decision trail |

## Core Problem

AI output exceeds human verification capacity. The bottleneck isn't AI speed—it's human attention.

**Root cause:** No explicit surfacing of what needs attention.

## Presence Markers

Surface these at natural breakpoints:

### 1. Decisions Made

What was just decided (not proposed, actually committed):

```
## Decisions Made
- [Decision]: [Rationale in <10 words]
- [Decision]: [Rationale]
```

### 2. Assumptions Active

What's being assumed true without verification:

```
## Assumptions Active
- [Assumption]: [Risk if wrong: LOW/MEDIUM/HIGH]
- [Assumption]: [Risk if wrong]
```

**If HIGH risk:** Flag for explicit confirmation.

### 3. Uncertainties Open

What's still unknown or ambiguous:

```
## Uncertainties Open
- [Unknown]: [Impact on work: BLOCKING/DEGRADED/MINOR]
- [Unknown]: [Impact]
```

**If BLOCKING:** Stop and surface before continuing.

### 4. Verification Needed

What requires human eyes or action:

```
## Verification Needed
- [ ] [What to verify]: [Why human needed]
- [ ] [What to verify]: [Why human needed]
```

## Output Format

When presence check is triggered:

```
# Presence Check

## Since Last Check
[1-2 sentence summary of work done]

## Decisions Made
- [List with rationale]

## Assumptions Active
- [List with risk level]

## Uncertainties Open
- [List with impact]

## Verification Needed
- [ ] [Checklist items]

## Attention Required
[Single most important thing human should focus on]
```

## Frequency Calibration

| Context Length | Presence Frequency |
| -------------- | ------------------ |
| < 20 messages | On request only |
| 20-50 messages | Every major milestone |
| 50-100 messages | Every 10-15 exchanges |
| > 100 messages | Every 5-10 exchanges |

## Integration with Other Skills

| Skill | Presence Handoff |
| ----- | ---------------- |
| soul | Presence markers feed quality footer |
| gate | Verification Needed → gate checklist |
| trace | Uncertainties → investigation targets |
| shape | Assumptions → spec clarification |

## Anti-Patterns

| Bad | Good |
| --- | ---- |
| "Everything is going well" | List specific decisions and assumptions |
| Waiting for user to ask | Proactively surface at breakpoints |
| Dumping full context | Distill to what needs attention |
| "Let me know if questions" | Surface specific verification items |
| Burying important info | Lead with highest-attention item |

## Common Rationalizations (All Wrong)

| Thought | Reality |
| ------- | ------- |
| "User can scroll up" | Context exceeds working memory after ~7 items |
| "It's all in the chat" | Presence requires active surfacing, not passive availability |
| "I'll summarize at the end" | Attention lost mid-stream is never recovered |
| "This is obvious" | What's obvious to AI ≠ what's salient to human |
| "User didn't ask" | Presence is proactive, not reactive |

## When NOT to Use

- Simple single-turn questions
- User explicitly wants stream-of-consciousness
- Context is short and clear
- Debugging session with tight feedback loop
