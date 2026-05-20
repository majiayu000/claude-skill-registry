---
name: summarizing-topic
description: Synthesize knowledge on a topic from multiple notes. Use when asked "what do I know about X", "summarize topic", "synthesize notes on", or "overview of".
allowed-tools: Read, Glob, Grep
---

# Synthesizing Topic Knowledge

This skill aggregates knowledge from multiple notes on a topic to create a unified understanding.

## Workflow

### 1. Identify the Topic

The user will specify a topic, which could be:
- A tag (e.g., "vue", "testing")
- A concept (e.g., "local-first", "composables")
- A question (e.g., "how to test Vue apps")

### 2. Find Related Notes

**Search by tag:**
```bash
grep -l "tags:.*topic-name" content/*.md
```

**Search by title/content:**
```bash
grep -l "topic keyword" content/*.md
```

**Search by wiki-links:**
```bash
grep -l "\[\[topic-related-slug\]\]" content/*.md
```

### 3. Read and Extract

For each related note, extract:
- **Title and type**: What is this content?
- **Summary**: The core idea
- **Key points**: Main takeaways
- **Quotes**: Memorable passages
- **Connections**: What it links to

### 4. Synthesize

Combine the extracted knowledge into a coherent overview:

```markdown
## What You Know About [Topic]

### Overview
[1-2 paragraph synthesis of the topic based on your notes]

### Key Themes
1. **Theme A**: Explanation drawing from multiple notes
2. **Theme B**: Explanation drawing from multiple notes

### Sources in Your Knowledge Base
| Note | Type | Key Contribution |
|------|------|------------------|
| [[note-1]] | article | Introduces concept X |
| [[note-2]] | book | Deep dive on approach Y |
| [[note-3]] | podcast | Practical examples |

### Notable Quotes
> "Quote from note-1"

> "Quote from note-2"

### Gaps and Questions
- You don't have notes on [related subtopic]
- Consider exploring: [suggested areas]

### Suggested Next Steps
- Read [[related-note]] for more on X
- Consider adding notes on Y
```

## Synthesis Guidelines

**Do:**
- Identify common threads across notes
- Note contradictions or different perspectives
- Highlight unique insights from each source
- Suggest gaps in coverage

**Don't:**
- Just list summaries without connecting them
- Ignore contradictions between sources
- Over-quote without synthesis
- Make up information not in the notes

## Output Formats

### Brief Summary
For quick reference - 2-3 paragraphs max.

### Comprehensive Overview
For deep understanding - includes all sections above.

### Gap Analysis
Focus on what's missing - useful for deciding what to read next.

## Quality Checklist

When synthesizing:
- [ ] Found all relevant notes (tags + keywords)
- [ ] Read each note thoroughly
- [ ] Identified common themes
- [ ] Noted contradictions or tensions
- [ ] Credited sources with wiki-links
- [ ] Highlighted gaps in coverage
- [ ] Provided actionable next steps
