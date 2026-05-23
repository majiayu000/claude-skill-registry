---
name: spec-driven-brainstorming
description: Spec-driven brainstorming and product discovery expert. Helps teams ideate features, break down epics, conduct story mapping sessions, prioritize using MoSCoW/RICE/Kano, and validate ideas with lean startup methods. Activates for brainstorming, product discovery, story mapping, feature ideation, prioritization, MoSCoW, RICE, Kano model, lean startup, MVP definition, product backlog, feature breakdown.
---

# Spec-Driven Brainstorming Skill

Expert in product discovery, feature ideation, and spec-driven brainstorming techniques. Helps teams move from vague ideas to concrete, well-defined specifications using structured facilitation methods.

## Core Facilitation Techniques

### 1. Story Mapping (User Story Mapping)

**Purpose**: Visualize user journey and identify features that deliver value at each step.

**Process**:

```
Step 1: Define User Activities (horizontal backbone)
┌──────────────┬──────────────┬──────────────┬──────────────┐
│ Discover     │ Browse       │ Purchase     │ Receive      │
│ Products     │ & Compare    │ & Checkout   │ & Review     │
└──────────────┴──────────────┴──────────────┴──────────────┘

Step 2: Break down into User Tasks (vertical slices)
Discover Products:
├─ Search by keyword
├─ Filter by category
├─ View trending products
└─ Get personalized recommendations

Browse & Compare:
├─ View product details
├─ Read reviews
├─ Compare products side-by-side
└─ Save to wishlist

Purchase & Checkout:
├─ Add to cart
├─ Apply discount code
├─ Select shipping method
└─ Enter payment info

Step 3: Prioritize by Walking Skeleton (MVP = top row)
┌────────────────────────────────────────────────────────┐
│ MVP (Release 1): Walking Skeleton                      │
├────────────────────────────────────────────────────────┤
│ Search → View Details → Add to Cart → Checkout        │
└────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────┐
│ Release 2: Enhanced Discovery                          │
├────────────────────────────────────────────────────────┤
│ Filters, Trending, Recommendations, Reviews            │
└────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────┐
│ Release 3: Advanced Features                           │
├────────────────────────────────────────────────────────┤
│ Wishlist, Compare, Discount Codes, Saved Payments     │
└────────────────────────────────────────────────────────┘
```

**Output**: Prioritized backlog aligned with user journey.

### 2. Event Storming

**Purpose**: Discover domain events and business processes through collaborative modeling.

**Process**:

```markdown
## Event Storming Workflow

### Step 1: Identify Domain Events (orange sticky notes)
- OrderPlaced
- PaymentProcessed
- OrderShipped
- OrderDelivered
- OrderCancelled

### Step 2: Identify Commands (blue sticky notes)
- PlaceOrder
- ProcessPayment
- ShipOrder
- CancelOrder

### Step 3: Identify Aggregates (yellow sticky notes)
- Order (handles PlaceOrder, CancelOrder)
- Payment (handles ProcessPayment)
- Shipment (handles ShipOrder)

### Step 4: Identify External Systems (pink sticky notes)
- PaymentGateway (Stripe)
- ShippingProvider (FedEx API)
- InventorySystem

### Step 5: Identify Policies (purple sticky notes)
- WHEN OrderPlaced THEN ProcessPayment
- WHEN PaymentProcessed THEN ReserveInventory
- WHEN InventoryReserved THEN ShipOrder
- WHEN OrderCancelled AND PaymentProcessed THEN RefundPayment
```

**Output**: Visual map of business processes and bounded contexts.

### 3. Impact Mapping

**Purpose**: Connect business goals to features through user impact.

