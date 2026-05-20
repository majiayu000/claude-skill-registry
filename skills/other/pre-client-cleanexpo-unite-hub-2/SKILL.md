---
name: pre-client
description: Pre-sales intelligence system. Ingests incoming emails, analyzes sender context, clusters related conversations, detects business opportunities, builds relationship timelines, and surfaces high-potential prospects for outreach.
---

# Pre-Client Identity Skill

## Overview

The Pre-Client Identity Skill is the **incoming lead intelligence engine**. It:
- Ingests and analyzes incoming emails automatically
- Extracts sender company, role, and background
- Clusters related messages into conversation threads
- Detects buying signals and business problems
- Builds relationship timelines for each prospect
- Surfaces high-potential opportunities for follow-up

Think of it as an AI that watches your inbox and alerts you when someone valuable walks in the door.

## Core Capabilities

### 1. Email Ingestion & Analysis

**What it captures:**
```
FROM SENDER:
- Name and email address
- Company name (extracted from email domain or signature)
- Job title/role
- Reporting to (if mentioned)
- Company size (estimated)
- Phone number (if provided)
- LinkedIn URL (if signature includes)
- Location/timezone

FROM EMAIL CONTENT:
- Subject line (intent signal)
- Body text (problem statement)
- Attachments (RFP, proposal, documentation)
- Links clicked (if tracking enabled)
- Email tone (formal, casual, urgent, desperate)

FROM EMAIL METADATA:
- Date received
- Time of day sent (weekend? off-hours?)
- Reply time (how quickly they respond)
- Response rate (how many emails before reply)
- Thread history (how long have they been in conversation)

EXAMPLE EMAIL ANALYSIS:

From: sarah.chen@techstartup.io
Subject: "Looking for better project management solution"

SENDER PROFILE:
- Name: Sarah Chen
- Company: TechStartup Inc (estimated 25-50 people)
- Role: Operations Manager
- Location: San Francisco, CA (timezone: PST)
- LinkedIn: linkedin.com/in/sarahchen
- Phone: Not provided

EMAIL CONTENT:
- Intent: Looking for solution (high intent signal)
- Problem: Current project management tool isn't meeting needs
- Pain points: Visibility, team collaboration, reporting
- Budget indicator: Not mentioned
- Timeline: "Looking to migrate Q1 2026"
- Current solution: Using Monday.com
- Dissatisfaction level: MODERATE (considering switch)

EMAIL TONE:
- Professional, respectful
- Not urgent or desperate
- Exploratory (gathering information)
- Open to solutions (receptive)

CONTEXT:
- Email sent Tuesday 9 AM (business hours)
- Took 2 hours to respond (attentive)
- First email in thread
- No attachments

SCORING:
- Fit score: 8/10 (perfect ICP match)
- Intent score: 7/10 (genuine interest, not urgent)
- Budget score: 5/10 (not mentioned, mid-market likely)
- Timeline score: 8/10 (Q1 2026 is soon)
- Response likelihood: 85% (warm prospect)
```

### 2. Thread Clustering & Organization

**Automatic conversation grouping:**

```
CLUSTERING ALGORITHM:
Groups emails into conversations based on:
1. Same sender + same company
2. Same topic/problem domain
3. Time proximity (within 2 weeks suggests related)
4. Reply-to-reply chains (email threading)

EXAMPLE CLUSTERED THREAD:
Conversation ID: SARAH_CHEN_PROJECT_MGMT_001

Email 1 (Nov 15, 9:02 AM):
From: sarah.chen@techstartup.io
Subject: "Looking for better project management solution"
[Initial inquiry]

Email 2 (Nov 15, 2:15 PM):
From: sarah.chen@techstartup.io
Subject: "RE: Looking for better project management solution"
[Follow-up with more details]

Email 3 (Nov 16, 10:30 AM):
From: sarah.chen@techstartup.io
Subject: "RE: Pricing and implementation timeline?"
[Asking about pricing and timeline]

Email 4 (Nov 18, 3:45 PM):
From: john.smith@techstartup.io (copied from email 3)
Subject: "RE: Pricing and implementation timeline?"
[CTO added to conversation - buying committee expanding]

THREAD SUMMARY:
- Duration: 3 days (active conversation)
- Participants: 2 (Sarah + John)
- Message count: 4
- Response time avg: 18 hours
- Engagement level: HIGH
- Buying committee growing: YES (CTO added)

OPPORTUNITY ASSESSMENT:
- This is a REAL opportunity (not just browsing)
- Buying committee forming (good sign)
- Timeline moving fast (3 days)
- Next step probability: 65%
```

