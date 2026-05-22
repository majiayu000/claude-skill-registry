---
name: qdrant
description: "Qdrant vector database: collections, points, payload filtering, indexing, quantization, snapshots, and Docker/Kubernetes deployment."
version: "1.16.3"
release_date: "2025-12-19"
---

# Qdrant (Skill Router)

This file is intentionally **introductory**.

It acts as a **router**: based on your situation, open the right note under `references/`.

## Start here (fast)

- New to Qdrant? Read: `references/concepts.md`.
- Want the fastest local validation? Read: `references/quickstart.md` + `references/deployment.md`.
- Integrating with Python? Read: `references/api-clients.md`.

## Choose by situation

### Data modeling

- What should go into vectors vs payload vs your main DB? Read: `references/modeling.md`.
- Working with IDs, upserts, and write semantics? Read: `references/points.md`.
- Need to understand payload types and update modes? Read: `references/payload.md`.

### Retrieval (search)

- One consolidated entry point (search + filtering + explore + hybrid): `references/retrieval.md`.

### Performance & indexing

- Index types and tradeoffs: `references/indexing.md`.
- Storage/optimizer internals that matter operationally: `references/storage.md` + `references/optimizer.md`.
- Practical tuning, monitoring, troubleshooting: `references/ops-checklist.md`.

### Deployment & ops

- Installation/Docker/Kubernetes: `references/deployment.md`.
- Configuration layering: `references/configuration.md`.
- Security/auth/TLS boundary: `references/security.md`.
- Backup/restore: `references/snapshots.md`.

### API interface choice

- REST vs gRPC, Python SDK: `references/api-clients.md`.

## How to maintain this skill

- Keep `SKILL.md` short (router + usage guidance).
- Put details into `references/*.md`.
- Merge or reorganize references when it improves discoverability.

## Critical prohibitions

- Do not ingest/quote large verbatim chunks of vendor docs; summarize in your own words.
- Do not invent defaults not explicitly grounded in documentation; record uncertainties as TODOs.
- Do not design backup/restore without testing a restore path.
- Do not use NFS as the primary persistence backend (installation docs explicitly warn against it).
- Do not expose internal cluster communication ports publicly; rely on private networking.
- Do not use API keys/JWT over untrusted networks without TLS.
- Do not rely on implicit runtime defaults for production; record effective configuration.

## Links

- Concepts: https://qdrant.tech/documentation/concepts/
- Installation: https://qdrant.tech/documentation/guides/installation/
