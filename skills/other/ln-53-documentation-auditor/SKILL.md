---
name: ln-53-documentation-auditor
description: "Audits documentation and comments for trust, coverage, consistency and freshness; read-only."
---

# Documentation Auditor

**Goal:** Audit documentation as a read-only evidence system: can a new contributor, operator, user, or coding agent find the right source, trust its claims, and act without hidden context? Review both standalone documents and code comments where they carry public or operational knowledge.

**Execution contract:** The ordered checkboxes are the Definition of Done. Track every item internally as `PENDING`, `PROVEN` with concrete evidence, `CLEARED` with evidence that its condition is absent, or `UNPROVEN` with a gap; reading, delegation, or tool failure is not proof. Reconcile items after each section. Before returning, resolve all `PENDING` and count only `PROVEN` and `CLEARED`; apply the skill's verdict and approval rules to every gap.
Preserve user intent, scope, and existing authorization. Continue authorized work; ask only for consequential unresolved choices or required external approval. Scale depth to material risk without silently skipping checks. Preserve dependency and safety ordering; otherwise choose the verification method appropriate to each obligation.
Treat equivalent user or repository evidence as valid input; another skill, named artifact, or complete lifecycle is not a prerequisite. Preserve source requirement and decision identifiers when available. Bind reused evidence to the relevant source version, dirty changes, configuration, and environment; invalidate only affected claims after a change.
On continuation, reconcile the task, existing authorization, current state, and unresolved evidence before resuming. For long work, return a compact continuation record or update an already authorized task artifact; read-only skills do not persist it. Distinguish artifact readiness, verified behavior, and authority to perform an external action.
Prepare authorized work before any required approval. If an instruction prevents progress, identify its exact source and explain the unresolved boundary; do not invent an approval gate from general caution.


## Tool Routing

| Need | Preferred tool | Use it when | Fallback |
|---|---|---|---|
| Document inventory and hierarchy | Native file listing with narrow patterns | Establishing documentation surfaces, generated areas, and navigation structure | Repository tree and known entry documents |
| Links, repeated terms, claims, and contradictions | Native text search, then focused reads | Finding references, stale names, duplicated guidance, paths, commands, and configuration keys | Manual cross-document comparison |
| Code and configuration truth | Native code search, manifests, schemas, and direct file reads | A document claims that a path, option, endpoint, behavior, or default exists | Execute a safe inspection command when text is insufficient |
| Freshness and ownership | Git log, blame, and diff | Determining when a claim changed, whether a document tracks active code, or who owns a convention | Current code and explicit ownership files |
| Commands and examples | Shell in non-mutating or dry-run mode | Verifying help text, command existence, config parsing, generated output, or example syntax | Inspect command registration and tests; mark runtime proof unavailable |
| External facts | Official documentation, specifications, and release notes | A current external API, version, standard, or platform behavior affects correctness | Primary-source web research; otherwise mark `UNVERIFIED` |

Do not run commands that publish, migrate, deploy, write production state, or rewrite documentation. Generated caches are acceptable only when permitted and disclosed.

## Evidence Rules

| Claim type | Required evidence |
|---|---|
| Repository path, symbol, command, configuration, endpoint, or default | Current repository or safe command output |
| External API, version, standard, or compatibility statement | Official source matching the relevant version |
| Count or coverage statement | Reproducible query with scope and exclusions |
| Historical rationale | Current decision record or history that still matches implementation |
| Recommendation | A demonstrated reader failure, contradiction, maintenance cost, or operational risk |

Absence of documentation is a finding only when a real audience needs the missing knowledge. Judge stale and missing guidance by the reader failure or harm they cause.

## Checklist

### 1. Establish Scope and Audiences

