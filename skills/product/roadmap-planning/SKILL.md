---
name: Roadmap Planning
description: Comprehensive guide to creating, communicating, and maintaining technical and product roadmaps for strategic alignment and stakeholder communication
---

# Roadmap Planning

## What is a Roadmap?

A **roadmap** is a visual plan that shows how your product or technology will evolve over time.

### Three Key Purposes

1. **Visual Plan of Work Over Time**
   - What we're building
   - When we're building it (roughly)
   - Why we're building it

2. **Strategic Alignment Tool**
   - Connects daily work to company strategy
   - Shows how initiatives support goals
   - Ensures team is working on right things

3. **Communication Device**
   - **Stakeholders:** Shows progress and plans
   - **Team:** Provides context and direction
   - **Customers:** Builds trust and manages expectations

### What a Roadmap is NOT

❌ **Not a Gantt Chart:** No specific dates, no detailed tasks
❌ **Not a Commitment:** Plans change based on learnings
❌ **Not a Feature List:** Focus on outcomes, not just features

---

## Types of Roadmaps

### 1. Product Roadmap (Features, Outcomes)

**Purpose:** Show how product will evolve to deliver value to users

**Contents:**
- User-facing features
- Product improvements
- New capabilities
- User experience enhancements

**Example:**
```
Q1 2024: Mobile App Launch
- Goal: Increase mobile engagement by 40%
- Key features: Native iOS/Android apps, offline mode

Q2 2024: Collaboration Features
- Goal: Increase team plan adoption by 30%
- Key features: Real-time collaboration, comments, @mentions

Q3 2024: AI-Powered Insights
- Goal: Reduce time to insights by 50%
- Key features: Auto-categorization, smart recommendations
```

### 2. Technology Roadmap (Tech Debt, Infrastructure)

**Purpose:** Show how technical foundation will improve

**Contents:**
- Infrastructure upgrades
- Technical debt reduction
- Platform improvements
- Performance optimization
- Security enhancements

**Example:**
```
Q1 2024: Database Migration
- Goal: Reduce query latency by 60%
- Work: Migrate from MySQL to PostgreSQL

Q2 2024: Microservices Architecture
- Goal: Enable independent team deployments
- Work: Break monolith into 5 services

Q3 2024: Observability Platform
- Goal: Reduce MTTR by 50%
- Work: Implement distributed tracing, centralized logging
```

### 3. Platform Roadmap (Shared Services)

**Purpose:** Show how shared platform capabilities will evolve

**Contents:**
- Shared APIs
- Common components
- Developer tools
- Platform services

**Example:**
```
Q1 2024: Authentication Platform
- Goal: Enable SSO for all products
- Services: OAuth2 server, user management API

Q2 2024: Notification Platform
- Goal: Centralize all notifications
- Services: Email, SMS, push notification service

Q3 2024: Analytics Platform
- Goal: Self-service analytics for all teams
- Services: Event pipeline, data warehouse, BI tools
```

### 4. Go-to-Market Roadmap (Launches, Marketing)

**Purpose:** Show how product will be launched and marketed

**Contents:**
- Product launches
- Marketing campaigns
- Sales enablement
- Partnership announcements

**Example:**
```
Q1 2024: Enterprise Launch
- Beta program (50 customers)
- Sales training
- Case studies

Q2 2024: Public Launch
- Press release
- Product Hunt launch
- Conference presence

Q3 2024: International Expansion
- EU market entry
- Localization (5 languages)
- Regional partnerships
```

---

## Roadmap Timeframes

### Now (Current Quarter): Committed

**Characteristics:**
- High confidence (80-90%)
- Specific deliverables
- Resources allocated
- In progress or starting soon

**Example:**
```
Now (Q1 2024):
✅ Mobile app beta (in progress)
✅ Payment integration (starting next week)
✅ Performance optimization (committed)
```

### Next (Next Quarter): Likely

**Characteristics:**
- Medium confidence (50-70%)
- Themes and goals defined
- Some details unclear
- May shift based on learnings

**Example:**
```
Next (Q2 2024):
🔄 Collaboration features (likely)
🔄 API v2 (depends on Q1 learnings)
🔄 Analytics dashboard (prioritized)
```

