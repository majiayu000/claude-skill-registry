---
name: archobs
description: "Run architecture observability analysis on a git repository to measure coupling, boundary health, risk hotspots, and temporal drift. Use when you need empirical data about code structure before making architecture or refactoring decisions, or to validate that changes improved boundary discipline. NOT for choosing architecture patterns (use architecture); NOT for choosing code patterns (use design); NOT for adversarial code review (use review)."
metadata: {"stage":"Define","tags":["architecture-observability","coupling","boundary-health","risk-hotspots","refactoring","graph-analysis","clustering","drift","code-structure"],"aliases":["archobs","architecture-analysis","coupling-analysis","boundary-analysis","code-health"]}
---

# Archobs (Architecture Observability)

## Overview

Measure the actual coupling structure of a codebase using three signals: git co-change history, import/dependency edges, and semantic similarity. These signals are fused into a weighted graph, clustered into logical subsystems, and scored for boundary health, risk, and temporal stability.

Use this skill to ground architecture and refactoring decisions in empirical data rather than intuition. The output feeds directly into `architecture`, `design`, `plan`, and `review` as evidence.

Success looks like: numbered risk hotspots, measured boundary leakage, and prioritized suggestions with concrete scope.

## Chooser (Analysis Mode)

- **Full report** (default): Run the complete pipeline and generate an HTML report with suggestions. Use for initial analysis or periodic health checks.
- **Targeted stage**: Run a single pipeline stage (inventory, git, deps, embed, build-graph, cluster) when you only need one artifact updated.
- **Suggestion loop**: Run analysis, apply one suggestion, re-analyze, repeat until convergence. Use for automated refactoring passes.
- **Regression check**: Compare current metrics against a previous run. Use in `finish` to verify architecture health did not degrade.

## Workflow

1. **Check prerequisites**:
   - Install codanna: `brew install codanna` (macOS) or `curl -fsSL --proto '=https' --tlsv1.2 https://install.codanna.sh | sh` (Linux)
   - Install `archobs` from the bundled tool: `pip install -e 'tools/archobs[full]'`
   - Verify the target repo has git history (`git log` must succeed)

2. **Initialize workspace** (first run only):
   ```bash
   archobs init --repo <path> --out .archobs
   ```
   Skip if running `report` directly — it initializes the workspace automatically. Only run `init` separately if you need to edit `config.json` before the first analysis.

   Then ensure archobs-related paths are in the project's `.gitignore` — these are generated artifacts, caches, and bundled assets that should not be committed:
   ```bash
   for entry in .archobs/ .codanna/ .codannaignore .fastembed_cache lib/; do
     grep -qxF "$entry" .gitignore 2>/dev/null || echo "$entry" >> .gitignore
   done
   ```

3. **Run full analysis (blocking — wait for completion)**:
   ```bash
   archobs report --repo <path> --out .archobs --suggestions-provider rules
   ```
   Use `--suggestions-provider rules` (the default) when running inside a skill — the rule-based engine is fast, deterministic, and produces structured suggestions that the current session can interpret directly.

   **Do not proceed to step 4 until the report command has finished.** Steps 4–6 depend on the artifacts produced by this command. If the command is run in the background, wait for it to complete before continuing.

4. **Read results** — use `archobs show` to extract metrics (no ad-hoc Python or Parquet libraries needed).

   All `show` subcommands read from Parquet artifacts independently — **run them in parallel** when calling from an agent. This avoids sequential round-trips and is 5-6x faster.

   **Recommended for agents** — run individual queries in parallel (avoids output truncation on large repos):
   ```bash
   # Run these in parallel:
   archobs show risks --top 10 --format json
   archobs show clusters --sort leakage --format json
   archobs show drift --format json
   archobs show summary --format json
   archobs show velocity --window 30 --compare --format json
   archobs show suggestions --format json
   ```

   **Note:** `show edges` requires a `cluster_id` from `show clusters` or `show velocity`. Run it **after** those complete, targeting the top 2-3 leakiest or most active clusters:
   ```bash
   archobs show edges <cluster_id> --format json
   ```

   Or use `--top-active` to auto-select the most active clusters by file_change_count (eliminates the sequential round-trip):
   ```bash
   archobs show edges --top-active 3 --format json
   ```

   **Large repos warning**: `--top-active` output scales with cluster size. Hub clusters (100+ files) can have 15+ neighbors, producing output that exceeds context limits. Use `--max-neighbors 10` to cap neighbor count per cluster:
   ```bash
   archobs show edges --top-active 3 --max-neighbors 10 --format json
   ```

   Edge JSON output schema (per neighbor):
   ```
   neighbor_cluster, neighbor_label, total_weight, edge_count, leakage_share,
   top_pairs: [{path_a, path_b, weight}]
   ```
   `leakage_share` = `total_weight / parent_cluster.external_weight` — the fraction of the queried cluster's leakage flowing to this neighbor (e.g., 0.62 means 62% of the cluster's external coupling goes to this neighbor).

   **Convenience** — compact all-in-one (agent-friendly, <50KB output):
   ```bash
   archobs show all --compact --format json
   ```
   The `--compact` flag limits output to 5 risks, 10 clusters, and edges for top-3 clusters only. Velocity always includes added_paths in JSON output.

   **When to use compact vs parallel queries:**
   - Repos < 500 files: `show all --compact` is sufficient for a quick overview
   - Repos 500–2000 files: parallel individual queries recommended — compact output truncates important context
   - Repos > 2000 files: parallel queries required, and consider `--top` limits to control output size

   **Full dump** — for human review or when you need everything:
   ```bash
   archobs show all --top 5 --format json
   ```
   Avoid `--top 0` on large repos — output can exceed context limits.

   Additional queries:
   ```bash
   archobs show files --format json                           # complete file-to-cluster mapping
   archobs show cluster-files <id> --format json              # files in a specific cluster
   archobs show velocity --window 30 --compare --format json  # added_paths included by default in JSON
   archobs show risks --min-risk 0.5 --min-volatility 0.5 --format json  # high-risk AND high-churn files
   archobs show commits --since 30 --format json              # commit-level data with cluster annotations
   archobs show hot-files --window 30 --top 10 --format json  # hottest files by commit count with clusters
   archobs show suggestions --format json                     # structured suggestions (reads suggestions.json)
   ```
   Use `--format table` (default) for human-readable output, `--format json` for structured agent consumption, or `--format csv` for piping.

   To discover column names for any artifact: `archobs schema file_metrics`

