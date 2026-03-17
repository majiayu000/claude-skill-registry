---
name: prd
description: Use when the user wants to write product requirements, define a feature spec, or create a PRD. Includes clarification, research, scoring, and plan-schema integration.
invocation: agent
---

# PRD Generator

Write a comprehensive Product Requirements Document for the given feature. Uses `plan-schema` skill as a structural foundation and extends with PRD-specific sections. Use `prd-schema` skill for structure validation and scoring criteria.

## PHASE 0: CLARIFICATION (MANDATORY)

Before writing ANY PRD content, ask the user:

```
I'll create a PRD for: **<feature>**

To make this PRD highly targeted, please answer briefly:

1. **Target Users**: Who will use this? (developers, end-users, admins, agencies?)
2. **Core Problem**: What pain point does this solve? Any metrics on current impact?
3. **Success Criteria**: How will you measure success? (KPIs, adoption rate, time saved?)
4. **Constraints**: Any technical, budget, timeline, or platform constraints?
5. **Existing Context**: Greenfield project or integrating with existing systems?

(Type "skip" to proceed with assumptions, or answer inline)
```

**WAIT for user response before proceeding.**

## PHASE 1: QUICK RESEARCH (Max 2 searches)

If topic is unfamiliar, do MAX 2 web searches:
- One for domain/market context
- One for technical patterns (only if needed)

Do NOT over-research. Move to writing quickly.

## PHASE 2: WRITE PRD

Write the PRD with these sections:

1. **Executive Summary** — vision + key value
2. **Problem Statement** — quantified, by user segment
3. **Goals & Metrics** — SMART, P0/P1/P2, success metrics table
4. **Non-Goals** — explicit boundaries
5. **User Personas** — 2-3 specific personas
6. **Functional Requirements** — FR-001 format, priority-ordered
7. **Implementation Phases** — dependency-ordered, maps to Arc plan phases
8. **Risks & Mitigations**

## PHASE 3: SELF-SCORE (100-point framework)

Score the PRD against:
- **AI-Specific Optimization**: 25 pts (structured for AI consumption, clear acceptance criteria)
- **Traditional PRD Core**: 25 pts (problem/solution clarity, stakeholder alignment)
- **Implementation Clarity**: 30 pts (phased plan, dependency order, exit criteria)
- **Completeness**: 20 pts (personas, non-goals, risks, metrics)

## PHASE 4: SAVE AND NEXT STEPS

Write to `openspec/plans/` with naming convention: `YY-MM-DD-prd-<feature-slug>-<hash5>.md`

Create the `openspec/plans/` directory if it doesn't exist.

```
## PRD Complete

**File**: openspec/plans/<filename>
**Score**: <N>/100
**Feature**: <feature name>

Next Steps:
1. Review the PRD
2. `/arc:core:plan` to create an implementation plan from this PRD
3. `/arc:core:spec` to generate OpenSpec artifacts
```
