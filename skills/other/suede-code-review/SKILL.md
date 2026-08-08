---
name: suede-code-review
description: "Find the bugs a diff can actually ship: TypeScript, React, Next.js, OWASP, accessibility, SEO, database, and deploy-risk review. Return findings, not a grade."
---

# Suede Code Review

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


Review code with full context: changed files, callers, contracts, deploy surface. Find real breakage. Rank by production impact. Every finding has a file, evidence, and a fix path. No findings without evidence. No volume without signal.

## Model Routing
Default: Sonnet. Recommend Opus for auth, payments, and public API surface reviews.

## Operating Stance

- Review current source, current diff, local docs, and relevant runtime behavior.
- Keep code generation and review separate by default. If you authored the code,
  switch into review mode and look for what your implementation would miss.
- Preserve user and other-agent WIP. Do not stage, revert, or rewrite unrelated
  files.
- Prefer high-signal findings over volume. Do not leave style nits when formatters
  or local conventions already handle them.
- Every blocking finding needs evidence, impact, and a concrete fix path.

## Review Contract

Before review, identify:

- target: repo, branch, PR, commit range, diff, route, API, or release build;
- intent: what the change claims to accomplish;
- risk lanes: frontend, backend, data, auth, payments, contracts, iOS, release,
  public copy, analytics, secrets, deployment, and docs.

## Context Graph

Build a lightweight graph before judging the diff:

1. Changed files and generated files.
2. Imports, callers, routes, API handlers, jobs, hooks, models, schemas, and
   config/env dependencies touched by the change.
3. Tests, fixtures, migrations, release scripts, docs, and screenshots that
   should move with the behavior.
4. Runtime surfaces: local route, live URL, API endpoint, simulator flow,
   dashboard, App Store metadata, or deployment target.
5. Suede domain contracts: creator ownership, rights/provenance, registry-backed
   media, royalty routing, agent commerce, wallet/payment flows, and
   published-statement accuracy.

Flag beyond-the-diff risks when related files, defaults, docs, env, or deploy
requirements no longer agree.

## Run the Repo's Own Gates

Do not hand-review for what a tool already decides. Before manual analysis, run the
gates the repo already ships and fold the output into findings. Detect what exists
from `package.json` scripts, config files, and lockfiles — run only those. Never
introduce a tool the repo does not use, and never fabricate a result you did not run.

- **Type check:** the repo's `typecheck` script, or the type checker directly. An error
  on a changed line is at least P2; on a changed critical path, P1.
- **Lint:** the repo's configured linter on changed files only. Report violations the
  change introduces; ignore pre-existing noise outside the diff.
- **Tests:** run the suite, or the changed-file subset. A failing test on changed
  behavior is P1; a test that silently stopped running is P2.
- **Dependency CVEs:** the repo's dependency auditor — the package manager's audit
  command, or a vulnerability scanner — when dependencies changed. A known-exploitable
  CVE reachable in a production path is P0/P1.
- **Secret scan:** a real entropy-based secret scanner over the diff when the repo
  provides one — it catches keys the Commit Dirt Score patterns miss. A verified live
  secret is P0.
- **Build:** for release reviews, the production build must pass. A broken build is P0.

### Gate Commands by Stack

The categories above are universal; the actual command differs by surface. Use this as
a reference, not a checklist — detect which of these apply to the target repo, run only
what exists, and never fabricate a result you did not run.

| Stack | Type check | Lint | Test | Other |
|---|---|---|---|---|
| Web / Node (TS/JS) | `npx tsc --noEmit` | `npm run lint` | `npm run test` | `npm audit` for dependency CVEs |
| MCP server (Node) | `node --check <server>.mjs` | repo's configured linter, if any | `npm run test:mcp` when provided | Run a complete session in one process: valid `initialize`, `notifications/initialized`, then list/call/read/get requests; use $suede-mcp-qa when available |
| iOS / Swift (Xcode) | — (compiler check is the build) | SwiftLint, if configured | XCTest target, if present | `xcodebuild -project X.xcodeproj -scheme X -destination 'platform=iOS Simulator,name=iPhone 16' build` |
| API / backend (generic) | language's own type/compile step, if any | repo's configured linter | contract or schema test — e.g. OpenAPI/schema validation against the live route, or the repo's own contract-test suite | — |

Cite the command, its exit status, and the file:line it implicates. If a gate cannot
run (no script, missing deps, sandboxed), say so in Verification — never report a gate
as passed that you did not execute.

## Project Rules and Learnings

A review that fights the house style produces noise, not signal. Honor what the repo
already encodes.

- **Read the rules first:** before judging, read `CLAUDE.md`, `AGENTS.md`,
  `CONTRIBUTING.md`, `.editorconfig`, formatter/linter config, and any review-config
  file at the repo root or in the changed directories. A documented convention is
  binding — do not flag what a rule permits; do flag what it forbids.
