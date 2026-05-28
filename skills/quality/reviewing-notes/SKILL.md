---
name: reviewing-notes
description: Audit notes for quality issues. Use when asked to "review notes", "check content quality", "audit my knowledge base", or "find broken links".
allowed-tools: Read, Glob, Grep
---

# Reviewing Notes for Quality

This skill audits the knowledge base for quality issues and produces an actionable report.

## Workflow

### 1. Scan All Content

```bash
# List all content files
ls content/*.md
```

### 2. Check Each Note For Issues

**Read each file and check for:**

#### Missing or Weak Summaries
- No `summary:` field in frontmatter
- Summary is empty or very short (<10 words)
- Summary doesn't capture the core idea

#### Broken Wiki-Links
Parse all `[[slug]]` patterns and verify each target exists:
```bash
# Extract wiki-links from a file
grep -o '\[\[[^]]*\]\]' content/note-name.md

# Check if target file exists
ls content/target-slug.md
```

#### Insufficient Tags
- Notes with fewer than 2 tags
- Notes with no tags at all

#### Orphan Notes
- No outgoing wiki-links (doesn't reference other notes)
- No incoming wiki-links (not referenced by other notes)
- Both = fully isolated

#### Short Content
- Body content under 100 words (may indicate incomplete note)

#### Missing Required Frontmatter
- No `title` field
- No `type` field
- Missing `date` field

### 3. Generate Report

Organize findings by severity:

```markdown
## Quality Audit Report

### Critical Issues
- **Broken Links**
  - `note-a.md`: links to [[non-existent]] (file not found)

### High Priority
- **Missing Summaries**
  - `note-b.md`: no summary field
  - `note-c.md`: summary is empty

- **Orphan Notes** (no connections)
  - `isolated-note.md`: 0 incoming, 0 outgoing links

### Medium Priority
- **Insufficient Tags** (<2 tags)
  - `note-d.md`: only 1 tag

- **Short Content** (<100 words)
  - `stub-note.md`: 45 words

### Low Priority
- **Missing Optional Fields**
  - `note-e.md`: no date field
```

## Issue Categories

| Issue | Severity | Impact |
|-------|----------|--------|
| Broken wiki-link | Critical | Navigation fails |
| Missing summary | High | Poor discoverability |
| Orphan note | High | Lost in graph |
| <2 tags | Medium | Harder to find |
| Short content | Medium | May be incomplete |
| Missing date | Low | Timeline unclear |

## Quality Checklist

When reviewing:
- [ ] Checked all content files
- [ ] Verified each wiki-link target exists
- [ ] Counted tags per note
- [ ] Identified orphan notes
- [ ] Measured content length
- [ ] Prioritized issues by severity