### 3. Buying Signals Detection

**Identifies high-intent indicators:**

```
TIER 1: HIGHEST INTENT (Act immediately)
Signal: "We need to migrate by Q1"
Signal: "We've allocated budget for this"
Signal: "We're evaluating vendors this month"
Signal: "Your solution solves problem X that's costing us $Y"
Signal: "When can you start implementation?"
Signal: "Can you do a demo tomorrow?"
Action: Schedule call immediately

TIER 2: HIGH INTENT (Respond within hours)
Signal: "We're looking for a solution like yours"
Signal: "Our current tool doesn't support feature X"
Signal: "How much does this cost?"
Signal: "Can you send pricing and case studies?"
Signal: "Tell me more about your solution"
Signal: "Does this integrate with [their tools]?"
Action: Respond with valuable information

TIER 3: MODERATE INTENT (Follow up within 24 hours)
Signal: "We might be interested in the future"
Signal: "Just exploring options"
Signal: "Can you add me to your mailing list?"
Signal: "Do you have any case studies?"
Signal: "What's your free trial period?"
Action: Provide resources, nurture

TIER 4: LOW INTENT (Add to nurture sequence)
Signal: "Just curious what you do"
Signal: "We're not looking to change right now"
Signal: "Can I learn more about your company?"
Signal: "Interesting product, thanks for sharing"
Action: Long-term nurture, stay in touch

EXAMPLE SIGNALS IN CONTEXT:

Email: "We have budget allocated for this in Q1"
Tier: 1 (HIGHEST)
Reasoning: Budget allocated = money reserved
Action: Call them before competitors do

Email: "How long is your implementation timeline?"
Tier: 1-2 (HIGH)
Reasoning: Specific implementation question = ready to execute
Action: Provide detailed timeline, case study

Email: "Can you send us pricing?"
Tier: 2 (HIGH)
Reasoning: Asking about price = considering buying
Action: Send pricing + case study showing ROI

Email: "What do you charge?"
Tier: 2-3 (MODERATE-HIGH)
Reasoning: Price question, but phrased casually
Action: Respond quickly with pricing framework

Email: "Just browsing your website"
Tier: 4 (LOW)
Reasoning: No specific problem mentioned
Action: Add to nurture, wait for signal
```

### 4. Business Problem Detection

**Identifies pain points and opportunity triggers:**

```
OPPORTUNITY TYPES:

1. TOOL REPLACEMENT
Signal: "Our current [tool] isn't meeting our needs"
Problem: Existing solution inadequate
Opportunity: Replace with your solution
Timeline: Usually 4-8 weeks
Approach: Comparison guide, migration support

Example:
"We use Monday.com but it doesn't support our workflow"
→ You have project management solution
→ Create comparison: Monday.com vs. Your tool
→ Highlight features they specifically need
→ Timeline: Could migrate in Q1

2. PROCESS PAIN
Signal: "We're struggling with [process]"
Problem: Manual process, inefficiency
Opportunity: Automate with your solution
Timeline: Depends on complexity
Approach: ROI calculator, process improvement plan

Example:
"We spend 20 hours/week on manual status reports"
→ Your solution automates reporting
→ Calculate time savings: 20 hrs/week × 50 weeks = 1,000 hrs = $50k/year
→ ROI: Huge
→ Timeline: 30-60 days

3. GROWTH BLOCKER
Signal: "We can't scale because [reason]"
Problem: Current setup can't support growth
Opportunity: Enable growth with your solution
Timeline: Urgent (growth is happening now)
Approach: Growth strategy, capacity planning

Example:
"We can't onboard more clients because we can't manage them"
→ Your solution supports unlimited clients
→ Calculate revenue impact: Each client = $10k/year
→ For every 10 clients: $100k new revenue
→ Timeline: URGENT - do this month

4. COMPETITIVE THREAT
Signal: "Competitor X has feature Y"
Problem: Falling behind in market
Opportunity: Close gap with your solution
Timeline: Medium urgency
Approach: Competitive comparison, feature roadmap

Example:
"Competitor is offering integration we don't have"
→ Your solution has that integration
→ Risk: Losing customers to competitor
→ Timeline: 6-8 weeks to close gap

5. TEAM/WORKFLOW IMPROVEMENT
Signal: "Our team would work better if [feature]"
Problem: Suboptimal workflows
Opportunity: Improve team productivity with your solution
Timeline: Medium term
Approach: Workflow assessment, ROI analysis

Example:
"Our team spends too much time in meetings coordinating"
→ Your solution has better collaboration features
→ Benefit: Fewer meetings, more focus time
→ Productivity gain: 5 hours/person/week = $10k/year for 10 people
```

