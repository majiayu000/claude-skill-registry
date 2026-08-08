---
name: suede-code-grader
description: "Give a blunt A-F ship grade for a code change across correctness, security, data, UX, verification, and deploy readiness. Use for a grade, not a findings review."
---

# Suede Code Grader

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


Blunt A-F read on whether code is ready to ship. The output is a grade with evidence, not a lint score or a pile of style notes.

## Source Truth

Read before grading. Do not grade from the PR description or commit message alone.

Inspect:

- repo, branch, remote, dirty state, and relevant local guidance;
- diff, changed files, generated files, and touched routes or APIs;
- imports, callers, schemas, configs, env requirements, jobs, webhooks, scripts,
  tests, and docs that move with the change;
- build, test, lint, typecheck, browser, simulator, MCP, or live/API evidence
  that directly exercises the changed behavior;
- published statements, rights/provenance claims, payment/wallet behavior, registry
  expectations, royalty routing, and agent-commerce contracts when relevant.

If live, test, or runtime checks are not practical, grade the source and mark those lanes as unverified.

## Instant-F Triggers

Check these before scoring any lane. Any single match is an automatic F — no other lanes matter until it is fixed. This list mirrors suede-code's canonical Step 1 list — change both together.

**Secrets and credentials**
- Hardcoded API key, secret, token, or password in source (not .env, not config — in the actual committed file)
- Private key or certificate committed to repo
- OAuth client secret or signing secret in any non-secret-manager location

**Injection**
- SQL query built by string concatenation with user-controlled input (no parameterization, no ORM escaping)
- Shell command assembled from user input via exec/spawn/eval
- Template rendered with unescaped user input where XSS is reachable

**Auth bypass**
- Middleware that checks auth but has a code path that skips it (early return, exception swallowed, condition that always resolves to "authenticated")
- Role or permission check that can be bypassed by manipulating a request parameter
- JWT verified with `alg: none` accepted or with the secret hardcoded in source

**Payment and wallet**
- Payment handler that swallows errors silently (try/catch with empty catch, unhandled promise rejection)
- Webhook handler with no signature verification
- Amount or recipient derived from untrusted user input without server-side validation

**Data destruction**
- Migration with a DROP or destructive ALTER with no rollback and no tested restore
- Bulk delete or update with no WHERE clause or with user-controlled WHERE
- Cache invalidation that clears production data stores without a restore path

**Plaintext sensitive data**
- Password stored or logged in plaintext
- PII written to an unencrypted log or analytics pipeline
- SSN, payment card, or health data in a non-encrypted column or field

If any Instant-F pattern is present: stop, report it, mark the grade F, list the specific file and line, and do not grade remaining lanes. The grade cannot be raised by other lane performance.

## Grade Lanes

Score each lane A-F, then give one overall grade. When grading non-Suede work, substitute "domain truth" for "Suede truth" — use whatever domain invariants apply (API contract truth, published-statement accuracy, data model truth).

- **Correctness:** intended behavior, edge cases, error paths, async behavior,
  routing, data flow, and regression risk.
- **Security and permissions:** auth, secrets, payment, wallet, injection, path,
  SSRF, permission, and data exposure risks fail closed.
- **Data and state:** schemas, migrations, caches, jobs, queues, webhooks,
  retries, idempotency, and state transitions stay consistent.
- **Suede truth:** public copy, rights, provenance, registry-backed media,
  royalty routing, licensing, agent-commerce, and product claims match the
  implementation.
- **UX and release behavior:** loading, empty, error, success, mobile/native,
  screenshot, metadata, route, and user-visible states hold together.
- **Tests and verification:** changed behavior has meaningful tests, builds,
  screenshots, simulator runs, MCP checks, live/API readbacks, or named caveats.
- **Deploy readiness:** env vars, feature flags, configs, migrations, rollback
  notes, install paths, docs, and release sequencing are clear.

## Grade Meaning