### Later (Beyond 2 Quarters): Exploratory

**Characteristics:**
- Low confidence (20-40%)
- Ideas and themes
- Research needed
- Will evolve significantly

**Example:**
```
Later (Q3+ 2024):
💡 AI-powered insights (exploring)
💡 Marketplace (idea stage)
💡 Mobile SDK (researching)
```

---

## Roadmap Formats

### 1. Timeline Roadmap (Gantt-Style)

**When to Use:**
- Need to show sequence
- Dependencies matter
- Stakeholders expect timelines

**Pros:**
- Clear timeline
- Shows dependencies
- Familiar format

**Cons:**
- Implies commitment to dates
- Hard to update
- Can become too detailed

**Example:**
```
Q1 2024          Q2 2024          Q3 2024
|----------------|----------------|----------------|
Mobile App       Collaboration    AI Insights
[████████████]   [████████████]   [████████████]
  API v2
  [████████]
    Performance
    [████]
```

### 2. Now-Next-Later (Flexible)

**When to Use:**
- Uncertainty is high
- Want to avoid date commitments
- Agile environment

**Pros:**
- Flexible
- No false precision
- Easy to update

**Cons:**
- No specific timelines
- Can be too vague

**Example:**
```
┌─────────────────────────────────────────────────┐
│ NOW (This Quarter)                              │
│ • Mobile app beta                               │
│ • Payment integration                           │
│ • Performance optimization                      │
├─────────────────────────────────────────────────┤
│ NEXT (Next Quarter)                             │
│ • Collaboration features                        │
│ • API v2                                        │
│ • Analytics dashboard                           │
├─────────────────────────────────────────────────┤
│ LATER (Future)                                  │
│ • AI-powered insights                           │
│ • Marketplace                                   │
│ • Mobile SDK                                    │
└─────────────────────────────────────────────────┘
```

### 3. Theme-Based (Group by Goal)

**When to Use:**
- Multiple initiatives support same goal
- Want to show strategic alignment
- Outcome-focused

**Pros:**
- Shows strategic alignment
- Groups related work
- Outcome-focused

**Cons:**
- Doesn't show timeline
- Can be abstract

**Example:**
```
Theme: Increase Mobile Engagement
├─ Mobile app (Q1)
├─ Offline mode (Q1)
├─ Push notifications (Q2)
└─ Mobile SDK (Q3)

Theme: Enable Team Collaboration
├─ Real-time editing (Q2)
├─ Comments and @mentions (Q2)
├─ Permissions (Q2)
└─ Activity feed (Q3)

Theme: Improve Performance
├─ Database migration (Q1)
├─ Caching layer (Q2)
└─ CDN integration (Q3)
```

### 4. Outcome-Based (Avoid Specific Features)

**When to Use:**
- Want to avoid feature factory
- Empower team to find solutions
- Focus on impact

**Pros:**
- Focuses on outcomes
- Flexible on solutions
- Empowers team

**Cons:**
- Can be too vague
- Stakeholders may want specifics

**Example:**
```
Q1 2024: Increase mobile engagement by 40%
- How: Mobile app, offline mode, push notifications
- Measure: DAU on mobile, session duration

Q2 2024: Increase team plan adoption by 30%
- How: Collaboration features, permissions, activity feed
- Measure: % of users on team plans, team size

Q3 2024: Reduce time to insights by 50%
- How: AI-powered categorization, smart recommendations
- Measure: Time from data upload to first insight
```

---

## Roadmap Inputs

### 1. Company Strategy and OKRs

**Questions:**
- What are company goals this year?
- What OKRs are we supporting?
- What's the strategic direction?

**Example:**
```
Company OKR: Increase revenue by 50%
→ Roadmap: Enterprise features, team plans, upsell flows

Company OKR: Expand to EU market
→ Roadmap: Localization, GDPR compliance, EU data centers
```

### 2. User Feedback and Requests

**Sources:**
- User interviews
- Support tickets
- Feature requests (ProductBoard, Canny)
- NPS surveys
- Churn interviews

**Example:**
```
Top user requests:
1. Mobile app (requested by 500 users)
2. Collaboration features (requested by 300 users)
3. API access (requested by 200 users)

→ Roadmap: Prioritize mobile app and collaboration
```

