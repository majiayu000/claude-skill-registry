---
name: lp-do-critique
description: Hardnosed critic for lp-do-fact-find, lp-do-analysis, lp-do-plan, lp-offer, and process/skill documents. Surfaces weak claims, missing evidence, hidden assumptions, feasibility gaps, and unaddressed risks with no glazing.
---

# Critique Document (Compact Hardnosed Mode)

Critique lp-do-fact-find, lp-do-analysis, lp-do-plan, lp-offer, or process/skill documents for decision quality.
No compliments, no filler, no vibe-based approval.

## Operating Mode

**CRITIQUE + AUTOFIX** — always. Full critique is produced first (Sections 1–11), then Concrete Fixes are applied to the target document (Autofix Phase), then a post-fix consistency scan runs on every edited section. The issues ledger is read at start and updated at end.

Allowed:
- Read target document and referenced docs/code/tests
- Search repo for verification
- Inspect git history for evidence
- Edit target document to apply Concrete Fixes
- Write/update issues ledger (`critique-history.md` adjacent to target doc)

Not allowed:
- Code changes to source files
- Commits
- Creating new docs other than `critique-history.md`

## Inputs

Required:
- Path to target doc

Supported targets:
- Planning docs (`docs/plans/*/fact-find.md`, `docs/plans/*/analysis.md`, `docs/plans/*/plan.md`)
- Domain plan docs (for example `docs/cms-plan/*.md`)
- Offer artifacts (`docs/business-os/strategy/*/*-offer.user.md` or similar)
- Process/skill docs (for example `.claude/skills/*/SKILL.md`)

Optional:
- Scope: `full` (default) or `focused`
- Context: extra constraints to pressure-test
- Prior critique reference (for delta scoring) — or read automatically from issues ledger if present

## Preflight Trust Policy

CI-gated linters pre-check some structural fields. Trust linter output rather than re-auditing; re-check only when a specific conflict with a higher-precedence doc is suspected.

**Trust and skip** (hard-fail in `plans-lint.ts` for lp-do-workflow plans at `docs/plans/*/plan.md`):
- `Domain`, `Last-reviewed`, `## Active tasks` section present
- `Execution-Track`, `Primary-Execution-Skill`, `Deliverable-Type`, `Feature-Slug`, `Workstream`
- IMPLEMENT task completeness: Confidence section, Validation contract (TC-/VC- reference), Acceptance criteria

**Still check** (warn-only or scoped — not authoritative gates):
- `Status` enum — docs-lint warns only, does not hard-fail
- Relates-to charter target validity — plans-lint warns only
- `Type` header — docs-lint has explicit exceptions; check if routing looks wrong

**Always check** (not covered by any linter):
- `Supporting-Skills`, `Overall-confidence`, `Confidence-Method`
- VC quality (isolated/pre-committed/time-boxed/diagnostic/repeatable/observable) and VC coverage ratio
- Confidence-gated markers coherence (if Confidence column in Task Summary → `Overall-confidence` must exist)

Note: plans-lint.ts planning-field checks apply only to `docs/plans/*/plan.md` (lp-do-workflow plans). For Fact-Find docs, linter coverage is minimal (Type header, Status warn-only) — all structural checks still apply.

## Auto-Detection and Schema Mode

Detection order:
1. If frontmatter `Type` is `Fact-Find`, `Analysis`, or `Plan` and structure is consistent, use Section A, B, or C.
2. Else if structure is consistent with planning docs, use Section A, B, or C (filename is supportive, not required).
3. Else if structure is consistent with offer docs, load `modules/offer-lens.md` (Offer schema mode).
4. Else use Section D (Process schema mode).

If `Type` conflicts with structure:
- Route by structure
- Downgrade confidence
- Record `Header/Structure override: Yes`

Structure consistency rubric (A/B/D routing):
- Fact-Find consistent if >=3 of 4 headings exist with substantive content:
  - `Scope` or `Scope & Intent`
  - `Evidence Audit` or `Evidence Audit (Current State)`
  - `Confidence Inputs` or `Confidence Assessment`
  - `Analysis Readiness` or `Planning Readiness`
