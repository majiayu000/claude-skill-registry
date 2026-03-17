---
name: github-project
description: "GitHub repository setup, configuration, and troubleshooting. AUTOMATICALLY TRIGGER when: (1) PRs won't merge or show BLOCKED status, (2) auto-merge not working for Dependabot/Renovate, (3) branch protection issues, (4) GitHub Actions workflow problems, (5) using gh CLI or GitHub API, (6) configuring CODEOWNERS or rulesets. By Netresearch."
---

# GitHub Project Skill

GitHub repository setup, configuration, troubleshooting, and best practices for collaboration workflows.

## Quick Diagnostics

### PR Won't Merge / Shows BLOCKED

```bash
# Check merge state
gh api graphql -f query='query($owner:String!,$repo:String!,$pr:Int!){
  repository(owner:$owner,name:$repo){pullRequest(number:$pr){
    mergeStateStatus reviewDecision mergeable
  }}
}' -f owner=OWNER -f repo=REPO -F pr=NUMBER --jq '.data.repository.pullRequest'

# Check required status checks vs actual
gh api repos/OWNER/REPO/branches/main/protection/required_status_checks --jq '.checks[].context'

# Check code owner requirement
gh api repos/OWNER/REPO/branches/main/protection/required_pull_request_reviews --jq '.require_code_owner_reviews'

# Check conversation resolution requirement
gh api repos/OWNER/REPO/branches/main/protection --jq '.required_conversation_resolution.enabled'

# Check for unresolved review threads on a PR
gh api graphql -f query='query($owner:String!,$repo:String!,$pr:Int!){
  repository(owner:$owner,name:$repo){pullRequest(number:$pr){
    reviewThreads(first:50){nodes{isResolved comments(first:1){nodes{body}}}}
  }}
}' -f owner=OWNER -f repo=REPO -F pr=NUMBER --jq '.data.repository.pullRequest.reviewThreads.nodes[] | select(.isResolved == false)'
```

### Auto-merge Not Working

```bash
# Check who enabled auto-merge (should be app/renovate for bypass)
gh api graphql -f query='query{repository(owner:"OWNER",name:"REPO"){
  pullRequest(number:PR){autoMergeRequest{enabledBy{login}}}
}}' --jq '.data.repository.pullRequest.autoMergeRequest'

# Check bypass apps
gh api repos/OWNER/REPO/branches/main/protection/required_pull_request_reviews \
  --jq '.bypass_pull_request_allowances.apps[].slug'
```

### GitHub Actions Issues

```bash
# List recent workflow runs
gh run list --repo OWNER/REPO --limit 10

# Check failed run logs
gh run view RUN_ID --repo OWNER/REPO --log-failed

# Re-run failed workflow
gh run rerun RUN_ID --repo OWNER/REPO

# Manually trigger workflow (requires workflow_dispatch)
gh workflow run WORKFLOW.yml --repo OWNER/REPO --ref main
```

## Core Workflow

To set up or configure a GitHub repository, follow these steps:

1. Consult the appropriate reference for your task
2. Copy and customize the relevant asset templates
3. Run `scripts/verify-github-project.sh` to validate configuration
4. Apply settings via GitHub UI or `gh` CLI

## Using Reference Documentation

### Repository Setup

When setting up repository structure, consult `references/repository-structure.md` for standard file layout, required documentation files, and directory conventions.

When migrating from master to main branch, consult `references/branch-migration.md` for step-by-step migration commands and branch protection updates.

### Dependency Management

When configuring automated dependency updates, consult `references/dependency-management.md` for Dependabot and Renovate configuration patterns, auto-merge workflows, and update strategies.

When troubleshooting why auto-merge isn't working, consult `references/dependency-management.md` for common issues like check name mismatches, code owner review conflicts, and bypass permission problems.

### GitHub Features

When working with sub-issues, consult `references/sub-issues.md` for GraphQL API usage, parent-child relationships, and issue hierarchy patterns.

When setting up automatic release labeling, consult `references/release-labeling.md` for PR labeling workflows, release categorization, and changelog automation.

## Running Scripts

### Repository Verification

To verify GitHub project configuration against best practices:

```bash
scripts/verify-github-project.sh /path/to/repository
```

