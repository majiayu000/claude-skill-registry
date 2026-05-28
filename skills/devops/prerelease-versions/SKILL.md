---
name: prerelease-versions
description: Alpha/beta/RC tagging patterns and GitHub pre-release workflows for managing pre-production releases. Use when creating alpha releases, beta releases, release candidates, managing pre-release branches, testing release workflows, or when user mentions pre-release, alpha, beta, RC, release candidate, or pre-production versioning.
allowed-tools: Bash, Read, Write, Edit
---

# Prerelease Versions

Pre-release version management patterns including alpha, beta, and release candidate (RC) tagging with GitHub pre-release workflows.

## Overview

This skill provides comprehensive patterns for managing pre-release versions throughout the software development lifecycle. It supports semantic versioning pre-release identifiers (alpha, beta, rc) with GitHub Actions automation for safe pre-production testing.

## Pre-release Version Format

Semantic versioning pre-release format:
```
<major>.<minor>.<patch>-<prerelease>.<number>
```

Examples:
- `1.0.0-alpha.1` - First alpha release
- `1.0.0-alpha.2` - Second alpha release
- `1.0.0-beta.1` - First beta release
- `1.0.0-beta.2` - Second beta release
- `1.0.0-rc.1` - First release candidate
- `1.0.0-rc.2` - Second release candidate
- `1.0.0` - Stable release (promoted from RC)

## Pre-release Types

### Alpha (α)

**Purpose**: Internal testing, highly unstable, breaking changes expected

**Characteristics**:
- Incomplete features
- No stability guarantees
- Frequent breaking changes
- Internal team only
- Rapid iteration

**When to use**:
- Feature development in progress
- API design validation
- Internal dogfooding
- Proof of concept testing

### Beta (β)

**Purpose**: External testing, feature complete but may have bugs

**Characteristics**:
- Feature complete
- API mostly stable
- Known bugs expected
- Open to early adopters
- Limited breaking changes

**When to use**:
- Feature freeze reached
- Ready for wider testing
- Gathering user feedback
- Performance optimization
- Documentation review

### Release Candidate (RC)

**Purpose**: Final pre-release testing, production ready unless critical bugs found

**Characteristics**:
- Fully tested features
- API stable
- Only critical bug fixes
- Production environment testing
- No new features

**When to use**:
- All tests passing
- Documentation complete
- Ready for production
- Final validation
- Stakeholder approval

## Scripts

All scripts are located in `scripts/` and provide functional pre-release management.

### 1. create-prerelease.sh

Create a new pre-release version with automatic version calculation.

**Usage**:
```bash
bash scripts/create-prerelease.sh <prerelease_type> <base_version>
```

**Parameters**:
- `prerelease_type`: alpha, beta, or rc
- `base_version`: Target stable version (e.g., 1.0.0)

**Example**:
```bash
# Create first alpha release for version 1.0.0
bash scripts/create-prerelease.sh alpha 1.0.0
# Output: 1.0.0-alpha.1

# Create next alpha release
bash scripts/create-prerelease.sh alpha 1.0.0
# Output: 1.0.0-alpha.2
```

**Features**:
- Auto-increments pre-release number
- Updates VERSION file
- Updates manifest files (package.json, pyproject.toml)
- Creates git tag
- Validates semantic versioning format

### 2. promote-prerelease.sh

Promote a pre-release to the next stage or stable release.

**Usage**:
```bash
bash scripts/promote-prerelease.sh <current_version>
```

**Promotion Path**:
```
alpha.N → beta.1
beta.N → rc.1
rc.N → stable (removes pre-release identifier)
```

**Example**:
```bash
# Promote alpha to beta
bash scripts/promote-prerelease.sh 1.0.0-alpha.3
# Output: 1.0.0-beta.1

# Promote beta to RC
bash scripts/promote-prerelease.sh 1.0.0-beta.2
# Output: 1.0.0-rc.1

# Promote RC to stable
bash scripts/promote-prerelease.sh 1.0.0-rc.2
# Output: 1.0.0
```

