---
name: posthog-analytics
description: Product analytics expert using PostHog MCP. Triggers on requests to understand user behavior, surface insights, create dashboards, analyze funnels, track metrics, set up experiments, or answer questions about product performance. Use when working with PostHog data, discussing analytics strategy, investigating user journeys, retention, conversion, feature adoption, or when asked to help understand what's happening in the product.
---

# PostHog Analytics Expert

Transform PostHog data into actionable product insights. This skill combines product analytics expertise with the PostHog MCP server to help discover patterns, surface opportunities, and build a data-informed product strategy.

## Product Context Management

Before diving into analysis, establish product context. Store discovered knowledge in `.claude/product-context.md` for persistence across sessions.

### First Session: Discovery

1. **Check for existing context**: Read `.claude/product-context.md` if it exists
2. **Interview the user** (if context is missing or incomplete):
   - What does the product do? Who are the users?
   - What are the key user actions/conversions?
   - What business metrics matter most?
3. **Explore PostHog data**:
   - `event-definitions-list` - Discover tracked events
   - `properties-list` - Understand available properties
   - `insights-get-all` - See existing insights
   - `dashboards-get-all` - Review current dashboards
4. **Save context**: Write discovered knowledge to `.claude/product-context.md`

### Context File Structure

```markdown
# Product Context

## Product Overview
[What the product does, target users]

## Key Events
| Event | Meaning | Importance |
|-------|---------|------------|
| $pageview | Page visit | Navigation tracking |
| signup_completed | User registered | Core conversion |
| [custom events discovered] | | |

## Important Properties
- user_tier: free/pro/enterprise
- [other key properties]

## Key Metrics
- Primary: [e.g., Weekly Active Users, Conversion Rate]
- Secondary: [e.g., Feature Adoption, Retention]

## Funnels
- Activation: signup → onboarding_complete → first_value_action
- [other key funnels]

## Last Updated: [date]
```

## Core Capabilities

### 1. Proactive Insight Discovery

When asked to "find insights" or "what's interesting", run this discovery workflow:

```
1. Trends Analysis
   - query-run: Total events over 30 days (spot volume changes)
   - query-run: DAU/WAU/MAU trends (engagement health)
   - query-run: Key conversion events over time

2. Funnel Health
   - query-run: Core activation funnel
   - query-run: Conversion funnel (trial → paid if SaaS)
   - Look for: Drop-off points, conversion changes

3. Retention Check
   - query-run: Cohort retention (week-over-week)
   - Look for: Retention curve shape, changes over time

4. Feature Adoption
   - query-run: Feature usage by user segment
   - Look for: Underused features, power user patterns

5. Error Impact
   - list-errors: Top errors by occurrence
   - error-details: Impact on user journeys
```

**Insight Presentation Format:**
```
## [Insight Title]
**Finding**: [One sentence summary]
**Evidence**: [Specific numbers/data]
**Impact**: [Why this matters]
**Recommended Action**: [What to do about it]
```

### 2. Answering Analytics Questions

Map common questions to PostHog queries:

| Question Pattern | Approach |
|-----------------|----------|
| "How many users..." | `query-run` with TrendsQuery, `math: "dau"` or `"total"` |
| "What % convert..." | `query-run` with FunnelsQuery |
| "Where do users drop off..." | FunnelsQuery → analyze step-by-step conversion |
| "Which feature is most used..." | TrendsQuery with breakdown by feature/event |
| "How is X changing over time..." | TrendsQuery with `interval: "day"` or `"week"` |
| "Who are our power users..." | TrendsQuery with breakdown by user property |
| "What's causing errors..." | `list-errors` → `error-details` for top issues |

### 3. Dashboard Creation

When building dashboards, follow this structure:

**Executive Dashboard** (high-level health):
- Active users (DAU/WAU/MAU)
- Core conversion rate
- Retention (week 1, week 4)
- Revenue metrics (if applicable)

**Product Dashboard** (feature-level):
- Feature adoption rates
- Feature engagement depth
- User journey completion
- Error rates by feature

**Growth Dashboard** (acquisition/activation):
- Signup funnel
- Activation funnel
- Traffic sources (if tracked)
- Onboarding completion

**Workflow:**
1. `dashboard-create` with descriptive name
2. Build insights with `query-run` → `insight-create-from-query`
3. Add to dashboard with `add-insight-to-dashboard`
4. Organize with `dashboard-reorder-tiles`

### 4. Experiment Design

When setting up A/B tests:

1. **Clarify hypothesis**: What change, expected impact, and why
2. **Find existing flags**: `feature-flag-get-all` (reuse if appropriate)
3. **Choose metrics**: Use `event-definitions-list` to find trackable events
4. **Set up experiment**: `experiment-create` with:
   - Clear name and description
   - Primary metric (what you're optimizing)
   - Secondary metrics (guardrails)
   - Appropriate sample size (MDE guidance)

See [references/experiments.md](references/experiments.md) for detailed experiment patterns.

### 5. Cohort & Segment Analysis

For understanding user segments:

```
1. Define cohort criteria (user properties, behaviors)
2. Compare cohorts on key metrics:
   - query-run with breakdownFilter by cohort property
   - Conversion rates per segment
   - Retention per segment
3. Identify highest-value segments
4. Recommend targeting strategies
```

## Query Patterns

### TrendsQuery (counts over time)

```json
{
  "kind": "InsightVizNode",
  "source": {
    "kind": "TrendsQuery",
    "dateRange": {"date_from": "-30d"},
    "interval": "day",
    "series": [{
      "kind": "EventsNode",
      "event": "event_name",
      "custom_name": "Display Name",
      "math": "total"
    }]
  }
}
```

Math options: `total`, `dau`, `weekly_active`, `monthly_active`, `unique_session`, `avg`, `sum`, `min`, `max`

### FunnelsQuery (conversion analysis)

```json
{
  "kind": "InsightVizNode",
  "source": {
    "kind": "FunnelsQuery",
    "dateRange": {"date_from": "-30d"},
    "series": [
      {"kind": "EventsNode", "event": "step_1", "custom_name": "Step 1"},
      {"kind": "EventsNode", "event": "step_2", "custom_name": "Step 2"},
      {"kind": "EventsNode", "event": "step_3", "custom_name": "Step 3"}
    ],
    "funnelsFilter": {
      "funnelWindowInterval": 7,
      "funnelWindowIntervalUnit": "day"
    }
  }
}
```

### Breakdown Analysis

Add to any query:
```json
"breakdownFilter": {
  "breakdown": "property_name",
  "breakdown_type": "event"  // or "person"
}
```

## SaaS Metrics Framework

For SaaS products, prioritize these metrics:

| Metric | Query Approach | Why It Matters |
|--------|---------------|----------------|
| **Activation Rate** | Funnel: signup → key_action | Validates onboarding |
| **DAU/MAU Ratio** | Trends: DAU ÷ MAU | Engagement stickiness |
| **Feature Adoption** | Trends: feature_used by user | Product-market fit signals |
| **Retention (D7, D30)** | Cohort retention query | Long-term value predictor |
| **Conversion (Trial→Paid)** | Funnel: trial_start → subscription | Revenue health |
| **Expansion Revenue** | Trends: upgrade events | Growth efficiency |
| **Churn Indicators** | Declining usage patterns | Early warning system |

## Resources

- [references/experiments.md](references/experiments.md) - Detailed experiment design patterns
- [references/saas-playbook.md](references/saas-playbook.md) - SaaS-specific analytics strategies
