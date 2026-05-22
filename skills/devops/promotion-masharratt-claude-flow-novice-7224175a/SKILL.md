---
name: cfn-promotion
version: 1.0.0
description: Skill Promotion Workflow - Atomic promotion from staging to production
author: CFN Integration Team
tags: [promotion, deployment, staging, production, sla]
dependencies: [cfn-coordination, cfn-deployment]
---

# Skill Promotion Workflow

Manages atomic promotion of skills from staging directory to production with validation, SLA enforcement, and optional auto-deployment.

## Overview

The skill promotion workflow automates the process of moving generated skills from the staging directory to production, ensuring:

- **Atomic Operations**: Skills are moved atomically to prevent partial promotions
- **Pre-Promotion Validation**: Content integrity, schema compliance, and test execution
- **SLA Enforcement**: Skills older than 48 hours in staging trigger alerts
- **Git Integration**: Optional automatic commit with promotion metadata
- **Auto-Deployment**: Optional integration with deployment pipeline (Task 1.1)

## Architecture

```
.claude/skills/
├── staging/              # Skills pending promotion (temporary)
│   ├── auth-v2/
│   │   ├── SKILL.md
│   │   ├── execute.sh
│   │   └── test.sh
│   └── logging-v3/
│       └── ...
└── [production]/         # Production skills (after promotion)
    ├── authentication/
    ├── logging/
    └── ...
```

## Usage

### CLI Script

```bash
# List all staged skills
./scripts/promote-staged-skills.sh --list

# Check for stale skills (>48h)
./scripts/promote-staged-skills.sh --check-stale

# Promote a specific skill (with confirmation prompt)
./scripts/promote-staged-skills.sh .claude/skills/staging/auth-v2

# Auto-promote if validation passes (no prompt)
./scripts/promote-staged-skills.sh .claude/skills/staging/auth-v2 --auto

# Promote with git commit and deployment
./scripts/promote-staged-skills.sh .claude/skills/staging/auth-v2 --auto --git-commit --deploy

# Force promotion (skip validation - admin only)
./scripts/promote-staged-skills.sh .claude/skills/staging/auth-v2 --force --auto
```

### TypeScript API

```typescript
import { SkillPromotionService } from './src/services/skill-promotion';
import { DatabaseService } from './src/lib/database-service';

const dbService = new DatabaseService({ type: 'sqlite', path: './data/cfn.db' });
const promotionService = new SkillPromotionService(dbService);

// Promote a skill
const result = await promotionService.promoteSkill(
  '.claude/skills/staging/auth-v2',
  {
    autoDeploy: true,
    gitCommit: true,
    notify: true,
    promotedBy: 'admin@example.com'
  }
);

if (result.success) {
  console.log(`Skill promoted: ${result.skillName}`);
  console.log(`Production path: ${result.productionPath}`);
  console.log(`Deployment ID: ${result.deploymentId}`);
} else {
  console.error(`Promotion failed: ${result.error}`);
}

// List staged skills
const stagedSkills = await promotionService.listStagedSkills();
console.log(`${stagedSkills.length} skills in staging`);

// Check for stale skills (>48h)
const staleSkills = await promotionService.checkStaleness();
if (staleSkills.length > 0) {
  console.log(`WARNING: ${staleSkills.length} stale skills detected`);
  for (const skill of staleSkills) {
    console.log(`  - ${skill.name} (${skill.ageHours}h, ${skill.slaBreachHours}h over SLA)`);
  }
}
```

## Validation Checks

The promotion validator performs the following checks:

### 1. Content Integrity
- `SKILL.md` exists and is readable
- `execute.sh` exists and is executable
- Optional: `test.sh`, `README.md` (warnings if missing)

### 2. Schema Compliance
- Frontmatter is valid YAML
- Required fields: `name`, `description`, `version`
- Version follows semantic versioning (X.Y.Z)
- Optional fields: `author`, `tags`, `dependencies`

### 3. Test Execution
- If `test.sh` exists, it must be executable
- Tests run with 30-second timeout
- Test failures generate warnings (non-fatal, allow --force)

### 4. Conflict Detection
- Check if production skill already exists
- Compare versions (staging vs production)
- Warn if overwriting (require --overwrite flag)

## SLA Enforcement

Skills in staging for >48 hours trigger SLA breach alerts:

### Manual Checking
```bash
./scripts/promote-staged-skills.sh --check-stale
```

### Automated Checking (Cron Job)
```bash
# Run daily at 9am to check for stale skills
0 9 * * * cd /path/to/project && ./scripts/promote-staged-skills.sh --check-stale
```

