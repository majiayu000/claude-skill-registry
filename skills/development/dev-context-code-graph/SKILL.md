---
name: dev-context-code-graph
description: "Builds per-repo code graphs in JSON and markdown-ready derived artifacts. Use when you need blast radius, symbol-level maps, import graphs, inheritance, or test links."
compatibility: Portable core. Works on Claude Code and Codex.
---

# Code Graph

Build a deterministic, machine-readable code graph for a single repository. Treat the graph as a machine-readable substrate for an LLM-maintained repo wiki or context hub, not just a terminal-only report. This skill mirrors the `dev-context-multi-repo` artifact workflow, but works at file and symbol level instead of portfolio level.

Use this skill when you need:

- a committable `graphs/code-graph.json` artifact
- file and symbol maps for one repo
- import, call, inheritance, and test-link analysis
- graph-theory review signals such as articulation points, bridges, cycles, topological order, and alternate paths
- blast radius and minimal review context for changed files or symbols
- budget-bounded context retrieval around 1–3 hot symbols via Personalized PageRank
- a grounded repo description or module description generated from graph data instead of ad hoc codebase prose

Do not use this skill for:

- portfolio-wide repo discovery or cross-repo system maps
- architecture or migration planning across many repos
- prose documentation cleanup without graph generation

Use related skills instead:

- [dev-context-multi-repo](../dev-context-multi-repo/SKILL.md) for repo portfolios and hub-level knowledge graphs
- [dev-context-engineering](../dev-context-engineering/SKILL.md) for deciding when code graph vs context graph vs repo graph is the right artifact
- [docs-ai-prd](../docs-ai-prd/SKILL.md) for code-graph specs and acceptance criteria
- [docs-codebase](../docs-codebase/SKILL.md) for publishing graph-backed docs and reports

## Quick Reference

| Need | Start here |
|------|------------|
| Generate the base artifact set | `## Workflow` |
| Validate schema and graph integrity | `### Phase 3: Validate` |
| Query blast radius or symbol neighborhoods | `### Phase 4: Query` |
| Surface structural graph risk | `query_code_graph.py --articulation-points`, `--bridges`, `--cycles`, `--topo-sort`, `--from ... --to ... --k N` |
| Run hot-symbol PPR retrieval | `query_code_graph.py --ppr --seed <id> [--seed <id> ...] --top N` |
| Detect modules via communities | `query_code_graph.py --communities [--resolution γ] [--community-seed N]` |
| Pick the right query for a review | [references/query-recipes.md](references/query-recipes.md) |
| Load scripts, schemas, and reports | `## Navigation` |

## Standard Outputs

Every run should target the same output model:

- `code-profiles/<repo>.json`
  Machine-readable code profile conforming to `schemas/code-profile.schema.json`.
- `graphs/code-graph.json`
  Primary machine-readable artifact. Queryable symbol graph conforming to `schemas/code-graph.schema.json`.
- `reports/code-graph-validation.json` *(optional but recommended)*
  Output of `scripts/validate_code_graph.py --output ...`.
- `reports/code-graph-report.md` *(optional but recommended)*
  Human-readable summary report generated from the graph.
- `reports/query-*.md` *(optional but recommended)*
  Persisted blast-radius, neighborhood, and relationship answers worth filing back into a repo knowledge base.
- `reports/code-graph-report.html` *(optional)*
  Static HTML report for local review.
- `reports/code-graph.mmd` *(optional)*
  Mermaid diagram export for graph neighborhoods or impact views.

## Workflow

### Phase 1: Scan

1. Identify supported source files by extension while skipping generated and vendored build trees.
2. Classify files as `source`, `test`, `config`, or `unknown`.
3. Parse each file with the best deterministic strategy available.
4. Record parse status explicitly: `parsed`, `heuristic`, `unsupported`, `error`, or `skipped`.

Primary helper: [scripts/scan_code_repo.py](scripts/scan_code_repo.py)

## ASCII Flow

```text
single-repo code graph request
  -> scan files and classify source, test, config, or unknown
  -> parse symbols with deterministic or heuristic parser
  -> build nodes and edges into graphs/code-graph.json
  -> validate schema, references, duplicates, orphans, and parse confidence
  -> query neighborhoods, impact, paths, PPR, communities, or structural risk
  -> persist useful reports back into repo context
  -> use findings for review, docs, onboarding, or blast-radius planning
```

### Phase 2: Build

1. Read one or more `code-profiles/*.json` files.
2. Materialize canonical nodes and edges into `graphs/code-graph.json`.
3. Add structural edges from repo to file and from parent symbol or file to child symbol.
4. Synthesize `external_symbol` nodes for unresolved or third-party import/call targets.