5. **Interpret key metrics** (see [`references/interpreting-metrics.md`](references/interpreting-metrics.md)):

   **File-level risk** (`archobs show risks`):
   | Signal | Threshold | Meaning |
   |--------|-----------|---------|
   | `risk` | > 0.5 | High combined risk — prioritize for refactoring |
   | `xnbr` | > 0.35 | Cross-boundary neighbor ratio — file bridges multiple concerns |
   | `hubness` | > 0.45 | High fan-in — changes here have wide blast radius |
   | `volatility` | relative | High churn rate compared to peers |

   Filter directly: `archobs show risks --min-risk 0.5 --format json` or `--min-xnbr 0.35` or `--min-hubness 0.45` or `--min-volatility 0.5`.

   **Cluster-level health** (`archobs show clusters`):
   | Signal | Threshold | Meaning |
   |--------|-----------|---------|
   | `leakage` | > 0.20 | Boundary is porous — responsibilities bleed across |
   | `cohesion` | < 0.30 | Weak internal connectivity — cluster may be artificial |
   | `conductance` | relative | Cross-boundary edge fraction (lower is healthier) |

   **Drift** (`archobs show drift`):
   | Signal | Threshold | Meaning |
   |--------|-----------|---------|
   | `ari_prev` | < 0.50 | Architecture is unstable — subsystem map is reshuffling |
   | `modularity` | declining | Boundaries are weakening over time |

   **Drift trend interpretation** — the trend across windows matters more than any single value:
   | Pattern | Interpretation |
   |---------|---------------|
   | ARI rising toward 1.0 | Stabilizing — architecture is settling after upheaval |
   | ARI falling across windows | Degrading — boundaries are being broken |
   | ARI oscillating | Volatile — team is experimenting with structure |
   | Modularity declining while ARI rises | New cross-cutting features are landing in a stable structure |

   When reporting drift, always examine the ARI trend (last 2+ windows) rather than applying a single threshold. A codebase with ARI 1.0 → 0.38 → 0.58 → 0.77 is stabilizing, not unstable.

   **Young repos**: Repos with less than 6 months of history may produce fewer drift windows than configured. This is expected — interpret the trend with whatever windows are available.

   **Velocity** (`archobs show velocity`):
   | Signal | Suggests |
   |--------|----------|
   | High `growth_ratio` | New capability being built — define boundaries early |
   | High `churn_ratio` | Feature refinement/iteration in progress |
   | High `acceleration` (with `--compare`) | Active development push |
   | Low `acceleration` | Work winding down — safe window for refactoring |
   | High `recent_file_changes_30d` in cluster | Focused sprint in one area |
   | High `external_inbound_weight` | Gravitational center — other clusters pull toward this one |

   **`--compare` flag**: Use `--compare` to enable acceleration metrics (compares current window to prior window of the same length). Without it, only absolute velocity is shown. With it, you get `prior_commit_count`, `acceleration` (current/prior ratio), and `is_emerging` (true when a cluster had zero commits in the prior window).

   **Velocity sort order**: `show velocity` sorts by `distinct_commits` by default. Use `--sort file_change_count` or `--sort acceleration` (requires `--compare`) for alternative orderings. Note that `show edges --top-active` sorts by `file_change_count`, which can produce a different ranking than the default velocity output.

   **Known limitation — deleted files**: Velocity uses an inner join between commits and the current file inventory. Files deleted during the analysis window have no cluster assignment, so their commits are silently dropped. The `deleted_count` column reflects only deletions of files that still exist in the inventory (renamed/moved), not files fully removed from the codebase.

   Filter to active clusters: `archobs show velocity --window 30 --compare --min-acceleration 1.0 --min-growth-ratio 0.1 --format json`

   For detailed velocity signal interpretation (feature adjacency reasoning, acceleration context, convergent hub patterns), see the [forecast skill](../forecast/SKILL.md) (internal engine).

