---
name: kb-ingest
description: Ingest external sources (articles, gists, docs, URLs) into the knowledge bank through interactive discussion. Follows the LLM Wiki pattern — READ source, DISCUSS key takeaways with user, CREATE wiki pages, INTEGRATE into existing knowledge. Triggers on "ingest this", "add to knowledge bank", "process this article", or when user provides external reference material for long-term retention.
user-invocable: true
---

# Knowledge Bank Ingest

Ingest external knowledge sources into the knowledge bank through an interactive workflow. Unlike session-recap (which extracts from Claude Code sessions), this skill handles standalone sources — articles, gists, design docs, PDFs, URLs, or any knowledge-bearing document.

**Knowledge Bank Location**: Read from `~/.claude/plugins/config/second-brain/config.json`. Configure via `skills/common/setup_kb_path.sh --configure`.

**Philosophy**: A single source can touch multiple KB pages. The discussion between you and the user shapes what gets preserved — this is not a summarizer, it's a collaborative knowledge integration tool.

---

## Invocation

### Manual
- **Slash command**: `/second-brain:kb-ingest`
- **Skill tool**: `Skill({ skill: "second-brain:kb-ingest" })`

### Natural Language Triggers
- "Ingest this article into the knowledge bank"
- "Add this to the KB"
- "Process this document for the knowledge bank"
- "I want to save the key insights from this"

### Arguments
Provide a source path, URL, or indicate inline content:
```
/second-brain:kb-ingest /path/to/article.md
/second-brain:kb-ingest https://example.com/interesting-post
```

---

## Workflow

### Step 1: READ

Read the source document:
- **File path**: Use Read tool directly
- **URL**: Use WebFetch to retrieve content
- **Inline text**: Accept content pasted by the user

For large sources (>100KB), apply the [distillation guide](../session-recap/references/distillation-guide.md) — extract essentials, target 95% size reduction.

Identify:
- Key concepts, patterns, and principles
- Actionable techniques or methodologies
- Connections to existing KB knowledge

### Step 2: DISCUSS

Present key takeaways to the user and engage in interactive discussion:

1. **Summarize** the source's main contributions (3-5 bullet points)
2. **Propose** what's worth preserving and as what type:
   - Concept doc — if the source reveals an architectural pattern or principle
   - Component doc — if it describes a specific system or tool
   - Best practice doc — if it documents a reusable methodology
   - Multiple docs — if the source covers several distinct topics
3. **Ask** the user:
   - What resonates most? What should be emphasized?
   - What's the project context? (determines KB placement under `projects/{project}/`)
   - Anything to add from their own experience?

The discussion itself generates insights beyond the raw source. Capture these.

**Example:**
```
Source: Article on event sourcing patterns
Summarize: "3 key takeaways: (1) events as source of truth, (2) projection 
  rebuilds from event stream, (3) snapshot optimization for large streams"
Propose: "This maps to a concept doc — fits under projects/cc/concepts/ 
  since it's an architectural pattern we could apply to session management"
Ask: "Does this connect to any patterns you've seen in your codebase? 
  Should we emphasize the snapshot optimization angle?"
```

### Step 3: CREATE

Generate KB document(s) incorporating both the source content AND discussion insights.

**Templates**: Use existing templates from `session-recap/references/`:
- [concept-template.md](../session-recap/references/concept-template.md)
- [component-template.md](../session-recap/references/component-template.md)
- [best-practice-template.md](../session-recap/references/best-practice-template.md)

**Cross-references**: Run cross-reference discovery:
```bash
./skills/session-recap/scripts/search_cross_references.sh "keyword" [project]
```
Target 5-8 WikiLinks (lower than session-recap's 10-15 since standalone ingests have less cross-referencing context).

**Frontmatter** (MUST include):
```yaml
---
title: Document Title
aliases: [Alt 1, Alt 2]
tags: [category, topic]
type: concept|component|best-practice
created: YYYY-MM-DD
modified: YYYY-MM-DD
project: {project}
source-type: article|document|url|gist
ingested-from: /path/to/source.md or https://url
---
```

**Obsidian Syntax**: When obsidian skills are available, MUST invoke `/obsidian:obsidian-markdown` before creating documents.

**Updating existing docs**: If the new knowledge connects to or supersedes existing KB pages, update them too — add cross-references, revise outdated claims, note where new data strengthens or challenges existing content. This follows the LLM Wiki principle that a single ingest can touch multiple pages.

### Step 4: INTEGRATE

After creating/updating documents:

1. **Regenerate index**:
```bash
source skills/common/generate_index.sh
generate_index "$KB_PATH"
```

2. **Append operation log**:
```bash
source skills/common/obsidian_helpers.sh
append_kb_log "$KB_PATH" "ingest" "kb-ingest" "Ingested [source name]. Created: [docs]. Updated: [docs]"
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
- DISCUSS as a batch — present combined takeaways, let user prioritize
- CREATE docs per source (or merged if topics overlap)
- INTEGRATE once at the end

---

## Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| Interactive DISCUSS step | User's context and emphasis shape what gets preserved — not a blind summarizer |
| 5-8 WikiLinks (not 10-15) | Standalone ingests have less cross-referencing context than full session recaps |
| Reuse session-recap templates | No duplication — one set of templates for all KB documents |
| No daily log | Daily logs are session-recap's responsibility |
| No reflection gate | Reflections come from *doing* work, not reading about it |
| Can update existing pages | LLM Wiki principle — a single source can touch multiple wiki pages |

---

## Resources

- [KB Schema](_meta/schema.md) — Unified conventions for all KB documents
- [Ingest Guide](references/ingest-guide.md) — Source types, classification, and quality standards
- [Distillation Guide](../session-recap/references/distillation-guide.md) — For large sources

---

## Completion Criteria

Ingest is complete when:

1. Source has been read and discussed with user
2. KB document(s) created with valid frontmatter and 5-8 WikiLinks
3. Obsidian syntax validation passes
4. `_meta/index.md` regenerated
5. `_meta/log.md` entry appended
