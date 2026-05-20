---
name: when-releasing-software-use-github-release-management
description: Comprehensive GitHub release orchestration with AI swarm coordination for automated versioning, testing, deployment, and rollback management. Coordinates release-manager, cicd-engineer, tester, and docs-writer agents through hierarchical topology to handle semantic versioning, changelog generation, release notes, deployment validation, and post-release monitoring. Supports multiple release strategies (rolling, blue-green, canary) and automated rollback. Use when creating releases, managing deployments, or coordinating version updates.
agents:
  - release-manager
  - cicd-engineer
  - tester
  - reviewer
  - docs-writer
topology: hierarchical
mcp_tools:
  - mcp__claude-flow__swarm_init
  - mcp__claude-flow__agent_spawn
  - mcp__claude-flow__task_orchestrate
---

# GitHub Release Management Skill

## Overview

Orchestrate end-to-end software release processes with intelligent agent coordination. This skill automates version bumping, changelog generation, release candidate testing, deployment orchestration, post-release validation, and rollback procedures for GitHub-hosted projects using comprehensive CI/CD integration.

## When to Use This Skill

Activate this skill when creating production releases with automated validation, coordinating multi-environment deployments (staging, production), generating release notes and changelogs automatically, managing semantic versioning across projects, implementing deployment strategies (rolling, blue-green, canary), handling hotfix releases and emergency patches, or establishing release automation for new projects.

Use for both small single-repository releases and complex multi-service deployments, scheduled regular releases or on-demand deployments, and establishing release governance and compliance.

## Agent Coordination Architecture

### Swarm Topology

Initialize a **hierarchical topology** with release-manager as coordinator overseeing specialized deployment, testing, and documentation agents. Hierarchical structure ensures coordinated decision-making for critical release operations.

```bash
# Initialize hierarchical swarm for release management
npx claude-flow@alpha swarm init --topology hierarchical --max-agents 8 --strategy specialized
```

### Specialized Agent Roles

**Release Manager** (`release-manager`): Top-level coordinator that oversees entire release process. Makes go/no-go decisions, coordinates deployment timing, manages rollback decisions, and ensures release quality standards. Acts as release captain.

**CI/CD Engineer** (`cicd-engineer`): Manages build pipelines, deployment automation, infrastructure provisioning, and deployment strategy execution. Handles technical deployment mechanics and environment configuration.

**Test Engineer** (`tester`): Validates release candidates through automated testing, regression testing, performance testing, and smoke testing. Verifies deployment success and monitors post-deployment health.

**Code Reviewer** (`reviewer`): Performs final code review of release branch, validates security compliance, checks for last-minute issues, and approves release artifacts.

**Documentation Writer** (`docs-writer`): Generates release notes, updates changelogs, creates deployment runbooks, and documents breaking changes. Ensures comprehensive release documentation.

## Release Management Workflows (SOP)

### Workflow 1: Standard Release (Major/Minor/Patch)

Execute full release cycle from version bump to production deployment.

**Phase 1: Pre-Release Preparation**

**Step 1.1: Initialize Release Swarm**

```bash
# Set up hierarchical release swarm
mcp__claude-flow__swarm_init topology=hierarchical maxAgents=8 strategy=specialized

# Spawn release team
mcp__claude-flow__agent_spawn type=coordinator name=release-manager
mcp__claude-flow__agent_spawn type=coder name=cicd-engineer
mcp__claude-flow__agent_spawn type=researcher name=tester
mcp__claude-flow__agent_spawn type=analyst name=reviewer
mcp__claude-flow__agent_spawn type=researcher name=docs-writer
```

**Step 1.2: Determine Release Version**

```plaintext
Task("Release Manager", "
  Determine next release version:

  1. Fetch current version from package.json / Cargo.toml / VERSION file
  2. Analyze commits since last release using git log
  3. Classify changes: breaking|features|fixes|docs
  4. Apply semantic versioning rules:
     - Breaking changes → major version bump
     - New features → minor version bump
     - Bug fixes only → patch version bump
  5. Check for forced version override in environment

  Use scripts/semver.sh for version calculation
  Store version decision in memory: release/version
  Run hooks: npx claude-flow@alpha hooks pre-task --description 'version determination'
", "release-manager")
```

```bash
# Calculate next version
NEXT_VERSION=$(bash scripts/semver.sh calculate \
  --current $(cat VERSION) \
  --commits-since-tag "v$(cat VERSION)" \
  --bump-strategy "auto")
```

**Step 1.3: Create Release Branch**

```bash
# Create release branch
git checkout -b "release/v${NEXT_VERSION}"
git push origin "release/v${NEXT_VERSION}"
```

**Step 1.4: Update Version Files**

