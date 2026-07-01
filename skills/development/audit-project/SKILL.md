---
name: audit-project
description: Run an iterative multi-agent code audit until critical and high findings are resolved. Use when the user says "audit my code", "find all the bugs", "deep code audit", "iterative review", or "review until clean".
metadata:
  short-description: Iterative multi-agent code audit
---

# Audit Project — correct-op multi-agent audit loop

`audit-project` is a `correct` op-cell. It restores the invariant: **no open critical/high findings remain in the selected scope**. This is not a one-pass critique; it selects reviewers from evidence, applies fixes in verified batches, re-reviews only changed files, and stops only at zero critical/high, a user decision gate, or the iteration cap.

Bulk reviewer prompts live in `references/review-roster.md`. Consolidation, dismissal, blocked-ratio, decision-gate, and priority-routing rules live in `references/false-positive-contract.md`.

> **Sync lineage:** the diff-scoped `review-fix-grill-loop` skill carries adapted copies of both reference files. The reviewer prompts, common schema, false-positive clause, blocked-ratio, stall-hash, and routing rules share an ancestor; a canonical edit here must be hand-propagated to `skills/review-fix-grill-loop/references/` (no CI enforces it).

## When to Apply / NOT

Apply when the user asks for a deep code audit, an iterative review until clean, release-readiness review, security/performance/test-quality review, post-refactor risk sweep, or a bug-hunting pass across a scope.

NOT when the user wants a read-only opinion, a single known test failure fixed, a narrow symbol explanation, dependency CVE remediation only, or a pure formatting/lint cleanup. Use the smaller direct operation instead; this loop is intentionally heavyweight.

## Inputs and State

Inputs:
- `scope`: path, glob, package, PR/diff, or `.`. Default `.`.
- `--recent`: audit files touched in the last five commits plus unstaged/staged changes.
- `--domain <reviewer>`: run one reviewer domain only; still apply the same consolidation contract.
- `--quick`: single review pass; no fixes, no iteration.
- `--resume`: load `.outline/audit/queue.json` if present.
- `--max-iterations N`: default `5`.

State:
- `.outline/audit/queue.json`: current scope, selected reviewers, raw reviewer output, consolidated findings, low-debt extraction, verification results, decisions, hash history.
- `.outline/audit/iterations/<n>.json`: per-iteration changed files, batches, verification command/output summary, re-review result hash.

## Workflow

### 1. Resolve scope and detect project shape

1. Resolve `scope` before any agent launch. If `--recent`, use changed-file scope from the last five commits plus staged/unstaged changes; otherwise use the user path or `.`.
2. Read manifests and config, not random files: `package.json`, `pyproject.toml`, `requirements.txt`, `Cargo.toml`, `go.mod`, `pom.xml`, `build.gradle*`, `Gemfile`, CI configs, Dockerfiles, route/framework config, migration dirs.
3. Count tracked files for the resolved scope. Prefer a tracked-file list (`git ls-files <scope>`) when in a git repo; fallback to ODIN `find` for non-git workspaces.
4. Detect framework and flags:

| Flag | Evidence |
|---|---|
| `HAS_DB` | migrations/schema dirs, `schema.prisma`, ORM deps, SQLAlchemy/Django/Rails models, TypeORM/Sequelize/Mongoose, raw SQL files |
| `HAS_API` | route/controller/handler dirs, OpenAPI files, Express/Fastify/Nest/FastAPI/Django/Flask/Rails/Spring deps |
| `FRONTEND` | `.tsx`, `.jsx`, `.vue`, `.svelte`, browser entrypoints, React/Vue/Angular/Svelte deps |
| `BACKEND` | services, workers, queues, server framework deps, CLI/server entrypoints, domain handlers |
| `CICD` | `.github/workflows`, `.gitlab-ci.yml`, `.circleci/config.yml`, `Jenkinsfile`, `Dockerfile`, deploy manifests |

### 2. Gather native priority signals

Use these signals to route attention, not to auto-dismiss anything.

1. **Test gaps** — high-churn files with no co-changing test file.
   - Git recipe: parse `git log --name-only --format='%H%x09%ad%x09%s' --date=short -- <scope>`; group files per commit; mark source files whose commit groups rarely include `test`, `spec`, `__tests__`, `tests/`, or language-native test suffixes.
   - Score: `test_gap_score = hotspot_score + 2 * bugfix_touches` when test co-change count is `0`; otherwise dampen by `1 / (1 + test_cochanges)`.
