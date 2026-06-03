---
name: palace-index-curator
description: Curate the web-capture index. Use when the capture backlog grows, captures sit unprocessed at seedling/pending, or to surface stored research during work.
alwaysApply: false
category: governance
tags:
- knowledge-management
- capture-index
- curation
- promotion
- analytics
dependencies:
- memory_palace.corpus.index_analytics
- memory_palace.corpus.index_promoter
---

# Palace Index Curator

## Overview

The web-research hooks auto-capture every WebFetch and WebSearch into
`hooks/memory-palace-index.yaml`, storing each as a markdown file and an
index entry. Captures land at the defaults `routing_type: pending`,
`maturity: seedling`, `importance_score: 50`, and nothing advances them.
Left alone, the index becomes a write-only graveyard: the majority of
entries are never incorporated, analyzed, or surfaced.

This skill drains that backlog and keeps it drained. It wires the
capture index to the corpus tooling the plugin already ships
(`decay_model`, `keyword_index`, `marginal_value`) through three
commands: a read-only report, a dry-run-first promotion engine, and a
SessionStart surfacing hook.

## When to Use

- The capture backlog has grown and most entries are still `pending`.
- You want a corpus health report (inert ratio, orphans, topic clusters).
- You want stored research surfaced automatically during sessions.

## When NOT to Use

- Ingesting a single new resource: use `knowledge-intake`.
- Searching stored knowledge ad hoc: use `knowledge-locator`.
- Tending a digital garden file: use `digital-garden-cultivator`.

## Workflow

### 1. Analyze (read-only)

```bash
uv run python scripts/memory_palace_cli.py index report
```

Reports total entries, the inert ratio, orphaned captures (entries whose
backing file is gone), the largest topic clusters by domain, and the
top promotion candidates. Writes nothing.

### 2. Incorporate (dry-run, then apply)

```bash
# Dry run: prints promote/archive proposals, writes nothing.
uv run python scripts/memory_palace_cli.py index promote

# Apply: backs up the index under data/backups/, then persists.
uv run python scripts/memory_palace_cli.py index promote --apply
```

Each `pending` entry is classified into one action:

- **promote**: recent, authoritative, or clustered. Gets a real
  importance score, a routing type, and maturity `seedling -> growing`.
- **archive**: orphaned or older than the archive horizon and never
  revisited. Marked `archived` rather than promoted, following the
  principle that unused captures should drain, not accumulate.
- **hold**: everything else stays `pending` with no change.

Applying is idempotent: promoted and archived entries are no longer
`pending`, so a second run proposes nothing new. The dry-run diff is
always shown before `--apply` writes.

### 3. Surface (learn)

A SessionStart hook (`hooks/index_surfacer.py`) names the highest-value
promoted captures at the start of a session. It is disabled by default.
Enable it in `memory-palace-config.yaml`:

```yaml
feature_flags:
  context_injection: true
```

The hook only speaks when promoted entries clear the importance floor,
and it exits silently on any error so it can never block a session.

## Design Notes

- Promotion uses only structural signals (recency, domain authority,
  cluster size). The decision logic is deterministic; no model call
  gates a transition.
- The decay half-lives (14/30/90 days) are tunable priors, not retention
  constants. Wixted & Ebbesen (1997) and Murre & Dros (2015) show
  forgetting follows a power law; FSRS (Ye, Su & Cao, 2022) validates
  exponential decay only with a learned per-item half-life. Calibrate
  against reopen logs if usage data accrues.
- Retrieval stays keyword-first (`cache_lookup` / `keyword_index`);
  embeddings are not required at the current corpus scale. BM25 is the
  workhorse up to ~5000 documents; embeddings add value only for
  vocabulary-mismatch discovery.
- Near-duplicate detection layers SHA-256 exact match (present via
  `content_hash`) then MinHash with k-shingling for near-duplicates
  (Broder, 1997). SimHash is preferable only at tens of thousands of
  documents.
- Importance formula: `relevance = w1 * centrality + w2 * decay(t) +
  w3 * usage`. The plugin ships all three terms (`graph_analyzer`
  PageRank, `decay_model`, `usage_tracker`).

## Exit Criteria

- [ ] `index report` runs and prints the inert ratio and orphan count
      for the live index.
- [ ] `index promote` (no flag) prints proposals and writes nothing
      (the index file is byte-identical afterward).
- [ ] `index promote --apply` creates a timestamped backup under
      `data/backups/` before persisting, and a re-run proposes nothing.
- [ ] With `context_injection: true`, a SessionStart event surfaces the
      top promoted captures; with the flag off, it stays silent.
- [ ] Failure modes (missing index, corrupt YAML, missing backing files)
      are handled without raising: report degrades, promote holds, hook
      exits silently.
