---
name: pm-knowledge-base
description: Product Management frameworks, methodologies, and best practices library. Provides PM knowledge including prioritization (RICE, MoSCoW), goal setting (OKR, SMART), customer research (JTBD, Personas), and product strategy. Use when needing PM methodology guidance or framework application.
allowed-tools: Read
model: inherit
---

# PM Knowledge Base - Product Management Frameworks & Methodologies

This Skill provides comprehensive Product Management knowledge, frameworks, and best practices to support PM decision-making and execution.

## When to Use This Skill

Activate this Skill when you need:
- Prioritization frameworks (RICE, MoSCoW, Kano Model, Value vs Effort)
- Goal-setting methodologies (OKR, SMART, North Star Metric)
- Customer research approaches (Jobs-to-be-Done, Persona creation, User interviews)
- Product strategy frameworks (Blue Ocean, Positioning, Go-to-Market)
- Roadmap planning and communication
- Metrics and analytics guidance

## Core PM Frameworks

### 1. Prioritization Frameworks

#### RICE Score
**Formula:** `(Reach × Impact × Confidence) / Effort`

**Components:**
- **Reach**: How many users/customers affected per time period
  - Example: 1000 users per quarter
- **Impact**: How much impact per user (scale)
  - 3 = Massive impact
  - 2 = High impact
  - 1 = Medium impact
  - 0.5 = Low impact
  - 0.25 = Minimal impact
- **Confidence**: How confident in estimates
  - 100% = High confidence
  - 80% = Medium confidence
  - 50% = Low confidence
- **Effort**: Person-months required
  - Example: 0.5 person-months

**Example:**
```
Feature: Social Login
- Reach: 1000 users/quarter
- Impact: 2 (high)
- Confidence: 80%
- Effort: 0.5 person-months

RICE Score = (1000 × 2 × 0.8) / 0.5 = 3200
```

Higher RICE score = Higher priority

#### MoSCoW Method
Categorize features into four buckets:

- **Must Have (P0)**: Critical for release, blocking
  - Without this, the release fails
  - Legal/regulatory requirements
  - Core value proposition

- **Should Have (P1)**: Important but not critical
  - Significant impact but workarounds exist
  - Can be delayed if necessary

- **Could Have (P2)**: Nice to have if time permits
  - Small impact
  - Easy to implement
  - Low risk

- **Won't Have (P3)**: Out of scope for this release
  - Explicitly documented
  - May reconsider for future releases

#### Value vs Effort Matrix

```
High Value, Low Effort → Quick Wins (Do First)
High Value, High Effort → Big Bets (Do Second)
Low Value, Low Effort → Fill-ins (Do Third)
Low Value, High Effort → Time Sinks (Don't Do)
```

**Application:**
1. Plot all features on 2x2 matrix
2. Focus resources on Quick Wins
3. Select 1-2 Big Bets per quarter
4. Use Fill-ins to balance workload
5. Avoid Time Sinks entirely

#### Kano Model
Categorize features by customer satisfaction impact:

- **Basic Needs**: Expected features (absence causes dissatisfaction)
  - Example: Product search, checkout

- **Performance Needs**: More is better (linear satisfaction)
  - Example: Page load speed, feature completeness

- **Delight Needs**: Unexpected features (presence causes joy)
  - Example: Personalized recommendations, Easter eggs

**Strategy:**
- Ensure all Basic Needs are met
- Compete on key Performance Needs
- Differentiate with Delight Needs

---

### 2. Goal-Setting Frameworks

#### OKR (Objectives and Key Results)

**Structure:**
```
Objective: Qualitative, inspiring, time-bound goal

Key Result 1: Measurable outcome (metric + target)
Key Result 2: Measurable outcome (metric + target)
Key Result 3: Measurable outcome (metric + target)
```

**Best Practices:**
- 3-5 Objectives per quarter
- 3-5 Key Results per Objective
- 70% achievable = good OKR
- Review weekly, grade quarterly (0-1 scale)

**Example:**
```
Objective: Become the go-to platform for small business productivity

Key Result 1: Increase MAU from 100K to 200K
Key Result 2: Improve Day 30 retention from 20% to 30%
Key Result 3: Achieve NPS of 50+
Key Result 4: Launch in 3 new markets
```

#### SMART Goals

- **S**pecific: Clear and unambiguous
- **M**easurable: Quantifiable
- **A**chievable: Realistic
- **R**elevant: Aligned with strategy
- **T**ime-bound: Has a deadline

**Example:**
❌ Bad: "Improve user engagement"
✅ Good: "Increase DAU from 10K to 15K by end of Q2"

#### North Star Metric

**Definition:** Single metric that best captures core value delivered

**Criteria:**
- Reflects customer value
- Measures product success
- Predicts revenue
- Easy to understand
- Actionable by team

**Examples:**
- Airbnb: Nights Booked
- Facebook: Daily Active Users
- Slack: Messages Sent
- Netflix: Hours Watched
- Spotify: Time Listening

