---
name: dev-context-multi-repo
description: "Builds multi-repo context hubs and compiled markdown knowledge maps. Use when profiling repo portfolios or assembling LLM-ready cross-repo knowledge bases."
compatibility: Portable core. Works on Claude Code and Codex.
---

# Multi-Repo Context

Use this skill to inventory, normalize, and publish one coherent knowledge hub for many repositories. The strongest default is a two-layer system: raw source captures plus an LLM-maintained compiled markdown hub with profiles, concept pages, backlinks, and derived reports. It owns repo discovery, high-signal extraction, cross-repo inference, artifact-set generation, and knowledge-graph assembly. It does not replace single-repo context or code-graph work.

## Quick Reference

| Task | Use |
|------|-----|
| Discover repos and classify portfolio shape | `scripts/discover_repos.py`, [references/repo-discovery-patterns.md](references/repo-discovery-patterns.md) |
| Scan repos into normalized profiles | `scripts/scan_repo.py`, `scripts/scan_portfolio.py`, [references/repo-classification-rules.md](references/repo-classification-rules.md) |
| Build standard artifact set | `scripts/build_artifact_set.py`, [references/output-model-and-gap-analysis.md](references/output-model-and-gap-analysis.md) |
| Build and validate graph outputs | `scripts/build_knowledge_graph.py`, `scripts/validate_graph.py`, `scripts/check_graph_consistency.py`, [references/knowledge-graph-patterns.md](references/knowledge-graph-patterns.md) |
| Calibrate graph edge weights from evidence | `scripts/calibrate_weights.py`, [references/knowledge-graph-patterns.md](references/knowledge-graph-patterns.md) |
| Query graph neighborhoods, paths, impact, rank, PPR, and communities | `scripts/query_graph.py --node\|--from\|--impact\|--rank\|--ppr\|--communities`, [references/knowledge-graph-patterns.md](references/knowledge-graph-patterns.md) |
| Detect communities (Louvain) and generate per-community summaries | `scripts/query_graph.py --communities --resolution`, [assets/community-summary-template.md](assets/community-summary-template.md) |
| Bitemporal time-slice queries | `scripts/query_graph.py --as-of <date> --known-at <date>`, [references/knowledge-graph-patterns.md](references/knowledge-graph-patterns.md) §12 |
| Create or operate a coordination hub | [assets/coordination-repo-layout-template.md](assets/coordination-repo-layout-template.md), [references/hub-operations-playbook.md](references/hub-operations-playbook.md) |
| Run a raw-ingest to compiled-wiki loop | the `docs-notes-retrieval` skill, [references/hub-design-patterns.md](references/hub-design-patterns.md), [references/hub-operations-playbook.md](references/hub-operations-playbook.md) |
| Freshness and drift checks | `scripts/report_drift.py`, `scripts/check_hub_freshness.sh`, [references/hub-freshness-checking.md](references/hub-freshness-checking.md) |

## When to Use

- Build a master context repo or docs hub for many services or repositories.
- Produce one normalized profile per repo instead of ad hoc summaries.
- Generate consistent repo descriptions from structured JSON profiles and graph edges instead of freehand summaries.
- Classify complex orchestration repos such as agent runtimes, remote bridges, terminal-first CLIs, plugin hosts, and worktree coordinators without collapsing them into `unknown`.
- Map stacks, interfaces, dependencies, owners, and integration edges across a portfolio.
- Generate hub artifacts for onboarding, migration planning, architecture review, or RAG.
- Retrofit a knowledge graph onto an existing coordination hub.
- Operate a `raw/` evidence layer plus a compiled markdown wiki for a repo portfolio.
- Maintain or refresh a large repo portfolio, including 100+ repo hubs where incremental compilation matters more than one-shot summarization.

## Recreate a Requirements-Hub

A ready-to-copy blank hub ships at [assets/hub-scaffold/](assets/hub-scaffold/). It is the same shape this skill produces — hot layer (`AGENTS.md`, `rules/`), compiled layer (`context/`), and one example domain folder — with zero organization-specific content.

```bash
cp -r assets/hub-scaffold ~/repos/requirements-hub
```

