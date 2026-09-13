---
name: ln-81-skill-reviewer
description: "Reviews skill instructions, trigger boundaries and distribution contracts; not product code."
---

# Skill Reviewer

**Goal:** Review skill quality and configured distribution surfaces without modifying repository or external state. Distinguish static contract assurance from observed execution behavior.

**Execution contract:** The ordered checkboxes are the Definition of Done. Track every item internally as `PENDING`, `PROVEN` with concrete evidence, `CLEARED` with evidence that its condition is absent, or `UNPROVEN` with a gap; reading, delegation, or tool failure is not proof. Reconcile items after each section. Before returning, resolve all `PENDING` and count only `PROVEN` and `CLEARED`; apply the skill's verdict and approval rules to every gap.
Preserve user intent, scope, and existing authorization. Continue authorized work; ask only for consequential unresolved choices or required external approval. Scale depth to material risk without silently skipping checks. Preserve dependency and safety ordering; otherwise choose the verification method appropriate to each obligation.
Treat equivalent user or repository evidence as valid input; another skill, named artifact, or complete lifecycle is not a prerequisite. Preserve source requirement and decision identifiers when available. Bind reused evidence to the relevant source version, dirty changes, configuration, and environment; invalidate only affected claims after a change.
On continuation, reconcile the task, existing authorization, current state, and unresolved evidence before resuming. For long work, return a compact continuation record or update an already authorized task artifact; read-only skills do not persist it. Distinguish artifact readiness, verified behavior, and authority to perform an external action.
Prepare authorized work before any required approval. If an instruction prevents progress, identify its exact source and explain the unresolved boundary; do not invent an approval gate from general caution.


## Tool Routing

| Need | Preferred capability | Fallback |
|---|---|---|
| Repository scope and evidence | Native file search, focused reads, and Git diff | Equivalent read-only shell commands |
| Frontmatter and skill structure | Repository-defined or host-native skill validator | Manual YAML, path, naming, and repository-contract checks |
| Plugin integration | Repository-defined plugin validator plus manifest parsing | Manual manifest and applicable catalog comparison |
| Host discovery | Host-native validator for every configured distribution surface | Manual catalog, manifest, and source-path inspection |
| Current host rules | Official host documentation | Mark the claim `UNVERIFIED` when unavailable |
| Behavioral independence | Fresh subagent or clean context | Separate self-review passes with reduced-confidence disclosure |

Use external research only for current host behavior or a changing standard. Do not use web sources to override the repository's actual files, installed versions, or local validation output.

Tool absence is not itself a skill defect. Apply the documented fallback and use `BLOCKED` only when the missing capability prevents a reliable verdict.

## Checklist

### Establish scope and evidence

- [ ] Resolve target paths, Git diff, staged and untracked files; establish review mode: static content/distribution review, or behavioral validation when requested or warranted and permitted. Honor an explicit no-testing instruction; do not run scenarios or delegate evaluation in static-only mode.
- [ ] Read the repository instructions, skill contracts, and every configured host catalog before judging repository-specific conventions; do not require a catalog that the repository does not distribute.
- [ ] Separate primary skills from manifests, catalogs, and documentation affected by the same change.
- [ ] Confirm the repository-defined canonical skill layout; treat unauthorized, stale, or divergent host-specific copies as defects, while permitting adapters or generated copies that repository policy explicitly requires.
- [ ] Confirm frontmatter and folder naming satisfy the repository contract and each target host; require only `name` and `description` when that is the declared local convention rather than imposing it universally.
- [ ] Check that each description states the capability, positive trigger, and important near-negative boundary.
- [ ] Check that descriptions stay within the host limit and avoid claims broader than the workflow supports.
- [ ] Confirm each skill is standalone: no required skill, MCP server, tracker, coordinator, worker, or shared runtime.
- [ ] Apply the repository's declared completion convention; when an ordered checklist is the Definition of Done, flag a duplicate completion section.
- [ ] Preserve domain algorithms, tool routing, safety gates, evidence, verdicts, output, and residual risks. For removed checks, identify the retained obligation owner or explain why the check does not support the Goal; item count alone proves neither loss nor preservation.
- [ ] Flag generic explanations that add no decision value; preserve non-obvious domain knowledge and concrete safeguards even when no prior failure was recorded.
- [ ] Check content hierarchy and single-source ownership: keep each rule in the narrowest canonical section and flag repeated or contradictory guidance across the body, supporting files, manifests, and repository instructions.
- [ ] Flag filler, generated-summary prose, copied implementation or business logic, and volatile versions, paths, counts, defaults, or host behavior that can be replaced by a stable contract, authoritative source, capability description, or explicit update trigger.
- [ ] Verify every required capability has an available tool path, a credible fallback, or an explicit `BLOCKED` outcome.
- [ ] Check that each skill's mutation boundary matches its declared outcome; read-only workflows must not acquire implicit write authority.
- [ ] For optimization or experiment skills, require an evidence-based retain, discard, or rollback decision when they mutate state.
- [ ] For test-building or other bounded writers, confirm they cannot repair product code or touch unapproved external state unless their declared contract explicitly authorizes it.
- [ ] Trace the text through normal completion, missing tools, insufficient context, dirty Git state, failed commands, and conflicting evidence. Check prerequisites precede dependent actions, stop conditions permit safe progress, and verdicts cover failure states without contradiction.
- [ ] Check that the output contract distinguishes facts, inferences, missing evidence, verdict, and residual risk.
- [ ] Compare neighboring triggers with each skill's Goal; require instructions to support an outcome, evidence need, or scope/safety constraint. Flag irrelevant work, missing obligations, and ambiguous branches without making skills depend on each other.

