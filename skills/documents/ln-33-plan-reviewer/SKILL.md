---
name: ln-33-plan-reviewer
description: "Reviews a concrete implementation plan for missing decisions, feasibility and risk before execution; read-only."
---

# Plan Reviewer

**Goal:** Perform a read-only, evidence-first second pass over an implementation plan. Verify the plan; do not execute it. A strong result is decision-complete, grounded in the actual repository, explicit about uncertainty, no more complex than the problem requires, and expressed in the fewest words and execution steps that preserve safety.

**Execution contract:** The ordered checkboxes are the Definition of Done. Track every item internally as `PENDING`, `PROVEN` with concrete evidence, `CLEARED` with evidence that its condition is absent, or `UNPROVEN` with a gap; reading, delegation, or tool failure is not proof. Reconcile items after each section. Before returning, resolve all `PENDING` and count only `PROVEN` and `CLEARED`; apply the skill's verdict and approval rules to every gap.
Preserve user intent, scope, and existing authorization. Continue authorized work; ask only for consequential unresolved choices or required external approval. Scale depth to material risk without silently skipping checks. Preserve dependency and safety ordering; otherwise choose the verification method appropriate to each obligation.
Treat equivalent user or repository evidence as valid input; another skill, named artifact, or complete lifecycle is not a prerequisite. Preserve source requirement and decision identifiers when available. Bind reused evidence to the relevant source version, dirty changes, configuration, and environment; invalidate only affected claims after a change.
On continuation, reconcile the task, existing authorization, current state, and unresolved evidence before resuming. For long work, return a compact continuation record or update an already authorized task artifact; read-only skills do not persist it. Distinguish artifact readiness, verified behavior, and authority to perform an external action.
Prepare authorized work before any required approval. If an instruction prevents progress, identify its exact source and explain the unresolved boundary; do not invent an approval gate from general caution.


## Tool Routing

| Need | Preferred tool | Use it when | Fallback |
|---|---|---|---|
| Repository instructions and current state | Native file read plus Git | Always read the active host's applicable repository instructions; use `git status`, `diff`, and history when branch or change context matters | Equivalent host file and shell tools |
| Paths, text, config, docs, and focused code reads | Native file listing, search, outline, and range reads | The question is textual or structural and does not require symbol identity | Narrow the path and pattern before expanding content |
| Symbols, references, callers, implementations, cycles, and blast radius | Language server or host-native code intelligence | A plan changes existing code relationships, public APIs, module boundaries, or architecture | Targeted search plus direct inspection of definitions and consumers |
| Planned edit risk | Code intelligence plus caller and consumer search | The plan names an edit region, route, event, response contract, or existing change surface | Inspect named symbols and adjacent integration points manually |
| Build, test, migration, and script feasibility | Repository-defined commands through the shell | The plan depends on a command, baseline, generated artifact, or existing test surface being available | Inspect scripts and CI configuration; mark execution unverified |
| Correction and external-claim research | Official vendor documentation, specifications, or standards through documentation search or the web | External behavior or a correction depends on changing platform semantics | Reputable primary engineering material; otherwise mark the claim or correction `UNVERIFIED` |
| Independent challenge | Native subagents in separate contexts | A plan benefits from execution, fresh-context, or adversarial perspective | Run the selected perspectives once as one bounded self-review batch and report reduced independence |

Use the preferred tool only when it answers the current evidence question. Tool failure is not a domain finding: report reduced confidence and block only when missing evidence prevents a safe decision. Do not use semantic tooling for prose or configuration questions, and do not use web research to rediscover stable local facts.

## Evidence Rules

| Evidence | Authority |
|---|---|
| Repository files, manifests, schemas, generated contracts, and executable behavior | Source of truth for the current project state |
| Official vendor documentation, specifications, RFCs, and security standards | Source of truth for external contracts and current supported behavior |
| Release notes and migration guides matching the project's actual version range | Source of truth for compatibility and upgrade claims |
| Reputable primary engineering material | Supporting evidence when official sources do not address a design tradeoff |
| Community discussion or training knowledge | Leads only; never sufficient for a blocking factual claim |

When sources disagree, prefer the repository for what is installed and implemented, and official documentation for what an external system promises. Repository evidence proves a plan defect; external practice sources justify the correction mechanism and cannot invent a local requirement. State disagreements instead of silently choosing the convenient answer.

## Checklist

### 1. Establish the Review Contract

