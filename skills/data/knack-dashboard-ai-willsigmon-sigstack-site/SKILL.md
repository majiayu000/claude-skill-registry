---
name: Knack Dashboard AI
description: Generates insight layers and visual summaries from HTI operational data. Transforms raw Knack records into actionable intelligence for stakeholders...
allowed-tools: Read, Edit
---

# Knack Dashboard AI

## Purpose
Generates insight layers and visual summaries from HTI operational data. Transforms raw Knack records into actionable intelligence for stakeholders and grant reporting.

## Core Capabilities

1. **Metrics Generation**: Aggregate data into KPIs
2. **Trend Analysis**: Identify patterns over time
3. **Predictive Insights**: Forecast progress toward goals
4. **Visual Recommendations**: Suggest optimal chart types
5. **Anomaly Detection**: Flag unusual data patterns

## Core Functions

### generate_metrics
**Purpose**: Calculate key performance indicators from raw data

**Parameters**:
- `fields` (array, required): Which metrics to calculate
- `dataset` (array, optional): Custom dataset (default: fetch all)
- `time_period` (string, optional): "all", "quarter", "month", "week"

**Available Metrics**:
```javascript
const metrics = {
  // Device Lifecycle
  acquired: "Total laptops received",
  converted: "Chromebooks successfully created",
  ready: "Devices ready for donation",
  presented: "Devices delivered to recipients",
  discarded: "Units recycled/unusable",

  // Conversion Rates
  conversion_rate: "(converted / acquired) * 100",
  success_rate: "(presented / ready) * 100",
  discard_rate: "(discarded / acquired) * 100",

  // Training
  train_hours: "Total digital literacy hours delivered",
  participants: "Unique individuals trained",

  // Business Development
  donors: "Unique donor organizations",
  recurring_donors: "Donors with 3+ donations",
  avg_donation_size: "Mean laptops per donation"
};
```

**Example**:
```javascript
const kpis = await generate_metrics({
  fields: ["acquired", "converted", "ready", "conversion_rate"],
  time_period: "quarter"
});

// Output:
// {
//   acquired: 875,
//   converted: 623,
//   ready: 89,
//   conversion_rate: 71.2
// }
```

### calculate_trends
**Purpose**: Analyze changes over time

**Example**:
```javascript
const trend = await calculate_trends({
  metric: "acquired",
  granularity: "month", // day, week, month, quarter
  periods: 6 // Last 6 months
});

// Output:
// {
//   data: [
//     { period: "2024-07", value: 145 },
//     { period: "2024-08", value: 167 },
//     { period: "2024-09", value: 152 },
//     { period: "2024-10", value: 178 },
//     { period: "2024-11", value: 156 },
//     { period: "2024-12", value: 189 }
//   ],
//   trend: "upward",
//   average: 164.5,
//   growth_rate: 4.2 // Percent per month
// }
```

### predict_goal_completion
**Purpose**: Forecast when goals will be reached

**Example**:
```javascript
const forecast = await predict_goal_completion({
  goal: { target: 3500, field: "acquired" },
  current_value: 1250,
  time_elapsed_months: 8,
  time_remaining_months: 16
});

// Output:
// {
//   projected_total: 3750,
//   will_meet_goal: true,
//   projected_completion: "2025-09-15",
//   confidence: 0.85,
//   recommendation: "On track - maintain current pace"
// }
```

### build_charts
**Purpose**: Generate chart configurations for visualization libraries

**Parameters**:
- `type` (string, required): "bar" | "line" | "donut" | "area" | "scatter"
- `data` (object, required): Dataset to visualize
- `options` (object, optional): Customization (colors, labels, etc.)

**Example - Bar Chart**:
```javascript
const chart = build_charts({
  type: "bar",
  data: {
    labels: ["Wake", "Durham", "Vance", "Franklin", "Granville"],
    values: [234, 189, 67, 45, 78]
  },
  options: {
    title: "Devices by County",
    colors: ["#0E2240", "#6FC3DF"], // HTI brand colors
    y_axis_label: "Number of Devices"
  }
});

// Output: Chart.js compatible config
```

