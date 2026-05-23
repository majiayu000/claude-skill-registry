---
name: extract-insights
description: This skill should be used when user wants to learn from their collected references, synthesize patterns across sources, or turn research into frameworks from curated reference collections (Are.na channels, bookmarks, saved articles).
---

# Extract Insights from Reference Collections

## When This Activates

- "Extract insights from my Are.na"
- "Synthesize these articles"
- "Turn my bookmarks into something useful"
- "What patterns are in my saved references?"

## The Process

### Phase 1: Audit

Understand the collection contents.

```
AUDIT CHECKLIST:
- Total items: [count]
- By type: [links, images, text, attachments]
- Link domains: [group by source - medium.com, specific blogs, etc.]
- Blocked sources: [paywalled, bot-detected]
- High-value targets: [articles > images > text snippets]
```

**For Are.na:** Run `npx tsx scripts/audit-channel.ts <slug>` if available, or fetch via API.

**Priority order for insight extraction:**
1. Articles/links (richest content)
2. Text blocks (direct notes)
3. Images with descriptions (frameworks, diagrams)
4. Images without descriptions (least context)

### Phase 2: Deep-Read

**For articles/links:**

```
FETCH STRATEGY:
1. Direct fetch (WebFetch)
2. If blocked or inaccessible:
   - Flag for manual review
   - Note: "[url] - blocked, needs manual access"
3. If success:
   - Extract key insights (not full content)
   - Note source for citation
```

**For PDFs and attachments:**

```
PDF STRATEGY:
1. Check file size first (if available from metadata)
   - < 5MB: Read directly with Read tool
   - 5-20MB: Read first 50 pages only
   - > 20MB: Skip, flag for manual review
2. If no size available, attempt read:
   - If succeeds: extract insights
   - If times out or fails: skip and flag
3. For scanned PDFs (no extractable text):
   - Skip, flag as "scanned PDF - needs OCR"
```

**Skip criteria (don't waste time):**
- PDFs > 20MB (likely books or massive reports)
- Scanned documents without OCR
- Zip files or archives
- Video/audio files (note title only)

**For each article, extract:**
```
SOURCE: [title] - [url]
TYPE: [framework / case-study / opinion / tutorial / research]
KEY INSIGHT: [1-2 sentence core idea]
ACTIONABLE: [Yes/No - can this become a process?]
FRAMEWORKS: [Any named methodologies?]
```

### Phase 3: Cluster

Group insights by theme:

```
CLUSTERING QUESTIONS:
- What problems do multiple sources address?
- What methodologies appear repeatedly?
- What contradictions exist?
- What's unique vs. common knowledge?
```

**Output format:**
```
THEME: [name]
Sources: [list]
Core insight: [synthesis]
Skill potential: [High/Medium/Low]
```

### Phase 4: Synthesize

For high-potential themes, create actionable output:

```
SYNTHESIS OPTIONS:
1. Skill - if it's a methodology Claude should auto-apply
2. Prompt - if it's a one-time process user would paste
3. Reference doc - if it's knowledge, not process
4. Discard - if it's common knowledge or too vague
```

**Skill criteria:**
- Specific trigger conditions
- Named principles or laws (not invented)
- Clear diagnostic/output format
- Adds value over Claude's base knowledge

## Output Format

```
INSIGHT EXTRACTION REPORT

COLLECTION: [name/url]
AUDITED: [date]
TOTAL ITEMS: [count]
SUCCESSFULLY READ: [count]
BLOCKED: [count]

THEMES IDENTIFIED:
1. [Theme]: [X sources] - [skill potential]
2. [Theme]: [X sources] - [skill potential]

HIGH-VALUE INSIGHTS:
- [Insight] (from: [source])
- [Insight] (from: [source])

RECOMMENDED ACTIONS:
- Create skill: [name] - based on [theme]
- Create prompt: [name] - for [use case]
- Manual review needed: [blocked URLs]

BLOCKED SOURCES (need manual access):
- [url] - [reason]

SKIPPED (too large or unsupported):
- [filename] - [size] - [reason]
```

## Failure Modes

| Problem | Solution |
|---------|----------|
| Most links blocked | Focus on non-paywalled sources first |
| Large PDFs (>20MB) | Skip and flag - likely books, not articles |
| Scanned PDFs | Skip - no extractable text without OCR |
| No clear themes | Collection may be too diverse - narrow scope |
| All common knowledge | Look for unique combinations, not individual insights |
| Too much content | Prioritize recent items, or items with descriptions |

## When to Stop

Stop when sufficient insights are extracted:
- You've extracted 10+ actionable insights
- Remaining sources are blocked/inaccessible
- Themes are repeating (saturation)
- User has enough to work with

Extract what's accessible, flag what's not, move on.
