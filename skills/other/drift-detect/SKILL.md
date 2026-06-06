---
name: drift-detect
description: Compare documented plan and intent against implementation reality across GitHub issues, pull requests, milestones, docs, and code, then emit an evidence-backed Reality Check Report with a prioritized reconstruction plan. Use when the user says "plan drift", "reality check", "compare docs to code", "roadmap alignment", "implementation gaps", or "is the plan up to date".
metadata:
  short-description: Plan-versus-reality drift scanner
---

# Drift Detect - reality check and reconstruction planning

Run an `extend` op-cell: add a temporary evidence layer over the repo, compare stated intent with actual implementation, then synthesize the next repair plan. This is read-only unless the caller explicitly asks to apply follow-up fixes.

The invariant: every drift claim cites a concrete source - issue number, PR, milestone, doc line, file path, symbol, test/CI signal, or git-history signal. No evidence line, no finding.

## When to Apply / NOT

Apply when the user asks whether a roadmap, PLAN, README, milestone, issue backlog, or project memory still matches the code. Also apply before restarting an abandoned project, cutting a release from stale plans, or deciding what to rebuild after scope changed.

Do NOT apply to one local test failure, a known bug with a single repro, a branch-quality audit, or greenfield planning with no existing docs/issues/code to compare. Do not mutate docs, close issues, or edit code during this pass.

## Inputs and Flags

Default invocation shape:

```text
drift-detect --sources=github,docs,code --depth=thorough
```

- `--sources=github,docs,code` - comma list; omit a source only when unavailable or irrelevant.
- `--depth=quick|thorough` - `quick` samples active surfaces; `thorough` follows related docs, symbols, and history.
- Optional output artifact: `.outline/drift-detect/reality-check-YYYYMMDD-HHMM.md` when the report is too long for chat.

## Workflow

1. **Scope the scan.**
   - Restate the user's target: whole repo, named plan file, named milestone, release branch, or feature area.
   - Resolve sources from flags. If no flags are given, use all three.
   - Create a scratch evidence bundle in memory or `.outline/drift-detect/evidence.json` only when needed for long synthesis. Keep it minimal: `{github, docs, code, signals, generatedAt}`.

2. **Collect GitHub reality (`--sources=github`).** Use `gh` JSON output; never scrape web HTML.

   ```bash
   gh issue list --state open --limit 200 --json number,title,labels,state,assignees,createdAt,updatedAt,milestone,url
   gh pr list --state open --limit 100 --json number,title,state,isDraft,labels,createdAt,updatedAt,mergeStateStatus,reviewDecision,changedFiles,additions,deletions,files,url
   gh api repos/{owner}/{repo}/milestones --paginate --jq '[.[] | {number,title,state,open_issues,closed_issues,due_on,updated_at,description}]'
   ```

   Extract:
   - stale issues: `updatedAt` older than 90 days; high-priority stale threshold = 60 days.
   - issue categories from labels/title: `security`, `bug`, `feature`, `docs`, `infra`, `tech-debt`.
   - PR risk: draft PRs older than 30 days, merge-conflicted PRs, PRs attached to promised milestones.
   - overdue milestones: due date older than today with `open_issues > 0`; critical if due >30 days ago and release-labeled.
   - already-done candidates: issue title terms that semantically match implemented files/symbols found in Phase 4.

   If `gh` is unavailable or unauthenticated, mark GitHub as `unavailable` and continue with docs/code. Do not invent issue state.

3. **Collect documentation intent (`--sources=docs`).** Use `find` for doc file names, then `read` only candidate files/sections.

   Candidate files:
   - root: `README*`, `PLAN*`, `ROADMAP*`, `TODO*`, `CHANGELOG*`, `CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING*`.
   - directories: `docs/**`, `documentation/**`, `.github/ISSUE_TEMPLATE/**`, `.github/PULL_REQUEST_TEMPLATE*`.

   Search patterns:

   ```text
   ^\s*[-*]\s+\[[ xX]\]\s+(.+)$          # checklist state
   ^\s{0,3}#{1,4}\s+(Phase|Milestone|Roadmap|Plan|Status|TODO|Features?)\b
   \b(feature|supports?|implements?|planned|roadmap|phase|milestone|done|complete|ship|release)\b
   ```

   For each document, record:
   - headings and nearby sections naming goals, phases, release targets, features, non-goals.
   - checkboxes: `total`, `checked`, `unchecked`, completion percentage = `checked / total`.
   - completion claims: headings or prose containing `complete`, `done`, `shipped`, `ready`, `implemented`, `v1`, `release`.
   - feature list items: bullets under Features/Roadmap/Plan/API sections; strip marketing adjectives before matching.
   - stale-doc hints: no recent git change in 180+ days, old version numbers, removed symbol references, examples importing nonexistent paths.

   Git history snippets for doc freshness:

   ```bash
   git --no-pager log -1 --format='%cs%x09%an%x09%h%x09%f' -- README.md PLAN.md docs 2>/dev/null
   git --no-pager log --since='180 days ago' --name-only --format='' -- README.md PLAN.md docs 2>/dev/null
   ```

   If no docs exist, classify as a **documentation gap**, not drift.

