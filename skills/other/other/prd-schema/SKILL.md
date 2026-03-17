---
name: prd-schema
description: Use when validating PRD structure, scoring PRD quality, or ensuring product requirements meet the 100-point framework.
invocation: agent
---

# PRD Schema

Defines the required structure for PRDs created by `/arc:specialized:prd`. PRDs extend Arc's `plan-schema` with product-specific sections.

## PRD Structure

### Required Sections

1. **Executive Summary** — Vision statement and key value proposition (2-4 sentences)
2. **Problem Statement** — Quantified by user segment, with current impact metrics
3. **Goals & Metrics** — SMART goals organized by P0/P1/P2 priority with success metrics table
4. **Non-Goals** — Explicit boundaries of what is NOT included
5. **User Personas** — 2-3 evidence-based personas with goals, frustrations, behaviors
6. **Functional Requirements** — Numbered FR-001 format, priority-ordered, with acceptance criteria
7. **Implementation Phases** — Dependency-ordered phases mapping to Arc plan structure
8. **Risks & Mitigations** — Risk matrix with likelihood, impact, and mitigation strategy

### Optional Sections

- **Technical Architecture** — High-level system design if relevant
- **Data Requirements** — Data models, storage, privacy considerations
- **Integration Points** — External systems and API dependencies
- **Accessibility Requirements** — WCAG compliance targets
- **Internationalization** — Language and locale requirements

## Scoring Framework (100 points)

### AI-Specific Optimization (25 pts)
- Structured for AI consumption (clear headings, numbered requirements)
- Machine-parseable acceptance criteria (Given/When/Then or equivalent)
- Unambiguous language (no "should consider" — use "must" or "must not")
- Compatible with Arc plan-schema for downstream conversion

### Traditional PRD Core (25 pts)
- Clear problem/solution articulation
- Stakeholder alignment (personas, non-goals)
- Market/user context with evidence
- Measurable success criteria

### Implementation Clarity (30 pts)
- Phased implementation plan with dependency order
- Exit criteria per phase
- Risk identification with mitigations
- Integration with Arc workflow (plan → spec → beads)

### Completeness (20 pts)
- All required sections present and populated
- Personas with behavioral detail (not demographics-only)
- Non-goals explicitly stated
- Metrics with baselines and targets

## Scoring Thresholds

- **90-100**: Production-ready, can proceed directly to `/arc:core:plan`
- **70-89**: Good, minor gaps to address before planning
- **50-69**: Needs revision, significant sections incomplete
- **Below 50**: Major rework needed, return to clarification phase

## Output Location

PRDs are written to `openspec/plans/` with naming: `YY-MM-DD-prd-<feature-slug>-<hash5>.md`

## Integration with Arc Workflow

```
/arc:specialized:prd <feature>
    ↓ writes
openspec/plans/YY-MM-DD-prd-<slug>-<hash5>.md
    ↓ consumed by
/arc:core:plan (creates implementation plan from PRD)
    ↓ continues
/arc:core:spec → /arc:core:beads → /arc:core:execute
```

## Validation

When reviewing a PRD, check:
- All required sections present
- FR numbers are sequential and unique
- Phases are dependency-ordered
- Acceptance criteria are testable (not vague)
- Non-goals don't contradict goals
- Personas are evidence-based (not assumed)
- Score >= 70 before proceeding to `/arc:core:plan`
