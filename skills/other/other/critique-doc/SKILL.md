---
name: critique-doc
description: Hardnosed critic for fact-find, plan-feature, and process/skill documents. Surfaces weak claims, missing evidence, hidden assumptions, feasibility gaps, and unaddressed risks with no glazing.
---

# Critique Document (Compact Hardnosed Mode)

Critique fact-find, plan-feature, or process/skill documents for decision quality.
No compliments, no filler, no vibe-based approval.

## Operating Mode

READ-ONLY CRITIQUE

Allowed:
- Read target document and referenced docs/code/tests
- Search repo for verification
- Inspect git history for evidence

Not allowed:
- Editing target document
- Code changes
- Commits
- Creating new docs

## Inputs

Required:
- Path to target doc

Supported targets:
- Planning docs (`docs/plans/*-fact-find.md`, `docs/plans/*-plan.md`)
- Domain plan docs (for example `docs/cms-plan/*.md`)
- Process/skill docs (for example `.claude/skills/*/SKILL.md`)

Optional:
- Scope: `full` (default) or `focused`
- Context: extra constraints to pressure-test
- Prior critique reference (for delta scoring)

## Auto-Detection and Schema Mode

Detection order:
1. If frontmatter `Type` is `Fact-Find` or `Plan` and structure is consistent, use Section A or B.
2. Else if structure is consistent with planning docs, use Section A or B (filename is supportive, not required).
3. Else use Section C (Process schema mode).

If `Type` conflicts with structure:
- Route by structure
- Downgrade confidence
- Record `Header/Structure override: Yes`

Structure consistency rubric (A/B routing):
- Fact-Find consistent if >=3 of 4 headings exist with substantive content:
  - `Scope` or `Scope & Intent`
  - `Evidence Audit` or `Evidence Audit (Current State)`
  - `Confidence Inputs` or `Confidence Assessment`
  - `Planning Readiness`
- Plan consistent if >=3 of 4 headings exist with substantive content:
  - `Summary` or `Overview`
  - `Task Summary` or `Task List`
  - `Tasks` or `Implementation Tasks`
  - `Risks & Mitigations` or `Risks and Mitigations`
- Substantive content means at least one concrete bullet, table row, or sentence with verifiable detail.

Schema modes:
- Current: aligns with current templates/policies
- Legacy: older/different schema
- Process: non Fact-Find/Plan docs

Current/Legacy classification is separate from defect scoring.
A doc can be Current and still contain decision-quality defects.

In Legacy mode:
- Split findings into template drift vs decision-quality defects.
- Do not fail solely for template drift unless it blocks a decision.

## Tone and Stance

- Blunt, professional, unsentimental.
- Treat claims as guilty until proven by evidence.
- Flag ambiguity directly and explain why it matters.
- Use concrete labels: unsupported, inconsistent, hand-wavy, non-falsifiable, missing baseline.

## Materiality and Anti-Pedantry Rules

Decision impact first:
- Only elevate issues that can change decision quality, execution risk, correctness, or validation confidence.
- Template/style drift without decision impact is minor by default.

Severity tiers:
- Critical: blocks safe go/no-go decision or hides major risk.
- Major: materially increases failure/regression risk.
- Moderate: weakens execution clarity or validation confidence but decision remains possible.
- Minor: style/template drift with no meaningful decision impact.

Guardrails:
- Top Issues section should be mostly Critical/Major/Moderate findings.
- Include at most 2 Minor findings in Top Issues; move remaining minor notes to a short tail note.
- Minor-only findings cannot reduce overall score by more than 0.5.
- If all findings are Minor, verdict should be `credible` with revision notes, not `partially credible`.

## Core Method (Required)

### Step 0 - Frame the Decision

Identify:
- Decision owner
- Decision/question
- Implicit claim (therefore we should do X)

If missing, flag as missing decision spine.

### Step 1 - Structural Map

Extract:
- Objectives
- Proposed actions
- Constraints
- Key factual claims
- Key assumptions
- Metrics/confidence
- Dependencies
- Timeline/milestones (if any)

For each candidate finding, tag severity and decision impact before adding it to Top Issues.

### Step 2 - Claim-Evidence Audit