4. **Collect code reality (`--sources=code`).** Prefer indexed native codegraph when available; otherwise use ODIN file/search tools plus `ast-grep` and `git grep` fallback commands.

   Framework and project sniff:
   - Node: read `package.json`; detect `react`, `next`, `vue`, `angular`, `express`, `fastify`, `nestjs`, `hono`, `jest`, `vitest`, `mocha`, `playwright`, `cypress`.
   - Python: read `pyproject.toml`, `requirements*.txt`, `setup.cfg`; detect `django`, `flask`, `fastapi`, `pytest`, `unittest`.
   - Rust: read `Cargo.toml`; detect bins, workspaces, tests, benches, `axum`, `actix`, `rocket`.
   - Go: read `go.mod`; detect `gin`, `echo`, `chi`, `_test.go` files.
   - CI: check `.github/workflows/**`, `.gitlab-ci.yml`, `circle.yml`, `Jenkinsfile`, `buildkite/**`.

   File-name lookups use ODIN `find`, e.g.:

   ```text
   find package.json pyproject.toml requirements*.txt Cargo.toml go.mod .github/workflows/**/* "**/*.{test,spec}.{js,jsx,ts,tsx}" "**/*_test.go" "tests/**"
   ```

   Symbol / dependency reality:
   - If codegraph is indexed: use `codegraph_explore` for the target area, `codegraph_search` for symbols, `codegraph_callers` / `codegraph_callees` for wiring, and `codegraph_impact` for blast radius.
   - Fallback commands when codegraph is absent:

   ```bash
   ast-grep --pattern 'export $X' --lang ts src
   ast-grep --pattern 'def $NAME($$$ARGS): $$$BODY' --lang python .
   ast-grep --pattern 'func $NAME($$$ARGS) $$$BODY' --lang go .
   git grep -nE '\b(auth|login|session|payment|route|controller|handler|model|migration|schema)\b' -- ':!node_modules' ':!dist' ':!build'
   ```

   Native drift signals to collect:
   - **doc-drift with zero coupling**: doc files whose recent changes do not co-change with related source. Compute from git when no graph signal exists:

     ```bash
     git --no-pager log --name-only --format='commit %H' -- README.md PLAN.md docs
     git --no-pager log --name-only --format='commit %H' -- src lib app packages
     ```

     Docs with repeated doc-only commits and no matching source commits for referenced terms are MEDIUM; exact removed symbol references are HIGH.
   - **at-risk areas**: directories with high bug-fix churn and stale/low ownership:

     ```bash
     git --no-pager log --since='180 days ago' --format='%H%x09%an%x09%s' --name-only
     git shortlog -sn --since='365 days ago' -- src lib app packages
     ```

     Mark HIGH when a planned feature maps to an area with high bug-fix density and no recent owner activity.
   - **stale docs**: docs older than 180 days that describe active or changed code paths.
   - **orphan exports / dead starts**: exported symbols or public endpoints not called/imported. Use codegraph impact when available; fallback to `ast-grep` export list + `git grep -n <symbol>` count. Orphan + documented feature = HIGH drift; orphan without docs = LOW cleanup signal.
   - **test gap**: implementation exists for documented critical behavior but no matching test file, no test script, or CI never runs tests.

5. **Normalize evidence.** Build a compact bundle, not a transcript dump.

   ```json
   {
     "github": {"issues": [], "prs": [], "milestones": [], "stale": [], "themes": []},
     "docs": {"files": {}, "features": [], "plans": [], "checkboxes": {"total": 0, "checked": 0, "percent": 0}},
     "code": {"frameworks": [], "testFrameworks": [], "ci": [], "entryPoints": [], "implementedFeatures": [], "health": {}},
     "signals": {"docDriftZeroCoupling": [], "atRiskAreas": [], "staleDocs": [], "orphanExports": [], "testGaps": []}
   }
   ```

   Every array item carries `{source, evidence, confidence}`. Evidence must be citeable: `README.md:42`, `issue #17`, `src/auth/session.ts`, `.github/workflows/test.yml`, or a command result.

