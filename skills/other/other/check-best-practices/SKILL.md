---
name: check-best-practices
description: "Check local branch changes against all best practices documentation. Systematically audits the diff between current branch and base branch against every applicable best practice. Triggers on: check best practices, best practices check, audit best practices, bp check, check bp."
allowed-tools: Bash(git diff:*), Bash(git log:*), Bash(git status:*), Bash(git merge-base:*), Bash(git branch:*), Bash(git rev-parse:*), Bash(gh pr view:*), Bash(pwd:*), Read, Grep, Glob
---

# Best Practices Check

Systematically audit the current branch's changes against every applicable best practice. This produces a per-document report showing which practices were checked, which violations were found, and which practices are not applicable to the current changes.

---

## Step 1: Detect Working Directory

Determine the brave source directory:

```bash
CURRENT_DIR=$(pwd)
```

- **If within `src/brave`**: `BRAVE_SRC="."`, `CHROMIUM_SRC="../../"`
- **If within `brave-core-bot`**: `BRAVE_SRC="../src/brave"`, `CHROMIUM_SRC="../src"`
- **Otherwise**: Look for characteristic files to detect, or ask the user

---

## Step 2: Determine Base Branch

Detect the base branch in this order:

1. **Check for an existing PR**:
   ```bash
   CURRENT_BRANCH=$(git -C $BRAVE_SRC branch --show-current)
   PR_BASE=$(gh pr view "$CURRENT_BRANCH" --repo brave/brave-core \
     --json baseRefName --jq '.baseRefName' 2>/dev/null) || true
   ```

2. **Check the upstream tracking branch**:
   ```bash
   TRACKING=$(git -C $BRAVE_SRC rev-parse --abbrev-ref \
     "$CURRENT_BRANCH@{upstream}" 2>/dev/null) || true
   ```

3. **Fall back to `master`**

Report the detected base branch at the start.

---

## Step 3: Gather the Diff

```bash
MERGE_BASE=$(git -C $BRAVE_SRC merge-base HEAD $BASE_BRANCH)

# All committed changes on this branch since diverging from base
git -C $BRAVE_SRC diff $MERGE_BASE..HEAD

# Uncommitted changes (staged + unstaged)
git -C $BRAVE_SRC diff HEAD

# List of changed files
git -C $BRAVE_SRC diff --name-only $MERGE_BASE..HEAD
git -C $BRAVE_SRC diff --name-only HEAD
```

Combine committed + uncommitted changes into the full diff to audit.

---

## Step 4: Classify Changed Files

Categorize every changed file to determine which best practices documents apply:

| File Pattern | Category | Best Practices Doc |
|---|---|---|
| `*.cc`, `*.h`, `*.mm` | C++ code | `coding-standards.md` |
| `*_browsertest*`, `*_unittest*`, `*test*.cc` | C++ tests | `testing-async.md`, `testing-isolation.md` |
| `*browsertest*` with JS eval | JS in tests | `testing-javascript.md` |
| `*browsertest*` with navigation | Navigation tests | `testing-navigation.md` |
| `*.ts`, `*.tsx`, `*.js`, `*.jsx` | Front-end | `frontend.md` |
| `BUILD.gn`, `*.gni`, `DEPS` | Build system | `build-system.md` |
| `chromium_src/**` | chromium_src overrides | `chromium-src-overrides.md` |
| Architecture/service files | Architecture | `architecture.md` |
| `*.md`, comments, docs | Documentation | `documentation.md` |

A file can match multiple categories (e.g., a `_browsertest.cc` is both C++ and test code).

**Always include `coding-standards.md` if any C++ files are changed**, since it covers universal C++ rules.

---

## Step 5: Systematic Best Practices Audit

For each applicable best practices document, perform a focused audit:

### Process for Each Document

1. **Read the full document** from `./brave-core-bot/docs/best-practices/<doc>.md`
2. **Read the changed files in full** to understand context (not just the diff)
3. **Check each practice in the document against the diff**, one by one
4. **Classify each practice** for this diff as:
   - **VIOLATION**: The diff introduces code that violates this practice
   - **PASS**: The diff includes code relevant to this practice and follows it correctly
   - **N/A**: This practice doesn't apply to any code in the diff

