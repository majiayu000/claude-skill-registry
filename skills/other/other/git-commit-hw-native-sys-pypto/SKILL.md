---
name: git-commit
description: Complete git commit workflow for PyPTO including pre-commit review, staging, message generation, and verification. Use when creating commits, preparing changes for commit, or when the user asks to commit changes.
---

# PyPTO Git Commit Workflow

## Prerequisites

**Check what changed to determine which agents to run:**

```bash
git diff --name-only
git diff --cached --name-only
```

**Determine testing needs based on changed files:**

| File Types Changed | Run Code Review | Run Testing | Run Clang-Tidy |
| ------------------ | --------------- | ----------- | -------------- |
| C++ (`.cpp`, `.h`) | ✅ Yes | ✅ Yes | ✅ Yes |
| Python (`.py`, bindings, tests) | ✅ Yes | ✅ Yes | ❌ Skip |
| Build system (`.cmake`, `CMakeLists.txt`) | ✅ Yes | ✅ Yes | ✅ Yes |
| Docs only (`.md`, `.rst`, `docs/`) | ✅ Yes | ❌ Skip | ❌ Skip |
| Config only (`.json`, `.yaml`, `.toml`, `.github/`) | ✅ Yes | ❌ Skip | ❌ Skip |
| Mixed (code + docs/config) | ✅ Yes | ✅ Yes | If C++ changed |

**Launch appropriate agents IN PARALLEL:**

- **`code-reviewer`** - ALWAYS run for all changes
- **`testing`** - ONLY run if code files changed
- **`clang-tidy`** - Run `python tests/lint/clang_tidy.py` if C++ files changed (via Bash agent)

## Workflow

1. Analyze changed files to determine testing needs
2. Launch in parallel (single message with multiple Task tool calls):
   - **code-reviewer** agent (always)
   - **testing** agent (if code changed)
   - **clang-tidy** via Bash agent: `python tests/lint/clang_tidy.py` (if C++ changed)
3. Wait for all agents to complete
4. Address any issues found
5. Stage changes
6. Generate commit message
7. Commit and verify

## Stage Changes

**Related changes together**:

```bash
git add path/to/file1.cpp path/to/file2.h
git diff --staged  # Review
```

**Cross-layer pattern** (C++ + Python + Type stubs + Tests):

```bash
git add include/pypto/ir/expr.h python/bindings/ir_binding.cpp \
        python/pypto/pypto_core/__init__.pyi tests/ut/ir/test_expr.py
```

**Never stage**: Build artifacts (`build/`, `*.o`), temp files, IDE configs

## Commit Message Format

**Structure**: `type(scope): description (≤72 chars)`

**Types**: feat, fix, refactor, test, docs, style, chore, perf
**Scope**: Module/component (ir, printer, builder)
**Description**: Present tense, action verb, no period

**Good examples**:

```text
feat(ir): Add unique identifier field to MemRef
fix(printer): Update printer to use yield_ instead of yield
refactor(builder): Simplify tensor construction logic
test(ir): Add edge case coverage for structural comparison
```

**Bad examples** (avoid):

```text
❌ feat(ir): Added feature.  # Past tense, has period
❌ Fix bug                   # Missing type prefix
❌ WIP                       # Not descriptive
```

## Commit

```bash
# Short message
git commit -m "feat(ir): Add tensor rank validation"

# Detailed message (in editor)
git commit
```

**In editor**:

```text
feat(ir): Add tensor rank validation

Validates tensor rank is positive before setting shape.
Raises ValueError for invalid ranks.
Updates tests with edge case coverage.
```

## Co-Author Policy

**❌ NEVER add AI assistants**: No Claude, ChatGPT, Cursor AI, etc.
**✅ Only credit human contributors**: `Co-authored-by: Name <email>`

**Why?** AI tools are not collaborators. Commits reflect human authorship.

## Post-Commit Verification

```bash
git show HEAD              # View commit
git log -1                 # Check message
git show HEAD --name-only  # Verify files
```

**Fix issues** (only if not pushed):

```bash
git commit --amend -m "Corrected message"      # Fix message
git add file && git commit --amend --no-edit   # Add forgotten file
```

⚠️ **Only amend unpushed commits!**

## Checklist

- [ ] Changed files analyzed (code vs docs/config only)
- [ ] Code review completed
- [ ] Tests passed (if code changed) or skipped (if docs/config only)
- [ ] Clang-tidy passed (if C++ changed) or skipped (if no C++)
- [ ] Only relevant files staged
- [ ] No build artifacts
- [ ] Message format: `type(scope): description` (≤72 chars, present tense, no period)
- [ ] No AI co-authors

## Remember

A good commit is thoroughly reviewed, groups related changes, has clear "why" message, and attributes only human authors.
