---
name: "create-clone"
description: "Create isolated git clone for feature"
argument-hint: "[feature-description]"
---

Creates a git clone for isolated feature development. Handles both new features and existing remote branches.

## Feature description from user input
"$ARGUMENTS"

### Feature Description Validation
  - If empty or missing: "Error: Feature description is required. Please provide a detailed description."

## Process

### Step 1: Parse Feature Description
- Decide on feature name based on description
- Convert feature name to kebab-case for branch naming

### Step 2: Check for Existing Remote Branch
```bash
git fetch --prune
git branch -r | grep "$FEATURE_NAME" || true
```

- If a matching remote branch exists → **Existing branch mode**
- If no match → **New branch mode**

### Step 3: Create Git Clone

```bash
ORIGINAL_REPO_DIR=$(pwd)
REPO_URL=$(git config --get remote.origin.url)
mkdir -p _clones
```

**New branch mode:**
```bash
git clone -b main "$REPO_URL" _clones/$FEATURE_NAME
cd _clones/$FEATURE_NAME
git checkout -b $FEATURE_NAME
git push -u origin $FEATURE_NAME
```

**Existing branch mode:**
```bash
git clone -b $FEATURE_NAME "$REPO_URL" _clones/$FEATURE_NAME
cd _clones/$FEATURE_NAME
```

### Step 4: Sync with Main
Run the sync skill to commit and push.

### Step 5: Symlink Environment Files
```bash
bash ~/.claude/skills/create-clone/symlink_env_files.sh "$ORIGINAL_REPO_DIR" "_clones/$FEATURE_NAME"
```

### Step 6: Setup Environment
```bash
bash ~/.claude/skills/create-clone/setup_project_env.sh
```

### Step 7: Notify User
Tell user:
- The clone has been created at `_clones/$FEATURE_NAME`
- The branch `$FEATURE_NAME` is tracking remote

### Step 8: Change to Feature Directory
Change to the feature clone directory.

**FROM NOW ALL NEW WORK SHOULD ONLY BE DONE IN THIS FEATURE DIR**