### 3. Technical Debt and Scalability

**Questions:**
- What's slowing us down?
- What will break at scale?
- What's causing incidents?

**Example:**
```
Technical debt:
- Database is slow (queries >1s)
- Monolith is hard to deploy (2 hour deploys)
- No observability (hard to debug)

→ Roadmap: Database migration, microservices, observability
```

### 4. Competitive Landscape

**Questions:**
- What are competitors building?
- What features are table stakes?
- Where can we differentiate?

**Example:**
```
Competitor analysis:
- All competitors have mobile apps (table stakes)
- Only 1 competitor has AI insights (differentiation)
- No competitor has real-time collaboration (opportunity)

→ Roadmap: Mobile app (table stakes), AI insights (differentiation)
```

### 5. Platform Capabilities

**Questions:**
- What platform services are available?
- What can we leverage vs build?
- What's missing from platform?

**Example:**
```
Platform capabilities:
- Auth platform available (can use SSO)
- No notification platform (need to build)
- Analytics platform in progress (wait for Q2)

→ Roadmap: Use auth platform, build notifications, defer analytics
```

---

## Prioritization Frameworks

### 1. RICE (Reach, Impact, Confidence, Effort)

**Formula:**
```
RICE Score = (Reach × Impact × Confidence) / Effort
```

**Reach:** How many users affected? (per quarter)
**Impact:** How much impact per user? (0.25 = minimal, 0.5 = low, 1 = medium, 2 = high, 3 = massive)
**Confidence:** How confident are we? (0-100%)
**Effort:** How much work? (person-months)

**Example:**

| Initiative | Reach | Impact | Confidence | Effort | RICE Score |
|------------|-------|--------|------------|--------|------------|
| Mobile app | 10,000 | 2 | 80% | 6 | 2,667 |
| Collaboration | 5,000 | 3 | 70% | 4 | 2,625 |
| API v2 | 2,000 | 1 | 90% | 3 | 600 |

**Decision:** Prioritize mobile app (highest RICE score)

### 2. Value vs Effort (2x2 Matrix)

