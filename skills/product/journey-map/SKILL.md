---
name: journey-map
description: Create user journey maps and customer journey maps (dual mode)
---

# Journey Map Skill

Map user experiences and customer lifecycles. Use two modes: User-focused (touchpoints, emotions, pain points) and Business-focused (full lifecycle, revenue metrics, cross-functional).

## When to Use This Skill

**User Journey Mapping:**
- Understanding how users experience your product
- Identifying friction points in user flows
- Designing better onboarding or core experiences
- Aligning team around user perspective

**Customer Journey Mapping:**
- Planning go-to-market strategy
- Optimizing sales and success processes
- Understanding full customer lifecycle (awareness → retention)
- Cross-functional alignment (marketing, sales, product, support)

## Two Modes

### Mode 1: User Journey Map
**Focus:** How users interact with your product
**Scope:** Single feature or product experience
**Audience:** Product, design, engineering teams
**Duration:** Covers minutes to weeks

### Mode 2: Customer Journey Map
**Focus:** How customers move through business relationship
**Scope:** Full lifecycle from awareness to advocacy
**Audience:** GTM teams (marketing, sales, CS) + product
**Duration:** Covers months to years

## Workflow

### Step 1: Choose Mode

Ask the PM:
```
Which type of journey map do you need?

1. **User Journey Map**
   - Maps: Product experience (onboarding, key workflow, feature usage)
   - Focus: Touchpoints, emotions, pain points, opportunities
   - Example: "User onboarding journey" or "Checkout flow journey"

2. **Customer Journey Map**
   - Maps: Full business relationship (awareness → expansion)
   - Focus: Lifecycle stages, revenue metrics, cross-functional handoffs
   - Example: "Enterprise customer journey" or "Self-serve PLG journey"

Your choice: [1 or 2]
```

---

## MODE 1: User Journey Map

### Step 2A: Define Journey Scope

```
Journey Name: [e.g., "New user onboarding"]

User Persona: [Who is this journey for?]
- [Persona name/type]
- [Key characteristics]
- [Goals/motivations]

Journey Goal: [What is the user trying to accomplish?]
- [Primary goal]

Time Span: [How long does this journey take?]
- [Minutes/Hours/Days/Weeks]

Entry Point: [Where does journey start?]
- [Starting point]

Exit Point: [Where does journey end?]
- [Ending point - success state]
```

### Step 3A: Map Journey Phases

Break journey into 3-7 phases:

```
## Journey Phases

1. **[Phase 1 Name]** (e.g., "Awareness")
   - Duration: [Time in this phase]
   - User goal: [What they're trying to do]

2. **[Phase 2 Name]** (e.g., "Signup")
   - Duration: [Time in this phase]
   - User goal: [What they're trying to do]

3. **[Phase 3 Name]** (e.g., "First Use")
   - Duration: [Time in this phase]
   - User goal: [What they're trying to do]

[Continue for all phases...]
```

### Step 4A: Detail Each Phase

For each phase, document:

```
### Phase: [Phase Name]

#### Touchpoints
[Every interaction user has with product]
- [Touchpoint 1: e.g., "Landing page"]
- [Touchpoint 2: e.g., "Signup form"]
- [Touchpoint 3: e.g., "Email confirmation"]

#### User Actions
[What user does]
- [Action 1: e.g., "Clicks 'Sign Up'"]
- [Action 2: e.g., "Enters email and password"]
- [Action 3: e.g., "Checks email for confirmation"]

#### User Thoughts
[What they're thinking]
- "[Thought 1: e.g., 'Is this worth my time?']"
- "[Thought 2: e.g., 'Will this be complicated?']"

#### Emotions
[How they feel - use emoji + description]
- 😐 Neutral: [Description]
- 😟 Frustrated: [Description]
- 😊 Satisfied: [Description]

#### Pain Points
🔴 [Critical pain]: [Description]
🟡 [Moderate pain]: [Description]
🟢 [Minor annoyance]: [Description]

#### Opportunities
💡 [Improvement 1]: [What we could do better]
💡 [Improvement 2]: [What we could do better]

#### Metrics
- [Metric 1: e.g., "Conversion rate: 45%"]
- [Metric 2: e.g., "Time to complete: 3.2 minutes"]
```

### Output Format (User Journey Map)

