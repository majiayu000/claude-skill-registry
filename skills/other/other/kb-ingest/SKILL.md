---
name: kb-ingest
description: Ingest external sources into the knowledge bank through interactive study or quick filing. Two modes — Quick (summarize → file) and Study (theme-by-theme deep dive with online research and personal notes → multi-layer KB output → optional blog/slack synthesis). Triggers on "ingest this", "study this article", "add to knowledge bank", "learn from this", "process this article", "take notes on this", "what are the key takeaways", "break this down for me", or when user provides external reference material for long-term retention. Also use when user says "let's go through this", wants to deeply engage with a source document, or shares an article/gist/doc and asks about its content.
user-invocable: true
---

# Knowledge Bank Ingest

Ingest external knowledge sources into the knowledge bank. Two modes serve different depths of engagement:

- **Quick mode**: Summarize → agree on doc type → file to KB. For sources you want to preserve but don't need to deeply study.
- **Study mode**: Theme-by-theme deep dive with online research → personal notes → multi-layer KB output → optional synthesis. For sources you want to actively learn from and potentially share.

**Knowledge Bank Location**: Read from `~/.claude/plugins/config/second-brain/config.json`.

**Philosophy**: The discussion between you and the user shapes what gets preserved — this is not a summarizer, it's a collaborative knowledge integration tool. A single source can touch multiple KB pages.

---

## Invocation

```
/second-brain:kb-ingest /path/to/article.md
/second-brain:kb-ingest https://example.com/interesting-post
```

---

## Step 1: READ

Read the source document (file path → Read tool, URL → WebFetch, inline → accept directly).

For large sources (>100KB), apply the [distillation guide](../session-recap/references/distillation-guide.md).

Identify the source's major themes, key concepts, and actionable patterns.

---

## Step 2: MODE SELECT

After reading, use the **AskUserQuestion tool** to let the user choose their engagement mode:

- **Quick** — Summarize key points, agree on doc type, file to KB
- **Study** — Walk through theme by theme with online research and personal notes, then create multi-layer KB output

---

## Step 3: ENGAGE

### Quick Mode

1. **Summarize** the source's main contributions (3-5 bullet points)
2. **Propose** what to preserve and as what type (concept / component / best-practice / multiple)
3. Use the **AskUserQuestion tool** to confirm: What resonates? What project context? Anything to add from their own experience?
4. Proceed to Step 4 (CREATE) once agreed

### Study Mode

Walk through the source **theme by theme**. For each theme:

1. **Present** — explain the core idea, key examples, and why it matters
2. **Explore** — research online (WebSearch/WebFetch) to find 2-3 relevant pieces that enrich the theme: related work, counter-arguments, real-world applications. The goal is to add context, not exhaustively survey. See [study-mode-guide.md](references/study-mode-guide.md) for depth guidance and a walkthrough example.
3. **Pause** — let the user note their takeaways in their own words
4. **Capture** — record the user's personal insights, reframings, and connections to existing knowledge. The user often synthesizes more sharply than the source — preserve their framing, not just the article's.
5. **Repeat** for the next theme until the source is covered

The user's notes are first-class output — they're not just "discussion", they're the learning record that becomes the study docs in Step 4.

---

## Step 4: CREATE

### Quick Mode Output

Generate concept/component/best-practice doc(s) as in the [ingest guide](references/ingest-guide.md). Target 5-8 WikiLinks.

### Study Mode Output — Three Layers

Study mode produces three layers of documentation, each serving a different future use:

| Layer | Location | Purpose |
|-------|----------|---------|
| **Source copy** | `projects/{project}/sources/` | Original article with KB frontmatter — raw material for re-reading |
| **Digest** | `projects/{project}/study/` | Numbered principles organized by category — quick reference |
| **Learning notes** | `projects/{project}/study/` | Per-theme notes capturing the interactive discussion and online research — personal thinking record |

Plus the standard concept/component/best-practice docs distilled from the study.

**Frontmatter for all docs:**
```yaml
---
title: Document Title
aliases: [Alt 1, Alt 2]
tags: [category, topic]
type: concept|component|best-practice|study|source
created: YYYY-MM-DD
modified: YYYY-MM-DD
project: {project}
source-type: article|document|url|gist
ingested-from: /path/to/source.md or https://url
source-doc: "[[Source Document Title]]"
---
```

**Cross-references**: Run `search_cross_references.sh "keyword" [project]`. Target 5-8 WikiLinks.

**Obsidian Syntax**: When obsidian skills are available, invoke `/obsidian:obsidian-markdown` before creating documents.

**Updating existing docs**: If new knowledge connects to or supersedes existing KB pages, update them — add cross-references, revise outdated claims, note where new data strengthens or challenges existing content.

---

## Step 5: SYNTHESIZE (optional, after Study mode)

After Study mode CREATE is complete, use the **AskUserQuestion tool** to ask what synthesis the user wants:

- **Blog post** — Synthesize into a listicle-style blog post following the [blog synthesis guide](references/blog-synthesis-guide.md)
- **Slack message** — Concise narrative prose (~150 words), no bullets, links at bottom
- **Skip** — No synthesis needed, KB docs are sufficient

The synthesis draws from the digest + learning notes + user's personal reframings — not the raw source. The user's voice and analytical angle are the value-add over the original article.

**Key principle**: The user owns their voice. Present drafts, but expect the user to rewrite key passages (especially openings). Polish what they give you — don't ghostwrite.

Save synthesis outputs to the session docs folder:
- `docs/polished-blog-YYYYMMDD/` — original draft, polished version, changelog, feedback
- `docs/polished-slack-YYYYMMDD/` — same structure for Slack

---

## Step 6: INTEGRATE

After creating/updating documents:

1. **Regenerate index** (so new docs appear in the unified catalog):
```bash
source skills/common/generate_index.sh
generate_index "$KB_PATH"
```

2. **Append operation log** (audit trail for KB changes):
```bash
source skills/common/obsidian_helpers.sh
append_kb_log "$KB_PATH" "ingest" "kb-ingest" "Ingested [source]. Created: [docs]. Updated: [docs]"
```

3. **Verify** created documents:
```bash
./skills/session-recap/scripts/count_wikilinks.sh document.md 5
./skills/session-recap/scripts/validate_obsidian_syntax.sh document.md
```

---

## Batch Ingest

For multiple sources: "Ingest all .md files in /path/to/folder/"

- READ all sources first
- ENGAGE as a batch — present combined takeaways, let user prioritize
- CREATE docs per source (or merged if topics overlap)
- INTEGRATE once at the end

---

## Resources

- [KB Schema](_meta/schema.md) — Unified conventions for all KB documents
- [Ingest Guide](references/ingest-guide.md) — Source types, classification, quality standards
- [Study Mode Guide](references/study-mode-guide.md) — Theme walkthrough example, explore depth guidance, capturing user notes
- [Blog Synthesis Guide](references/blog-synthesis-guide.md) — How to create blog posts from studied material
- [Distillation Guide](../session-recap/references/distillation-guide.md) — For large sources

---

## Completion Criteria

| Mode | Complete when |
|------|---------------|
| **Quick** | KB doc(s) created with frontmatter and 5-8 WikiLinks, index regenerated, log appended |
| **Study** | Source copy + digest + learning notes + concept docs created, index regenerated, log appended |
| **Study + Synthesis** | All of Study, plus polished blog/slack output in session docs |
