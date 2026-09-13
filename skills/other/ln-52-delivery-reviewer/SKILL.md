---
name: ln-52-delivery-reviewer
description: "Reviews a completed change for acceptance, regressions and release risk; read-only, not a whole-codebase audit."
---

# Delivery Reviewer

**Goal:** Review only the requested delivery change and the causal paths needed to prove its business outcome. Judge scoped acceptance and release safety with concise evidence; do not audit unrelated code, repair findings, update trackers, or widen scope.

**Execution contract:** The ordered checkboxes are the Definition of Done. Track every item internally as `PENDING`, `PROVEN` with concrete evidence, `CLEARED` with evidence that its condition is absent, or `UNPROVEN` with a gap; reading, delegation, or tool failure is not proof. Reconcile items after each section. Before returning, resolve all `PENDING` and count only `PROVEN` and `CLEARED`; apply the skill's verdict and approval rules to every gap.
Preserve user intent, scope, and existing authorization. Continue authorized work; ask only for consequential unresolved choices or required external approval. Scale depth to material risk without silently skipping checks. Preserve dependency and safety ordering; otherwise choose the verification method appropriate to each obligation.
Treat equivalent user or repository evidence as valid input; another skill, named artifact, or complete lifecycle is not a prerequisite. Preserve source requirement and decision identifiers when available. Bind reused evidence to the relevant source version, dirty changes, configuration, and environment; invalidate only affected claims after a change.
On continuation, reconcile the task, existing authorization, current state, and unresolved evidence before resuming. For long work, return a compact continuation record or update an already authorized task artifact; read-only skills do not persist it. Distinguish artifact readiness, verified behavior, and authority to perform an external action.
Prepare authorized work before any required approval. If an instruction prevents progress, identify its exact source and explain the unresolved boundary; do not invent an approval gate from general caution.


## Tool Routing

| Need | Preferred capability | Use when | Fallback |
|---|---|---|---|
| Scope and repository state | Native file reads plus Git | Establishing outcome, non-goals, base, head, and worktree | Supplied requirements with explicit limitations |
| Changed behavior | Diff, status, and focused reads | Resolving the implementation delta and entrypoints | Compare supplied artifacts with their stated baseline |
| Definitions and consumers | Code intelligence | An affected path depends on unchanged symbols or contracts | Targeted search that stops when the causal path is proven |
| Automated verification | Repository-defined commands | Build, lint, type, test, migration, or smoke gates exist | Inspect scripts and CI; mark execution `UNPROVEN` |
| Observable behavior | Browser, client, or runtime evidence | Acceptance depends on UI, interaction, protocol, or logs | Static trace plus an exact manual check |
| Reuse and correction research | Installed manifests plus current official documentation, specifications, and package sources | A changed generic mechanism needs a reuse decision, external behavior affects correctness, or an externally dependent correction needs verification | Reputable primary engineering material; otherwise mark the decision or correction `UNVERIFIED` |
| Independent review | Native subagents in separate contexts | An unresolved distinct risk warrants independent evidence | Linked panel protocol; otherwise direct review with independence limits |

Use tools only for the current evidence question. Tool failure is a limitation, not a defect. Do not convert an unavailable command, runtime, or source into a finding without implementation evidence.

## Evidence Rules

| Evidence | Weight |
|---|---|
| Reproduced behavior, failing test, compiler output, or deterministic command | Strongest current-behavior evidence |
| Changed code plus verified caller, consumer, schema, or configuration path | Strong static evidence |
| Acceptance criterion mapped to implementation and verification | Required delivery evidence |
| Official external contract matching the used version | Strong compatibility evidence |
| Pattern, intuition, or generic practice | Lead only until tied to a concrete failure or risk |

Apply the finding fields in Output Contract. Repository evidence establishes the defect; external guidance supports corrections and cannot invent local requirements. The review unit is the business change, not the repository. Read unchanged code only to prove an affected path; do not report style preferences or unrelated repository health.

