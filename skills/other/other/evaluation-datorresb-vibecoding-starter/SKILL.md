---
name: evaluation
description: Systematic evaluation and comparison of technologies, tools, frameworks, and approaches using weighted criteria and scoring matrices. Use when choosing between multiple technologies, vendor/tool selection, framework comparison, library selection, or architecture pattern selection.
---

# Evaluation Skill

## Core Principle

**Evaluate with criteria, decide with data. Document the trade-offs.**

Good evaluation:
- **Starts with clear criteria** — Define what matters before evaluating
- **Uses consistent scoring** — Apply the same standards to all options
- **Weighs criteria by importance** — Not all factors are equal
- **Documents trade-offs** — Every choice has costs and benefits
- **Leads to defensible decisions** — Data-driven, not opinion-driven

---

## When to Use This Skill

Use this skill when:
- **Choosing between multiple technologies** — React vs Vue vs Angular
- **Vendor/tool selection** — Cloud providers, monitoring tools, CI/CD platforms
- **Framework comparison** — Express vs Fastify, Django vs Flask
- **Library selection** — State management, testing frameworks, HTTP clients
- **Architecture pattern selection** — Microservices vs Monolith, REST vs GraphQL

---

## Evaluation Framework

```
┌────────────────────────────────────────────────────┐
│           EVALUATION PROCESS                       │
└────────────────────────────────────────────────────┘

1. Define Evaluation Criteria
   ↓
2. Assign Weights to Criteria
   ↓
3. Research Each Option
   ↓
4. Score Against Criteria
   ↓
5. Hands-On Testing (PoCs)
   ↓
6. Calculate Weighted Scores
   ↓
7. Document Trade-offs
   ↓
8. Make Recommendation
```

---

## Step 1: Define Evaluation Criteria

### Categories of Criteria

#### Technical Criteria

**Features:**
- Does it have required functionality?
- Are critical features mature and stable?
- Does it support our use cases?
- Are there deal-breaker missing features?

**Performance:**
- Throughput (requests/sec, transactions/sec)
- Latency (response times, p95, p99)
- Resource usage (CPU, memory, disk)
- Benchmark results for our workload

**Scalability:**
- Horizontal scaling capabilities
- Vertical scaling limits
- Load handling characteristics
- Data volume limits

**Security:**
- Vulnerability history
- Security update frequency
- Authentication/authorization support
- Compliance certifications (SOC2, ISO, HIPAA)
- Data encryption (at rest, in transit)

---

#### Operational Criteria

**Reliability:**
- Uptime history (SLA guarantees)
- Error handling capabilities
- Fault tolerance features
- Disaster recovery support

**Monitoring:**
- Built-in observability
- Metrics export (Prometheus, etc.)
- Logging capabilities
- Tracing support (OpenTelemetry)

**Maintenance:**
- Update frequency and process
- Breaking change policy
- Backward compatibility
- Upgrade complexity

---

#### Team Criteria

**Learning Curve:**
- Time to productivity for new developers
- Similarity to existing tools
- Conceptual complexity
- Available training materials

**Documentation:**
- Quality of official docs
- API reference completeness
- Tutorial and guide availability
- Example code quality

**Community:**
- Community size and activity
- GitHub stars/forks/activity
- Stack Overflow questions
- Forum/Discord/Slack activity
- Response time for issues

---

#### Business Criteria

**Cost:**
- Licensing fees (per user, per server, per transaction)
- Infrastructure costs
- Training costs
- Migration costs
- Opportunity costs

**Licensing:**
- License type (MIT, Apache, GPL, proprietary)
- Compatibility with our license
- Commercial use restrictions
- Attribution requirements

**Vendor Lock-in:**
- Portability to alternatives
- Data export capabilities
- Proprietary features vs standards
- Switching costs

**Support:**
- Commercial support availability
- Support response times
- Support quality
- Community vs paid support

---

#### Strategic Criteria

**Ecosystem:**
- Integration with other tools
- Plugin/extension marketplace
- Third-party tool support
- Industry adoption

