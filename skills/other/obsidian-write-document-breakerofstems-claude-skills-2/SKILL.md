---
name: obsidian-write-document
description: Create or update canonical Obsidian documents with proper formatting and wikilinks. Use when writing new documentation or updating existing vault documents.
---

# Obsidian Write Document Skill

Create or update canonical Obsidian documents with consistent formatting and proper linking.

> **See also**: [Shared Conventions](../shared/CONVENTIONS.md) | [Safety Guidelines](../shared/SAFETY.md)

## Purpose

Write well-structured Obsidian Markdown documents that follow vault conventions, use proper wikilinks, and include source attribution.

## Background Knowledge

### Obsidian Markdown Conventions

Obsidian uses standard Markdown with extensions:

- **Wikilinks**: `[[Page Name]]` or `[[path/to/page|Display Text]]`
- **Embeds**: `![[embedded-note]]` or `![[image.png]]`
- **Tags**: `#tag` or nested `#parent/child`
- **Frontmatter**: YAML block at file start between `---` markers

### Document Quality Standards

Canonical documents must be:

- **Git-safe**: No special characters that cause issues
- **Obsidian-compatible**: Valid wikilinks and formatting
- **Human-reviewable**: Clear structure and language
- **Traceable**: Source notes referenced in footer

### Write Modes

| Mode | Behavior | Use Case |
|------|----------|----------|
| `create` | Create new file, fail if exists | New documents |
| `replace` | Overwrite entire file | Full document updates |
| `append` | Add to end of file | Adding sections to existing docs |

## Input Sources

The skill accepts:

- **Target path**: Destination file path within vault
- **Mode**: `create`, `replace`, or `append`
- **Content**: Document content to write
- **Source files**: List of source notes for attribution
- **Proposal**: Optional proposal from `obsidian-extract-inbox`

## Document Structure

### Required Elements

Every canonical document must include:

```markdown
---
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: draft | review | canonical
tags:
  - relevant-tag
---

# Document Title

Brief one-paragraph summary of document scope.

## Section Heading

Content organized by topic.

## Another Section

More content with [[wikilinks]] to related documents.

---

## Sources

- [[_inbox/source-note-1]]
- [[_inbox/source-note-2]]
```

### Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `created` | Yes | Creation date (YYYY-MM-DD) |
| `updated` | Yes | Last update date (YYYY-MM-DD) |
| `status` | Yes | Document status |
| `tags` | No | Relevant categorization tags |
| `aliases` | No | Alternative names for linking |

### Heading Hierarchy

Use consistent heading levels:

- `#` - Document title (one per document)
- `##` - Major sections
- `###` - Subsections
- `####` - Sub-subsections (use sparingly)

### Source Footer

Every document must end with a Sources section:

```markdown
---

## Sources

- [[_inbox/original-note-1]] - Primary source for Section X
- [[_inbox/original-note-2]] - Additional context for Section Y
```

## Workflow

### 1. Validate Inputs

Before writing, verify:

```bash
# Check if target directory exists
ls -la /path/to/vault/$(dirname target-path)

# For create mode, verify file doesn't exist
test ! -f /path/to/vault/target-path.md && echo "Safe to create"

# For replace/append mode, verify file exists
test -f /path/to/vault/target-path.md && echo "File exists"
```

### 2. Prepare Content

Format content according to standards:

1. Add frontmatter with required fields
2. Ensure single H1 heading (document title)
3. Convert plain links to wikilinks
4. Validate heading hierarchy
5. Add source footer

### 3. Validate Wikilinks

Check that wikilinks reference valid targets:

```bash
# Extract wikilinks from content
grep -oE "\[\[[^\]]+\]\]" content.md

# Verify targets exist (optional, warn if not)
for link in $(grep -oE "\[\[[^\]|]+"); do
  target="${link#[[}"
  test -f "/path/to/vault/${target}.md" || echo "Warning: $target not found"
done
```

### 4. Execute Write

Based on mode:

