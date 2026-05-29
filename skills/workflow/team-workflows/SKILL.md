---
name: team-workflows
description: Team collaboration patterns - shared configs, standards, onboarding
version: 1.0.0
author: Claude Code SDK
tags: [team, collaboration, standards, onboarding]
---

# Team Workflows

Establish consistent Claude Code practices across your team with shared configurations, standards, and onboarding patterns.

## Quick Reference

| Aspect | Location | Scope |
|--------|----------|-------|
| Project Config | `./CLAUDE.md` | Checked into repo, shared by all |
| Project Rules | `./.claude/rules/*.md` | File-specific team standards |
| Personal Config | `~/.claude/CLAUDE.md` | Individual preferences (not shared) |
| Team Skills | `./.claude/skills/` | Project-specific workflows |
| Settings | `./.claude/settings.json` | Team tool settings |

## Configuration Hierarchy for Teams

```
Team Member's Machine
|
+-- ~/.claude/CLAUDE.md           # Personal (not checked in)
|
+-- Project Repository (shared)
    |
    +-- CLAUDE.md                 # Project standards
    |
    +-- .claude/
        +-- CLAUDE.md             # Alternative location
        +-- settings.json         # Tool settings
        +-- rules/*.md            # File-specific rules
        +-- skills/*.md           # Team workflows
```

### What to Share vs. Keep Personal

| Share (Version Control) | Keep Personal (~/.claude/) |
|------------------------|---------------------------|
| Project conventions | Editor preferences |
| Build commands | Tool aliases |
| Code style rules | API keys |
| Architecture docs | Personal shortcuts |
| Team workflows | Experimental settings |

## Team Standards Pattern

### Code Style Enforcement

Create `.claude/rules/code-style.md`:

```yaml
---
globs: ["**/*.ts", "**/*.tsx"]
description: Team TypeScript conventions
alwaysApply: true
---

# Code Style Standards

## Formatting
- Use 2-space indentation
- Single quotes for strings
- No semicolons (Prettier handles)
- Max line length: 100 characters

## Naming
- Components: PascalCase
- Functions: camelCase
- Constants: UPPER_SNAKE_CASE
- Files: kebab-case.ts

## Imports
- Absolute imports from `@/`
- Group: external, internal, relative
- Sort alphabetically within groups
```

### Review Standards

Create `.claude/rules/reviews.md`:

```yaml
---
globs: ["**/*"]
description: Code review standards
alwaysApply: false
---

# Code Review Checklist

When reviewing or preparing code for review:

## Required
- [ ] Tests cover new functionality
- [ ] No console.log statements
- [ ] Error handling for async operations
- [ ] TypeScript strict mode passes

## Performance
- [ ] No N+1 queries
- [ ] Large lists use pagination
- [ ] Images are optimized

## Security
- [ ] No secrets in code
- [ ] User input is validated
- [ ] SQL uses parameterized queries
```

## Shared Skills Pattern

Teams can create project-specific skills in `.claude/skills/`:

### Structure

```
.claude/
  skills/
    deploy/
      SKILL.md           # Deployment workflow
    pr-workflow/
      SKILL.md           # PR creation standards
    incident-response/
      SKILL.md           # On-call procedures
```

### Example Team Skill

Create `.claude/skills/feature-workflow/SKILL.md`:

```yaml
---
name: feature-workflow
description: Team feature development workflow from branch to merge.
---

# Feature Workflow

## 1. Create Branch
```bash
git checkout main && git pull
git checkout -b feature/TICKET-123-description
```

## 2. Development
- Follow `.claude/rules/code-style.md`
- Write tests alongside code
- Update CHANGELOG.md

## 3. Pre-PR Checks
```bash
bun test
bun lint
bun typecheck
```

## 4. Create PR
- Title: `feat(scope): description`
- Link to ticket
- Add reviewers from CODEOWNERS
```

## Team Settings

Share tool configurations via `.claude/settings.json`:

```json
{
  "permissions": {
    "allow": [
      "Bash(bun:*)",
      "Bash(git:*)",
      "Bash(docker compose:*)"
    ],
    "deny": [
      "Bash(rm -rf:*)",
      "Bash(git push --force:*)"
    ]
  }
}
```