### 5. Relationship Timeline Building

**Constructs prospect journey:**

```
TIMELINE EXAMPLE: Sarah Chen (TechStartup Inc)

STAGE 1: AWARENESS (Nov 15, 9 AM)
Event: Email received
Content: "Looking for better project management solution"
Status: New prospect discovered
Action: Add to tracking

STAGE 2: INITIAL RESEARCH (Nov 15, 9 AM - 2 PM)
Event: Multiple emails in quick succession
Content: Asking detailed questions about features
Status: Active research
Intent: Medium-High
Action: Respond with valuable resources

STAGE 3: BUYING COMMITTEE FORMATION (Nov 16, 10 AM)
Event: CTO (John Smith) added to conversation
Content: Technical questions about integration, security
Status: Moving toward decision
Intent: High
Signal: Multiple decision-makers involved = serious

STAGE 4: EVALUATION PHASE (Nov 16 - 20)
Event: Requesting demo, technical documentation
Content: Specific questions about implementation
Status: In evaluation phase
Timeline: "Looking to migrate Q1 2026"
Action: Schedule demo, provide case studies

STAGE 5: PROPOSAL/NEGOTIATION (Expected Nov 20-30)
Prediction: Based on engagement velocity
Content: Would include pricing discussions, requirements confirmation
Status: Likely approaching proposal stage
Action: Prepare proposal, service level agreements

TIMELINE VISUALIZATION:
Nov 15 (Day 1)
│  Sarah initial inquiry
│  ├─ 9 AM: First email
│  └─ 2 PM: Follow-up email
│
Nov 16 (Day 2)
│  Research & committee
│  ├─ 10 AM: CTO joins (signal: serious buyer)
│  └─ 3 PM: Technical questions
│
Nov 18 (Day 3)
│  Evaluation
│  └─ Demo request expected

Nov 20 (Day 5)
│  Proposal phase expected

Q1 2026 (Implementation window mentioned)
│  Expected implementation timeline

ENGAGEMENT METRICS:
- Response time: 12-18 hours (very attentive)
- Message frequency: 4 emails in 5 days (active)
- Buying committee: Expanding (2 people → likely more)
- Specificity: Very specific about needs (serious)
- Timeline: Concrete (Q1 2026)

CONVERSION PROBABILITY: 60-75%
Based on: High engagement, buying committee, concrete timeline
Confidence: HIGH

RECOMMENDED ACTIONS:
1. TODAY: Send personalized welcome + case studies
2. TOMORROW: Offer 15-min discovery call
3. THIS WEEK: Share technical documentation + demo
4. NEXT WEEK: Proposal + pricing discussion
5. WEEK 3: Contract review + implementation planning
```

### 6. Opportunity Surfacing

**Highlights high-potential leads:**

```
OPPORTUNITY SCORING SYSTEM:

Each prospect gets a composite score (0-100):

FIT SCORE (30%):
- Are they in your ICP (ideal customer profile)?
- Company size match: +25
- Industry match: +25
- Role/title match: +20
- Budget capacity: +20
- Timeline alignment: +10
Score example: Sarah Chen = 28/30 (92%)

INTENT SCORE (40%):
- How serious are they?
- Explicit problem mentioned: +25
- Asking about pricing: +20
- Requesting demo: +20
- Budget allocated: +20
- Concrete timeline: +15
Score example: Sarah Chen = 32/40 (80%)

ENGAGEMENT SCORE (20%):
- How active are they?
- Response time (fast = high): +20
- Message frequency: +15
- Buying committee growth: +20
- Email specificity: +15
Score example: Sarah Chen = 18/20 (90%)

TIMELINE SCORE (10%):
- How soon do they need this?
- Q1 2026 = +10 (6 weeks away, urgent)
- "Soon" = +7 (vague, medium urgency)
- "Someday" = +3 (low urgency)
Score example: Sarah Chen = 10/10 (100%)

COMPOSITE SCORE CALCULATION:
- Fit: 28/30 × 30% = 28 points
- Intent: 32/40 × 40% = 32 points
- Engagement: 18/20 × 20% = 18 points
- Timeline: 10/10 × 10% = 10 points
TOTAL: 88/100 (EXCELLENT opportunity)

OPPORTUNITY RANKING:

TIER 1 (85-100): ACT IMMEDIATELY
- Sarah Chen (TechStartup Inc): 88/100
  Action: Call today, offer same-day demo
  Expected close: 60-75%
  Expected value: $50k-150k/year

TIER 2 (70-84): RESPOND WITHIN 24 HOURS
- John Doe (FinanceInc): 78/100
  Action: Personalized email + case study
  Expected close: 40-50%
  Expected value: $20k-50k/year

TIER 3 (55-69): RESPOND WITHIN 48 HOURS
- Lisa Brown (MediaCorp): 62/100
  Action: Informational resources
  Expected close: 20-30%
  Expected value: $10k-30k/year

TIER 4 (<55): ADD TO NURTURE SEQUENCE
- Various low-intent: <55/100
  Action: Automated nurture email sequence
  Expected close: 5-10%
  Expected value: Variable
```

