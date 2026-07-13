---
name: review
description: >
  Use when the user wants their code or PR reviewed before merging — runs
  parallel specialized reviews (code quality, plan compliance, change
  correctness) then synthesizes one verdict. Examples: "review this PR",
  "review my branch before I merge", "check this code before merge", "get
  feedback on this implementation", "is this ready to merge".
---

# /review - Code Review Workflow

Multi-perspective code review with parallel specialists.

## When to Use

- "Review this code"
- "Review my PR"
- "Check this before I merge"
- "Get feedback on implementation"
- Before merging significant changes
- Quality gates

## Workflow Overview

```
         ┌──────────┐
         │  critic  │ ─┐
         │ (code)   │  │
         └──────────┘  │
                       │
         ┌──────────┐  │      ┌──────────────┐
         │plan-reviewer│ ─┼────▶ │ review-agent │
         │ (plan)   │  │      │ (synthesis)  │
         └──────────┘  │      └──────────────┘
                       │
         ┌──────────┐  │
         │plan-reviewer│ ─┘
         │ (change) │
         └──────────┘

         Parallel                Sequential
         perspectives            synthesis
```

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "The code looks clean, ship it" | Clean code can still miss requirements entirely. Check spec compliance first. |
| "I'll combine spec and quality review" | Mixing concerns causes both to suffer. Separate passes catch more issues. |
| "Minor issues, not worth flagging" | Minor issues compound into major technical debt. Flag everything. |
| "The tests pass so it's fine" | Tests verify what was tested, not what was missed. Review the gaps. |
| "I trust this developer's code" | Trust doesn't replace verification. Review all code equally. |

## Review Stages

### Stage 1: Spec Compliance (MUST complete first)

**Agent:** critic
**Question:** Did it build what was asked?

- Compare implementation against requirements/plan/ticket
- Check every requirement is addressed
- Flag missing features, wrong behavior, or scope violations
- Verdict: PASS (all requirements met) or FAIL (gaps identified)

```
Task(
  subagent_type="critic",
  prompt="""
  Spec compliance review: [SCOPE]

  Compare implementation against requirements/plan/ticket.

  Check:
  - Every requirement is addressed
  - Behavior matches specification
  - No scope violations (extra or missing)
  - Edge cases from requirements are handled

  Output: PASS or FAIL with specific gaps listed
  """
)
```

<HARD-GATE>
Do NOT proceed to Stage 2 until Stage 1 passes.
If spec compliance fails, stop the review and report gaps.
Code quality is irrelevant if the wrong thing was built.
</HARD-GATE>

### Stage 2: Code Quality (only after Stage 1 passes)

**Agent:** judge
**Question:** Is it well-built?

- Code style, patterns, DRY, edge cases
- Error handling, security, performance
- Test coverage and test quality
- Maintainability and readability

Runs parallel sub-reviews, then synthesizes:

| # | Agent | Focus | Execution |
|---|-------|-------|-----------|
| 2a | **critic** | Code quality, patterns, readability | Parallel |
| 2a | **plan-reviewer** | Architecture, plan adherence | Parallel |
| 2a | **plan-reviewer** | Change impact, risk assessment | Parallel |
| 2b | **review-agent** | Synthesize all reviews, final verdict | After 2a |

```
# Code quality review
Task(
  subagent_type="critic",
  prompt="""
  Review code quality: [SCOPE]

  Evaluate:
  - Code style and consistency
  - Design patterns used
  - Readability and maintainability
  - Error handling
  - Test coverage

  Output: List of issues with severity (critical/major/minor)
  """,
  run_in_background=true
)

# Architecture review
Task(
  subagent_type="plan-reviewer",
  prompt="""
  Review architecture alignment: [SCOPE]

  Check:
  - Follows established patterns
  - Matches implementation plan (if exists)
  - Consistent with system design
  - No architectural violations

  Output: Alignment assessment with concerns
  """,
  run_in_background=true
)

# Change impact review
Task(
  subagent_type="plan-reviewer",
  prompt="""
  Review change impact: [SCOPE]

  Assess:
  - Risk level of changes
  - Affected systems/components
  - Backward compatibility
  - Potential regressions
  - Security implications

  Output: Risk assessment with recommendations
  """,
  run_in_background=true
)

# Wait for all parallel reviews
[Check TaskOutput for all three]
```

### Synthesis

```
Task(
  subagent_type="review-agent",
  prompt="""
  Synthesize reviews for: [SCOPE]

  Reviews:
  - critic: [code quality findings]
  - plan-reviewer: [architecture findings]
  - plan-reviewer: [change impact findings]

  Create final review:
  - Overall verdict (APPROVE / REQUEST_CHANGES / NEEDS_DISCUSSION)
  - Prioritized action items
  - Blocking vs non-blocking issues
  - Summary for PR description
  """
)
```

## Review Modes

### Full Review
```
User: /review
→ All four agents, comprehensive review
```

### Quick Review
```
User: /review --quick
→ critic only, fast feedback
```

### Security Focus
```
User: /review --security
→ Add aegis (security agent) to parallel phase
```

### PR Review
```
User: /review PR #123
→ Fetch PR diff, review changes
```

## Example

```
User: /review the authentication changes

Claude: Starting /review workflow...

Phase 1: Running parallel reviews...
┌────────────────────────────────────────────┐
│ critic: Reviewing code quality...          │
│ plan-reviewer: Checking architecture...         │
│ plan-reviewer: Assessing change impact...         │
└────────────────────────────────────────────┘

critic: Found 2 issues
- [minor] Inconsistent error messages in auth.ts
- [major] Missing input validation in login()

plan-reviewer: ✅ Matches authentication plan

plan-reviewer: Medium risk
- Affects: login, signup, password reset
- Breaking change: session token format

Phase 2: Synthesizing...

┌─────────────────────────────────────────────┐
│ Review Summary                              │
├─────────────────────────────────────────────┤
│ Verdict: REQUEST_CHANGES                    │
│                                             │
│ Blocking:                                   │
│ 1. Add input validation to login()          │
│                                             │
│ Non-blocking:                               │
│ 2. Standardize error messages               │
│                                             │
│ Notes:                                      │
│ - Document session token format change      │
│ - Consider migration path for existing      │
│   sessions                                  │
└─────────────────────────────────────────────┘
```

## Personal Standards

Before starting a review, load the user's engineering standards:
- Read `~/.claude/rules/engineering-standards.md`
- Apply severity calibration (CRITICAL/HIGH/MEDIUM/LOW)
- Reference specific standards when flagging issues

## Verdicts

- **APPROVE**: Ready to merge, all issues are minor
- **REQUEST_CHANGES**: Blocking issues must be fixed
- **NEEDS_DISCUSSION**: Architectural decisions need input