```
GOAL: Increase revenue by 20% in Q2

WHY? (Impact)
├─ Increase conversion rate (5% → 8%)
│  ├─ WHO? (Actors)
│  │  ├─ New visitors
│  │  └─ Returning customers
│  ├─ HOW? (Features)
│  │  ├─ Simplify checkout (1-click purchase)
│  │  ├─ Add product recommendations
│  │  └─ Offer guest checkout
│  └─ WHAT? (Deliverables)
│     ├─ US-001: 1-click checkout for logged-in users
│     ├─ US-002: ML-based product recommendations
│     └─ US-003: Guest checkout flow
│
├─ Increase average order value ($50 → $65)
│  ├─ WHO? (Actors)
│  │  └─ Existing customers
│  ├─ HOW? (Features)
│  │  ├─ Bundle discounts (buy 3, get 10% off)
│  │  ├─ Free shipping threshold ($75+)
│  │  └─ Upsell related products
│  └─ WHAT? (Deliverables)
│     ├─ US-004: Bundle discount engine
│     ├─ US-005: Dynamic shipping calculator
│     └─ US-006: Related product suggestions
│
└─ Reduce cart abandonment (40% → 25%)
   ├─ WHO? (Actors)
   │  └─ Users with items in cart
   ├─ HOW? (Features)
   │  ├─ Cart abandonment emails
   │  ├─ Save cart across devices
   │  └─ Show trust signals (reviews, secure badges)
   └─ WHAT? (Deliverables)
      ├─ US-007: Automated cart recovery emails
      ├─ US-008: Persistent cart sync
      └─ US-009: Trust badge UI components
```

**Output**: Features directly linked to business outcomes.

## Prioritization Frameworks

### 1. MoSCoW Method

**Definition**: Categorize features into Must, Should, Could, Won't.

```markdown
## Feature Prioritization: E-commerce Platform MVP

### MUST Have (Critical for Launch)
- [ ] User registration & login
- [ ] Product catalog with search
- [ ] Shopping cart
- [ ] Checkout with payment processing
- [ ] Order confirmation email

**Rationale**: Core transactional flow, no sales without these.

### SHOULD Have (Important but not critical)
- [ ] Product reviews and ratings
- [ ] Wishlist/Save for Later
- [ ] Order history
- [ ] Basic analytics dashboard (admin)

**Rationale**: Enhance UX and trust, but MVP can ship without.

### COULD Have (Nice to have if time allows)
- [ ] Product recommendations
- [ ] Social login (Google, Facebook)
- [ ] Advanced filtering (price range, brand)
- [ ] Guest checkout

**Rationale**: Competitive features, but not required for MVP.

### WON'T Have (Explicitly deferred)
- [ ] Mobile app (web-first)
- [ ] Multi-currency support
- [ ] Subscription billing
- [ ] Loyalty program

**Rationale**: Future roadmap items, not needed for initial market validation.
```

**Best For**: MVP scope definition, time-boxed releases.

### 2. RICE Score (Reach, Impact, Confidence, Effort)

**Formula**: `RICE Score = (Reach × Impact × Confidence) / Effort`

```markdown
## RICE Scoring Example

### Feature A: 1-Click Checkout
- **Reach**: 5000 users/month will use this
- **Impact**: High (3/3) - significantly reduces friction
- **Confidence**: 80% (have data from competitor analysis)
- **Effort**: 4 person-weeks

**RICE Score** = (5000 × 3 × 0.8) / 4 = **3000**

### Feature B: Product Recommendations
- **Reach**: 8000 users/month will see recommendations
- **Impact**: Medium (2/3) - incremental revenue lift
- **Confidence**: 50% (no A/B test data yet)
- **Effort**: 8 person-weeks

**RICE Score** = (8000 × 2 × 0.5) / 8 = **1000**

### Feature C: Guest Checkout
- **Reach**: 2000 users/month (30% of visitors)
- **Impact**: High (3/3) - reduces abandonment significantly
- **Confidence**: 90% (industry benchmarks strong)
- **Effort**: 2 person-weeks

**RICE Score** = (2000 × 3 × 0.9) / 2 = **2700**

### Priority Order
1. **1-Click Checkout** (RICE: 3000)
2. **Guest Checkout** (RICE: 2700)
3. **Product Recommendations** (RICE: 1000)
```

**Best For**: Data-driven prioritization, roadmap planning.

### 3. Kano Model

**Categories**:
- **Basic Needs (Must-be)**: Absence causes dissatisfaction, presence doesn't delight
- **Performance Needs (One-dimensional)**: More is better (linear satisfaction)
- **Excitement Needs (Delighters)**: Absence doesn't hurt, presence delights

```markdown
## Kano Analysis: Email Client

### Basic Needs (Hygiene Factors)
- Send and receive email (expected, must work flawlessly)
- Attachment support (expected)
- Spam filtering (expected)

**Action**: Must implement, but won't differentiate product.

### Performance Needs (Satisfiers)
- Search speed (faster = better satisfaction)
- Storage quota (more = better satisfaction)
- Mobile app performance

**Action**: Invest proportionally based on competitive benchmarks.

### Excitement Needs (Delighters)
- AI-powered email summarization (unexpected, delights users)
- Smart reply suggestions
- Scheduled send with timezone awareness
- Undo send (5-second window)

**Action**: Focus on 1-2 delighters for differentiation.

### Indifferent Features (Low Priority)
- Custom email signatures (users don't care much)
- Theme customization (low impact)

**Action**: Deprioritize or skip.

### Reverse Features (Causes Dissatisfaction)
- Intrusive ads in inbox (annoys users)
- Forced social features (users resist)

**Action**: Avoid completely.
```

