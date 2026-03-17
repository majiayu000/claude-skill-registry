---
name: linkedin-export
description: Parse, search, analyze, and ingest LinkedIn GDPR data exports. This skill should be used when working with LinkedIn data — searching messages, analyzing connections, exporting to Markdown, or ingesting into RLAMA for semantic search. Requires a LinkedIn GDPR data export ZIP file.
---

# LinkedIn Export Skill

Parse LinkedIn GDPR data exports into structured JSON, then search messages, analyze connections, export to Markdown, and ingest into RLAMA for semantic search.

## Prerequisites

- **Python 3.10+** via `uv`
- **LinkedIn GDPR export ZIP** — Request at: LinkedIn → Settings → Data Privacy → Get a copy of your data
- **RLAMA + Ollama** (optional, for semantic search ingestion)

## Quick Start

```bash
# 1. Parse the export ZIP (run once)
uv run ~/.claude/skills/linkedin-export/scripts/li_parse.py ~/Downloads/Basic_LinkedInDataExport_*.zip

# 2. Search, analyze, export, or ingest
uv run ~/.claude/skills/linkedin-export/scripts/li_search.py --list-partners
uv run ~/.claude/skills/linkedin-export/scripts/li_network.py summary
uv run ~/.claude/skills/linkedin-export/scripts/li_export.py all --output ~/linkedin-archive/
uv run ~/.claude/skills/linkedin-export/scripts/li_ingest.py
```

All scripts read from `~/.claude/skills/linkedin-export/data/parsed.json`. Parse once, query many times.

---

## Parse — `li_parse.py`

Unzip and parse all CSVs from the LinkedIn GDPR export into structured JSON.

```bash
uv run ~/.claude/skills/linkedin-export/scripts/li_parse.py <linkedin-export.zip>
uv run ~/.claude/skills/linkedin-export/scripts/li_parse.py <zip> --output /custom/path.json
```

**Output**: `~/.claude/skills/linkedin-export/data/parsed.json`

Parses: messages, connections, profile, positions, education, skills, endorsements, invitations, recommendations, shares, reactions, certifications.

Auto-detects CSV column names (case-insensitive) to handle LinkedIn format changes between exports.

---

## Search Messages — `li_search.py`

Search messages by person, keyword, date range, or combination.

```bash
# Search by person
uv run ~/.claude/skills/linkedin-export/scripts/li_search.py --person "Jane Doe"

# Search by keyword
uv run ~/.claude/skills/linkedin-export/scripts/li_search.py --keyword "project proposal"

# Date range
uv run ~/.claude/skills/linkedin-export/scripts/li_search.py --after 2025-01-01 --before 2025-06-01

# Combined filters
uv run ~/.claude/skills/linkedin-export/scripts/li_search.py --person "Jane" --keyword "meeting" --after 2025-06-01

# Full conversation by ID
uv run ~/.claude/skills/linkedin-export/scripts/li_search.py --conversation "CONVERSATION_ID"

# List all conversation partners (sorted by message count)
uv run ~/.claude/skills/linkedin-export/scripts/li_search.py --list-partners

# Show context around matches
uv run ~/.claude/skills/linkedin-export/scripts/li_search.py --keyword "AI" --context 3

# Full message content + JSON output
uv run ~/.claude/skills/linkedin-export/scripts/li_search.py --keyword "proposal" --full --json
```

**Flags**: `--person`, `--keyword`, `--after`, `--before`, `--conversation`, `--list-partners`, `--context N`, `--full`, `--limit N`, `--json`

---

## Network Analysis — `li_network.py`

Analyze the connection graph — companies, roles, timeline.

