---
description: Context Optimization - Orchestrate RPI workflow TODO generation with interactive scoping
---

# Context Engineering: Optimization Orchestrator

When invoked, orchestrate context engineering optimization with interactive scoping:

## Process

1. **Interactive Scoping (if no --auto flag)**
   - Ask up to 4 multiple choice questions to define scope
   - Questions cover: optimization focus, codebase areas, enhancement types, priority order
   - Skip questions if --scope or --auto flag provided

2. **Context System Audit**
   - Analyze `.claude/` directory structure
   - Check workflow file coverage and accuracy
   - Verify index file completeness
   - Identify orphaned or outdated files
   - Assess agent and command coverage gaps

3. **Generate RPI TODO List**
   - Create actionable TODO with research, plan, implement phases
   - Save to `.claude/plans/active/context-optimization_plan.md`
   - Include specific commands for each task

4. **Redundant File Detection**
   - Find files not referenced by any index
   - Identify duplicate or overlapping content
   - Flag outdated files with stale line references
   - Report empty placeholder files

5. **Enhancement Recommendations**
   - Suggest new specialized agents based on codebase patterns
   - Recommend workflow commands for common tasks
   - Identify undocumented workflows needing documentation

## Scoping Questions (Max 4)

**Q1: Optimization Focus**
- A) Functionalize the entire context engineering system
- B) Update outdated documentation and line references
- C) Identify and remove redundant context files
- D) Discover enhancement opportunities (new agents/commands)

**Q2: Codebase Coverage**
- A) Core business logic
- B) API/External integrations
- C) Database/Data layer
- D) All areas equally

**Q3: Enhancement Preferences**
- A) New specialized agents for specific domains
- B) New workflow commands for common tasks
- C) Improved documentation structure
- D) Better cross-referencing and navigation

**Q4: TODO Priority Order**
- A) Quick wins first (< 30 min each)
- B) High impact first (regardless of effort)
- C) By workflow area (grouped logically)
- D) By dependency order (foundational first)

## Context Budget
- Target: 20% of 200k tokens (40k)
- Output: TODO checklist + recommendations

## Output
- TODO checklist saved to `.claude/plans/active/context-optimization_plan.md`
- Audit findings in `.claude/research/active/context-audit_research.md`

## Arguments
- `$ARGUMENTS` can include:
  - `--auto` - Use intelligent defaults, skip questions
  - `--scope documentation` - Focus on docs only
  - `--scope agents` - Focus on agent gaps
  - `--scope workflows` - Focus on workflow coverage
  - `--scope cleanup` - Focus on redundant file removal

## Next Steps
After completion, execute the generated TODO list:
1. `/rpi-research [first-research-task]`
2. `/rpi-plan [first-plan-task]`
3. `/rpi-implement [first-impl-task]`
4. `/validate-all`
