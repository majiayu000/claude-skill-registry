---
name: cortex-mine
description: >
  Mine Gmail history into a local flat-file knowledge base (~/.cortex/).
  Use when asked to "run the cortex", "mine emails", "cortex run", "cortex dry run",
  "set up the cortex", "cortex from DATE", or "mine my inbox".
  Extracts contacts, clients, communications and knowledge facts into portable JSONL/JSON files.
  Requires gws CLI and ANTHROPIC_API_KEY.
compatibility: claude-code-only
---

# Knowledge Cortex — Mine

Mine your Gmail history into structured flat files — contacts, clients, communications, and key facts — stored in `~/.cortex/`. No server required. Files you own.

## When invoked

Read `{skill_path}/references/file-schema.md` for the storage format before any file operations.

## Commands

| What user says | Action |
|----------------|--------|
| "run the cortex" / "cortex run" | Run mining pass |
| "cortex dry run" | Mine without writing — pass `--dry-run` |
| "cortex from DATE" | Mine from specific date — pass `--from YYYY-MM-DD` |
| "set up the cortex" | Run first-time setup |

## Setup (first run)

Check prerequisites:
```bash
which gws || echo "MISSING: npm install -g @googleworkspace/cli"
python3 -c "import anthropic" 2>/dev/null || echo "MISSING: pip install anthropic"
ls ~/.cortex/state.json 2>/dev/null || echo "FIRST RUN"
```

If `gws` missing: tell user `npm install -g @googleworkspace/cli` then `gws auth setup`.
If `anthropic` missing: tell user `pip install anthropic` (or `pip install anthropic --break-system-packages` on managed Python).
If first run: initialise storage.

```bash
mkdir -p ~/.cortex/originals
echo '{}' > ~/.cortex/contacts.json
echo '{}' > ~/.cortex/clients.json
touch ~/.cortex/communications.jsonl ~/.cortex/knowledge.jsonl ~/.cortex/files.jsonl
```

Write `~/.cortex/state.json`:
```json
{"version":"1.0","cursors":{"gmail":null},"last_run":null,"totals":{"contacts":0,"clients":0,"communications":0,"knowledge":0,"files":0},"runs":[]}
```

## Mining

```bash
python3 {skill_path}/scripts/cortex-mine.py
python3 {skill_path}/scripts/cortex-mine.py --dry-run
python3 {skill_path}/scripts/cortex-mine.py --from 2024-01-01
python3 {skill_path}/scripts/cortex-mine.py --batch-size 25
```

The script prints a run report on completion. Show it to the user verbatim.

**Common errors:**
- `gws: command not found` — install gws CLI
- `AuthError` / `403` — run `gws auth setup`
- `ANTHROPIC_API_KEY not set` — set env var or add to `~/.cortex/.env`
- `ModuleNotFoundError: anthropic` — `pip install anthropic`

## Scheduling

- Claude Code Desktop: Cowork > Scheduled > New Task > `Run the cortex-mine skill` > Daily
- CLI: `/loop 24h run the cortex-mine skill`
- Cron: `0 6 * * * cd ~ && ANTHROPIC_API_KEY=sk-... python3 /path/to/cortex-mine.py`

## Exporting data

See `{skill_path}/references/export-adapters.md` for patterns to export cortex data to Obsidian, SQLite, Notion, CRM systems, or custom APIs.

## Environment

| Variable | Default | Purpose |
|----------|---------|---------|
| `CORTEX_DIR` | `~/.cortex` | Storage root |
| `ANTHROPIC_API_KEY` | — | Required for extraction |
| `CORTEX_BATCH_SIZE` | `50` | Threads per run |
| `CORTEX_OWNER_EMAIL` | — | Your email — excluded from contacts |

## References

- File schemas: `{skill_path}/references/file-schema.md`
- Pre-filter rules: `{skill_path}/references/prefilter-patterns.md`
- Export patterns: `{skill_path}/references/export-adapters.md`