Then follow [assets/hub-scaffold/context/scripts/README.md](assets/hub-scaffold/context/scripts/README.md) for the end-to-end command sequence: `discover_repos.py` → `scan_portfolio.py` → `build_knowledge_graph.py` → `query_graph.py --rank` → `validate_graph.py`, then build/validate the hub's own context graph with the reused `dev-context-engineering` scripts. The scaffold's `rules/` stubs point at the clearly-labelled generic templates in `dev-context-engineering/assets/` — swap each regime reference for your own regulatory context.

## Route Elsewhere

- Single-repo context layers and rollout across tools: use [dev-context-engineering](../dev-context-engineering/SKILL.md).
- Symbol or file graph inside one repo: use [dev-context-code-graph](../dev-context-code-graph/SKILL.md).
- Spec writing or decision docs: use [docs-ai-prd](../docs-ai-prd/SKILL.md).
- Documentation freshness audits: use [qa-docs-coverage](../qa-docs-coverage/SKILL.md).
- Parallel discovery across many repos with explicit delegation: use [agents-swarm-orchestration](../agents-swarm-orchestration/SKILL.md).

## Defaults

- Structured metadata first, narrative second.
- One canonical profile per repo.
- Raw ingest first, compiled wiki second.
- Treat repo knowledge as the system of record and keep root agent files as maps, not encyclopedias.
- Use just-in-time loading by default: store stable identifiers, paths, graph node IDs, and report links, then load the relevant artifact at task time.
- High-signal file reads before deep reads.
- Separate raw evidence, normalized metadata, and human summaries.
- Prefer markdown-native index pages, summaries, and backlinks before adding heavier retrieval layers.
- Let the LLM maintain the compiled hub; humans review, prune, and correct drift instead of hand-editing every page.
- File durable answers, diagrams, and reports back into the hub so portfolio queries compound over time.
- Treat hidden differentiators as first-class extraction targets: transport model, control plane, permission bridge, session lifecycle, worktree model, plugin lifecycle, and recovery policy are often more important than language or package metadata.
- Mark claims as `verified`, `subset-verified`, `inferred`, or `unverified` when coverage is incomplete.
- Keep generated artifacts under one artifact root instead of scattering them through docs.
- Do not create free-floating Markdown reports for every portfolio query; route reusable outputs into the hub catalog, reports lifecycle, or generated context artifact set.

## May 2026 Stance

The current best default is not "index everything and stuff it into a prompt." Build a small, navigable context system that can select the right evidence at runtime.

- Keep `AGENTS.md` and sibling runtime files short; they should route agents to the hub, not duplicate the hub.
- Make structured artifacts the compiler inputs: profiles, code graphs, system edges, freshness reports, and evidence refs.
- Make markdown the operator surface: catalog pages, concept notes, architecture maps, and reusable query outputs.
- Use graph traversal when relationship structure changes the answer: dependency paths, ownership, blast radius, shared providers, cross-repo flows, migration seams, or "catch me up on this system" questions.
- Use lexical search, index pages, or direct file reads for simple lookup questions; graph-first retrieval for every query adds latency and noise.
- Use Personalized PageRank when the question is seeded by a repo/domain/process but needs budget-bounded context beyond a 1-2 hop neighborhood.
- Use community detection (`--communities`) at multiple resolutions when the question is global ("what does the platform look like?") and a single-seed walk would miss the structure. Drop in Leiden via `igraph` or `graspologic` when you need stronger connectedness guarantees on portfolios > 1k nodes.
- Calibrate weights when prose, Mermaid, manifests, and schemas all contribute edges; direct multi-source evidence should outrank single-source prose edges.
- Keep symbol-level graphs as per-repo artifacts from `dev-context-code-graph`; import summaries or links into the hub instead of merging every symbol into the portfolio graph.
- Apply context-hygiene gates before publishing: relevance, provenance, freshness, ACL/sensitivity scope, contradiction risk, and bounded token shape.
- Prefer dynamic pruning of irrelevant graph communities or subgraphs over static "include the whole graph" prompts.

## Workflow

