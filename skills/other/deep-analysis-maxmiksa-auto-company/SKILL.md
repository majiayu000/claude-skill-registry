---
name: deep-analysis
description: Analytical thinking patterns for comprehensive evaluation, code audits, security analysis, and performance reviews. Provides structured templates for thorough investigation with extended thinking support.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Task
  - WebFetch
  - WebSearch
dependencies:
  - extended-thinking
  - complex-reasoning
triggers:
  - analyze
  - audit
  - review
  - assess
  - evaluate
  - investigate
  - deep dive
  - comprehensive review
  - security analysis
  - performance analysis
  - code audit
---

# Deep Analysis Skill

Comprehensive analytical templates for thorough investigation, audits, and evaluations leveraging extended thinking capabilities.

## When to Use

- **Code audits** requiring systematic review
- **Security assessments** and threat modeling
- **Performance analysis** and optimization planning
- **Architecture reviews** and technical debt assessment
- **Incident post-mortems** and root cause analysis
- **Compliance audits** and risk assessments

## Analysis Templates

### Code Audit Template

```markdown
## Code Audit Report

**Repository**: [repo-name]
**Scope**: [files/modules audited]
**Date**: [YYYY-MM-DD]
**Auditor**: Claude + [Human reviewer]

### Executive Summary
[2-3 sentence overview of findings]

### Audit Criteria
- [ ] Code quality and maintainability
- [ ] Security vulnerabilities
- [ ] Performance concerns
- [ ] Test coverage
- [ ] Documentation completeness
- [ ] Dependency health

### Critical Findings
| ID | Severity | Location | Issue | Recommendation |
|----|----------|----------|-------|----------------|
| C1 | Critical | file:line | [Issue] | [Fix] |
| C2 | Critical | file:line | [Issue] | [Fix] |

### High Priority Findings
| ID | Severity | Location | Issue | Recommendation |
|----|----------|----------|-------|----------------|
| H1 | High | file:line | [Issue] | [Fix] |

### Medium Priority Findings
[...]

### Low Priority / Suggestions
[...]

### Metrics
| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Test Coverage | 75% | 80% | ⚠️ |
| Cyclomatic Complexity | 12 | <10 | ⚠️ |
| Technical Debt | 4.2d | <3d | ❌ |
| Security Score | 8/10 | 9/10 | ⚠️ |

### Recommendations
1. **Immediate**: [Critical fixes]
2. **Short-term**: [Within sprint]
3. **Long-term**: [Tech debt reduction]

### Sign-off
- [ ] All critical issues addressed
- [ ] High priority issues have timeline
- [ ] Audit findings documented in backlog
```

### Security Threat Model Template

```markdown
## Threat Model: [System/Component Name]

**Version**: [1.0]
**Last Updated**: [YYYY-MM-DD]
**Classification**: [Internal/Confidential]

### System Overview
[Brief description of the system being modeled]

### Assets
| Asset | Description | Sensitivity | Owner |
|-------|-------------|-------------|-------|
| User Data | PII, credentials | Critical | Auth Team |
| API Keys | Service credentials | High | DevOps |
| Business Data | Transactions | High | Product |

### Trust Boundaries
```
┌─────────────────────────────────────────┐
│           External (Untrusted)          │
│  [Internet Users] [Third-party APIs]    │
└──────────────────┬──────────────────────┘
                   │ WAF/Load Balancer
┌──────────────────┴──────────────────────┐
│              DMZ (Semi-trusted)         │
│  [API Gateway] [CDN] [Public Services]  │
└──────────────────┬──────────────────────┘
                   │ Internal Firewall