### Repository Validation

- [ ] Discover and run every repository-required skill validator for the changed skill directories; do not assume a validator name or location absent from repository evidence.
- [ ] If a required validator is unavailable, manually validate YAML parsing, naming, description constraints, and required file layout against the repository and host contracts.
- [ ] Run every repository-required plugin or package validator for affected distribution units.
- [ ] Run each host-native strict validator when its corresponding catalog or manifest exists; record its actual coverage and do not treat marketplace validation as skill-frontmatter validation unless the host demonstrably traverses those skills.
- [ ] Parse all configured catalogs; compare plugin names and ordering only when repository policy requires cross-host parity.
- [ ] Confirm every declared catalog source, manifest path, and skill path exists.
- [ ] Confirm duplicated metadata such as plugin descriptions agree wherever the repository requires parity.
- [ ] For marketplace repositories, confirm stable identifiers have not changed unintentionally; display branding is not an identifier substitute.
- [ ] Search for stale names, deleted paths, draft markers, MCP coupling, orchestration terms, and generated copies.
- [ ] Apply line-count targets only when repository policy defines them, and treat them as a maintenance constraint rather than evidence of behavioral quality.

### Behavioral Review When In Scope

- [ ] Apply this phase only when behavioral execution is in scope and authorized; otherwise mark its execution-only items `CLEARED` with the scope reason and state that behavior was not tested. Static inspection does not prove activation or execution quality.
- [ ] Derive representative positive prompts from the stated trigger rather than from the skill title alone.
- [ ] Derive close negative prompts from adjacent capabilities and likely ambiguous user wording.
- [ ] Verify the skill would activate for the positive prompts and remain inactive for close negatives.
- [ ] Walk at least one normal scenario, one missing-evidence scenario, and one safety-boundary scenario.
- [ ] When the skill writes code or other artifacts, evaluate a real agent-produced result and diff against an independent task contract; do not substitute prose review, answer brevity, or static inspection for execution behavior.
- [ ] Grade task completeness, correctness, safety, scope containment, and cleanup independently; treat code or token reduction as supporting evidence only after the required outcome passes.
- [ ] For complex or high-risk changes, use fresh independent contexts when available and provide only the skill plus raw task artifacts.
- [ ] Do not reveal expected findings, intended fixes, or prior conclusions to an independent evaluator.
- [ ] Treat a forward test that succeeds only with leaked context as a skill defect.
- [ ] Check independent contexts for contamination from globally installed skills, hooks, plugins, user instructions, environment settings, caches, or artifacts; prove target-skill activation and invalidate an arm whose behavior cannot be attributed reliably.
- [ ] Do not create or retain an evaluation harness unless a concrete recurring failure proves it necessary.

### Evidence Rules

- [ ] Cite each finding to an exact file and the smallest useful line or section.
- [ ] Distinguish validator failures from manual concerns and speculative improvements.
- [ ] Require deterministic validator evidence, an authorized reproduction, or a complete static contradiction/failure path before assigning blocking severity; do not execute scenarios excluded by the review mode.
- [ ] Record commands executed, exit status, and material output without exposing secrets.
- [ ] Report coverage gaps when a required host or clean-context test cannot be run. Keep any permitted diagnostic artifact temporary, outside canonical plugin directories, and disclose it; do not stage, publish, or create external state during review.

## Verdict

- `PASS` — all required checks for the declared mode pass with no material concern; static-only `PASS` does not certify execution behavior.
- `PASS WITH CONCERNS` — no confirmed blocking defect in the reviewed scope, but bounded non-blocking uncertainty remains; do not infer untested publication or behavioral readiness.
- `FAIL` — a confirmed defect can cause wrong triggering, unsafe behavior, broken installation, or an invalid contract.
- `BLOCKED` — required evidence or tooling is unavailable and no credible fallback exists.

- [ ] Review input/output compatibility, stale-evidence handling, continuation, and instruction conflicts while preserving detailed checklists and the common final report; distinguish static checks from observed agent behavior.

## Self-Check

- [ ] **Reconcile before returning.** Check item-level evidence, requirement coverage, contradictions, scope, verdict, and applicable cleanup. Correct the report or authorized artifacts. Reuse valid evidence; do not automatically rescan the repository or rerun successful commands. Repeat checks only for relevant changes, failures, or unresolved evidence. Disclose remaining gaps.

## Output Contract

Report in the user's language, in this order; retain all five fields and state each fact once. Small results may use one line per field; omit empty tables and do not copy linked artifacts:

1. **Result:** Skill-specific verdict and supported outcome.
2. **Scope:** Reviewed/changed scope, exclusions, baseline, and material assumptions.
3. **Evidence:** Skill-specific fields below; distinguish facts, inferences, and unverified claims. Link artifacts; use tables when useful.
4. **Verification:** Checks/results, unavailable evidence, and applicable cleanup/external state.
5. **Completion:** `Checklist: X/Y complete`; `Incomplete: None` or each `UNPROVEN` item's reason, outcome impact, and exact next action; residual risks and required decisions.

**Skill-specific evidence:** Target skills and distribution surfaces; structural/host parity, trigger boundaries, static versus behavioral coverage, and validator results. Findings need severity, exact location, impact, evidence, and minimal correction. Distinguish confirmed defects, manual concerns, and speculative improvements; report unavailable clean-context or runtime evidence and disclosed temporary artifacts.
