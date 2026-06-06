---
name: repo-intel
description: Native repository intelligence from git history, codegraph when indexed, manifest reads, and compressed repo digests; no cache, no generated state, every signal is recomputed on demand. Use when the user asks to analyze git history, find hotspots, code coupling, bus factor, bugspots, code ownership, entry points, or repo health.
metadata:
  short-description: Native repo intelligence recipes
---

# repo-intel — native repository intelligence

`extend` op-cell: add situational awareness before planning, review, onboarding, or risk triage. The skill answers temporal, social, graph, symbol, and project-shape questions with native tool recipes only; no prebuilt artifact is required.

All signal recipes are in `references/signals.md`. Run the smallest recipe set that answers the user's query, then report the evidence shape directly: file, count, score, owner, last-seen, callers, callees, or manifest field.

## When to Apply

- The user asks for git-history intelligence: hotspots, coldspots, bugspots, churn, recent activity, stale areas, file history.
- The user asks for social risk: ownership, bus factor, stale owners, contributor concentration.
- The user asks for code coupling: files that co-change, risky refactor surfaces, hidden module boundaries.
- The user asks for symbol intelligence: entry points, exported symbols, callers, callees, dependents, impact.
- The user asks for repo health: activity, high-churn/bug-fix overlap, owner staleness, entry-point clarity, manifest/tooling shape.
- The user is about to refactor, review, onboard, or choose a next area and needs evidence before touching code.

## When NOT to Apply

- The ask is a single known symbol lookup and the answer is already in context.
- The ask needs runtime profiling, production telemetry, or benchmark evidence rather than repository-history evidence.
- The directory is not a git repository and the user specifically asked for history-derived signals. Degrade to manifests/symbols only and state that history signals are unavailable.
- The user asks for a complete architecture map. Use repo-intel only for entry points, hotspots, ownership, and dependence evidence; do not invent architecture from churn.

## Workflow

1. **Detect scope.** Resolve the repo root with `git rev-parse --show-toplevel`; run recipes from that root. If the user names a path, keep every command path-scoped.
2. **Detect graph index availability.** Prefer codegraph for symbol/dependent/entry-point questions when indexed: `codegraph_explore`, `codegraph_search`, `codegraph_callers`, `codegraph_callees`, `codegraph_impact`, `codegraph_files`. If unavailable or stale, degrade to `ast-grep` plus `git grep` fallbacks from `references/signals.md`.
3. **Pick signals, not a bundle.** Match the user's noun to the query menu. Avoid whole-repo digest unless the question asks for broad orientation or synthesis.
4. **Run native recipes on demand.** Use git-history commands for temporal/social signals; codegraph or AST/text fallbacks for symbol signals; manifest reads for project metadata; `npx -y repomix --compress` for compressed whole-repo context.
5. **Normalize evidence.** Suppress generated-file noise for bug attribution and churn summaries: `*.d.ts`, `*.snap`, lockfiles, `generated/`, `codegen/`, `dist/`, `build/`, `vendor/`.
6. **Grade certainty.** HIGH = git/codegraph direct evidence. MEDIUM = AST/text fallback with exact file:line hits. LOW = inferred repo-health synthesis from multiple signals.
7. **Report compactly.** Lead with the answer, then a ranked table. Include the command family used, formula, and cutoff window when scores appear.

## Query Menu

| Query | Primary evidence | Output |
|---|---|---|
| `hotspots [path]` | `git --no-pager log --format` churn, 90-day recent window | files ranked by `score = (recentChanges*2 + totalChanges)/(totalChanges+1)` |
| `bugspots [path]` | fix/hotfix commit subjects + changed files, generated suppression | files ranked by bug-fix density |
| `coupling <file>` | commits touching target and co-changing files | related files with common commit count + Jaccard/target ratios |
| `ownership <path>` | per-file/path author commits | primary owner, owner shares, stale owner flags |
| `bus-factor [path]` | commit ownership concentration, bots ignored when identifiable | people required to cover 80% of commits + at-risk paths |
| `contributors [path]` | `git shortlog -sne` + per-author last seen | contributors, commits, recent/stale status |
| `recency [path]` | last commit per file/author | active/cold/stale files and owners |
| `entry-points` | codegraph entry-point exploration; manifest and AST fallbacks | scripts, commands, `main` functions, service starts |
| `symbols <file|name>` | codegraph search/explore; AST fallback | definitions, exports, imports, locations |
| `dependents <symbol>` | codegraph callers/impact; AST/text fallback | files/symbols that call/import/reference the target |
| `metadata` | manifest reads | stack, package manager, CI/test scripts, workspace shape |
| `digest` | `npx -y repomix --compress` | compressed repo packet for synthesis |
| `health` | hotspots + bugspots + bus factor + recency + metadata | evidence-backed repo health summary |

## Interpretation Rules

- **Hotspot is not bad by itself.** It means high change pressure. Risk appears when hotspot overlaps with bugspots, stale owners, weak tests, or broad dependents.
- **Bugspot is a defect signal, not blame.** It counts fix-classified commits touching a file after generated-file suppression.
- **Coupling above 0.5 target ratio is suspicious.** If two files change together in most target commits, review them as one refactor surface.
- **Bus factor is path-sensitive.** A repo-level bus factor can look safe while `src/payments/` is single-owner.
- **Staleness is snapshot-relative.** Compare author/file `lastSeen` to the repo's last commit; stale means more than 90 days older than that point, not older than wall-clock today.
- **Symbol fallbacks are weaker than codegraph.** `git grep` proves references exist; it does not prove call semantics.

## Degradation Note

Git history is the stable baseline for this skill. Codegraph is optional and improves symbol, caller, callee, impact, and entry-point precision when the repo is indexed. When codegraph is unavailable, use `ast-grep` for structural matches and `git grep` for exact text references; mark those answers MEDIUM and include the fallback command.

## Anti-patterns

- **Running every recipe.** Choose the minimal evidence set; repo-intel is a scalpel, not a census.
- **Treating churn as quality.** Churn is pressure; only combined signals justify risk claims.
- **Ignoring generated files.** Schema or snapshot churn can swamp real bugspots.
- **Using wall-clock staleness.** Always anchor the 90-day window to the repo's last commit.
- **Conflating ownership with authority.** Ownership means observed change history, not design responsibility.
- **Reporting ungrounded health labels.** Every health claim needs at least two cited signals.

## Validation Gates

- For a ranked table, state the formula and path scope.
- For bugspots, state that generated-file suppression was applied.
- For bus-factor, separate repo-level and path-level risk.
- For symbol/dependent answers, state whether codegraph or fallback evidence was used.
- For repo health, include at least: activity recency, top hotspot, top bugspot, bus factor, and one manifest/tooling fact.
