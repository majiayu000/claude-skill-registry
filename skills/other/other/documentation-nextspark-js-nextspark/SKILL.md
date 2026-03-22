---
name: documentation
description: |
  Documentation patterns for this Next.js application.
  Covers documentation structure, numbered hierarchy, frontmatter, BDD format, and feature documentation.
  Use this skill when creating or maintaining project documentation.
allowed-tools: Read, Glob, Grep
version: 1.0.0
---

# Documentation Skill

Patterns for creating and maintaining project documentation.

## Architecture Overview

```
DOCUMENTATION STRUCTURE:

Core Documentation:
core/docs/
├── 01-fundamentals/      # Project basics
├── 02-architecture/      # System architecture
├── 03-registry-system/   # Registry patterns
├── 04-entities/          # Entity system
├── 05-api/               # API documentation
├── 06-authentication/    # Auth patterns
├── 07-authorization/     # Permissions
├── 08-database/          # Database patterns
├── 09-frontend/          # Frontend patterns
├── 10-blocks/            # Page builder blocks
├── 11-themes/            # Theming system
├── 12-testing/           # Testing guides
├── 13-i18n/              # Internationalization
├── 14-deployment/        # Deployment guides
├── 15-performance/       # Performance
├── 16-billing/           # Billing system
├── 17-devtools/          # Developer tools
├── 18-guides/            # How-to guides
└── 19-appendix/          # Reference materials

Theme Documentation:
contents/themes/{theme}/docs/
├── 01-overview/
├── 02-configuration/
├── 03-customization/
└── ...

Plugin Documentation:
contents/plugins/{plugin}/docs/
└── ...

Development Rules:
.rules/
├── core.md               # Core development principles
├── testing.md            # Testing guidelines
├── components.md         # Component patterns
├── api.md                # API standards
├── auth.md               # Authentication
├── i18n.md               # Internationalization
├── plugins.md            # Plugin development
├── migrations.md         # Database migrations
├── documentation.md      # Documentation standards
└── ...
```

## When to Use This Skill

- Creating feature documentation
- Writing BDD test documentation
- Structuring new documentation files
- Understanding documentation standards
- Following numbered hierarchy patterns

## Numbered Hierarchy Pattern

Documentation uses numbered prefixes for ordering:

```
{NN}-{category}/
├── {NN}-{topic}.md
├── {NN}-{topic}.md
└── {NN}-{topic}/
    ├── {NN}-{subtopic}.md
    └── {NN}-{subtopic}.md

Examples:
01-fundamentals/
├── 01-project-overview.md
├── 02-getting-started.md
└── 03-quick-start.md

04-entities/
├── 01-introduction.md
├── 02-entity-config.md
├── 03-api-endpoints.md
└── 04-entity-types/
    ├── 01-core-entities.md
    └── 02-theme-entities.md
```

### Numbering Rules

1. **Categories**: Start at `01-`, increment by 1
2. **Topics within category**: Start at `01-`, increment by 1
3. **New content**: Add at the end with next number
4. **Renumbering**: Only when reorganizing (rare)

## File Naming Conventions

```
Correct:
- 01-project-overview.md
- 02-getting-started.md
- auth-testing-guide.md
- entity-creation-guide.md

Incorrect:
- ProjectOverview.md        # Use kebab-case
- getting_started.md        # Use hyphens, not underscores
- 1-overview.md             # Use two-digit prefix: 01-
- overview.md               # Need category context
```

## Documentation Types

### 1. Core Documentation (core/docs/)

Comprehensive project documentation for developers.

```markdown
# [Topic Title]

## Overview
[Brief description and context]

## [Main Section]
[Content with examples]

### [Subsection]
[Detailed content]

## Usage Examples
[Practical code examples]

## Best Practices
[Recommended approaches]

## Troubleshooting
[Common issues and solutions]

## Related Documentation
- [Related Doc 1](./path/to/doc.md)
- [Related Doc 2](./path/to/doc.md)
```

