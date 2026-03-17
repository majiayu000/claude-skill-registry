---
name: codebase-documenter
description: This skill should be used when writing documentation for codebases, including README files, architecture documentation, code comments, and API documentation. Use this skill when users request help documenting their code, creating getting-started guides, explaining project structure, or making codebases more accessible to new developers. The skill provides templates, best practices, and structured approaches for creating clear, beginner-friendly documentation.
---

# Codebase Documenter

Create comprehensive, beginner-friendly documentation for any codebase.

## When to Use

**Use for:**

- Writing or updating README files
- Creating architecture documentation
- Adding meaningful code comments
- Documenting APIs and endpoints
- Creating getting-started guides
- Explaining project structure

**Don't use when:**

- Code review → use `generic-code-reviewer`
- UX design decisions → use `generic-ux-designer`
- Adding code features → use `generic-feature-developer`

## Core Principles

1. **Start with "Why"** - Explain purpose before implementation
2. **Progressive Disclosure** - Simple to complex
3. **Provide Context** - Why code exists, not just what it does
4. **Include Examples** - Concrete usage for every concept
5. **Assume No Prior Knowledge** - Define terms, avoid jargon
6. **Visual Aids** - Diagrams, file trees, flowcharts
7. **Quick Wins** - Get something running in 5 minutes

## Documentation Workflow

1. **Analyze** - Entry points, dependencies, core concepts, configuration
2. **Choose Type** - README → Architecture → API → Comments
3. **Generate** - Use templates, customize for project
4. **Verify** - Read as beginner, test examples

## Documentation Types

### README (Project Entry Point)

```markdown
# Project Name

## What This Does

[1-2 sentence explanation]

## Quick Start

[< 5 minute setup]

## Project Structure

[Visual file tree]

## Key Concepts

[Core abstractions]

## Common Tasks

[Step-by-step guides]
```

### Architecture Documentation

```markdown
# Architecture Overview

## System Design

[High-level diagram]

## Data Flow

[How data moves through system]

## Key Design Decisions

[Why certain choices were made]

## Extension Points

[Where to add new features]
```

### Code Comments

```typescript
// ✅ GOOD - Explains WHY and context
// IndexedDB quota check: Prevents silent failures when storage is full.
// Without this, writes fail with cryptic QuotaExceededError.
if (quota.percentUsed > 80) showStorageWarning();

// ❌ BAD - Just repeats what code does
// Check if quota is over 80
```

### API Documentation

```markdown
## Endpoint: POST /api/resource

### What It Does

[Plain-English purpose]

### Request/Response

[JSON examples]

### Common Errors

[Error codes and meanings]
```

## Visual Patterns

### File Tree

```
project/
├── src/                    # Source code
│   ├── components/        # Reusable UI
│   ├── services/          # Business logic
│   └── types/             # TypeScript types
├── tests/                 # Test files
└── package.json           # Dependencies
```

### Data Flow

```
User Request Flow:
1. User submits → 2. Validation → 3. API → 4. Database → 5. Response

[1] components/Form.tsx
    ↓ validates
[2] services/validation.ts
    ↓ calls API
[3] services/api.ts
    ↓ queries
[4] Database
    ↓ returns
[5] Form.tsx (updates UI)
```

### Design Decision (ADR)

```markdown
## Why We Use [Technology]

**Decision:** [What we chose]
**Context:** [Why we needed to choose]
**Reasoning:** [Why this option]
**Trade-offs:** [What we gave up]
```

## Documentation Quality Checklist

### Before Publishing

- [ ] Quick start works in < 5 minutes
- [ ] Code examples are copy-pasteable
- [ ] File paths are accurate
- [ ] Links work
- [ ] Jargon is defined
- [ ] Diagrams are included for complex flows

### Common Mistakes to Avoid

- Assuming reader knows the codebase
- Outdated code examples
- Missing prerequisites
- No visual aids for complex systems
- Explaining "what" without "why"

## Verification Workflow

After writing documentation:

1. **Fresh Eyes Test** - Read as if you've never seen the codebase
2. **Run Examples** - Copy-paste and verify they work
3. **Check Links** - All internal/external links resolve
4. **Beginner Review** - Would a new developer understand?
5. **Update Check** - Does it reflect current code?

## See Also

- [Code Review Standards](../_shared/CODE_REVIEW_STANDARDS.md) - Documentation quality
- Project `CLAUDE.md` - Documentation rules