**Features**:
- Automatic promotion logic
- Version file updates
- Manifest synchronization
- Git tag creation
- Changelog generation

### 3. test-prerelease.sh

Validate pre-release version format and readiness.

**Usage**:
```bash
bash scripts/test-prerelease.sh <version>
```

**Validations**:
- Semantic versioning format
- Pre-release identifier validity
- Version consistency across files
- Git tag availability
- Changelog entry presence

**Exit Codes**:
- `0`: All validations passed
- `1`: Format validation failed
- `2`: Consistency check failed
- `3`: Git tag conflict
- `4`: Changelog missing

**Example**:
```bash
# Validate alpha release
bash scripts/test-prerelease.sh 1.0.0-alpha.1

# Validate RC release
bash scripts/test-prerelease.sh 1.0.0-rc.1
```

## Templates

All templates are located in `templates/` and provide production-ready configurations.

### 1. github-prerelease-workflow.yml

GitHub Actions workflow for automated pre-release creation and testing.

**Location**: `templates/github-prerelease-workflow.yml`

**Features**:
- Automatic pre-release detection from branch name
- Parallel testing for alpha/beta/RC
- Pre-release asset uploading
- GitHub pre-release flag setting
- Notification integration

**Trigger Branches**:
- `alpha/*` → Creates alpha releases
- `beta/*` → Creates beta releases
- `release/*` → Creates RC releases

**Usage**:
```bash
# Copy to project
cp templates/github-prerelease-workflow.yml .github/workflows/prerelease.yml

# Customize as needed
vim .github/workflows/prerelease.yml
```

### 2. alpha-version-tag.template

Git tag annotation template for alpha releases.

**Location**: `templates/alpha-version-tag.template`

**Format**:
```
Alpha Release v{VERSION}

🚧 INTERNAL TESTING ONLY

This is an unstable alpha release for internal testing.
Breaking changes are expected in future releases.

Changes:
{CHANGELOG}

Testing:
- [ ] Unit tests passed
- [ ] Integration tests passed
- [ ] Manual testing completed

DO NOT USE IN PRODUCTION
```

### 3. beta-version-tag.template

Git tag annotation template for beta releases.

**Location**: `templates/beta-version-tag.template`

**Format**:
```
Beta Release v{VERSION}

🧪 EARLY ACCESS

This is a beta release for early adopters and testing.
Features are complete but bugs may exist.

Changes:
{CHANGELOG}

Testing:
- [ ] All tests passing
- [ ] Performance benchmarks completed
- [ ] Documentation reviewed
- [ ] Known issues documented

Use with caution in production environments.
```

### 4. rc-version-tag.template

Git tag annotation template for release candidates.

**Location**: `templates/rc-version-tag.template`

**Format**:
```
Release Candidate v{VERSION}

✅ PRODUCTION READY (pending final validation)

This release candidate is considered stable and ready for production
unless critical issues are discovered during final testing.

Changes:
{CHANGELOG}

Validation:
- [x] All tests passing
- [x] Performance validated
- [x] Documentation complete
- [x] Security audit completed
- [ ] Production deployment tested

Expected stable release: {EXPECTED_DATE}
```

### 5. prerelease-config.json

Configuration template for pre-release workflow settings.

**Location**: `templates/prerelease-config.json`

**Structure**:
```json
{
  "prerelease": {
    "alpha": {
      "branch_pattern": "alpha/*",
      "auto_increment": true,
      "testing_required": ["unit", "integration"],
      "notification_channels": ["slack-dev"],
      "retention_days": 30
    },
    "beta": {
      "branch_pattern": "beta/*",
      "auto_increment": true,
      "testing_required": ["unit", "integration", "e2e"],
      "notification_channels": ["slack-qa", "slack-dev"],
      "retention_days": 90
    },
    "rc": {
      "branch_pattern": "release/*",
      "auto_increment": true,
      "testing_required": ["unit", "integration", "e2e", "performance"],
      "notification_channels": ["slack-releases", "slack-qa"],
      "retention_days": 180
    }
  }
}
```

