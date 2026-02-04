---
name: monorepo-readme
description: |
  Write README files for monorepo projects with multiple packages.
  Use when: (1) creating monorepo root README, (2) adding package
  to monorepo, (3) documenting workspace commands. Covers architecture
  diagrams, package tables, build order, publishing workflows.
category: documentation
user-invocable: true
---

# Monorepo README

Write effective README files for monorepo projects.

## Quick Reference

| README Location | Purpose | Key Sections |
|-----------------|---------|--------------|
| Root README | Project overview, architecture | Package table, architecture diagram |
| Package README | Package-specific docs | API, installation, usage |

## Root vs Package README

### Root README Should Have

- Project overview and tagline
- Architecture diagram (Mermaid)
- Package table with descriptions
- Workspace commands (install, build, test)
- Development workflow
- Publishing/release process
- Contributing guide link

### Package README Should Have

- Package-specific tagline
- Installation (from npm)
- API/usage documentation
- Link back to root README
- Package-specific contributing notes

## Architecture Diagram

Use Mermaid for package relationships:

```markdown
\`\`\`mermaid
graph TD
    A[cli] --> B[library]
    A --> C[config]
    B --> C
    D[web] --> B
\`\`\`
```

## Package Table

List all packages with their purpose:

```markdown
## Packages

| Package | Description | npm |
|---------|-------------|-----|
| `@scope/cli` | Command-line interface | [![npm](badge-url)](npm-url) |
| `@scope/lib` | Core library | [![npm](badge-url)](npm-url) |
| `@scope/config` | Shared configuration | (internal) |
```

## Workspace Commands

Document common workspace operations:

```markdown
## Development

\`\`\`bash
# Install all dependencies
npm install

# Build all packages
npm run build

# Test all packages
npm test

# Build specific package
npm run build -w @scope/cli
\`\`\`
```

## Decision Tree

**What goes in root README?**
- Overview and "why use this" → Root
- Architecture and package relationships → Root
- How to contribute → Root
- Detailed API for one package → Package

**What goes in package README?**
- Package-specific installation → Package
- Package-specific API docs → Package
- Package-specific examples → Package
- How packages work together → Root

## Reference Files

| Topic | File |
|-------|------|
| README responsibilities | [references/root-vs-package.md](references/root-vs-package.md) |
| Mermaid patterns | [references/architecture.md](references/architecture.md) |
| Publishing workflow | [references/publishing.md](references/publishing.md) |

## Skill Chaining

This skill works with:
- **readme-writer**: For general README best practices
- **markdown-writer**: For consistent prose style
- **doc-maintenance**: For keeping READMEs updated

## Sources

- [wixplosives/sample-monorepo](https://github.com/wixplosives/sample-monorepo)
- [Lerna documentation](https://lerna.js.org/)
- [npm workspaces](https://docs.npmjs.com/cli/using-npm/workspaces)
