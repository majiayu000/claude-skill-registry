---
name: docs-generate-readme
description: Generate Level 1 (README.md) user documentation from design docs. Use when creating or updating package README files for npm/GitHub.
allowed-tools: Read, Glob, Edit, Write
context: fork
agent: docs-gen-agent
---

# Generate Package README

Generates Level 1 user documentation (README.md) from design docs and package metadata.

## Overview

This skill transforms internal design documentation into a user-friendly
package README by:

1. Reading design docs for the module
2. Extracting package.json metadata
3. Analyzing the overview and features
4. Generating quick start examples
5. Creating or updating README.md following the Level 1 template
6. Ensuring readability and accessibility for npm/GitHub users

## Quick Start

**Generate README for a module:**

```bash
/docs-generate-readme effect-type-registry
```

**Update existing README preserving custom sections:**

```bash
/docs-generate-readme rspress-plugin-api-extractor --update
```

**Preview without writing:**

```bash
/docs-generate-readme website --dry-run
```

## How It Works

### 1. Parse Parameters

- `module`: Module name to generate README for [REQUIRED]
- `--template`: Custom template path (default: `.claude/skills/docs-generate-readme/templates/readme.template.md`)
- `--dry-run`: Preview output without writing
- `--update`: Update existing README preserving custom sections

### 2. Load Configuration and Context

Read `.claude/design/design.config.json` to get:

- Module configuration and paths
- User docs configuration (Level 1 settings)
- Quality standards for READMEs

Read module metadata:

- `package.json` - name, version, description, license, dependencies
- Design docs in module's `designDocsPath`
- Existing README.md (if `--update` mode)

### 3. Extract Content from Design Docs

**Overview Section:**

- Extract high-level purpose from design doc overview
- Simplify to 1-2 sentence description
- Remove technical jargon

**Features:**

- Extract key features from design docs
- Transform technical features into user benefits
- Format as 3-5 bullet points
- Focus on "what it does" not "how it works"

**Quick Start:**

- Find common usage patterns in design docs
- Create minimal working example (5-15 lines)
- Ensure example is copy-paste ready
- Include imports and basic setup

**API Overview:**

- List main exports and their purposes
- High-level only (not exhaustive)
- Link to detailed API documentation

### 4. Apply Transformation Rules

Transform internal terminology to user-friendly language:

- "Architecture" → omit (too technical)
- "Implementation Details" → simplify to "How it works" (optional)
- "Integration Points" → "Usage with other tools"
- Effect-TS patterns → plain TypeScript
- Internal service names → public API names

### 5. Generate README Content

Fill the Level 1 template with extracted content:

- Package name and description
- Features list
- Installation command
- Quick start example
- API overview with link to full docs
- Links to documentation, contributing, license

### 6. Write or Update README

**New README mode (default):**

- Write complete README.md to module root
- Validate against Level 1 quality standards
- Check line length, word count, required sections

**Update mode (`--update`):**

- Parse existing README.md
- Preserve custom sections (badges, screenshots, etc.)
- Update standard sections with new content
- Maintain user-added examples

**Dry-run mode (`--dry-run`):**

- Generate content but don't write
- Display preview to user
- Show what would change

### 7. Validate Output

Check generated README against quality standards:

- Length: 200-500 words (warn if >800)
- Required sections: Description, Installation, Quick Start, Links
- Code examples are valid TypeScript
- Links are not broken
- Markdown linting passes

## Supporting Documentation

When you need detailed information, load these files:

- `instructions.md` - Detailed step-by-step implementation
- `transformation-rules.md` - Content transformation guidelines
- `examples.md` - Example READMEs and transformations
- `quality-standards.md` - Validation criteria

## Success Criteria

A generated README is successful when:

- ✅ Clear, accessible description (1-2 sentences)
- ✅ 3-5 user-benefit focused features
- ✅ Working quick start example (copy-paste ready)
- ✅ All required sections present
- ✅ 200-500 words total length
- ✅ No technical jargon or internal terms
- ✅ Valid markdown and code examples
- ✅ Links to comprehensive documentation

## Example Usage

```bash
# Generate README for effect-type-registry
/docs-generate-readme effect-type-registry

# Output: pkgs/effect-type-registry/README.md created
# Content:
# - Title: effect-type-registry
# - Description: TypeScript type definition registry with caching
# - Features: Version-aware caching, HTTP retry, VFS generation
# - Quick start: 10-line working example
# - Links: API docs, contributing, license
```

## Integration Points

- Uses `.claude/design/design.config.json` for module configuration
- Uses `.claude/skills/docs-generate-readme/templates/readme.template.md` for structure
- Reads design docs from module's `designDocsPath`
- Reads `package.json` for metadata
- Writes to module's `userDocs.readme` path
- Validates against `quality.userDocs.level1` standards

## Related Skills

- `/docs-sync` - Sync README with design doc changes
- `/docs-review` - Review README quality
- `/docs-generate-repo` - Generate Level 2 repository docs
- `/design-review` - Review source design documentation
