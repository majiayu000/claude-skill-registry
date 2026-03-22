---
name: review-prd
description: Review an existing PRD for completeness, quality, and anti-patterns when the user asks to review, critique, or check a PRD
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Read, Glob, Grep, Write
argument-hint: "[path to PRD or PRD name]"
read-only: false
destructive: false
idempotent: false
open-world: false
user-invocable: true
tags: review, product, quality
---

# Review PRD

## Overview

Critically review a Product Requirements Document for structural completeness, substantive quality, and common anti-patterns. A good review catches what the author missed, not what they formatted wrong.

## Workflow

1. **Locate the PRD** — If `$ARGUMENTS` is a file path, read it directly. If it is a name or keyword, search `.chalk/docs/product/` for matching PRD files. If multiple matches exist, list them and ask the user to pick one.

2. **Read product context** — Load `.chalk/docs/product/0_product_profile.md` and any JTBD docs to understand the product's goals, target users, and strategic direction. This context is needed to assess whether the PRD aligns with the product.

3. **Read engineering context** — Scan `.chalk/docs/engineering/` for architecture docs. This is needed to assess feasibility of what the PRD proposes.

4. **Run the review checklist** — Evaluate the PRD against every item in the Review Checklist below. For each item, assign one of: PASS, WARN, FAIL.

5. **Write detailed findings** — For every WARN or FAIL, explain specifically what is wrong and suggest a concrete fix. Do not just say "needs improvement" — say what the improvement is.

6. **Produce the review** — Either:
   - (a) Output the review as a response in the conversation, or
   - (b) If the user asks for a written review, save to `.chalk/docs/product/<n>_prd_review_<slug>.md`

7. **Summarize** — End with a verdict: Ready for Engineering, Needs Revisions (list the blockers), or Needs Rewrite (fundamental problems).

## Review Checklist

### Problem & Users

| # | Check | Criteria |
|---|-------|----------|
| 1 | Problem statement exists | There is a dedicated section articulating the user problem, not a system problem |
| 2 | Problem is user-centric | Written from the user's perspective, not "the system needs to..." |
| 3 | Links to JTBD or user research | References a known user need, not an internal assumption |
| 4 | Target users defined | Specific personas or user segments are named, not "all users" |
| 5 | Anti-personas identified | States who this is NOT for |

### Success Metrics

| # | Check | Criteria |
|---|-------|----------|
| 6 | Metrics exist | At least 2 success metrics are defined |
| 7 | Metrics are measurable | Each metric has a number or clear threshold, not "improve engagement" |
| 8 | Metrics are time-bound | Each metric specifies a measurement period |
| 9 | Baselines included | Current state is documented so improvement can be measured |
| 10 | Metrics connect to user outcomes | Metrics measure user value, not just system activity |

### User Stories & Acceptance Criteria

| # | Check | Criteria |
|---|-------|----------|
| 11 | User stories present | At least one user story in "As a / I want / So that" format |
| 12 | Stories have acceptance criteria | Every story has at least 1 Given/When/Then criterion |
| 13 | Acceptance criteria are testable | A QA engineer could write a test from each criterion without asking the PM for clarification |
| 14 | Feature-level acceptance criteria exist | There are overall completion criteria beyond individual stories |
| 15 | No stories that are really tasks | Stories describe user value, not implementation steps like "Set up database table" |

### Scope & Edge Cases

| # | Check | Criteria |
|---|-------|----------|
| 16 | Out of scope defined | There is an explicit out-of-scope section with specific exclusions |
| 17 | Edge cases enumerated | Error states, empty states, boundary conditions, and permission boundaries are covered |
| 18 | No contradictions | Out-of-scope items are not also described as in-scope elsewhere in the document |

### Dependencies & Risks

| # | Check | Criteria |
|---|-------|----------|
| 19 | Dependencies listed | Internal, external, and technical dependencies are identified |
| 20 | Open questions flagged | Unresolved items are explicitly listed with owners |
| 21 | Feasibility checked | Proposed solution is compatible with the current architecture |

### Writing Quality

| # | Check | Criteria |
|---|-------|----------|
| 22 | Problem-first structure | The document leads with the problem, not the solution |
| 23 | No vague language | Terms like "intuitive," "fast," "seamless" are replaced with specific, measurable descriptions |
| 24 | No feature-list syndrome | The PRD describes user outcomes, not just a list of features to build |
| 25 | Internally consistent | Metrics, stories, and acceptance criteria align with each other |

## Output

When writing a review doc:
- **File**: `.chalk/docs/product/<n>_prd_review_<slug>.md`
- **Format**: Plain markdown, no YAML frontmatter
- **First line**: `# PRD Review: <Feature Name>`
- **Second line**: `Last updated: <YYYY-MM-DD> (Initial review)`

Review doc structure:
```markdown
# PRD Review: <Feature Name>

Last updated: <YYYY-MM-DD> (Initial review)

## Verdict

[Ready for Engineering | Needs Revisions | Needs Rewrite]

## Summary

1-3 sentence assessment of the PRD's overall quality and readiness.

## Checklist Results

| # | Check | Result | Notes |
|---|-------|--------|-------|
| 1 | Problem statement exists | PASS/WARN/FAIL | ... |
| ... | ... | ... | ... |

## Critical Issues (FAIL)

### [Issue title]
**What's wrong**: ...
**Suggested fix**: ...

## Warnings (WARN)

### [Issue title]
**What's wrong**: ...
**Suggested fix**: ...

## Strengths

What the PRD does well. Reinforce good practices.
```

## Anti-patterns

- **Rubber-stamping** — Never approve a PRD just because it has the right section headings. A PRD with all sections filled but poor content is worse than a short PRD with honest gaps, because it creates false confidence.
- **Format-only reviews** — Checking that Given/When/Then syntax is correct while ignoring whether the criteria are actually testable is the most common review failure. Read each criterion and ask: "Could I write an automated test from this sentence alone?"
- **Not checking testability** — "The page loads quickly" passes a format check but fails a testability check. Push for "Given a user on a 3G connection, when they load the dashboard, then the first contentful paint occurs within 2 seconds."
- **Ignoring product context** — A PRD that conflicts with the product profile or duplicates an existing PRD is a structural problem, not a cosmetic one. Always cross-reference.
- **Suggestions without specifics** — "The metrics section needs work" is not actionable. Say "Metric 2 ('improve retention') needs a baseline (current: X%), a target (Y%), and a timeframe (within Z weeks of launch)."
- **Skipping the verdict** — Every review must end with a clear verdict. The author needs to know whether to proceed, revise, or start over.