This script checks:
- Repository documentation (README, LICENSE, SECURITY.md)
- Collaboration setup (CODEOWNERS, issue/PR templates)
- Dependency automation (Dependabot/Renovate, auto-merge)
- Release configuration

## Using Asset Templates

### Repository Documentation

To set up CODEOWNERS for code review assignments, copy `assets/CODEOWNERS.template` to `.github/CODEOWNERS`.

To add contribution guidelines, copy `assets/CONTRIBUTING.md.template` to `CONTRIBUTING.md`.

To configure security vulnerability reporting, copy `assets/SECURITY.md.template` to `SECURITY.md`.

### Issue and PR Templates

To add a bug report template, copy `assets/bug_report.md.template` to `.github/ISSUE_TEMPLATE/bug_report.md`.

To add a feature request template, copy `assets/feature_request.md.template` to `.github/ISSUE_TEMPLATE/feature_request.md`.

To standardize PR descriptions, copy `assets/PULL_REQUEST_TEMPLATE.md.template` to `.github/PULL_REQUEST_TEMPLATE.md`.

### Dependency Automation

To configure Dependabot, copy `assets/dependabot.yml.template` to `.github/dependabot.yml`.

To configure Renovate, copy `assets/renovate.json.template` to `renovate.json`.

### Auto-Merge Workflows

To enable basic auto-merge for dependency updates, copy `assets/auto-merge.yml.template` to `.github/workflows/auto-merge.yml`.

To enable auto-merge with direct commits (no merge queue), copy `assets/auto-merge-direct.yml.template` to `.github/workflows/auto-merge.yml`.

To enable auto-merge with merge queue support, copy `assets/auto-merge-queue.yml.template` to `.github/workflows/auto-merge.yml`.

### Release Automation

To set up automatic release labeling for PRs, copy `assets/release-labeler.yml.template` to `.github/workflows/release-labeler.yml`.

## Go Project CI Checklist

When setting up CI for Go projects, ensure these GitHub configurations:

| Setting | Purpose | How |
|---------|---------|-----|
| Branch protection | Require tests pass before merge | Branch settings or Rulesets |
| Dependabot/Renovate | Automated dependency updates | `.github/dependabot.yml` or `renovate.json` |
| Auto-merge workflow | Merge minor/patch updates automatically | `assets/auto-merge*.yml` templates |
| Required checks | CI workflow names in branch protection | Match exact workflow job names |

## Polyglot Project CI Checklist (PHP + JavaScript)

When setting up CI for projects with both PHP and JavaScript, ensure coverage from ALL languages:

| Requirement | Implementation | Why |
|-------------|----------------|-----|
| PHP test coverage | `phpunit --coverage-clover` for each test suite | Codecov needs all suites |
| JavaScript test coverage | `npm run test:coverage` with lcov output | Codecov aggregates all languages |
| vitest lcov reporter | `reporter: ['text', 'json', 'html', 'lcov']` | Required for Codecov compatibility |
| Codecov upload | List ALL coverage files in `files:` parameter | Ensures complete coverage picture |

### Example CI Configuration

```yaml
# Run all PHP test suites with coverage
- run: php -d pcov.enabled=1 .Build/bin/phpunit -c Build/phpunit/UnitTests.xml --coverage-clover .Build/coverage/unit.xml
- run: php -d pcov.enabled=1 .Build/bin/phpunit -c Build/phpunit/IntegrationTests.xml --coverage-clover .Build/coverage/integration.xml

# Run JavaScript tests with coverage
- uses: actions/setup-node@SHA # vX.Y.Z
  with:
    node-version: '22'
- run: npm install
- run: npm run test:coverage

# Upload ALL coverage files
- uses: codecov/codecov-action@SHA # vX.Y.Z
  with:
    files: .Build/coverage/unit.xml,.Build/coverage/integration.xml,coverage/lcov.info
```

### vitest Configuration

When using vitest, the `lcov` reporter is **required** for Codecov:

```javascript
// vitest.config.js
coverage: {
    provider: 'v8',
    reporter: ['text', 'json', 'html', 'lcov'],  // lcov REQUIRED
    reportsDirectory: 'coverage',
}
```