Primary helper: [scripts/build_code_graph.py](scripts/build_code_graph.py)

### Phase 3: Validate

Run validation after every build:

```bash
python3 scripts/validate_code_graph.py graphs/code-graph.json \
  --output reports/code-graph-validation.json
```

The validator checks:

- schema and enum compliance
- dangling references
- orphan nodes
- duplicate IDs
- containment / parent edge consistency
- circular imports
- stale verification metadata
- parse-status and confidence bounds

### Phase 4: Query

Common query patterns:

```bash
# Neighborhood around a file or symbol
python3 scripts/query_code_graph.py graphs/code-graph.json --node <id> --hops 1

# Blast radius from a file or symbol
python3 scripts/query_code_graph.py graphs/code-graph.json --impact <id> --hops 2

# Path between two nodes
python3 scripts/query_code_graph.py graphs/code-graph.json --from <id> --to <id>

# Up to three node-disjoint shortest paths
python3 scripts/query_code_graph.py graphs/code-graph.json --from <id> --to <id> --k 3

# Personalized PageRank from one or more hot symbols
python3 scripts/query_code_graph.py graphs/code-graph.json --ppr --seed <id> --top 30

# Module detection via Louvain communities (γ=1 default; >1 = smaller modules, <1 = larger)
python3 scripts/query_code_graph.py graphs/code-graph.json --communities --format table
python3 scripts/query_code_graph.py graphs/code-graph.json --communities --resolution 1.4 --top 25

# Search by label, path, summary, or tags
python3 scripts/query_code_graph.py graphs/code-graph.json --search "invoice service"

# Structural risk
python3 scripts/query_code_graph.py graphs/code-graph.json --articulation-points --relations imports --top 20
python3 scripts/query_code_graph.py graphs/code-graph.json --bridges --relations imports --top 20
python3 scripts/query_code_graph.py graphs/code-graph.json --cycles --relations imports,inherits,calls
python3 scripts/query_code_graph.py graphs/code-graph.json --topo-sort imports

# Mermaid diagram export
python3 scripts/query_code_graph.py graphs/code-graph.json --diagram --output reports/code-graph.mmd
```

Primary helper: [scripts/query_code_graph.py](scripts/query_code_graph.py)

When a query produces durable knowledge, write it to markdown or Mermaid instead of leaving it only in chat output.

Use query outputs to generate:
- repo-area descriptions
- module summaries
- change-impact notes
- review packets for risky symbols or subsystems

### Phase 5: Publish

Generate static reports for humans:

```bash
python3 scripts/export_code_graph_report.py graphs/code-graph.json \
  --output-dir reports/
```

Prefer markdown, Mermaid, or HTML outputs that can be reviewed in Obsidian or filed back into a broader context hub.

### Phase 6: Enhance

Run lightweight health checks over the graph-backed knowledge:

1. Review validation results for missing edges, parse gaps, and unsupported areas that need explanation.
2. Ask the LLM to suggest reusable reports, concept pages, or follow-up questions based on dense or weakly connected graph regions.
3. File durable findings back into `reports/` or a higher-level repo knowledge base instead of repeating the same exploration later.

If the graph is feeding repo descriptions, keep the generation bounded:
- summarize only what the graph can support
- call out parse gaps explicitly
- do not invent ownership, runtime behavior, or architectural roles from symbol names alone

## Supported V1 Scope

The v1 parser pipeline is deterministic and conservative.

- Full parser: Python via `ast`
- Heuristic parser: JavaScript, TypeScript, TSX, C#, Swift
- Unsupported languages: emit file nodes only and mark them explicitly

Swift support is intentionally heuristic in v1. The scanner extracts top-level type and function symbols from `.swift` files, records `imports` and inheritance/protocol edges conservatively, and avoids generated Apple build output such as `.build`, `DerivedData`, `Pods`, `Carthage`, and `SourcePackages`.

The graph covers:

- `repo`, `file`, `class`, `function`, `method`, `test`, `external_symbol` nodes
- `contains`, `defines`, `imports`, `calls`, `inherits`, `references`, `tests` edges

It does not attempt:

- semantic embeddings
- watch mode or IDE sync
- SQLite persistence
- whole-program type inference
- guaranteed perfect call resolution across dynamic code

For small and medium repos, direct graph queries plus compact markdown reports are often enough. Do not add heavier retrieval or indexing layers until graph JSON and summaries stop being operationally sufficient.

## Command Pattern

Start with one of these instructions:

- "Use dev-context-code-graph to build a code graph for this repo."
- "Use dev-context-code-graph to find the blast radius of `<file-or-symbol>`."
- "Use dev-context-code-graph to map tests that cover `<module>`."
- "Use dev-context-code-graph to export a Mermaid diagram for this area of the codebase."
- "Use dev-context-code-graph to generate a repo-area description from graph evidence."

## Recommended Layout

```text
code-hub/
├── AGENTS.md
├── code-profiles/
├── graphs/
├── reports/
├── schemas/
└── scripts/
```

Keep generated graph data in `code-profiles/`, `graphs/`, and `reports/`. Do not paste inventories or raw symbol lists into root instruction files.

## Stable Types

The skill assumes these canonical contracts:

- [schemas/code-profile.schema.json](schemas/code-profile.schema.json)
- [schemas/code-graph.schema.json](schemas/code-graph.schema.json)

Do not invent alternate shapes unless a downstream system requires a transform layer.

## Validation Checklist

- [ ] Every scanned repo emits one `code-profiles/<repo>.json`.
- [ ] Every node has a stable normalized ID.
- [ ] Every node with `parent_id` has a matching `contains` or `defines` edge.
- [ ] All unsupported or failed parses are marked explicitly.
- [ ] `graphs/code-graph.json` validates cleanly.
- [ ] Impact and path queries return bounded, readable results.
- [ ] External targets are represented as `external_symbol` nodes instead of dangling edges.
- [ ] Findings worth reusing are written back as markdown or diagram files instead of being left only in chat history.
- [ ] Any generated repo or module description is grounded in graph evidence and explicitly notes parse gaps.

## Known Traps

- Treating heuristic parser output as semantic truth when the file format or language support is only partial.
- Skipping explicit parse-status and confidence fields, which makes downstream summaries look more certain than the graph can justify.
- Building graph edges directly from ad hoc scripts or LLM summaries instead of normalizing through the profile and schema contracts.
- Assuming unsupported languages can be silently ignored instead of recording the coverage gap that affects blast-radius answers.
- Using one giant graph query for every question when a bounded neighborhood or impact query is enough and far easier to validate.
- Treating the code graph as a replacement for reading source files; it is a routing and blast-radius substrate, not the final authority for behavior.
- Pulling whole-repo graph output into an LLM prompt instead of using graph node IDs, paths, and bounded queries for just-in-time context.

## Common Anti-Patterns

- Turning the graph into a prose-heavy report generator and losing the machine-readable substrate that made it trustworthy.
- Inventing new node or edge types opportunistically instead of preserving the stable schema and adding a transform layer if needed.
- Treating external libraries and unresolved symbols as missing data rather than representing them as `external_symbol` nodes.
- Publishing repo or module descriptions from graph output without calling out parse gaps, heuristics, and unsupported areas.
- Adding heavier retrieval or embeddings before the deterministic graph and query workflow is already operationally sufficient.
- Feeding generated summaries back into graph extraction as if they were source evidence.
- Letting per-repo symbol nodes leak into the portfolio knowledge graph instead of publishing linked code-graph reports or selected summaries.

## Navigation

### References

- [references/code-graph-patterns.md](references/code-graph-patterns.md)
- [references/parser-support-matrix.md](references/parser-support-matrix.md)
- [references/query-recipes.md](references/query-recipes.md)

### Schemas

- [schemas/code-profile.schema.json](schemas/code-profile.schema.json)
- [schemas/code-graph.schema.json](schemas/code-graph.schema.json)

### Scripts

- [scripts/scan_code_repo.py](scripts/scan_code_repo.py)
- [scripts/build_code_graph.py](scripts/build_code_graph.py)
- [scripts/validate_code_graph.py](scripts/validate_code_graph.py)
- [scripts/query_code_graph.py](scripts/query_code_graph.py)
- [scripts/export_code_graph_report.py](scripts/export_code_graph_report.py)
- [scripts/test_code_graph_regressions.py](scripts/test_code_graph_regressions.py)

### Examples

- [examples/python-mini-repo.md](examples/python-mini-repo.md)
- [examples/typescript-mini-repo.md](examples/typescript-mini-repo.md)

## Fact-Checking

- Known bugs, regressions, framework/compiler/runtime footguns, and version-specific crash or workaround guidance must be verified against current primary web sources before being treated as current fact.
- Re-verify parser support claims before user-facing answers if the implementation changes.
- Prefer primary references for parser runtimes, AST behavior, and JSON Schema semantics.
- Use [data/sources.json](data/sources.json) as the curated source map.