- [ ] Identify documentation entrypoints, public docs, maintainer docs, operational runbooks, generated references, examples, and code-comment surfaces in scope.
- [ ] Identify intended audiences and their concrete tasks: understand, install, configure, operate, troubleshoot, extend, or verify the system.
- [ ] Read applicable repository instructions and detect documentation ownership, generation commands, language policy, and source-of-truth conventions.
- [ ] Separate authored documents from generated, vendored, archived, temporary, and example content before scoring defects.
- [ ] Classify each target as entrypoint/index, reference, how-to, explanation, decision record, generated output, or example; prioritize canonical and claim-dense documents before navigation-only files.
- [ ] Define which code, configuration, schemas, tests, and external contracts can verify documentation claims.
- [ ] Keep the audit read-only and record any unavailable source, command, or environment as a limitation.

### 2. Check Structure and Discoverability

- [ ] Verify that the root entry document explains purpose, supported use, prerequisites, installation path, and navigation appropriate to its audience.
- [ ] Check hierarchy, headings, table of contents, local navigation, cross-links, anchors, and predictable placement of related material.
- [ ] Verify local paths and anchors, including case sensitivity, and inspect external redirects for a wrong or unavailable destination; a working intentional redirect is not a defect.
- [ ] Identify orphan documents, duplicate entrypoints, circular navigation, deep chains, and important content reachable only by repository search.
- [ ] Check that concepts have one canonical owner and that secondary documents link rather than fork rules, thresholds, or procedures.
- [ ] Verify that generated documentation names its generator and does not invite hand editing that will be overwritten.
- [ ] Check whether large documents can be split or compressed without hiding the sequence or context needed to act safely.

### 3. Check Relevance, Coverage, and Consistency

- [ ] Compare each document's title, scope statement, and intended audience with its actual content.
- [ ] Judge content by document kind: indexes route without duplicating detail, references optimize exact lookup, how-to guides are safely sequenced, explanations build the right mental model, and decision records preserve context, decision, alternatives, and consequences.
- [ ] Flag filler, repeated summaries, speculative narration, generic generated prose, and ceremonial sections that do not help the intended audience decide or act.
- [ ] Prefer durable intent, contracts, constraints, and operations over copied implementation or business logic; retain only minimal verified code or command examples needed to act safely.
- [ ] Identify off-topic content, scope creep, unexplained prerequisites, hidden assumptions, and sections that no longer support an active task.
- [ ] Check coverage of public behavior, configuration, deployment, migrations, failure recovery, security-sensitive operation, and extension points where applicable.
- [ ] Trace requirements and architecture statements across documents; report contradictions and ambiguous ownership rather than choosing silently.
- [ ] Find obsolete future-tense plans, completed TODOs, removed features, legacy compatibility guidance, old directory layouts, and stale screenshots or examples.
- [ ] Check terminology, entity names, identifiers, capitalization, and lifecycle states for consistency with code and across documents.
- [ ] Verify that warnings, prerequisites, destructive actions, rollback steps, and failure outcomes appear at the point where readers need them.
- [ ] In always-loaded agent instructions, identify redundant formatting prose already enforced by tooling and path-specific detail that can move to supported scoped files. Preserve discovery, non-obvious requirements, and host compatibility.

### 4. Verify Facts and Examples

- [ ] Extract material claims about paths, files, symbols, versions, counts, commands, flags, environment variables, configuration keys, ports, endpoints, schemas, and defaults.
- [ ] Build a normalized claim ledger before verification and group repeated claims by subject so one repository check can expose both stale copies and cross-document contradictions.
- [ ] Verify each claim against current repository evidence or a safe command; record the exact source and scope of the check.
- [ ] Resolve installed versions from manifests and lockfiles before consulting external documentation or claiming current support.
- [ ] Use official sources for external APIs, deprecations, security standards, platform limits, and compatibility statements.
- [ ] Execute examples only in a safe local or disposable context; otherwise inspect parsing, tests, and expected output and mark them statically verified.
- [ ] Check examples for missing imports, placeholders presented as real values, invalid paths, unsafe secrets, obsolete syntax, and output that no longer matches behavior.
- [ ] Interpret examples, templates, future plans, and external references in their declared context. Verify conditional guidance for supported prerequisites even when currently disabled; do not judge a hypothetical example as deployed behavior.
- [ ] Verify numeric counts with a reproducible query and documented exclusions; avoid preserving aggregate counts that will drift without automation.
- [ ] Recommend moving change-prone versions, paths, defaults, inventories, generated output, and status snapshots to authoritative code, configuration, or generated sources where practical; otherwise identify the source, scope, and owner or generation/update trigger needed to prevent silent staleness.
- [ ] Apply the research-to-action gate: external guidance becomes a finding only when it proves a concrete in-repository defect or risk.

