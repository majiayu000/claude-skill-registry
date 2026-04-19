---
name: motherduck-share-data
description: Create and manage MotherDuck data shares for zero-copy data distribution. Use when sharing databases with team members, other organizations, or making data publicly available.
license: MIT
---

# Share Data with MotherDuck

Use this skill when you need to distribute a MotherDuck database without copying data. Shares are read-only, zero-copy database clones and should be treated as explicit provisioning operations.

## Source Of Truth

- Prefer the current MotherDuck sharing docs and SQL reference first.
- If the MotherDuck MCP `ask_docs_question` feature is available, use it before falling back to public docs.
- Keep the sharing model aligned with the documented behavior:
  - zero-copy and metadata-only
  - database-granularity sharing
  - read-only recipients
  - owner-controlled update mode

## Prerequisites

- MotherDuck connection established via `motherduck-connect`
- Source database identified via `motherduck-explore`
- Share SQL validated via `motherduck-query`

## Default Posture

- Default internal sharing to `ACCESS ORGANIZATION`, `VISIBILITY DISCOVERABLE`, and `UPDATE AUTOMATIC`.
- Use `UPDATE MANUAL` when the recipient needs a stable snapshot or versioned delivery.
- Use `ACCESS RESTRICTED` or `VISIBILITY HIDDEN` when distribution should stay tightly controlled.
- For write-heavy publishers, current clients with DuckDB 1.5+ reduce checkpoint blocking during share-update workflows; verify client versions before relying on concurrent checkpoint behavior.
- Never treat a share as row-level security. Shares operate at database granularity.

## Workflow

1. Identify the exact database to publish and who should consume it.
2. Decide sensitivity, discoverability, and freshness requirements before writing SQL.
3. Create the share with explicit access, visibility, and update settings.
4. If access is restricted, grant readers explicitly. If the share is hidden or link-based, distribute the share URL directly.
5. Have recipients `ATTACH` the shared database and query it read-only.
6. If the share uses `UPDATE MANUAL`, the owner runs `UPDATE SHARE` and consumers run `REFRESH DATABASE` when a new snapshot is ready.

## Open Next

- `references/SHARE_PLAYBOOK.md` for the full SQL playbook, access/update decision matrix, consumer workflow, and common failure modes

## Related Skills

- `motherduck-connect` for MotherDuck authentication and connection setup
- `motherduck-explore` for discovering databases, tables, columns, and existing shares
- `motherduck-query` for validating share SQL and downstream queries
- `motherduck-duckdb-sql` for DuckDB SQL syntax and lookup support
