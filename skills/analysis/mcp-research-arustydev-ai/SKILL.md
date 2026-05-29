---
name: mcp-research
description: >-
  Discover, profile, and evaluate MCP servers for a given domain or purpose.
  Use when searching for MCP servers to add to a project, comparing server
  capabilities, enriching the local registry cache, or evaluating whether
  a server suite covers a stated need. Covers cache-first discovery,
  remote registry scanning, deep server profiling, and gap analysis.
---

# MCP Server Research

Guide for discovering, profiling, and evaluating MCP servers using the local SQLite+FTS5 registry cache and three specialized agents.

## When to Use This Skill

- Finding MCP servers for a specific domain (e.g., "code analysis", "database management")
- Profiling an MCP server to understand its tools, install method, and quality
- Comparing multiple servers to recommend the best fit
- Seeding or enriching the local registry cache
- Running the `/find-mcp-servers` slash command

## Architecture

```
┌─────────────────────┐
│  /find-mcp-servers  │  ← Slash command (entry point)
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐     ┌──────────────────────┐
│ plugin-mcp-researcher│────▶│ SQLite+FTS5 Cache    │
│ (orchestrator)       │     │ .data/mcp/registry-  │
└────────┬────────────┘     │ cache.db             │
         │                   └──────────────────────┘
    ┌────┴────┐
    ▼         ▼
┌────────┐ ┌─────────────┐
│Scanner │ │  Profiler    │
│(haiku) │ │  (sonnet)    │
└────────┘ └─────────────┘
```

### Components

| Component | Type | Model | Purpose |
|-----------|------|-------|---------|
| `plugin-mcp-researcher` | agent | haiku | Cache-first orchestrator — queries FTS, dispatches scanner/profiler |
| `mcp-registry-scanner` | agent | haiku | Lightweight discovery — finds NEW servers across remote registries |
| `mcp-server-profiler` | agent | sonnet | Deep enrichment — fetches README, extracts tools, updates cache |
| `/find-mcp-servers` | command | — | User-facing slash command for server discovery |

### Storage Layer

MCP server data lives in the unified knowledge graph:

```
.data/mcp/knowledge-graph.db   ← SQLite + sqlite-vec (gitignored)
.data/mcp/knowledge-graph.sql  ← SQL dump (version controlled)
```

**Tables:**

| Table | Purpose |
|-------|---------|
| `entities` | Core records with `entity_type = 'mcp_server'` |
| `mcp_servers_ext` | MCP-specific fields (install, repo, transport, etc.) |
| `mcp_server_tools` | Tools exposed by each server |
| `mcp_server_deps` | Dependencies required by each server |
| `mcp_server_assessments` | Quality/relevance assessments per server |
| `v_mcp_servers` | Unified view joining entities + mcp_servers_ext |

**Management commands:**

```bash
just mcp-stats          # Show server/registry counts
just mcp-search "query" # Search servers by name/description
just mcp-list           # List top servers by stars
just mcp-show <slug>    # Show server details
just mcp-tools <slug>   # Show server's tools
just kg-dump            # Dump entire knowledge graph
```

## Workflow: Discovering Servers

### Step 1: Query Local Cache

Always check the cache first. Use FTS5 or LIKE queries on the knowledge graph:

```bash
sqlite3 -json .data/mcp/knowledge-graph.db "
  SELECT e.id, e.name, e.slug, e.content as description,
         ext.install_method, ext.install_command, ext.repository, ext.stars,
         json_extract(e.metadata, '$.features') as features
  FROM entities e
  JOIN entities_fts f ON e.id = f.rowid
  LEFT JOIN mcp_servers_ext ext ON e.id = ext.entity_id
  WHERE e.entity_type = 'mcp_server'
    AND entities_fts MATCH '<keyword1> OR <keyword2>'
  ORDER BY rank
  LIMIT 20;
"
```

Or use the convenience view:

