---
name: edge-verifier
description: >
  Verifies relationships between a source text (e.g. Episode, Task) and existing Knowledge Graph lessons.
  Runs KNN/Hybrid search to find candidates, then uses LLM (scillm) to verify "verifies", "contradicts",
  or "related" stances with strict rationales.
allowed-tools: Bash, Mom
triggers:
  - verify edges
  - link content
  - generate relationships
  - schedule verification
metadata:
  short-description: KNN + LLM verification for KG edges
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
.agents/skills/edge-verifier/run.sh --source_id <ID> --text "Content to verify..."

# With explicit options
.agents/skills/edge-verifier/run.sh --source_id <ID> --text "..." --type "episode_turn"
```

## Scheduling (Mom Integration)

This skill is designed to be scheduled via **mom (Master Of Mischief)** to ensure continuous verification of new memory artifacts.

To schedule this, copy the provided `schedule_template.json` to mom's `events` directory (e.g., `data/events/`).

### Template (`schedule_template.json`)

```json
{
  "type": "periodic",
  "channelId": "YOUR_CHANNEL_ID",
  "text": "Run .agents/skills/edge-verifier/run.sh on recent data",
  "schedule": "0 2 * * *",
  "timezone": "America/New_York"
}
```

### Setup Steps for Mom

1.  **Link Skill**: Ensure `mom` can see this skill.
    ```bash
    ln -s $(pwd)/.agents/skills/edge-verifier ~/.pi/mom/data/skills/edge-verifier
    ```
2.  **Schedule**: Copy the template.
    ```bash
    cp .agents/skills/edge-verifier/schedule_template.json ~/.pi/mom/data/events/verify-daily.json
    # Edit the channelId in the new file!
    ```

## Prerequisites

- `.env` must expose ArangoDB credentials.
- `CHUTES_API_KEY` for LLM calls.
