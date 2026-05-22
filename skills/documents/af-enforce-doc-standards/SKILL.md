---
name: af-enforce-doc-standards
description: Enforce AgentFlow documentation standards for frontmatter, linking, and structure. Use when validating documentation compliance, checking bidirectional links, or auditing file organization and markup patterns.

# AgentFlow documentation fields
title: Documentation Standards Expertise
created: 2025-10-29
updated: 2025-12-11
last_checked: 2025-12-11
tags: [skill, expertise, documentation, standards, frontmatter]
parent: ../README.md
---

# Documentation Standards Expertise

## Essential Reading

**⚠️ BEFORE creating documentation, read this comprehensive guide:**

@.claude/docs/guides/documentation-system.md

This guide explains:
- **Three-layer documentation pattern** (Asset → Index → Reference)
- When to create guides vs asset documentation
- Complete workflows for all documentation scenarios
- Edge cases and troubleshooting

**Without reading this guide first, you will create incomplete documentation.**

## When to Use This Skill

Invoke this skill when:
- Creating any new `.md` file (guides, specs, documentation)
- Adding framework components (agents, skills, commands, orchestrators)
- Validating documentation before commits
- Fixing broken links or metadata issues
- Updating existing documentation after code changes
- Setting up documentation in brownfield projects

## Rules: FOLLOW THESE

### Frontmatter Rules

1. **All `.md` files MUST have frontmatter** with required fields
2. **Required fields**: `title`, `created`, `updated`, `last_checked`, `tags`
3. **At least ONE linking field required**: `parent`, `children`, `code_files`, or `related`
4. **Dates MUST be YYYY-MM-DD format**
5. **Tags MUST be an array** with at least one tag
6. **`last_checked` MUST be within 30 days** (or document is stale)
7. **Agent files NEED dual frontmatter**: Claude Code registration + AgentFlow documentation
8. **Skill files NEED minimal frontmatter**: Only Claude Code registration fields
9. **Quote YAML special characters**: Values with `< > [ ] : { }` must be quoted

### Linking Rules

10. **Every child MUST declare its parent** in frontmatter
11. **Every parent MUST list its children** in children array
12. **Parent-child relationships MUST be bidirectional** and reciprocal
13. **All referenced paths MUST exist** (no broken links)
14. **Use relative paths only** (never absolute paths)
15. **Only these files can have no parent**: `.claude/README.md`, `.claude/docs/README.md`, `docs/README.md`, `README.md`
16. **Use `related` field for peer relationships** (not parent-child)
17. **Cross-directory links use `related` field** not parent-child

### Code Documentation Rules

18. **All TypeScript/JavaScript MUST have JSDoc** comment blocks
19. **All code MUST include `@documentation` tag** pointing to guide
20. **Use `@requirements` tag** to link to BDD feature files (when applicable)
21. **Use `@adr` tag** to reference architecture decisions (when applicable)

### Quality Rules

22. **Complete over concise** - No artificial size limits on documentation
23. **Update `updated` date when changing content**
24. **Update `last_checked` even if content unchanged** (proves review happened)
25. **README.md files MUST list all children** in their directory
26. **Files in `.claude/work/` are exempt** from linking and freshness rules

## Workflows

### Workflow: Creating Documentation for New Features

When implementing a new feature (BDD workflow):

1. **Refinement Phase** - BDD scenarios, mini-PRD, visual specs
2. **Implementation Phase** - Write code with JSDoc, include `@documentation` tags
3. **Documentation Phase** - Create guides in `/docs/guides/`, API docs in `/docs/api/`
4. **Validation Phase** - Run validation scripts and docs-quality-agent

**Key principle**: Documentation created BEFORE code (Refinement), then enhanced DURING implementation, then validated AFTER completion.

**Example structure**:
```
docs/requirements/mini-prd/auth.md       # Refinement phase (contains Markdown scenarios)
src/lib/auth.ts                          # Implementation phase (with TSDoc)
docs/guides/authentication.md            # Documentation phase
docs/api/auth-endpoints.md               # Documentation phase
```

### Workflow: Adding Framework Components

When adding agents, skills, commands, or orchestrators:

1. **Create asset file** with proper frontmatter (include parent field)
2. **Update parent's children array** to include new asset
3. **Run validation**: `npx ts-node .claude/scripts/validate-links.ts`
4. **Run docs-quality-agent** for semantic validation

