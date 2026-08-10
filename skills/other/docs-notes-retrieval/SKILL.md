---
name: docs-notes-retrieval
description: "Builds local-first note vault retrieval for Obsidian, markdown notebooks, and NotebookLM-adjacent exports. Use when packaging notes into LLM-ready context."
compatibility: Portable core. Works on Claude Code and Codex.
version: "1.1"
last_validated: 2026-07-11
---

# Notes Retrieval

## Quick Start — Concrete Commands

Three common scenarios using the scripts in `scripts/`.

### Scenario 1: Vault inventory

Before indexing or packaging, understand what is in the vault.

```bash
# Full inventory as JSON — one record per note with title, frontmatter, wikilinks, tags, word count, mtime
python scripts/scan_vault.py inventory /path/to/vault > vault-inventory.json

# Tag summary sorted by note count
python scripts/scan_vault.py tags /path/to/vault

# CSV for spreadsheet review
python scripts/scan_vault.py inventory /path/to/vault --format csv > vault-inventory.csv
```

### Scenario 2: Packaged context for an LLM session

Build a markdown bundle ready to paste into a Claude or GPT session.

```bash
# Keyword search — include all notes matching "weekly review", budget 40k chars
python scripts/build_context_pack.py /path/to/vault \
    --query "weekly review" \
    --max-chars 40000 > context-pack.md

# Specific notes with heading-level chunking
python scripts/build_context_pack.py /path/to/vault \
    --notes "Projects/Alpha.md" "Projects/Beta.md" \
    --chunk-strategy heading \
    --max-chars 60000 > project-alpha-pack.md

# Most recent notes first, paragraph chunking, written to file
python scripts/build_context_pack.py /path/to/vault \
    --query "architecture decision" \
    --order-by recency \
    --chunk-strategy paragraph \
    --out session-context.md
```

### Scenario 3: Orphan note cleanup

Find and review notes with no inbound or outbound wikilinks — usually stale or misplaced.

```bash
# List orphans as JSON
python scripts/scan_vault.py orphans /path/to/vault

# Pipe into jq to see just paths and word counts
python scripts/scan_vault.py orphans /path/to/vault | jq '.[] | {path, word_count}'

# CSV for manual triage
python scripts/scan_vault.py orphans /path/to/vault --format csv > orphans.csv
```

Orphan cleanup workflow:
1. Run `orphans` to get the list.
2. Review word count: orphans < 50 words are likely stubs — archive or delete.
3. Orphans > 200 words with no links may be valuable but unconnected — add wikilinks or a backlink from a map-of-content note.
4. Re-run `orphans` after cleanup to verify the count dropped.

Judgment call before acting on the list: `scan_vault.py orphans` only detects `[[wikilink]]` topology. In vaults that organize by folder hierarchy or tags instead of wikilinks (common in Logseq-style or PARA-folder vaults), a genuinely well-connected note can show up as a false-positive orphan. Cross-check folder placement and tags before archiving anything the tool flags — treat the orphan list as a triage queue, not a deletion list.

---

Use this skill to build or operate local-first retrieval pipelines for note vaults, markdown knowledge bases, and notebook-style exports.

This skill covers:

- Obsidian-style markdown vaults with frontmatter, wikilinks, tags, and aliases
- Local notebook exports and source packs prepared for NotebookLM-style workflows
- Raw ingest folders such as transcript exports that feed a canonical note system
- Read-only extraction of note text, metadata, backlinks, and neighborhood context
- Packaging note sets into Markdown or retrieval-ready context for LLMs, agents, and MCP tools
- Optional write-back routing of summaries, actions, and decisions into canonical notes when the user explicitly wants synchronized notes

## Quick Reference

