---
name: claudemap-runtime
description: Internal ClaudeMap runtime for turning a repository into a live architecture map and driving that map during walkthroughs. Prefer the public commands in .claude/commands for normal use.
---

ClaudeMap is a repo-to-architecture-map workflow.

High-level model:

- snapshot the repository
- ask `@claudemap-architect` to turn that snapshot into a detailed, human-legible graph
- render the graph in the bundled ClaudeMap UI
- keep the graph and presentation state updated as the user explores the codebase

Public commands:

- `/setup-claudemap`: build or rebuild the map for the current repository
- `/open-claudemap`: reopen the existing UI without rebuilding
- `/create-map`: create or refresh a scoped subsystem map from the current root graph
- `/refresh`: update the graph after code changes
- `/explain`: run a guided walkthrough through the live map
- `/show`: direct the live map for highlights, focus, presentation, and flows

If this skill is invoked directly, default to the setup workflow.

Target repository:

- If the user passed an argument to the invoked skill command, use `$ARGUMENTS` as the project root.
- If no argument was passed, use the current working directory.

Execution rules:

1. Resolve the bundled ClaudeMap workspace from `${CLAUDE_SKILL_DIR}`.
2. Generate a raw repo snapshot by running `${CLAUDE_SKILL_DIR}/skill/commands/snapshot.js` for the target project root.
3. Read `${CLAUDE_SKILL_DIR}/skill/prompts/enrichment.txt`.
4. Use the `@claudemap-architect` subagent explicitly. Give it:
   - the raw snapshot JSON
   - the graph schema contract from the enrichment prompt
   - instructions to return only valid graph JSON
   - instructions to optimize for a detailed graph with intuitive human grouping
5. **Wait for the subagent Task call to fully return**, then save the returned JSON to `${CLAUDE_SKILL_DIR}/tmp/claudemap-enrichment.json`. Do not run the setup JS command until after this file has been written with non-empty valid graph JSON. Do not run setup in parallel with the subagent call.
6. Run `${CLAUDE_SKILL_DIR}/skill/commands/setup-claudemap.js` for the target project root with `--enrichment-file ${CLAUDE_SKILL_DIR}/tmp/claudemap-enrichment.json`. The setup command is strict: if the file is missing, empty, or unparseable it will exit non-zero and refuse to render a heuristic graph. Do not retry setup without fixing the enrichment file first.
7. Add `--force-refresh` only when the user explicitly asks for a fresh rebuild.
8. If the subagent fails to return valid JSON after two attempts, tell the user the architect pass failed and stop. Do not silently rerun setup without `--enrichment-file` — that would render a heuristic graph and pollute the cache. The user should rerun `/setup-claudemap` once the architect issue is resolved.
9. Let the bundled launcher start the app unless the user explicitly asks not to.
10. Summarize the analyzed file count, system count, graph source, render transport, and app readiness. Runtime graph outputs land in `${CLAUDE_SKILL_DIR}/app/public/graph/` (served by the bundled Vite app as `/graph/*`).
11. End the graph-generation flow with a short feedback prompt such as: `Does this map look right, or should I refine it?`
12. If the user says the map is good, stop there.
13. If the user asks for refinement, reuse the current target project's `claudemap-cache.json` graph and file snapshot as context when available instead of starting from a blank prompt again.
14. For refinement passes, send the existing graph plus the user's requested changes back through `@claudemap-architect`, save the refined JSON to `${CLAUDE_SKILL_DIR}/tmp/claudemap-enrichment.json`, and run `${CLAUDE_SKILL_DIR}/skill/commands/refresh.js` with `--enrichment-file` so the graph iterates in place.
15. After the refined graph renders, ask the same short feedback prompt again.

`/create-map` runs an architect-first scoped pipeline:

1. Resolve the target scope from the user's request (either a scope JSON payload copied from the UI, or a natural language description of a subsystem the architect should locate in the root graph).
2. Read `${CLAUDE_SKILL_DIR}/skill/prompts/scoped-enrichment.txt`. This is a dedicated scoped prompt — do not reuse the root enrichment prompt.
3. Build a scoped snapshot by filtering the root graph's file list to the files inside the target subsystem. Include any prior scoped graph from the target map's `cachePath` when one exists so the architect can refine rather than rebuild.
4. Call the `@claudemap-architect` subagent with the scoped snapshot, the scoped prompt, and any user instructions. Instruct it to emit a richer internal breakdown (2-6 internal subsystems, tighter edges, function nodes welcome) and to decide between edit-in-place and rebuild based on the intent of the request.
5. Save the returned JSON to `${CLAUDE_SKILL_DIR}/tmp/claudemap-enrichment.json` and run `${CLAUDE_SKILL_DIR}/skill/commands/create-map.js` with `--enrichment-file` (plus `--scope-json` and optional `--instructions`). The command deletes the tmp file after it reads it.
6. If the architect pass fails, the command can still fall back to `buildScopedGraphFromRoot` by running without `--enrichment-file`, but warn the user the scoped map will be a plain filter view and suggest rerunning with architect enrichment for richer grouping.
7. After the scoped map renders, ask the same short feedback prompt (`Does this map look right, or should I refine it?`).
8. If the user asks for refinement, reuse the scoped map's own cache as prior graph context (via `buildScopedSnapshot`'s `priorGraph` option) and rerun the architect. Save the refined JSON to the tmp file and rerun `create-map.js` with the same `--scope-json` payload plus `--enrichment-file`.
9. After the refined scoped graph renders, ask the same short feedback prompt again.

`/refresh` is change-aware for scoped maps:

- The root graph is always diffed against the cached snapshot.
- For each scoped map, if none of its files were in the diff and its cached graph was produced by the architect (`meta.source === 'claude-scoped'`), the scoped map is preserved untouched — no rebuild, no filter fallback.
- If the scoped map's files were touched, it is rebuilt from the updated root graph filter and marked `needsRebuild: true` so the next `/create-map` pass knows to rerun the architect for that scope.
- If a scope can no longer be resolved in the new root graph, it is marked `stale: true` and `needsRebuild: true` and left for the user to confirm.

Important details:

- The bundled runtime lives inside this skill directory, so keep all paths anchored to `${CLAUDE_SKILL_DIR}`.
- `/setup-claudemap` should treat the `@claudemap-architect` path as the primary path, not an optional extra.
- The packaged project includes a `claudemap-architect` subagent in `.claude/agents/` for system identification, graph refinement, and human-first graph restructuring.
- If a cached Claude-authored graph already exists, do not replace it with a heuristic regeneration unless the user explicitly asks for `--force-refresh`.
- If the user only wants to reopen the existing map UI, use `/open-claudemap` instead of rerunning setup.
- Follow-up refreshes should use the `/refresh` command shipped in `.claude/commands/refresh.md`.
- Graph refinements should prefer `${CLAUDE_SKILL_DIR}/skill/commands/refresh.js --enrichment-file ...` over rerunning setup so the current graph context is reused.
- `/show` should be treated as a presentation-direction command, not just a low-level transport wrapper.
