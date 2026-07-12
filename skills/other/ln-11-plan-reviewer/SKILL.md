---
name: ln-11-plan-reviewer
description: "Reviews implementation plans against repository evidence and current authoritative guidance. Use before execution to expose gaps and risks; not for completed delivery review."
---

# Plan Reviewer

Perform a read-only, evidence-first second pass over an implementation plan. Verify the plan; do not execute it. A strong result is decision-complete, grounded in the actual repository, explicit about uncertainty, and no more complex than the problem requires.

## Tool Routing

| Need | Preferred tool | Use it when | Fallback |
|---|---|---|---|
| Repository instructions and current state | Native file read plus Git | Always read applicable `AGENTS.md`/`CLAUDE.md`; use `git status`, `diff`, and history when branch or change context matters | Equivalent host file and shell tools |
| Paths, text, config, docs, and focused code reads | Native file listing, search, outline, and range reads | The question is textual or structural and does not require symbol identity | Narrow the path and pattern before expanding content |
| Symbols, references, callers, implementations, cycles, and blast radius | Language server or host-native code intelligence | A plan changes existing code relationships, public APIs, module boundaries, or architecture | Targeted search plus direct inspection of definitions and consumers |
| Planned edit risk | Code intelligence plus caller and consumer search | The plan names an edit region, route, event, response contract, or existing change surface | Inspect named symbols and adjacent integration points manually |
| Build, test, migration, and script feasibility | Repository-defined commands through the shell | The plan depends on a command, baseline, generated artifact, or existing test surface being available | Inspect scripts and CI configuration; mark execution unverified |
| External APIs, versions, standards, and current practice | Official vendor documentation or standards through documentation search or the web | An external or time-sensitive fact can change the plan | Built-in knowledge only when tools fail, marked `UNVERIFIED` |
| Independent challenge | Native subagents in separate contexts | A non-trivial plan benefits from execution, fresh-context, and adversarial perspectives | Run the same perspectives as distinct self-review passes and report reduced independence |

Use the preferred tool only when it answers the current evidence question. Tool failure is not a domain finding: report reduced confidence and block only when missing evidence prevents a safe decision. Do not use semantic tooling for prose or configuration questions, and do not use web research to rediscover stable local facts.

## Evidence Rules

| Evidence | Authority |
|---|---|
| Repository files, manifests, schemas, generated contracts, and executable behavior | Source of truth for the current project state |
| Official vendor documentation, specifications, RFCs, and security standards | Source of truth for external contracts and current supported behavior |
| Release notes and migration guides matching the project's actual version range | Source of truth for compatibility and upgrade claims |
| Reputable primary engineering material | Supporting evidence when official sources do not address a design tradeoff |
| Community discussion or training knowledge | Leads only; never sufficient for a blocking factual claim |

When sources disagree, prefer the repository for what is installed and implemented, and official documentation for what an external system promises. State the disagreement instead of silently choosing the convenient answer.

## Checklist

### 1. Establish the Review Contract

- [ ] Resolve the exact plan, user request, linked requirements, and repository scope. If no concrete plan exists, stop with `BLOCKED` rather than inventing one to review.
- [ ] Read all applicable repository instruction files before interpreting code, documentation, or expected workflow.
- [ ] Inspect Git state when it can affect the review: current branch, uncommitted changes, comparison base, and relevant recent history.
- [ ] State the real goal, observable definition of done, explicit non-goals, constraints, and assumptions implied by the request or plan.
- [ ] Distinguish facts discoverable from the repository from choices that require user intent; explore first and ask only about consequential choices that remain unresolved.
- [ ] Classify the review depth. Treat authentication, authorization, money, destructive operations, data migration, public APIs, concurrency, distributed workflows, and irreversible rollout as high-risk.
- [ ] Keep the run read-only. Do not mutate the source plan, implementation, task tracker, branch, or external system; a corrected plan may appear only in the review response. Allow only host-permitted rebuildable diagnostic caches or build artifacts and disclose them when created.

