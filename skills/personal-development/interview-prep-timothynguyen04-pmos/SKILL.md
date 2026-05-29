---
name: interview-prep
description: Pre-interview preparation for PM job interviews (Product Sense, Execution, Behavioral)
---

**Note:** This skill is for PM career interviews (job interviews). For preparing to conduct user research interviews, see `/interview-guide`.

# Interview Prep Skill

Prepare effectively for PM job interviews. Master Product Sense, Product Execution, Behavioral, and other interview types with structured research and practice strategies.

## Quick Start

```
/interview-prep

Preparing for a PM job interview? I'll help you get ready.

Tell me:
1. What company and role? (e.g., "Senior PM at Stripe")
2. What interview type? (Product Sense / Execution / Behavioral / Design / Technical)
3. When is the interview? (so I can scope the prep plan)

I'll generate a research checklist, framework cheat sheets, practice questions,
and a day-of game plan tailored to that company.

Say "mock interview" and I'll run you through a live practice round with feedback.

For user research interview prep, use /interview-guide instead.
```

## When to Use This Skill

- 1-2 weeks before PM job interviews
- Preparing for specific interview rounds (Product Sense, Execution, Design, etc.)
- Before take-home assignments or case studies
- Mock interview preparation

## Interview Types Overview

### 1. Product Sense Interview
**What they test:** Creativity, data acumen, user understanding, prioritization

**Question types:**
- Product improvement ("How would you improve Instagram Stories?")
- Product growth ("How would you grow Spotify users?")
- Product launch ("Should Netflix launch gaming?")
- Product design ("Design a product for X")
- Product pricing ("How would you price YouTube Premium?")

### 2. Product Execution Interview
**What they test:** Metrics definition, goal-setting, analytical rigor, execution depth

**Core skills:**
- Define north star metrics
- Set measurable success criteria
- Analyze root causes of metric changes
- Think at scale (especially for Meta/Google)

### 3. Behavioral/Leadership Interview
**What they test:** Past experience, collaboration, decision-making, conflict resolution

