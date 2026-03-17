---
name: marketing-planning
description: Plan marketing strategies, campaigns, content calendars, and initiatives using proven frameworks (RACE, SOSTAC, STP). Activates marketing-research for data-driven insights.
license: MIT
---

# Marketing Planning

Create detailed marketing plans through market research, competitive analysis, strategy design, and actionable campaign documentation.

## Skill Invocation

**Before planning, activate:** `marketing-research` skill for market data, competitor insights, and audience analysis.

## When to Use

Use this skill when:
- Planning marketing campaigns and launches
- Creating content strategies and editorial calendars
- Developing brand positioning and messaging
- Designing customer acquisition funnels
- Building multi-channel marketing initiatives
- Evaluating marketing approach trade-offs

## Core Responsibilities & Rules

Focus on actionable marketing strategy and campaign planning.
**Be honest, be brutal, straight to the point, and be concise.**

### 1. Market Research
Load: `references/research-phase.md`
**Skip if:** Provided with market research reports

### 2. Brand & Context Understanding
Load: `references/brand-context.md`
**Skip if:** Provided with brand guidelines or strategy docs

### 3. Strategy Design
Load: `references/strategy-design.md`

### 4. Plan Creation & Organization
Load: `references/plan-organization.md`

### 5. Task Breakdown & Output Standards
Load: `references/output-standards.md`

## Workflow Process

1. **Initial Analysis** → Read brand docs, understand business context
2. **Research Phase** → Market, competitor, audience research
3. **Synthesis** → Analyze insights, identify positioning opportunities
4. **Strategy Phase** → Define positioning, channels, messaging
5. **Plan Documentation** → Write comprehensive marketing plan
6. **Review & Refine** → Ensure completeness, feasibility, brand alignment

## Output Requirements

- DO NOT execute campaigns - only create plans
- Respond with plan file path and summary
- Ensure self-contained plans with brand context
- Include creative concepts when clarifying approach
- Provide multiple options with trade-offs when appropriate
- Fully respect the `./docs/brand-guidelines.md` file.

**Plan Directory Structure**
```
plans/
└── {date}-campaign-name/
    ├── research/
    │   ├── market-analysis.md
    │   ├── competitor-audit.md
    │   └── audience-insights.md
    ├── reports/
    │   └── campaign-brief.md
    ├── plan.md
    ├── phase-XX-phase-name.md
    └── ...
```

## Active Plan State

Prevents version proliferation by tracking current working plan via session state.

### Active vs Suggested Plans

Check the `## Plan Context` section injected by hooks:
- **"Plan: {path}"** = Active plan, explicitly set via `set-active-plan.cjs` - use for reports
- **"Suggested: {path}"** = Branch-matched, hint only - do NOT auto-use
- **"Plan: none"** = No active plan

### Rules

1. **If "Plan:" shows a path**: Ask "Continue with existing plan? [Y/n]"
2. **If "Suggested:" shows a path**: Inform user, ask if they want to activate or create new
3. **If "Plan: none"**: Create new plan using naming from `## Naming` section
4. **Update on create**: Run `node .claude/scripts/set-active-plan.cjs {plan-dir}`

### Report Output Location

All agents writing reports MUST:
1. Check `Plan Context` section injected by hooks for `Reports Path`
2. Only `$CK_ACTIVE_PLAN` plans use plan-specific reports path
3. `$CK_SUGGESTED_PLAN` plans use default `plans/reports/` (not plan folder)
4. Use naming: `{date}-{agent}-{slug}.md`

**Important:** Suggested plans do NOT get plan-specific reports - this prevents pollution of old plan folders.

## Quality Standards

- Be thorough and specific about strategy
- Consider brand consistency and voice
- Research thoroughly when uncertain
- Address competitive differentiation
- Make plans detailed enough for marketing team execution
- Validate against brand guidelines

**Remember:** Plan quality determines campaign success. Be comprehensive and consider all marketing aspects.

