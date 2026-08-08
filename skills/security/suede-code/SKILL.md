---
name: suede-code
description: "Review and grade code in one pass: real findings, A-F ship verdict, auth/payment risk, OWASP checks, deploy safety, and fix briefs."
---

# Suede Code

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


One pass for code: a deep, evidence-based review **and** a blunt A-F ship grade, together by default. Findings tell you what is wrong; the grade tells you whether it ships. Every finding has a file, evidence, and a fix path. No findings without evidence. No volume without signal.

**Runs only when asked.** This skill never auto-fires on a diff, a save, or a commit. Invoke it explicitly (review this, grade this, security-check this, is this safe to ship). Do not run it as a side effect of other work.

## Model Routing

Default: Sonnet. Recommend Opus for auth, payments, and public API surface reviews.

## Operating Stance

- Review current source, current diff, local docs, and relevant runtime behavior.
- Keep code generation and review separate. If you authored the code, switch into review mode and look for what your implementation would miss.
- Preserve user and other-agent WIP. Do not stage, revert, or rewrite unrelated files.
- Prefer high-signal findings over volume. Do not leave style nits when formatters or local conventions already handle them.
- Every blocking finding needs evidence, impact, and a concrete fix path.

## Review Contract

Before reviewing, identify:

- **target:** repo, branch, PR, commit range, diff, route, API, or release build;
- **intent:** what the change claims to accomplish;
- **risk lanes:** frontend, backend, data, auth, payments, contracts, iOS, release, public copy, analytics, secrets, deployment, docs.

## Context Graph

Build a lightweight graph before judging the diff:

1. Changed files and generated files.
2. Imports, callers, routes, API handlers, jobs, hooks, models, schemas, and config/env dependencies touched by the change.
3. Tests, fixtures, migrations, release scripts, docs, and screenshots that should move with the behavior.
4. Runtime surfaces: local route, live URL, API endpoint, simulator flow, dashboard, App Store metadata, or deployment target.
5. Domain contracts: creator ownership, rights/provenance, registry-backed media, royalty routing, agent commerce, wallet/payment flows, and published-statement accuracy.

Flag beyond-the-diff risks when related files, defaults, docs, env, or deploy requirements no longer agree.

## Run Gates and Honor Project Rules

Before manual analysis, run the gates the repo already ships and fold results in — typecheck, the configured linter on changed files, the test suite, the dependency auditor when deps changed, and a real secret scanner over the diff. Detect what exists; run only that; never fabricate a result you did not run, and note in Verification when a gate could not run. Then read the repo's own conventions — `CLAUDE.md`, `AGENTS.md`, linter/formatter config, nearest-ancestor rules — and treat them as binding: do not flag what a rule permits, do flag what it forbids, and do not re-raise a pattern the user already accepted.

## Review Modes

- **Fast diff review:** small change, narrow blast radius, focused findings.
- **Deep PR review:** multi-file behavior, public surface, data/auth/payment, release, or cross-repo risk.
- **Plan review:** implementation has not started; inspect scope, sequencing, acceptance criteria, test mapping, missing decisions.
- **Fix verification:** review after fixes; rescan changed files and confirm the original finding is gone.
- **Release review:** validate build, secrets, env, public copy, screenshots, metadata, deployment, and live/API readback.

### Depth Levels

Add a `--depth` modifier:

- **`--quick`** (~2 min): pattern scan — obvious bugs, hardcoded secrets, missing null checks, injection patterns, broken error handling. No cross-file analysis.
- **`--standard`** (default, ~10 min): per-file correctness on changed paths, language traps (below), state handling, test coverage on changed behavior, call graph within changed files.
- **`--deep`** (~25 min): cross-file analysis with full import graph and call-chain tracing — semantic bugs that only appear when you follow data across module boundaries. Use for auth, payments, migrations, and public API changes.

State the depth level at the top of every output.

---

## Step 1 — Instant-F Triggers (check before scoring anything)

