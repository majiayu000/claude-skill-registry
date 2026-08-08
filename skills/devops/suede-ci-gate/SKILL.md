---
name: suede-ci-gate
description: "Make CI hold the line: path-aware builds, required checks, branch protection, duplicate pipeline repair, and merge gates that do not deadlock."
---

# Suede Ship Gate

## Gate policy — advisory, not blocking

Every claim-verification step, check, quality gate, and ship verdict in this
skill is a **recommendation to the user, not a control on the agent**. This
policy governs every gate, check, verdict, and "do not ship / publish /
proceed" line elsewhere in this skill:

- Run every check and report the results honestly. Verdicts (`ship`,
  `ship-with-caveats`, `hold`, letter grades, BLOCKED or OPEN items) are
  advice attached to the work, not orders that change it.
- Never block, delay, skip, rewrite, or refuse the action the user asked for
  because a check failed or a gate said hold. Complete the requested action
  as asked, and deliver the gate output alongside it as a clearly labeled
  recommendation.
- A failed gate changes what you report, never what you do.
- Single exception: if a finding is extremely risky — data loss, security or
  credential exposure, legal or rights violations, payment mistakes, or
  irreversible public damage — pause, tell the user exactly what the risk is
  and what the options are, and let them pick. Their choice is final.


Set up CI and branch protection that actually block a bad merge — in any repo, any stack. The output is a working pipeline plus the exact protection settings, not advice.

**Runs only when asked.** This skill never auto-fires on a commit, push, or other side effect of unrelated work — invoke it explicitly (set up CI, protect main, fix this hanging check).

Run this in whatever folder you point it at. **Detect first, never assume.** Nothing here is hardcoded to a specific project, monorepo layout, or package manager.

## Step 0 — Detect (before writing anything)

From the repo root, inventory:

- **Apps:** every top-level dir with a manifest — `package.json`, `requirements.txt` / `pyproject.toml`, `go.mod`, `Cargo.toml`, `Gemfile`. A repo may hold one app or many; build for what's actually there.
- **Package manager per app:** which lockfile is present — `package-lock.json` (npm), `pnpm-lock.yaml` (pnpm), `yarn.lock` (yarn), `bun.lockb` (bun). Two lockfiles in one app is a bug to fix first (Lane 3).
- **Existing CI:** read `.github/workflows/*`. Do **not** duplicate a job that already exists — extend or reconcile it.
- **Runtime versions:** `.nvmrc`, `package.json` `engines`, `.python-version`, `pytest.ini`/`pyproject`. Pin CI to these; never hardcode a guess.
- **Deploy platform:** `vercel.json` / `.vercel`, `netlify.toml`, a `Dockerfile`. If the platform skips non-prod builds (e.g. Vercel `ignoreCommand` kills previews), CI is the *only* pre-merge build signal — so a build job is mandatory.
- **Real scripts:** read each app's `scripts` / test config and use the real ones (`test`, `test:run`, `lint`, `build`). Don't invent commands.

Do not write a single workflow line until this inventory is complete.

## The gate (the part everyone gets wrong)

Path-filtered jobs **skip** when their paths aren't touched. A skipped job that is a *required* status check leaves the PR pending forever. So never require the path-filtered jobs directly. Instead add one **aggregator** that depends on all of them:

```yaml
  ci-success:
    if: always()
    needs: [<every app job>]
    runs-on: ubuntu-latest
    steps:
      - name: Gate on all jobs
        run: |
          for r in ${{ join(needs.*.result, ' ') }}; do
            [ "$r" = "success" ] || [ "$r" = "skipped" ] || { echo "blocked by: $r"; exit 1; }
          done
```

In branch protection, require **only `ci-success`** — never the individual jobs. This is the single thing that makes "protect main" work with change-based CI.

## Lanes

