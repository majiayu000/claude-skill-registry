---
name: example-complete-skill
description: This skill should be used when the user asks to "perform complex task", "implement advanced pattern", "handle multiple scenarios", or needs comprehensive guidance with validation tools. Demonstrates full-featured skill structure.
compatibility: opencode
---

# Example Complete Skill

## When to Use This Skill

### Primary Triggers (Explicit)

Use this skill when the user says:
- "perform complex task"
- "implement advanced pattern"
- "handle multiple scenarios"
- "need comprehensive validation"

### Contextual Triggers (Implicit)

Use this skill when:
- Domain is complex with multiple patterns
- Users need both basic and advanced guidance
- Validation and testing are important
- Task has many edge cases or variations

## Purpose

Provide comprehensive guidance for complex tasks that require:
- Core concepts and workflows in SKILL.md
- Extensive reference documentation
- Multiple working examples for different scenarios
- Validation and testing utilities

## Core Concepts

### Concept 1: Fundamental Pattern

The foundational approach for this domain:

```
[Brief explanation with essential code]
```

Key principles:
- Principle 1 - Core idea
- Principle 2 - Core idea
- Principle 3 - Core idea

### Concept 2: Standard Workflow

The recommended workflow:

1. **Preparation** - Set up requirements
2. **Implementation** - Apply core pattern
3. **Validation** - Verify correctness
4. **Testing** - Ensure reliability
5. **Iteration** - Refine based on results

### Concept 3: Advanced Patterns

For complex scenarios, see `references/advanced.md`.

Quick overview:
- Pattern A - For scenario X
- Pattern B - For scenario Y
- Pattern C - For scenario Z

## Quick Reference

### Common Tasks

| Task | Command | Notes |
|------|---------|-------|
| Basic validation | `./scripts/validate.sh` | Quick check |
| Full validation | `./scripts/validate.sh --strict` | Comprehensive |
| Run tests | `./scripts/test.sh` | All scenarios |
| Check structure | `./scripts/check-structure.sh` | File organization |

### Key Patterns

| Pattern | Use When | Example |
|---------|----------|---------|
| Pattern A | Scenario X | `examples/basic-example.sh` |
| Pattern B | Scenario Y | See `references/patterns.md` |
| Pattern C | Scenario Z | See `references/advanced.md` |

## Validation

Verify implementation using provided scripts:

```bash
# Basic structure validation
./scripts/validate.sh path/to/implementation

# Strict validation (all checks)
./scripts/validate.sh --strict path/to/implementation

# Run full test suite
./scripts/test.sh path/to/implementation
```

Manual validation checklist:
- [ ] Structure matches requirements
- [ ] Core concepts applied correctly
- [ ] Edge cases handled
- [ ] Tests pass
- [ ] Documentation complete

## Additional Resources

### Reference Files

Detailed documentation in `references/`:

- **`references/patterns.md`** - Comprehensive pattern catalog with examples
- **`references/advanced.md`** - Advanced techniques and edge cases
- **`references/troubleshooting.md`** - Common issues and solutions
- **`references/migration.md`** - Upgrading from older approaches (if applicable)

### Working Examples

Complete examples in `examples/`:

- **`examples/basic-example.sh`** - Simple implementation for common case
- **`examples/intermediate-example.sh`** - Moderate complexity scenario
- **`examples/advanced-example.sh`** - Complex scenario with edge cases
- **`examples/complete-example/`** - Full-featured implementation

### Utility Scripts

Tools in `scripts/`:

- **`scripts/validate.sh`** - Structure and correctness validation
- **`scripts/test.sh`** - Automated testing utility
- **`scripts/check-structure.sh`** - File organization checker
- **`scripts/generate-template.sh`** - Scaffold new implementation

## Progressive Disclosure

This skill uses three-level loading:

1. **Always loaded**: This SKILL.md with core concepts (~2,000 words)
2. **Load as needed**: Reference files for detailed patterns
3. **Copy/execute**: Examples and scripts when required

Keep SKILL.md focused on essential workflows. Move detailed content to references/.

## Summary

This complete skill structure provides:
- Lean SKILL.md with essential concepts (1,500-2,500 words)
- Comprehensive reference documentation (in references/)
- Multiple working examples (in examples/)
- Validation and testing utilities (in scripts/)
- Progressive disclosure for efficient context usage

Use this structure for complex domains requiring extensive documentation and tooling.
