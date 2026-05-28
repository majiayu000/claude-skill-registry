---
name: write-spec
description: Spec document structure, formatting rules, and guidelines for updating .workaholic/specs/.
allowed-tools: Bash
user-invocable: false
---

# Write Spec

Guidelines for writing and updating specification documents in `.workaholic/specs/`.

## Gather Context

Run the bundled script to collect information about what changed:

```bash
bash .claude/skills/write-spec/sh/gather.sh [base-branch]
```

Default base branch is `main`.

### Output Sections

The script outputs structured information:

```
=== BRANCH ===
<current branch name>

=== TICKETS ===
<list of archived tickets for this branch, or "No archived tickets">

=== SPECS ===
<list of existing spec files>

=== DIFF ===
<git diff stat against base branch>

=== COMMIT ===
<current short commit hash>
```

### Using the Output

- **BRANCH**: Use to locate archived tickets
- **TICKETS**: Read these to understand what changed and why
- **SPECS**: Survey these to find documents needing updates
- **DIFF**: Use when no tickets exist to understand changes
- **COMMIT**: Use in frontmatter `commit_hash` field

## Directory Structure

| Audience   | Directory            | Content                                  |
| ---------- | -------------------- | ---------------------------------------- |
| Users      | `.workaholic/guides/` | How to use: commands, workflows, setup   |
| Developers | `.workaholic/specs/`  | How it works: architecture, contributing |

## Frontmatter

Required for every spec file:

```yaml
---
title: Document Title
description: Brief description of this document
category: user | developer
modified_at: <ISO 8601 datetime>
commit_hash: <from context COMMIT section>
---
```

## File Naming

- Use kebab-case: `getting-started.md`, `command-reference.md`
- Exception: `README.md` uses uppercase

## Content Style

- Write full paragraphs, not bullet-point fragments
- Code blocks must specify language
- Links use relative paths within `.workaholic/`
- Use Mermaid charts for diagrams

## Design Policy

- Rewrite to reflect present reality, not append changes
- Think "what does a new reader need to know today?"

## Cross-Cutting Concerns

Before updating individual docs, analyze changes for patterns that span multiple components:

- **Data flow paths**: How data moves through layers
- **Shared concepts**: Abstractions used across multiple files
- **Integration points**: Where different subsystems connect
- **Architectural patterns**: Design decisions that affect multiple areas

For each cross-cutting concern:

- Check if `.workaholic/specs/` already has a document covering this concept
- Prefer extending existing docs over creating new files for minor patterns

**Writing cross-cutting documentation:**

- Prefer prose over file listings - explain how components work together
- Use Mermaid sequence diagrams to show interactions between layers
- Document the "why" behind design decisions, not just implementation details

## Index File Updates

**When adding a document:**

- Add link to parent README
- Include brief description

**When removing a document:**

- Remove link from parent README
- Verify no other docs link to it

**i18n README mirroring:**

- Any document added to one README must have its translation linked in the other
- Follow the preloaded `translate` skill for translation requirements

## Critical Rules

- **"No updates needed" is almost always wrong** - Re-analyze if you think nothing changed
- **Every ticket affects docs somehow** - Even small changes have documentation implications
- **Only delete within `.workaholic/`** - Safety constraint for file deletions
- **No orphan documents** - Every doc must be linked from a parent README
- **Category matches directory** - A doc with `category: user` must be in `guides/`, `category: developer` in `specs/`
- **Update `modified_at`** - Set to current datetime (use `date -Iseconds`) when modifying any doc
- **Update `commit_hash`** - Use value from context COMMIT section