**Common frameworks:**
- STAR method (Situation, Task, Action, Result)
- Leadership principles (Amazon's 16, etc.)

### 4. Technical Interview
**What they test:** System design, API knowledge, data structures, SQL

### 5. Product Design Interview
**What they test:** User-centric thinking, wireframing, usability, design critique

## Workflow

### Step 1: Research the Company (2-3 hours, 1 week before)

```
Company Research Checklist:

**Product Usage:**
- [ ] Use their product daily for 1+ week
- [ ] Note friction points, delights, questions
- [ ] Track which features you use most/least
- [ ] Screenshot bugs or UX issues

**Business Model:**
- [ ] How do they make money? (ads, subs, marketplace take rate, etc.)
- [ ] Who are their customers? (B2C, B2B, B2B2C?)
- [ ] Revenue: [Estimate from earnings reports or TechCrunch]
- [ ] Growth stage: Early/Growth/Mature/Declining?

**Competitive Landscape:**
- [ ] Top 3 competitors
- [ ] What's their competitive moat? (Network effects, switching costs, etc.)
- [ ] Recent competitive threats or wins

**Recent News:**
- [ ] Last 3 product launches (TechCrunch, company blog)
- [ ] Recent controversies or challenges
- [ ] Earnings call highlights (if public company)

**Company Culture:**
- [ ] Read Glassdoor reviews (especially PM reviews)
- [ ] LinkedIn: Connect with current PMs, ask for coffee chat
- [ ] Company blog: What do they value? (Move fast, user-first, data-driven, etc.)
```

**Pro tip:** Create a one-pager summary of all this research to review 30 min before your interview.

---

### Step 2: Prep by Interview Type

#### Product Sense Prep (3-4 hours)

**Framework Practice:**
```
The 5-Step Product Sense Framework:

1. **Clarify** (2 min)
   - Understand the question
   - Ask clarifying questions
   - Define success criteria

2. **User Segments** (3 min)
   - Who are the users?
   - Pick your target segment
   - Explain why (size, pain, willingness to pay)

3. **Pain Points** (5 min)
   - What problems does this segment face?
   - Prioritize by severity + frequency
   - Pick top 1-2 to solve

4. **Solutions** (10 min)
   - Brainstorm 3-5 solutions
   - Evaluate pros/cons
   - Prioritize (impact vs. effort)

5. **Success Metrics** (5 min)
   - Define north star metric
   - Add 2-3 supporting metrics
   - Set success criteria
```

**Practice Questions:**
- Pick 5 products you use daily
- For each, practice: "How would you improve [Product]?"
- Time yourself: 25 minutes per answer
- Record yourself (audio/video) and review

**Company-Specific Twists:**
- **Meta/Facebook:** Think at global scale, diverse user bases
- **Google:** Data-driven, A/B testing mindset
- **Amazon:** Customer obsession, work backwards from user
- **Apple:** Design elegance, simplicity, ecosystem thinking

---

#### CIRCLES Framework (for Product Design Questions)

```
The CIRCLES Method - 7 Steps for Product Design:

1. **Comprehend** the situation
   - What is the product? Who is the user?
   - Restate the question to confirm understanding
   - Ask: "Am I designing for mobile, web, or both?"

2. **Identify** the customer
   - List 2-3 user segments
   - Pick one to focus on (explain why)
   - Describe their demographics, behaviors, goals

3. **Report** customer needs
   - List 5-7 needs/pain points for your chosen segment
   - Prioritize by severity and frequency
   - Pick top 2-3 to solve

4. **Cut** through prioritization
   - Use a 2x2 matrix: Impact vs. Effort
   - Evaluate each need against business goals
   - Select the #1 need to address

5. **List** solutions
   - Brainstorm 3-5 solutions for the top need
   - Be creative -- don't just copy competitors
   - Include at least one "bold" solution

6. **Evaluate** trade-offs
   - Pros/cons for each solution
   - Technical feasibility, time to build, scalability
   - Pick the winning solution with clear rationale

7. **Summarize** your recommendation
   - Restate: user, need, solution
   - Success metrics for the solution
   - Risks and how to mitigate them
```

**When to use CIRCLES:** "Design a product for...", "How would you build...", "Create a new feature for..."

---

#### Product Execution Prep (2-3 hours)

**Core Skills to Master:**

**1. Metrics Definition**
```
For any feature, define:

**North Star Metric:**
- The one metric that best captures value delivered
- Example: DAU/MAU for engagement, GMV for marketplace

**Supporting Metrics:**
- Metric 1: [Leading indicator]
- Metric 2: [Usage depth]
- Metric 3: [Business impact]

**Guardrail Metrics:**
- What you WON'T sacrifice
- Example: User satisfaction > 4.0, Latency < 200ms
```

**2. Root Cause Analysis**
```
"Metric X dropped by Y%. Why?"

Step 1: Clarify the data
- Which user segments affected?
- Which platforms/geographies?
- Time period?

Step 2: Hypotheses
- Internal changes (product, bug, experiment)
- External factors (seasonality, competition, news)
- Data issues (tracking broken, definition changed)

Step 3: Investigate
- Check recent launches
- Segment the data
- Compare to historical patterns

Step 4: Recommend action
- If bug: Fix immediately
- If experiment: Kill or iterate
- If external: Monitor or adapt strategy
```

**3. AARM Framework (for Metrics Questions)**
```
AARM - 4 Steps for Any Metrics Question:

1. **Acquire** - How do users find the product?
   - Acquisition channels (organic, paid, referral, viral)
   - Top-of-funnel metrics: impressions, clicks, signups
   - Cost per acquisition by channel

2. **Activate** - How do users get to the "aha moment"?
   - Activation funnel: signup → onboarding → first value
   - Time to value, completion rates at each step
   - What defines an "activated" user?

3. **Retain** - How do users keep coming back?
   - Retention curves: D1, D7, D30
   - Engagement frequency and depth
   - Churn signals and re-engagement triggers

4. **Monetize** - How does the product make money?
   - Revenue per user (ARPU), lifetime value (LTV)
   - Conversion to paid, expansion revenue
   - LTV:CAC ratio, payback period
```

**When to use AARM:** "What metrics would you track for...", "How would you measure success for...", "A metric dropped X%, diagnose it"

**Practice:**
- Find 3 recent product launches (TechCrunch, Product Hunt)
- For each, define: North star + 3 supporting metrics + 2 guardrails
- Practice explaining your reasoning out loud

---

### Company-Type Specific Prep

Tailor preparation based on the company category:

**AI/ML Companies** (OpenAI, Anthropic, Midjourney):
- Emphasize: AI product trade-offs (accuracy vs latency, safety vs capability), evaluation methodology, prompt engineering as product design
- Study: Their model capabilities, API pricing, developer ecosystem
- Unique angles: "How would you measure if an AI feature is actually helping users vs just impressive?"

**Marketplaces** (Airbnb, Uber, DoorDash):
- Emphasize: Supply vs demand balancing, chicken-and-egg problems, trust & safety, unit economics
- Study: Their take rate, geographic expansion strategy, supply acquisition
- Unique angles: "How would you design for the supply side without hurting demand experience?"

**Enterprise SaaS** (Salesforce, Slack, Notion):
- Emphasize: Multi-persona buying (end user vs buyer vs admin), seat expansion, enterprise security/compliance
- Study: Their pricing tiers, integration ecosystem, competitive positioning
- Unique angles: "How would you balance individual user experience with admin control needs?"

**Consumer Social** (Meta, TikTok, Snap):
- Emphasize: Engagement loops, creator vs consumer dynamics, content ranking, growth mechanics
- Study: Their DAU/MAU ratios, monetization model, content moderation approach
- Unique angles: "How would you measure healthy engagement vs addictive patterns?"

**Fintech** (Stripe, Square, Plaid):
- Emphasize: Trust, compliance, fraud prevention, API-first thinking, developer experience
- Study: Their regulatory environment, payment flow, risk management
- Unique angles: "How would you design for both the merchant and the end consumer?"

---

#### Behavioral Prep (2 hours)

**STAR Method Template:**
```
Situation: [Set context in 1-2 sentences]
Task: [What needed to be done?]
Action: [What YOU specifically did - use "I" not "we"]
Result: [Quantified outcome + learning]
```

**Top 10 Behavioral Questions:**
1. Tell me about a time you failed
2. Describe a conflict with a teammate and how you resolved it
3. Tell me about your most impactful product
4. How do you prioritize features?
5. Describe a time you influenced without authority
6. Tell me about a time you disagreed with your manager
7. How do you handle ambiguity?
8. Describe a time you had to make a decision with incomplete data
9. Tell me about a time you had to say no to a stakeholder
10. Why product management? Why this company?

**Prep Strategy:**
- Write out 5-7 stories from your experience
- Each story should be usable for 2-3 different questions
- Focus on recent work (last 2 years)
- Include failures and learnings (not just wins)
- Quantify results wherever possible

**Specific Guidance: "Tell me about a time you used data to make a decision"**

This is one of the most common behavioral questions. Structure your answer:

```
1. **Set the stage** (15 sec)
   - "We were deciding whether to [build X / launch Y / kill Z]"
   - Mention the stakes: revenue, users, team resources

2. **Describe the data you gathered** (30 sec)
   - What data sources? (analytics, surveys, A/B tests, user interviews)
   - What was the key metric or insight?
   - Use exact numbers: "Conversion was 3.2%, below our 5% threshold"

3. **Show the analysis** (30 sec)
   - How did you interpret the data?
   - What did the data suggest vs. what your gut said?
   - Any conflicting signals? How did you resolve them?

4. **The decision and outcome** (30 sec)
   - What did you decide? Why?
   - Quantified result: "This led to a 15% increase in retention"
   - What did you learn about using data?

Red flags to avoid:
- Vague data: "We looked at some metrics" (which ones?)
- No conflict: The best stories involve data surprising you
- No learning: Always end with what you'd do differently
```

---

### Mock Interview Mode

**If the PM says "mock interview", enter this mode:**

1. **Ask for setup:**
   - "What interview type? (Product Sense / Execution / Behavioral / Design)"
   - "What company? (I'll tailor the question)"
   - "Timer on or off? (Real interviews are 25-35 min)"

2. **Present a question:**
   - Pick a realistic question for the company and interview type
   - Say: "Your time starts now. Take a moment to structure your thoughts, then walk me through your answer."

3. **Wait for their full answer.** Do not interrupt. Let them finish.

4. **Provide structured feedback:**

```
## Mock Interview Feedback

**Question:** [The question asked]
**Time taken:** [Estimate]

### Scores (1-5)

| Dimension | Score | Notes |
|-----------|-------|-------|
| Framework Usage | X/5 | Did they use a clear structure? |
| Specificity | X/5 | Real examples, data, concrete details? |
| Creativity | X/5 | Did their answer stand out? Unique insights? |
| Communication Clarity | X/5 | Concise, easy to follow, no rambling? |
| Product Sense | X/5 | User empathy, business understanding? |

### What Went Well
- [Specific strength 1]
- [Specific strength 2]

### What to Improve
- [Specific improvement 1 with how to fix it]
- [Specific improvement 2 with how to fix it]

### Model Answer Outline
Here's how a strong candidate might structure this:
- [Key point 1]
- [Key point 2]
- [Key point 3]
```

5. **Ask:** "Want to try another question, or work on one of the weak areas?"

---

### Step 3: Mock Interviews (1 week before)

```
Mock Interview Checklist:

**Find a partner:**
- [ ] PM friend or mentor
- [ ] Career coach or interviewer
- [ ] Pramp, Exponent, or IGotAnOffer platforms

**Structure the mock:**
- [ ] Pick interview type (Product Sense, Execution, etc.)
- [ ] Set a timer (25-30 min)
- [ ] Ask partner to interrupt/probe like real interviewer
- [ ] Record the session

**Post-mock debrief:**
- [ ] What went well?
- [ ] What felt rushed or unclear?
- [ ] Did I clarify assumptions?
- [ ] Were my metrics specific enough?
- [ ] Did I structure my answer before diving in?

**Iterate:**
- [ ] Do 3-5 mocks minimum
- [ ] Focus on weak areas each time
- [ ] Get faster at structuring answers
```

---

### Step 4: Day-Before Prep (1 hour)

```
Final Prep Checklist:

**Review your research:**
- [ ] Re-read company one-pager
- [ ] Review recent product launches
- [ ] Refresh on company metrics (if public)

**Prepare questions to ask:**
- [ ] About the role: "What does success look like in the first 90 days?"
- [ ] About the team: "What's the biggest challenge the team is facing?"
- [ ] About the product: "What's the product vision for the next year?"
- [ ] About culture: "How does the team balance speed vs. quality?"

**Logistics:**
- [ ] Test Zoom/tech setup
- [ ] Prepare quiet space (close door, mute phone)
- [ ] Have water nearby
- [ ] Pen + paper ready for notes/sketching
- [ ] Resume printed (if in-person)

**Mindset:**
- [ ] Get good sleep (8+ hours)
- [ ] Light exercise (walk, yoga)
- [ ] Review framework cheat sheet (15 min)
- [ ] Don't cram new content day-of
```

---

### Step 5: Interview Day (30 min before)

```
Pre-Interview Routine:

**T-30 min:**
- [ ] Review company one-pager (5 min)
- [ ] Review framework cheat sheets (5 min)
- [ ] Do 1 quick practice question out loud (10 min)
- [ ] Breathe, center yourself (5 min)
- [ ] Use bathroom, get water (5 min)

**T-5 min:**
- [ ] Join call early
- [ ] Check audio/video
- [ ] Have pen + paper ready
- [ ] Smile - set positive energy

**During interview:**
- [ ] Take notes on question
- [ ] Ask clarifying questions
- [ ] Structure before diving in
- [ ] Check time midway through
- [ ] Leave 2-3 min for questions
```

---

## Output Format

```markdown
# Interview Prep: [Company Name] - [Role]

**Interview Date:** [Date]
**Interview Type:** [Product Sense / Execution / Behavioral / etc.]

---

## Company Research Summary

**Product:** [1-sentence description]
**Business Model:** [How they make money]
**Recent News:** [3 bullet points]
**Competitors:** [Top 3]
**My Usage Notes:** [Friction points, delights, questions]

---

## Key Metrics to Know

- North Star: [Metric]
- Revenue: [Estimate]
- Growth Stage: [Early/Growth/Mature]
- User Base: [Size + segments]

---

## Interview Type Prep

### [Product Sense / Execution / Behavioral]

**Framework to use:** [5-step Product Sense, STAR, etc.]

**Practice questions completed:**
1. [Question 1] - [Time: X min] - [Rating: Good/Needs work]
2. [Question 2] - [Time: X min] - [Rating: Good/Needs work]
3. [Question 3] - [Time: X min] - [Rating: Good/Needs work]

**Weak areas to focus on:**
- [Area 1: e.g., "Need to be more specific on metrics"]
- [Area 2: e.g., "Clarify assumptions upfront"]

---

## Questions to Ask Interviewer

1. [Question about role]
2. [Question about team]
3. [Question about product]
4. [Question about culture]

---

## Day-Of Checklist

- [ ] Reviewed company one-pager
- [ ] Practiced 1 question out loud
- [ ] Tech setup tested
- [ ] Water + pen + paper ready
- [ ] Mindset: confident and curious
```

---

## Pro Tips

1. **Structure before you speak:** Take 30-60 seconds to outline your answer
2. **Think out loud:** Let interviewer follow your thought process
3. **Ask clarifying questions:** Shows you don't make assumptions
4. **Be specific on metrics:** "Increase engagement" → "Increase DAU/MAU from 40% to 50%"
5. **Show trade-offs:** "Option A is faster to build, but Option B has more long-term value"
6. **Use real data:** "Based on Instagram having 2B users..." not "I assume they have a lot of users"
7. **Time management:** Spend 5 min on problem definition, not 20 min on solutions
8. **Connect to company:** "This aligns with Meta's mission of bringing people together"

---

## Common Mistakes to Avoid

❌ Jumping to solutions without understanding the problem
✅ Spend time on user segments and pain points first

❌ Vague metrics ("improve engagement")
✅ Specific metrics with targets ("increase 7-day retention from 30% to 40%")

❌ Only considering one solution
✅ Generate 3+ options and evaluate trade-offs

❌ Ignoring the business
✅ Connect user value to business value (revenue, retention, virality)

❌ Not asking clarifying questions
✅ Ask about constraints, success criteria, user segments

❌ Going overtime
✅ Check time at 50% mark, wrap up with 2-3 min buffer

---

## Resources

**Practice Platforms:**
- Exponent: Mock interviews + courses
- Pramp: Free peer mock interviews
- IGotAnOffer: Company-specific prep
- Product Alliance: Video courses

**Reading:**
- Cracking the PM Interview (Gayle McDowell)
- Decode and Conquer (Lewis Lin)
- Company blogs: Meta, Google, Amazon PM blogs

**Aakash Gupta's Guides:**
- [Master the Product Sense Interview](https://www.news.aakashg.com/p/master-the-product-sense-interview)
- [Crack the Product Execution Interview](https://www.news.aakashg.com/p/crack-the-product-execution-interview)
- [Big 3 PM Interview Guide](https://www.news.aakashg.com/p/big-3-pm-interview-guide-google-microsoft)

---

### Improvement Loop: Connect to /interview-feedback

After each real interview, run `/interview-feedback` to debrief. Over time, this creates a feedback loop:
1. `/interview-prep` identifies areas to practice -- you prepare
2. You do the interview
3. `/interview-feedback` scores your performance on 5 dimensions
4. Scores inform what to focus on in `/interview-prep` for the next round

After 3+ debriefs, `/interview-feedback` shows trend data. Use this to target your prep: if "Specificity" is consistently low, `/interview-prep` should emphasize researching company metrics and practicing with numbers.

---

## Output Quality Self-Check

Before delivering the prep plan, verify:

| Check | Criteria | Pass? |
|-------|----------|-------|
| **Company-specific** | Research and questions are tailored to the target company, not generic | [ ] |
| **Framework included** | At least one relevant framework provided (5-Step, CIRCLES, AARM, STAR) | [ ] |
| **Practice questions** | At least 3 practice questions with timing guidance | [ ] |
| **Metrics are specific** | Example metrics use real numbers, not vague ("increase engagement") | [ ] |
| **Checklist provided** | Day-before and day-of checklists included | [ ] |
| **Questions to ask** | At least 3 thoughtful questions for the PM to ask the interviewer | [ ] |
| **Weak areas identified** | Specific areas to focus practice on, based on interview type | [ ] |
| **Time-boxed** | Prep plan is scoped to the available time before the interview | [ ] |

**If any check fails, address it before delivering the output.**

---

Remember: Great preparation beats natural talent. Put in the 10-15 hours of structured prep, and you'll walk in confident and ready to nail the interview.