**Create mode:**
```bash
# Fail if file exists
test -f /path/to/target.md && exit 1
cat > /path/to/target.md << 'EOF'
[content]
EOF
```

**Replace mode:**
```bash
# Backup existing content (in memory, for undo message)
cat /path/to/target.md > /tmp/backup.md
cat > /path/to/target.md << 'EOF'
[content]
EOF
```

**Append mode:**
```bash
cat >> /path/to/target.md << 'EOF'

[content to append]
EOF
```

### 5. Verify Write

After writing, confirm success:

```bash
# Verify file exists and has content
test -s /path/to/target.md && echo "Write successful"

# Show file stats
wc -l /path/to/target.md
```

## Example: Creating a Spec Document

**Input:**

```json
{
  "target_path": "specs/authentication.md",
  "mode": "create",
  "title": "Authentication Specification",
  "sections": [
    {
      "heading": "Overview",
      "content": "This document specifies the authentication system..."
    },
    {
      "heading": "OAuth Integration",
      "content": "The system uses OAuth 2.0 with the following flow..."
    },
    {
      "heading": "Token Management",
      "content": "JWT tokens are used for session management..."
    }
  ],
  "source_files": ["_inbox/auth-notes.md", "_inbox/login-flow.md"]
}
```

**Output document: `specs/authentication.md`**

```markdown
---
created: 2026-01-18
updated: 2026-01-18
status: draft
tags:
  - authentication
  - security
---

# Authentication Specification

This document specifies the authentication system for the application, including OAuth integration and token management.

## Overview

This document specifies the authentication system...

## OAuth Integration

The system uses OAuth 2.0 with the following flow...

See also: [[specs/oauth-providers]] for supported providers.

## Token Management

JWT tokens are used for session management...

Related: [[design/session-handling]] for session lifecycle details.

---

## Sources

- [[_inbox/auth-notes.md]] - Original authentication design notes
- [[_inbox/login-flow.md]] - Login flow documentation
```

## Formatting Rules

### Do

- Use proper heading hierarchy
- Include frontmatter on all documents
- Use `[[wikilinks]]` for internal references
- Add descriptive link text when helpful: `[[path/file|Display Text]]`
- Include source attribution footer
- Use standard Markdown formatting

### Do Not

- Use emojis in document content
- Add "fluff" or filler content
- Use HTML tags (pure Markdown only)
- Create deeply nested headings (max 4 levels)
- Leave broken wikilinks without noting them
- Include timestamps in document body (use frontmatter)

### Link Formatting

```markdown
# Good
See [[authentication]] for details.
Refer to [[specs/api-design|API Design Spec]] for endpoints.

# Bad
See [authentication](authentication.md) for details.
Refer to the API design spec.
```

## Policies

### Always

- Require explicit instruction before writing files
- Validate target path is within vault boundaries
- Include frontmatter with required fields
- Add source attribution footer
- Use create mode for new files, replace/append for existing
- Preserve existing content in append mode

### Never

- Write files without explicit instruction
- Overwrite files in create mode
- Delete source files after writing
- Write outside the designated vault
- Add content not derived from sources
- Use replace mode when append is appropriate

### Mode Selection Guidance

| Scenario | Recommended Mode |
|----------|-----------------|
| New document from scratch | `create` |
| Complete document rewrite | `replace` |
| Adding new section to existing doc | `append` |
| Updating specific section | Use Edit tool, not this skill |

### Error Handling

If write fails:

1. Report the error clearly
2. Do not retry automatically
3. Preserve any backup information
4. Suggest remediation steps

## Integration

This skill works with:

- `obsidian-read-context` - Informs document structure and links
- `obsidian-extract-inbox` - Consumes proposals to create documents
- `obsidian-issue-from-doc` - Documents can become issue sources

## Output Format

When run, report:

1. Action taken (create/replace/append)
2. Target file path
3. File statistics (lines, size)
4. Wikilinks created
5. Warnings (missing link targets, etc.)
6. Next steps recommendation
