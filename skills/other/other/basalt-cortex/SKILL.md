---
name: basalt-cortex
description: "Mine knowledge from Gmail, Google Chat, Slack, Drive, local files, MCP servers, and web into an Obsidian-compatible vault (~/Documents/basalt-cortex/). Basalt format: markdown files with YAML frontmatter for clients, contacts, communications, and knowledge facts. Opens directly in Obsidian, syncs to basaltcortex.com via CLI daemon. Triggers: 'run the cortex', 'mine emails', 'mine slack', 'mine chat', 'cortex init', 'cortex search', 'cortex stats', 'what do I know about', 'set up cortex', 'mine my inbox'."
compatibility: claude-code-only
---

# Basalt Cortex

Mine knowledge from multiple sources into Obsidian-compatible markdown files stored in `~/Documents/basalt-cortex/`. Each file has structured YAML frontmatter. Files auto-sync to basaltcortex.com via the `basalt-cortex` CLI tray daemon.

**Read [references/basalt-format.md](references/basalt-format.md) before any file operations.**

## Modes

| Mode | Trigger | What it does |
|------|---------|-------------|
| **init** | "set up cortex", "cortex init" | Create vault structure, state.json, example notes |
| **mine** | "run the cortex", "mine emails", "mine slack" | Extract from a source, write Basalt files |
| **query** | "cortex search", "what do I know about" | Search across Basalt files |
| **stats** | "cortex stats" | Count files, show vault totals |
| **sync** | "cortex sync" | Push to Frond API (future — see references/sync-patterns.md) |

---

## Init Mode

Create the vault structure. Run once before first mine.

### Check for existing vault

```bash
ls ~/Documents/basalt-cortex/state.json 2>/dev/null && echo "EXISTS" || echo "FRESH"
```

If EXISTS: ask user — skip, reset (data loss warning), or continue (add missing folders only).

### Create structure

```bash
mkdir -p ~/Documents/basalt-cortex/{clients,contacts,communications,knowledge,projects,notes,.obsidian}
```

### Write state.json

```json
{
  "version": "1.0",
  "format": "basalt",
  "cursors": { "gmail": null, "google_chat": null, "slack": null, "calendar": null },
  "last_run": null,
  "totals": { "clients": 0, "contacts": 0, "communications": 0, "knowledge": 0 },
  "processed_source_ids": [],
  "runs": []
}
```

### Write Obsidian config

```json
// ~/Documents/basalt-cortex/.obsidian/app.json
{ "newFileLocation": "folder", "newFileFolderPath": "notes" }
```

### Write 3 example notes

Create one example client, contact, and knowledge note in Basalt format so the user can see the structure. Use templates from [references/basalt-format.md](references/basalt-format.md).

Report the created structure to the user. Tell them to open `~/Documents/basalt-cortex/` in Obsidian.

---

## Mine Mode

Extract knowledge from a source and write Basalt-format files.

### Source Selection

Ask or detect which source to mine:

| Source | Fetch method | Notes |
|--------|-------------|-------|
| **gmail** (default) | Gmail MCP (`gmail_messages`) | Use `extract_contacts` + `list` + `get` |
| **google-chat** | Google Chat MCP (`chat_messages`) | Mine space-by-space, NOT `search_active` |
| **slack** | Slack MCP or API token | MCP tools or `curl` with token |
| **google-drive** | Drive MCP or `gws` CLI | Metadata + summaries, don't copy full docs |
| **local** | Read tool + Glob | `find` + `cat` on local directories |
| **mcp** | MCP tool calls | Any connected MCP server with searchable data |
| **web** | WebFetch or browser | Firecrawl, Playwright, or WebFetch |
| **calendar** | Calendar MCP or `gws` CLI | Events, attendees, meeting notes |

### Proven Extraction Workflow (Two-Phase)

Mining works in two phases. Phase 1 (reconnaissance) uses MCP tools interactively. Phase 2 (batch write) generates a Python script for efficiency.

#### Phase 1: Reconnaissance via MCP (interactive)

Use MCP tools to fetch raw data and identify entities. Claude does the AI extraction in-context — no external LLM call needed.

**Gmail example:**
```
1. extract_contacts — scan 100 recent emails, get deduplicated contacts with names/emails/counts
   - Use `field: "from"` for inbound contacts
   - Use `field: "to"` for outbound contacts (from sent mail)
   - Exclude automated domains: jezweb.net, google.com, github.com, cloudflare.com, etc.

2. list — fetch 30-50 emails per batch with bodyPreview
   - Query: `in:inbox -category:promotions -category:social -category:updates -category:forums after:YYYY/MM/DD`
   - Format: compact or full, bodyPreview: 1000-2000

3. get — fetch full content for significant threads (client conversations, support requests, decisions)

4. Pre-filter while scanning:
   - Skip: 2FA codes, domain expiry notices, payment receipts, Wordfence alerts, auto top-ups
   - Keep: Real human conversations, support requests, project discussions, business decisions
   - See references/prefilter-patterns.md for full skip/keep rules
```

**Google Chat example:**
```
1. chat_spaces list — get all spaces with lastActiveTime
2. chat_messages list — fetch ONE space at a time, limit 25-50
   - NEVER use search_active for mining (times out on 50+ spaces)
   - Iterate space by space, save progress after each
3. Pre-filter: skip bot messages, join/leave events, webhook posts
```

From the fetched data, identify:
- **CLIENTS**: businesses/organisations (name, domain, industry)
- **CONTACTS**: people mentioned (name, email, role, company, phone if visible)
- **COMMUNICATIONS**: the interaction itself (subject, participants, summary, type)
- **KNOWLEDGE**: facts, decisions, preferences, commitments, relationships, deadlines

