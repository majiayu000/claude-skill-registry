---
description: Product roadmap and feature prioritization expert with RICE, MoSCoW, and Kano frameworks. Use when planning product roadmaps, prioritizing features across increments, or defining success metrics and KPIs. Covers ROI analysis, stakeholder communication, and quarterly planning.
---

# Roadmap Planner - Strategic Product Planning

**Purpose**: Provide expert guidance on product roadmaps, feature prioritization frameworks, success metrics definition, and stakeholder communication.

**When to Use**:
- Planning product roadmaps (quarterly, annual)
- Prioritizing features across multiple increments
- Defining success metrics and KPIs
- Communicating technical decisions to stakeholders
- Analyzing ROI and business impact

---

## Feature Prioritization Frameworks

### RICE Score

**Formula**: `RICE = (Reach × Impact × Confidence) / Effort`

**Components**:
- **Reach**: How many users/customers will this impact per quarter?
- **Impact**: How much will this impact each user? (0.25 = minimal, 0.5 = low, 1 = medium, 2 = high, 3 = massive)
- **Confidence**: How confident are you in your estimates? (50% = low, 80% = medium, 100% = high)
- **Effort**: How many person-weeks/months will this take?

**Example**:
```
Feature: Real-time Collaboration
- Reach: 8000 users/quarter (80% of user base)
- Impact: 3 (Massive impact on user satisfaction)
- Confidence: 70% (some unknowns in WebSocket scalability)
- Effort: 8 person-weeks

RICE = (8000 × 3 × 0.7) / 8 = 2100

Higher RICE = Higher Priority
```

**When to Use RICE**:
- ✅ Large feature backlogs (50+ features)
- ✅ Data-driven product teams
- ✅ B2C products with large user bases
- ✅ Need to compare features objectively

**RICE Scoring Table Example**:
```markdown
| Feature | Reach | Impact | Confidence | Effort | RICE Score | Priority |
|---------|-------|--------|------------|--------|------------|----------|
| Real-time Collaboration | 8000 | 3 | 70% | 8 | 2100 | P1 |
| Dark Mode | 6000 | 1 | 90% | 2 | 2700 | P1 |
| Advanced Search | 4000 | 2 | 60% | 6 | 800 | P2 |
| Mobile App | 10000 | 3 | 50% | 20 | 750 | P2 |
| AI Suggestions | 5000 | 2 | 40% | 12 | 333 | P3 |
```

---

### MoSCoW Prioritization

**Categories**:
- **Must Have**: Critical for MVP, without these product fails
  - Non-negotiable requirements
  - Legal/compliance requirements
  - Core value proposition

- **Should Have**: Important but not critical, workarounds exist
  - Adds significant value
  - Can be deferred if necessary
  - User experience improvements

- **Could Have**: Nice-to-have, adds value but not essential
  - Desirable features
  - Low implementation effort
  - "Polish" items

- **Won't Have**: Out of scope for this release
  - Future roadmap items
  - Technical debt cleanup
  - Edge case features

**Example**:
```markdown
## Feature Prioritization (Q1 2026 MVP)

### Must Have (P1)
| Feature | Reason |
|---------|--------|
| User Authentication | Foundation for all other features, security requirement |
| Task CRUD Operations | Core value proposition, minimum viable product |
| Real-time Synchronization | Key differentiator vs competitors |

### Should Have (P2)
| Feature | Reason |
|---------|--------|
| File Attachments | Requested by 60% of beta users, improves collaboration |
| Task Comments | Team collaboration feature, workaround: use Slack |

### Could Have (P3)
| Feature | Reason |
|---------|--------|
| Dark Mode | UI polish, low effort, nice-to-have |
| Custom Themes | Requested by enterprise customers, can wait for v2 |

### Won't Have (This Release)
- Mobile apps (Q2 2026 roadmap)
- Advanced analytics dashboard (Q3 2026)
- API for third-party integrations (Q4 2026)
- Offline mode (technical complexity too high for MVP)
```

