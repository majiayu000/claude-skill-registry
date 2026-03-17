---
name: full-dev-cycle
description: Complete development workflow integrating Git operations, GitHub PR management, and Docker deployment. Use for end-to-end development tasks. Triggers include "deploy changes", "create PR and deploy", "full cycle", "git to production", "commit and deploy", "development workflow", or any multi-stage development task.
version: 1.0.0
author: Miyabi
depends_on:
  - mcp-context-optimizer
  - docker-compose-workflow
---

# Full Development Cycle Workflow

End-to-end development workflow: Git → GitHub PR → Docker Deploy

## Workflow Overview

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   DEVELOP   │ → │    COMMIT   │ → │  CREATE PR  │ → │   DEPLOY    │
│             │    │             │    │             │    │             │
│ Code changes│    │ Git add/    │    │ Open PR     │    │ Docker      │
│ Test locally│    │ commit/push │    │ Add labels  │    │ rebuild     │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
       │                  │                  │                  │
       ▼                  ▼                  ▼                  ▼
   file tools         git tools        github tools       docker tools
```

## Phase 1: Development Check

### 1.1 Review Current State
```bash
# Check git status
miyabi:git_status()

# View current branch
miyabi:git_current_branch()

# Check for uncommitted changes
miyabi:git_diff()
```

### 1.2 Validate Changes
```bash
# Review staged changes
miyabi:git_staged_diff()

# Check recent commits
miyabi:git_log({ limit: 5 })
```

## Phase 2: Git Operations

### 2.1 Stage and Commit
```bash
# Stage all changes (via bash if needed)
bash: git add -A

# Or stage specific files
bash: git add src/feature.ts tests/feature.test.ts
```

### 2.2 Create Semantic Commit
```markdown
## Commit Message Format
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types:**
| Type | Use Case |
|------|----------|
| feat | New feature |
| fix | Bug fix |
| docs | Documentation |
| style | Formatting |
| refactor | Code restructure |
| test | Tests |
| chore | Maintenance |

### 2.3 Push Changes
```bash
# Push to remote
bash: git push origin $(git branch --show-current)

# If new branch
bash: git push -u origin $(git branch --show-current)
```

## Phase 3: GitHub PR Creation

### 3.1 Check Repository State
```bash
# View existing PRs
miyabi:github_list_prs({ state: "open" })

# Check branch comparison
miyabi:github_compare_commits({
  base: "main",
  head: "feature-branch"
})
```

### 3.2 Create Pull Request
```bash
miyabi:github_create_pr({
  title: "feat(module): Add new feature",
  head: "feature-branch",
  base: "main",
  body: "## Summary\n\n- Added X\n- Fixed Y\n\n## Testing\n\n- [ ] Unit tests\n- [ ] Integration tests"
})
```

### 3.3 Add Labels and Metadata
```bash
# Add labels
miyabi:github_add_labels({
  issue_number: PR_NUMBER,
  labels: ["enhancement", "ready-for-review"]
})

# Add comment
miyabi:github_add_comment({
  issue_number: PR_NUMBER,
  body: "Ready for review. CI passing."
})
```

## Phase 4: Docker Deployment

### 4.1 Pre-Deployment Checks
```bash
# Check current containers
miyabi:docker_ps({ all: true })

# View current resource usage
miyabi:docker_stats({ noStream: true })
```

### 4.2 Rebuild and Deploy
```bash
# Stop current services
miyabi:compose_down({
  path: "./docker-compose.yml"
})

# Rebuild with no cache
miyabi:docker_build({
  tag: "myapp:latest",
  noCache: true
})

# Start services
miyabi:compose_up({
  path: "./docker-compose.yml",
  build: true,
  detach: true
})
```

### 4.3 Verify Deployment
```bash
# Check container status
miyabi:compose_ps({
  path: "./docker-compose.yml"
})

# View logs for errors
miyabi:compose_logs({
  path: "./docker-compose.yml",
  tail: 50
})

# Health check
miyabi:health_check()

# Port verification
miyabi:network_port_check({
  host: "localhost",
  port: 3000
})
```

## Complete Workflow Scripts

### Quick Deploy (Single Command Workflow)

