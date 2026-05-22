---
name: safe-commit
description: ⚠️ MANDATORY - YOU MUST invoke this skill when committing. Complete commit workflow with all safety checks. Invokes security-scan, quality-check, and run-tests skills. Shows diff, gets user approval, creates commit with conventional format. NO AI attribution. User approval REQUIRED except during PR creation. NEVER commit manually.
version: 1.0.1
---

# Safe Commit Skill

## ⚠️ MANDATORY SKILL - YOU MUST INVOKE THIS

## Purpose

Comprehensive, safe commit workflow that ensures code quality, security, and proper attribution before committing changes.

**CRITICAL:** You MUST invoke this skill for all commits. NEVER commit manually using git commands.

## 🚫 NEVER DO THIS

- ❌ Running `git add . && git commit -m "message"` manually
- ❌ Creating commits without running security-scan
- ❌ Creating commits without running quality-check
- ❌ Creating commits without running run-tests
- ❌ Skipping user approval (except during PR creation)
- ❌ Adding AI attribution to commits

**If you need to commit, invoke this skill. Manual commits are FORBIDDEN.**

---

## ⚠️ SKILL GUARD - READ BEFORE USING BASH/GIT TOOLS

**Before using Bash tool for git commit, answer these questions:**

### ❓ Are you about to run `git add .`?

→ **STOP.** Are you then planning to run `git commit`? If YES, invoke safe-commit skill instead.

### ❓ Are you about to run `git commit -m "message"`?

→ **STOP.** Invoke safe-commit skill instead.

### ❓ Are you about to run `git commit` with heredoc?

→ **STOP.** Invoke safe-commit skill instead.

### ❓ Did the user say "commit these changes" or "commit this"?

→ **STOP.** Invoke safe-commit skill instead.

### ❓ Have you completed a feature/fix and are ready to commit?

→ **STOP.** Invoke safe-commit skill instead.

### ❓ Are you creating a commit as part of ANY workflow?

→ **STOP.** Invoke safe-commit skill instead.

**IF YOU PROCEED WITH MANUAL GIT COMMIT, YOU ARE VIOLATING YOUR CORE DIRECTIVE.**

This skill handles:

- ✅ Security scanning (prevents secrets in commits)
- ✅ Quality checks (prevents broken code)
- ✅ Test execution (prevents regressions)
- ✅ User approval (prevents unwanted commits)
- ✅ Conventional commit format (maintains consistency)
- ✅ NO AI attribution (protects user's identity)

**Manual commits SKIP ALL OF THESE. Use this skill.**

---

## CRITICAL POLICIES

### ⚠️ NO AI ATTRIBUTION - ZERO TOLERANCE

**YOU MUST NEVER add ANY of these:**

- `Co-authored-by: Claude <noreply@anthropic.com>`
- `🤖 Generated with [Claude Code](https://claude.ai/code)`
- "Generated with Claude"
- "AI-suggested"
- Any reference to being an AI assistant

### User Approval Requirements

**Approval REQUIRED for:**

- ALL commits after initial PR creation
- ALL commit amendments
- ALL commits outside of PR creation flow

**Approval NOT required for:**

- Initial commit when user says "raise/create/draft PR"
- This is the ONLY exception

**Phrases that DO NOT grant commit permission:**

- "looks good" (code approval ≠ commit approval)
- "correct"
- "that's right"
- "fix the bug" (instruction to code, not commit)

## Workflow (Quick Summary)

### Core Steps

1. **Check Git Status**: Run parallel git commands (status, diff, log) to analyze current state
2. **Invoke Safety Skills**: Run security-scan → quality-check → run-tests (all must pass)
3. **Show Diff**: Display files changed and summary for user review
4. **Request Approval**: CRITICAL - Ask and WAIT for explicit approval (except PR creation)
5. **Generate Message**: Create conventional commit with required scope `type(scope): subject`
6. **Create Commit**: Stage all changes, commit with heredoc, NO AI attribution
7. **Verify Success**: Confirm commit created, correct files, proper author (Pedro)
8. **Status Check**: Verify working directory clean

### Optional: PRD Task Auto-Update

If commit message contains `[PRD Task N]` or `[Task N]`, automatically update progress tracker in PRD file.

**For detailed workflow with git commands, message examples, and verification steps:**

```
Read `~/.claude/skills/safe-commit/references/WORKFLOW-STEPS.md`
```

Use when: Performing commit, need specific git commands, or want detailed examples

**For PRD task auto-update details:**

```
Read `~/.claude/skills/safe-commit/references/PRD-TASK-UPDATE.md`
```

Use when: Working with PRD tracking or implementing progress automation

**For pre-commit hook handling:**

```
Read `~/.claude/skills/safe-commit/references/PRE-COMMIT-HOOKS.md`
```

Use when: Dealing with hook-modified files or commit amendment scenarios

---

## Integration with Other Skills

This skill invokes:

- **`security-scan`** - Step 2.1
- **`quality-check`** - Step 2.2
- **`run-tests`** - Step 2.3

This skill is invoked by:

- **`create-pr`** - As part of PR creation workflow

---

## Exception: PR Creation Flow

When invoked by `create-pr` skill:

- Skip Step 4 (user approval)
- Proceed directly to commit
- This is the ONLY time auto-commit is allowed

**The `create-pr` skill is only invoked when user explicitly says "raise/create/draft PR"**

---

## Error Handling

### If security scan fails:

```
❌ Cannot commit: Security issues detected

[Details from security-scan skill]

Please fix security issues and try again.
```

### If quality check fails:

```
❌ Cannot commit: Code quality issues detected

[Details from quality-check skill]

Please fix linter/formatter issues and try again.
```

### If tests fail:

```
❌ Cannot commit: Tests failing or coverage below threshold

[Details from run-tests skill]

Please fix failing tests and improve coverage, then try again.
```

### If git commit fails:

```
❌ Commit failed

Error: [git error message]

Possible causes:
- Pre-commit hook failure
- Git configuration issue
- File system permissions

Please investigate and retry.
```

---

## Best Practices

1. **Always run in order** - Security → Quality → Tests → Commit
2. **No skipping checks** - All must pass
3. **Get explicit approval** - Don't assume permission (except PR creation)
4. **Descriptive messages** - Help future you understand why
5. **Proper scopes** - Never omit scope from commit message
6. **Verify attribution** - Always ensure Pedro is sole author
7. **Clean commits** - Stage all changes, commit once

---

## Commit Message Quality Checklist

Before committing, verify message has:

- ✅ Type and scope in format: `type(scope):`
- ✅ Imperative mood in subject
- ✅ Subject ≤ 50 characters
- ✅ Body explains why (if needed)
- ✅ References issues/tickets (if applicable)
- ✅ NO AI attribution anywhere
- ✅ NO Co-authored-by tags

---

## Emergency Override

If user explicitly states "force commit" or "skip checks":

**YOU MUST:**

1. Warn about risks
2. List which checks are being skipped
3. Get explicit re-confirmation
4. Document in commit message what was skipped
5. Create follow-up ticket for remediation

**This should be EXTREMELY RARE.**