1. Inventory candidate repos and classify repo shape.
2. Index raw evidence first: repo roots, architecture docs, API contracts, datasets, screenshots, and other source captures should live in a raw layer instead of being flattened into summaries.
3. Read only high-signal manifests, docs, CI files, schema clues, and instruction artifacts.
4. Normalize evidence into one `RepoProfile` per repo.
5. If the repo appears to be an orchestration-heavy runtime, deepen the scan around transport, remote/session, approval, worktree, plugin, and recovery files before accepting a generic classification.
6. Infer repo kind, interfaces, dependencies, storage, ownership, and capability families without overclaiming.
7. Generate or refresh one repo description per repo from the normalized profile and relationship edges, with confidence labels derived from evidence coverage.
8. Compile the markdown hub incrementally: repo catalog pages, cross-repo concept notes, backlinks, and index files that help the agent navigate without scanning the whole corpus every time.
9. Rebuild only the changed pages, indexes, and graph edges when possible; do not re-summarize the whole portfolio by default.
10. Materialize the artifact set: profiles, catalog pages, graphs, and reports.
11. Validate graph consistency and freshness, then run hub health checks for stale claims, missing summaries, unindexed reports, and candidate pages worth adding before calling the hub current.

## ASCII Flow

```text
multi-repo context request
  -> discover repos and classify portfolio shape
  -> ingest raw evidence without flattening it into prose
  -> scan high-signal files into one RepoProfile per repo
  -> build compiled hub: catalog pages, indexes, backlinks, reports
  -> build graph artifacts: system edges and knowledge graph
  -> query with lexical search, direct reads, graph paths, PPR, or communities
  -> validate coverage, freshness, consistency, and unindexed outputs
  -> publish only durable hub artifacts, not free-floating reports
```

## Core Decisions

### Output Model

Default artifact set:
- `profiles/<repo>.json`
- `catalog/<repo>.md`
- `graphs/system-edges.json`
- `graphs/knowledge-graph.json`
- `reports/coverage.md`
- `reports/drift.json`

Do not invent alternate shapes unless there is a downstream consumer that requires a transform layer.

Treat `catalog/` and `reports/` as the compiled markdown layer by default. Add folders such as `concepts/` or `research/` only when there is a clear downstream consumer for concept articles or query outputs.

The repo description page should usually be generated from:
- verified fields in `profiles/<repo>.json`
- relationship edges from `graphs/system-edges.json`
- a bounded set of direct evidence references

Do not let the description page become an ungrounded prose summary.

For complex repos, the profile should capture capability families rather than only surface metadata. A strong profile often needs fields or derived sections for:
- runtime or deployment mode
- control-plane and transport model
- remote or bridge responsibilities
- session and resume semantics
- permission and approval path
- worktree or parallel-task isolation model
- plugin, hook, or hot-reload lifecycle
- recovery or retry policy

### Extraction Strategy

Start from files that reveal repo reality quickly:
- manifests and lockfiles
- CI workflows
- container and infra files
- native/mobile project manifests such as `Package.swift`, `project.yml`, `.xcodeproj`, and `.xcworkspace`
- schema and migration files
- API contracts
- repo instruction files
- specs and plans

If the hub also stores non-repo evidence, keep those captures in the raw layer and summarize them into the compiled hub rather than treating screenshots, exports, or article clips as first-class catalog pages.

Use deep reads only when the high-signal layer is insufficient to classify the repo or prove an integration.

For orchestration-heavy repos, the high-signal layer must include runtime spine files, not just manifests:
- transport implementations
- remote bridge or client/server session managers
- permission and approval bridge code
- worktree and task orchestration setup
- plugin, hook, and hot-reload loaders
- reconnect, backpressure, batching, and recovery logic

Many of the most important differentiators are invisible in package metadata. If the extractor only sees language, lockfiles, and README text, it will under-classify repos that actually win on runtime design.

### Complex Runtime Classification

When a repo contains files or modules for multiple of the following, prefer a complex-runtime classification over `unknown`:
- remote bridge or remote execution support
- explicit transport abstractions such as SSE, WebSocket, or hybrid read/write transport
- session manager or resume lifecycle
- permission or approval mediation
- task, coordinator, teammate, or worker orchestration
- worktree creation, branch isolation, or tmux/session bootstrapping
- plugin, hook, or lazy-loader infrastructure
- explicit recovery, retry suppression, buffering, or backpressure mechanisms

Typical classifications worth recognizing:
- agent runtime
- coding-agent CLI
- remote execution bridge
- terminal UI host
- plugin platform
- multi-repo coordinator

### Verification Scope

Before synthesis:
- separate direct evidence from inferred structure
- avoid portfolio-wide universal claims unless every relevant repo was checked
- verify storage engines from manifests and drivers, not from README prose
- mark partial coverage explicitly in summaries and tables

