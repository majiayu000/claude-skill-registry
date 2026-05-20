---
name: edge-verifier
description: >
  Verifies relationships between a source text (e.g. Episode, Task) and existing Knowledge Graph lessons.
  Runs KNN/Hybrid search to find candidates, then uses LLM (scillm) to verify "verifies", "contradicts",
  or "related" stances with strict rationales.
allowed-tools: Bash
triggers:
  - verify edges
  - link content
  - generate relationships
  - schedule verification
metadata:
  short-description: KNN + LLM verification for KG edges
provides:
  - edge-verification
composes:
  - scillm
  - task-monitor

taxonomy:
  - validation
  - knowledge
  - precision
---

# Edge Verifier

This skill links new content to the existing Knowledge Graph by:

1.  **Recall**: Running a KNN/Hybrid search (`graph_memory.search`) to find potential related lessons.
2.  **Verify**: Using `scillm` (LLM) to audit the relationship, classifying it as `verifies`, `contradicts`, or `neutral`.
3.  **Link**: Creating verified `lesson_edges` in ArangoDB.

## Usage

### Manual Execution

```bash
# Verify edges for a specific source text
.pi/skills/edge-verifier/run.sh --source_id <ID> --text "Content to verify..."

# With explicit options
.pi/skills/edge-verifier/run.sh --source_id <ID> --text "..." --type "episode_turn"
```

## Scheduling (Scheduler Integration)

This skill is designed to be scheduled via the `/scheduler` skill for continuous verification of new memory artifacts.

### Register with Scheduler

```bash
.pi/skills/scheduler/run.sh register \
  --name "edge-verify-nightly" \
  --cron "0 2 * * *" \
  --command ".pi/skills/edge-verifier/run.sh --batch" \
  --description "Nightly edge verification"
```

Jobs and logs are stored under `~/.pi/scheduler/`. See `.pi/skills/scheduler/SKILL.md` for full options.

## Prerequisites

- `.env` must expose ArangoDB credentials.
- `CHUTES_API_KEY` for LLM calls.