## Independent Review

The lead owns scope, evidence, and verdict. Use no panel when direct evidence suffices or the user excludes delegation. When a distinct unresolved risk warrants independent review, read [the panel protocol](references/independent-review.md) before selecting or launching reviewers; it owns lens selection, frozen context, round limits, retries, and result handling. Missing independence is a limitation unless it leaves essential evidence unproven.

## Checklist

### 1. Establish Business and Change Scope

- [ ] From the request and a focused initial inspection, state the affected actors, problem, protected outcome, changed behavior, acceptance criteria, existing user experience, explicitly authorized user-facing changes, invariants, non-goals, and release boundary. Mark unsupported interpretations `UNKNOWN`; use `BLOCKED` when the thesis cannot be established.
- [ ] Establish complexity fit from evidenced maturity, business horizon, scale, team capacity, and lifecycle cost; do not infer enterprise needs from hypothetical growth or call safety-required complexity overengineering.
- [ ] Read applicable repository instructions, inspect uncommitted work, and resolve the authoritative task, base, head, implementation delta, approved plan or target architecture, and permitted transitional compatibility. Identify only change-relevant project policies, standards, and ADRs; do not treat every document as binding.
- [ ] Discover only change-relevant baseline, current-state, target-design, policy, decision, diagram, and migration artifacts by repository convention. Record authority, owner, status, freshness, and supersession, and keep one policy and decision ledger of applicable sources and implementation evidence for compliance, explicit approved deviation, or an unresolved gap.
- [ ] Map changed, causally supporting, and explicitly excluded surfaces. Read outside the diff only to trace affected behavior; do not hunt unrelated code for findings.
- [ ] Classify change-triggered risk from trust, money, destructive action, migration, public contracts, concurrency, distributed coordination, and rollback difficulty; define acceptance evidence before implementation review.
- [ ] Record whether direct review suffices. If a panel is justified, apply the linked protocol to classify the pass, freeze scope, select distinct questions, and record coverage without sharing provisional findings.
- [ ] Keep the review read-only. Permit only host-approved caches or build artifacts; do not edit tracked files, create tasks, commit, push, deploy, or repair findings.

### 2. Trace Requirements into Implementation

- [ ] Enumerate every authoritative task requirement and acceptance criterion, plus every required approved-plan item. Map each to concrete implementation and independent behavioral evidence; mark task and plan items `COMPLETE`, `DEVIATED`, `OMITTED`, or `UNPROVEN` and acceptance `PASS`, `FAIL`, or `UNPROVEN`. Author claims, checked boxes, commits, and code presence are not completion evidence.
- [ ] Inspect changed files and only the unchanged definitions, consumers, interfaces, tests, migrations, and registration needed to prove an affected path.
- [ ] Verify each required plan item was implemented and works in its intended runtime path. Treat unexplained omissions as unmet; accept `DEVIATED` only when explicit evidence proves the alternative fully preserves the task, protected outcome, constraints, and acceptance. Distinguish justified deviation from stale or proposed documentation.
- [ ] Compare the user-observable baseline with the delivery. Existing screens, copy, styles, navigation, interaction order, focus, accessibility, and user scenarios may change only when a specific task requirement authorizes that change; otherwise treat any delta as a regression. Additive screens, copy, controls, and scenarios also require a task-grounded purpose and authorized scope; list each with its trigger, rationale, and evidence.
- [ ] Trace each critical scenario from actor trigger through entrypoint, runtime wiring, usage context, and observable outcome; include first meaningful use, material failure, recovery, and repetition where relevant.
- [ ] Confirm new components, routes, commands, handlers, jobs, events, and configuration are registered and discoverable at runtime.
- [ ] Within affected behavior, inspect applicable boundaries, collections, state transitions, duplicates, ordering, numeric behavior, empty and maximum inputs, errors, retries, idempotency, cancellation, timeouts, rollback, and cleanup.
- [ ] Within affected async paths, inspect shared state, transactions, races, lock ordering, and blocking work.

