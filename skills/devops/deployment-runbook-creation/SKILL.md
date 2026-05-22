---
name: deployment-runbook-creation
description: "Generate deployment runbook documentation following the DEPLOYMENT-RUNBOOK template. Use when planning deployments, documenting procedures, or when the user asks for a runbook."
event: deployment-planning
auto_trigger: false
version: "1.0.0"
last_updated: "2026-01-26"

# Inputs/Outputs
inputs:
  - deployment_target
  - environment
  - services_affected
  - dependencies
  - rollback_strategy
output: deployment_runbook
output_format: "Markdown runbook (08-DEPLOYMENT-RUNBOOK-TEMPLATE.md)"
output_path: "docs/technical/infrastructure/"

# Auto-Trigger Rules
auto_invoke:
  events:
    - "deployment-planning"
    - "release-preparation"
  conditions:
    - "user requests deployment docs"
    - "new release being prepared"

# Validation
validation_rules:
  - "pre-deployment checklist included"
  - "rollback procedure documented"
  - "monitoring/alerting defined"
  - "contact information current"

# Chaining
chain_after: []
chain_before: [doc-index-update]

# Agent Association
called_by: ["@DevOps"]
mcp_tools:
  - container-tools_get-config
  - read_file
  - mcp_payment-syste_search_full_text
---

# Deployment Runbook Creation Skill

> **Purpose:** Generate deployment runbook documentation. Ensures safe, repeatable deployments with rollback procedures.

## Trigger

**When:** New release being prepared OR user requests deployment documentation
**Context Needed:** Services, environments, dependencies
**MCP Tools:** `container-tools_get-config`, `read_file`

## Required Sections

```markdown
# [Service/Feature] - Deployment Runbook

## Overview

- Service: [name]
- Version: [version]
- Environment: [dev/staging/prod]

## Pre-Deployment Checklist

- [ ] All tests passing
- [ ] Database migrations ready
- [ ] Config changes documented
- [ ] Monitoring alerts configured

## Deployment Steps

1. [step]
2. [step]

## Rollback Procedure

1. [step]
2. [step]

## Monitoring

- Health check: [URL]
- Logs: [location]
- Alerts: [channel]
```

## Environment-Specific Sections

### Development

````markdown
## Dev Deployment

```bash
bun run deploy:dev
```
````

`````

- Auto-deploys from `develop` branch
- No approval required

````

### Staging
```markdown
## Staging Deployment
```bash
bun run deploy:staging
````

- Requires PR approval
- Runs integration tests

````

### Production
```markdown
## Production Deployment
```bash
bun run deploy:prod
````

- Requires 2 approvals
- Maintenance window: [time]
- Rollback within: 15 minutes

````

## Contact Information

```markdown
## On-Call

| Role | Name | Contact |
|:-----|:-----|:--------|
| Primary | @oncall | [channel] |
| Secondary | @backup | [channel] |
| Escalation | @lead | [channel] |
````

## Reference

- [08-DEPLOYMENT-RUNBOOK-TEMPLATE.md](/docs/templates/08-DEPLOYMENT-RUNBOOK-TEMPLATE.md)
- [DOCKER-GUIDE.md](/docs/technical/infrastructure/DOCKER-GUIDE.md)

```

`````