```bash
sqlite3 -json .data/mcp/knowledge-graph.db "
  SELECT * FROM v_mcp_servers
  WHERE name LIKE '%<keyword>%' OR content LIKE '%<keyword>%'
  ORDER BY stars DESC NULLS LAST
  LIMIT 20;
"
```

### Step 2: Evaluate Coverage

Count enriched matches (those with `description` AND `features` populated):

- **>= 3 enriched**: Sufficient — skip to ranking
- **< 3 enriched**: Insufficient — proceed to remote discovery

### Step 3: Remote Discovery (if needed)

Spawn `mcp-registry-scanner` (haiku) via Task tool:

```
Domain: <keywords>
Plugin: standalone-search
```

The scanner searches 24+ registries in tiered priority order, deduplicates against the cache, and inserts minimal records for new finds.

### Step 4: Deep Profiling (if needed)

For each new discovery (or shallow cache hit missing description/features), spawn `mcp-server-profiler` (sonnet) via Task tool:

```
Server: <slug>
Plugin: standalone-search
Need: <original purpose string>
```

Run up to 5 profilers in parallel. Each enriches the cache with:
- Full description and feature tags
- Install method and command
- Repository URL and stars
- Language and transport protocol
- Tools exposed (inserted into `mcp_server_tools`)
- Dependencies (inserted into `mcp_server_deps`)

### Step 5: Rank and Present

Score matches using weighted criteria:

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Feature relevance | 40% | How well do features match the stated purpose |
| Maintenance | 25% | Stars, last_updated recency, active development |
| Install ease | 20% | brew/npx > pip > docker > manual |
| Tool coverage | 15% | Number and relevance of MCP tools exposed |

## Workflow: Profiling a Single Server

When you need to deeply research one specific server:

1. Check if it exists in cache: `sqlite3 .data/mcp/knowledge-graph.db "SELECT * FROM mcp_servers WHERE slug='<slug>';"`
2. If not cached, insert a minimal record first
3. Spawn `mcp-server-profiler` with the slug
4. The profiler will:
   - Fetch the repository README (via `gh api` or WebSearch)
   - Extract metadata: description, features, install method, language, transport
   - Identify tools from README documentation or package manifests
   - Check quality signals: stars, forks, last commit date, open issues
   - UPDATE the cache record and INSERT tool/dep records

## Workflow: Seeding from YAML Config

When bulk-loading servers from `settings/mcp/*.yaml`:

```bash
# Read category entries from YAML
# For each entry, INSERT OR IGNORE into mcp_servers with:
#   - slug (normalized from name)
#   - source_registry (from YAML source field)
#   - source_url (from YAML url field)
# Then dump knowledge graph
just kg-dump
```

## Registry Reference

See `reference/registries.yaml` for the full list of 24+ MCP server registries organized by tier.

### Tier 1 (always search)

- smithery.ai — Curated registry with install commands
- registry.modelcontextprotocol.io — Official MCP registry
- glama.ai — Detailed server profiles
- pulsemcp.com — Community registry
- mcp.so — Search-focused directory
- GitHub topic search (`gh search repos --topic mcp-server`)

### Tier 2 (search on cache miss)

- mcpservers.org, mcpdb.org, mcp-get.com, opentools.com, cursor.directory, lobehub.com

### Tier 3 (search if Tier 2 insufficient)

- himcp.ai, mcpmarket.com, portkey.ai, cline.bot, apitracker.io, and others

## Web Scraping for Profiling

The profiler agent needs to fetch web content (READMEs, registry pages) and convert to markdown. Available methods in priority order:

Use this 9-tier fallback chain in order:

### 1. gh api (preferred for GitHub repos)

```bash
gh api repos/<owner>/<repo>/readme --jq '.content' | base64 -d
```

### 2. crawl4ai-mcp

If the crawl4ai MCP server is connected, use it for JS-rendered pages.

### 3. trafilatura

```bash
trafilatura -u <url>
```

