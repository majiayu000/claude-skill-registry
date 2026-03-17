---
name: strategic-planner
description: Interview-based strategic planning for complex software tasks. Conducts structured requirements gathering, gap analysis, and generates detailed work plans before implementation begins.
---

# Strategic Planner

An intelligent interviewer that helps think through complex software tasks before writing code. Separates planning from execution to prevent cognitive drift and scope creep.

## When to Use This Skill

- Multi-day or multi-step implementation projects
- Critical production changes requiring careful planning
- Complex refactoring with behavior preservation needs
- Any task where "just start coding" leads to rework

## What This Skill Does

### Phase 1: Interview — Requirements Gathering

Adapt interview style based on intent:

| Intent | Focus | Example Questions |
|--------|-------|-------------------|
| Refactoring | Safety — behavior preservation | "What tests verify current behavior?" "Rollback strategy?" |
| Build from Scratch | Discovery — patterns first | "Found pattern X in codebase. Follow it or deviate?" |
| Mid-sized Task | Guardrails — exact boundaries | "What must NOT be included? Hard constraints?" |
| Architecture | Strategic — long-term impact | "Expected lifespan? Scale requirements?" |

**Clearance check after each response:**
- Core objective defined?
- Scope boundaries established?
- No critical ambiguities?
- Technical approach decided?
- Test strategy confirmed?

Continue interviewing until all checks pass. Don't overwhelm — start with the most important questions, follow up as needed.

### Phase 2: Gap Analysis

Before writing the plan, catch what the interview missed:

- Hidden intentions in the user's request
- Ambiguities that could derail implementation
- Over-engineering or scope creep tendencies
- Missing acceptance criteria
- Edge cases not addressed

The plan author has "working memory ADHD" — makes connections that never make it onto the page. Gap analysis forces externalization of implicit knowledge.

### Phase 3: Plan Generation

Write a structured plan with:

1. **Objective** — One sentence, crystal clear
2. **Scope** — What's in, what's explicitly out
3. **Tasks** — Ordered, each with:
   - Description of what to do
   - Files to read/modify (specific paths)
   - Acceptance criteria (concrete, measurable)
   - Dependencies on other tasks
4. **Test Strategy** — How to verify each task
5. **Risks** — Known unknowns and mitigation

### Phase 4: Plan Review (Optional, High-Accuracy Mode)

Validate the plan against four criteria:

1. **Clarity**: Does each task specify WHERE to find implementation details?
2. **Verification**: Are acceptance criteria concrete and measurable?
3. **Context**: Sufficient context to proceed without >10% guesswork?
4. **Completeness**: Purpose, background, and workflow clear?

Approval requires:
- 100% of file references verified
- >=80% of tasks have clear reference sources
- >=90% of tasks have concrete acceptance criteria
- Zero tasks requiring assumptions about business logic

If rejected, fix issues and resubmit. No maximum retry limit.

## Example

**User**: "I want to refactor the auth system to support OAuth"

**Interview output**:
```
Q: What OAuth providers need support? → Google + GitHub
Q: Keep existing password auth? → Yes, alongside OAuth
Q: What tests exist for current auth? → Unit tests in tests/auth/
Q: Rollback strategy? → Feature flag, disable OAuth without removing code
```

**Plan output**: 6 tasks with specific file paths, acceptance criteria, dependency ordering, and test strategy.

## Tips

- Don't skip the interview — even 3 questions prevent major rework
- Plans are living documents — update as you learn during implementation
- The gap analysis step catches 30-40% of issues that interviews miss
- High-accuracy review mode is worth the time for production-critical changes

**Inspired by:** [oh-my-opencode](https://github.com/code-yeongyu/oh-my-opencode) Prometheus planning agent