**When to Use MoSCoW**:
- ✅ MVP planning (focus on "Must Have")
- ✅ Agile sprints (prioritize within time-box)
- ✅ Stakeholder alignment (clear categories)
- ✅ Resource-constrained teams

---

### Kano Model

**Categories**:
- **Basic Needs** (Threshold Attributes):
  - Users expect these by default
  - Absence causes dissatisfaction
  - Presence doesn't increase satisfaction
  - Examples: Authentication, data persistence, security

- **Performance Needs** (Linear Attributes):
  - More is better
  - Satisfaction increases linearly with quality
  - Examples: Speed, reliability, uptime, accuracy

- **Excitement Needs** (Delighters):
  - Unexpected features that delight users
  - Absence doesn't cause dissatisfaction
  - Presence creates competitive advantage
  - Examples: AI suggestions, beautiful UI, thoughtful details

**Example Analysis**:
```markdown
## Kano Model Analysis: Task Management App

### Basic Needs (Must Work)
- User authentication (email/password)
- Create, read, update, delete tasks
- Data persistence (don't lose my tasks!)
- Secure data storage (HTTPS, encrypted)
- Basic search functionality

### Performance Needs (More is Better)
- **Speed**: Task creation < 100ms
- **Reliability**: 99.9% uptime SLA
- **Accuracy**: Search finds relevant tasks
- **Capacity**: Support 10K+ tasks per user
- **Responsiveness**: UI updates instantly

### Excitement Needs (Delighters)
- **AI-powered task suggestions**: "You might want to schedule a follow-up"
- **Beautiful, minimalist UI**: Thoughtful animations, delightful interactions
- **Smart reminders**: Context-aware notifications
- **Collaboration magic**: Seamless real-time updates
- **Voice input**: "Add task: Buy milk"
```

**When to Use Kano**:
- ✅ Understanding user expectations
- ✅ Differentiating from competitors
- ✅ Balancing "table stakes" vs innovation
- ✅ UX/product design decisions

---

## Product Roadmap Creation

### Quarterly Roadmap Template

**Structure**: Themes → Features → Success Metrics

**Example**:
```markdown
# Product Roadmap 2026

## Q1 2026: Foundation (MVP)
**Theme**: Core Task Management
**Goal**: Launch with 100 beta users
**Team Focus**: Backend + Frontend (1:1 split)

### Features
- ✅ User Authentication (Weeks 1-2) - COMPLETED
  - Email/password login
  - Password reset flow
  - Session management

- ✅ Task CRUD Operations (Weeks 3-4) - COMPLETED
  - Create, read, update, delete tasks
  - Task properties: title, description, due date, priority
  - Basic filtering and sorting

- 🔄 Real-time Synchronization (Weeks 5-7) - IN PROGRESS
  - WebSocket-based live updates
  - Conflict resolution (Operational Transform)
  - Offline queue with sync on reconnect

- ⏳ File Attachments (Weeks 8-9) - PLANNED
  - Upload files (images, PDFs, docs)
  - S3 storage integration
  - Virus scanning

- ⏳ Beta Launch (Week 10) - PLANNED
  - Onboarding flow
  - User feedback mechanism
  - Analytics instrumentation

### Success Metrics
- **User Acquisition**: 100 active beta users
- **Engagement**: >70% weekly active usage
- **Performance**: <5 min average onboarding time
- **Quality**: <5 critical bugs reported per week

### Risks & Mitigations
- **Risk**: WebSocket scalability issues at 100 concurrent users
  - **Mitigation**: Load testing with 200 users, fallback to polling
- **Risk**: Low beta signups
  - **Mitigation**: ProductHunt launch, Reddit outreach

---

## Q2 2026: Collaboration
**Theme**: Team Features
**Goal**: 1K paying customers, $50K MRR
**Team Focus**: Backend + Frontend + Mobile (2:2:1 split)

### Features
- Team workspaces (multi-tenant architecture)
- Role-based permissions (owner, admin, member, viewer)
- Task comments and @mentions
- Activity feeds (real-time notifications)
- Mobile apps (iOS/Android React Native)

### Success Metrics
- **Revenue**: $50K MRR (avg $5/user/month)
- **Growth**: 1K paying customers
- **Retention**: <2% monthly churn rate
- **Activation**: 60% of signups create a team within 7 days

---

## Q3 2026: Integrations
**Theme**: Workflow Automation
**Goal**: 5K customers, $200K MRR

### Features
- Slack integration (notifications, create tasks from Slack)
- GitHub integration (link tasks to PRs, auto-close on merge)
- Zapier webhooks (connect to 3000+ apps)
- Public API for third-party apps (REST + GraphQL)
- Workflow automation (IFTTT-style rules)

### Success Metrics
- **Integration Adoption**: 40% of teams use at least one integration
- **API Usage**: 500K API calls/month
- **Revenue**: $200K MRR
- **NPS**: >50 (promoters significantly outnumber detractors)

---

## Q4 2026: Enterprise
**Theme**: Scale & Compliance
**Goal**: 10K customers, $500K MRR

### Features
- SSO (SAML, OAuth for enterprise)
- Advanced permissions (custom roles, granular ACLs)
- Audit logs (compliance requirements)
- SOC 2 Type II compliance
- Custom SLAs for enterprise customers

### Success Metrics
- **Enterprise Customers**: 50 companies (>100 seats each)
- **Revenue**: $500K MRR ($200K from enterprise tier)
- **Compliance**: SOC 2 Type II certification
- **Uptime**: 99.99% SLA for enterprise tier
```