### 3. Review Safety, Contracts, and Simplicity

- [ ] Within affected paths, inspect applicable authentication, authorization, ownership, validation, injection, secrets, sensitive data, logging, and destructive-operation guards.
- [ ] For changed destructive behavior, require recovery, rollback, blast-radius, environment or authorization, and preview or dry-run evidence; justify infeasible controls.
- [ ] Verify changed API, event, schema, configuration, serialization, and storage producers and consumers, including names, payloads, registration, ordering, and compatibility. For changed semantic values and closed sets--such as states, roles, permissions, event names, error codes, configuration keys, feature identifiers, limits, timeouts, and routing keys--require one authoritative owner shared by every in-scope producer and consumer through the repository-standard mechanism (for example a typed union, enum, constant set, value object, schema, typed configuration, or generated contract). Accept a harmless one-off local literal when it creates no duplication, invalid-state, or drift risk.
- [ ] Verify migrations, backfills, defaults, indexes, deployment ordering, and mixed-version behavior when persisted or distributed state changes.
- [ ] Check ownership and cleanup of files, streams, sessions, connections, processes, subscriptions, and temporary artifacts on success and failure.
- [ ] Inspect only architecture and policy boundaries crossed or changed. Verify that responsibility, dependency direction, contracts, state, lifecycle, and failure ownership remain coherent with the approved architecture or the simplest established repository mechanism. Apply every current authoritative project policy or ADR in the change-scoped ledger, including project-defined logging (logger, structured fields, levels, correlation, and redaction) and error handling (taxonomy, types or codes, boundary mapping, propagation, retry, and recovery) when affected; accept deviation only with explicit approval and evidence that scoped acceptance remains intact. Do not turn adjacent architecture or policy compliance into an audit.
- [ ] Trace the owning correction across in-scope entrypoints, producers, consumers, registration, state transitions, and material failure/recovery paths. Reject symptom masking, caller special cases, side channels, and accidental ordering/timing/data dependencies. Tactical containment requires explicit intent or immediate safety, an owner, removal condition, and durable follow-up; stop at the causal business scope.
- [ ] When code is replaced, verify old implementations, signatures, aliases, re-exports, shims, adapters, flags, dual paths, and files are removed and callers migrated. Retain compatibility only for a supported contract with an owner and bounded removal condition.
- [ ] Inspect superseded constraints, configuration, schemas, states, permissions, metrics, and rollout scaffolding in the changed capability. Require proven supersession before removal; otherwise record retention evidence or a temporary owner and removal condition.
- [ ] For added or materially expanded generic mechanisms, compare credible simpler alternatives against the exact contract; stop once an existing mechanism is sufficient. Investigate a new package only when a material gap remains. Record `REUSE_EXISTING`, `ADOPT_PACKAGE`, `KEEP_CUSTOM`, `DELETE`, or `MERGE` with local evidence and, for external semantics, official sources; assess material security, maintenance, license, bundle/runtime, API-stability, migration, and wrapper costs. Prefer the lowest-lifecycle-cost complete fit; do not add a dependency for compact domain logic or when its residual wrapper is no smaller or safer, and inspect only mechanisms changed by or necessary to the delivery.
- [ ] **Simplicity:** Require the minimum sufficient diff and simplest correct, efficient algorithm. Reject needless duplication, files, layers, abstractions, dependencies, configuration, branches, compatibility paths, or custom machinery when existing mechanisms suffice; never trade away safeguards or maintainability.

### 4. Verify Tests, Documentation, and Operations

