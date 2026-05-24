---
name: github-project-management
title: GitHub Project Management
version: 2.0.0
category: github
description: Comprehensive GitHub project management with swarm-coordinated issue tracking, project board automation, and sprint planning
author: Claude Code
tags:
  - github
  - project-management
  - issue-tracking
  - project-boards
  - sprint-planning
  - agile
  - swarm-coordination
difficulty: intermediate
prerequisites:
  - GitHub CLI (gh) installed and authenticated
  - ruv-swarm or claude-flow MCP server configured
  - Repository access permissions
tools_required:
  - mcp__github__*
  - mcp__claude-flow__*
  - Bash
  - Read
  - Write
  - TodoWrite
related_skills:
  - github-pr-workflow
  - github-release-management
  - sparc-orchestrator
estimated_time: 30-45 minutes
---

# GitHub Project Management

## Behavioral Classification

**Type**: Guided Decision

This skill guides you through project management decisions and then executes based on your choices.

**Decision Points**:
1. Which project management mode? (issues, boards, sprints)
2. Swarm topology for coordination?
3. Auto-sync or manual updates?

---

## Overview

A comprehensive skill for managing GitHub projects using AI swarm coordination. This skill combines intelligent issue management, automated project board synchronization, and swarm-based coordination for efficient project delivery.

---

## Quick Start

### Basic Issue Creation with Swarm Coordination

```bash
# Create a coordinated issue
gh issue create \
  --title "Feature: Advanced Authentication" \
  --body "Implement OAuth2 with social login..." \
  --label "enhancement,swarm-ready"

# Initialize swarm for issue
npx claude-flow@alpha hooks pre-task --description "Feature implementation"
```

### Project Board Quick Setup

```bash
# Get project ID
PROJECT_ID=$(gh project list --owner @me --format json | \
  jq -r '.projects[0].id')

# Initialize board sync
npx ruv-swarm github board-init \
  --project-id "$PROJECT_ID" \
  --sync-mode "bidirectional"
```

---

## Sub-Documentation

For detailed information, see the following files:

| Document | Contents |
|----------|----------|
| [Issues](./issues.md) | Issue creation, triage, batch operations, swarm conversion |
| [Boards](./boards.md) | Project boards, column management, automation |
| [Sprints](./sprints.md) | Sprint planning, milestones, velocity tracking |
| [Coordination](./coordination.md) | Swarm coordination, multi-repo workflows |

---

## Quick Reference

### Core Capabilities

| Capability | Description |
|------------|-------------|
| **Issue Management** | Create, triage, batch process issues |
| **Project Boards** | Automated board sync, column management |
| **Sprint Planning** | Sprint creation, milestone tracking |
| **Swarm Coordination** | Multi-agent task execution |

### Common Commands

```bash
# Issue operations
gh issue create --title "Title" --body "Body" --label "label"
gh issue list --label "label"
gh issue edit 123 --add-label "new-label"
gh issue close 123

# Project operations
gh project list --owner @me
gh project view PROJECT_ID
gh project item-add PROJECT_ID --url ISSUE_URL

# Swarm operations
npx ruv-swarm github issue-to-swarm 123
npx ruv-swarm github board-sync --project-id PROJECT_ID
```

### Label-Based Automation

```json
{
  "rules": [
    {
      "keywords": ["bug", "error", "broken"],
      "labels": ["bug", "swarm-debugger"],
      "agents": ["debugger", "tester"]
    },
    {
      "keywords": ["feature", "implement", "add"],
      "labels": ["enhancement", "swarm-feature"],
      "agents": ["architect", "coder", "tester"]
    },
    {
      "keywords": ["docs", "documentation", "readme"],
      "labels": ["documentation"],
      "agents": ["researcher", "writer"]
    }
  ]
}
```

### Issue Comment Commands

Execute swarm operations via issue comments:

```markdown
/swarm analyze
/swarm decompose 5
/swarm assign @agent-coder
/swarm estimate
/swarm start
```

---

## Swarm Integration

### Initialize Project Swarm

```javascript
// Initialize project management swarm
mcp__claude-flow__swarm_init { topology: "star", maxAgents: 3 }
mcp__claude-flow__agent_spawn { type: "coordinator", name: "Issue Coordinator" }
mcp__claude-flow__agent_spawn { type: "researcher", name: "Requirements Analyst" }
mcp__claude-flow__agent_spawn { type: "coder", name: "Implementation Planner" }

// Create comprehensive issue
mcp__github__create_issue {
  owner: "org",
  repo: "repository",
  title: "Integration Review: Complete system integration",
  body: "## Overview\n\nComprehensive review...",
  labels: ["integration", "review", "enhancement"]
}

// Set up automated tracking
mcp__claude-flow__task_orchestrate {
  task: "Monitor and coordinate issue progress",
  strategy: "adaptive",
  priority: "medium"
}
```

---

## GitHub Actions Integration

```yaml
# .github/workflows/project-sync.yml
name: Project Board Sync
on:
  issues:
    types: [opened, labeled, closed]
  pull_request:
    types: [opened, ready_for_review, closed]

jobs:
  sync-board:
    runs-on: ubuntu-latest
    steps:
      - name: Sync to Project Board
        run: |
          gh project item-add $PROJECT_ID --url ${{ github.event.issue.html_url }}
```

---

## Best Practices

1. **Use Labels Consistently** - Define and enforce label conventions
2. **Automate Triage** - Set up auto-labeling and assignment rules
3. **Sync Boards Bidirectionally** - Keep issues and boards in sync
4. **Track Velocity** - Use sprint metrics for planning
5. **Coordinate with Swarms** - Leverage multi-agent task execution

---

## Related Skills

- `github-pr-workflow` - Pull request management
- `github-release-management` - Release coordination
- `sparc-orchestrator` - Development methodology integration

---

**Version:** 2.0.0
**Last Updated:** 2025-10-19
