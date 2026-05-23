---
name: funnel-metric-mapping
description: Use when designing dashboards or defining product metrics - decomposes user journey into lifecycle stages (Reach → Activation → Engagement → Retention) with stage-appropriate metrics and identifies value creation/loss at transitions
---

# Funnel-Based Metric Mapping

## Purpose

Structure metrics along the user journey to ensure comprehensive coverage of product health. Identifies where users find value, where they drop off, and how different stages connect to create growth flywheels.

## When to Use This Skill

Activate automatically when:
- Designing dashboards to monitor product health
- Defining success metrics for new products/features
- Diagnosing where users drop off in the journey
- `metrics-definition` workflow needs to decompose user journey
- `dashboard-design` workflow structures metrics by lifecycle
- Need holistic view beyond single North Star metric
- Identifying gaps in current measurement approach

**When NOT to use:**
- Feature is too small to have a multi-stage journey
- User journey is non-sequential (pure utility tools)
- Only measuring single point-in-time outcome

## The Standard Funnel Stages

### Stage 1: Reach
**Definition:** Users become aware of and access your product

**Appropriate Metrics:**
- App downloads
- Website visits
- Sign-up page views
- Marketing campaign impressions
- Referral link clicks

**What matters:** Volume of potential users entering top of funnel

**Example (Uber Drivers):** Driver app downloads

### Stage 2: Activation
**Definition:** Users complete setup and reach "first value" moment

**Appropriate Metrics:**
- Profile completion rate
- Registration → "ready to use" conversion
- Time to first value action
- Onboarding completion rate
- Setup abandonment rate

**What matters:** Efficiency of converting reach to active usage

**Example (Uber Drivers):** Profile setup completion, background check passed, ready to drive

### Stage 3: Engagement (Active Usage)
**Definition:** Users perform core product actions regularly

**Appropriate Metrics:**
- Daily/Weekly/Monthly Active Users (DAU/WAU/MAU)
- Time spent in product
- Core actions per session
- Feature adoption rates
- Session frequency

**What matters:** Breadth of usage, how often users return

**Example (Uber Drivers):** Time spent browsing app, earnings page clicks (intent signal)

### Stage 4: Engagement (Depth)
**Definition:** Users complete valuable transactions or deep interactions

**Appropriate Metrics:**
- Transactions per period
- Messages sent (quality interactions)
- Content created
- Successful completions
- Value realization events

**What matters:** Depth of engagement, actual value exchange

**Example (Uber Drivers):** Rides accepted and completed, cash-outs (value realization)

### Stage 5: Retention
**Definition:** Users return repeatedly over extended time periods

**Appropriate Metrics:**
- Weekly/Monthly returning user rate
- Churn rate
- Lifetime value (LTV)
- Cohort retention curves
- Days active per month

**What matters:** Long-term stickiness, habit formation

**Example (Uber Drivers):** Weekly rides per driver, hours driven per month, month-over-month active drivers

## Funnel Variations by Product Type

### Two-Sided Marketplaces
**Critical:** Measure BOTH sides separately

**Supply Side Example (Uber Drivers):**
- Reach: Driver app downloads
- Activation: Profile complete, ready to drive
- Engagement: Hours online, rides accepted
- Retention: Monthly active drivers

**Demand Side Example (Uber Riders):**
- Reach: Rider app downloads
- Activation: Account created, payment added
- Engagement: Rides requested per week
- Retention: Monthly active riders

**Balance Metric:** Supply/demand ratio by geography and time

### Content Platforms
**Focus:** Creation vs. consumption

**Creator Funnel:**
- Reach: Sign-ups
- Activation: First post/video/story
- Engagement: Posts per week
- Retention: Creators active monthly

**Consumer Funnel:**
- Reach: App opens
- Activation: Follow first creator
- Engagement: Time spent viewing content
- Retention: Daily active users

**Key Insight:** Creator side drives demand side (more content = more engagement)

### SaaS Products
**Focus:** Trial to paid conversion

**User Funnel:**
- Reach: Trial sign-ups
- Activation: Core feature used (aha moment)
- Engagement: Weekly active usage
- Retention: Subscription renewals

**Account Expansion:**
- Seat additions
- Feature tier upgrades
- Contract expansions

## Identifying Flywheel Dynamics

**Definition:** Outputs of one stage feed inputs of another, creating self-reinforcing growth

### Example 1: Social Media Flywheel (Snapchat)

```
Stories Shared → Notifications to Friends → Friend Opens App → Friend Sends Message → 
Original User Gets Notification → Opens App → Creates More Stories → [LOOP]
```

