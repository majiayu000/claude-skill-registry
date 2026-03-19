---
name: basalt-cortex
description: "Mine knowledge from Gmail, Google Chat, Slack, Drive, local files, MCP servers, and web into an Obsidian-compatible vault (~/.cortex/). Basalt format: markdown files with YAML frontmatter for clients, contacts, communications, and knowledge facts. Opens directly in Obsidian, syncs to Frond. Triggers: 'run the cortex', 'mine emails', 'mine slack', 'mine chat', 'cortex init', 'cortex search', 'cortex stats', 'what do I know about', 'set up cortex', 'mine my inbox'."
compatibility: claude-code-only
---

# Basalt Cortex

Mine knowledge from multiple sources into Obsidian-compatible markdown files stored in `~/.cortex/`. Each file has structured YAML frontmatter. Open `~/.cortex/` in Obsidian at any time — it's a valid vault.

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
ls ~/.cortex/state.json 2>/dev/null && echo "EXISTS" || echo "FRESH"
```

If EXISTS: ask user — skip, reset (data loss warning), or continue (add missing folders only).

### Create structure

```bash
mkdir -p ~/.cortex/{clients,contacts,communications,knowledge,projects,notes,.obsidian}
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
// ~/.cortex/.obsidian/app.json
{ "newFileLocation": "folder", "newFileFolderPath": "notes" }
```

### Write 3 example notes

Create one example client, contact, and knowledge note in Basalt format so the user can see the structure. Use templates from [references/basalt-format.md](references/basalt-format.md).

Report the created structure to the user. Tell them to open `~/.cortex/` in Obsidian.

---

## Mine Mode

Extract knowledge from a source and write Basalt-format files.

### Source Selection

Ask or detect which source to mine:

| Source | Prerequisites | Fetch method |
|--------|-------------|-------------|
| **gmail** | `gws` CLI + auth | `gws gmail messages list`, `gws gmail messages get` |
| **google-chat** | `gws` CLI + auth | `gws chat spaces list`, `gws chat messages list` |
| **slack** | Slack MCP or API token | MCP tools or `curl` with token |
| **google-drive** | `gws` CLI + auth | `gws drive files list`, `gws drive files get` |
| **local** | — | `find` + `cat` on local directories |
| **mcp** | MCP server connected | MCP tool calls (brain_recall, vault recall, etc.) |
| **web** | Web scraper or fetch | WebFetch, Firecrawl, or browser automation |
| **calendar** | `gws` CLI + auth | `gws calendar events list` |
| **obsidian** | Existing vault path | Read `.md` files, normalise frontmatter to Basalt |

Default: `gmail` if no source specified.

### Prerequisites Check

```bash
# For Gmail/Chat/Drive/Calendar:
which gws || echo "MISSING: npm install -g @googleworkspace/cli"
# For AI extraction:
echo $ANTHROPIC_API_KEY | head -c 5 || echo "MISSING: set ANTHROPIC_API_KEY"
# Vault exists:
ls ~/.cortex/state.json 2>/dev/null || echo "NOT INITIALISED: run cortex init first"
```

### Extraction Workflow

For each source, the pattern is the same:

1. **Fetch** raw data (emails, messages, files, pages)
2. **Pre-filter** — skip automated content, check source_id against state.json processed list. See [references/prefilter-patterns.md](references/prefilter-patterns.md).
3. **AI Extract** — send content to an LLM with an extraction prompt (see below)
4. **Write** Basalt files — one `.md` file per entity with YAML frontmatter
5. **Update state** — add source_ids to processed list, update cursors and totals

### AI Extraction Prompt Pattern

Generate a script that sends each piece of raw content to an LLM with this prompt structure:

```
You are extracting structured knowledge from a [source type].
For each item, identify and output JSON for:

1. CONTACTS: people mentioned (name, email, role, company)
2. CLIENTS: businesses/organisations (name, domain, industry)
3. COMMUNICATIONS: the interaction itself (subject, participants, summary, type)
4. KNOWLEDGE: facts, decisions, preferences, commitments extracted from the content

For each entity, generate a `summary` field: 1-3 sentences, dense with names and context.
This summary is used for semantic search — make it specific and useful.

Output as JSON array of {type, data} objects.
```

### Basalt File Writing Pattern

For each extracted entity, write a markdown file with YAML frontmatter:

- **Path**: determined by type (see basalt-format.md)
- **ID**: deterministic — `client_{domain}`, `contact_{email_slug}`, `comm_{timestamp}_{hash}`
- **Upsert**: if file exists, merge (keep earlier `first_seen`, update `last_seen`, increment `thread_count`)
- **Wikilinks**: add `[[related]]` links between connected entities

See [references/basalt-format.md](references/basalt-format.md) for complete field specs per entity type.

### Script Generation

**Do NOT look for a pre-built script.** Generate a Python script in `.jez/scripts/` adapted to:
- The user's chosen source
- Their available tools (gws CLI, MCP servers, API keys)
- Their preferred LLM (Anthropic API, local Ollama, Workers AI)
- Batch size and date range from arguments

See [references/source-patterns.md](references/source-patterns.md) for per-source fetch + extract patterns.

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
| `CORTEX_DIR` | `~/.cortex` | Storage root |
| `ANTHROPIC_API_KEY` | — | For AI extraction |
| `CORTEX_BATCH_SIZE` | `50` | Items per run |
| `CORTEX_OWNER_EMAIL` | — | Your email — excluded from contacts |

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
grep -rl "QUERY" ~/.cortex/ --include="*.md"

# Frontmatter field search
grep -rl "client_domain: example.com" ~/.cortex/ --include="*.md"
```

For structured queries, read frontmatter with Python `frontmatter` library or parse YAML between `---` markers.

---

## Stats Mode

```bash
echo "Clients:        $(find ~/.cortex/clients -name '*.md' 2>/dev/null | wc -l)"
echo "Contacts:       $(find ~/.cortex/contacts -name '*.md' 2>/dev/null | wc -l)"
echo "Communications: $(find ~/.cortex/communications -name '*.md' 2>/dev/null | wc -l)"
echo "Knowledge:      $(find ~/.cortex/knowledge -name '*.md' 2>/dev/null | wc -l)"
echo "Notes:          $(find ~/.cortex/notes -name '*.md' 2>/dev/null | wc -l)"
```

Also read `state.json` for last run date, cursor positions, and run history.

---

## Sync Mode (Future)

Push Basalt files to Frond, D1, or Vectorize. See [references/sync-patterns.md](references/sync-patterns.md).

Not yet built — placeholder for when Frond API token auth is ready.

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
| Per-source fetch and extract patterns | [references/source-patterns.md](references/source-patterns.md) |
| Before processing raw content | [references/prefilter-patterns.md](references/prefilter-patterns.md) |
| When syncing to Frond/D1/Vectorize | [references/sync-patterns.md](references/sync-patterns.md) |
