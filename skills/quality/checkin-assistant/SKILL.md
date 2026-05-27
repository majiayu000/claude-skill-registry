---
name: checkin-assistant
description: |
  Guide pre-commit quality gates and check-in workflow.
  Use when: committing code, preparing commits, quality gate verification.
  Keywords: commit, checkin, pre-commit, quality gate, git add, 提交, 簽入, 品質關卡.
---

# Checkin Assistant

> **Language**: English | [繁體中文](../../../locales/zh-TW/skills/claude-code/checkin-assistant/SKILL.md)

**Version**: 1.0.0
**Last Updated**: 2026-01-12
**Applicability**: Claude Code Skills

---

## Purpose

This skill guides developers through pre-commit quality gates, ensuring every commit maintains codebase stability and follows best practices.

**Note**: This skill focuses on **when and how to commit**. For code review during PR, see [Code Review Assistant](../code-review-assistant/SKILL.md).

---

## Quick Reference (YAML Compressed)

```yaml
# === CORE PHILOSOPHY ===
every_commit_should:
  - "Be a complete logical unit of work"
  - "Leave codebase in working state"
  - "Be reversible without breaking functionality"
  - "Contain its own tests (for new features)"
  - "Be understandable to future developers"

# === MANDATORY CHECKLIST ===
checklist:
  build:
    - "Code compiles (zero errors)"
    - "Dependencies satisfied"
    verify: "Run build command, exit code 0"

  tests:
    - "All existing tests pass (100%)"
    - "New code has tests"
    - "Coverage not decreased"
    verify: "Run test suite, check coverage"

  quality:
    - "Follows coding standards"
    - "No code smells (methods≤50, nesting≤3, complexity≤10)"
    - "No hardcoded secrets"
    - "No security vulnerabilities"
    verify: "Run linter, security scanner"

  docs:
    - "API docs updated"
    - "README updated (if needed)"
    - "CHANGELOG updated (user-facing changes → [Unreleased])"

  workflow:
    - "Branch naming correct (feature/, fix/, docs/, chore/)"
    - "Commit message formatted (conventional commits)"
    - "Synced with target branch"

# === NEVER COMMIT WHEN ===
blockers:
  - "Build has errors"
  - "Tests are failing"
  - "Feature incomplete (would break functionality)"
  - "Contains WIP/TODO in critical logic"
  - "Contains debugging code (console.log, print)"
  - "Contains commented-out code blocks"

# === COMMIT TIMING ===
good_times:
  - completed_unit: "Feature fully implemented with tests"
  - bug_fixed: "Bug fixed with regression test"
  - independent_refactor: "Refactoring complete, all tests pass"
  - runnable_state: "Code compiles, app can run"

bad_times:
  - "Build failures"
  - "Test failures"
  - "Incomplete features"
  - "Experimental code with scattered TODOs"

# === GRANULARITY ===
ideal_commit:
  files: "1-10 (split if >10)"
  lines: "50-300"
  scope: "Single concern"

split_rules:
  combine: ["feature + its tests", "tightly related multi-file changes"]
  separate: ["Feature A + B", "refactor + new feature", "bugfix + incidental refactor"]

# === SPECIAL SCENARIOS ===
emergency_leave:
  recommended: "git stash save 'WIP: description'"
  alternative: "Create wip/ branch"
  prohibited: "Commit WIP directly on feature branch"

experimental:
  branch: "experiment/topic-name"
  rules: "Free commits (no strict format)"
  success: "Clean up, squash, merge to feature"
  failure: "Document lessons, delete branch"

hotfix:
  branch: "hotfix/issue-name from main"
  rules: "Minimize changes, only fix the problem"
  message: "fix(scope): [URGENT] description"
```

---

## Checklist Visual Format

Use this checklist before every commit:

```
┌─────────────────────────────────────────────────────────────────┐
│  📋 PRE-COMMIT CHECKLIST                                        │
├─────────────────────────────────────────────────────────────────┤
│  🔨 BUILD                                                       │
│  □ Code compiles successfully (zero errors)                     │
│  □ All dependencies satisfied                                   │
├─────────────────────────────────────────────────────────────────┤
│  🧪 TESTS                                                       │
│  □ All existing tests pass (100%)                               │
│  □ New code has corresponding tests                             │
│  □ Test coverage not decreased                                  │
├─────────────────────────────────────────────────────────────────┤
│  ✨ CODE QUALITY                                                │
│  □ Follows project coding standards                             │
│  □ No hardcoded secrets or credentials                          │
│  □ No security vulnerabilities                                  │
├─────────────────────────────────────────────────────────────────┤
│  📝 DOCUMENTATION                                               │
│  □ API documentation updated (if applicable)                    │
│  □ CHANGELOG updated (user-facing changes)                      │
├─────────────────────────────────────────────────────────────────┤
│  🔄 WORKFLOW                                                    │
│  □ Branch naming follows convention                             │
│  □ Commit message follows conventional commits                  │
│  □ Synced with target branch (no conflicts)                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## Check-in Trigger Points

### When to Prompt for Commit

| Trigger | Condition | Reminder Level |
|---------|-----------|----------------|
| Phase Complete | Completed a development phase | Suggest |
| Checkpoint | Reached defined checkpoint | Suggest |
| Change Accumulation | Files ≥5 or lines ≥200 | Suggest |
| Consecutive Skips | Skipped commit 3 times | Warning |
| Work Complete | Uncommitted changes before finishing | Strongly Recommend |

### Reminder Format

```
┌────────────────────────────────────────────────┐
│ 🔔 Check-in Checkpoint                         │
├────────────────────────────────────────────────┤
│ Phase 1 completed                              │
│                                                │
│ Change Statistics:                             │
│   - Files: 5                                   │
│   - Added: 180 lines                           │
│   - Deleted: 12 lines                          │
│                                                │
│ Test Status: ✅ Passed                         │
│                                                │
│ Suggested commit message:                      │
│   feat(module): complete Phase 1 setup         │
│                                                │
│ Options:                                       │
│   [1] Commit now (will show git commands)      │
│   [2] Commit later, continue to next phase     │
│   [3] View detailed changes                    │
└────────────────────────────────────────────────┘
```

### Skip Warning

After 3 consecutive skips:

```
⚠️ Warning: You have skipped check-in 3 times consecutively
Current accumulated changes: 15 files, +520 lines
Recommend committing soon to avoid changes becoming too large to review
```

---

## AI Assistant Workflow

When AI completes code changes, follow this workflow:

### Step 1: Evaluate Timing

```
✅ Complete: "Implemented user registration with validation, tests, and docs"
⚠️ Incomplete: "Added registration form but backend validation pending"
❌ Not Ready: "Started working on registration, several TODOs remain"
```

### Step 2: Run Checklist

```
### Checklist Results

✅ Build: npm run build succeeded
✅ Code Quality: Follows project standards
⚠️ Tests: Unit tests pass, integration tests need verification
✅ Documentation: JSDoc comments added
✅ Commit Message: Prepared following conventional commits
```

### Step 3: Prompt User

```markdown
## Please Confirm Check-in

Completed: [Brief description]

### Checklist Results
✅ Build passes
✅ Tests pass
✅ Code quality verified
✅ Documentation updated

Suggested commit message:
```
feat(auth): add OAuth2 Google login support

- Implement OAuth2 flow with Google provider
- Add user session management
- Include unit tests for auth service

Refs #123
```

Proceed with commit?
```

### Step 4: Wait for Confirmation

**AI MUST**:
- ✅ Wait for explicit user approval
- ✅ Provide clear checklist summary
- ✅ Allow user to decline or request changes

**AI MUST NOT**:
- ❌ Automatically execute `git add`
- ❌ Automatically execute `git commit`
- ❌ Automatically execute `git push`

---

## Common Violations

### ❌ WIP Commits

```bash
# Bad
git commit -m "WIP"
git commit -m "save work"

# Solution: Use git stash
git stash save "WIP: feature description"
```

### ❌ Commented Code

```javascript
// Bad: Committing commented old code
// const oldValue = calculate(x);
const newValue = calculateV2(x);

// Solution: Delete commented code, rely on git history
const newValue = calculateV2(x);
```

### ❌ Mixed Concerns

```bash
# Bad: One commit with multiple unrelated changes
git commit -m "fix bug and refactor and add feature"

# Solution: Separate commits
git commit -m "fix(module-a): resolve null pointer"
git commit -m "refactor(module-b): extract validation"
git commit -m "feat(module-c): add CSV export"
```

---

## Directory Hygiene

Before committing, verify no unwanted files:

```bash
# Check for IDE artifacts in staging
git diff --cached --name-only | grep -E '\.idea|\.vs/|\.DS_Store'

# Check for abnormal directories
git ls-files | grep -E '^\$'

# Unstage unwanted files
git reset HEAD <file>
```

### Common Artifacts to Exclude

| Pattern | Source | Action |
|---------|--------|--------|
| `.idea/` | JetBrains | gitignore |
| `.vs/` | Visual Studio | gitignore |
| `.DS_Store` | macOS | gitignore |
| `Thumbs.db` | Windows | gitignore |

---

## Configuration Detection

### Detection Order

1. Check `CONTRIBUTING.md` for "Disabled Skills" section
2. Check `CONTRIBUTING.md` for "Check-in Standards" section
3. Check for pre-commit hooks configuration
4. If not found, **default to standard checklist**

### First-Time Setup

If no configuration found:

1. Suggest documenting in `CONTRIBUTING.md`:

```markdown
## Check-in Standards

### Build Commands
```bash
npm run build
```

### Test Commands
```bash
npm test
```

### Quality Commands
```bash
npm run lint
```

### Minimum Coverage
- Line: 80%
- Branch: 75%
```

---

## Detailed Guidelines

For complete standards, see:
- [Checkin Standards](../../../core/checkin-standards.md)

---

## Related Standards

- [Checkin Standards](../../../core/checkin-standards.md) - Core standard
- [Commit Message Guide](../../../core/commit-message-guide.md) - Message format
- [Code Review Checklist](../../../core/code-review-checklist.md) - PR review
- [Code Review Assistant](../code-review-assistant/SKILL.md) - Review skill
- [Commit Standards Skill](../commit-standards/SKILL.md) - Commit message skill

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-12 | Initial release |

---

## License

This skill is released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

**Source**: [universal-dev-standards](https://github.com/AsiaOstrich/universal-dev-standards)