- [ ] Build one change-scoped test decision ledger from requirements, approved plan, changed behavior, and affected tests. For every material risk and affected test, record existing proof, independent oracle, gate and result, level rationale, and `KEEP`, `ADD`, `UPDATE`, `MERGE`, `DELETE`, or justified `NO_TEST`; verify planned actions were actually completed and explain evidence-backed deviations.
- [ ] Rank only changed business risks by likelihood, impact, blast radius, reversibility, and regression history. Prohibit tests that merely re-prove language, framework, package, database-vendor, pass-through, or other trivial behavior; crossing a real dependency is valid only for a repository-owned rule, configuration, wiring, contract, query, schema, permission, transaction, recovery path, or journey. `NO_TEST` must name existing proof, another control, or accepted residual risk.
- [ ] Choose the smallest reliable unit, integration, contract, or E2E boundary that proves each material risk. Require end-to-end evidence when the user journey cannot be established at a narrower boundary. Recommend the fewest tests with distinct failure signals, never test count, raw coverage, or one-test-per-acceptance-row targets.
- [ ] Use stable project-native semantic locators (roles, accessible names, labels) or explicit IDs/test hooks according to the observable contract and locale strategy. Avoid styling, position, timing, and incidental structure. Treat exact-copy assertions separately when copy is a requirement; do not require product edits solely to add hooks when a robust semantic locator exists.
- [ ] Validate each ledger decision against defect sensitivity, assertions, success and failure paths, authorization, boundaries, data integrity, over-mocking, snapshots, flakes, shared state, time, randomness, order dependence, and CI placement. Assign `DELETE` to obsolete, duplicate, trivial, implementation-detail, or immaterial proof and `MERGE` when its unique value survives consolidation; preserve replacement traceability and never retain superseded tests, fixtures, helpers, snapshots, or gates by inertia.
- [ ] Check required versus diagnostic gate placement, visible skips, retries and quarantine, and any review or retirement trigger for temporary characterization, migration, compatibility, incident, or workaround evidence. Quarantine is an execution state, not a portfolio action, and must not become a silent pass.
- [ ] Discover commands from repository docs, tool configuration, and manifests before justified fallback. Run narrow checks first, then required build, lint, type, test, migration, and smoke gates with CI-safe options.
- [ ] Record command source, exit status, actual executed scope, and limitations. Confirm required scenarios ran; zero selected tests or skipped suites do not prove acceptance. Attribute failures to change, baseline, or environment.
- [ ] Verify user-visible acceptance from the other side when static proof is insufficient, including material failure and recovery; for applicable UI, check keyboard, focus, accessible names, motion, responsive states, copy, and localization.
- [ ] Review only documentation and comments changed by or required for the scoped business change; classify each as `KEEP`, `ADD`, `UPDATE`, `DELETE`, or `MERGE`. Delete or merge only when canonical coverage preserves every needed audience task and contract.
- [ ] Verify documentation SSOT and hierarchy: the delivery updates the narrowest canonical owner, links rather than copies rules, reuses suitable documents, and removes superseded references. Report violations without editing or auditing unrelated documentation.
- [ ] Reject documentation filler, repeated summaries, speculation, and code restatement. Preserve audience-needed intent, contracts, actions, constraints, and minimal verified examples.
- [ ] Keep volatile versions, paths, defaults, counts, commands, generated output, and current-state data in authoritative code, configuration, or generated sources where practical. Otherwise require the source, scope, and owner or generation/update trigger.
- [ ] Verify affected API and configuration references, examples, migrations, runbooks, operator steps, and comments against implementation and requirements; comments explain enduring intent or constraints rather than syntax.
- [ ] Check logs, metrics, traces, health signals, feature controls, deployment order, rollback, and recovery where the change creates operational risk.

### 5. Challenge and Synthesize