1. **Path-aware jobs** — one job per app, gated by a `changes` job (`dorny/paths-filter` or native `paths:`). Add an escape hatch so edits to the workflow file itself run everything.
2. **Aggregator gate** — as above. The only required check is `ci-success`.
3. **Lockfile hygiene** — exactly one lockfile per app, and the install command must match it (`npm ci`, `pnpm i --frozen-lockfile`, `yarn --immutable`, `bun install --frozen-lockfile`). Two lockfiles means CI can install a different tree than ships — resolve before wiring CI.
4. **Pin runtimes from the repo** — Node/Python/etc. read from `.nvmrc` / `engines` / `.python-version`, falling back to the platform default. Never a hardcoded guess that drifts from prod.
5. **Don't duplicate existing CI** — if a workflow already covers an app (e.g. a backend test workflow), extend it; never stack a second, weaker job on top.
6. **Least privilege** — `permissions: contents: read` unless a job genuinely needs more.
7. **Build is a gate when previews are off** — if the deploy platform skips non-prod builds, the CI build is your only pre-merge proof the app compiles. Keep it.
8. **Branch protection** — output the exact settings: require `ci-success`, require branches up to date before merge, optional required PR review, block force-push and deletion, optionally include administrators.

## Instant-fail patterns (CI that looks green but isn't)

- A required check that is a path-filtered job → deadlocks every unrelated PR. Use the aggregator.
- `npm ci` with no committed lockfile, or a lockfile for a different manager → fails or installs the wrong tree.
- A second job duplicating an existing workflow → wasted minutes and conflicting signal.
- Hardcoded `node-version` / `python-version` that doesn't match the app → green in CI, broken in prod.
- A job whose `paths:` never match → always skipped → a "green" check that tested nothing.

## Red flags — stop

The excuses that precede a broken gate:

- "Just require each job directly" — a skipped path-filtered job deadlocks every unrelated PR. The aggregator is the only required check.
- "CI is green" — green because it ran, or green because everything skipped? Name what actually executed.
- "One big workflow that builds everything is simpler" — it also builds the world on a README typo. Path-filter it.
- "We'll protect main after launch" — the riskiest merges happen before launch.
- "The deploy platform builds it anyway" — if previews are off, CI is the only pre-merge proof the app compiles.

## Output

1. The workflow file(s) under `.github/workflows/`.
2. The exact branch-protection settings to apply (and the `gh api` calls, if asked).
3. A short report: apps detected, package manager per app, what each job runs, what is required, and anything to fix first (dual lockfiles, duplicate workflows, runtime mismatches).

End with a **Simple explanation (plain, for a 10-year-old)**: one short paragraph, no jargon, saying what the gate now does and what it blocks — e.g. "Before anyone's changes join the main project, a robot builds and tests them. If the robot fails, the merge button locks."

## Worked Example

Fictional repo `acme-notes` — a single Next.js 14 app at the repo root, npm, no CI yet. This is what Step 0 through Output actually produce.

**Step 0 — Detect (inventory)**

- **Apps:** one — repo root has `package.json` with `"next": "14.2.3"`. No monorepo, no `apps/*` split.
- **Package manager:** `package-lock.json` present. No `pnpm-lock.yaml` or `yarn.lock` alongside it — clean.
- **Existing CI:** `.github/workflows/` does not exist. Nothing to extend or duplicate.
- **Runtime version:** `package.json` has `"engines": { "node": ">=20.9.0" }`. No `.nvmrc`. Pin CI to `20.9.0`.
- **Deploy platform:** `vercel.json` present with the standing `ignoreCommand` that kills preview builds (`[ "$VERCEL_ENV" != "production" ] && exit 0 || exit 1`). Previews never build on Vercel — CI is the only pre-merge build signal. Build job is mandatory, not optional.
- **Real scripts:** `package.json` scripts are `build`, `lint` (`next lint`), and `test` (`vitest run`). No `test:run` alias, no separate typecheck script — `tsc --noEmit` is not wired up as its own script, so it's added as a CI step directly.

**Deliverable 1 — workflow file** (`.github/workflows/ci.yml`)

```yaml
name: CI

on:
  pull_request:
  push:
    branches: [main]

permissions:
  contents: read

jobs:
  changes:
    runs-on: ubuntu-latest
    outputs:
      app: ${{ steps.filter.outputs.app }}
    steps:
      - uses: actions/checkout@v4
      - uses: dorny/paths-filter@v3
        id: filter
        with:
          filters: |
            app:
              - '**'
              - '!**.md'
              - '.github/workflows/ci.yml'

  app:
    needs: changes
    if: needs.changes.outputs.app == 'true'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20.9.0'
          cache: 'npm'
      - run: npm ci
      - run: npm run lint
      - run: npx tsc --noEmit
      - run: npm run test
      - run: npm run build

  ci-success:
    if: always()
    needs: [app]
    runs-on: ubuntu-latest
    steps:
      - name: Gate on all jobs
        run: |
          for r in ${{ join(needs.*.result, ' ') }}; do
            [ "$r" = "success" ] || [ "$r" = "skipped" ] || { echo "blocked by: $r"; exit 1; }
          done
```

