---
name: research-processing
description: Use when adding external sources to research library - normalizes source, extracts insights, assigns topic, validates integrity, and writes to datasets/research/{topic}/
---

# Research Processing

## Purpose

Add external sources to organized research library:
- Normalize source format (file, URL, or note)
- Extract key insights and strategic applications
- Assign topic category
- Validate source integrity
- Write to datasets/research/{topic}/

## When to Use

Activate when:
- User invokes `/research:process-source`
- Adding external article, report, or framework
- Building research context for strategy sessions

## Workflow

### 1. Accept Source Input

**Input formats:**
- `--url='https://...'`: Fetch external URL
- `--file='/path/to/file.pdf'`: Local file
- `--from-chat`: Use conversation context as note

### 2. Normalize Source

**Invoke:** `source-normalization` skill

**Outputs:**
- Stable ID (src_{hash})
- Checksum calculation
- Metadata extraction (title, author, date)
- Saved to temp location

### 3. Extract Content

**For URLs:**
- Fetch with WebFetch
- Extract title from <title> or H1
- Convert HTML to markdown
- Save cleaned content

**For files:**
- Read content
- Extract metadata from frontmatter if present
- Copy to research library

**For notes:**
- Use conversation text
- Generate title from first sentence
- Save as markdown

### 4. Extract Insights

**Interactive or auto:**

**Ask user (or analyze):**
- What are the key insights? (3-5 bullets)
- How does this apply strategically? (use cases)
- Notable quotes to preserve?
- Related internal context? (meetings, epics)

**Structure:**
```markdown
## Key Insights
- Insight 1
- Insight 2
- Insight 3

## Strategic Applications
- How this informs decisions
- Relevant use cases

## Citations / Quotes
> "Verbatim quote"
> — Author, Source (Date)

## Related Internal Links
- [Meeting](datasets/meetings/...)
- [Epic](datasets/product/epics/...)
```

### 5. Assign Topic

**Topics:**
- competitive-analysis
- pricing-strategy
- market-positioning
- product-strategy
- customer-segmentation
- growth-strategy

**Ask user or auto-assign based on content.**

### 6. Set Expiry Date

**Apply guidelines:**
- Frameworks: 365-730 days (1-2 years)
- Market data: 90-180 days (3-6 months)
- Competitor intel: 180-365 days (6-12 months)
- Customer insights: 180-365 days (6-12 months)

### 7. Validate Source Integrity

**Invoke:** `source-integrity` skill

- Verify checksum calculated
- Verify all required metadata present
- Verify expiry_date set appropriately
- Validate schema compliance

### 8. Write to Research Library

**Output:** `datasets/research/{topic}/{filename}.md`

**Filename:** `{YYYYMMDD}_{slug_from_title}.md`

**Full YAML frontmatter:**
```yaml
---
title: "Source Title"
kind: "url" | "file" | "note"
topic: "{topic}"
url: "https://..." (if URL)
checksum: "sha256:..."
added_utc: "2025-10-21T..."
expiry_date: "YYYY-MM-DD"
author: "..." (if available)
published_date: "..." (if available)
tags: ["keyword1", "keyword2"]
---
```

## Success Criteria

- Source normalized with stable ID
- Insights extracted (key insights, strategic applications)
- Topic assigned
- Expiry date set
- Source integrity validated
- Written to datasets/research/{topic}/

## Related Skills

- `source-normalization`: Normalizes input format
- `source-integrity`: Validates metadata and checksum
- `research-gathering`: Uses processed sources for strategy sessions
