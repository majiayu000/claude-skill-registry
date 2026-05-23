---
name: github-issue-tracker
description: Intelligent issue management and project coordination with automated tracking, progress monitoring, and team coordination. Use for issue creation with smart templates, progress tracking with swarm coordination, multi-agent collaboration, and cross-repository synchronization.
---

# GitHub Issue Tracker Skill

## Overview

Intelligent issue management with swarm coordination. This skill handles automated issue creation, progress tracking, multi-agent collaboration on complex issues, project milestone coordination, and cross-repository issue synchronization.

## Quick Start

```bash
# Create an issue
gh issue create --title "Bug: Login fails" --body "Steps to reproduce..." --label "bug"

# List open issues
gh issue list --state open

# View issue details
gh issue view 54

# Add comment to issue
gh issue comment 54 --body "Progress update..."

# Close issue
gh issue close 54 --reason completed
```

## When to Use

- Creating issues with smart templates
- Tracking issue progress with swarm coordination
- Multi-agent collaboration on complex issues
- Project milestone coordination
- Cross-repository issue synchronization
- Automated issue labeling and organization

## Core Capabilities

| Capability | Description |
|------------|-------------|
| Smart templates | Automated issue creation with templates |
| Progress tracking | Swarm-coordinated updates |
| Multi-agent collaboration | Complex issue resolution |
| Milestone coordination | Project workflow integration |
| Cross-repo sync | Monorepo issue management |

## Usage Examples

### 1. Create Issue with Swarm Tracking

```javascript
// Initialize issue management swarm
mcp__claude-flow__swarm_init({ topology: "star", maxAgents: 3 })
mcp__claude-flow__agent_spawn({ type: "coordinator", name: "Issue Coordinator" })
mcp__claude-flow__agent_spawn({ type: "researcher", name: "Requirements Analyst" })
mcp__claude-flow__agent_spawn({ type: "coder", name: "Implementation Planner" })

// Set up automated tracking
mcp__claude-flow__task_orchestrate({
    task: "Monitor and coordinate issue progress with automated updates",
    strategy: "adaptive",
    priority: "medium"
})
```

### 2. Create Comprehensive Issue with gh CLI

```bash
gh issue create \
  --repo owner/repo \
  --title "Integration Review: claude-code-flow and ruv-swarm" \
  --body "## Overview
Comprehensive review and integration between packages.

## Objectives
- [ ] Verify dependencies and imports
- [ ] Ensure MCP tools integration
- [ ] Check hook system integration
- [ ] Validate memory systems alignment

## Swarm Coordination
This issue will be managed by coordinated swarm agents." \
  --label "integration,review,enhancement" \
  --assignee username
```

### 3. Automated Progress Updates

```javascript
// Update issue with progress from swarm memory
mcp__claude-flow__memory_usage({
    action: "retrieve",
    key: "issue/54/progress"
})

// Store progress
mcp__claude-flow__memory_usage({
    action: "store",
    key: "issue/54/latest_update",
    value: JSON.stringify({
        timestamp: Date.now(),
        progress: "89%",
        status: "near_completion"
    })
})
```

```bash
# Add progress comment
gh issue comment 54 --body "## Progress Update

### Completed Tasks
- Architecture review completed
- Dependency analysis finished
- Integration testing verified

### Current Status
- Documentation review in progress
- Integration score: 89% (Excellent)

### Next Steps
- Final validation and merge preparation"
```

### 4. Search and Coordinate Related Issues

```bash
# Search related issues
gh issue list --repo owner/repo --label "integration" --state open --json number,title,labels

# Update issue with milestone
gh issue edit 54 --milestone "v1.0.0"

# Add labels
gh issue edit 54 --add-label "in-progress"

# Transfer issue
gh issue transfer 54 owner/new-repo
```

### 5. Batch Issue Operations