2. **Pain / hotspots** — files likely to hide bugs.
   - Git recipe: `total_touches`, `recent_touches` over the last 90 days, and bug-fix touches from subjects matching `fix|bug|regress|crash|fault|hotfix|panic|leak`.
   - Complexity proxy: use `codegraph_explore`/`codegraph_files` for symbol count and dependency fan-in/fan-out when indexed; fallback to `ast-grep` counts for functions, conditionals, loops, catches, and nested classes.
   - Score: `hotspot_score = total_touches + (2 * recent_touches)`; `bug_rate = bugfix_touches / max(total_touches, 1)`; `pain_score = hotspot_score * (1 + bug_rate) * (1 + complexity_band)`.
3. **Bugspots** — files repeatedly touched by fixes.
   - Git recipe: filter fix-like commits above, count affected files, rank by `bugfix_touches` then `bug_rate`.
   - Route to security, test-quality, and code-quality reviewers with explicit “fragile file” context.
4. **Slop concentration** — files with mechanical cleanliness hazards.
   - HIGH-certainty scans: `ast-grep`/search for empty catches, blanket `catch {}`, `TODO: implement`, `throw new Error('not implemented')`, `console.log`/debug prints in production paths, `unwrap()`/`expect()` in non-test Rust, hardcoded secrets, commented-out code blocks, dead branches after `return`, obvious pass-through wrappers.
   - Rank files with `>=3` hits; top 5 feed code-quality first. Cross-file clusters feed architecture if they imply wrapper towers, duplicate implementations, or boundary sprawl.
5. **Entry-points / exposed surfaces**.
   - Primary: `codegraph_explore` with “entry points, handlers, routes, CLIs, jobs, exported API surface” and then `codegraph_callers` / `codegraph_impact` for risky fan-in.
   - Fallback: `ast-grep` for `main`, route registration, exported handlers, controllers, Lambda/Cloudflare handlers, CLI command registration, package scripts, framework config, Docker/CI entry commands.
   - Route to security and devops always; route to API/backend/frontend according to file kind.

Persist a compact `prioritySignals` object in `.outline/audit/queue.json`: top 20 test gaps, top 20 pain/hotspots, top 20 bugspots, top 5 slop concentration files, top 20 entry-points.

### 3. Select reviewers

Always select the 4 core reviewers:
- `code-quality`
- `security`
- `performance`
- `test-quality`

Select up to 6 conditional reviewers:
- `architecture` when file count > 50, cross-file slop targets exist, or codegraph impact shows broad fan-in/fan-out.
- `database` when `HAS_DB`.
- `api` when `HAS_API`.
- `frontend` when `FRONTEND`.
- `backend` when `BACKEND`.
- `devops` when `CICD` or entry-points include build/deploy/runtime surfaces.

If `--domain` is set, run only that domain unless doing so would make the requested domain meaningless (for example, `--domain database` with `HAS_DB=false`); then return a clear no-scope result.

### 4. Launch review pass in parallel

Use generic ODIN `reviewer` or `task` agents. Do not name model tiers. Do not spawn bespoke agent IDs as if they exist on disk.

Each selected reviewer receives:
1. The resolved scope and framework flags.
2. The priority signals relevant to that reviewer.
3. Its role prompt from `references/review-roster.md`.
4. The mandatory output schema:

```json
{
  "pass": "code-quality|security|performance|test-quality|architecture|database|api|frontend|backend|devops",
  "findings": [
    {
      "file": "path/to/file.ext",
      "line": 42,
      "severity": "critical|high|medium|low",
      "category": "short category",
      "description": "what is wrong and why it matters",
      "suggestion": "specific fix",
      "confidence": "high|medium|low",
      "falsePositive": false,
      "falsePositiveReason": "required non-empty string only when falsePositive is true"
    }
  ]
}
```

Reviewer findings must be evidence-based: exact `file`, exact `line`, concrete failure mode, and fix. Missing location or vague “consider improving” text is not a finding; downgrade to note or drop.

### 5. Consolidate findings and apply the false-positive contract

Use `references/false-positive-contract.md` exactly:

1. Normalize all reviewer JSON.
2. Honor `falsePositive: true` **only** when `falsePositiveReason.trim()` is non-empty.
3. If the reason is missing, force the finding back to `OPEN` and set `reasonMissing: true`.
4. Deduplicate by `pass:file:line:description`.
5. Sort severity: `critical`, `high`, `medium`, `low`.
6. Count only non-dismissed findings as open.
7. Extract LOW findings into a `TECHNICAL_DEBT.md` list and `.outline/audit/queue.json.lowDebt`; low items do not block the critical/high loop.
8. Compute blocked ratio: `dismissed_false_positive / total_findings`. If `total_findings >= 10 && ratio > 0.5`, stop and trigger `ask` with:
   - `treat-all-as-open` (Recommended): strip all false-positive flags from current raw results and continue.
   - `override-and-accept-dismissals`: accept dismissals as-is and continue/complete.
   - `abort`: stop with queue intact for manual inspection.

