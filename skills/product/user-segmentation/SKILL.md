---
name: user-segmentation
description: Framework for clustering users into behavioral segments and personas. Use when analyzing user cohorts, identifying patterns, and personalizing product features.
---

# User Segmentation Skill

Cluster users into actionable segments based on behavioral patterns and usage data.

## When to Use

Use this skill when you need to:
- Understand different user types in your product
- Identify high-value vs. at-risk users
- Personalize features for specific segments
- Prioritize product improvements by user impact
- Track segment migration over time (churn, activation, etc.)
- Create targeted interventions for specific user groups

## Segmentation Framework

### The Three Dimensions

Effective user segmentation analyzes behavior across multiple dimensions:

**1. Engagement Level** (Frequency & Recency)
- How often do they use the product?
- When did they last use it?

**2. Feature Usage** (Breadth)
- What features do they use?
- Do they use one feature or many?

**3. Value Signals** (Quality)
- Do they provide feedback (reactions, reviews)?
- Do they refer others or upgrade?

**Combine these dimensions to create personas** - users who share similar behavioral patterns across all three.

---

## SQL Templates

### Query 1: Raw Behavioral Metrics

**Purpose:** Gather raw data for each user across all dimensions

```sql
-- User Behavioral Metrics
-- Calculates engagement, feature usage, and value signals for each user

WITH user_activity AS (
  SELECT
    p.id as person_id,
    p.name,

    -- ENGAGEMENT METRICS
    COUNT(DISTINCT m.id) as total_messages_sent,
    COUNT(DISTINCT CASE WHEN m.provider_timestamp >= NOW() - INTERVAL '30 days' THEN m.id END) as messages_last_30d,
    COUNT(DISTINCT CASE WHEN m.provider_timestamp >= NOW() - INTERVAL '7 days' THEN m.id END) as messages_last_7d,
    NOW()::date - MAX(m.provider_timestamp)::date as days_since_last_message,

    -- FEATURE USAGE METRICS
    COUNT(DISTINCT CASE WHEN c.type = 'ONE_ON_ONE' THEN m.id END) as messages_1on1,
    COUNT(DISTINCT CASE WHEN c.type = 'GROUP' THEN m.id END) as messages_group,

    -- VALUE SIGNAL METRICS
    COUNT(DISTINCT CASE
      WHEN m.content LIKE 'Loved %' OR m.content LIKE 'Liked %' OR m.content LIKE 'Disliked %'
      THEN m.id
    END) as total_reactions,

    -- TIME PATTERNS (optional)
    AVG(EXTRACT(HOUR FROM m.provider_timestamp))::int as avg_hour_of_day,
    MAX(m.provider_timestamp)::date as last_message_date

  FROM persons p
  LEFT JOIN person_contacts pc ON pc.person_id = p.id
  LEFT JOIN message m ON m.sender_person_contact_id = pc.id
  LEFT JOIN conversation c ON m.conversation_id = c.id
  WHERE p.name NOT LIKE '%Coach%'
    AND p.name NOT LIKE '%Codel%'
    AND p.name NOT LIKE '%Wren%'
  GROUP BY p.id, p.name
  HAVING COUNT(DISTINCT m.id) > 10  -- Filter out users with insufficient data
)
SELECT
  person_id,
  name,
  total_messages_sent,
  messages_last_30d,
  messages_last_7d,
  total_reactions,
  messages_1on1,
  messages_group,
  last_message_date,
  days_since_last_message,

  -- CALCULATED SEGMENTS

  -- Engagement Level
  CASE
    WHEN messages_last_7d >= 50 THEN 'Very Active'
    WHEN messages_last_7d >= 20 THEN 'Active'
    WHEN messages_last_7d >= 5 THEN 'Moderate'
    WHEN messages_last_30d >= 5 THEN 'Low'
    WHEN days_since_last_message <= 60 THEN 'Inactive'
    ELSE 'Churned'
  END as engagement_level,

  -- Reaction Behavior (Value Signal)
  CASE
    WHEN total_reactions >= 10 THEN 'Power Reactor'
    WHEN total_reactions >= 3 THEN 'Regular Reactor'
    WHEN total_reactions >= 1 THEN 'Occasional Reactor'
    ELSE 'Non-Reactor'
  END as reaction_behavior,

  -- Conversation Preference (Feature Usage)
  CASE
    WHEN messages_1on1 > messages_group * 2 THEN '1:1 Focused'
    WHEN messages_group > messages_1on1 * 2 THEN 'Group Focused'
    WHEN messages_1on1 > 0 AND messages_group > 0 THEN 'Balanced'
    WHEN messages_1on1 > 0 THEN '1:1 Only'
    ELSE 'Group Only'
  END as conversation_preference

FROM user_activity
ORDER BY total_messages_sent DESC
LIMIT 100;
```