### Background Job (TypeScript)
```typescript
import { PromotionSLAEnforcer } from './src/jobs/promotion-sla-enforcer';

const enforcer = new PromotionSLAEnforcer(dbService, {
  autoPromote: true,  // Auto-promote stale skills
  notifyStale: true,  // Send notifications
});

await enforcer.enforceSLA();
```

## Configuration

Environment variables:

```bash
# SLA threshold (hours)
CFN_PROMOTION_SLA_THRESHOLD=48

# Auto-promote stale skills
CFN_PROMOTION_AUTO_PROMOTE=true

# Enable git commits
CFN_PROMOTION_GIT_COMMIT=true

# Enable auto-deployment
CFN_PROMOTION_AUTO_DEPLOY=true
```

## Monitoring

### Database Queries

```sql
-- Skills currently in staging
SELECT name, created_at,
       ROUND((julianday('now') - julianday(created_at)) * 24, 1) as age_hours
FROM staged_skills
WHERE promoted = 0
ORDER BY created_at ASC;

-- Promotion success rate (last 30 days)
SELECT
  COUNT(*) as total_promotions,
  SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successful,
  ROUND(100.0 * SUM(success) / COUNT(*), 2) as success_rate
FROM skill_promotions
WHERE promoted_at > datetime('now', '-30 days');

-- SLA breaches (skills >48h in staging)
SELECT COUNT(*) as sla_breaches
FROM staged_skills
WHERE promoted = 0
  AND created_at < datetime('now', '-48 hours');
```

### Dashboard Metrics

- **Staged Skills Count**: Number of skills awaiting promotion
- **Average Time in Staging**: Mean age of staged skills
- **SLA Breach Count**: Skills >48h in staging
- **Promotion Success Rate**: Successful promotions / total attempts
- **Auto-Deploy Success Rate**: Successful deployments / total promotions

## Integration Points

### Task 1.1: Skill Deployment Pipeline
After promotion, skills can be automatically deployed:

```typescript
const result = await promotionService.promoteSkill(stagingPath, {
  autoDeploy: true  // Triggers SkillDeploymentPipeline
});
```

### Task 0.5: Utilities
- `file-operations.ts`: Atomic moves, file locking
- `logging.ts`: Structured logging
- `errors.ts`: Error handling

### Phase 4: Skill Generation
Generated skills are placed in staging directory:

```typescript
// Skill generator outputs to staging
const stagingPath = await skillGenerator.generate({
  output: '.claude/skills/staging/new-skill'
});

// Later: promote to production
await promotionService.promoteSkill(stagingPath);
```

## Error Handling

### Promotion Failures
- Validation errors: Fix skill and retry
- Conflicts: Use `--overwrite` or resolve manually
- Test failures: Use `--force` (admin only) or fix tests

### Rollback
If promotion fails mid-operation:

1. Staging skill remains in staging (atomic move failed)
2. Production skill is unchanged (or restored from backup)
3. Database records rollback
4. Git commits are not created

### Manual Rollback
```bash
# If promotion succeeded but deployment failed
rm -rf .claude/skills/production-skill
mv .claude/skills/staging/backup-skill .claude/skills/staging/production-skill
```

## Troubleshooting

### "Validation failed: Missing required file: execute.sh"
**Solution**: Add execute.sh to staged skill

### "execute.sh is not executable"
**Solution**: Run `chmod +x execute.sh`

### "Tests failed (non-fatal)"
**Solution**: Fix tests or use `--force` to skip

### "Skill already exists in production"
**Solution**: Use `--overwrite` flag or choose different name

### "Git commit failed"
**Solution**: Ensure git repo is initialized and configured

## Best Practices

1. **Always validate before promotion** (don't use --force unless necessary)
2. **Run tests in staging** before promotion
3. **Monitor SLA breaches** (check stale skills daily)
4. **Use git commits** for audit trail
5. **Enable auto-deployment** for production readiness
6. **Backup production skills** before overwriting
7. **Test promotions in dev environment** first

## Future Enhancements

- [ ] Webhook notifications (Slack, email)
- [ ] Multi-stage promotion (staging → qa → production)
- [ ] Approval workflows (require manual approval for production)
- [ ] Promotion rollback automation
- [ ] Integration with CI/CD pipelines
- [ ] Promotion scheduling (promote at specific times)
- [ ] Batch promotion (promote multiple skills at once)

## Related Documentation

- **Task 1.1**: `.claude/skills/cfn-deployment/SKILL.md`
- **Task 0.5**: `docs/IMPLEMENTATION_UTILITIES.md`
- **Phase 4**: `docs/SKILL_GENERATION.md` (future)
- **Operational Guide**: `docs/SKILL_PROMOTION_WORKFLOW.md`
