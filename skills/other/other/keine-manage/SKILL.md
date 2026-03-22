---
name: keine-manage
description: Always use this skill before creating, editing, or tagging any document in the knowledge base. Use it when asked to add, ingest, find, link, or manage any entry.
compatibility: Requires git, uv and Python
---

# Keine Knowledge Base Management

## Assets

```
references
|-- TEMPLATE_ENTRY.md
|-- TEMPLATE_TAG.md
`-- TEMPLATE_TOPIC.md
scripts
`-- maintain_tags.py    — maintain tag index
```

## Document Format

### Knowledge Entry (`docs/<yyyy-mm-dd-slug>.md`)

```yaml
---
title: "Human-readable title"
description: "One sentence for use in tag indexes"
tags: ["tag1", "tag2"]
source: "URL, DOI, or other reference"   # required — link to the original
source_type: "url | pdf | book | note"   # required — omit only for original writing
---
```

Body structure:
- **H1** = title (exactly one)
- **## Summary** — 2-5 sentences
- **## Content** — main knowledge, use H3+ for subsections
- **## Related** — relative links to other docs, tags, or maps

### Tag Index (`docs/tags/<slug>.md`)

Auto-maintained. **Do not edit manually.** Run `scripts/maintain_tags.py`

### Topic Map (`docs/maps/<slug>.md`)

```yaml
---
title: "Topic Area Name"
tags: [tag-a, tag-b]
---
```

Body: structured overview, mindmap, or learning path linking to entries.

## Workflow

For the task at hand, use the appropriate sub-skill:

| Task | Skill |
|---|---|
| Create or edit a knowledge entry | `keine-update-entries` |
| Create or edit a topic map | `keine-update-maps` |
| Create a deep research report | `keine-research` |

### Finding entries

- By keyword: `grep -ri "term" docs/`
- By tag: read `docs/tags/<tag>.md`
- By topic: check `docs/maps/` for a topic map