### 2. Ground the Plan in the Repository

- [ ] Build a narrow map of the affected modules, entrypoints, configuration, schemas, migrations, tests, documentation, and deployment surfaces.
- [ ] Verify every existing path, symbol, component, command, environment key, interface, and dependency named by the plan. Mark genuinely new artifacts as new.
- [ ] Read enough implementation context to understand ownership and invariants, not just the files explicitly named by the plan.
- [ ] Use semantic graph queries when a conclusion depends on symbol identity, callers, implementations, module coupling, API consumers, or blast radius.
- [ ] Inspect Git history or blame only when it can reveal a still-relevant constraint or convention; do not treat historical code as proof that the current design is correct.
- [ ] Check the existing test and CI surface so proposed verification commands, fixtures, environments, and acceptance evidence are feasible.
- [ ] Keep an evidence ledger for material claims: claim, source, confidence, and the plan decision it supports or contradicts.
- [ ] Check active branches, plans, migrations, or sibling work for structural overlap: shared contracts, files, schemas, or the same trigger with a conflicting outcome; keyword similarity alone is only a lead.
- [ ] Stop expanding the scan when additional files cannot change a plan decision, finding, or confidence level.

### 3. Research Only the Unknown External Surface

- [ ] Extract plan claims that are external or unstable: versions, API signatures, deprecations, standards, security requirements, library capabilities, performance characteristics, and platform limits.
- [ ] Resolve installed versions and enabled features from project manifests, lockfiles, configuration, and generated metadata before searching generic documentation.
- [ ] Search official documentation or standards for each consequential external claim, matching the documentation to the installed or proposed version rather than merely the latest page.
- [ ] Use web search for recent ecosystem practice, comparative alternatives, or gaps not covered by primary sources; prefer original sources over summaries.
- [ ] Open and inspect any specific document, proposal, issue, or URL that the plan relies on instead of trusting a quotation or paraphrase.
- [ ] Record research as compact evidence: topic, source and date, verified claim, confidence, impact on the plan, and required action.
- [ ] Apply the research-to-action gate: if a source does not reveal a specific defect, risk, missing decision, or better-supported alternative, keep it informational and do not inflate the review.
- [ ] If authoritative research is unavailable, label the affected claim `UNVERIFIED`; use `BLOCKED` only when implementation safety or a consequential design choice depends on it.

### 4. Review from Every Applicable Perspective

- [ ] **Intent and traceability:** Every proposed change maps to the goal or an acceptance criterion; no requirement is uncovered and no step is speculative scope.
- [ ] **Repository fit:** The plan respects actual project structure, conventions, supported stack, existing capabilities, and current work without overwriting unrelated changes.
- [ ] **Architecture and ownership:** Layers, modules, orchestration, side effects, dependency direction, and resource ownership remain explicit and coherent.
- [ ] **Interfaces and data:** Public APIs, events, schemas, configuration, persistence, serialization, compatibility, and migration paths are named wherever they change.
- [ ] **Scenario completeness:** For each critical flow, trace actor trigger -> entrypoint -> runtime discovery or wiring -> usage context -> observable outcome.
- [ ] **Correctness and failure modes:** Cover boundaries, invalid state, partial failure, retries, idempotency, concurrency, cancellation, timeouts, rollback, and cleanup where applicable.
- [ ] **Security and privacy:** Cover trust boundaries, authentication, authorization, validation, secrets, sensitive data, logging, destructive actions, and abuse paths in proportion to risk.
- [ ] **Dependencies and sequencing:** Model prerequisites as a DAG; parallel steps have no same-wave dependency or shared mutable output, and migrations, producers, consumers, deployments, and compatibility transitions are ordered safely.
- [ ] **Capacity and degradation:** Bound user- or data-controlled work, state load and rate assumptions, and define behavior when a critical dependency, provider, queue, cache, or worker is unavailable.
- [ ] **Testing and acceptance:** Each important behavior has an observable verification method; tests cover critical product logic, errors, integration seams, and likely regressions.
- [ ] **Delivery and operations:** Include documentation, configuration rollout, observability, deployment, rollback, and operator actions only where the change requires them.
- [ ] **Simplicity and alternatives:** Challenge custom mechanisms, excess abstraction, duplicated platform or dependency features, premature extensibility, and changes with poor value-to-risk ratio.
- [ ] Mark a perspective `N/A` only when its absence is evident from the plan and repository; never silently skip a high-risk perspective.

