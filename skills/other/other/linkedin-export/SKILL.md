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

Parses 23 CSV types:

**Core**: messages, connections, profile, positions, education, skills, endorsements, invitations, recommendations, shares, reactions, certifications

**Extended**: comments (548), projects (3), honors (2), organizations (3), volunteering (1), languages (9), events (12), member_follows (828), job_applications (443, merged from multiple files), recommendations_given (3), inferences (4)

Auto-detects CSV column names (case-insensitive), handles LinkedIn's preamble format (Connections.csv), and merges split files (Job Applications).

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

**Collection**: `linkedin-tdimino` (fixed/600/100 chunking, reranker enabled, 13 docs, 2.14 MB)

**Query (default: retrieve-only, Claude synthesizes)**:
```bash
# Retrieve raw chunks — Claude reads and synthesizes (best quality)
python3 ~/.claude/skills/rlama/scripts/rlama_retrieve.py linkedin-tdimino "What projects has Tom built?" -k 10

# Fallback: local LLM answers (only without Claude)
rlama run linkedin-tdimino --query "Who works at Google?"
```

**RLAMA document structure (13 files)**:
- `messages-conversations-{a-f,g-l,m-r,s-z}.md` — Conversations grouped alphabetically
- `connections-companies.md` — Connections by company
- `connections-timeline.md` — Connections by year
- `profile-positions-education.md` — Resume data
- `endorsements-skills.md` — Skills and endorsements
- `shares-reactions.md` — Posts and activity
- `comments-activity.md` — 548 comments with dates and links
- `projects-honors-volunteering.md` — Projects, honors, volunteering, organizations
- `metadata-languages-events-follows.md` — Languages, events, follows, job applications, recommendations given, inferences
- `INDEX.md` — Collection metadata and counts

---

## Data Format Reference

See `references/linkedin-export-format.md` for complete CSV column documentation.

**Key files in the LinkedIn export ZIP (23 parsed)**:

| CSV | Contents |
|-----|----------|
| `messages.csv` | All messages and InMail |
| `Connections.csv` | 1st-degree connections (preamble format) |
| `Profile.csv` | Profile data |
| `Positions.csv` | Work history |
| `Education.csv` | Education |
| `Skills.csv` | Listed skills |
| `Endorsement_Received_Info.csv` | Endorsements received |
| `Invitations.csv` | Connection requests |
| `Recommendations_Received.csv` | Recommendations received |
| `Shares.csv` | Posts and shares |
| `Reactions.csv` | Post reactions |
| `Certifications.csv` | Certifications |
| `Comments.csv` | Comments on posts |
| `Projects.csv` | Projects (Bazaar, Dream Daimon, etc.) |
| `Honors.csv` | Awards and hackathon wins |
| `Organizations.csv` | Clubs and groups |
| `Volunteering.csv` | Volunteer roles |
| `Languages.csv` | Language proficiencies |
| `Events.csv` | LinkedIn events |
| `Member_Follows.csv` | People/companies followed |
| `Jobs/Job Applications*.csv` | Job applications (split across multiple files) |
| `Recommendations_Given.csv` | Recommendations written |
| `Inferences_about_you.csv` | LinkedIn's inferences |

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