## Examples

All examples are located in `examples/` and demonstrate real-world workflows.

### 1. alpha-workflow.md

Complete alpha release workflow from creation to promotion.

**Location**: `examples/alpha-workflow.md`

**Covers**:
- Creating alpha branch
- Initial alpha release
- Iterative alpha releases
- Bug fixes in alpha
- Promoting to beta

### 2. beta-workflow.md

Complete beta release workflow including feedback integration.

**Location**: `examples/beta-workflow.md`

**Covers**:
- Beta release creation
- User feedback collection
- Bug fix releases
- Feature freeze enforcement
- Promotion to RC

### 3. rc-workflow.md

Complete release candidate workflow to stable release.

**Location**: `examples/rc-workflow.md`

**Covers**:
- RC creation
- Production validation
- Hotfix handling
- Stakeholder approval
- Stable release promotion

### 4. multi-prerelease-pipeline.md

Managing multiple concurrent pre-release tracks.

**Location**: `examples/multi-prerelease-pipeline.md`

**Covers**:
- Parallel alpha/beta releases
- Feature branch integration
- Version conflict resolution
- Backport strategies

## Integration with Commands

This skill supports versioning plugin commands:

- **/versioning:bump** - Extended with `--prerelease` flag
- **/versioning:info** - Shows pre-release status
- **/versioning:rollback** - Supports pre-release rollback

## Best Practices

### Alpha Stage

1. **Release frequently** - Daily or per-feature releases
2. **Document breaking changes** - Track API changes
3. **Internal only** - Never expose to external users
4. **Fast iteration** - Rapid development cycles
5. **Version cleanup** - Archive old alphas regularly

### Beta Stage

1. **Feature freeze** - No new features, only bug fixes
2. **Wider testing** - Include early adopters
3. **Gather feedback** - Document user issues
4. **Performance testing** - Validate at scale
5. **Documentation review** - Ensure docs match features

### RC Stage

1. **Minimal changes** - Critical fixes only
2. **Production testing** - Test in production-like environment
3. **Stakeholder approval** - Get sign-off before stable
4. **Final documentation** - Complete all docs
5. **Release notes** - Prepare comprehensive release notes

### General

1. **Clear communication** - Announce each pre-release
2. **Version consistency** - Keep all files synchronized
3. **Automated testing** - Use CI/CD for all pre-releases
4. **GitHub pre-release flag** - Mark appropriately in GitHub
5. **Retention policy** - Clean up old pre-releases

## Troubleshooting

### Version Number Conflicts

If version already exists:
```bash
# Check existing tags
git tag -l "v1.0.0-*"

# Delete conflicting tag
git tag -d v1.0.0-alpha.1

# Recreate with correct number
bash scripts/create-prerelease.sh alpha 1.0.0
```

### Promotion Issues

If promotion fails:
```bash
# Validate current version
bash scripts/test-prerelease.sh 1.0.0-alpha.3

# Check promotion path
# alpha.N → beta.1 → rc.1 → stable

# Force promotion if needed
bash scripts/promote-prerelease.sh 1.0.0-alpha.3 --force
```

### GitHub Workflow Failures

If GitHub Actions workflow fails:
```bash
# Check workflow logs
gh run list --workflow=prerelease.yml

# View specific run
gh run view <run-id>

# Re-run failed jobs
gh run rerun <run-id>
```

### Inconsistent Versions

If versions are out of sync:
```bash
# Check all version locations
bash scripts/test-prerelease.sh 1.0.0-beta.1

# Manual sync if needed
# Update VERSION file
echo '{"version": "1.0.0-beta.1"}' > VERSION

# Update package.json
npm version 1.0.0-beta.1 --no-git-tag-version

# Update pyproject.toml
sed -i 's/version = .*/version = "1.0.0-beta.1"/' pyproject.toml
```

## See Also

- @plugins/versioning/skills/version-manager/SKILL.md - Core version management
- @plugins/versioning/commands/bump.md - Version bumping command
- @plugins/versioning/agents/release-validator.md - Release validation agent
