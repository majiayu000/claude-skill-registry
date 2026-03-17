---
name: "feature-continue"
description: "Resume work on existing feature clone"
argument-hint: "[feature-description]"
---

Continues work on an existing feature clone with proper context analysis.

## Feature description from user input
"$ARGUMENTS"

### Feature Description Validation
If empty or missing: "Error: Feature description is required. Please provide a detailed description of the feature you want to continue implementing."

## Process

### Step 1: Search for Existing Clone
List existing clones in _clones/ directory and try to match the feature description:
```bash
ls -1 _clones/
```

If found → Continue to Step 3 (navigate)
If not found → Continue to Step 2

### Step 2: Check for Remote Branch
Check if a remote feature branch exists that matches the description:
```bash
git fetch --prune
git branch -r
```

Review the list of remote branches and match one to the user's feature description.

If found → Run `/create-clone` with the matched branch name, then continue to Step 4
If not found → Exit with error:
- Tell user: "Feature branch not found locally or remotely"
- Suggest: "Use /create-clone <feature-description> to create a new feature clone"

### Step 3: Navigate to Feature Clone
```bash
cd _clones/FEATURE_NAME
```

### Step 4: Sync with Main
Run `/sync` to commit and push.

### Step 5: Run Feature Loop
Run `/feature-loop-scheme` to execute the full development workflow.