**How to Use:**
```bash
arsenal/dot-claude/skills/sql-reader/connect.sh "
[Paste SQL above]
"
```

**Expected Output:** Table with each user's raw metrics and their segment assignments

---

### Query 2: Segment Distribution Summary

**Purpose:** Understand how users are distributed across segments

```sql
-- Segment Distribution Summary
-- Shows percentage of users in each segment

WITH user_activity AS (
  SELECT
    p.id as person_id,
    COUNT(DISTINCT m.id) as total_messages_sent,
    COUNT(DISTINCT CASE WHEN m.provider_timestamp >= NOW() - INTERVAL '7 days' THEN m.id END) as messages_last_7d,
    COUNT(DISTINCT CASE WHEN m.provider_timestamp >= NOW() - INTERVAL '30 days' THEN m.id END) as messages_last_30d,
    COUNT(DISTINCT CASE
      WHEN m.content LIKE 'Loved %' OR m.content LIKE 'Liked %' OR m.content LIKE 'Disliked %'
      THEN m.id
    END) as total_reactions,
    COUNT(DISTINCT CASE WHEN c.type = 'ONE_ON_ONE' THEN m.id END) as messages_1on1,
    COUNT(DISTINCT CASE WHEN c.type = 'GROUP' THEN m.id END) as messages_group,
    NOW()::date - MAX(m.provider_timestamp)::date as days_since_last_message
  FROM persons p
  LEFT JOIN person_contacts pc ON pc.person_id = p.id
  LEFT JOIN message m ON m.sender_person_contact_id = pc.id
  LEFT JOIN conversation c ON m.conversation_id = c.id
  WHERE p.name NOT LIKE '%Coach%'
    AND p.name NOT LIKE '%Codel%'
    AND p.name NOT LIKE '%Wren%'
  GROUP BY p.id
  HAVING COUNT(DISTINCT m.id) > 10
),
user_segments AS (
  SELECT
    CASE
      WHEN messages_last_7d >= 50 THEN 'Very Active'
      WHEN messages_last_7d >= 20 THEN 'Active'
      WHEN messages_last_7d >= 5 THEN 'Moderate'
      WHEN messages_last_30d >= 5 THEN 'Low'
      WHEN days_since_last_message <= 60 THEN 'Inactive'
      ELSE 'Churned'
    END as engagement_level,

    CASE
      WHEN total_reactions >= 10 THEN 'Power Reactor'
      WHEN total_reactions >= 3 THEN 'Regular Reactor'
      WHEN total_reactions >= 1 THEN 'Occasional Reactor'
      ELSE 'Non-Reactor'
    END as reaction_behavior,

    CASE
      WHEN messages_1on1 > messages_group * 2 THEN '1:1 Focused'
      WHEN messages_group > messages_1on1 * 2 THEN 'Group Focused'
      WHEN messages_1on1 > 0 AND messages_group > 0 THEN 'Balanced'
      WHEN messages_1on1 > 0 THEN '1:1 Only'
      ELSE 'Group Only'
    END as conversation_preference
  FROM user_activity
)
SELECT
  '=== ENGAGEMENT LEVEL DISTRIBUTION ===' as metric, '' as segment, 0 as user_count, 0.0 as percentage
UNION ALL
SELECT
  'Engagement' as metric,
  engagement_level as segment,
  COUNT(*) as user_count,
  ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER(), 1) as percentage
FROM user_segments
GROUP BY engagement_level

UNION ALL
SELECT '=== REACTION BEHAVIOR DISTRIBUTION ===' as metric, '' as segment, 0 as user_count, 0.0 as percentage

UNION ALL
SELECT
  'Reaction' as metric,
  reaction_behavior as segment,
  COUNT(*) as user_count,
  ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER(), 1) as percentage
FROM user_segments
GROUP BY reaction_behavior

UNION ALL
SELECT '=== CONVERSATION PREFERENCE DISTRIBUTION ===' as metric, '' as segment, 0 as user_count, 0.0 as percentage

UNION ALL
SELECT
  'Conversation' as metric,
  conversation_preference as segment,
  COUNT(*) as user_count,
  ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER(), 1) as percentage
FROM user_segments
GROUP BY conversation_preference

ORDER BY metric, user_count DESC;
```

