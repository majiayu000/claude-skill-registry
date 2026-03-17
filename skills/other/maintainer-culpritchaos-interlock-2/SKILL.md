---
name: maintainer
description: PR triage, merge receipts, CI sanity, artifact/PII hygiene
allowed_tools:
  - git
  - npm
  - npx
  - python
  - py
  - pwsh
  - powershell
denied_patterns:
  - rm -rf
  - del /
  - Remove-Item
  - format
  - diskpart
---

# Maintainer Skill

Use this skill for PR triage, merge preparation, and repository hygiene tasks.

## When to Use

- Reviewing PRs for merge readiness
- Running CI sanity checks locally
- Checking for PII or artifact leaks
- Preparing merge receipts
- Triaging issues and Dependabot PRs

## Pre-Merge Checklist

Before requesting merge approval, complete ALL items:

- [ ] `npm run lint` passes
- [ ] `npm run validate` passes (if applicable)
- [ ] `pwsh -File tools/precommit_safety_scan.ps1` passes
- [ ] No PII paths in staged files (`C:\Users`, `/Users/`, `/home/`)
- [ ] No receipt/artifact files staged
- [ ] GitHub Actions CI is green
- [ ] Merge receipt comment posted on PR

## Merge Receipt Template

Post this on the PR:

```markdown
## Merge Receipt

**Summary**: [Brief description of changes]

**Risk Assessment**: [Low/Medium/High] - [justification]

**Rollback Plan**: `git revert <commit>` or [specific steps]

**Local Checks**:
- `npm run lint` - PASS
- `npm run validate` - PASS
- `tools/precommit_safety_scan.ps1` - PASS

**Confirmation**: No receipts, artifacts, or PII committed.

---
Ready for: `APPROVE MERGE PR #<number>`
```

## Safety Commands

```bash
# Check for PII in staged files
git diff --cached | grep -E "(C:\\\\Users|/Users/|/home/)"

# Check git status
git status

# Run safety scan
pwsh -File tools/precommit_safety_scan.ps1

# Lint check
npm run lint

# Validation tests
npm run validate
```

## Prohibited Actions

This skill does NOT authorize:
- Merging without explicit `APPROVE MERGE PR #<number>` from Rob
- Force pushing to protected branches
- Deleting files or branches without approval
- Bypassing safety scans
