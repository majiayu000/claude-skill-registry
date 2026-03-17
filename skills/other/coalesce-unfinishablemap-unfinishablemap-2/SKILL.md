---
name: coalesce
description: Combine multiple related articles into one unified piece. Archives originals to preserve URLs.
---

# Coalesce Articles

Merge multiple related articles into a single unified piece, archiving the originals to preserve their URLs for external links.

## When to Use

- When explicitly invoked: `/coalesce`
- When multiple articles have significant overlap
- When a topic has fragmented into too many small pieces
- After identifying redundancy during review

## Arguments

Provide as space-separated arguments or answer when prompted:
1. **Source articles** (comma-separated paths): `obsidian/concepts/article-1.md,obsidian/concepts/article-2.md`
2. **Target location**: `obsidian/topics/new-unified-article.md`

Example: `/coalesce obsidian/concepts/a.md,obsidian/concepts/b.md obsidian/topics/combined.md`

## Instructions

### 1. Validate Inputs

Verify all source files exist and target location is valid:
- Source files must exist in obsidian/
- Target must be in a valid sync directory (topics/, concepts/, voids/, etc.)
- Target should not already exist (or ask for confirmation to merge into existing)

If arguments are not provided, search for articles that exhibit overlap and duplication, or are strong candidates for merging.  Choose the most promisng two or more for candidates merging,  If there are no good candidates, abandon the attempt and do not merge anything.

### 2. Analyze Source Content

Read all source articles and identify:
- Common themes and overlapping content
- Unique contributions from each source
- Conflicting claims or framings
- Cross-references between sources

Also search for external references to these articles:
```
grep -r "[[source-slug" obsidian/
```

If you selected aricles automaticall but find that the articles ar well-differntiated and should not be merged, search again.  If after five iterations there are still no strong candiates, abaon the attempt and do not merge anything.

### 3. Plan the Merge

Create a mental outline:
- What is the unified article's core claim?
- How do the sources' unique contributions organize into sections?
- Which redundant content to eliminate?
- How to reconcile any conflicts?

### 4. Generate Unified Article

Create the new article at the target location.

**Frontmatter:**
```yaml
---
title: "[Unified Title]"
created: [earliest source created date]
modified: [today's date]
human_modified: [latest human_modified from sources, or null]
ai_modified: [current timestamp]
draft: false
topics: [merge from sources, deduplicate]
concepts: [merge from sources, deduplicate]
related_articles: [merge from sources, remove self-references, deduplicate]
ai_contribution: [calculate: if all sources were AI, use 100; if mixed, estimate]
author: [preserve if any human-authored sources]
ai_system: [current model]
ai_generated_date: [today]
last_curated: null
coalesced_from:
  - "/[section]/[source-1-slug]/"
  - "/[section]/[source-2-slug]/"
---
```

**Content guidelines:**
- Follow writing-style.md
- Front-load the key claim
- Self-contained article
- Include "Relation to Site Perspective" section
- Include "Further Reading" section
- Preserve valuable unique insights from each source
- Eliminate redundancy

### 5. Archive Source Articles

For each source article:

1. **Calculate archive path**: `archive/[original-section]/[slug].md`
   - Example: `obsidian/concepts/old-article.md` → `archive/concepts/old-article.md`

2. **Move file** to archive directory (preserving content)

3. **Update frontmatter** with archive metadata:
```yaml
archived: true
archived_date: [current ISO timestamp]
superseded_by: "/[target-section]/[target-slug]/"
archive_reason: "Coalesced into [new article title]"
original_path: "/[original-section]/[original-slug]/"
```

The original content remains intact below the frontmatter. The archive notice will be displayed by Hugo templates.

### 6. Check for References

Search for wikilinks to the archived articles in active content:
```
grep -r "\[\[source-slug" obsidian/
```

For each reference found:
- Note the file and context
- These may need updating to point to the new unified article
- Create a follow-up task if references found

### 7. Update Todo

If this was a todo item, mark it complete.

If references were found to archived articles, create a follow-up task:
```markdown
### P2: Update references to coalesced articles
- **Type**: other
- **Notes**: Coalesce created [new-article]. The following files reference archived articles and may need review: [list files]
- **Source**: coalesce
- **Generated**: [today]
```

### 8. Log to Changelog

Prepend to `obsidian/workflow/changelog.md` (add immediately after frontmatter, before existing entries):

```markdown
## [current time from prompt] - coalesce
- **Status**: Success
- **Sources**: [list of source files as wikilinks]
- **Target**: [[new article path without .md extension]]
- **Archived**: [list of archive paths as wikilinks]
- **References to review**: [count or "none"]
```

### 9. Commit Changes

Create a git commit:
```
feat(content): coalesce [N] articles into [new-article-slug]

Merged:
- [source-1] → archive/[section]/[slug].md
- [source-2] → archive/[section]/[slug].md

New article: [target-path]
```

## Important

- ALWAYS preserve source content in archive (never delete)
- ALWAYS update frontmatter with archival metadata
- The original URLs will continue to work via the archive
- Check for external references before archiving