## TYPO3 Extension Repository Standards

When setting up repositories for TYPO3 extensions, apply these standards for consistency across Netresearch projects.

### Repository Settings

Configure via GitHub UI or `gh` CLI:

```bash
# Enable Projects tab
gh repo edit --enable-projects

# Set description (template)
gh repo edit --description "TYPO3 extension for <purpose> - by Netresearch"

# Add topics
gh api repos/OWNER/REPO/topics -X PUT -f names='["typo3","typo3-extension","php","<domain-topics>"]'
```

| Setting | Value | Why |
|---------|-------|-----|
| `has_projects` | true | Project board for issue tracking |
| `has_wiki` | false | Use Documentation/ folder instead |
| Description | `<What it does> - by Netresearch` | Consistent branding |

### Required Topics

All TYPO3 extension repos MUST have these topics:

| Topic | Required | Example |
|-------|----------|---------|
| `typo3` | ✅ Always | - |
| `typo3-extension` | ✅ Always | - |
| `php` | ✅ Always | - |
| Domain-specific | ✅ 2-5 more | `ckeditor`, `llm`, `ai`, `rte` |

**Example from t3x-rte_ckeditor_image:**
```
typo3, typo3-extension, typo3cms-extension, ckeditor, ckeditor-plugin, rte-ckeditor, magic-images
```

**Example from t3x-nr-llm:**
```
typo3, typo3-extension, php, ai, llm, openai, anthropic, claude, gemini, gpt
```

### README Badge Order

Badges should appear in this order (see `netresearch-branding` skill for templates):

```markdown
<!-- Row 1: CI/Quality badges -->
[![CI](...)][ci]
[![codecov](...)][codecov]
[![Documentation](...)][docs]  <!-- if applicable -->

<!-- Row 2: Security badges -->
[![OpenSSF Scorecard](...)][scorecard]
[![OpenSSF Best Practices](...)][bestpractices]
[![SLSA 3](...)][slsa]

<!-- Row 3: Standards badges -->
[![PHPStan](...)][phpstan]
[![PHP 8.x+](...)][php]
[![TYPO3 vXX](...)][typo3]
[![License](...)][license]
[![Latest Release](...)][release]
[![Contributor Covenant](...)][covenant]

<!-- Row 4: TYPO3 TER badges (if published to TER) -->
![Composer](https://typo3-badges.dev/badge/EXT_KEY/composer/shields.svg)
![Downloads](https://typo3-badges.dev/badge/EXT_KEY/downloads/shields.svg)
![Extension](https://typo3-badges.dev/badge/EXT_KEY/extension/shields.svg)
![Stability](https://typo3-badges.dev/badge/EXT_KEY/stability/shields.svg)
![TYPO3](https://typo3-badges.dev/badge/EXT_KEY/typo3/shields.svg)
![Version](https://typo3-badges.dev/badge/EXT_KEY/version/shields.svg)
<!-- Generated with 🧡 at typo3-badges.dev -->
```

### Quick Setup Commands

```bash
# Set topics for TYPO3 extension
gh api repos/netresearch/t3x-EXTNAME/topics -X PUT \
  -f names='["typo3","typo3-extension","php","DOMAIN1","DOMAIN2"]'

# Enable projects
gh repo edit netresearch/t3x-EXTNAME --enable-projects

# Update description
gh repo edit netresearch/t3x-EXTNAME \
  --description "TYPO3 extension for PURPOSE - by Netresearch"
```

### Verification

Check repository compliance:

```bash
# Check topics
gh api repos/OWNER/REPO/topics --jq '.names | if contains(["typo3","typo3-extension","php"]) then "✅ Required topics present" else "❌ Missing required topics" end'

# Check has_projects
gh api repos/OWNER/REPO --jq 'if .has_projects then "✅ Projects enabled" else "❌ Projects disabled" end'
```

## Merge Strategy & Signed Commits

When configuring repositories that require signed commits with clean history, consult `references/merge-strategy.md` for the recommended settings.

### Quick Reference

For signed commits workflow (rebase locally + merge commit):

