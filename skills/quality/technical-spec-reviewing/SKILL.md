---
name: technical-spec-reviewing
description: Reviews technical specifications for completeness, feasibility, and production readiness. Validates architecture, APIs, security, and operational concerns. Use when reviewing tech specs before implementation or architecture review meetings.
version: 1.0.0
---

# Technical Spec Reviewing

## Purpose

Systematically review technical specifications to ensure they are complete, feasible, secure, and ready for implementation. Catches architectural issues, security gaps, and operational blind spots before engineering work begins.

## When NOT to Use This Skill

- Creating technical specs (use `technical-spec-writing` instead)
- Reviewing PRDs (use `prd-reviewing` instead)
- Reviewing feature specs (use `feature-spec-reviewing` instead)
- Code review (different domain)
- No spec exists yet (nothing to review)

## Review Workflow

### Step 1: Document Assessment

Read the entire technical spec and assess completeness:

```markdown
Initial Assessment:
- [ ] System overview explains the approach
- [ ] Component architecture is defined
- [ ] APIs are fully specified
- [ ] Data model is documented
- [ ] Performance targets exist
- [ ] Security considerations addressed
- [ ] Migration plan included
```

**Red Flags:**
- No rationale for design decisions
- Missing component responsibilities
- APIs without error responses
- No performance targets
- Security as afterthought
- No rollback plan

### Step 2: System Overview Review

Evaluate the problem and solution framing:

```markdown
System Overview Checklist:
1. Is the problem statement clear?
2. Does the solution address the problem?
3. Are design decisions justified with rationale?
4. Is the scope clearly bounded?
5. Are out-of-scope items documented?
6. Does it align with requirements (PRD/Feature Spec)?
```

**Severity Guide:**
| Issue | Severity |
|-------|----------|
| No problem statement | BLOCKER |
| Solution doesn't address problem | BLOCKER |
| No design rationale | CRITICAL |
| Scope unclear | CRITICAL |
| Misaligned with requirements | MAJOR |

### Step 3: Architecture Review

Evaluate the component architecture:

```markdown
Architecture Checklist:
- [ ] Components have clear responsibilities
- [ ] Component boundaries are well-defined
- [ ] Dependencies are documented
- [ ] Data flow is clear
- [ ] Coupling is appropriate
- [ ] Scalability is considered
- [ ] Failure modes identified
```

**Architecture Questions:**
| Question | Good Answer | Bad Answer |
|----------|-------------|------------|
| Why this component boundary? | "Separates read/write concerns" | "It seemed logical" |
| How does it scale? | "Horizontal via stateless design" | "Not sure" |
| Single point of failure? | "No, using redundancy at X" | "The database" |
| What if component X fails? | "Y takes over via Z" | Not addressed |

### Step 4: API Design Review

Evaluate API completeness and quality:

```markdown
API Review Checklist:
- [ ] All endpoints documented
- [ ] Request/response schemas complete
- [ ] Error responses specified
- [ ] Authentication/authorization defined
- [ ] Rate limiting documented
- [ ] Versioning strategy clear
- [ ] Idempotency addressed (for mutations)
```

**API Quality Tests:**

| Test | Pass | Fail |
|------|------|------|
| Can a developer implement from this? | Full schemas, examples | Vague descriptions |
| Error handling clear? | Error catalog with codes | "Returns error" |
| Security defined? | Auth method, permissions | "Requires auth" |
| Backward compatible? | Versioning strategy | Breaking changes unclear |

### Step 5: Data Model Review

Evaluate data design:

```markdown
Data Model Checklist:
- [ ] All entities defined
- [ ] Relationships documented
- [ ] Indexes specified
- [ ] Constraints defined
- [ ] Migration scripts included
- [ ] Data lifecycle addressed
- [ ] Backup/recovery considered
```

**Data Model Questions:**
| Question | Expected Answer |
|----------|-----------------|
| Why this schema design? | Trade-offs explained |
| How does it handle growth? | Partitioning, archival strategy |
| Query patterns supported? | Indexes match queries |
| Backward compatible? | Migration path defined |

### Step 6: Performance Review

Evaluate performance planning:

```markdown
Performance Checklist:
- [ ] Latency targets defined (p50, p95, p99)
- [ ] Throughput targets specified
- [ ] Caching strategy documented
- [ ] Database query optimization planned
- [ ] Async processing identified
- [ ] Load testing approach
```

