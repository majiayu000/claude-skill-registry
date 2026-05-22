---
name: architecture-evolution
description: Manage architecture changes with impact analysis, ADR generation, and migration planning. Use when relevant to the task.
---

# architecture-evolution

Manage architecture changes with impact analysis, ADR generation, and migration planning.

## Triggers

- "evolve architecture"
- "architecture change"
- "add new component"
- "deprecate [component]"
- "migration plan"
- "breaking change"
- "architecture impact"

## Purpose

This skill manages controlled architecture evolution by:
- Analyzing impact of proposed changes
- Generating Architecture Decision Records (ADRs)
- Planning migration paths
- Tracking breaking changes
- Coordinating cross-team dependencies
- Maintaining architecture health

## Behavior

When triggered, this skill:

1. **Identifies change scope**:
   - Parse proposed change
   - Map affected components
   - Identify stakeholders
   - Classify change type

2. **Performs impact analysis**:
   - Direct dependencies
   - Transitive dependencies
   - Data migration needs
   - API compatibility
   - Performance implications

3. **Generates documentation**:
   - Create or update ADR
   - Update component diagrams
   - Document migration path
   - Update API contracts

4. **Plans migration**:
   - Phase-by-phase approach
   - Rollback strategy
   - Feature flags if needed
   - Communication plan

5. **Coordinates execution**:
   - Notify affected teams
   - Track migration progress
   - Validate each phase
   - Confirm completion

## Change Categories

### Component Addition

```yaml
component_addition:
  description: Adding new service, module, or component

  impact_areas:
    - infrastructure: New deployment resources
    - networking: New routes, load balancing
    - security: Access controls, secrets
    - monitoring: New dashboards, alerts
    - dependencies: Integration points

  artifacts:
    - adr: ADR for new component
    - diagram: Updated architecture diagram
    - contract: API specification
    - runbook: Operational documentation
```

### Component Deprecation

```yaml
component_deprecation:
  description: Phasing out existing component

  impact_areas:
    - dependents: Who uses this component?
    - migration: Where do they migrate to?
    - timeline: How long to deprecate?
    - data: What happens to stored data?
    - cleanup: Resource removal plan

  artifacts:
    - adr: Deprecation decision record
    - migration_guide: How to migrate
    - timeline: Phase-out schedule
    - communication: Stakeholder notifications
```

### Breaking Change

```yaml
breaking_change:
  description: Incompatible change to existing interface

  impact_areas:
    - api_consumers: Who calls this API?
    - contract: What changes in the contract?
    - versioning: How to version the change?
    - backward_compat: Can we support both?
    - rollout: How to phase the rollout?

  artifacts:
    - adr: Breaking change decision
    - migration_guide: Upgrade instructions
    - changelog: Version history update
    - deprecation_notice: Timeline for old version
```

### Technology Migration

```yaml
technology_migration:
  description: Replacing underlying technology

  impact_areas:
    - learning_curve: Team training needs
    - code_changes: Rewrite scope
    - data_migration: Data format changes
    - testing: New test requirements
    - operations: New ops procedures

  artifacts:
    - adr: Technology choice rationale
    - migration_plan: Step-by-step migration
    - runbooks: Updated operational docs
    - training: Team education materials
```

## Impact Analysis Template

```markdown
# Architecture Impact Analysis

**Change**: [Description of proposed change]
**Date**: 2025-12-08
**Author**: [Name]
**Status**: Under Review

## Change Summary

### What is Changing
[Detailed description of the change]

### Why This Change
[Business or technical driver]

### Scope
- **Type**: Component Addition / Deprecation / Breaking Change / Migration
- **Risk Level**: Low / Medium / High / Critical
- **Estimated Effort**: [Time estimate]

## Impact Assessment

### Direct Dependencies

| Component | Impact | Migration Required | Effort |
|-----------|--------|-------------------|--------|
| Service A | High | Yes | 2 weeks |
| Service B | Medium | Yes | 1 week |
| Library X | Low | No | N/A |

### Transitive Dependencies

```
Proposed Change
    ├── Service A (direct)
    │   ├── Service C (transitive)
    │   └── Service D (transitive)
    └── Service B (direct)
        └── Service E (transitive)
