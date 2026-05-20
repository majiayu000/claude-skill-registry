---
name: keine-update-entries
description: Use this skill when creating a new knowledge entry or editing an existing one in the Keine knowledge base. Trigger when asked to add, ingest, document, or update any piece of knowledge — a URL, PDF, book, concept, note, or research finding. Use this skill even when the user doesn't say "entry" — if they want to capture or update knowledge, this is the skill.
compatibility: Require `keine-manage` skill
---

# Creating and Editing Knowledge Entries

## Creating a new entry

### 1. Search first

Before creating, check whether something close already exists:

```sh
grep -ri "keyword" docs/
ls docs/tags/
```

If a close match exists, consider updating it instead of creating a new file.

### 2. Choose a slug

Format: `YYYY-MM-DD-short-descriptive-slug.md`. Use today's date. Keep the slug lowercase and hyphen-separated. Prefer concrete nouns over vague ones (`2026-03-11-docker-networking.md` beats `2026-03-11-containers.md`).

### 3. Write the file

Fill all frontmatter fields:

```yaml
---
title: "Human-readable title"
description: "One sentence for use in tag indexes"
tags: ["tag1", "tag2"]
source: "URL, DOI, or other reference"   # required — link to the original
source_type: "url | pdf | book | note"   # required — omit only for original writing
---
```

Body:
- **H1** = title (exactly one)
- **## Summary** — 2-5 sentences capturing the core idea
- **## Content** — main knowledge; use H3+ for subsections
- **## Related** — relative links to other entries, tags, or maps

For ingested content (URL, PDF, book), summarize in your own words — do not copy verbatim.

#### Academic papers: extended content format

Use this format when the source is an academic paper. This applies when:
- The user explicitly says the source is a paper or research paper
- The source is a PDF and it appears to be an academic paper (has abstract, authors, references, venue/conference/journal markers), or the source is a url of an academic paper

When any of the above is true, replace the plain `## Content` section with the three-pass structure below, and add the `## Evaluation` section.

```markdown
## First Pass — Bird's-Eye View

### Category
What type of paper is this? (measurement, system design, analysis, survey, …)

### Context
Which prior work does it build on? What theoretical foundations does it use?

### Correctness
Do the core assumptions appear valid?

### Contributions
What are the 2-4 main contributions claimed?

### Clarity
Is the paper well-structured and clearly written?

## Second Pass — Content Grasp

### Problem & Motivation
What problem is solved and why does it matter?

### Approach
High-level description of the method, architecture, or analysis technique.

### Key Figures & Results
Summarize the most important graphs, tables, or experimental findings. Note whether axes are labeled, error bars are present, and whether conclusions are statistically supported.

### Key References
List 3-5 important cited works worth following up on.

## Third Pass — Deep Understanding

### Core Mechanism
Explain the central idea in enough detail that a peer could re-implement it.

### Hidden Assumptions
What implicit assumptions does the work rely on? Are any questionable?

### Reproducibility & Limitations
Data availability, missing implementation details, or scope constraints.

### Ideas for Future Work
Extensions or open questions surfaced during reading.

## Evaluation

### Advantages
1. …
2. …
3. …

### Disadvantages
1. …
2. …
3. …

## Key References
List important references of this work.
```

### 4. Update tags

Run from the repo root after writing the file `scripts/maintain_tags.py`

### 5. Commit

You *must* stage the new entry and any updated tag files:

```sh
git add docs/<new-entry>.md docs/tags/
git commit -m "docs: add <title>"
```

---

## Editing an existing entry

1. Find the entry — search by keyword or tag (see below)
2. Edit content or frontmatter as needed
3. If tags changed, re-run `scripts/maintain_tags.py`
4. You *must* commit:
   ```sh
   git add docs/<entry>.md docs/tags/
   git commit -m "docs: update <title>"
   ```

---

## Finding entries

- By keyword: `grep -ri "term" docs/`
- By tag: read `docs/tags/<tag>.md`
- By topic: check `docs/maps/` for a topic map
