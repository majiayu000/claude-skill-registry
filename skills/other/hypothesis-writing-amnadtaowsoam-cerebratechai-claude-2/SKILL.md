---
name: Hypothesis Writing
description: Comprehensive guide to writing testable product hypotheses that drive learning and prevent building the wrong things
---

# Hypothesis Writing

## What is a Product Hypothesis?

A **product hypothesis** is a testable statement about user behavior and business outcomes.

### Structure
```
If [action/change],
then [outcome],
because [reasoning/belief].
```

### Example
> "If we add social login, then 30% more users will complete signup within 2 weeks, because password creation is a major friction point."

### Why It's Not Just a Feature Idea

**Feature Idea (Bad):**
> "We should add social login."

**Hypothesis (Good):**
> "If we add social login, then signup completion will increase by 30%, because users abandon the flow when creating passwords."

**Difference:**
- Feature idea = What to build
- Hypothesis = Why it will work + How to measure success

---

## Why Hypotheses Matter

### 1. Forces Clarity Before Building

**Without Hypothesis:**
> "Let's build a chatbot because everyone has one."

**With Hypothesis:**
> "If we add a chatbot to answer common questions, then support ticket volume will decrease by 20% within 1 month, because 60% of tickets are repetitive questions."

**Benefit:** Forces you to think through the "why" and "how much."

### 2. Makes Assumptions Explicit

**Hidden Assumptions:**
- Users want this feature
- Users will find it
- Users will use it correctly
- It will have the desired impact

**Hypothesis Makes Them Visible:**
> "We assume users abandon signup because password creation is too hard."

**Now you can test this assumption!**

### 3. Enables Learning (Confirm or Invalidate)

**Hypothesis Confirmed:**
> "Social login increased signup by 35% ✅ Ship it!"

**Hypothesis Invalidated:**
> "Social login only increased signup by 5% ❌ Our assumption was wrong. What else causes abandonment?"

**Key:** Invalidation is learning, not failure.

### 4. Prevents "Build Trap"

**Build Trap:**
- Build features without validation
- Measure success by features shipped (not outcomes)
- Never learn what actually works

**Hypothesis-Driven:**
- Test before building
- Measure outcomes (not outputs)
- Learn and iterate

---

## Hypothesis Structure (AARRR Framework)

### Template

```
If we [change/feature]
For [target users]
We will see [measurable outcome]
Because [underlying belief]
We'll measure success with [metric]
```

### Example 1: Acquisition

```
If we add a referral program
For existing active users
We will see 20% more signups from referrals
Because users want to share products they love with friends
We'll measure success with referral signups / total signups
```

### Example 2: Activation

```
If we add an interactive onboarding tutorial
For new users in their first session
We will see 40% more users complete their first project
Because users don't understand how to get started
We'll measure success with % of users who complete first project within 24 hours
```

### Example 3: Retention

```
If we send weekly digest emails
For users who haven't logged in for 7 days
We will see 15% more users return within 14 days
Because users forget about the product without reminders
We'll measure success with 7-day retention rate
```

### Example 4: Revenue

```
If we add annual billing with 20% discount
For monthly subscribers
We will see 30% of monthly users upgrade to annual
Because users want to save money and prefer fewer transactions
We'll measure success with % of monthly users who convert to annual
```

### Example 5: Referral

```
If we add social sharing buttons on project completion
For users who finish a project
We will see 10% more social shares
Because users are proud of their work and want to show it off
We'll measure success with shares per completed project
```

---

## Good Hypothesis Characteristics

### 1. Specific (Not Vague)

**Bad (Vague):**
> "If we improve the UI, users will be happier."

**Good (Specific):**
> "If we reduce the checkout flow from 5 steps to 3 steps, cart abandonment will decrease by 15%."

### 2. Measurable (Quantifiable Outcome)

**Bad (Not Measurable):**
> "Users will like the new design."