```markdown
# User Journey Map: [Journey Name]

**Persona:** [User type]
**Goal:** [What they want to accomplish]
**Duration:** [Time span]

---

## Journey Overview

[Entry Point] → [Phase 1] → [Phase 2] → [Phase 3] → ... → [Success State]

---

## Phase 1: [Phase Name]

**Duration:** [Time] | **Goal:** [User objective]

| Element | Details |
|---------|---------|
| **Touchpoints** | [List touchpoints] |
| **Actions** | [User actions] |
| **Thoughts** | [What they think] |
| **Emotions** | 😐 Neutral → 😟 Frustrated |
| **Pains** | 🔴 [Critical pain]<br>🟡 [Moderate pain] |
| **Opportunities** | 💡 [Improvement 1]<br>💡 [Improvement 2] |
| **Metrics** | [Key metrics for this phase] |

---

[Repeat for each phase]

---

## Summary

### Biggest Pain Points
1. 🔴 [Critical pain 1] - In [Phase X]
2. 🔴 [Critical pain 2] - In [Phase Y]
3. 🟡 [Moderate pain 3] - In [Phase Z]

### Top Opportunities
1. 💡 [Opportunity 1] - Would improve [metric/experience]
2. 💡 [Opportunity 2] - Would improve [metric/experience]
3. 💡 [Opportunity 3] - Would improve [metric/experience]

### Emotional Journey
```
😊 Excited → 😐 Neutral → 😟 Frustrated → 🤔 Confused → 😊 Satisfied
[Phase 1]    [Phase 2]    [Phase 3]      [Phase 4]     [Phase 5]
```

### Next Steps
- [ ] [Action 1: e.g., "Simplify signup form"]
- [ ] [Action 2: e.g., "Add progress indicator to onboarding"]
- [ ] [Action 3: e.g., "Reduce time to first value"]
```

---

## MODE 2: Customer Journey Map

### Step 2B: Define Customer Lifecycle

```
Customer Type: [e.g., "Enterprise B2B customer"]
- [Segment details]
- [Typical company size/industry]

Journey Scope: [Full lifecycle or specific segment?]
- [E.g., "Awareness through first renewal"]

Business Model: [How do customers buy/use product?]
- [Sales-led / Product-led / Hybrid]
- [Contract length: Monthly/Annual/Multi-year]

Revenue Model: [How do we make money?]
- [Subscription / Usage-based / Hybrid]
```

### Step 3B: Map Lifecycle Stages

Typical B2B SaaS stages:

```
## Lifecycle Stages

1. **Awareness** (Pre-customer)
   - How they discover us

2. **Consideration** (Pre-customer)
   - Evaluating alternatives

3. **Purchase** (Conversion)
   - Becoming a customer

4. **Onboarding** (Early customer)
   - Getting set up

5. **Adoption** (Active customer)
   - Using product regularly

6. **Expansion** (Growth)
   - Upgrading, adding seats/features

7. **Renewal** (Retention)
   - Staying vs churning

8. **Advocacy** (Champion)
   - Referring others, case studies
```

### Step 4B: Detail Each Stage

For each stage, document:

```
### Stage: [Stage Name]

#### Timeframe
[How long customers typically spend in this stage]
- Average: [X days/weeks/months]

#### Customer Goals
[What customer wants to achieve]
- [Goal 1]
- [Goal 2]

#### Company Goals
[What we want to achieve]
- [Goal 1: e.g., "Convert 30% to paid"]
- [Goal 2: e.g., "Time to value < 7 days"]

#### Key Touchpoints
[Every interaction customer has with company]
- [Touchpoint 1: e.g., "Website visit"]
- [Touchpoint 2: e.g., "Sales demo"]
- [Touchpoint 3: e.g., "Email nurture sequence"]

#### Responsible Teams
[Who owns this stage]
- Primary: [Team name]
- Supporting: [Other teams]

#### Key Activities
[What happens in this stage]
- [Activity 1]
- [Activity 2]
- [Activity 3]

#### Pain Points
🔴 [Critical friction]: [Description]
🟡 [Moderate friction]: [Description]

#### Success Metrics
- [Metric 1: e.g., "Trial-to-paid conversion: 25%"]
- [Metric 2: e.g., "Time to first value: 5 days"]

#### Revenue Impact
- MRR/ARR contribution: [$ or %]
- Conversion rate: [%]
- Churn risk: [High/Med/Low]
```

### Step 5B: Map Cross-Functional Handoffs

Identify where responsibility transfers:

```
## Key Handoffs

**Marketing → Sales**
- Trigger: [When leads are qualified]
- Handoff process: [How it happens]
- Common issues: [What breaks]

**Sales → Customer Success**
- Trigger: [When deal closes]
- Handoff process: [How it happens]
- Common issues: [What breaks]

**Customer Success → Product**
- Trigger: [When customer is self-sufficient]
- Handoff process: [How it happens]
- Common issues: [What breaks]
```

### Output Format (Customer Journey Map)

```markdown
# Customer Journey Map: [Customer Type]

**Segment:** [Customer segment]
**Business Model:** [Sales-led/Product-led/Hybrid]
**Journey Duration:** [Typical customer lifecycle length]

---

## Lifecycle Overview

```
Awareness → Consideration → Purchase → Onboarding → Adoption → Expansion → Renewal → Advocacy
[Marketing]   [Marketing]    [Sales]     [CS]        [CS/Product] [Sales/CS]  [CS]       [Marketing]
```

---

## Stage 1: [Stage Name]

**Timeframe:** [Duration] | **Owner:** [Primary team]

| Element | Details |
|---------|---------|
| **Customer Goals** | [What customer wants] |
| **Company Goals** | [What we want] |
| **Touchpoints** | [List all interactions] |
| **Key Activities** | [What happens] |
| **Pain Points** | 🔴 [Critical]<br>🟡 [Moderate] |
| **Metrics** | [Success metrics] |
| **Revenue Impact** | [MRR/ARR contribution] |

**Handoff to next stage:** [How/when transition happens]

---

[Repeat for each stage]

---

## Summary

### Conversion Funnel
```
Stage           | Volume | Conversion | Time
----------------|--------|------------|------
Awareness       | 10,000 | -          | -
Consideration   | 1,000  | 10%        | 2 weeks
Purchase        | 200    | 20%        | 1 week
Onboarding      | 200    | 100%       | 2 weeks
Adoption        | 150    | 75%        | 1 month
Expansion       | 60     | 40%        | 6 months
Renewal         | 180    | 90%        | 12 months
Advocacy        | 30     | 17%        | 18+ months
```

### Critical Pain Points by Stage
1. **[Stage]:** 🔴 [Pain] - Causes [X% drop-off]
2. **[Stage]:** 🔴 [Pain] - Adds [X days to cycle]
3. **[Stage]:** 🟡 [Pain] - Reduces [satisfaction score]

### Revenue Optimization Opportunities
1. **[Opportunity 1]** - Could improve [metric] by [X%]
   - Stage impacted: [Stage]
   - Investment: [Low/Med/High]
   - Expected impact: [Revenue/retention gain]

2. **[Opportunity 2]** - Could improve [metric] by [X%]
   - Stage impacted: [Stage]
   - Investment: [Low/Med/High]
   - Expected impact: [Revenue/retention gain]

### Cross-Functional Issues
- **[Handoff 1]:** [Problem and impact]
- **[Handoff 2]:** [Problem and impact]

### Next Steps
- [ ] [Action 1: Owned by [Team]]
- [ ] [Action 2: Owned by [Team]]
- [ ] [Action 3: Owned by [Team]]
```

---

## Visual Representation Tips

Journey maps are often visual. If creating slides/diagrams:

**User Journey Map Visual:**
```
Phase 1      Phase 2       Phase 3       Phase 4
────────────────────────────────────────────────
Actions:     [Icons/steps in each phase]
Emotions:    😊 → 😐 → 😟 → 😊 (line graph)
Touchpoints: [Product screens, emails, etc.]
Pains:       🔴🟡 markers at friction points
Ideas:       💡 markers for opportunities
```

**Customer Journey Map Visual:**
```
Timeline: [Months 1-12+]
Stages:   Awareness → Consideration → Purchase → ...
Teams:    Marketing → Sales → CS → Product
Metrics:  [Conversion rates between stages]
Revenue:  [MRR/ARR progression over time]
```

## Pro Tips

1. **Use real data:** Don't guess - use analytics, interviews, support tickets
2. **Emotion matters:** The feeling is as important as the function
3. **Quantify pain:** "45% of users drop off here" > "users get stuck"
4. **One persona at a time:** Different users = different journeys
5. **Update regularly:** Journeys change as product evolves
6. **Workshop format:** Best created collaboratively with cross-functional team
7. **Prioritize ruthlessly:** Can't fix everything - focus on biggest impact