- **A:** All lanes pass. Behavior is verified at runtime. No known follow-ups. Example: new feature with unit + integration tests, live readback confirmed, env vars documented, rollback is trivial.
- **B:** No blockers. One or more lanes have named, bounded follow-ups that do not affect correctness or safety in the current release. Example: happy-path tested but edge-case coverage is thin; or migration is forward-only but rollback risk is low and documented.
- **C:** At least one lane has a real defect or unverified risk that could surface in production but is not immediately catastrophic. Hold until that lane is fixed and rechecked. Example: auth path not fully tested; or a data migration with no rollback plan on a low-traffic table; or a God object in a payment module that obscures correctness.
- **D:** A serious defect exists that is likely to cause data loss, auth bypass, broken payments, or a user-visible production failure. Recommend not shipping until the defect is fixed and verified, and because these are extreme-risk categories, pause and put the choice to the user before any ship step. Example: missing auth check on a state-changing endpoint; migration with no tested rollback on a high-traffic table; payment flow that silently swallows errors.
- **F:** Strongly recommend against shipping. The change breaks core behavior, introduces an Instant-F pattern, or verification evidence is absent for a critical surface. Example: hardcoded API key in source, SQL injection via string concatenation, auth middleware that can be bypassed, or a payment handler with zero test coverage and no live readback.

## Grade Caps by Surface Type

Certain surfaces cannot receive A or B without specific evidence beyond passing CI.

**Auth changes** (login, session, token validation, middleware, role assignment, permission checks)
- A requires: explicit test coverage for the bypass/escalation path, not just the happy path. Named evidence (e.g., "tested with expired token returns 401", "role escalation attempt returns 403").
- B requires: happy-path tested plus named caveats on what is not tested.
- If neither condition is met: cap at C regardless of other lane performance.

**Payment and wallet flows** (checkout, subscription, refund, payout, wallet transfer, webhook)
- A requires: error path tested (failed charge, declined card, webhook replay), amount/recipient validated server-side, and no silent error swallowing.
- B requires: happy-path tested, error paths documented as follow-ups with named risk.
- If neither: cap at C.

**Data migrations** (schema changes, backfills, column drops, index changes on production tables)
- A requires: rollback plan documented, restore tested against a copy of production data (or explicitly waived with justification for low-risk/reversible migrations).
- B requires: rollback plan exists but restore is untested.
- If no rollback plan exists: cap at D.

**Public-facing API changes** (new endpoints, breaking changes, removed fields, changed auth)
- A requires: backward compatibility verified or explicit version bump with documented migration path.
- If breaking change with no migration path: cap at C minimum.

State these caps explicitly in the output when they apply.

## Technical Debt Indicators

Flag these patterns as part of the grade assessment:

- **Magic numbers/strings**: constants with no name or explanation that appear in logic.
- **God objects/functions**: a single function or class doing 5+ unrelated things.
- **Deep coupling**: code that reaches across 3+ abstraction layers to access internals.
- **Missing abstraction**: the same 20-line block duplicated in 3+ places.
- **Leaky abstraction**: a module that requires callers to know its internal implementation details to use it correctly.
- **Implicit state**: program behavior depends on hidden global or module-level state.
- **Dead code**: functions, branches, or imports that can never be reached.

Grade impact depends on where the debt lives, not just what it is:

- Debt in **auth, payment, or data migration paths**: one level stricter. A God object in a payment module is D (not C); a missing abstraction in a payment flow with 3+ duplicated branches is C (not B).
- Debt in **core business logic or high-traffic routes**: standard scale below.
- Debt in **utility helpers, scripts, or low-traffic internals**: flag it, record it as a Required Upgrade, but do not lower the overall grade unless it bleeds into a critical path.

Apply grade impact:

- Debt that actively impairs correctness or masks a real bug: D in that lane.
- Debt that creates meaningful maintenance risk in the changed area: C in that lane.
- Debt present but bounded with a named, tracked follow-up: B in that lane.

**Debt severity by location — concrete examples:**

| Pattern | Location | Grade Impact |
|---|---|---|
| God object (5+ unrelated concerns) | Payment module | D in Correctness |
| God object | Utility helper | B in Correctness |
| Missing abstraction (3+ duplicated blocks) | Auth flow | C in Security |
| Missing abstraction | UI component | B in Correctness |
| Deep coupling (3+ layer reach) | Data migration | C in Data and state |
| Implicit global state | API route handler | C in Correctness |
| Dead code | Any | Flag only; no grade impact unless it shadows live code |
| Magic numbers in payment amounts | Payment flow | C in Correctness |
| Magic numbers in UI spacing | UI component | No grade impact; flag as P3 |

Do not block a ship on tech debt alone unless it directly obscures a P0/P1 bug. Name the debt in Required Upgrades and let the overall grade reflect it.

## Red Flags — Stop

- "CI passed, round up" — CI that never exercised the changed behavior raises nothing.
- "The work was clearly hard" — effort never moves a grade; evidence does.
- "It's just a refactor" — Instant-F triggers run on every grade, every time.
- "Happy path works, call it an A" — the grade caps exist because happy paths are never where the risk lives.
- "The PR description is clear enough" — grade the diff and its evidence, or mark the lane unverified.