```markdown
## Trigger: "deploy my changes"

1. git_status → Check for changes
2. git_diff → Review changes
3. bash: git add -A && git commit -m "message"
4. bash: git push
5. github_create_pr → Create PR
6. compose_down → Stop services
7. compose_up --build → Rebuild and start
8. compose_logs → Verify
```

### Hotfix Workflow

```markdown
## Trigger: "hotfix for issue #123"

1. bash: git checkout -b hotfix/issue-123 main
2. [make changes]
3. git_status → Verify changes
4. bash: git add -A && git commit -m "fix: resolve #123"
5. bash: git push -u origin hotfix/issue-123
6. github_create_pr → PR to main
7. github_add_labels → ["hotfix", "urgent"]
8. compose_up --build → Deploy
```

### Feature Branch Workflow

```markdown
## Trigger: "complete feature X"

1. git_current_branch → Verify on feature branch
2. git_log → Review commit history
3. github_compare_commits → See diff from main
4. github_create_pr → Create detailed PR
5. [wait for review/approval]
6. github_merge_pr → Merge when ready
7. bash: git checkout main && git pull
8. compose_up --build → Deploy main
```

## Tool Reference Table

| Phase | Tool | Purpose |
|-------|------|---------|
| Dev | git_status | Check working tree |
| Dev | git_diff | Review changes |
| Commit | git_log | View history |
| Commit | git_staged_diff | Review staged |
| PR | github_list_prs | Existing PRs |
| PR | github_create_pr | New PR |
| PR | github_add_labels | Categorize |
| Deploy | docker_ps | Container status |
| Deploy | compose_up | Start services |
| Deploy | compose_logs | Verify logs |
| Verify | health_check | System health |
| Verify | network_port_check | Port status |

## Error Handling

### Git Conflicts
```bash
# Check for conflicts
miyabi:git_conflicts()

# If conflicts exist:
1. Review conflicting files
2. Resolve manually or with tool
3. Stage resolved files
4. Complete merge/rebase
```

### Docker Build Failures
```bash
# Check build logs
miyabi:docker_logs({
  container: "build-container",
  tail: 100
})

# Common fixes:
1. Clear Docker cache: docker system prune
2. Check Dockerfile syntax
3. Verify dependencies
```

### Deployment Verification Failed
```bash
# Debug steps:
1. compose_logs → Check for errors
2. docker_inspect → Container config
3. network_connections → Network issues
4. resource_overview → Resource constraints
```

## Integration with Context Optimizer

This skill uses **mcp-context-optimizer** principles:

```markdown
## Progressive Tool Loading

Phase 1: Load git tools only
Phase 2: Load github tools only
Phase 3: Load docker tools only
Phase 4: Load network/health tools only

Never load all 172 tools at once!
```

## Automation Hooks

### Pre-Commit Hook
```bash
# Verify before commit
1. Run linter
2. Run tests
3. Check formatting
```

### Post-Deploy Hook
```bash
# After deployment
1. health_check
2. network_port_check
3. Slack/Discord notification
```

## Best Practices

### DO:
- ✅ Small, focused commits
- ✅ Descriptive PR titles
- ✅ Test before deploying
- ✅ Monitor logs after deploy
- ✅ Use semantic versioning

### DON'T:
- ❌ Force push to main
- ❌ Skip pre-deploy checks
- ❌ Deploy without testing
- ❌ Ignore failing health checks
- ❌ Commit sensitive data

## Rollback Procedure

```markdown
## If deployment fails:

1. compose_down → Stop broken deployment
2. git_log → Find last good commit
3. bash: git checkout <good-commit>
4. compose_up --build → Redeploy
5. github_create_issue → Document failure
```

## Metrics and Monitoring

### Deployment Success Criteria
- [ ] All containers running
- [ ] Health checks passing
- [ ] No errors in logs (last 50 lines)
- [ ] Expected ports accessible
- [ ] Response time < threshold

### Post-Deployment Monitoring
```bash
# Continuous monitoring
miyabi:docker_stats → Resource usage
miyabi:compose_logs → Error tracking
miyabi:network_bandwidth → Traffic monitoring
```
