---
name: docs-generate-repo
description: Generate Level 2 (repository docs) from design docs. Use when
  creating comprehensive topic-based documentation for developers.
allowed-tools: Read, Glob, Edit, Write
context: fork
agent: docs-gen-agent
---

# Generate Repository Documentation

Generates Level 2 repository documentation from design docs with
topic-based organization.

## Overview

This skill transforms design documentation into comprehensive
repository documentation by:

1. Analyzing design docs for the module
2. Creating topic-based documentation structure
3. Generating architecture guides
4. Creating integration guides
5. Adding troubleshooting sections
6. Following the Level 2 template structure

## Quick Start

**Generate all repository docs for a module:**

```bash
/docs-generate-repo effect-type-registry
```

**Generate specific topic only:**

```bash
/docs-generate-repo effect-type-registry --topic=caching
```

**Preview without writing:**

```bash
/docs-generate-repo rspress-plugin-api-extractor --dry-run
```

## How It Works

### 1. Parse Parameters

- `module`: Module name to generate docs for [REQUIRED]
- `--topic`: Generate specific topic only (default: all topics)
- `--structure`: Output directory structure (default: `docs/`)
- `--dry-run`: Preview file structure without writing

### 2. Load Configuration and Design Docs

Read `.claude/design/design.config.json` for:

- Module configuration and paths
- Repository docs settings (Level 2)
- Quality standards

Read design docs:

- Find all design docs for module
- Parse frontmatter and content
- Identify major topics and sections
- Map design content to user-facing topics

### 3. Identify Topics from Design Docs

Extract major topics from design documentation:

- **Architecture topics** - System design, components, data flow
- **Feature topics** - Specific capabilities and how they work
- **Integration topics** - Using with other tools and frameworks
- **Performance topics** - Optimization and benchmarks
- **Testing topics** - How to test code using the package

### 4. Generate Topic Documentation

For each topic:

**Extract Content:**

- Overview from design doc introduction
- Key concepts explained simply
- Usage patterns and examples
- API reference for topic
- Common issues and solutions

**Apply Transformations:**

- Simplify technical language
- Add practical examples
- Include troubleshooting
- Cross-link related topics

### 5. Create Documentation Structure

Organize generated docs into directories:

```text
docs/
├── README.md               # Index of all documentation
├── architecture/
│   ├── overview.md        # High-level architecture
│   └── components.md      # Component breakdown
├── guides/
│   ├── getting-started.md # Detailed getting started
│   └── {topic}.md         # Topic-specific guides
└── troubleshooting.md     # Common issues
```

### 6. Write Documentation Files

Write each generated document:

- Apply repo-doc template
- Fill in topic-specific content
- Add table of contents for longer docs
- Validate against Level 2 standards

### 7. Validate Output

Check generated docs:

- Length: 500-2000 words per document
- Code examples present
- Cross-references valid
- Markdown linting passes

## Supporting Documentation

Load these files for detailed guidance:

- `instructions.md` - Step-by-step implementation
- `examples.md` - Example repository documentation
- `topic-mapping.md` - Design doc to user doc topic mapping

## Success Criteria

Generated repository documentation is successful when:

- ✅ Comprehensive coverage of module features
- ✅ Topic-based organization (not implementation-based)
- ✅ 500-2000 words per document
- ✅ Practical code examples in each guide
- ✅ Cross-references between related topics
- ✅ Table of contents for documents >800 words
- ✅ Troubleshooting section with common issues
- ✅ Valid markdown and working examples

## Integration Points

- Uses `.claude/design/design.config.json` for configuration
- Uses `.claude/skills/docs-generate-repo/templates/repo-doc.template.md` for structure
- Reads design docs from module's `designDocsPath`
- Writes to module's `userDocs.repoDocs` path
- Validates against `quality.userDocs.level2` standards

## Related Skills

- `/docs-generate-readme` - Generate Level 1 package README
- `/docs-generate-site` - Generate Level 3 site documentation
- `/docs-sync` - Sync docs with design doc changes
- `/design-review` - Review source design docs
