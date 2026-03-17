---
name: moc-curator
description: |
  Suggest MOC updates and new MOCs based on semantic clustering.
  Use when asked to "curate MOCs", "update maps", "find clusters",
  "what MOCs need updating", or "organize my notes".
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion
---

# MOC Curator

This skill uses semantic embeddings to suggest MOC (Map of Content) updates and discover new MOC opportunities.

## Capabilities

1. **Find MOC Gaps**: Notes that should be in existing MOCs but aren't linked
2. **Discover Clusters**: Groups of orphan notes that could form new MOCs
3. **Detect Hub Notes**: Notes with many outgoing links that could become MOCs
4. **Per-Note Suggestions**: Which MOCs a specific note should join

Embeddings include title, summary, and first 500 characters of body content for improved semantic accuracy.

## Workflow

### Phase 1: Gather Context

Run the clustering script to analyze the knowledge base:

```bash
python3 .claude/skills/moc-curator/scripts/cluster-notes.py --mode=full
```

Parse the JSON output:
- `moc_updates`: Existing MOCs with missing notes
- `new_clusters`: Orphan note clusters that could be MOCs

### Phase 2: Present MOC Update Suggestions

For each MOC with gaps, show:

```markdown
### [[moc-slug]] - MOC Title

Currently has X members. Suggested additions:

1. **[[note-slug]]** (score: 0.82)
   - Type: article | Tags: tag1, tag2
   - Shares tags: shared-tag

2. **[[another-note]]** (score: 0.75)
   - Type: youtube | Tags: tag3
   - High semantic similarity to existing members
```

### Phase 3: Present New MOC Opportunities

For each orphan cluster:

```markdown
### Potential New MOC: "Inferred Theme"

Common tags: tag1, tag2, tag3

Notes in this cluster:
- [[note-a]] - Note A Title
- [[note-b]] - Note B Title
- [[note-c]] - Note C Title

**Suggested MOC name**: `theme-name-guide.md`
```

### Phase 4: User Selection (Blocking Gate)

Use the `AskUserQuestion` tool to ask which suggestions to apply:

```yaml
question: "Which MOC suggestions would you like me to apply?"
header: "MOC Updates"
multiSelect: false
options:
  - label: "Apply all MOC updates"
    description: "Add suggested notes to existing MOCs"
  - label: "Apply all new MOC creations"
    description: "Create new MOCs from discovered clusters"
  - label: "Select specific suggestions"
    description: "Choose individual suggestions to apply"
  - label: "Skip all"
    description: "Don't make any changes"
```

**Wait for explicit approval before making any changes.**

### Phase 5: Apply Changes

**For MOC Updates:**
1. Read the existing MOC file
2. Append new links to a `## Suggested` section at the end

```markdown
## Suggested

- [[new-note-1]] - Brief description of why it belongs
- [[new-note-2]] - Brief description of why it belongs
```

**For New MOCs:**
1. Read the writing-style skill for prose guidelines:
   - Use the Read tool on `.claude/skills/writing-style/SKILL.md`
   - Apply its 10 rules when writing MOC descriptions
2. Create a new map note following the pattern:

```yaml
---
title: "Theme Name Guide"
type: map
tags:
  - common-tag-1
  - common-tag-2
---

Description of what this map covers.

## Section Name

- [[note-a]] - What this note contributes
- [[note-b]] - What this note contributes
```

### Phase 6: Quality Check

Run linter and type check to catch any issues:

```bash
pnpm lint:fix && pnpm typecheck
```

If errors are found, fix them before completing the task.

## Script Usage

```bash
# Full analysis (MOC gaps + new clusters + hub notes)
python3 .claude/skills/moc-curator/scripts/cluster-notes.py --mode=full

# Only MOC gaps
python3 .claude/skills/moc-curator/scripts/cluster-notes.py --mode=moc-gaps

# Only orphan clusters
python3 .claude/skills/moc-curator/scripts/cluster-notes.py --mode=new-clusters

# Only hub notes (potential MOCs)
python3 .claude/skills/moc-curator/scripts/cluster-notes.py --mode=hub-notes

# Suggestions for a specific note (used by adding-notes hook)
python3 .claude/skills/moc-curator/scripts/cluster-notes.py --mode=for-note --note=slug-name

# Adjust threshold (default: 0.7 - strict)
python3 .claude/skills/moc-curator/scripts/cluster-notes.py --threshold=0.6

# Adjust minimum links for hub detection (default: 5)
python3 .claude/skills/moc-curator/scripts/cluster-notes.py --mode=hub-notes --min-links=3
```

## JSON Output Format

```json
{
  "moc_updates": [
    {
      "moc": "slug",
      "moc_title": "Title",
      "current_members": 5,
      "missing_notes": [
        {"slug": "note", "title": "Title", "score": 0.82, "shared_tags": ["tag"], "type": "article"}
      ]
    }
  ],
  "new_clusters": [
    {
      "cluster_id": 0,
      "theme": "Inferred Theme",
      "common_tags": ["tag1", "tag2"],
      "notes": [{"slug": "note", "title": "Title", "type": "article"}],
      "size": 3
    }
  ],
  "orphan_stats": {
    "total_orphans": 20,
    "clustered": 8,
    "unclustered": 12
  },
  "potential_mocs": [
    {
      "slug": "note-slug",
      "title": "Note Title",
      "type": "article",
      "outgoing_links": 7,
      "links": ["link-a", "link-b", "link-c"]
    }
  ],
  "for_note": [
    {"moc": "slug", "moc_title": "Title", "score": 0.82, "reason": "shares tags: x; semantic similarity: 82%"}
  ]
}
```

## Error Recovery

| Issue | Resolution |
|-------|------------|
| No embeddings cache | Script will auto-generate embeddings |
| sklearn not installed | `pip install scikit-learn` |
| Empty results | Try lower threshold: `--threshold=0.6` |
| sentence-transformers missing | `pip install sentence-transformers` |

## Quality Guidelines

- Only suggest notes with similarity >= 0.7 (strict threshold)
- New MOCs require at least 3 notes in a cluster
- Always show the reasoning (shared tags, similarity score)
- Let the user decide what to apply - never auto-modify MOCs