**Performance Quality:**
| Aspect | Good | Bad |
|--------|------|-----|
| Targets | "< 200ms p95" | "Should be fast" |
| Caching | "Redis, 5min TTL, invalidate on update" | "Use caching" |
| Optimization | "Index on (user_id, created_at)" | "Add indexes" |

### Step 7: Security Review

Evaluate security considerations:

```markdown
Security Checklist:
- [ ] Authentication mechanism defined
- [ ] Authorization model specified
- [ ] Data protection (at rest, in transit)
- [ ] Input validation strategy
- [ ] OWASP Top 10 addressed
- [ ] Audit logging planned
- [ ] Secrets management
```

**Security Red Flags:**
| Red Flag | Severity |
|----------|----------|
| No authentication section | BLOCKER |
| No input validation | CRITICAL |
| Hardcoded secrets | BLOCKER |
| No encryption specified | CRITICAL |
| Missing rate limiting | MAJOR |
| No audit logging | MAJOR |

### Step 8: Operational Readiness

Evaluate operational concerns:

```markdown
Operations Checklist:
- [ ] Logging strategy defined
- [ ] Metrics identified
- [ ] Alerting thresholds set
- [ ] Health checks specified
- [ ] Deployment strategy clear
- [ ] Rollback plan documented
- [ ] Feature flags defined
- [ ] On-call runbook items
```

**Operational Maturity:**
| Level | Characteristics |
|-------|-----------------|
| Basic | Logging exists, some metrics |
| Good | Structured logging, dashboards, basic alerts |
| Excellent | Full observability, runbooks, chaos testing |

### Step 9: Migration & Rollout Review

Evaluate deployment planning:

```markdown
Migration Checklist:
- [ ] Migration steps defined
- [ ] Each step is reversible
- [ ] Data migration addressed
- [ ] Feature flags for gradual rollout
- [ ] Rollback triggers defined
- [ ] Rollout phases planned
- [ ] Success criteria per phase
```

**Migration Questions:**
| Question | Good Answer | Bad Answer |
|----------|-------------|------------|
| What if migration fails? | "Rollback script ready" | "Fix forward" |
| How to verify success? | "Check metrics A, B, C" | "Monitor logs" |
| Blast radius? | "5% of users first" | "Full deployment" |

### Step 10: Generate Review Report

Compile findings using the template below.

## Severity Levels

| Level | Definition | Action |
|-------|------------|--------|
| **BLOCKER** | Cannot implement safely | Must fix before approval |
| **CRITICAL** | Will cause major issues | Should fix before implementation |
| **MAJOR** | Will cause rework | Should fix soon |
| **MINOR** | Nice to have | Can address during implementation |

### Severity Examples

**BLOCKER:**
- No security section
- Missing authentication design
- No error handling defined
- Data model fundamentally flawed
- No rollback possible

**CRITICAL:**
- Performance targets missing
- Incomplete API error responses
- No rate limiting
- Missing migration plan
- Security gaps (e.g., no input validation)

**MAJOR:**
- Vague component responsibilities
- Missing non-functional requirements
- Incomplete observability plan
- No feature flags for rollout
- Missing capacity planning

**MINOR:**
- Minor documentation gaps
- Additional edge cases nice to have
- Could add more examples
- Formatting inconsistencies

## Review Report Template

