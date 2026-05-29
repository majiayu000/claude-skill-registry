---
name: analyze-performance
description: Evaluation framework for analyzing decision-making quality across five dimensions.
user-invocable: false
---

# Analyze Performance

Evaluate a development branch's decision-making quality.

## Evaluation Framework

Evaluate the developer's decision-making across five dimensions. For each, provide:

- A rating: Strong / Adequate / Needs Improvement
- 1-2 sentences of evidence-based analysis

### 1. Consistency

Did decisions follow established patterns? Were similar problems solved similarly? Did pivots converge toward better solutions rather than oscillate indecisively?

### 2. Intuitivity

Were solutions obvious and easy to understand? Did decisions align with common expectations? Would another developer find the choices natural?

### 3. Describability

Did final names land well? Were naming improvements made when better options were discovered? Did terminology avoid semantic conflicts and support future extension?

### 4. Agility

How well did the developer respond to unexpected issues? Did they iterate effectively, incorporating lessons learned into subsequent work? Were course corrections made quickly when needed?

### 5. Density

Does the code express meaning economically? Is the ratio of conceptual value to textual surface area high? Does the solution achieve its purpose without verbose scaffolding, redundant abstractions, or diluted semantics?

## Output Format

Return structured markdown:

```markdown
### Decision Quality Analysis

| Dimension      | Rating                            | Notes             |
| -------------- | --------------------------------- | ----------------- |
| Consistency    | Strong/Adequate/Needs Improvement | Brief observation |
| Intuitivity    | ...                               | ...               |
| Describability | ...                               | ...               |
| Agility        | ...                               | ...               |
| Density        | ...                               | ...               |

**Strengths**: [Key positive patterns observed]

**Areas for Improvement**: [Constructive suggestions]
```

## Guidelines

- Be fair and constructive
- Base ratings on evidence from tickets and commits
- Highlight both strengths and improvement areas
- Keep analysis concise (150-250 words total)
- Value iteration over perfection: mid-stream improvements indicate healthy development practice, not poor planning
- Penalize only oscillation (changing back and forth) not convergence (steadily improving toward better solutions)
- When noting design changes, distinguish between productive iteration (good) and indecisive oscillation (needs improvement)
- Density evaluates the expressiveness of the software artifact itself, not development process metrics (commit count, frequency). High-density code packs meaning into minimal structure. Low-density code spreads thin concepts across verbose implementations.
