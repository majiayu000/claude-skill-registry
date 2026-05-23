---
name: deep-analyze
description: >
  Deep codebase analysis that extracts learnings from documentation.
  Creates context entries and learnings from docs/ with pattern matching.
---

# Deep Analyze

Extract full content and learnings from your documentation.

## What It Does

Runs `kodo analyze --deep --auto` which:

1. **Standard Analysis** - All normal analyzers (tech-stack, architecture, etc.)
2. **Content Extraction** - Parses all `.md` files in `docs/`
3. **Learning Extraction** - Finds patterns:
   - Rules: "always/never/must" statements
   - Decisions: "we chose X because..."
   - Tech Stack: "uses X for..."
   - Workflows: step sequences
   - Domain: entity definitions
   - Conventions: naming patterns

## Output

- `.kodo/context-tree/` - Context entries with YAML frontmatter
- `.kodo/learnings/` - Learnings grouped by category:
  - `rules.md`
  - `decisions.md`
  - `tech-stack.md`
  - `workflows.md`
  - `domain.md`
  - `conventions.md`

## Confidence Levels

- **HIGH** - Your design docs (`docs/plans/`)
- **MEDIUM** - Inherited/pre-existing documentation

## Usage

Just invoke this skill - it runs automatically:

```bash
# This skill runs:
kodo analyze --deep --auto
```

## When to Use

- Starting a new project with existing docs
- After writing design documents
- When onboarding to capture institutional knowledge
- Before major refactoring to preserve context

## Single File Extraction

For extracting from a single file:

```bash
kodo extract docs/plans/your-design.md
# or
kodo x docs/plans/your-design.md
```
