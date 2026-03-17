---
name: ship
description: Complete end-of-session workflow - verify work quality, organize commits, and track progress. Use at the end of a development session to ship cleanly.
hooks:
  SubagentStart:
    - matcher: ".*"
      hooks:
        - type: command
          command: |
            echo ""
            echo "🤖 Using agent: $AGENT_TYPE"
  SubagentStop:
    - hooks:
        - type: command
          command: "echo '   ✓ Agent complete'"
  Stop:
    - hooks:
        - type: prompt
          prompt: |
            Verify that /ship completed all required phases successfully:

            1. Phase 0 (Verify Work):
               - Did /verify-work run and find all issues?
               - Were ALL blocking issues resolved (security, best practices, standards)?
               - Did tests run and pass?

            2. Phase 1 (Organize Commits):
               - Were git commits created with conventional commit format?
               - Were changes grouped logically?

            3. Phase 2 (Track Progress):
               - Did /track-progress run and record the work?

            Context: $ARGUMENTS

            Return {"ok": true} ONLY if all three phases completed successfully.
            Return {"ok": false, "reason": "specific issue"} if any phase was incomplete or failed.
          timeout: 30
---

# Ship Skill

Complete end-of-session workflow: verify work, organize commits, and track progress.

## When to Use

Invoke with `/ship` when you're done with a development session and want to:
- Verify code quality and security
- Create clean, organized commits from your changes
- Track progress in changelog and/or project roadmap

## Instructions

### Phase 0: Verify Work (Mandatory)

**IMPORTANT**: All code changes MUST pass verification before organizing commits.

1. **Run comprehensive verification** by invoking the verify-work skill:
   - Security checks (secrets, SQL injection, XSS, validation, rate limits)
   - Best practices (debug code, TypeScript, error handling)
   - Efficiency (React hooks, re-renders, imports)
   - Code standards (CSS Modules, API patterns, naming)

2. **Review all findings** presented by verification:
   - 🔒 Security issues (BLOCKING)
   - ⚠️ Best practice violations (BLOCKING)
   - 💡 Efficiency issues (optimization recommendations)
   - 📝 Code standard violations (BLOCKING)

3. **Resolve all BLOCKING issues**:
   - Use 'fix all' to auto-fix available issues
   - Manually fix issues that require code changes
   - Re-run verification until all blocking issues are resolved

4. **Cannot proceed** to Phase 1 until:
   - All security issues are resolved
   - All best practice violations are fixed
   - All code standard violations are corrected
   - User has explicitly approved any remaining optimizations

5. **Check if tests need updates**:
   - Search for existing tests related to changed files/functions
   - If changing constants, limits, or config values, check test mocks and assertions
   - If changing function signatures, check test function calls
   - If changing API behavior, check API tests for expected responses

   Common patterns to check:
   - `tests/lib/*.test.ts` for library changes in `lib/`
   - `tests/config/*.test.ts` for config changes in `src/config/`
   - Mock values (`mockResolvedValue`, `mockReturnValue`) that simulate changed data
   - Assertions (`expect(x).toBe(y)`) that verify changed values

   Update any tests that would fail due to the code changes.

6. **Run tests** to ensure nothing is broken:
   ```bash
   npm test
   ```
   - If tests fail, fix the issues before proceeding
   - All tests must pass to continue to Phase 1

**This ensures code quality, security standards, and test coverage before any commit is made.**

---

### Phase 1: Organize Commits

1. **Analyze Changes**
   ```bash
   git status
   git diff --stat HEAD
   ```

2. **Group into Logical Commits**
   Categorize by: feat, fix, refactor, style, docs, chore, test, perf

3. **Present Commit Plan**
   Show proposed groupings and ask for approval.

4. **Execute Commits**
   Create each commit with conventional commit messages.

### Phase 2: Track Progress (Automatic)

After commits are created, automatically track progress:

```
Recording progress...
- Scanning commits for changelog/progress routing
- User-facing changes → changelog + progress
- Admin/test/refactor → progress only

✓ Changelog: 2026-02-01 - Feature Name (draft)
✓ Progress: Feature Name (3 items)

Done! Review changelog at /admin/changelog to publish.
```

**How it works:**
- Analyzes commit types and scopes to route automatically
- `feat`, `fix` (user-facing) → changelog + progress
- `feat(admin)`, `test`, `refactor` → progress only
- Checks for duplicates before creating
- Creates changelog entries as drafts for review
- Progress entries are **initiatives only** (no individual action items) to keep the view focused

**To skip tracking (rare):**
If you need to skip tracking for a specific session, say "skip tracking" when prompted. This should be rare - tracking helps maintain project visibility.

## Quick Reference

| Phase | Action | Command/Tool |
|-------|--------|--------------|
| 0 | Verify work | `/verify-work` skill |
| 0 | Fix issues | Auto-fix or manual |
| 0 | Check test updates | Search `tests/` for related tests |
| 0 | Run tests | `npm test` |
| 1 | Check changes | `git status` |
| 1 | Create commits | `git add` + `git commit` |
| 2 | Track progress | Automatic (uses commit data) |

## Example Flow

```
User: /ship

Claude: I'll help you ship your changes. First, let me verify all code quality...

[Phase 0: Runs verification]

## Verification Results

### Best Practices [BLOCKING] - 2 found
- [ ] Debug Code - 3 console.logs in src/components/Dashboard.tsx
  Auto-fix: Available

### Code Standards [BLOCKING] - 1 found
- [ ] API Pattern - Missing errorResponse helper in app/api/filters/route.ts
  Auto-fix: Available

**Summary:** 3 blocking issues found
**Actions:** Type 'fix all' to auto-fix

User: fix all

Claude: Applying fixes...
- Removed 3 console.log statements
- Added errorResponse import and usage

Re-running verification... All checks passed!

Running tests...
✓ 45 tests passed
All tests passing!

[Phase 1: Analyzes changes]

I found 12 changed files across 3 categories:
1. feat(filters): Add active filter and counts (4 files)
2. fix(import): Include missing schema fields (1 file)
3. refactor(plan): Reorder tabs for workflow (1 file)

Does this grouping look right?

User: yes

Claude: Creating commits...
- Commit 1: feat(filters): add active filter and counts
- Commit 2: fix(import): include missing schema fields
- Commit 3: refactor(plan): reorder tabs for workflow

[Phase 2: Track Progress - Automatic]

Recording progress...

Analyzing commits:
  ★ feat(filters): add active filter and counts → changelog + progress
  ★ fix(import): include missing schema fields → changelog + progress
  ○ refactor(plan): reorder tabs for workflow → progress only

Creating entries...
  ✓ Changelog: 2026-01-13 - Add active filter and counts (draft)
  ✓ Progress: Add active filter and counts (1 item)
  ✓ Changelog: 2026-01-13 - Include missing schema fields (draft)
  ✓ Progress: Include missing schema fields (1 item)
  ✓ Progress: Reorder tabs for workflow (1 item)

Ship complete!
- 3 commits created
- 2 changelog entries (draft) - review at /admin/changelog
- 3 progress entries
```

## Notes

- **Phase 0 is mandatory** - Cannot skip verification or tests
- Verification ensures code quality, security, and adherence to project standards
- **Always check if tests need updates** when changing constants, limits, config values, or function behavior
- All tests must pass before proceeding to commits
- Auto-fix available for common issues (console.logs, rate limiting, etc.)
- Manual fix required for complex issues (SQL injection, Zod schemas)
- If verification or tests fail, Phase 1 will not proceed until issues are resolved
- `/track-progress` writes directly to database - no manual import needed
- Commits follow conventional commit format with Co-Authored-By