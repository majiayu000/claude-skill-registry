---
name: claude-workspace
description: This skill should be used when creating or organizing working files in the .claude/ directory. It enforces consistent structure, naming conventions, and required cross-references for plans, architecture docs, examples, research, and analysis files.
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
  - Glob
---

# Claude Workspace Organization

## Purpose

Maintain organized working files in the `.claude/` directory with enforced structure, consistent naming, and required cross-references to codebase files and related documentation.

**Use this skill when:**
- Creating implementation plans, architecture decisions, or design documents
- Documenting research findings or code analysis
- Capturing reusable code examples or patterns
- Organizing existing loose planning files
- Validating workspace structure

## Directory Structure

```
.claude/
├── plans/              # Implementation plans, migration plans, project plans
│   └── INDEX.md
├── architecture/       # ADRs, design decisions, system diagrams
│   └── INDEX.md
├── examples/           # Code examples, usage patterns, reference implementations
│   └── INDEX.md
├── research/           # Research notes, external findings, comparative analysis
│   └── INDEX.md
└── analysis/           # Code analysis, performance studies, security reviews
    └── INDEX.md
```

---

## Essential Principles

### 1. Every File Links to Codebase

Every working file MUST contain at least one link to a relevant codebase file. No orphan documentation.

### 2. Every File Links to Related .claude/ Docs

Files should cross-reference related documents in other categories when relevant connections exist.

### 3. INDEX.md is Auto-Updated

When creating or modifying files, always update the category's INDEX.md.

### 4. Consistent Frontmatter

All files use YAML frontmatter with required fields per category. See [frontmatter-schemas.md](./references/frontmatter-schemas.md).

---

## Intake

**What would you like to do?**

1. **Create new file** - Create a plan, architecture doc, example, research, or analysis
2. **Update INDEX** - Manually refresh a category's INDEX.md
3. **Validate workspace** - Check workspace structure and fix issues
4. **Migrate existing** - Organize loose files into proper structure

**Wait for response before proceeding.**

---

## Routing

| Response | Workflow |
|----------|----------|
| 1, "create", "new", "add", "plan", "architecture", "example", "research", "analysis" | [create-file.md](./workflows/create-file.md) |
| 2, "index", "update index", "refresh" | [update-index.md](./workflows/update-index.md) |
| 3, "validate", "check", "verify" | [validate-workspace.md](./workflows/validate-workspace.md) |
| 4, "migrate", "organize", "cleanup", "move" | [migrate-existing.md](./workflows/migrate-existing.md) |

---

## Quick Reference

### File Naming Convention

```
{category}/{YYYY-MM-DD}-{kebab-case-description}.md
```

**Examples:**
- `plans/2025-01-07-user-authentication-migration.md`
- `architecture/2025-01-07-event-sourcing-design.md`
- `research/2025-01-07-auth-library-comparison.md`
- `examples/2025-01-07-pagination-pattern.md`
- `analysis/2025-01-07-n-plus-one-audit.md`

See [naming-conventions.md](./references/naming-conventions.md) for details.

### Required Cross-References

Every file MUST include a `## Related` section:

```markdown
## Related

### Codebase
- [user.rb](../../app/models/user.rb) - Primary model affected by this plan

### Related Documentation
- [Auth Architecture](../architecture/2025-01-07-auth-design.md) - Design decision this implements
```

See [cross-reference-rules.md](./references/cross-reference-rules.md) for full rules.

### Category Guide

| Category | Purpose | Status Values |
|----------|---------|---------------|
| plans/ | Implementation plans, migration plans | draft, in-progress, approved, implemented, superseded |
| architecture/ | ADRs, design decisions | proposed, accepted, deprecated, superseded |
| examples/ | Code patterns, reference implementations | (no status) |
| research/ | External research, comparisons | in-progress, complete |
| analysis/ | Code analysis, performance studies | in-progress, complete |

See [file-categories.md](./references/file-categories.md) for detailed guidance.

---

## Integration Points

**Invoked by:**
- Manual invocation when creating planning/architecture documents
- When Claude detects file creation that should go in .claude/
- `/workspace` command (if configured)

**Works with:**
- `file-todos` - Todos can link to plans or architecture docs
- `compound-docs` - Solution docs can reference research or analysis files
- `/workflows:plan` - Plans created via workflow can use this organization

---

## Success Criteria

A workspace file is valid when ALL of the following are true:

- Valid YAML frontmatter with all required fields
- File in correct category directory
- Filename follows `YYYY-MM-DD-description.md` pattern
- At least one codebase link in `## Related > ### Codebase`
- INDEX.md updated with file entry