| Need | Default path | Notes |
|------|--------------|-------|
| Inspect a vault before indexing | `references/obsidian-and-local-vaults.md` | Inventory note types, frontmatter conventions, attachments, and private areas first |
| Run vault inventory from the CLI | `scripts/scan_vault.py inventory` | Extracts path, title, frontmatter, wikilinks, tags, word count, mtime |
| Find orphan notes (no links) | `scripts/scan_vault.py orphans` | Returns notes with no inbound or outbound wikilinks |
| List all tags with counts | `scripts/scan_vault.py tags` | Sorted by note count descending |
| Package notes for LLM context | `scripts/build_context_pack.py` + `references/context-packaging-patterns.md` | Keyword or explicit-note selection; whole/heading/paragraph chunking; char budget |
| Understand chunk strategies and token budgets | `references/context-packaging-patterns.md` | Char→token ratios, ordering, deduplication, attribution format |
| Avoid retrieval mistakes | `references/retrieval-anti-patterns.md` | 8 anti-patterns with fixes |
| Structure a vault as durable agent memory | `references/obsidian-and-local-vaults.md` | Separate session memory, canonical notes, and ingest artifacts instead of one flat note dump |
| Turn a vault into an operating memory loop | `references/obsidian-and-local-vaults.md` | Keep notes canonical and treat transcripts or exports as ingest inputs |
| Use AI-owned wiki (solo, high-volume capture) | `references/ai-curated-wiki-pattern.md` | Folder layout, invariants, compounding loop, scale heuristic, snapshots |
| Decide note-vault retrieval vs generic RAG | `../ai-rag/SKILL.md` + this skill | Use this skill for note-shape and packaging rules; use `ai-rag` for retrieval architecture |
| Turn note access into a repeatable tool | `../agents-mcp/SKILL.md` | Build an MCP wrapper only after the local note workflow is clear |

## Supported Inputs

Default support in v1:

- markdown note vaults
- Obsidian frontmatter and wikilinks
- folder-based personal or team knowledge bases
- NotebookLM-adjacent exported note packs, summaries, and source bundles
- transcript or export folders that are later summarized into canonical notes
- read-only local file trees prepared for agent retrieval

Explicitly out of scope in v1:

- direct NotebookLM API automation
- mutating or auto-rewriting the source vault by default
- OCR-heavy attachment pipelines
- closed-source vendor note apps without an export path

## Three-Layer Operating Memory Pattern

For agent workflows, separate these three layers — collapsing them into one pool is the most common vault anti-pattern:

| Layer | Role | Examples |
|-------|------|---------|
| Session memory | Orients the agent; always loaded, tiny | Onboarding notes, repo CLAUDE.md, orientation files |
| Knowledge graph | Persists and connects knowledge | Canonical notes with frontmatter, wikilinks, stable destinations |
| Ingest pipeline | Evidence and raw material | Transcripts, exports, recordings, raw captures |

## AI-Curated Wiki Variant (Ganim Pattern)

The three-layer default assumes humans curate the canonical layer. A second mode exists where the AI owns the curated layer entirely and the human only appends to a junk-drawer source folder. Use this variant for solo operators capturing source material faster than they can hand-organize it.

Full details, invariants, compounding loop, monthly health check, scale heuristic (~100 articles / ~400K words before vector RAG is needed), image-aware ingest, and snapshot strategy: [`references/ai-curated-wiki-pattern.md`](references/ai-curated-wiki-pattern.md).

## ASCII Flow

```text
Notes request
  |
  v
Classify source shape
  |-- Obsidian vault
  |-- markdown folder
  |-- notebook export
  |-- transcript / raw ingest dump
  |-- mixed notes repo
  |
  v
Separate layers
  |-- session memory -----> tiny always-loaded orientation
  |-- canonical notes ----> durable graph with metadata + links
  |-- raw ingest ---------> transcripts, exports, recordings
  |
  v
Inventory metadata + topology
  |-- frontmatter
  |-- wikilinks / backlinks
  |-- tags / aliases
  |-- private folders / attachments
  |
  v
Choose output
  |-- Markdown context pack ----> scripts/build_context_pack.py
  |-- vault report -------------> scripts/scan_vault.py
  |-- retrieval architecture ---> ai-rag
  |-- repeatable tool ----------> agents-mcp
  |
  v
Package with stable attribution and budget limits
```

## Default Workflow

1. Identify the source shape: Obsidian vault, markdown folder, notebook export, transcript dump, or mixed notes repo.
2. Separate canonical notes from raw ingest areas before indexing or packaging.
3. Inventory note conventions before indexing: frontmatter keys, aliases, tags, task syntax, attachments, private folders.
4. Extract note text and metadata separately.
5. Preserve note relationships: wikilinks, backlinks, tags, path hierarchy, and recent edits.
6. If external transcripts or exports feed the vault, route extracted summaries, decisions, and actions into stable note destinations instead of treating raw dumps as the memory layer.
7. Only then choose whether the downstream consumer needs direct Markdown bundles, a search index, or an MCP server.

## Packaging Rules