### 2. Development Rules (.rules/)

Guidelines for Claude Code development.

```markdown
# [Rule Category] Rules

## Overview
[What this rule file covers]

## MANDATORY Practices
[Required patterns]

## FORBIDDEN Patterns
[Anti-patterns to avoid]

## Examples

### Good Example
```typescript
// ✅ CORRECT
[correct code pattern]
```

### Bad Example
```typescript
// ❌ WRONG
[incorrect code pattern]
```

## Checklist
- [ ] [Verification item 1]
- [ ] [Verification item 2]
```

### 3. Theme Documentation (contents/themes/{theme}/docs/)

Theme-specific documentation.

```markdown
# [Theme Name] Theme

## Overview
[Theme description and purpose]

## Configuration
[How to configure the theme]

## Customization
[How to customize]

## Components
[Theme-specific components]
```

### 4. BDD Test Documentation (*.bdd.md)

Behavior-Driven Development documentation for tests.

```markdown
# BDD: [Feature Name]

**Test File:** `cypress/e2e/uat/[feature].cy.ts`
**Last Updated:** [YYYY-MM-DD]

---

## Feature: [Feature Name]

### Scenario: [Scenario Name]

**Given** [precondition]
**When** [action]
**Then** [expected result]

**Test ID:** `[test-id]`
**Tags:** `@[tag1]`, `@[tag2]`

---

### Scenario: [Another Scenario]

**Given** [precondition]
**When** [action]
**Then** [expected result]
**And** [additional expectation]

---

## Edge Cases

### Scenario: [Edge Case]

**Given** [edge case condition]
**When** [action]
**Then** [expected behavior]
```

## Frontmatter (Optional)

Some documentation files use YAML frontmatter:

```markdown
---
title: Entity System Overview
description: How the entity system works
category: entities
order: 1
---

# Entity System Overview
[Content...]
```

## Code Example Standards

### TypeScript Examples

```markdown
```typescript
// ✅ CORRECT: Include imports when relevant
import { useAuth } from '@/core/hooks/useAuth'

// ✅ CORRECT: Add comments for complex logic
const { user, isAuthenticated } = useAuth()

// ✅ CORRECT: Show practical usage
if (isAuthenticated) {
  console.log(`Welcome, ${user.name}`)
}
```
```

### Bash Examples

```markdown
```bash
# Install dependencies
pnpm install

# Run development server
pnpm dev

# Run tests
pnpm test
```
```

### JSON Examples

```markdown
```json
{
  "name": "example",
  "version": "1.0.0",
  "description": "Example configuration"
}
```
```

## Documentation Templates

### Feature Documentation Template

```markdown
# [Feature Name]

## Overview
[Brief description of the feature]

## Quick Start
[Fastest way to get started]

## Configuration
[How to configure the feature]

## Usage

### Basic Usage
[Simple example]

### Advanced Usage
[Complex example]

## API Reference

### [Function/Method Name]

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `param1` | string | Yes | Description |
| `param2` | number | No | Description |

**Returns:** `ReturnType`

**Example:**
```typescript
const result = functionName(param1, param2)
```

## Best Practices
- [Practice 1]
- [Practice 2]

## Troubleshooting

### [Common Issue]
**Problem:** [Description]
**Solution:** [How to fix]

## Related
- [Related Doc 1](./path.md)
- [Related Doc 2](./path.md)
```

### API Endpoint Documentation

```markdown
## [HTTP Method] [Endpoint Path]

### Description
[What this endpoint does]

### Authentication
- **API Key**: Requires `[scope]` scope
- **Session**: Dashboard access required

### Parameters

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `id` | string | path | Yes | Resource ID |
| `limit` | number | query | No | Page size (default: 20) |

### Request Example
```bash
curl -X POST https://api.example.com/v1/resource \
  -H "Authorization: Bearer sk_xxx" \
  -H "Content-Type: application/json" \
  -d '{"name": "Example"}'
