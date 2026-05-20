---
name: weekly-review
description: Summarize the past week's daily journal entries. Use when asked to "weekly review", "review the week", "summarize this week", or "week summary".
allowed-tools: Read, Write, Edit, Glob, Grep, AskUserQuestion
---

# Weekly Review

Summarize the past week's daily entries into a weekly review note.

## Location

All private notes live in `content/private/` with flat structure (no subfolders).

## Date Format

- Weekly reviews: `YYYY-Www.md` (ISO week number)
- Example: `2024-W02.md` for week 2 of 2024

---

## Phase 1: Determine Week Boundaries

Calculate the current ISO week:
- Week starts Monday, ends Sunday
- Use ISO 8601 week numbering

Find date range for the week being reviewed (default: current week).

---

## Phase 2: Gather Daily Notes

### 2.1 Find Daily Notes

Search for all daily notes in the week's date range:

```text
Glob: content/private/YYYY-MM-DD.md
```

Filter to notes where date falls within the week.

### 2.2 Load Content

Read each daily note found and extract:
- Morning Thoughts
- Done Today items
- Learnings
- Links Captured

### 2.3 Present Summary

Display to user:
- Number of daily entries found (e.g., "Found 5 of 7 days")
- Key themes identified
- Most linked public notes

---

## Phase 3: Generate Weekly Summary

### 3.1 Ask for User Input

```yaml
question: "What were the main themes this week?"
header: "Themes"
options:
  - label: "Auto-generate"
    description: "Identify themes from daily entries"
  - label: "Manual"
    description: "I'll describe the themes"
```

If user chooses manual, gather their input.

### 3.2 Create Weekly Note

**Frontmatter:**
```yaml
---
title: "Week {N}, {YYYY}"
type: weekly
week: YYYY-Www
date: {week end date YYYY-MM-DD}
dailies:
  - "[[YYYY-MM-DD]]"
  - "[[YYYY-MM-DD]]"
private: true
---
```

**Body structure:**
```markdown
## Week Summary

{user themes or auto-generated summary}

## Key Events

- {aggregated from Done Today sections}

## Learnings

- {consolidated from daily Learnings sections}

## Public Notes Created

- [[note-1]] - {brief context}
- [[note-2]] - {brief context}
```

### 3.3 Review with User

Present the generated weekly review:

```yaml
question: "Does this weekly summary look good?"
header: "Review"
options:
  - label: "Save"
    description: "Create the weekly review file"
  - label: "Edit"
    description: "Make changes before saving"
```

---

## Phase 4: Save Weekly Review

Save to `content/private/{YYYY-Www}.md`.

Confirm with:
- File path
- Number of days covered
- Key themes captured

---

## Template Reference

Full weekly review template:

```markdown
---
title: "Week N, YYYY"
type: weekly
week: YYYY-Www
date: YYYY-MM-DD
dailies:
  - "[[2024-01-08]]"
  - "[[2024-01-09]]"
  - "[[2024-01-10]]"
  - "[[2024-01-11]]"
  - "[[2024-01-12]]"
private: true
---

## Week Summary

High-level themes and patterns from the week.

## Key Events

- Monday: ...
- Tuesday: ...
- Notable accomplishment

## Learnings

- Insight 1 from [[2024-01-08]]
- Insight 2 from [[2024-01-10]]

## Public Notes Created

- [[book-title]] - Finished reading and captured notes
- [[podcast-episode]] - Great episode on X topic
```

---

## Quality Checklist

Before saving:
- [ ] Filename matches `YYYY-Www.md` format (w lowercase)
- [ ] Frontmatter has `type: weekly` and `private: true`
- [ ] Week number in title and frontmatter match
- [ ] `dailies` array lists all daily notes included
- [ ] Summary synthesizes themes, not just lists
- [ ] Wiki-links use correct `[[slug]]` format

---

## Edge Cases

| Situation | Handling |
|-----------|----------|
| No daily notes found | Warn user, offer to create anyway |
| Partial week (< 7 days) | Proceed with available entries |
| Weekly review already exists | Offer to update or skip |
| User wants different week | Allow specifying week number |