**Supporting Metrics:**
- Input Metrics: Actions that drive North Star
- Output Metrics: Results of those actions
- Guardrail Metrics: Prevent gaming the system

---

### 3. Customer Research Frameworks

#### Jobs-to-be-Done (JTBD)

**Framework:**
```
When I [situation],
I want to [motivation],
So I can [expected outcome].
```

**Example:**
```
When I'm working on multiple projects,
I want to organize my tasks automatically,
So I can focus on important work without feeling overwhelmed.
```

**Application:**
1. Identify the "job" customers hire your product for
2. Understand context/situation (when)
3. Define desired progress (outcome)
4. Find competing solutions (alternatives)
5. Design product around the job, not demographics

**Interview Questions:**
- "Tell me about the last time you [did this task]"
- "What were you trying to accomplish?"
- "What did you use? What didn't work?"
- "What would your ideal solution look like?"

#### Persona Creation

**Persona Template:**
```
Name: [Persona Name]

Demographics:
- Age: [Range]
- Location: [Where]
- Job Title: [Role]
- Income: [Range]
- Education: [Level]

Goals:
- Primary goal: [What they want to achieve]
- Secondary goals: [Additional objectives]

Pain Points:
- Pain 1: [Frustration, problem]
- Pain 2: [Challenge, obstacle]
- Pain 3: [Need, gap]

Behaviors:
- Shopping habits: [How they buy]
- Media consumption: [Where they spend time]
- Technology proficiency: [Skill level]

Motivations:
- [What drives them]
- [What they value]

Quote:
"[In their words, what matters most]"
```

**Types of Personas:**
- **Primary Persona**: Main target user (design for them)
- **Secondary Persona**: Additional user types (accommodate)
- **Anti-Persona**: Who you're NOT building for (explicitly exclude)

#### Customer Interview Best Practices

**Before Interview:**
- [ ] Define research questions
- [ ] Create interview script
- [ ] Recruit right participants (6-10 for patterns)
- [ ] Prepare recording setup

**During Interview:**
- Ask open-ended questions
- Listen more than talk (80/20 rule)
- Dig deeper with "Why?" (5 Whys technique)
- Observe behavior, not just words
- Stay neutral, don't lead

**After Interview:**
- Transcribe and tag key quotes
- Identify patterns across interviews
- Synthesize insights
- Share findings with team

**Good Questions:**
✅ "Walk me through the last time you [did task]"
✅ "What frustrated you about that experience?"
✅ "How did you work around that problem?"

