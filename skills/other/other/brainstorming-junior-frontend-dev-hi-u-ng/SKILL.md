---
name: brainstorming
description: "You MUST use this before any creative work - creating features, building components, adding functionality, or modifying behavior. Explores user intent, requirements and design before implementation."
---

# Brainstorming Skill

## Purpose

Pure collaborative dialogue skill for exploring ideas. This skill focuses ONLY on understanding and exploration - it does NOT generate specifications, tests, or implementation plans.

**This skill outputs:** Understanding, not artifacts.

---

## Core Principles

### 1. One Question at a Time
Never overwhelm with multiple questions. Each message should contain exactly ONE question.

```
BAD:  "What's the purpose? Who are the users? What's the timeline?"
GOOD: "What problem are you trying to solve with this feature?"
```

### 2. Multiple Choice Preferred
When possible, offer 2-4 concrete options instead of open-ended questions.

```
BAD:  "How should we handle authentication?"
GOOD: "For authentication, which approach fits your needs?
       A) JWT tokens (stateless, good for APIs)
       B) Session cookies (simpler, good for web apps)
       C) OAuth only (delegate to providers)"
```

### 3. Lead with Recommendation
When presenting options, lead with your recommended choice and explain why.

```
GOOD: "I'd recommend option A (JWT tokens) because your API will be consumed
       by mobile apps. That said, here are the alternatives..."
```

### 4. Incremental Validation
Present ideas in 200-300 word chunks. Validate each before moving on.

```
"Here's how I understand the data flow so far...
[200-300 words]
Does this match your thinking?"
```

### 5. Explore Alternatives
Always propose 2-3 different approaches before settling on one.

### 6. YAGNI Ruthlessly
Challenge any feature that isn't essential. Ask "Do we need this for v1?"

---

## Dialogue Flow

```
┌─────────────────────────────────┐
│  1. UNDERSTAND THE IDEA         │
│  - What problem are we solving? │
│  - Who is this for?             │
│  - What does success look like? │
└──────────────┬──────────────────┘
               ▼
┌─────────────────────────────────┐
│  2. EXPLORE CONSTRAINTS         │
│  - Technical limitations?       │
│  - Timeline/scope constraints?  │
│  - Integration requirements?    │
└──────────────┬──────────────────┘
               ▼
┌─────────────────────────────────┐
│  3. PROPOSE APPROACHES          │
│  - Present 2-3 options          │
│  - Explain trade-offs           │
│  - Lead with recommendation     │
└──────────────┬──────────────────┘
               ▼
┌─────────────────────────────────┐
│  4. VALIDATE UNDERSTANDING      │
│  - Summarize in sections        │
│  - Check each section           │
│  - Iterate until aligned        │
└──────────────┴──────────────────┘
```

---

## Question Categories

### Discovery Questions
Understanding the core idea:
- "What problem does this solve?"
- "Who will use this and how?"
- "What does success look like?"
- "Why now? What triggered this need?"

### Constraint Questions
Understanding boundaries:
- "What existing systems does this need to work with?"
- "Are there performance requirements?"
- "What's the scope for v1 vs later?"
- "Any technical constraints I should know about?"

### Clarification Questions
Drilling into specifics:
- "When you say X, do you mean A or B?"
- "Can you give me an example of...?"
- "What should happen when...?"

### Validation Questions
Confirming understanding:
- "So if I understand correctly... Is that right?"
- "Does this match what you had in mind?"
- "Anything I'm missing?"

---

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Do This Instead |
|--------------|--------------|-----------------|
| Multiple questions per message | Overwhelming, unfocused | One question only |
| Open-ended when options exist | Harder to answer | Offer concrete choices |
| Jumping to solutions | Miss requirements | Understand first |
| Long monologues | Loses engagement | 200-300 word chunks |
| Assuming requirements | Builds wrong thing | Ask, don't assume |
| Skipping alternatives | Misses better options | Always explore 2-3 approaches |

---

## Output

This skill produces **shared understanding**, not documents.

The calling command (e.g., `/research:feature`) is responsible for:
- Capturing the dialogue outcomes
- Generating formal requirements documents
- Creating specifications

This skill focuses purely on the conversation.

---

## Integration Points

This skill is used by:
- `/research:feature` - Feature requirements gathering
- `/research:plan` - Architecture exploration
- `/start` - Initial scoping

The skill provides dialogue structure; the command provides context and output handling.