### 5. Run an Independent Challenge When It Adds Signal

- [ ] For a non-trivial plan, launch three blind perspectives in separate contexts: an execution simulator for sequencing and feasibility, a fresh implementer for implicit knowledge and ambiguity, and an adversarial reviewer for failure, corruption, and rollback risk.
- [ ] For a small local plan, use only perspectives that can change a decision and record why the others add no signal; never skip independent challenge for high-risk, architectural, cross-service, unfamiliar, or materially ambiguous work.
- [ ] Give every reviewer the same frozen packet—plan, real goal, relevant repository paths, constraints, assumptions, and evidence questions—without the primary review's conclusions or sibling outputs.
- [ ] Run independent perspectives in parallel or blind waves, wait for all selected results, and treat every suggestion as a candidate finding that requires repository or authoritative evidence.
- [ ] Classify pre-mortem concerns as evidence-backed risk, unsupported fear, or unstated assumption; dismiss unsupported fear, and give each accepted risk or assumption an invalidation impact and concrete validation or mitigation step.
- [ ] Treat reviewer unavailability, tool failure, rate limits, or questions as coverage limitations, not evidence that the plan is defective.

### 6. Synthesize a Decision-Complete Result

- [ ] Deduplicate findings from repository inspection, research, and independent review; keep the strongest evidence and preserve meaningful disagreements.
- [ ] Classify findings as `BLOCKER`, `MAJOR`, or `MINOR`: blockers prevent safe handoff, majors predict substantial rework or regression, and minors improve clarity without changing feasibility.
- [ ] Reject unsupported findings, stylistic preferences presented as requirements, and generic best practices with no demonstrated connection to this plan.
- [ ] Confirm that every consequential implementation choice is fixed: interfaces, ownership, data flow, failure behavior, compatibility, verification, and rollout where applicable.
- [ ] For every material assumption, record confidence, what breaks if it is false, and who or what step validates it before dependent work begins.
- [ ] Map findings to verdicts: use `BLOCKED` when a required user choice, access, or authoritative fact is unavailable; use `REVISE` for any correctable `BLOCKER` or `MAJOR`, and for an unresolved `MINOR` unless it is explicitly accepted as residual risk; use `READY` only when no corrective finding or blocking evidence gap remains.
- [ ] For `REVISE`, provide a complete replacement plan that preserves the user's intent and incorporates accepted corrections; do not leave the implementer to merge prose fragments.
- [ ] For `BLOCKED`, ask only the smallest questions that materially unlock a different plan, and state what was already verified.
- [ ] Respect any host-required wrapper for plans, but keep the output content and verdict semantics below unchanged.

## Output Contract

```markdown
# Plan Review

**Verdict:** READY | REVISE | BLOCKED

## Scope and evidence
- Plan reviewed
- Repository areas inspected
- Commands or semantic queries used
- External sources consulted
- Limitations

## Findings
### [BLOCKER | MAJOR | MINOR] Finding title
- Evidence: file, symbol, command result, or authoritative source
- Impact: concrete failure, rework, or uncertainty
- Required change: smallest sufficient correction

## Corrected plan
Complete replacement plan for REVISE; otherwise state that the reviewed plan is ready or explain why correction is blocked.

## Open decisions and residual risks
Only unresolved user choices, explicitly accepted tradeoffs, and risks that remain after correction.
```
