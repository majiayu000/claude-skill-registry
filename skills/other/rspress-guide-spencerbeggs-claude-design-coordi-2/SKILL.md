---
name: rspress-guide
description: Generate progressive learning guides for RSPress documentation. Use when
  creating concept docs, how-to guides, or example pages with Twoslash code blocks.
allowed-tools: Read, Glob, Grep, Edit, Write
context: fork
agent: rspress-doc-agent
---

# Generate RSPress Learning Guide

Generates progressive learning guides (concepts, guides, examples) for
RSPress documentation sites.

## Overview

This skill creates structured, user-friendly documentation pages with:

1. Template-based page generation
2. Twoslash VFS code examples
3. Cross-links to API documentation
4. Progressive disclosure patterns
5. Navigation metadata updates

## Quick Start

**Generate a concept page:**

```bash
/rspress-guide effect-type-registry --type=concept --topic="Caching Strategy"
```

**Generate a how-to guide:**

```bash
/rspress-guide rspress-plugin-api-extractor --type=guide --topic="Testing Hooks"
```

**Generate an example page:**

```bash
/rspress-guide website --type=example --topic="Blog Integration"
```

## How It Works

### 1. Parse Parameters

- `module`: Module name from design.config.json [REQUIRED]
- `--type`: Page type (concept, guide, example) [REQUIRED]
- `--topic`: Page topic/title [REQUIRED]
- `--design-docs`: Path to design docs (optional)
- `--template`: Custom template path (optional)
- `--dry-run`: Preview without writing (optional)

### 2. Load Configuration

Reads `design.config.json` to determine:

- Module's `siteDocs` path
- Design docs location
- RSPress configuration path

Reads `rspress.config.ts` to understand:

- Available dependencies for Twoslash
- API extractor configuration
- Global components

### 3. Select Template

Uses appropriate template based on page type:

- **Concept**: `.claude/templates/rspress-concept.mdx`
- **Guide**: `.claude/templates/rspress-guide.mdx`
- **Example**: `.claude/templates/rspress-example.mdx`

Falls back to default templates if custom ones not found.

### 4. Generate Content

For each page type:

**Concept Pages:**

- Explain single concept in depth
- Include diagrams (Mermaid)
- Show common patterns
- Link to related concepts
- Cross-link to API docs

**Guide Pages:**

- Task-oriented how-to
- Step-by-step instructions
- Complete working examples
- Troubleshooting section
- Next steps guidance

**Example Pages:**

- Real-world scenario
- Complete solution with annotations
- Alternative approaches
- Related examples

### 5. Create Twoslash Code Blocks

All code examples use `typescript twoslash vfs`:

- Complete, compilable TypeScript programs
- Explicit imports for all types
- Auto-loaded dependencies from rspress.config.ts
- Cut notations to hide boilerplate

### 6. Add Cross-References

Links to related content:

- API documentation (auto-generated)
- Related concept pages
- Related guides
- Related examples

### 7. Update Navigation

Updates or creates `_meta.json` in the section directory to include the
new page.

### 8. Validate

Checks:

- MDX syntax is valid
- Frontmatter is complete
- Navigation structure is correct
- Cross-references resolve

## Supporting Documentation

- `instructions.md` - Detailed generation process
- `examples.md` - Sample outputs for each page type

## Success Criteria

- ✅ Page created in correct location
- ✅ Twoslash code blocks are complete
- ✅ Cross-links to API docs work
- ✅ Navigation metadata updated
- ✅ MDX syntax is valid

## Integration Points

- Uses `.claude/design/design.config.json`
- Reads `rspress.config.ts` for dependencies
- Uses templates from `.claude/templates/`
- Updates `_meta.json` files for navigation

## Related Skills

- `/rspress-page` - Scaffold basic RSPress pages
- `/rspress-examples` - Generate code examples
- `/rspress-navigation` - Generate navigation structure
- `/rspress-review` - Review doc quality