**Roadmap:**
- Future feature plans
- Product vision alignment
- Investment in development
- Feature request process

**Adoption Trends:**
- Growing vs declining usage
- Industry momentum
- Job market demand
- Analyst recommendations

---

## Step 2: Assign Weights

Not all criteria are equally important. Weight them based on your context.

### Weighting Scale

| Weight | Priority | Meaning |
|--------|----------|---------|
| HIGH | Critical | Deal-breaker if inadequate |
| MEDIUM | Important | Significant impact on decision |
| LOW | Nice-to-have | Minor impact on decision |

### Example: Choosing a Database

| Criterion | Weight | Rationale |
|-----------|--------|-----------|
| ACID guarantees | HIGH | Financial data requires consistency |
| Query performance | HIGH | Core to user experience |
| Horizontal scaling | MEDIUM | Will need in 12-18 months |
| Document flexibility | MEDIUM | Schema will evolve |
| Managed service available | MEDIUM | Small ops team |
| SQL compatibility | LOW | Team can learn new query language |
| Graph query support | LOW | Not a current requirement |

---

## Step 3: Create Scoring Matrix

### Scoring Matrix Template

| Criterion | Weight | Option A | Option B | Option C |
|-----------|--------|----------|----------|----------|
| **Category 1** |
| Criterion 1.1 | HIGH | 8 | 6 | 9 |
| Criterion 1.2 | MEDIUM | 7 | 9 | 5 |
| **Category 2** |
| Criterion 2.1 | HIGH | 9 | 7 | 8 |
| Criterion 2.2 | LOW | 6 | 8 | 7 |
| **Weighted Score** | | **X.X** | **X.X** | **X.X** |

### Scoring Scale

**0-10 Scoring:**
- **9-10** — Excellent, exceeds requirements
- **7-8** — Good, meets requirements well
- **5-6** — Acceptable, meets minimum requirements
- **3-4** — Poor, below requirements
- **0-2** — Inadequate, deal-breaker

**Visual Indicators:**
- ✅ Excellent (8-10)
- ⚠️ Acceptable (5-7)
- ❌ Poor (0-4)

---

## Step 4: Research Each Option

### Research Sources

**Trusted:**
- ✅ Official documentation
- ✅ GitHub repository (code, issues, PRs)
- ✅ Release notes and changelog
- ✅ Production case studies
- ✅ Performance benchmarks (reputable sources)
- ✅ Security advisories and CVE database
- ✅ Team experience and feedback

**Skeptical:**
- ⚠️ Vendor marketing materials
- ⚠️ Paid comparison sites
- ⚠️ Outdated blog posts (>2 years old)
- ⚠️ Hype-driven articles
- ⚠️ Benchmarks by vendors

---

### Technology Evaluation Checklist

For each option, evaluate:

**Documentation Quality:**
- [ ] Getting started guide exists and works
- [ ] API reference is complete
- [ ] Examples cover common use cases
- [ ] Troubleshooting guide available
- [ ] Migration guides (if applicable)

**Community Health:**
- [ ] Active maintainers (commits in last month)
- [ ] Issues are being addressed (response rate)
- [ ] Pull requests are being reviewed
- [ ] Community guidelines exist
- [ ] Code of conduct present

**GitHub Activity (if open source):**
- [ ] Stars: >1000 for libraries, >5000 for frameworks
- [ ] Recent commits (weekly activity)
- [ ] Issue response time (<7 days for critical)
- [ ] PR merge rate (not stagnant)
- [ ] Number of contributors (>10 for critical tools)

**Production Usage:**
- [ ] Companies using it in production
- [ ] Scale of production deployments
- [ ] Case studies available
- [ ] Known production issues

**Integration Complexity:**
- [ ] Works with our existing stack
- [ ] Clear integration examples
- [ ] Migration path from current solution
- [ ] Breaking changes in recent versions

**Performance Characteristics:**
- [ ] Benchmark data available
- [ ] Performance under our expected load
- [ ] Resource requirements documented
- [ ] Performance tuning guidance

