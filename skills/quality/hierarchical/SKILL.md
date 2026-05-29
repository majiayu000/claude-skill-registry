---
name: hierarchical
user-invocable: true
description: Comprehensive multi-stage code review using specialized subagents
argument-hint: [files-or-directories]
allowed-tools: Task
---

# Hierarchical Code Review

## Context

- Current branch: !`git branch --show-current`
- Git status: !`git status --porcelain`
- Base branch: !`(git show-branch | grep '*' | grep -v "$(git rev-parse --abbrev-ref HEAD)" | head -1 | sed 's/.*\[\([^]]*\)\].*/\1/' | sed 's/\^.*//' 2>/dev/null) || echo "develop"`
- Changes since base: !`BASE=$(git merge-base HEAD develop 2>/dev/null || git merge-base HEAD main 2>/dev/null) && git log --oneline $BASE..HEAD`
- Files changed since base: !`BASE=$(git merge-base HEAD develop 2>/dev/null || git merge-base HEAD main 2>/dev/null) && git diff --name-only $BASE..HEAD`
- Test commands available: !`([ -f package.json ] && echo "npm/pnpm/yarn test") || ([ -f Cargo.toml ] && echo "cargo test") || ([ -f pyproject.toml ] && echo "pytest/uv run pytest") || ([ -f go.mod ] && echo "go test") || echo "no standard test framework detected"`

## Requirements

- Use **@tech-lead-reviewer** — architectural impact assessment — to scope architectural risk before launching specialized reviews.
- Run parallel reviews with:
  - **@code-reviewer** — logic correctness, tests, error handling.
  - **@security-reviewer** — authentication, data protection, validation.
  - **@ux-reviewer** — usability and accessibility (skip if purely backend/CLI).
- Consolidate findings by priority (Critical → High → Medium → Low) and confidence (High → Medium → Low).
- Offer optional implementation support and ensure commits follow Git conventions (详见 `skills/references/git-commit-conventions.md`).

## Your Task

**IMPORTANT: You MUST use the Task tool to complete ALL tasks.**

1. Perform a leadership assessment with **@tech-lead-reviewer** — architectural impact assessment — to map risk areas and determine which specialized agents to involve.
2. Launch the required specialized reviews in parallel via the Task tool, collect outcomes, and resolve conflicting feedback.
3. Present a consolidated report with prioritized recommendations, ask whether the user wants fixes implemented, and if so, execute optimizations and testing before summarizing results.

### Review Flow

- **Technical Leadership Assessment**: Evaluate architecture, technical debt, scalability, and maintainability impact.
- **Parallel Specialized Reviews**:
  - **@code-reviewer** — logic correctness, tests, error handling.
  - **@security-reviewer** — authentication, data protection, validation.
  - **@ux-reviewer** — usability and accessibility (skip if purely backend/CLI).
- **Consolidated Analysis**: Merge findings, prioritize by impact/confidence, and produce actionable improvements.
- **Optional Implementation**: Address security, quality, or UX issues as requested, then run tests and validations.
- **Final Optimization**: Engage **@code-simplifier** — code simplification and optimization — to refactor implemented fixes, remove redundancy, and verify compliance with SOLID principles before finalizing the summary.
