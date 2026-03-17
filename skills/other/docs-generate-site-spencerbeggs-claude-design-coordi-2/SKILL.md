---
name: docs-generate-site
description: Generate Level 3 (documentation sites) from design docs. Use when
  creating feature-rich, interactive documentation for RSPress/Docusaurus sites.
allowed-tools: Read, Glob, Edit, Write
context: fork
agent: docs-gen-agent
---

# Generate Documentation Site

Generates Level 3 documentation site content from design docs with
framework-specific features.

## Overview

This skill transforms design documentation into interactive documentation
site content by:

1. Analyzing design docs for the module
2. Creating landing page with hero and features
3. Generating getting started guide
4. Creating concept documentation
5. Generating how-to guides
6. Integrating with API docs
7. Following framework-specific template (RSPress, Docusaurus, VitePress)

## Quick Start

**Generate RSPress site docs:**

```bash
/docs-generate-site effect-type-registry --framework=rspress
```

**Include API docs integration:**

```bash
/docs-generate-site rspress-plugin-api-extractor --framework=rspress \
  --api-docs=./docs/en/api
```

**Preview without writing:**

```bash
/docs-generate-site website --framework=rspress --dry-run
```

## How It Works

### 1. Parse Parameters

- `module`: Module to document [REQUIRED]
- `--framework`: Documentation framework (rspress, docusaurus, vitepress)
- `--api-docs`: Path to auto-generated API docs to integrate
- `--dry-run`: Preview structure without writing

### 2. Load Configuration

Read `.claude/design/design.config.json` for:

- Module configuration
- Site docs settings (Level 3)
- Framework configuration
- Output directory

### 3. Analyze Design Documentation

Extract content for different doc types:

- **Landing page** - Overview, value propositions, key features
- **Getting started** - Installation, first example, next steps
- **Concepts** - Architecture, design decisions, how it works
- **Guides** - Task-oriented how-tos
- **Examples** - Real-world use cases

### 4. Generate Landing Page

Create `index.mdx` with framework-specific features:

- Hero section with description
- Feature highlights
- Quick start preview
- Links to guides

**RSPress-specific:**

- Use frontmatter for hero configuration
- Add feature cards
- Include navigation

### 5. Generate Getting Started Guide

Create progressive learning path:

1. Installation (detailed)
2. First working example
3. Understanding the basics
4. Common patterns
5. Next steps

### 6. Generate Concept Documentation

Transform architecture design docs into user-friendly concepts:

- Break down into digestible topics
- Add diagrams and visualizations
- Progressive disclosure (beginner → advanced)
- Use framework components (tabs, callouts)

### 7. Generate How-To Guides

Create task-oriented guides:

- Specific problems and solutions
- Complete working examples
- Step-by-step instructions
- Troubleshooting tips

### 8. Apply Framework Features

**RSPress features:**

- Tabs for multiple approaches
- Callouts (tip, warning, note)
- Code blocks with copy button
- Mermaid diagrams

**Docusaurus features:**

- Admonitions
- Code blocks with highlighting
- Tabs
- MDX components

### 9. Create Navigation Structure

Generate navigation metadata:

- Sidebar configuration
- Category organization
- Progressive navigation flow

### 10. Validate Output

Check generated site docs:

- Framework-specific frontmatter valid
- MDX syntax correct
- Interactive elements work
- Cross-references valid

## Supporting Documentation

Load these files when needed:

- `instructions.md` - Step-by-step implementation
- `examples.md` - Example site documentation
- `framework-features.md` - Framework-specific component usage

## Success Criteria

Generated site documentation is successful when:

- ✅ Engaging landing page with clear value proposition
- ✅ Progressive getting started guide
- ✅ Concept docs broken into digestible topics
- ✅ Task-oriented how-to guides
- ✅ Interactive elements (tabs, callouts, code blocks)
- ✅ Clear navigation structure
- ✅ API docs integrated (if available)
- ✅ Mobile responsive
- ✅ Valid framework-specific syntax

## Integration Points

- Uses `.claude/design/design.config.json` for configuration
- Uses `.claude/skills/docs-generate-site/templates/site-doc.template.mdx` for structure
- Reads design docs from module's `designDocsPath`
- Writes to module's `userDocs.siteDocs` path
- Validates against `quality.userDocs.level3` standards

## Related Skills

- `/docs-generate-readme` - Generate Level 1 README
- `/docs-generate-repo` - Generate Level 2 repository docs
- `/rspress-page` - Create individual RSPress pages
- `/docs-sync` - Sync docs with changes
