---
name: code-review-repo
description: Review local codebase for bugs and CLAUDE.md compliance using multi-agent analysis
version: 1.0.0
---

# Local Code Review

Review the entire local codebase for bugs, issues, and CLAUDE.md compliance.

## Process

1. **Gather CLAUDE.md files**: Use a Haiku agent to find all CLAUDE.md files in the repository (root and subdirectories)

2. **Identify source files**: Determine which files to review:
   - Include: `.ts`, `.tsx`, `.js`, `.jsx`, `.py`, `.rs`, `.go` and similar source files
   - Exclude: `node_modules/`, `dist/`, `.git/`, vendor directories, generated files

3. **Multi-agent review**: Launch 5 parallel Sonnet agents to independently review the codebase. Each agent returns a list of issues with reasons:
   - **Agent #1**: Audit for CLAUDE.md compliance. Check that code follows guidelines in all relevant CLAUDE.md files.
   - **Agent #2**: Shallow bug scan. Look for obvious bugs, error handling issues, and logic errors. Focus on significant bugs, not nitpicks.
   - **Agent #3**: Git history context. Use git blame and history to identify patterns, recent changes, and potential issues in light of historical context.
   - **Agent #4**: Previous PR comments. Check closed PRs that touched these files for any feedback that might apply.
   - **Agent #5**: Code comment compliance. Ensure code follows any guidance in TODO, FIXME, NOTE, or other code comments.

4. **Confidence scoring**: For each issue found, launch a parallel Haiku agent to score confidence (0-100):
   - **0**: False positive, doesn't hold up to scrutiny
   - **25**: Might be real, but unverified. Stylistic issues not in CLAUDE.md
   - **50**: Real but minor, rarely hit in practice
   - **75**: Verified real issue, important, directly impacts functionality or mentioned in CLAUDE.md
   - **100**: Definitely real, frequently hit, evidence confirms

5. **Filter**: Only report issues with score >= 80

## False Positive Examples

Avoid flagging:

- Issues that linters/typecheckers catch (imports, types, formatting)
- General quality issues unless in CLAUDE.md
- Code with lint-ignore comments for that specific issue
- Pre-existing issues unrelated to recent changes
- Pedantic nitpicks a senior engineer wouldn't mention

## Output Format

### Code review

Found N issues:

1. Brief description (CLAUDE.md says "...")
   `file/path.ts:42`

2. Brief description (bug due to missing error handling)
   `file/path.ts:88-95`

---

Or if no issues:

### Code review (no issues)

No issues found. Checked for bugs and CLAUDE.md compliance.
