---
name: finish-feature
description: Finish a feature by merging changes back, cleaning up the copy, and creating a release. This is the high-level workflow that orchestrates merge-back, cleanup-copy, and release-pr.
disable-model-invocation: true
allowed-tools:
  - Bash
---

# Finish Feature

High-level workflow to complete a feature: merge back, clean up, and optionally release.

## What it does

This is a **workflow** that orchestrates multiple skills in sequence:

1. **Merge back** - Brings changes from the copy to the original (`/merge-back`)
2. **Review** - Shows a summary of changes for the user to review
3. **Cleanup** - Deletes the copy after confirmation (`/cleanup-copy`)
4. **Release** (optional) - Creates a tag and pushes to main (`/release-pr`)

## Usage

```
/finish-feature <feature-name>
```

## How to execute

**This MUST be run from the ORIGINAL project directory** (not the copy).

### Step 1: Merge back

```bash
bash .claude/skills/merge-back/scripts/merge-back.sh "<feature-name>"
```

If this fails (tests fail, merge conflicts), STOP and help the user resolve the issue before continuing.

### Step 2: Show changes for review

After a successful merge, show the user what changed:

```bash
git log --oneline main..merge/<feature-name>
echo "---"
git diff main..merge/<feature-name> --stat
```

Tell the user: "Here are the changes from `<feature-name>`. Review them and confirm to proceed with cleanup and release."

### Step 3: Wait for user confirmation

**IMPORTANT**: Do NOT proceed to cleanup without explicit user confirmation. Ask:
"Changes look good? Should I proceed to clean up the copy and create a release?"

### Step 4: Cleanup copy

Only after user confirms:

```bash
bash .claude/skills/cleanup-copy/scripts/cleanup-copy.sh "<feature-name>"
```

### Step 5: Ask about release

Ask the user: "Do you want to create a release? I can auto-detect the version bump (patch/minor/major) based on commit messages, or you can specify one."

### Step 6: Release (if user wants)

Only if the user confirms:

```bash
bash .claude/skills/release-pr/scripts/release-pr.sh [patch|minor|major]
```

## Important

- This workflow is **interactive** - it pauses for user confirmation at key points
- If ANY step fails, STOP and help the user resolve the issue
- The merge-back step runs tests in the copy before merging
- The cleanup step warns about unmerged changes
- The release step is OPTIONAL - the user may want to review more before releasing
- Never add `Co-Authored-By` headers to any commits
