---
name: ln-21-documentation-auditor
description: "Audits documentation and code comments for structure, coverage, factual accuracy, and maintainability. Use for documentation trust reviews; not code, test, or architecture audits."
---

# Documentation Auditor

Audit documentation as a read-only evidence system: can a new contributor, operator, user, or coding agent find the right source, trust its claims, and act without hidden context? Review both standalone documents and code comments where they carry public or operational knowledge.

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

Absence of documentation is a finding only when a real audience needs the missing knowledge. A stale claim is more serious than a missing optional explanation because it directs readers toward incorrect action.

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
- [ ] Find broken, redirected, case-sensitive, or repository-relative links and verify that linked files and headings exist.
- [ ] Identify orphan documents, duplicate entrypoints, circular navigation, deep chains, and important content reachable only by repository search.
- [ ] Check that concepts have one canonical owner and that secondary documents link rather than fork rules, thresholds, or procedures.
- [ ] Verify that generated documentation names its generator and does not invite hand editing that will be overwritten.
- [ ] Check whether large documents can be split or compressed without hiding the sequence or context needed to act safely.

### 3. Check Relevance, Coverage, and Consistency

- [ ] Compare each document's title, scope statement, and intended audience with its actual content.
- [ ] Judge content by document kind: indexes route without duplicating detail, references optimize exact lookup, how-to guides are safely sequenced, explanations build the right mental model, and decision records preserve context, decision, alternatives, and consequences.
- [ ] Identify off-topic content, scope creep, unexplained prerequisites, hidden assumptions, and sections that no longer support an active task.
- [ ] Check coverage of public behavior, configuration, deployment, migrations, failure recovery, security-sensitive operation, and extension points where applicable.
- [ ] Trace requirements and architecture statements across documents; report contradictions and ambiguous ownership rather than choosing silently.
- [ ] Find obsolete future-tense plans, completed TODOs, removed features, legacy compatibility guidance, old directory layouts, and stale screenshots or examples.
- [ ] Check terminology, entity names, identifiers, capitalization, and lifecycle states for consistency with code and across documents.
- [ ] Verify that warnings, prerequisites, destructive actions, rollback steps, and failure outcomes appear at the point where readers need them.
- [ ] In always-loaded agent instruction files, flag deterministic formatting rules better enforced by tooling and path-specific rules placed at repository root instead of scoped near the affected paths.

### 4. Verify Facts and Examples

- [ ] Extract material claims about paths, files, symbols, versions, counts, commands, flags, environment variables, configuration keys, ports, endpoints, schemas, and defaults.
- [ ] Build a normalized claim ledger before verification and group repeated claims by subject so one repository check can expose both stale copies and cross-document contradictions.
- [ ] Verify each claim against current repository evidence or a safe command; record the exact source and scope of the check.
- [ ] Resolve installed versions from manifests and lockfiles before consulting external documentation or claiming current support.
- [ ] Use official sources for external APIs, deprecations, security standards, platform limits, and compatibility statements.
- [ ] Execute examples only in a safe local or disposable context; otherwise inspect parsing, tests, and expected output and mark them statically verified.
- [ ] Check examples for missing imports, placeholders presented as real values, invalid paths, unsafe secrets, obsolete syntax, and output that no longer matches behavior.
- [ ] Filter examples, templates, future plans, conditional instructions, and external-system references before declaring a claim false; verify a conditional claim only when its prerequisite is active in this project.
- [ ] Verify numeric counts with a reproducible query and documented exclusions; avoid preserving aggregate counts that will drift without automation.
- [ ] Apply the research-to-action gate: external guidance becomes a finding only when it proves a concrete in-repository defect or risk.

### 5. Review Comments and Produce the Report

- [ ] Check comments and docstrings for useful rationale, invariants, contracts, side effects, failure behavior, and non-obvious constraints.
- [ ] Match docstrings for public or non-obvious interfaces against the current signature, parameters, return value, raised errors, side effects, nullability, and lifecycle obligations.
- [ ] Flag comments that narrate syntax, preserve history, contain dead code, promise behavior the code does not provide, or duplicate information better expressed by names and types.
- [ ] Check public interfaces for documentation required by the language or ecosystem and for examples that match the actual contract.
- [ ] Filter intentional audience simplification, framework convention, generated prose, and accepted legacy constraints before reporting.
- [ ] Classify findings as `P0`-`P3` based on the harm caused by wrong action, inability to operate, maintenance drift, or minor friction.
- [ ] Support every finding with document location, verifying evidence, affected audience, impact, and a concrete correction or canonical owner.
- [ ] Use `BLOCKED` when a safety-critical claim, required audience journey, or authoritative source cannot be verified without a credible fallback; use `FAIL` when evidence proves unsafe guidance, an inoperable required journey, or an unresolved `P0/P1`; use `CONCERNS` only for material non-blocking trust gaps, and `PASS` only when required claims and journeys are verified with no material finding.
- [ ] Return the verdict with audited scope, verified and unverified claims, prioritized findings, blind spots, and residual trust risk.

## Output Contract

```markdown
# Documentation Audit

**Verdict:** PASS | CONCERNS | FAIL | BLOCKED

## Scope and audiences
- Documents and comment surfaces audited
- Audiences and tasks considered
- Exclusions and generated content

## Trust summary
| Area | Status | Evidence |
|---|---|---|
| Structure | PASS / CONCERNS / FAIL | ... |
| Coverage | PASS / CONCERNS / FAIL | ... |
| Factual accuracy | PASS / CONCERNS / FAIL | ... |
| Comments and examples | PASS / CONCERNS / FAIL | ... |

## Findings
### [P0 | P1 | P2 | P3] Finding title
- Location: document, heading, or code symbol
- Evidence: repository, command, or official source
- Audience impact: incorrect action, missing capability, or maintenance cost
- Required change: correction and canonical owner

## Unverified claims and residual risks
Claims that could not be checked, why, and the evidence still required.
```
