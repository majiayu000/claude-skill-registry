---
name: motherduck-ducklake
description: Decide when DuckLake is the right MotherDuck storage pattern. Use when evaluating fully managed DuckLake, BYOB, own-compute DuckLake access, data inlining, object-storage layout, or file-aware maintenance instead of native MotherDuck storage.
license: MIT
---

# Use DuckLake on MotherDuck

Use this skill when the storage decision is genuinely about open table format and object-store behavior, not just about where to put another analytical table.

## Source Of Truth

- Prefer current MotherDuck DuckLake docs first.
- Use the upstream DuckLake and DuckDB extension docs only to clarify extension-level behavior that MotherDuck docs reference.
- Keep the guidance aligned with the documented product posture:
  - native MotherDuck first
  - upstream DuckLake v1.0 is production-ready and supported by DuckDB 1.5.2, while MotherDuck's DuckLake docs still define the MotherDuck product surface and preview/compatibility limits
  - fully managed, BYOB, and own-compute paths are distinct
  - maintenance and compaction are explicit operations, not background magic

## Default Posture

- Start with native MotherDuck storage unless there is a concrete DuckLake requirement.
- Reach for DuckLake when you need open-table-format semantics, object storage as the source of truth, BYOB, or file-aware maintenance.
- Do not recommend DuckLake just because a workload is "large"; MotherDuck's docs explicitly note native storage is often faster for reads.
- Choose the operating mode deliberately: fully managed for easiest evaluation, BYOB for customer bucket ownership, own compute only when the compute boundary matters too.
- Document the fallback to native MotherDuck storage if the DuckLake requirement is weak, unverified, or only about future portability.
- For DuckLake v1.0, data inlining, sorted tables, bucket partitioning, deletion vectors, or extension behavior, verify the current MotherDuck DuckLake docs and DuckDB/DuckLake version matrix before giving syntax guarantees.
- Do not infer MotherDuck client/runtime support from upstream DuckDB release notes alone; check the MotherDuck lifecycle docs when the exact DuckDB version matters.
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
