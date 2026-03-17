---
name: Confluence Documentation Patterns
description: This skill should be used when the user asks to "confluence page", "create documentation", "tech design", "write to confluence", "read from confluence", "link confluence", "create TDD", "write runbook", "meeting notes", "release notes", "architecture decision", or needs guidance on creating, managing, and organizing documentation in Confluence with integration to Jira workflows.
version: 1.0.0
categories:
  - confluence
  - documentation
  - atlassian
  - knowledge-base
  - technical-writing
trigger_phrases:
  - confluence page
  - create documentation
  - tech design
  - write to confluence
  - read from confluence
  - link confluence
  - create TDD
  - write runbook
  - meeting notes
  - release notes
  - architecture decision
  - ADR
  - API documentation
  - sprint retrospective
  - technical documentation
---

# Confluence Documentation Patterns

Comprehensive guide for creating, managing, and organizing technical documentation in Confluence with seamless Jira integration.

## When to Use This Skill

Activate this skill when:
- Creating technical design documents (TDD)
- Writing API documentation
- Documenting architecture decisions (ADR)
- Creating runbooks and playbooks
- Writing release notes
- Taking meeting notes
- Conducting sprint retrospectives
- Linking documentation to Jira issues
- Searching for existing documentation
- Organizing knowledge bases

## Documentation Patterns

### 1. Technical Design Document (TDD)

**Purpose:** Document design decisions, architecture, and implementation approach before coding.

**When to Create:**
- Starting a new feature (Story/Epic)
- Significant architectural change
- Complex technical implementation
- Cross-team dependencies

**Template:**

```markdown
# [Feature Name] - Technical Design Document

**Status:** Draft | In Review | Approved | Implemented
**Author:** [Name]
**Created:** [Date]
**Last Updated:** [Date]
**Jira Issue:** [PROJ-XXX](link)
**Reviewers:** @reviewer1, @reviewer2

---

## Executive Summary

Brief 2-3 sentence summary of what this design achieves.

## Problem Statement

### Current Situation
Describe the current state and why it's problematic.

### Goals
- Goal 1: Specific measurable goal
- Goal 2: Specific measurable goal
- Goal 3: Specific measurable goal

### Non-Goals
- What this design explicitly does NOT address
- Future considerations left for later

## Background and Context

### Business Context
Why this matters from a business perspective.

### Technical Context
Existing systems, constraints, and technical background.

### Related Work
- Links to related TDDs
- Reference documentation
- Similar implementations

## Proposed Solution

### High-Level Design

[Diagram or high-level architecture description]

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Client    │────▶│   API       │────▶│  Database   │
└─────────────┘     └─────────────┘     └─────────────┘
```

### Component Design

#### Component 1: [Name]
**Responsibility:** What this component does
**Dependencies:** What it depends on
**Interfaces:** APIs it exposes

```typescript
// Interface example
interface ComponentA {
  method1(param: Type): ReturnType;
  method2(param: Type): ReturnType;
}
```

#### Component 2: [Name]
**Responsibility:** What this component does
**Dependencies:** What it depends on
**Interfaces:** APIs it exposes

### Data Model

```sql
-- Database schema changes
CREATE TABLE example (
  id BIGINT PRIMARY KEY,
  field1 VARCHAR(255),
  field2 TIMESTAMP,
  CONSTRAINT fk_reference FOREIGN KEY (ref_id) REFERENCES other_table(id)
);
```

### API Design

#### Endpoint 1
```http
POST /api/v1/resource
Content-Type: application/json

{
  "field1": "value",
  "field2": 123
}

Response: 201 Created
{
  "id": "resource-id",
  "field1": "value",
  "field2": 123,
  "created_at": "2025-01-15T10:00:00Z"
}
```

#### Endpoint 2
```http
GET /api/v1/resource/{id}

Response: 200 OK
{
  "id": "resource-id",
  "field1": "value",
  "field2": 123,
  "created_at": "2025-01-15T10:00:00Z"
}
```

## Alternatives Considered

### Alternative 1: [Name]
**Description:** Brief description of this approach
**Pros:**
- Pro 1
- Pro 2

**Cons:**
- Con 1
- Con 2

**Reason Not Chosen:** Why we rejected this

### Alternative 2: [Name]
**Description:** Brief description of this approach
**Pros:**
- Pro 1
- Pro 2

**Cons:**
- Con 1
- Con 2

**Reason Not Chosen:** Why we rejected this

## Security Considerations

### Authentication & Authorization
- How users are authenticated
- Authorization rules and roles
- Token management

### Data Protection
- Sensitive data handling
- Encryption at rest and in transit
- Data retention policies

### Threat Model
| Threat | Mitigation |
|--------|------------|
| SQL Injection | Parameterized queries, ORM |
| XSS | Input sanitization, CSP |
| CSRF | CSRF tokens, SameSite cookies |

## Performance Considerations

### Expected Load
- Requests per second: XXX
- Peak load: XXX
- Concurrent users: XXX

### Performance Requirements
- Response time: < XXXms (p95)
- Throughput: XXX req/s
- Availability: 99.9%

### Optimization Strategies
- Caching strategy
- Database indexing
- Query optimization
- CDN usage

## Scalability

### Horizontal Scaling
How the system scales out with more instances.

### Vertical Scaling
Resource requirements for scaling up.

### Bottlenecks
Potential scalability bottlenecks and mitigation strategies.

## Testing Strategy

### Unit Tests
- Component coverage > 80%
- Mock external dependencies
- Test edge cases

### Integration Tests
- API contract tests
- Database integration
- Third-party service mocks

### E2E Tests
- Critical user flows
- Happy path scenarios
- Error scenarios

### Performance Tests
- Load testing approach
- Stress testing criteria
- Baseline metrics

## Deployment Strategy

### Rollout Plan
1. Deploy to dev environment
2. Run automated tests
3. Deploy to staging
4. Manual QA validation
5. Deploy to production (blue-green)
6. Monitor metrics for 24h

### Rollback Plan
- Rollback triggers
- Rollback procedure
- Data migration rollback (if applicable)

### Feature Flags
- Feature flag strategy
- Gradual rollout percentage
- Kill switch

## Monitoring and Observability

### Metrics to Track
- Request rate
- Error rate
- Response latency (p50, p95, p99)
- CPU/Memory usage

### Alerts
| Alert | Condition | Severity | Action |
|-------|-----------|----------|--------|
| High error rate | > 5% errors | Critical | Page on-call |
| Slow response | p95 > 500ms | Warning | Investigate |

### Dashboards
- Grafana dashboard link
- CloudWatch/DataDog dashboard

### Logging
- Log level strategy
- Structured logging format
- Log retention

## Dependencies