**Expected Output:**
```
=== ENGAGEMENT LEVEL DISTRIBUTION ===
Engagement | Churned        | 37 | 39.4%
Engagement | Inactive       | 17 | 18.1%
Engagement | Very Active    | 15 | 16.0%
...

=== REACTION BEHAVIOR DISTRIBUTION ===
Reaction   | Non-Reactor    | 42 | 44.7%
Reaction   | Power Reactor  | 34 | 36.2%
...

=== CONVERSATION PREFERENCE DISTRIBUTION ===
Conversation | Group Focused | 72 | 76.6%
Conversation | 1:1 Focused   | 14 | 14.9%
...
```

---

### Query 3: User Personas (Combined Dimensions)

**Purpose:** Create actionable user personas by combining all dimensions

```sql
-- User Personas: Combined Multi-Dimensional Segments
-- Creates archetypal users by combining engagement, feature usage, and value signals

WITH user_activity AS (
  SELECT
    p.id as person_id,
    p.name,
    COUNT(DISTINCT m.id) as total_messages_sent,
    COUNT(DISTINCT CASE WHEN m.provider_timestamp >= NOW() - INTERVAL '7 days' THEN m.id END) as messages_last_7d,
    COUNT(DISTINCT CASE WHEN m.provider_timestamp >= NOW() - INTERVAL '30 days' THEN m.id END) as messages_last_30d,
    COUNT(DISTINCT CASE
      WHEN m.content LIKE 'Loved %' OR m.content LIKE 'Liked %' OR m.content LIKE 'Disliked %'
      THEN m.id
    END) as total_reactions,
    COUNT(DISTINCT CASE WHEN c.type = 'ONE_ON_ONE' THEN m.id END) as messages_1on1,
    COUNT(DISTINCT CASE WHEN c.type = 'GROUP' THEN m.id END) as messages_group,
    NOW()::date - MAX(m.provider_timestamp)::date as days_since_last_message,
    AVG(EXTRACT(HOUR FROM m.provider_timestamp))::int as avg_hour_of_day
  FROM persons p
  LEFT JOIN person_contacts pc ON pc.person_id = p.id
  LEFT JOIN message m ON m.sender_person_contact_id = pc.id
  LEFT JOIN conversation c ON m.conversation_id = c.id
  WHERE p.name NOT LIKE '%Coach%'
    AND p.name NOT LIKE '%Codel%'
    AND p.name NOT LIKE '%Wren%'
  GROUP BY p.id, p.name
  HAVING COUNT(DISTINCT m.id) > 10
),
user_personas AS (
  SELECT
    person_id,
    name,
    total_messages_sent,
    total_reactions,

    -- PERSONA ASSIGNMENT LOGIC
    -- Priority matters - first match wins
    CASE
      -- Power Users: Very active + Power reactors
      WHEN messages_last_7d >= 50 AND total_reactions >= 10
        THEN 'Power User'

      -- Engaged Couples: Very active in group chats
      WHEN messages_last_7d >= 20 AND messages_group > messages_1on1 * 2
        THEN 'Engaged Couple'

      -- 1:1 Seekers: Prefer coaching over couple chat
      WHEN messages_1on1 > messages_group * 2
        THEN '1:1 Coaching Seeker'

      -- Feedback Givers: High reaction ratio to message ratio
      WHEN total_reactions::float / NULLIF(total_messages_sent, 0) > 0.1
        THEN 'Feedback Giver'

      -- Lurkers: Active but rarely react
      WHEN messages_last_30d >= 20 AND total_reactions < 3
        THEN 'Active Lurker'

      -- At Risk: Was active but declining
      WHEN days_since_last_message BETWEEN 14 AND 60 AND total_messages_sent > 100
        THEN 'At Risk Churn'

      -- Churned: Haven't used in 60+ days
      WHEN days_since_last_message > 60
        THEN 'Churned'

      -- Casual Users: Low volume, occasional use
      WHEN messages_last_30d < 20 AND total_messages_sent > 50
        THEN 'Casual User'

      -- New Users: Recently joined, still exploring
      WHEN total_messages_sent < 100 AND days_since_last_message <= 30
        THEN 'New User'

      ELSE 'Other'
    END as persona,

    messages_last_7d,
    messages_1on1,
    messages_group,
    days_since_last_message,
    avg_hour_of_day
  FROM user_activity
)
SELECT
  persona,
  COUNT(*) as user_count,
  ROUND(AVG(total_messages_sent)::numeric) as avg_total_messages,
  ROUND(AVG(total_reactions)::numeric) as avg_reactions,
  ROUND(AVG(messages_last_7d)::numeric) as avg_weekly_messages,
  ROUND((100.0 * AVG(messages_1on1::float / NULLIF(total_messages_sent, 0)))::numeric, 1) as pct_1on1,
  ROUND(AVG(avg_hour_of_day)::numeric) as avg_active_hour,
  STRING_AGG(name, ', ' ORDER BY total_messages_sent DESC) FILTER (WHERE total_messages_sent > 500) as top_users
FROM user_personas
GROUP BY persona
ORDER BY user_count DESC;
```

