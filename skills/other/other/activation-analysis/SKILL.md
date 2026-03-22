---
name: activation-analysis
description: Analyze user activation using Setup → Aha → Habit framework. Identifies activation bottlenecks.
disable-model-invocation: false
user-invocable: true
---

# Activation Analysis: Setup → Aha → Habit Framework

## Quick Start

```
/activation-analysis
```
Then provide:
1. **Your product** and core value proposition (or I'll pull from business-info)
2. **Current onboarding flow** (what steps do new users take?)
3. **Any metrics you have** (setup completion %, D7 retention, time-to-value)

I'll diagnose your activation funnel using Setup -> Aha -> Habit,
identify the biggest bottleneck, and recommend specific fixes.

**Output:** Saved to `outputs/analyses/activation-analysis-[date].md`
**Time:** ~15 min with data, ~25 min if defining stages from scratch

**When to use:** When diagnosing activation problems, improving onboarding, or measuring early product engagement

**Framework source:** Aakash Gupta's "Ultimate Guide to Activation" and "How to Measure Onboarding"

## Context Routing Logic (Internal - for Claude)

**Automatic Context Checks:**
When this skill is invoked, immediately check:

| Source | Files/Folders | Search Terms | What to Extract |
|--------|---------------|--------------|-----------------|
| Metrics/Analytics | `context-library/metrics/*.md` | "onboarding", "setup", "activation", D7, D30, "time to value", TTV | Current activation rates by stage, onboarding metrics, D7/D30 retention |
| User Research | `context-library/research/*.md` | "onboarding", "setup", "first time", "confused", "stuck", "struggle" | User feedback on onboarding, confusion points, success moments |
| Meeting Notes | `context-library/meetings/*.md` | "activation", "onboarding", "new users", "drop-off", "support tickets" | CS/support feedback on where users get stuck, win/loss reasons |
| PRDs | `context-library/prds/*.md` | "onboarding", "activation", "tutorial", "first-time user" | Past onboarding improvements, features to drive activation |
| Business Info | `context-library/business-info-template.md` | target user, customer segment, use case, primary value | Who you're activating, what value matters to them |

**Context Priority:**
1. Internal context FIRST (business info, existing activation metrics, user research)
2. Analytics MCP SECOND (if connected - query activation funnel, D7/D30 by cohort)
3. Framework guidance LAST (generic activation tactics)

**Cross-Skill Links:**
- If retention issues mentioned → Link to `retention-analysis`
- If expansion opportunities found → Link to `expansion-strategy`
- If user struggles identified → Link to `user-research-synthesis`

---

## Step 0: Understanding Your Current Activation Landscape

Before measuring the Setup → Aha → Habit stages, let me check what data already exists...

**Checking:**
- `context-library/business-info-template.md` for your product and target users
- `context-library/metrics/` for existing activation metrics and onboarding data
- `context-library/research/` for user research on onboarding struggles
- `context-library/meetings/` for CS/support feedback on where users get stuck
- `context-library/prds/` for past onboarding improvements

**[If analytics MCP connected]:** "Let me also query [Amplitude/Mixpanel] for your current activation funnel, setup completion rates, and D7/D30 retention by cohort."

**Based on what I find, I'll show you:**

### Internal Intelligence Summary

**From Business Info:**
- [Your product and core value proposition]
- [Target user segments]
- [Primary use case]
- Example: "Help product: [description], target: small teams, primary value: [outcome]"

**From Metrics/Analytics:**
- [Current setup completion rate]
- [Current Aha rate (if defined)]
- [D7/D30 retention by cohort]
- [Time to Aha median]
- Example: "Setup: 65%, Aha: 40% (overall activation: 26%), D7 retention: 35%"

**From User Research:**
- [User feedback on onboarding friction]
- [What makes successful users different]
- Example: "Users who complete setup in <5 min have 3x higher D30 retention"

**From Sales/CS Meetings:**
- [Drop-off points where users get stuck]
- [Common confusion or support tickets]
- Example: "70% of support tickets in first week are about [feature]"

**From PRDs:**
- [Past onboarding improvements and their impact]
- Example: "PRD-2024-02 added templates, increased setup completion by 8%"

### Gaps in Knowledge

Based on internal context, we **don't yet know:**
- [Gap 1]: Exact definition of your Aha moment (based on user behavior data)
- [Gap 2]: Drop-off points in your setup flow
- [Gap 3]: Why churned users didn't persist (need churn interview analysis)

**Should I help define your three stages, or would you like to provide existing activation data first?**

---

## Step 1: Activation Diagnostic Questions

Instead of generic "what's your onboarding flow," I'll ask:

### Question 1: The Biggest Leak
**"Where do most new users drop off—in the first 5 minutes, or later in the week?"**

This identifies whether the problem is setup friction, Aha not resonating, or habit formation.

### Question 2: Aha Moment Evidence
**"Among users who stuck around (D7+), what did they all do in their first session that churned users didn't?"**

Your Aha must be defined by actual user behavior, not guesses.

### Question 3: Onboarding Goals
**"What specific actions should every new user complete in their first session to get value?"**

This defines your Setup stage.

### Question 4: Success Signal
**"How do you know a user 'got it'—what behavior indicates they experienced the core value?"**

This is your Aha moment definition.

### Question 5: Current Metrics
**"What % of new signups complete your onboarding, and what % come back on Day 7?"**

These baselines inform where to focus.

---

## Overview

Activation is the bridge between signup and retention.

The Setup → Aha → Habit framework breaks activation into three measurable stages:

1. **Setup:** User configures the product to work for them
2. **Aha:** User experiences the core value (magic moment)
3. **Habit:** User turns that value into recurring behavior

---

## The Framework

### Stage 1: Setup

**What it is:** The initial configuration required before a user can experience value

**Examples by product type:**
- **Slack:** Create workspace, invite team members, set up channels
- **Notion:** Create first page, set up workspace structure
- **Figma:** Create first file, invite collaborators
- **Stripe:** Connect bank account, configure payment settings
- **TaskFlow** (example): Create first project, add team members, create first task

**Key principle:** Setup should be the MINIMUM required to reach Aha

**Metrics to track:**
- Setup completion rate
- Time to setup completion
- Drop-off points in setup flow

---

### Stage 2: Aha

**What it is:** The moment when the user experiences your product's core value for the first time

**How to find your Aha moment:**
1. Look at retained vs churned users
2. What did retained users do that churned users didn't?
3. That differentiating action is your Aha

**Examples by product:**
- **Slack:** Sent 2,000 messages (team-wide)
- **Dropbox:** Put at least 1 file in 1 folder on 1 device
- **Facebook:** Add 7 friends in 10 days
- **Airbnb:** Book 1 trip
- **LinkedIn:** Make 5 connections
- **TaskFlow** (example): Complete first task with team member

**Aha characteristics:**
- ✅ Directly tied to core product value
- ✅ Measurable and clear
- ✅ Achievable within first session (or first week)
- ✅ Predictive of retention

**Metrics to track:**
- Aha completion rate (% of setups → Aha)
- Time to Aha (from signup)
- Correlation between Aha and D7/D30 retention

---

### Stage 3: Habit

**What it is:** Recurring behavior pattern that cements long-term retention

**Why it matters:**
- One-time Aha isn't enough
- Habit is what separates million-dollar companies from billion-dollar companies
- Habit = predictable retention

**Examples by product:**
- **Slack:** Daily active usage, multiple messages per day
- **Notion:** Weekly return to update docs
- **Figma:** Multiple files created per week
- **TaskFlow** (example): Daily task updates, weekly task creation

**Habit = Frequency + Value Pattern**

**Metrics to track:**
- % of Aha users who return (Day 7, Day 14, Day 30)
- Weekly Active Users (WAU) or Daily Active Users (DAU)
- Frequency of core action (e.g., tasks created per week)
- L28 (28-day retention cohort)

---

## How to Use This Framework

### Step 1: Define Your Three Stages

Use this prompt pattern:

```
Use /activation-analysis and reference context-library/business-info-template.md

Help me define the Setup → Aha → Habit stages for my product.

Our product: [describe your product]
Core value proposition: [what value do users get]
Current onboarding flow: [describe existing flow]

For each stage, help me identify:
1. What actions constitute this stage?
2. What should we measure?
3. Where are users dropping off?
```

---

### Step 2: Measure Each Stage

**Calculate these metrics:**

```
Setup Rate = (Users who complete setup) / (Total signups) × 100
Aha Rate = (Users who hit Aha) / (Users who complete setup) × 100
Habit Rate = (Users who form habit) / (Users who hit Aha) × 100

Overall Activation = Setup Rate × Aha Rate × Habit Rate
```

**Example:**
- Setup: 75% (750 of 1000 signups)
- Aha: 60% (450 of 750 setups)
- Habit: 40% (180 of 450 Ahas)
- **Overall Activation: 18%** (180 of 1000 signups)

**Where's the bottleneck?** The biggest drop is your priority.

---

### Step 3: Diagnose Drop-offs

**If Setup is low (<70%):**
- Too much friction in onboarding
- Asking for too much information upfront
- Unclear value proposition
- Technical issues

**If Aha is low (<50%):**
- Users don't understand how to get value
- Aha moment requires too much work
- Wrong users are signing up
- Product value isn't clear enough

**If Habit is low (<30%):**
- Product isn't sticky enough
- No triggers to bring users back
- Value isn't compelling enough for repeat use
- Competing with existing habits

---

### Step 4: Improve Activation

**Use this prioritization:**

1. **Fix the biggest drop first**
   - If 75% drop at Setup → fix Setup
   - If 50% drop at Aha → fix Aha
   - If 60% drop at Habit → fix Habit

2. **For Setup improvements:**
   - Reduce required fields
   - Add progress indicators
   - Provide templates/examples
   - Allow "skip" for non-essential items
   - Use social proof ("Join 10,000 teams...")

3. **For Aha improvements:**
   - Shorten time-to-value
   - Add in-product guidance
   - Provide sample data
   - Create success paths for different user types
   - Make the value obvious

4. **For Habit improvements:**
   - Add email/push notifications
   - Create daily/weekly rituals
   - Build social loops (team activity)
   - Gamification (streaks, achievements)
   - Integration hooks (Slack, email)

---

## Time-to-Value (TTV)

**TTV = Time from signup to Aha moment**

**Why it matters:**
- Faster TTV = Higher activation
- Faster TTV = Better retention
- Benchmark: Best products get users to Aha in <5 minutes

**How to reduce TTV:**

1. **Eliminate unnecessary steps**
   - Question every field in signup
   - Can it happen later? Move it later.

2. **Provide shortcuts**
   - Sample data/templates
   - Import from competitors
   - AI-generated starting points

3. **Progressive disclosure**
   - Show advanced features AFTER Aha
   - Don't overwhelm new users

4. **Different paths for different users**
   - Solo user vs team setup
   - Technical vs non-technical
   - Personal vs work use

---

## Advanced: Cohort Analysis

**Compare activation by cohort:**

```
Use /activation-analysis

I have activation data for the past 3 months:
[paste your data or describe metrics]

Help me analyze:
1. Which cohorts have highest activation?
2. What changed between cohorts?
3. Where should we focus improvement efforts?
```

**Look for:**
- Seasonality (weekday vs weekend signups)
- Channel quality (organic vs paid)
- User segment differences (small vs large teams)
- Feature launch impact (before/after comparisons)

---

## Activation Metrics Dashboard

Track these KPIs weekly:

| Metric | Definition | Target | Current |
|--------|------------|--------|---------|
| Signup → Setup | % who complete setup | 70%+ | ___ |
| Setup → Aha | % who reach Aha moment | 50%+ | ___ |
| Aha → Habit | % who form habit (D7 return) | 30%+ | ___ |
| Overall Activation | Signup → Habit | 15%+ | ___ |
| Time to Aha (median) | Minutes from signup to Aha | <10 min | ___ |
| D7 Retention | % active on Day 7 | 40%+ | ___ |
| D30 Retention | % active on Day 30 | 25%+ | ___ |

---

## Common Mistakes

❌ **Optimizing Aha without fixing Setup**
- If users never complete setup, Aha doesn't matter
- Fix bottlenecks in order

❌ **Defining Aha based on what you WANT users to do**
- Aha must be based on DATA (retained vs churned behavior)
- Not your opinion of what's valuable

❌ **Ignoring Habit formation**
- One-time Aha doesn't predict retention
- Recurring behavior is what matters

❌ **Same onboarding for all user types**
- Solo vs team users have different needs
- Technical vs non-technical users need different paths

❌ **Measuring activation without connecting to retention**
- If your "activated" users don't retain, you defined it wrong
- Always validate activation metrics against retention data

---

## Real-World Examples

### Example 1: Slack

- **Setup:** Create workspace, invite 2+ team members
- **Aha:** Team sends 2,000 messages
- **Habit:** Daily active usage by team
- **Result:** 93% of teams that send 2,000 messages become retained customers

### Example 2: Dropbox

- **Setup:** Install desktop app
- **Aha:** Add 1 file to 1 folder on 1 device
- **Habit:** Weekly file uploads/syncs
- **TTV:** <5 minutes
- **Result:** Simple, clear Aha moment drove explosive growth

### Example 3: LinkedIn

- **Setup:** Complete profile
- **Aha:** Make 5 connections
- **Habit:** Weekly profile views, weekly connection activity
- **Key insight:** Social activation (connections) drove retention

---

## Worksheet: Define Your Activation

Use this with your team:

### 1. Setup Stage
- **Actions required:** ___________
- **Ideal time to complete:** ___________
- **Current completion rate:** ___________
- **Biggest drop-off point:** ___________

### 2. Aha Stage
- **Core value action:** ___________
- **How to measure:** ___________
- **Current Aha rate:** ___________
- **Time to Aha (median):** ___________

### 3. Habit Stage
- **Recurring behavior:** ___________
- **Target frequency:** ___________
- **Current habit formation rate:** ___________
- **D7/D30 retention:** ___________

### 4. Priority Improvement
- **Biggest bottleneck:** ___________
- **Hypothesis to test:** ___________
- **Success metric:** ___________

---

## Output Integration

### Where to Save Your Activation Analysis

**Research & Findings:**
- Save to: `outputs/analyses/activation-analysis-[date].md`
- When finalized, move to: `context-library/research/activation-[product].md`

**Onboarding Improvements:**
- Create PRD in `context-library/prds/` for each onboarding change
- Link this activation analysis as context
- Track changes in the PRD's success metrics section

**Activation Metrics:**
- Update `context-library/metrics/` with your Setup, Aha, Habit definitions and rates
- Track weekly changes as baseline for comparison

### Cross-Skill Integration

**Feeds into:**
- `/retention-analysis` - Activation rate by stage informs retention analysis (Aha users retain better)
- `/prd-draft` - Onboarding improvements become features in PRDs
- `/experiment-decision` - Test setup flow changes or Aha moment triggers
- `/metrics-framework` - Define leading indicators (setup rate, Aha rate as early signals)

**Pulls from:**
- `/user-research-synthesis` - User feedback on onboarding struggles
- `/retention-analysis` - Understand habit formation patterns
- `/competitor-analysis` - How competitors handle onboarding
- `/expansion-strategy` - Activation enables expansion (activated users more likely to expand)

### Key Questions to Revisit

After defining Setup → Aha → Habit, ask:
- Is our Aha moment definition based on DATA (retained vs churned behavior)?
- What's the time-to-Aha for our fastest 10% of users (that's the optimized path)?
- Do we have different Aha moments for different user segments (solo vs team)?
- Is our setup flow truly minimal, or are we collecting unnecessary info upfront?

