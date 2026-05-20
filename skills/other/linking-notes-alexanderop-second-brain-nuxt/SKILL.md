---
name: linking-notes
description: Discover and add wiki-links between notes. Use when asked to "find connections", "link this note", "what should I link to", or "connect my notes".
allowed-tools: Read, Glob, Grep
---

# Discovering Wiki-Link Connections

This skill helps find meaningful connections between notes in the knowledge base.

## Workflow

### 1. Identify the Target Note

If a specific note is mentioned, read it first:

```bash
# List all content to find the note
ls content/*.md
```

Extract from the target note:
- Title
- Tags
- Key concepts/terms
- Existing wiki-links

### 2. Search for Related Content

**By Title Mentions:**
```bash
# Search for the note's title in other files
grep -l "note title" content/*.md
```

**By Tag Overlap:**
```bash
# Find notes sharing the same tags
grep -l "tags:.*tag-name" content/*.md
```

**By Key Terms:**
```bash
# Search for key concepts
grep -l "specific concept" content/*.md
```

### 3. Evaluate Connection Strength

**Aim for connection, not perfection.** Every note benefits from 2-3 meaningful links. An orphan note is harder to discover than an over-connected one.

✅ **Link when:**
- Same author or creator
- Explicitly references or cites the other work
- Directly builds on or responds to the other content
- Covers the same core topic (e.g., two notes about "habit formation")
- Part of the same series or project
- Should be grouped together in a **Map Note** (MOC)
- Offers a contrasting perspective on the same idea
- Applies theory from one note to practice in another

❌ **Avoid linking when:**
- Only a vague thematic overlap (e.g., "both mention AI")
- The connection requires multiple hops of reasoning
- You haven't read the target note and can't explain the relationship

**Every link needs context.** Don't just link - explain WHY the connection exists in 1 sentence.

### 4. Present Suggestions

For each suggested link, provide:
1. The slug to link: `[[slug-name]]`
2. Brief justification (1 sentence)
3. Where in the note it would fit (if applicable)

## Output Format

```markdown
## Suggested Wiki-Links for [Note Title]

### Strong Connections
- [[related-note-1]] - Same author, discusses related concepts
- [[related-note-2]] - Directly cited in this content

### Potential Connections (Review Needed)
- [[maybe-related]] - Shares "testing" tag, similar topic
```

## Map Notes for Clustering

If you find a group of 3+ notes with strong thematic connections, consider suggesting a **Map Note** (MOC) instead of individual links:

```bash
# Check existing maps
grep -l "type: map" content/*.md
```

Map notes (`type: map`) create visual clusters on the graph - notes linked from the map are pulled together. This is useful for:
- Learning paths (e.g., "Vue 3 Development Guide")
- Topic clusters (e.g., "Leadership Principles")
- Curated collections (e.g., "AI Agents Roadmap")

## Quality Checklist

Before suggesting links:
- [ ] Read the target note thoroughly
- [ ] Verified each suggestion has a strong, direct connection
- [ ] Excluded vague thematic overlaps
- [ ] Checked that suggested notes actually exist
- [ ] Provided clear justification for each link
- [ ] Considered whether a Map Note would better organize related content