### 6. Fix loop: critical/high first, verified by batch

Loop condition: `openCriticalHigh > 0 && iteration < maxIterations`.

1. Build a fix queue from open `critical` then `high`; within each severity, sort by effort small→large, then group by file.
2. Apply one file batch at a time. Keep the patch minimal; fix the named invariant, not adjacent style.
3. After each batch, run the repo’s own verification command. Discover from manifests and CI (`test`, `check`, `build`, `lint`, `cargo test`, `go test ./...`, `pytest`, etc.). If no verifier exists, ask before mutating more than one batch; otherwise mark remaining fixes as blocked-by-no-verifier.
4. On regression, run `git restore -- <changed files in that batch>`, record `regressed: true`, and keep the finding open with the regression note.
5. Re-review only changed files, using only reviewers whose domain touches those files plus the original reviewers that emitted the fixed findings.
6. Re-consolidate. Run the blocked-ratio gate before checking for zero remaining issues.
7. Compute `findingsHash = sha256(sorted(open critical/high keys: pass:file:line:severity:description:suggestion))`. If the same hash appears in two consecutive iterations, stall.
8. At every iteration boundary where critical/high remain, trigger `ask`:
   - `continue-fixing` (Recommended when verifier is green and not stalled)
   - `create-issues-for-rest`
   - `move-remainder-to-TECHNICAL_DEBT`
   - `leave-in-queue`

Stall handling: if the hash repeats twice, `continue-fixing` is not Recommended. Recommend creating issues or leaving the queue unless there is a clear new fix plan.

### 7. Completion

Complete only when one is true:
- zero open critical/high findings after consolidation and re-review;
- user chose a deferral path at an iteration gate;
- max iterations reached and the queue/debt artifacts are current.

Report: scope, selected reviewers, iterations, critical/high fixed, remaining critical/high, low debt count, verification commands run, regressions rolled back, queue path.

## Anti-patterns

- **Single-agent audit**: defeats domain separation; only valid with explicit `--domain`.
- **Fix before consolidation**: raw reviewer output is untrusted until deduped and false-positive-checked.
- **Honor empty false-positive flags**: dismissal without reason is ignored.
- **Let a high false-positive ratio auto-pass**: >50% dismissal on >=10 findings is a prompt-injection smell, not success.
- **Re-review the whole repo after every batch**: wasteful and noisy; re-review changed files plus impacted entry-points.
- **Suppress tests or guards**: never disable a verifier to land an audit fix.
- **Create public issues for security-sensitive findings**: keep exploitable details internal; fix immediately or leave private queue notes.
- **Move critical/high to debt by default**: only a user decision gate can defer them.
- **Ship placeholders**: “TODO: fix later” is a failed audit fix.

## Validation Gates

| Gate | Pass Criteria | Blocking |
|---|---|---|
| Scope resolved | Concrete file set or path exists; recent mode has changed files | Yes |
| Context detected | Framework, flags, file count, priority signals collected or marked unavailable with fallback tried | Yes |
| Reviewer roster selected | 4 core reviewers plus justified conditional reviewers; no more than 10 total | Yes |
| Parallel dispatch | Selected reviewers launched in one parallel batch with role prompts and schema | Yes |
| Findings schema valid | Every finding has file, line, severity, category, description, suggestion, confidence, false-positive fields | Yes for queue ingestion |
| False-positive contract | Empty-reason dismissals forced open; blocked-ratio gate applied before zero-check | Yes |
| Low debt extracted | LOW findings copied into `TECHNICAL_DEBT.md` list and queue lowDebt | No, but must happen before completion |
| Fix ordering | Critical before high; batched by file | Yes |
| Verification | Repo-native verifier run after every batch | Yes when a verifier exists |
| Regression rollback | Failing batch restored with `git restore -- <files>` and noted | Yes |
| Targeted re-review | Only changed files plus impacted surfaces re-reviewed | Yes |
| Stall detection | Identical open critical/high hash twice triggers decision gate | Yes |
| Completion invariant | Zero open critical/high or explicit user deferral path | Yes |
