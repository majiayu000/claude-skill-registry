---
name: doc
description: Write or improve documentation using the Diataxis framework. Creates user-centered docs in four types - tutorials, how-to guides, reference, explanation. Use when writing docs, improving documentation, auditing docs, or when the user mentions Diataxis.
---

# Documentation Skill (Diataxis Framework)

Write documentation that serves user needs using the Diataxis framework.

## Quick Reference

| User Need | Doc Type | User Mode | Content Focus |
|-----------|----------|-----------|---------------|
| Learning | [Tutorial](./TUTORIAL.md) | Study | Action (doing) |
| Goal completion | [How-to Guide](./HOWTO.md) | Work | Action (doing) |
| Information lookup | [Reference](./REFERENCE.md) | Work | Cognition (knowing) |
| Understanding | [Explanation](./EXPLANATION.md) | Study | Cognition (knowing) |

## Decision Matrix

Use the [Diataxis Compass](./COMPASS.md) to determine doc type:

```
Is the content about ACTION or COGNITION?
├── ACTION (practical steps, doing)
│   ├── For ACQUISITION (study/learning) → Tutorial
│   └── For APPLICATION (work/tasks) → How-to Guide
└── COGNITION (theoretical knowledge, thinking)
    ├── For APPLICATION (work/tasks) → Reference
    └── For ACQUISITION (study/learning) → Explanation
```

## Instructions

### 1. Determine Documentation Type

**If type is specified:** Use that type directly.

**If audit is requested:** Analyze existing docs against Diataxis principles. Report:
- What type each doc appears to be
- Whether content matches its apparent type
- Boundary violations (e.g., explanation bleeding into reference)
- Gaps in coverage

**Otherwise, ask these questions:**
1. Does this inform the user's **action** (doing) or **cognition** (knowing)?
2. Does it serve **acquisition** (study) or **application** (work)?

### 2. Apply Type-Specific Guidelines

Read the detailed guide for your documentation type:
- [TUTORIAL.md](./TUTORIAL.md) - Learning-oriented lessons
- [HOWTO.md](./HOWTO.md) - Goal-oriented directions
- [REFERENCE.md](./REFERENCE.md) - Information-oriented descriptions
- [EXPLANATION.md](./EXPLANATION.md) - Understanding-oriented discussion

### 3. Key Principles (All Types)

**Do:**
- Focus on user needs, not product features
- Keep boundaries clear between doc types
- Link to other doc types rather than mixing content
- Use language appropriate to the doc type

**Don't:**
- Mix learning content with task guidance
- Add explanation where description is needed
- Include reference details in tutorials
- Blur boundaries between doc types

### 4. Structural Guidelines

**Naming conventions:**
- Tutorials: "Getting started with X", "Learn to X"
- How-to: "How to X", "Configuring X for Y"
- Reference: "X API", "X configuration options"
- Explanation: "About X", "Understanding X", "Why X"

**Landing pages** for each section should:
- Provide overview of contents
- Use headings and snippets (not just lists)
- Group related items (max 7 items per group)

## Common Anti-Patterns

| Problem | Symptom | Fix |
|---------|---------|-----|
| Tutorial-as-reference | Lists all options | Remove options, show one path |
| How-to-as-tutorial | Teaches concepts | Move teaching to tutorial/explanation |
| Reference-as-explanation | Discusses "why" | Move discussion to explanation |
| Explanation-in-tutorial | Long digressions | Link to explanation, keep minimal |

## Workflow Summary

1. **Identify** the user need (learning/goal/info/understanding)
2. **Select** doc type using the compass
3. **Read** the detailed guide for that type
4. **Write** following type-specific principles
5. **Review** for boundary violations
6. **Link** to related docs of other types

## Further Reading

- [COMPASS.md](./COMPASS.md) - Decision tool for doc type selection
- [QUALITY.md](./QUALITY.md) - Functional vs deep quality
- [WORKFLOW.md](./WORKFLOW.md) - Iterative improvement process
