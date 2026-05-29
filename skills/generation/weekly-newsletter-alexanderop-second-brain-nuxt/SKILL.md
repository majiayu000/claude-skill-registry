---
name: weekly-newsletter
description: Generate a weekly newsletter summarizing resources added last week. Use when asked to "weekly newsletter", "newsletter", "what did I add this week", "generate newsletter", or "Monday newsletter".
allowed-tools: Read, Write, Glob, Grep, Bash, AskUserQuestion
---

# Weekly Newsletter

Generate a newsletter summarizing public notes added during the previous week (Mon-Sun), grouped by content type. Designed for Monday publishing.

## Output

- **Format:** Markdown file saved to `content/newsletter-drafts/`
- **Content:** Public notes only (excludes private/draft content)
- **Organization:** Grouped by content type (books, articles, podcasts, etc.)
- **Purpose:** Ready to copy/paste for external publishing

---

## Phase 1: Run Collection Script

Run the CLI script to collect all notes added this week:

```bash
node .claude/skills/weekly-newsletter/scripts/collect-weekly-notes.mjs
```

The script outputs JSON with:
- `week` - ISO week (e.g., "2026-W05")
- `weekStart` - Monday date
- `weekEnd` - Sunday date
- `notes` - Array of notes with slug, title, type, summary, url, tags
- `tweets` - Array of tweets (if any)

For a specific week:
```bash
node .claude/skills/weekly-newsletter/scripts/collect-weekly-notes.mjs --week 2026-W04
```

---

## Phase 2: Group by Content Type

Organize notes from the JSON output into sections based on their `type` field:

| Type | Section Header |
|------|----------------|
| book | Books |
| article | Articles |
| podcast | Podcasts |
| youtube | Videos |
| talk | Talks |
| github | GitHub Repos |
| reddit | Reddit Threads |
| tweet | Tweets |
| newsletter | Newsletter Issues |
| course | Courses |
| movie | Movies |
| tv | TV Shows |
| manga | Manga |
| note | Notes |
| evergreen | Evergreens |
| quote | Quotes |

Only include sections that have content.

---

## Phase 3: Generate Newsletter Content

### 3.1 Newsletter Template

```markdown
---
title: "Weekly Digest: {Week Start} - {Week End}"
date: {Today YYYY-MM-DD}
week: {YYYY-Www}
---

# Weekly Digest

*Resources added {Week Start} - {Week End}*

## Summary

This week I added **{total count}** resources to my knowledge base:
{type counts, e.g., "3 articles, 2 podcasts, 1 book"}

---

## {Section Header}

### [[{note-slug}|{title}]]

{summary or "[No summary]" if missing}

**Tags:** {tags as comma-separated list}
**Source:** {url if present}

---

{repeat for each note in section}

{repeat for each section with content}

---

## Stats

- Total resources: {count}
- Most active type: {type with most entries}
- Top tags: {3 most frequent tags}
```

### 3.2 Writing Guidelines

- Keep summaries concise (1-2 sentences max)
- Use wiki-links: `[[slug|title]]` format for internal references
- Include source URL for external sharing

---

## Phase 4: Review with User

Present the generated newsletter:

```yaml
question: "Does this newsletter look ready?"
header: "Review"
options:
  - label: "Save"
    description: "Save to newsletter-drafts folder"
  - label: "Edit"
    description: "Make changes before saving"
  - label: "Regenerate"
    description: "Try generating again with different options"
```

---

## Phase 5: Save Newsletter

### 5.1 Ensure Directory Exists

```bash
mkdir -p content/newsletter-drafts
```

### 5.2 Save File

Filename: `{YYYY-Www}.md` (ISO week number from JSON output)
Path: `content/newsletter-drafts/{YYYY-Www}.md`

### 5.3 Confirmation

Display:
- File path saved
- Total notes included
- Sections generated

---

## Edge Cases

| Situation | Handling |
|-----------|----------|
| No notes added this week | Inform user, offer to check previous week |
| Week already has newsletter | Offer to overwrite or append |
| Note missing summary | Use "[No summary]" |
| Mixed public/private notes | Script excludes private by default |

---

## Quality Checklist

Before saving:
- [ ] Filename matches `YYYY-Www.md` format
- [ ] Summaries are concise (1-2 sentences)
- [ ] Wiki-links use `[[slug|title]]` format
- [ ] Source URLs included for external sharing
- [ ] Stats section reflects actual counts