Any single match is an automatic **F**. Stop, report the file and line, and do not grade the remaining lanes — the grade cannot be raised by other lanes. This list is the canonical copy; suede-code-grader carries the identical list — change both together.

**Secrets and credentials** — hardcoded API key/secret/token/password in committed source; private key or certificate committed; OAuth/signing secret outside a secret manager.
**Injection** — SQL built by string concatenation with user input; shell command from user input via exec/spawn/eval; template rendered with unescaped user input where XSS is reachable.
**Auth bypass** — auth middleware with a path that skips it (early return, swallowed exception, always-true condition); permission check bypassable via request param; JWT accepting `alg: none` or a hardcoded secret.
**Payment and wallet** — payment handler swallowing errors silently; webhook with no signature verification; amount or recipient from untrusted input without server-side validation.
**Data destruction** — migration with DROP/destructive ALTER, no rollback, no tested restore; bulk delete/update with no WHERE or user-controlled WHERE; cache invalidation that clears production stores with no restore path.
**Plaintext sensitive data** — password stored or logged in plaintext; PII to an unencrypted log/analytics pipeline; SSN/payment card/health data in a non-encrypted field.

## Step 2 — Language Traps

**TypeScript** — `any` where `unknown` + a guard belongs; non-null `!` without a proving guard; non-exhaustive discriminated unions (missing `assertNever`); unsafe `as` casts without a preceding guard; `Object.keys()` without `keyof typeof`; `return someAsyncFn()` that should `await`.

**React** — missing/incomplete `useEffect` deps; stale closures (e.g. `setInterval` in `useEffect(fn, [])` reading state); missing/`index`-as-`key` on `.map()` with identity items; inline object/function props without `useMemo`/`useCallback` in hot paths; prop drilling past 2 levels (P3); state mutation without a setter (`arr.push` on state).

**Next.js** — server/client boundary violations (`'use client'` importing server-only modules, or server files using browser globals); missing `Suspense` around async server components; missing `error.tsx`/`loading.tsx` on user-facing data routes (P2); non-`NEXT_PUBLIC_` secrets reachable in client bundle; uncached `generateMetadata`/`getServerSideProps` external fetches; `next/router` imported in App Router.

**Database (Drizzle/Prisma)** — N+1 queries in loops; missing index on filtered/sorted/join columns; multi-table writes without a transaction; missing unique constraints on logically-unique fields; unbounded selects with no `LIMIT` on growable tables.

**Performance** — new >20 KB minzipped imports (flag with size, prefer tree-shaken); render-blocking `<script>` without `async`/`defer`; non-critical routes not lazy-loaded (`next/dynamic`); raw `<img>` instead of `next/image` for non-SVG assets.

**Swift / iOS** — force `!`/`try!`/`as!` without a proving guard (P1 on runtime-throwing `try!`); escaping closures capturing `self` strongly (need `[weak self]`); UI/`@Published`/`@State` mutation off the main thread; actor reentrancy across suspension points; non-optional `Codable` fields the server may omit; `ForEach` over non-stable `id`; URLSession tasks/observers not cancelled.

**Whole-repo (`--deep`)** — past the changed-file import graph, sweep every caller of a changed symbol across the repo, check shared assumptions (config/defaults/env mirrored elsewhere), `git log -L`/`blame` the touched lines for reintroduced regressions, and confirm the change matches its sibling pattern. Name what you traced.

## Step 3 — OWASP Top 10 (auto-runs on auth/api/middleware/routes or crypto/session/payment imports)

Cite the category in the finding. A01 Broken Access Control (authz at every data access, no horizontal escalation) · A02 Cryptographic Failures (encryption in transit/at rest, no MD5/SHA-1/DES, secrets in env) · A03 Injection (parameterize, escape output) · A04 Insecure Design (assume unauthenticated attacker, designed-in rate limits) · A05 Misconfiguration (changed defaults, safe errors, debug off) · A06 Vulnerable Components (current deps, no CVEs) · A07 Auth Failures (MFA, brute-force protection, session invalidation) · A08 Integrity Failures (protected CI/CD, verified checksums, validated deserialization) · A09 Logging/Monitoring Failures (auth/access/validation failures logged and tamper-protected) · A10 SSRF (URL allowlist, no internal fetches).