- [ ] Resolve the exact plan, user request, linked requirements, and repository scope. If no concrete plan exists, stop with `BLOCKED` rather than inventing one to review.
- [ ] Read all applicable repository instruction files before interpreting code, documentation, or expected workflow. Identify only change-relevant project policies, standards, and ADRs; distinguish current accepted authority from draft, superseded, stale, or merely descriptive material instead of treating every document as binding.
- [ ] Inspect Git state when it can affect the review: current branch, uncommitted changes, comparison base, and relevant recent history.
- [ ] Separate the literal request and proposed solution from the underlying intent; state the actor, protected outcome, observable definition of done, non-goals, constraints, and assumptions, and label unsupported intent inferences.
- [ ] Calibrate acceptable complexity to evidenced project or product maturity, decision horizon, current scale, team and operational capacity, and business stakes. Treat future growth as a requirement only when a concrete horizon, consumer, load, or constraint supports it.
- [ ] Separate defects in the plan from pre-existing adjacent problems. Treat an existing problem as a plan finding only when the plan introduces or worsens it, depends on a false assumption about it, must resolve it to satisfy the goal, or creates immediate delivery risk; otherwise record it as an out-of-scope observation and do not expand the plan.
- [ ] Distinguish facts discoverable from the repository from choices that require user intent; explore first, and when plausible interpretations would produce materially different plans, ask one concise question that resolves the decision rather than a survey.
- [ ] Classify the review depth. Treat authentication, authorization, money, destructive operations, data migration, public APIs, concurrency, distributed workflows, and irreversible rollout as high-risk.
- [ ] Keep the run read-only. Do not mutate the source plan, implementation, task tracker, branch, or external system; a corrected plan may appear only in the review response. Allow only host-permitted rebuildable diagnostic caches or build artifacts and disclose them when created.

### 2. Ground the Plan in the Repository

- [ ] Build a narrow map of the affected modules, entrypoints, configuration, schemas, migrations, tests, documentation, and deployment surfaces.
- [ ] Discover shared architecture and governance artifacts by repository convention and common roles: system-design baseline, current-state map, target design, accepted decisions, engineering policies, diagrams, and migration plan. Treat them as optional evidence, never as required workflow dependencies.
- [ ] Check artifact status, authority, owner, source, as-of date, supersession, and review triggers before applying a constraint. Keep one change-scoped policy and decision ledger of applicable sources and the plan evidence for compliance, explicit approved deviation, or an unresolved gap. Missing artifacts do not block review by themselves; a material unresolved driver does.
- [ ] Verify every existing path, symbol, component, command, environment key, interface, and dependency named by the plan. Mark genuinely new artifacts as new.
- [ ] Read enough implementation context to understand ownership and invariants, not just the files explicitly named by the plan.
- [ ] Inspect Git history or blame only when it can reveal a still-relevant constraint or convention; do not treat historical code as proof that the current design is correct.
- [ ] Check the existing test and CI surface so proposed verification commands, fixtures, environments, and acceptance evidence are feasible.
- [ ] Keep an evidence ledger for material claims: claim, source, confidence, and the plan decision it supports or contradicts.
- [ ] Check known concurrent work when it can collide with affected contracts, schemas, files, or outcomes; do not inventory every branch or plan without an overlap signal.
- [ ] Stop expanding the scan when additional files cannot change a plan decision, finding, or confidence level.

### 3. Research Corrections and Unknown External Claims

- [ ] Research a correction only after repository evidence establishes a material candidate gap; prefer an existing repository mechanism and do not browse to invent findings.
- [ ] Extract plan claims that are external or unstable: versions, API signatures, deprecations, standards, security requirements, library capabilities, performance characteristics, and platform limits.
- [ ] Resolve installed versions and enabled features from project manifests, lockfiles, configuration, and generated metadata before searching generic documentation.
- [ ] Before recommending a correction that depends on an external API, library, security control, protocol, platform, standard, or version, verify the supported solution, constraints, deprecations, and security guidance in official documentation matched to the installed or proposed version.
- [ ] For unresolved design tradeoffs, compare primary engineering evidence with local requirements and operating constraints; document where the evidence does not select a unique solution.
- [ ] Open and inspect any specific document, proposal, issue, or URL that the plan relies on instead of trusting a quotation or paraphrase.
- [ ] Add solution research to the material-claim ledger: source/date, supported mechanism, corrections considered, decision, confidence, and plan impact; do not create a separate research register.
- [ ] Apply the research-to-action gate: if a source does not reveal a specific defect, risk, missing decision, or better-supported alternative, keep it informational and do not inflate the review.
- [ ] If authoritative research is unavailable, label the affected claim `UNVERIFIED`; use `BLOCKED` when implementation safety or a consequential design choice depends on it. Review approval never authorizes execution; identify unstable external facts and their revalidation trigger for the implementer; reuse evidence while its version and assumptions remain valid.

### 4. Review from Every Applicable Perspective