### 7. Prospect Enrichment

**Gathers additional context:**

```
DATA ENRICHMENT SOURCES:
- LinkedIn (company size, employees, industries)
- Crunchbase (funding, investors, acquisition history)
- Google search (company website, news, social media)
- Industry databases (Dun & Bradstreet equivalent)
- Email metadata (company tech stack)
- Previous interactions (past emails, website visits)

ENRICHMENT RESULT EXAMPLE:

PROSPECT: Sarah Chen
Company: TechStartup Inc
Role: Operations Manager
Email: sarah.chen@techstartup.io
Phone: (415) 555-0123

ENRICHED DATA:

Company Profile:
- Name: TechStartup Inc
- Founded: 2019
- Size: 32 employees
- Funding: Series A ($5M in 2021)
- Investors: Sequoia Capital, Y Combinator
- Website: techstartup.io
- Industry: SaaS / Project Management
- HQ: San Francisco, CA
- Notable news: Raised Series B planning

Sarah's Profile:
- Title: Operations Manager (since June 2023)
- LinkedIn: 1,200 followers, 5 years operations experience
- Previous roles: Coordinator at Adobe, Operations at Stripe
- Education: UC Berkeley MBA
- Connections: 2 mutual LinkedIn connections

Company's Needs (inferred):
- Current tools: Monday.com, Slack, Hubspot
- Recent hiring: 3 operations staff in 6 months
- Growth trajectory: 50% YoY growth expected
- Pain points: Scaling operations, coordination across distributed team
- Likely budget: Series B funding = significant budget available

Sarah's Influence:
- Decision-making authority: Medium-high (manages operations team)
- Influence on purchases: High (tool recommendations likely followed)
- Reporting: Likely to VP/CTO
- Budget authority: $10k-50k likely (needs approval above)

Company's Buying Patterns:
- Sales cycle: Likely 4-8 weeks (Series B backed)
- Decision-makers: Operations + CTO + CFO probable
- Risk profile: Growth-focused, willing to invest in solutions

RECOMMENDATION:
- High-quality opportunity
- Timing: Perfect (Series B funded, scaling)
- Approach: Solutions-focused, ROI-based
- Message: How to scale operations efficiently
```

## Command Reference

### Email Analysis

```
Analyze email
- Email address: sender to extract data from
- Subject: thread to search for
- Focus: Extract sender info, identify intent, assess tier
- Output: Structured prospect analysis

Extract sender data
- Email: incoming email to analyze
- Data to extract: Company, role, location, signal
- Output: Sender profile

Detect buying signals
- Email content: the message to analyze
- Signal type: tool replacement, growth blocker, etc.
- Output: Buying signal assessment + opportunity tier
```

### Thread & Opportunity Management

```
Cluster conversation
- Sender: the prospect
- Company: their organization
- Organize into: conversation thread
- Output: Related emails grouped + analysis

Build relationship timeline
- Prospect: who to track
- Emails: conversation thread
- Output: Timeline of engagement + predictions

Surface opportunities
- Threshold: show only score 75+? 85+?
- Timeframe: last 7 days, last month, all-time
- Output: Ranked list of opportunities

Opportunity details
- Opportunity ID: specific prospect
- Show: Fit, intent, engagement scores
- Recommendations: Next actions
- Output: Full opportunity profile
```

### Enrichment & Tracking

```
Enrich prospect data
- Email: prospect to enrich
- Sources: LinkedIn, Crunchbase, search
- Output: Enriched prospect profile

Track relationship
- Prospect: who to track
- Start from: first email date
- Output: Timeline + engagement analysis

Next steps recommendation
- Prospect: who needs action
- Based on: tier, signals, timeline
- Output: Recommended actions + timing
```

## Integration Points

Pre-Client Identity Skill works with:
- **Email systems** - Gmail, Outlook API
- **LinkedIn API** - Profile enrichment
- **Crunchbase API** - Company data
- **Slack/Zapier** - Alert notifications
- **CRM systems** - Sync with Salesforce, HubSpot
- **Claude NLP** - Intent extraction, classification
- **Content library** - Relevant case studies, assets
- **Sales calendar** - Schedule demos, meetings

