---
name: context-file-generator
description: Generate standardized context documentation files (.ctx.md) for systems, APIs, features, and infrastructure. Use when documenting codebases, creating developer context, or when the user mentions documentation, context files, or needs to explain how a system works.
---

# Context File Generator

Generate comprehensive, standalone developer context documentation in the `.ctx.md` format.

## Overview

Context files (`.ctx.md`) are self-sufficient documentation files that provide developers and AI assistants with all necessary information to understand and modify a system. They follow a strict format optimized for:

- **AI-readability**: Clear structure, code references with line numbers
- **Human-readability**: Logical flow, ASCII diagrams, examples
- **Standalone principle**: No cross-repository references

## Quick Start

1. Identify the documentation type (System, API, Feature, Infrastructure)
2. Select the appropriate template from `templates/`
3. Fill in all sections with code references
4. Validate standalone compliance
5. Update `_index.md` in the context folder

## Template Selection

```
┌─────────────────────────────────────────────────────────────┐
│                    TEMPLATE DECISION TREE                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  What are you documenting?                                  │
│                                                             │
│  ├─ Backend service/module/system?                          │
│  │   └─► templates/system-context.md                        │
│  │                                                          │
│  ├─ REST endpoints or WebSocket events?                     │
│  │   └─► templates/api-context.md                           │
│  │                                                          │
│  ├─ UI feature or frontend functionality?                   │
│  │   └─► templates/feature-context.md                       │
│  │                                                          │
│  ├─ Docker, servers, CI/CD, deployment?                     │
│  │   └─► templates/infrastructure-context.md                │
│  │                                                          │
│  └─ Index file for a context folder?                        │
│      └─► templates/index-template.md                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Context File Format

### Required Sections

Every context file MUST include:

1. **Header Block** - Title and metadata
2. **Overview** - Brief explanation of the system
3. **Definitions** - Enums, types, key concepts
4. **Code References** - File paths with line numbers
5. **Data Flow** - ASCII diagram showing system flow
6. **Change Scenarios** - Common modification patterns
7. **Key Files Reference** - Complete file list
8. **Debugging Tips** - Troubleshooting guidance

### Header Block Format

```markdown
# {System Name} - Developer Context

> **Purpose:** {One-line description of what this document covers}
>
> **Last Updated:** {Month Year}
> **Status:** {Current | Outdated | WIP}
```

### Code Reference Format

Always use the format: `{repo}/{path/to/file}:{line-number}`

**Examples:**
```markdown
**File:** `cm-backend/src/modules/auth/auth.service.ts:45-67`

| Action | Status | Code Reference |
|--------|--------|----------------|
| User login | `AUTHENTICATED` | `cm-backend/src/modules/auth/auth.service.ts:89` |
```

### ASCII Diagram Standards

Use box-drawing characters for flow diagrams:

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Source    │────►│  Processor  │────►│   Output    │
└─────────────┘     └─────────────┘     └─────────────┘
```

Symbols:
- `┌ ┐ └ ┘` - Box corners
- `─` - Horizontal line
- `│` - Vertical line
- `►` `◄` `▼` `▲` - Arrows
- `├ ┤ ┬ ┴ ┼` - Connectors

## Validation Rules

### Standalone Compliance

Context files MUST be self-sufficient:

```
✅ ALLOWED:
- References to files within the SAME repository
- Inline explanations of dependencies
- Relative paths within the repo

❌ FORBIDDEN:
- Cross-repository file references
- Assumptions about other repos' structure
- Links to files in parent/sibling repos
```

### Validation Checklist

Before completing a context file, verify:

- [ ] All code paths exist and are accessible
- [ ] Line numbers are current (not outdated)
- [ ] No cross-repository references
- [ ] ASCII diagrams render correctly
- [ ] All sections from template are filled
- [ ] Change scenarios cover common modifications
- [ ] Debugging tips are actionable

## File Naming Convention

```
{system-name}.ctx.md

Examples:
- account-status-system.ctx.md
- authentication-flow.ctx.md
- copy-cycle-api.ctx.md
- docker-deployment.ctx.md
```

## Folder Structure

Context files should be organized in `docs/context/` or `docs/`:

```
{repo}/
└── docs/
    ├── context/
    │   ├── _index.md          # Index of all context files
    │   ├── system-a.ctx.md
    │   └── system-b.ctx.md
    └── other-docs.md
```

## Index File Management

The `_index.md` file tracks all context documentation:

```markdown
# Context Documentation Index

| Document | System | Status | Last Updated |
|----------|--------|--------|--------------|
| [account-status.ctx.md](account-status.ctx.md) | Account Status | ✅ Current | Dec 2025 |
| [auth-flow.ctx.md](auth-flow.ctx.md) | Authentication | ⚠️ Outdated | Nov 2025 |
| [copy-cycle.ctx.md](copy-cycle.ctx.md) | Copy Trading | 🚧 WIP | Dec 2025 |
```

Status indicators:
- ✅ Current - Up to date
- ⚠️ Outdated - Needs review
- 🚧 WIP - Work in progress

## Template Usage

### Loading a Template

```bash
# Read the appropriate template
cat templates/system-context.md
```

### Filling the Template

1. Replace all `{PLACEHOLDER}` values
2. Remove instructional comments (lines starting with `<!-- -->`)
3. Add actual code references with line numbers
4. Create ASCII diagrams specific to your system
5. Document real change scenarios from the codebase

## Examples

### Example: System Documentation

See reference implementation: `docs/account-status-system.ctx.md`

Key characteristics:
- Clear enum definitions with code references
- Complete data flow from source to UI
- Specific line numbers for all references
- Actionable debugging commands

### Example: Minimal Context File

```markdown
# User Settings - Developer Context

> **Purpose:** Documents the user settings storage and retrieval system
>
> **Last Updated:** January 2025

## Overview

The user settings system manages persistent user preferences using Redis for caching and PostgreSQL for storage.

## Key Files

| File | Purpose |
|------|---------|
| `src/modules/settings/settings.service.ts` | Core service logic |
| `src/modules/settings/settings.controller.ts` | REST endpoints |
| `prisma/schema.prisma:234-256` | UserSettings model |

## Data Flow

```
User Request → Controller → Service → Redis Cache
                                   ↓ (miss)
                              PostgreSQL
```

## Change Scenarios

### Add new setting field

1. Update Prisma schema (`prisma/schema.prisma:234`)
2. Run migration: `npm run prisma:migrate:dev`
3. Update DTO (`src/modules/settings/dto/settings.dto.ts`)
4. Update service methods

## Debugging

```bash
# Check Redis cache
redis-cli GET user:settings:{userId}

# View service logs
docker logs -f main-backend | grep "SettingsService"
```
```

## Integration with Documentation Architect Agent

This skill is used by the `documentation-architect` agent for:

1. Template selection based on documentation type
2. Format validation
3. Standalone compliance checking
4. Index file updates

## Reference Documents

- Architecture: `DOCUMENTATION-ARCHITECTURE-PLAN.md`
- Example: `docs/account-status-system.ctx.md`
- Agent: `.claude/commands/agent-prompts/documentation-architect.md`

## Best Practices

1. **Be Specific**: Include exact line numbers, not ranges when possible
2. **Stay Current**: Update line numbers after code changes
3. **Think Standalone**: Each file should work without external context
4. **Use Tables**: Structure repeated information in tables
5. **Test Diagrams**: Verify ASCII art renders in preview
6. **Document Changes**: Include common modification scenarios
7. **Add Debugging**: Include practical troubleshooting commands
