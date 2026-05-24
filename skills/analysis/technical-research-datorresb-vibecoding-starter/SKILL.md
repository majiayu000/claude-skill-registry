---
name: technical-research
description: Systematic technical research methodology for evaluating technologies, libraries, and approaches. Use when researching new technologies, comparing alternatives, or making technical decisions.
---

# Technical Research Skill

## Core Principle

**Research systematically to make evidence-based decisions.**

Good technical research:
- **Starts with clear questions** — Know what you're trying to decide
- **Evaluates systematically** — Consistent criteria across options
- **Documents findings** — Share knowledge with team
- **Leads to action** — Research informs decisions

---

## Research Process

```
┌────────────────────────────────────────────────────┐
│           RESEARCH PROCESS                         │
└────────────────────────────────────────────────────┘

1. Define Question
   ↓
2. Establish Criteria
   ↓
3. Find Candidates
   ↓
4. Evaluate Systematically
   ↓
5. Hands-On Verification
   ↓
6. Document & Decide
```

---

## Step 1: Define the Research Question

### Start with "Why"

❌ **Vague:** "Research state management libraries"
✅ **Clear:** "Which state management library best fits our React app with complex async workflows?"

### Good Research Questions

✅ "Should we migrate from REST to GraphQL for our mobile API?"
✅ "Which message queue (RabbitMQ, Kafka, AWS SQS) handles our 10M events/day use case best?"
✅ "Can we replace our custom auth with Auth0 without breaking existing integrations?"

### Bad Research Questions

❌ "What's the best framework?" (Depends on context)
❌ "Should we use microservices?" (Missing constraints)
❌ "Is technology X good?" (No decision criteria)

---

## Step 2: Establish Evaluation Criteria

### Categories of Criteria

**Functional:**
- Does it solve our problem?
- Does it have required features?
- Does it integrate with our existing stack?

**Non-Functional:**
- Performance (speed, resource usage)
- Scalability (handles our load?)
- Reliability (uptime, error rates)
- Security (vulnerabilities, updates)

**Team & Org:**
- Team expertise (learning curve)
- Documentation quality
- Community support
- License compatibility

**Operational:**
- Maintenance burden
- Hosting/infrastructure costs
- Monitoring/observability
- Deployment complexity

---

### Prioritize Criteria

Not all criteria are equally important.

**Example: Choosing a Database**

| Criterion | Weight | Why |
|-----------|--------|-----|
| Query performance | HIGH | Core to user experience |
| ACID guarantees | HIGH | Financial data, must be consistent |
| Horizontal scaling | MEDIUM | Will need it in 12-18 months |
| SQL compatibility | LOW | Team can learn new query language |

---

## Step 3: Find Candidates

### Sources

**Trusted sources:**
- Official documentation
- GitHub repos (stars, activity, issues)
- Technology radars (ThoughtWorks, etc.)
- Stack Overflow trends
- Team experience

**Be skeptical of:**
- Marketing websites
- Outdated blog posts
- Hype-driven articles
- Vendor comparisons

---

### Narrowing Down

Start broad, narrow systematically:

1. **Initial research:** 10-20 candidates
2. **Quick filter:** 3-5 top candidates (based on obvious deal-breakers)
3. **Deep dive:** 2-3 finalists
4. **Hands-on:** 1-2 prototypes

---

## Step 4: Evaluate Systematically

### Use a Scoring Matrix

**Example: API Client Libraries**

| Criterion | Weight | Option A | Option B | Option C |
|-----------|--------|----------|----------|----------|
| **Functional** |
| RESTful support | HIGH | ✅ 10 | ✅ 10 | ⚠️ 6 |
| GraphQL support | MEDIUM | ✅ 8 | ❌ 0 | ✅ 10 |
| Auth integration | HIGH | ✅ 9 | ⚠️ 7 | ✅ 9 |
| **Non-Functional** |
| Performance | MEDIUM | ⚠️ 7 | ✅ 9 | ⚠️ 7 |
| Bundle size | LOW | ✅ 9 | ⚠️ 6 | ❌ 4 |
| **Team & Org** |
| Learning curve | HIGH | ✅ 9 | ⚠️ 6 | ❌ 3 |
| Documentation | HIGH | ✅ 10 | ✅ 8 | ⚠️ 5 |
| **Operational** |
| Maintenance | MEDIUM | ✅ 9 | ⚠️ 6 | ⚠️ 6 |
| **Weighted Score** | | **8.6** | **6.9** | **6.7** |

**Legend:**
- ✅ Excellent (8-10)
- ⚠️ Acceptable (5-7)
- ❌ Poor (0-4)

**Conclusion:** Option A best fits our needs

---

## Step 5: Hands-On Verification

### Build a Proof of Concept (POC)

**Purpose:** Validate assumptions with real code

**Scope:**
- Small (1-3 days max)
- Focused (test key concerns)
- Disposable (will be thrown away)

**What to test:**
- Integration points
- Performance with realistic data
- Developer experience
- Edge cases that matter

---

### POC Structure