**Good (Measurable):**
> "NPS score will increase from 30 to 45 within 1 month."

### 3. Falsifiable (Can Be Proven Wrong)

**Bad (Not Falsifiable):**
> "The new feature will be useful."

**Good (Falsifiable):**
> "30% of users will use the new feature at least once per week."

**Why:** If you can't prove it wrong, you can't learn from it.

### 4. Time-Bound (Test Duration)

**Bad (No Time Frame):**
> "Conversion rate will increase."

**Good (Time-Bound):**
> "Conversion rate will increase by 10% within 2 weeks of launch."

### 5. Focused (One Variable at a Time)

**Bad (Multiple Variables):**
> "If we redesign the homepage, add social proof, and change the CTA button, conversion will increase."

**Good (Single Variable):**
> "If we add customer testimonials to the homepage, conversion will increase by 8%."

**Why:** Can't tell which change caused the effect.

---

## Hypothesis Types

### 1. Value Hypothesis: Will Users Find This Valuable?

**Question:** Do users actually want this?

**Example:**
> "If we add dark mode, 40% of users will enable it within 1 week, because users prefer dark interfaces at night."

**Test Methods:**
- User interviews
- Surveys
- Landing page test (measure signups)
- Prototype testing

### 2. Usability Hypothesis: Can Users Use This Easily?

**Question:** Can users figure out how to use this?

**Example:**
> "If we add tooltips to the dashboard, new users will complete setup 25% faster, because they currently get stuck on configuration."

**Test Methods:**
- Usability testing
- Prototype testing
- Time-to-task completion
- Error rates

### 3. Feasibility Hypothesis: Can We Build This Technically?

**Question:** Is this technically possible within constraints?

**Example:**
> "We can build real-time collaboration in 6 weeks with our current tech stack, because we already have WebSocket infrastructure."

**Test Methods:**
- Technical spike
- Proof of concept
- Architecture review

### 4. Viability Hypothesis: Is This Sustainable for Business?

**Question:** Will this make/save money?

**Example:**
> "If we add a premium tier at $49/month, 10% of free users will upgrade, generating $50k MRR, because power users need advanced features."

**Test Methods:**
- Pricing surveys
- Willingness to pay studies
- Competitor analysis
- Unit economics

---

## Example Hypotheses

### Example 1: Social Login

```
If we add social login (Google, Facebook)
For new users during signup
We will see 30% more users complete signup within 2 weeks
Because password creation is a major friction point (60% abandon at this step)
We'll measure success with signup completion rate
```

**Assumptions:**
- Users abandon because of password friction (not other reasons)
- Users trust social login
- Users have Google/Facebook accounts

### Example 2: Product Recommendations

```
If we show personalized product recommendations on the cart page
For users with items in their cart
We will see average order value increase by 15% within 1 month
Because users discover complementary products they didn't know about
We'll measure success with average order value (AOV)
```

**Assumptions:**
- Users are open to buying more
- Recommendations are relevant
- Users see recommendations before checkout

### Example 3: Onboarding Checklist

```
If we add an onboarding checklist with 5 key tasks
For new users in their first week
We will see 40% more users reach "activated" status (complete 3+ tasks)
Because users don't know what to do first and get overwhelmed
We'll measure success with activation rate (% completing 3+ tasks in week 1)
```

**Assumptions:**
- Users want guidance
- 5 tasks is the right number (not too many/few)
- Tasks are the right ones

### Example 4: Email Reminders

```
If we send email reminders 24 hours before subscription renewal
For paying customers
We will see churn decrease by 10% within 1 month
Because users forget about renewal and are surprised by charges
We'll measure success with monthly churn rate
```

**Assumptions:**
- Surprise charges cause churn
- Email is the right channel
- 24 hours is the right timing

### Example 5: Free Trial Extension