- Analysis consistent if >=3 of 4 headings exist with substantive content:
  - `Decision Frame`
  - `Evaluation Criteria`
  - `Options Considered`
  - `Chosen Approach` or `Planning Handoff`
- Plan consistent if >=3 of 4 headings exist with substantive content:
  - `Summary` or `Overview`
  - `Task Summary` or `Task List`
  - `Tasks` or `Implementation Tasks`
  - `Risks & Mitigations` or `Risks and Mitigations`
- Offer consistent if >=3 of 4 headings exist with substantive content:
  - `ICP Segmentation` or `ICP`
  - `Pain/Promise Mapping` or `Pain` or `Promise`
  - `Offer Structure` or `Core Offer`
  - `Pricing` or `Pricing/Packaging`
- Substantive content means at least one concrete bullet, table row, or sentence with verifiable detail.

Schema modes:
- Current: aligns with current templates/policies
- Legacy: older/different schema
- Analysis: analysis artifacts
- Offer: offer artifacts (lp-offer output)
- Process: non Fact-Find/Analysis/Plan/Offer docs

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

## Issues Ledger

Path: `<plan-dir>/critique-history.md` for plan/fact-find targets (adjacent to the target doc); `<parent-dir>/critique-history.md` for other targets. Create on first critique run.

**At start:**
- Check if `critique-history.md` exists at the path above.
- If it does: read it and extract:
  - Confirmed-resolved issues → do not re-score as new findings; if they reappear, label as "regression" not "new".
  - Issues open for >1 round → elevate to priority review and note the round count in Top Issues.
- If it does not: proceed without prior context.

**At end:**
- Write or append a new round entry (see format below).

**Ledger format:**
```markdown
# Critique History: <feature-slug>

## Round N — YYYY-MM-DD

### Issues Opened This Round
| ID | Severity | Target | Summary |
|---|---|---|---|
| N-01 | Major | TASK-05 Notes | Contradictory delta tables |

### Issues Confirmed Resolved This Round
| Prior ID | Severity | Summary | How resolved |
|---|---|---|---|
| 2-01 | Major | Missing sort step | Sort added to TASK-05 Green step |

### Issues Carried Open (not yet resolved)
| Prior ID | Severity | Rounds Open | Summary |
|---|---|---|---|
| 2-02 | Moderate | 2 | buildCandidate signature gap |
```

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
4. Skill templates (`/lp-do-plan`, `/lp-do-fact-find`)
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

### Step 5a: Forward Rehearsal Trace

Load and follow: `../_shared/simulation-protocol.md`

After completing the checks above, run a forward rehearsal trace of the target document. Follow the Forward Rehearsal Trace Instructions defined in the shared protocol (Step 5a section).

In summary: identify the proposed execution sequence (task order for plans; investigation order for fact-finds; proposed implementation steps for other artifacts), apply the issue taxonomy to each step, classify findings by severity, and record findings inline within Step 5 output using the `[Rehearsal]` label.

Blocking-tier rehearsal findings (`Critical`, `Major`, or `Moderate`) must be surfaced in the Top Issues section (Section 2) and in the Fix List (Section 11). They do not trigger a separate hard gate in critique mode — that gate is defined in the shared rehearsal protocol and enforced in lp-do-plan and lp-do-fact-find. Rehearsal findings here are advisory to the critique score.

### Step 5b: Process Walkthrough Verification

For fact-finds, analyses, and plans that describe or imply a process/operating-model change, verify the process sections against repository evidence:
- `## Current Process Map`
- `## End-State Operating Model`
- `## Delivered Processes`

