---
name: keine-update-maps
description: Use this skill when creating or editing a topic map in the Keine knowledge base. Trigger after ingesting a set of related entries on a topic, or when asked to summarize, compare, survey, or give an overview of a subject area. Also use when a user asks a broad question and you want to leave a synthesized overview for future agents or readers. Maps are different from entries — they synthesize rather than document.
compatibility: Require `keine-manage` skill
---

# Creating and Editing Topic Maps

## What a topic map is for

A topic map is a synthesized overview of a subject area. Where entries capture individual pieces of knowledge, a map connects them — explaining how things evolved, how they compare, and where to start depending on what someone needs.

Maps serve two audiences equally:
- **Humans** wanting to understand a topic landscape at a glance
- **Future agents** that need to quickly orient themselves before answering questions or creating more entries

A map is worth creating when there are enough related entries (roughly 4–5+) that the relationships between them tell a story worth telling.

## Creating a new map

### 1. Gather related entries

Search for everything relevant to the topic:

```sh
grep -ri "keyword" docs/
ls docs/tags/<relevant-tag>.md
```

Read the entries. Understand the landscape before writing — the map's value comes from synthesis, not just listing links.

### 2. Write the map

File location: `docs/maps/<slug>.md`

Frontmatter:

```yaml
---
title: "Topic Area Name"
tags: [tag-a, tag-b]
---
```

Suggested body structure (adapt as needed):

- **H1** = title
- **## Overview** — brief introduction: what this topic area is and why it matters
- **## Landscape** — how the technologies/concepts relate, how they evolved, how they compare; use H3 subheadings per major area or technology
- **## Where to start** — practical guidance for different starting points (e.g. "if you want X, start with Y")
- **## Learning Path** *(optional)* — ordered list of entries to read in sequence
- **## Entries** — full list of related entries with one-line descriptions

The map should read like a knowledgeable friend orienting you to a topic — not a dry index.

### 3. Commit

```sh
git add docs/maps/<slug>.md
git commit -m "docs(map): add <title>"
```

---

## Editing an existing map

Maps go stale as new entries are added. Update a map when:
- New entries have been created that belong in it
- The landscape has shifted (new technology, deprecated approach, etc.)
- The overview or comparisons are no longer accurate

After editing:

```sh
git add docs/maps/<slug>.md
git commit -m "docs(map): update <title>"
```
