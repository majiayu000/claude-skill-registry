---
name: github-modes
description: Comprehensive GitHub integration modes for workflow orchestration, PR management, and repository coordination. Use for GitHub CLI operations, automated workflows, PR reviews, issue tracking, release management, and CI/CD coordination.
---

# GitHub Integration Modes Skill

## Overview

This skill provides comprehensive GitHub integration modes for workflow orchestration, PR management, issue tracking, and repository coordination. Each mode is optimized for specific GitHub workflows with batch operation support.

**Key Capabilities:**
- GitHub workflow orchestration and coordination
- Pull request management and review automation
- Issue tracking and project management
- Release coordination and deployment
- Repository architecture and organization
- CI/CD pipeline coordination

## Quick Start

```bash
# Verify GitHub CLI authentication
gh auth status

# Check repository access
gh repo view

# List open PRs
gh pr list

# List issues
gh issue list

# Check workflow runs
gh run list --limit 5
```

## GitHub Workflow Modes

### 1. gh-coordinator
**GitHub workflow orchestration and coordination**

```bash
# Coordinate multiple GitHub operations
gh issue create --title "Feature: New Integration" --body "Description here"
gh pr create --title "Implement feature" --body "Closes #123"
gh workflow run ci.yml
```

- **Coordination Mode**: Hierarchical
- **Max Parallel Operations**: 10
- **Best For**: Complex GitHub workflows, multi-repo coordination

### 2. pr-manager
**Pull request management and review coordination**

```bash
# Create PR with reviewers
gh pr create \
  --title "Feature implementation" \
  --body "## Summary\n- Feature 1\n- Feature 2" \
  --reviewer user1,user2 \
  --assignee @me

# Review PR
gh pr review 123 --approve --body "LGTM!"

# Merge with squash
gh pr merge 123 --squash --delete-branch
```

- **Review Mode**: Automated
- **Multi-reviewer**: Yes
- **Best For**: PR reviews, merge coordination, conflict resolution

### 3. issue-tracker
**Issue management and project coordination**

```bash
# Create structured issue
gh issue create \
  --title "Bug: Login failure" \
  --body "## Description\n...\n## Steps to Reproduce\n1. ..." \
  --label "bug,priority:high" \
  --assignee @me \
  --milestone "v2.0"

# Update issue
gh issue edit 123 --add-label "in-progress"

# Close with comment
gh issue close 123 --comment "Fixed in #456"
```

- **Issue Workflow**: Automated
- **Label Management**: Smart
- **Best For**: Project management, issue coordination, progress tracking

### 4. release-manager
**Release coordination and deployment**

```bash
# Create release
gh release create v1.2.0 \
  --title "Release v1.2.0" \
  --notes "## What's New\n- Feature 1\n- Bug fix 2" \
  --target main

# Upload release assets
gh release upload v1.2.0 ./dist/*.zip

# List releases
gh release list
```

- **Release Pipeline**: Automated
- **Versioning**: Semantic
- **Best For**: Release management, version coordination, deployment pipelines

## Repository Management Modes

### 5. repo-architect
**Repository structure and organization**

```bash
# Create repository
gh repo create my-project --public --description "Project description"

# Clone with specific options
gh repo clone owner/repo -- --depth=1

# Fork repository
gh repo fork owner/repo --clone

# Set repository settings
gh repo edit --enable-issues --enable-wiki=false
```

- **Structure Optimization**: Yes
- **Multi-repo**: Support
- **Best For**: Repository setup, structure optimization, multi-repo management

### 6. code-reviewer
**Automated code review and quality assurance**

```bash
# Get PR diff
gh pr diff 123

# Get changed files
gh pr view 123 --json files --jq '.files[].path'

# Add review comment
gh pr review 123 --comment --body "Consider refactoring this function"

# Request changes
gh pr review 123 --request-changes --body "Please address the following..."
```

- **Review Quality**: Deep
- **Security Analysis**: Yes
- **Best For**: Code quality, security reviews, performance analysis

### 7. branch-manager
**Branch management and workflow coordination**

```bash
# Create feature branch via API
gh api repos/:owner/:repo/git/refs \
  -f ref='refs/heads/feature/new-feature' \
  -f sha=$(gh api repos/:owner/:repo/git/refs/heads/main --jq '.object.sha')

# Delete branch
gh api repos/:owner/:repo/git/refs/heads/old-branch --method DELETE

# List branches
gh api repos/:owner/:repo/branches --jq '.[].name'
```

- **Branch Strategy**: GitFlow
- **Merge Strategy**: Intelligent
- **Best For**: Branch coordination, merge strategies, workflow management

## Integration Modes

### 8. sync-coordinator
**Multi-package synchronization**

```bash
# Sync files across repos
gh api repos/:owner/:repo/contents/file.md --jq '.content' | base64 -d

# Create sync PR
gh pr create \
  --title "Sync: Update shared configurations" \
  --head sync/config-update \
  --base main
```

### 9. ci-orchestrator
**CI/CD pipeline coordination**

```bash
# Trigger workflow
gh workflow run ci.yml --ref main

# Check workflow status
gh run list --workflow=ci.yml --limit=5

# View run details
gh run view $RUN_ID

# Download artifacts
gh run download $RUN_ID
```

