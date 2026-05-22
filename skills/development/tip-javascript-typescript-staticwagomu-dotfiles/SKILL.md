---
name: tip-javascript-typescript
description: This skill should be used when writing or refactoring TypeScript/JavaScript code. It provides coding patterns and best practices aligned with the user's preferred development style, typescript language usage patterns, and library-specific tips.
---

# TypeScript/JavaScript Coding Techniques

## Overview

Apply the user's preferred TypeScript/JavaScript coding techniques automatically when writing or refactoring code. This skill encapsulates coding patterns, best practices, and architectural decisions to ensure consistency with the user's mental model and development philosophy.

## When to Use

Use this skill automatically in the following scenarios:

- Writing new TypeScript/JavaScript code
- Refactoring existing TypeScript/JavaScript code
- Planning improvements of code quality
  - e.g. reduce duplication, improve readability, enhance maintainability, etc.
- Reviewing code for improvements
- Making architectural decisions in TypeScript/JavaScript projects

Apply these techniques proactively as the default approach.

## Reference Structure

Coding techniques and tips are organized into two categories:

### `references/typescript/` - Language-Level Patterns

TypeScript/JavaScript language syntax, patterns, and best practices.

See `references/typescript/README.md` for details.

### `references/libraries/` - Library-Specific Tips

Usage patterns, optimizations, and gotchas for specific libraries and frameworks.

See `references/libraries/README.md` for details.

## Usage

When writing TypeScript/JavaScript code, load and apply patterns from the relevant reference files automatically. Reference files contain template sections for adding new patterns as they emerge.

## How to add new patterns

READ each reference categories' README to file place / naming conventions.
It also includes DOs and DON'Ts for writing new patterns.

Use this template for tip files.

```markdown
# [Topic Name]

## Overview

[Brief description and why these tips are needed]

## Basic Patterns

### [Pattern Name]

**When to use**: [Description of use case]

**Example**:

\`\`\`typescript
// ✅ Good: Recommended pattern
// Code example
\`\`\`

**Anti-pattern to avoid**:

\`\`\`typescript
// ❌ Bad: What to avoid
// Anti-pattern example
\`\`\`

**Notes**: [Additional context, edge cases, considerations]

## Common Issues & Solutions

### [Issue Title]

**Problem**: [What goes wrong]

**Solution**:

\`\`\`typescript
// Solution code
\`\`\`

## Performance Optimization

[If applicable]

## Type Usage

[TypeScript type patterns for this library]

## References

- Official docs: [URL]
- Related articles: [URL]
```