## Common Mistakes to Avoid

❌ Too many phases (10+ is overwhelming)
✅ 3-7 phases that map to real stages

❌ Company perspective only (what we want)
✅ Customer perspective first (what they experience)

❌ Happy path only (ignoring failures)
✅ Include drop-offs, errors, frustrations

❌ No metrics (purely qualitative)
✅ Quantify: conversion rates, time, sentiment scores

❌ One-time exercise (never referenced again)
✅ Living document, updated quarterly

## Integration with Other Skills

**Feeds into:**
- `/prd-draft` - Inform feature specs with journey insights
- `/write-prod-strategy` - User/customer understanding in strategy
- `/activation-analysis` - Setup → Aha → Habit maps to journey phases
- `/retention-analysis` - Journey reveals retention drivers

**Requires:**
- User research (interviews, surveys)
- Analytics data (funnel metrics, behavior)
- Support data (common issues, friction points)

## Questions to Ask Before Starting

1. **Scope:** Single feature flow or full customer lifecycle?
2. **Persona:** Which user/customer type are we mapping?
3. **Data sources:** What research/analytics inform this map?
4. **Audience:** Who will use this journey map?
5. **Decisions:** What product/business decisions will this inform?

Remember: Journey maps are tools for empathy and alignment. A good journey map makes the team feel what the customer feels - and act on it.

---

## Context Routing Strategy

When the PM uses `/journey-map`, I automatically:

### 1. Pull User Research for Personas & Pain Points
**Source:** `context-library/research/`, user research MCPs (Dovetail, UserTesting)
- **What I look for:** User personas, quotes, pain points, behavior patterns
- **How I use it:** Pre-populate persona sections with real research data
- **Example:** Auto-pull quotes from interviews: "I always get stuck at the checkout step"

### 2. Extract Relevant Metrics & Analytics
**Source:** Amplitude, Mixpanel, Posthog (if connected), `context-library/metrics/`
- **What I look for:** Conversion rates, drop-off points, time-in-flow metrics
- **How I use it:** Quantify pain points with actual data
- **Example:** "Phase 3 has a 45% drop-off rate (vs 12% in Phase 2)"

### 3. Align With Strategy & OKRs
**Source:** `context-library/strategy/`, PRDs
- **What I look for:** Current strategic focus, activation goals, retention goals
- **How I use it:** Suggest which journey phases matter most for strategy
- **Example:** "Since we're focused on retention, let's emphasize the habit-formation phase"

### 4. Cross-Reference Customer Lifecycle
**Source:** Sales/CS data, past customer journey maps in `context-library/`
- **What I look for:** Typical customer progression, expansion patterns
- **How I use it:** Build customer journey map that aligns with business model
- **Example:** For PLG model, include activation → expansion → advocacy phases

### 5. Identify Cross-Functional Stakeholders
**Source:** `context-library/stakeholder-template.md`
- **What I look for:** Who owns different journey phases (sales, product, CS, success)
- **How I use it:** Suggest who to involve in journey mapping workshop
- **Example:** "Phase 3 (onboarding) involves Product + CS, should workshop together"

### 6. Route for Action
**Routing logic:**
- **User journey map:** Feeds into `/prd-draft` and design decisions
- **Customer journey map:** Feeds into GTM strategy and `/write-prod-strategy`
- **Activation journey:** Maps to `/activation-analysis` framework
- **Retention journey:** Maps to `/retention-analysis` cohorts

---

## Output Quality Self-Check

Before presenting output to the PM, verify:

- [ ] **File saved to correct location:** Output saved to `outputs/journey-maps/[journey-name]-[date].md`
- [ ] **Context routing table was checked:** Reviewed `context-library/research/` for user research, interview transcripts, and persona data before building the map
- [ ] **Every stage has all four elements:** Each journey phase includes actions, thoughts, emotions, and pain points (no empty or missing sections)
- [ ] **User quotes from research included:** Where available, real user quotes from `context-library/research/` are embedded in relevant journey stages (not fabricated quotes)
- [ ] **Opportunities linked to specific product improvements:** Each opportunity names a concrete product change (e.g., "add progress bar to onboarding step 3"), not generic advice like "improve the experience"
- [ ] **Emotional journey shows highs and lows:** The emotional arc across stages is not flat; it includes at least one high point and one low point with explanations for the shifts
