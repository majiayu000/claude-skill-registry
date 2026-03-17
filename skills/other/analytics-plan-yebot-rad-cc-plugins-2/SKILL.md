---
description: Define analytics tracking plan for features and initiatives
disable-model-invocation: false
---

# Analytics Plan

Create comprehensive analytics tracking plans to measure feature success.

## When to Use

- Before implementing a new feature (define what to track)
- When launching an experiment
- When setting up product analytics
- When defining success metrics

## Used By

- Data Analyst (primary owner)
- Growth Marketer (growth metrics)
- Product Manager (success metrics)
- Full-Stack Engineer (implementation)

---

## Analytics Plan Template

```markdown
# Analytics Plan: [Feature/Initiative Name]

**Author**: [Name]
**Date**: [Date]
**Status**: Draft | Approved | Implemented

---

## Overview

### Feature Description
[Brief description of the feature]

### Business Questions
What decisions will this data inform?

1. [Question 1]
2. [Question 2]
3. [Question 3]

### Success Criteria
How will we know if this feature is successful?

- **Primary Metric**: [Metric] - Target: [X]
- **Secondary Metric**: [Metric] - Target: [X]
- **Guardrail Metric**: [Metric] - Should not decrease by [X%]

---

## Event Tracking

### Core Events

| Event Name | Trigger | Properties | Priority |
|------------|---------|------------|----------|
| `[event_name]` | [When fired] | [Key properties] | P1 |
| `[event_name]` | [When fired] | [Key properties] | P1 |
| `[event_name]` | [When fired] | [Key properties] | P2 |

### Event Specifications

#### `feature_viewed`
**Trigger**: When user views the feature for the first time in session

**Properties**:
| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `source` | string | Yes | Where user came from |
| `variant` | string | No | A/B test variant |
| `user_tier` | string | Yes | Free/Pro/Enterprise |

**Example**:
```json
{
  "event": "feature_viewed",
  "properties": {
    "source": "navigation",
    "variant": "control",
    "user_tier": "pro"
  }
}
```

#### `feature_action_completed`
**Trigger**: When user completes the primary action

**Properties**:
| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `action_type` | string | Yes | Type of action |
| `time_to_complete` | number | Yes | Seconds from start |
| `success` | boolean | Yes | Action succeeded |

---

## Funnel Definition

### Primary Funnel: [Feature Adoption]

```
Step 1: feature_viewed
    ↓ [Target: 80%]
Step 2: feature_started
    ↓ [Target: 60%]
Step 3: feature_completed
    ↓ [Target: 40%]
Step 4: feature_repeated (within 7 days)
```

### Funnel Analysis Questions
- Where is the biggest drop-off?
- How does drop-off vary by user segment?
- What's the time between steps?

---

## User Properties

| Property | Type | Description | When Updated |
|----------|------|-------------|--------------|
| `has_used_feature` | boolean | User has ever used feature | On first use |
| `feature_usage_count` | number | Times user used feature | On each use |
| `first_feature_use` | timestamp | When first used | On first use |
| `last_feature_use` | timestamp | Most recent use | On each use |

---

## Segments

### Key Segments to Analyze

| Segment | Definition | Why Important |
|---------|------------|---------------|
| New Users | account_age < 7 days | Adoption patterns |
| Power Users | feature_usage > 10/week | Success indicators |
| At-Risk | no_activity > 14 days | Retention insights |
| By Plan | plan_type = [free/pro/enterprise] | Monetization |

---

## Dashboard Requirements

### Overview Dashboard

**Purpose**: Daily monitoring of feature health

**Metrics to Include**:
- Daily Active Users (DAU)
- Feature adoption rate
- Primary action completion rate
- Error rate

**Filters**:
- Date range
- User segment
- Platform

### Deep Dive Dashboard

**Purpose**: Understanding patterns and opportunities

**Charts to Include**:
- Funnel visualization
- Cohort retention
- Time-based trends
- Segment comparison

---

## Experiment Plan (if applicable)

### Hypothesis
[Change] will lead to [X% improvement] in [metric] because [reason].

### Test Setup
- **Control**: [Current experience]
- **Variant**: [New experience]
- **Allocation**: [50/50 or other]
- **Duration**: [X weeks]
- **Sample Size Needed**: [X users per variant]

### Success Metrics
| Metric | Baseline | MDE | Direction |
|--------|----------|-----|-----------|
| Primary: [metric] | [X%] | [Y%] | Increase |
| Secondary: [metric] | [X] | [Y] | Increase |
| Guardrail: [metric] | [X%] | [Y%] | No decrease |

### Analysis Plan
- Primary analysis at [X] days
- Segment analysis by [dimensions]
- Document learnings regardless of outcome

---

## Implementation Checklist

### Before Development
- [ ] Analytics plan reviewed by data/product
- [ ] Event names follow naming convention
- [ ] Success metrics approved

### During Development
- [ ] Events implemented with correct properties
- [ ] Events fire at correct times
- [ ] Properties populated correctly

### Before Launch
- [ ] Events tested in staging
- [ ] Dashboard created
- [ ] Baseline metrics captured
- [ ] Alert thresholds set

### After Launch
- [ ] Verify data flowing correctly
- [ ] Check for data quality issues
- [ ] Monitor metrics daily for first week

---

## Data Quality Checks

| Check | Query/Method | Expected |
|-------|--------------|----------|
| Events firing | Count by day | > 0 after launch |
| Required properties | Null check | No nulls |
| Property values | Distinct values | Expected options |
| User join rate | user_id present | 100% |
```

---

## Event Naming Convention

### Format
```
[object]_[action]
```

### Objects (nouns)
- `page` - Page views
- `button` - Button interactions
- `form` - Form interactions
- `feature` - Feature usage
- `subscription` - Subscription events
- `user` - User lifecycle

### Actions (past tense verbs)
- `viewed` - Something was seen
- `clicked` - Something was clicked
- `submitted` - Form was submitted
- `started` - Process began
- `completed` - Process finished
- `failed` - Something went wrong

### Examples
```
page_viewed
button_clicked
form_submitted
feature_started
feature_completed
subscription_upgraded
user_signed_up
```

---

## Property Guidelines

### Always Include
- `timestamp` - When event occurred
- `user_id` - Logged-in user identifier
- `session_id` - Session identifier
- `platform` - web/ios/android
- `page` - Current page/screen

### Contextual Properties
- `source` - What triggered the action
- `variant` - A/B test variant
- `value` - Numeric value if applicable
- `error_type` - For error events

### Naming Rules
- Use `snake_case`
- Be descriptive but concise
- Use consistent naming across events
- Document allowed values for enums

---

## Metrics Definitions

### Common Metrics

**Daily Active Users (DAU)**
```
Count of unique users with any event in past 24 hours
```

**Activation Rate**
```
(Users who completed key action) / (Users who signed up) × 100
```

**Retention Rate (Day N)**
```
(Users active on day N) / (Users who signed up N days ago) × 100
```

**Feature Adoption**
```
(Users who used feature) / (Total users) × 100
```

**Conversion Rate**
```
(Users who completed goal) / (Users who started flow) × 100
```

---

## Quick Reference

### Before Feature Launch
1. Define success metrics
2. Create event tracking plan
3. Implement events
4. Test in staging
5. Set up dashboard
6. Capture baseline

### After Feature Launch
1. Verify data quality
2. Monitor daily
3. Analyze after 1 week
4. Deep dive after 1 month
5. Document learnings
