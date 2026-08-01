---
name: ai-optimization
description: 'Optimize input context for AI consumption using context engineering
  principles. Use when: (1) User wants to optimize content for AI/Claude explicitly,
  (2) User invokes with --foryou flag.'
---

---
name: ai-optimization
description: Optimize input context for AI consumption using context engineering principles. Use when: (1) User wants to optimize content for AI/Claude explicitly, (2) User invokes with --foryou flag.
allowed-tools: Read, Write, TodoWrite
---

# Context Engineering Optimizer

Optimize content for AI consumption by reducing tokens while preserving essential information.

## Core Principle

Context is finite. Every token depletes the attention budget. Optimize ruthlessly.

Reference: [context-engineering-guide.md](references/context-engineering-guide.md)

## Optimization Workflow

Use TodoWrite

### Step 1: Create Draft

Analyze input and create optimized version:

**Remove/Reduce**:
- Redundant explanations (AI already knows common knowledge)
- Verbose transitions ("In this section, we will discuss...")
- Duplicate information across sections
- Filler words and phrases
- Overly detailed examples when one suffices
- Charts/diagrams/tables if text conveys same info more efficiently

**Preserve**:
- Domain-specific knowledge AI lacks
- Concrete examples that demonstrate behavior
- Critical constraints and rules
- Structural organization (headers, sections)
- Actionable instructions

**Format choices**:
- Prefer bullet points over prose
- Use imperative form
- Choose text OR graphical representation, not both
- Keep code examples minimal but complete

**Language**:
- English no matter the original language unless otherwise specified through prompt
- Most token-efficient for current models
- Preserves technical terminology accuracy

**XML + Markdown tables**:

```markdown
<!-- WRONG -->
<data>
| Col | Val |
|-----|-----|
| A   | B   |
</data>

<!-- CORRECT - empty lines required -->
<data>

| Col | Val |
|-----|-----|
| A   | B   |

</data>
```

### Step 2: Compare and Refine

Compare draft against original:

**Check for information loss**:
- Critical details missing?
- Context for understanding removed?
- Edge cases dropped that matter?

**Check for over-optimization**:
- Can sections be further condensed?
- Any remaining redundancy?
- Self-evident comments still present?

**Restore if**:
- Meaning becomes ambiguous
- Important nuance lost
- Actionability reduced

### Step 3: Output

**For materials (files to overwrite)**:
- Overwrite original with optimized version

**For transient content**:
- Output the optimized version as final result

## Quality Criteria

Optimized content should:
- Reduce token count by 30-70% typically
- Preserve all actionable information
- Maintain clear structure
- Be self-contained (no dangling references)
- Target the Goldilocks zone: specific enough to guide, flexible enough to adapt