For generated repo descriptions:
- distinguish what is proven from manifests or workflows vs what is inferred from naming or topology
- prefer concise, structured descriptions over narrative confidence theater
- include unknowns explicitly when a repo cannot be confidently classified

### Knowledge Graph

Use the knowledge graph when the hub needs queryable relationships across repos, systems, and artifacts. Keep symbol-level graph work out of this layer; that belongs to single-repo code-graph workflows.

The graph complements the markdown hub; it does not replace it. The best default is graph-backed markdown pages with backlinks, index notes, and concise summaries that an agent can read directly at small and medium corpus sizes.

For complex runtimes, add capability and behavior edges, not just dependency edges. Useful examples:
- `uses_transport`
- `splits_read_write_channels`
- `supports_resumable_streams`
- `bridges_permissions`
- `manages_remote_sessions`
- `supports_worktree_isolation`
- `supports_plugin_hot_reload`
- `serializes_writes`
- `buffers_stream_events`
- `has_recovery_policy`

### Q&A and Derived Outputs

Prefer answers as files, not terminal-only output:
- markdown reports for architecture questions or migration maps
- Mermaid or other diagrams for relationship views
- slide or image outputs when a viewer exists and the question is presentation-heavy

If an answer will likely be useful again, file it back into the hub and link it from the relevant repo or concept page.

Before adding the file, run the hub placement test:
- does this belong in an existing repo catalog, concept page, or report?
- will it be linked from the hub index or related repo page?
- is it generated from structured inputs, and if so is the rebuild command known?
- does it have a lifecycle state if it is a point-in-time analysis?

If not, keep it in the task thread or update an existing hub page.

### Operating at 100+ Repos

At large portfolio scale, optimize for maintenance loops, not heroic one-off scans:
- keep a registry of repos and last-refresh state
- compile incrementally instead of rebuilding every page on every run
- maintain short index pages that help the LLM find the right repo or concept quickly
- prefer JSON + markdown + graph artifacts that can be diffed, linted, and repaired
- add lightweight CLIs for search, freshness checks, and targeted rebuilds before reaching for heavier retrieval systems

### Hub Layout

Prefer a coordination repo with:
- root entry files
- domain folders at the root
- generated hub infrastructure under `context/` or `docs/context/`
- optional `raw/` capture areas for evidence the LLM compiles into the hub

Keep the root navigation-focused. Do not paste inventories into `AGENTS.md`.

For native/mobile repos, the default scanner should classify from high-signal project files before falling back to generic language heuristics. Swift/Xcode repos should resolve cleanly as `app` repos when `project.yml`, `.xcodeproj`, or `.xcworkspace` evidence is present, and scans should ignore generated build trees such as `.build`, `DerivedData`, `Pods`, and `SourcePackages`.

## Output Modes

Default to one of these:

- Portfolio inventory:
  repo registry, classifications, and scan coverage.
- Context hub:
  profiles, catalog pages, relationship edges, and knowledge graph.
- Compiled wiki:
  raw evidence registry, markdown indexes, concept notes, backlinks, and reusable query outputs.
- Repo description set:
  one grounded page per repo compiled from profile JSON, graph edges, and verified evidence.
- Capability map:
  per-repo runtime capabilities, differentiators, and operational behaviors derived from source evidence rather than README-level summaries.
- Migration map:
  active vs legacy systems, integration edges, and transition hotspots.
- Freshness report:
  drift, stale documents, and re-verification queue.

## Known Traps

- Accepting a generic repo classification too early and missing the operational behavior that actually distinguishes orchestrators, bridges, or control planes.
- Reading README-heavy repos as if they were authoritative when manifests, workflows, and runtime scripts say something else.
- Rebuilding the full hub on every scan instead of compiling incrementally from the repos that actually changed.
- Letting inferred cross-repo edges harden into "facts" before they are traced back to manifests, schemas, or concrete integration evidence.
- Using portfolio summaries as the source of truth while raw evidence and normalized profiles quietly drift underneath them.
- Treating a longer model context window as permission to load the whole hub; large irrelevant context still causes distraction and context rot.
- Applying GraphRAG or graph traversal to every question even when a direct catalog lookup, lexical search, or bounded file read is more accurate.
- Letting generated markdown and generated JSON drift independently instead of regenerating prose from the structured profile and graph contracts.
- Re-ingesting LLM-generated summaries as fresh evidence without keeping the original source and timestamp.