**Critical Metrics:**
- Stories shared per user (creates notifications)
- Messages sent (creates reciprocal engagement)
- Notifications received (drives app opens)

**What Breaks It:**
- Reduced story sharing → Fewer notifications → Less app opening
- Snapchat redesign example: Time on creator content ↑ but messages ↓ = broken flywheel

### Example 2: Marketplace Flywheel (Uber)

```
More Drivers → Shorter Wait Times → More Riders → More Driver Earnings → 
More Drivers Want to Join → [LOOP]
```

**Critical Metrics:**
- Driver supply (hours online per geography)
- Wait time (demand-side experience)
- Rides per driver (earnings proxy)
- New driver sign-ups (supply growth)

**What Breaks It:**
- Poor driver experience → Driver churn → Longer wait times → Rider churn

### Example 3: Content Platform Flywheel (YouTube)

```
More Creators → More Content Variety → More Viewers → Better Creator Earnings → 
More Creators Join → [LOOP]
```

**Critical Metrics:**
- New creators per month
- Content upload frequency
- Viewer watch time
- Creator monetization rate

**What Breaks It:**
- Algorithm favors passive consumption over discovery → Fewer creator views → Creator churn

## Transition Analysis: Where Value Is Lost

**Purpose:** Identify biggest drop-offs and opportunities

### Conversion Rates Between Stages

Calculate:
- Reach → Activation: % who complete setup
- Activation → Engagement: % who perform core action
- Engagement → Retention: % who return next period

**Red flags:**
- <20% reach to activation: Onboarding friction
- <50% activation to engagement: "Aha moment" not compelling
- <40% engagement to retention: Value not sustained

### Time-to-Conversion

Measure:
- Time from download to first value
- Time from sign-up to daily habit
- Time from trial to paid conversion

**Benchmarks vary by category:**
- Consumer social: Minutes to first value
- B2B SaaS: Days/weeks to first value
- Marketplaces: Hours to first transaction

## Balancing Quantity vs. Quality

**Challenge:** More users doesn't always mean more value

### Quality Indicators by Stage

**Activation Quality:**
- % who reach "aha moment" vs. just complete setup
- Depth of profile completion
- Speed to first value action

**Engagement Quality:**
- Two-way interactions vs. one-way consumption
- Deep actions vs. shallow browsing
- Value-creating behaviors vs. vanity metrics

**Retention Quality:**
- Power users (top quartile activity) vs. marginal users
- Paying customers vs. free users
- Advocates (NPS promoters) vs. detractors

### Example: Uber Driver Quality Funnel

Instead of flat funnel, bucket by quality:

**Reach:** All driver applicants
**Activation (tiered):**
- Tier 1: Profile complete
- Tier 2: Background check passed
- Tier 3: First ride completed

**Engagement (tiered by rating):**
- 4.5-4.74: Active drivers
- 4.75-5.0: High-quality drivers  
- 5.0 + tips: Exceptional drivers

**Goal:** Maximize hours driven in highest quality tiers

## Workflow Steps

### 1. Map User Journey

Ask:
- What's the first touchpoint with your product?
- What setup/configuration is required?
- What's the core value action?
- How do users build habits?

Sketch journey stages.

### 2. Assign Metrics to Stages

For each stage:
- What defines success at this stage?
- What's the key conversion event?
- What volume metric matters?
- What quality indicator matters?

List 1-3 metrics per stage.

### 3. Identify Transitions

Between each stage:
- What's the conversion rate?
- How long does transition take?
- What causes drop-off?
- What accelerates progress?

Calculate or estimate conversion rates.

### 4. Find Flywheel Connections

Ask:
- Does output of Stage N feed input of Stage M?
- Are there network effects?
- Does supply create demand or vice versa?
- What virtuous cycles exist?

Map feedback loops.

### 5. Prioritize Metrics

From comprehensive list:
- Which 1-2 metrics per stage are most actionable?
- Which transitions have worst conversion rates?
- Which flywheel connections are weakest?

Create prioritized metrics dashboard.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Only measuring final stage (retention) | Cover all stages to find drop-off points |
| Same metric for all stages | Use stage-appropriate metrics |
| Ignoring quality, only measuring quantity | Add quality indicators at each stage |
| Not calculating transition rates | Measure conversion between stages |
| Missing flywheel dynamics | Identify feedback loops and network effects |
| Flat funnel for two-sided markets | Separate funnels for each market side |

## Anti-Rationalization Blocks

| Rationalization | Reality |
|-----------------|---------|
| "We only care about retention" | Can't fix retention without understanding earlier stages |
| "Our product doesn't have stages" | Every product has awareness → usage → habit |
| "Activation metrics are obvious" | Define precisely what "activated" means |
| "Quality doesn't matter yet" | Quality users drive retention and flywheel effects |
| "Funnel is linear" | Real funnels have loops and feedback effects |

