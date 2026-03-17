---
name: monthly-review
description: Aggregate weekly summaries into a monthly overview. Use when asked to "monthly review", "review the month", "summarize this month", or "month summary".
allowed-tools: Read, Write, Edit, Glob, Grep, AskUserQuestion
---

# Monthly Review

Aggregate weekly summaries into a comprehensive monthly overview.

## Location

All private notes live in `content/private/` with flat structure (no subfolders).

## Date Format

- Monthly reviews: `YYYY-MM.md`
- Example: `2024-01.md` for January 2024

---

## Phase 1: Determine Month Boundaries

Identify the month being reviewed (default: previous month if early in month, current month otherwise).

Calculate:
- Month start and end dates
- ISO week numbers that fall within the month

---

## Phase 2: Gather Weekly Reviews

### 2.1 Find Weekly Reviews

Search for weekly reviews from the target month:

```text
Glob: content/private/YYYY-W*.md
```

Filter to weeks where `week` frontmatter falls within the month.

### 2.2 Load Content

Read each weekly review and extract:
- Week summaries
- Key events
- Learnings
- Public notes created

### 2.3 Present Summary

Display to user:
- Number of weekly reviews found
- Weeks covered (e.g., "W01-W04")
- Major themes identified

---

## Phase 3: Generate Monthly Summary

### 3.1 Ask for User Input

```yaml
question: "What were the big themes this month?"
header: "Themes"
options:
  - label: "Auto-generate"
    description: "Synthesize themes from weekly reviews"
  - label: "Manual"
    description: "I'll describe the month's themes"
```

If user chooses manual, gather their input.

### 3.2 Ask About Achievements

```yaml
question: "Any notable achievements to highlight?"
header: "Wins"
options:
  - label: "Yes"
    description: "I have achievements to add"
  - label: "Extract from weeklies"
    description: "Pull from key events"
```

### 3.3 Create Monthly Note

**Frontmatter:**
```yaml
---
title: "{Month Name} {YYYY}"
type: monthly
month: YYYY-MM
date: {first of next month YYYY-MM-DD}
weeks:
  - "[[YYYY-W01]]"
  - "[[YYYY-W02]]"
  - "[[YYYY-W03]]"
  - "[[YYYY-W04]]"
private: true
---
```

**Body structure:**
```markdown
## Month Summary

{user themes or auto-generated summary}

## Themes

- Theme 1: {description}
- Theme 2: {description}

## Achievements

- Achievement 1
- Achievement 2

## Top Public Notes

- [[most-linked-note]] - {why it was significant}
- [[another-note]] - {context}
```

### 3.4 Review with User

Present the generated monthly review:

```yaml
question: "Does this monthly summary look good?"
header: "Review"
options:
  - label: "Save"
    description: "Create the monthly review file"
  - label: "Edit"
    description: "Make changes before saving"
```

---

## Phase 4: Save Monthly Review

Save to `content/private/{YYYY-MM}.md`.

Confirm with:
- File path
- Weeks covered
- Key themes and achievements

---

## Template Reference

Full monthly review template:

```markdown
---
title: "January 2024"
type: monthly
month: 2024-01
date: 2024-02-01
weeks:
  - "[[2024-W01]]"
  - "[[2024-W02]]"
  - "[[2024-W03]]"
  - "[[2024-W04]]"
private: true
---

## Month Summary

Overview of the month's patterns, progress, and observations.

## Themes

- **Work:** Major project focus or accomplishments
- **Learning:** Key topics studied or explored
- **Personal:** Life events or milestones

## Achievements

- Completed X project
- Published Y blog posts
- Read Z books

## Top Public Notes

- [[book-title]] - Major influence on thinking this month
- [[article-slug]] - Referenced multiple times in weeklies
```

---

## Quality Checklist

Before saving:
- [ ] Filename matches `YYYY-MM.md` format
- [ ] Frontmatter has `type: monthly` and `private: true`
- [ ] Month in title and frontmatter match
- [ ] `weeks` array lists all weekly reviews included
- [ ] Themes synthesize patterns (not just aggregated lists)
- [ ] Achievements are concrete and specific
- [ ] Wiki-links use correct `[[slug]]` format

---

## Edge Cases

| Situation | Handling |
|-----------|----------|
| No weekly reviews found | Offer to scan dailies directly |
| Partial month (< 4 weeks) | Proceed with available entries |
| Monthly review already exists | Offer to update or skip |
| User wants different month | Allow specifying month |
| Week spans two months | Include if majority in target month |