**Example - Line Chart (Trend)**:
```javascript
const trend_chart = build_charts({
  type: "line",
  data: {
    labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    datasets: [
      { label: "Acquired", values: [145, 167, 152, 178, 156, 189] },
      { label: "Converted", values: [98, 112, 108, 125, 110, 134] }
    ]
  },
  options: {
    title: "Device Pipeline - Q1/Q2 2025",
    colors: ["#0E2240", "#6FC3DF"]
  }
});
```

**Example - Donut Chart (Breakdown)**:
```javascript
const status_chart = build_charts({
  type: "donut",
  data: {
    labels: ["Ready", "In Progress", "Awaiting Parts", "Discarded"],
    values: [89, 234, 45, 12]
  },
  options: {
    title: "Current Device Status",
    colors: ["#0E2240", "#6FC3DF", "#A0C4D9", "#E0E0E0"]
  }
});
```

### detect_anomalies
**Purpose**: Flag unusual patterns requiring attention

**Example**:
```javascript
const anomalies = await detect_anomalies({
  metric: "discard_rate",
  threshold: 20, // Alert if >20%
  time_period: "month"
});

// Output:
// [
//   {
//     period: "2024-11",
//     value: 28.5,
//     expected_range: [10, 20],
//     severity: "high",
//     message: "Discard rate 42% above normal - check testing process"
//   }
// ]
```

### compare_performance
**Purpose**: Benchmark against goals or historical data

**Example**:
```javascript
const performance = await compare_performance({
  actual: { acquired: 1250, converted: 890 },
  target: { acquired: 1458, converted: 1042 }, // Proportional to 3500/2500 goal
  period: "8 months into 24-month grant"
});

// Output:
// {
//   acquired: { actual: 1250, target: 1458, variance: -14.3, status: "behind" },
//   converted: { actual: 890, target: 1042, variance: -14.6, status: "behind" },
//   overall_health: "at_risk",
//   recommendation: "Increase acquisition efforts by 15% to meet goal"
// }
```

## HTI-Specific Dashboards

### Executive Summary Dashboard
```javascript
const executive_summary = {
  kpis: await generate_metrics({
    fields: ["acquired", "converted", "ready", "train_hours"]
  }),
  progress: await compare_performance({
    actual: kpis,
    target: { acquired: 3500, converted: 2500, train_hours: 156 }
  }),
  trends: await calculate_trends({ metric: "acquired", periods: 12 }),
  counties: await county_breakdown()
};
```

### Operations Dashboard
```javascript
const ops_dashboard = {
  pipeline: await generate_metrics({
    fields: ["acquired", "converted", "ready", "discarded"]
  }),
  bottlenecks: await detect_anomalies({ metric: "conversion_rate" }),
  county_map: await build_charts({
    type: "bar",
    data: await county_breakdown()
  }),
  recent_activity: await recent_transactions(limit: 10)
};
```

### Grant Compliance Dashboard
```javascript
const compliance_dashboard = {
  quarterly_progress: await generate_quarterly_report("Q4", "2024"),
  goal_forecast: await predict_goal_completion({
    goal: { target: 3500, field: "acquired" }
  }),
  training_hours: await generate_metrics({
    fields: ["train_hours", "participants"]
  }),
  county_coverage: await verify_15_county_coverage()
};
```

### Donor Relations Dashboard
```javascript
const donor_dashboard = {
  top_donors: await rank_donors({ limit: 10 }),
  recurring_donors: await identify_recurring_donors({ min_donations: 3 }),
  avg_donation: await generate_metrics({ fields: ["avg_donation_size"] }),
  retention_rate: await calculate_donor_retention(),
  outreach_targets: await identify_outreach_opportunities()
};
```

## Chart Type Recommendations

### When to Use Each Chart Type