- [ ] **Intent and traceability:** Every proposed change and source of complexity maps to the intended outcome, an acceptance criterion, a safety need, or an evidenced constraint; combine work serving the same outcome, and remove speculative or merely ceremonial steps.
- [ ] **Repository fit:** The plan respects actual project structure, conventions, supported stack, existing capabilities, maturity, current scale, team and operational capacity, and current work without overwriting unrelated changes. For each applicable current project policy or ADR in the ledger, trace the affected plan surface to compliance or an explicitly approved and justified deviation; include project-defined logging, error taxonomy and boundary mapping, configuration, observability, security, persistence, testing, and release rules only when the change reaches them.
- [ ] **Architecture, ownership, and traceability:** Layers, modules, orchestration, side effects, dependency direction, and resource ownership remain explicit, coherent, and proportionate. The plan respects confirmed constraints, accepted decisions, target boundaries, and the active migration phase; expose stale or contradictory artifacts instead of silently selecting the convenient one.
- [ ] **Root cause and completeness:** Trace the owning correction across in-scope entrypoints, producers, consumers, registration, state transitions, and material failure/recovery paths. Reject symptom masking, caller special cases, side channels, and accidental ordering/timing/data dependencies. Tactical containment requires explicit intent or immediate safety, an owner, removal condition, and durable follow-up; stop at the causal business scope.
- [ ] **Interfaces and data:** Public APIs, events, schemas, configuration, persistence, serialization, compatibility, and migration paths are named wherever they change. For changed semantic values and closed sets--such as states, roles, permissions, event names, error codes, configuration keys, feature identifiers, limits, timeouts, and routing keys--plan one authoritative owner shared by every in-scope producer and consumer through the repository-standard mechanism (for example a typed union, enum, constant set, value object, schema, typed configuration, or generated contract). Do not demand extraction of a harmless one-off local literal with no duplication, invalid-state, or drift risk.
- [ ] **Scenario completeness:** For each critical flow, trace actor trigger -> entrypoint -> runtime discovery or wiring -> usage context -> observable outcome; include first meaningful use, failure, recovery, and repetition when they can change the intended experience.
- [ ] **Correctness and failure modes:** Cover boundaries, invalid state, partial failure, retries, idempotency, concurrency, cancellation, timeouts, rollback, and cleanup where applicable.
- [ ] **Security and privacy:** Cover trust boundaries, authentication, authorization, validation, secrets, sensitive data, logging, destructive actions, and abuse paths in proportion to risk.
- [ ] **Dependencies and sequencing:** Use the fewest dependency-ordered steps that can reach acceptance safely; parallel steps have no same-wave dependency or shared mutable output, and migrations, producers, consumers, deployments, and compatibility transitions remain ordered correctly.
- [ ] **Capacity and degradation:** Bound user- or data-controlled work and state load from evidenced demand; state rate assumptions and failure behavior without introducing scaling machinery for hypothetical traffic.
- [ ] **Testing and acceptance:** For every material changed risk and affected test, the plan names the test basis, existing proof, independent oracle, level and gate rationale, and one portfolio action: `KEEP`, `ADD`, `UPDATE`, `MERGE`, `DELETE`, or justified `NO_TEST`. Choose the smallest reliable boundary that proves each material risk; use E2E when the journey requires it; require the fewest tests with unique defect signals, completion evidence rather than count or raw coverage, and a review or retirement trigger for temporary proof without redesigning unrelated test health.
- [ ] **Delivery and operations:** Include documentation, configuration rollout, observability, deployment, rollback, and operator actions only where the change requires them.
- [ ] **Simplicity and alternatives:** Evaluate `NO_CHANGE`, `DELETE_OR_CONFIGURE`, `REUSE_LOCAL`, `USE_PLATFORM_OR_STDLIB`, `REUSE_INSTALLED`, `ADOPT_DEPENDENCY`, then `MINIMAL_CUSTOM`; justify the selected rung and rejected applicable simpler options. New code, dependencies, layers, services, configuration, extensibility, or operational machinery need a concrete capability or lifecycle-cost reason. Consolidation must preserve ownership, verification, correctness, safety, compatibility, testability, and reversibility.
- [ ] **Subtractive completeness:** For changed logic, constraints, configuration, schemas, routes, states, or operations, identify obsolete code, branches, flags, keys, defaults, shims, data paths, documentation, tests, permissions, metrics, and rollout scaffolding. Plan removal only when evidence proves it superseded and in scope; otherwise record retention evidence or a temporary path's owner and removal condition.

### 5. Challenge Material Uncertainty When Needed

