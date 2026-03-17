---
name: memory
description: "Permanent memory using Lisa."
---

## Purpose
Reusable memory helper that routes remember/recall requests to Graphiti MCP while staying model-neutral and providing cache fallback. **Always summarizes results into human-readable format.**

## Triggers
Use when the user says things like: "load memory", "recall notes", "remember", "pull saved context", "fetch past tasks".

## How to use
1) For recall: run `lisa memory load --cache [--query <q>] [--limit 10] [--group <id>]`. Reads Graphiti facts and prints JSON. Uses cache if MCP is down.
2) For remember: run `lisa memory add "<text>" --cache [--group <id>] [--tag foo] [--source <src>]` to append an episode.
3) Endpoint: reads ${GRAPHITI_ENDPOINT} from `.lisa/.env` (written by init); group ID is automatically derived from the project folder path. See root `AGENTS.md` for canonical defaults.
4) Cache fallback: stored at `cache/memory.log` inside this skill. On failure, last cached result is returned with `status: "fallback"`.
5) **IMPORTANT: After loading facts, ALWAYS synthesize them into a human-readable summary (see Summarization section below).**

## Summarization (Required for Recall)

After running the load command, **you MUST synthesize the raw JSON facts into a useful summary**. Never just show raw JSON to the user.

### Summary Structure
Organize facts into these categories (skip empty categories):

1. **Project Overview** - What the project is and does
2. **Recent Activity** - What was worked on recently (files modified, features added)
3. **Conventions & Patterns** - Naming conventions, coding standards, folder structure
4. **Configuration** - Docker, environments, tools, dependencies
5. **Milestones** - Completed features, important checkpoints
6. **Open Items** - Pending tasks, known issues

### How to Summarize
- **ALWAYS sort memories by `created_at` descending** (newest first)
- Group related facts together
- Use bullet points for clarity
- Include specific file names and paths when relevant
- Include the date for each memory (format: "Jan 23" or "Jan 23, 2026")
- Filter out expired or superseded facts (check `expired_at` field)
- Prioritize recent facts over older ones - show newest at top of each section
- Extract the `fact` field from each item - that's the human-readable content

### Example Output Format
```
## Memory Summary

**Project:** Lisa - Long-term memory system for Claude Code

**Recent Activity:**
- Modified `src/lib/mcp.ts` for MCP integration
- Updated Docker config to use `zepai/knowledge-graph-mcp:standalone`
- Added init-review script

**Conventions:**
- Files use kebab-case naming
- JavaScript/TypeScript as primary languages

**Configuration:**
- Docker Compose at `.lisa/docker-compose.graphiti.yml`
- Config file: `config-docker-neo4j.yaml`

**Milestones:**
- Memory system reached major milestone (date)
```

## I/O contract (examples)
- Recall: output JSON `{ status: "ok", action: "load", group, query, facts: [...] }`.
- Remember: JSON `{ status: "ok", action: "add", group, text }`.
- Fallback: JSON `{ status: "fallback", error, fallback: <last cached object> }`.

## Cross-model checklist
- Claude: confirm concise trigger phrasing; keep under system limits; avoid markdown-heavy instructions.
- Gemini: ensure commands are explicit; avoid model-specific tokens; keep JSON small.

## Notes
- All commands use the `lisa` CLI binary — no scripts to run directly.
- Facts query defaults to `*` with `max_facts=10`; tune via `--limit` and `--query`.
- The `fact` field in each JSON object contains the human-readable content to summarize.