**Best For**: Understanding customer satisfaction drivers, differentiation strategy.

## Lean Startup Validation

### 1. Build-Measure-Learn Loop

```markdown
## Hypothesis Testing: Feature X

### BUILD
**Hypothesis**: Adding product recommendations will increase average order value by 15%.

**Minimum Viable Test**:
- Implement simple "Customers also bought" section
- Show on 50% of product pages (A/B test)
- Track: clicks, add-to-cart rate, order value

**Effort**: 1 week (backend + frontend)

### MEASURE
**Metrics to Track**:
- Click-through rate on recommendations
- Add-to-cart conversion from recommendations
- Average order value (treatment vs control)
- Revenue per visitor

**Success Criteria**:
- CTR > 5%
- AOV increase > 10%
- Statistical significance (p < 0.05)

**Data Collection Period**: 2 weeks (minimum 10,000 visitors)

### LEARN
**Scenario A: Hypothesis Validated**
- AOV increased 18% (exceeded target!)
- CTR on recommendations: 12%
- **Action**: Roll out to 100%, invest in ML-based recommendations

**Scenario B: Hypothesis Rejected**
- AOV increased 2% (below target)
- CTR on recommendations: 1% (low engagement)
- **Action**: Pivot - test alternative hypothesis (e.g., bundle discounts)

**Scenario C: Mixed Results**
- AOV increased 12% (close to target)
- High CTR but low conversion
- **Action**: Iterate - improve recommendation quality (ML model)
```

### 2. MVP Definition Canvas

```markdown
## MVP Canvas: Task Management SaaS

### Target Users
- Solo freelancers and small teams (2-5 people)
- Knowledge workers (designers, developers, writers)
- Currently using: Spreadsheets, Trello, Notion

### Problem Being Solved
- Task prioritization is manual and time-consuming
- No visibility into blockers and dependencies
- Team collaboration requires constant status updates

### Unique Value Proposition
Auto-prioritized task list using AI + team workload balancing.

### MVP Features (Walking Skeleton)
**Core Flow**: Create task → AI prioritizes → Assign → Complete

**Must-Have Features**:
- [ ] Task creation (title, description, due date)
- [ ] AI prioritization (urgency + importance algorithm)
- [ ] Task assignment to team members
- [ ] Task status updates (To Do, In Progress, Done)
- [ ] Team dashboard (workload overview)

**NOT in MVP**:
- ❌ Time tracking
- ❌ Custom workflows
- ❌ Integrations (Slack, GitHub)
- ❌ Mobile app
- ❌ Advanced reporting

### Success Metrics
- **Activation**: 70% of signups create 3+ tasks in first week
- **Retention**: 40% weekly active users (WAU) after 4 weeks
- **Engagement**: Average 5 tasks completed/week per user

### Risks & Assumptions
- **Assumption**: Users trust AI prioritization
  - **Test**: Survey 50 users after 2 weeks, ask "Do you trust the priority scores?"
- **Risk**: AI prioritization is inaccurate
  - **Mitigation**: Manual override, feedback loop to improve model
- **Assumption**: Teams of 2-5 are willing to pay $10/user/month
  - **Test**: Offer paid tier after 2-week trial, track conversion rate
```

## Brainstorming Techniques

### 1. Crazy 8s (Rapid Ideation)

**Process**: 8 sketches in 8 minutes (1 minute per idea).

```markdown
## Crazy 8s Session: Improve Checkout Flow

### Ideas Generated (8 minutes)
1. **1-Click Purchase** - Saved payment + address, single button
2. **Progressive Disclosure** - Multi-step wizard (cart → shipping → payment)
3. **Guest Checkout** - No account required, email-only
4. **Cart Abandonment Recovery** - Email + discount code
5. **Payment Link Sharing** - Send checkout link to someone else (gift)
6. **Buy Now Pay Later** - Installment payments (Klarna integration)
7. **Voice Checkout** - "Alexa, complete my order"
8. **AR Try-On** - Virtual fitting room before checkout

### Voting (Dot Voting)
- 1-Click Purchase: ●●●●● (5 votes)
- Guest Checkout: ●●●● (4 votes)
- BNPL Integration: ●●● (3 votes)
- Progressive Disclosure: ●● (2 votes)

### Top 3 for Deeper Exploration
1. 1-Click Purchase (quick win, high impact)
2. Guest Checkout (reduce friction)
3. BNPL Integration (competitive parity)
```