| Repository Setting | Value | Why |
|--------------------|-------|-----|
| `allow_merge_commit` | **true** | Preserves signatures on feature branch commits |
| `allow_rebase_merge` | true | GitHub requires at least one of squash/rebase |
| `allow_squash_merge` | false | Destroys individual commit signatures |

| Branch Protection | Value | Why |
|-------------------|-------|-----|
| `required_signatures` | true | Enforces GPG/SSH signed commits |
| `required_linear_history` | **false** | Must be false - conflicts with merge commits |
| `required_conversation_resolution` | true | All review threads must be resolved before merge |

### Workflow

```bash
# 1. Developer rebases PR branch locally (signs commits)
git fetch origin && git rebase origin/main
git push --force-with-lease

# 2. Merge via merge commit (preserves signatures)
gh pr merge <number> --merge
```

### Auto-Merge Compatibility

| Merge Strategy | Works with `required_signatures`? |
|----------------|-----------------------------------|
| Merge commit | ✅ Yes - GitHub signs the merge commit |
| Rebase merge | ❌ No - GitHub cannot sign rewritten commits |
| Squash merge | ❌ No - GitHub cannot sign squashed commit |

**Important:** When enabling auto-merge, select "Create a merge commit" strategy.

## Required Conversation Resolution (MANDATORY)

All review threads on a PR **must be resolved** before merging. This prevents addressed feedback from being silently ignored.

### Enable via API

```bash
# Enable conversation resolution requirement
gh api repos/OWNER/REPO/branches/main/protection -X PUT \
  --input - << 'EOF'
{
  ...existing settings...,
  "required_conversation_resolution": true
}
EOF
```

### Enable via GitHub UI

Settings → Branches → Branch protection rules → Edit → Check **"Require conversation resolution before merging"**

### Verify

```bash
# Check if enabled
gh api repos/OWNER/REPO/branches/main/protection --jq 'if .required_conversation_resolution.enabled then "✅ Conversation resolution required" else "❌ Conversation resolution NOT required - ENABLE IT" end'
```

### Resolve Threads via API

```bash
# List unresolved threads on a PR
gh api graphql -f query='query($owner:String!,$repo:String!,$pr:Int!){
  repository(owner:$owner,name:$repo){pullRequest(number:$pr){
    reviewThreads(first:50){nodes{id isResolved comments(first:1){nodes{body}}}}
  }}
}' -f owner=OWNER -f repo=REPO -F pr=NUMBER --jq '.data.repository.pullRequest.reviewThreads.nodes[] | select(.isResolved == false) | {id, body: .comments.nodes[0].body}'

# Resolve a specific thread
gh api graphql -f query='mutation($id:ID!){resolveReviewThread(input:{threadId:$id}){thread{isResolved}}}' -f id=THREAD_NODE_ID
```

## Required Reviews from All Requested Reviewers (MANDATORY)

PRs must **not be merged until all requested reviewers have submitted their review**. This includes human reviewers and automated reviewers (e.g., GitHub Copilot). Do not merge while any reviewer's status is still "PENDING".

> **Note:** GitHub branch protection only enforces a *minimum* approval count, not "all requested reviewers must respond." This rule is enforced as a **workflow policy** — agents and humans must verify before merging.

### Check Reviewer Status Before Merging

```bash
# List all requested reviewers and their review state
gh pr view NUMBER --repo OWNER/REPO --json reviewRequests,reviews --jq '{
  pending: [.reviewRequests[].login],
  completed: [.reviews[] | {user: .author.login, state: .state}]
}'

# GraphQL: full reviewer status (requested + completed)
gh api graphql -f query='query($owner:String!,$repo:String!,$pr:Int!){
  repository(owner:$owner,name:$repo){pullRequest(number:$pr){
    reviewRequests(first:20){nodes{requestedReviewer{...on User{login}...on Bot{login}}}}
    reviews(last:20){nodes{author{login}state}}
  }}
}' -f owner=OWNER -f repo=REPO -F pr=NUMBER --jq '.data.repository.pullRequest | {
  awaiting: [.reviewRequests.nodes[].requestedReviewer.login],
  reviews: [.reviews.nodes[] | {user: .author.login, state: .state}]
}'
```

If `awaiting` is non-empty, the PR is **not ready to merge** — those reviewers haven't responded yet.

