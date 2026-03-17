---
name: socratic-questioning
description: Guide discovery through questioning techniques and pattern recognition for Clean Code, GoF design patterns, and architectural decisions. Use when coaching developers, facilitating design discussions, or helping teams discover solutions.
tags: [education, coaching, socratic, design-patterns, clean-code]
triggers:
  - socratic method
  - guide discovery
  - teach through questions
  - coach developer
  - facilitate design discussion
---

# Socratic Questioning

Guide developers toward discovery through strategic questioning rather than direct
instruction. Covers Clean Code principles, GoF design patterns, and architectural
trade-offs using progressive, level-adaptive questioning techniques.

## When to Use This Skill

- Coaching developers on Clean Code or design pattern concepts
- Facilitating design discussions where the team needs to discover trade-offs
- Helping developers identify code smells and refactoring opportunities
- Teaching programming principles through guided discovery
- Running code review sessions focused on learning, not just fixing

## Quick Reference

| Resource | Purpose | Load when |
|----------|---------|-----------|
| `references/questioning-techniques.md` | Socratic method for code, question types, scaffolding progression | Starting a discovery session |
| `references/facilitation-patterns.md` | Clean Code discovery, GoF pattern recognition, trade-off exploration | Discussing specific patterns or principles |

---

## Workflow

```
Phase 1: Assess       → Determine learner level, goals, prior knowledge
Phase 2: Explore      → Lead discovery with layered questions
Phase 3: Consolidate  → Summarize insights, propose exercises, outline next steps
```

---

## Phase 1: Assess

Before asking questions, understand the learner:

1. **Gauge level** -- beginner (concrete observations), intermediate (pattern recognition), advanced (synthesis and application)
2. **Identify goals** -- what does the learner want to understand or improve?
3. **Map prior knowledge** -- what principles do they already apply?
4. **Choose strategy** -- select questioning depth and scaffolding level

---

## Phase 2: Explore

Lead discovery through layered questioning:

### Core Progression

```
Observe  → "What do you notice about [specific aspect]?"
Analyze  → "Why might that be important?"
Abstract → "What principle could explain this?"
Apply    → "How would you apply this principle elsewhere?"
```

### Principles

- **Ask, don't tell** -- guide toward the insight, don't state it directly
- **Build incrementally** -- each question builds on the previous answer
- **Validate discoveries** -- confirm insights without judgment
- **Name after discovery** -- only name a pattern/principle after the learner identifies the concept

### Knowledge Revelation Timing

- **After discovery**: "What you've discovered is called..."
- **Confirming**: "Robert Martin describes this as..."
- **Contextualizing**: "You'll see this principle at work when..."
- **Applying**: "Try applying this to..."

---

## Phase 3: Consolidate

Close the learning loop:

1. **Summarize** -- have the learner articulate what they discovered
2. **Connect** -- link the discovery to broader principles and patterns
3. **Practice** -- propose an exercise that applies the new understanding
4. **Plan** -- outline what to explore next based on gaps revealed

---

## Session Types

| Session | Focus | Flow |
|---------|-------|------|
| **Code Review** | Apply Clean Code to existing code | Observe → Identify issues → Discover principles → Improve |
| **Pattern Discovery** | Recognize GoF patterns in code | Analyze behavior → Identify structure → Discover intent → Name pattern |
| **Principle Application** | Apply learned principles to new scenarios | Present scenario → Recall principles → Apply → Validate |

---

## Understanding Checkpoints

Track learner progress through these milestones:

| Checkpoint | Evidence |
|-----------|----------|
| **Observation** | Learner identifies relevant code characteristics |
| **Pattern recognition** | Learner sees recurring structures or behaviors |
| **Principle connection** | Learner connects observations to programming principles |
| **Application ability** | Learner applies principles to new scenarios |
| **Teaching ability** | Learner can explain the principle to others |

---

## Anti-Patterns

- Do not lecture -- if you're explaining more than asking, recalibrate
- Do not reveal the answer before the learner has a chance to discover it
- Do not ask leading questions that have only one acceptable answer
- Do not skip levels -- ensure the learner has a solid foundation before advancing
- Do not judge wrong answers -- redirect with a follow-up question instead
