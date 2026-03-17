---
name: commit-work
description: Use when work is complete and ready to commit. Triggers after code review passes, when asked to "commit", "save this", or "wrap up". Runs quality checks, updates changelog, creates commit.
---

# Commit Work

Commit workflow that ensures quality gates pass and changelog is updated before committing.

## When to Use

- After `/code-review` passes with no critical issues
- When asked to commit, save, or wrap up work
- Before creating a PR

## Workflow

```
┌─────────────────────┐
│ 1. Run quality      │
│    checks           │
│    ty → ruff → pytest
└─────────┬───────────┘
          │
          ▼
    ┌─────────────┐
    │ All pass?   │───No──→ STOP. Fix issues first.
    └─────┬───────┘
          │Yes
          ▼
┌─────────────────────┐
│ 2. Update CHANGELOG │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ 3. Stage + Commit   │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ 4. Verify success   │
└─────────────────────┘
```

## Step 1: Run Quality Checks

Run in this order. Stop on first failure. Prefer the deterministic scripts in `scripts/`.

```bash
scripts/run_quality_checks.sh
```

**If any fail:** Fix the issue. Do not proceed to commit.

**No exceptions:**
- "It's a flaky test" → Fix the test or mark it properly
- "I manually tested it" → Automated tests must pass
- "We can fix it later" → Later never comes. Fix now.

## Step 2: Update CHANGELOG

Create or update `CHANGELOG.md` in project root. After editing, verify the `[Unreleased]` section has entries:

```bash
uv run python scripts/ensure_changelog_unreleased.py
```

**IMPORTANT:** Review ALL staged changes, not just the most recent work. The changelog entry must cover everything being committed. If multiple features, fixes, or changes are being committed together, document all of them.

**Format:**

```markdown
# Changelog

## [Unreleased]

### Added
- New feature description

### Changed
- Modified behavior description

### Fixed
- Bug fix description

### Removed
- Removed feature description
```

**Rules:**
- Add entry under `[Unreleased]` section
- Use appropriate category (Added/Changed/Fixed/Removed)
- Be concise but specific - what changed and why it matters
- If CHANGELOG.md doesn't exist, create it

## Step 3: Stage and Commit

```bash
git add -A  # Or specific files if preferred
git commit -m "$(cat <<'EOF'
Short summary in imperative mood (max 50 chars)

Longer description if needed. Explain what changed and why.
Keep lines under 72 characters.

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

**Commit message guidelines:**
- First line: imperative mood, max 50 chars ("Add feature" not "Added feature")
- Blank line after summary
- Body: explain what and why, not how
- Reference issues if applicable
- **Cover ALL changes:** Review `git diff --staged` to ensure the message describes everything being committed, not just the most recent work. If the user wants only a subset of changes committed, they will specify which ones.

## Step 4: Verify Success

```bash
scripts/verify_clean_tree.sh
git log -1  # Verify commit message looks correct
```

## Red Flags - STOP

- Tests failing → Fix before commit
- Linting errors → Fix before commit
- Type errors → Fix before commit
- No changelog entry → Add one
- Vague commit message → Rewrite it

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Skipping checks "to save time" | Checks catch bugs. Run them. |
| Committing with failing tests | Fix the test or the code |
| Forgetting changelog | Always update before commit |
| "WIP" or "fix" commit messages | Write meaningful messages |
| Not verifying after commit | Always check git status/log |