```

Total affected: 5 components

### Data Impact

| Data Store | Action | Data Volume | Downtime |
|------------|--------|-------------|----------|
| PostgreSQL | Schema migration | 10M rows | ~5 min |
| Redis | Key format change | 100K keys | None |
| S3 | Path restructure | 500GB | None |

### API Impact

| API | Change Type | Breaking | Version Strategy |
|-----|-------------|----------|------------------|
| /users | Response field added | No | Additive |
| /orders | Endpoint deprecated | Yes | v1 → v2 |
| /auth | Token format | Yes | Dual support 30d |

### Performance Impact

| Metric | Current | Expected | Risk |
|--------|---------|----------|------|
| Latency p99 | 150ms | 180ms | Medium |
| Throughput | 1000 rps | 1200 rps | Positive |
| Memory | 2GB | 2.5GB | Low |

### Security Impact

| Area | Change | Risk | Mitigation |
|------|--------|------|------------|
| Auth | New token type | Medium | Security review |
| Data | New PII field | High | Privacy assessment |
| Network | New endpoint | Low | Firewall rules |

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Migration failure | Medium | High | Rollback plan |
| Performance regression | Low | Medium | Load testing |
| Data loss | Low | Critical | Backup + validation |
| Extended downtime | Low | High | Blue-green deploy |

## Migration Plan

### Phase 1: Preparation (Week 1)
- [ ] Create new infrastructure
- [ ] Deploy in shadow mode
- [ ] Set up monitoring
- [ ] Train ops team

### Phase 2: Gradual Rollout (Week 2-3)
- [ ] 10% traffic migration
- [ ] Monitor for issues
- [ ] 50% traffic migration
- [ ] Validate performance

### Phase 3: Full Migration (Week 4)
- [ ] 100% traffic migration
- [ ] Deprecate old system
- [ ] Cleanup resources

### Rollback Plan

| Phase | Rollback Time | Data Impact | Procedure |
|-------|---------------|-------------|-----------|
| Phase 1 | 5 minutes | None | Disable shadow |
| Phase 2 | 15 minutes | Sync required | Route traffic back |
| Phase 3 | 30 minutes | Manual merge | Full rollback |

## Stakeholders

| Role | Name | Notification | Approval |
|------|------|--------------|----------|
| Architecture | Sarah Chen | Required | Required |
| Security | Elena Rodriguez | Required | Required |
| Ops/SRE | David Kim | Required | Informed |
| Product | James Wilson | Informed | Informed |
| Affected Teams | [List] | Required | Informed |

## Decision

**Recommendation**: Proceed with Phase 1
**Conditions**:
- Security review complete
- Load test passes
- Stakeholder sign-off

## Related Documents

- ADR: .aiwg/architecture/adr-XXX.md
- Migration Guide: .aiwg/architecture/migrations/XXX.md
- Rollback Procedure: .aiwg/deployment/rollback-XXX.md
```

## ADR Generation

When evolution is approved, generate ADR:

```markdown
# ADR-XXX: [Title]

## Status

Proposed → Accepted → Superseded by ADR-YYY (if applicable)

## Context

[What is the issue that we're seeing that is motivating this decision or change?]

## Decision

[What is the change that we're proposing and/or doing?]

## Consequences

### Positive
- [Benefit 1]
- [Benefit 2]

### Negative
- [Trade-off 1]
- [Trade-off 2]

### Risks
- [Risk 1 with mitigation]
- [Risk 2 with mitigation]

## Alternatives Considered

### Option A: [Name]
[Description and why rejected]

### Option B: [Name]
[Description and why rejected]

## Implementation

### Migration Path
[High-level migration steps]

### Timeline
- Phase 1: [Date] - [Description]
- Phase 2: [Date] - [Description]
- Phase 3: [Date] - [Description]

### Rollback Strategy
[How to undo if needed]

## References

- Impact Analysis: [link]
- Design Document: [link]
- Related ADRs: [links]
```

## Usage Examples

### Plan Component Addition