┌──────────────────┴──────────────────────┐
│           Internal (Trusted)            │
│  [App Servers] [Databases] [Queues]     │
└─────────────────────────────────────────┘
```

### Threat Categories (STRIDE)

#### Spoofing
| Threat | Likelihood | Impact | Mitigation |
|--------|------------|--------|------------|
| Credential theft | Medium | High | MFA, rate limiting |
| Session hijacking | Low | High | Secure cookies, HTTPS |

#### Tampering
| Threat | Likelihood | Impact | Mitigation |
|--------|------------|--------|------------|
| SQL injection | Medium | Critical | Parameterized queries |
| Data modification | Low | High | Integrity checks |

#### Repudiation
[...]

#### Information Disclosure
[...]

#### Denial of Service
[...]

#### Elevation of Privilege
[...]

### Attack Vectors
1. **Vector 1**: [Description]
   - Entry point: [Where]
   - Technique: [How]
   - Mitigation: [Defense]

### Risk Matrix
| Threat | Likelihood | Impact | Risk Score | Priority |
|--------|------------|--------|------------|----------|
| T1     | High       | Critical | 9 | P1 |
| T2     | Medium     | High | 6 | P2 |
| T3     | Low        | Medium | 3 | P3 |

### Security Controls
| Control | Type | Status | Coverage |
|---------|------|--------|----------|
| WAF | Preventive | ✅ Active | External |
| SAST | Detective | ✅ CI/CD | Code |
| DAST | Detective | ⚠️ Partial | Runtime |
| Encryption | Preventive | ✅ Active | Data |

### Recommendations
1. [Priority 1 recommendations]
2. [Priority 2 recommendations]
3. [Priority 3 recommendations]
```

### Performance Analysis Template

```markdown
## Performance Analysis Report

**System**: [System name]
**Period**: [Date range]
**Environment**: [Production/Staging]

### Executive Summary
[Key findings and recommendations]

### Performance Metrics

#### Response Times
| Endpoint | P50 | P95 | P99 | Target | Status |
|----------|-----|-----|-----|--------|--------|
| /api/users | 45ms | 120ms | 350ms | <200ms | ✅ |
| /api/search | 230ms | 890ms | 2.1s | <500ms | ❌ |
| /api/reports | 1.2s | 3.4s | 8.2s | <2s | ❌ |

#### Throughput
| Service | Current RPS | Peak RPS | Capacity | Utilization |
|---------|-------------|----------|----------|-------------|
| API | 1,200 | 2,400 | 5,000 | 48% |
| Worker | 500 | 800 | 1,000 | 80% |

#### Resource Utilization
| Resource | Average | Peak | Threshold | Status |
|----------|---------|------|-----------|--------|
| CPU | 45% | 78% | 80% | ⚠️ |
| Memory | 62% | 85% | 85% | ⚠️ |
| Disk I/O | 30% | 55% | 70% | ✅ |
| Network | 25% | 40% | 60% | ✅ |

### Bottleneck Analysis

#### Identified Bottlenecks
1. **Database Queries** (High Impact)
   - Location: `/api/search` endpoint
   - Cause: Missing index on `created_at` column
   - Impact: 890ms P95 latency
   - Fix: Add composite index

2. **Memory Pressure** (Medium Impact)
   - Location: Report generation service
   - Cause: Large dataset loading into memory
   - Impact: GC pauses, OOM risks
   - Fix: Implement streaming/pagination

### Load Test Results
| Scenario | Users | Duration | Errors | Avg Response |
|----------|-------|----------|--------|--------------|
| Baseline | 100 | 10min | 0% | 120ms |
| Normal | 500 | 30min | 0.1% | 180ms |
| Peak | 1000 | 15min | 2.3% | 450ms |
| Stress | 2000 | 5min | 15% | 2.1s |

### Optimization Recommendations

#### Quick Wins (This Sprint)
1. Add database indexes - Expected: 40% improvement
2. Enable query caching - Expected: 25% improvement
3. Optimize N+1 queries - Expected: 30% improvement

#### Medium Term (Next Quarter)
1. Implement read replicas
2. Add CDN for static assets
3. Optimize serialization

#### Long Term (6+ Months)
1. Service decomposition
2. Event-driven architecture
3. Edge computing deployment

### Capacity Planning
| Timeframe | Expected Load | Current Capacity | Gap | Action |
|-----------|---------------|------------------|-----|--------|
| 3 months | +25% | 5,000 RPS | ✅ | Monitor |
| 6 months | +50% | 5,000 RPS | ⚠️ | Scale |
| 12 months | +100% | 5,000 RPS | ❌ | Redesign |
```

