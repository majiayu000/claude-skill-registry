---
name: learned-docs
description: This skill should be used when writing, modifying, or reorganizing
  documentation in docs/learned/. Use when creating new documents, updating frontmatter,
  choosing categories, creating index files, updating routing tables, or moving
  files between categories. Essential for maintaining consistent documentation structure.
---

# Learned Documentation Guide

Overview: `docs/learned/` contains agent-focused documentation with:

- YAML frontmatter for routing and discovery
- Hierarchical category organization (categories listed in index below)
- Index files for category navigation
- Routing tables in AGENTS.md

## Core Knowledge (ALWAYS Loaded)

@learned-docs-core.md

## Document Registry (Auto-Generated)

@docs/learned/index.md

## Frontmatter Requirements

Every markdown file (except index.md) MUST have:

```yaml
---
title: Document Title
read_when:
  - "first condition"
  - "second condition"
---
```

### Required Fields

| Field       | Type         | Purpose                                    |
| ----------- | ------------ | ------------------------------------------ |
| `title`     | string       | Human-readable title for index tables      |
| `read_when` | list[string] | Conditions when agent should read this doc |

### Writing Effective read_when Values

- Use gerund phrases: "creating a plan", "styling CLI output"
- Be specific: "fixing merge conflicts in tests" not "tests"
- Include 2-4 conditions covering primary use cases
- Think: "An agent should read this when they are..."

Good:

```yaml
read_when:
  - "creating or closing plans"
  - "understanding plan states"
  - "working with .impl/ folders"
```

Bad:

```yaml
read_when:
  - "plans" # Too vague
  - "the user asks" # Not descriptive
```

## Documentation Structure

**Read the master index for current categories and documents:**

`docs/learned/index.md`

The index contains:

- All category paths and descriptions
- Root-level documents
- Document listings with "Read when..." conditions

## Category Placement Guidelines

1. **Match by topic** - Does the doc clearly fit one category? (see index above for categories)
2. **Match by related docs** - Are similar docs already in a category?
3. **When unclear** - Place at root level; categorize later when patterns emerge
4. **Create new category** - When 3+ related docs exist at root level

### Distinguishing cli/ vs architecture/

This is the most common confusion:

- **cli/**: Patterns for **building CLI commands** - how users interact with the tool
  - Fast-path patterns (skipping expensive ops)
  - Output formatting and styling
  - Script mode behavior
  - Command organization

- **architecture/**: **Internal implementation patterns** - how the code works
  - Gateway ABCs and dependency injection
  - Dry-run via wrapper classes
  - Shell integration constraints
  - Protocol vs ABC decisions

## Document Structure Template

```markdown
---
title: [Clear Document Title]
read_when:
  - "[first condition]"
  - "[second condition]"
---

# [Title Matching Frontmatter]

[1-2 sentence overview]

## [Main Content Sections]

[Organized content with clear headers]

## Related Topics

- [Link to related docs](../category/doc.md) - Brief description
```

## Index File Template

Each category has an `index.md` following this pattern:

```markdown
---
title: [Category] Documentation
read_when:
  - "[when to browse this category]"
---

# [Category] Documentation

[Brief category description]

## Quick Navigation

| When you need to... | Read this        |
| ------------------- | ---------------- |
| [specific task]     | [doc.md](doc.md) |

## Documents in This Category

### [Document Title]

**File:** [doc.md](doc.md)

[1-2 sentence description]

## Related Topics

- [Other Category](../other/) - Brief relevance
```

## Reorganizing Documentation

When moving files between categories:

### Step 1: Move Files with git mv

```bash
cd docs/learned
git mv old-location/doc.md new-category/doc.md
```

### Step 2: Update Cross-References

Find all references to moved files:

```bash
grep -r "old-filename.md" docs/learned/
```

Update relative links:

- Same category: `[doc.md](doc.md)`
- Different category: `[doc.md](../category/doc.md)`
- To category index: `[Category](../category/)`

### Step 3: Update Index Files

Update Quick Navigation tables in affected index files.

### Step 4: Update AGENTS.md

If the doc was in the routing table, update the path.

### Step 5: Validate

Run `make fast-ci` to catch broken links and formatting issues.

## Updating Routing Tables

AGENTS.md contains the Quick Routing Table for agent navigation.

### When to Add Entries

- New category additions
- High-frequency tasks
- Tasks where wrong approach is common

### Entry Format

```markdown
| [Task description] | → [Link or skill] |
```

Examples:

- `| Understand project architecture | → [Architecture](docs/learned/architecture/) |`
- `| Write Python code | → Load \`dignified-python\` skill FIRST |`

## Validation

Run before committing:

```bash
make fast-ci
```

This validates:

- YAML frontmatter syntax
- Required fields present
- Markdown formatting (prettier)

## ⚠️ Generated Files - Do Not Edit Directly

The following files are **auto-generated** from frontmatter metadata:

| File                                   | Source                                |
| -------------------------------------- | ------------------------------------- |
| `docs/learned/index.md`                | Frontmatter from all docs             |
| `docs/learned/<category>/index.md`     | Frontmatter from category             |
| `docs/learned/<category>/tripwires.md` | `tripwires:` field in category docs   |
| `docs/learned/tripwires-index.md`      | Category tripwires with routing hints |

**Never edit these files directly.** Changes will be overwritten.

### Workflow for Changes

1. **Edit the source frontmatter** in the relevant documentation file(s)
2. **Run sync**: `erk docs sync`
3. **Verify changes** in the generated files
4. **Commit both** the source and generated files

### Adding a New Tripwire

To add a tripwire rule:

1. Add to the `tripwires:` field in the relevant doc's frontmatter:
   ```yaml
   tripwires:
     - action: "doing something dangerous"
       warning: "Do this instead."
   ```
2. Run `erk docs sync` to regenerate `tripwires.md`

## Quick Reference

- Full navigation: [docs/learned/guide.md](docs/learned/guide.md)
- Category index: [docs/learned/index.md](docs/learned/index.md)
- Regenerate indexes: `erk docs sync`
- Run validation: `make fast-ci`
