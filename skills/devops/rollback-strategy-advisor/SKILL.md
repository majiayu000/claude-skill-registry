---
name: rollback-strategy-advisor
description: Suggests rollback strategies for failed deployments across different platforms and failure types. Use when deployments fail and need to be reverted, including application code rollbacks, database migration reversions, infrastructure changes, and configuration updates. Supports Docker/Docker Compose environments with step-by-step procedural guidance for safe and effective rollback execution.
---

# Rollback Strategy Advisor

Provide safe and effective rollback strategies for failed deployments.

## Core Capabilities

This skill helps recover from failed deployments by:

1. **Assessing failure impact** - Identifying what failed and what needs rollback
2. **Recommending rollback strategy** - Choosing the appropriate approach based on failure type
3. **Providing step-by-step guidance** - Clear procedural instructions for execution
4. **Validating rollback success** - Ensuring system returns to stable state
5. **Preventing data loss** - Protecting critical data during rollback operations

## Rollback Strategy Workflow

### Step 1: Assess the Failure

Understand what failed and the scope of impact.

**Key Questions:**

- What component failed? (Application, database, infrastructure, configuration)
- When did the failure occur? (During deployment, post-deployment, gradual degradation)
- What is the current system state? (Partially deployed, fully deployed, crashed)
- Is the system serving traffic? (Production load, maintenance mode, offline)
- Are there data changes? (Database migrations applied, user data modified)

**Gather Information:**

```bash
# Check deployment status
docker ps -a  # Container status
docker logs <container-name> --tail 100  # Recent logs

# Check system health
curl http://localhost:8080/health  # Health endpoint
docker stats  # Resource usage

# Identify deployment artifacts
docker images | grep <app-name>  # Available images
git log --oneline -10  # Recent commits
```

**Output: Failure Assessment**

```
Component: Application container
Failure Time: 5 minutes post-deployment
System State: New version deployed, returning 500 errors
Traffic: Receiving production traffic (degraded service)
Data Changes: No database migrations in this deployment
```

### Step 2: Choose Rollback Strategy

Select the appropriate strategy based on failure type and system state.

**Strategy Decision Tree:**

```
Is database migration involved?
├─ YES → See "Database Rollback Strategy" (Step 3.4)
└─ NO → Continue

Is infrastructure changed?
├─ YES → See "Infrastructure Rollback Strategy" (Step 3.3)
└─ NO → Continue

Is configuration changed?
├─ YES → See "Configuration Rollback Strategy" (Step 3.2)
└─ NO → Application Code Rollback (Step 3.1)
```

**Common Strategies:**

| Failure Type | Strategy | Risk Level | Downtime |
|--------------|----------|------------|----------|
| Application code bug | Redeploy previous image | Low | Seconds |
| Configuration error | Restore previous config | Low | Seconds |
| Infrastructure change | Revert compose file | Medium | Minutes |
| Database migration | Reverse migration + app rollback | High | Minutes |
| Multiple components | Sequential rollback (reverse order) | High | Minutes |

### Step 3: Execute Rollback

Perform the rollback with validation at each step.

#### Step 3.1: Application Code Rollback

Revert to the previous working application version.

**Standard Procedure:**

```bash
# 1. Identify previous working version
docker images | grep <app-name>
# Look for the previous tag (e.g., v1.2.3 if current is v1.2.4)

# 2. Stop current containers
docker-compose stop <service-name>

# 3. Update docker-compose.yml to previous version
# Change: image: myapp:v1.2.4 → image: myapp:v1.2.3

# 4. Start with previous version
docker-compose up -d <service-name>

# 5. Validate rollback (see Step 4)
curl http://localhost:8080/health
docker logs <service-name> --tail 50
```

**Fast Rollback (if compose file unchanged):**

```bash
# Restart with previous image tag
docker-compose stop <service-name>
docker run -d --name <service-name> \
  --network <network-name> \
  -p 8080:8080 \
  myapp:v1.2.3

# Or update compose and restart
sed -i 's/myapp:v1.2.4/myapp:v1.2.3/g' docker-compose.yml
docker-compose up -d <service-name>
```

**Considerations:**