### PR Merge Checklist

Before merging any PR, verify **all** of these:

| # | Prerequisite | How to check |
|---|-------------|--------------|
| 1 | All CI checks pass | `gh pr checks NUMBER` |
| 2 | All requested reviewers have responded | `gh pr view NUMBER --json reviewRequests` → must be empty |
| 3 | All review threads resolved | `gh pr view NUMBER --json reviewThreads` or GraphQL |
| 4 | Branch rebased on target | `gh pr view NUMBER --json mergeStateStatus` → `CLEAN` |

## Auto-merge Troubleshooting Quick Reference

When dependency PRs aren't auto-merging, check these common issues:

| Symptom | Cause | Fix |
|---------|-------|-----|
| PR BLOCKED, checks pass | Check names don't match | Update branch protection to use exact names (e.g., `job (variant)` not `job`) |
| PR BLOCKED, `reviewDecision: REVIEW_REQUIRED` | `require_code_owner_reviews: true` | Disable code owner reviews or add code owner approval |
| PR BLOCKED, unresolved threads | `required_conversation_resolution: true` | Resolve all review threads before merging |
| PR has pending reviewers | Requested reviewers haven't responded | Wait for all requested reviewers to submit their review |
| Renovate PR not using bypass | Workflow racing with Renovate | Only approve in workflow; let Renovate enable auto-merge via `platformAutomerge` |
| CI can't push to main | Branch protection blocks direct push | Use Renovate `lockFileMaintenance` instead |
| Workflow not triggering | Rapid merges skip push events | Add `workflow_dispatch` trigger, run manually |
| "Merge method X not allowed" | Wrong merge strategy | Check `gh api repos/O/R --jq '{merge: .allow_merge_commit, squash: .allow_squash_merge, rebase: .allow_rebase_merge}'`; match workflow |
| Bot detection misses reruns | `github.actor` changes on synchronize | Use `github.event.pull_request.user.login` instead of `github.actor` |
| Gitleaks fails on bot PRs | `GITLEAKS_LICENSE` secret unavailable | Skip gitleaks for bot PRs or use `.gitleaks.toml` allowlist |
| Old PRs not auto-merging | Opened before workflow existed | Comment `@dependabot rebase` / `@renovate rebase` to trigger `synchronize` |
| Can't merge workflow file PRs | `GITHUB_TOKEN` lacks `workflows` scope | Merge manually; use workflow check in `auto-merge-direct.yml` template |

### Branch Protection for Auto-merge

```bash
# Check required checks vs actual check names
gh api repos/OWNER/REPO/branches/main/protection/required_status_checks --jq '.checks[].context'

# Check code owner requirement (should be false for auto-merge)
gh api repos/OWNER/REPO/branches/main/protection/required_pull_request_reviews --jq '.require_code_owner_reviews'

# Check bypass apps
gh api repos/OWNER/REPO/branches/main/protection/required_pull_request_reviews --jq '.bypass_pull_request_allowances.apps[].slug'

# Fix: Disable code owner reviews, add bypass apps
gh api repos/OWNER/REPO/branches/main/protection/required_pull_request_reviews -X PATCH \
  --input - << 'EOF'
{
  "require_code_owner_reviews": false,
  "required_approving_review_count": 1,
  "bypass_pull_request_allowances": {
    "apps": ["dependabot", "renovate"]
  }
}
EOF
```

### Recommended Renovate Config for Auto-merge

```json
{
  "extends": ["config:recommended"],
  "automergeType": "pr",
  "platformAutomerge": true,
  "lockFileMaintenance": {
    "enabled": true,
    "schedule": ["before 6am on monday"]
  },
  "packageRules": [
    {
      "matchUpdateTypes": ["patch", "minor", "pin", "digest"],
      "automerge": true
    }
  ]
}
```

**Key settings:**
- `platformAutomerge: true` - Renovate enables auto-merge (uses bypass permissions)
- `lockFileMaintenance` - Handles lock file updates via PR (not direct push)

## CodeQL Configuration (MANDATORY)

Netresearch projects use custom CodeQL workflows (`.github/workflows/codeql.yml`). GitHub's "Default Setup" **MUST be disabled** - they cannot coexist.