```
User: "Evolve architecture to add caching layer"

Skill executes:
1. Identify change: Add Redis caching
2. Map affected components
3. Analyze impact
4. Generate migration plan

Output:
"Architecture Evolution: Add Caching Layer

Impact Analysis:
- Direct dependencies: 3 services
- Data stores: 1 new (Redis)
- API changes: None
- Performance: +40% expected improvement

Migration Plan:
Phase 1: Deploy Redis cluster (Week 1)
Phase 2: Add cache-aside to read paths (Week 2)
Phase 3: Enable cache warming (Week 3)
Phase 4: Monitor and tune (Week 4)

Risk: Medium
- Rollback: Disable cache reads, direct DB

Generated:
- ADR: .aiwg/architecture/adr-023-caching-layer.md
- Impact Analysis: .aiwg/architecture/impact/caching-layer.md
- Migration Guide: .aiwg/architecture/migrations/add-caching.md"
```

### Handle Breaking Change

```
User: "Breaking change: new auth token format"

Skill analyzes:
1. Identify all token consumers
2. Plan dual-support period
3. Document migration path

Output:
"Breaking Change Analysis: Auth Token Format

Impact:
- 5 services consume auth tokens
- 2 external API consumers identified
- Mobile apps: iOS 3.2+, Android 4.1+

Migration Strategy:
1. Deploy services with dual-token support
2. Issue new tokens, accept both formats
3. Monitor old token usage decline
4. Set deprecation date (30 days)
5. Remove old token support

Communication Plan:
- Internal teams: Slack + email (immediate)
- External consumers: Email + docs (this week)
- Deprecation notice: 30 days minimum

ADR: .aiwg/architecture/adr-024-token-format.md"
```

### Deprecation Planning

```
User: "Deprecate legacy order service"

Skill executes:
1. Map all dependents
2. Identify migration target
3. Plan phase-out timeline

Output:
"Deprecation Plan: Legacy Order Service

Current Consumers: 8 services
Migration Target: Order Service v2

Dependency Migration:
| Consumer | Migration Effort | Target Date |
|----------|-----------------|-------------|
| Cart | 2 weeks | Jan 15 |
| Checkout | 3 weeks | Jan 22 |
| Reports | 1 week | Jan 10 |
| ... | ... | ... |

Timeline:
- Jan 1: Deprecation notice sent
- Jan 31: All consumers migrated
- Feb 15: Service decommissioned

Data Migration:
- 5M orders to migrate
- Strategy: Batch migration + sync
- Duration: 2 hours (off-peak)

ADR: .aiwg/architecture/adr-025-deprecate-order-v1.md
Migration Guide: .aiwg/architecture/migrations/order-v1-to-v2.md"
```

## Integration

This skill uses:
- `decision-support`: For architectural decisions
- `project-awareness`: For component topology
- `artifact-metadata`: For tracking ADRs

## Agent Orchestration

```yaml
agents:
  analysis:
    agent: architecture-designer
    focus: Impact analysis and design

  security:
    agent: security-architect
    focus: Security implications
    condition: security_relevant == true

  reliability:
    agent: reliability-engineer
    focus: Performance and availability impact

  migration:
    agent: deployment-manager
    focus: Migration planning and execution
```

## Configuration

### Change Classification

```yaml
change_classification:
  risk_factors:
    - data_migration: +2
    - breaking_api: +3
    - cross_team: +1
    - production_impact: +2
    - security_change: +2

  risk_levels:
    low: 0-2
    medium: 3-5
    high: 6-8
    critical: 9+

  approval_requirements:
    low: team_lead
    medium: architecture_review
    high: architecture_board
    critical: executive_approval
```

### Migration Strategies

```yaml
migration_strategies:
  big_bang:
    use_when: Low risk, small scope
    downtime: Possible
    rollback: Full

  phased:
    use_when: Medium risk, manageable scope
    downtime: Minimal
    rollback: Per-phase

  blue_green:
    use_when: High availability required
    downtime: Near-zero
    rollback: Traffic switch

  strangler:
    use_when: Large legacy migration
    downtime: None
    rollback: Route traffic
```

## Output Locations

- Impact analyses: `.aiwg/architecture/impact/`
- ADRs: `.aiwg/architecture/adr-*.md`
- Migration plans: `.aiwg/architecture/migrations/`
- Deprecation notices: `.aiwg/architecture/deprecations/`

## References

- ADR template: templates/analysis-design/adr-template.md
- Impact analysis template: templates/analysis-design/impact-analysis.md
- Migration guide template: templates/deployment/migration-guide.md
- Architecture diagram: .aiwg/architecture/diagrams/
