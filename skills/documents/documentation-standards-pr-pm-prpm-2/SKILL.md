---
name: documentation-standards
description: Standards and guidelines for organizing, structuring, and maintaining documentation in the PRPM repository - ensures consistency across user docs, development docs, and internal references
---

# PRPM Documentation Standards

## Documentation Organization

### Internal Documentation (development/docs/)
**Purpose:** Documentation for developers working on PRPM itself

**Location:** `development/docs/`

**Files:**
- `GITHUB_WORKFLOWS.md` - GitHub Actions workflows reference
- `PUBLISHING.md` - NPM package publishing process and order
- `DEVELOPMENT.md` - Development setup, environment, and workflows
- `DOCKER.md` - Docker setup, services, and troubleshooting

**Audience:** PRPM contributors, maintainers, CI/CD systems

---

### User-Facing Documentation (docs/)
**Purpose:** Documentation for PRPM users and package authors

**Location:** `docs/` (at project root)

**Files:**
- User guides
- API documentation
- Package authoring guides
- CLI command reference
- Examples and tutorials

**Audience:** PRPM end users, package authors, integrators

---

### Project-Level Documentation (root)
**Purpose:** Standard project files that belong at repository root

**Location:** Project root `/`

**Files:**
- `README.md` - Project overview, quick start, installation
- `CONTRIBUTING.md` - Contribution guidelines
- `CHANGELOG.md` - Version history and changes
- `LICENSE` - License information
- `ROADMAP.md` - Project roadmap and future plans

**Audience:** Everyone (first impression)

---

### Claude Skills (.claude/skills/)
**Purpose:** Knowledge base and reference materials for AI assistants

**Location:** `.claude/skills/`

**Files:**
- `postgres-migrations-skill.md` - PostgreSQL migrations guidance
- `pulumi-troubleshooting-skill.md` - Pulumi troubleshooting
- `NEW_SKILLS.md` - How to create new skills
- `documentation-standards.md` - This file

**Subdirectories:**
- `prpm-development/` - PRPM-specific development knowledge
- `self-improving/` - Self-improvement patterns
- `thoroughness/` - Thoroughness and quality guidelines

**Audience:** AI assistants (Claude, etc.)

---

## Rules for Documentation Placement

### When to use development/docs/
✅ GitHub Actions workflows and CI/CD
✅ Internal build/release processes
✅ Development environment setup
✅ Architecture decision records
✅ Internal troubleshooting guides
✅ Database schema documentation
✅ Infrastructure documentation

❌ User-facing tutorials
❌ CLI usage guides
❌ API reference for end users

### When to use docs/
✅ User guides and tutorials
✅ CLI command reference
✅ Package authoring guides
✅ API documentation for users
✅ Integration examples
✅ FAQ for users

❌ Internal development workflows
❌ CI/CD documentation
❌ Build/release processes

### When to use .claude/skills/
✅ Specialized knowledge for AI assistants
✅ Domain-specific best practices
✅ Troubleshooting patterns
✅ Code review guidelines
✅ Project-specific conventions

❌ General documentation
❌ User guides
❌ API references

---

## Documentation Standards

### Markdown Files
- Use clear, descriptive filenames (kebab-case)
- Include table of contents for docs > 200 lines
- Use proper heading hierarchy (# → ## → ###)
- Include code examples with syntax highlighting
- Add frontmatter if using a static site generator

### Example Structure
```markdown
# Title

Brief description (1-2 sentences)

## Table of Contents
- [Section 1](#section-1)
- [Section 2](#section-2)

## Section 1
Content...

### Subsection 1.1
Details...

## Examples
\`\`\`bash
# Example command
prpm install @username/package-name
\`\`\`

## See Also
- [Related Doc](./related.md)
```

### Cross-References
- Use relative paths for links
- Keep links within same category when possible
- Update links when moving files

**Internal → Internal:**
```markdown
See [Publishing Guide](./PUBLISHING.md)
```

**Internal → User:**
```markdown
See [User Guide](../../docs/user-guide.md)
```

---

## Migration Checklist

When reorganizing documentation:

1. ✅ Move file to correct location
2. ✅ Update all references to moved file
3. ✅ Update README.md links if needed
4. ✅ Update .gitignore if needed
5. ✅ Test that all links work
6. ✅ Commit with clear message explaining move

---

## Package-Specific Documentation

Each package should have its own README:

```
packages/
├── cli/
│   └── README.md          # CLI package overview
├── registry/
│   └── README.md          # Registry server docs
├── registry-client/
│   └── README.md          # Client library docs
├── types/
│   └── README.md          # Type definitions docs
└── webapp/
    └── README.md          # WebApp docs
```

---

## Maintenance

### Regular Reviews
- Quarterly review of docs/ for accuracy
- Remove outdated documentation
- Update examples to use latest version
- Check for broken links

### When Adding Features
- Update relevant user docs in `docs/`
- Update internal docs in `development/docs/` if needed
- Add examples
- Update CHANGELOG.md

### When Deprecating Features
- Add deprecation notice to docs
- Provide migration guide
- Keep docs until feature is removed
- Update CHANGELOG.md

---

## Quick Reference

| Documentation Type | Location | Audience | Examples |
|--------------------|----------|----------|----------|
| Internal Dev | `development/docs/` | Contributors | CI/CD, publishing |
| User-Facing | `docs/` | Users | Guides, tutorials |
| Project Root | `/` | Everyone | README, LICENSE |
| AI Skills | `.claude/skills/` | AI assistants | Troubleshooting |
| Package Docs | `packages/*/README.md` | Package users | API reference |

---

## Tools

### Documentation Generators
- **TypeDoc** - For TypeScript API docs (future)
- **VitePress** or **Docusaurus** - For docs/ site (future)

### Linting
```bash
# Check markdown
markdownlint docs/

# Check links
markdown-link-check docs/**/*.md
```

### Building Docs Site (Future)
```bash
cd docs/
npm run build
```

---

## Examples

### Good Documentation Structure
```
prpm/
├── README.md                    # Project overview
├── CONTRIBUTING.md              # How to contribute
├── CHANGELOG.md                 # Version history
├── ROADMAP.md                   # Future plans
├── development/
│   └── docs/
│       ├── GITHUB_WORKFLOWS.md  # CI/CD reference
│       ├── PUBLISHING.md        # Release process
│       ├── DEVELOPMENT.md       # Dev setup
│       └── DOCKER.md            # Services setup
├── docs/
│   ├── getting-started.md       # User onboarding
│   ├── cli-reference.md         # Command reference
│   ├── package-authoring.md     # Creating packages
│   └── api/
│       └── registry-client.md   # API docs
└── .claude/
    └── skills/
        ├── documentation-standards.md
        ├── postgres-migrations-skill.md
        └── pulumi-troubleshooting-skill.md
```

### Bad Documentation Structure ❌
```
prpm/
├── README.md
├── WORKFLOWS.md                 # Should be in development/docs/
├── USER_GUIDE.md                # Should be in docs/
├── dev-setup.md                 # Should be in development/docs/
└── troubleshooting.md           # Unclear audience/location
```

---

## Version

**Last Updated:** 2025-10-21
**Applies To:** PRPM v2+
**Review Date:** 2026-01-21