6. **Route findings to the right skill**:
   - High leakage between clusters: `architecture` (boundary redesign) or `patterns-structural` (Facade)
   - High-risk file with mixed concerns: `design` (pattern selection) then `patterns-*` (implementation)
   - Multiple high-risk areas needing sequencing: `plan` (prioritize refactoring order)
   - Development momentum and feature prediction: `forecast` internal engine (which clusters are active, what features are likely next). When running forecast in the same session, archobs artifacts are already available — the forecast skill can read directly from `.archobs/` without re-extraction. `added_paths` are included by default in JSON output, surfacing exactly which new files are being built in each cluster.
     **Quick trajectory in the same session** (no skill switch needed): run `archobs show velocity --window 30 --compare --format json` (added_paths included by default), check `git branch -r --sort=-committerdate | head -20`, and apply feature adjacency heuristics from the forecast skill. For full trajectory analysis with commit message themes and detailed interpretation, invoke the `forecast` skill (internal mode).
   - Pre-merge health check: `finish` (verify metrics did not regress)
   - Thorough assessment of structural findings: `review` (type: architecture)

7. **Read suggestions** (if generated):
   If you already ran `archobs show all --format json` in step 4, suggestions are included under the `"suggestions"` key — no additional command needed.

   **When using individual parallel queries (step 4)**, add `archobs show suggestions --format json` to your parallel batch — this reads `suggestions.json` directly with no extra computation:
   ```bash
   archobs show suggestions --format json
   ```

   Alternatively, use `archobs prompts --out .archobs` for markdown-formatted output.

   Each suggestion includes: priority, title, why (evidence), change (action), scope (affected files).

## Combined Archobs + Trajectory Workflow

For the combined archobs + trajectory workflow, see the [forecast skill](../forecast/SKILL.md) (internal engine — combined archobs + trajectory workflow). That version includes `archobs show suggestions --format json` in the parallel batch and is the canonical reference.

## Clarifying Questions

- What is the target repository path?
- Is this a first analysis or a follow-up? (Previous `.archobs/` artifacts will be overwritten.)
- Should suggestions use an LLM provider (claude/codex) or rule-based only?
- Is there a specific area of concern, or should we analyze the full codebase?
- What languages are in the repo? (Supports Python, TypeScript, JavaScript, Java.)

## Guardrails

- Do not run on repos with fewer than ~10 tracked source files — the graph needs sufficient signal.
- Do not treat cluster assignments as ground truth — they are statistical groupings that approximate logical subsystems.
- Do not skip interpreting metrics before routing to other skills — raw numbers without context lead to wrong decisions.
- Do not use the suggestion loop without human review of each applied change.
- Do not commit archobs artifacts to the repository — `.archobs/`, `.codanna/`, `.codannaignore`, `.fastembed_cache`, and `lib/` must all be in `.gitignore`.
- If `leidenalg` is not installed, the tool falls back to greedy modularity (lower-quality clustering) — note this in output.

## Map To Existing Skills

- Boundary redesign from leakage data: [`architecture`](../architecture/SKILL.md)
- In-process pattern selection from coupling data: [`design`](../design/SKILL.md)
- Refactoring prioritization from risk scores: [`plan`](../plan/SKILL.md)
- Development trajectory and feature prediction from cluster activity: [`forecast`](../forecast/SKILL.md) (internal engine)
- Architecture health regression gate: [`finish`](../finish/SKILL.md)
- Architecture-type adversarial review: [`review`](../review/SKILL.md)
- Facade/Adapter for porous boundaries: [`patterns-structural`](../patterns-structural/SKILL.md)
- Mediator for high-hubness coordination files: [`patterns-behavioral`](../patterns-behavioral/SKILL.md)

## References

- Interpreting archobs metrics: [`references/interpreting-metrics.md`](references/interpreting-metrics.md)
- Running archobs locally: [`references/running-archobs.md`](references/running-archobs.md)
- Tool source and standalone docs: [`tools/archobs/README.md`](../../tools/archobs/README.md)

## Output Template

When reporting analysis results:

- **Summary**: cluster count, edge count, embedding provider, modularity score.
- **Top risk files** (3-5): path, risk score, primary signal (xnbr/hubness/volatility), recommended action.
- **Leakiest clusters** (1-3): cluster ID, leakage %, strongest outward pull, boundary recommendation.
- **Drift assessment**: stable / degrading / improving (with ARI values).
- **Suggestions** (if generated): priority-ordered list with scope and evidence.
- **Trajectory** (when running with forecast internal engine):
  - Active feature initiatives (grouped by domain, not by cluster)
  - Feature adjacency predictions with confidence levels
  - Recommended architectural actions for growing areas
- **Next skill**: which skill to invoke based on the dominant finding pattern.
