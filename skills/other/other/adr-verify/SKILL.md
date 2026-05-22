---
name: adr-verify
description: Read back adr-patterns + adr-edges namespaces, surface dangling refs / supersede cycles / status mismatches; exit 1 on cycles
argument-hint: ""
allowed-tools: Bash mcp__claude-flow__memory_list mcp__claude-flow__memory_retrieve
---

# ADR Verify

Companion to `adr-index`. After import, reads the persisted graph and surfaces integrity issues:

- **Dangling refs** — edge points at an ADR ID that doesn't exist in `adr-patterns`. Common cause: the referenced ADR is in a sibling repo or got deleted.
- **Supersede cycles** — `ADR-A supersedes ADR-B` and `ADR-B supersedes ADR-A` (or longer cycles). Always data corruption.
- **Status mismatches** — an ADR is the source of a `supersedes` edge but its own status isn't `Superseded`. Usually a missed status update during a successor ADR's promotion.

## When to use

- Right after `adr-index` to confirm the graph is healthy
- In CI as a fail-closed gate (`VERIFY_STRICT=1` exits 1 on any issue)
- Before publishing an ADR-related release

## Steps

```bash
node plugins/ruflo-adr/scripts/verify.mjs
```

Optional env:
- `VERIFY_FORMAT=json` — JSON instead of markdown
- `VERIFY_STRICT=1` — exit 1 on ANY issue (default: only on cycles)

## Exit codes

| Code | Meaning |
|---|---|
| `0` | Graph healthy (or dangling refs / status mismatches present in non-strict mode) |
| `1` | Supersede cycle detected, OR strict mode + any issue present |

## Cross-references

- `adr-index` — populates the data this skill verifies
- `scripts/import.mjs` — has its own dry-run validation; this skill is the read-back companion