**Quadrants:**
- **High Value, Low Effort:** Quick wins (do first)
- **High Value, High Effort:** Big bets (do second)
- **Low Value, Low Effort:** Fill-ins (do if time)
- **Low Value, High Effort:** Money pits (don't do)

**Example:**
```
High Value │ Big Bets        │ Quick Wins
           │ • Mobile app    │ • Push notifications
           │ • Collaboration │ • Dark mode
───────────┼─────────────────┼─────────────────
Low Value  │ Money Pits      │ Fill-ins
           │ • Custom reports│ • UI polish
           │ • Advanced admin│ • Minor features
           └─────────────────┴─────────────────
             High Effort       Low Effort
```

### 3. MoSCoW (Must, Should, Could, Won't)

**Categories:**
- **Must Have:** Critical, non-negotiable
- **Should Have:** Important, but not critical
- **Could Have:** Nice to have, if time
- **Won't Have:** Out of scope for now

**Example:**
```
Must Have (Q1):
• Mobile app beta
• Payment integration

Should Have (Q1):
• Push notifications
• Offline mode

Could Have (Q1):
• Dark mode
• Keyboard shortcuts

Won't Have (Q1):
• Collaboration features (Q2)
• AI insights (Q3)
```

### 4. Weighted Scoring

**Criteria:**
- Strategic alignment (30%)
- User impact (25%)
- Revenue potential (20%)
- Technical feasibility (15%)
- Competitive advantage (10%)

**Example:**

| Initiative | Strategic | User Impact | Revenue | Feasibility | Competitive | Total |
|------------|-----------|-------------|---------|-------------|-------------|-------|
| Mobile app | 9 (2.7) | 8 (2.0) | 7 (1.4) | 6 (0.9) | 5 (0.5) | 7.5 |
| Collaboration | 8 (2.4) | 9 (2.25) | 8 (1.6) | 7 (1.05) | 8 (0.8) | 8.1 |
| API v2 | 6 (1.8) | 5 (1.25) | 6 (1.2) | 8 (1.2) | 4 (0.4) | 5.85 |

**Decision:** Prioritize collaboration (highest weighted score)

---

## Creating a Roadmap

### Step 1: Start with Goals (What to Achieve)

**Questions:**
- What are we trying to accomplish?
- What outcomes do we want?
- How does this support company strategy?

**Example:**
```
Goal 1: Increase mobile engagement by 40%
Goal 2: Increase team plan adoption by 30%
Goal 3: Reduce infrastructure costs by 25%
```

### Step 2: Identify Themes (Groups of Work)

**Themes:** High-level categories of work

**Example:**
```
Theme 1: Mobile Experience
Theme 2: Team Collaboration
Theme 3: Platform Scalability
```

### Step 3: List Initiatives (Major Projects)

**Initiatives:** Specific projects that support themes

**Example:**
```
Theme: Mobile Experience
├─ Initiative 1: Native mobile app
├─ Initiative 2: Offline mode
└─ Initiative 3: Push notifications

Theme: Team Collaboration
├─ Initiative 1: Real-time editing
├─ Initiative 2: Comments and @mentions
└─ Initiative 3: Permissions and roles

Theme: Platform Scalability
├─ Initiative 1: Database migration
├─ Initiative 2: Microservices architecture
└─ Initiative 3: Observability platform
```

### Step 4: Estimate Effort (T-Shirt Sizes)

**Sizes:**
- **S (Small):** 1-2 weeks
- **M (Medium):** 3-4 weeks
- **L (Large):** 1-2 months
- **XL (Extra Large):** 3+ months

**Example:**
```
Mobile app: XL (4 months)
Offline mode: M (3 weeks)
Push notifications: S (1 week)
Real-time editing: L (2 months)
Comments: M (4 weeks)
Permissions: M (3 weeks)
```

### Step 5: Sequence Work (Dependencies, Capacity)

**Considerations:**
- Dependencies (what must come first?)
- Capacity (how much can we do?)
- Risk (what's most uncertain?)
- Value (what's most important?)

**Example:**
```
Q1 2024 (Capacity: 3 months):
• Mobile app (XL, 4 months) → Start in Q1, finish in Q2
• Push notifications (S, 1 week) → Quick win
• Database migration (L, 2 months) → Critical for scale

Q2 2024 (Capacity: 3 months):
• Mobile app (finish from Q1)
• Real-time editing (L, 2 months)
• Comments (M, 4 weeks)

Q3 2024 (Capacity: 3 months):
• Permissions (M, 3 weeks)
• Observability (L, 2 months)
• Microservices (XL, ongoing)
```

---

## Capacity Planning

### 1. Team Velocity (Story Points or Time)

**Measure:**
- Historical velocity (average over last 3-6 sprints)
- Story points completed per sprint
- Or: Days of work completed per sprint

**Example:**
```
Team velocity: 40 story points per 2-week sprint
Per quarter (6 sprints): 240 story points

Mobile app: 100 points
Offline mode: 20 points
Push notifications: 10 points
Database migration: 80 points

Total: 210 points (fits in Q1 capacity)
```

### 2. Available Capacity (Minus Meetings, Support, Etc.)

**Formula:**
```
Available Capacity = Total Time - (Meetings + Support + Incidents + Other)
```

**Example:**
```
Total time: 10 days per sprint (2 weeks)
Meetings: 2 days (standups, planning, retros)
Support: 1 day (bug fixes, customer issues)
Incidents: 0.5 days (on-call, firefighting)
Other: 0.5 days (hiring, admin)

Available capacity: 10 - 4 = 6 days per sprint
Per quarter: 6 days × 6 sprints = 36 days
```

### 3. Buffer for Unknowns (20-30%)

**Why:**
- Estimates are often wrong
- Unexpected work arises
- Scope creep happens

**Example:**
```
Available capacity: 36 days per quarter
Buffer (25%): 9 days
Planned capacity: 27 days

Don't plan more than 27 days of work!
```

---

## Dependencies Management

### Identify Cross-Team Dependencies

**Questions:**
- What work depends on other teams?
- What work do other teams depend on us for?
- What are the risks?

**Example:**
```
Our work: Mobile app
Depends on:
• Auth team: SSO integration (needed by week 4)
• Platform team: Push notification service (needed by week 8)
• Design team: Mobile UI designs (needed by week 2)

Risk: If auth team delays, mobile app delays
```

### Visualize Dependencies (Network Diagram)

**Example:**
```
[Mobile App] ──depends on──> [SSO Integration (Auth Team)]
     │
     └──depends on──> [Push Notifications (Platform Team)]
     │
     └──depends on──> [Mobile UI (Design Team)]

[Real-time Editing] ──depends on──> [WebSocket Service (Platform Team)]
```

### Risk of Blocked Work

**Mitigation:**
- Identify dependencies early
- Communicate with dependent teams
- Have contingency plans
- Build mocks/stubs to unblock

**Example:**
```
Risk: Auth team may not deliver SSO by week 4

Mitigation:
• Weekly check-ins with auth team
• Build against mock SSO service
• Have fallback: Email/password login
```

---

## Communicating Roadmaps

### Executive View (Outcomes, Business Impact)

**Focus:**
- Business goals
- Revenue impact
- Strategic alignment
- High-level timeline

**Example:**
```
Q1 2024: Increase Mobile Engagement by 40%
• Launch native mobile app
• Expected impact: +$500k ARR from mobile users
• Risk: Dependency on auth team

Q2 2024: Increase Team Plan Adoption by 30%
• Launch collaboration features
• Expected impact: +$300k ARR from team plans
• Risk: Technical complexity of real-time editing
```

### Team View (Specific Projects, Timelines)

**Focus:**
- Specific initiatives
- Technical details
- Timeline and milestones
- Dependencies

**Example:**
```
Q1 2024:
Week 1-2: Mobile app setup (iOS, Android)
Week 3-4: SSO integration (depends on auth team)
Week 5-8: Core features (offline, sync)
Week 9-10: Push notifications (depends on platform team)
Week 11-12: Beta testing, bug fixes

Dependencies:
• Auth team: SSO by week 4
• Platform team: Push service by week 10
```

### Customer View (Features, Benefits)

**Focus:**
- User-facing features
- Benefits and value
- Rough timeline
- How to get early access

**Example:**
```
Coming Soon:

📱 Mobile App (Q1 2024)
Access your projects on the go with our native iOS and Android apps.
• Offline mode: Work without internet
• Push notifications: Stay updated
• Beta signup: [link]

👥 Collaboration Features (Q2 2024)
Work together in real-time with your team.
• Real-time editing: See changes instantly
• Comments: Discuss within the app
• Permissions: Control who can edit
```

---

## Roadmap Tools

### ProductBoard

**Features:**
- User feedback integration
- Prioritization frameworks
- Roadmap views (timeline, now-next-later)
- Stakeholder portal

**Pricing:** $20+/user/month

### Aha!

**Features:**
- Strategy to execution
- Multiple roadmap views
- Integrations (Jira, Slack)
- Custom fields

**Pricing:** $59+/user/month

### Jira (Roadmap View)

**Features:**
- Built into Jira
- Timeline view
- Dependency tracking
- Free with Jira

**Limitations:**
- Less flexible than dedicated tools
- Focused on execution, not strategy

### Monday.com

**Features:**
- Visual roadmaps
- Timeline view
- Customizable
- Collaboration features

**Pricing:** $8+/user/month

### Miro/FigJam (Manual)

**Features:**
- Fully customizable
- Visual collaboration
- Templates available
- Free tier

**Limitations:**
- Manual updates
- No automation

---

## Roadmap Anti-Patterns

### 1. Feature Factory (No Outcome Focus)

**Problem:**
- Roadmap is just a list of features
- No connection to goals or outcomes
- Measure success by features shipped, not impact

**Example (Bad):**
```
Q1: Ship mobile app, dark mode, keyboard shortcuts
Q2: Ship collaboration, API v2, admin panel
```

**Example (Good):**
```
Q1: Increase mobile engagement by 40%
• How: Mobile app, offline mode
• Measure: DAU on mobile

Q2: Increase team plan adoption by 30%
• How: Collaboration features
• Measure: % of users on team plans
```

### 2. Too Detailed (Gantt Chart with Specific Dates)

**Problem:**
- Roadmap looks like project plan
- Specific dates create false precision
- Hard to update, becomes stale

**Example (Bad):**
```
Jan 15-29: Mobile app setup
Jan 30-Feb 12: SSO integration
Feb 13-Mar 5: Core features
Mar 6-19: Push notifications
```

**Example (Good):**
```
Q1 2024: Mobile app
• Weeks 1-4: Foundation and SSO
• Weeks 5-10: Core features
• Weeks 11-12: Beta testing
```

### 3. Ignoring Technical Debt

**Problem:**
- Only user-facing features on roadmap
- Technical debt grows
- Eventually slows down everything

**Example (Bad):**
```
Q1: Mobile app
Q2: Collaboration
Q3: AI insights
(No technical debt, infrastructure, or platform work)
```

**Example (Good):**
```
Q1: Mobile app (70%) + Database migration (30%)
Q2: Collaboration (70%) + Observability (30%)
Q3: AI insights (70%) + Microservices (30%)
```

### 4. Over-Committing (No Buffer)

**Problem:**
- Plan 100% of capacity
- No room for unknowns
- Always behind schedule

**Example (Bad):**
```
Q1 capacity: 36 days
Planned work: 36 days (100% utilization)
```

**Example (Good):**
```
Q1 capacity: 36 days
Buffer (25%): 9 days
Planned work: 27 days (75% utilization)
```

### 5. Not Reviewing/Updating (Stale Roadmap)

**Problem:**
- Create roadmap once, never update
- Roadmap becomes outdated
- Loses trust

**Example (Bad):**
```
Created roadmap in January
Never updated
In June, roadmap still shows Q1 plans
```

**Example (Good):**
```
Monthly review:
• What shipped?
• What changed?
• What's next?
• Update roadmap
```

---

## Quarterly Planning

### Step 1: Review Previous Quarter

**Questions:**
- What did we ship?
- What didn't we ship? Why?
- What did we learn?
- What surprised us?

**Example:**
```
Q4 2023 Review:
✅ Shipped: Mobile app beta, push notifications
❌ Didn't ship: Offline mode (technical complexity)
📚 Learned: SSO integration took 2x longer than expected
🎉 Surprise: Mobile app beta had 2x expected signups
```

### Step 2: Align on Goals for Next Quarter

**Questions:**
- What are company OKRs for next quarter?
- What are team goals?
- What's the strategic priority?

**Example:**
```
Company OKR: Increase revenue by 50%
Team Goal: Increase team plan adoption by 30%
Strategic Priority: Collaboration features
```

### Step 3: Prioritize Work

**Process:**
1. List all potential initiatives
2. Score using prioritization framework (RICE, Value/Effort)
3. Rank by score
4. Select top initiatives that fit capacity

**Example:**
```
Potential initiatives:
1. Collaboration features (RICE: 2,625)
2. API v2 (RICE: 600)
3. Admin panel (RICE: 400)
4. Dark mode (RICE: 200)

Capacity: 27 days
Selected:
• Collaboration features (20 days)
• API v2 (7 days)
```

### Step 4: Commit to Deliverables

**Commitment Levels:**
- **Committed:** 80-90% confidence, will ship
- **Likely:** 50-70% confidence, probably ship
- **Exploratory:** 20-40% confidence, may not ship

**Example:**
```
Q1 2024 Commitments:
✅ Committed:
• Collaboration features (real-time editing, comments)
• API v2 (core endpoints)

🔄 Likely:
• Permissions (depends on collaboration progress)

💡 Exploratory:
• Activity feed (if time permits)
```

---

## Roadmap Review and Updates

### Monthly Review (Are We On Track?)

**Agenda:**
1. Review progress (what shipped, what's in progress)
2. Identify blockers (dependencies, technical issues)
3. Adjust priorities (based on learnings)
4. Update roadmap (reflect current reality)

**Example:**
```
January Review:
✅ Shipped: Mobile app beta (on track)
🚧 In progress: Push notifications (blocked by platform team)
⚠️ Blocker: SSO integration delayed by 2 weeks
📝 Adjustment: Push offline mode to Q2, prioritize SSO

Updated roadmap:
Q1: Mobile app beta, SSO, push notifications
Q2: Offline mode, collaboration features
```

### Adjust for Learnings

**Questions:**
- What did we learn this month?
- What assumptions were wrong?
- What should we change?

**Example:**
```
Learning: Mobile app beta had 2x expected signups
Assumption: We thought mobile was nice-to-have
Reality: Mobile is critical for user engagement

Adjustment: Increase investment in mobile (add offline mode to Q1)
```

### Rebalance Priorities

**When to Rebalance:**
- New strategic priority emerges
- Major blocker arises
- Learnings invalidate assumptions
- Competitive threat

**Example:**
```
New priority: Competitor launched AI insights
Impact: Our differentiation is at risk
Action: Move AI insights from Q3 to Q2, defer admin panel
```

---

## Real Roadmap Examples (Anonymized)

### Example 1: SaaS Product Roadmap

```
┌─────────────────────────────────────────────────────────┐
│ NOW (Q1 2024)                                           │
│                                                         │
│ 📱 Mobile Experience (40% of capacity)                  │
│ • Native iOS/Android app                               │
│ • Offline mode                                         │
│ • Push notifications                                   │
│ Goal: Increase mobile DAU by 40%                       │
│                                                         │
│ 🔧 Platform Scalability (30% of capacity)               │
│ • Database migration (MySQL → PostgreSQL)              │
│ • Caching layer (Redis)                                │
│ Goal: Reduce query latency by 60%                      │
│                                                         │
│ 🐛 Technical Debt (30% of capacity)                     │
│ • Observability platform                               │
│ • Automated testing                                    │
│ Goal: Reduce MTTR by 50%                               │
├─────────────────────────────────────────────────────────┤
│ NEXT (Q2 2024)                                          │
│                                                         │
│ 👥 Team Collaboration (60% of capacity)                 │
│ • Real-time editing                                    │
│ • Comments and @mentions                               │
│ • Permissions and roles                                │
│ Goal: Increase team plan adoption by 30%               │
│                                                         │
│ 🚀 API Platform (40% of capacity)                       │
│ • API v2 (REST + GraphQL)                              │
│ • Developer portal                                     │
│ Goal: Enable 100 API integrations                      │
├─────────────────────────────────────────────────────────┤
│ LATER (Q3+ 2024)                                        │
│                                                         │
│ 🤖 AI-Powered Insights                                  │
│ • Auto-categorization                                  │
│ • Smart recommendations                                │
│ • Predictive analytics                                 │
│                                                         │
│ 🌍 International Expansion                              │
│ • Localization (5 languages)                           │
│ • EU data centers                                      │
│ • GDPR compliance                                      │
└─────────────────────────────────────────────────────────┘
```

### Example 2: Platform Engineering Roadmap

```
Q1 2024: Foundation
├─ Authentication Platform
│  • OAuth2 server
│  • User management API
│  • SSO for all products
│  Goal: Enable single sign-on across all products
│
├─ Observability Platform
│  • Distributed tracing (Jaeger)
│  • Centralized logging (ELK)
│  • Metrics (Prometheus + Grafana)
│  Goal: Reduce MTTR by 50%
│
└─ CI/CD Pipeline
   • GitHub Actions
   • Automated testing
   • Deployment automation
   Goal: Reduce deployment time from 2h to 15min

Q2 2024: Scale
├─ Notification Platform
│  • Email service
│  • SMS service
│  • Push notification service
│  Goal: Centralize all notifications
│
├─ Data Platform
│  • Event pipeline (Kafka)
│  • Data warehouse (Snowflake)
│  • BI tools (Looker)
│  Goal: Self-service analytics for all teams
│
└─ Microservices Architecture
   • Break monolith into 5 services
   • Service mesh (Istio)
   • API gateway
   Goal: Enable independent team deployments

Q3 2024: Optimize
├─ Developer Experience
│  • Local development environment
│  • Testing frameworks
│  • Documentation
│  Goal: Reduce onboarding time from 2 weeks to 3 days
│
└─ Cost Optimization
   • Right-size infrastructure
   • Reserved instances
   • Auto-scaling
   Goal: Reduce infrastructure costs by 30%
```

---

## Templates

### Template 1: Now-Next-Later

```markdown
# Product Roadmap

## NOW (This Quarter)
**Theme:** [Theme name]
**Goal:** [Measurable outcome]

### Initiatives
- [ ] [Initiative 1] (Size: L, Owner: [Name])
- [ ] [Initiative 2] (Size: M, Owner: [Name])
- [ ] [Initiative 3] (Size: S, Owner: [Name])

**Success Metrics:**
- [Metric 1]: [Target]
- [Metric 2]: [Target]

## NEXT (Next Quarter)
**Theme:** [Theme name]
**Goal:** [Measurable outcome]

### Initiatives
- [ ] [Initiative 1] (Size: XL, Owner: [Name])
- [ ] [Initiative 2] (Size: M, Owner: [Name])

**Success Metrics:**
- [Metric 1]: [Target]
- [Metric 2]: [Target]

## LATER (Future)
**Ideas to Explore:**
- [Idea 1]
- [Idea 2]
- [Idea 3]
```

### Template 2: Theme-Based

```markdown
# Roadmap by Theme

## Theme 1: [Theme Name]
**Goal:** [Measurable outcome]
**Timeline:** Q1-Q2 2024

### Initiatives
| Initiative | Quarter | Size | Owner | Status |
|------------|---------|------|-------|--------|
| [Initiative 1] | Q1 | L | [Name] | In Progress |
| [Initiative 2] | Q1 | M | [Name] | Not Started |
| [Initiative 3] | Q2 | XL | [Name] | Planned |

**Dependencies:**
- [Dependency 1]
- [Dependency 2]

**Success Metrics:**
- [Metric 1]: [Baseline] → [Target]
- [Metric 2]: [Baseline] → [Target]

## Theme 2: [Theme Name]
[Repeat structure]
```

### Template 3: Timeline Roadmap

```markdown
# Timeline Roadmap

## Q1 2024 (Jan-Mar)
**Capacity:** 27 days (after 25% buffer)

| Initiative | Size | Weeks | Dependencies | Owner |
|------------|------|-------|--------------|-------|
| [Initiative 1] | L | 1-8 | None | [Name] |
| [Initiative 2] | M | 3-6 | [Team X] | [Name] |
| [Initiative 3] | S | 9-10 | [Initiative 1] | [Name] |

**Goals:**
- [Goal 1]: [Target]
- [Goal 2]: [Target]

## Q2 2024 (Apr-Jun)
[Repeat structure]

## Q3 2024 (Jul-Sep)
[Repeat structure]
```

---

## Summary

### Quick Reference

**Roadmap Types:**
- Product: Features and outcomes
- Technology: Tech debt and infrastructure
- Platform: Shared services
- Go-to-market: Launches and marketing

**Timeframes:**
- Now (current quarter): Committed (80-90% confidence)
- Next (next quarter): Likely (50-70% confidence)
- Later (beyond 2 quarters): Exploratory (20-40% confidence)

**Formats:**
- Timeline: Shows sequence and dependencies
- Now-Next-Later: Flexible, no dates
- Theme-based: Groups by goal
- Outcome-based: Focuses on impact

**Prioritization:**
- RICE: (Reach × Impact × Confidence) / Effort
- Value vs Effort: 2x2 matrix
- MoSCoW: Must, Should, Could, Won't
- Weighted scoring: Multiple criteria

**Creating Roadmap:**
1. Start with goals
2. Identify themes
3. List initiatives
4. Estimate effort (S, M, L, XL)
5. Sequence work

**Capacity Planning:**
- Team velocity (historical average)
- Available capacity (minus meetings, support)
- Buffer for unknowns (20-30%)

**Communication:**
- Executive: Outcomes, business impact
- Team: Specific projects, timelines
- Customer: Features, benefits

**Anti-Patterns:**
- Feature factory (no outcomes)
- Too detailed (specific dates)
- Ignoring technical debt
- Over-committing (no buffer)
- Not reviewing/updating

**Tools:**
- ProductBoard, Aha! (dedicated)
- Jira (built-in)
- Monday.com (visual)
- Miro/FigJam (manual)
