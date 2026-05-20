---
skill: audit-and-fix
description: Security audit with automatic fixes for vulnerabilities
arguments: package names, glob pattern, or '.' for all
---

# Security Audit: $ARGUMENTS

Scan for vulnerabilities and automatically fix them in an isolated worktree.

## Process

### 1. Create Isolated Worktree

```bash
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
WORKTREE_PATH="../audit-fix-$TIMESTAMP"
git worktree add "$WORKTREE_PATH" -b "security-audit-$TIMESTAMP"
cd "$WORKTREE_PATH"
```

### 2. Run Security Audit

```bash
npm audit --json > audit-report.json
```

If no vulnerabilities, clean up and exit.

### 3. Categorize by Severity

Parse audit results:
- **Critical**: Immediate action required
- **High**: Serious risk, patch ASAP
- **Moderate**: Should fix soon
- **Low**: Fix when convenient

### 4. Determine Strategy

- **1-3 packages**: Update sequentially
- **4+ packages**: Use parallel Task subagents (2 packages per agent)

### 5. Update Packages

For each package:
```bash
npm install <package>@latest
```

Then validate:
```bash
npm run build && npm run lint && npm test
```

If validation fails, revert to previous version.

### 6. Post-Audit Scan

```bash
npm audit
```

Compare before/after vulnerability counts.

### 7. Report and Prompt

Generate security report with:
- Initial vs remaining vulnerabilities
- Successfully updated packages
- Failed updates with reasons
- Recommendations for remaining issues

Prompt: merge fixes, keep for review, or discard.

### 8. Cleanup

```bash
git worktree remove "$WORKTREE_PATH"
git branch -d "security-audit-$TIMESTAMP"
```

## Parallel Execution

When >3 packages, split into groups and launch Task subagents:

```
Task({
  subagent_type: 'general-purpose',
  prompt: 'Update packages X, Y with full validation...',
  run_in_background: true
})
```

Collect results from all agents before generating final report.
