---
name: motherduck-ducklake
description: Decide when DuckLake is the right MotherDuck storage pattern. Use when evaluating fully managed DuckLake, BYOB, own-compute DuckLake access, data inlining, object-storage layout, or file-aware maintenance instead of native MotherDuck storage.
argument-hint: [storage-scenario]
license: MIT
---

# Use DuckLake on MotherDuck

Use this skill when the storage decision is genuinely about open table format and object-store behavior, not just about where to put another analytical table.

## Source Of Truth

- Prefer current MotherDuck DuckLake docs first.
- Use the upstream DuckLake and DuckDB extension docs only to clarify extension-level behavior that MotherDuck docs reference.
- Keep the guidance aligned with the documented product posture:
  - native MotherDuck first
  - MotherDuck supports DuckLake 1.0, but DuckLake remains an opt-in storage decision
  - fully managed, BYOB, and own-compute paths are distinct
  - maintenance and compaction are explicit operations, not background magic

## Default Posture

- Start with native MotherDuck storage unless there is a concrete DuckLake requirement.
- Reach for DuckLake when you need open-table-format semantics, object storage as the source of truth, BYOB, or file-aware maintenance.
- Do not recommend DuckLake just because a workload is "large"; MotherDuck's docs explicitly note native storage is often faster for reads.
- Choose the operating mode deliberately: fully managed for easiest evaluation, BYOB for customer bucket ownership, own compute only when the compute boundary matters too.
- For DuckLake 1.0 compatibility or extension behavior, verify the current DuckDB/DuckLake version matrix before giving syntax guarantees.
- Keep the MotherDuck product surface separate from raw DuckLake-extension assumptions.

## Workflow

1. Confirm why native MotherDuck storage is insufficient.
2. Pick the operating mode: fully managed, BYOB with MotherDuck compute, or BYOB with own compute.
3. Verify regional and bucket constraints before proposing BYOB.
4. Define the ingestion and maintenance posture up front, including data inlining, file compaction, and cleanup expectations.
5. Validate who will query the data and from which compute surface before finalizing the architecture.

## Open Next

- `references/DUCKLAKE_PLAYBOOK.md` for the mode decision matrix, MotherDuck-specific SQL patterns, BYOB constraints, data-inlining behavior, maintenance functions, and common DuckLake mistakes

## Related Skills

- `motherduck-connect` for choosing native DuckDB versus Postgres-endpoint access paths
- `motherduck-load-data` when the real issue is ingestion rather than storage format
- `motherduck-model-data` when the user still needs analytical table design after the storage decision
- `motherduck-build-data-pipeline` when DuckLake is just one part of a broader ingestion-to-serving workflow