**Security:**
- [ ] Security policy documented
- [ ] CVE history reviewed
- [ ] Security update frequency
- [ ] Authentication/authorization support
- [ ] Encryption support

**License:**
- [ ] License type identified
- [ ] Compatible with our project
- [ ] Commercial use allowed
- [ ] Attribution requirements clear

**Cost:**
- [ ] Pricing model clear
- [ ] Hidden costs identified (support, training, infrastructure)
- [ ] Total cost of ownership calculated
- [ ] Budget impact assessed

---

## Step 5: Hands-On Testing

### Build Proof of Concepts (PoCs)

For finalists (typically 2-3 options), build focused PoCs.

**PoC Scope:**
- Time-boxed (1-3 days per option)
- Tests critical features only
- Validates key assumptions
- Measures actual performance
- Assesses developer experience

**What to Test:**
- Integration with critical systems
- Performance with realistic data
- Learning curve (time to hello world)
- Key features that matter most
- Migration complexity (if replacing existing tool)

**PoC Documentation:**
```markdown
# PoC: [Option Name]

## Objective
[What we're validating]

## Setup Time
[How long to get running]

## Key Features Tested
- [ ] Feature 1: [Result]
- [ ] Feature 2: [Result]
- [ ] Feature 3: [Result]

## Performance Results
- Throughput: [X requests/sec]
- Latency p95: [X ms]
- Resource usage: [CPU/Memory]

## Developer Experience
- Ease of use: [Rating 1-10]
- Documentation quality: [Rating 1-10]
- Time to productivity: [X hours/days]

## Issues Encountered
- [Issue 1 and resolution]
- [Issue 2 and resolution]

## Recommendation
[Go/No-go with rationale]
```

See the [proof-of-concept](../proof-of-concept) skill for detailed PoC guidance.

---

## Step 6: Document Trade-offs

Every choice involves trade-offs. Document them explicitly.

### Trade-off Template

**Option A vs Option B:**

| Dimension | Option A | Option B | Winner |
|-----------|----------|----------|--------|
| Performance | 100k req/sec | 50k req/sec | A |
| Learning curve | 2 weeks | 2 days | B |
| Community size | 10k stars | 100k stars | B |
| Flexibility | High | Low | A |
| Maintenance burden | High | Low | B |

**Analysis:**
- Option A is **2x faster** but requires **10x more learning time**
- Option B has **10x larger community** but **less flexibility**
- Trade-off: Do we optimize for performance or team velocity?

---

## Complete Evaluation Example

### Scenario: Frontend Framework Selection

**Context:**
- Team: 5 developers (React experience)
- Project: New e-commerce platform
- Requirements: High performance, SEO support, large ecosystem
- Timeline: 6 months to MVP

---

### Evaluation Criteria with Weights

| Criterion | Weight | Rationale |
|-----------|--------|-----------|
| **Technical** |
| Component model | HIGH | Core to development experience |
| Performance | HIGH | Critical for e-commerce |
| SSR/SSG support | HIGH | Required for SEO |
| TypeScript support | MEDIUM | Team prefers strong typing |
| Mobile support | MEDIUM | Future React Native consideration |
| **Operational** |
| Bundle size | MEDIUM | Affects page load time |
| Build tooling | LOW | All options have good tooling |
| **Team** |
| Learning curve | HIGH | Team has React experience |
| Documentation | HIGH | Need to onboard new devs |
| Community | HIGH | Need plugins and support |
| **Business** |
| Ecosystem | HIGH | Need rich plugin ecosystem |
| Job market | MEDIUM | Hiring considerations |
| Long-term viability | HIGH | 5+ year commitment |

---

### Scoring Matrix