### 2. Six Thinking Hats (De Bono)

**Purpose**: Explore ideas from different perspectives.

```markdown
## Six Hats Analysis: Feature X (AI-Powered Email Summarization)

### White Hat (Facts & Data)
- Average email length: 200 words
- Users spend 3 minutes reading complex emails
- 40% of emails are > 500 words
- Competitor Y launched similar feature (20% adoption)

### Red Hat (Emotions & Intuition)
- "This feels like a gimmick, I don't trust AI to summarize important emails"
- "Love this! Saves time on long threads"
- "Worried about missing critical details in summary"

### Yellow Hat (Optimism & Benefits)
- Saves 2 minutes per long email → 20 min/day for heavy users
- Reduces cognitive load, improves focus
- Differentiator from competitors (if done well)
- Could upsell as premium feature

### Black Hat (Risks & Caution)
- AI hallucination risk (incorrect summaries)
- Privacy concerns (email content processed by AI)
- High development cost (NLP model training)
- May annoy users who prefer full context

### Green Hat (Creativity & Alternatives)
- Alternative 1: Highlight key sentences (instead of summary)
- Alternative 2: TL;DR generated by sender (not AI)
- Alternative 3: Voice-to-summary (read email aloud, generate summary)

### Blue Hat (Process & Conclusion)
**Decision**: Proceed with MVP (limited rollout)
- Build: Highlight key sentences (lower risk than full summary)
- Test: 10% of users, measure engagement + feedback
- Iterate: If successful, invest in full AI summarization
```

### 3. How Might We (HMW) Questions

**Purpose**: Reframe problems as opportunities.

```markdown
## Problem Statement
Users abandon checkout because the form is too long (12 fields).

### HMW Questions
- **HMW reduce the number of required fields?**
  - Idea: Use address autocomplete (Google Places API)
  - Idea: Prefill from previous orders
- **HMW make the form feel shorter?**
  - Idea: Multi-step wizard (psychological chunking)
  - Idea: Progress bar showing "80% complete"
- **HMW eliminate the form entirely?**
  - Idea: 1-click checkout for returning users
  - Idea: Voice input for address/payment
- **HMW make filling the form more enjoyable?**
  - Idea: Gamify with rewards (10 points per field completed)
  - Idea: Show real-time savings ("You've saved $15 so far!")
- **HMW help users trust the checkout process?**
  - Idea: Show trust badges (SSL, money-back guarantee)
  - Idea: Live chat support during checkout
```

## Feature Breakdown Templates

### Epic → Features → User Stories

```markdown
## Epic: User Onboarding Experience

### Feature 1: Account Creation
**User Story US-001**: Email/Password Registration
- **As a** new user
- **I want to** create an account with email/password
- **So that** I can access personalized features

**Acceptance Criteria**:
- Email validation (RFC 5322 format)
- Password complexity (8+ chars, 1 uppercase, 1 number, 1 special)
- Duplicate email detection
- Verification email sent within 5 minutes

**User Story US-002**: Social Login (Google, GitHub)
- **As a** new user
- **I want to** sign up with my Google/GitHub account
- **So that** I don't have to remember another password

**Acceptance Criteria**:
- OAuth 2.0 integration
- Consent screen shown
- Email auto-verified for social logins

### Feature 2: Profile Setup
**User Story US-003**: Basic Profile Information
- **As a** new user
- **I want to** set my display name and avatar
- **So that** other users can recognize me

**User Story US-004**: Preferences Configuration
- **As a** new user
- **I want to** configure notification preferences
- **So that** I only receive relevant updates

### Feature 3: Guided Tour
**User Story US-005**: Interactive Product Tour
- **As a** first-time user
- **I want** a guided tour of key features
- **So that** I understand how to use the product

**User Story US-006**: Sample Data Pre-population
- **As a** new user
- **I want** sample data to explore
- **So that** I can try features without manual setup
```

## Collaborative Workshop Formats

### 1. Remote Brainstorming (Miro/FigJam)