### 10. security-guardian
**Security and compliance management**

```bash
# List secret scanning alerts
gh api repos/:owner/:repo/secret-scanning/alerts

# List code scanning alerts
gh api repos/:owner/:repo/code-scanning/alerts

# Check Dependabot alerts
gh api repos/:owner/:repo/dependabot/alerts
```

## Batch Operations

All GitHub modes support batch operations for maximum efficiency:

```bash
# Parallel issue creation
gh issue create --title "Task 1" --body "..." &
gh issue create --title "Task 2" --body "..." &
gh issue create --title "Task 3" --body "..." &
wait

# Batch label management
for issue in 1 2 3 4 5; do
  gh issue edit $issue --add-label "sprint-24" &
done
wait

# Parallel PR reviews
for pr in 10 11 12; do
  gh pr review $pr --approve --body "Automated approval" &
done
wait
```

## MCP Tool Integration

### Swarm Coordination

```javascript
// Initialize GitHub workflow swarm
mcp__claude-flow__swarm_init { topology: "hierarchical", maxAgents: 5 }
mcp__claude-flow__agent_spawn { type: "coordinator", name: "GitHub Coordinator" }
mcp__claude-flow__agent_spawn { type: "reviewer", name: "Code Reviewer" }
mcp__claude-flow__agent_spawn { type: "tester", name: "QA Agent" }

// Execute workflow with coordination
mcp__claude-flow__task_orchestrate {
  task: "GitHub workflow coordination",
  strategy: "parallel",
  priority: "high"
}

// Store workflow state
mcp__claude-flow__memory_usage {
  action: "store",
  key: "github/workflow/state",
  value: {
    mode: "pr-manager",
    activePRs: [123, 124, 125],
    status: "reviewing"
  }
}
```

### GitHub-Specific Tools

```javascript
// Repository analysis
mcp__claude-flow__github_repo_analyze {
  repo: "owner/repo",
  analysis_type: "code_quality"
}

// PR management
mcp__claude-flow__github_pr_manage {
  repo: "owner/repo",
  action: "review",
  pr_number: 123
}

// Issue tracking
mcp__claude-flow__github_issue_track {
  repo: "owner/repo",
  action: "triage"
}
```

## Usage Examples

### Complete PR Workflow

```bash
# 1. Create feature branch
git checkout -b feature/new-feature

# 2. Make changes and commit
git add .
git commit -m "feat: Add new feature"
git push -u origin feature/new-feature

# 3. Create PR with full metadata
gh pr create \
  --title "feat: Add new feature" \
  --body "## Summary
- Implements feature X
- Adds tests for Y

## Testing
- [x] Unit tests pass
- [x] Integration tests pass

Closes #123" \
  --reviewer tech-lead,senior-dev \
  --assignee @me \
  --label "enhancement,needs-review" \
  --milestone "v2.0"

# 4. Wait for reviews and CI
gh pr checks 456 --watch

# 5. Merge when ready
gh pr merge 456 --squash --delete-branch
```

### Automated Issue Management

```bash
# Triage unlabeled issues
gh issue list --label "" --json number,title | \
  jq -r '.[] | "\(.number): \(.title)"'

# Bulk close stale issues
gh issue list --label "stale" --json number | \
  jq -r '.[].number' | while read num; do
    gh issue close $num --comment "Closing stale issue"
  done

# Create linked issues
PARENT=$(gh issue create --title "Epic: Feature Set" --body "Parent issue")
gh issue create --title "Sub-task 1" --body "Part of #$PARENT"
gh issue create --title "Sub-task 2" --body "Part of #$PARENT"
```

## Best Practices

### 1. Authentication
- Use `gh auth login` for initial setup
- Store tokens securely in GitHub Secrets
- Use GITHUB_TOKEN in workflows
- Rotate tokens regularly

### 2. Rate Limiting
- Batch operations when possible
- Use GraphQL for complex queries
- Implement exponential backoff
- Cache API responses

### 3. Workflow Design
- Use reusable workflows
- Implement proper error handling
- Add meaningful commit messages
- Follow semantic versioning

### 4. Security
- Enable branch protection
- Require PR reviews
- Use signed commits
- Enable security scanning

## Configuration Options

| Mode | Max Parallel | Batch Optimized | Primary Use |
|------|-------------|-----------------|-------------|
| gh-coordinator | 10 | Yes | Complex workflows |
| pr-manager | 5 | Yes | PR reviews |
| issue-tracker | 20 | Yes | Issue management |
| release-manager | 3 | No | Releases |
| repo-architect | 5 | Yes | Repo setup |
| code-reviewer | 5 | Yes | Code review |
| branch-manager | 10 | Yes | Branch ops |

## Related Skills

- [github-sync](../github-sync/SKILL.md) - Repository synchronization
- [github-workflow](../github-workflow/SKILL.md) - CI/CD automation
- [github-swarm-pr](../github-swarm-pr/SKILL.md) - PR swarm management
- [github-swarm-issue](../github-swarm-issue/SKILL.md) - Issue swarm coordination
- [github-project-board](../github-project-board/SKILL.md) - Project board sync

---

## Version History

- **1.0.0** (2026-01-02): Initial skill conversion from github-modes agent