| Criterion | Weight | React | Vue | Svelte | Angular |
|-----------|--------|-------|-----|--------|---------|
| **Technical** |
| Component model | HIGH | ✅ 9 | ✅ 9 | ✅ 10 | ⚠️ 7 |
| Performance | HIGH | ✅ 8 | ✅ 8 | ✅ 10 | ⚠️ 7 |
| SSR/SSG support | HIGH | ✅ 10 | ✅ 9 | ✅ 8 | ✅ 9 |
| TypeScript | MEDIUM | ✅ 9 | ⚠️ 7 | ✅ 9 | ✅ 10 |
| Mobile support | MEDIUM | ✅ 10 | ⚠️ 6 | ❌ 3 | ⚠️ 7 |
| **Operational** |
| Bundle size | MEDIUM | ⚠️ 6 | ✅ 8 | ✅ 10 | ❌ 4 |
| Build tooling | LOW | ✅ 9 | ✅ 8 | ✅ 8 | ✅ 9 |
| **Team** |
| Learning curve | HIGH | ✅ 10 | ✅ 8 | ⚠️ 7 | ⚠️ 6 |
| Documentation | HIGH | ✅ 10 | ✅ 9 | ⚠️ 7 | ✅ 9 |
| Community | HIGH | ✅ 10 | ✅ 8 | ⚠️ 6 | ✅ 9 |
| **Business** |
| Ecosystem | HIGH | ✅ 10 | ✅ 8 | ⚠️ 5 | ✅ 9 |
| Job market | MEDIUM | ✅ 10 | ⚠️ 7 | ⚠️ 5 | ✅ 8 |
| Long-term | HIGH | ✅ 10 | ✅ 8 | ⚠️ 6 | ✅ 9 |
| **Weighted Score** | | **9.2** | **7.9** | **7.0** | **7.8** |

**Legend:**
- ✅ Excellent (8-10)
- ⚠️ Acceptable (5-7)
- ❌ Poor (0-4)

---

### Detailed Analysis

**React (Score: 9.2):**

**Strengths:**
- Team already knows React (minimal learning curve)
- Largest ecosystem (components, tools, libraries)
- Best SSR/SSG story (Next.js is industry standard)
- React Native path for mobile app
- Massive community and job market
- Proven long-term viability

**Weaknesses:**
- Larger bundle size than Vue/Svelte
- Performance slightly behind Svelte
- More boilerplate than Svelte

**PoC Findings:**
- Setup time: 30 minutes with Create React App
- First component: 1 hour
- Full CRUD page: 4 hours
- Next.js SSG working out of the box
- Found excellent UI library (shadcn/ui)

---

**Vue (Score: 7.9):**

**Strengths:**
- Excellent documentation
- Great developer experience
- Good SSR support (Nuxt.js)
- Smaller bundle size than React
- Strong community

**Weaknesses:**
- Team has no Vue experience
- Smaller ecosystem than React
- TypeScript support improving but not as mature
- React Native vs Vue Native comparison

**PoC Findings:**
- Setup time: 45 minutes
- Learning curve steeper than expected for React developers
- Composition API similar to React hooks
- Found most needed plugins

---

**Svelte (Score: 7.0):**

**Strengths:**
- Best performance (compiles to vanilla JS)
- Smallest bundle size
- Elegant syntax, minimal boilerplate
- Growing momentum

**Weaknesses:**
- Smallest ecosystem
- Team has no experience
- SSR story (SvelteKit) less mature than Next.js
- No mobile story
- Smaller job market

**PoC Findings:**
- Setup time: 1 hour
- Syntax very different from React
- Impressed by performance
- Harder to find UI components
- SvelteKit less documented than Next.js

---

**Angular (Score: 7.8):**

**Strengths:**
- Complete framework (batteries included)
- Enterprise backing (Google)
- Excellent TypeScript support
- Strong patterns and structure

**Weaknesses:**
- Steep learning curve (RxJS, dependency injection)
- Largest bundle size
- Team has no Angular experience
- Less flexibility than React/Vue

**PoC Not Pursued:**
- Eliminated after research phase
- Learning curve too steep for timeline
- Team preference for React-like model

---

### Trade-offs Summary

**React vs Vue:**
- React: Better ecosystem, team knowledge, mobile path
- Vue: Slightly better performance, smaller bundle
- **Winner: React** (team velocity and ecosystem outweigh minor performance gains)

