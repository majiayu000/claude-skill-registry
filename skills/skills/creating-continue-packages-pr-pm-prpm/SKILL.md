---
name: creating-continue-packages
description: Use when creating Continue rules - provides required name field, alwaysApply semantics, glob/regex patterns, and markdown format with optional frontmatter
---

# Creating Continue Packages

## Overview

Continue uses markdown files with YAML frontmatter in `.continuerules/*.md` or YAML configuration in `config.yaml`. Rules are context-aware using glob patterns, regex matching, or always-applied globally.

**CRITICAL**: The `name` field is REQUIRED in frontmatter (unlike other formats where it's optional).

## Quick Reference

### Required Frontmatter

```yaml
---
name: Rule display name (REQUIRED)
---
```

### Optional Frontmatter

```yaml
description: Description of when rule should be used
globs: "**/*.{ts,tsx}"  # String or array
regex: "^import .* from '.*';$"  # String or array
alwaysApply: true  # true, false, or undefined
version: "1.0.0"
schema: "v1"
```

## AlwaysApply Semantics

| Value | Behavior |
|-------|----------|
| `true` | Always included, regardless of context |
| `false` | Included if globs match OR agent decides based on description |
| `undefined` (default) | Included if no globs exist OR globs match |

## Creating Rules with Globs

Glob patterns match file paths:

```markdown
---
name: Documentation Standards
globs: docs/**/*.{md,mdx}
alwaysApply: false
description: Standards for writing and maintaining documentation
---

# Documentation Standards

## Structure

- Follow consistent heading hierarchy starting with h2 (##)
- Include YAML frontmatter with title, description, and keywords
- Use descriptive alt text for images

## Writing Style

- Keep paragraphs concise and scannable
- Use code blocks with appropriate language tags
- Include cross-references to related documentation
```

### Glob Patterns (String or Array)

```yaml
# Single pattern (string)
globs: "**/*.{ts,tsx}"

# Multiple patterns (array)
globs:
  - "src/**/*.ts"
  - "tests/**/*.ts"
```

## Creating Rules with Regex

Regex patterns match file content:

```markdown
---
name: React Component Standards
regex: "^import React"
globs: "**/*.{tsx,jsx}"
alwaysApply: false
description: Standards for React component development
---

# React Component Standards

## Component Structure

- Use functional components with hooks
- Keep components under 200 lines
- Extract logic into custom hooks when appropriate
- Co-locate styles with components

## Examples

\`\`\`typescript
// Good: Focused component
function UserProfile({ userId }: Props) {
  const user = useUser(userId);
  return <div>{user.name}</div>;
}
\`\`\`
```

### Regex Patterns (String or Array)

```yaml
# Single pattern (string)
regex: "^import .* from '.*';$"

# Multiple patterns (array)
regex:
  - "^import .*"
  - "^export .*"
```

## Creating Always-Applied Rules

Rules that apply to all files in the project:

```markdown
---
name: Code Quality Standards
alwaysApply: true
---

# Code Quality Standards

These standards apply to all code in the project.

## General Principles

- Write self-documenting code
- Keep functions under 50 lines
- Use meaningful variable names
- Add comments only for complex logic
```

## YAML Configuration Format

Alternative to markdown files in `.continuerules/`:

```yaml
name: API Development Rules
version: 1.0.0
schema: v1

rules:
  - name: REST API Standards
    globs:
      - "src/api/**/*.ts"
      - "src/routes/**/*.ts"
    alwaysApply: false
    rule: >
      ## REST Conventions

      - Use semantic HTTP methods (GET, POST, PUT, DELETE)
      - Return appropriate status codes (200, 201, 400, 404, 500)
      - Include error messages in response body
      - Version APIs using URL paths (/api/v1/)

  - name: TypeScript Standards
    globs: "**/*.{ts,tsx}"
    regex: "^import.*typescript"
    alwaysApply: false
    rule: >
      ## Type Safety

      - Always define explicit types for function parameters
      - Avoid using `any` type
      - Use strict mode in tsconfig.json
```

## Common Glob Patterns

```yaml
globs:
  - "**/*.ts"           # All TypeScript files
  - "src/**/*.tsx"      # React components in src/
  - "**/*.{ts,tsx}"     # Multiple extensions
  - "tests/**/*"        # All files in tests/
  - "*.config.js"       # Config files in root
  - "docs/**/*.md"      # Documentation files
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Missing name field | Name is REQUIRED in Continue frontmatter |
| Using MDC format | Continue uses plain markdown, not MDC |
| Complex frontmatter | Keep frontmatter minimal (name + optional fields) |
| Mixing alwaysApply semantics | Understand true/false/undefined behavior |

## When to Use Each Approach

**alwaysApply: true** - Core standards that influence all code generation:
- Workspace-wide standards
- Technology preferences
- Security policies
- Universal coding conventions

**globs with alwaysApply: false** - Domain-specific standards:
- Component patterns
- API design rules
- Testing approaches
- Deployment procedures

**No globs (undefined alwaysApply)** - Agent-decided relevance:
- Let agent determine when to include based on description
- Flexible application based on context

## Content Format

Plain markdown after frontmatter:

- **H1 title**: Main heading
- **H2/H3 sections**: Organize content
- **Lists**: Rules and guidelines
- **Code blocks**: Examples with language tags
- **Standard markdown**: Bold, italic, links

## Validation

Schema location: `/Users/khaliqgant/Projects/prpm/app/packages/converters/schemas/continue.schema.json`

Documentation: `/Users/khaliqgant/Projects/prpm/app/packages/converters/docs/continue.md`

## Best Practices

1. **Always include name**: Required field, not optional
2. **Be specific**: Target actual patterns in your codebase
3. **Include examples**: Show real code from your project
4. **Update regularly**: Keep rules in sync with codebase changes
5. **One concern per file**: Split large rule sets into focused files
6. **Understand alwaysApply**: Choose true/false/undefined based on use case

## Example: Complete Rule File

```markdown
---
name: TypeScript Type Safety
description: Type safety standards for TypeScript code
globs:
  - "**/*.ts"
  - "**/*.tsx"
alwaysApply: false
---

# TypeScript Type Safety Standards

## Type Definitions

- Always define explicit types for function parameters
- Avoid using `any` type
- Use `unknown` instead of `any` for truly unknown types
- Define return types for public functions

## Examples

\`\`\`typescript
// ❌ Bad: Using any
function processData(data: any): any {
  return data.value;
}

// ✅ Good: Explicit types
interface DataInput {
  value: string;
}

function processData(data: DataInput): string {
  return data.value;
}
\`\`\`

## Type Guards

Use type guards for narrowing:

\`\`\`typescript
function isString(value: unknown): value is string {
  return typeof value === 'string';
}
\`\`\`
```

---

**Remember**: Continue REQUIRES `name` field in frontmatter. Use globs/regex for file matching. Understand alwaysApply semantics (true/false/undefined).
