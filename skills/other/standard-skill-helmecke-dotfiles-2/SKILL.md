---
name: example-standard-skill
description: This skill should be used when the user asks to "perform standard task", "follow best practices", "implement common pattern", or needs comprehensive guidance. Demonstrates recommended skill structure with progressive disclosure.
compatibility: opencode
---

# Example Standard Skill

## When to Use This Skill

### Primary Triggers (Explicit)

Use this skill when the user says:
- "perform standard task"
- "follow best practices"
- "implement common pattern"
- "show me comprehensive example"

### Contextual Triggers (Implicit)

Use this skill when:
- Task requires multiple steps
- Users need both overview and detailed guidance
- Working examples would be helpful
- Domain has established patterns

## Purpose

Provide comprehensive guidance for a moderately complex task that benefits from:
- Core concepts in SKILL.md
- Detailed documentation in references/
- Working examples users can copy

## Core Concepts

### Concept 1: Essential Pattern

The fundamental approach:

```
[Brief explanation of core pattern]
```

Key principles:
- Principle 1
- Principle 2
- Principle 3

### Concept 2: Common Workflow

Standard workflow for this task:

1. Preparation step
2. Implementation step
3. Validation step
4. Iteration step

### Concept 3: Best Practices

Essential best practices:
- Practice 1 - Brief explanation
- Practice 2 - Brief explanation
- Practice 3 - Brief explanation

For detailed patterns and advanced techniques, see references/.

## Quick Reference

| Task | Approach |
|------|----------|
| Common task 1 | Brief guidance |
| Common task 2 | Brief guidance |
| Common task 3 | Brief guidance |

## Validation

Verify implementation by:
- Checking structure matches patterns
- Testing with provided examples
- Running validation if available

## Additional Resources

### Reference Files

For detailed guidance, consult:
- **`references/detailed-guide.md`** - Comprehensive patterns and techniques
- **`references/advanced-patterns.md`** - Advanced use cases (if needed)
- **`references/troubleshooting.md`** - Common issues (if needed)

### Working Examples

Complete examples in `examples/`:
- **`basic-example.sh`** - Simple implementation
- **`advanced-example.sh`** - Complex implementation (if needed)

### Utility Scripts

Tools in `scripts/` (if applicable):
- **`validate.sh`** - Validation utility
- **`test.sh`** - Testing utility

## Summary

This standard skill structure provides:
- Lean SKILL.md with core concepts (1,500-2,000 words)
- Detailed documentation in references/
- Working examples users can copy
- Progressive disclosure for efficient context use

Use this structure for most OpenCode skills.
