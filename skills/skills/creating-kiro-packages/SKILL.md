---
name: creating-kiro-packages
description: Use when creating Kiro steering files or hooks - provides inclusion modes (always/fileMatch/manual), foundational files (product.md/tech.md/structure.md), and JSON hook configuration with event triggers
---

# Creating Kiro Packages

## Overview

Kiro uses two package types:
1. **Steering files** (`.kiro/steering/*.md`) - Markdown with optional YAML frontmatter
2. **Hooks** (`.kiro/hooks/*.json`) - JSON configuration for event-driven automation

## Package Types

| Type | Location | Format | Purpose |
|------|----------|--------|---------|
| **Steering Files** | `.kiro/steering/*.md` | Markdown + YAML | Context-aware instructions |
| **Hooks** | `.kiro/hooks/*.json` | JSON | Event-driven automation |

## Steering Files

### Inclusion Modes

| Mode | Frontmatter | When Applied |
|------|-------------|--------------|
| **always** (default) | `inclusion: always` | All contexts |
| **fileMatch** | `inclusion: fileMatch` + `fileMatchPattern` | Files matching pattern |
| **manual** | `inclusion: manual` | User manually triggers |

### Quick Reference

```yaml
---
inclusion: always  # always, fileMatch, or manual
fileMatchPattern: "components/**/*.tsx"  # Required for fileMatch
domain: testing  # Optional: for organization
---
```

## Creating Always-Included Steering Files

Used for workspace-wide standards that influence all code generation:

```markdown
---
inclusion: always
---

# Core Technology Stack

Our workspace uses the following technologies and standards.

## Stack

- **Frontend**: React 18 + TypeScript + Vite
- **Backend**: Node.js + Express + Prisma
- **Database**: PostgreSQL
- **Testing**: Vitest + Testing Library

## Universal Principles

- Write self-documenting code
- Keep functions under 50 lines
- Use meaningful variable names
- Add comments only for complex logic
```

## Creating FileMatch Steering Files

Applied automatically when working with files matching the pattern:

```markdown
---
inclusion: fileMatch
fileMatchPattern: "components/**/*.tsx"
domain: frontend
---

# React Component Guidelines

Applied automatically when working with React components.

## Component Standards

- Use functional components with hooks
- Keep components under 200 lines
- Extract logic into custom hooks
- Co-locate styles with components

## Example

\`\`\`tsx
// Good: Focused component
function UserProfile({ userId }: Props) {
  const user = useUser(userId);
  return <div>{user.name}</div>;
}
\`\`\`
```

### Common FileMatch Patterns

```yaml
# React components
fileMatchPattern: "*.tsx"

# API routes
fileMatchPattern: "app/api/**/*"

# Test files
fileMatchPattern: "**/*.test.*"

# Components in specific directory
fileMatchPattern: "src/components/**/*"

# Documentation
fileMatchPattern: "*.md"
```

## Creating Manual Steering Files

User explicitly activates when needed:

```markdown
---
inclusion: manual
domain: performance
---

# Performance Optimization Guide

Manually activate when optimizing performance-critical code.

## Profiling First

- Always measure before optimizing
- Use Chrome DevTools or similar
- Identify actual bottlenecks

## Common Optimizations

- Memoization for expensive calculations
- Lazy loading for large components
- Debouncing for frequent events
- Virtual scrolling for long lists
```

## Foundational Files

Kiro recognizes special steering files with reserved names:

### product.md

```markdown
---
inclusion: always
foundationalType: product
---

# Product Context

## Mission

Build the best task management app for remote teams.

## Key Features

1. Real-time collaboration
2. Offline-first architecture
3. Natural language task input
4. Smart scheduling

## User Personas

- **Project Manager**: Needs overview and reporting
- **Team Member**: Needs task details and updates
- **Stakeholder**: Needs high-level progress tracking
```

### tech.md

```markdown
---
inclusion: always
foundationalType: tech
---

# Technical Architecture

## Stack

- **Frontend**: React 18 + TypeScript + Vite
- **Backend**: Node.js + Express + Prisma
- **Database**: PostgreSQL
- **Cache**: Redis
- **Deploy**: Docker + AWS ECS

## Architecture Patterns

- Clean architecture (domain/application/infrastructure)
- CQRS for complex operations
- Event sourcing for audit trail
- Repository pattern for data access
```

### structure.md

```markdown
---
inclusion: always
foundationalType: structure
---

# Project Structure

## Directory Layout

\`\`\`
src/
  api/              # API routes and controllers
  domain/           # Business logic and entities
  services/         # Application services
  repositories/     # Data access layer
  middleware/       # Express middleware
  utils/            # Helper functions
\`\`\`

## File Naming Conventions

- **Components**: PascalCase (e.g., `UserProfile.tsx`)
- **Services**: camelCase with Service suffix (e.g., `userService.ts`)
- **Types**: PascalCase (e.g., `User.ts`)
- **Tests**: `*.test.ts` or `*.spec.ts`
```

## Kiro Hooks

Hooks are JSON configuration files for event-driven automation:

### Hook Structure

```json
{
  "name": "Hook Name",
  "description": "What this hook does",
  "version": "1",
  "when": {
    "type": "eventType",
    "patterns": ["glob", "patterns"]
  },
  "then": {
    "type": "actionType",
    "prompt": "Instructions for agent"
  }
}
```