**Agenda** (90 minutes):
```
00:00 - 00:10  Introduction & Problem Statement
00:10 - 00:25  Individual Ideation (silent brainstorming)
00:25 - 00:45  Group Sharing (2 min per person)
00:45 - 01:00  Affinity Grouping (cluster similar ideas)
01:00 - 01:15  Dot Voting (3 votes per person)
01:15 - 01:30  Discussion & Action Items
```

**Tools**:
- Miro Board with templates
- Timer for timeboxing
- Anonymous voting

### 2. Design Sprint (5-Day Format)

```
Day 1: Map (Understand the problem)
- User journey mapping
- Identify pain points
- Set sprint goal

Day 2: Sketch (Diverge - generate ideas)
- Crazy 8s
- Solution sketches
- Silent critique

Day 3: Decide (Converge - choose solution)
- Dot voting
- Storyboard creation
- Prototype plan

Day 4: Prototype (Build realistic facade)
- High-fidelity mockup
- Interactive prototype (Figma)
- Test script preparation

Day 5: Test (Validate with users)
- 5 user interviews
- Record findings
- Decide: build, iterate, or pivot
```

## Output Templates

### Brainstorming Session Summary

```markdown
# Brainstorming Session: [Topic]

**Date**: 2024-01-15
**Participants**: Alice (PM), Bob (Eng), Carol (Design)
**Facilitator**: Alice

## Problem Statement
Users are abandoning checkout at 40% rate (industry avg: 25%).

## Ideas Generated (22 total)

### High Priority (Top 5 by voting)
1. **1-Click Checkout** (8 votes)
   - Rationale: Removes friction for returning users
   - Effort: 2 weeks
   - Impact: Est. 10% reduction in abandonment

2. **Guest Checkout** (7 votes)
   - Rationale: 30% of users don't want accounts
   - Effort: 1 week
   - Impact: Est. 8% reduction in abandonment

3. **Progress Indicator** (6 votes)
   - Rationale: Reduces anxiety about form length
   - Effort: 2 days
   - Impact: Est. 3% reduction in abandonment

4. **Autofill Address** (5 votes)
   - Rationale: Saves time, reduces errors
   - Effort: 1 week (Google Places API)
   - Impact: Est. 5% reduction in abandonment

5. **Save Cart for Later** (4 votes)
   - Rationale: Users can return without starting over
   - Effort: 3 days
   - Impact: Est. 4% recovery of abandoned carts

### Medium Priority (Parking Lot)
- Buy Now Pay Later integration
- Live chat support during checkout
- Trust badges (SSL, money-back guarantee)

### Deferred (Low ROI or High Risk)
- Voice checkout (too experimental)
- AR try-on (out of scope)

## Action Items
- [ ] Alice: Create specs for Top 3 (1-Click, Guest, Progress)
- [ ] Bob: Technical feasibility assessment (3 days)
- [ ] Carol: Mockups for guest checkout flow (5 days)
- [ ] Team: Review specs on Friday standup

## Next Session
- Date: 2024-01-22
- Topic: Refine top 3 ideas into user stories
```

## Best Practices

### 1. Timebox Everything
- Ideation: 10-15 minutes max
- Discussion: 5 minutes per idea
- Voting: 2 minutes

### 2. Diverge Before Converging
- Generate quantity first (no criticism)
- Evaluate quality later (structured voting)

### 3. Make It Visual
- Sketches > Text
- Whiteboards > Documents
- Prototypes > Specs

### 4. Include Diverse Perspectives
- Engineering (feasibility)
- Design (usability)
- Product (business value)
- Support (user pain points)

### 5. Document Decisions
- Why did we choose X over Y?
- What assumptions are we making?
- What will we measure?

## Resources

- [User Story Mapping - Jeff Patton](https://www.jpattonassociates.com/user-story-mapping/)
- [Impact Mapping - Gojko Adzic](https://www.impactmapping.org/)
- [Design Sprint - Google Ventures](https://www.gv.com/sprint/)
- [Kano Model Analysis](https://en.wikipedia.org/wiki/Kano_model)

## Activation Keywords

Ask me about:
- "How to run a brainstorming session"
- "Story mapping for product discovery"
- "Prioritization frameworks (MoSCoW, RICE, Kano)"
- "How to break down epics into user stories"
- "Lean startup validation techniques"
- "MVP definition and scoping"
- "Feature prioritization methods"
- "Design sprint facilitation"
- "Impact mapping for product roadmaps"