### Internal Dependencies
- Service A (API v2)
- Service B (gRPC)
- Shared library X v1.2.3

### External Dependencies
- Third-party API (SLA: 99.9%)
- Payment provider
- Analytics service

### Dependency Risks
| Dependency | Risk | Mitigation |
|------------|------|------------|
| Payment API | Downtime | Circuit breaker, retry logic |
| Auth service | Latency | Caching, fallback |

## Migration Plan

### Data Migration
- Migration script location
- Estimated duration: XXX hours
- Rollback procedure

### Code Migration
- Backward compatibility
- Deprecation timeline
- Migration guide for consumers

## Documentation

### User Documentation
- User guide location
- API documentation
- Integration examples

### Developer Documentation
- Setup guide
- Architecture diagrams
- Code walkthrough

## Timeline and Milestones

| Milestone | Date | Status |
|-----------|------|--------|
| TDD Approval | 2025-01-20 | In Progress |
| Implementation Start | 2025-01-22 | Not Started |
| Dev Complete | 2025-02-05 | Not Started |
| QA Complete | 2025-02-12 | Not Started |
| Production Deploy | 2025-02-15 | Not Started |

## Open Questions

1. **Question 1:** Description of open question
   - **Owner:** @person
   - **Due:** Date
   - **Status:** Open

2. **Question 2:** Description of open question
   - **Owner:** @person
   - **Due:** Date
   - **Status:** Resolved

## Risks and Mitigation

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Third-party API changes | High | Medium | Version pinning, contract tests |
| Database migration failure | Critical | Low | Thorough testing, rollback plan |
| Performance degradation | Medium | Medium | Load testing, monitoring |

## Sign-off

### Reviewers
- [ ] @architect - Architecture review
- [ ] @security - Security review
- [ ] @devops - Infrastructure review
- [ ] @qa-lead - Testing strategy review

### Approvers
- [ ] @tech-lead - Technical approval
- [ ] @product-manager - Product approval
- [ ] @engineering-manager - Resource approval

---

## Related Documentation
- [Architecture Decision Record](link)
- [API Documentation](link)
- [Deployment Runbook](link)

## Revision History
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-01-15 | @author | Initial draft |
| 1.1 | 2025-01-18 | @author | Added security section |
```

---

### 2. Architecture Decision Record (ADR)

**Purpose:** Document significant architectural decisions and their rationale.

**When to Create:**
- Choosing between architectural patterns
- Selecting technologies/frameworks
- Making design tradeoffs
- Establishing standards

**Template:**

```markdown
# ADR-[NUMBER]: [Short Title]

**Status:** Proposed | Accepted | Deprecated | Superseded
**Date:** [YYYY-MM-DD]
**Decision Makers:** @person1, @person2
**Related Jira:** [PROJ-XXX](link)
**Supersedes:** ADR-XXX (if applicable)

---

## Context

### Problem
Clear description of the problem or situation that requires a decision.

### Business Context
- Business driver or requirement
- Stakeholder needs
- Market conditions

### Technical Context
- Current architecture
- Existing constraints
- Technology landscape

### Constraints
- Time constraints
- Resource constraints
- Technical limitations
- Regulatory requirements

## Decision

We will [verb phrase describing the decision].

### Rationale
Detailed explanation of why this decision makes sense:

1. **Reason 1:** Explanation
2. **Reason 2:** Explanation
3. **Reason 3:** Explanation

## Options Considered

### Option 1: [Name]

**Description:** Detailed description of this option

**Pros:**
- ✅ Advantage 1
- ✅ Advantage 2
- ✅ Advantage 3

**Cons:**
- ❌ Disadvantage 1
- ❌ Disadvantage 2
- ❌ Disadvantage 3

**Cost:** [Time/Money/Effort estimation]

**Risk:** [Low/Medium/High]

### Option 2: [Name]

**Description:** Detailed description of this option

**Pros:**
- ✅ Advantage 1
- ✅ Advantage 2

**Cons:**
- ❌ Disadvantage 1
- ❌ Disadvantage 2

**Cost:** [Time/Money/Effort estimation]

**Risk:** [Low/Medium/High]

### Option 3: [Name]

**Description:** Detailed description of this option

**Pros:**
- ✅ Advantage 1
- ✅ Advantage 2

**Cons:**
- ❌ Disadvantage 1
- ❌ Disadvantage 2

**Cost:** [Time/Money/Effort estimation]

**Risk:** [Low/Medium/High]

## Comparison Matrix

| Criteria | Weight | Option 1 | Option 2 | Option 3 |
|----------|--------|----------|----------|----------|
| Performance | 5 | 4 | 3 | 5 |
| Maintainability | 4 | 5 | 3 | 4 |
| Cost | 3 | 3 | 5 | 2 |
| Developer Experience | 4 | 4 | 3 | 5 |
| **Total** | | **67** | **54** | **71** |

**Selected:** Option 3 (highest score)

## Consequences

### Positive Consequences
- ✅ Benefit 1: Description
- ✅ Benefit 2: Description
- ✅ Benefit 3: Description

### Negative Consequences
- ⚠️ Tradeoff 1: Description and mitigation
- ⚠️ Tradeoff 2: Description and mitigation

### Risks
- 🔴 Risk 1: High - Description and mitigation plan
- 🟡 Risk 2: Medium - Description and mitigation plan
- 🟢 Risk 3: Low - Description

## Implementation

### Immediate Actions
1. Action 1 - @owner - Due: [Date]
2. Action 2 - @owner - Due: [Date]
3. Action 3 - @owner - Due: [Date]

### Long-term Actions
- Action A - Q2 2025
- Action B - Q3 2025

### Migration Path
Steps to transition from current state to target state:

1. **Phase 1:** [Description] - [Timeline]
2. **Phase 2:** [Description] - [Timeline]
3. **Phase 3:** [Description] - [Timeline]

## Success Metrics

How we'll measure if this decision was successful:

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| Performance | < 200ms p95 | APM monitoring |
| Adoption | 100% teams | Survey |
| Cost savings | -30% | Cost analysis |

**Review Date:** [Date to review this decision]

## References

- [External article or documentation](link)
- [Internal wiki page](link)
- [Related ADR](link)
- [Research spike](link)

## Discussion

### Key Discussion Points
- Point 1 raised by @person
- Point 2 raised by @person
- Resolution: Description

### Dissenting Opinions
- @person: "Concern about Option 3's complexity"
  - Response: "Mitigated by providing training and documentation"

## Approval

- [x] @architect
- [x] @tech-lead
- [x] @engineering-manager
- [ ] @cto (if major decision)

---