```

### Response Example
```json
{
  "success": true,
  "data": {
    "id": "resource_123",
    "name": "Example"
  }
}
```

### Error Responses

| Status | Code | Description |
|--------|------|-------------|
| 400 | VALIDATION_ERROR | Invalid input |
| 401 | UNAUTHORIZED | Missing auth |
| 404 | NOT_FOUND | Resource not found |
```

## Documentation Agent

The `documentation-writer` agent creates documentation:

```typescript
// Only create documentation when explicitly requested
await launchAgent('documentation-writer', {
  feature: 'entity_system',
  includeExamples: true,
  includeApiDocs: true,
  includeTroubleshooting: true
})
```

### NEVER Create Documentation Proactively

```typescript
// ❌ WRONG - Don't create docs unless requested
// Claude Code should NOT create documentation automatically

// ✅ RIGHT - Only when explicitly requested
if (userRequestsDocumentation) {
  await launchAgent('documentation-writer', { task: 'create_docs' })
}
```

## Documentation Quality Checklist

### Before Publishing

- [ ] All code examples are tested and working
- [ ] Links are valid and accessible
- [ ] Screenshots are current (if any)
- [ ] Grammar and spelling correct
- [ ] Table of contents accurate (for long docs)
- [ ] Examples cover common use cases
- [ ] Error scenarios documented
- [ ] Prerequisites stated
- [ ] Related docs linked

### Maintenance Schedule

- **Daily**: Fix reported documentation bugs
- **Weekly**: Update changed API endpoints
- **Monthly**: Review and update examples
- **Quarterly**: Comprehensive documentation audit
- **Release**: Update all affected documentation

## Anti-Patterns

```markdown
# NEVER: Document obvious code
// ❌ BAD: Set the variable to true
const isActive = true

# NEVER: Include auto-generated files in docs
# core/lib/registries/*.ts - DO NOT DOCUMENT

# NEVER: Create documentation without explicit request
# Only create when user asks

# NEVER: Duplicate information
# Link to authoritative sources instead

# NEVER: Skip code examples
# Always include practical examples

# NEVER: Use outdated screenshots
# Update or remove if outdated

# NEVER: Leave TODO comments in published docs
# TODO: Add example later ❌
```

## Core Documentation Statistics

```
core/docs/
├── 01-fundamentals/      # ~5 files
├── 02-architecture/      # ~3 files
├── 03-registry-system/   # ~4 files
├── 04-entities/          # ~8 files
├── 05-api/               # ~10 files
├── 06-authentication/    # ~6 files
├── 07-authorization/     # ~4 files
├── 08-database/          # ~5 files
├── 09-frontend/          # ~12 files
├── 10-blocks/            # ~6 files
├── 11-themes/            # ~4 files
├── 12-testing/           # ~15 files
├── 13-i18n/              # ~3 files
├── 14-deployment/        # ~4 files
├── 15-performance/       # ~3 files
├── 16-billing/           # ~5 files
├── 17-devtools/          # ~4 files
├── 18-guides/            # ~6 files
└── 19-appendix/          # ~3 files

Total: ~100+ documentation files
```

## Checklist

Before finalizing documentation:

- [ ] File uses correct naming convention (kebab-case)
- [ ] Numbered prefix matches category order
- [ ] Content follows appropriate template
- [ ] Code examples are syntax-highlighted
- [ ] All links work correctly
- [ ] No hardcoded paths (use relative)
- [ ] Examples are tested and working
- [ ] Related documentation linked
- [ ] BDD docs use Given/When/Then format
- [ ] No TODO comments left in content

## Related Skills

- `session-management` - Session documentation patterns
- `cypress-e2e` - BDD test documentation
- `pom-patterns` - Test documentation in tests.md
- `i18n-nextintl` - Documentation translations
