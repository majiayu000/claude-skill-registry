---
name: rails-analyst
description: Business and systems analyst for Rails projects. Use when decomposing features into tasks, estimating complexity, describing architecture, writing JTBD (Jobs To Be Done), creating use cases, identifying risks, analyzing project weaknesses, and planning product features.
---

# Rails Analyst

Business and systems analysis for Rails applications. Decompose features, estimate work, analyze risks, and document requirements.

## When to Use This Skill

- Feature decomposition into implementable tasks
- Task complexity estimation (story points, time estimates)
- Architecture design and documentation
- Writing JTBD (Jobs To Be Done) for product features
- Creating use cases and user stories
- Risk identification and mitigation planning
- Project weakness analysis
- Technical feasibility assessment
- Requirements gathering and documentation
- Stakeholder communication and clarification

## Jobs To Be Done (JTBD) Framework

JTBD focuses on **why** users "hire" your product, not what they do with it.

**Format:**
```
When [situation], I want to [motivation], so I can [expected outcome].
```

**Example:**
- When I have a draft article ready, I want to publish it with one click, so I can share my ideas without technical hassle.

**Translating to Features:**
- One-click publish button
- Draft auto-save
- Validation before publish
- Preview before publishing

## Use Cases

### Use Case Template

```markdown
## Use Case: [Name]

**Actor:** [Who performs this action]
**Goal:** [What they want to achieve]
**Preconditions:** [What must be true before]

### Main Flow:
1. User does X
2. System validates Y
3. System performs Z
4. User sees confirmation

### Error Scenarios:
- Validation fails → Show errors
- Authorization fails → Show 403
```

## Task Decomposition

Break features into implementable chunks:

```markdown
## Epic: Article Comments System

### Stage 1: Data & Models (2 days)
- [ ] Create Comment migration
- [ ] Add Comment model with associations
- [ ] Write model specs (100% coverage)

### Stage 2: Business Logic (2 days)
- [ ] Create Comments::Create interaction
- [ ] Add comment moderation (AASM)
- [ ] Write interaction specs

### Stage 3: API/Controllers (2 days)
- [ ] Create CommentsController
- [ ] Add authorization (Pundit)
- [ ] Write request specs

**Total:** 6 days + 20% buffer = 7-8 days
```

## Estimation Techniques

### Story Points (Fibonacci)

- **1 point:** Trivial (add validation, update text)
- **2 points:** Simple (add model field, basic CRUD)
- **3 points:** Moderate (new model with associations)
- **5 points:** Complex (feature with multiple models)
- **8 points:** Very complex (new subsystem)
- **13+ points:** Too large - decompose further

### T-Shirt Sizing

- **XS (< 2h):** Trivial changes, bug fixes
- **S (2-4h):** Simple features, single file
- **M (1-2 days):** Moderate features, multiple files
- **L (3-5 days):** Complex features, cross-cutting
- **XL (1-2 weeks):** Major features, architecture
- **XXL (> 2 weeks):** Epic - must decompose

## Risk Analysis

### Risk Matrix

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Database migration fails | Medium | Critical | Test on staging, plan rollback |
| Third-party API limits | High | Medium | Implement caching, retry logic |
| Security vulnerability | Low | Critical | Add encryption, security audit |

**Risk Levels:**
- **Critical:** Data loss, security breach, compliance
- **High:** Performance degradation, user experience
- **Medium:** Minor bugs, cosmetic issues
- **Low:** Nice-to-have features

## Architecture Decision Records (ADRs)

```markdown
# ADR-001: Use Solid Queue for Background Jobs

## Status
Accepted

## Context
Need background job processing for emails, reports, exports.

## Decision
Use Solid Queue (Rails 7.1+ native, database-backed).

## Rationale
- No additional infrastructure (vs Redis/Sidekiq)
- Mission Control web UI included
- Simpler deployment
- Good enough for our scale

## Consequences
**Positive:** Lower costs, simpler ops
**Negative:** Slightly slower than Redis
**Review Date:** 6 months
```

## Project Weakness Analysis

### Analysis Framework

1. **Code Quality**
   - Test coverage gaps
   - Code duplication
   - Complex methods

2. **Architecture**
   - Tight coupling
   - Missing abstractions
   - Technical debt

3. **Security**
   - Unencrypted sensitive data
   - Missing authorization
   - Vulnerabilities

4. **Performance**
   - N+1 queries
   - Missing indexes
   - Slow endpoints

5. **Operations**
   - Missing monitoring
   - No backup strategy
   - Deployment risks

### Quick Assessment

```markdown
## Critical Issues
1. No database backups (Priority: Immediate)
2. Unencrypted PII (Priority: This week)
3. Missing rate limiting (Priority: This month)

## Recommendations
- **Immediate:** Setup backups, fix N+1 queries
- **Short Term:** Encrypt PII, add rate limiting
- **Long Term:** Refactor controllers, improve tests
```

## Communication Templates

### Feature Proposal

```markdown
# Feature Proposal: [Name]

## Problem Statement
[What problem? Who experiences it?]

## Jobs To Be Done
[3-5 JTBD from different user perspectives]

## Proposed Solution
[High-level description]

## Success Metrics
- Reduce support tickets by 30%
- Increase engagement by 20%

## Complexity
- **Estimate:** 2 weeks
- **Risk Level:** Medium
- **Dependencies:** None

## Recommendation
[Go / No-Go / Defer]
```

## Best Practices

### ✅ Do

- **Start with JTBD** - Understand the "why"
- **Decompose ruthlessly** - No task >2 days
- **Document decisions** - Use ADRs
- **Identify risks early** - Surface concerns upfront
- **Estimate conservatively** - Add 20% buffer
- **Track velocity** - Use historical data
- **Communicate clearly** - Write for stakeholders
- **Update estimates** - Revise as you learn

### ❌ Don't

- **Don't skip use cases** - They catch edge cases
- **Don't ignore risks** - Hope is not mitigation
- **Don't overestimate** - Be realistic
- **Don't work in isolation** - Validate with devs
- **Don't ignore feedback** - Users know best
- **Don't plan too far** - Requirements change

---

## Reference Documentation

For detailed examples and templates:
- Full analyst guide: `analyst-reference.md` (comprehensive templates, examples, and workflows)

---

**Remember**: The analyst's job is to **reduce uncertainty** and **enable informed decisions**. Good analysis turns "we should build X" into "here's exactly what X means, what it costs, what could go wrong, and whether we should do it."