## Anti-Patterns

- Treating one repo summary as a portfolio model.
- Claiming complete coverage without a verified scan registry.
- Mixing raw evidence, normalized data, and commentary in the same file.
- Verifying storage or runtime claims from docs instead of manifests.
- Leaving useful portfolio answers in chat output instead of filing them back into the hub.
- Pasting portfolio inventories into root agent-memory files.
- Forcing symbol-level code graphs into the portfolio knowledge graph.
- Reaching for heavy RAG before maintaining index pages, concise summaries, and backlinks.
- Rebuilding 130 repo descriptions from scratch when only a subset changed.
- Writing repo descriptions directly from chat impressions instead of profile JSON and graph edges.
- Letting complex repos remain `unknown` because the scanner only looked at manifests and README text.
- Modeling only dependency edges and missing operational edges such as permission bridges, session control planes, resumable streams, or worktree isolation.
- Using a vector database, GraphRAG stack, or MCP server as a substitute for repo-owned profiles, evidence refs, and freshness checks.
- Publishing "complete codebase context" claims without parse coverage, scan date, excluded paths, and unsupported-language notes.
- Mixing public docs, private code evidence, secrets, and customer data in one context layer without sensitivity labels and access boundaries.

## Navigation

- Core references: [references/repo-discovery-patterns.md](references/repo-discovery-patterns.md), [references/repo-classification-rules.md](references/repo-classification-rules.md), [references/architecture-inference-rules.md](references/architecture-inference-rules.md), [references/integration-signal-detection.md](references/integration-signal-detection.md), [references/confidence-scoring.md](references/confidence-scoring.md)
- Hub and graph operations: [references/output-model-and-gap-analysis.md](references/output-model-and-gap-analysis.md), [references/knowledge-graph-patterns.md](references/knowledge-graph-patterns.md), [references/hub-design-patterns.md](references/hub-design-patterns.md), [references/hub-operations-playbook.md](references/hub-operations-playbook.md), [references/hub-freshness-checking.md](references/hub-freshness-checking.md), [references/large-portfolio-strategy.md](references/large-portfolio-strategy.md)
- [references/network-science-applied.md](references/network-science-applied.md) — Centrality, PageRank, community detection, contagion applied to multi-repo knowledge graphs and portfolio topology.
- Assets: [assets/hub-scaffold/](assets/hub-scaffold/) (copy-paste blank hub — see "Recreate a Requirements-Hub"), [assets/coordination-repo-layout-template.md](assets/coordination-repo-layout-template.md), [assets/repo-catalog-page-template.md](assets/repo-catalog-page-template.md), [assets/architecture-map-template.md](assets/architecture-map-template.md), [assets/integration-matrix-template.md](assets/integration-matrix-template.md), [assets/freshness-report-template.md](assets/freshness-report-template.md), [assets/legacy-transition-map-template.md](assets/legacy-transition-map-template.md), [assets/hub-agents-template.md](assets/hub-agents-template.md)
- Scripts and schemas: `scripts/discover_repos.py`, `scripts/scan_repo.py`, `scripts/scan_portfolio.py`, `scripts/build_artifact_set.py`, `scripts/build_hub_views.py`, `scripts/build_knowledge_graph.py`, `scripts/query_graph.py`, `scripts/validate_profiles.py`, `scripts/validate_graph.py`, `scripts/check_graph_consistency.py`, `scripts/report_drift.py`, `scripts/check_hub_freshness.sh`, [schemas/repo-profile.schema.json](schemas/repo-profile.schema.json), [schemas/knowledge-graph.schema.json](schemas/knowledge-graph.schema.json), [schemas/system-edge.schema.json](schemas/system-edge.schema.json)

## Fact-Checking

- Known bugs, regressions, framework/compiler/runtime footguns, and version-specific crash or workaround guidance must be verified against current primary web sources before being treated as current fact.
- External source mapping lives in [data/sources.json](data/sources.json).
- Portfolio summaries must distinguish verified facts from inferred edges.
- If a claim cannot be traced to a manifest, schema, workflow, or other direct evidence, label it accordingly instead of hardening it into a fact.