- Keep previous images available (don't prune immediately after deploy)
- Tag images with version numbers or git commit SHAs
- Test the previous version still works in staging first if possible
- Monitor resource usage during rollback

#### Step 3.2: Configuration Rollback

Restore previous configuration files or environment variables.

**Configuration File Rollback:**

```bash
# 1. Locate configuration backup or git history
git log -- config/app.conf
git show HEAD~1:config/app.conf > config/app.conf

# 2. Update mounted config in docker-compose.yml if needed
# Ensure volume mount points to correct config

# 3. Restart services to load previous config
docker-compose restart <service-name>

# 4. Validate configuration loaded correctly
docker exec <service-name> cat /app/config/app.conf
curl http://localhost:8080/health
```

**Environment Variable Rollback:**

```bash
# 1. Edit docker-compose.yml to restore previous env vars
# Update the environment section or .env file

# 2. Recreate container with new env vars
docker-compose up -d --force-recreate <service-name>

# 3. Verify environment variables
docker exec <service-name> env | grep APP_
```

**Feature Flag Rollback:**

```bash
# If using feature flags, disable the problematic feature
# Update flag config or environment variable
# Example: FEATURE_NEW_CHECKOUT=false

docker-compose restart <service-name>
```

**Considerations:**

- Keep configuration in version control (git)
- Use .env files for environment-specific configs
- Backup configs before deployment
- Validate config syntax before applying

#### Step 3.3: Infrastructure Rollback

Revert infrastructure changes like network configurations, volume mounts, or docker-compose structure.

**Docker Compose Rollback:**

```bash
# 1. Restore previous docker-compose.yml from git
git checkout HEAD~1 -- docker-compose.yml

# 2. Recreate infrastructure
docker-compose down
docker-compose up -d

# 3. Validate all services running
docker-compose ps
docker-compose logs --tail 50
```

**Network Configuration Rollback:**

```bash
# If network configuration changed
# 1. Remove new network
docker network rm <new-network>

# 2. Recreate previous network
docker network create --driver bridge <old-network>

# 3. Reconnect containers
docker network connect <old-network> <container-name>
```

**Volume Rollback:**

```bash
# If volume mounts changed (be careful with data!)
# 1. Stop services
docker-compose stop

# 2. Update docker-compose.yml volume configuration
git checkout HEAD~1 -- docker-compose.yml

# 3. Restart services
docker-compose up -d

# Note: Data in volumes persists, only mount configuration changes
```

**Considerations:**

- Infrastructure changes may affect multiple services
- Test in staging environment first if possible
- Document infrastructure dependencies
- Consider using infrastructure-as-code tools (Terraform)

#### Step 3.4: Database Rollback

Reverse database migrations and restore schema to previous state.

**Migration Rollback (with Migration Tool):**

```bash
# Using Alembic (Python)
docker exec <db-container> alembic downgrade -1  # Rollback one migration
docker exec <db-container> alembic downgrade <revision>  # Rollback to specific revision

# Using Flyway (Java)
docker exec <app-container> flyway undo  # Rollback last migration

# Using Django
docker exec <app-container> python manage.py migrate <app> <migration>

# Using Rails
docker exec <app-container> rails db:rollback STEP=1
```

**Manual Migration Rollback:**

```bash
# 1. Identify the migration to reverse
docker exec <db-container> psql -U user -d dbname -c "\d+"  # List tables

# 2. Execute reverse migration SQL
docker exec <db-container> psql -U user -d dbname -f /migrations/rollback_v1.2.4.sql

# 3. Verify schema state
docker exec <db-container> psql -U user -d dbname -c "\d table_name"
```

**Database Rollback with Application:**

```bash
# CRITICAL: Rollback database BEFORE rolling back application
# to prevent new app code from working with old schema

# 1. Stop application (prevent new requests)
docker-compose stop app-service

# 2. Backup current database state
docker exec <db-container> pg_dump -U user dbname > backup_$(date +%Y%m%d_%H%M%S).sql

# 3. Rollback migration
docker exec <db-container> alembic downgrade -1

# 4. Rollback application to version compatible with old schema
docker-compose stop app-service
sed -i 's/myapp:v1.2.4/myapp:v1.2.3/g' docker-compose.yml
docker-compose up -d app-service

# 5. Validate
curl http://localhost:8080/health
docker logs app-service --tail 50
```

**Considerations:**

- **Always backup before rollback** - Database changes are risky
- Coordinate app and DB rollback carefully
- Test rollback migrations in staging
- Consider data loss implications (irreversible data changes)
- For destructive migrations (dropped columns), may need data restore from backup
- Use database versioning tools (Alembic, Flyway, Liquibase)

See `references/database_rollback_patterns.md` for detailed migration rollback examples and data preservation strategies.

### Step 4: Validate Rollback Success

Confirm the system is working correctly after rollback.

**Health Checks:**

```bash
# 1. Container health
docker ps  # All containers running?
docker-compose ps  # Services in "Up" state?

# 2. Application health
curl http://localhost:8080/health
curl -I http://localhost:8080  # HTTP status code

# 3. Service logs
docker logs <service-name> --tail 100 | grep ERROR
docker logs <service-name> --tail 100 | grep WARN

# 4. Database connectivity
docker exec <app-container> psql -U user -d dbname -c "SELECT 1;"

# 5. Resource usage
docker stats --no-stream
```

**Functional Testing:**

```bash
# Test critical user flows
curl -X POST http://localhost:8080/api/login -d '{"user":"test","pass":"test"}'
curl http://localhost:8080/api/users/1

# Run smoke tests if available
docker exec <app-container> pytest tests/smoke/

# Check monitoring dashboards
# - Response times back to normal?
# - Error rates dropped?
# - Traffic being served?
```

**Validation Checklist:**

- ✓ All containers running
- ✓ Health endpoints returning 200
- ✓ No error spikes in logs
- ✓ Database queries executing
- ✓ Critical API endpoints responding
- ✓ Monitoring shows normal metrics
- ✓ Users can access the application

### Step 5: Document and Communicate

Record the incident and inform stakeholders.

**Incident Report Template:**

```markdown
## Deployment Rollback - [Date/Time]

**Summary:** Brief description of what failed and rollback action taken

**Timeline:**
- [Time] - Deployment started (v1.2.4)
- [Time] - Failure detected (500 errors)
- [Time] - Rollback initiated
- [Time] - Rollback completed
- [Time] - System validated stable

**Root Cause:** What caused the deployment to fail

**Rollback Actions:**
1. Stopped application service
2. Reverted docker-compose.yml to v1.2.3
3. Restarted service
4. Validated health checks

**Impact:**
- Downtime: X minutes
- Affected users: Y requests failed
- Data loss: None

**Follow-up Actions:**
- [ ] Fix root cause in v1.2.5
- [ ] Add test coverage for failure scenario
- [ ] Update deployment checklist
- [ ] Review rollback procedure effectiveness
```

**Communication:**

```
Team notification (Slack/email):

🚨 Deployment Rollback Completed

We rolled back the v1.2.4 deployment due to [issue].
System is now stable on v1.2.3.

Impact: X minutes downtime
Status: Fully operational
Next steps: Root cause analysis, fix in v1.2.5

For details see: [link to incident report]
```

### Step 6: Prevent Future Failures

Analyze the incident and improve deployment practices.

**Post-Incident Review:**

1. **What went wrong?**
   - Code bug not caught in testing
   - Configuration incompatibility
   - Missing database index caused performance degradation
   - Infrastructure resource limits exceeded

2. **Why wasn't it caught earlier?**
   - Insufficient test coverage
   - Staging environment differs from production
   - Load testing not performed
   - Migration not tested with production data volume

3. **What can prevent this?**
   - Add integration test for failure scenario
   - Improve staging/production parity
   - Implement canary deployments
   - Add automated rollback triggers
   - Enhance monitoring and alerting

**Deployment Improvements:**

```yaml
# Implement health checks in docker-compose.yml
services:
  app:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

**Rollback Automation:**

```bash
# Create rollback script for quick recovery
#!/bin/bash
# rollback.sh - Quick rollback to previous version

PREVIOUS_VERSION=$1

if [ -z "$PREVIOUS_VERSION" ]; then
  echo "Usage: ./rollback.sh <version>"
  exit 1
fi

echo "Rolling back to $PREVIOUS_VERSION..."
docker-compose stop app
sed -i "s/myapp:.*$/myapp:$PREVIOUS_VERSION/g" docker-compose.yml
docker-compose up -d app
docker-compose ps
echo "Rollback complete. Check logs: docker logs app"
```

**Best Practices:**

1. **Maintain deployment history** - Keep previous images, configs, and compose files
2. **Test rollback procedures** - Practice rollbacks in staging regularly
3. **Automate health checks** - Use docker healthchecks and monitoring
4. **Version everything** - Tag images, version configs, track migrations
5. **Backup before risky changes** - Database backups before migrations
6. **Document dependencies** - Track what depends on what for coordinated rollbacks
7. **Gradual rollouts** - Use canary or blue-green deployments when possible
8. **Monitor post-deployment** - Watch metrics closely for 30+ minutes after deploy

## Quick Reference

### Rollback Decision Matrix

| Scenario | Strategy | Estimated Time |
|----------|----------|----------------|
| App code bug, no DB changes | Redeploy previous image | 1-2 minutes |
| Config error | Restore previous config | 1-2 minutes |
| Failed DB migration | Reverse migration + app rollback | 5-10 minutes |
| Infrastructure change | Revert compose file | 3-5 minutes |
| Multiple component failure | Sequential rollback (DB → App → Infra) | 10-15 minutes |

### Common Rollback Commands

```bash
# Quick app rollback
docker-compose stop <service>
sed -i 's/v1.2.4/v1.2.3/g' docker-compose.yml
docker-compose up -d <service>

# Config rollback
git checkout HEAD~1 -- config/
docker-compose restart <service>

# Database migration rollback
docker exec <db-container> alembic downgrade -1

# Full infrastructure rollback
git checkout HEAD~1 -- docker-compose.yml
docker-compose down && docker-compose up -d
```

## Resources

- **`references/database_rollback_patterns.md`** - Detailed database migration rollback strategies and data preservation techniques
- **`references/platform_guides.md`** - Docker and Docker Compose specific rollback procedures and best practices

## Best Practices

1. **Always backup before rollback** - Especially for database changes
2. **Test rollback in staging first** - If time permits
3. **Stop traffic during risky rollbacks** - Prevent inconsistent state
4. **Rollback in reverse order** - Undo changes in opposite sequence of deployment
5. **Validate each step** - Don't proceed if validation fails
6. **Document everything** - Create audit trail for compliance and learning
7. **Communicate clearly** - Keep stakeholders informed of status
8. **Practice rollbacks regularly** - Ensure procedures work when needed
9. **Automate common rollbacks** - Reduce human error and recovery time
10. **Learn from failures** - Use incidents to improve deployment process
