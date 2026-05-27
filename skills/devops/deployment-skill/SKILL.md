---
document_name: "deployment.skill.md"
location: ".claude/skills/deployment.skill.md"
codebook_id: "CB-SKILL-DEPLOY-001"
version: "1.0.0"
date_created: "2026-01-04"
date_last_edited: "2026-01-04"
document_type: "skill"
purpose: "Procedures for deployment automation and execution"
skill_metadata:
  category: "devops"
  complexity: "intermediate"
  estimated_time: "varies"
  prerequisites:
    - "Infrastructure ready"
    - "CI/CD configured"
category: "skills"
status: "active"
tags:
  - "skill"
  - "deployment"
  - "devops"
ai_parser_instructions: |
  This skill defines procedures for deployment.
  Section markers: === SECTION ===
  Procedure markers: === PROCEDURE: NAME ===
---

# Deployment Skill

=== PURPOSE ===

This skill provides procedures for deployment automation and execution. Used by the DevOps Engineer in coordination with Delivery Lead.

---

=== USED BY ===

| Agent | Purpose |
|-------|---------|
| @agent(devops-engineer) @ref(CB-AGENT-DEVOPS-001) | Primary skill for deployment |

---

=== PREREQUISITES ===

Before using this skill:
- [ ] Infrastructure provisioned
- [ ] CI/CD pipeline ready
- [ ] Release approved by Delivery Lead

---

=== PROCEDURE: Deployment Checklist ===

**Pre-Deployment:**
- [ ] All tests passing
- [ ] Build artifacts ready
- [ ] Database migrations prepared
- [ ] Environment variables configured
- [ ] Rollback plan documented
- [ ] Team notified

**Deployment:**
- [ ] Take backup (if applicable)
- [ ] Run database migrations
- [ ] Deploy application
- [ ] Run health checks
- [ ] Verify functionality

**Post-Deployment:**
- [ ] Monitor logs
- [ ] Check error rates
- [ ] Verify key flows
- [ ] Update status
- [ ] Log in buildlog

---

=== PROCEDURE: Zero-Downtime Deployment ===

**Strategies:**

**Blue-Green:**
1. Deploy to inactive environment (green)
2. Run tests on green
3. Switch traffic to green
4. Keep blue for rollback

**Rolling:**
1. Deploy to subset of servers
2. Verify health
3. Continue to next subset
4. Complete when all updated

**Canary:**
1. Deploy to small percentage
2. Monitor metrics
3. Gradually increase percentage
4. Full rollout when confident

---

=== PROCEDURE: Database Migration ===

**Steps:**
1. Backup database
2. Run migrations in staging first
3. Apply to production during low-traffic
4. Verify data integrity
5. Keep rollback scripts ready

**Rules:**
- Migrations must be backwards compatible
- Test rollback scripts
- Never drop columns immediately

---

=== PROCEDURE: Rollback ===

**When to Rollback:**
- Critical errors in production
- Performance degradation
- Data integrity issues
- Security vulnerabilities

**Steps:**
1. Notify team immediately
2. Switch to previous version/environment
3. Rollback database if needed
4. Verify functionality
5. Document incident
6. Log with `#issue-encountered`

---

=== PROCEDURE: Health Checks ===

**Endpoint:** `/health` or `/healthz`

**Response:**
```json
{
  "status": "healthy",
  "version": "1.2.3",
  "timestamp": "2026-01-04T12:00:00Z",
  "checks": {
    "database": "healthy",
    "cache": "healthy",
    "external_api": "healthy"
  }
}
```

**Use Cases:**
- Load balancer health checks
- Kubernetes liveness/readiness probes
- Monitoring systems

---

=== PROCEDURE: Deployment Documentation ===

**Runbook Contents:**
- Step-by-step deployment process
- Environment-specific configurations
- Rollback procedures
- Contact information
- Common issues and solutions

**Location:** `docs/deployment-runbook.md`

---

=== ANTI-PATTERNS ===

### No Rollback Plan
**Problem:** Can't recover from bad deployment
**Solution:** Always have rollback ready

### Manual Deployments
**Problem:** Error-prone, inconsistent
**Solution:** Automate everything

### No Health Checks
**Problem:** Can't verify deployment success
**Solution:** Implement health endpoints

### Big Bang Deployments
**Problem:** High risk, hard to debug
**Solution:** Use incremental strategies

---

=== RELATED SKILLS ===

| Skill | Relationship |
|-------|--------------|
| @skill(cicd-pipeline) | CI/CD triggers deployment |
| @skill(infrastructure) | Infrastructure hosts deployment |
| @skill(release-management) | Releases coordinate deployment |