## Success Criteria

Funnel-based metric mapping succeeds when:
- All 4-5 major lifecycle stages identified
- 1-3 metrics assigned to each stage
- Stage-appropriate metric types used (volume for reach, quality for retention)
- Transition conversion rates estimated or measured
- Flywheel dynamics identified and measured
- Two-sided markets have separate funnels per side
- Quality indicators complement quantity metrics
- Prioritization complete (not all metrics are equal)

## Real-World Examples

### Example 1: Uber Driver Funnel

**Reach:**
- Driver app downloads
- Referral link clicks

**Activation:**
- Profile completion rate: 70%
- Background check pass rate: 85%
- Time to first ride: 5 days (median)

**Engagement (Breadth):**
- Weekly active drivers
- Hours online per week
- Earnings page views (intent signal)

**Engagement (Depth):**
- Rides accepted per week
- Acceptance rate: 90%+
- Cash-outs per month (value realization)

**Retention:**
- Monthly active drivers
- Hours driven per month
- Month-over-month retention rate: 80%

**Quality Dimensions:**
- Rating buckets: 4.5-4.74, 4.75-5.0, 5.0+ with tips
- Goal: Maximize hours in 5.0+ bucket

**Flywheel:** More quality drivers → Shorter wait times → More riders → More earnings per driver → Driver retention ↑

### Example 2: Facebook Dating Funnel

**Reach:**
- Users who view dating tab
- Dating profile views

**Activation:**
- Profile created and complete
- First match made
- Time to first match: 24 hours

**Engagement (Breadth):**
- Weekly active dating users
- Profile views per user
- Swipes per session

**Engagement (Depth):**
- Matches per user per week
- Two-message conversations (quality interaction)
- Messages per conversation

**Retention:**
- Week-over-week returning users
- Days active per month

**Counter-metrics (Cannibalization):**
- Facebook main feed engagement
- Timeline posts per day

**Flywheel:** Matches → Conversations → Satisfied users → Tell friends → More users join → Better match pool → More matches

**What could break it:** Users succeed and leave (find partner), need constant new user influx

### Example 3: Airbnb Guest Check-in Journey

**Reach:**
- Booking confirmation received

**Activation:**
- 2-3 day reminder acknowledged
- Check-in instructions received

**Engagement (Check-in Process):**
- Questions sent to host (INVERSE metric - lower is better)
- Host response lag time (lower is better)
- Time from arrival vicinity to WiFi connected

**Engagement (During Stay):**
- In-stay messages (operational questions - lower is better)
- Amenity usage
- Length of stay

**Retention:**
- Rebook rate (same guest books another Airbnb)
- Days to next booking
- Lifetime bookings per guest

**Flywheel:** Seamless check-in → Great stay experience → 5-star review → Host reputation ↑ → More bookings → Host stays on platform

### Example 4: YouTube Homepage Feature

**Reach:**
- Users who land on homepage
- Homepage impressions

**Activation:**
- % scrolling down homepage (exploration)
- % clicking any video from homepage

**Engagement (Breadth):**
- Videos clicked per homepage visit
- Save-to-watch-later clicks
- New genre exploration rate

**Engagement (Depth):**
- Watch time from homepage-sourced videos
- % completing videos found on homepage
- Return visits to homepage

**Retention:**
- Daily active users (platform-wide)
- Homepage visit frequency

**Mission Alignment (Beyond Metrics):**
- % discovering new genres/interests
- Diversity of content consumed
- Educational content engagement

**Flywheel:** Better recommendations → More clicks → More watch time → Better algorithm training → Better recommendations

## Related Skills

- **north-star-alignment**: Ensures funnel metrics ladder up to company goals
- **proxy-metric-selection**: Creates measurable proxies for each funnel stage
- **tradeoff-evaluation**: Resolves conflicts when optimizing different funnel stages
- **root-cause-diagnosis**: Uses funnel location to narrow problem scope
- **metrics-definition** (workflow): Uses funnel mapping as Step 2
- **dashboard-design** (workflow): Structures dashboard by funnel stages

## Integration Points

**Called by workflows:**
- `metrics-definition` - Step 2: Decompose user journey into funnel stages
- `dashboard-design` - Step 2: Ensure coverage across lifecycle stages
- `tradeoff-decision` - Step 4: Identify where in funnel problem occurs

**Works with:**
- `north-star-alignment` to connect funnel metrics to company goals
- `proxy-metric-selection` to create measurable indicators per stage
- `meeting-synthesis` to find customer evidence of friction points