**React vs Svelte:**
- Svelte: Best performance, cleanest code
- React: Mature ecosystem, team knowledge, proven at scale
- **Winner: React** (maturity and team velocity critical for 6-month timeline)

---

### Recommendation

**Recommended: React with Next.js**

**Rationale:**
1. **Zero learning curve** — Team already knows React
2. **Best ecosystem** — Largest selection of components and tools
3. **Proven SSR/SSG** — Next.js is production-ready and well-documented
4. **Future mobile app** — React Native provides clear path
5. **Hiring advantage** — Largest React job market
6. **Long-term safety** — React is here to stay

**Risks & Mitigations:**
- **Risk:** Larger bundle size than alternatives
  - **Mitigation:** Use Next.js code splitting, lazy loading, bundle analysis
- **Risk:** Team could become React-only
  - **Mitigation:** Encourage learning Vue/Svelte for side projects

**Implementation Plan:**
1. Setup Next.js project with TypeScript (Week 1)
2. Choose and configure UI library (Week 1)
3. Setup testing framework (Week 1-2)
4. Build design system (Week 2-3)
5. Begin feature development (Week 3+)

**Estimated Effort:** 1 week setup, team productive immediately

---

## Common Evaluation Scenarios

### 1. Database Selection

**Key Criteria:**
- Data model fit (relational, document, graph, time-series)
- ACID vs eventual consistency requirements
- Query patterns and performance
- Horizontal scaling needs
- Managed service availability
- Team expertise

**Example Comparison:**
- PostgreSQL: ACID, complex queries, good scaling, mature
- MongoDB: Flexible schema, horizontal scaling, eventual consistency
- DynamoDB: Fully managed, massive scale, limited query flexibility
- Cassandra: Write-heavy, linear scaling, eventual consistency

---

### 2. Cloud Provider Selection

**Key Criteria:**
- Service offerings for your use case
- Regional availability and latency
- Pricing model and total cost
- Team expertise and learning curve
- Vendor lock-in concerns
- Compliance certifications
- Support quality

**Example Comparison:**
- AWS: Most complete offering, most complex, largest ecosystem
- Azure: Best for Microsoft shops, good enterprise features
- GCP: Excellent for data/ML, strong Kubernetes support, competitive pricing
- DigitalOcean: Simplest, lower cost, fewer features

---

### 3. Testing Framework

**Key Criteria:**
- Language/framework support
- Test types supported (unit, integration, e2e)
- Speed of test execution
- Mocking capabilities
- Assertion library quality
- IDE integration
- Learning curve

**Example Comparison (JavaScript):**
- Jest: Complete solution, React-friendly, good DX
- Vitest: Faster than Jest, Vite integration, modern
- Mocha: Flexible, mature, requires more setup
- Playwright: Best for e2e, multi-browser support

---

### 4. CI/CD Platform

**Key Criteria:**
- Integration with version control
- Pipeline flexibility
- Performance (build speed)
- Cost (minutes, concurrent jobs)
- Self-hosted vs cloud
- Secret management
- Marketplace/plugins

**Example Comparison:**
- GitHub Actions: Tight GitHub integration, generous free tier
- GitLab CI: All-in-one platform, self-hosted option
- Jenkins: Fully self-hosted, maximum flexibility, maintenance burden
- CircleCI: Fast, good DX, credit-based pricing

---

## Decision Documentation

### Link to ADR

For significant decisions, create an Architecture Decision Record (ADR).

See the [adr](../../documentation/adr) skill for ADR templates and workflow.

### ADR Quick Template

```markdown
# ADR-XXX: [Decision Title]

## Status
Accepted

## Context
[Why we needed to evaluate options]
[Constraints and requirements]
[Timeline and stakeholders]

## Options Considered
1. Option A
2. Option B
3. Option C

## Evaluation
[Link to full evaluation document or scoring matrix]

## Decision
We chose [Option X] because [key reasons].

## Consequences

**Positive:**
- [Benefit 1]
- [Benefit 2]

**Negative:**
- [Trade-off 1] — Mitigated by [mitigation]
- [Trade-off 2] — Accepted because [rationale]

## Follow-up Actions
- [ ] Action 1
- [ ] Action 2
```