For each major claim:
1. State claim in falsifiable form.
2. Cite evidence.
3. Rate source quality (primary vs secondary; current vs stale).
4. Judge adequacy.
5. State what would disconfirm.

Required verification rule:
- Rank top 3 load-bearing claims first.
- Verify those 3 against repo/source docs.

### Step 2A - Source Conflict Arbitration (Before Scoring)

Precedence:
1. Direct user instruction in current request
2. `AGENTS.md`
3. `docs/AGENTS.docs.md`
4. Skill templates (`/plan-feature`, `/fact-find`)
5. Target doc assertions

Tie-breakers:
- More specific rule beats broader rule.
- Same specificity in same file: later line wins.
- Same precedence across files:
  - Newer `Last-reviewed`/`Last-updated` wins.
  - Else explicit gating/validation contracts beat advisory text.
- If unresolved: mark unresolved conflict, downgrade credibility, and recommend reconciliation before proceeding.

Mandatory known-conflict check for Plan/Fact-Find critiques:
- Check metadata requirement differences between `AGENTS.md`, `docs/AGENTS.docs.md`, and templates.

### Step 3 - Assumption Mining

Classify assumptions:
- Stated
- Implied
- Convenient

Rate fragility and identify cheap tests.

### Step 4 - Logic Check

Look for:
- Non sequiturs
- Term shifts
- Overgeneralization
- Missing counterfactuals
- Circular reasoning
- Confidence not supported by evidence

### Step 5 - Feasibility and Execution Reality

Check (code/mixed):
- Paths/patterns exist
- Dependency chain realism
- Failure points and rollback paths
- Effort honesty

Check (business-artifact/mixed — additionally):
- Can each VC actually be executed within the stated time-box and budget?
- Is the falsification cost realistic given the business's current resources?
- Are approval paths available (reviewer named, process exists)?
- Is measurement infrastructure in place (tracking pixel, analytics, CRM), or does it need to be built first?

### Step 6 - Contrarian Attacks

Do at least 3:
- Inversion
- Pre-mortem
- Competing hypothesis
- Goodhart risk
- Second-order effects
- Boundary test

### Step 7 - Fix List

Provide concrete rewrite instructions with section targets.
Prefer merged, high-leverage fixes over many tiny edits.

## Section A: Fact-Find Lens

Required checks:
- Frontmatter fields:
  - `Type`, `Outcome`, `Status`, `Domain`, `Workstream`, `Created`, `Last-updated`, `Feature-Slug`, `Deliverable-Type`, `Execution-Track`, `Primary-Execution-Skill`, `Supporting-Skills`, `Related-Plan`
  - `Business-OS-Integration` must be explicit (`on`/`off`)
  - If `on`, require `Business-Unit` and `Card-ID`
  - **Card-ID timing:** The fact-find skill creates cards even at `Needs-input` status. A missing `Card-ID` when `Business-OS-Integration: on` means the card creation workflow was skipped — flag as Moderate (process gap), not Critical.
  - In Legacy mode, missing BOS fields are template drift unless higher-precedence policy says mandatory
- Sections present and substantive:
  - Scope (summary/goals/non-goals)
  - Evidence Audit
  - Confidence Inputs
  - Risks (specific to the work, not generic)
  - Planning Readiness
  - Test Landscape for code/mixed
  - Delivery and Channel Landscape for business-artifact/mixed
  - Hypothesis & Validation Landscape for business-artifact/mixed (key hypotheses, existing signal coverage, falsifiability assessment, recommended validation approach) — this feeds `/plan-feature`'s Business VC Quality Checklist. Missing on a business-artifact/mixed brief is Major (downstream VCs will lack grounding).

Fact-Find confidence dimensions:
- The fact-find skill defines **5 dimensions**: Implementation, Approach, Impact, Delivery-Readiness, Testability.
- Do NOT penalize fact-finds for having 5 dimensions instead of 3. The 3-dimension model (Implementation/Approach/Impact) applies to plan tasks, not fact-find briefs.

Fact-Find `Related-Plan` field:
- `Related-Plan` is a **forward pointer** to the plan that will be created by `/plan-feature`.
- It is normal and expected for this file to not exist at fact-find time.
- Do NOT flag a non-existent `Related-Plan` target as an issue.

