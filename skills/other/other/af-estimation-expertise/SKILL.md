---
name: af-estimation-expertise
description: Use when estimating effort for tasks or features in hours, decomposed by functional area and role, with conversion to Linear story points.

# AgentFlow documentation fields
title: Estimation Expertise
created: 2026-02-06
updated: 2026-02-06
last_checked: 2026-02-06
tags: [skill, expertise, estimation, effort, story-points, linear, planning]
parent: ../README.md
related:
  - ../af-work-management-expertise/SKILL.md
  - ../af-linear-api-expertise/SKILL.md
  - ../af-refinement-process/SKILL.md
  - ../af-discovery-process/SKILL.md
---

# Estimation Expertise

## When to Use This Skill

Load this skill when you need to:
- Estimate effort for a Linear issue, feature, or mini-PRD
- Decompose work into functional areas and role-based effort
- Convert hour estimates to Linear story points
- Write a structured estimate into a Linear issue comment
- Review or refine existing estimates

**Common triggers:**
- During Refinement phase when refining effort estimates
- When creating or updating Linear features with story points
- When a PM or SE asks "how long will this take?"

## Quick Reference

### Constants

| Parameter | Value |
|-----------|-------|
| Productive hours per day | 6 |
| Hours per story point | 3 |
| Story point scale (fibonacci) | 0, 1, 2, 3, 5, 8, 13, 21, 34 |
| Maximum story points | 34 |

### Points-to-Hours Mapping

| Points | Hours | Days | Guideline |
|--------|-------|------|-----------|
| 0 | 0 | 0 | Trivial — config change, typo fix |
| 1 | 3 | 0.5 | Small — single-file change, simple bug fix |
| 2 | 6 | 1 | Moderate — a few files, straightforward logic |
| 3 | 9 | 1.5 | Medium — multiple files, some complexity |
| 5 | 15 | 2.5 | Large — cross-cutting change, new component |
| 8 | 24 | 4 | Very large — significant feature, ~1 week |
| 13 | 39 | 6.5 | Epic-sized — multi-component, ~1.5 weeks |
| 21 | 63 | 10.5 | Very epic — major system change, ~2 weeks |
| 34 | 102 | 17 | Maximum — consider decomposing further |

### Functional Areas

| Area | Abbreviation | Typical Work |
|------|-------------|--------------|
| Frontend | FE | UI components, pages, styling, client-side logic |
| Backend | BE | API endpoints, business logic, data models, Lambda |
| Infrastructure | INFRA | AWS setup, CI/CD, environments, DNS, secrets |
| Testing | TEST | Unit, integration, E2E tests, test infrastructure |
| Design | UX | Storybook stories, component specs, design tokens |
| Documentation | DOCS | Feature docs, API docs, README updates |

### Roles

| Role | Abbreviation | Primary Areas |
|------|-------------|---------------|
| Software Engineer | SE | FE, BE, INFRA, TEST |
| UX Designer | UX | UX, FE (component specs) |
| QA Engineer | QA | TEST (E2E, acceptance) |
| Product Manager | PM | DOCS (PRDs, requirements) |

---

## Parent and Sub-issue Estimation

### The Model

When a parent issue has specification sub-issues ([Behaviour], [UX]):

**Parent estimate = total effort** (specs + implementation)

**Sub-issue estimates = breakdown** of the parent total (not additions)

### Example

```
Issue: Login Flow (8 pts total)
  ├── [Behaviour] Login scenarios (2 pts) — part of the 8
  ├── [UX] Login Storybook (2 pts) — part of the 8
  └── Implementation (4 pts) — implicit remainder, not a sub-issue
```

### Velocity Calculation

When calculating velocity:
- Count the **parent issue points** (8 pts)
- Do NOT add sub-issue points on top (that would double-count to 12 pts)

Sub-issues exist for assignment and scheduling, not for inflating totals.

### Estimation Timing

**Discovery Estimate (on parent):**
- Created during Discovery phase
- Rough total for the whole capability (specs + implementation)
- Confidence: Low/Medium
- No sub-issues exist yet

**Refined Estimate (during Refinement):**
- Sub-issues created with individual estimates
- Parent estimate updated if scope changed during refinement
- Verify: parent estimate ≥ sum of sub-issue estimates
- Confidence: Medium/High

---

## Zero-Point Issues and Batching

### The Problem

The 1-point minimum (3 hours) includes overhead for code + test + docs. For trivial changes (typo fix, config tweak), this overhead is disproportionate and inflates velocity.

### The Solution

