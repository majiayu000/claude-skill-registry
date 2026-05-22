---
name: review:pre-merge
description: Pre-merge review focusing on correctness, testing, security, refactor safety, and maintainability. Spawns the senior-review-specialist agent for thorough pre-merge analysis.
---

# Pre-Merge Code Review

Run a pre-merge review using 5 critical checklists via the senior-review-specialist agent.

## Instructions

Spawn the `senior-review-specialist` agent to perform this review.

## Checklists to Apply

Load and apply these review checklists:

- `commands/review/correctness.md` - Logic flaws, broken invariants, edge-case failures
- `commands/review/testing.md` - Test quality, coverage, reliability
- `commands/review/security.md` - Vulnerabilities, insecure defaults, missing controls
- `commands/review/refactor-safety.md` - Semantic drift, behavior equivalence
- `commands/review/maintainability.md` - Readability, change amplification

## Agent Instructions

The agent should:

1. **Get working tree changes**: Run `git diff` to see all changes
2. **For each changed file**:
   - Read the full file content
   - Go through each diff hunk
   - Apply the 5 checklists to the changes
   - Pay special attention to behavior-changing code
3. **Cross-reference related files**: Follow imports, check callers
4. **Verify test coverage**: Ensure changes are properly tested
5. **Find ALL issues**: This is the last line of defense before merge

## Output Format

Generate a pre-merge review report with:

- **Critical Issues**: Blocking problems (must fix before merge)
- **Warnings**: Should strongly consider addressing
- **Suggestions**: Post-merge improvements
- **Test Coverage**: Assessment of test coverage for changes
- **File Summary**: Issues per file with counts by severity
- **Overall Assessment**: Merge/Don't Merge recommendation with clear rationale
