---
name: consume-feed
description: >
  Manage and run nightly ingestion of upstream feeds (RSS).
  GitHub and NVD support coming in Phase 2.
  Fetch updates, store summaries in ArangoDB, and integrate with Memory.
  Use this skill to "check for updates" or "add a new source" to the knowledge graph.
triggers:
  - pull the feeds
  - run feed ingest
  - check upstream updates
  - fetch nightly updates
  - add rss feed
  - check feed ingest health
metadata:
  short-description: Ingest RSS feeds into Memory
---

# Consume Feed Skill

A robust ingestion engine for upstream data sources.

## Phase 1: RSS (Implemented)

- "Pull the feeds now" -> `./run.sh run --mode manual`
- "Add this RSS feed <url>" -> `./run.sh sources add rss --url <url>`
- "Check feed ingest health" -> `./run.sh doctor`

## Phase 2: GitHub & NVD (Aspirational)

- "Add GitHub repo <owner>/<repo>" -> `sources add github --repo <owner>/<repo>`
- "Track NVD for <keyword>" -> `sources add nvd --query <keyword>`

## Usage

### Run Ingestion

```bash
# Run nightly crawl (all sources, respect intervals)
./run.sh run --mode nightly

# Run specific source immediately
./run.sh run --source <key>
```

### Manage Sources

```bash
# List all
./run.sh sources list

# Add RSS
./run.sh sources add rss --url "https://github.blog/feed/"
```

### Diagnosis & Initialization

```bash
# Health check
./run.sh doctor

# Force initialize search views and indexes
./run.sh doctor --init
```

## Resilience

- Uses **exponential backoff** and **jitter** for all network requests.
- Persists **checkpoints** (ETags, Timestamps) to resume efficiently.
- Reuses **Memory skill connection** for stable, shared database access.
