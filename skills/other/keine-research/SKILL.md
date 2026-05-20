---
name: keine-research
description: >
  Use this skill only when the user explicitly requests deep research or a detailed report on a topic —
  phrases like "research X", "give me a detailed report on X", "deep dive into X", "I want a thorough
  analysis of X", or "write me a research report on X". Do NOT trigger for casual questions, quick
  lookups, or requests to add/edit entries. This is a heavyweight, multi-step workflow that mines the
  knowledge base, fills gaps with web research, creates new KB entries along the way, and produces a
  long-form, citation-rich research report saved to reports/.
compatibility: Require `keine-manage` skill
---

# Keine Research

This skill produces a long-form research report grounded in the knowledge base and supplemented by
web research. The output is saved as a Markdown file in `reports/`.

## When to use this skill

Only trigger when the user explicitly asks for research, a deep dive, or a detailed report. This is
not a lookup skill — it is a slow, thorough process. If the user asks a quick question, answer it
directly. If they want to *add* something to the KB, use `keine-update-entries` instead.

## Report location

All reports go in `reports/<yyyy-mm-dd-slug>.md`. This directory is separate from entries
(`docs/`) and maps (`docs/maps/`). Reports are synthesis documents — they cite KB entries and web
sources but are not themselves knowledge entries.

---

## Workflow

Work through each phase in order. Do not skip ahead.

### Phase 1 — Understand the question

Before touching the KB, decompose the research question:

- What is the user actually asking? Restate it precisely.
- What sub-questions or facets need to be addressed for a complete answer?
- What depth of coverage is expected? (If unclear, assume comprehensive.)

Write these sub-questions down — they become the skeleton of the report.

### Phase 2 — Mine the knowledge base

Use the KB's structure to orient yourself quickly:

```sh
# Survey topic maps
ls docs/maps/

# Survey available tags
ls docs/tags/

# Search for relevant keywords
grep -ri "keyword" docs/
```

Read all relevant map files first — they give the fastest orientation to a topic area and link to
the most relevant entries.

Then read the specific entries linked from those maps and tags. For each entry, note:
- What it covers
- Which sub-questions it answers (fully or partially)
- What it does NOT cover

Be honest about gaps. Local knowledge is almost always incomplete for a substantive research
question.

### Phase 3 — Web research

For each gap or unanswered sub-question identified in Phase 2, search the web. Be systematic:
search each facet deliberately rather than doing a single broad search.

**For each significant web finding:**
- If the finding has durable value (it's not ephemeral news or trivial), create a KB entry using
  the `keine-update-entries` skill. This ensures future agents can find it.
- Track the source URL to include in the report's references, whether or not you create an entry.

Do not create entries for every result — only for knowledge worth keeping. A good rule: if a
future agent researching a related question would benefit from finding this entry, create it.

After creating new entries, run tag maintenance `scripts/maintain_tags.py`

### Phase 4 — Write the report

Write a detailed, long-form report. Inline citations (`[1]`, `[2]`, ...) should appear throughout
the body wherever a claim is grounded in a specific source. Numbered references are listed at the
end.

Aim for depth over brevity — this is not a summary. Each section should explain, not just list.

#### Report frontmatter

```yaml
---
title: "Research Report: <topic>"
question: "<the original user question, verbatim>"
---
```

#### Report structure

```markdown
# Research Report: [Topic]

## Research Question
State the exact question being answered and any clarifications about scope.

## Executive Summary
5–8 sentences capturing the key answer, major findings, and most important takeaways.
Write this last, after the full report is drafted.

## [Section per major facet or sub-question]

Detailed prose covering the facet. Use H3 subheadings for subsections.
Cite sources inline: "According to [1], ..." or "This pattern is well-documented [2][3]."

Repeat for each sub-question identified in Phase 1.

## Synthesis
How do the findings across sections connect? What is the overall picture?
What tensions, trade-offs, or unresolved debates exist?

## Gaps & Open Questions
Aspects that couldn't be fully resolved with available sources.
Questions worth pursuing in future research.

## References

### Knowledge Base Entries
- [KB-1] [Title](../relative/path/to/entry.md) — one-line description
- [KB-2] ...

### Web Sources
- [W-1] [Title or description](URL)
- [W-2] ...
```

Use `[KB-N]` for KB entries and `[W-N]` for web sources as inline citation keys.

### Phase 5 — Save and commit

Save the report to `reports/<yyyy-mm-dd-slug>.md`. The slug should reflect the topic, not the
date (e.g., `2026-03-11-transformer-attention-mechanisms.md`).

Commit everything created in this workflow:

```sh
git add reports/<report>.md docs/ docs/tags/
git commit -m "docs(report): <topic>"
```

### Phase 6 — Update topic map (if warranted)

If Phase 3 produced several new entries on a coherent topic, consider updating or creating a topic
map using `keine-update-maps`. This is optional — only do it if the new entries genuinely enrich
an existing map or justify a new one.

---

## Quality bar

A good research report:

- Has inline citations throughout — claims should be traceable to sources
- Covers all sub-questions identified in Phase 1
- Is honest about what is unknown or unresolved
- Creates at least a few new KB entries from web research (unless local knowledge was already
  comprehensive)
- Is long enough to be genuinely useful — several hundred to a few thousand words depending on the
  topic

A poor report is a bullet-point summary with no citations and no new entries created. Push past
the surface.
