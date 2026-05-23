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
└── YYYYMMDD-HHmm-plan-name/
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

Prevents version proliferation by tracking current working plan.

### State File
`<WORKING-DIR>/.claude/active-plan` - Single line containing path to current plan folder.

`<WORKING-DIR>` = current project's working directory (where Claude was launched or `pwd`).

**Example content:**
```
plans/20251128-1654-fix-agent-coordination
```

### Rules

1. **Check first**: Before creating plan, check if `<WORKING-DIR>/.claude/active-plan` exists
2. **Validate path**: If exists, verify the path is a valid directory
3. **Prompt user**: If valid, ask "Continue with existing plan? [Y/n]"
   - Y (default): Reuse existing plan path
   - n: Create new plan, update state file
4. **Set on create**: When creating new plan, write path to `<WORKING-DIR>/.claude/active-plan`
5. **Reset**: User can delete file manually (`rm .claude/active-plan`) to start fresh

### Report Output Location

All agents writing reports MUST:
1. Read `<WORKING-DIR>/.claude/active-plan` to get current plan path
2. Write reports to `{plan-path}/reports/`
3. Use naming: `{agent}-{YYMMDD}-{slug}.md`

**Fallback:** If no active-plan file exists, use `plans/reports/`

## Quality Standards

- Be thorough and specific
- Consider long-term maintainability
- Research thoroughly when uncertain
- Address security and performance concerns
- Make plans detailed enough for junior developers
- Validate against existing codebase patterns

**Remember:** Plan quality determines implementation success. Be comprehensive and consider all solution aspects.