```javascript
[Single Message - Issue Lifecycle Management]:
    // Initialize issue coordination swarm
    mcp__claude-flow__swarm_init({ topology: "mesh", maxAgents: 4 })
    mcp__claude-flow__agent_spawn({ type: "coordinator", name: "Issue Manager" })
    mcp__claude-flow__agent_spawn({ type: "analyst", name: "Progress Tracker" })
    mcp__claude-flow__agent_spawn({ type: "researcher", name: "Context Gatherer" })

    // Create multiple related issues
    Bash(`gh issue create --repo owner/repo \
      --title "Feature: Advanced GitHub Integration" \
      --body "Implement comprehensive GitHub workflow automation..." \
      --label "feature,github,high-priority"`)

    Bash(`gh issue create --repo owner/repo \
      --title "Bug: PR merge conflicts" \
      --body "Resolve merge conflicts in integration branch..." \
      --label "bug,integration,urgent"`)

    Bash(`gh issue create --repo owner/repo \
      --title "Documentation: Update integration guides" \
      --body "Update all documentation for new workflows..." \
      --label "documentation,integration"`)

    // Track in todos
    TodoWrite({ todos: [
      { id: "github-feature", content: "Implement GitHub integration", status: "pending", priority: "high" },
      { id: "merge-conflicts", content: "Resolve PR conflicts", status: "pending", priority: "critical" },
      { id: "docs-update", content: "Update documentation", status: "pending", priority: "medium" }
    ]})

    // Store coordination state
    mcp__claude-flow__memory_usage({
        action: "store",
        key: "project/github_integration/issues",
        value: JSON.stringify({ created: Date.now(), total_issues: 3, status: "initialized" })
    })
```

## Smart Issue Templates

### Integration Issue Template

```markdown
## Integration Task

### Overview
[Brief description of integration requirements]

### Objectives
- [ ] Component A integration
- [ ] Component B validation
- [ ] Testing and verification
- [ ] Documentation updates

### Integration Areas

#### Dependencies
- [ ] Package.json updates
- [ ] Version compatibility
- [ ] Import statements

#### Functionality
- [ ] Core feature integration
- [ ] API compatibility
- [ ] Performance validation

#### Testing
- [ ] Unit tests
- [ ] Integration tests
- [ ] End-to-end validation

### Swarm Coordination
- **Coordinator**: Overall progress tracking
- **Analyst**: Technical validation
- **Tester**: Quality assurance
- **Documenter**: Documentation updates
```

### Bug Report Template

```markdown
## Bug Report

### Problem Description
[Clear description of the issue]

### Expected Behavior
[What should happen]

### Actual Behavior
[What actually happens]

### Reproduction Steps
1. [Step 1]
2. [Step 2]
3. [Step 3]

### Environment
- Package: [package name and version]
- Node.js: [version]
- OS: [operating system]

### Investigation Plan
- [ ] Root cause analysis
- [ ] Fix implementation
- [ ] Testing and validation
- [ ] Regression testing

### Swarm Assignment
- **Debugger**: Issue investigation
- **Coder**: Fix implementation
- **Tester**: Validation and testing
```

## MCP Tool Integration

### Swarm Coordination

```javascript
mcp__claude-flow__swarm_init({
    topology: "star",  // Central coordinator with peripheral agents
    maxAgents: 3,
    strategy: "adaptive"
})
```

### Memory Management

```javascript
// Store issue state
mcp__claude-flow__memory_usage({
    action: "store",
    key: "issue/54/state",
    namespace: "issues",
    value: JSON.stringify({
        status: "in-progress",
        assignees: ["user1"],
        labels: ["bug", "high-priority"],
        lastUpdate: Date.now()
    })
})

// Search issues in memory
mcp__claude-flow__memory_search({
    pattern: "issue/*",
    namespace: "issues",
    limit: 20
})
```

## Best Practices

### 1. Swarm-Coordinated Issue Management
- Always initialize swarm for complex issues
- Assign specialized agents based on issue type
- Use memory for progress coordination

### 2. Automated Progress Tracking
- Regular automated updates with swarm coordination
- Progress metrics and completion tracking
- Cross-issue dependency management

### 3. Smart Labeling and Organization
- Consistent labeling strategy across repositories
- Priority-based issue sorting and assignment
- Milestone integration for project coordination

### 4. Batch Issue Operations
- Create multiple related issues simultaneously
- Bulk updates for project-wide changes
- Coordinated cross-repository issue management

## Integration with Other Skills

| Skill | Integration |
|-------|-------------|
| `github-pr-manager` | Link issues to pull requests |
| `github-release-manager` | Coordinate release issues |
| `sparc-workflow` | Complex project coordination |
| `agent-orchestration` | Multi-agent issue resolution |

## Metrics and Analytics

### Automatic tracking of:
- Issue creation and resolution times
- Agent productivity metrics
- Project milestone progress
- Cross-repository coordination efficiency

### Reporting features:
- Weekly progress summaries
- Agent performance analytics
- Project health metrics
- Integration success rates

---

## Version History

- **1.0.0** (2025-01-02): Initial release - converted from issue-tracker agent