```bash
# Summary stats
uv run ~/.claude/skills/linkedin-export/scripts/li_network.py summary

# Top companies by connection count
uv run ~/.claude/skills/linkedin-export/scripts/li_network.py companies --top 20

# Connection timeline
uv run ~/.claude/skills/linkedin-export/scripts/li_network.py timeline --by year
uv run ~/.claude/skills/linkedin-export/scripts/li_network.py timeline --by month

# Role/title distribution
uv run ~/.claude/skills/linkedin-export/scripts/li_network.py roles --top 20

# Search connections
uv run ~/.claude/skills/linkedin-export/scripts/li_network.py search "Anthropic"

# Export connections to CSV or JSON
uv run ~/.claude/skills/linkedin-export/scripts/li_network.py export --format csv
uv run ~/.claude/skills/linkedin-export/scripts/li_network.py export --format json
```

**Subcommands**: `summary`, `companies`, `timeline`, `roles`, `search`, `export`

---

## Export to Markdown — `li_export.py`

Convert parsed data to clean Markdown files.

```bash
# Export messages (one file per conversation)
uv run ~/.claude/skills/linkedin-export/scripts/li_export.py messages --output ~/linkedin-archive/messages/

# Export connections as Markdown table
uv run ~/.claude/skills/linkedin-export/scripts/li_export.py connections --output ~/linkedin-archive/connections.md

# Export everything
uv run ~/.claude/skills/linkedin-export/scripts/li_export.py all --output ~/linkedin-archive/

# Export RLAMA-optimized documents
uv run ~/.claude/skills/linkedin-export/scripts/li_export.py rlama --output ~/linkedin-archive/rlama/
```

**Subcommands**: `messages`, `connections`, `all`, `rlama`

---

## RLAMA Ingestion — `li_ingest.py`

Prepare RLAMA-optimized documents and create a semantic search collection.

```bash
# Full pipeline: prepare docs + create RLAMA collection
uv run ~/.claude/skills/linkedin-export/scripts/li_ingest.py

# Prepare docs only (no RLAMA required)
uv run ~/.claude/skills/linkedin-export/scripts/li_ingest.py --prepare-only

# Rebuild existing collection
uv run ~/.claude/skills/linkedin-export/scripts/li_ingest.py --rebuild
```

**Collection**: `linkedin-tdimino` (fixed/600/100 chunking, BM25-heavy hybrid search)

**Query examples**:
```bash
rlama run linkedin-tdimino --query "What did I discuss with [person]?"
rlama run linkedin-tdimino --query "Who works at [company]?"
rlama run linkedin-tdimino --query "What are my top skills?"
```

**RLAMA document structure**:
- `messages-conversations-{a-f,g-l,m-r,s-z}.md` — Conversations grouped alphabetically
- `connections-companies.md` — Connections by company
- `connections-timeline.md` — Connections by year
- `profile-positions-education.md` — Resume data
- `endorsements-skills.md` — Skills and endorsements
- `shares-reactions.md` — Posts and activity
- `INDEX.md` — Collection metadata

---

## Data Format Reference

See `references/linkedin-export-format.md` for complete CSV column documentation.

**Key files in the LinkedIn export ZIP**:

| CSV | Contents |
|-----|----------|
| `messages.csv` | All messages and InMail |
| `Connections.csv` | 1st-degree connections |
| `Profile.csv` | Profile data |
| `Positions.csv` | Work history |
| `Education.csv` | Education |
| `Skills.csv` | Listed skills |
| `Endorsement_Received_Info.csv` | Endorsements |
| `Invitations.csv` | Connection requests |
| `Recommendations_Received.csv` | Recommendations |
| `Shares.csv` | Posts and shares |
| `Reactions.csv` | Post reactions |
| `Certifications.csv` | Certifications |

---

## Script Selection Guide

| Task | Script | Example |
|------|--------|---------|
| First-time setup | `li_parse.py` | Parse the ZIP |
| Find a conversation | `li_search.py --person` | Search by person name |
| Find a topic | `li_search.py --keyword` | Search by keyword |
| Who do I talk to most? | `li_search.py --list-partners` | Sorted partner list |
| Company breakdown | `li_network.py companies` | Top companies |
| Network growth | `li_network.py timeline` | Connections over time |
| Archive messages | `li_export.py messages` | Markdown per conversation |
| Semantic search | `li_ingest.py` | RLAMA collection |