```
If we extend free trial from 7 days to 14 days
For new trial users
We will see trial-to-paid conversion increase by 20%
Because users need more time to experience value
We'll measure success with trial conversion rate
```

**Assumptions:**
- Time is the constraint (not value)
- 14 days is enough (not too long)
- Doesn't hurt revenue (longer trial = delayed revenue)

---

## Identifying Assumptions

### What Must Be True?

For each hypothesis, ask: **"What must be true for this to work?"**

**Example Hypothesis:**
> "If we add live chat, support satisfaction will increase by 20%."

**Assumptions:**
1. Users want live chat (not email/phone)
2. We can staff live chat adequately
3. Response time is fast enough
4. Agents can solve problems in chat
5. Users will find the chat widget
6. Chat is better than current support channels

### Riskiest Assumptions (Test First)

**Prioritize testing assumptions that are:**
1. **Most uncertain** (we have least evidence)
2. **Most critical** (if wrong, hypothesis fails)
3. **Hardest to reverse** (expensive to undo)

**Example:**
- Riskiest: "Users want live chat" → Test with user interviews
- Less risky: "We can staff it" → Internal feasibility check

### Knowns vs Unknowns

**Knowns (Data/Evidence):**
- Current support satisfaction: 65%
- Average response time: 4 hours
- Support ticket volume: 500/month

**Unknowns (Assumptions):**
- Do users prefer chat over email?
- Will chat reduce ticket volume?
- Can we maintain quality in chat?

**Action:** Test unknowns before building.

---

## Hypothesis Prioritization

### ICE Score Framework

**Formula:**
```
ICE Score = Impact × Confidence × Ease
```

**Impact (1-10):** How big is the expected outcome?
- 10 = Game-changing (2x revenue)
- 5 = Meaningful (20% improvement)
- 1 = Marginal (2% improvement)

**Confidence (1-10):** How likely is this to work?
- 10 = Very confident (strong evidence)
- 5 = Moderate confidence (some evidence)
- 1 = Low confidence (pure guess)

**Ease (1-10):** How easy is it to test?
- 10 = Very easy (1 day, no eng)
- 5 = Moderate (1 week, some eng)
- 1 = Very hard (1 month, major eng)

### Example Scoring

| Hypothesis | Impact | Confidence | Ease | ICE Score | Priority |
|------------|--------|------------|------|-----------|----------|
| Social login | 8 | 7 | 6 | 336 | 1 |
| Dark mode | 4 | 8 | 9 | 288 | 2 |
| Live chat | 7 | 5 | 3 | 105 | 3 |
| Mobile app | 9 | 6 | 1 | 54 | 4 |

**Decision:** Test social login first (highest ICE score).

### RICE Score (Alternative)

**Formula:**
```
RICE Score = (Reach × Impact × Confidence) / Effort
```

**Reach:** How many users affected?
**Impact:** How much impact per user?
**Confidence:** How confident are we?
**Effort:** How much work required?

---

## Hypothesis Validation Methods

### 1. User Interviews

**Use For:** Problem validation, solution validation

**Example:**
> "We believe users abandon signup due to password friction."

**Interview Questions:**
- "Tell me about the last time you signed up for a new service."
- "What parts were frustrating?"
- "Have you ever abandoned a signup? Why?"

**Evidence:**
- 8 out of 10 users mentioned password frustration
- 5 users said they'd prefer social login

### 2. Surveys

**Use For:** Quantify demand, measure satisfaction

**Example:**
> "We believe 30% of users would use dark mode."

**Survey Question:**
- "Would you use dark mode if available?"
  - [ ] Yes, definitely
  - [ ] Maybe
  - [ ] No

**Evidence:**
- 45% said "Yes, definitely" → Hypothesis supported

### 3. A/B Tests

**Use For:** Measure actual behavior change

**Example:**
> "Social login will increase signup by 30%."

**Test:**
- Control: Email/password signup
- Treatment: Social login option

