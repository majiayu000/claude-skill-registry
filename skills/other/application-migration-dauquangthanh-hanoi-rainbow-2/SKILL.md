---
name: application-migration
description: Guides comprehensive application migration projects including legacy system modernization, cloud migration, technology stack upgrades, database migration, and architecture transformation. Covers assessment, planning, migration strategies (strangler fig, big bang, phased), risk management, data migration, testing, and cutover. Use when migrating applications, modernizing legacy systems, moving to cloud, changing technology stacks, or when users mention "migration", "modernization", "replatform", "lift and shift", "refactor", "strangler pattern", or "legacy transformation".
---

# Application Migration

Plan and execute application migration projects—from legacy system modernization to cloud migration and technology stack transformation.

## Migration Workflow

Follow this systematic approach for successful migrations:

## 1. Assess Current State

Analyze the application portfolio and environment:

```
Actions:
- Create application inventory (name, tech stack, dependencies)
- Map data flows and integration points
- Identify business criticality (critical/important/low)
- Document compliance requirements (PCI-DSS, HIPAA, GDPR, etc.)
- Measure current performance metrics (response time, throughput, uptime)
```

**Output:** Application assessment report with complexity scores (low/medium/high)

**Example Assessment:**

```
Application: Customer Portal
Tech Stack: Java 8, Oracle 11g, Apache Tomcat 7
Dependencies: Payment Gateway API, CRM System, Email Service
Business Criticality: Critical (revenue-generating)
Complexity: High (20+ integrations, legacy code)
→ Recommendation: Strangler fig pattern with 12-month timeline
```

### 2. Select Migration Strategy

Choose the approach based on complexity and business constraints:

**Strangler Fig Pattern** (recommended for complex applications):

- Build new functionality alongside old system
- Incrementally redirect traffic to new components
- Retire old components gradually
- Timeline: 6-18 months
- Risk: Low (gradual transition with rollback capability)

**Big Bang Migration** (for simple applications):

- Complete migration in single cutover event
- All users switch simultaneously
- Timeline: 1-3 months
- Risk: High (no gradual rollback option)

**Phased Migration** (for multi-tenant or regional deployments):

- Migrate one tenant/region at a time
- Validate each phase before proceeding
- Timeline: 3-12 months
- Risk: Medium (parallel operations required)

### 3. Plan Migration

Create detailed execution roadmap with these components:

**Timeline:** Define phases with 2-week sprint cycles
**Resources:** Allocate developers (3-10), QA (2-4), DevOps (1-2), architects (1)
**Budget:** Estimate 1.5-2x initial projection (migrations typically exceed estimates)
**Risk Mitigation:** Document top 5 risks with contingency plans
**Rollback Plan:** Test rollback procedures before cutover

### 4. Execute Migration

Implement in controlled iterations:

```
Iteration Pattern:
1. Migrate component/module (1-2 weeks)
2. Deploy to staging environment
3. Run automated test suite (unit, integration, E2E)
4. Conduct performance testing (load, stress, spike)
5. Execute user acceptance testing (UAT)
6. Deploy to production with feature flag (OFF initially)
7. Monitor metrics for 48 hours
8. Enable feature flag for 10% of traffic
9. Gradually increase to 100% over 1 week
10. Retire old component after 30-day observation period
```

**Critical Rule:** Never migrate data and code simultaneously—migrate code first, then data.

### 5. Validate and Cutover

Execute final switchover with validation:

**Pre-Cutover Checklist:**

- [ ] All automated tests passing (unit, integration, E2E)
- [ ] Performance meets SLA requirements (response time < 2s for 95th percentile)
- [ ] Data validation complete (row counts match, checksums verified)
- [ ] Rollback procedure tested successfully
- [ ] Monitoring dashboards operational
- [ ] On-call team briefed and available
- [ ] Communication sent to all stakeholders

**Cutover Window:** Schedule during lowest traffic period (typically Sunday 2-6 AM)

**Post-Cutover Monitoring:** Monitor these metrics for 72 hours:

- Error rate (must be < 0.1%)
- Response time (must be < 2s for 95th percentile)
- Database connection pool utilization (must be < 80%)
- CPU and memory usage (must be < 70%)
- Business transaction success rate (must be > 99.5%)

## Reference Documentation

Load detailed guides based on migration phase:

- **[migration-assessment.md](references/migration-assessment.md)** - Comprehensive assessment framework with templates and tools. Load when starting assessment phase.

- **[migration-strategies.md](references/migration-strategies.md)** - Detailed strategy patterns with decision matrices and application-specific recommendations. Load when selecting migration approach.

- **[migration-planning.md](references/migration-planning.md)** - Resource planning, timeline estimation, governance setup. Load when creating migration roadmap.

- **[execution-playbook.md](references/execution-playbook.md)** - Step-by-step implementation checklist with environment setup and deployment procedures. Load during execution phase.

- **[best-practices.md](references/best-practices.md)** - Proven patterns, common pitfalls, and optimization techniques. Load when encountering challenges.

- **[metrics-and-success-criteria.md](references/metrics-and-success-criteria.md)** - KPI definitions, measurement methods, success thresholds. Load when defining success criteria.

- **[post-migration-activities.md](references/post-migration-activities.md)** - Decommissioning procedures, optimization strategies, monitoring setup. Load after cutover completion.

## Critical Success Factors

**Never skip these steps:**

1. **Dependency mapping** - Unknown dependencies cause 60% of migration failures
2. **Data validation** - Verify data integrity before AND after migration (row counts, checksums, business rules)
3. **Performance testing** - Test with 2x expected peak load
4. **Rollback testing** - Execute full rollback procedure in staging before cutover
5. **Incremental deployment** - Use feature flags and canary releases (10% → 25% → 50% → 100%)

**Budget Reality:** Migrations typically take 1.5-2x initial estimates. Plan accordingly.

**Communication Cadence:** Send status updates to stakeholders weekly during planning, daily during execution.