**Important:**
- Only flag VIOLATION for code that is **newly introduced or modified** in the diff. Don't flag pre-existing code that wasn't touched.
- Read surrounding code context to avoid false positives. A pattern that looks wrong in isolation may be correct in context.
- For each violation, cite the specific practice title, the file and line, and what should change.

### Document Audit Order

Audit documents in this order (most impactful first):

1. **`coding-standards.md`** — if any C++ files changed
2. **`testing-async.md`** — if any test files changed
3. **`testing-isolation.md`** — if any test files changed
4. **`testing-javascript.md`** — if tests use JS evaluation
5. **`testing-navigation.md`** — if tests involve navigation
6. **`architecture.md`** — if service/component architecture changed
7. **`chromium-src-overrides.md`** — if chromium_src files changed
8. **`build-system.md`** — if BUILD.gn/gni/DEPS files changed
9. **`frontend.md`** — if TypeScript/React files changed
10. **`documentation.md`** — if documentation or comments changed

**Skip documents entirely if no changed files fall into their category.** Report which documents were skipped and why.

---

## Step 6: Check the Quick Checklist

After the per-document audit, also check the quick checklist from `BEST-PRACTICES.md` if any async test code was changed:

- [ ] No `RunLoop::RunUntilIdle()` usage
- [ ] No `EvalJs()` or `ExecJs()` inside `RunUntil()` lambdas
- [ ] Using manual polling loops for JavaScript conditions
- [ ] Using `base::test::RunUntil()` only for C++ conditions
- [ ] Waiting for specific completion signals, not arbitrary timeouts
- [ ] Using isolated worlds (`ISOLATED_WORLD_ID_BRAVE_INTERNAL`) for test JS
- [ ] Per-resource expected values for HTTP request testing
- [ ] Large throttle windows for throttle behavior tests
- [ ] Proper observers for same-document navigation
- [ ] Testing public APIs, not implementation details
- [ ] Searched Chromium codebase for similar patterns
- [ ] Included Chromium code references in comments when following patterns
- [ ] Prefer event-driven JS (MutationObserver) over C++ polling for DOM changes

---

## Step 7: Generate Report

```markdown
# Best Practices Audit: <branch-name>

## Overview
- **Branch**: <branch-name>
- **Base branch**: <base-branch> (detection method: PR / tracking / default)
- **Files changed**: <count>
- **Documents audited**: <count> of 10
- **Documents skipped**: <count> (not applicable)

## Violations Found

### <violation-count> Violation(s)

For each violation:

#### [<doc-name>] <practice-title>
- **File**: `path/to/file.cc:<line>`
- **Practice**: <brief description of the practice>
- **Issue**: <what the code does wrong>
- **Fix**: <what should be done instead, with code example if helpful>

## Per-Document Results

### <doc-name> — <VIOLATIONS_FOUND | ALL_PASS | SKIPPED>

<If audited, list practices checked with their status:>
- PASS: <practice title> — <brief note on what was checked>
- VIOLATION: <practice title> — see Violations section
- N/A: <practice title>

<If skipped:>
Skipped — no <category> files in the diff.

## Summary

**Result**: <PASS (no violations) | FAIL (<N> violations found)>

<If violations found:>
<N> violation(s) across <M> best practices document(s). Fix the violations listed above before proceeding.

<If no violations:>
All applicable best practices checked. No violations found in the branch changes.
```

---

## Important Guidelines

### Accuracy Over Speed
- **Read changed files in full** — don't just rely on the diff. Context matters.
- **Don't flag false positives** — if unsure whether something is a violation, read more context. A false positive wastes developer time.
- **Only flag new/modified code** — pre-existing violations in untouched code are out of scope.

### Be Specific and Actionable
- Every violation must include file, line, and a concrete fix suggestion.
- Reference the specific best practice by its title from the document.
- Include code examples when the fix isn't obvious.

### Don't Over-Report
- **N/A practices don't need individual listings** in the summary unless verbose output is requested. Group them as a count.
- Focus the report on violations and notable passes.
- Keep the report scannable — developers should be able to find violations quickly.
