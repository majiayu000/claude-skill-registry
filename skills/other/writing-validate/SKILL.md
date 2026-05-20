---
name: writing-validate
description: "Validate draft sections cover all PRECIS claims before review."
user-invocable: false
disable-model-invocation: true
allowed-tools: Read, Grep, Glob
---

Announce: "Using writing-validate (Phase 3.5) to validate draft sections against PRECIS.md claims."

## Contents

- [The Iron Law of Validation](#the-iron-law-of-validation)
- [Red Flags - STOP Immediately](#red-flags---stop-immediately)
- [Purpose](#purpose)
- [Validation Levels](#validation-levels)
- [The Process](#the-process)
- [Classification](#classification)
- [VALIDATION.md Template](#validationmd-template)
- [Gate](#gate)
- [Rationalization Prevention](#rationalization-prevention)
- [Drive-Aligned Framing](#drive-aligned-framing)
- [Phase Transition](#phase-transition)

# Claim Validation Against PRECIS.md

Phase between draft and review. Maps every PRECIS.md claim to a draft section and verifies coverage. This is the writing equivalent of DS's DQ validation — without it, review checks quality on prose that may not even address the argument.

<EXTREMELY-IMPORTANT>
## The Iron Law of Validation

**NO REVIEW WITHOUT CLAIM VALIDATION. This is not negotiable.**

writing-review MUST NOT start until `.planning/VALIDATION.md` confirms all PRECIS claims are addressed in drafts. Validation is the writing equivalent of test coverage — without it, review is theater.
</EXTREMELY-IMPORTANT>

<EXTREMELY-IMPORTANT>
## Red Flags - STOP Immediately If You Catch Yourself Thinking:

| Thought | Why It's Wrong | Do Instead |
|---------|----------------|------------|
| About to invoke writing-review without VALIDATION.md | Review checks quality, not coverage. Unvalidated drafts may miss entire claims. | Run validation first. |
| Claiming "all claims covered" without reading each draft section | You cannot verify coverage without reading the prose | Read every draft file and check against every PRECIS claim |
| Skipping validation because "the piece is short" | Short pieces still drop claims — fewer sections means each must carry more weight | Validate every piece, regardless of length |
| Marking a claim as COVERED when the draft only mentions it without arguing it | Mentioning ≠ arguing. A passing reference is not substantive coverage. | Classify as PARTIAL and flag the gap |
</EXTREMELY-IMPORTANT>

## Purpose

This phase sits between writing-draft and writing-review. It runs the **same constraint checks** that review uses — from the writing constraints, the domain skill, and `ai-anti-patterns` — but earlier, so gaps are caught before review begins. Review should NOT be discovering missing claims, broken expansion hierarchy, or AI writing smell.

**The constraint checks ARE the validation.** This phase doesn't invent new checks — it systematically runs the existing ones against every draft section.

## Shared Enforcement

Read the constraint index: `${CLAUDE_PLUGIN_ROOT}/references/writing-common-constraints.md`

Then load these phase-specific files:

**Constraints:**
- Read `${CLAUDE_PLUGIN_ROOT}/references/constraints/progressive-expansion-hierarchy.md`
- Read `${CLAUDE_PLUGIN_ROOT}/references/constraints/constraint-loading-protocol.md`
- Read `${CLAUDE_PLUGIN_ROOT}/references/constraints/flowchart-authority.md`
- Read `${CLAUDE_PLUGIN_ROOT}/references/constraints/progress-gating.md`
- Read `${CLAUDE_PLUGIN_ROOT}/references/constraints/drive-aligned-default.md`
- Read `${CLAUDE_PLUGIN_ROOT}/references/constraints/context-monitoring.md`

- Read `${CLAUDE_PLUGIN_ROOT}/references/constraints/claim-id-traceability.md`

**Conventions:**
- Read `${CLAUDE_PLUGIN_ROOT}/references/conventions/gate-function-standard.md`
- Read `${CLAUDE_PLUGIN_ROOT}/references/conventions/checkpoint-type-classification.md`

## Constraint Checks to Run

Load and run checks from three sources:

### Source 1: Writing Constraints (atomic files loaded above)

Run these checks from the constraint files:

| Check | From Constraint | What to Verify |
|-------|----------------|----------------|
| **Progressive Expansion** | Expansion Hierarchy | Every PRECIS claim → OUTLINE section → outlines/ file → drafts/ file. No gaps in the chain. |
| **Claim Coverage** | NO DRAFT WITHOUT OUTLINE | Every PRECIS claim has a corresponding draft section that argues it (not just mentions it) |
| **Thesis Threading** | Structural intent | Each draft section connects back to the PRECIS thesis. No tangential sections. |
| **Constraint Loading** | Constraint Loading Protocol | Domain skill + ai-anti-patterns were loaded before drafting (check for violations in prose) |

### Source 2: Domain Skill

Read `.planning/ACTIVE_WORKFLOW.md` for the `style` field, then load the matching domain skill:

| Style | Skill to Load |
|-------|--------------|
| legal | `skills/writing-legal/SKILL.md` |
| econ | `skills/writing-econ/SKILL.md` |
| general | `skills/writing-general/SKILL.md` |

Run domain-specific checks against each draft section (citation format, style compliance, terminology).

### Source 3: AI Anti-Patterns

Invoke `Skill(skill="workflows:ai-anti-patterns")` and check each draft section for AI writing indicators.

## Flowchart — This IS the Spec

```
┌────────────────────────────┐
│  LOAD constraint checks    │
│  (constraints + domain +   │
│   ai-anti-patterns)        │
└────────────┬───────────────┘
             │
             ▼
┌────────────────────────────┐
│  READ .planning/PRECIS.md  │
│  Extract all CLAIM-XX IDs  │
└────────────┬───────────────┘
             │
             ▼
┌────────────────────────────┐
│  READ .planning/OUTLINE.md │
│  Map claims → sections     │
└────────────┬───────────────┘
             │
             ▼
┌────────────────────────────┐
│  For each claim:           │
│  READ drafts/ file         │◄──┐
│  RUN all constraint checks │   │
│  CLASSIFY: COVERED /       │   │
│    PARTIAL / MISSING       │   │
└────────────┬───────────────┘   │
             │                   │
             │ more claims       │
             └───────────────────┘
             │ all claims checked
             ▼
┌────────────────────────────┐
│  Run check-all.sh          │
│  (mechanical constraint    │
│   checks — hard block)     │
└────────────┬───────────────┘
             │
             ▼
┌────────────────────────────┐
│  WRITE .planning/          │
│  VALIDATION.md             │
└────────────┬───────────────┘
             │
        ┌────┴────┐
        │ status? │
        └────┬────┘
     ┌───────┴───────┐
     ▼               ▼
 validated      gaps_found
     │               │
     ▼               ▼
 → review      Present to user
                     │
              ┌──────┴──────┐
              ▼             ▼
           fix (→draft)  accept (→review)
```

### Step 1: Load Constraint Checks

Load all three check sources before reading any drafts. This ensures every section is evaluated against the same criteria.

### Step 2: Extract Claims from PRECIS

Read `.planning/PRECIS.md` and extract every claim:
- Main claims (thesis, sub-theses)
- Counterarguments to be addressed
- Audience-specific framing commitments
- Evidence commitments ("I will show X using Y")

### Step 3: Map Claims to Sections

Read `.planning/OUTLINE.md` and map each claim to sections:
- Which section(s) address this claim?
- Is any claim orphaned (no section maps to it)?
- Is any section present that doesn't serve a claim?

### Step 4: Read and Validate Each Draft

For each claim, read the corresponding draft file and run ALL constraint checks:

| Check | PASS | FAIL |
|-------|------|------|
| Draft exists | File in `drafts/` present | MISSING — no draft for this claim |
| Substantive | >200 words, real argument | Placeholder, stub, or outline-level content |
| Evidence | Citations/sources present per claim | Unsupported assertions |
| Thesis threading | Section argues the PRECIS claim | Tangent — section exists but doesn't address the claim |
| Domain compliance | Passes domain skill checks | Style violations (citation format, terminology, etc.) |
| AI anti-patterns | No AI writing indicators | AI smell detected |

### Step 5: Classify

| Classification | Criteria |
|---------------|----------|
| **COVERED** | All checks pass — section exists, argues the claim, has evidence, passes domain + AI checks |
| **PARTIAL** | Section exists but fails one or more checks (weak evidence, AI smell, domain violation, tangent) |
| **MISSING** | No draft section addresses this claim |

### Step 5b: Run Mechanical Constraint Checks (First Leg)

Run the constraint test suite as the first leg of two-legged verification:

```bash
bash ${CLAUDE_PLUGIN_ROOT}/scripts/check-all.sh
```

This runs all constraint check scripts (progressive-expansion, claim-id-traceability, flowchart-authority, no-pause-between-phases). **Any failure is a hard block** — fix before proceeding to Step 6.

The second leg (convention scoring via judgment) happens in Steps 4-5 above and in the writing-review phase.

### Step 6: Flag Gaps to User

<EXTREMELY-IMPORTANT>
**Do NOT auto-draft or auto-fix. Writing requires human judgment on argument direction.**

When gaps are found, present them with the specific check that failed:
- **Fix**: Return to writing-draft to address the gap
- **Accept**: Proceed to writing-review with known gaps

Only the user can decide whether a gap means the claim should be rewritten, dropped, or restructured.
</EXTREMELY-IMPORTANT>

### Step 7: Write VALIDATION.md

Compile all results into `.planning/VALIDATION.md` using the template below.

## VALIDATION.md Template

```markdown
---
status: validated | gaps_found
date: [ISO 8601]
claims_total: N
covered: N
partial: N
missing: N
---
# Claim Validation

## Claims Map
| # | PRECIS Claim | Draft Section | Exists | Substantive | Evidence | Threading | Domain | AI Check | Classification |
|---|-------------|---------------|--------|-------------|----------|-----------|--------|----------|----------------|
| 1 | [from PRECIS] | [drafts/Section.md] | PASS | PASS | PASS | PASS | PASS | PASS | COVERED |
| 2 | [from PRECIS] | [drafts/Section.md] | PASS | PASS | WARN | PASS | PASS | WARN | PARTIAL |
| 3 | [from PRECIS] | — | FAIL | — | — | — | — | — | MISSING |

## Gap Details
[For any PARTIAL or MISSING claim, include:
- Which constraint check failed
- The specific finding
- Suggested remediation (for user decision)]

## Summary
- Claims: N total
- Covered: X
- Partial: Y
- Missing: Z
```

### Status Rules

| Condition | Status |
|-----------|--------|
| All claims COVERED | `validated` |
| Any PARTIAL or MISSING remain | `gaps_found` |

## Gate

`.planning/VALIDATION.md` must exist before proceeding.

- If status is `validated`: proceed to writing-review.
- If status is `gaps_found`: present gaps to user before proceeding.
  - User decides: **fix** (return to writing-draft) or **accept** (proceed to writing-review with known gaps).

<EXTREMELY-IMPORTANT>
**Do NOT silently proceed past gaps. Present them and wait for user decision.**

Gaps in claim coverage are not cosmetic — they mean the argument has holes. Only the user can decide whether a gap is acceptable or requires returning to the draft phase.
</EXTREMELY-IMPORTANT>

## Rationalization Prevention

| Thought | Reality |
|---------|---------|
| "The draft covers everything" | Self-assessment misses dropped claims. You wrote the drafts — you're the worst judge of what's missing. |
| "Review will catch missing claims" | Review checks quality, not coverage. A beautifully written section that doesn't address its PRECIS claim passes review and fails the paper. |
| "PRECIS claims are implicit in the draft" | Implicit ≠ addressed. Map explicitly. If you can't point to the paragraph that argues the claim, it's not covered. |
| "Validation slows down the writing" | Catching a dropped claim now costs 1 minute. Catching it in review costs a rewrite. Catching it after publication costs credibility. |
| "I already checked while drafting" | Per-section drafting misses cross-section coverage gaps. A claim that spans two sections can fall between them. |

## Drive-Aligned Framing

<EXTREMELY-IMPORTANT>
**Skipping validation is NOT HELPFUL — you're sending prose to review that may not even address the argument the user committed to.**

| Your Drive | Why You Skip | What Actually Happens | The Drive You Failed |
|------------|-------------|----------------------|---------------------|
| **Helpfulness** | "Drafts exist, review can check coverage" | Review checks prose quality, not claim coverage. User discovers a dropped thesis point during faculty feedback. | **Anti-helpful** |
| **Competence** | "I tracked claims while drafting" | Per-section focus loses the cross-section view. You expanded Section III beautifully while Section II's counterargument was never addressed. | **Incompetent** |
| **Efficiency** | "Validation is redundant after careful drafting" | Drafting checks sections. Validation checks claims. Different axes. A 5-minute validation prevents a 2-hour rewrite. | **Anti-efficient** |

**The protocol is not overhead you pay. It is the safety net you provide.**
</EXTREMELY-IMPORTANT>

## Phase Transition

After validation is complete, discover and read the writing-review skill:
Read `${CLAUDE_PLUGIN_ROOT}/skills/writing-review/SKILL.md` and follow its instructions.