```plaintext
Task("CI/CD Engineer", "
  Update version across project files:

  1. Update package.json version field
  2. Update Cargo.toml version (if Rust project)
  3. Update VERSION or version.txt file
  4. Update hardcoded versions in documentation
  5. Update version constants in source code
  6. Commit changes: 'chore: bump version to ${NEXT_VERSION}'

  Use scripts/version-bumper.sh for automation
  Store version update status in memory: release/version-update
", "cicd-engineer")
```

**Phase 2: Release Candidate Testing**

**Step 2.1: Build Release Candidate**

```plaintext
Task("CI/CD Engineer", "
  Build release candidate artifacts:

  1. Trigger CI build for release branch
  2. Run full test suite (unit, integration, e2e)
  3. Build production artifacts (binaries, containers, packages)
  4. Sign artifacts with release signing key
  5. Upload artifacts to staging repository
  6. Generate artifact checksums

  Use scripts/build-release.sh
  Store build artifacts in memory: release/artifacts
", "cicd-engineer")
```

**Step 2.2: Deploy to Staging Environment**

```bash
# Deploy release candidate to staging
bash scripts/deploy.sh \
  --environment "staging" \
  --version "${NEXT_VERSION}" \
  --strategy "rolling" \
  --wait-for-healthy true
```

**Step 2.3: Execute Release Validation Suite**

```plaintext
Task("Test Engineer", "
  Validate release candidate in staging:

  1. Run smoke tests against staging deployment
  2. Execute regression test suite
  3. Perform load testing with production-like traffic
  4. Validate API compatibility and contracts
  5. Check database migrations successful
  6. Test rollback procedure
  7. Verify monitoring and alerting working

  Use scripts/release-validation.sh
  Store test results in memory: release/validation
", "tester")
```

**Step 2.4: Security and Compliance Review**

```plaintext
Task("Code Reviewer", "
  Perform final security and compliance checks:

  1. Scan for known vulnerabilities (npm audit, cargo audit)
  2. Check for exposed secrets in release branch
  3. Validate license compliance
  4. Review CHANGELOG for security advisories
  5. Check compliance with organizational policies
  6. Approve or flag issues blocking release

  Use references/security-checklist.md
  Store review status in memory: release/security-review
", "reviewer")
```

**Phase 3: Release Artifact Generation**

**Step 3.1: Generate Changelog**

```plaintext
Task("Documentation Writer", "
  Generate comprehensive changelog:

  1. Fetch all commits since last release
  2. Categorize by type: breaking|features|fixes|docs|chore
  3. Extract issue references and PR numbers
  4. Format using references/changelog-template.md
  5. Highlight breaking changes prominently
  6. Include migration guide if breaking changes present

  Use scripts/changelog-generator.sh
  Store changelog in memory: release/changelog
", "docs-writer")
```

**Step 3.2: Write Release Notes**

```plaintext
Task("Documentation Writer", "
  Create user-facing release notes:

  1. Summarize major features and improvements
  2. Document breaking changes with upgrade path
  3. List bug fixes with issue references
  4. Include known issues and workarounds
  5. Add installation/upgrade instructions
  6. Acknowledge contributors

  Use references/release-notes-template.md
  Store release notes in memory: release/notes
", "docs-writer")
```

**Step 3.3: Update Documentation**

```bash
# Update version in documentation
bash scripts/docs-updater.sh \
  --version "${NEXT_VERSION}" \
  --changelog "CHANGELOG.md" \
  --docs-dir "docs/"
```

**Phase 4: Production Deployment**

**Step 4.1: Create GitHub Release (Draft)**

```bash
# Create draft GitHub release
bash scripts/github-api.sh create-release \
  --repo <owner/repo> \
  --tag "v${NEXT_VERSION}" \
  --name "Version ${NEXT_VERSION}" \
  --body-file "references/release-notes-v${NEXT_VERSION}.md" \
  --draft true \
  --prerelease false
```

**Step 4.2: Go/No-Go Decision**

```plaintext
Task("Release Manager", "
  Make final go/no-go decision:

  1. Review all agent findings from memory
  2. Check validation test results: release/validation
  3. Verify security review passed: release/security-review
  4. Confirm stakeholder approval received
  5. Validate deployment window available
  6. Make final decision: proceed or abort

  Store decision in memory: release/go-no-go
", "release-manager")
```

**Step 4.3: Execute Production Deployment**

```plaintext
Task("CI/CD Engineer", "
  Deploy release to production:

  1. Select deployment strategy from references/deployment-strategies.md
     - Rolling: gradual instance replacement
     - Blue-Green: parallel environment swap
     - Canary: phased rollout with traffic splitting
  2. Execute deployment with chosen strategy
  3. Monitor deployment health metrics
  4. Validate deployment success criteria
  5. Keep rollback option available

  Use scripts/deploy.sh with strategy flag
  Store deployment status in memory: release/deployment
", "cicd-engineer")
```

