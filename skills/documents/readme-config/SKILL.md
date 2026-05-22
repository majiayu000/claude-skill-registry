---
name: readme-config
description: README.md documentation templates and validation logic for MetaSaver monorepos. Includes repository type detection (library vs consumer), required sections (Title, Description, Installation, Usage, Scripts), and line count guidance (consumer 75-100 lines, library 150-200 lines). Use when creating or auditing README.md files at monorepo root.
---

# README.md Configuration Skill

This skill provides README.md templates and validation logic for project documentation following MetaSaver standards based on repository type.

## Purpose

Manage README.md documentation to:

- Provide clear project overview and quick start
- Follow repository type conventions (library vs consumer)
- Include required sections and structure
- Link to detailed documentation
- Maintain appropriate content length

## Usage

This skill is invoked by the `readme-agent` when:

- Creating new README.md files at monorepo root
- Auditing existing README.md documentation
- Validating README.md against type-specific standards

## Templates

Two standard README templates are located at:

```
templates/root-readme-consumer.md.template
templates/root-readme-library.md.template
```

## Repository Type Detection

Use `/skill scope-check` if not provided.

**Quick Reference:** Library = `@metasaver/multi-mono`, Consumer = all other repos

## Standards by Repository Type

| Type     | Target Lines | Required Sections                                   | Location  |
| -------- | ------------ | --------------------------------------------------- | --------- |
| Consumer | 75-100       | Title, Overview, Quick Start, Commands, Docs links  | Root only |
| Library  | 150-200      | Title, Packages, Quick Start, Integration, Commands | Root only |

## Consumer Repository README Standards

**Target:** 75-100 lines of focused, essential information

### Required Sections

1. **Title with @metasaver scope**

```markdown
# @metasaver/consumer-repo-name

**Architecture:** Multi-mono consumer
```

2. **Overview section with features**

- Brief project description
- Key features (3-5 bullet points)
- Technology stack

3. **Quick Start section**

```markdown
## Quick Start

pnpm setup:all # Install dependencies
docker:up # Start infrastructure
db:migrate # Run migrations
dev # Start development server
```

4. **Commands section**

- Development commands (dev, build)
- Database commands (db:migrate, db:seed)
- Quality commands (lint, test)
- Docker commands (docker:up, docker:down)

5. **Documentation links**

```markdown
## Documentation

- [Setup Guide](docs/SETUP.md)
- [Development Guide](CLAUDE.md)
```

### Validation

```bash
# Check title with @metasaver scope
grep -q "# @metasaver/" README.md || echo "VIOLATION: Missing @metasaver scope in title"

# Check architecture line
grep -q "Architecture.*consumer" README.md || echo "VIOLATION: Missing architecture identifier"

# Check required sections
grep -q "## Overview" README.md || echo "VIOLATION: Missing Overview section"
grep -q "## Quick Start" README.md || echo "VIOLATION: Missing Quick Start section"
grep -q "## Commands" README.md || echo "VIOLATION: Missing Commands section"

# Check documentation links
grep -q "SETUP.md" README.md || echo "VIOLATION: Missing SETUP.md link"
grep -q "CLAUDE.md" README.md || echo "VIOLATION: Missing CLAUDE.md link"

# Check line count (guidance, not strict)
LINE_COUNT=$(wc -l < README.md)
[ $LINE_COUNT -gt 120 ] && echo "WARNING: README.md exceeds 100 lines ($LINE_COUNT lines) - consider condensing"
```

## Library Repository README Standards

**Target:** 150-200 lines (flexible based on package count)

### Required Sections

1. **Title (@metasaver/multi-mono)**

```markdown
# @metasaver/multi-mono

**Architecture:** Multi-mono producer library
```

2. **Producer/library role explanation**

- Explain shared package purpose
- Describe workspace protocol usage
- Note consumer repository dependencies

3. **Packages section with descriptions**

```markdown
## Packages

### Core Packages

- `@metasaver/package-name` - Brief description

### Shared Packages

- `@metasaver/shared-utils` - Brief description
```

4. **Quick Start section**

```markdown
## Quick Start

pnpm install # Install dependencies
pnpm build # Build all packages
pnpm test # Run all tests
```

5. **Integration guide showing workspace:\* protocol**

```markdown
## Integration

Add to consumer package.json:

{
"dependencies": {
"@metasaver/package-name": "workspace:\*"
}
}
```

6. **Commands section**

- Build commands (build, build:packages)
- Test commands (test, test:watch)
- Quality commands (lint, type-check)

### Validation

```bash
# Check title
grep -q "# @metasaver/multi-mono" README.md || echo "VIOLATION: Missing library title"

# Check architecture line
grep -q "Architecture.*producer" README.md || echo "VIOLATION: Missing architecture identifier"

# Check required sections
grep -q "## Packages" README.md || echo "VIOLATION: Missing Packages section"
grep -q "## Quick Start" README.md || echo "VIOLATION: Missing Quick Start section"
grep -q "## Integration" README.md || echo "VIOLATION: Missing Integration section"
grep -q "workspace:\*" README.md || echo "VIOLATION: Missing workspace protocol example"

# Line count is flexible for libraries (depends on package count)
LINE_COUNT=$(wc -l < README.md)
[ $LINE_COUNT -lt 100 ] && echo "WARNING: README.md may be too brief ($LINE_COUNT lines) for library repo"
```

## Best Practices

1. **Root only** - README.md belongs at repository root
2. **Consumer: FOCUSED** - 75-100 lines with essential info only
3. **Library: FLEXIBLE** - As long as needed for package descriptions
4. **Link to detailed docs** - README is entry point, docs/ have details
5. **Detect repo type first** - Check package.json name for @metasaver scope
6. **Re-audit after changes** - Verify compliance

## Repository Type Considerations

- **Consumer Repos**: Strict enforcement, concise content, quick start emphasis
- **Library Repos**: Flexible length, package descriptions, integration guide emphasis
- **All Repos**: Must have README.md at root only (not in subdirectories for monorepo root)

## Integration

This skill integrates with:

- Repository type provided via `scope` parameter. If not provided, use `/skill scope-check`
- `/skill audit-workflow` - Bi-directional comparison workflow
- `/skill remediation-options` - Conform/Update/Ignore choices