Clean text extraction CLI. Works well for static pages and documentation sites.

### 4. WebSearch

Use `site:<domain> <server-name>` queries to find registry pages. Results include summaries with key metadata.

### 5. WebFetch

Fetches URL content and converts HTML to markdown. Works for static pages. May be auto-denied in background subagents.

### 6. Jina Reader

```bash
curl -sL "https://r.jina.ai/<url>"
```

Free tier API for converting web pages to markdown.

### 7. firecrawl

`firecrawl_scrape` with `formats: ["markdown"]`. Handles JS-rendered pages. Use when credits are available.

### 8. markdownify

```bash
curl -sL <url> | python3 -c "import sys; from markdownify import markdownify; print(markdownify(sys.stdin.read()))"
```

### 9. html2text

```bash
curl -sL <url> | html2text
```

Last resort — basic HTML-to-text conversion.

## Common Patterns

### Inserting a new server

```sql
-- First insert into entities
INSERT INTO entities (entity_type, slug, name, content, metadata)
VALUES ('mcp_server', '<slug>', '<name>', '<description>',
        json_object('features', '<comma,separated,tags>'));

-- Then insert into mcp_servers_ext
INSERT INTO mcp_servers_ext (entity_id, source_registry, source_url, discovered_at)
SELECT id, '<registry>', '<url>', datetime('now')
FROM entities WHERE slug = '<slug>' AND entity_type = 'mcp_server';
```

### Updating after profiling

```sql
-- Update entity content
UPDATE entities SET
  content = '<description>',
  metadata = json_set(metadata, '$.features', '<comma,separated,tags>'),
  updated_at = datetime('now')
WHERE slug = '<slug>' AND entity_type = 'mcp_server';

-- Update extension fields
UPDATE mcp_servers_ext SET
  install_method = '<brew|npx|pip|docker|manual>',
  install_command = '<command>',
  repository = '<url>',
  language = '<lang>',
  stars = <N>,
  last_updated = '<ISO date>',
  refreshed_at = datetime('now')
WHERE entity_id = (SELECT id FROM entities WHERE slug = '<slug>' AND entity_type = 'mcp_server');
```

### Inserting tools

```sql
INSERT INTO mcp_server_tools (server_id, name, description)
SELECT id, '<tool_name>', '<tool_description>'
FROM entities WHERE slug = '<slug>' AND entity_type = 'mcp_server';
```

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| FTS returns no results | Keywords too specific or DB empty | Use broader terms, check `just mcp-stats` |
| Profiler can't fetch README | WebFetch/firecrawl denied in subagent | Fall back to `gh api` or WebSearch |
| Firecrawl credits exhausted | API quota hit | Use `gh api`, WebSearch, or CLI fallbacks |
| Duplicate slugs on insert | Server already exists | Use `INSERT OR IGNORE` or check before inserting |
| DB locked errors | Concurrent writes from parallel agents | Run profilers sequentially or use WAL mode |
| Changes not persisted | Forgot to dump after changes | Run `just kg-dump` |

## Checklist

- [ ] Knowledge graph initialized (`just kg-init`)
- [ ] FTS/LIKE query built from purpose keywords
- [ ] Cache checked before any remote calls
- [ ] Scanner spawned only on cache miss
- [ ] Profilers run in parallel (max 5)
- [ ] Knowledge graph dumped after modifications (`just kg-dump`)
- [ ] Results ranked by weighted criteria
- [ ] Tools fetched for top results

## References

- [MCP Specification](https://spec.modelcontextprotocol.io)
- [Awesome MCP Servers](https://github.com/punkpeye/awesome-mcp-servers)
- Registry list: `reference/registries.yaml`
- Agent definitions: `context/agents/mcp-registry-scanner.md`, `context/agents/mcp-server-profiler.md`, `context/agents/plugin-mcp-researcher.md`
- Command: `context/commands/find-mcp-servers.md`