**Expected Output:**
```
persona             | user_count | avg_total_messages | avg_reactions | avg_weekly_messages | pct_1on1 | avg_active_hour | top_users
--------------------+------------+--------------------+---------------+---------------------+----------+-----------------+-----------------------
Churned             |         27 |                180 |             5 |                   0 |     10.1 |              15 | lynn, anna, yoni
1:1 Coaching Seeker |         14 |                385 |             0 |                  17 |     83.5 |              13 | Matt
Power User          |         11 |               2832 |           234 |                 166 |      3.2 |              13 | craig, amy, mark, vai
Feedback Giver      |         11 |                275 |            38 |                   2 |      3.8 |              14 | karen, ryan
Engaged Couple      |          7 |               1046 |            53 |                  82 |      5.8 |              14 | tracy, greg, arthur
At Risk Churn       |          6 |                821 |            33 |                   0 |      8.9 |              14 | abby, daniel
Other               |          6 |                700 |            24 |                  11 |     24.2 |              13 | samuel, Mallory
Casual User         |          5 |                103 |             0 |                   1 |     32.8 |              12 |
Active Lurker       |          4 |                179 |             0 |                  16 |     23.6 |              14 |
New User            |          3 |                 29 |             0 |                   3 |     16.3 |              13 |
```

---

## Persona Definitions

### Power User 🔥
**Criteria:** messages_last_7d >= 50 AND total_reactions >= 10
**Characteristics:**
- Most active users (166 messages/week average)
- High engagement with product (give lots of feedback)
- Drive product metrics and growth
**Size:** ~12% of active users
**Value:** Extremely high - potential advocates and beta testers
**Product Strategy:**
- Give early access to new features
- Request feedback frequently
- Create referral incentives
- Build community among power users

### Engaged Couple 💑
**Criteria:** messages_last_7d >= 20 AND messages_group > messages_1on1 * 2
**Characteristics:**
- Use product for primary purpose (couple communication)
- Active but not necessarily giving feedback
- Group chat is their main feature
**Size:** ~7% of active users
**Value:** High - using product as intended
**Product Strategy:**
- Focus on group chat features
- Reduce friction in couple workflow
- Measure couple satisfaction metrics

### 1:1 Coaching Seeker 🎯
**Criteria:** messages_1on1 > messages_group * 2
**Characteristics:**
- Prefer private coaching over couple chat (83.5% of messages are 1:1)
- May be using product differently than intended
- Lower weekly volume but consistent
**Size:** ~15% of active users
**Value:** Medium - engaged but different use case
**Product Strategy:**
- Understand why they prefer 1:1 (relationship issues? partner not engaged?)
- Consider 1:1 coaching as separate tier
- May need different pricing model

### Feedback Giver 💬
**Criteria:** total_reactions / total_messages > 0.1
**Characteristics:**
- High reaction-to-message ratio (>10%)
- Provide lots of feedback
- Not necessarily high volume users
**Size:** ~12% of active users
**Value:** High for product development
**Product Strategy:**
- Recruit for user research
- Beta test new features with them
- Create feedback loop / roadmap voting

