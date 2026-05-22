---
name: release-rollback
description: Rollback a failed release by deleting tags and reverting version changes. Use when a release fails, needs to be cancelled, or when reverting a problematic release.
---

# Rollback Failed Release

Rollback a failed release by deleting the release and reverting version changes.

⚠️ **This will delete the release and revert version changes.**

---

## Current Situation Check

Check recent tags:
```bash
git tag -l --sort=-version:refname | head -5
```

Review which version needs to be rolled back.

---

## Rollback Process

### Step 1: Verify Version to Rollback

Confirm with the user:
- What is the version to rollback?
- Is this the correct version to rollback?

### Step 2: Run Rollback Script

Execute the rollback command:
```bash
npm run release:rollback <version>
```

Example:
```bash
npm run release:rollback 1.5.0-beta.3
```

### Step 3: What the Script Will Do

The rollback script performs:
- Delete local git tag for specified version
- Delete remote git tag for specified version
- Delete GitHub release for specified version
- Revert version changes in all files
- Clean up RELEASE_NOTES files
- Provide next steps

### Step 4: After Rollback

Post-rollback verification:
1. Check GitHub to confirm release is deleted
2. Verify tags are removed: `git tag -l`
3. Fix the issues that caused the failure
4. Run: `npm run release:check` to validate fixes

### Step 5: Create New Release

Once issues are fixed, create new release:
- For beta: Use release-beta skill
- For stable: Use release-stable skill

---

## Common Rollback Scenarios

### Build Failed
- Fix build errors
- Run: `npm run build` to test
- Run: `npm run test:smoke`
- Re-run validation

### Linting/Type Errors
- Run: `npm run lint` to auto-fix
- Run: `npm run type-check` to verify
- Fix reported issues
- Re-run validation

### Version Mismatch
- Check all version files are synced:
  - [package.json](package.json)
  - [manifest.json](custom_components/linus_dashboard/manifest.json)
  - [const.py](custom_components/linus_dashboard/const.py)
- Re-run bump command

### Validation Failed
- Run: `npm run release:check`
- Address all errors and warnings
- Fix issues systematically
- Re-run validation

---

## Usage Example

```bash
# Rollback beta release
/release-rollback 2.0.0-beta.3

# Rollback stable release
/release-rollback 1.5.0
```

This requires the version number to rollback.

---

## Important Notes

- **Destructive operation:** Cannot be undone easily
- **Confirm version:** Double-check before proceeding
- **Fix root cause:** Address the issue that caused failure
- **Re-validate:** Run all checks before creating new release
- **Communication:** If release was public, inform users

---

## Rollback Checklist

Before proceeding with rollback:
- [ ] Identified the version to rollback
- [ ] Confirmed the version is correct
- [ ] Understood why the release failed
- [ ] Ready to fix the underlying issue

After rollback:
- [ ] Verified tag deletion locally and remotely
- [ ] Confirmed GitHub release deletion
- [ ] Fixed the root cause issue
- [ ] Ran validation checks
- [ ] Ready for new release attempt