**Critical**: Both steps (add parent reference, update children array) are required for bidirectional linking.

### Workflow: Updating Existing Documentation

When code changes require doc updates:

1. **Identify affected docs** - Check `@documentation` tags in changed code
2. **Update content** - Modify docs to reflect changes, update examples
3. **Update metadata** - Increment `updated` and `last_checked` dates
4. **Validate changes** - Run `validate-frontmatter.ts` and `validate-links.ts`
5. **Update related docs** - Check `related` field for connected documents

**Common mistake**: Forgetting to update `last_checked` even when content hasn't changed.

### Workflow: Validating Documentation

Before committing documentation changes:

1. **Run validation scripts**:
   - `validate-frontmatter.ts` - Check metadata compliance
   - `validate-links.ts` - Check bidirectional links
   - `validate-tsdoc.ts` - Check code documentation
   - `check-stale-docs.ts` - Check for outdated docs

2. **Review output** - Fix errors (missing fields, broken links)
3. **Run docs-quality-agent** - Semantic content validation
4. **Fix issues iteratively** - Infrastructure first, then metadata, then content
5. **Re-validate until clean** - All scripts pass, agent confirms quality

### Workflow: Migrating Legacy Documentation

When adding documentation to brownfield projects:

1. **Audit existing docs** - Identify all `.md` files, assess coverage
2. **Add frontmatter** - Use `repair-frontmatter.ts` for batch updates
3. **Create README indexes** - Add navigation to each directory
4. **Fill gaps** - Generate missing reference documentation
5. **Establish baseline** - Run validation scripts, fix critical issues
6. **Set up continuous validation** - Add to CI/CD, configure hooks

## Common Patterns

### Two-Layer Pattern (Framework `.claude/`)
1. **Asset Documentation** - Self-documenting files next to assets
2. **Index Documentation** - README.md files for navigation

### Three-Layer Pattern (Project `docs/`)
1. **Code Documentation** - Inline TSDoc/JSDoc in source files
2. **Index Documentation** - README.md navigation files
3. **Reference Documentation** - Comprehensive guides in `/docs/`

### Handling Edge Cases

**Circular references**: Choose one as parent, use `related` for the other
**Multiple parents**: Choose primary parent, use `related` for others
**Orphaned docs**: Add to parent's children or move to `.claude/work/`
**Cross-directory links**: Use `related` field, not parent-child
**Deprecated features**: Move to `docs/deprecated/`, add deprecation notice

## Examples

### Good: Complete Frontmatter
```yaml
---
title: Authentication System Guide
created: 2025-12-09
updated: 2025-12-09
last_checked: 2025-12-09
tags: [authentication, security, guide]
parent: ./README.md
related:
  - ../api/auth-endpoints.md
  - ../../.claude/docs/guides/security.md
---
```

### Bad: Missing Required Fields
```yaml
---
title: My Doc
# Missing: created, updated, last_checked
# Missing: at least one linking field
---
```

### Good: Bidirectional Linking
```yaml
# Parent: .claude/agents/README.md
children:
  - ./bdd-agent.md

# Child: .claude/agents/bdd-agent.md
parent: .claude/agents/README.md
```

### Bad: Unidirectional Linking
```yaml
# Parent: .claude/agents/README.md
# (missing children array)

# Child: .claude/agents/bdd-agent.md
parent: .claude/agents/README.md  # Parent doesn't list this!
```

### Good: Code Documentation
```typescript
/**
 * Authenticates user with credentials
 *
 * @documentation /docs/guides/authentication.md
 * @requirements /docs/requirements/mini-prd/auth.md
 * @adr /docs/architecture/adr/adr-015-auth-strategy.md
 */
export function authenticate(credentials: Credentials): Promise<User>
```

### Bad: Missing @documentation Tag
```typescript
/**
 * Authenticates user with credentials
 * (No @documentation tag - how do users learn about this?)
 */
export function authenticate(credentials: Credentials): Promise<User>
```

## Detailed Reference

**For complete documentation patterns**: Read @.claude/docs/guides/documentation-system.md (REQUIRED reading)

**For full specification**: See `.claude/docs/standards/documentation-standards.md`

**For validation process**: See `.claude/skills/af-validate-quality/SKILL.md`

**For validation scripts**: See `.claude/scripts/documentation/README.md`

**For templates**: See `.claude/templates/` (glossary, mini-PRD, ADR templates)
