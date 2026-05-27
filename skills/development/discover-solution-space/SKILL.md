---
name: discover-solution-space
description: Use when research phase is complete and you need to explore implementation
  options before planning. Triggers after /research, when facing architectural decisions,
  or when multiple valid approaches exist for a task.
argument-hint: <optional: file path or issue number containing research>
---

# Discover Solution Space

Deeply explore the solution space to find the optimal approach before committing to a plan.

## Position in Workflow

Step 2 of development workflow:
1. `/research` - Understand problem, explore implementation
2. `/discover_solution_space` - Explore solutions (THIS)
3. Plan Mode - Create implementation plan
4. Code, review, ship

## Core Principle

**Comprehensive exploration. High-quality decisions.**

You have a bias toward finishing quickly. Resist it. The cost of choosing a suboptimal solution compounds over time. Rushed decisions degrade codebases.

Spend significant time on:
- Understanding the codebase architecture
- Generating multiple options
- Analyzing trade-offs thoroughly

**Quality over speed.** This is the moment to think hard.

## Input

**Default:** Use research findings from the current conversation.

**If argument provided:**
- File path: Read the file for research context
- GitHub issue: Fetch with `gh issue view $ARG --comments`

## Workflow

### 1. Gather Context

**From research:** Understand the problem, requirements, and constraints.

**From codebase:** Invest significant time exploring:
- Existing architecture and patterns
- Related implementations (how similar problems were solved)
- Dependencies and integration points
- Code conventions and style
- Test patterns

**Do not rush this.** Thorough codebase understanding prevents solutions that fight the existing architecture.

### 2. Ask Clarifying Questions

Before exploring solutions, ask about anything that improves decision quality:
- Business goals and priorities
- How the feature will be used
- Performance requirements
- Future extensibility needs
- Constraints (timeline, compatibility, etc.)
- Strategic direction

**Do not assume.** Bad assumptions lead to suboptimal solutions.

### 3. Deep Exploration

Generate multiple solutions across these dimensions:

| Dimension | Examples |
|-----------|----------|
| **Architectural approach** | Event-driven vs request-response, monolith vs service |
| **Implementation strategy** | Extend existing class vs new module, refactor vs add |
| **Library/tool choice** | Redis vs in-memory, REST vs GraphQL |
| **Feature design** | Wizard flow vs single form, eager vs lazy loading |

**Generate at least 3-5 distinct approaches** before evaluating. Don't anchor on the first idea.

### 4. First Principles Check

For each solution, challenge assumptions:

- **Do we need this?** Is the feature/change actually necessary?
- **Are requirements correct?** Should we push back on any constraints?
- **Are existing patterns optimal?** Or should we challenge/improve them?
- **What's the simplest solution?** Complexity should be justified.
- **What would we regret?** In 6 months, what would we wish we'd done differently?

### 5. Analyze Trade-offs

For each viable solution, evaluate:

- **Pros:** Benefits, strengths, what it enables
- **Cons:** Drawbacks, risks, what it complicates
- **Codebase fit:** How well it aligns with existing architecture
- **Effort:** Relative complexity (low/medium/high)
- **Reversibility:** How hard to change course later

### 6. Present and Discuss

Present ranked options. Engage with user feedback until a solution is chosen.

## Output Format

```
## Solution Space Analysis

### Context Summary
[Brief restatement of problem and key constraints from research]

### Clarifying Questions
[Questions about strategy, usage, or requirements - if any]

---

### Options

#### Option 1: [Name] - Recommended
[Description]

**Pros:**
- ...

**Cons:**
- ...

**Codebase fit:** [How it aligns with existing patterns]
**Effort:** [Low/Medium/High]
**Reversibility:** [Easy/Moderate/Hard to change later]

#### Option 2: [Name]
[Same structure]

#### Option 3: [Name]
[Same structure]

---

### Recommendation
[Why Option 1 is recommended, and under what conditions you'd choose differently]

### Open Questions
[Anything that could change the recommendation]

### Next Step
Ready to plan implementation. Enter Plan Mode or run `/plan`
```

## Explicit Depth Instructions

**Spend significant time on this task.**

Read more files than feels necessary. Generate more options than feels necessary. Analyze trade-offs more thoroughly than feels necessary.

This is not the place to be efficient. This is the place to be thorough.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Anchoring on first idea | Generate 3-5 options BEFORE evaluating any |
| Shallow codebase exploration | Read related files, understand patterns first |
| Assuming requirements | Ask clarifying questions early |
| Rushing to recommendation | Spend time on trade-off analysis |
| Not challenging assumptions | Apply first principles check to every option |
| Fighting the codebase | Ensure solutions fit existing architecture |
| Skipping "do we need this?" | Always question if the change is necessary |

## What NOT to Do

- Do NOT rush through exploration
- Do NOT present only one option
- Do NOT skip the first principles check
- Do NOT ignore existing codebase patterns
- Do NOT make assumptions without asking
- Do NOT proceed to planning until user chooses a solution