## Example Workflows

### Workflow 1: Incoming Email → Opportunity Surfaced

```
Email arrives: sarah.chen@techstartup.io
"Looking for better project management solution"

PRE-CLIENT SYSTEM:
1. Extract sender data
   - Sarah Chen, TechStartup Inc, Operations Manager
   - Company size: 32, Location: SF

2. Detect intent
   - Signal: Tool replacement (looking for better solution)
   - Tier: HIGH (2/2)

3. Identify problem
   - Current tool: Monday.com inadequate
   - Opportunity: Replace with your solution

4. Score opportunity
   - Fit: 92/100 (perfect ICP match)
   - Intent: 80/100 (genuine interest)
   - Engagement: Will track over time
   - Initial score: 78/100

5. Surface to sales team
   Notification: "🔥 NEW OPPORTUNITY: Sarah Chen (TechStartup Inc)

   Score: 78/100 | Tier: HIGH
   Problem: Needs better project management tool
   Timeline: Q1 2026 migration planned
   Action: Respond within 2 hours with case study
   Expected value: $50k-100k/year"

6. Track activity
   - Email received: Nov 15, 9 AM
   - Intent: HIGH
   - Status: Awaiting response
   - Follow-up: If no response in 24h, send case study
```

### Workflow 2: Thread Clustering & Timeline

```
Over 5 days, 4 emails from Sarah + John

PRE-CLIENT SYSTEM:
1. Day 1: Sarah's initial inquiry
   - Opportunity score: 68/100
   - Action: Respond with resources

2. Day 2: Sarah's follow-up + CTO John joins
   - Buying committee expanding (good sign)
   - Opportunity score: 82/100 (↑14 points)
   - Action: Schedule discovery call

3. Day 3: John asks technical questions
   - Deep evaluation phase
   - Opportunity score: 88/100 (↑6 points)
   - Action: Provide technical docs + demo

4. Day 5: Expected demo request
   - Moving to proposal phase
   - Opportunity score: 90/100 (↑2 points)
   - Action: Demo + proposal preparation

TIMELINE VISUALIZATION FOR SALES TEAM:
"Sarah Chen opportunity is in ACTIVE EVALUATION phase
Last activity: 2 hours ago (high engagement)
Buying committee: Growing (Sarah + CTO John)
Timeline: Q1 2026 implementation
Next step: Demo expected within 48 hours
Probability: 65-75% (high confidence)
Close timeline: 4-6 weeks"
```

### Workflow 3: Opportunity Ranking

```
Email inbox analysis over last week:

Opportunities found: 12
Tier 1 (85-100): 2 opportunities → ACT TODAY
Tier 2 (70-84): 4 opportunities → ACT TOMORROW
Tier 3 (55-69): 4 opportunities → ACT THIS WEEK
Tier 4 (<55): 2 opportunities → NURTURE

TIER 1 RANKING:
1. Sarah Chen (TechStartup Inc): 88/100
   - Problem: Tool replacement (Q1 timeline)
   - Action: Call within 2 hours
   - Expected value: $75k/year

2. Michael Zhang (DataCorp): 86/100
   - Problem: Growth blocker (urgent)
   - Action: Demo today
   - Expected value: $50k/year

RECOMMENDATION:
Sarah Chen is highest priority. Call her within 1 hour.
Michael Zhang is second. Schedule demo within 24 hours.
This sequence can likely yield $125k/year in new revenue."
```

## Triggers & Keywords

User says any of:
- "Check email"
- "Any new opportunities?"
- "Who just emailed?"
- "New prospects"
- "Buying signals detected?"
- "Thread analysis for..."
- "Opportunity score for..."
- "Timeline for..."
- "Should I follow up with..."
- "Rank these opportunities"
- "Who should I call?"
- "Prospect enrichment for..."

## Version 1 Scope

**What we deliver:**
- Email ingestion and basic analysis
- Intent detection and tier classification
- Buying signal identification
- Conversation clustering
- Opportunity scoring framework
- Relationship timeline visualization
- Enrichment data aggregation

**What we don't deliver (Post-V1):**
- Real-time email API integration
- Automated CRM sync
- Machine learning for scoring
- Predictive follow-up timing
- Conversation auto-response suggestions
- Email template library

---

**Key Principle**: Your inbox is your lead source.
Treat inbound with respect and urgency. The best
opportunities come from people who reach out to you.
Build systems to find them fast and respond faster.
