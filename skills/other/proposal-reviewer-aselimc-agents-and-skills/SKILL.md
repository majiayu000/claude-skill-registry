---
name: proposal-reviewer
description: "Review technical project proposals for quality, overpromises, legal risk, and internal consistency. Use when the user asks to review, check, evaluate, or critique a project proposal, grant proposal, or any section thereof. Also use when asked to find overpromises, check for legally binding language, verify consistency between sections (objectives vs work packages vs deliverables vs budget), or assess proposal readiness for submission. Accepts proposals as docx, pdf, or plain text input."
---

# Technical Proposal Reviewer

Review technical project proposals for quality, consistency, overpromises, and legal risk. Produce actionable feedback the author can use to improve the proposal.

## Review Workflow

1. **Read the proposal** — Load the full document (use `docx` or `pdf` skill as needed)
2. **Assess structure** — Check all expected sections are present and properly ordered
3. **Check consistency** — Verify cross-references between objectives, WPs, deliverables, budget, and timeline
4. **Flag overpromises** — Identify language that oversells or makes unsupported claims
5. **Flag legal risk** — Identify language that could create binding obligations
6. **Evaluate content quality** — Assess depth, citations, and clarity per section
7. **Produce review report** — Structured feedback with severity levels

## Review Dimensions

### 1. Structural Completeness

Check that the proposal contains all standard sections. Missing sections should be flagged.

Expected sections (adapt to funding call):
- Abstract/Executive Summary
- State of the Art
- Objectives
- Methodology
- Work Plan / Work Packages
- Deliverables & Milestones
- Timeline
- Budget
- Risk Management
- Impact & Exploitation
- References

### 2. Internal Consistency

Cross-check these mappings:

| From | To | Check |
|------|----|-------|
| Objectives (O1..On) | Work Packages | Every objective covered by ≥1 WP |
| Work Packages | Objectives | Every WP maps to ≥1 objective |
| Tasks | Deliverables | Every deliverable traces to tasks |
| Deliverables | Timeline | Due dates within WP duration |
| Milestones | Timeline | Milestone dates on Gantt chart |
| Budget (effort) | WP effort tables | Person-months match |
| Partner roles | WP leads | Partners listed in WPs match consortium |

### 3. Overpromise Detection

Flag statements that claim more than the evidence supports:

**Red flags:**
- "Will achieve X" without feasibility evidence → suggest "Aims to achieve X"
- Benchmark numbers stated as guaranteed outcomes → suggest framing as targets
- Claims of "first ever", "unique", "revolutionary" without strong justification
- Objectives that exceed project scope/budget/timeline
- Impact claims disconnected from project outputs

**Suggested replacement patterns:**

| Overpromise | Suggested Alternative |
|-------------|----------------------|
| "will achieve 95% accuracy" | "targets 95% accuracy based on preliminary results showing 88%" |
| "will revolutionize" | "has the potential to significantly advance" |
| "guaranteed delivery" | "planned delivery, subject to milestone review" |
| "unique solution" | "novel approach that differs from existing methods in [specific way]" |
| "will solve the problem" | "addresses key aspects of the problem, specifically [X, Y]" |

### 4. Legal Risk Assessment

Flag language that could create enforceable obligations:

**High risk:**
- Unconditional commitments: "we will deliver", "we guarantee", "we commit to"
- Quantitative guarantees without caveats: "system will process 1M records/sec"
- IP transfer language without legal review
- Data sharing commitments that may conflict with GDPR or institutional policy
- Liability-implying language: "we accept responsibility for", "we ensure"

**Recommended mitigations:**
- Add "subject to" clauses for conditional commitments
- Frame deliverables as "planned" rather than "guaranteed"
- Add standard disclaimers for performance targets
- Flag IP and data clauses for legal counsel review

### 5. Content Quality

Per-section quality assessment:

| Section | Key Quality Criteria |
|---------|---------------------|
| Abstract | Self-contained, concise, compelling, no jargon |
| State of the Art | Recent citations, fair comparison, clear gap statement |
| Objectives | SMART criteria met, realistic scope |
| Methodology | Concrete approach, justification over alternatives, feasibility |
| Work Plan | Clear task breakdown, realistic effort, dependencies shown |
| Impact | Concrete exploitation paths, quantified where possible |
| Risks | Honest assessment, high-impact risks included, mitigations concrete |

## Output Format

Produce a structured review report:

```
# Proposal Review: [Project Title/Acronym]

## Summary Assessment
[2-3 sentence overall assessment]
Overall readiness: [Ready / Needs Minor Revisions / Needs Major Revisions / Not Ready]

## Critical Issues (must fix)
1. [Issue description] — [Location in document] — [Suggested fix]

## Major Issues (should fix)
1. [Issue description] — [Location in document] — [Suggested fix]

## Minor Issues (nice to fix)
1. [Issue description] — [Location in document] — [Suggested fix]

## Overpromise Flags
1. [Quoted text] → [Suggested alternative] — [Section]

## Legal Risk Flags
1. [Quoted text] → [Risk description] — [Recommended action]

## Consistency Issues
1. [Description of mismatch] — [Sections involved]

## Strengths
1. [What works well]

## Section-by-Section Notes
### [Section Name]
- [Specific feedback]
```

Save the review report to `data/output/` with naming: `review_<project_name>_<YYYYMMDD>.md`