**Evidence:**
- Treatment: 35% signup rate
- Control: 25% signup rate
- Lift: 40% → Hypothesis validated ✅

### 4. MVPs (Minimum Viable Products)

**Use For:** Test full solution with real users

**Example:**
> "Users will pay $49/month for premium features."

**MVP:**
- Build basic premium tier
- Offer to 100 users
- Measure conversion

**Evidence:**
- 12 out of 100 upgraded (12%)
- Target was 10% → Hypothesis validated ✅

### 5. Prototypes

**Use For:** Test usability before building

**Example:**
> "Users can complete onboarding in 5 minutes."

**Prototype:**
- Figma clickable prototype
- 10 user tests

**Evidence:**
- Average completion: 7 minutes
- Target was 5 minutes → Hypothesis invalidated ❌
- Learning: Simplify step 3 (users got stuck)

### 6. Analytics

**Use For:** Validate with existing data

**Example:**
> "60% of users abandon at password creation step."

**Analytics:**
- Check funnel drop-off rates
- Segment by device, source

**Evidence:**
- 58% drop-off at password step → Hypothesis supported

---

## Hypothesis Canvas

### Template

```
┌─────────────────────────────────────────────────────────┐
│ HYPOTHESIS CANVAS                                       │
├─────────────────────────────────────────────────────────┤
│ Problem Statement:                                      │
│ [What problem are we solving?]                          │
│                                                         │
│ Target Users:                                           │
│ [Who has this problem?]                                 │
│                                                         │
│ Proposed Solution:                                      │
│ [What are we building/changing?]                        │
│                                                         │
│ Expected Outcome:                                       │
│ [What will happen? By how much?]                        │
│                                                         │
│ Success Metrics:                                        │
│ [How will we measure success?]                          │
│                                                         │
│ Test Method:                                            │
│ [How will we validate this?]                            │
│                                                         │
│ Assumptions:                                            │
│ [What must be true for this to work?]                   │
│                                                         │
│ Riskiest Assumption:                                    │
│ [What's the biggest unknown?]                           │
└─────────────────────────────────────────────────────────┘
```

### Example: Social Login

```
┌─────────────────────────────────────────────────────────┐
│ HYPOTHESIS CANVAS: Social Login                        │
├─────────────────────────────────────────────────────────┤
│ Problem Statement:                                      │
│ 60% of users abandon signup at password creation step   │
│                                                         │
│ Target Users:                                           │
│ New users signing up for free trial                     │
│                                                         │
│ Proposed Solution:                                      │
│ Add Google and Facebook social login options            │
│                                                         │
│ Expected Outcome:                                       │
│ Signup completion rate increases from 25% to 35%        │
│ (40% relative improvement) within 2 weeks               │
│                                                         │
│ Success Metrics:                                        │
│ - Signup completion rate                                │
│ - % using social login vs email/password                │
│ - Time to complete signup                               │
│                                                         │
│ Test Method:                                            │
│ A/B test: 50% see social login, 50% see only email      │
│ Run for 2 weeks, need 10,000 visitors                   │
│                                                         │
│ Assumptions:                                            │
│ 1. Password friction is the main abandonment cause      │
│ 2. Users trust social login                             │
│ 3. Users have Google/Facebook accounts                  │
│ 4. Social login is technically feasible                 │
│                                                         │
│ Riskiest Assumption:                                    │
│ Password friction is the main cause (not other issues)  │
│ → Test with user interviews first                       │
└─────────────────────────────────────────────────────────┘
```

---

## Common Mistakes

### 1. Hypothesis is Actually a Solution

**Bad (Solution, Not Hypothesis):**
> "We need a chatbot."

**Good (Hypothesis):**
> "If we add a chatbot to answer common questions, support ticket volume will decrease by 20%, because 60% of tickets are repetitive."

**Fix:** Add the "because" and measurable outcome.

### 2. Not Measurable

