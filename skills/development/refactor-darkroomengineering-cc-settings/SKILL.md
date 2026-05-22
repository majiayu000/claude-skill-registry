---
name: refactor
description: |
  Code refactoring workflow. Use when:
  - User says "refactor", "clean up", "reorganize", "restructure"
  - Code needs improvement without changing behavior
  - User wants to improve code quality, readability, or performance
  - Technical debt needs addressing
context: fork
---

# Refactoring Workflow

You are in **Maestro orchestration mode**. Delegate immediately.

## Workflow

1. **Explore** - Spawn `explore` agent to analyze current code
2. **Plan** - Spawn `planner` agent to design refactoring approach
3. **Implement** - Spawn `implementer` agent to refactor
4. **Test** - Spawn `tester` agent to verify behavior unchanged
5. **Review** - Spawn `reviewer` agent to check quality
6. **Learn** - Store patterns discovered during refactoring

## Agent Delegation

```
Task(explore, "Analyze the code to refactor: $ARGUMENTS. Identify patterns, issues, dependencies.")
Task(planner, "Design refactoring approach based on analysis. Keep behavior unchanged.")
Task(implementer, "Refactor according to plan. Preserve all functionality.")
Task(tester, "Verify refactored code behaves identically to original.")
Task(reviewer, "Review refactoring for quality and completeness.")
```

## Refactoring Principles

1. **Preserve behavior** - Tests should pass before AND after
2. **Small steps** - Make incremental changes
3. **Run tests often** - Verify after each change
4. **Document decisions** - Explain WHY, not just WHAT

## Common Refactoring Tasks

- Extract component/hook
- Simplify complex logic
- Remove duplication
- Improve naming
- Split large files
- Optimize performance

## Output

Return a summary:
- **What changed**: Brief description
- **Files modified**: List of files
- **Tests passing**: Verification status
- **Improvements**: What's better now
- **Learnings**: Patterns worth remembering