6. **Synthesize with a generic ODIN agent role.** Delegate exactly one synthesis pass to an ODIN `oracle` or `plan` subagent role. The role is semantic analyst, not collector: it receives the evidence bundle and `references/drift-taxonomy.md`, then emits the report. Do not hardcode model names. Do not name or invoke any skill as a dependency.

   Prompt shape:

   ```text
   You are the semantic analyst for a plan-vs-reality drift scan.
   Input: structured evidence from GitHub, docs, code, and native signals.
   Task: produce a Reality Check Report.
   Rules:
   - Be specific. Each finding includes Evidence.
   - Verify each completed checkbox/phase against code evidence.
   - Verify each open issue as active, stale, already implemented, duplicate, or blocked.
   - Cross-reference documented features to implemented features using fuzzy/semantic matching.
   - Classify drift and gaps using the taxonomy.
   - Produce Immediate / Short-term / Medium-term / Backlog plan buckets.
   - No generic advice; every plan item has severity and evidence.
   ```

7. **Emit the Reality Check Report.** Required sections:
   - `# Reality Check Report`
   - Executive Summary: 2-3 sentences plus key numbers.
   - Drift Analysis: type, severity, description, evidence, recommendation.
   - Gap Analysis: category, severity, impact, recommendation, evidence.
   - Cross-Reference Table: documented item ↔ implementation evidence ↔ status ↔ confidence.
   - Prioritized Reconstruction Plan: Immediate / Short-term / Medium-term / Backlog; each item has severity and an `Evidence:` line.
   - Quick Wins: only when evidence shows low effort and high confidence.
   - Unknowns / Unavailable Sources: gh unavailable, missing docs, unindexed codegraph, shallow clone, etc.

## Severity and Certainty

- **critical** - release/user/security blocker, overdue milestone with open critical work, docs promise a shipped capability that is absent, or planned completed phase is materially false.
- **high** - misleading public docs, stale high-priority issue cluster, orphan implementation for documented feature, missing tests for implemented critical path, at-risk code area mapped to active roadmap.
- **medium** - stale docs with likely but not exact coupling, draft PR drift, partial implementation without test/docs parity, completed checkbox missing secondary behavior.
- **low** - cleanup-only drift, undocumented internal implementation, low-impact stale issue, old TODO without external promise.

Certainty:
- **HIGH** - exact issue/PR/milestone/doc line/file/symbol evidence.
- **MEDIUM** - fuzzy semantic match plus supporting path/history evidence.
- **LOW** - weak heuristic only; report under Unknowns or Backlog, never as a blocker.

## Anti-patterns

- **Transcript dump**: pasting raw `gh`/search output instead of synthesizing.
- **Generic plan**: "add tests" without naming the feature/file/evidence.
- **Exact-string matching only**: misses `user authentication` ↔ `auth/login/session`.
- **No-source findings**: severity without an Evidence line.
- **Issue closure by vibe**: never say close an issue unless code evidence proves it implemented or obsolete.
- **Graph absolutism**: missing codegraph index is not failure; degrade to `ast-grep` + `git grep`.
- **Mutation during scan**: do not update PLAN/README/issues in the drift pass.

## Validation Gates

| Gate | Pass Criteria | Blocking |
|---|---|---|
| Source selection | requested `--sources` parsed; unavailable sources listed | No, unless all sources unavailable |
| GitHub evidence | `gh issue list`, `gh pr list`, milestones attempted when selected | No, degrade with explicit unknown |
| Docs evidence | plan/readme/docs candidates scanned; checkbox percent computed when checkboxes exist | Yes for docs-only ask |
| Code evidence | framework/test/CI sniff complete; symbol lookup via codegraph or fallback | Yes for code comparison ask |
| Native signals | doc-drift, stale docs, at-risk areas, orphan exports attempted or marked unavailable | No |
| Synthesis | generic ODIN semantic agent role produces required report sections | Yes |
| Evidence lines | every drift/gap/plan item cites concrete evidence | Yes |
| No mutation | no files/issues/PRs changed during scan | Yes |
