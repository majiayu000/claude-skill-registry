---
name: exploring-graph
description: Analyze the knowledge graph for insights. Use when asked to "analyze connections", "graph report", "show hubs", "find orphans", or "knowledge map".
allowed-tools: Read, Glob, Grep
---

# Exploring the Knowledge Graph

This skill analyzes the structure of connections in the knowledge base to surface insights.

## Workflow

### 1. Build the Connection Map

Parse all wiki-links from every content file:

```bash
# Extract all wiki-links
grep -oh '\[\[[^]]*\]\]' content/*.md

# Get links per file
for f in content/*.md; do
  echo "=== $f ==="
  grep -o '\[\[[^]]*\]\]' "$f"
done
```

Build an adjacency list:
- `note-a` → links to: `[note-b, note-c]`
- `note-b` → links to: `[note-a]`
- etc.

### 2. Calculate Metrics

**For each note, determine:**

| Metric | Description |
|--------|-------------|
| Outgoing links | Wiki-links in this note |
| Incoming links | Other notes linking to this one |
| Total connections | Outgoing + Incoming |

### 3. Identify Patterns

#### Hub Notes (Most Connected)
Notes with the highest total connections - these are central to the knowledge base.

#### Orphan Notes
- **Full orphans**: 0 incoming AND 0 outgoing links
- **Dead ends**: Has outgoing but 0 incoming
- **Sources**: Has incoming but 0 outgoing

#### Clusters
Groups of notes that link heavily to each other but less to the rest. Identify by:
- Shared tags
- Mutual links
- **Map membership** - notes linked from a `type: map` note form visual clusters

#### Map Notes (MOCs)
Map notes (`type: map`) act as cluster centers on the graph:
- Appear as **pink hexagons** instead of circles
- Pull member notes toward them with gravitational force
- Members are defined by wiki-links FROM the map
- Use the Maps filter in the graph UI to focus on specific clusters

To find existing maps:
```bash
grep -l "type: map" content/*.md
```

#### Broken Links
Wiki-links pointing to non-existent notes.

### 4. Generate Insights Report

```markdown
## Knowledge Graph Analysis

### Overview
- Total notes: 15
- Total connections: 42
- Average connections per note: 2.8

### Hub Notes (Top 5 Most Connected)
| Note | Outgoing | Incoming | Total |
|------|----------|----------|-------|
| [[central-concept]] | 5 | 8 | 13 |
| [[key-framework]] | 4 | 6 | 10 |
| ... | | | |

### Orphan Notes (Need Attention)
**Full Orphans** (isolated):
- `lonely-note.md` - no connections at all

**Dead Ends** (no incoming links):
- `new-note.md` - links out but not referenced

**Sources** (no outgoing links):
- `reference-only.md` - referenced but doesn't link

### Potential Clusters
**Vue Ecosystem** (5 notes, 12 internal links):
- [[vue-composables]]
- [[vue-testing]]
- [[nuxt-patterns]]
- ...

**AI/Agents** (3 notes, 6 internal links):
- [[12-factor-agents]]
- [[context-efficient-backpressure]]
- ...

### Connection Opportunities
Based on shared tags and titles, these notes might benefit from links:
- [[note-a]] and [[note-b]] share 3 tags but aren't linked
```

## Graph Health Indicators

| Indicator | Healthy | Warning |
|-----------|---------|---------|
| Orphan rate | <10% | >20% |
| Avg connections | >2 | <1 |
| Broken links | 0 | Any |

## Quality Checklist

When analyzing:
- [ ] Parsed all wiki-links from all files
- [ ] Counted incoming/outgoing per note
- [ ] Identified hub notes
- [ ] Found orphan notes
- [ ] Detected potential clusters
- [ ] Checked for broken links
- [ ] Suggested connection opportunities
