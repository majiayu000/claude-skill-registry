---
name: adr-index
description: Build or rebuild the ADR index and dependency graph in AgentDB
argument-hint: ""
allowed-tools: mcp__claude-flow__agentdb_hierarchical-store mcp__claude-flow__agentdb_hierarchical-query mcp__claude-flow__agentdb_causal-edge mcp__claude-flow__agentdb_causal-query mcp__claude-flow__memory_store mcp__claude-flow__memory_search Bash Read Grep Glob
---

# ADR Index

Build or rebuild the full ADR index and dependency graph in AgentDB from the `docs/adr/` directory.

## When to use

After importing ADRs from another project, when the AgentDB graph is out of sync, or when bootstrapping ADR tracking on an existing codebase that already has ADR files.

## Steps

1. **Scan directory** -- `Glob` for `docs/adr/ADR-*.md` to find all ADR files. If no files found, report that no ADRs exist yet.

2. **Parse each ADR** -- `Read` each file and extract:
   - **ID**: from the filename (e.g., `ADR-042` from `ADR-042-use-postgres.md`)
   - **Title**: from the `# ADR-NNN: <Title>` heading
   - **Status**: from the `**Status**:` line
   - **Date**: from the `**Date**:` line
   - **Tags**: from the `**Tags**:` line
   - **Links**: from the `## Links` section (supersedes, amended-by, related)

3. **Store in AgentDB** -- For each ADR, call `mcp__claude-flow__agentdb_hierarchical-store` with:
   - path: `adr/<adr-id>`
   - value: `{ "id": "<id>", "title": "<title>", "status": "<status>", "date": "<date>", "tags": "<tags>", "file": "<filepath>" }`

4. **Build causal edges** -- For each ADR with links:
   - "Supersedes ADR-XXX" -> `mcp__claude-flow__agentdb_causal-edge` with `from: ADR-XXX`, `to: <current>`, `relation: supersedes`
   - "Amended by ADR-YYY" -> `mcp__claude-flow__agentdb_causal-edge` with `from: <current>`, `to: ADR-YYY`, `relation: amends`
   - "Related: ADR-ZZZ" -> `mcp__claude-flow__agentdb_causal-edge` with `from: <current>`, `to: ADR-ZZZ`, `relation: related`
   - "Depends on ADR-WWW" -> `mcp__claude-flow__agentdb_causal-edge` with `from: <current>`, `to: ADR-WWW`, `relation: depends-on`

5. **Store in memory** -- For each ADR, call `mcp__claude-flow__memory_store` with:
   - namespace: `adr-patterns`
   - key: `<adr-id>`
   - value: `<title> — <first paragraph of Context section>`
   This enables semantic search across ADRs.

6. **Verify graph** -- Call `mcp__claude-flow__agentdb_causal-query` to retrieve all edges and verify:
   - No dangling references (edges pointing to non-existent ADRs)
   - No circular supersedes chains
   - All superseded ADRs have status "superseded"

7. **Report** -- Output a summary:
   ```
   ## ADR Index Summary

   Total ADRs: N
   - Proposed: X
   - Accepted: Y
   - Deprecated: Z
   - Superseded: W

   Relationships: M edges
   - Supersedes: A
   - Amends: B
   - Depends-on: C
   - Related: D

   Issues found: (list any dangling refs or status mismatches)
   ```