**Bad (Not Measurable):**
> "Users will be happier with the new design."

**Good (Measurable):**
> "NPS score will increase from 30 to 45 within 1 month after redesign."

**Fix:** Define specific metric and target.

### 3. Too Ambitious

**Bad (Too Ambitious):**
> "Revenue will double in 1 month."

**Good (Realistic):**
> "Revenue will increase by 15% in 3 months."

**Fix:** Set realistic targets based on data.

### 4. No Time Frame

**Bad (No Time Frame):**
> "Conversion rate will increase."

**Good (Time-Bound):**
> "Conversion rate will increase by 10% within 2 weeks."

**Fix:** Add specific time frame.

### 5. Multiple Variables

**Bad (Multiple Changes):**
> "If we redesign the homepage, add testimonials, and change the CTA, conversion will increase."

**Good (Single Variable):**
> "If we add customer testimonials above the fold, conversion will increase by 8%."

**Fix:** Test one change at a time.

---

## Learning from Invalidated Hypotheses

### Hypothesis Invalidated ≠ Failure

**Mindset Shift:**
- ❌ "Our idea failed"
- ✅ "We learned our assumption was wrong"

### Example: Social Login

**Hypothesis:**
> "If we add social login, signup completion will increase by 30%."

**Result:**
> Signup completion increased by only 5% ❌

### Ask: Why Was Our Assumption Wrong?

**Possible Reasons:**
1. Password friction wasn't the main issue
2. Users don't trust social login
3. Users don't have Google/Facebook accounts
4. Social login wasn't visible enough

### Dig Deeper

**Actions:**
- Analyze data: Where do users actually drop off?
- User interviews: Why did you abandon signup?
- Heatmaps: Did users see social login button?

**Findings:**
- Users actually abandon at "Enter credit card" step
- Password step is fine

### What Did We Learn?

**Learning:**
> "Payment friction, not password friction, is the main abandonment cause."

### What's the Next Hypothesis?

**New Hypothesis:**
> "If we remove credit card requirement from free trial, signup completion will increase by 40%, because users don't want to commit payment upfront."

**Test:** A/B test with/without credit card requirement.

---

## Hypothesis Tracking

### Hypothesis Log

**Template:**

| ID | Hypothesis | Status | Start Date | End Date | Result | Learning |
|----|------------|--------|------------|----------|--------|----------|
| H001 | Social login → 30% more signups | Invalidated | 2024-01-15 | 2024-01-29 | +5% | Payment friction is real issue |
| H002 | Remove CC → 40% more signups | Testing | 2024-02-01 | - | - | - |
| H003 | Dark mode → 40% adoption | Validated | 2024-01-20 | 2024-02-03 | 45% | Users love dark mode |

### Status Types

- **Backlog:** Not yet tested
- **Testing:** Currently running experiment
- **Validated:** Hypothesis confirmed ✅
- **Invalidated:** Hypothesis disproven ❌
- **Inconclusive:** Not enough data

### Learnings Repository

**For each hypothesis, document:**
1. What we expected
2. What actually happened
3. Why (root cause)
4. What we'll do next

**Example:**
```markdown
## H001: Social Login

**Expected:** 30% increase in signup completion
**Actual:** 5% increase
**Why:** Payment friction is the real issue, not password
**Next:** Test removing credit card requirement (H002)
```

---

## Tools

### 1. Miro / FigJam

**Use For:** Collaborative hypothesis brainstorming

**Features:**
- Sticky notes for ideas
- Hypothesis canvas templates
- Voting/prioritization
- Visual organization

### 2. Google Docs

**Use For:** Hypothesis documentation

**Template:**
```
Hypothesis: [Title]
Date: [YYYY-MM-DD]
Owner: [Name]

If we [change]
For [users]
We will see [outcome]
Because [belief]
We'll measure with [metric]

Assumptions:
1. [Assumption 1]
2. [Assumption 2]

Test Plan:
- Method: [A/B test, interview, etc.]
- Duration: [X weeks]
- Sample size: [N users]

Results:
- [To be filled after test]
```

