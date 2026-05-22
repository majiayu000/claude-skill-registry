---
name: code-explanation
description: Explains complex code through clear narratives, visual diagrams, and step-by-step breakdowns. Use when user asks to explain code, understand algorithms, analyze design patterns, wants code walkthroughs, or mentions "explain this code", "how does this work", "code breakdown", or "understand this function".
---

# Code Explanation

Expert skill for explaining complex code to developers at all levels through visual aids, step-by-step breakdowns, and progressive complexity.

## Quick Start

### 1. Analyze Complexity First

Before explaining, assess the code:
- **Lines of code** and structural complexity
- **Concepts used** (async, decorators, generators, etc.)
- **Design patterns** present
- **Difficulty level** (beginner/intermediate/advanced)

### 2. Choose Explanation Depth

| Audience | Approach |
|----------|----------|
| Beginner | Start with analogies, avoid jargon, explain fundamentals |
| Intermediate | Focus on patterns and design decisions |
| Advanced | Deep dive into implementation details and trade-offs |

### 3. Use Visual Aids

Generate Mermaid diagrams for:
- **Flow diagrams** - Control flow and decision trees
- **Class diagrams** - Object relationships and inheritance
- **Sequence diagrams** - Method calls and interactions

### 4. Progressive Disclosure

Structure explanations from simple to complex:
1. **Overview** - What does this code do? (1-2 sentences)
2. **Key Concepts** - What programming concepts are used?
3. **Step-by-Step** - Walk through the logic
4. **Deep Dive** - Advanced details for those who want more

## Output Format

### Standard Explanation Structure

```markdown
## What This Code Does
[1-2 sentence summary]

## Key Concepts
- Concept 1: Brief explanation
- Concept 2: Brief explanation

## Visual Overview
[Mermaid diagram if complexity warrants]

## Step-by-Step Breakdown
1. [First step with code reference]
2. [Second step with code reference]
...

## Common Questions
- Why is X done this way?
- What happens if Y?

## Related Patterns
[Links to similar patterns or alternatives]
```

## Core Techniques

### Explaining Algorithms
1. State the problem being solved
2. Show input → output transformation
3. Visualize with step-by-step execution
4. Analyze time/space complexity

### Explaining Design Patterns
1. Name the pattern
2. Explain the problem it solves
3. Show UML-style diagram
4. List benefits and trade-offs

### Explaining Complex Functions
1. Signature and purpose
2. Parameter meanings
3. Return value
4. Side effects (if any)
5. Edge cases

## Best Practices

- **Use analogies** - Compare to real-world concepts
- **Show, don't just tell** - Include code snippets
- **Reference line numbers** - Use `file_path:line_number` format
- **Highlight gotchas** - Point out non-obvious behavior
- **Suggest improvements** - When appropriate

## Resources

- [WORKFLOW.md](WORKFLOW.md) - Detailed step-by-step methodology
- [EXAMPLES.md](EXAMPLES.md) - Comprehensive explanation examples

## Integration

This skill auto-invokes when triggered by explanation-related keywords. For explicit control, use the `/code-explain` command.
