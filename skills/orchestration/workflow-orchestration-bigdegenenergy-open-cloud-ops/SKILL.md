# Workflow Orchestration Skill

> Design and execute typed, multi-step workflows with approval gates.

## Overview

The Lobster workflow engine enables deterministic pipelines that:

- Execute steps in sequence with state tracking
- Pause at approval gates for human verification
- Persist state across sessions
- Handle failures gracefully

## Core Concepts

### Workflow Definition

A YAML file defining the pipeline:

```yaml
name: feature-pipeline
description: Complete feature implementation

steps:
  - name: plan
    command: /plan

  - name: implement
    agent: "@typescript-pro"

  - name: test
    command: /qa
    gate:
      type: manual
      message: "Tests pass. Continue?"

on_failure: notify
```

### Step Types

| Type     | Usage                      | Example                 |
| -------- | -------------------------- | ----------------------- |
| command  | Execute a slash command    | `/plan`, `/qa`, `/ship` |
| agent    | Invoke a subagent          | `@code-reviewer`        |
| shell    | Run a shell command        | `npm test`              |
| parallel | Execute steps concurrently | Multiple agents at once |

### Gate Types

| Type        | When to Use                              |
| ----------- | ---------------------------------------- |
| manual      | Critical decisions (deploy, ship)        |
| timeout     | Non-critical checks (auto-approve in 5m) |
| conditional | Based on previous step output            |

## Workflow Patterns

### Pattern 1: Feature Development

```yaml
name: feature-pipeline
steps:
  - name: plan
    command: /plan
    inputs:
      description: "{{ feature_description }}"

  - name: implement
    agent: "@typescript-pro"
    inputs:
      task: "Implement the plan"

  - name: test
    command: /qa
    gate:
      type: conditional
      condition: "test_results.failed == 0"

  - name: review
    agent: "@code-reviewer"
    gate:
      type: manual
      message: "Review complete. Ship?"

  - name: ship
    command: /ship
```

### Pattern 2: Security Audit

```yaml
name: security-audit
steps:
  - name: scan
    agent: "@security-auditor"
    outputs:
      - findings

  - name: analyze
    agent: "@zeno-analyzer"
    gate:
      type: conditional
      condition: "findings.critical == 0"
      fallback: fail

  - name: report
    shell: |
      echo "## Security Audit Report" > report.md
      # Generate report

  - name: notify
    command: /notify
    inputs:
      channel: "#security"
```

### Pattern 3: Staged Deployment

```yaml
name: deploy-pipeline
steps:
  - name: build
    shell: "npm run build"

  - name: test
    shell: "npm test"
    gate:
      type: conditional
      condition: "exit_code == 0"

  - name: deploy-staging
    command: /deploy-staging
    gate:
      type: timeout
      timeout_seconds: 300
      message: "Staging deployed. Auto-continues in 5 minutes."

  - name: smoke-test
    agent: "@test-automator"
    inputs:
      environment: staging

  - name: deploy-production
    shell: "npm run deploy:prod"
    gate:
      type: manual
      message: "Deploy to production?"
      approvers:
        - lead-developer
        - devops-team
```

## Variables and Templating

Use `{{ variable }}` for dynamic values:

```yaml
steps:
  - name: plan
    command: /plan
    inputs:
      description: "{{ feature_description }}"
      priority: "{{ priority }}"
```

Pass variables when starting:

```
/workflow feature-pipeline --var feature_description="Add OAuth" --var priority=high
```

## State Management

Workflow state is persisted in `.claude/artifacts/workflow-state/`:

```
workflow-state/
├── feature-pipeline-abc123.json       # Workflow state
├── feature-pipeline-abc123.approval.json  # Pending approval
└── feature-pipeline-abc123.lock       # Concurrency lock
```

### State Fields

| Field            | Description                         |
| ---------------- | ----------------------------------- |
| workflow_id      | Unique execution ID                 |
| status           | Current status (RUNNING, PAUSED...) |
| current_step     | Index of current/last step          |
| step_results     | Results of completed steps          |
| pending_approval | Step waiting for approval           |
| variables        | Workflow variables                  |

## Error Handling

### Retry Configuration

```yaml
steps:
  - name: flaky-test
    shell: "npm run e2e"
    retry_count: 3
    timeout_seconds: 300
```

### Continue on Failure

```yaml
steps:
  - name: optional-lint
    shell: "npm run lint"
    continue_on_failure: true
```

### Failure Actions

```yaml
on_failure: notify  # Send notification
on_failure: rollback  # (not yet implemented)
on_failure: continue  # Continue anyway
```

## Best Practices

1. **Gate Critical Steps**: Always add manual gates before deploy/ship
2. **Use Conditions**: Auto-approve non-critical gates based on metrics
3. **Set Timeouts**: Prevent workflows from hanging indefinitely
4. **Persist State**: Let workflows resume across sessions
5. **Notify on Gate**: Alert team when approval is needed

## Integration Points

| Component           | Integration                  |
| ------------------- | ---------------------------- |
| `/workflow`         | Start a workflow             |
| `/workflow-status`  | Check progress               |
| `/workflow-approve` | Approve pending gate         |
| Gateway             | Approve via Slack/Discord    |
| Notifications       | Alert when gates are reached |

## Activation Triggers

This skill activates when prompts contain:

- "workflow", "pipeline", "orchestrat"
- "approval gate", "multi-step"
- "lobster", "typed workflow"
- "pause for approval", "wait for review"
