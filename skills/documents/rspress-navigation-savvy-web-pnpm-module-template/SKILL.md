---
name: rspress-navigation
description: Generate progressive navigation structure for RSPress documentation. Use
  when setting up or reorganizing module documentation navigation.
allowed-tools: Read, Glob, Grep, Edit, Write
context: fork
agent: rspress-doc-agent
---

# Generate RSPress Navigation Structure

Generates progressive navigation structure (`_meta.json` files) for RSPress
documentation sites.

## Overview

This skill creates hierarchical navigation by:

1. Analyzing existing documentation structure
2. Organizing content by user journey
3. Creating `_meta.json` files
4. Setting collapsible sections
5. Ordering content progressively (basic → advanced)
6. Generating breadcrumb paths

## Quick Start

**Generate navigation for entire module:**

```bash
/rspress-navigation effect-type-registry
```

**Generate navigation for specific section:**

```bash
/rspress-navigation rspress-plugin-api-extractor --section=guides
```

**Preview structure without writing:**

```bash
/rspress-navigation website --dry-run
```

## How It Works

### 1. Parse Parameters

- `module`: Module name from design.config.json [REQUIRED]
- `--section`: Specific section (concepts, guides, examples) (optional)
- `--strategy`: Organization strategy (journey, alphabetical, category)
  (optional)
- `--dry-run`: Preview without writing (optional)

### 2. Load Module Configuration

Reads `design.config.json` to find:

- Site docs path
- Module structure
- Configured sections

### 3. Scan Documentation Structure

Finds all documentation files:

- Landing page (index.mdx)
- Concept pages (concepts/*.mdx)
- Guide pages (guides/*.mdx)
- Example pages (examples/*.mdx)
- API docs (api/*.md - excluded from user navigation)

### 4. Extract Page Metadata

For each page, reads:

- Frontmatter title
- File name
- Heading structure
- Dependencies (prerequisites)
- Complexity indicators

### 5. Determine Organization Strategy

**User Journey (default):**

- Order by learning progression
- Beginner content first
- Advanced content last
- Related pages grouped

**Alphabetical:**

- Sort by title A-Z
- Simple, predictable
- Good for reference sections

**Category:**

- Group by topic/feature
- Collapsible categories
- Related content together

### 6. Generate Top-Level Navigation

Creates `{siteDocs}/_meta.json`:

```json
{
  "index": {
    "title": "Overview",
    "type": "page"
  },
  "concepts": {
    "title": "Concepts",
    "type": "dir",
    "collapsible": true,
    "collapsed": false
  },
  "guides": {
    "title": "Guides",
    "type": "dir",
    "collapsible": true,
    "collapsed": false
  },
  "examples": {
    "title": "Examples",
    "type": "dir",
    "collapsible": true,
    "collapsed": true
  },
  "api": {
    "title": "API Reference",
    "type": "dir",
    "collapsible": true,
    "collapsed": true
  }
}
```

### 7. Generate Section Navigation

Creates `{siteDocs}/{section}/_meta.json` for each section:

```json
{
  "index": {
    "title": "Overview"
  },
  "getting-started": {
    "title": "Getting Started"
  },
  "advanced-usage": {
    "title": "Advanced Usage"
  }
}
```

### 8. Set Collapsible Behavior

Determines which sections should be:

- **Expanded by default**: Core concepts, getting started
- **Collapsed by default**: Advanced topics, API reference
- **Always visible**: Critical pages

### 9. Validate Navigation

Checks:

- All `_meta.json` files are valid JSON
- All referenced files exist
- No orphaned pages (files not in navigation)
- No circular references
- Breadcrumb paths work

### 10. Generate Navigation Report

Creates report with:

- Navigation structure visualization
- Orphaned pages
- Missing titles
- Recommended improvements

## Organization Strategies

### User Journey Strategy

Organizes content for progressive learning:

1. Overview (what and why)
2. Getting Started (first steps)
3. Basic Concepts (foundations)
4. How-To Guides (common tasks)
5. Advanced Concepts (deeper understanding)
6. Examples (real-world scenarios)
7. API Reference (detailed specs)

### Alphabetical Strategy

Simple A-Z ordering:

- Predictable navigation
- Easy to find specific topics
- No semantic grouping

### Category Strategy

Groups by topic or feature:

- Related content together
- Collapsible categories
- Feature-based navigation

## Navigation Best Practices

**Hierarchy:**

- Max 3 levels deep
- Landing page at root
- Sections for major topics
- Individual pages within sections

**Ordering:**

- Basic before advanced
- Prerequisites before dependents
- Frequently used before rarely used
- Concepts before implementation

**Titles:**

- Clear and descriptive
- Consistent naming
- Action-oriented for guides ("How to...")
- Noun-based for concepts

**Collapsibility:**

- Core content expanded by default
- Advanced content collapsed
- API reference collapsed
- Examples collapsed unless featured

## Supporting Documentation

- `instructions.md` - Detailed navigation generation process
- `examples.md` - Sample navigation structures

## Success Criteria

- ✅ All `_meta.json` files generated
- ✅ Valid JSON structure
- ✅ All pages included in navigation
- ✅ Logical ordering applied
- ✅ Collapsible sections configured
- ✅ No orphaned pages

## Integration Points

- Uses `.claude/design/design.config.json`
- Scans files in `{siteDocs}` directory
- Reads frontmatter from MDX files
- Excludes auto-generated API docs from organization

## Related Skills

- `/rspress-guide` - Generate documentation pages
- `/rspress-page` - Scaffold individual pages
- `/rspress-nav` - Configure top-level navigation
- `/rspress-review` - Review navigation structure
