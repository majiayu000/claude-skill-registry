---
name: archive-ticket
description: Complete commit workflow - format, archive, update changelog, and commit in one operation.
allowed-tools: Bash
user-invocable: false
---

# Archive Ticket

Complete commit workflow after user approves implementation.

## When to Use

Use this skill after user approves implementation. The script handles formatting, archiving, changelog, and commit.

**IMPORTANT**: Always use the script. Never manually move tickets or create changelogs.

**Note**: Archiving requires being on a named branch (not detached HEAD). The script will exit with an error if not on a branch.

## Instructions

Run the bundled script with ticket path, commit message, repo URL, and optional description:

```bash
bash .claude/skills/archive-ticket/sh/archive.sh <ticket-path> <commit-message> <repo-url> [description] [files...]
```

Example:

```bash
bash .claude/skills/archive-ticket/sh/archive.sh \
  .workaholic/tickets/todo/20260115-feature.md \
  "Add new feature" \
  https://github.com/org/repo \
  "Enables users to authenticate with session-based login, addressing the need for secure access control." \
  src/foo.ts src/bar.ts
```

## Commit Message Rules

- **NO prefixes** - Do not use `[feat]`, `[fix]`, `feat:`, `fix:`, etc.
- Start with a present-tense verb (Add, Update, Fix, Remove, Refactor)
- Keep the title concise (50 characters or less)
- Focus on **WHAT** changed in the title

### Examples

```
Add JSDoc comments to gateway exports
Update traceparent format with W3C spec
Fix session decryption to handle invalid tokens
Remove unused RegisterTool type after consolidation
```

## Description Rules

The optional description parameter captures the **WHY** behind the change:

- 1-2 sentences explaining the motivation or problem being solved
- Extract from the ticket's Overview section
- Appears as a second line in CHANGELOG entries
- Used by `/report` to generate comprehensive PR descriptions

### Example

```
"Enables users to authenticate with session-based login, addressing the need for secure access control."
```

## File Locations

The script manages two separate locations:

- **Tickets** are archived to `.workaholic/tickets/archive/<branch>/`
- **Changelogs** are written to `.workaholic/changelogs/<branch>.md`

This separation keeps change requests (tickets) distinct from change summaries (changelogs).

## CHANGELOG Format

Entries are automatically categorized based on commit verb and include optional descriptions:

### Categorization

- **Added**: Add, Create, Implement, Introduce
- **Changed**: Update, Fix, Refactor (default)
- **Removed**: Remove, Delete

### Entry Format

```markdown
- Commit title ([hash](url)) - [ticket](file.md)
  Description explaining why this change was made.
```

The description line is optional but recommended for generating comprehensive PR summaries.
