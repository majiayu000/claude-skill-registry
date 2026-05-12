<!-- SOURCE-OF-TRUTH: shared/references/mcp_tool_preferences.md. Edit ONLY here; run `node tools/marketplace/shared.mjs sync` -->

# Tool Preferences for Code Work

Compact hard rules for skills that materially inspect or edit repository code, config, scripts, or tests.

## Primary Policy

- Use `hex-line` first for repository text reads/search/edits when available.
- Use `hex-graph` first only for semantic code questions: symbol identity, references, architecture, edit blast radius, clone groups, or semantic diff risk.
- Use `hex-research` first only for project researchgraph questions: hypotheses, goals, benchmark runs, evidence, lineage, goal alignment, proposal readiness, or graph drift.
- Use built-in Read/Edit/Write/Grep/Glob or shell only when MCP is unavailable, unsupported, outside scope, or the task is shell-native.
- Do not use repo-wide shell search/read patterns when `hex-line` or `hex-graph` covers the task.
- Do not require `hex-graph` for docs, community, external research, runtime execution, profiling, benchmarking, or other work that does not depend on semantic code structure.
- Do not require `hex-research` unless the project has `docs/hypotheses/`, `docs/goals/`, or `benchmark/runs/*/manifest.yaml` and graph state can change the decision.

## Minimal Flow

| Need | Preferred flow |
|------|----------------|
| Discover files | `inspect_path` with a narrow path |
| Search text | `grep_search(output_mode="summary")`, then narrow before content mode |
| Read code | `outline` or targeted `read_file`; use edit-ready reads only before verified edits |
| Edit code | `read_file(edit_ready=true)` -> `edit_file(base_revision)` -> verify/check changes |
| Semantic risk | `index_project` -> symbol/architecture/edit-region analysis |
| Researchgraph status | `verify_index` -> targeted hypothesis/goal/run query or audit |

## Fallback Contract

Fallbacks are valid for Git history, builds, tests, package managers, containers, images, PDFs, notebooks, external websites, binary/media files, paths outside the project root, unsupported languages, unavailable MCP servers, missing researchgraph layout, or small markdown/metadata reads where MCP setup adds no value.

When falling back, keep the scope narrow and preserve the same evidence standard.

---
**Version:** 5.0.0
**Last Updated:** 2026-03-20