**For genuinely trivial changes:**
- Assign 0 points if it needs tracking
- Or batch into a "Housekeeping" parent issue

**For batches of trivial changes:**
- Create a "Housekeeping" or "Polish" parent issue
- Add trivial items as sub-issues (titles only, no individual estimates)
- Estimate the parent collectively (e.g., 2-3 points for 10-15 items)

### Example

```
Issue: Housekeeping — Week of Feb 10 (3 pts)
  ├── Sub-issue: Fix typo in login button
  ├── Sub-issue: Update copyright year in footer
  ├── Sub-issue: Remove unused import in auth.ts
  ├── Sub-issue: Add missing alt text to logo
  └── ... (10-15 trivial items)
```

### Decision Guide

| Situation | Approach |
|-----------|----------|
| Single trivial change, needs tracking | 0-point standalone issue |
| Single trivial change, no tracking needed | Just do it, no issue |
| Multiple trivial changes accumulating | Batch into Housekeeping parent |
| Small but non-trivial change | Normal 1-3 point issue |

### Avoid

- Estimating each trivial change at 1 point (inflates velocity)
- Creating issues for changes that don't need tracking
- Letting trivial changes accumulate without batching them

---

## Two-Tier Estimation

Estimation happens in two phases with increasing precision:

### Discovery Estimate (Feature-Level)