---

## Success Metrics & KPIs

### Framework: OKRs (Objectives & Key Results)

**Example**:
```yaml
objective: "Become the #1 task management tool for remote teams"

key_results:
  KR1:
    metric: "Daily Active Users (DAU)"
    target: "70% of registered users"
    measurement: "Track unique logins per day (Mixpanel)"
    current: "52%"
    target_date: "2026-Q2"

  KR2:
    metric: "Feature Adoption - Real-time Collaboration"
    target: "50% of teams use real-time editing within first week"
    measurement: "Track WebSocket connections per team"
    current: "0% (feature not launched)"
    target_date: "2026-Q1"

  KR3:
    metric: "Customer Satisfaction (NPS)"
    target: "NPS > 40"
    measurement: "In-app survey after 1 week of use"
    current: "28"
    target_date: "2026-Q3"

  KR4:
    metric: "Revenue Growth"
    target: "$200K MRR by end of Q3"
    measurement: "Stripe dashboard (MRR)"
    current: "$15K MRR"
    target_date: "2026-Q3"
```

### Metric Categories

**Engagement Metrics**:
- Daily Active Users (DAU)
- Weekly Active Users (WAU)
- Monthly Active Users (MAU)
- DAU/MAU ratio (stickiness)
- Session duration
- Feature adoption rate

**Performance Metrics**:
- API response time (p50, p95, p99)
- Page load time (< 2 seconds)
- Sync latency (< 100ms)
- Error rate (< 0.1%)
- Uptime SLA (99.9% → 99.99%)

**Business Metrics**:
- Monthly Recurring Revenue (MRR)
- Customer Acquisition Cost (CAC)
- Lifetime Value (LTV)
- LTV:CAC ratio (should be > 3:1)
- Churn rate (< 2% monthly)
- Net Promoter Score (NPS)

**Example Measurement Plan**:
```markdown
## Measurement Plan: Real-time Collaboration Feature

### Instrumentation
1. **Analytics Events** (Mixpanel/Amplitude)
   - `collaboration_session_started`
   - `collaboration_edit_made`
   - `collaboration_conflict_resolved`
   - `collaboration_session_ended`

2. **Performance Monitoring** (Grafana/Datadog)
   - WebSocket connection metrics
   - Message round-trip latency (p50, p95, p99)
   - Concurrent user count per workspace
   - Operational Transform conflict rate

3. **User Feedback** (In-app surveys)
   - NPS survey after 1 week of use
   - "How would you rate the real-time collaboration feature?" (1-5 stars)
   - "What could we improve?"

### Success Criteria (Go/No-Go Decision)
- ✅ **PASS**: 50%+ teams adopt feature within 1 week
- ✅ **PASS**: p95 latency < 200ms
- ✅ **PASS**: < 1% conflict rate requiring manual merge
- ✅ **PASS**: NPS improvement of +10 points

- ❌ **FAIL**: Adoption < 30% after 2 weeks → Investigate UX issues
- ❌ **FAIL**: p95 latency > 500ms → Performance optimization required
```

