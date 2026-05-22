---
name: write-howto
description: >
  Create task-oriented documentation for accomplishing specific goals.
  PROACTIVELY activate for: (1) procedures and recipes, (2) quick reference guides,
  (3) troubleshooting guides, (4) operational runbooks.
  Triggers: "write howto", "how to guide", "procedure", "recipe", "quick guide",
  "step by step", "instructions for"
argument-hint: [task]
---

# Write How-To

Generate task-oriented documentation optimized for the Developer persona.

## When to Use

Use this skill when you need documentation that:
- Helps accomplish a specific, concrete task
- Assumes the reader already knows WHY they want to do this
- Provides copy-paste ready solutions
- Gets the reader to their goal as fast as possible

## Workflow

Invoke the `create-documentation` skill for: "$ARGUMENTS"

### Parameters to Apply

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| `doc_type` | how_to | Task-oriented, goal-focused |
| `persona` | developer | Time-pressured, wants essentials |
| `reading_level` | grade_12 | Technical but scannable |
| `include_examples` | true | Copy-paste ready code |
| `validation_depth` | standard | Focus on task completion |

### Required Elements

1. **Clear goal statement** - What will they accomplish?
2. **Prerequisites** - What must be in place before starting?
3. **Numbered steps** - Imperative verbs, one action per step
4. **Copy-paste code** - Ready to use, not pseudocode
5. **Expected outcome** - How to verify success
6. **Links to related guides** - For context they might need

### Cognitive Load Management

- **Intrinsic**: Assume away - reader already understands the domain
- **Extraneous**: Eliminate - no explanations unless critical to success
- **Germane**: Optional - link to explanations for those who want depth

## Output Format

The generated how-to should follow this structure:

```markdown
# How to [Accomplish Task]

> **Goal**: [One sentence describing the outcome]

## Prerequisites

- [Requirement 1]
- [Requirement 2]

## Steps

### 1. [First Action]

[Brief context if absolutely necessary]

```[language]
[Copy-paste ready code]
```

### 2. [Second Action]

```[language]
[Copy-paste ready code]
```

### 3. [Third Action]
...

## Verify It Worked

[How to confirm success]

## Related Guides

- [Link to related how-to]
- [Link to explanation for context]
```

## Quality Gates

- [ ] Goal stated in one sentence
- [ ] Prerequisites are actionable items
- [ ] Steps use imperative verbs ("Run", "Create", "Add")
- [ ] Code blocks are copy-paste ready
- [ ] Verification step included
- [ ] No unnecessary explanations (link instead)
- [ ] Scannable structure (reader can skim to relevant step)