### Architecture Review Template

```markdown
## Architecture Review

**System**: [System name]
**Version**: [Current architecture version]
**Review Date**: [YYYY-MM-DD]
**Participants**: [Team members]

### Current Architecture

#### System Diagram
```
[Include architecture diagram or ASCII representation]
```

#### Components
| Component | Purpose | Technology | Owner |
|-----------|---------|------------|-------|
| API Gateway | Request routing | Kong | Platform |
| Auth Service | Authentication | Keycloak | Security |
| Core API | Business logic | Python/FastAPI | Backend |
| Database | Data persistence | PostgreSQL | Data |

#### Data Flow
1. User request → API Gateway
2. API Gateway → Auth validation
3. Auth → Core API
4. Core API → Database
5. Response → User

### Evaluation Criteria

#### Scalability
| Aspect | Current | Target | Gap | Score |
|--------|---------|--------|-----|-------|
| Horizontal scaling | Manual | Auto | Yes | 6/10 |
| Database scaling | Single | Sharded | Yes | 5/10 |
| Caching | Redis | Distributed | No | 8/10 |

#### Reliability
| Aspect | Current | Target | Gap | Score |
|--------|---------|--------|-----|-------|
| Availability | 99.5% | 99.9% | Yes | 7/10 |
| Disaster recovery | Manual | Auto | Yes | 5/10 |
| Data backup | Daily | Real-time | Yes | 6/10 |

#### Maintainability
| Aspect | Current | Target | Gap | Score |
|--------|---------|--------|-----|-------|
| Code modularity | Medium | High | Yes | 6/10 |
| Documentation | Partial | Complete | Yes | 5/10 |
| Test coverage | 70% | 85% | Yes | 7/10 |

### Technical Debt Assessment
| Item | Impact | Effort | Priority | Age |
|------|--------|--------|----------|-----|
| Legacy auth system | High | High | P1 | 2y |
| Monolithic API | Medium | High | P2 | 1.5y |
| Missing monitoring | Medium | Low | P1 | 1y |

### Recommendations

#### Immediate (0-3 months)
1. [Recommendation 1]
2. [Recommendation 2]

#### Short-term (3-6 months)
1. [Recommendation 1]
2. [Recommendation 2]

#### Long-term (6-12 months)
1. [Recommendation 1]
2. [Recommendation 2]

### Decision Log
| Decision | Rationale | Alternatives Considered | Date |
|----------|-----------|------------------------|------|
| [Decision 1] | [Why] | [Options] | [Date] |
```

## Integration with Extended Thinking

For deep analysis tasks, use maximum thinking budget:

```python
response = client.messages.create(
    model="claude-opus-4-5-20250514",
    max_tokens=32000,
    thinking={
        "type": "enabled",
        "budget_tokens": 25000  # Maximum budget for deep analysis
    },
    system="""You are a senior technical analyst performing a
    comprehensive review. Use structured analysis templates and
    document all findings systematically.""",
    messages=[{
        "role": "user",
        "content": "Perform a security threat model for..."
    }]
)
```

## Best Practices

1. **Use appropriate templates**: Match template to analysis type
2. **Be systematic**: Follow the template structure completely
3. **Quantify findings**: Use metrics and severity ratings
4. **Prioritize actionable**: Focus on findings that can be fixed
5. **Document evidence**: Link to specific code/logs/data
6. **Track progress**: Update findings as they're addressed

## See Also

- [[extended-thinking]] - Enable deep reasoning capabilities
- [[complex-reasoning]] - Reasoning frameworks
- [[testing]] - Validation strategies
- [[debugging]] - Issue investigation
