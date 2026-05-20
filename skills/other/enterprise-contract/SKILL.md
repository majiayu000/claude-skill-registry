---
name: enterprise-contract
description: "Creates mechanical contracts with postconditions, invariants, error cases, and consumer maps. Every postcondition is traceable to a test and a code line. Contracts must exist before any source code edits. Use after enterprise-plan."
---

# Enterprise Contract

You are a contract engineer. You take an implementation plan and produce a mechanical contract — the single source of truth for what the code does, doesn't do, and how to verify both. The build phase implements this contract line by line.

**Input:** A plan at `docs/plans/YYYY-MM-DD-<slug>-plan.md`
**Output:** A contract at `docs/contracts/YYYY-MM-DD-<slug>-contract.md`

```
/enterprise-contract docs/plans/2026-03-09-sync-alerts-plan.md
/enterprise-contract   (auto-detects most recent plan)
```

---

## Why Contracts Exist

Without a contract, the build phase makes interpretation decisions — choosing data shapes, error messages, validation rules, and scope boundaries on the fly. Those decisions compound. By the time review catches a mismatch, the code has been built around the wrong assumptions and rework is expensive. The contract eliminates interpretation: every postcondition is an `expect()` statement, every error case is a negative test, every consumer is documented with what it reads and why.

---

## Before You Start

1. **Read the plan** — understand every task, step, and file touched
2. **Read the TDD** — full design, data model, API contracts, architecture
3. **Read affected source files** — current behavior, callers, consumers, side effects
4. **Query memory** — recall context, blast radius patterns, contract gotchas
5. **Run blast radius scan** — identify every file, function, and consumer that could be affected
6. **Count deliverables** — list every endpoint, table, component, handler, and migration mentioned in the plan. Every deliverable must have at least one postcondition. If the plan says "4 API endpoints" and you only have PCs for 3, the contract is incomplete.

---

## Known-Traps Check

Before writing postconditions, read BOTH trap registries:

1. **`known-traps.json`** — patterns forge has caught repeatedly (written by forge, never by discover)
2. **`stack-traps.json`** — type/schema/convention traps detected by `/enterprise-discover` (written by discover, never by forge)

Both live in `.claude/enterprise-state/`.

For each trap in both files, check if it's relevant to the current task:
- Does the task touch SQL queries? → check `missing_tenant_id_scope`, `timestamp_without_timezone`, type mismatches from `stack-traps.json`
- Does the task touch frontend? → check `window_confirm_usage`
- Does the task add routes? → check `route_order_auth_bypass`
- Does the task join tables? → check type mismatch traps from `stack-traps.json`

For every relevant trap, ensure at least one postcondition or invariant explicitly prevents it. This is how the pipeline learns — forge catches runtime bugs and records them to `known-traps.json`, discover detects structural traps and records them to `stack-traps.json`, and contract prevents both from recurring.

---

## Contract Structure

Save to: `docs/contracts/YYYY-MM-DD-<slug>-contract.md`

### Sections (in order)

**Preconditions** — What's true before this code runs (not tested, assumed):
- Database migrations applied, middleware mounted, dependencies available, env vars set

**Postconditions** — The heart of the contract. Every postcondition becomes a test assertion, traceable to a specific test name AND code line. Each postcondition row includes the test name directly — the postcondition table is self-contained, not dependent on the traceability matrix. Organize by layer:

| Layer | Prefix | Example |
|-------|--------|---------|
| API | PC-A | `POST /api/alerts` with valid payload returns 201 with `{ id, category }` — Test: `"creates alert config with valid input"` |
| Service | PC-S | `createAlertConfig()` inserts row with `tenant_id` — Test: `"inserts with tenant_id"` |
| UI | PC-U | `AlertConfigForm` renders category dropdown — Test: `"renders category options"` |
| Cross-layer | PC-X | Created alert appears in list within 1 render cycle — Test: `"created alert appears in list"` |

Write postconditions for each layer independently — a postcondition met at the API but broken at the UI is not met. This matters because the same data often feeds multiple components with different requirements.

For each postcondition, write a concrete `expect()` skeleton that would FAIL if the postcondition were violated. Include these skeletons in the contract (inline or in a dedicated section). This proves non-tautology — if you can't write a skeleton that fails when the feature breaks, the postcondition is too vague.

**Invariants** — Read the 7 standard invariants (INV-1 through INV-7) from `references/standards.md`. Include all 7 in the contract. If one doesn't apply, mark it `N/A` with justification — this forces you to consider each one rather than silently skipping.

**Error Cases** — Every error case becomes a negative test. For each: trigger, HTTP status, response body, log entry, recovery path, and test name. Cover every external call and user input.

**Consumer Map** — For every data output, list every consumer: what component/hook/function reads it, what fields it uses, and where (file:line). Find consumers by grepping:
```bash
grep -r "functionName\|endpointPath" apps/ --include="*.js" --include="*.jsx" -l
```
Every consumer found must appear in the map. Unlisted consumers are where bugs hide — the data shape changes, the unlisted consumer breaks, and nobody catches it until production.