- **Most-specific rule wins:** a rule in a subdirectory config or a nearest-ancestor
  `AGENTS.md` overrides a repo-root rule for files under that path.
- **Record learnings:** when the user dismisses a finding as a false positive or a
  deliberate house pattern, capture it in one line — pattern, why it is allowed, path
  scope — and do not re-raise that pattern this review or in later ones. Repeat nitpicks
  erode trust faster than a missed P3.
- **No rule from silence:** the absence of a convention is not license to impose a
  personal preference. A style choice not governed by a rule, a formatter, or a real
  cost is not a finding.

## Review Modes

- **Fast diff review:** small change, narrow blast radius, focused findings.
- **Deep PR review:** multi-file behavior, public surface, data/auth/payment,
  release, or cross-repo risk.
- **Plan review:** implementation has not started; inspect scope, sequencing,
  acceptance criteria, test mapping, and missing decisions.
- **Fix verification:** review after fixes; rescan changed files and confirm the
  original finding is gone.
- **Release review:** validate build, secrets, env, public copy, screenshots,
  metadata, deployment, and live/API readback.

### Review Depth Levels

Add a `--depth` modifier to any review:

- **`--quick`** (~2 min): Pattern-based scan. Flag obvious bugs, hardcoded
  secrets, missing null checks, SQL/command injection patterns, broken error
  handling. No cross-file analysis. Use for PRs with narrow blast radius.
- **`--standard`** (default, ~10 min): Per-file analysis: correctness on changed paths, language-specific traps (see checklists below), state handling, test coverage on changed behavior, call graph within changed files. Default for all PRs unless the user says otherwise.
- **`--deep`** (~25 min): Cross-file analysis including full import graph and
  call chain tracing. Finds semantic bugs that only appear when you follow data
  across module boundaries. Use for auth changes, payment flows, data
  migrations, and public API changes.

State depth level at the top of every review output.

## TypeScript Traps

Check these on every TypeScript file in the diff:

- **`any` vs `unknown`:** `any` disables type checking for everything downstream. If the type is truly unknown at the call site, use `unknown` and narrow with a type guard. Flag every `any` annotation that isn't in a third-party type shim.
- **Non-null assertions (`!`):** Each `foo!.bar` is a runtime crash waiting for the condition that makes `foo` null. Flag unless the null case is provably eliminated by a guard two lines above.
- **Missing discriminated unions:** When a function returns `{ type: 'a', ... } | { type: 'b', ... }`, the switch/if must be exhaustive. Missing `default: assertNever(x)` is a silent future bug.
- **Unsafe casts (`as Foo`):** A cast without a preceding type guard means "trust me." Flag every `as` that isn't a DOM cast (`as HTMLInputElement`) or a narrow type refinement proven by the preceding condition.
- **`Object.keys()` without `keyof typeof`:** `Object.keys(obj).forEach(k => obj[k])` fails type checking silently at runtime when keys are typed. Require `(Object.keys(obj) as Array<keyof typeof obj>)` or a typed `Object.entries()`.
- **`Promise` without `await` in an `async` function:** Returns the Promise object instead of the resolved value. Flag any `return someAsyncFn()` inside an `async` that should `return await someAsyncFn()`.

## React Traps

Check these on every React component or hook in the diff:

- **Missing `useEffect` dependency array:** `useEffect(fn)` (no array) runs on every render. `useEffect(fn, [])` runs once. `useEffect(fn, [dep])` runs when dep changes. Flag any effect where the deps array is absent or obviously incomplete (function references, object literals, values used inside the effect but not listed).
- **Stale closures:** An effect or callback captures a value at mount time and never re-captures it. Most common pattern: a `setInterval` inside `useEffect(fn, [])` that reads a stateful value. The fix is either adding the dep or using a ref.
- **Missing `key` props:** Any `.map()` returning JSX elements must have a stable, unique `key`. Using array index as key is a bug when the list can reorder or filter. Flag index-keyed lists where items have identity (id, slug, etc.).
- **Unnecessary re-renders:** Flag components that receive object or function props without `useMemo`/`useCallback` when those objects are created inline in the parent render. Flag components that could be wrapped in `React.memo` but aren't, when rendered in tight loops or high-frequency update paths.
- **Prop drilling past 2 levels:** If a prop is passed through 2+ components without being used at intermediate levels, flag as P3. The fix is context, Zustand, or component composition. Note which fits the existing pattern in this repo.
- **State mutation without setter:** `arr.push(item)` on state does not trigger a re-render. Flag any direct mutation of state variables.

## Accessibility Traps

Check these on every React component or HTML-producing file in the diff:

- **Missing alt text:** `<img>` without `alt`, or `alt=""` on non-decorative images. Empty alt skips the element for screen readers; flag when the image conveys content.
- **Interactive elements without accessible names:** `<button>`, `<a>`, `<input>` with no visible text, no `aria-label`, and no `aria-labelledby`. An icon-only button with no label is invisible to assistive tech.
- **Wrong element semantics:** `<div onClick={...}>` used as a button; `<span>` used as a link; heading levels skipped (h1 → h3) or used for visual styling instead of document hierarchy. Use the correct element or add `role=` with keyboard handlers.
- **Missing focus management:** modals, drawers, toasts, and route transitions that don't trap or restore focus. When a modal opens, focus must move inside it; when it closes, focus must return to the trigger.
- **Keyboard inaccessibility:** custom components (dropdowns, date pickers, carousels) that handle `onClick` but not `onKeyDown` (`Enter`, `Space`, arrow keys). Flag interactive elements that can't be reached or operated by keyboard alone.
- **Color contrast:** inline styles or Tailwind classes that set foreground/background color combinations. Flag likely failures: `text-gray-400` on white, `text-white` on light-colored buttons, any low-contrast pairing below ~4.5:1 for body text or ~3:1 for large text.
- **Missing form labels:** `<input>` or `<select>` without an associated `<label>` (via `htmlFor`/`id`) or `aria-label`. Placeholder text is not a label.
- **ARIA misuse:** `aria-hidden="true"` on interactive elements (traps keyboard users); `role="presentation"` on semantically meaningful elements; ARIA roles that contradict the native element's semantics.

## Next.js Traps

Check these on every Next.js file in the diff:

- **Server/client boundary:** Any file with `'use client'` cannot import server-only modules (DB clients, `fs`, `crypto`, server-side env vars). Any file without `'use client'` that uses `useState`, `useEffect`, browser globals (`window`, `document`), or event handlers is a runtime crash. Flag the mismatch, not just the symptom.
- **Missing `Suspense` boundary:** Async server components that fetch data and are rendered inside a client component tree need a `<Suspense fallback={...}>` wrapper. Missing boundaries cause the entire parent tree to suspend without a fallback.
- **Missing `error.tsx` / `loading.tsx`:** Any new route segment that fetches data or can throw should have both. Flag their absence as P2 when the route is user-facing.
- **Server-only secrets in client bundle:** `process.env.SECRET_KEY` in a `'use client'` file or in a prop passed from server to client component is exposed in the browser bundle. Only `NEXT_PUBLIC_*` vars are safe client-side. Flag any non-`NEXT_PUBLIC_` env var referenced in client code.
- **Unguarded `generateMetadata` / `getServerSideProps` fetches:** These run on every request. An uncached external fetch here is a latency and cost bomb. Flag missing `{ next: { revalidate: N } }` or `unstable_cache` wrapping.
- **`useRouter` from `next/router` in App Router:** App Router uses `next/navigation`. Importing from `next/router` in an App Router project silently fails or returns stale data. Flag the wrong import.

## SEO Impact

Check on any file that touches routes, layouts, metadata, or public-facing content:

- **Metadata regression:** changes to `generateMetadata`, `<Head>`, `<title>`, `description`, `og:title`, `og:description`, `og:image`, `twitter:card`. Any removal or blanking of previously populated fields is a regression. Flag if `generateMetadata` now returns fewer keys than before the change.
- **Canonical drift:** `canonical` URL changed, removed, or now pointing to a different domain. Flag any change to canonical logic — canonical changes can consolidate or fragment link equity unintentionally.
- **Robots / noindex added unintentionally:** `noindex`, `nofollow`, or `X-Robots-Tag: noindex` appearing on pages that were previously indexable. Flag any new `robots` metadata that restricts crawling on a route that wasn't restricted before.
- **Sitemap impact:** new routes not added to sitemap; removed routes not pruned; `sitemap.ts` / `sitemap.xml` not updated when routes change. Flag route additions or removals without a corresponding sitemap change.
- **OG image regression:** `og:image` URLs broken, pointing to localhost, missing dimension params, or removed from previously covered pages. Flag layout-level changes that remove OG image generation entirely.
- **Structured data / JSON-LD drift:** `schema.org` markup changed, fields removed, or `@type` changed. Flag removals of `@type`, `name`, `url`, or `description` from any existing structured data block.
- **URL structure changes without redirects:** route renames, slug changes, or path restructuring without a corresponding 301. A renamed route without a redirect is a hard 404 for crawlers and any existing backlinks.
- **`llms.txt` / AI discoverability:** if the repo includes `llms.txt` or `llms-full.txt`, flag any changes that expand or restrict what AI crawlers are permitted to see.

