---
name: prompt
description: "Capture each prompt into Graphiti memory (episodes) for this repo/user."
---

## Purpose
Store every prompt (and optional role/kind) as a memory episode in Graphiti MCP, so agents can recall recent context.

## Triggers
- "load prompt", "capture prompt", or any per-prompt hook integration
- Use when you want every prompt stored automatically.

## Usage
- `lisa-prompt add --text "..." [--role user|assistant] [--kind Direction|Decision|Requirement|Observation] [--force]`
- By default uses `GRAPHITI_ENDPOINT` from `.lisa/.env`. Group ID is automatically derived from the project folder path. Falls back to `http://localhost:8010/mcp/`.

## Notes
- Adds a fingerprint tag to avoid duplicate prompts unless `--force` is passed.
- Output: JSON with status/action.