**Bad Questions:**
❌ "Would you use a feature that does X?" (Hypothetical)
❌ "Do you like our product?" (Leading, not actionable)
❌ "What features do you want?" (Users don't know)

---

### 4. Product Strategy Frameworks

#### Blue Ocean Strategy

**Core Concept:** Create uncontested market space instead of competing in "red oceans"

**Four Actions Framework:**
1. **Eliminate**: Which factors can be removed?
2. **Reduce**: Which factors should be reduced below industry standard?
3. **Raise**: Which factors should be raised above industry standard?
4. **Create**: Which factors should be created that industry never offered?

**Example: Cirque du Soleil**
- Eliminated: Animals, star performers, multiple rings
- Reduced: Humor, thrill/danger
- Raised: Artistic music/dance, unique venues
- Created: Theme, refined environment

#### Positioning Statement

**Template:**
```
For [target customer]
Who [statement of need or opportunity],
[Product name] is a [product category]
That [key benefit, reason to buy].
Unlike [primary competitive alternative],
[Product name] [statement of primary differentiation].
```

**Example:**
```
For busy professionals
Who need to stay productive across multiple projects,
TaskMaster is a smart task management app
That automatically organizes and prioritizes your work.
Unlike Todoist or Asana,
TaskMaster uses AI to learn your patterns and suggest optimal schedules.
```

#### Go-to-Market (GTM) Strategy

**Key Components:**

1. **Target Market:**
   - TAM/SAM/SOM
   - Beachhead market (initial focus)
   - Expansion plan

2. **Value Proposition:**
   - Core benefit
   - Differentiation
   - Proof points

3. **Pricing Strategy:**
   - Pricing model (subscription, freemium, usage-based)
   - Price points
   - Competitive positioning

4. **Distribution Channels:**
   - Direct vs indirect
   - Online vs offline
   - Partnerships

5. **Marketing Mix:**
   - Content marketing
   - SEO/SEM
   - Social media
   - PR and influencers
   - Events and community

6. **Sales Approach:**
   - Self-serve vs sales-assisted
   - Trial strategy
   - Onboarding plan

7. **Success Metrics:**
   - Acquisition: CAC, conversion rates
   - Activation: onboarding completion
   - Engagement: DAU/MAU
   - Retention: churn rate
   - Revenue: LTV, MRR

---

### 5. Roadmap Planning

#### Roadmap Types

**Now-Next-Later Roadmap:**
```
Now (Current Quarter):
- Feature A
- Feature B

Next (Next 1-2 Quarters):
- Feature C
- Feature D

Later (Future, 6+ months):
- Feature E
- Feature F
```

Benefits: Flexible, acknowledges uncertainty

**Theme-Based Roadmap:**
```
Q1 2024: User Onboarding
Q2 2024: Power User Features
Q3 2024: Mobile Experience
Q4 2024: Enterprise Capabilities
```

Benefits: Focuses on outcomes, not outputs

**Feature-Based Roadmap:**
```
Q1: Social Login, Profile Customization
Q2: Advanced Search, Filters
Q3: Mobile App (iOS), Push Notifications
Q4: Analytics Dashboard, Export Tools
```

Benefits: Clear deliverables, easy to communicate

#### Roadmap Communication

**For Executives:**
- Strategic themes
- Business impact
- Revenue opportunities
- Competitive positioning

**For Sales:**
- Customer-facing features
- Competitive advantages
- Timeline (quarters, not dates)
- Caveats about changes

**For Engineering:**
- Technical dependencies
- Architecture decisions
- Resource requirements
- Risk mitigation

**For Customers:**
- Value and benefits
- Use cases
- General timeframes (not promises)
- How to provide feedback

---

### 6. Metrics and Analytics

#### AARRR (Pirate Metrics)

**Acquisition:** Users discovering product
- Website visitors
- Sign-ups
- App downloads
- CAC (Customer Acquisition Cost)

**Activation:** Users having great first experience
- Onboarding completion rate
- Time to first value
- Aha moment achievement

**Retention:** Users coming back
- Day 1, 7, 30 retention
- DAU/MAU ratio
- Churn rate

**Revenue:** Monetization
- MRR/ARR
- ARPU
- LTV
- Conversion rate (free → paid)

**Referral:** Users telling others
- NPS
- Viral coefficient
- Referral rate

#### Key Product Metrics

**Engagement:**
- DAU (Daily Active Users)
- MAU (Monthly Active Users)
- DAU/MAU Ratio (Stickiness): Target 20%+
- Session length
- Session frequency

**Growth:**
- MoM (Month-over-Month) growth: Target 20%+ for startups
- Activation rate: Target 40%+ consumer, 60%+ B2B
- Viral coefficient (K-factor): >1 = viral growth

**Business:**
- MRR (Monthly Recurring Revenue)
- ARR (Annual Recurring Revenue)
- LTV (Lifetime Value)
- CAC (Customer Acquisition Cost)
- LTV/CAC Ratio: Target 3:1 or higher
- Payback Period: Target <12 months
- Gross Margin

**Satisfaction:**
- NPS (Net Promoter Score): 0-30 good, 30-70 great, 70+ excellent
- CSAT (Customer Satisfaction): Target 80%+
- CES (Customer Effort Score): Lower is better

---

## How to Apply These Frameworks

### For Idea Validation
1. Use JTBD to understand customer needs
2. Create personas for target users
3. Conduct customer interviews
4. Apply Blue Ocean strategy for differentiation

### For Prioritization
1. List all potential features
2. Calculate RICE scores
3. Apply MoSCoW categorization
4. Plot on Value vs Effort matrix
5. Validate with customer feedback

### For Goal Setting
1. Define North Star Metric
2. Set quarterly OKRs
3. Ensure goals are SMART
4. Align team around objectives

### For Roadmap Planning
1. Group features by theme
2. Prioritize using RICE/MoSCoW
3. Consider dependencies
4. Use Now-Next-Later for flexibility
5. Communicate with stakeholders

### For Metrics Tracking
1. Map product to AARRR funnel
2. Identify key metrics for each stage
3. Set targets based on benchmarks
4. Build dashboards for monitoring
5. Review weekly, adjust monthly

---

## Quick Reference

### Prioritization Quick Decision Tree
```
Is it critical for launch? → Yes → Must Have (P0)
                         → No ↓

Does it have high RICE score (>100)? → Yes → Should Have (P1)
                                    → No ↓

Is it quick win (high value, low effort)? → Yes → Could Have (P2)
                                          → No → Won't Have (P3)
```

### Metric Selection Guide
```
Early stage (0-1): Focus on Activation, Retention
Growth stage (1-10): Focus on Acquisition, Retention
Scale stage (10-100): Focus on Revenue, Referral
```

### Interview Question Templates
```
Opening: "Tell me about yourself and your role"
Context: "Walk me through the last time you [did task]"
Problem: "What challenges did you face?"
Solution: "How did you solve it? What didn't work?"
Ideal: "What would your ideal experience look like?"
Closing: "Is there anything else you'd like to share?"
```

---

## Usage Instructions

When this Skill is activated, use the frameworks above to:

1. **Analyze situations** using appropriate framework
2. **Provide structured guidance** based on PM best practices
3. **Reference specific methodologies** with examples
4. **Recommend approaches** suited to the context
5. **Cite frameworks** to establish credibility

**Example Usage:**
- User asks: "How should I prioritize these 10 features?"
- Response: Apply RICE scoring framework, then validate with MoSCoW method
- Provide step-by-step calculation example
- Recommend final prioritization with rationale

---

This knowledge base should be used as a reference to inform PM decisions with proven frameworks and industry best practices.
