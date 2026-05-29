---
name: session-end
description: Complete verification steps before ending the session
---

# Session End Checklist

Before ending the session, complete these verification steps:

## 1. Work Verification

- [ ] All TodoWrite items marked as completed or documented as blocked
- [ ] All commits pushed to remote branch
- [ ] All code review suggestions addressed or documented as skipped (with
      reason)
- [ ] Tests pass: `npm test`
- [ ] Lint passes: `npm run lint`
- [ ] Pattern check passes: `npm run patterns:check`

## 2. CI Verification

If you modified any of these, verify they still work:

- [ ] `.github/workflows/ci.yml` - Main CI pipeline
- [ ] `.github/workflows/docs-lint.yml` - Documentation linting
- [ ] `scripts/check-docs-light.js` - Doc linter script
- [ ] `scripts/check-pattern-compliance.js` - Pattern checker
- [ ] `eslint.config.mjs` - ESLint configuration

## 3. Documentation Updates

- [ ] Update SESSION_CONTEXT.md with:
  - Work completed this session
  - Any new blockers discovered
  - Next steps for future sessions
- [ ] Update ROADMAP.md Active Sprint checkboxes if features completed
- [ ] Log any significant learnings in AI_REVIEW_LEARNINGS_LOG.md
- [ ] Archive completed/cancelled plans to `docs/archive/completed-plans/`
- [ ] **Cross-document check**: Review docs modified this session against
      [DOCUMENT_DEPENDENCIES.md](../../docs/DOCUMENT_DEPENDENCIES.md#cross-document-update-triggers)
      trigger matrix - update any dependent documents

### 3.1 Roadmap Sync Check (MANDATORY for Feature Work)

> **Session #69 Guardrail:** Prevents roadmap staleness by ensuring feature work
> is reflected in ROADMAP.md.

If you implemented features, completed tasks, or made significant progress this
session:

- [ ] **Verify ROADMAP.md reflects current status**
  - Check Active Sprint tasks - mark completed items with `[x]`
  - Check M1.6/M2 phase tasks - update status indicators
  - Update sprint progress percentage if significant work done
- [ ] **No new features without roadmap entry**
  - If you added a new feature not in ROADMAP.md, add it now
  - If you completed a planned feature, mark it done

**Quick Check:**

```bash
# See what code was changed this session
git diff --name-only HEAD~5

# If you see new components/features, verify they're in ROADMAP.md
```

**Why This Matters:**

- Roadmap drift causes planning confusion
- Future sessions won't know what's already implemented
- Session #69 found Sentry was 90% done but roadmap showed "Planned"

## 4. Learning Consolidation (AUTOMATIC - Session #69)

Consolidation now runs **automatically** during SessionStart when the threshold
is reached (10+ reviews). No manual action required.

**What happens automatically:**

- When threshold is reached, `npm run consolidation:run --auto` runs
- Counter is reset in AI_REVIEW_LEARNINGS_LOG.md
- Patterns are analyzed and counted

**Manual follow-up (optional, if you want to persist patterns):**

```bash
npm run consolidation:check   # Check current status
npm run consolidation:run     # Preview what was consolidated
npm run patterns:suggest      # Find automatable patterns
```

If you want to manually add patterns to documentation:

- Add critical patterns to claude.md Section 4 (top 5 only)
- Add full patterns to docs/agent_docs/CODE_PATTERNS.md
- Add suggested patterns to check-pattern-compliance.js

**Why this matters:**

- claude.md is loaded at session START
- Patterns in claude.md will be in context for NEXT session
- This is how the AI "learns" from previous sessions

## 5. Code Review Completeness Audit

If you received code review feedback this session:

```
VERIFICATION CHECKLIST:
├─ Did you address ALL suggestions? (not just some)
├─ Did you test regex patterns for performance?
├─ Did you verify path-based filtering works correctly?
├─ Did you check for CI workflow impacts?
└─ Did you commit descriptive messages explaining WHY changes were made?
```

## 6. Automated Verification (RUN BEFORE MANUAL AUDIT)

Execute these automated checks to verify session compliance:

```bash
# 1. Verify expected skills were used based on activity
npm run skills:verify-usage

# 2. Check if any triggers are pending
npm run triggers:check

# 3. Review any overrides used this session
npm run override:list

# 4. View session activity summary
npm run session:summary
```

**Interpreting Results:**

- **Skills verification failures** indicate skills that should have been used
  but weren't. Either use the skill now, or document why it was skipped.
- **Pending triggers** should be resolved before push. If already resolved,
  document the resolution.
- **Override history** should be reviewed - ensure reasons were provided and are
  legitimate.
- **Session summary** shows what was done this session for documentation
  purposes.

---

## 7. Agent/Skill/MCP/Hook/Script Audit (MANDATORY)

**Complete this audit for every session. If gaps found, document why or fix
before ending.**

### 7.1 Session Start Scripts

| Script                    | Required | Ran? | If No, Why? |
| ------------------------- | -------- | ---- | ----------- |
| `npm run patterns:check`  | ✅       | [ ]  |             |
| `npm run review:check`    | ✅       | [ ]  |             |
| `npm run lessons:surface` | ✅       | [ ]  |             |

### 7.2 Agent Usage (based on work performed)

| Condition                    | Agent            | Should Invoke? | Did Invoke? | If No, Why? |
| ---------------------------- | ---------------- | -------------- | ----------- | ----------- |
| Wrote/modified .js/.ts files | code-reviewer    | [ ]            | [ ]         |             |
| Security-related changes     | security-auditor | [ ]            | [ ]         |             |
| Bug/error debugging          | debugger         | [ ]            | [ ]         |             |
| Complex codebase exploration | Explore          | [ ]            | [ ]         |             |
| Multi-step planning needed   | Plan             | [ ]            | [ ]         |             |

### 7.3 Skill Usage

| Condition             | Skill                | Should Invoke? | Did Invoke? | If No, Why? |
| --------------------- | -------------------- | -------------- | ----------- | ----------- |
| Bug/error encountered | systematic-debugging | [ ]            | [ ]         |             |
| UI/frontend work      | frontend-design      | [ ]            | [ ]         |             |
| Code review requested | code-reviewer        | [ ]            | [ ]         |             |

### 7.4 MCP Servers

| Server                        | Available | Used? | Purpose if Used |
| ----------------------------- | --------- | ----- | --------------- |
| (list from SessionStart hook) |           | [ ]   |                 |

### 7.5 Hooks Executed

| Hook             | Should Trigger | Did Trigger? | Passed? |
| ---------------- | -------------- | ------------ | ------- |
| SessionStart     | ✅             | [ ]          | [ ]     |
| UserPromptSubmit | ✅             | [ ]          | [ ]     |
| Pre-commit       | On commit      | [ ]          | [ ]     |
| Pre-push         | On push        | [ ]          | [ ]     |

### 7.6 Audit Result

**Overall Result:** [ ] PASS [ ] FAIL

**PASS criteria:** All required items ran AND passed (or justified with
explanation)

**If FAIL, select disposition:**

- [ ] Fixes applied this session (describe below)
- [ ] Documented for next session (note in SESSION_CONTEXT.md)

**Remediation notes (if FAIL):**

```
(describe what was invoked/run to address gaps, or next steps)
```

## 8. Key Learnings to Remember

Today's session reinforced these patterns:

### DO:

- Read files before editing
- Use TodoWrite for multi-step tasks
- Check all code review items multiple times
- Add path-based filtering for context-specific patterns
- Use bounded regex (`{0,N}?`) instead of greedy (`.*`)
- Spread ESLint plugin configs in flat config format
- Exclude archive files (`docs/archive/`) from strict linting
- Add `continue-on-error` for pre-existing issues in CI

### DON'T:

- Skip code review suggestions without documenting why
- Use greedy regex that can cause runaway matches
- Forget to test changes before committing
- Push without verifying CI impact
- Edit files without reading them first

## 9. Commit Summary

Provide a summary of all commits made this session:

```
git log --oneline -10
```

---

## 10. Update Session State (AUTOMATIC)

**IMPORTANT:** Run this command to update session state tracking:

```bash
npm run hooks:health -- --end
```

This updates the cross-session validation system so that:

- Next session-begin knows this session ended properly
- Session statistics are tracked
- No false warnings about incomplete sessions

---

Session complete. All work has been verified and documented.