Rules:
- Each section must either be substantive or explicitly `None: <reason>`.
- When the document changes CI/deploy/release lanes, approvals, orchestration, lifecycle states, or multi-step operator flows, a missing or hand-wavy process section is Major.
- Reconstruct the process area by area and check trigger, step order, systems/owners, handoffs, end state, and unresolved issues against the code/docs.
- If the walkthrough contradicts the chosen approach, task graph, or current repo state, score it Major or Critical depending on blast radius.
- Record findings inline within Step 5 output using the `[Walkthrough]` label.

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

For fact-find artifacts, load `modules/fact-find-lens.md`. It contains required frontmatter and section checks, confidence dimension rules, and the fact-find minimum bar.

## Section B: Analysis Lens

For analysis artifacts, load `modules/analysis-lens.md`. It contains analysis frontmatter checks, minimum comparison requirements, recommendation quality checks, and planning-handoff requirements.

## Section C: Plan Lens

For plan artifacts, load `modules/plan-lens.md`. It contains plan frontmatter checks, confidence-gated marker rules, IMPLEMENT task structural requirements, VC quality checks, and agent-resolvable deferral checks.

## Section D: Process/Skill Lens

Required checks:
- Audience and decision/action are explicit
- Inputs/outputs/boundaries are explicit
- Allowed vs disallowed actions are explicit
- Escalation/exception paths are explicit
- No internal rule contradictions
- Output template enforces method steps
- Alignment with source-of-truth docs and legacy handling

## Section E: Offer Lens

For offer artifacts (lp-offer output), load `modules/offer-lens.md`. It contains required checks for all 6 lp-offer sections, Offer-Specific Quality Dimensions scoring weights, and Munger Inversion Attacks (Offer-Specific).

## Cross-Document Consistency (Analysis + Fact-Find, Plan + Analysis)

If an analysis references a fact-find:
- Compare goals, outcome contract, evidence limits, open questions, and risk transfer.

If a plan references an analysis:
- Compare goals, selected approach, open questions, confidence transitions, execution routing, and coverage gaps.
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
Schema mode: **Current / Legacy / Offer / Process**
Header/Structure override: **Yes/No** - <if yes, why>
Mode evidence: <matched headings/markers used for routing>

Biggest decision-quality failures: ...
Recommended action: **proceed** / **revise and re-critique** / **return to /lp-do-fact-find** / **run /lp-do-replan** / **revise process or skill doc and re-critique**

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

### 5) Feasibility, Execution Reality, and Rehearsal Trace

Prose output from Step 5 checks (code/mixed paths, dependency chain realism, failure points, effort honesty) and business-artifact checks (VC executability, falsification cost, approval paths, measurement infrastructure).

Forward rehearsal trace findings (from Step 5a) are written inline here with the `[Rehearsal]` label. Critical rehearsal findings are also surfaced in Section 2 (Top Issues) and Section 11 (Concrete Fixes).

Process walkthrough verification findings (from Step 5b) are written inline here with the `[Walkthrough]` label. Missing or contradictory walkthroughs for process-affecting work must also be surfaced in Section 2 (Top Issues) and Section 11 (Concrete Fixes).

### 6) Hidden Assumptions

| # | Assumption | Type | Fragility | Cheap Test |
|---|---|---|---|---|

### 7) Logic / Reasoning Faults

### 8) Contrarian Section

Include at least 3 distinct attacks.

### 9) Risks and Second-Order Effects

| Risk | Likelihood | Impact | Mitigation in Doc | Adequate? |
|---|---|---|---|---|

### 10) What Is Missing to Make This Decisionable

### 11) Concrete Fixes

Format:
- Fix -> Section -> Action

### 12) Scorecard (skip for `focused`)

| Dimension | Score | Justification |
|---|---|---|

Include:
- Weighted overall score
- Any severity cap applied
- Severity distribution summary (Critical/Major/Moderate/Minor counts)
- If prior critique exists: delta note (what changed and why)

## Autofix Phase

Runs after the critique output (Sections 1–12) is fully produced.

### Step AF-1: Section Rewrite Gate

Before applying any point edits, evaluate each affected named section (e.g., each IMPLEMENT task block in a plan):

