---
name: brainstorm
description: Use in Full tier before planning, or when divergent thinking is needed to explore multiple solution directions.
invocation: agent
---

# Brainstorm

Apply four structured ideation techniques to a problem and produce at least three concrete options with one recommended direction. Use this in the Full tier before planning, or whenever divergent thinking is needed.

## Techniques

### 1. Pattern Spotting

Identify recurring patterns, prior art, and analogies from similar problems. Search the codebase and broader ecosystem for how comparable challenges have been solved before. Extract transferable patterns and adapt them to the current context.

Output: 2-3 relevant patterns with source references and applicability notes.

### 2. Paradox Hunting

Find contradictions, tensions, and competing constraints in the requirements. Surface tradeoffs that are not immediately obvious. Ask: what two desirable properties conflict? What assumption, if reversed, would change the solution space?

Output: 1-3 paradoxes or tensions with brief explanation of why they matter.

### 3. Naming the Unnamed

Identify implicit concepts, hidden abstractions, or emergent entities that the current design does not name. When a cluster of behavior lacks a name, it often signals a missing abstraction. Giving it a name makes it discussable and designable.

Output: 1-3 named concepts with proposed definitions and scope.

### 4. Contrast Creation

Generate deliberately different approaches that span the solution space. Ensure at least one conservative option (minimal change), one ambitious option (rethink the approach), and one unconventional option (challenge assumptions). The goal is breadth, not convergence.

Output: 3+ distinct approaches with key differentiators highlighted.

## Output Format

Present results as a structured document:

```markdown
## Brainstorm: [Topic]

### Patterns Found
- [pattern]: [source] — [applicability]

### Tensions Identified
- [tension]: [why it matters]

### Named Concepts
- [name]: [definition]

### Options
1. **[Conservative option]** — [description, tradeoffs]
2. **[Ambitious option]** — [description, tradeoffs]
3. **[Unconventional option]** — [description, tradeoffs]

### Recommendation
[Which option and why, with conditions that would change the recommendation]
```

## When to Use Brainstorm vs. Debate

- **Brainstorm** generates divergent options. Use when the solution space is unexplored and multiple directions are viable.
- **Debate** evaluates and stress-tests a narrower set of options. Use after brainstorming to select among the generated options, or when two clear alternatives already exist.

A common Full-tier sequence: brainstorm first to generate options, then debate to select among them.