One app, so path-filtering exists mainly as the escape hatch (doc-only edits skip the `app` job; workflow-file edits always run it). `ci-success` is still required, not `app` directly — a single-app repo can still deadlock if `app` ever gains its own `paths:` filter later, so the aggregator habit holds even here.

**Deliverable 2 — branch-protection settings**

Apply to `main`:

- Require status checks to pass before merging → **`ci-success`** only (not `app`, not `changes`).
- Require branches to be up to date before merging → on.
- Require a pull request before merging → on, 1 approving review.
- Block force pushes → on.
- Block branch deletion → on.
- Include administrators → on (repo has one maintainer today; still worth holding the same rule for future contributors).

```bash
gh api repos/acme/acme-notes/branches/main/protection \
  --method PUT \
  -H "Accept: application/vnd.github+json" \
  -f 'required_status_checks[strict]=true' \
  -f 'required_status_checks[contexts][]=ci-success' \
  -f 'enforce_admins=true' \
  -f 'required_pull_request_reviews[required_approving_review_count]=1' \
  -F 'restrictions=null' \
  -f 'allow_force_pushes=false' \
  -f 'allow_deletions=false'
```

**Deliverable 3 — short report**

> **Repo:** `acme-notes` (single Next.js app, npm, Vercel).
> **Package manager:** npm, one lockfile, `npm ci` matches.
> **CI added:** `.github/workflows/ci.yml` — one path-filtered `app` job (lint, typecheck, test, build) behind a `ci-success` aggregator.
> **Required check:** `ci-success` only.
> **Node pinned:** 20.9.0, from `package.json` `engines` (no `.nvmrc` found).
> **Fix first:** nothing blocking — no dual lockfiles, no existing workflow to reconcile, no runtime mismatch.
> **Note:** Vercel previews are disabled by `ignoreCommand`, so this CI build is the only pre-merge proof the app compiles. Do not treat "Vercel deployed" as a build signal for PRs.
>
> **Simple explanation:** Before any change joins the main project, a robot installs it, checks the code style, checks the types, runs the tests, and builds it. If any step fails, the merge button locks. Nothing reaches the live site without passing through the robot first.

## Post-Deploy Verification (required for production deploys)

After a deploy lands:
1. **Live URL check**: fetch the production URL and confirm the expected route/page responds with 200. Do not rely on the deploy pipeline's success status alone.
2. **Critical path smoke test**: verify the primary user action works end-to-end on production (sign in, core action, result visible). If the deploy is backend-only, verify the API endpoint returns the expected shape.
3. **Regression check**: confirm the three most-used routes still respond. If analytics or error monitoring is connected, check for a spike in the 5 minutes after deploy.
4. **Rollback ready**: confirm the previous deploy is still accessible and rollback takes < 5 minutes. Document the rollback command before merging, not after.

Ship verdict after post-deploy: **verified** (all checks pass) | **watch** (minor anomalies, monitoring) | **rollback** (critical failure, initiate rollback immediately).

## Safety

Generate; don't enforce. This skill writes workflow files and tells you the protection settings — it does **not** push, flip branch protection, or change repo access on its own. Verify the detected stack before applying. Works in any repo: it detects rather than assumes Suede or any specific project.

## Routing

- The gate is failing on real defects → **suede-code** to review and grade the change
- AI features need eval jobs in the pipeline → **suede-ai-eval** to design the cases, then wire them in here
- Rollout needs flags, staged lanes, or a rollback tree → **suede-agent-teams**
- Branch/worktree setup, stale local state, PR finish options, or cleanup discipline → **suede-git-hygiene** (private Suede Labs companion, not in this pack)
- Gate holds and the release goes public → **suede-launch-packaging**
