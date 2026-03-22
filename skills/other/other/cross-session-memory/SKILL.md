<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
---
name: cross-session-memory
description: >-
  Cross-session persistent memory for security engagements. Provides tri-layer
  indexing (semantic embeddings + BM25 keywords + structured metadata) with
  reciprocal rank fusion retrieval. Stores findings, IOCs, TTPs, credentials,
  host info, and analyst decisions. Supports memory decay, consolidation, and
  engagement-scoped context loading.
domain: cybersecurity
subdomain: memory-system
tags:
  - memory
  - persistence
  - tri-layer-indexing
  - semantic-search
  - engagement-context
  - ioc-management
  - knowledge-base
version: "1.0"
author: defconxt
license: AGPL-3.0
compatibility: Designed for Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI, and any agentskills.io-compatible agent.
metadata:
  frameworks: ["SimpleMem tri-layer", "ProjectDiscovery Neo persistent memory"]
---

# Cross-Session Memory

## When to Use

Activate when the operator needs persistent memory across sessions — loading
previous engagement context, searching past findings, managing IOC collections,
or building cumulative security knowledge. The memory system automatically
indexes entries across semantic, lexical, and symbolic layers.

## Architecture

```
Query: "SQL injection on login endpoint"
         │
         ├─── Semantic Layer (LanceDB)
         │    Dense embedding similarity → finds conceptually related entries
         │
         ├─── Lexical Layer (SQLite FTS5)
         │    BM25 keyword matching → finds exact term matches
         │
         └─── Symbolic Layer (SQLite)
              Structured metadata → filters by engagement, severity, type
         │
         ▼
    Reciprocal Rank Fusion (RRF)
    Fuse ranked lists → unified result ranking
```

## Memory Types

| Type | Content | Example |
|------|---------|---------|
| `finding` | Vulnerability or security issue | "SQLi on /api/login allows auth bypass" |
| `ioc` | Indicator of compromise | "C2 domain: evil.example.com" |
| `ttp` | Tactic, technique, procedure | "T1558.003 Kerberoasting via GetUserSPNs" |
| `credential` | Credential reference (hashed) | "Found default admin creds on Jenkins" |
| `host` | Asset information | "10.0.0.5 runs Apache 2.4.49 (CVE-2021-41773)" |
| `network` | Topology or flow data | "DMZ segment 10.0.1.0/24 → internal via port 8443" |
| `config` | Configuration or policy | "S3 bucket public ACL on customer-data bucket" |
| `note` | Analyst observation | "Client uses Okta SSO, MFA only for admins" |
| `decision` | Engagement decision | "Decided to pivot to AD attack path after web assessment" |
| `artifact` | Evidence reference | "Memory dump stored at /evidence/host01_mem.lime SHA256:abc..." |

## Usage

```python
from memory.core.engine import CipherMemory, MemoryEntry, MemoryType

memory = CipherMemory()

# Store a finding
memory.store(MemoryEntry(
    content="SQL injection on /api/v2/login POST parameter 'username' allows authentication bypass and database access",
    memory_type=MemoryType.FINDING,
    engagement_id="pentest-2026-acme",
    source_skill="web-application-attacks",
    targets=["https://acme.com/api/v2/login"],
    mitre_attack=["T1190"],
    cve_ids=[],
    severity="critical",
    keywords=["sqli", "authentication", "bypass", "login"],
    tags=["web", "api", "owasp-a03"],
))

# Search across all layers
results = memory.search("authentication bypass vulnerabilities")

# Search with filters
results = memory.search(
    query="credential access",
    engagement_id="pentest-2026-acme",
    severity="critical",
)

# Load full engagement context
context = memory.get_engagement_context("pentest-2026-acme")

# Maintenance
memory.consolidate()  # Decay, archive stale entries
print(memory.stats())
memory.close()
```

## Retrieval Pipeline

1. **Query** received (natural language or structured)
2. **Semantic search** — embed query, find nearest vectors in LanceDB
3. **Lexical search** — BM25 match in SQLite FTS5
4. **Symbolic search** — filter by engagement, type, severity, MITRE technique
5. **Reciprocal Rank Fusion** — fuse three ranked lists: `RRF(d) = Σ 1/(k + rank_i(d))`
6. **Boost on access** — accessed entries get decay score boost
7. **Return** — unified ranked list of MemoryEntry objects

## Memory Lifecycle

```
Store → Index (3 layers) → Search → Access (boost) → Decay → Archive/Prune

Consolidation (periodic):
├── Decay: multiply all scores by 0.98
├── Boost: accessed entries get +0.05
├── Archive: entries with score < 0.05 archived
└── Merge: duplicate IOCs/findings deduplicated (future)
```

## Verification

- [ ] Memory engine initializes without errors
- [ ] Entries stored and retrievable across all three layers
- [ ] RRF fusion returns results from multiple layers
- [ ] Engagement-scoped queries filter correctly
- [ ] Decay and consolidation maintain memory hygiene
- [ ] Archived entries excluded from search results
