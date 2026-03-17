---
name: code-review
description: Perform a maximally picky and professional code review of recent changes. Reviews all code added since the last review, checking for thread safety, async safety, security vulnerabilities, data integrity, test quality, and code smells. Use before committing significant changes.
---

# Code Review Skill

Perform a professional code review following the standards in `prompts/CODE_REVIEW.md`.

## When to Use

- Before committing significant code changes
- After completing a spike or feature
- When the Stop hook reminds you
- When explicitly requested by user

## Process

1. **Identify scope** - Determine what code needs review:
   - Check `git status` and `git diff` for uncommitted changes
   - Check `git log` to find commits since last review
   - Look for any existing code review documents to find the last review point

2. **Read the review template** - Load `prompts/CODE_REVIEW.md` for the full criteria

3. **Perform the review** - Apply all criteria from the template:
   - MANDATORY: No Quick Hacks policy
   - Race Condition Audit Checklist
   - Critical issues (thread safety, async safety, security, data integrity)
   - High priority (type hints, input validation, logging, test coverage)
   - Medium priority (magic numbers, hard-coded config, duplication)
   - Test quality (primary use cases tested, no anti-patterns)

4. **Write the review document** - Save to `.claude/plans/` with:
   - Executive summary
   - Issues grouped by severity with file:line references
   - Specific code fixes (before/after)
   - Checklist of items to fix
   - Verification steps
   - Notes for future work

5. **Report the path** - Tell the user where to find the review document

## Key Principles

- Be specific and critical
- Every issue needs a file:line reference
- Provide concrete fixes, not just descriptions
- Consider whether code enables future architectural goals
- Quick hacks are absolutely forbidden