| Rule | Why it matters |
|------|---------------|
| A note ≠ a chunk — preserve whole-note metadata even when chunking | Path, title, aliases, timestamps are retrieval signals |
| Keep canonical notes and raw ingest artifacts separate | A transcript dump is not the operating note system |
| Prefer note titles that read like claims or decisions | Helps an agent triage relevance before opening the file |
| Use maps-of-content / home notes for navigation | Semantic search alone cannot recover the right abstraction level |
| Separate private, shared, and project-specific spaces before retrieval | Prevents accidental cross-space leakage |
| Default to local-first, read-only flows | Only add write-back when the user explicitly needs it |
| If notes are one corpus among many, route to [ai-rag](../ai-rag/SKILL.md) | This skill covers note-shape; ai-rag covers retrieval architecture |

## Judgment Calls

These are the calls a non-expert tends to get wrong. Full detail and the anti-pattern behind each is in `references/retrieval-anti-patterns.md`.

- **Full-text/grep beats semantic search for most personal vaults.** Notes are small, high-lexical-overlap, and often need exact-phrase or exact-title recall (a decision title, a project name, a specific date). Reach for embeddings only once keyword/tag/path search demonstrably under-recalls — typically past a few hundred notes, or when queries are conceptual ("what did I conclude about X") rather than lexical. Below that, a vector index adds latency and infra without improving grounding.
- **Citation integrity is non-negotiable.** Never let a downstream agent cite a note without a resolvable `path` + `mtime`. If a wikilink target does not resolve to an actual file, that is a stop-and-fix signal — flag it in the pack footer, do not silently drop it or silently invent a path.
- **An orphan is a triage signal, not a verdict.** See the vault-hygiene note in Scenario 3 above — orphan detection is topology-specific (wikilinks only) and produces false positives in folder- or tag-organized vaults.
- **Status metadata beats recency for trust, not just freshness.** A note edited yesterday but marked `status: draft` is less trustworthy than a `status: active` note from three months ago. Filter on status before recency, not instead of it.

## When To Use This Skill

Use this skill when the user asks:

- "Search my Obsidian vault."
- "Prepare my notes for an LLM."
- "Package markdown notebooks into retrieval-ready context."
- "How should I structure note metadata, links, and summaries for AI?"
- "I want Claude to keep my Obsidian vault up to date from transcripts or exports."
- "I have NotebookLM-style exports or source packs and want a reusable local workflow."

## Navigation

**Scripts**
- [scripts/scan_vault.py](scripts/scan_vault.py) - vault scanner: inventory, tags, orphans subcommands; JSON/CSV output
- [scripts/build_context_pack.py](scripts/build_context_pack.py) - context pack builder: keyword/path selection, chunk strategies, char budget

**References**
- [references/obsidian-and-local-vaults.md](references/obsidian-and-local-vaults.md) - vault conventions, metadata, and safe inventory rules
- [references/context-packaging-patterns.md](references/context-packaging-patterns.md) - chunk strategies, token budgets, ordering, deduplication, attribution
- [references/retrieval-anti-patterns.md](references/retrieval-anti-patterns.md) - 8 anti-patterns with fixes (blind chunking, ignoring topology, draft notes, etc.)
- [references/ai-curated-wiki-pattern.md](references/ai-curated-wiki-pattern.md) - AI-owned wiki variant: folder layout, invariants, compounding loop, scale heuristic, snapshots
- [data/sources.json](data/sources.json) - official and community sources for note-vault retrieval patterns

**Related Skills**
- [../ai-rag/SKILL.md](../ai-rag/SKILL.md) - retrieval architecture, ranking, and evaluation
- [../agents-mcp/SKILL.md](../agents-mcp/SKILL.md) - MCP wrappers for repeated note retrieval workflows
- [../agents-memory/SKILL.md](../agents-memory/SKILL.md) - repo-native memory and long-lived agent context

## Fact-Checking

- Start from `data/sources.json` for source-app behavior and community patterns.
- Verify current vendor export paths and app capabilities before citing volatile details.
- If web access is unavailable, mark product-specific claims as unverified.

## Learnings Loop

Before applying this skill on a non-trivial task, read `learnings.consolidated.md` in this directory (and `learnings.md` if present).

After applying it, if you encountered a pattern worth remembering, a mistake worth preventing, or a domain fact that surprised you, append one dated bullet to `learnings.md` via `agents-skills-feedback-loop/scripts/append_learning.py`. Do not modify `SKILL.md` itself.

