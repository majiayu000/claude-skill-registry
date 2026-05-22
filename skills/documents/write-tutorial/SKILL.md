---
name: write-tutorial
description: >
  Create learning-oriented documentation following Diataxis framework.
  PROACTIVELY activate for: (1) teaching new concepts, (2) onboarding guides,
  (3) getting started documentation, (4) step-by-step learning paths.
  Triggers: "write tutorial", "create tutorial", "onboarding guide", "getting started",
  "teach me", "learning guide", "beginner guide"
argument-hint: [topic]
---

# Write Tutorial

Generate learning-oriented documentation optimized for the Anxious Novice persona.

## When to Use

Use this skill when you need documentation that:
- Teaches a new concept or skill from scratch
- Guides a beginner through their first experience
- Builds understanding progressively
- Includes verification points so readers know they're on track

## Workflow

Invoke the `create-documentation` skill for: "$ARGUMENTS"

### Parameters to Apply

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| `doc_type` | tutorial | Learning-oriented, teaches by doing |
| `persona` | anxious_novice | Worried reader who needs reassurance |
| `reading_level` | grade_12 | Accessible but not condescending |
| `include_examples` | true | Concrete examples aid learning |
| `validation_depth` | comprehensive | Tutorials need thorough validation |

### Required Elements

1. **Start with an analogy** - Connect new concept to something familiar
2. **Clear prerequisites** - What must the reader know/have before starting?
3. **Step-by-step progression** - One concept at a time, building on previous
4. **Verification points** - "If you see X, you're on track" checkpoints
5. **Recovery paths** - What to do if something goes wrong
6. **Working example** - Complete, runnable code they can copy

### Cognitive Load Management

- **Intrinsic**: Manage carefully - sequence concepts from simple to complex
- **Extraneous**: Minimize aggressively - no jargon, clear language
- **Germane**: Maximize - analogies, examples, reflection prompts

## Output Format

The generated tutorial should follow this structure:

```markdown
# [Tutorial Title]

## What You'll Learn
- [Outcome 1]
- [Outcome 2]

## Prerequisites
- [Requirement 1]
- [Requirement 2]

## [Step 1: First Concept]
[Analogy to introduce concept]
[Explanation]
[Example]
[Verification: "You should see..."]

## [Step 2: Building On Step 1]
...

## Troubleshooting
[Common issues and recovery paths]

## Next Steps
[Where to go from here]
```

## Quality Gates

- [ ] Analogy present in introduction
- [ ] Prerequisites clearly stated
- [ ] Each step has verification point
- [ ] Recovery paths for common errors
- [ ] No assumed knowledge beyond prerequisites
- [ ] Code examples are complete and runnable