## Output Format

```text
Simple explanation:
Plain-language summary of the grade and the one biggest reason.

Usual breakdown:
Target:
Change reviewed:
Runtime surfaces:

Grades:
Correctness: A-F
Security and permissions: A-F
Data and state: A-F
Suede truth: A-F
UX and release behavior: A-F
Tests and verification: A-F
Deploy readiness: A-F
Overall: A-F
Grade cap applied: [surface type] — [what evidence would lift the cap] | none

Why:
Evidence-backed explanation of why the overall grade landed there.

Required upgrades:
1. Highest-impact fix.
2. Second fix.
3. Third fix.

Verification:
Checked:
Not checked:
Ship gate: ship | ship-with-caveats | hold
```

Ship gate follows the overall grade, mechanically: A → `ship`; B → `ship-with-caveats`; C, D, F → `hold`.

To revise this grade: name what changed.
To bank a pattern: name what worked so it can be reused.
Silence = accepted.

## Boundaries

- Do not block on style preferences unless they create real maintenance, behavior, accessibility, release, or product-risk cost.
- Do not invent tests, screenshots, live checks, deploy status, or evidence for published statements.
- Never report a C, D, or F without naming the required upgrade that would move the grade.
- Keep the grade independent. Do not raise a grade because the implementation was hard, because CI passed without exercising the changed behavior, or because the author explains the intent well.

## Worked Example

A real grade, not a fictional one — this is `suede-code-grader` actually grading a real file from this repo: `mcp/suede-skills-mcp.mjs` (715 lines, the stdio JSON-RPC MCP server this skill pack ships). Read in full, then exercised at runtime (spawned the process, sent real JSON-RPC requests over stdin, read the stdout responses) before scoring. This is what the Output Format block looks like filled in, not a template.