## Step 4 — Grade (A-F, runs by default)

Score each lane A-F, then one overall. For non-Suede work, substitute "domain truth" for "Suede truth."

- **Correctness** — behavior, edge cases, error paths, async, routing, data flow, regression risk.
- **Security and permissions** — auth, secrets, payment, wallet, injection, path, SSRF, permission, data exposure fail closed.
- **Data and state** — schemas, migrations, caches, jobs, queues, webhooks, retries, idempotency, state transitions stay consistent.
- **Suede truth** — public copy, rights, provenance, registry-backed media, royalty routing, licensing, agent-commerce, product claims match the implementation.
- **UX and release behavior** — loading, empty, error, success, mobile/native, screenshot, metadata, route states hold together.
- **Tests and verification** — changed behavior has meaningful tests, builds, screenshots, simulator runs, live/API readbacks, or named caveats.
- **Deploy readiness** — env vars, flags, configs, migrations, rollback notes, install paths, docs, release sequencing are clear.

**Grade meaning:** **A** all lanes pass, runtime-verified, no follow-ups. **B** no blockers, named bounded follow-ups. **C** a real defect or unverified risk that could surface in production — recommend hold until fixed. **D** a serious defect likely to cause data loss, auth bypass, broken payments, or user-visible failure — recommend against shipping and, because these are extreme-risk categories, pause and put the ship choice to the user. **F** breaks core behavior, hits an Instant-F, or critical-surface evidence is absent.

**Recommended gate follows the grade, mechanically:** A → `ship`; B → `ship-with-caveats`; C, D, F → `hold`. A Deploy Safety finding (Step 5) also moves the recommended gate to `hold` regardless of grade. The gate is a recommendation the user acts on, not a lock on the agent.

**Grade caps by surface** (state explicitly when they apply):
- **Auth** (login, session, token, middleware, roles) — A needs the bypass/escalation path tested, not just happy path; B needs happy-path + named caveats; else cap **C**.
- **Payment/wallet** (checkout, subscription, refund, payout, transfer, webhook) — A needs error paths tested (failed charge, declined, replay) + server-side amount/recipient validation + no silent swallowing; B needs happy-path + documented error-path risk; else cap **C**.
- **Data migrations** — A needs a documented rollback + restore tested against prod-like data (or justified waiver); B needs a rollback plan, restore untested; no rollback plan caps at **D**.
- **Public API changes** — A needs verified backward-compat or a versioned migration path; breaking with no path caps at **C**.

**Tech debt** — grade impact depends on location, not just pattern. Debt in auth/payment/migration paths is one level stricter (a God object in a payment module is D, not C). Debt in core/high-traffic is standard. Debt in utilities/scripts is flagged as a Required Upgrade but does not lower the overall grade unless it bleeds into a critical path. Do not block a ship on tech debt alone unless it directly obscures a P0/P1 bug.

## Step 5 — Deploy Safety Gate (runs at the end, every time)

Grade each pass/conditional/block: **breaking changes** (block if a contract changes with no migration), **rollback safety** (block if `git revert` can't undo it — migrations, charges, sent email, deletes), **blast radius** (state ~0% / ~partial / ~100%), **environment readiness** (block if a required env var isn't in prod yet), **dependency changes** (block on CVE or unpinned prod dep), **data mutations** (block on irreversible writes with no tested restore), **security delta** (block if new attack surface without mitigation).

## Finding Format

Lead with findings, ordered by severity. Group repeated patterns once.

