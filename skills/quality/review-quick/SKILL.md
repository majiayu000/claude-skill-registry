---
name: review:quick
description: Quick code review focusing on correctness, style, DX, UX copy, and overengineering. Spawns the senior-review-specialist agent for focused analysis.
---

# Quick Code Review

Run a focused review using 5 essential checklists via the senior-review-specialist agent.

## Instructions

Spawn the `senior-review-specialist` agent to perform this review.

## Checklists to Apply

Load and apply these review checklists:

- `commands/review/correctness.md` - Logic flaws, broken invariants, edge-case failures
- `commands/review/style-consistency.md` - Codebase style, language idioms
- `commands/review/dx.md` - Developer experience, onboarding
- `commands/review/ux-copy.md` - User-facing text clarity, error recovery
- `commands/review/overengineering.md` - Unnecessary complexity, YAGNI violations

## Agent Instructions

The agent should:

1. **Get working tree changes**: Run `git diff` to see all changes
2. **For each changed file**:
   - Read the full file content
   - Go through each diff hunk
   - Apply the 5 checklists to the changes
   - Focus on quick wins and obvious issues
3. **Cross-reference related files**: Follow imports, check callers
4. **Find issues efficiently**: Balance thoroughness with speed

## Output Format

Generate a focused review report with:

- **Critical Issues**: Blocking problems (must fix)
- **Warnings**: Should address before merge
- **Suggestions**: Quick improvements
- **File Summary**: Issues per file with counts by severity
- **Overall Assessment**: Ship/Don't Ship recommendation