### The Problem

When both Default Setup and a custom workflow exist, CI fails with:
```
CodeQL analyses from advanced configurations cannot be processed when the default setup is enabled
```

### Required Action

**Before pushing a custom CodeQL workflow**, disable Default Setup:

```bash
# Check current state
gh api repos/OWNER/REPO/code-scanning/default-setup --jq '.state'

# Disable default setup (MANDATORY)
gh api repos/OWNER/REPO/code-scanning/default-setup -X PATCH -f state=not-configured
```

| Setting | Required State | Why |
|---------|----------------|-----|
| Default Setup | `not-configured` | Conflicts with custom workflow |
| Custom `codeql.yml` | Present in `.github/workflows/` | Our standard security scanning |

### Verification

```bash
# Verify default setup is disabled
gh api repos/OWNER/REPO/code-scanning/default-setup --jq 'if .state == "not-configured" then "✅ Default Setup disabled" else "❌ Default Setup still enabled - DISABLE IT" end'
```

## Essential `gh` CLI Commands Reference

### Repository Information

```bash
# Get repo info
gh repo view OWNER/REPO --json name,defaultBranchRef,description

# List branches
gh api repos/OWNER/REPO/branches --jq '.[].name'

# Get branch protection rules
gh api repos/OWNER/REPO/branches/main/protection
```

### Pull Requests

```bash
# List PRs
gh pr list --repo OWNER/REPO --state open

# View PR details
gh pr view NUMBER --repo OWNER/REPO --json state,mergeStateStatus,reviewDecision,autoMergeRequest

# Check PR merge status (GraphQL - more detailed)
gh api graphql -f query='query($owner:String!,$repo:String!,$pr:Int!){
  repository(owner:$owner,name:$repo){pullRequest(number:$pr){
    state mergeStateStatus reviewDecision mergeable
    autoMergeRequest{enabledBy{login}mergeMethod}
    commits(last:1){nodes{commit{statusCheckRollup{state}}}}
  }}
}' -f owner=OWNER -f repo=REPO -F pr=NUMBER

# Approve PR
gh pr review NUMBER --repo OWNER/REPO --approve

# Enable auto-merge
gh pr merge NUMBER --repo OWNER/REPO --auto --merge

# Merge PR directly
gh pr merge NUMBER --repo OWNER/REPO --merge  # or --squash, --rebase

# Comment on PR
gh pr comment NUMBER --repo OWNER/REPO --body "message"

# Trigger bot rebase
gh pr comment NUMBER --repo OWNER/REPO --body "@dependabot rebase"
gh pr comment NUMBER --repo OWNER/REPO --body "@renovate rebase"
```

### Branch Protection

```bash
# Get full branch protection
gh api repos/OWNER/REPO/branches/main/protection

# Get required status checks
gh api repos/OWNER/REPO/branches/main/protection/required_status_checks

# Update required status checks
gh api repos/OWNER/REPO/branches/main/protection/required_status_checks -X PATCH \
  --input - << 'EOF'
{
  "strict": true,
  "checks": [
    {"context": "lint"},
    {"context": "build"},
    {"context": "test"}
  ]
}
EOF

# Get/update PR review requirements
gh api repos/OWNER/REPO/branches/main/protection/required_pull_request_reviews

# Disable code owner reviews, add bypass apps
gh api repos/OWNER/REPO/branches/main/protection/required_pull_request_reviews -X PATCH \
  --input - << 'EOF'
{
  "require_code_owner_reviews": false,
  "required_approving_review_count": 1,
  "bypass_pull_request_allowances": {
    "apps": ["dependabot", "renovate"]
  }
}
EOF
```

### GitHub Actions

```bash
# List workflow runs
gh run list --repo OWNER/REPO --limit 10

# List runs for specific workflow
gh run list --repo OWNER/REPO --workflow=build.yml

# View run details
gh run view RUN_ID --repo OWNER/REPO

# View failed logs
gh run view RUN_ID --repo OWNER/REPO --log-failed

# Re-run failed jobs
gh run rerun RUN_ID --repo OWNER/REPO --failed

# Manually trigger workflow
gh workflow run WORKFLOW.yml --repo OWNER/REPO --ref main

# List workflows
gh workflow list --repo OWNER/REPO
```

