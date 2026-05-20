---
name: brainstorm-solutions
description: Generate multiple viable solution options after research is complete, before converging on a single approach. Use when you need to explore the solution space, ask clarifying questions, and produce 3-5 distinct options to consider.
---

# Brainstorm Solutions

Explore the solution space broadly before committing to a single path.

## Position in Workflow

Step 2 of development workflow:
1. `/research` - Understand problem and constraints
2. `/brainstorm-solutions` - Explore solution space (THIS)
3. `/design-solution` - Converge on a single solution
4. Plan, code, review, ship

## Core Principle

**Breadth first.** Generate multiple distinct options before evaluating or ranking them.

## Input

**Default:** Use research findings from the current conversation.

**If argument provided:**
- File path: Read the file for research context
- GitHub issue: Fetch with `gh issue view $ARG --comments`

## Workflow

### 1. Gather Context

- Summarize the problem, constraints, and goals from research.
- Identify existing architecture patterns and similar implementations.

### 2. Ask Clarifying Questions

Ask only what improves solution quality:
- Business goals and priorities
- User workflows and usage patterns
- Performance or scalability requirements
- Extensibility or future roadmap considerations
- Hard constraints (timeline, compatibility, cost)

### 3. Generate Options

Generate at least 3-5 distinct approaches across dimensions:

| Dimension | Examples |
|-----------|----------|
| **Architectural approach** | Event-driven vs request-response, monolith vs service |
| **Implementation strategy** | Extend existing module vs new module, refactor vs add |
| **Library/tool choice** | Redis vs in-memory, REST vs GraphQL |
| **Feature design** | Wizard flow vs single form, eager vs lazy loading |

Avoid anchoring on the first idea. Expand, then refine.

### 4. First Principles Check

For each option, challenge assumptions:
- Do we need this?
- Are requirements correct?
- Are existing patterns optimal?
- What is the simplest viable solution?
- What would we regret in 6 months?

## Output Format

```
## Solution Brainstorm

### Context Summary
[Brief restatement of problem and key constraints]

### Clarifying Questions
[Questions about strategy, usage, or requirements - if any]

---

### Options

#### Option 1: [Name]
[Description]

#### Option 2: [Name]
[Description]

#### Option 3: [Name]
[Description]

[Add Option 4/5 if useful]

---

### Notes
[Any assumptions or risks that should be validated before choosing]

### Next Step
Ready to converge on a single solution. Run `/design-solution`.
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Anchoring on first idea | Generate 3-5 options BEFORE evaluating any |
| Shallow codebase exploration | Read related files and patterns first |
| Assuming requirements | Ask clarifying questions early |
| Skipping first principles | Apply first principles to each option |
| Rushing to recommendation | Save evaluation for design-solution |

## What NOT to Do

- Do NOT present only one option
- Do NOT recommend a solution yet
- Do NOT skip clarifying questions when uncertainty exists
- Do NOT ignore existing codebase patterns