**Related Documents:**
- [[TDD: Feature Name]]
- [[Runbook: Service Deployment]]
- [[ADR-XXX: Previous Related Decision]]
```

---

### 3. API Documentation

**Purpose:** Document REST/GraphQL APIs for internal and external consumers.

**Template:**

```markdown
# [Service Name] API Documentation

**Version:** v1.2.3
**Base URL:** `https://api.example.com/v1`
**Authentication:** Bearer Token
**Last Updated:** [Date]

---

## Overview

Brief description of what this API does and who should use it.

## Authentication

### Getting a Token

```bash
POST /auth/token
Content-Type: application/json

{
  "client_id": "your-client-id",
  "client_secret": "your-client-secret",
  "grant_type": "client_credentials"
}

Response: 200 OK
{
  "access_token": "eyJhbGci...",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

### Using the Token

```bash
curl -H "Authorization: Bearer eyJhbGci..." \
     https://api.example.com/v1/resource
```

## Rate Limits

| Tier | Requests per minute | Burst |
|------|---------------------|-------|
| Free | 60 | 10 |
| Pro | 600 | 100 |
| Enterprise | Unlimited | Unlimited |

**Headers:**
- `X-RateLimit-Limit`: Total requests allowed
- `X-RateLimit-Remaining`: Requests remaining
- `X-RateLimit-Reset`: Unix timestamp when limit resets

## Endpoints

### Resource Management

#### Create Resource

```http
POST /api/v1/resources
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "Resource Name",
  "type": "example",
  "attributes": {
    "key": "value"
  },
  "tags": ["tag1", "tag2"]
}
```

**Request Schema:**
```typescript
interface CreateResourceRequest {
  name: string;           // Required, 1-255 chars
  type: string;           // Required, enum: [example, test, production]
  attributes?: object;    // Optional, arbitrary JSON
  tags?: string[];        // Optional, array of strings
}
```

**Response: 201 Created**
```json
{
  "id": "res_1234567890",
  "name": "Resource Name",
  "type": "example",
  "attributes": {
    "key": "value"
  },
  "tags": ["tag1", "tag2"],
  "created_at": "2025-01-15T10:00:00Z",
  "updated_at": "2025-01-15T10:00:00Z"
}
```

**Errors:**
- `400 Bad Request`: Invalid input
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: Insufficient permissions
- `429 Too Many Requests`: Rate limit exceeded

#### Get Resource

```http
GET /api/v1/resources/{id}
Authorization: Bearer {token}
```

**Path Parameters:**
- `id` (string, required): Resource ID

**Response: 200 OK**
```json
{
  "id": "res_1234567890",
  "name": "Resource Name",
  "type": "example",
  "attributes": {
    "key": "value"
  },
  "tags": ["tag1", "tag2"],
  "created_at": "2025-01-15T10:00:00Z",
  "updated_at": "2025-01-15T10:00:00Z"
}
```

**Errors:**
- `404 Not Found`: Resource not found
- `401 Unauthorized`: Missing or invalid token

#### List Resources

```http
GET /api/v1/resources
Authorization: Bearer {token}
```

**Query Parameters:**
- `page` (integer, optional): Page number (default: 1)
- `per_page` (integer, optional): Items per page (default: 20, max: 100)
- `type` (string, optional): Filter by type
- `tags` (string, optional): Comma-separated tags (AND logic)
- `sort` (string, optional): Sort field (name, created_at, updated_at)
- `order` (string, optional): Sort order (asc, desc)

**Response: 200 OK**
```json
{
  "data": [
    {
      "id": "res_1234567890",
      "name": "Resource Name",
      "type": "example"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total_pages": 5,
    "total_count": 100
  }
}
```

#### Update Resource

```http
PATCH /api/v1/resources/{id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "Updated Name",
  "tags": ["new-tag"]
}
```

**Request Schema:** All fields optional, only provided fields are updated.

**Response: 200 OK** (same as Get Resource)

#### Delete Resource

```http
DELETE /api/v1/resources/{id}
Authorization: Bearer {token}
```

**Response: 204 No Content**

## Error Responses

Standard error format:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input provided",
    "details": [
      {
        "field": "name",
        "message": "Name is required"
      }
    ],
    "request_id": "req_abc123"
  }
}
```

**Error Codes:**
- `VALIDATION_ERROR`: Input validation failed
- `AUTHENTICATION_ERROR`: Authentication failed
- `AUTHORIZATION_ERROR`: Insufficient permissions
- `NOT_FOUND`: Resource not found
- `RATE_LIMIT_EXCEEDED`: Too many requests
- `INTERNAL_ERROR`: Server error

## Webhooks

Subscribe to events:

```http
POST /api/v1/webhooks
Authorization: Bearer {token}
Content-Type: application/json

{
  "url": "https://your-server.com/webhook",
  "events": ["resource.created", "resource.updated"],
  "secret": "your-webhook-secret"
}
```

**Event Format:**
```json
{
  "id": "evt_123456",
  "type": "resource.created",
  "created_at": "2025-01-15T10:00:00Z",
  "data": {
    "resource": { /* full resource object */ }
  }
}
```

**Signature Verification:**
```javascript
const crypto = require('crypto');

function verifySignature(payload, signature, secret) {
  const hmac = crypto.createHmac('sha256', secret);
  const computed = hmac.update(payload).digest('hex');
  return computed === signature;
}
```

## SDKs and Client Libraries

| Language | Library | Installation |
|----------|---------|--------------|
| JavaScript/TypeScript | `@company/api-client` | `npm install @company/api-client` |
| Python | `company-api` | `pip install company-api` |
| Go | `github.com/company/api-go` | `go get github.com/company/api-go` |
| Ruby | `company-api` | `gem install company-api` |

**Example Usage (JavaScript):**
```javascript
import { Client } from '@company/api-client';

const client = new Client({ apiKey: 'your-api-key' });

const resource = await client.resources.create({
  name: 'My Resource',
  type: 'example'
});
```

## Changelog

### v1.2.3 (2025-01-15)
- Added `tags` field to resources
- Fixed pagination bug in list endpoint

### v1.2.0 (2024-12-01)
- Added webhook support
- New `attributes` field for flexible metadata

### v1.1.0 (2024-10-15)
- Added filtering to list endpoint
- Improved error messages

---

**Support:**
- Email: api-support@company.com
- Slack: #api-support
- Status Page: https://status.company.com
```

---

### 4. Runbook / Playbook

**Purpose:** Document operational procedures for common tasks and incidents.

**Template:**

```markdown
# Runbook: [Service/Task Name]

**Service:** [Service Name]
**Team:** [Team Name]
**On-Call:** [PagerDuty/Slack Channel]
**Last Updated:** [Date]
**Jira Epic:** [PROJ-XXX](link)

---

## Overview

Brief description of what this service does and when to use this runbook.

## Quick Reference

| Item | Value |
|------|-------|
| Service URL | https://service.example.com |
| Health Check | https://service.example.com/health |
| Logs | https://logs.example.com/service |
| Metrics | https://metrics.example.com/dashboard |
| Repository | https://github.com/org/service |
| Deployment | Kubernetes namespace: `production` |

## Emergency Contacts

| Role | Name | Contact |
|------|------|---------|
| Primary On-Call | @person1 | +1-555-0001 |
| Secondary On-Call | @person2 | +1-555-0002 |
| Engineering Manager | @manager | +1-555-0003 |
| Product Owner | @po | +1-555-0004 |

**Escalation Path:**
1. Primary On-Call (respond within 15 min)
2. Secondary On-Call (if no response in 15 min)
3. Engineering Manager (if not resolved in 1 hour)
4. VP Engineering (if critical and not resolved in 2 hours)

## Common Procedures

### 1. Deploy New Version

**When:** Deploying a new release to production

**Prerequisites:**
- [ ] PR approved and merged
- [ ] CI/CD pipeline passed
- [ ] Staging testing complete
- [ ] Rollback plan ready

**Steps:**

```bash
# 1. Check current version
kubectl get deployment service -n production -o jsonpath='{.spec.template.spec.containers[0].image}'

# 2. Deploy new version
helm upgrade service ./charts/service \
  --namespace production \
  --set image.tag=v1.2.3 \
  --wait

# 3. Verify deployment
kubectl rollout status deployment/service -n production

# 4. Check pod health
kubectl get pods -n production -l app=service

# 5. Monitor logs
kubectl logs -n production -l app=service -f --tail=100

# 6. Verify metrics
# Open Grafana dashboard and check:
# - Error rate < 1%
# - Response time p95 < 500ms
# - CPU/Memory within normal range
```

**Rollback Procedure:**
```bash
# If deployment fails or causes issues:
helm rollback service -n production
kubectl rollout status deployment/service -n production
```

**Post-Deployment:**
- [ ] Monitor metrics for 1 hour
- [ ] Update Jira release
- [ ] Notify stakeholders in #releases channel

### 2. Scale Service

**When:** Handling increased load or reducing costs

**Scale Up:**
```bash
# Increase replicas
kubectl scale deployment service -n production --replicas=10

# Verify scaling
kubectl get deployment service -n production

# Monitor resource usage
kubectl top pods -n production -l app=service
```

**Scale Down:**
```bash
# Decrease replicas (during low traffic)
kubectl scale deployment service -n production --replicas=3

# Verify no errors after scale down
kubectl logs -n production -l app=service --tail=100
```

**Auto-Scaling:**
```bash
# Check HPA status
kubectl get hpa service -n production

# Adjust HPA if needed
kubectl autoscale deployment service \
  --cpu-percent=70 \
  --min=3 \
  --max=10 \
  -n production
```

### 3. Restart Service

**When:** Service is unresponsive or needs configuration reload

**Graceful Restart:**
```bash
# Rolling restart
kubectl rollout restart deployment/service -n production

# Watch restart progress
kubectl rollout status deployment/service -n production

# Verify all pods are healthy
kubectl get pods -n production -l app=service
```

**Force Restart (Emergency):**
```bash
# Delete pods (will be recreated)
kubectl delete pods -n production -l app=service

# Wait for new pods
kubectl wait --for=condition=ready pod -l app=service -n production
```

### 4. Check Service Health

**Quick Health Check:**
```bash
# HTTP health check
curl https://service.example.com/health

# Expected response:
# {"status": "healthy", "version": "1.2.3", "uptime": 3600}

# Kubernetes health check
kubectl get pods -n production -l app=service

# Check pod details
kubectl describe pod <pod-name> -n production
```

**Detailed Diagnostics:**
```bash
# Check recent logs
kubectl logs -n production -l app=service --tail=1000

# Check resource usage
kubectl top pods -n production -l app=service

# Check events
kubectl get events -n production --sort-by='.lastTimestamp' | grep service
```

## Incident Response

### High Error Rate Alert

**Alert Condition:** Error rate > 5% for 5 minutes

**Response Time:** 15 minutes

**Procedure:**

1. **Acknowledge Alert**
   ```bash
   # Respond in #incidents channel
   "Acknowledged error rate alert for service. Investigating."
   ```

2. **Check Dashboards**
   - Open Grafana dashboard
   - Identify error types
   - Check if errors are recent or ongoing

3. **Analyze Logs**
   ```bash
   # Filter error logs
   kubectl logs -n production -l app=service --tail=1000 | grep ERROR

   # Check specific error types
   kubectl logs -n production -l app=service | grep "Database connection"
   ```

4. **Identify Root Cause**
   - Database connectivity issue?
   - External API timeout?
   - Resource exhaustion?
   - Recent deployment?

5. **Mitigate**
   - **If recent deployment:** Rollback
   - **If database issue:** Check database health, scale connections
   - **If external API:** Enable circuit breaker, use fallback
   - **If resource issue:** Scale up service

6. **Resolve and Document**
   - Update #incidents channel with resolution
   - Create Jira incident ticket
   - Update this runbook if new scenario

### High Latency Alert

**Alert Condition:** p95 latency > 1000ms for 5 minutes

**Response Time:** 30 minutes

**Procedure:**

1. **Check Current Performance**
   ```bash
   # Check APM dashboard
   # Look for slow endpoints, database queries, external calls
   ```

2. **Identify Bottleneck**
   - Slow database queries?
   - External API calls timing out?
   - High CPU/Memory usage?
   - Network issues?

3. **Quick Fixes**
   ```bash
   # Scale up if resource constrained
   kubectl scale deployment service -n production --replicas=10

   # Restart if memory leak suspected
   kubectl rollout restart deployment/service -n production
   ```

4. **Long-term Fix**
   - Create Jira ticket for performance optimization
   - Add database indexes if slow queries
   - Implement caching
   - Optimize algorithms

### Service Down Alert

**Alert Condition:** No healthy pods or health check failing

**Response Time:** Immediate

**Procedure:**

1. **Assess Impact**
   ```bash
   kubectl get pods -n production -l app=service
   kubectl describe pods -n production -l app=service
   ```

2. **Check Dependencies**
   - Database accessible?
   - Required services up?
   - Network connectivity?

3. **Restart Service**
   ```bash
   kubectl rollout restart deployment/service -n production
   ```

4. **If Restart Fails**
   - Check recent deployments
   - Rollback if recent change
   - Check configuration changes
   - Verify secrets/config maps

5. **Escalate**
   - If not resolved in 30 minutes, escalate to engineering manager
   - Consider switching to backup/failover

## Maintenance Procedures

### Database Migration

**Prerequisites:**
- [ ] Backup database
- [ ] Test migration in staging
- [ ] Notify users of maintenance window
- [ ] Have rollback script ready

**Procedure:**
```bash
# 1. Create backup
kubectl exec -n production postgres-0 -- pg_dump -U postgres dbname > backup.sql

# 2. Put service in maintenance mode (optional)
kubectl scale deployment service -n production --replicas=0

# 3. Run migration
kubectl exec -n production service-pod -- npm run migrate:up

# 4. Verify migration
kubectl exec -n production postgres-0 -- psql -U postgres -d dbname -c "SELECT version FROM migrations;"

# 5. Restart service
kubectl scale deployment service -n production --replicas=3

# 6. Verify functionality
curl https://service.example.com/health
```

**Rollback:**
```bash
# Run down migration
kubectl exec -n production service-pod -- npm run migrate:down

# Restore from backup if needed
kubectl exec -n production postgres-0 -- psql -U postgres dbname < backup.sql
```

### Certificate Renewal

**When:** TLS certificates expiring

```bash
# Check certificate expiry
kubectl get certificate -n production

# Renew certificate (cert-manager handles automatically)
# Manual renewal if needed:
kubectl delete secret tls-secret -n production
# cert-manager will recreate automatically

# Verify new certificate
kubectl get certificate -n production
```

## Monitoring and Alerts

### Key Metrics

| Metric | Warning | Critical | Dashboard |
|--------|---------|----------|-----------|
| Error Rate | > 2% | > 5% | [Link](https://grafana.example.com/d/errors) |
| Latency (p95) | > 500ms | > 1000ms | [Link](https://grafana.example.com/d/latency) |
| CPU Usage | > 70% | > 90% | [Link](https://grafana.example.com/d/resources) |
| Memory Usage | > 80% | > 95% | [Link](https://grafana.example.com/d/resources) |
| Disk Usage | > 80% | > 90% | [Link](https://grafana.example.com/d/disk) |

### Alert Channels

- **PagerDuty:** Critical incidents
- **Slack #alerts:** Warnings and info
- **Email:** Daily digest

## Troubleshooting

### Common Issues

#### Issue: Pods Crash Looping

**Symptoms:**
```bash
kubectl get pods -n production -l app=service
# Shows CrashLoopBackOff status
```

**Diagnosis:**
```bash
kubectl logs -n production <pod-name> --previous
kubectl describe pod -n production <pod-name>
```

**Common Causes:**
- Configuration error
- Missing environment variable
- Database connection failure
- Out of memory

**Resolution:**
Check logs, fix configuration, scale resources, or rollback deployment.

#### Issue: High Memory Usage

**Symptoms:** Memory usage > 90%, potential OOM kills

**Diagnosis:**
```bash
kubectl top pods -n production -l app=service
kubectl describe pod -n production <pod-name> | grep -A 5 Resources
```

**Resolution:**
```bash
# Increase memory limit
kubectl set resources deployment service -n production \
  --limits=memory=2Gi \
  --requests=memory=1Gi

# Or restart to clear memory leak
kubectl rollout restart deployment/service -n production
```

## Knowledge Base Links

- [[TDD: Service Architecture]]
- [[ADR: Technology Choices]]
- [[API Documentation]]
- [[Service Diagram]]

## Revision History

| Date | Author | Changes |
|------|--------|---------|
| 2025-01-15 | @author | Initial creation |
| 2025-01-20 | @author | Added certificate renewal procedure |
```

---

### 5. Release Notes

**Purpose:** Communicate changes, new features, and fixes to stakeholders.

**Template:**

```markdown
# Release Notes - v[X.Y.Z]

**Release Date:** [YYYY-MM-DD]
**Release Manager:** @person
**Jira Release:** [PROJ vX.Y.Z](link)

---

## Summary

Brief 2-3 sentence summary of this release.

## Highlights

🎉 **Top Features:**
- **Feature 1:** Brief description - [PROJ-123](link)
- **Feature 2:** Brief description - [PROJ-456](link)
- **Feature 3:** Brief description - [PROJ-789](link)

## New Features

### [Feature Name] ([PROJ-XXX](link))

**Description:** Detailed description of new feature

**Benefits:**
- Benefit 1
- Benefit 2

**Usage:**
```javascript
// Example code showing how to use new feature
const result = api.newFeature({ option: 'value' });
```

**Screenshots:**
![Feature Screenshot](link)

**Documentation:** [User Guide](link)

### [Another Feature] ([PROJ-YYY](link))

Similar format...

## Improvements

- **Performance:** Reduced API response time by 30% - [PROJ-111](link)
- **UX:** Improved loading states for better user feedback - [PROJ-222](link)
- **DevEx:** Added TypeScript types to SDK - [PROJ-333](link)

## Bug Fixes

- Fixed authentication timeout issue - [PROJ-444](link)
- Resolved data race condition in cache layer - [PROJ-555](link)
- Corrected pagination bug in list endpoints - [PROJ-666](link)

## Breaking Changes

⚠️ **IMPORTANT:** This release contains breaking changes

### Change 1: [Description]

**Impact:** Who/what is affected

**Migration Guide:**
```javascript
// Before
oldApi.method();

// After
newApi.method({ newParam: 'required' });
```

**Timeline:** Deprecated: vX.Y.Z, Removed: vX+1.0.0

## Deprecations

| Item | Deprecated | Removed | Alternative |
|------|------------|---------|-------------|
| `oldMethod()` | v1.5.0 | v2.0.0 | Use `newMethod()` |
| `/api/v1/old` | v1.5.0 | v2.0.0 | Use `/api/v2/new` |

## Security Updates

🔒 Updated dependencies with security vulnerabilities:
- package-a: v1.0.0 → v1.1.0 (CVE-2024-12345)
- package-b: v2.0.0 → v2.1.0 (CVE-2024-67890)

## Known Issues

- Issue 1: Description - Workaround: Do X - [PROJ-777](link)
- Issue 2: Description - Fix planned for next release - [PROJ-888](link)

## Upgrade Instructions

### Prerequisites
- Backup your data
- Check compatibility with your environment
- Review breaking changes section

### Steps

1. **Backup:**
   ```bash
   ./scripts/backup.sh
   ```

2. **Update Dependencies:**
   ```bash
   npm install @company/api@1.5.0
   ```

3. **Run Migrations:**
   ```bash
   npm run migrate
   ```

4. **Verify:**
   ```bash
   npm test
   ```

### Rollback

If issues occur:
```bash
./scripts/rollback.sh v1.4.0
```

## Performance Metrics

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| API Response Time (p95) | 800ms | 560ms | 30% faster |
| Database Queries | 10/req | 3/req | 70% reduction |
| Bundle Size | 500KB | 350KB | 30% smaller |

## Contributors

Special thanks to:
- @contributor1 - Feature development
- @contributor2 - Bug fixes
- @contributor3 - Documentation
- @contributor4 - Testing

## Next Release

**Planned for:** v1.6.0 - [Date]

**Focus Areas:**
- Mobile app support
- Real-time notifications
- Advanced analytics

**Track Progress:** [v1.6.0 Roadmap](link)

## Feedback

Questions or issues? Contact us:
- Slack: #product-feedback
- Email: product@company.com
- Support: https://support.company.com

---

**Full Changelog:** [GitHub Releases](link)
```

---

### 6. Meeting Notes

**Purpose:** Document meetings, decisions, and action items.

**Template:**

```markdown
# [Meeting Name] - [Date]

**Date:** [YYYY-MM-DD]
**Time:** [HH:MM - HH:MM]
**Location:** Zoom / Conference Room
**Facilitator:** @person
**Note Taker:** @person

---

## Attendees

**Present:**
- @person1 (Role)
- @person2 (Role)
- @person3 (Role)

**Absent:**
- @person4 (Role) - Reason

## Agenda

1. Topic 1 (10 min)
2. Topic 2 (15 min)
3. Topic 3 (20 min)
4. AOB (5 min)

## Discussion

### 1. Topic 1: [Name]

**Context:** Brief context

**Discussion Points:**
- Point 1 raised by @person
- Point 2 raised by @person
- Consensus reached on approach

**Decision:** We will proceed with Option B

**Action Items:**
- [ ] @person1: Implement solution - Due: 2025-01-20 - [PROJ-123](link)
- [ ] @person2: Update documentation - Due: 2025-01-22

### 2. Topic 2: [Name]

Similar format...

## Decisions Made

| Decision | Owner | Impact |
|----------|-------|--------|
| Use PostgreSQL for new service | @tech-lead | High |
| Postpone mobile app to Q2 | @product | Medium |

## Action Items

All action items consolidated:

| Action | Owner | Due Date | Jira | Status |
|--------|-------|----------|------|--------|
| Implement auth flow | @dev1 | 2025-01-20 | [PROJ-123](link) | 🔄 In Progress |
| Write TDD | @arch | 2025-01-18 | [PROJ-124](link) | ✅ Done |
| Review PR | @dev2 | 2025-01-17 | [PROJ-125](link) | ⏱️ Pending |

## Parking Lot

Items tabled for future discussion:
- Topic A - Revisit in next sprint planning
- Topic B - Needs more research

## Next Meeting

**Date:** [Next Date]
**Agenda Items:**
- Follow-up on decisions from this meeting
- New topic 1
- New topic 2

---

**Related:** [[Sprint Planning]], [[Retrospective]]
```

---

### 7. Sprint Retrospective

**Purpose:** Reflect on sprint, identify improvements.

**Template:**

```markdown
# Sprint [Number] Retrospective

**Sprint:** Sprint [N]
**Date:** [YYYY-MM-DD]
**Team:** [Team Name]
**Facilitator:** @person
**Participants:** @person1, @person2, @person3

---

## Sprint Summary

**Duration:** [Start Date] - [End Date]
**Sprint Goal:** [Goal]
**Outcome:** ✅ Met / ⚠️ Partially Met / ❌ Not Met

### Metrics

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Story Points Committed | 40 | 40 | ✅ |
| Story Points Completed | 40 | 35 | ⚠️ |
| Bugs Created | < 5 | 3 | ✅ |
| Bugs Fixed | All | 6/8 | ⚠️ |
| Velocity | 35-45 | 35 | ✅ |

## What Went Well 🎉

1. **Excellent Collaboration**
   - Pairing sessions helped knowledge transfer
   - Quick responses on Slack reduced blockers
   - *Action:* Continue pairing on complex tickets

2. **Improved Testing**
   - Reached 85% code coverage (target was 80%)
   - Caught 2 critical bugs before production
   - *Action:* Maintain testing discipline

3. **On-Time Delivery**
   - Key feature shipped on schedule
   - Stakeholders very happy with demo
   - *Action:* Keep realistic estimations

## What Needs Improvement 🔧

1. **Unclear Requirements**
   - Lost 10 story points to rework due to unclear acceptance criteria
   - Multiple back-and-forth with product
   - **Action Items:**
     - [ ] @product: Attend refinement sessions - Owner: @product
     - [ ] @team: Ask clarifying questions in refinement - All
     - [ ] Create requirements checklist - Owner: @scrummaster

2. **Technical Debt**
   - Accumulated tech debt in authentication module
   - Slowing down feature development
   - **Action Items:**
     - [ ] Allocate 20% of next sprint to tech debt - Owner: @tech-lead - [PROJ-200](link)
     - [ ] Create tech debt backlog - Owner: @dev1 - [PROJ-201](link)

3. **Testing Environment Issues**
   - Staging env down 2 times during sprint
   - Blocked testing for 8 hours total
   - **Action Items:**
     - [ ] Improve staging stability - Owner: @devops - [PROJ-202](link)
     - [ ] Add monitoring for staging - Owner: @devops - [PROJ-203](link)

## Action Items

| Action | Owner | Due | Jira | Priority |
|--------|-------|-----|------|----------|
| Attend refinement sessions | @product | Next Sprint | - | High |
| Create requirements checklist | @scrummaster | 2025-01-20 | [PROJ-199](link) | High |
| Allocate 20% sprint to tech debt | @tech-lead | Next Sprint | [PROJ-200](link) | High |
| Create tech debt backlog | @dev1 | 2025-01-18 | [PROJ-201](link) | Medium |
| Improve staging stability | @devops | 2025-01-25 | [PROJ-202](link) | High |
| Add monitoring for staging | @devops | 2025-01-25 | [PROJ-203](link) | Medium |

## Team Health Check

| Aspect | Score (1-5) | Notes |
|--------|-------------|-------|
| Team Morale | 4 | Good energy, positive interactions |
| Work-Life Balance | 3 | Some late nights due to staging issues |
| Clarity of Goals | 4 | Sprint goal was clear |
| Process Adherence | 4 | Following Scrum practices |
| Technical Excellence | 3 | Need to address tech debt |

**Overall Health:** 🟢 Good (18/25)

## Shout-Outs ⭐

- **@dev1:** Excellent debugging on the production issue!
- **@dev2:** Great mentorship with new team member
- **@devops:** Quick turnaround on infra requests

## Experiments

### Previous Experiments

| Experiment | Outcome | Continue? |
|------------|---------|-----------|
| Pair programming on complex tickets | ✅ Positive | Yes |
| No-meeting Wednesdays | ✅ Helped focus | Yes |
| Daily standup at 9 AM | ⚠️ Mixed feedback | Adjust to 9:30 AM |

### New Experiments

1. **Experiment:** Move standup to 9:30 AM
   - **Hypothesis:** Better attendance and focus
   - **Measure:** Attendance rate and feedback
   - **Duration:** 2 sprints

2. **Experiment:** Tech debt Fridays (last Friday of sprint)
   - **Hypothesis:** Regular tech debt work improves velocity
   - **Measure:** Tech debt tickets completed, velocity trend
   - **Duration:** 3 sprints

## Next Sprint Focus

🎯 **Top 3 Priorities:**
1. Implement action items from retro
2. Maintain code quality and testing standards
3. Reduce technical debt by 20%

---

**Next Retrospective:** [Date]
**Follow-up:** Review action items in mid-sprint check-in
```

---

## Confluence Best Practices

### Page Naming Conventions

**Format:** `[Category] - [Name]`

**Examples:**
- `TDD - User Authentication System`
- `ADR - 001 - Database Selection`
- `Runbook - Service Deployment`
- `API - Payment Service v2`
- `Release - v1.5.0 - Q1 2025`

**Rules:**
- Use descriptive, searchable names
- Include version numbers for versioned docs
- Avoid special characters
- Keep under 100 characters
- Use consistent prefixes per doc type

### Space Organization

```
Company Wiki (Root)
├── Engineering/
│   ├── Architecture/
│   │   ├── ADRs/
│   │   ├── System Diagrams/
│   │   └── Tech Stacks/
│   ├── Technical Designs/
│   │   ├── Feature TDDs/
│   │   └── Infrastructure TDDs/
│   ├── API Documentation/
│   ├── Runbooks/
│   └── Release Notes/
├── Product/
│   ├── Product Requirements/
│   ├── User Research/
│   └── Roadmaps/
├── Team/
│   ├── Meeting Notes/
│   ├── Retrospectives/
│   └── Team Playbooks/
└── General/
    ├── Onboarding/
    ├── Company Policies/
    └── FAQs/
```

### Labels and Categorization

**Standard Labels:**
- **Status:** `draft`, `in-review`, `approved`, `implemented`, `deprecated`
- **Type:** `tdd`, `adr`, `api-doc`, `runbook`, `release-notes`, `meeting-notes`
- **Team:** `backend`, `frontend`, `devops`, `mobile`, `data`
- **Technology:** `react`, `nodejs`, `kubernetes`, `postgres`, `aws`
- **Priority:** `p0-critical`, `p1-high`, `p2-medium`, `p3-low`
- **Project:** `project-alpha`, `project-beta`

**Applying Labels:**
```
When creating/editing a page, add labels in the page properties:
- At bottom of editor, click "Add labels"
- Type label name (auto-suggests existing)
- Press Enter to add
- Add multiple labels for better discoverability
```

### Cross-Linking Strategies

**Link Types:**

1. **Inline Links:**
   ```markdown
   As described in [TDD - Authentication](link), we will use JWT tokens.
   ```

2. **Related Pages Section:**
   ```markdown
   ## Related Documentation
   - [ADR - JWT Token Strategy](link)
   - [API - Authentication Endpoints](link)
   - [Runbook - Auth Service Deployment](link)
   ```

3. **Jira Integration:**
   ```markdown
   This feature is tracked in [PROJ-123](jira-link).

   Or use Jira macro:
   {jira:PROJ-123}
   ```

4. **Bi-directional Links:**
   - Always link back to parent/related docs
   - Use "Child Pages" macro for hierarchical links
   - Use "Excerpt Include" macro to embed content

### Template Usage

**Creating Templates:**

1. Go to Space Settings → Templates
2. Click "Create new template"
3. Add template content with placeholders:
   ```
   # [PLACEHOLDER: Document Title]

   **Author:** $currentUser
   **Date:** $date

   ## Overview
   [PLACEHOLDER: Brief description]
   ```

4. Save and make available to space

**Using Templates:**
- Create page → Select template
- Fill in placeholders
- Remove placeholder brackets

### Permissions Management

**Space Permissions:**
- **View:** All employees
- **Add/Edit:** Team members
- **Delete:** Team leads only
- **Administer:** Space admins

**Page Restrictions:**
- Use page restrictions for sensitive docs (security, financial)
- Clearly mark restricted pages with banner macro
- Review permissions quarterly

**Best Practices:**
- Default to open (within company)
- Restrict only when necessary
- Use groups instead of individual permissions
- Document why restrictions exist

## Jira-Confluence Integration

### Linking Issues to Pages

**Method 1: Smart Links**

In Jira issue description:
```markdown
Design Document: [TDD - New Feature](confluence-url)
```

In Confluence page:
```markdown
Related Jira Issue: [PROJ-123](jira-url)
```

**Method 2: Jira Macro**

In Confluence, use `/jira` command:
```
{jira:PROJ-123}
```

Shows issue card with status, assignee, and summary.

**Method 3: Jira Issues Macro**

Display multiple issues:
```
{jira:project=PROJ AND status="In Progress"}
```

### Embedding Jira Macros

**Single Issue:**
```
{jira:PROJ-123|columns=key,summary,status,assignee}
```

**JQL Query:**
```
{jira:jql=project=PROJ AND labels=feature-x|columns=key,summary,status}
```

**Issue Count:**
```
Total bugs: {jiraissues:project=PROJ AND type=Bug|count}
```

**Roadmap:**
```
{jira-chart:type=timeline|project=PROJ}
```

### Status Synchronization

**Workflow Integration:**

1. **Link Documentation to Workflow:**
   - In Jira workflow, add post-function
   - "Create Confluence page from template" (requires plugin)
   - Automatically creates TDD when story moves to "In Progress"

2. **Status Badges:**
   - Use Confluence status macros that mirror Jira:
   ```
   {status:color=Green|title=Implemented}
   {status:color=Yellow|title=In Progress}
   {status:color=Grey|title=Draft}
   ```

3. **Sync Strategy:**
   - Update Confluence page status when Jira issue status changes
   - Add comment to Jira when documentation is completed
   - Use automation rules in Jira to notify of doc updates

### Automated Page Creation

**Jira Automation Rule:**

```yaml
Trigger: Issue transitioned to "In Progress"
Condition: Issue type = Story
Action:
  - Create Confluence page from template "TDD Template"
  - Title: "TDD - {{issue.key}} - {{issue.summary}}"
  - Labels: tdd, {{issue.project}}, {{issue.labels}}
  - Link page to issue
  - Add comment to issue with page link
```

**Example Automation:**

```javascript
// When issue is created, create matching Confluence page
{
  "trigger": "Issue Created",
  "condition": "Issue Type = Epic",
  "actions": [
    {
      "type": "CreateConfluencePage",
      "template": "Epic Overview Template",
      "space": "ENG",
      "title": "Epic - {{issue.key}} - {{issue.summary}}",
      "labels": ["epic", "{{issue.project}}"],
      "parent": "Epic Overview Index"
    },
    {
      "type": "AddComment",
      "comment": "Epic documentation created: {{confluence.page.url}}"
    }
  ]
}
```

## Search Patterns

### Confluence Query Language (CQL)

**Basic Syntax:**
```
field operator value
```

**Common Fields:**
- `title`: Page title
- `text`: Page content
- `label`: Page labels
- `space`: Space key
- `type`: page, blogpost, comment
- `creator`: User who created
- `lastModified`: Date last modified
- `ancestor`: Parent page ID

**Operators:**
- `=`: Equals
- `!=`: Not equals
- `~`: Contains
- `>`, `<`, `>=`, `<=`: Comparison
- `IN`: In list
- `AND`, `OR`, `NOT`: Boolean logic

### CQL Examples

**1. Find All TDDs:**
```cql
label = "tdd" AND space = "ENG" ORDER BY lastModified DESC
```

**2. Find Pages Modified This Week:**
```cql
lastModified >= now("-1w") AND space = "ENG"
```

**3. Find API Docs for Specific Service:**
```cql
title ~ "API" AND label = "authentication" AND space = "ENG"
```

**4. Find Approved Architecture Decisions:**
```cql
label = "adr" AND text ~ "Status: Approved" ORDER BY created DESC
```

**5. Find Runbooks for Production:**
```cql
label = "runbook" AND label = "production" AND space = "OPS"
```

**6. Find Draft Documents:**
```cql
label = "draft" AND creator = currentUser() ORDER BY lastModified DESC
```

**7. Find Related Documentation:**
```cql
(text ~ "PROJ-123" OR title ~ "PROJ-123") AND space = "ENG"
```

**8. Find Stale Documentation:**
```cql
space = "ENG" AND lastModified < now("-6M") AND label != "deprecated"
```

**9. Find Pages by Team:**
```cql
label = "backend-team" AND type = page ORDER BY title
```

**10. Complex Query:**
```cql
(label = "tdd" OR label = "adr") AND
space = "ENG" AND
lastModified >= now("-3M") AND
(text ~ "kubernetes" OR text ~ "docker")
ORDER BY lastModified DESC
```

### Full-Text Search Strategies

**Search Tips:**

1. **Use Quotes for Exact Phrases:**
   ```
   "user authentication flow"
   ```

2. **Use Wildcards:**
   ```
   auth*  (matches auth, authentication, authorization)
   ```

3. **Exclude Terms:**
   ```
   kubernetes -minikube
   ```

4. **Search Specific Spaces:**
   ```
   In: Engineering AND postgresql
   ```

5. **Search by Label:**
   ```
   label:tdd label:high-priority
   ```

6. **Search by Date:**
   ```
   Updated: This Week AND label:api-doc
   ```

7. **Search Attachments:**
   ```
   filename:diagram.png
   ```

### Finding Related Documentation

**Strategy 1: Label-Based Search**
```cql
label IN ("project-alpha", "authentication") AND space = "ENG"
```

**Strategy 2: Text-Based Search**
```cql
text ~ "JWT token" AND (label = "tdd" OR label = "api-doc")
```

**Strategy 3: Link Graph**
- Use "Linked Pages" macro
- Use "Incoming Links" to see what references your page

**Strategy 4: Excerpt Search**
```cql
excerpt ~ "Redis cache" AND space = "ENG"
```

## Macros and Formatting

### Useful Macros

**1. Status Macro:**
```
{status:color=Blue|title=In Progress}
{status:color=Green|title=Completed}
{status:color=Red|title=Blocked}
{status:color=Yellow|title=Under Review}
{status:color=Grey|title=Draft}
```

**2. Panel Macro:**
```
{panel:title=Important Note|borderStyle=solid|borderColor=#red}
This is a critical security consideration.
{panel}
```

**3. Expand Macro:**
```
{expand:title=Click to see detailed explanation}
Detailed content here...
{expand}
```

**4. Code Block:**
```
{code:language=javascript|title=Example.js|linenumbers=true}
function example() {
  return "Hello World";
}
{code}
```

**5. Info/Warning/Note Macros:**
```
{info}This is informational{info}
{warning}This is a warning{warning}
{note}This is a note{note}
{tip}This is a tip{tip}
```

**6. Table of Contents:**
```
{toc:maxLevel=3}
```

**7. Children Display:**
```
{children:all=true|sort=title}
```

**8. Excerpt:**
```
{excerpt:hidden=true}
This content can be included in other pages.
{excerpt}
```

**9. Jira Filter Results:**
```
{jiraissues:jql=project=PROJ AND sprint in openSprints()|columns=key,summary,status,assignee}
```

**10. Task List:**
```
{task-list:status=complete,incomplete}
```

### Formatting Best Practices

1. **Use Headings Hierarchically:** H1 → H2 → H3
2. **Use Tables for Structured Data**
3. **Use Panels for Callouts**
4. **Use Code Blocks for Code/Config**
5. **Use Status Macros for Visual States**
6. **Use TOC for Long Documents**
7. **Use Expand for Optional Details**

## Version Control for Confluence

### Page Versioning

- Confluence auto-saves versions on each edit
- View version history: Page menu → View History
- Compare versions: Select two versions → Compare
- Restore version: Select version → Restore

### Change Notifications

**Watch Pages:**
- Star important pages
- Receive notifications on updates
- Configure notification frequency in settings

**Page Notifications:**
```
Space Settings → Notifications → Configure
- Immediate email
- Daily digest
- Weekly digest
```

### Review Workflows

**Manual Review:**
1. Creator adds `draft` label
2. Creator @mentions reviewers
3. Reviewers add inline comments
4. Creator addresses feedback
5. Reviewers approve (via comment)
6. Creator removes `draft`, adds `approved`

**Automated Review:**
- Use "Content Reviews" feature
- Set review dates
- Assign reviewers
- Track review completion

## Conclusion

This skill provides comprehensive patterns for creating and managing documentation in Confluence with seamless Jira integration. Use the templates, CQL queries, and best practices to maintain high-quality, discoverable documentation that supports your development workflows.

## Related Skills

- **jira-orchestration** - For linking docs to development workflows
- **technical-writing** - For general writing best practices
- **api-documentation** - For API-specific documentation patterns
- **knowledge-management** - For organizing and maintaining knowledge bases
