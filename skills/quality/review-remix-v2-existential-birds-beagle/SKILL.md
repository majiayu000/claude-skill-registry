---
description: Comprehensive Remix v2 code review with optional parallel agents. Detects Remix v2 in package.json, loads relevant review skills, runs verification protocol.
name: review-remix-v2
---

# Remix v2 Code Review

## Arguments

- `--parallel`: Spawn specialized subagents per technology area
- Path: Target directory (default: current working directory)

## Step 1: Identify Changed Files

```bash
git diff --name-only $(git merge-base HEAD main)..HEAD | grep -E '\.(tsx?|jsx?|mjs|cjs|css)$|^(remix|vite)\.config\.'
```

If nothing is returned, ask the user for an explicit path list before continuing.

## Step 2: Detect Remix v2 + Techs

```bash
# Detect Remix v2 in package.json (any official adapter)
grep -E '"@remix-run/(react|node|cloudflare|deno|serve)"' package.json | head -3

# Confirm app router layout
ls app/routes/ 2>/dev/null | head -5

# meta exports (route metadata)
grep -rE 'export const meta|export function meta|export let meta' app/ --include="*.tsx" --include="*.ts" -l | head -3

# Sessions / cookies / auth
grep -rE 'createCookieSessionStorage|getSession\(|commitSession\(|destroySession\(' app/ --include="*.ts" --include="*.tsx" -l | head -3

# Form primitives (forms-review)
grep -rE 'useFetcher\(|<Form|useSubmit\(|useNavigation\(' app/ --include="*.tsx" -l | head -3

# Form anti-patterns: native form / manual fetch (forms-review trigger even without Remix imports)
grep -rE '(^|[^.])<form |fetch\(' app/ --include="*.tsx" -l | head -3

# Error boundaries
grep -rE 'export function ErrorBoundary|export const ErrorBoundary|useRouteError|isRouteErrorResponse' app/ --include="*.tsx" -l | head -3

# Headers / streaming / server-only modules
grep -rE 'export const headers|export function headers|defer\(' app/ --include="*.tsx" --include="*.ts" -l | head -3
find app -type f \( -name '*.server.ts' -o -name '*.server.tsx' -o -name '*.client.ts' -o -name '*.client.tsx' \) | head -5

# Prefetch hygiene (perf-ssr-review)
grep -rE 'prefetch=|<PrefetchPageLinks' app/ --include="*.tsx" -l | head -3

# Loaders / actions (data flow)
grep -rE 'export (async )?function (loader|action)|export const (loader|action)' app/ --include="*.tsx" --include="*.ts" -l | head -3
```

If the package.json check returns nothing, stop and tell the user: this skill expects a Remix v2 project.

## Step 3: Load Verification Protocol

Load `beagle-core:review-verification-protocol` before any substantive judgment on code. This is the canonical cross-plugin protocol; do not substitute a framework-specific copy.

**Pass before Step 5:** The skill is loaded (or its checklist is open in context). Do not classify severity or write findings until this gate clears.

## Step 4: Load Skills

Use the `Skill` tool to load each applicable skill (e.g., `Skill(skill: "beagle-react:remix-v2-routing-review")`).

**Always load** (a non-trivial Remix v2 app exercises all six areas):

- `beagle-react:remix-v2-routing-review`
- `beagle-react:remix-v2-data-flow-review`
- `beagle-react:remix-v2-forms-review`
- `beagle-react:remix-v2-error-boundaries-review`
- `beagle-react:remix-v2-perf-ssr-review`
- `beagle-react:remix-v2-meta-sessions-review`