---

## Evaluation Document Template

```markdown
# Technology Evaluation: [Topic]

**Date:** YYYY-MM-DD
**Author:** [Your name]
**Reviewers:** [Team members who reviewed]
**Status:** [Draft | Under Review | Approved]

---

## Executive Summary

**Decision needed:** [One sentence]
**Recommendation:** [Option X]
**Key reason:** [Primary rationale in one sentence]

---

## Context

**Problem:**
[What problem are we solving?]

**Requirements:**
- [Requirement 1]
- [Requirement 2]
- [Requirement 3]

**Constraints:**
- [Constraint 1: e.g., Budget]
- [Constraint 2: e.g., Timeline]
- [Constraint 3: e.g., Team size]

**Stakeholders:**
- [Stakeholder 1: Interest]
- [Stakeholder 2: Interest]

**Decision deadline:** [Date]

---

## Evaluation Criteria

| Criterion | Weight | Rationale |
|-----------|--------|-----------|
| [Criterion 1] | HIGH | [Why critical] |
| [Criterion 2] | MEDIUM | [Why important] |
| [Criterion 3] | LOW | [Why nice-to-have] |

---

## Options Evaluated

### Option A: [Name]

**Description:** [Brief overview]

**Pros:**
- [Pro 1]
- [Pro 2]
- [Pro 3]

**Cons:**
- [Con 1]
- [Con 2]
- [Con 3]

**Score:** X.X / 10

**PoC findings:** [Link or summary]

---

### Option B: [Name]

[Same structure as Option A]

---

### Option C: [Name]

[Same structure as Option A]

---

## Scoring Matrix

[Include full scoring matrix from evaluation]

---

## Trade-offs Analysis

[Document key trade-offs between top options]

---

## Recommendation

**Recommended:** [Option X]

**Rationale:**
1. [Key reason 1]
2. [Key reason 2]
3. [Key reason 3]

**Risks & Mitigations:**
- **Risk:** [Potential issue]
  - **Mitigation:** [How we'll handle it]
- **Risk:** [Another concern]
  - **Mitigation:** [Response plan]

---

## Implementation Plan

### Phase 1: Setup (Timeline)
- [ ] Task 1
- [ ] Task 2

### Phase 2: Migration (Timeline)
- [ ] Task 1
- [ ] Task 2

### Phase 3: Validation (Timeline)
- [ ] Task 1
- [ ] Task 2

**Total estimated effort:** [Time]

---

## References

- [Official documentation]
- [Benchmark source]
- [PoC repository]
- [Case study]
- [Related ADR]

---

## Appendix: Detailed Scoring

[Include research notes, detailed scores, calculations]
```

---

## Evaluation Anti-Patterns

### 1. Resume-Driven Evaluation

❌ **Anti-pattern:** Choosing technology because it's trendy or looks good on resume

**Signs:**
- "Everyone's talking about [new tech]"
- Ignoring that current solution works well
- Chasing hype cycles
- Complexity for complexity's sake

**Fix:** Evaluate based on actual needs, not trends

---

### 2. Analysis Paralysis

❌ **Anti-pattern:** Evaluating forever, never deciding

**Signs:**
- Evaluating 10+ options
- Adding criteria endlessly
- "Let's research more" when data is sufficient
- Perfectionism blocking decision

**Fix:** Set decision deadline, limit options to 3-5, accept "good enough"

---

### 3. Confirmation Bias

❌ **Anti-pattern:** Deciding first, evaluating to confirm

**Signs:**
- Only researching preferred option deeply
- Ignoring negative evidence
- Scoring subjectively to favor preference
- Cherry-picking benchmarks

**Fix:** Score all options before forming opinion, blind evaluation where possible

---

### 4. Sunk Cost Fallacy

❌ **Anti-pattern:** Continuing with poor choice due to past investment

**Signs:**
- "We've already invested 6 months"
- Ignoring better alternatives
- Escalating commitment despite evidence
- Defending past decision