**Bar Chart**: Comparing categories
- County-level device distribution
- Donor organization rankings
- Monthly acquisition totals

**Line Chart**: Trends over time
- Cumulative devices acquired
- Conversion rate over 24 months
- Training hours per quarter

**Donut/Pie**: Parts of a whole
- Device status breakdown (Ready, In Progress, Discarded)
- County coverage (what % of 15 counties reached)

**Area Chart**: Cumulative growth
- Progress toward 3,500 laptop goal
- Training hours accumulation

**Scatter Plot**: Correlation analysis
- Donation size vs. donor frequency
- Conversion rate vs. device age

## Brand-Aligned Visualizations

### HTI Color Palette
```javascript
const HTI_COLORS = {
  primary: "#0E2240",      // Navy Blue
  secondary: "#6FC3DF",    // Light Blue
  white: "#FFFFFF",
  accent: "#A0C4D9",       // Muted blue
  neutral: "#E0E0E0",      // Light gray
  success: "#4CAF50",
  warning: "#FF9800",
  danger: "#F44336"
};
```

### Chart Styling
```javascript
const brand_chart_options = {
  font_family: "Inter, sans-serif",
  colors: [HTI_COLORS.primary, HTI_COLORS.secondary],
  background: HTI_COLORS.white,
  grid_color: HTI_COLORS.neutral,
  title_size: 18,
  label_size: 12
};
```

## Real-Time Insights

### Live Progress Indicator
```javascript
const live_progress = await generate_metrics({ fields: ["acquired", "converted"] });
const progress_pct = (live_progress.acquired / 3500) * 100;

const indicator = {
  value: progress_pct.toFixed(1),
  display: `${progress_pct.toFixed(1)}% toward 3,500 laptop goal`,
  color: progress_pct > 50 ? HTI_COLORS.success : HTI_COLORS.warning
};
```

### Dynamic Goal Status
```javascript
const goal_status = await predict_goal_completion({
  goal: { target: 3500, field: "acquired" }
});

const status_message = goal_status.will_meet_goal
  ? "✅ On track to meet goal"
  : "⚠️ Action needed to meet goal";
```

## Integration Points

- **knack_reader**: Fetch raw data for analysis
- **knack_pagination**: Retrieve full datasets for accurate metrics
- **knack_filter_sort**: Filter data by time period or category
- **knack_cache_optimizer**: Cache computed metrics (expensive calculations)
- **knack_reporting_sync**: Power quarterly reports with AI-generated insights
- **knack_goal_tracker**: Real-time progress monitoring

## Export Formats

### JSON (API Responses)
```javascript
const metrics = await generate_metrics({ fields: ["acquired", "converted"] });
res.json(metrics);
```

### HTML (Email Reports)
```javascript
const html = generate_html_report({
  metrics: kpis,
  charts: [trend_chart, status_chart],
  branding: HTI_COLORS
});
```

### PDF (Quarterly Reports)
```javascript
const pdf = generate_pdf_report({
  data: compliance_dashboard,
  template: "ncdit_quarterly_template"
});
```

## Best Practices

1. **Cache metrics**: Expensive aggregations should be cached (5-min TTL)
2. **Use appropriate granularity**: Daily for ops, monthly for trends, quarterly for grants
3. **Brand consistency**: Always use HTI color palette
4. **Contextual insights**: Include "why" and "what next" with every metric
5. **Progressive disclosure**: Start with summary, drill down on click

## Grant Reporting Automation

### Auto-Generate Quarterly Narrative
```javascript
const narrative = await generate_narrative({
  metrics: await generate_quarterly_report("Q1", "2025"),
  template: "ncdit_compliance",
  tone: "factual, mission-driven"
});

// Output:
// "During Q1 2025, HTI acquired 875 laptops from 12 donor organizations
// across 8 counties, converting 623 into HTI Chromebooks. This represents
// a 71% conversion rate, exceeding our 70% target. We delivered 42 hours
// of digital literacy training to 156 participants..."
```