### Active Lurker 👀
**Criteria:** messages_last_30d >= 20 AND total_reactions < 3
**Characteristics:**
- Active users who rarely provide feedback
- Hard to understand their experience
- Using product but silently
**Size:** ~4% of active users
**Value:** Medium - engaged but unknown satisfaction
**Product Strategy:**
- Survey to understand experience
- Test in-app prompts for feedback
- May be satisfied (don't need to react) or disengaged

### At Risk Churn ⚠️
**Criteria:** days_since_last_message BETWEEN 14 AND 60 AND total_messages_sent > 100
**Characteristics:**
- Were active users (100+ messages historically)
- Haven't used product in 2-8 weeks
- Churn risk
**Size:** ~6% of users
**Value:** High recovery opportunity
**Product Strategy:**
- **URGENT** - Send re-engagement email/SMS
- Offer incentive to return (free month, new feature, etc.)
- Survey to understand why they stopped
- Win-back campaign

### Churned 😔
**Criteria:** days_since_last_message > 60
**Characteristics:**
- Haven't used product in 60+ days
- Likely lost forever
**Size:** ~29% of users
**Value:** Low (cost of recovery > value)
**Product Strategy:**
- Analyze why they churned (exit survey, usage patterns)
- Prevent future churn by fixing root causes
- Low priority for recovery (focus on active users)

### Casual User 🌙
**Criteria:** messages_last_30d < 20 AND total_messages_sent > 50
**Characteristics:**
- Infrequent but consistent use
- Low weekly volume (<20 msgs/month)
- May be in maintenance phase of relationship
**Size:** ~5% of users
**Value:** Medium - paying customers, low engagement
**Product Strategy:**
- Understand their use case (seasonal? busy periods?)
- Offer flexible pricing (pause/resume)
- Don't over-message them

### New User 🌱
**Criteria:** total_messages_sent < 100 AND days_since_last_message <= 30
**Characteristics:**
- Recently signed up
- Still exploring product
- Critical onboarding phase
**Size:** ~3% of users
**Value:** High potential
**Product Strategy:**
- **CRITICAL** - Optimize onboarding
- Measure activation rate (do they become Engaged Couple?)
- Reduce friction in first week
- Set up couple + coach introduction

---

## Analysis Workflow

### Step 1: Run All Three Queries
```bash
# 1. Get raw metrics for each user
arsenal/dot-claude/skills/sql-reader/connect.sh "[Query 1]" > user_metrics.csv

# 2. Get segment distributions
arsenal/dot-claude/skills/sql-reader/connect.sh "[Query 2]" > segment_distribution.txt

# 3. Get user personas
arsenal/dot-claude/skills/sql-reader/connect.sh "[Query 3]" > user_personas.txt
```

### Step 2: Analyze Distribution
Look at segment distribution to understand:
- **What % are churned?** (Health indicator)
- **What % are power users?** (Growth indicator)
- **What % give feedback?** (Product development capacity)

### Step 3: Identify Opportunities
Based on personas, identify:
- **Highest value segments** to double down on
- **At-risk segments** to save
- **Underserved segments** to build for

### Step 4: Create Action Plan
For each persona:
- What features do they need?
- What's their primary pain point?
- How can we increase their value or retention?

---

## Real-World Examples

### Example 1: Personalizing Suggested Responses

**Question:** Should we enable suggested responses by default?

**Analysis:**
1. Run Query 1 to get reaction behavior by user
2. Cross-reference with loved/disliked reactions to suggested responses
3. Discover: Power Reactors love SR, Non-Reactors dislike SR

**Insight:** Make SR opt-in based on reaction behavior segment

**Action:**
- Default OFF for Non-Reactors
- Default ON for Power Reactors
- A/B test for middle segments

### Example 2: Reducing Churn

**Question:** Why are users churning?

**Analysis:**
1. Run Query 3 to identify At Risk Churn segment (n=6, 6% of users)
2. Run custom query to find common patterns:
   - When did they last use product?
   - What was their last message about?
   - What features did they use?

**Insight:** At-risk users stopped after conflict without resolution

**Action:**
- Create intervention when conflict detected but not resolved
- Survey churned users to validate hypothesis
- Build "repair nudge" feature for at-risk couples

### Example 3: Feature Prioritization

**Question:** Should we build group video calls or 1:1 video coaching?

**Analysis:**
1. Run Query 3 to get persona distribution
2. See: Engaged Couple (7 users, 7%) vs 1:1 Coaching Seeker (14 users, 15%)

**Insight:** More users prefer 1:1 coaching, but Engaged Couples are using product as intended

**Decision:**
- Prioritize Engaged Couple features (target use case)
- But investigate why 15% are 1:1 Focused (may be a product issue)

---

## Customization Guide

### Adding New Segments

To add a new segment dimension:

**Step 1: Define the metric**
```sql
-- Example: Add "Time of Day Preference"
AVG(EXTRACT(HOUR FROM m.provider_timestamp))::int as avg_hour_of_day
```

**Step 2: Create classification logic**
```sql
CASE
  WHEN avg_hour_of_day BETWEEN 6 AND 12 THEN 'Morning User'
  WHEN avg_hour_of_day BETWEEN 12 AND 17 THEN 'Afternoon User'
  WHEN avg_hour_of_day BETWEEN 17 AND 22 THEN 'Evening User'
  ELSE 'Night Owl'
END as time_preference
```

**Step 3: Add to persona logic**
```sql
-- Combine with other dimensions
WHEN messages_last_7d >= 50 AND avg_hour_of_day BETWEEN 22 AND 6
  THEN 'Night Owl Power User'
```

### Adapting for Your Product

Change the thresholds based on your product:

**High-frequency products (daily use):**
- Very Active: messages_last_7d >= 20 (vs 50)
- Active: messages_last_7d >= 10 (vs 20)

**Low-frequency products (weekly use):**
- Very Active: messages_last_30d >= 10 (vs 50/week)
- Active: messages_last_30d >= 4 (vs 20/week)

**Different features:**
- Replace "1:1 vs Group" with your feature dimensions
- Example: "Mobile vs Desktop", "Free vs Paid features"

---

## Integration with Other Skills

**Use with:**
- **product-analytics** - Deep dive into specific segments
- **funnel-analysis** - Track segment movement through funnels
- **cohort-analysis** - See how segments change over time

**Feeds into:**
- **feature-spec-writer** - Spec features for specific personas
- Linear tickets - Create epics per persona

---

## Best Practices

### 1. Segment Regularly
- Run segmentation monthly (not daily - segments are stable)
- Track segment migration over time
- Alert on sudden changes (e.g., spike in At Risk Churn)

### 2. Validate Segments
- Interview users in each segment
- Confirm your assumptions about their needs
- Refine persona definitions based on research

### 3. Measure Segment Health
- Track key metrics per segment (retention, NPS, revenue)
- Goal: Increase % in high-value segments
- Warning: Decrease % in churned/at-risk segments

### 4. Don't Over-Segment
- Start with 5-10 personas max
- Too many segments = analysis paralysis
- Combine similar personas if behaviors overlap

### 5. Tie to Business Metrics
- Which personas drive revenue?
- Which have highest LTV?
- Which are most expensive to serve?

---

## Common Pitfalls

### ❌ Segmenting on Demographics, Not Behavior
**Wrong:** "Users aged 25-35"
**Right:** "Power Users who engage daily"
**Why:** Behavior predicts future behavior; demographics don't

### ❌ Creating Segments You Can't Act On
**Wrong:** "Users who like the color blue"
**Right:** "Users who prefer 1:1 coaching over group chat"
**Why:** You can't build features for color preference

### ❌ Not Updating Segments
**Wrong:** Segment once, use forever
**Right:** Re-segment monthly, track migration
**Why:** Users move between segments (activate, churn, etc.)

### ❌ Treating All Segments Equally
**Wrong:** Build features for every segment equally
**Right:** Prioritize high-value segments
**Why:** Limited resources, 80/20 rule

---

## Quick Reference

### Useful Metrics by Segment

| Metric | Engagement | Feature Usage | Value Signal |
|--------|-----------|---------------|--------------|
| DAU/MAU ratio | ✅ | | |
| Messages per week | ✅ | | |
| Days since last use | ✅ | | |
| Feature adoption rate | | ✅ | |
| Features per user | | ✅ | |
| Reaction rate | | | ✅ |
| NPS | | | ✅ |
| Referrals | | | ✅ |

### Threshold Recommendations

| Product Type | Very Active | Active | At Risk Days |
|-------------|------------|--------|--------------|
| Daily (social) | 50+/week | 20+/week | 7 days |
| Weekly (productivity) | 20+/month | 8+/month | 14 days |
| Monthly (coaching) | 10+/month | 4+/month | 30 days |

---

## Notes

- **Sample size matters** - Need 30+ users for reliable segments
- **Context matters** - Churned users may return (seasonal product)
- **Segments evolve** - New users become power users or churn
- **Combine with qualitative** - Interview users to validate

Remember: The goal isn't perfect segmentation. It's actionable segmentation that drives product decisions.