Example deployment commands:

```bash
# Rolling deployment (default)
bash scripts/deploy.sh \
  --environment "production" \
  --version "${NEXT_VERSION}" \
  --strategy "rolling" \
  --wait-for-healthy true \
  --rollback-on-failure true

# Blue-Green deployment
bash scripts/deploy.sh \
  --environment "production" \
  --version "${NEXT_VERSION}" \
  --strategy "blue-green" \
  --traffic-switch-delay 300

# Canary deployment
bash scripts/deploy.sh \
  --environment "production" \
  --version "${NEXT_VERSION}" \
  --strategy "canary" \
  --canary-percentage "10,25,50,100" \
  --canary-delay-seconds 600
```

**Phase 5: Post-Release Validation**

**Step 5.1: Production Smoke Tests**

```plaintext
Task("Test Engineer", "
  Validate production deployment:

  1. Run production smoke test suite
  2. Validate critical user journeys
  3. Check error rates and latency metrics
  4. Verify monitoring dashboards showing healthy state
  5. Test rollback procedure (in separate environment)

  Use scripts/production-validation.sh
  Store validation results in memory: release/prod-validation
", "tester")
```

**Step 5.2: Publish GitHub Release**

Once production validated, publish the draft release:

```bash
# Publish GitHub release
bash scripts/github-api.sh publish-release \
  --repo <owner/repo> \
  --tag "v${NEXT_VERSION}"
```

**Step 5.3: Post-Release Monitoring**

```plaintext
Task("Release Manager", "
  Monitor post-release health:

  1. Track error rates for 24 hours post-release
  2. Monitor user reports and support tickets
  3. Watch for performance degradation
  4. Check for unexpected edge cases
  5. Prepare hotfix if critical issues discovered

  Use scripts/release-monitoring.sh
  Store monitoring data in memory: release/monitoring
", "release-manager")
```

**Step 5.4: Merge Release Branch**

```bash
# Merge release branch back to main
git checkout main
git merge --no-ff "release/v${NEXT_VERSION}"
git tag "v${NEXT_VERSION}"
git push origin main --tags

# Merge to develop if using gitflow
git checkout develop
git merge --no-ff "release/v${NEXT_VERSION}"
git push origin develop
```

### Workflow 2: Hotfix Release

Execute emergency patch release for critical production issues.

**Phase 1: Hotfix Initiation**

**Step 1.1: Create Hotfix Branch**

```bash
# Create hotfix branch from production tag
git checkout -b "hotfix/v${CURRENT_VERSION}-hotfix.1" "v${CURRENT_VERSION}"
git push origin "hotfix/v${CURRENT_VERSION}-hotfix.1"
```

**Step 1.2: Apply Fix and Test**

```plaintext
Task("CI/CD Engineer", "
  Apply hotfix and validate:

  1. Cherry-pick fix commits to hotfix branch
  2. Bump version with hotfix suffix
  3. Run targeted regression tests
  4. Build hotfix artifacts
  5. Deploy to staging for validation
  6. Document fix in hotfix-specific changelog

  Use scripts/hotfix.sh for automation
  Store hotfix status in memory: release/hotfix
", "cicd-engineer")
```

**Phase 2: Expedited Deployment**

**Step 2.1: Fast-Track Approval**

```plaintext
Task("Release Manager", "
  Expedite hotfix approval:

  1. Assess severity and urgency
  2. Fast-track security review (critical paths only)
  3. Skip non-critical validation steps
  4. Get stakeholder approval via emergency process
  5. Approve for immediate production deployment

  Store approval in memory: release/hotfix-approval
", "release-manager")
```

**Step 2.2: Deploy Hotfix**

```bash
# Deploy hotfix to production immediately
bash scripts/deploy.sh \
  --environment "production" \
  --version "${HOTFIX_VERSION}" \
  --strategy "rolling" \
  --fast-rollout true
```

**Step 2.3: Backport Hotfix**

```bash
# Merge hotfix to main and develop branches
git checkout main
git merge --no-ff "hotfix/${HOTFIX_VERSION}"
git push origin main

git checkout develop
git merge --no-ff "hotfix/${HOTFIX_VERSION}"
git push origin develop
```

### Workflow 3: Rollback Management

Handle failed deployments with automated rollback.

**Phase 1: Failure Detection**

**Step 1.1: Monitor Deployment Health**

```bash
# Continuous health monitoring
bash scripts/health-monitor.sh \
  --environment "production" \
  --error-rate-threshold 5.0 \
  --latency-threshold-p99 2000 \
  --alert-on-threshold true
```

**Step 1.2: Identify Failure Criteria**

```plaintext
Task("Release Manager", "
  Assess deployment health and determine if rollback needed:

  1. Check error rate spike (>5% increase)
  2. Monitor latency degradation (>50% increase)
  3. Track failed health checks
  4. Review user impact reports
  5. Make rollback decision based on severity

  Use references/rollback-criteria.md
  Store decision in memory: release/rollback-decision
", "release-manager")
```

