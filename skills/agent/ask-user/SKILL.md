---
name: ask-user
description: Pattern for effectively interacting with users to gather information or get decisions. Use when you need user input.
allowed-tools: AskUserQuestion
---

# Ask User Skill

Pattern for effective user interaction.

## When to Load This Skill

- You need to clarify requirements
- You need user to make a decision
- You have options to present

## Principles

### 1. Be Specific, Not Open-Ended

Bad: "What do you want?"
Good: "Should authentication use JWT or sessions?"

### 2. Offer Options When Possible

```
AskUserQuestion(
  questions: [
    {
      question: "Which authentication method should we use?",
      header: "Auth method",
      options: [
        { label: "JWT", description: "Stateless, good for APIs" },
        { label: "Sessions", description: "Stateful, good for web apps" }
      ],
      multiSelect: false
    }
  ]
)
```

### 3. Provide Context

Explain WHY you're asking:
- What decision depends on this
- What trade-offs exist
- What you recommend and why

### 4. Batch Related Questions

Ask related questions together:
```
questions: [
  { question: "Auth method?", ... },
  { question: "Token expiry?", ... },
  { question: "Refresh token?", ... }
]
```

## When to Ask vs Decide

### ASK when:
- Multiple valid approaches with different trade-offs
- User preference matters
- Scope is unclear
- Risk of wasted work

### DECIDE when:
- Clear best practice exists
- Low impact choice
- Easily reversible
- Standard convention applies

## Question Types

### Clarification
"You mentioned 'fast' - do you mean response time < 100ms or just faster than current?"

### Confirmation
"I understand you want X, Y, and Z. Is this correct?"

### Decision
"Option A has [pros/cons]. Option B has [pros/cons]. Which do you prefer?"

### Scope
"Should this also handle [related case] or just [original request]?"