```markdown
# Technical Spec Review: [System/Feature Name]

**Reviewer:** [Name]
**Review Date:** [Date]
**Spec Version:** [Version]
**Spec Author:** [Name]

---

## Summary

**Status:** [APPROVE / APPROVE WITH CHANGES / NEEDS REVISION / MAJOR REVISION]

**Implementation Readiness:** [Ready / Ready After Fixes / Not Ready]

**Assessment:**
[2-3 sentences on overall quality and readiness]

---

## Findings by Severity

### Blockers
- [ ] [Finding with location and recommendation]

### Critical
- [ ] [Finding with location and recommendation]

### Major
- [ ] [Finding with location and recommendation]

### Minor
- [ ] [Finding with location and recommendation]

---

## Section Ratings

| Section | Rating | Notes |
|---------|--------|-------|
| System Overview | [Strong/Adequate/Weak/Missing] | |
| Architecture | [Strong/Adequate/Weak/Missing] | |
| API Design | [Strong/Adequate/Weak/Missing] | |
| Data Model | [Strong/Adequate/Weak/Missing] | |
| Performance | [Strong/Adequate/Weak/Missing] | |
| Security | [Strong/Adequate/Weak/Missing] | |
| Operations | [Strong/Adequate/Weak/Missing] | |
| Migration | [Strong/Adequate/Weak/Missing] | |

---

## Architecture Assessment

**Scalability:** [Good / Concerns / Not Addressed]
- [Notes]

**Reliability:** [Good / Concerns / Not Addressed]
- [Notes]

**Maintainability:** [Good / Concerns / Not Addressed]
- [Notes]

---

## Security Assessment

□ Authentication - [Adequate/Gaps/Missing]
□ Authorization - [Adequate/Gaps/Missing]
□ Data Protection - [Adequate/Gaps/Missing]
□ Input Validation - [Adequate/Gaps/Missing]
□ OWASP Top 10 - [Addressed/Gaps/Missing]

**Security Score:** [X/5]

---

## Operational Readiness

□ Logging - [Defined/Partial/Missing]
□ Metrics - [Defined/Partial/Missing]
□ Alerting - [Defined/Partial/Missing]
□ Deployment - [Defined/Partial/Missing]
□ Rollback - [Defined/Partial/Missing]

**Operations Score:** [X/5]

---

## Strengths
- [What the spec does well]
- [What the spec does well]

## Risks
1. [Risk and suggested mitigation]
2. [Risk and suggested mitigation]

---

## Questions for Author
1. [Clarifying question]
2. [Clarifying question]

---

## Recommendation

[Detailed recommendation with specific next steps]
```

## Examples

### Example 1: Strong Spec (Minor Feedback)

**Status:** APPROVE WITH CHANGES

**Assessment:**
Well-designed system with clear architecture and comprehensive API documentation. Minor gaps in observability and could benefit from more detailed rollback procedures.

**Findings:**
- MINOR: Missing p99 latency targets
- MINOR: Alerting thresholds not defined
- MINOR: Add example for error recovery flow

**Section Ratings:**
| Section | Rating |
|---------|--------|
| Architecture | Strong |
| API Design | Strong |
| Security | Adequate |
| Operations | Weak |

---

### Example 2: Needs Work (Critical Gaps)

**Status:** NEEDS REVISION

**Assessment:**
Good system overview but significant gaps in security and operational planning. Error handling incomplete. Recommend addressing security concerns before implementation begins.

**Findings:**
- CRITICAL: No rate limiting defined
- CRITICAL: Input validation strategy missing
- CRITICAL: No rollback plan for database migration
- MAJOR: Missing circuit breaker for external dependencies
- MAJOR: No feature flags for gradual rollout
- MAJOR: Alerting strategy undefined

**Security Score:** 2/5
**Operations Score:** 1/5

---

### Example 3: Major Problems

**Status:** MAJOR REVISION REQUIRED

**Assessment:**
Architecture has fundamental issues - single point of failure in message queue, no data consistency strategy for distributed writes. Recommend architectural review session.

**Findings:**
- BLOCKER: No authentication for internal service communication
- BLOCKER: Single message queue with no failover
- BLOCKER: Distributed transaction across 3 services without saga pattern
- CRITICAL: No data backup strategy
- CRITICAL: Missing capacity planning

**Recommendation:** Schedule architecture review meeting. Consider:
1. Add service mesh for internal auth
2. Implement message queue clustering
3. Design saga pattern for distributed transactions

## Review Focus Areas by Spec Type

### New Service
Focus on: Architecture, scalability, operational readiness, security

### New API
Focus on: API design, authentication, rate limiting, documentation

### Database Changes
Focus on: Data model, migrations, backward compatibility, performance

### Performance Optimization
Focus on: Targets, measurement, caching, async processing

### Security Enhancement
Focus on: Threat model, authentication, authorization, encryption

## Integration with Other Skills

**Reviews Output From:**
- `technical-spec-writing` - Validate completed technical specs

**Works With:**
- `feature-spec-reviewing` - Review associated feature specs
- `prd-reviewing` - Verify alignment with product requirements

**Leads To:**
- `sparc-planning` - After spec approved, plan implementation

## Resources

- See CHECKLIST.md for comprehensive review checklist


---

## Related Agent

For comprehensive specification guidance that coordinates this and other spec skills, use the **`specification-architect`** agent.
