---
name: Trade-off Analysis
description: Systematic evaluation of architectural trade-offs to make informed decisions balancing competing concerns.
---

# Trade-off Analysis

## Overview

Trade-off Analysis is the process of evaluating competing concerns (performance vs cost, flexibility vs simplicity) to make informed architectural decisions. Every architectural choice involves trade-offs.

**Core Principle**: "There are no perfect solutions, only trade-offs. Choose consciously."

---

## 1. Common Architectural Trade-offs

| Trade-off | Description |
|-----------|-------------|
| **Performance vs Cost** | Faster systems cost more (bigger instances, more caching) |
| **Flexibility vs Simplicity** | More flexible systems are more complex |
| **Consistency vs Availability** | CAP theorem: can't have both under partition |
| **Speed vs Quality** | Ship fast vs build it right |
| **Build vs Buy** | Custom solution vs third-party |
| **Coupling vs Duplication** | DRY vs independent services |

---

## 2. Trade-off Matrix

```markdown
## Trade-off: Microservices vs Monolith

| Dimension | Microservices | Monolith | Winner |
|-----------|---------------|----------|--------|
| **Scalability** | ⭐⭐⭐⭐⭐ (independent scaling) | ⭐⭐⭐ (scale entire app) | Microservices |
| **Operational Complexity** | ⭐⭐ (many services to manage) | ⭐⭐⭐⭐⭐ (single deployment) | Monolith |
| **Development Speed** | ⭐⭐⭐ (parallel teams) | ⭐⭐⭐⭐ (simpler coordination) | Depends on team size |
| **Debugging** | ⭐⭐ (distributed tracing needed) | ⭐⭐⭐⭐⭐ (single codebase) | Monolith |
| **Technology Flexibility** | ⭐⭐⭐⭐⭐ (polyglot) | ⭐⭐ (single stack) | Microservices |
| **Team Size Requirement** | ⭐⭐ (needs 10+ engineers) | ⭐⭐⭐⭐⭐ (works with 2+) | Monolith |

**Decision**: Start with modular monolith, extract microservices later if needed.
```

---

## 3. CAP Theorem Trade-offs

```
Choose 2 of 3:
- Consistency (all nodes see same data)
- Availability (system always responds)
- Partition Tolerance (works despite network failures)

Examples:
- PostgreSQL: CP (Consistency + Partition Tolerance)
- Cassandra: AP (Availability + Partition Tolerance)
- Traditional RDBMS: CA (Consistency + Availability, no partition tolerance)
```

---

## 4. Performance vs Cost Analysis

```markdown
## Scenario: Caching Strategy

### Option 1: Redis Cluster (High Performance)
- **Cost**: $500/month
- **Latency**: 1-5ms
- **Availability**: 99.99%
- **Complexity**: High (cluster management)

### Option 2: In-Memory Cache (Low Cost)
- **Cost**: $0 (included in app servers)
- **Latency**: <1ms
- **Availability**: 99.9% (tied to app)
- **Complexity**: Low

### Option 3: No Cache (Lowest Cost)
- **Cost**: $0
- **Latency**: 50-200ms (database query)
- **Availability**: 99.95%
- **Complexity**: Very low

**Decision**: Start with Option 2 (in-memory), migrate to Option 1 when traffic > 10K req/s
```

---

## 5. Build vs Buy Decision Framework

```markdown
## Criteria Scoring (1-5, 5 = best)

| Criteria | Build Custom | Buy SaaS | Weight |
|----------|--------------|----------|--------|
| **Time to Market** | 2 (6 months) | 5 (1 week) | 0.3 |
| **Cost (Year 1)** | 3 ($100K eng time) | 4 ($20K subscription) | 0.2 |
| **Customization** | 5 (full control) | 2 (limited) | 0.2 |
| **Maintenance** | 2 (our responsibility) | 5 (vendor handles) | 0.2 |
| **Security** | 3 (our expertise) | 4 (vendor expertise) | 0.1 |

**Weighted Score**:
- Build: 2×0.3 + 3×0.2 + 5×0.2 + 2×0.2 + 3×0.1 = 2.9
- Buy: 5×0.3 + 4×0.2 + 2×0.2 + 5×0.2 + 4×0.1 = 4.1

**Decision**: Buy SaaS solution
```

---

## 6. Flexibility vs Simplicity

```typescript
// Simple but inflexible
function sendEmail(to: string, subject: string, body: string) {
  // Hardcoded to SendGrid
  sendgrid.send({ to, subject, body });
}

// Flexible but complex
interface EmailProvider {
  send(email: Email): Promise<void>;
}

class EmailService {
  constructor(private provider: EmailProvider) {}
  
  async send(email: Email) {
    // Can swap providers (SendGrid, SES, Postmark)
    await this.provider.send(email);
  }
}

// Trade-off: Flexibility adds abstraction layer
// Decision: Use simple version until we need to swap providers
```

---

## 7. Consistency vs Availability (PACELC)

```
PACELC Theorem:
- If Partition: Choose Availability or Consistency
- Else (no partition): Choose Latency or Consistency

Examples:
- DynamoDB: PA/EL (Availability + Low Latency)
- MongoDB: PC/EC (Consistency + Consistency)
- Cassandra: PA/EL (Availability + Low Latency)
```

---

## 8. Technical Debt vs Feature Velocity

```markdown
## Scenario: Refactor vs New Feature

### Option A: Refactor Legacy Code
- **Time**: 3 weeks
- **Business Value**: $0 (no new features)
- **Technical Value**: Easier to add features later
- **Risk**: Low (improves code quality)

### Option B: Build New Feature on Legacy Code
- **Time**: 1 week
- **Business Value**: $50K revenue
- **Technical Value**: Increases technical debt
- **Risk**: Medium (harder to maintain)

### Option C: Hybrid (Minimal Refactor + Feature)
- **Time**: 2 weeks
- **Business Value**: $50K revenue
- **Technical Value**: Slight improvement
- **Risk**: Medium

**Decision**: Option C - Refactor only the parts we touch for the new feature
```

---

## 9. Trade-off Documentation Template

```markdown
## Trade-off: [Decision Name]

### Context
[What problem are we solving?]

### Options Considered

#### Option 1: [Name]
**Pros**:
- [Benefit 1]
- [Benefit 2]

**Cons**:
- [Drawback 1]
- [Drawback 2]

**Cost**: [Time/Money]
**Risk**: [Low/Medium/High]

#### Option 2: [Name]
[Same structure]

### Decision Criteria
1. [Criterion 1] (Weight: 30%)
2. [Criterion 2] (Weight: 25%)
3. [Criterion 3] (Weight: 20%)

### Scoring
[Use matrix or weighted scoring]

### Decision
We chose [Option X] because [rationale].

### Mitigations
To address the downsides of our choice:
- [Mitigation 1]
- [Mitigation 2]
```

---

## 10. Trade-off Analysis Checklist

- [ ] **Options Identified**: At least 2-3 alternatives?
- [ ] **Criteria Defined**: Clear decision criteria?
- [ ] **Pros/Cons Listed**: Honest assessment of each?
- [ ] **Quantified**: Costs, time, risks estimated?
- [ ] **Weighted**: Criteria weighted by importance?
- [ ] **Scored**: Objective scoring applied?
- [ ] **Mitigations**: Downsides addressed?
- [ ] **Documented**: Decision recorded in ADR?

---

## Related Skills
- `59-architecture-decision/adr-templates`
- `59-architecture-decision/tech-stack-selection`
- `00-meta-skills/decision-making`