**Detection telemetry** (records what each area review will actually find; does not gate loading — all six skills always load, but record matches/non-matches for the final report's coverage section):

| Condition | Skill |
|-----------|-------|
| `app/routes/` present | `remix-v2-routing-review` |
| `loader` / `action` exports found | `remix-v2-data-flow-review` |
| `<Form>`, `useFetcher`, `useSubmit`, `useNavigation`, native `<form`, or manual `fetch(` found | `remix-v2-forms-review` |
| `ErrorBoundary` / `useRouteError` found | `remix-v2-error-boundaries-review` |
| `headers` export, `defer(`, or `.server.ts` / `.client.ts` files or `prefetch=`/`<PrefetchPageLinks` found | `remix-v2-perf-ssr-review` |
| `meta` export or session/cookie helpers found | `remix-v2-meta-sessions-review` |

If a detection row returns no matches, record that explicitly in the report's coverage section — the skill still loads, but the reviewer should note the area had no surface to review.

## Step 5: Review

**Sequential (default):**
1. Load applicable skills
2. Review routing + nested route structure first
3. Review loader/action data flow
4. Review forms and progressive enhancement
5. Review error boundaries
6. Review meta, sessions, and headers/SSR
7. Consolidate findings

**Parallel (--parallel flag):**
1. Detect all areas upfront
2. Spawn one subagent per area with the `Task` tool
3. Each agent loads its skill and reviews its domain only
4. Wait for all agents
5. Consolidate findings into a single output

## Step 6: Verify Findings

Before reporting any issue:
1. Re-read the actual code (not just diff context)
2. For "unused" claims — did you search all references, including route-file conventions?
3. For "missing" claims — did you check parent routes, root.tsx, or framework defaults?
4. For syntax issues — did you verify against Remix v2 docs (not v1, not React Router v7)?
5. Remove findings that are style preferences, not actual issues

**Pass before promoting to Critical/Major:** For that item, (2)–(4) are satisfied with a concrete artifact — opened file at `FILE:LINE`, grep output for references, or cited parent/framework code — not only diff context.

## Step 7: Review Convergence

- **Single-pass:** report ALL issues across routing, data flow, forms, errors, SSR/perf, meta/sessions, types, and security in one pass. Before submitting, ask whether your recommended fixes would themselves trigger new findings — if yes, include those now.
- **Scope:** review only code in the diff and directly related existing code. Missing test coverage is ONE Minor issue, no implementation prescriptions. No new dependencies.
- **Fix complexity:** real severity for fixes to existing code. Requests for net-new code (new modules, dependencies, test suites, extracted abstractions) are **Informational**, not blocking.
- **Re-review:** verify previous fixes only — no new discovery, no re-flagging unfixed Minor/Nice-to-Have items.

## Output Format

```markdown
## Review Summary
[1-2 sentence overview]

## Issues

### Critical (Blocking)
1. [FILE:LINE] ISSUE_TITLE
   - Issue / Why / Fix

### Major (Should Fix)
2. [FILE:LINE] ISSUE_TITLE
   - Issue / Why / Fix

### Minor (Nice to Have)
N. [FILE:LINE] ISSUE_TITLE
   - Issue / Why / Fix

### Informational (For Awareness)
N. [FILE:LINE] SUGGESTION_TITLE
   - Suggestion / Rationale

## Good Patterns
- [FILE:LINE] Pattern description (preserve this)

## Verdict
Ready: Yes | No | With fixes 1-N (Critical/Major only; Minor items are acceptable)
Rationale: [1-2 sentences]
```

## Post-Fix Verification

After fixes are applied, run:

```bash
npm run lint
npm run typecheck
npm run test
```

All checks must pass before approval.

## Gates

Advance in order; do not skip a **pass condition** by restating it informally.

1. **Scope recorded** — **Pass when:** You have the output of the Step 1 command (or an explicit substitute path list) naming what is in scope.
2. **Protocol + always skills loaded** — **Pass when:** `beagle-core:review-verification-protocol` and all six `beagle-react:remix-v2-*-review` skills are loaded before the first severity judgment.
3. **Conditional skills audited** — **Pass when:** For each Step 2 detection row you either confirmed a match or recorded that the command returned no results.
4. **Critical/Major evidence** — **Pass when:** Each such finding cites a `FILE:LINE` that exists in the tree and meets the Step 6 pass rule for that finding type.
5. **Single output** — **Pass when:** The Issues section uses one continuous numbering sequence and the deliverable satisfies Step 7 single-pass completeness.

## Rules

- Load skills BEFORE reviewing — not after.
- Number every issue sequentially with `FILE:LINE` and clear Issue / Why / Fix.
- This is Remix v2 — do not apply React Router v7, Remix v1, or Next.js (`"use client"`, server components) conventions.
- Run the Post-Fix Verification block after fixes; Verdict ignores Minor and Informational items.