### Releases and Tags

```bash
# List releases
gh release list --repo OWNER/REPO

# Create release (after pushing signed tag)
git tag -s vX.Y.Z -m "vX.Y.Z"
git push origin vX.Y.Z
gh release create vX.Y.Z --repo OWNER/REPO --title "vX.Y.Z" --notes "Release notes"

# Get latest release
gh release view --repo OWNER/REPO

# Download release assets
gh release download TAG --repo OWNER/REPO
```

### Files and Content

```bash
# Get file contents (base64 encoded)
gh api repos/OWNER/REPO/contents/PATH --jq '.content' | base64 -d

# Update file via API
gh api repos/OWNER/REPO/contents/PATH -X PUT \
  -f message="commit message" \
  -f content="$(base64 -w0 < file)" \
  -f sha="$(gh api repos/OWNER/REPO/contents/PATH --jq '.sha')"
```

### Repository Settings

```bash
# Update repo settings
gh repo edit OWNER/REPO --enable-projects --enable-wiki=false

# Set topics
gh api repos/OWNER/REPO/topics -X PUT -f names='["topic1","topic2"]'

# Update description
gh repo edit OWNER/REPO --description "New description"
```

## Common Patterns for Troubleshooting

### Debug Auto-merge Pipeline

```bash
# 1. Check PR status
gh pr view NUMBER --repo OWNER/REPO --json mergeStateStatus,reviewDecision,autoMergeRequest

# 2. Check actual vs required checks
echo "=== Required checks ===" && \
gh api repos/OWNER/REPO/branches/main/protection/required_status_checks --jq '.checks[].context' && \
echo "=== Actual checks ===" && \
gh api graphql -f query='query{repository(owner:"OWNER",name:"REPO"){
  pullRequest(number:NUMBER){commits(last:1){nodes{commit{
    statusCheckRollup{contexts(first:30){nodes{...on CheckRun{name conclusion}}}}
  }}}}
}}' --jq '.data.repository.pullRequest.commits.nodes[0].commit.statusCheckRollup.contexts.nodes[].name'

# 3. Check bypass permissions
gh api repos/OWNER/REPO/branches/main/protection/required_pull_request_reviews \
  --jq '{code_owner: .require_code_owner_reviews, bypass: .bypass_pull_request_allowances.apps[].slug}'

# 4. Check if branch is behind
gh api graphql -f query='query{repository(owner:"OWNER",name:"REPO"){
  pullRequest(number:NUMBER){mergeStateStatus}
}}' --jq '.data.repository.pullRequest.mergeStateStatus'
```

### Fix Common Issues

```bash
# Fix: Update check names in branch protection
gh api repos/OWNER/REPO/branches/main/protection/required_status_checks -X PATCH \
  -f strict=true \
  --input - << 'EOF'
{"checks": [{"context": "job-name (variant)"}]}
EOF

# Fix: Disable code owner reviews blocking auto-merge
gh api repos/OWNER/REPO/branches/main/protection/required_pull_request_reviews -X PATCH \
  -f require_code_owner_reviews=false

# Fix: Add bypass apps
gh api repos/OWNER/REPO/branches/main/protection/required_pull_request_reviews -X PATCH \
  --input - << 'EOF'
{"bypass_pull_request_allowances": {"apps": ["dependabot", "renovate"]}}
EOF
```

## Related Skills

When implementing Go code patterns and CI/CD workflows, use the `go-development` skill.

When implementing OpenSSF Scorecard, SLSA provenance, or signed releases, use the `enterprise-readiness` skill.

When establishing Git branching strategies or conventional commits, use the `git-workflow` skill.

When conducting deep security audits (OWASP, CVE analysis), use the `security-audit` skill.

## External Resources

When understanding GitHub Actions syntax, consult the [GitHub Actions Documentation](https://docs.github.com/en/actions).

When configuring branch protection, consult the [GitHub Branch Protection Guide](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches).

When setting up Dependabot, consult the [Dependabot Documentation](https://docs.github.com/en/code-security/dependabot).

---

> **Contributing:** https://github.com/netresearch/github-project-skill