**Phase 2: Rollback Execution**

**Step 2.1: Trigger Automated Rollback**

```bash
# Execute rollback to previous version
bash scripts/rollback.sh \
  --environment "production" \
  --target-version "${PREVIOUS_VERSION}" \
  --strategy "immediate" \
  --preserve-data true
```

**Step 2.2: Validate Rollback Success**

```plaintext
Task("Test Engineer", "
  Validate rollback restored service:

  1. Confirm previous version deployed
  2. Run smoke tests
  3. Verify error rates normalized
  4. Check data integrity maintained
  5. Monitor for 1 hour post-rollback

  Store rollback validation in memory: release/rollback-validation
", "tester")
```

**Step 2.3: Post-Mortem Analysis**

```plaintext
Task("Release Manager", "
  Conduct rollback post-mortem:

  1. Document failure root cause
  2. Identify what testing missed the issue
  3. Create action items to prevent recurrence
  4. Update release process with learnings
  5. Schedule fix and re-release

  Use references/postmortem-template.md
  Store post-mortem in memory: release/postmortem
", "release-manager")
```

## Deployment Strategies

### Rolling Deployment

Gradually replace instances with new version. Default strategy for most releases.

**Characteristics:**
- Low risk: issues affect subset of users
- Gradual rollout: 10% → 25% → 50% → 100%
- Easy rollback: stop deployment and roll back affected instances
- No extra infrastructure required

### Blue-Green Deployment

Maintain two identical environments, switch traffic atomically.

**Characteristics:**
- Zero downtime: instant traffic switch
- Easy rollback: switch traffic back
- Requires 2x infrastructure temporarily
- Good for database migration testing

### Canary Deployment

Route small percentage of traffic to new version, gradually increase.

**Characteristics:**
- Minimal blast radius: 1-5% initial exposure
- A/B testing capability: compare metrics
- Gradual confidence building
- Requires traffic routing capabilities

## MCP Tool Integration

### Task Orchestration

```bash
# Orchestrate full release workflow
mcp__claude-flow__task_orchestrate \
  task="Execute release v2.0.0" \
  strategy=sequential \
  maxAgents=5 \
  priority=critical
```

### Swarm Monitoring

```bash
# Monitor release agent progress
mcp__claude-flow__swarm_status verbose=true

# Get deployment metrics
mcp__claude-flow__agent_metrics metric=performance
```

## Best Practices

**Semantic Versioning**: Always follow semver strictly. Breaking changes require major version bump, features require minor, fixes require patch.

**Release Automation**: Automate all repeatable tasks. Human intervention should only be required for go/no-go decisions.

**Comprehensive Testing**: Never skip testing phases. Staging validation catches 80% of production issues.

**Incremental Rollout**: Use canary or rolling deployments for major releases. Minimize blast radius of issues.

**Rollback Readiness**: Always maintain ability to rollback. Test rollback procedure before production deployment.

**Documentation First**: Generate release notes and changelog before deployment. Documentation helps with debugging post-release issues.

**Monitoring and Alerts**: Ensure comprehensive monitoring before release. Post-release issues should trigger automatic alerts.

**Communication**: Notify stakeholders at each phase: release start, deployment begin, deployment complete, validation passed.

## Error Handling

**Build Failures**: If CI build fails, automatically abort release and notify release manager. Do not proceed with broken builds.

**Test Failures**: Any validation test failure blocks release. Investigate root cause before retry.

**Deployment Failures**: Trigger automatic rollback if deployment health checks fail. Preserve application state and data.

**Monitoring Gaps**: If monitoring unavailable, delay deployment until monitoring restored. Flying blind is unacceptable.

**Version Conflicts**: If version already exists, coordinator decides: force bump or abort. Never overwrite existing releases.

## References

- `references/semver-guide.md` - Semantic versioning rules and examples
- `references/deployment-strategies.md` - Deployment strategy comparison
- `references/rollback-criteria.md` - When to rollback decision matrix
- `references/release-notes-template.md` - Release notes formatting
- `references/changelog-template.md` - Changelog generation format
- `references/security-checklist.md` - Pre-release security validation
- `references/postmortem-template.md` - Incident post-mortem structure
- `scripts/semver.sh` - Semantic version calculation
- `scripts/version-bumper.sh` - Multi-file version update
- `scripts/build-release.sh` - Release artifact building
- `scripts/deploy.sh` - Deployment orchestration
- `scripts/rollback.sh` - Automated rollback
- `scripts/release-validation.sh` - Validation test suite
- `scripts/health-monitor.sh` - Production health monitoring
- `scripts/changelog-generator.sh` - Automated changelog creation