Open questions checks:
- Each open question should include `Decision owner` (name or role).
- Missing decision owner weakens accountability but is Moderate, not Critical.

Fact-Find minimum bar:
- Falsifiable goals
- Evidence trail for major factual claims
- Confidence justifications tied to evidence
- At least one specific risk identified
- No Ready-for-planning with untested load-bearing assumptions

## Section B: Plan Lens

Apply checks in order:
1. Plan-template conformance
2. Repo metadata policy conformance

Plan frontmatter baseline:
- `Type`, `Status`, `Domain`, `Workstream`, `Created`, `Last-updated`, `Feature-Slug`, `Deliverable-Type`, `Execution-Track`, `Primary-Execution-Skill`, `Supporting-Skills`

Repo metadata policy check:
- `Last-reviewed` and `Relates-to charter`
- Missing repo-required metadata is a decision-quality defect unless explicit higher-precedence exemption applies

Confidence-gated markers:
- Task Summary includes `Confidence` column
- One or more tasks include confidence breakdowns (Implementation/Approach/Impact)
- Frontmatter includes `Overall-confidence` or `Confidence-Method`

Confidence metadata rule:
- If confidence-gated markers exist, missing `Overall-confidence` and/or `Confidence-Method` is a decision-quality defect.
- If markers do not exist, missing confidence metadata is standards drift.

Each IMPLEMENT task must include:
- Type, Deliverable, Execution-Skill, Affects, Depends on, Blocks
- Confidence (3 dimensions + evidence)
- Acceptance criteria
- Validation contract (TC-XX or VC-XX)
- Execution plan:
  - Code/mixed: Red -> Green -> Refactor
  - Business-artifact/mixed: VC-first Red -> Green -> Refactor
- Rollout/rollback
- Documentation impact

Business-artifact/mixed VC quality check (apply to each VC-XX):
- Each VC must be **isolated** (tests one variable), **pre-committed** (pass/fail decision stated before data), **time-boxed** (measurement deadline defined), **minimum viable sample** (smallest signal that constitutes evidence), **diagnostic** (failure indicates *why*), **repeatable** (another operator reaches same conclusion), and **observable** (metric is directly measurable).
- Anti-patterns to flag: "Validate demand is sufficient" (not isolated, not pre-committed, not observable), "Check market response" (no sample size, no deadline), "Confirm unit economics work" (conflates multiple variables).
- VCs failing ≥3 quality principles are Major; failing 1-2 is Moderate.

Plan minimum bar:
- Falsifiable objective
- Risk-first dependency order
- Enumerated validation cases
- Confidence tied to evidence
- Explicit risks and mitigations

## Section C: Process/Skill Lens

Required checks:
- Audience and decision/action are explicit
- Inputs/outputs/boundaries are explicit
- Allowed vs disallowed actions are explicit
- Escalation/exception paths are explicit
- No internal rule contradictions
- Output template enforces method steps
- Alignment with source-of-truth docs and legacy handling

## Cross-Document Consistency (Plan + Fact-Find)

If a plan references a fact-find:
- Compare goals, approach, open questions, confidence transitions, execution routing, and coverage gaps.
- If conflicts arise, apply Step 2A and record resolution.

## Scoring (Recalibrated)

Use 0-5 scores per dimension:
- Evidence quality
- Coherence
- Completeness (decision-grade)
- Feasibility
- Measurability
- Risk handling

Weighted overall score:
- Overall(raw) =
  - 0.25 Evidence
  - 0.20 Coherence
  - 0.15 Completeness
  - 0.15 Feasibility
  - 0.10 Measurability
  - 0.15 Risk handling
- Round to nearest 0.5.

Completeness (decision-grade) anchors:
- 5.0: All decision-critical components present and substantive; only minor drift remains.
- 4.0-4.5: One or two non-critical gaps; decision remains well-supported.
- 3.0-3.5: At least one meaningful (Moderate) gap that weakens confidence but does not block decision.
- 2.0-2.5: Multiple Major gaps or one unresolved Critical gap that blocks reliable decision.
- 0.0-1.5: Missing decision spine or pervasive evidence/control gaps.