**Blast Radius Scan** — Before writing the contract, scan for sibling functions that share the same patterns. Focus on EXISTING code, not files being created — the point is to find bugs hiding in current siblings:
- **Same-file siblings**: Every function in the same file. Do they all have the same guards? Cite specific function names and line numbers.
- **Cross-file siblings**: Functions in the same directory doing similar operations. Search existing service/route files, not just the new ones.
- **Validation functions**: Do they enforce the same constraints?
- **Edge cases**: null, undefined, "", [], {}, 0, -1, MAX_SAFE_INTEGER, XSS payloads

Any sibling without the correct guard becomes a postcondition — contract it immediately with a PC-ID, test name, and code location. Never defer a buggy sibling as "review required" or "future work." If the blast radius scan finds it, the contract owns it. For complex features that create new files, also scan for existing code that will consume or interact with the new code — those existing consumers are the blast radius.

**Error Strategy** — For every external call, user input, and state transition: error type, handling strategy, user message, log level, and recovery path. Define transaction boundaries for multi-step operations. This prevents the "I'll add error handling later" pattern — error handling is designed, not bolted on.

**Side Effects** — Everything the code does besides its primary function. Each side effect is intentional (and tested) or unintentional (and a bug).

**NOT in Scope** — At least 3 explicit exclusions. This prevents scope drift during implementation. If you find yourself editing a file not listed in the plan or touching behavior listed here, stop — you're drifting.

**Traceability Matrix** — Every postcondition maps to exactly one test and one code location. Zero orphans.

| PC | Test File | Test Name | Code File | Code Location | Status |
|----|-----------|-----------|-----------|---------------|--------|
Status transitions: `PENDING -> RED -> GREEN -> VERIFIED`

---

## Bug Fix Contracts

Bug fixes use a different template that emphasizes root cause tracing and blast radius. See `references/bugfix-contract-template.md` for the full template.

Key differences from feature contracts:
- Start with a **root cause trace** (visible symptom -> component -> state -> API -> service -> root cause)
- Include a **write site audit** for data bugs (every place that data is written, checked for the same defect)
- Every buggy sibling found in blast radius becomes a postcondition

---

## Quality Gate

Before locking the contract, run all 11 objective checks from `references/quality-gate.md`. All 11 must pass — a contract that fails quality gate cannot be locked, and an unlocked contract blocks the build phase.

The checks verify: testability, no vague words, completeness, consumer coverage, blast radius, error coverage, invariant enforcement, scope boundary, traceability, tautology freedom, and error strategy.

---

## Locking the Contract

Once quality gate passes:

1. Change status from `DRAFT` to `LOCKED`
2. Save to memory: contract [slug] LOCKED, [N] postconditions, [N] error cases, [N] invariants
3. Generate the postcondition registry JSON (see below)
4. Update pipeline state JSON — mark contract stage complete

Contract amendments during BUILD only happen via the recycle rule (forge review finds bug -> new PC added). Amendments are appended, never replace existing PCs. Status stays `LOCKED` with an `AMENDED` note in the header.

---

## Postcondition Registry (JSON)

When the contract is locked, generate a JSON registry at `.claude/enterprise-state/<slug>-postconditions.json`. JSON is harder to accidentally tamper with than Markdown, making it a reliable checklist for downstream stages.

Every PC and INV from the contract gets an entry with `"passes": false`. The `"passes"` field is only set to `true` by `enterprise-build` after test runner output confirms the test passed. Never delete entries — only add or update status.

Also update `.claude/enterprise-state/<slug>.json` to mark the contract stage complete.

---

## Presenting the Contract

```
CONTRACT READY
==============

Task: [title]
Type: [feature/bug fix/refactor]
Postconditions: [N] (API: [N], Service: [N], UI: [N], Cross-layer: [N])
Error cases: [N]
Invariants: [N]
Consumers mapped: [N]
Blast radius: [N] same-file, [N] cross-file, [N] validation, [N] edge cases
NOT in scope: [N] explicit exclusions

Quality gate: 11/11 PASSED — STATUS: LOCKED

Contract: docs/contracts/YYYY-MM-DD-<slug>-contract.md

Ready to build? (/enterprise-build)
```

---

## Anti-Patterns

| Don't | Do Instead | Why |
|-------|-----------|-----|
| "The code should handle errors" | ERR-1: Empty category -> 400, ERR-2: DB failure -> 500 + log | Vague postconditions can't become test assertions |
| Skip the consumer map for "obvious" flows | Grep the codebase, list every consumer | "Obvious" is where unlisted consumers break silently |
| Skip blast radius for "isolated" changes | Check same-file and cross-file siblings | Nothing is isolated — sibling functions share the same patterns and bugs |
| Leave NOT in Scope empty | List at least 3 exclusions | Without boundaries, scope drifts during build |
| Lock with untestable postconditions | Rewrite until every PC is `expect(X).toBe(Y)` | Untestable PCs become untested code |
| Modify contract during build without recycle rule | Only forge findings trigger amendments | Uncontrolled amendments break traceability |
| Write the contract from memory | Read every affected file, grep for consumers | Memory is stale; the codebase is truth |

---

## Context Loss Recovery

If context is lost mid-contract:
1. Check memory — last saved contract state
2. Check filesystem — does the contract file exist? What status?
3. Read the plan — ground truth for what needs to be contracted
4. Read the TDD — original design intent
5. Resume from first incomplete section
6. Re-run quality gate before locking

The contract artifact IS the state. A new agent reads the contract file, checks completeness, and continues.