```
poc-experiment/
├── README.md           # What you're testing and why
├── setup.sh            # How to run it
├── src/
│   ├── integration.js  # Test key integration
│   └── performance.js  # Test performance concern
├── results.md          # Findings and measurements
└── decision.md         # Recommendation based on POC
```

---

### Example POC Goals

**Evaluating a new database:**
- ✅ Can we migrate existing data?
- ✅ Does query performance meet our <100ms requirement?
- ✅ Can we implement our complex search feature?

**Evaluating a framework:**
- ✅ Can we integrate with our auth system?
- ✅ Does it handle our file upload use case?
- ✅ Is the learning curve acceptable for the team?

---

## Step 6: Document & Decide

### Research Document Template

```markdown
# Research: [Topic]

## Context

**Problem:** [What problem are we solving?]

**Decision needed by:** [Date]

**Stakeholders:** [Who cares about this decision?]

---

## Research Question

[Clear, specific question]

---

## Evaluation Criteria

| Criterion | Priority | Rationale |
|-----------|----------|-----------|
| [Criterion 1] | HIGH | [Why this matters] |
| [Criterion 2] | MEDIUM | [Why this matters] |

---

## Candidates Evaluated

### Option A: [Name]

**Pros:**
- [Pro 1]
- [Pro 2]

**Cons:**
- [Con 1]
- [Con 2]

**Score:** X/10

**POC findings:** [Link to POC or summary]

---

### Option B: [Name]

[Same structure]

---

## Recommendation

**Recommended:** [Option X]

**Rationale:**
- [Key reason 1]
- [Key reason 2]
- [Key reason 3]

**Risks & Mitigations:**
- **Risk:** [Potential issue]
  **Mitigation:** [How we'll handle it]

---

## Implementation Plan

1. [Step 1]
2. [Step 2]
3. [Step 3]

**Estimated effort:** [Time estimate]

---

## References

- [Link to documentation]
- [Link to POC]
- [Link to similar case studies]

---

**Date:** 2026-01-09
**Author:** [Your name]
**Reviewers:** [Who reviewed this]
```

---

## Research Anti-Patterns

### 1. Analysis Paralysis

❌ **Anti-pattern:** Researching forever, never deciding

**Signs:**
- Evaluating 15+ options
- Adding more criteria endlessly
- "Let's do more research" when decision is clear

**Fix:** Set time limits and decision deadlines

---

### 2. Resume-Driven Development

❌ **Anti-pattern:** Choosing tech because it looks good on resume

**Signs:**
- "Let's use [hot new tech] because everyone is talking about it"
- Ignoring that current solution works fine
- Choosing complex over simple without justification

**Fix:** Evaluate based on actual needs, not hype

---

### 3. Not Invented Here (NIH)

❌ **Anti-pattern:** Building custom solution instead of using existing tools

**Signs:**
- "It's simple, we can build it ourselves"
- Underestimating maintenance burden
- Ignoring mature, well-tested alternatives

**Fix:** Calculate total cost of ownership (development + maintenance)

---

### 4. Sunk Cost Fallacy

❌ **Anti-pattern:** Continuing with poor choice because of past investment

**Signs:**
- "We've already invested 6 months in this"
- Ignoring better alternatives
- Escalating commitment to failing approach

**Fix:** Evaluate current state objectively, past is sunk cost

---

## Research Checklists

### Before Starting Research

- [ ] Clear research question defined
- [ ] Evaluation criteria established
- [ ] Priorities assigned to criteria
- [ ] Decision deadline set
- [ ] Stakeholders identified

---

### During Research

- [ ] Evaluating at least 2-3 alternatives
- [ ] Using consistent criteria across all options
- [ ] Documenting findings as you go
- [ ] Building POCs for top candidates
- [ ] Measuring against real requirements

---

### Before Making Decision

- [ ] All high-priority criteria evaluated
- [ ] Hands-on validation completed (POC)
- [ ] Team has reviewed findings
- [ ] Risks identified with mitigations
- [ ] Implementation plan outlined
- [ ] Decision documented

---

## Integration with Other Skills

### With Documentation Writing

- Document research in Architecture Decision Records (ADRs)
- Share findings with team
- Create decision trail for future reference

### With Code Review

- Use research findings to inform coding standards
- Reference research when reviewing architectural decisions

### With Testing Strategy

- POCs should include tests
- Validate performance claims with benchmarks

---

## Quick Reference

### Research Question Template

"Which [technology/approach] best [solves our problem] given [our constraints]?"

### Evaluation Criteria Categories

1. **Functional** — Does it work for our use case?
2. **Non-Functional** — Performance, security, reliability
3. **Team** — Learning curve, documentation, support
4. **Operational** — Maintenance, cost, complexity

### POC Scope

- **Time:** 1-3 days
- **Goal:** Validate key assumptions
- **Output:** Decision recommendation

---

**Remember:** Good research leads to good decisions. Define clear questions, evaluate systematically, validate with hands-on testing. Document your findings so others can learn from your work. Don't let perfect be the enemy of good—research enough to decide, then act.
