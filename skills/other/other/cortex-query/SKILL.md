---
name: cortex-query
description: >
  Search and query your Knowledge Cortex (~/.cortex/).
  Use when asked to "cortex stats", "cortex search", "cortex client",
  "cortex contacts", "cortex export", "cortex prune",
  "search my knowledge base", or "what do I know about COMPANY".
  Queries portable JSONL/JSON files for contacts, clients, communications, and facts.
compatibility: claude-code-only
---

# Knowledge Cortex — Query

Search, browse, and export your Knowledge Cortex flat files.

## When invoked

Read `{skill_path}/references/file-schema.md` for the storage format.

## Commands

| What user says | Action |
|----------------|--------|
| "cortex stats" | Show knowledge base stats |
| "cortex search QUERY" | Search across all records |
| "cortex client DOMAIN" | Full dossier for a client |
| "cortex contacts [filter]" | List contacts |
| "cortex export TYPE" | Export contacts, clients, knowledge, or comms |
| "cortex prune" | Remove low-value records |

## Usage

```bash
python3 {skill_path}/scripts/cortex-query.py stats
python3 {skill_path}/scripts/cortex-query.py search "QUERY"
python3 {skill_path}/scripts/cortex-query.py client domain.com
python3 {skill_path}/scripts/cortex-query.py contacts [filter]
python3 {skill_path}/scripts/cortex-query.py export contacts --format csv
python3 {skill_path}/scripts/cortex-query.py export knowledge --format json
python3 {skill_path}/scripts/cortex-query.py prune --dry-run
python3 {skill_path}/scripts/cortex-query.py prune
```

Print output directly to the user.

## Environment

| Variable | Default | Purpose |
|----------|---------|---------|
| `CORTEX_DIR` | `~/.cortex` | Storage root |

## References

- File schemas: `{skill_path}/references/file-schema.md`
