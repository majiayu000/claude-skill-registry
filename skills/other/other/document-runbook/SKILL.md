---
name: document-runbook
description: Document CI/CD, deployment, and operational procedures. Use when creating runbooks, documenting deployment processes, or writing operational guides.
---

# Runbook Documentation Skill

## Purpose

Create operational runbooks for deployment, database operations, incident response, and maintenance procedures. These are "How-To" documents in the Diátaxis framework, specifically for operations tasks.

## Smart Interaction

### ASK the User When:

- **Creating new runbook**: Confirm process name and risk level
- **Deleting runbook**: Always confirm before deletion
- **High-risk procedures**: Confirm rollback steps are adequate

### PROCEED Autonomously When:

- **Updating existing runbook**: Add new steps, update commands
- **Adding troubleshooting**: Enhance with new failure scenarios
- **Fixing commands**: Correct outdated or broken commands
- **Adding verification steps**: Improve procedure completeness

## Documentation Principles (CRITICAL)

**Before writing ANY documentation**, review `../DOCUMENTATION_PRINCIPLES.md` for:

1. **Ground Truth Only** - Document what exists in code, no speculation
2. **Writing Tone** - Clear and educational without audience labels
3. **Code Examples** - Real files with paths and line numbers
4. **Performance Docs** - Techniques + measurement methods, NOT estimated timings
5. **What NOT to include** - No troubleshooting, future work, or meta-commentary
6. **Diagrams** - Use when they clarify technicals, not for decoration

These principles override any template suggestions that conflict with them.

**Note**: Runbooks are the APPROPRIATE place for troubleshooting content (unlike feature docs).

## Instructions

When documenting operational procedures:

1. **Identify the process** (deploy, rollback, migration, etc.)
2. **Use the runbook template** at `templates/runbook.md`
3. **Include actual commands** that can be copy-pasted
4. **Document failure scenarios** and recovery steps
5. **Output to** `/docs/operations/[process-name].md`

## Template

Use the template at: `.claude/skills/document-runbook/templates/runbook.md`

## Runbook Categories

Organize runbooks by category:

```
docs/operations/
├── index.md                    # Operations overview
├── deployment/
│   ├── deploy-to-production.md
│   ├── deploy-to-staging.md
│   └── rollback-deployment.md
├── database/
│   ├── database-migration.md
│   ├── backup-restore.md
│   └── seed-data.md
├── maintenance/
│   ├── dependency-updates.md
│   └── log-rotation.md
└── incident-response/
    ├── service-outage.md
    └── data-corruption.md
```

## Command Standards

- All commands must be copy-paste ready
- Use environment variables for secrets: `$DATABASE_URL`
- Include `--dry-run` options where available
- Show both successful and error outputs

## Risk Levels

| Level  | Definition                           | Review Required |
| ------ | ------------------------------------ | --------------- |
| Low    | No data loss risk, easily reversible | None            |
| Medium | Potential service disruption         | Team lead       |
| High   | Data loss risk, hard to reverse      | Team approval   |

## Output Location

| Category    | Output Path                                    |
| ----------- | ---------------------------------------------- |
| Deployment  | `/docs/operations/deployment/[name].md`        |
| Database    | `/docs/operations/database/[name].md`          |
| Maintenance | `/docs/operations/maintenance/[name].md`       |
| Incident    | `/docs/operations/incident-response/[name].md` |

## Quality Checklist

Before completing:

- [ ] All commands are copy-paste ready
- [ ] Expected outputs documented
- [ ] Failure scenarios covered
- [ ] Rollback procedure included
- [ ] Troubleshooting table complete
- [ ] Prerequisites clearly listed
- [ ] Time estimate provided
- [ ] Risk level assessed
- [ ] Emergency contacts included (for high-risk)

## Examples

### Creating New Runbooks (Will Ask User)

- "Create a deployment runbook" → Ask: Risk level? Environment?
- "Document the database migration process" → Confirm category and scope

### Updating Existing Runbooks (Autonomous)

- "Add new step to deployment runbook" → Updates existing doc
- "Fix the database restore command" → Corrects command
- "Add troubleshooting for timeout errors" → Adds to troubleshooting table

### By Category

- "Document production deployment" → `/docs/operations/deployment/deploy-to-production.md`
- "Create database backup runbook" → `/docs/operations/database/backup-restore.md`
- "Write incident response for outages" → `/docs/operations/incident-response/service-outage.md`
