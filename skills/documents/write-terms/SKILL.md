---
name: write-terms
description: Term document structure, formatting rules, and guidelines for updating .workaholic/terms/.
allowed-tools: Bash
user-invocable: false
---

# Write Terms

Guidelines for writing and updating terminology documentation in `.workaholic/terms/`.

## Gather Context

Run the bundled script to collect information about what changed:

```bash
bash .claude/skills/write-terms/sh/gather.sh [base-branch]
```

Default base branch is `main`.

### Output Sections

The script outputs structured information:

```
=== BRANCH ===
<current branch name>

=== TICKETS ===
<list of archived tickets for this branch, or "No archived tickets">

=== TERMS ===
<list of existing term files>

=== DIFF ===
<git diff stat against base branch>

=== COMMIT ===
<current short commit hash>
```

### Using the Output

- **BRANCH**: Use to locate archived tickets
- **TICKETS**: Read these to understand what changed and what new terms may exist
- **TERMS**: Survey these to find documents needing updates
- **DIFF**: Use when no tickets exist to understand changes
- **COMMIT**: Use in frontmatter `commit_hash` field

## Term Categories

| File                  | Terms                                    |
| --------------------- | ---------------------------------------- |
| `core-concepts.md`    | plugin, command, skill, rule, agent      |
| `artifacts.md`        | ticket, spec, story, changelog           |
| `workflow-terms.md`   | drive, archive, sync, release            |
| `file-conventions.md` | kebab-case, frontmatter, icebox, archive |
| `inconsistencies.md`  | Known terminology issues                 |

## Term Entry Format

```markdown
## term-name

Brief one-sentence definition.

### Definition

Full explanation of what this term means in the Workaholic context.

### Usage Patterns

- **Directory names**: examples
- **File names**: examples
- **Code references**: examples

### Related Terms

- Related term 1, related term 2

### Inconsistencies (if any)

- Description of inconsistency and potential resolution
```

## Frontmatter

Required for every terms file:

```yaml
---
title: Document Title
description: Brief description of this document
category: developer
last_updated: YYYY-MM-DD
commit_hash: <short-hash>
---
```

Use the commit hash from the COMMIT section of the context output.

## Index File Updates

**When adding a term:**

- Add to the appropriate category file
- If it's a major new concept, consider adding to README

**When deprecating a term:**

- Mark as deprecated in the definition
- Note what replaced it
- Keep for historical reference

**i18n mirroring:**

When terminology files have translations (e.g., `artifacts.md` and `artifacts_ja.md`):

- Any term added to one file must have its translation in the other
- Follow the preloaded `translate` skill for translation requirements

## Critical Rules

- **Consistency over precision** - A term should mean the same thing everywhere
- **Every ticket may introduce terms** - Even small changes may use new terminology
- **Only delete within `.workaholic/`** - Safety constraint for file deletions
- **Update `last_updated`** - Set to current date when modifying any doc
- **Update `commit_hash`** - Use value from context COMMIT section
- **Keep translations in sync** - If `_ja.md` exists, update both files