```
[P0] path/to/file.ts:142
Issue: JWT secret falls back to empty string; any token is valid when SECRET is unset.
Fix: process.env.JWT_SECRET ?? (() => { throw new Error('JWT_SECRET required') })()
Verify: set JWT_SECRET="" and curl /api/me — expect 401, currently 200.
OWASP: A02 Cryptographic Failures
Confidence: high
```
P2/P3 get one line each. **Severity:** P0 data loss/security/payment/broken release/unsafe public behavior · P1 likely prod regression, auth bug, broken primary path, false published statement, missing deploy requirement · P2 meaningful edge-case failure, incomplete state, test gap on changed behavior · P3 low-risk improvement, clarity, cleanup. If it can't be tied to a file/route/command/state/behavior, mark it an open question.

## Fix Mode (only on `--fix` or explicit request)

Auto-apply local P2/P3 fixes (single file, no contract change), each as its own commit with the finding ID. Present P0/P1 as confirmed fix briefs before applying — never auto-apply to auth, payment, or data-migration code without explicit confirmation. Re-run the relevant mode on changed files after fixing; cap at 3 cycles, then escalate as a design issue.

## Suede-Specific Checks

Auth/session behavior across app, API, native shells, and server · creator rights/provenance/registry/licensing/royalty/agent-commerce claims match implemented behavior · payment/wallet/x402/checkout/credit flows fail closed · public pages invent no metrics, pricing, partners, testimonials, or release promises · Vercel/account/deploy assumptions match local guidance before prod claims · App Store/iOS screenshots, metadata, privacy answers, and build behavior match the app · migrations, env, flags, cron/jobs, queues, webhooks, secrets are documented and deployable · multi-surface contracts don't drift across web, backend, mobile, sites, docs.

## Intent, Scope, and Precision

Confirm the diff delivers what it claims — map each acceptance criterion to code or a test; unbacked claims are a P1 truth gap — and flag scope creep (unrelated refactors, bundled dep bumps, formatting sweeps that bury the change); recommend splitting an over-large PR. Before emitting, self-check: every finding has a file:line + fix, nothing duplicates a gate's job, low-confidence style notes collapse into one "nitpicks" line, and anything that would not move the ship decision is cut.

## Red Flags — Stop

Catch yourself thinking any of these and re-run the gate you were about to skip:

- "CI is green, so it's fine" — CI that never exercised the changed behavior is not evidence.
- "The diff is small" — small diffs touch auth and payments too; Instant-F triggers run every time.
- "I wrote this, I know it works" — switch into review mode and hunt what your implementation would miss.
- "The author explains the intent well" — intent is not a test, a readback, or a screenshot.
- "It was hard work, round up to B" — effort never moves a grade; evidence does.
- "Skip the deploy gate, it's just a copy change" — Step 5 runs at the end, every time.

## Output Shape

Lead with a **Simple explanation (plain, for a 10-year-old)** — one plain-English paragraph a 10-year-old follows: did it pass, and the single biggest reason. Then:

```text
Findings           (by severity, with evidence + fix)
Code Grade         (7 lanes A-F + overall, grade cap if any, why, required upgrades)
Deploy Safety      (the 7 dimensions + verdict)
Open Questions
Verification       (checked / not checked)
SHIP GATE: hold | ship-with-caveats | ship — [one sentence naming the blocker or caveat]
```

For no findings, say so clearly and name any residual risk or unrun checks. Do not invent tests, screenshots, live checks, or deploy status. To revise a grade, name what changed; to bank a pattern, name what worked; silence = accepted.

## Worked Example