- Count severity of issues targeting that section.
- If a single named section has **≥2 Major issues** OR **≥4 total issues** of any severity: trigger a **full section rewrite** instead of point edits.
  - Re-read the full existing section.
  - Produce a corrected replacement that incorporates all findings from the critique for that section.
  - Replace the entire section with a single write operation.
  - After the rewrite, run Step AF-3 (consistency scan) on the rewritten content before moving on.
- Sections below the rewrite threshold proceed to Step AF-2.

### Step AF-2: Point Fix Application

Apply each Concrete Fix in document order (top to bottom):

1. Before applying each fix: verify the exact target text still exists in the document. A prior fix in the same section may have superseded it; if so, skip this fix and note the skip.
2. Apply the edit using a targeted string replacement.
3. Do not re-read between individual fixes within the same section — accumulate all section edits, then scan at Step AF-3.

### Step AF-3: Post-Fix Consistency Scan (per affected section)

After all fixes for a section are applied (whether via rewrite or point edits), re-read the **full section** and check for:

- **Duplicate definitions**: two or more tables, bullet lists, or inline statements defining the same concept (e.g., two delta-value tables, two threshold constant definitions). Keep the version just introduced by the fix; remove the superseded one.
- **Orphaned terminology**: text using old names, old field names, old TC counts, or old threshold values that a fix just replaced. Update inline.
- **Numerical disagreement**: the same count, threshold, or identifier appears in two places with different values. Reconcile to the value the fix intended, or flag explicitly if ambiguous.
- **Cross-section drift**: a fix introduced a term or value that is also defined in an adjacent section (e.g., Notes, Acceptance criteria, Validation contract) with a different value. Check those adjacent sections and reconcile.

Apply cleanup edits for any stale or contradictory text found.

### Step AF-4: Issues Ledger Update

Write or append to `<plan-dir>/critique-history.md`:

- New round entry using the ledger format defined in the Issues Ledger section above.
- Mark this round's opened issues, confirmed-resolved prior issues, and carried-open prior issues.
- If `critique-history.md` does not exist: create it.

### Autofix Completion Message

After all steps, output:

> Autofix complete. Applied N fixes (M section rewrites, K point fixes). Consistency scan: P cleanup edits applied. Issues ledger updated at `<path>`. Remaining open issues: Q.

## Workflow Integration

Recommended next actions:
- Fact-find has major evidence gaps -> additional `/lp-do-fact-find`
- Analysis lacks a decisive recommendation -> revise `/lp-do-analysis`
- Fact-find confidence unjustified -> rework confidence with evidence
- Plan confidence inflation -> `/lp-do-replan`
- Plan missing validation contracts -> revise plan before `/lp-do-build`
- Plan contradicts lp-do-fact-find -> `/lp-do-replan` with lp-do-fact-find input
- Offer ICP too broad -> return to `/lp-offer` with narrower segmentation
- Offer pricing unjustified -> gather competitor/WTP data, then re-run `/lp-offer`
- Offer positioning generic -> research competitive alternatives, then revise positioning
- Offer objections incomplete -> conduct customer interviews or competitive research
- Offer risk reversals weak -> strengthen guarantees/trials before `/lp-forecast`
- Unresolved source conflict -> reconcile source docs, then re-critique
- Process/skill contradictions -> revise rules, then re-critique
- Document fundamentally sound -> proceed

## Quality Checks (Self-Audit)

**Critique output:**
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

**Autofix:**
- Section rewrite gate evaluated for every affected named section — rewrite triggered where threshold is met.
- Step AF-3 consistency scan run on every section that received edits (rewrite or point fix).
- Duplicate definitions and orphaned terminology removed, not just new content added.
- Point fixes verified for target-text existence before application; skipped fixes noted.
- Issues ledger updated at `critique-history.md` with this round's opened, resolved, and carried-open issues.

**Ledger (always):**
- `critique-history.md` read at start if present; prior resolved issues not re-scored as new.
- Issues open for >1 round flagged with round count in Top Issues.
