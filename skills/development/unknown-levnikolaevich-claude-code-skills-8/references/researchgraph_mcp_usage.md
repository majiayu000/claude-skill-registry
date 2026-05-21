<!-- SOURCE-OF-TRUTH: shared/references/researchgraph_mcp_usage.md. Edit ONLY here; run `node tools/marketplace/shared.mjs sync` -->

# Research Graph MCP Usage

<!-- SCOPE: Routing policy for using hex-research MCP against hypothesis, goal, evidence, and benchmark graphs. -->

## Applicability

Use `hex-research` only when project evidence can change planning, validation, readiness, scope, or priority and the project has at least one canonical graph path: `docs/hypotheses/*.md`, `docs/goals/*.md`, or `benchmark/runs/*/manifest.yaml`.

Do not use it for code symbol identity, references, architecture, or edit blast radius; those remain `hex-graph` concerns.

## Safety Rules

- Prefer read-only query/audit tools first.
- Start with `verify_index({ path })`.
- Run `index_hypotheses({ path })` only when the index is missing, stale, explicitly requested, or current graph state is required.
- Treat `STALE` as graph debt, not tool failure.
- Treat `INVALID` from `verify_index` as diagnostic state; `INVALID` from `index_hypotheses` means rebuild failed.
- Goal `metrics_current` is derived from explicit comprehensive run manifests; manual `metrics_current` in goal frontmatter is drift.
- Source quality is derived from `sources`, optional `docs/sources/lib.yaml`, source type inference, and weighted `evidence_depth`.
- Run `export_canvas` and `export_research_map` with `dry_run: true` before writing.
- If MCP is unavailable, read split markdown/manifests manually and mark confidence degraded.

## Intent Routing

| Intent | Tool |
|--------|------|
| freshness | `verify_index` |
| rebuild/first index | `index_hypotheses` |
| hypothesis search/status | `find_hypotheses` |
| inspect `H##` / `G##` | `inspect_hypothesis` / `inspect_goal` |
| evidence, citations, benchmark runs | `find_evidence`, `find_runs` |
| lineage, graph shape, goal tree | `trace_lineage`, `analyze_topology`, `trace_goal_tree` |
| gaps, drift, readiness | `audit_orphans`, `audit_goal_alignment`, `analyze_progress`, `analyze_proposed` |
| goal metric drift / missing comprehensive metrics | `inspect_goal`, `audit_goal_alignment` |
| source quality / evidence depth | `inspect_hypothesis`, `find_evidence`, `analyze_proposed` |
| field-level diff | `analyze_progress` |
| visual map / generated research-map.md | `export_canvas`, `export_research_map` |

## Integration Rules

- Planning/review skills use graph evidence only when H/G IDs, benchmark runs, readiness, or changed researchgraph files affect the decision.
- External-doc research still prioritizes official/current sources; graph evidence is local preflight only.
- Task planning keeps `hex-graph` for code modules and uses `hex-research` only for hypothesis/task readiness and proposal status.
- Manual fallback reads frontmatter in hypotheses/goals, narrowed benchmark manifests, and wiki links by direct file lookup; label lineage/topology/drift as manual approximations.

---
**Version:** 0.1.0
**Last Updated:** 2026-05-08