For each entity, craft a `summary` field: 1-3 sentences, dense with names and context. This is the Vectorize embedding input — make it specific and useful for semantic search.

#### Phase 2: Batch Write via Python Script

Once entities are identified, generate a Python script to write all Basalt files at once. This is dramatically faster than individual Write tool calls (55 files in one execution vs 8 tool calls for 17 files).

**Script location:** `.jez/scripts/mine-{source}-batch.py`

**Script must include these helper functions:**
- `slugify(text)` — lowercase, hyphens, no special chars, max 60 chars
- `write_client(domain, name, industry, summary, contacts, tags)`
- `write_contact(name, email, role, company, company_domain, summary, phone, tags)`
- `write_communication(date, subject_slug, subject, summary, participants, client_domain, comm_type, body, source_id)`
- `write_knowledge(topic_slug, summary, kind, client_domain, contact_email, body, date)`

**Key script behaviours:**
- Check `if path.exists(): return` — never overwrite existing files (dedup)
- Use human-readable filenames (see basalt-format.md filename conventions)
- Keep machine IDs in frontmatter (`id` field) for sync
- Update `~/.cortex/state.json` totals and run history at the end
- Print each file written for progress tracking

**Data goes directly in the script** as Python data structures — not loaded from a JSON file. Claude populates the data arrays from Phase 1 analysis:

```python
clients = [
    ("bigcolour.com.au", "Big Colour", "signage",
     "Signage company. Justin is director. Active client with L2Chat agent.",
     [("Justin Big Colour", "Director")]),
    # ... more clients
]

for domain, name, industry, summary, contacts in clients:
    write_client(domain, name, industry, summary, contacts)
```

### Common Arguments

| Argument | Effect |
|----------|--------|
| `--dry-run` | Print what would be written, don't touch disk |
| `--from YYYY-MM-DD` | Only process items from this date onward |
| `--batch-size N` | Process N items per run (default: 50) |
| `--source SOURCE` | Which source to mine |

### Environment

| Variable | Default | Purpose |
|----------|---------|---------|
| `CORTEX_DIR` | `~/Documents/basalt-cortex` | Vault root (syncs to basaltcortex.com) |
| `CORTEX_STATE` | `~/.cortex/state.json` | Cursor + run history |
| `CORTEX_OWNER_EMAIL` | `jeremy@jezweb.net` | Your email — excluded from contacts |

---

## Query Mode

Search across Basalt files. Claude can do this natively — no script needed.

### Commands

| What user says | Action |
|----------------|--------|
| "cortex search QUERY" | Grep frontmatter + content across all files |
| "what do I know about COMPANY" | Read `clients/{domain}.md` + find related comms and knowledge |
| "cortex contacts" | List all files in `contacts/` with name and email from frontmatter |
| "cortex client DOMAIN" | Full dossier — client file + linked contacts + recent comms + facts |
| "cortex export TYPE" | Export to CSV or JSON |

### Search Pattern

```bash
# Keyword search across all Basalt files
grep -rl "QUERY" ~/Documents/basalt-cortex/ --include="*.md"

# Frontmatter field search
grep -rl "client_domain: example.com" ~/Documents/basalt-cortex/ --include="*.md"
```

For structured queries, read frontmatter with Python `frontmatter` library or parse YAML between `---` markers.

---

## Stats Mode

```bash
echo "Clients:        $(find ~/Documents/basalt-cortex/clients -name '*.md' 2>/dev/null | wc -l)"
echo "Contacts:       $(find ~/Documents/basalt-cortex/contacts -name '*.md' 2>/dev/null | wc -l)"
echo "Communications: $(find ~/Documents/basalt-cortex/communications -name '*.md' 2>/dev/null | wc -l)"
echo "Knowledge:      $(find ~/Documents/basalt-cortex/knowledge -name '*.md' 2>/dev/null | wc -l)"
echo "Notes:          $(find ~/Documents/basalt-cortex/notes -name '*.md' 2>/dev/null | wc -l)"
```

Also read `state.json` for last run date, cursor positions, and run history.

---

## Sync Mode

Files in `~/Documents/basalt-cortex/` auto-sync to basaltcortex.com via the `basalt-cortex` CLI tray daemon. No manual sync needed.

The daemon uses chokidar to watch for file changes and pushes to the API with content hash comparison (skip unchanged files) and last-write-wins conflict resolution.

**Start daemon:** `basalt-cortex tray` (runs in system tray)
**Manual push:** `basalt-cortex push`
**Manual pull:** `basalt-cortex pull`
**Bidirectional:** `basalt-cortex sync` (watches local + polls remote every 30s)

---

## Scheduling

| Method | How |
|--------|-----|
| Claude Code Cowork | Scheduled task: "Run basalt-cortex mine gmail" > Daily |
| Cron | `0 6 * * * ANTHROPIC_API_KEY=sk-... python3 ~/.jez/scripts/cortex-mine-gmail.py` |
| `/loop` | `/loop 24h basalt-cortex mine gmail` |

## References

| When | Read |
|------|------|
| Before any file operations | [references/basalt-format.md](references/basalt-format.md) |
| When extracting semantic fields from threads | [references/field-catalog.md](references/field-catalog.md) |
| Per-source fetch and extract patterns | [references/source-patterns.md](references/source-patterns.md) |
| Before processing raw content | [references/prefilter-patterns.md](references/prefilter-patterns.md) |
| When syncing to Frond/D1/Vectorize | [references/sync-patterns.md](references/sync-patterns.md) |
