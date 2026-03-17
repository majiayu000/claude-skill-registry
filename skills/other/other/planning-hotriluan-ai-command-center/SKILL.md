---
name: planning
description: Use when you need to plan technical solutions that are scalable, secure, and maintainable.
license: MIT
---

# Planning

Create detailed technical implementation plans through research, codebase analysis, solution design, and comprehensive documentation.

## When to Use

Use this skill when:
- Planning new feature implementations
- Architecting system designs
- Evaluating technical approaches
- Creating implementation roadmaps
- Breaking down complex requirements
- Assessing technical trade-offs

## Core Responsibilities & Rules

Always honoring **YAGNI**, **KISS**, and **DRY** principles.
**Be honest, be brutal, straight to the point, and be concise.**

### 1. Research & Analysis
Load: `references/research-phase.md`
**Skip if:** Provided with researcher reports

### 2. Codebase Understanding
Load: `references/codebase-understanding.md`
**Skip if:** Provided with scout reports

### 3. Solution Design
Load: `references/solution-design.md`

### 4. Plan Creation & Organization
Load: `references/plan-organization.md`

### 5. Task Breakdown & Output Standards
Load: `references/output-standards.md`

## Workflow Process

1. **Initial Analysis** → Read codebase docs, understand context
2. **Research Phase** → Spawn researchers, investigate approaches
3. **Synthesis** → Analyze reports, identify optimal solution
4. **Design Phase** → Create architecture, implementation design
5. **Plan Documentation** → Write comprehensive plan
6. **Review & Refine** → Ensure completeness, clarity, actionability

## Output Requirements

- DO NOT implement code - only create plans
- Respond with plan file path and summary
- Ensure self-contained plans with necessary context
- Include code snippets/pseudocode when clarifying
- Provide multiple options with trade-offs when appropriate
- Fully respect the `./docs/development-rules.md` file.

**Plan Directory Structure**
```
plans/
└── {date}-plan-name/
    ├── research/
    │   ├── researcher-XX-report.md
    │   └── ...
    ├── reports/
    │   ├── XX-report.md
    │   └── ...
    ├── scout/
    │   ├── scout-XX-report.md
    │   └── ...
    ├── plan.md
    ├── phase-XX-phase-name-here.md
    └── ...
```

## Active Plan State

Prevents version proliferation by tracking current working plan via session state.

### Active vs Suggested Plans

| Type | Env Var | Meaning |
|------|---------|---------|
| **Active** | `$CK_ACTIVE_PLAN` | Explicitly set via `set-active-plan.cjs` - use for reports |
| **Suggested** | `$CK_SUGGESTED_PLAN` | Branch-matched, hint only - do NOT auto-use |

### How It Works

Plan context is managed through:
1. **`$CK_ACTIVE_PLAN` env var**: Only set for explicitly activated plans (via session state)
2. **`$CK_SUGGESTED_PLAN` env var**: Branch-matched plans shown as hints, not directives
3. **Session temp file**: `/tmp/ck-session-{id}.json` stores explicit activations only
4. **SubagentStart hook**: Injects differentiated context (Active vs Suggested)

### Rules

1. **Check `$CK_ACTIVE_PLAN` first**: If set and valid directory, ask "Continue with existing plan? [Y/n]"
2. **Check `$CK_SUGGESTED_PLAN` second**: If set, inform user "Found suggested plan from branch: {path}"
   - This is a hint only - do NOT auto-use it
   - Ask user if they want to activate it or create new
3. **If neither set**: Proceed to create new plan
4. **Update on create**: Run `node .claude/scripts/set-active-plan.cjs plans/...`

### Report Output Location

All agents writing reports MUST:
1. Check `Plan Context` section injected by hooks for `Reports Path`
2. Only `$CK_ACTIVE_PLAN` plans use plan-specific reports path
3. `$CK_SUGGESTED_PLAN` plans use default `plans/reports/` (not plan folder)
4. Use naming: `{agent}-{date}-{slug}.md`

**Important:** Suggested plans do NOT get plan-specific reports - this prevents pollution of old plan folders.

## Quality Standards

- Be thorough and specific
- Consider long-term maintainability
- Research thoroughly when uncertain
- Address security and performance concerns
- Make plans detailed enough for junior developers
- Validate against existing codebase patterns

**Remember:** Plan quality determines implementation success. Be comprehensive and consider all solution aspects.