---

## Related Skills

- `user-research-synthesis` - Understand user struggles in onboarding, synthesis of feedback
- `experiment-decision` - Test activation improvements and measure impact
- `retention-analysis` - Measure habit formation (Aha → habit stage)
- `prd-draft` - Build features to improve activation based on this analysis
- `metrics-framework` - Define leading indicators of activation success
- `expansion-strategy` - Activation enables expansion (prerequisite)
- `define-north-star` - Align activation metrics to North Star

---

## Structured Output Template

When delivering an activation analysis, use this consistent format:

```markdown
# Activation Analysis: [Product/Feature Name]

**Date:** [Date]
**Analyst:** [PM Name]

---

## Executive Summary
[1-2 sentences: Current activation rate, biggest bottleneck, recommended action]

## Current Activation Funnel

| Stage | Definition | Rate | Benchmark | Gap |
|-------|-----------|------|-----------|-----|
| Signup → Setup | [actions] | __% | 70%+ | [+/- vs benchmark] |
| Setup → Aha | [actions] | __% | 50%+ | [+/- vs benchmark] |
| Aha → Habit | [actions] | __% | 30%+ | [+/- vs benchmark] |
| **Overall Activation** | Signup → Habit | __% | 15%+ | [+/- vs benchmark] |

**Time to Aha (median):** __ minutes
**Biggest bottleneck:** [Stage with largest drop]

## Stage Definitions
- **Setup:** [Specific actions for your product]
- **Aha:** [Specific moment/action for your product]
- **Habit:** [Specific recurring behavior for your product]

## Bottleneck Diagnosis
[Root cause of biggest drop-off: friction, confusion, wrong users, missing value]

## Segment Differences
| Segment | Setup Rate | Aha Rate | Habit Rate | Insight |
|---------|-----------|----------|-----------|---------|
| [Segment 1] | __% | __% | __% | [insight] |
| [Segment 2] | __% | __% | __% | [insight] |

## Recommendations (Prioritized)
1. **[Fix 1]** - Expected impact: +__% on [stage] rate
2. **[Fix 2]** - Expected impact: +__% on [stage] rate
3. **[Fix 3]** - Expected impact: +__% on [stage] rate

## Next Steps
- [ ] [Action 1] - Owner: [name] - Due: [date]
- [ ] [Action 2] - Owner: [name] - Due: [date]
```

---

## Output Quality Self-Check

Before delivering the activation analysis, verify:

- [ ] **All three stages** (Setup, Aha, Habit) are defined with specific, measurable actions for this product
- [ ] **Aha moment** is based on data (retained vs churned behavior), not opinion
- [ ] **Rates calculated** for each stage with clear numerator/denominator
- [ ] **Biggest bottleneck** is identified and the diagnosis explains WHY (not just where)
- [ ] **Time to Aha** is measured or estimated
- [ ] **Segment differences** are analyzed (at least new vs existing, or by acquisition channel)
- [ ] **Recommendations** are specific, prioritized, and tied to the bottleneck
- [ ] **Benchmarks** are included for context (industry-appropriate, not generic)
- [ ] **Connected to retention** -- does activation actually predict D30 retention?
- [ ] **No generic advice** -- all recommendations reference this specific product and data

---

**Framework credit:** Adapted from Aakash Gupta's activation frameworks. Read the full articles:
- https://www.news.aakashg.com/p/ultimate-guide-activation
- https://www.news.aakashg.com/p/how-to-measure-onboarding-advanced