A real review, not a fictional one — this is `suede-code` actually reviewing
and grading a real file from this repo: `scripts/validate-skill-pack.mjs`
(398 lines, the script that gates every skill-pack release). Read in full,
then run directly (`node scripts/validate-skill-pack.mjs`, exit 0, "Validated
21 skills against 21 catalog entries") and probed with targeted Node
snippets against its own regexes and real frontmatter from this repo before
writing the finding below. Depth: `--standard`. This is what the Output
Shape looks like filled in, not a template.

**Historical snapshot:** the pack had 21 public skills when this example was
written; the counts and named skills below (21, "16 of 21") are frozen
evidence from that run, not a claim about the current pack size. The finding
itself — the regex only catching the first `(use X)` target per `NOT FOR`
line — is still live regardless of pack size.

**Simple explanation (plain, for a 10-year-old):** This robot checks that
every skill folder has its paperwork in order before anything ships. It
works, and running it right now says everything currently passes. But the
robot has one blind spot: when a skill says "don't use me for X or Y, use
those instead," the robot only double-checks that X is a real skill and
forgets to check Y. Right now that blind spot hasn't let anything broken
through, but it's not actually checking what it claims to check.

```text
Findings

[P2] scripts/validate-skill-pack.mjs:48 (used at line 257)
Issue: extractNotForRedirects() uses the regex
  /NOT FOR:[^.]*?\(use ([a-z][a-z0-9-]+)(?: — private)?\)/g
  which anchors every match on the literal "NOT FOR:" string. When a single
  NOT FOR clause names multiple redirect targets separated by semicolons —
  e.g. "NOT FOR: full findings+grade in one pass (use suede-code);
  findings-only ... (use suede-code-review)" — only the first "(use X)" is
  captured, because the second is not preceded by another "NOT FOR:" and
  the non-greedy [^.]*? stops consuming at the first match. Confirmed live:
  16 of 21 skills in this pack (76%) have 2+ "(use X)" targets on one NOT
  FOR line — johnny-suede-design, johnny-suede-write, suede-agent-teams,
  suede-ai-eval, suede-campaign-in-a-box, suede-code (3 targets),
  suede-code-grader, suede-code-review, suede-release-linter,
  suede-rights-audit (3), suede-rights-passport, suede-seo-audit (3),
  suede-ci-gate, suede-site-alchemy (3), suede-sync-packaging (3),
  suede-visibility-grader — and for every one of them, the existence check
  at line 258 ("named skill X does not exist in skill pack") only runs
  against the first target, never the second or third. Today this hasn't
  let a broken reference through — spot-checked suede-code's own 3 targets
  (suede-code-review, suede-code-grader, suede-ai-eval per the file, though
  the regex only actually verifies suede-code-review) and all named skills
  genuinely exist as folders — but the coverage gap is real: 2 of every 3
  redirect targets in a 3-target NOT FOR line ship with zero validation.
  A renamed or deleted skill referenced only as the 2nd/3rd target in
  someone else's NOT FOR line would pass this gate silently.
Fix: run the regex per-clause instead of per-line, e.g. split on
  /;\s*/ within the NOT FOR sentence and match each clause independently,
  or drop the "NOT FOR:" anchor requirement after the first match and
  keep matching "(use X)" until the sentence-ending period:
    const re = /\(use ([a-z][a-z0-9-]+)(?: — private)?\)/g;
  run only within the substring from "NOT FOR:" to the next ". " —
  this catches every parenthetical redirect in the clause, not just the
  first.
Verify: after the fix, run extractNotForRedirects() against suede-code's
  real frontmatter description and confirm it returns 3 matches
  (suede-code-review, suede-code-grader, suede-ai-eval), not 1. Then rerun
  `node scripts/validate-skill-pack.mjs` and confirm it still exits 0 on
  the current, already-correct skill pack (a fixed regex should not
  introduce new failures against content that was already valid).
Confidence: high — reproduced directly against the live regex and real
  frontmatter from this repo, not inferred from reading alone.

[P3] scripts/validate-skill-pack.mjs:72-81
descriptionsDiffer() returns false (no warning) whenever either input
string is empty or whitespace-only, because wa.size === 0 short-circuits
before the Jaccard comparison. An empty frontmatter description is
already caught separately by the explicit `if (!skillFmDesc)` check at
line 195, so this doesn't currently let a real gap through — but the
function's own contract ("do these two descriptions differ") silently
degrades to "don't know" on empty input rather than "yes, maximally."
Low-risk; flagging for clarity, not blocking.

[P3] scripts/validate-skill-pack.mjs — no committed test file
This script has no unit tests of its own (no scripts/*.test.mjs, no test
runner in package.json). Its regexes and heuristics (frontmatterYamlIssues,
descriptionsDiffer, extractNotForRedirects, openaiYamlStructureIssues) are
exercised only by running it against whatever the skill pack currently
contains — which means a regression in the checker itself (like the P2
above) has no regression net and can only be caught by someone manually
probing the regex, as done for this review. Worth a small fixtures-based
test file given this script is the release gate for the whole pack.

Code Grade

Correctness: B — the script does what it says for single-target NOT FOR
  lines and every other check (VERSION/catalog version match, frontmatter
  name match, YAML frontmatter issues, OpenAI agent YAML structure,
  short_description length, docs page presence, catalog/filesystem skill
  parity, plugin skill references, private-path/secret pattern sweep,
  README/docs skill-count match) — all verified by reading the logic and
  cross-checking against the real repo state, and the live run confirms
  a clean pass. The P2 above is a real correctness gap in one specific
  check's coverage, not a false negative today, so it holds at B rather
  than dropping further.
Security and permissions: A — no auth, no network, no user input in the
  execution path; it's a build-time linter run locally and (per its
  purpose) presumably in CI. The privatePathPatterns/secretPatterns sweep
  (lines 294-311) is itself a security-adjacent control and was verified
  to correctly match a live example (the current repo's own /Users/
  jasoncolapietro/... path pattern, tested directly and confirmed to trip
  the leak detector as designed).
Data and state: A — no database, no writes, no migration; it's a pure
  read-and-report script (fs.readFileSync everywhere, zero fs.writeFileSync
  calls in the file).
Domain truth: A — every claim this script encodes about the skill pack's
  own rules (VERSION must match catalog.json, frontmatter name must match
  folder name, description must exist and be non-trivial, docs pages must
  exist for flagship skills, README/docs skill counts must match the real
  folder count) was cross-checked against the actual current repo state
  and the checks are accurate to what they claim to verify, with the one
  documented exception in the P2 finding.
UX and release behavior: A — clear pass/fail output (Validated N skills
  against M catalog entries on success; Warnings/Failures lists with
  process.exit(1) on failure), suitable for both a human running it
  locally and a CI step gating a merge.
Tests and verification: C — no committed tests for this script itself,
  and the P2 above is exactly the kind of regression a fixtures-based
  test suite would have caught before it shipped. This is a QA/gating
  script with no regression net on its own logic — real gap, not a style
  nit, because the entire job of this file is being a reliable safety
  net for everything else.
Deploy readiness: A — zero config, zero env vars, runs via
  `node scripts/validate-skill-pack.mjs` with an optional --profile flag;
  confirmed the current invocation runs clean with no setup.
Overall: B
Grade cap applied: none — not an auth, payment, migration, or public-API
  surface; standard scale applies.
Why: No P0/P1s, no Instant-F triggers, and the script's core job (gate
  the release) works today against the real repo. It holds at B rather
  than A because of one real, reproduced coverage gap (P2, drags
  Correctness and Tests and verification down) in the exact category of
  logic this script exists to be trustworthy about — a validator with an
  unverified corner of its own validation logic is a bounded, named
  follow-up, not a blocker, but it keeps this out of A until closed.
Required upgrades:
1. Fix extractNotForRedirects() to catch every "(use X)" target in a
   multi-target NOT FOR clause, not just the first (P2 above).
2. Add a small fixtures-based test file for this script's regex/heuristic
   functions, so a future regression in the gate itself doesn't require
   manual probing to catch (P3 above).

Deploy Safety

Breaking changes: n/a — this run graded the file as a standing artifact,
  not a proposed diff; no contract is changing.
Rollback safety: n/a — read-only script, nothing to roll back.
Blast radius: ~0% today (script currently passes clean against the real
  repo) but the P2 gap means blast radius for a future bad reference is
  larger than the script's stated coverage implies — silently ~66% of a
  3-target NOT FOR line's redirects go unchecked.
Environment readiness: pass — zero env vars required.
Dependency changes: pass — single dependency (js-yaml ^5.0.0, already in
  package.json), no new or unpinned deps introduced by this review.
Data mutations: pass — no writes.
Security delta: pass — no new attack surface; this review found a
  QA-coverage gap, not a security hole.
Verdict: no deploy blockers. The P2 finding is a correctness gap in the
  gate's own logic, not a reason to hold today's clean run.

Open Questions
- Is scripts/validate-skill-pack.mjs actually wired into CI (a GitHub
  Actions workflow), or is it a local-only pre-release habit? Not
  verifiable from this file alone — no .github/workflows/ directory was
  inspected as part of this review's scope.

Verification
Checked: full file read; live run (`node scripts/validate-skill-pack.mjs`)
  exit 0, "Validated 21 skills against 21 catalog entries"; extractNotForRedirects()
  regex traced step-by-step against a real multi-target NOT FOR string
  from suede-code's own frontmatter, confirmed only 1 of 3 targets
  captured; scripted a repo-wide count of skills with 2+ "(use X)"
  targets in one NOT FOR line (16 of 21, listed by name above);
  descriptionsDiffer() edge case tested directly with empty-string input;
  privatePathPatterns[0] tested directly against this repo's own live
  filesystem path and confirmed it correctly trips.
Not checked: whether this script runs in CI (no workflow file inspected);
  behavior of openaiYamlStructureIssues() against a deliberately malformed
  agents/openai.yaml (only read, not exercised against a broken fixture);
  performance/behavior on a much larger skill pack (walk() and the regex
  sweeps are O(n) over files, not tested at scale).
SHIP GATE: ship-with-caveats — the script works and gates the pack
  correctly today; the P2 finding (multi-target NOT FOR redirects only
  partially checked) should be fixed before the next time someone adds a
  skill whose only reference is a 2nd/3rd redirect target in another
  skill's NOT FOR line, since that's exactly the failure mode this check
  exists to catch.
```

This is what "genuine" looks like: the P2 finding is reproduced against the
live regex and real frontmatter in this repo (not inferred from reading
alone), the grade lanes cite what was actually checked, and the open
question is named as unverified rather than guessed at.

---

## --threat-verify Mode

Verify that threat mitigations declared in a threat model (ADR threat table, PLAN.md risk section, or an architecture review's threat table) are actually implemented in the codebase.

**Trigger:** pass `--threat-verify` or say "verify threat mitigations" / "check threat model compliance"

**Input:** threat model source — file path or pasted content. Accepted formats: ADR threat table (private Suede Labs companion, not in this pack: suede-arch), PLAN.md risk section, free-form "Threat: X / Mitigation: Y" pairs.

**Process:**
1. Parse the threat model into: { threat_id, description, declared_mitigation, expected_location }
2. For each threat: grep the codebase for the declared mitigation at ALL relevant entry points (routes, handlers, middleware, auth layers)
3. Classify each threat:
   - **CLOSED** — mitigation confirmed at all relevant entry points
   - **OPEN** — mitigation partially implemented (found in some but not all entry points)
   - **UNREGISTERED** — no evidence of declared mitigation in codebase
4. Output THREAT-REVIEW.md:

```
| Threat ID | Description | Declared Mitigation | Status | Evidence | Gaps |
| --- | --- | --- | --- | --- | --- |
```

**Blockers:** OPEN and UNREGISTERED items are reported as blockers — the recommendation is to close them before shipping; the user makes the final call.

**What this is NOT:** This mode does not scan for new vulnerabilities (that is what the OWASP lane does). It only verifies previously declared mitigations exist.

## Routing

- Findings-only, with Accessibility and SEO lanes → **suede-code-review**
- The letter grade alone, no findings → **suede-code-grader**
- Verdict delivered; make CI enforce it on every merge → **suede-ci-gate**
- The diff ships AI behavior with no eval coverage → **suede-ai-eval**
- Fixes span multiple coordinated lanes → **suede-agent-teams**
- Completion-claim law for saying a fix is done, live, merged, or ready →
  private Suede Labs companion, not in this pack: suede-verification-law