```text
Simple explanation:
This file runs fine and doesn't have any dangerous bugs. It's a small local
tool, not something the public logs into or pays through, so the bar is
lower than an auth or payment file. One small paint-by-numbers gap: one
tool's reply doesn't get its text length capped like all the others do,
but that data comes from a file in this repo, not from a stranger, so it
can't be used to attack anything.

Usual breakdown:
Target: mcp/suede-skills-mcp.mjs (715 lines), suede-creator-skills repo,
branch main, clean working tree.
Change reviewed: full file (no diff — graded as a standing artifact, not a
PR), since the task was to grade a real file rather than a specific change.
Runtime surfaces: local stdio JSON-RPC MCP server. No network listener, no
auth, no payment, no database, no user-facing production route — it talks
to an MCP client over stdin/stdout on the machine that spawns it.

Grades:
Correctness: A
Security and permissions: A
Data and state: A
Suede truth: B
UX and release behavior: A
Tests and verification: B
Deploy readiness: A
Overall: A
Grade cap applied: none — surface is a local stdio MCP server, not
auth/payment/migration/public-API, so no cap lane applies.

Why:
Correctness: A. Traced every JSON-RPC method by hand and confirmed at
runtime: `initialize`, `ping`, `tools/list`, `tools/call`, `resources/list`,
`resources/read`, `prompts/list`, and `prompts/get` all returned the
expected shape. Unknown tool name, unknown resource URI, and unknown skill
name each produced correct, distinct error handling — `get_suede_skill`
with a bad name returns a tool-level `isError: true` result (per MCP spec,
since the tool ran but found nothing), while `resources/read` and
`tools/call` on to a genuinely unregistered name throw a JSON-RPC
`-32602 Unknown resource/tool` error, caught by the outer try/catch at
line 703-713 and serialized correctly. Verified live:
  - `tools/call get_suede_skill {name: "nonexistent-skill"}` ->
    `{"isError":true,"structuredContent":{"found":false}}`
  - `resources/read {uri: "suede://bogus"}` -> JSON-RPC error -32602
  - `tools/call {name: "bogus_tool"}` -> JSON-RPC error -32602
The 1 MiB input-buffer guard (lines 686-690) was exercised directly: sent
a >1 MiB unterminated chunk, confirmed it resets `buffer = ""` and emits
a clean `-32603` error, then confirmed the very next well-formed request
(`ping`) on the same connection still succeeds. No stuck state after the
overflow path.

Security and permissions: A. No secrets, no injected shell/SQL, no auth
surface to bypass (there is no auth — this is a local dev tool spawned by
an MCP client, same trust boundary as the process that starts it). No
user-controlled path construction; `catalogPath` is built from
`__dirname`, not request input. `boundedString` (line 27-30) caps every
tool argument that gets echoed into `structuredContent` at 2000 chars
before it goes back out, which is the right instinct for a JSON-RPC
server that will eventually take arguments from less-trusted callers.

Data and state: A. No database, no migration, no cache. `catalog.json` is
read once at module load (line 22-23) and treated as immutable static
data for the life of the process — no write path exists anywhere in this
file.

Suede truth: B. Minor inconsistency, not a false claim: `get_suede_skill`
(line 496-506) returns the matched skill's `description` and `useWhen`
straight from `catalog.json` into both `content` text and
`structuredContent.skill` without running them through `boundedString`,
while every other tool handler in the same function (lines 507-548) bounds
every argument-derived string it echoes back. Confirmed by reading: the
longest live `catalog.json` description is 1016 chars (suede-campaign-in-a-box),
so nothing is actually breaking today — this is a consistency gap that
would only bite if a future catalog entry grew past a client's tolerance
for an unbounded field, or if catalog.json ever stopped being pure
repo-controlled data. Named as a Required Upgrade below, not a blocker.

UX and release behavior: A. Every JSON-RPC error path returns a properly
shaped `{jsonrpc, id, error: {code, message}}` envelope (lines 671-680);
parse errors on malformed input lines are caught per-line (line 696-702)
without killing the buffer for subsequent valid lines; notifications
(messages with no `id`) are correctly treated as fire-and-forget and
never generate a response (line 707-709), matching JSON-RPC 2.0 spec.

Tests and verification: B. No committed test file or npm test script
exists for this MCP server specifically (`package.json` only lists the
`js-yaml` dependency, no test runner). Correctness here was verified by
manually spawning the process and sending real requests this session, not
by an automated suite that runs in CI. The repo does have
`scripts/validate-skill-pack.mjs` and the `suede-mcp-qa` skill, which
cover catalog/skill-folder alignment but not this file's JSON-RPC
behavior directly. That's a real, bounded gap — not a blocker, since the
runtime behavior checked out clean by hand, but there's no regression net
if a future change breaks `tools/call` error shaping.

Deploy readiness: A. No env vars, no config, no build step — it's a
single `.mjs` file with one dependency (`js-yaml`, used indirectly via
the shared catalog tooling, not by this file itself... actually unused
by this file: confirmed no `js-yaml` import in suede-skills-mcp.mjs
itself, only `fs`, `path`, and `node:url`). Runs directly via
`node mcp/suede-skills-mcp.mjs` with zero setup, which matches what the
install docs describe.

Required upgrades:
1. Route `get_suede_skill`'s `content`/`structuredContent.skill` output
   through `boundedString` (or an equivalent bound on `description` and
   `useWhen`) for consistency with every other tool handler in the file —
   currently harmless since catalog.json is trusted static data, but the
   inconsistency is worth closing before this server's argument surface
   changes.
2. Add a small scripted smoke test (a checked-in version of the manual
   JSON-RPC exercise run for this grade) so `tools/call`, `resources/read`,
   and error-path shaping have a regression net instead of relying on
   manual verification each time.
3. No third required upgrade — nothing else surfaced.

Verification:
Checked: full file read; live process spawn with real JSON-RPC requests
over stdin covering initialize, ping, tools/list, tools/call (success and
two distinct error shapes), resources/list, resources/read (success and
error), prompts/list; 1 MiB buffer-overflow guard exercised directly and
confirmed recovery; catalog.json's longest description measured against
the unbounded echo path; grep confirmed no `js-yaml` import in this file.
Not checked: behavior under a real MCP client (Claude Code, Codex, etc.)
end to end — only raw stdio JSON-RPC was exercised directly; concurrent/
overlapping request handling under load; the `prompts/get` argument-
substitution paths for all five prompts (spot-checked `suede-copy-seo-audit`
only).
Ship gate: ship
```

This is what "genuine" looks like: every claim above ties to either a line
number in the file or a command actually run against it in this session,
not an invented test result or a guessed line number.

## Routing

- Findings and fix briefs behind the grade → **suede-code** (combined) or **suede-code-review** (findings only, plus Accessibility/SEO lanes)
- Grade is C or below and the repo has no merge gate → **suede-ci-gate**
- The change ships AI behavior with no eval coverage → **suede-ai-eval**
