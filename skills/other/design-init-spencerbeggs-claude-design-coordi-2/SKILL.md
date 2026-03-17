---
name: design-init
description: Initialize new design documentation from templates. Use when creating new design docs, documenting new systems, starting architecture documentation, or setting up design docs for a new module.
allowed-tools: Read, Write, Glob, AskUserQuestion
context: fork
agent: design-doc-agent
---

# Design Documentation Initialization

Creates new design documentation files from templates with proper frontmatter
and structure.

## Overview

This skill initializes new design documentation files by:

1. Reading the design configuration
2. Selecting the appropriate template based on category
3. Populating frontmatter with current metadata
4. Creating the file in the correct module location
5. Validating the output

## Quick Start

**Basic usage:**

```bash
/design-init effect-type-registry cache-optimization
```

**With explicit category:**

```bash
/design-init rspress-plugin-api-extractor component-lifecycle --category=architecture
```

**Specify template:**

```bash
/design-init website deployment --template=default
```

## Parameters

### Required

- `module` - Module name (must exist in config)
- `topic` - Topic/filename for the document (kebab-case)

### Optional

- `category` - Design doc category (default: infer from topic)
- `template` - Specific template to use (default: auto-select)

## Workflow Overview

1. **Parse Parameters** - Extract module, topic, category, template
2. **Load Configuration** - Read config, verify module exists
3. **Determine Category** - Infer from topic or ask user
4. **Select Template** - Category-specific or default
5. **Populate Frontmatter** - Set status, dates, metadata
6. **Populate Body** - Replace template variables
7. **Determine Path** - Construct output path
8. **Create File** - Write to disk
9. **Report Success** - Show summary and next steps

## Supporting Documentation

### For Detailed Workflow Steps

See [instructions.md](instructions.md) for:

- Complete step-by-step workflow
- Validation rules before creation
- Special case handling
- Success criteria

**Load when:** Need detailed implementation guidance or handling edge cases

### For Category and Template Selection

See [category-templates.md](category-templates.md) for:

- Category inference patterns and keywords
- Template selection logic
- Template variable replacement
- Title case conversion rules

**Load when:** Determining which category or template to use for a new doc

### For Error Handling

See [error-messages.md](error-messages.md) for:

- All error message formats
- Error handling strategies
- Special case handling (long names, invalid chars, existing files)
- Fix instructions for each error type

**Load when:** Encountering errors or need to handle edge cases

### For Usage Examples

See [examples.md](examples.md) for:

- Complete usage scenarios
- Example outputs for different cases
- Multi-step walkthroughs
- Success report format

**Load when:** User wants to see concrete examples or needs clarification

## Integration

Use this skill in combination with:

- `/design-validate` - Validate after creation
- `/design-update` - Update newly created docs
- `/design-review` - Review doc quality