- [ ] Use an independent challenge only when an unresolved material question warrants it and the user permits it; clear the conditional challenge items otherwise. Select the smallest distinct set of execution-simulation, fresh-context, or adversarial perspectives that can change the verdict, without quotas. Keep the challenge to one bounded round; resolve resulting evidence gaps directly.
- [ ] Give every reviewer the same frozen packet—plan, real goal, relevant repository paths, constraints, assumptions, and evidence questions—without prior conversation history, the primary review's conclusions, or sibling outputs. If the host cannot provide fresh isolated contexts, use distinct self-review passes and disclose reduced independence.
- [ ] Launch the selected perspectives once in parallel or one blind wave, wait for all, and treat every suggestion as a candidate finding requiring repository or authoritative evidence. Resolve conflicts and verify candidates directly; never launch a verifier or another reviewer round.
- [ ] Classify pre-mortem concerns as evidence-backed risk, unsupported fear, or unstated assumption; dismiss unsupported fear, and give each accepted risk or assumption an invalidation impact and concrete validation or mitigation step.
- [ ] Treat reviewer unavailability, tool failure, rate limits, or questions as coverage limitations, not evidence that the plan is defective. Retry or replace one technically failed selected reviewer only when a concrete cause changes, using the same evidence question; this completes the original round and must not broaden it.

### 6. Synthesize a Decision-Complete Result

- [ ] Deduplicate findings from repository inspection, research, and independent review; keep the strongest evidence and preserve meaningful disagreements.
- [ ] Classify findings as `BLOCKER`, `MAJOR`, or `MINOR`: blockers prevent safe handoff, majors predict substantial rework or regression, and minors improve clarity without changing feasibility.
- [ ] Apply a materiality and acceptable-alternative gate to every candidate. Require a violated requirement or contract, or a concrete user, business, safety, operational, delivery, or lifecycle impact at evidenced scale. Reject unsupported or pre-existing unrelated problems, nitpicks, personal taste, theoretical purity, generic practice, hypothetical scale, and a merely different implementation when the current tradeoff is reasonable. For every accepted finding, explain why the compromise is unacceptable and require the smallest complete outcome while allowing equivalent solutions.
- [ ] Cite verified sources for externally dependent corrections; cite local evidence for repository-owned defects. Mark only unsupported claims `UNVERIFIED`; do not obscure an independently proven defect because an optional practice source is unavailable.
- [ ] Confirm that consequential interfaces, ownership, data flow, failure behavior, compatibility, verification, and rollout are decided or bounded by explicit constraints; leave equivalent implementation details to the implementer.
- [ ] For every material assumption, record confidence, what breaks if it is false, and who or what step validates it before dependent work begins.
- [ ] Map findings to verdicts: use `BLOCKED` when a required user choice, access, or authoritative fact is unavailable; use `REVISE` for any correctable `BLOCKER` or `MAJOR`; use `READY WITH CONCERNS` only when the plan is safe and executable with no uncovered requirement or consequential decision, but bounded non-blocking `MINOR` amendments or explicitly accepted residual risks remain; use `READY` only when no corrective finding or blocking evidence gap remains.
- [ ] For `REVISE`, provide exact local amendments when they make the plan coherent; provide a complete replacement only when changes span its structure or dependencies. Preserve intent, accepted corrections, and required implementation/verification outcomes.
- [ ] For `READY WITH CONCERNS`, provide only the exact local plan amendments and accepted non-blocking risks; do not restate unchanged sections of the plan.
- [ ] For `BLOCKED`, ask only the smallest questions that materially unlock a different plan, and state what was already verified.

- [ ] Verify the plan covers complete observable increments, dependency ordering, integration between increments, and required verification; expose consequential decisions deferred to the implementer.

## Self-Check

- [ ] **Reconcile before returning.** Check item-level evidence, requirement coverage, contradictions, scope, verdict, and applicable cleanup. Correct the report or authorized artifacts. Reuse valid evidence; do not automatically rescan the repository or rerun successful commands. Repeat checks only for relevant changes, failures, or unresolved evidence. Disclose remaining gaps.

## Output Contract

Report in the user's language, in this order; retain all five fields and state each fact once. Small results may use one line per field; omit empty tables and do not copy linked artifacts:

1. **Result:** Skill-specific verdict and supported outcome.
2. **Scope:** Reviewed/changed scope, exclusions, baseline, and material assumptions.
3. **Evidence:** Skill-specific fields below; distinguish facts, inferences, and unverified claims. Link artifacts; use tables when useful.
4. **Verification:** Checks/results, unavailable evidence, and applicable cleanup/external state.
5. **Completion:** `Checklist: X/Y complete`; `Incomplete: None` or each `UNPROVEN` item's reason, outcome impact, and exact next action; residual risks and required decisions.

**Skill-specific evidence:** Plan decision, required corrections, acceptance and sequencing gaps; task/plan requirement → evidence → status. Include applicable policy/ADR compliance and approved deviations, root-cause completeness, retained or removed mechanisms, test and documentation actions, independent-challenge coverage, and authoritative references only for externally dependent corrections. Each finding needs priority, location, violated contract, material impact, and the smallest sufficient correction; allow equivalent valid solutions. Preserve the corrected plan or decision-changing amendments in the response only.