**Fix:** Evaluate current state objectively, past investment is sunk

---

### 5. Feature Checklist Evaluation

❌ **Anti-pattern:** Choosing option with most features

**Signs:**
- Counting features without weighting importance
- Ignoring that 80% of features won't be used
- Missing quality vs quantity distinction
- Complexity without benefit

**Fix:** Weight features by actual need, value simplicity

---

## Integration with Other Skills

### With Proof-of-Concept

Evaluation identifies options, PoC validates top candidates.

**Workflow:**
1. Evaluate → Narrow to 2-3 finalists
2. PoC → Test finalists hands-on
3. Update scores → Based on PoC findings
4. Decide → With data from both evaluation and PoC

See [proof-of-concept](../proof-of-concept) skill.

---

### With Technical Research

Research gathers information, evaluation structures decision-making.

**Workflow:**
1. Research → Understand the landscape
2. Evaluate → Score options systematically
3. Document → Create decision record

See [technical-research](../technical-research) skill.

---

### With Architecture Review

Evaluation informs architecture decisions, review validates them.

**Workflow:**
1. Evaluate → Choose technology/pattern
2. Design → Create architecture
3. Review → Validate architectural decisions

See [architecture-review](../../engineering/architecture-review) skill.

---

### With ADR

Evaluation provides the data, ADR documents the decision.

**Workflow:**
1. Evaluate → Create scoring matrix
2. Decide → Make recommendation
3. ADR → Record decision with context

See [adr](../../documentation/adr) skill.

---

### With Technical Lead Role

Tech leads use evaluation to make informed decisions.

**Workflow:**
1. Tech lead identifies need for evaluation
2. Team collaborates on criteria and weights
3. Tech lead facilitates evaluation process
4. Team reviews findings
5. Tech lead makes final decision

See [technical-lead-role](../../engineering/technical-lead-role) skill.

---

## Quick Reference

### Evaluation Process Checklist

**Planning:**
- [ ] Define evaluation criteria (technical, operational, team, business, strategic)
- [ ] Assign weights based on context (HIGH/MEDIUM/LOW)
- [ ] Identify 3-5 options to evaluate
- [ ] Set decision deadline

**Research:**
- [ ] Review official documentation for each option
- [ ] Check GitHub activity and community health
- [ ] Research production usage and case studies
- [ ] Review security and licensing

**Scoring:**
- [ ] Create scoring matrix (0-10 scale)
- [ ] Score all options consistently
- [ ] Calculate weighted scores
- [ ] Document rationale for scores

**Validation:**
- [ ] Build PoCs for top 2-3 options
- [ ] Test critical features
- [ ] Measure actual performance
- [ ] Assess developer experience
- [ ] Update scores based on findings

**Decision:**
- [ ] Analyze trade-offs between options
- [ ] Document risks and mitigations
- [ ] Make recommendation with rationale
- [ ] Create ADR for significant decisions
- [ ] Communicate decision to stakeholders

---

### Evaluation Criteria Quick List

**Technical:** Features, performance, scalability, security
**Operational:** Reliability, monitoring, maintenance
**Team:** Learning curve, documentation, community
**Business:** Cost, licensing, vendor lock-in, support
**Strategic:** Ecosystem, roadmap, adoption trends

---

### Scoring Guidelines

- **9-10:** Excellent, exceeds requirements
- **7-8:** Good, meets requirements well
- **5-6:** Acceptable, meets minimum
- **3-4:** Poor, below requirements
- **0-2:** Inadequate, deal-breaker

---

### When to Re-evaluate

- New major version released
- Significant change in requirements
- Team size or expertise changes
- Better alternatives emerge
- Performance degrades
- Security issues discovered
- Vendor acquired or direction changes
- Every 1-2 years for critical dependencies

---

**Remember:** Good evaluation leads to good decisions. Define criteria before scoring, weight by importance, validate with hands-on testing. Document trade-offs transparently so future you (and your team) understands why the decision was made. Every choice has costs—make them explicit.