### 5. Review Comments and Produce the Report

- [ ] Check comments and docstrings for useful rationale, invariants, contracts, side effects, failure behavior, and non-obvious constraints.
- [ ] Match docstrings for public or non-obvious interfaces against the current signature, parameters, return value, raised errors, side effects, nullability, and lifecycle obligations.
- [ ] Flag syntax narration, obsolete history, dead code, false promises, and information better expressed by names or types; preserve historical rationale that still explains a constraint or prevents a known regression.
- [ ] Check public interfaces for documentation required by the language or ecosystem and for examples that match the actual contract.
- [ ] Filter intentional audience simplification, framework convention, generated prose, and accepted legacy constraints before reporting.
- [ ] Classify every in-scope document or comment surface as `KEEP`, `ADD`, `UPDATE`, `DELETE`, or `MERGE`; recommend deletion or consolidation only when canonical coverage preserves every required audience task and contract.
- [ ] Apply the materiality gate: require concrete reader error, blocked task, unsafe action, contradiction, or recurring maintenance cost at evidenced scale. Reject taste, theoretical purity, generic practice, hypothetical scale, and reasonable alternatives; require the outcome or constraint, not a preferred implementation.
- [ ] Ground external corrections in version-matched official contracts, using primary engineering sources for unresolved tradeoffs. Cite the supported mechanism; local evidence suffices for local defects.
- [ ] Classify findings as `P0`-`P3` based on the harm caused by wrong action, inability to operate, maintenance drift, or minor friction.
- [ ] Use `BLOCKED` when a safety-critical claim, required audience journey, or authoritative source cannot be verified without a credible fallback; use `FAIL` when evidence proves unsafe guidance, an inoperable required journey, or an unresolved `P0/P1`; use `CONCERNS` only for material non-blocking trust gaps, and `PASS` only when required claims and journeys are verified with no material finding.

- [ ] For each accepted finding, identify the owning documentation surface, affected reader outcome, and evidence that a correction would restore trust; do not turn recommendations into authorized edits.

## Self-Check

- [ ] **Reconcile before returning.** Check item-level evidence, requirement coverage, contradictions, scope, verdict, and applicable cleanup. Correct the report or authorized artifacts. Reuse valid evidence; do not automatically rescan the repository or rerun successful commands. Repeat checks only for relevant changes, failures, or unresolved evidence. Disclose remaining gaps.

## Output Contract

Report in the user's language, in this order; retain all five fields and state each fact once. Small results may use one line per field; omit empty tables and do not copy linked artifacts:

1. **Result:** Skill-specific verdict and supported outcome.
2. **Scope:** Reviewed/changed scope, exclusions, baseline, and material assumptions.
3. **Evidence:** Skill-specific fields below; distinguish facts, inferences, and unverified claims. Link artifacts; use tables when useful.
4. **Verification:** Checks/results, unavailable evidence, and applicable cleanup/external state.
5. **Completion:** `Checklist: X/Y complete`; `Incomplete: None` or each `UNPROVEN` item's reason, outcome impact, and exact next action; residual risks and required decisions.

**Skill-specific evidence:** Documentation audiences and journeys; structure, coverage, accuracy, durability/SSOT, and comment trust. Record `KEEP / ADD / UPDATE / DELETE / MERGE` per in-scope surface. Findings need priority, document location, verifying evidence, affected audience, material impact, unacceptable tradeoff, and minimal correction or canonical owner; allow equivalent structures. Distinguish unverified claims from proven defects.