### 3. Notion

**Use For:** Hypothesis database

**Features:**
- Database views (table, kanban, calendar)
- Status tracking
- Linked pages for detailed notes
- Templates

**Database Properties:**
- Hypothesis (text)
- Status (select: Backlog, Testing, Validated, Invalidated)
- Owner (person)
- Start Date (date)
- End Date (date)
- Impact (number)
- Confidence (number)
- Ease (number)
- ICE Score (formula)
- Result (text)
- Learning (text)

### 4. Airtable

**Use For:** Hypothesis tracking with automation

**Features:**
- Similar to Notion
- Better automation
- Integrations with other tools

---

## Real Hypothesis Examples from Successful Products

### Example 1: Dropbox (2008)

**Hypothesis:**
> "If we create a 3-minute explainer video showing how Dropbox works, signups will increase significantly, because people don't understand what Dropbox is."

**Test:** Created video, posted on Hacker News

**Result:**
- Signups increased from 5,000 to 75,000 overnight
- Hypothesis validated ✅

**Learning:** People wanted Dropbox, they just didn't understand it.

### Example 2: Airbnb (2009)

**Hypothesis:**
> "If we replace amateur photos with professional photography, booking rate will increase by 2-3x, because listings look more appealing."

**Test:** Hired photographers for NYC listings

**Result:**
- Bookings increased by 2.5x
- Hypothesis validated ✅

**Learning:** Photo quality is critical for trust and conversion.

### Example 3: LinkedIn (2012)

**Hypothesis:**
> "If we show 'People You May Know' suggestions, connection growth will increase by 30%, because users don't know who else is on LinkedIn."

**Test:** A/B test with/without suggestions

**Result:**
- Connection growth increased by 40%
- Hypothesis validated ✅

**Learning:** Discovery is a major growth lever.

### Example 4: Slack (2014)

**Hypothesis:**
> "If a team sends 2,000 messages, they will become a paying customer, because they've experienced the value of Slack."

**Test:** Analyzed usage data, found correlation

**Result:**
- Teams with 2,000+ messages had 93% retention
- Hypothesis validated ✅

**Learning:** 2,000 messages became the "activation metric."

### Example 5: Superhuman (2019)

**Hypothesis:**
> "If we only allow users who are 'very disappointed' without Superhuman to use the product, we'll build a product people love, because we'll focus on the right users."

**Test:** Survey: "How would you feel if you could no longer use Superhuman?"
- Very disappointed
- Somewhat disappointed
- Not disappointed

**Result:**
- Focused on "very disappointed" segment
- Achieved product-market fit
- Hypothesis validated ✅

**Learning:** Focus on users who love you, not everyone.

---

## Summary

### Quick Reference

**Hypothesis Structure:**
```
If we [change]
For [users]
We will see [outcome]
Because [belief]
We'll measure with [metric]
```

**Good Hypothesis Characteristics:**
1. Specific
2. Measurable
3. Falsifiable
4. Time-bound
5. Focused (one variable)

**Hypothesis Types:**
- Value: Will users find this valuable?
- Usability: Can users use this?
- Feasibility: Can we build this?
- Viability: Is this sustainable?

**Prioritization (ICE):**
- Impact × Confidence × Ease

**Validation Methods:**
- User interviews
- Surveys
- A/B tests
- MVPs
- Prototypes
- Analytics

**Common Mistakes:**
- Hypothesis is a solution
- Not measurable
- Too ambitious
- No time frame
- Multiple variables

**Learning from Invalidation:**
1. Why was assumption wrong?
2. What did we learn?
3. What's next hypothesis?

**Tools:**
- Miro, FigJam (brainstorming)
- Google Docs (documentation)
- Notion, Airtable (tracking)
