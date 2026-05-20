---
name: datasette
tier: skill
type: bridge
protocol: DATASETTE-BRIDGE
aliases: [datasette, data-explorer, sqlite-web]
audience: ["operators", "devs", "agents", "data-journalists"]
platforms: ["macos", "linux", "windows"]
author: "Simon Willison (Datasette); Don Hopkins (MOOLLM integration)"
license: Apache-2.0
related: [cursor-mirror, yaml-jazz, sister-script, play-learn-lift]
state:
  creates:
    - "cursor-mirror.db (consolidated export)"
  reads:
    - "~/.cursor/**/agent-transcripts/*.db (transcript indexes)"
    - "~/Library/Application Support/Cursor/User/globalStorage/state.vscdb"
tools:
  required: [terminal]
  optional: [read_file, web_search]
invoke_when:
  - "Want to explore cursor-mirror data in a browser"
  - "Want to share analysis results via URL"
  - "Want a dashboard of agent activity"
  - "Want to query cursor-mirror data via JSON API"
  - "Want to publish cursor-mirror findings"
---

# Datasette: WordPress for Data

> *"Datasette is the fastest way to publish data online as an interactive,
> searchable database."* -- Simon Willison

Datasette takes any SQLite database and gives it a web UI, JSON API,
full-text search, faceting, filtering, CSV export, and 154+ plugins.
One command. Zero backend code.

cursor-mirror already produces SQLite databases (transcript indexes,
consolidated exports). Datasette is how those databases get a face.

## Quick Start

```bash
# Install (in cursor-mirror venv or globally)
pip install datasette

# Serve Cursor's own database (read-only, safe)
datasette ~/Library/Application\ Support/Cursor/User/globalStorage/state.vscdb

# Serve a cursor-mirror consolidated export
python -c "
import sys; sys.path.insert(0,'.')
from lib.datasette_export import export_datasette
from pathlib import Path
export_datasette(Path('cursor-mirror.db'))
"
datasette cursor-mirror.db -o
```

The `-o` flag opens your browser. Every page has a JSON equivalent (add `.json` to the URL).

## What You Get

| Table | Rows (typical) | What |
|-------|----------------|------|
| composers | 200+ | Every conversation with metadata, bubble counts |
| transcript_sections | 30,000+ | Parsed sections: USER, ASSISTANT, TOOL_CALL, THINKING |
| shell_commands | 2,000+ | Every terminal command with line numbers |
| tool_calls | 2,000+ | Tool usage with params, error status |
| feature_flags | 30+ | Model vs live flags with drift detection |

Full-text search is enabled on transcript previews. Faceting works on
section type, tool name, composer, workspace.

## Key Datasette Features

**URLs are the API.** Every query, filter, and facet combination has a
permanent URL. Share it with a colleague. Add `.json` for machine access.
Add `.csv` for spreadsheet export. This is Datasette's core insight.

**Faceting.** Click a column name to see value distribution. Filter by
clicking values. Combine multiple facets. No SQL needed.

**SQL.** Full SQL editor built in. Write any query, get results as HTML,
JSON, or CSV. Canned queries can be pre-configured.

**Plugins.** 154+ plugins for charts (datasette-vega), maps
(datasette-cluster-map), dashboards (datasette-dashboards), auth,
search, and more.

**Publishing.** `datasette publish vercel cursor-mirror.db` deploys
your data to a public URL in one command. Also supports Fly, Cloud Run.

## Integration with cursor-mirror

### Direct serve (zero code)

Datasette can open any of cursor-mirror's SQLite files directly:

```bash
# Cursor's global database (ItemTable, cursorDiskKV)
datasette state.vscdb

# A transcript index (sections, shell_commands, tool_params)
datasette ~/.cursor/projects/*/agent-transcripts/*.db

# Multiple databases at once
datasette state.vscdb transcript-index.db
```

### Consolidated export

The `export_datasette()` function in `cursor-mirror/lib/datasette_export.py`
produces a single optimized database combining:
- All composer metadata
- Parsed transcript sections (with FTS)
- Shell commands
- Tool calls from bubbles
- Feature flag drift

### Planned: datasette-cursor-mirror plugin

A Datasette plugin that auto-discovers cursor-mirror data, renders
transcript sections as formatted HTML, and adds a dashboard. See
`designs/DATASETTE-CURSOR-MIRROR-INTEGRATION.md` for the full plan.

## Useful Datasette Commands

```bash
# Serve with CORS (for JavaScript access from other domains)
datasette cursor-mirror.db --cors

# Serve read-only (immutable mode, enables caching)
datasette -i cursor-mirror.db

# Install a plugin
datasette install datasette-vega

# Publish to Vercel (free tier)
datasette publish vercel cursor-mirror.db --project my-cursor-data

# Run a SQL query from the command line (no server)
datasette cursor-mirror.db --get '/cursor-mirror.json?sql=select+tool_name,count(*)+from+tool_calls+group+by+1+order+by+2+desc&_shape=array'
```

## Useful SQL Queries (Canned Queries for Datasette)

### Most used tools
```sql
select tool_name, count(*) as calls, sum(is_error) as errors
from tool_calls group by tool_name order by calls desc
```

### Shell commands by workspace
```sql
select workspace, count(*) as commands
from shell_commands group by workspace order by commands desc
```

### Feature flag drift
```sql
select flag, model_enabled, live_enabled
from feature_flags where drift = 1 order by flag
```

### Busiest composers
```sql
select c.name, c.bubble_count, c.workspace_folder,
       (select count(*) from transcript_sections ts where ts.composer_id = c.id) as sections
from composers c order by c.bubble_count desc limit 20
```

### Thinking blocks (search for keywords)
```sql
select composer_id, start_line, end_line, text_preview
from transcript_sections where type = 'THINKING'
and text_preview like '%security%' order by start_line
```

## About Datasette

Created by Simon Willison (co-creator of Django). Open source, Apache 2.0.
10.8k GitHub stars, 154+ plugins, Python 3.14 compatible.

- Website: https://datasette.io
- Docs: https://docs.datasette.io
- Plugins: https://datasette.io/plugins
- Source: https://github.com/simonw/datasette
- Cloud: https://www.datasette.cloud

## Part of MOOLLM

This is a MOOLLM skill. See the [MOOLLM README](../../README.md) and
[skills index](../README.md) for context.