### Event Types

**File Events** (require `patterns`):

| Event | Triggers When |
|-------|---------------|
| `fileCreated` | New files created matching patterns |
| `fileModified` | Files modified matching patterns |
| `fileDeleted` | Files deleted matching patterns |

**Lifecycle Events** (no patterns needed):

| Event | Triggers When |
|-------|---------------|
| `agentSpawn` | Agent is activated/session starts |
| `userPromptSubmit` | User submits a prompt (before processing) |
| `preToolUse` | Before tool execution (can block) |
| `postToolUse` | After tool execution completes |
| `stop` | Agent finishes responding (end of turn) |

### Action Types

| Action | Behavior |
|--------|----------|
| `askAgent` | Asks Kiro agent to perform task |
| `runCommand` | Executes shell command |

## Creating Hooks

### Automatic Test File Creation

`.kiro/hooks/auto-test-files.json`:
```json
{
  "name": "Auto Test Files",
  "description": "Creates test files for new components",
  "version": "1",
  "when": {
    "type": "fileCreated",
    "patterns": ["src/components/**/*.tsx"]
  },
  "then": {
    "type": "askAgent",
    "prompt": "A new component was created. Create a corresponding test file following our testing patterns. Use React Testing Library and include tests for rendering and key interactions."
  }
}
```

### Image Asset Indexer

`.kiro/hooks/image-indexer.json`:
```json
{
  "name": "Image Asset Indexer",
  "description": "Adds references to new images in index.ts",
  "version": "1",
  "when": {
    "type": "fileCreated",
    "patterns": [
      "client/src/assets/*.png",
      "client/src/assets/*.jpg",
      "client/src/assets/*.svg"
    ]
  },
  "then": {
    "type": "askAgent",
    "prompt": "A new image file has been added to the assets folder. Please update the index.ts file in the assets folder to include a reference to this new image. First, check the current structure of the index.ts file to understand how images are referenced. Then add an appropriate export statement for the new image file following the existing pattern."
  }
}
```

### Dependency Update Checker

`.kiro/hooks/dependency-checker.json`:
```json
{
  "name": "Dependency Update Checker",
  "description": "Checks for breaking changes in package.json",
  "version": "1",
  "when": {
    "type": "fileModified",
    "patterns": ["package.json"]
  },
  "then": {
    "type": "askAgent",
    "prompt": "package.json was modified. Check if any dependencies were updated and review the changelog for breaking changes. Suggest any code updates needed."
  }
}
```

### Session Context Loader (Lifecycle Hook)

`.kiro/hooks/session-setup.json`:
```json
{
  "name": "Session Setup",
  "description": "Loads project context when agent starts",
  "version": "1",
  "when": {
    "type": "agentSpawn"
  },
  "then": {
    "type": "askAgent",
    "prompt": "Read the README.md and CONTRIBUTING.md to understand the project structure and coding conventions before starting work."
  }
}
```

### Security Gate (Lifecycle Hook)

`.kiro/hooks/security-check.json`:
```json
{
  "name": "Security Check",
  "description": "Reviews tool calls for security concerns",
  "version": "1",
  "when": {
    "type": "preToolUse"
  },
  "then": {
    "type": "askAgent",
    "prompt": "Review this tool call for potential security issues. Block if it accesses sensitive files (.env, credentials) or runs dangerous commands."
  }
}
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Missing fileMatchPattern with fileMatch | fileMatchPattern is REQUIRED when inclusion is fileMatch |
| Missing inclusion field | Defaults to always if omitted |
| Using regex in fileMatchPattern | Globs only, no regex support |
| Multiple patterns in fileMatchPattern | Use single pattern string only |
| Forgetting domain field | Use domain for organization and discovery |
| Adding patterns to lifecycle hooks | Lifecycle events (agentSpawn, preToolUse, etc.) don't need patterns |
| Missing patterns for file hooks | File events (fileCreated, fileModified, fileDeleted) require patterns |

## Validation

Schemas location:
- Steering: `/Users/khaliqgant/Projects/prpm/app/packages/converters/schemas/kiro-steering.schema.json`
- Hooks: `/Users/khaliqgant/Projects/prpm/app/packages/converters/schemas/kiro-hooks.schema.json`

Documentation:
- Steering: `/Users/khaliqgant/Projects/prpm/app/packages/converters/docs/kiro.md`
- Hooks: `/Users/khaliqgant/Projects/prpm/app/packages/converters/docs/kiro-hooks.md`

## Best Practices

### Steering Files

1. **Start with foundational files**: product.md, tech.md, structure.md
2. **Use always for core patterns**: Code style, architecture principles
3. **Use fileMatch for specific contexts**: Component rules, API patterns
4. **Group by domain**: Consistent naming helps discovery
5. **Manual for workflows**: Special procedures, optimization guides

### Hooks

1. **Specific patterns**: Use precise globs to avoid unnecessary triggers
2. **Clear prompts**: Write detailed agent prompts with context
3. **Idempotent actions**: Ensure hooks can run multiple times safely
4. **Performance**: Avoid hooks on frequently modified files
5. **Testing**: Test hooks in isolation before deploying

---

**Remember**: Steering files use inclusion modes (always/fileMatch/manual). Hooks use JSON with event triggers (fileCreated/fileModified/fileDeleted).
