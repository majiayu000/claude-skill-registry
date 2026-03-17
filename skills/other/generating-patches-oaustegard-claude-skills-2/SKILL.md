---
name: generating-patches
description: Generates git patch files from codebase modifications for local application. Use when user mentions patch, diff, export changes, bring changes back, apply locally, or after editing uploaded codebases.
metadata:
  version: 0.1.0
---

# Generating Patches

Generate portable git patch files from codebase modifications, enabling users to apply Claude's edits to their local repositories.

## When to Use

Activate after modifying files in an uploaded codebase when the user needs to transfer changes back to their local environment. Typical workflow: user uploads zip → Claude edits files → this skill exports changes as a patch.

## Prerequisites

Verify git is available and the working directory is a git repository (or can be initialized as one):

```bash
git status 2>/dev/null || git init
```

If working with an uploaded codebase that lacks git history, initialize and create a baseline commit before making edits:

```bash
git init
git add -A
git commit -m "Baseline: original uploaded state"
```

## Generating the Patch

After completing edits, generate a unified diff:

```bash
# For uncommitted changes (working tree modifications)
git diff > /mnt/user-data/outputs/changes.patch

# If changes are staged but not committed
git diff --cached > /mnt/user-data/outputs/changes.patch

# For both staged and unstaged
git diff HEAD > /mnt/user-data/outputs/changes.patch
```

For committed changes (preserves commit messages and metadata):

```bash
# All commits since baseline
git format-patch --stdout baseline..HEAD > /mnt/user-data/outputs/changes.patch

# Or specify number of commits
git format-patch --stdout -n 3 > /mnt/user-data/outputs/changes.patch
```

## Handling Edge Cases

**Binary files**: Git diff excludes binaries by default. Warn the user if binary files were modified:

```bash
git diff --name-only --diff-filter=M | xargs file | grep -v "ASCII\|UTF-8\|empty"
```

**Large patches**: For extensive changes, consider splitting by directory or file type:

```bash
git diff -- "*.py" > /mnt/user-data/outputs/python-changes.patch
git diff -- src/ > /mnt/user-data/outputs/src-changes.patch
```

**No changes detected**: Verify files were actually modified. Common issues:
- Edits made to copies outside the git tree
- Files not tracked by git (need `git add` first)

## Output Requirements

Always output to `/mnt/user-data/outputs/` with a descriptive filename. Provide the download link:

```markdown
[Download changes.patch](computer:///mnt/user-data/outputs/changes.patch)
```

## User Instructions

Include these instructions with every patch delivery:

---

**To apply this patch locally:**

```bash
cd /path/to/your/repo

# Preview changes (dry run)
git apply --check changes.patch

# Apply to working tree
git apply changes.patch
```

**If using format-patch output (includes commit metadata):**

```bash
git am changes.patch
```

**Troubleshooting:**

- `git apply --reject changes.patch` — applies what it can, writes `.rej` files for conflicts
- `git apply -R changes.patch` — reverses a previously applied patch
- `git apply --3way changes.patch` — enables three-way merge for conflicts

---

## Optional: PR Description

When requested, generate a pull request description from the patch:

```bash
# Extract summary of changes
echo "## Summary"
git diff --stat
echo ""
echo "## Changes"
git diff --name-only | while read f; do echo "- \`$f\`"; done
```

Combine with a brief description of what was changed and why, suitable for GitHub PR body.