**Note:** Personal API keys and sensitive settings should remain in `~/.claude/settings.json`.

## Workflow: Setting Up Team Standards

### Prerequisites
- [ ] Git repository initialized
- [ ] Team coding conventions discussed
- [ ] Key commands documented

### Steps

1. **Create Project CLAUDE.md**
   - [ ] Add project description
   - [ ] Document all commands
   - [ ] List tech stack
   - [ ] Note key architecture decisions

2. **Create Rules Directory**
   - [ ] `.claude/rules/code-style.md`
   - [ ] `.claude/rules/testing.md`
   - [ ] `.claude/rules/security.md`

3. **Add Team Skills**
   - [ ] `.claude/skills/` for common workflows
   - [ ] Document team-specific procedures

4. **Configure Settings**
   - [ ] `.claude/settings.json` with permissions
   - [ ] Add to `.gitignore` if contains secrets

5. **Document Onboarding**
   - [ ] Add onboarding section to CLAUDE.md
   - [ ] Create onboarding skill if complex

### Validation
- [ ] All files committed to version control
- [ ] New team member can onboard using docs
- [ ] Rules load correctly for target files

## Common Team Patterns

### Monorepo Team Setup

```
monorepo/
  CLAUDE.md                    # Shared conventions
  .claude/
    rules/
      frontend.md              # Globs: apps/web/**/*
      backend.md               # Globs: apps/api/**/*
      shared.md                # Globs: packages/**/*
    skills/
      release/SKILL.md         # Release workflow
  apps/
    web/CLAUDE.md              # Frontend-specific
    api/CLAUDE.md              # Backend-specific
```

### Feature Team Setup

```
project/
  CLAUDE.md                    # Project-wide
  .claude/
    rules/
      team-alpha.md            # Globs: src/features/alpha/**/*
      team-beta.md             # Globs: src/features/beta/**/*
    skills/
      handoff/SKILL.md         # Cross-team handoff
```

### Rotating Roles Setup

```
project/
  .claude/
    rules/
      on-call.md               # On-call procedures
      review-duty.md           # Review rotation rules
    skills/
      incident/SKILL.md        # Incident response
      triage/SKILL.md          # Bug triage
```

## Knowledge Sharing

### Decision Documentation

Include in CLAUDE.md:

```markdown
## Architecture Decisions

### ADR-001: Use Drizzle over Prisma
**Status:** Accepted
**Context:** Need TypeScript ORM with good Bun support
**Decision:** Use Drizzle for lighter bundle and better TS inference
**Consequences:** Team needs to learn Drizzle API
```

### Pattern Library

Create `.claude/rules/patterns.md`:

```yaml
---
globs: ["src/**/*.ts"]
description: Approved implementation patterns
alwaysApply: true
---

# Approved Patterns

## API Calls
Use the `apiClient` wrapper, not fetch directly:
```ts
// Good
const data = await apiClient.get('/users');

// Avoid
const data = await fetch('/api/users');
```

## Error Handling
Always use Result type for operations that can fail:
```ts
// Good
const result = await createUser(data);
if (result.isErr()) { handle error }

// Avoid
try { await createUser(data) } catch { ... }
```
```

## Best Practices

### Do

- Commit CLAUDE.md and .claude/ to version control
- Keep personal preferences in ~/.claude/
- Review configurations during onboarding
- Update docs when conventions change
- Use rules for file-specific guidance

### Avoid

- Putting secrets in shared configs
- Overly long CLAUDE.md files
- Conflicting personal and project settings
- Stale documentation
- Duplicating official docs

## Reference Files

| File | Contents |
|------|----------|
| [SHARED-CONFIG.md](./SHARED-CONFIG.md) | Sharing configurations across team |
| [STANDARDS.md](./STANDARDS.md) | Establishing team standards |
| [ONBOARDING.md](./ONBOARDING.md) | Onboarding new team members |

## Validation Checklist

Before sharing team configuration:

- [ ] CLAUDE.md checked into version control
- [ ] No secrets in shared configurations
- [ ] Rules have appropriate glob patterns
- [ ] Skills are documented and tested
- [ ] Onboarding process documented
- [ ] Team has reviewed and approved