Severity caps (apply after weighting):
- Unresolved source conflict: overall <= 2.0
- Internal contradiction in routing/scoring rules: overall <= 2.5
- Top 3 load-bearing claims not verified against sources: overall <= 3.0
- Missing validation contracts on >30% IMPLEMENT tasks (plan): overall <= 3.0
- Caps apply only to Critical failures. Major/Moderate findings do not trigger these caps.

Stability rule (to prevent score whiplash):
- If prior critique exists and no new Critical or Major issues are found, overall score cannot move by more than 0.5.
- Any move >0.5 requires explicit delta justification:
  - Newly discovered issues (with references)
  - Resolved issues (with references)
  - Why the net score moved

Anchor definitions:
- 5.0: Decision-ready, no material defects
- 4.0-4.5: Credible, only minor/non-blocking defects
- 3.0-3.5: Partially credible, bounded but meaningful gaps
- 2.0-2.5: Not credible, major defects block safe decision
- 0.0-1.5: Structurally broken for decision use

## Required Output Template

### 1) Executive Verdict

The document is **(credible / partially credible / not credible)** because: ...

Decision frame: **Decision owner:** ... | **Decision/question:** ...
Schema mode: **Current / Legacy / Process**
Header/Structure override: **Yes/No** - <if yes, why>
Mode evidence: <matched headings/markers used for routing>

Biggest decision-quality failures: ...
Recommended action: **proceed** / **revise and re-critique** / **return to /fact-find** / **run /re-plan** / **revise process or skill doc and re-critique**

### 2) Top Issues (ranked)

- `full`: 5-12 issues
- `focused`: top 5 issues only
- Include severity tags (`Critical`, `Major`, `Moderate`, `Minor`) for each issue.
- Keep Minor issues to max 2 in this section.

### 2a) Legacy Mode Split (only if Schema mode is Legacy)

- Template drift
- Decision-quality defects

### 3) Top 3 Load-Bearing Claims (ranked)

### 4) Claim-Evidence Audit

| # | Claim | Section | Evidence | Adequacy | Disconfirming Test |
|---|---|---|---|---|---|

### 4a) Conflict Resolution Notes (if conflicts occurred)

- Conflict
- Source A (`path:line`)
- Source B (`path:line`)
- Applied precedence/tie-breaker
- Residual ambiguity

### 5) Hidden Assumptions

| # | Assumption | Type | Fragility | Cheap Test |
|---|---|---|---|---|

### 6) Logic / Reasoning Faults

### 7) Contrarian Section

Include at least 3 distinct attacks.

### 8) Risks and Second-Order Effects

| Risk | Likelihood | Impact | Mitigation in Doc | Adequate? |
|---|---|---|---|---|

### 9) What Is Missing to Make This Decisionable

### 10) Concrete Fixes

Format:
- Fix -> Section -> Action

### 11) Scorecard (skip for `focused`)

| Dimension | Score | Justification |
|---|---|---|

Include:
- Weighted overall score
- Any severity cap applied
- Severity distribution summary (Critical/Major/Moderate/Minor counts)
- If prior critique exists: delta note (what changed and why)

## Workflow Integration

Recommended next actions:
- Fact-find has major evidence gaps -> additional `/fact-find`
- Fact-find confidence unjustified -> rework confidence with evidence
- Plan confidence inflation -> `/re-plan`
- Plan missing validation contracts -> revise plan before `/build-feature`
- Plan contradicts fact-find -> `/re-plan` with fact-find input
- Unresolved source conflict -> reconcile source docs, then re-critique
- Process/skill contradictions -> revise rules, then re-critique
- Document fundamentally sound -> proceed

## Quality Checks (Self-Audit)

- Every issue has section/line reference.
- Schema mode, decision frame, and header/structure override are explicit.
- Mode evidence is explicit.
- Top 3 load-bearing claims were ranked then verified.
- Claim table aligns with top 3 claims.
- Conflict notes are complete when conflicts exist.
- Contrarian section has >=3 distinct attacks.
- Fixes are concrete and actionable.
- Scorecard justifications trace to cited issues.
- Completeness score justification references decision-critical coverage, not template box-ticking.
- Minor findings are not allowed to dominate verdict or score movement.
- If score moved >0.5 from prior critique, delta justification is included.
- No praise, no filler, no motivational language.
