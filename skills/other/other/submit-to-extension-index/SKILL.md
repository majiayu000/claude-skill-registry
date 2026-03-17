---
name: submit-to-extension-index
description: Complete workflow for submitting an extension to the 3D Slicer Extension Index
allowed-tools:
  - Bash
  - Read
  - Write
context: manual
---

# Submit to Extension Index Skill

Submit an extension to the 3D Slicer Extension Index.

## When to Use

- Ready to submit extension to the Slicer Extension Index
- All validation checks pass (`./scripts/validate_extension.sh`)

## Prerequisites

Before submitting:

1. Run validation: `./scripts/validate_extension.sh`
2. All checks must pass (0 failures)
3. Extension JSON file exists in repository root

## Submission Steps

### Step 1: Validate

```bash
./scripts/validate_extension.sh
```

Must show "Ready for submission!" before proceeding.

### Step 2: Fork ExtensionsIndex

```bash
gh repo fork Slicer/ExtensionsIndex --clone=false
```

### Step 3: Clone Fork and Create Branch

Get the GitHub username and extension name, then clone:

```bash
# Get values from current repo
GITHUB_USER=$(gh api user -q .login)
EXT_NAME=$(grep -oP 'project\(\K[^)]+' CMakeLists.txt)

cd /tmp
rm -rf ExtensionsIndex
gh repo clone $GITHUB_USER/ExtensionsIndex
cd ExtensionsIndex
git remote add upstream https://github.com/Slicer/ExtensionsIndex.git 2>/dev/null || true
git fetch upstream
git checkout -b add-$EXT_NAME upstream/main
```

### Step 4: Copy JSON and Commit

```bash
# Copy from the extension repository (adjust path as needed)
cp /path/to/extension/$EXT_NAME.json .
git add $EXT_NAME.json
git commit -m "Add $EXT_NAME extension"
git push -u origin add-$EXT_NAME
```

### Step 5: Fetch Current PR Template

**CRITICAL:** Always fetch the latest PR template - it may have changed!

```bash
# Fetch and save the current PR template
curl -s "https://raw.githubusercontent.com/Slicer/ExtensionsIndex/main/.github/PULL_REQUEST_TEMPLATE.md" > /tmp/pr_template.md

# Review the template
cat /tmp/pr_template.md
```

### Step 6: Create PR Body

Read the fetched template and:

1. Keep the "# New extension" section
2. Mark completed items with `[x]`
3. Leave incomplete items as `[ ]`
4. Delete sections that don't apply

**DO NOT** hardcode the template - always use the fetched version as the authoritative source.

### Step 7: Create PR

**Option A: GitHub Web Interface (Recommended)**

1. Go to https://github.com/Slicer/ExtensionsIndex/compare
2. Select your fork and branch
3. The PR template will auto-populate
4. Review each checklist item and mark `[x]` for completed items
5. Submit the PR

**Option B: CLI**

```bash
# Edit /tmp/pr_template.md to mark completed items with [x]
# Then create PR:
gh pr create --repo Slicer/ExtensionsIndex \
  --title "Add $EXT_NAME extension" \
  --body-file /tmp/pr_template.md
```

## Post-Submission

1. Wait for automated build tests
2. Respond to reviewer feedback
3. Extension appears in Extensions Manager after merge

Monitor PR: https://github.com/Slicer/ExtensionsIndex/pulls

## Troubleshooting

### Build Fails

Check CDash logs. Common issues:
- Missing dependencies in `build_dependencies`
- Wrong `build_subdirectory`
- CMakeLists.txt errors

### Extension Not Appearing

1. Verify PR was merged
2. Use Slicer Preview Release (not Stable)
3. Clear Extensions Manager cache