- [ ] When selected, run the independent panel under its linked protocol; otherwise record `None` and use direct evidence. Treat suggestions as candidates requiring verification.
- [ ] Verify each candidate against code, commands, behavior, declared intent, or authoritative documentation; trace symptom to causal path and violated contract, and reject subjective or symptom-only claims.
- [ ] Accept a finding only when the diff introduced, exposed, or worsened it; it violates scoped acceptance; or the change caused a required-gate failure. Treat other issues only as limitations when they block acceptance; never recommend their repair.
- [ ] Apply a materiality and acceptable-alternative gate to every in-scope candidate. Ask whether it proves a concrete user, business, safety, operational, delivery, or lifecycle impact at the evidenced project scale. Reject nitpicks, personal taste, theoretical purity, generic best practice, hypothetical scale, and an implementation that is merely different when the current tradeoff is reasonable. When several approaches are valid, require the outcome or constraint rather than one preferred design.
- [ ] Research corrections after local evidence establishes a defect; investigate reuse alternatives when the changed generic mechanism has a material capability gap or lifecycle cost. Prefer repository mechanisms. Verify externally dependent choices against official version-matched documentation or primary engineering sources, citing the supported claim and tradeoff. Local evidence suffices for local business defects. Mark unsupported external claims `UNVERIFIED`; review does not authorize repair.
- [ ] Deduplicate by root cause, preserve the strongest evidence and widest demonstrated impact, and recommend one smallest sufficient correction.
- [ ] Resolve contradictions through direct evidence; carry material unresolved gaps into the verdict or residual risk.
- [ ] Classify findings `P0` catastrophic, `P1` release-blocking, `P2` important non-blocking, or `P3` minor actionable.
- [ ] Use `FAIL` for unresolved `P0/P1`, a required task or plan item that is `OMITTED` or demonstrably incorrect, unmet acceptance, an unauthorized change to existing user experience, a change-caused required-gate failure, or demonstrated unsafe high-risk behavior. Use `CONCERNS` only for explicit non-blocking risk. Use `PASS` only when every required task and plan item is `COMPLETE` or evidence-backed `DEVIATED`, every acceptance criterion passes, and all required evidence is complete.
- [ ] Use `BLOCKED` when a required task or plan item remains `UNPROVEN`, or a required lens, specialist, safety environment, authoritative contract, or acceptance prerequisite has no credible replacement; report the coverage gap, not a product defect.

- [ ] Bind the final verdict to the actual reviewed bytes, relevant dirty/configuration state, and execution environment; after corrections, reassess affected findings and dependent acceptance without automatically repeating unrelated review.

## Self-Check

- [ ] **Reconcile before returning.** Check item-level evidence, requirement coverage, contradictions, scope, verdict, and applicable cleanup. Correct the report or authorized artifacts. Reuse valid evidence; do not automatically rescan the repository or rerun successful commands. Repeat checks only for relevant changes, failures, or unresolved evidence. Disclose remaining gaps.

## Output Contract

Report in the user's language, in this order; retain all five fields and state each fact once. Small results may use one line per field; omit empty tables and do not copy linked artifacts:

1. **Result:** Skill-specific verdict and supported outcome.
2. **Scope:** Reviewed/changed scope, exclusions, baseline, and material assumptions.
3. **Evidence:** Skill-specific fields below; distinguish facts, inferences, and unverified claims. Link artifacts; use tables when useful.
4. **Verification:** Checks/results, unavailable evidence, and applicable cleanup/external state.
5. **Completion:** `Checklist: X/Y complete`; `Incomplete: None` or each `UNPROVEN` item's reason, outcome impact, and exact next action; residual risks and required decisions.

**Skill-specific evidence:** Task/plan requirement → implementation → behavioral evidence → status; scope/base/head and initial/follow-up review state. Include authorized UX changes and additive surfaces, applicable policy/ADR compliance, reuse and subtraction decisions, selected independent lenses and coverage, and test/documentation actions. Each finding needs priority, location, affected business behavior, change-causal evidence, violated contract, material impact, and smallest sufficient correction; allow equivalent solutions. Use `None` when no candidate survives the evidence gates.
