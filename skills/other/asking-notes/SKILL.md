---
name: asking-notes
description: Query your Second Brain with keyword search. Use when asked to "ask my notes", "what do I know about", "query my knowledge", "/ask", or when the user has a question that their notes might answer.
allowed-tools: Read, Bash, Glob, Grep
---

# Ask Your Second Brain

This skill answers questions by searching your notes with keyword matching, reading the most relevant ones, and synthesizing an answer — all locally, no external API calls.

## Workflow

### 1. Search — Find Relevant Notes

Use Grep and Glob to find notes matching the user's question:

```bash
# Search by keywords in content
Grep pattern="keyword" path="content/" glob="*.md"

# Search by tags
Grep pattern="tags:.*keyword" path="content/" glob="*.md"

# Search by title
Grep pattern="title:.*keyword" path="content/" glob="*.md"
```

Combine multiple keyword searches to find the most relevant notes.

### 2. Read — Understand the Content

Read the **top 5** note files returned by the search (full markdown content). If the top 5 don't fully answer the question, read more from the results list.

### 3. Synthesize — Answer the Question

Combine insights across the notes into a direct answer. Follow these rules strictly:

- **Never invent information** not present in the notes
- **Always cite** which note each claim comes from using `[[wiki-links]]`
- **If no notes are relevant**, say so honestly — don't guess
- **Connect ideas** across notes when they complement each other
- **Note contradictions** if different notes disagree

### 4. Extend — Identify Gaps and Follow-ups

After answering, highlight what's missing from the knowledge base and suggest related questions.

## Output Format

```markdown
## Answer

[Direct answer synthesized from notes, citing [[sources]] inline]

## Sources Used

| Note | Type | Relevance |
|------|------|-----------|
| [[slug-1]] | article | Core source on topic |
| [[slug-2]] | book | Supporting framework |
| [[slug-3]] | podcast | Practical examples |

## Gaps & Follow-ups

- No notes covering [subtopic X]
- Try asking: "What about [related question]?"
```

## Quality Checklist

- [ ] Searched with multiple relevant keywords
- [ ] Read the top matching notes thoroughly
- [ ] Every claim is attributed to a specific note via `[[wiki-link]]`
- [ ] No information was invented or assumed
- [ ] Contradictions between notes are flagged
- [ ] Gaps in coverage are identified
- [ ] Follow-up questions are suggested
