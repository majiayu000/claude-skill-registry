---
description: Prepare a milestone for release by verifying success criteria, checking backwards compatibility, ensuring ticket tagging, and reviewing documentation.
argument-hint: <version> [--deploy-aws] [--skip-docs]
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, Task, WebFetch, Skill
context: full
---

# Release Preparation Workflow

Comprehensive release preparation for a GitHub milestone.

## Arguments

- `$ARGUMENTS`: The milestone version (e.g., "v0.4.0" or "0.4.0")
  - `--deploy-aws`: Deploy a test stack to AWS to verify features (optional)
  - `--skip-docs`: Skip documentation review (optional)

## Workflow Steps

Execute these steps in order, providing progress updates to the user.

### 1. Milestone Status Check

Use the `/milestone` skill to get the current status:

```
/milestone <version>
```

Then fetch the full narrative issue body for success criteria:

```bash
gh issue view <epic-number> --json number,title,body
```

Report: milestone progress, open vs closed issues, narrative theme and success criteria.

### 2. Explore Code Changes

Compare changes between the previous version tag and current branch:

```bash
# List commits since previous version
git log v<prev>..<current> --oneline

# Show changed files
git diff v<prev>..<current> --stat

# For public API changes, examine:
# - src/zae_limiter/__init__.py (exports)
# - src/zae_limiter/limiter.py (RateLimiter methods)
# - src/zae_limiter/models.py (data models)
# - src/zae_limiter/cli.py (CLI commands)
```

Report: Summary of changes organized by area (API, CLI, infra, docs).

### 3. Verify Backwards Compatibility

Check that changes are backwards compatible:

- **New parameters**: Must have defaults (optional)
- **New methods**: Addition only, no removals
- **Schema changes**: Check for migration support
- **CLI changes**: New flags should have defaults

Look for:
- Function signatures with new required parameters
- Removed public exports in `__init__.py`
- Breaking changes in models

Report: Compatibility assessment with specific findings.

### 4. Verify Success Criteria (Optional: AWS Deployment)

If `--deploy-aws` is specified OR if success criteria require runtime verification:

1. Deploy a test stack:
   ```bash
   AWS_PROFILE=zeroae-code/AWSPowerUserAccess uv run zae-limiter deploy \
     --name test-release-prep \
     --region us-east-1 \
     --permission-boundary "arn:aws:iam::aws:policy/PowerUserAccess" \
     --role-name-format "PowerUserPB-{}"
   ```

2. Write and run verification script based on success criteria from narrative

3. Clean up:
   ```bash
   AWS_PROFILE=zeroae-code/AWSPowerUserAccess uv run zae-limiter delete \
     --name test-release-prep --yes
   ```

Report: Success criteria verification results (pass/fail for each).

### 5. Tag Untracked Work

Find and tag any commits/PRs between versions that aren't in the milestone:

```bash
# Find PRs merged since previous version
gh pr list --state merged --json number,title,mergedAt,milestone \
  --jq '.[] | select(.milestone == null or .milestone.title != "vX.Y.Z")'

# Find closed issues that may be missing milestone
gh issue list --state closed --json number,title,closedAt,milestone \
  --jq '.[] | select(.milestone == null)'
```

For each untracked item:
1. Check if it was part of the release work
2. Assign to milestone if appropriate
3. Update narrative issue with "Ad-hoc Tickets" section

### 6. Documentation Review (unless --skip-docs)

Review documentation for completeness:

1. Check narrative issue for documentation requirements
2. Read relevant docs files:
   - `CLAUDE.md` - developer reference
   - `docs/` - user-facing documentation
3. Verify examples match current API
4. Update any outdated sections

Report: Documentation status (up-to-date / needs updates).

### 7. Update Narrative Issue

Update the epic issue with:
- Verified success criteria (check off completed items)
- Ad-hoc tickets section if untracked work was found
- Documentation status

```bash
gh issue edit <epic-number> --body "<updated-body>"
```

### 8. Final Summary

Provide a release readiness summary:

```
## Release Readiness: vX.Y.Z

**Status:** Ready / Needs Work

### Checklist
- [ ] All success criteria verified
- [ ] Backwards compatible
- [ ] All work tagged to milestone
- [ ] Documentation up-to-date
- [ ] Open issues: N remaining

### Open Items (if any)
- Issue #X: <title>

### Next Steps
1. Close remaining issues (if any)
2. Close narrative epic #X
3. Create release tag: `git tag vX.Y.Z && git push origin vX.Y.Z`
```

## Important Notes

- Always use `AWS_PROFILE=zeroae-code/AWSPowerUserAccess` for AWS operations
- Use permission boundary for Lambda stacks (see `.claude/rules/aws-testing.md`)
- Keep the user informed of progress at each step
- Ask for confirmation before making changes to issues/PRs
- If any step fails, report the failure and ask how to proceed
