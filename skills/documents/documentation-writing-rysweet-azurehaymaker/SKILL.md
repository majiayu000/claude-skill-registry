---
name: documentation-writing
version: 1.0.0
description: Writing clear, discoverable software documentation following the Eight Rules and Diataxis framework. Use when creating README files, API docs, tutorials, how-to guides, or any project documentation. Automatically enforces docs/ location, linking requirements, and runnable examples.
source_urls:
  - https://diataxis.fr/
  - https://www.writethedocs.org/guide/writing/docs-principles/
  - https://github.blog/developer-skills/documentation-done-right-a-developers-guide/
auto_activates:
  - "write documentation"
  - "create docs"
  - "document this feature"
  - "create a README"
  - "write a tutorial"
  - "api docs"
  - "how-to guide"
token_budget: 1800
---

# Documentation Writing Skill

## Purpose

Creates high-quality, discoverable documentation following the Eight Rules and Diataxis framework. Ensures all docs are properly located, linked, and contain real runnable examples.

## When I Activate

I load automatically when you mention:

- "write documentation" or "create docs"
- "document this feature/module/API"
- "create a README" or "write a tutorial"
- "explain how this works"
- Any request to create markdown documentation

## Core Rules (MANDATORY)

### The Eight Rules

1. **Location**: All docs in `docs/` directory
2. **Linking**: Every doc linked from at least one other doc
3. **Simplicity**: Plain language, remove unnecessary words
4. **Real Examples**: Runnable code, not "foo/bar" placeholders
5. **Diataxis**: One doc type per file (tutorial/howto/reference/explanation)
6. **Scanability**: Descriptive headings, table of contents for long docs
7. **Local Links**: Relative paths, context with links
8. **Currency**: Delete outdated docs, include update metadata

### What Stays OUT of Docs

**Never put in `docs/`:**

- Status reports or progress updates
- Test results or benchmarks
- Meeting notes or decisions
- Plans with dates
- Point-in-time snapshots

**Where temporal info belongs:**

- Test results → CI logs, GitHub Actions
- Status updates → GitHub Issues
- Progress → Pull Request descriptions
- Decisions → Commit messages

## Quick Start

### Creating a New Document

```markdown
# [Feature Name]

Brief one-sentence description of what this is.

## Quick Start

Minimal steps to get started (3-5 steps max).

## Contents

- [Configuration](#configuration)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)

## Configuration

Step-by-step setup with real examples.

## Usage

Common use cases with runnable code.

## Troubleshooting

Common problems and solutions.
```

### Document Types (Diataxis)

| Type        | Purpose       | Location          | User Question           |
| ----------- | ------------- | ----------------- | ----------------------- |
| Tutorial    | Learning      | `docs/tutorials/` | "Teach me how"          |
| How-To      | Doing         | `docs/howto/`     | "Help me do X"          |
| Reference   | Information   | `docs/reference/` | "What are the options?" |
| Explanation | Understanding | `docs/concepts/`  | "Why is it this way?"   |

## Workflow

### Step 1: Determine Document Type

Ask: What is the reader trying to accomplish?

- Learning something new → Tutorial
- Solving a specific problem → How-To
- Looking up details → Reference
- Understanding concepts → Explanation

### Step 2: Choose Location

```
docs/
├── tutorials/     # Learning-oriented
├── howto/         # Task-oriented
├── reference/     # Information-oriented
├── concepts/      # Understanding-oriented
└── index.md       # Links to all docs
```

### Step 3: Write with Examples

Every concept needs a runnable example:

```python
# Example: Analyze file complexity
from amplihack import analyze

result = analyze("src/main.py")
print(f"Complexity: {result.score}")
# Output: Complexity: 12.5
```

### Step 4: Link from Index

Add entry to `docs/index.md`:

```markdown
- [New Feature Guide](./howto/new-feature.md) - How to configure X
```

### Step 5: Validate

Checklist before completion:

- [ ] File in `docs/` directory
- [ ] Linked from index or parent doc
- [ ] No temporal information
- [ ] All examples tested
- [ ] Follows one Diataxis type

## Navigation Guide

### When to Read Supporting Files

**reference.md** - Read when you need:

- Complete frontmatter specification
- Detailed Diataxis type definitions
- Markdown style conventions
- Documentation review checklist

**examples.md** - Read when you need:

- Full document templates for each type
- Real-world documentation examples
- Before/after improvement examples
- Complex documentation patterns

## Anti-Patterns to Avoid

| Anti-Pattern       | Why It's Bad  | Better Approach                |
| ------------------ | ------------- | ------------------------------ |
| "Click here" links | No context    | "See [auth config](./auth.md)" |
| foo/bar examples   | Not realistic | Use real project code          |
| Wall of text       | Hard to scan  | Use headings and bullets       |
| Orphan docs        | Never found   | Link from index                |
| Status in docs     | Gets stale    | Use Issues/PRs                 |

## Retcon Documentation Exception

When writing documentation BEFORE implementation (document-driven development):

````markdown
# [PLANNED - Implementation Pending]

This document describes the intended behavior of Feature X.

## Planned Interface

```python
# [PLANNED] - This API will be implemented
def future_function(input: str) -> Result:
    """Process input and return result."""
    pass
```
````

Once implemented, remove the `[PLANNED]` markers and update with real examples.

```

---

**Full reference**: See [reference.md](./reference.md) for complete specification.
**Templates**: See [examples.md](./examples.md) for copy-paste templates.
```
