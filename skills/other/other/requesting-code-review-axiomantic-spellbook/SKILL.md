---
name: requesting-code-review
description: "Use when implementation is done and you need a structured pre-PR review workflow. Triggers: 'ready for review', 'review my changes before PR', 'pre-merge check', 'is this ready', 'submit for review'. Orchestrates multi-phase review (planning, context assembly, dispatch, triage, fix, gate). Dispatches code-review internally. NOT the same as finishing-a-development-branch (which handles merge/PR decisions after review passes)."
---

# Requesting Code Review

<ROLE>
Self-review orchestrator. Coordinates pre-PR code review workflow.
</ROLE>

<analysis>
Before starting review workflow, analyze:
1. What is the scope of changes? (files, lines, complexity)
2. Is there a plan/spec document to review against?
3. What is the current git state? (branch, merge base)
4. What phase should we resume from if this is a re-review?
</analysis>

## Invariant Principles

1. **Phase gates are blocking** - Never proceed to next phase without meeting exit criteria
2. **Evidence over opinion** - Every finding must cite specific code location and behavior
3. **Critical findings are non-negotiable** - No Critical finding may be deferred or ignored
4. **SHA persistence** - Always use reviewed_sha from manifest, never current HEAD
5. **Traceable artifacts** - Each phase produces artifacts for resume and audit capability

<FORBIDDEN>
- Proceeding past Phase 6 gate with unfixed Critical findings
- Making findings without specific file:line evidence
- Using current HEAD instead of reviewed_sha for inline comments
- Skipping re-review when fix adds >100 lines or modifies new files
- Deferring Critical findings for any reason
</FORBIDDEN>

<reflection>
After each phase, verify:
- Did we meet all exit criteria before proceeding?
- Are all findings backed by specific evidence?
- Did we persist the correct SHA for future reference?
- Is the artifact properly saved for traceability?
</reflection>

## Phase-Gated Workflow

Reference: `patterns/code-review-formats.md` for output schemas.

### Phases 1-2: Planning + Context

Determine git range, list files, identify plan/spec, estimate complexity, then assemble reviewer context bundle with plan excerpts, related code, and prior findings.

**Execute:** `/request-review-plan`

**Outputs:** Review scope definition, reviewer context bundle

**Self-Check:** Git range defined, file list confirmed, context bundle ready for dispatch.

### Phases 3-6: Dispatch + Triage + Execute + Gate

Invoke code-reviewer agent, triage findings by severity, execute fixes (Critical first), then apply quality gate for proceed/block decision.

**Execute:** `/request-review-execute`

**Outputs:** Review findings, triage report, fix report, gate decision

**Self-Check:** Valid findings received, triaged, blocking findings addressed, clear verdict.

### Artifact Contract

Directory structure, phase artifact table, manifest schema, and SHA persistence rule.

**Reference:** `/request-review-artifacts`

## Gate Rules

Reference: `patterns/code-review-taxonomy.md` for severity definitions.

### Blocking Rules

| Condition | Result |
|-----------|--------|
| Any Critical unfixed | BLOCKED - must fix before proceed |
| Any High unfixed without rationale | BLOCKED - fix or document deferral |
| >=3 High unfixed | BLOCKED - systemic issues |
| Only Medium/Low/Nit unfixed | MAY PROCEED |

<CRITICAL>
Always use `reviewed_sha` from manifest for inline comments.
Never query current HEAD - commits may have been pushed since review started.
</CRITICAL>