## Database Traps (Drizzle / Prisma)

Check these on any file that touches DB queries:

- **N+1 queries:** A loop that issues a query per iteration. The fix is a single query with `WHERE id IN (...)` or a join. Flag any `.map()` or `for` loop that calls `db.query()`, `prisma.find*()`, or `db.select()` inside the body.
- **Missing index on filtered/sorted columns:** Any `WHERE`, `ORDER BY`, `GROUP BY`, or join condition on a column that isn't indexed is a full-table scan. Flag new query predicates on columns with no corresponding index in the migration/schema.
- **Multi-table writes without transactions:** Two or more `INSERT`/`UPDATE`/`DELETE` calls that must succeed or fail together. Flag any multi-table write that isn't wrapped in `db.transaction()` / `prisma.$transaction()`.
- **Missing unique constraints:** Fields that are logically unique (user email, slug, external ID) but lack a `UNIQUE` constraint are race-condition bugs at scale. Flag schema definitions where uniqueness is enforced in application code but not the DB.
- **Unbounded queries:** `db.select().from(table)` with no `LIMIT` on a user-facing route is a DoS vector and a cost spike. Flag selects with no limit when the table can grow.

## Performance Flags

- **Large dependency import:** Any new `import` of a package not already in the bundle. If the package's minzipped size is >20 KB, flag as P3 with the size estimate. Prefer tree-shaken imports (`import { X } from 'pkg'` not `import pkg from 'pkg'`).
- **Render-blocking scripts:** `<script src="...">` without `async` or `defer` in HTML head blocks page paint. Flag in any HTML template or `_document.tsx`.
- **Missing lazy loading for non-critical routes:** Any page-level component imported with a static `import` at the top of `_app.tsx` or a layout file when it could be `next/dynamic` with `ssr: false`. Flag routes not in the critical path (settings pages, dashboards, modals).
- **Images without `next/image`:** `<img src="...">` bypasses Next.js image optimization. Flag raw `<img>` tags in Next.js files pointing to non-SVG assets.

## Agent Team Review (--deep only)

For `--deep` reviews on auth changes, payment flows, data migrations, or public API changes, run as separate lanes:

- **Change mapper:** summarizes what changed and which systems are touched.
- **Runtime critic:** hunts execution failures, state drift, race conditions, error paths, and deploy prerequisites.
- **Security critic:** reviews auth, secrets, permissions, injection, SSRF, payment safety, wallet flows, and data exposure.
- **Product critic:** checks feature truth, Suede positioning, user-visible behavior, empty/error states, and release claims.
- **Test critic:** maps claims to tests, screenshots, simulator runs, builds, and live/API checks.

Collect consensus first. If high-severity concerns persist after a fix cycle, keep status at `hold` and name the smallest next check or patch.

## Whole-Repo and History Pass (--deep)

The changed-file import graph is the floor. The bugs that ship hide outside the diff. On `--deep`, widen past the immediate callers:

- **Reverse-dependency sweep:** find every caller of a changed function, type, route, or constant across the whole repo (search the symbol repo-wide, not just the changed file's imports). A signature, return-shape, or nullability change is safe only if every call site agrees — name the sites you checked.
- **Shared-assumption check:** for a changed schema, env var, default, or invariant, find the other places that assume the old value — config read in two services, a default mirrored in a client, a magic value duplicated in a test. These drift silently.
- **History of the touched lines:** `git log -L` or `git blame` the changed region. If this area was fixed before, a change that reintroduces the old shape is a regression — cite the prior commit. If it churns repeatedly, flag it as fragile.
- **Sibling-pattern consistency:** find the nearest existing analog — the other route handlers, the other migrations — and confirm the change follows the established pattern. A lone handler that skips the shared auth wrapper the other four use is P1 even if it "works."

State what you traced. A whole-repo claim with no symbols named is not evidence.

## Observability Delta

Check on any new route handler, API endpoint, background job, cron, queue consumer, or service function:

- **Swallowed errors:** `try/catch` blocks that catch without logging or Sentry capture. Flag `catch (e) {}` and `catch (e) { console.error(e) }` — a caught error that only `console.error`s is invisible in production. Require `Sentry.captureException(e)` or equivalent on unexpected errors.
- **Dark code paths:** new route handlers, API functions, or jobs with no log line at entry and no log on failure. If the path produces no signal, the first indication of failure will be a user report.
- **Missing error boundaries:** new React subtrees not wrapped in an error boundary; new server functions that don't surface errors to the monitoring layer.
- **Uninstrumented slow paths:** new DB queries, external API calls, AI model calls, or file I/O with no timing log or trace span. These are the paths that will page oncall first.
- **Orphaned analytics events:** feature flags or analytics events that were fired in the old code and are no longer fired after the change. A metric drop in the dashboard will look like a product regression.
- **Silent background jobs:** cron or queue consumer that completes without logging item count processed, duration, or failure reason. Silent jobs are unmonitorable until they stop running entirely.

## Deploy Safety Gate

Run this automatically at the end of every review. No exceptions. It answers one question: **is this safe to deploy right now?**

Grade each dimension. Each is pass / conditional / block:

- **Breaking changes**: Does this change any public API signature, database schema, config key, or interface contract without a versioned migration or backward-compatible fallback? Recommend blocking if yes without migration path.
- **Rollback safety**: Can a `git revert` fully undo this? Red flags: schema migrations, irreversible external API calls (email sent, payment charged, data permanently deleted), S3/storage mutations, message queue publishes. Recommend blocking if rollback requires manual data repair.
- **Blast radius**: What fraction of users or requests does this code path serve? State it: `~0%` (new feature, flagged), `~partial` (specific flow), `~100%` (shared middleware, auth, DB query in hot path). Higher blast radius requires more evidence before deploy.
- **Environment readiness**: Are all required env vars, secrets, feature flags, and config values already deployed to production? Recommend blocking if a required env var doesn't exist in production yet.
- **Dependency changes**: Are new or updated packages pinned to an exact version, from a trusted source, and CVE-free? Recommend blocking if a new dependency has a known CVE or is unpinned in a production context.
- **Data mutations**: Does this write, update, or delete production data in a way that can't be undone by revert alone? Recommend blocking if yes without a tested restore path.
- **Security delta**: Does this change improve, hold neutral, or worsen the security posture? Recommend blocking if it introduces new attack surface without mitigation.
- **Automation coverage**: Does `.github/workflows/` (or equivalent CI) exist and cover the changed surface (build, types, tests)? Are required status checks enforced on `main`? Recommend blocking if the changed surface has no automated gate and the repo is production-connected.

Output block — required at the end of every review:

```text
DEPLOY SAFETY
Breaking changes: pass | conditional | block — [evidence]
Rollback safety: pass | conditional | block — [evidence or red flag]
Blast radius: ~X% — [which path or user segment]
Environment readiness: pass | conditional | block — [missing vars if any]
Dependency changes: pass | conditional | block — [new deps and CVE status]
Data mutations: pass | conditional | block — [irreversible operations if any]
Security delta: improved | neutral | block — [surface changed]
Verdict: SAFE TO DEPLOY | DEPLOY WITH CONDITIONS | DO NOT DEPLOY
Conditions (if any):
```

This skill emits no letter grade. When the caller wants lane grades too, run $suede-code (findings + grade) or $suede-code-grader (grade only) — those two carry the canonical Instant-F trigger list, grade caps, and A-F scale. Instant-F patterns found here (hardcoded secrets, injection, auth bypass, unverified payment webhooks, destructive migrations with no rollback, plaintext sensitive data) are P0 findings and set the Ship Gate to `hold`.

## Commit Dirt Score

Run automatically on every review. Scan the raw diff for content that should never reach git history. No exception for "it's just a branch" — dirty commits propagate.

**Check every line added (`+`) in the diff for:**

- **Secrets and credentials**: API keys, tokens, passwords, private keys, connection strings, JWTs, `.env` variable values hardcoded in source. Patterns: `sk_`, `pk_`, `Bearer `, `-----BEGIN`, `password=`, `secret=`, `token=`, `AKIA`, `ghp_`, `xoxb-`, long hex/base64 strings adjacent to key-like identifiers.
- **Debug artifacts**: `console.log`, `console.error`, `debugger`, `print(`, `pprint(`, `binding.pry`, `byebug`, `dd(`, `dump(`, `var_dump(`, hardcoded test user IDs, `TODO: remove`, `FIXME: before merge`, `HACK:`, commented-out blocks of real logic.
- **Conflict markers**: `<<<<<<<`, `=======`, `>>>>>>>`, `|||||||`. A conflict marker in a `+` line means the file was not fully resolved.
- **Accidentally staged files**: `node_modules/`, `.next/`, `dist/`, `build/`, `*.pyc`, `__pycache__/`, `.DS_Store`, `*.log`, `*.sqlite`, `*.db`, migration snapshot files that weren't meant to commit, generated lock-file noise from the wrong package manager.
- **WIP breadcrumbs**: `[WIP]`, `DO NOT MERGE`, `TEMP:`, `SKIP CI` in non-CI files, `stash this`, placeholder copy like `lorem ipsum`, `foo`, `bar`, `asdf` in production-facing strings.
- **Oversized or binary blobs**: files >500 KB added to the diff, font files, compiled binaries, video/audio, uncompressed images outside a designated `public/` or `assets/` directory.
- **Exposed internal references**: internal IP addresses, internal hostnames, staging/dev URLs hardcoded in non-config files, personal email addresses in source.

**Score:**

```
COMMIT DIRT SCORE
Secrets / credentials:   clean | suspicious | dirty — [pattern found or "none"]
Debug artifacts:         clean | suspicious | dirty — [symbol or line or "none"]
Conflict markers:        clean | dirty — ["none" or file:line]
Accidentally staged:     clean | dirty — [path or "none"]
WIP breadcrumbs:         clean | suspicious | dirty — [marker or "none"]
Oversized / binary:      clean | dirty — [file and size or "none"]
Exposed internals:       clean | suspicious | dirty — [pattern or "none"]
Overall dirt rating:     CLEAN | SUSPICIOUS | DIRTY
```

- **CLEAN**: no hits across all dimensions.
- **SUSPICIOUS**: low-confidence hit that could be a false positive (e.g. a test fixture, a sample value in docs). Call it out; let the reviewer confirm.
- **DIRTY**: high-confidence hit that must be removed before merge. Escalate as P0 in the Findings section.

A `DIRTY` overall rating automatically sets the Ship Gate to `hold`.

## Finding Format

Lead with findings, ordered by severity. Group repeated patterns once: "This pattern appears in 4 files: [list]. Fix described once below."

**P0 / P1**: use the full block:

```
[P0] path/to/file.ts:142
Issue: JWT secret falls back to empty string; any token is valid when SECRET is unset.
Fix: `process.env.JWT_SECRET ?? (() => { throw new Error('JWT_SECRET required') })()`
Verify: set JWT_SECRET="" and curl /api/me — expect 401, currently 200.
OWASP: A02 Cryptographic Failures
Confidence: high
```

**P2 / P3**: one line each:

```
[P2] components/Feed.tsx:88 — missing key prop on .map() return; use item.id not index. TS will catch post-fix.
[P3] utils/format.ts:12 — magic number 86400; extract as SECONDS_PER_DAY.
```

Severity:

- **P0:** data loss, security exposure, payment loss, broken release, or public behavior that should not ship — extreme-risk findings that also warrant a pause-and-ask to the user before any ship step.
- **P1:** likely production regression, auth/permission bug, broken primary path, false published statement, or missing critical deploy requirement.
- **P2:** meaningful edge-case failure, incomplete state handling, test gap on changed behavior, or maintainability issue with real cost.
- **P3:** low-risk improvement, clarity issue, local cleanup, or follow-up.

If the issue cannot be tied to a file, route, command, state, or user-visible behavior, mark it as an open question instead.

## Fix Briefs

When asked to fix, convert each accepted finding into an agent-ready brief:

- failing behavior and evidence;
- exact files or areas to inspect first;
- expected change;
- acceptance criteria;
- verification command or browser/simulator path;
- caveats and WIP to preserve.

Fix one risk cluster at a time. After fixing, rerun the relevant review mode and
do not close the finding until evidence confirms it.

### Fix Mode

When the user asks to apply fixes (`--fix` flag or equivalent instruction):

1. Auto-apply P2/P3 fixes that are local (single file, no behavior contract change). Stage each fix as its own commit with the finding ID in the message.
2. Present P0 and P1 findings as confirmed fix briefs before applying. Do not
   auto-apply to production-critical, auth, payment, or data-migration code
   without explicit user confirmation.
3. After applying fixes, re-run the relevant review mode on only the changed
   files. Mark original findings as resolved or escalated.
4. Cap the iteration loop at 3 cycles. If the same finding persists after 3 fix
   attempts, escalate as a design issue requiring human decision.

## Current OWASP Security Baselines

Run the web baseline automatically on `auth/`, `api/`, `middleware/`, `routes/`,
`pages/api/`, or code importing crypto, session, or payment modules. Cite the
exact standard and category in each finding. Use the current official lists;
do not remap a finding to an older category number.

### OWASP Top 10 (2025)

- **A01 Broken Access Control:** enforce object, function, tenant, and admin
  authorization server-side; default deny and prevent horizontal escalation.
- **A02 Security Misconfiguration:** safe production defaults, least-exposed
  services, hardened headers, no debug output, and reviewed cloud/runtime config.
- **A03 Software Supply Chain Failures:** lock and verify dependencies and build
  inputs; protect CI/CD, registries, provenance, and update paths.
- **A04 Cryptographic Failures:** approved algorithms and key management; protect
  sensitive data in transit and at rest; never place secrets in source.
- **A05 Injection:** parameterize commands and queries, validate untrusted input,
  and contextually encode output.
- **A06 Insecure Design:** threat-model trust boundaries, abuse cases, rate
  limits, and fail-closed behavior before implementation.
- **A07 Authentication Failures:** resist enumeration and brute force; use secure
  recovery, MFA where warranted, rotation, expiry, and session invalidation.
- **A08 Software or Data Integrity Failures:** verify signatures and provenance,
  validate deserialized data, and prevent untrusted update or plugin execution.
- **A09 Security Logging and Alerting Failures:** record and protect meaningful
  security events, detect abuse, alert operators, and avoid sensitive log data.
- **A10 Mishandling of Exceptional Conditions:** handle errors, timeouts,
  resource exhaustion, partial failure, and cleanup without failing open.

Official list: https://owasp.org/Top10/

### OWASP API Security Top 10 (2023)

For APIs, explicitly check **API1 Broken Object Level Authorization**, **API2
Broken Authentication**, **API3 Broken Object Property Level Authorization**,
**API4 Unrestricted Resource Consumption**, **API5 Broken Function Level
Authorization**, **API6 Unrestricted Access to Sensitive Business Flows**,
**API7 Server Side Request Forgery**, **API8 Security Misconfiguration**, **API9
Improper Inventory Management**, and **API10 Unsafe Consumption of APIs**.
Trace each request through object/property/function authorization, quotas and
cost bounds, business-flow abuse controls, outbound URL policy, versioned API
inventory, and validation of third-party responses.

Official list: https://owasp.org/API-Security/editions/2023/en/0x10-api-security-risks/

### OWASP MASVS v2.1+ Mobile Baseline

For native or hybrid mobile changes, map findings to **MASVS-STORAGE**,
**MASVS-CRYPTO**, **MASVS-AUTH**, **MASVS-NETWORK**, **MASVS-PLATFORM**,
**MASVS-CODE**, **MASVS-RESILIENCE**, or **MASVS-PRIVACY**. Check local data and
backup exposure, key handling, authentication/session flows, TLS and endpoint
trust, IPC/deep links/web views, update/runtime safety, tamper resistance where
the threat model requires it, and privacy-minimized collection/disclosure.

Official standard: https://mas.owasp.org/MASVS/

## Suede-Specific Checks

Always check these when relevant:

- auth/session behavior between app, API routes, native shells, and server code;
- creator rights, provenance, registry, licensing, royalty, and agent-commerce
  claims match implemented behavior;
- payment, wallet, x402, checkout, and credit flows fail closed;
- public pages do not invent metrics, pricing, partner claims, testimonials, or
  release promises;
- Vercel/account/deploy assumptions match local guidance before production
  claims;
- App Store/iOS screenshots, metadata, privacy answers, and build behavior match
  the actual app;
- migrations, env vars, feature flags, cron/jobs, queues, webhooks, and secrets
  are documented and deployable;
- multi-repo or multi-surface contracts do not drift across web, backend,
  mobile, public sites, and docs.

## Swift / iOS Traps

Check on every Swift file in the diff. iOS ships on a release cycle with no hot-fix — a crash here is live for days.

- **Force operations (`!`, `try!`, `as!`):** each crashes when the optional is nil or the cast fails. Flag unless the failure case is provably eliminated immediately above. `try!` on anything that throws at runtime (decoding, file I/O) is P1.
- **Retain cycles in closures:** an escaping closure that strongly captures `self` inside a stored property, `Task`, Combine sink, or callback leaks the owner. Require `[weak self]` (or `[unowned self]` only when lifetime is provably bound).
- **UI work off the main thread:** mutating `@State`, `@Published`, or UIKit views from a background context is undefined behavior. Flag observable or UI mutation inside `Task.detached`, a URLSession callback, or a background queue with no hop to `@MainActor` / `DispatchQueue.main`.
- **Actor and concurrency misuse:** actor-isolated state mutated across a suspension point without re-checking invariants (reentrancy); `nonisolated` used to silence a warning rather than because access is truly isolation-free; `@MainActor` work awaited from a path that should already be on main.
- **Codable fragility:** a non-optional property decoding a field the server may omit or send null fails the whole decode and drops the response. Match optionality to the real API contract; flag `decode` on fields the backend does not guarantee.
- **SwiftUI identity and lifecycle:** `ForEach` over a non-stable `id` (index, or a value that changes) loses state and breaks animations; `onAppear` used for one-time work re-fires on re-insertion; `@StateObject` vs `@ObservedObject` confusion (owning vs observing) re-creates or prematurely releases models.
- **Leaked resources:** unbounded image/data caches; URLSession tasks not cancelled on disappearance; observers or timers added with no matching removal.

Pair with iOS / Native Contract Drift below: crash risk here, contract break there.

## iOS / Native Contract Drift

Check on any API route, response shape, auth header, or shared type that iOS or other native consumers depend on:

- **Response shape change:** field renamed, field removed, field type changed (string → number, nullable → required), or new required field added without a default. Flag any change to an API route's return value that is not purely additive and backward-compatible.
- **Route path or method change:** endpoint renamed, HTTP method changed (POST → PUT), or path parameters reordered. iOS has no hot-reload — a renamed route is a hard crash until the app ships an update.
- **Auth header or token format change:** changes to how `Authorization`, `X-Session-Token`, or similar headers are validated server-side. If the server changes the expected format, the iOS app gets 401s on every request.
- **Error response shape change:** iOS likely pattern-matches on `{ error: string }` or `{ code: number }`. Changing the error envelope silently breaks native error handling with no visible failure on the web surface.
- **New required query param or body field:** adding a required field that old app versions don't send causes the new server to reject requests from users who haven't updated yet.
- **Shared type drift:** TypeScript types in `types/`, `shared/`, or `lib/` consumed by both web and a native build step. A field rename or removal here breaks both surfaces simultaneously.

Blast radius note: identify which iOS version is currently in production. If the app hasn't shipped an update in >2 weeks, assume the old contract is live for the majority of users and treat breaking changes as P0.

## Technical Debt

Flag tech debt patterns as P3, group by file, don't block ship. Do not block a ship on P3 tech debt unless it directly obscures a P0/P1 bug. File as follow-up.

## Intent Compliance and Scope

Code that works but does not do what it claimed is still a defect.

- **Claim vs diff:** restate what the change says it does — PR title, description, linked issue, commit subject — and confirm the diff delivers it. Map every acceptance criterion to a code path or a test. Claimed behavior with no corresponding change is a P1 truth gap.
- **Scope creep:** flag changes that do more than they claim — an unrelated refactor riding inside a bugfix, a dependency bump bundled with a feature, a formatting sweep that buries the real diff. Name the unrelated clusters and recommend splitting.
- **Review-effort signal:** state diff size (files / net lines) and an effort read — trivial / moderate / heavy / too-large-to-review-safely. A single PR mixing auth, payments, and a migration should be split before it is safe to judge.

## Change Walkthrough (multi-file PRs)

For a PR summary or any review spanning four or more files, lead with a walkthrough so the reader sees the shape before the findings:

- **Per-file table:** file → one-line what-changed → risk lane. Collapse generated or trivial files into one row.
- **Flow diagram when warranted:** emit a mermaid `sequenceDiagram` (request → handler → service → data) or `flowchart` when the change moves data across three or more boundaries or alters an async, auth, or payment path. Skip it for a localized edit — a diagram of a one-file change is noise.

The walkthrough orients; it never replaces findings, and stays above the Findings block.

## Precision Pass (before output)

False positives are why reviewers get muted. Self-check the draft findings before emitting:

- **Evidence test:** every finding ties to a file:line, a reproduction or trace, and a concrete fix. Drop what cannot.
- **Already-handled test:** drop what a formatter, the type checker, a configured linter, or a documented project rule already covers — do not re-report a gate's job as a manual finding.
- **Confidence gate:** mark each finding high / medium / low. Collapse low-confidence style observations into a single "nitpicks" line; never let them outrank a real P-level finding.
- **Net-signal test:** if a finding would not change the ship decision and would not be worth a human reviewer's comment, cut it. Volume is not the product.

## Red Flags — Stop

- "CI is green, skim the checklists" — green CI that never exercised the change proves nothing.
- "The PR description explains it" — review the diff, not the story about the diff.
- "Small diff, skip the gates" — the Deploy Safety Gate and Commit Dirt Score run on every review, no exceptions.
- "Flag everything to be safe" — volume is noise; run the Precision Pass and cut what won't move the ship decision.
- "I wrote this code, a quick self-check will do" — switch fully into review mode and hunt what your implementation would miss.

## Output Shape

For a review:

```text
Findings
Deploy Safety
Commit Dirt Score
Open Questions
Verification Checked
Ship Gate
```

For no findings, say that clearly and name any residual risk or unrun checks.

For a PR summary:

```text
Summary
Change Map
Risk Map
Verification
Ship Gate
```

The ship gate is always the last line of a review output:

```
SHIP GATE: hold | ship-with-caveats | ship
Reason: [one sentence, naming the blocking finding ID or named caveat]
```

- `hold`: a blocker or high-risk unknown remains.
- `ship-with-caveats`: no blocker remains, but named non-critical caveats exist.
- `ship`: no known blocker remains and required verification passed.

## Routing

- Findings plus a letter grade in one pass → **suede-code**
- The grade alone, no findings → **suede-code-grader**
- Findings fixed; make CI block regressions on merge → **suede-ci-gate**
- The diff touches an LLM, RAG, or agent surface → **suede-ai-eval**
- Fixes need coordinated parallel lanes → **suede-agent-teams**