---

## Stakeholder Communication

### Translating Technical to Business Impact

**Input**: Technical architecture decision
**Output**: Business-friendly explanation with ROI

**Example**:
```markdown
## Stakeholder Update: Microservices Architecture Migration

### Executive Summary
We're proposing a shift from our current monolithic architecture to microservices. This is a significant technical change that will deliver measurable business benefits.

### Business Impact Summary

**Benefits**:

1. **Faster Feature Delivery** (30% improvement)
   - **Current**: Teams block each other, 3-week average time-to-market
   - **Future**: Teams work independently, 2-week average time-to-market
   - **Impact**: Ship features 33% faster, respond to customer requests quicker
   - **Revenue Impact**: Faster iteration → better product-market fit → higher conversion

2. **Better Scalability** (2x cost efficiency)
   - **Current**: Scale entire system even if only one feature needs it ($100K/year infrastructure)
   - **Future**: Scale only the parts that need it ($50K/year infrastructure)
   - **Impact**: Save $50K/year in AWS costs
   - **Example**: During Black Friday, scale only payment service, not entire app

3. **Reduced Risk** (99.9% → 99.99% uptime)
   - **Current**: If one service fails, entire app goes down (8 hours downtime/year)
   - **Future**: If one service fails, others keep running (1 hour downtime/year)
   - **Impact**: 7 hours less downtime = $200K revenue protected
   - **Customer Trust**: Fewer incidents = better reputation

**Costs**:
- **Engineering Time**: 8 weeks of dedicated migration work
- **New Tools**: +$5K/year for monitoring and orchestration (Kubernetes, Datadog)
- **Short-term Risk**: Temporary productivity dip during migration

**ROI Analysis**:
- **Costs**: $150K (8 weeks × 3 engineers × $75K salary + $5K tools)
- **Benefits Year 1**: $250K ($50K infra savings + $200K revenue protection)
- **Net Benefit Year 1**: $100K
- **Break-even**: 6 months
- **Payback Period**: 18 months for 3x ROI

**Recommendation**: Approve for Q3 implementation
**Timeline**: 8 weeks (Q3 2026)
**Team**: 3 backend engineers, 1 DevOps engineer
**Risk Level**: Medium (well-established pattern, many success stories)
```

---

## Integration with SpecWeave

### When PM Agent Should Use Roadmap Planner

**Automatic Activation**:
- User asks: "What should we prioritize?"
- User mentions: "roadmap", "RICE", "MoSCoW", "Kano"
- User wants: Quarterly planning, feature ranking

**PM Agent Workflow**:
1. Gather feature ideas (from user, backlog, stakeholders)
2. **Delegate to Roadmap Planner skill** for prioritization
3. Present prioritized roadmap with rationale
4. Create increments for P1 (Must Have) features
5. Defer P2/P3 to backlog

---

## Related Skills

- **PM Agent**: Uses roadmap-planner for strategic planning
- **increment-planner**: Executes individual increments from roadmap
- **spec-generator**: Creates detailed specs for prioritized features

---

## Version History

- **v1.0.0** (2025-11-21): Initial release, extracted from PM agent for better modularity

## Project-Specific Learnings

**Before starting work, check for project-specific learnings:**

```bash
# Check if skill memory exists for this skill
cat .specweave/skill-memories/roadmap-planner.md 2>/dev/null || echo "No project learnings yet"
```

Project learnings are automatically captured by the reflection system when corrections or patterns are identified during development. These learnings help you understand project-specific conventions and past decisions.