- **When:** During Discovery phase, when creating Linear features
- **Granularity:** Feature-level only (sub-issues don't exist yet)
- **Confidence:** Typically Low or Medium
- **Purpose:** Rough order-of-magnitude for planning and prioritisation
- **Tag:** `[Discovery Estimate]` in Linear comment

### Refined Estimate (Atomic with Roll-Up)

- **When:** During Refinement phase, after Behaviour scenarios and mini-PRD are written
- **Granularity:** Per sub-issue, with hours and points rolling up to the parent feature
- **Confidence:** Typically Medium or High
- **Purpose:** Detailed breakdown for sprint planning and delivery
- **Tag:** `[Refined Estimate]` in Linear comment

**Roll-up rule:** Both hours AND points roll up from sub-issues to the parent feature. Do not rely solely on Linear's points roll-up — explicitly track total hours in the parent feature's estimate comment and mini-PRD.

**Small feature exception:** Features estimated at 3 points or fewer can stay as a single issue without sub-issue decomposition.

---

## Rules

1. **Always decompose before estimating.** Never assign a single number without breaking work into functional areas first.
2. **Estimate in hours, convert to points.** Hours are the base unit. Convert to the nearest fibonacci point value using the mapping table.
3. **Round up to the next fibonacci value.** If total hours fall between two values, always round up (e.g., 20 hours rounds to 8 points, not 5).
4. **Issues over 34 points must be decomposed.** If an estimate exceeds 34 points, split the work into smaller issues.
5. **Include all functional areas.** Don't forget testing, documentation, and infrastructure — they are often 30-50% of total effort.
6. **Estimate for a single competent human.** Assume one person working at normal pace, not a team in parallel.
7. **State confidence level.** Every estimate must include a confidence indicator based on requirement clarity.
8. **Use the structured output format.** All estimates posted to Linear must use the standard format below.
9. **Roll up both hours and points.** When estimating sub-issues, always sum total hours in the parent feature — do not rely solely on Linear's points roll-up.
10. **Tag estimates by phase.** Use `[Discovery Estimate]` or `[Refined Estimate]` to differentiate in Linear comments.

---

## Workflow: Estimate a Task

**When:** You need to estimate a Linear issue or feature.

**Procedure:**

1. **Read the requirements.** Read the issue description, comments, mini-PRD, and any BDD scenarios. If requirements are vague, flag this in the confidence level.

2. **Identify functional areas.** List which areas are involved (FE, BE, INFRA, TEST, UX, DOCS). Not every task touches all areas.

3. **Estimate hours per area.** For each functional area, estimate the hours a single competent person would need:
   - What specific work is required?
   - What's the complexity? (new code vs. modification, known vs. unknown patterns)
   - Are there dependencies or integration points?

4. **Assign roles.** Map each functional area to the role that would do the work. Some areas may involve multiple roles.

5. **Sum total hours.** Add up all area estimates.

6. **Convert to points.** Find the nearest fibonacci value at or above the total hours using the mapping table.

7. **Assess confidence.** Rate confidence based on requirement clarity:
   - **High** — Clear requirements, BDD scenarios exist, known patterns
   - **Medium** — Refinement understood but some ambiguity, partially specified
   - **Low** — Vague requirements, unknown technical approach, significant unknowns

8. **Write the estimate.** Use the structured output format and post to the Linear issue.

---

## Workflow: Update Linear with Estimate

**When:** You have completed an estimate and need to record it.

**Procedure:**

1. **Set the story points on the issue:**
   ```bash
   curl -s -X POST https://api.linear.app/graphql \
     -H "Content-Type: application/json" \
     -H "Authorization: $LINEAR_API_KEY" \
     -d '{
       "query": "mutation { issueUpdate(id: \"ISSUE-ID\", input: { estimate: POINTS }) { success } }"
     }'
   ```

   Or via `linearis` if the CLI supports it in future versions.

2. **Post the detailed breakdown as a comment:**
   ```bash
   linearis issues comment ISSUE-ID "ESTIMATE_MARKDOWN"
   ```

---

## Structured Output Format

Use this format when posting estimates to Linear issue comments:

```markdown
## [Discovery Estimate] or [Refined Estimate]

**Total: X points (Y hours / Z days)**
**Confidence: High | Medium | Low**

### Breakdown

| Area | Work | Hours | Role |
|------|------|-------|------|
| FE | [description] | X | SE |
| BE | [description] | X | SE |
| TEST | [description] | X | SE/QA |
| DOCS | [description] | X | PM/SE |
| **Total** | | **X** | |

### Assumptions
- [Key assumption 1]
- [Key assumption 2]

### Risks
- [Risk that could increase estimate]
```

### Example: Discovery Estimate (Feature-Level)

```markdown
## [Discovery Estimate]

**Total: 8 points (24 hours / 4 days)**
**Confidence: Medium**

### Breakdown

| Area | Work | Hours | Role |
|------|------|-------|------|
| BE | Auth API endpoints, JWT middleware, user model | 8 | SE |
| FE | Login page, auth context, protected routes | 6 | SE |
| INFRA | Cognito setup, env vars, CORS | 2 | SE |
| TEST | Unit + E2E tests | 5 | SE/QA |
| DOCS | Auth flow docs, API docs | 2 | SE |
| UX | Login form Storybook story | 1 | UX |
| **Total** | | **24** | |

### Assumptions
- Using AWS Cognito (not custom auth)
- Email/password auth only (no social login)

### Risks
- Cognito config complexity could add 4-8 hours
```

### Example: Refined Estimate (Atomic with Roll-Up)

```markdown
## [Refined Estimate]

**Feature Total: 10 points (30 hours / 5 days)**
**Confidence: High**

### Sub-Issue Breakdown

| Sub-Issue | Area | Hours | Points |
|-----------|------|-------|--------|
| AF-50a: Backend API + data model | BE | 9 | 3 |
| AF-50b: Frontend UI components | FE, UX | 9 | 3 |
| AF-50c: E2E tests + integration | TEST | 6 | 2 |
| AF-50d: Documentation + infra | DOCS, INFRA | 6 | 2 |
| **Total** | | **30** | **10** |

### Change from Discovery
- Discovery estimate: 8 points (24 hours)
- Refined estimate: 10 points (30 hours)
- Reason: BDD scenarios revealed additional error handling and edge cases

### Assumptions
- Using AWS Cognito (not custom auth)
- Email/password auth only (no social login)
- SSO not required

### Risks
- Cognito configuration complexity could add 4-8 hours
```

---

## Estimation Heuristics

Use these rules of thumb when detailed decomposition isn't practical:

### By Change Type

| Change Type | Typical Points | Notes |
|-------------|---------------|-------|
| Config/typo fix | 0 | No testing impact |
| Single bug fix | 1-2 | Depends on diagnosis time |
| Simple UI change | 1-2 | Styling, copy, layout tweaks |
| New API endpoint | 2-3 | CRUD with tests |
| New UI component | 2-3 | With Storybook + tests |
| New page/feature | 5-8 | FE + BE + tests + docs |
| Cross-cutting refactor | 5-13 | Depends on blast radius |
| New integration | 8-13 | External API, error handling, tests |
| New system/service | 13-34 | Consider decomposing |

### Testing Multiplier

Testing typically adds 30-50% to implementation time:

| Implementation Hours | Add for Testing |
|---------------------|----------------|
| 1-3 | +1-2 hours |
| 4-8 | +2-4 hours |
| 9-15 | +4-8 hours |
| 16+ | +8-12 hours |

### Documentation Overhead

| Scope | Documentation Hours |
|-------|-------------------|
| Bug fix | 0-1 |
| Small feature | 1-2 |
| Major feature | 2-4 |
| New system | 4-8 |

---

## Common Pitfalls

1. **Forgetting testing effort.** Testing is 30-50% of total work. Always include TEST in your breakdown.
2. **Ignoring infrastructure.** New features often need env vars, CI changes, or AWS resources.
3. **Underestimating integration.** Connecting to external APIs or services takes longer than expected.
4. **Not accounting for review cycles.** Code review and feedback rounds add time. Include 1-2 hours for non-trivial PRs.
5. **Estimating for the best case.** Estimate for normal pace, not "if everything goes perfectly."
6. **Skipping documentation.** Docs are part of "done." Include them in every estimate.
7. **Over-precision in large estimates.** A 34-point issue doesn't need hour-level precision — focus on getting the right order of magnitude and flag that it should be decomposed.
8. **Estimating Epic parents that have estimated children.** When an issue is labelled "Epic" and has sub-issues that carry estimates, the parent should have estimate = 0. Carrying estimates on both parent and children causes double-counting in project totals. Always check: does this issue have estimated children? If so, zero the parent estimate.
9. **Missing delivery by-products.** Issues created during delivery as follow-on work ("what's left to do" breakdowns) bypass the estimation workflow. These need an estimation sweep — either via a recurring task (like AGV-85) or as part of cycle planning.
10. **Not checking for overlapping scope.** Before estimating, check if the issue's scope overlaps with existing issues. If two issues cover the same work, one should be marked as a duplicate or made a sub-issue of the other. Estimating both inflates the project total.

---

## Integration Points

**Discovery phase** (af-discovery-process):
- Feature-level estimates when creating Linear features in Phase 4
- Tag as `[Discovery Estimate]` in Linear comment
- Set story points on the feature issue directly
- Confidence is typically Low or Medium

**Refinement phase** (af-refinement-process):
- Refined estimates after Behaviour scenarios and mini-PRD are complete
- Tag as `[Refined Estimate]` in Linear comment
- For features > 3 points: create specification sub-issues ([Behaviour], [UX]) with individual estimates
- Sub-issue estimates are a breakdown of the parent total (not additions)
- Hours AND points roll up to the parent feature
- Document final estimate in mini-PRD Section 7 (Effort Estimation)
- Story points must be set before moving to "Approved"

**Mini-PRD** (templates/mini-prd-template.md):
- Section 7 captures the refined estimate with full breakdown
- Becomes the permanent record of how the estimate was calculated

**Work management** (af-work-management-expertise):
- Story points drive sprint planning and velocity tracking
- Use `issueUpdate` mutation to set `estimate` field on Linear issues

**Linear API** (af-linear-api-expertise):
- Set estimates via GraphQL: `issueUpdate(id: "...", input: { estimate: N })`
- Query estimates: `issue(id: "...") { estimate }`

**Database** (agents.db `tasks` table):
- After producing an estimate, persist it to the `tasks` table
- Discovery estimates: update `discovery_points`, `discovery_hours`, `discovery_confidence`, `discovery_breakdown`
- Refined estimates: update `refined_points`, `refined_hours`, `refined_confidence`, `refined_breakdown`
- Use this command after each estimate:

```bash
sqlite3 /var/lib/claude-agents/agents.db "
  INSERT INTO tasks (issue_id, issue_title, project, team_key, created_at, updated_at)
  VALUES ('<ISSUE_ID>', '<TITLE>', '<PROJECT>', '<TEAM_KEY>', datetime('now'), datetime('now'))
  ON CONFLICT(issue_id) DO UPDATE SET updated_at = datetime('now');

  UPDATE tasks SET
    discovery_points = <POINTS>,
    discovery_hours = <HOURS>,
    discovery_confidence = '<CONFIDENCE>',
    discovery_breakdown = '<JSON_BREAKDOWN>',
    discovery_estimated_at = datetime('now'),
    updated_at = datetime('now')
  WHERE issue_id = '<ISSUE_ID>';
"
```

For refined estimates, replace `discovery_*` columns with `refined_*`.

---

**Remember:**
1. Decompose first, estimate second — never guess a single number
2. Hours are the base unit, points are for Linear
3. 1 point = 3 hours = half a productive day
4. Always include testing, docs, and infrastructure
5. Round up to the next fibonacci value, never down
6. Roll up BOTH hours and points from sub-issues to parent feature
7. Tag estimates: `[Discovery Estimate]` or `[Refined Estimate]`
8. Persist estimates to the `tasks` table in agents.db after setting on Linear
