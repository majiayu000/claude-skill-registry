---
name: Knack Goal Tracker
description: Tracks HTI's performance against both grant and business development goals in real-time. Provides early warning system for goal attainment risks an...
allowed-tools: Edit
---

# Knack Goal Tracker

## Purpose
Tracks HTI's performance against both grant and business development goals in real-time. Provides early warning system for goal attainment risks and generates actionable insights.

## Grant Goals (2024-2026)

### Primary Grant Commitments
```javascript
const grant_goals = {
  devices: {
    acquire: { target: 3500, unit: "laptops", deadline: "2026-12-31" },
    convert: { target: 2500, unit: "HTI Chromebooks", deadline: "2026-12-31" },
    conversion_rate: { target: 70, unit: "percent", type: "minimum" }
  },

  training: {
    hours: { target: 156, unit: "hours", deadline: "2026-12-31" },
    geographic: { target: 15, unit: "counties", type: "coverage" }
  },

  timeline: {
    start: "2024-01-01",
    end: "2026-12-31",
    duration_months: 24
  }
};
```

### 2026 Business Development Goals
```javascript
const business_goals = {
  donors: {
    unique_orgs: { target: 10, unit: "organizations" },
    recurring: { target: 6, unit: "donors", criteria: "50+ laptops annually" },
    major: { target: 20, unit: "donations", criteria: ">$500 each" }
  },

  financial: {
    grant_match: { target: 65000, unit: "USD" },
    corporate_sponsors: { target: 2, unit: "sponsors" }
  },

  sustainability: {
    recurring_revenue: { target: "sustainable post-grant", type: "qualitative" }
  }
};
```

## Core Functions

### check_progress
**Purpose**: Calculate current progress toward all goals

**Parameters**:
- `goal_targets` (object, required): Goal definitions
- `live_data` (object, optional): Current metrics (default: fetch from Knack)
- `as_of_date` (date, optional): Point-in-time check (default: now)

**Example**:
```javascript
const progress = await check_progress({
  goal_targets: grant_goals,
  live_data: await generate_metrics({ fields: ["acquired", "converted", "train_hours"] })
});

// Output:
// {
//   acquire: {
//     current: 1250,
//     target: 3500,
//     progress_pct: 35.7,
//     status: "behind", // on_track | ahead | behind | at_risk
//     variance: -2250,
//     projected_final: 3125, // Based on current pace
//     will_meet_goal: false
//   },
//   convert: {
//     current: 890,
//     target: 2500,
//     progress_pct: 35.6,
//     status: "behind",
//     variance: -1610,
//     projected_final: 2225,
//     will_meet_goal: false
//   },
//   train_hours: {
//     current: 78,
//     target: 156,
//     progress_pct: 50.0,
//     status: "on_track",
//     variance: -78,
//     projected_final: 156,
//     will_meet_goal: true
//   }
// }
```

### calculate_status
**Purpose**: Determine if goal is on track based on time elapsed

**Logic**:
```javascript
function calculate_status({ current, target, time_elapsed_pct }) {
  const progress_pct = (current / target) * 100;

  // Expected progress = time elapsed
  // e.g., 8 months into 24-month grant = 33.3% expected

  if (progress_pct >= time_elapsed_pct + 10) {
    return "ahead"; // More than 10% ahead of schedule
  } else if (progress_pct >= time_elapsed_pct - 5) {
    return "on_track"; // Within 5% of expected
  } else if (progress_pct >= time_elapsed_pct - 15) {
    return "behind"; // 5-15% behind
  } else {
    return "at_risk"; // More than 15% behind
  }
}
```

**Example**:
```javascript
// 8 months into 24-month grant (33.3% time elapsed)
// Current: 1250 acquired, Target: 3500
// Progress: 35.7% (ahead of timeline!)

const status = calculate_status({
  current: 1250,
  target: 3500,
  time_elapsed_pct: 33.3
});
// Returns: "ahead"
```

### forecast_completion
**Purpose**: Predict final values and completion dates

**Algorithm**:
```javascript
function forecast_completion({ current, target, time_elapsed_months, time_remaining_months }) {
  // Calculate current rate
  const rate_per_month = current / time_elapsed_months;

  // Project forward
  const projected_additional = rate_per_month * time_remaining_months;
  const projected_final = current + projected_additional;

  // Will goal be met?
  const will_meet = projected_final >= target;

  // Estimated completion date (if on current pace)
  const months_to_complete = will_meet
    ? time_elapsed_months + ((target - current) / rate_per_month)
    : null;

  return {
    projected_final: Math.round(projected_final),
    will_meet_goal: will_meet,
    estimated_completion: months_to_complete
      ? addMonths(grant_start_date, months_to_complete)
      : "Will not meet at current pace",
    confidence: calculate_confidence({ current, time_elapsed_months })
  };
}
```

**Example**:
```javascript
const forecast = await forecast_completion({
  current: 1250,
  target: 3500,
  time_elapsed_months: 8,
  time_remaining_months: 16
});

// Output:
// {
//   projected_final: 3750,
//   will_meet_goal: true,
//   estimated_completion: "2025-09-15",
//   confidence: 0.85
// }
```

### generate_dashboard_summary
**Purpose**: Create visual progress summary for dashboards

**Example**:
```javascript
const summary = await generate_dashboard_summary();

// Output:
// {
//   overall_health: "at_risk", // ahead | on_track | behind | at_risk
//   goals: [
//     {
//       name: "Laptops Acquired",
//       current: 1250,
//       target: 3500,
//       progress_pct: 35.7,
//       status: "behind",
//       icon: "⚠️",
//       color: "#FF9800" // HTI warning color
//     },
//     {
//       name: "Training Hours",
//       current: 78,
//       target: 156,
//       progress_pct: 50.0,
//       status: "on_track",
//       icon: "✅",
//       color: "#4CAF50" // HTI success color
//     }
//   ],
//   alerts: [
//     {
//       severity: "high",
//       message: "Acquisition pace 15% below target - increase donor outreach"
//     }
//   ],
//   last_updated: "2025-04-15T14:30:00Z"
// }
```

### identify_risks
**Purpose**: Flag goals at risk of not being met

**Example**:
```javascript
const risks = await identify_risks();

// Output:
// [
//   {
//     goal: "Laptops Acquired",
//     risk_level: "high",
//     current: 1250,
//     target: 3500,
//     gap: -2250,
//     recommendation: "Increase acquisition by 20% per month to meet goal",
//     action_items: [
//       "Contact 5 new potential donor organizations",
//       "Launch Q3 laptop drive campaign",
//       "Engage corporate sponsors for bulk donations"
//     ]
//   },
//   {
//     goal: "Recurring Donors (6 with 50+ laptops)",
//     risk_level: "medium",
//     current: 3,
//     target: 6,
//     gap: -3,
//     recommendation: "Nurture current one-time donors into recurring relationships",
//     action_items: [
//       "Quarterly check-ins with major donors",
//       "Create recurring donation program",
//       "Share impact reports to retain engagement"
//     ]
//   }
// ]
```

### generate_recommendations
**Purpose**: AI-driven suggestions to get back on track

**Example**:
```javascript
const recommendations = await generate_recommendations({
  goal: "acquire",
  current: 1250,
  target: 3500,
  time_remaining_months: 16
});

// Output:
// {
//   required_pace: {
//     per_month: 141,
//     per_week: 33,
//     change_from_current: "+20%"
//   },
//   strategies: [
//     {
//       strategy: "Expand donor outreach",
//       impact: "high",
//       effort: "medium",
//       description: "Target 10 new organizations in underserved counties"
//     },
//     {
//       strategy: "Corporate laptop refresh campaigns",
//       impact: "high",
//       effort: "high",
//       description: "Partner with Triangle-area corporations upgrading devices"
//     },
//     {
//       strategy: "Community laptop drives",
//       impact: "medium",
//       effort: "low",
//       description: "Host collection events in Wake & Durham"
//     }
//   ],
//   confidence: "If implemented, 85% likelihood of meeting goal"
// }
```

## Real-Time Progress Widgets

### Progress Bar Component
```javascript
function render_progress_bar({ current, target, label }) {
  const progress_pct = (current / target) * 100;
  const status_color = get_status_color(progress_pct);

  return {
    label: label,
    current: current,
    target: target,
    progress_pct: progress_pct.toFixed(1),
    bar: {
      width: `${progress_pct}%`,
      color: status_color
    },
    text: `${current.toLocaleString()} / ${target.toLocaleString()}`
  };
}

function get_status_color(progress_pct) {
  if (progress_pct >= 90) return "#4CAF50"; // Green
  if (progress_pct >= 70) return "#6FC3DF"; // HTI Blue
  if (progress_pct >= 50) return "#FF9800"; // Orange
  return "#F44336"; // Red
}
```

### Circular Progress Indicator
```javascript
function render_circular_progress({ current, target, label }) {
  const progress_pct = (current / target) * 100;

  return {
    type: "circular",
    progress: progress_pct,
    center_text: `${progress_pct.toFixed(0)}%`,
    label: label,
    color: get_status_color(progress_pct),
    stroke_width: 10
  };
}
```

### Countdown to Goal
```javascript
function render_countdown({ current, target, rate_per_month }) {
  const remaining = target - current;
  const months_left = remaining / rate_per_month;

  return {
    label: "Est. Time to Goal",
    value: months_left > 0 ? `${months_left.toFixed(1)} months` : "Goal Met!",
    icon: months_left < 12 ? "🚀" : "⏳"
  };
}
```

## Alerts & Notifications

### Automated Alerts
```javascript
// Check progress daily, alert if status changes
cron.schedule('0 9 * * *', async () => {
  const progress = await check_progress({ goal_targets: grant_goals });

  // Check each goal
  for (const [goal_name, goal_data] of Object.entries(progress)) {
    const previous_status = await get_previous_status(goal_name);

    if (goal_data.status !== previous_status) {
      await notify_team({
        channel: "#grant-tracking",
        message: `Goal status changed: ${goal_name} is now ${goal_data.status}`,
        data: goal_data
      });
    }

    if (goal_data.status === "at_risk") {
      await notify_admin({
        urgency: "high",
        subject: `ACTION REQUIRED: ${goal_name} at risk`,
        body: `Current: ${goal_data.current}, Target: ${goal_data.target}`,
        recommendations: await generate_recommendations({ goal: goal_name })
      });
    }
  }
});
```

### Quarterly Progress Notifications
```javascript
// Send stakeholder updates at quarter-end
cron.schedule('0 9 1 1,4,7,10 *', async () => {
  const quarter = getCurrentQuarter();
  const progress = await check_progress({ goal_targets: grant_goals });

  await sendEmail({
    to: "board@hubzonetech.org",
    subject: `HTI ${quarter} Goal Progress Update`,
    html: render_progress_email(progress)
  });
});
```

## Integration Points

- **knack_reader**: Fetch current metrics
- **knack_pagination**: Retrieve full datasets for accurate counts
- **knack_dashboard_ai**: Generate forecasts and recommendations
- **knack_reporting_sync**: Include in quarterly reports
- **knack_cache_optimizer**: Cache progress calculations (5-min TTL)
- **knack_realtime**: Live progress updates on dashboard

## Dashboard Views

### Executive Goal Dashboard
```javascript
const executive_dashboard = {
  widgets: [
    { type: "kpi_grid", data: await check_progress({ goal_targets: grant_goals }) },
    { type: "progress_bars", data: await generate_dashboard_summary() },
    { type: "forecast_chart", data: await forecast_all_goals() },
    { type: "risk_alerts", data: await identify_risks() }
  ]
};
```

### Operations Goal Dashboard
```javascript
const ops_dashboard = {
  widgets: [
    { type: "real_time_counter", goal: "acquired", refresh: "live" },
    { type: "pace_indicator", goal: "acquired", unit: "per_month" },
    { type: "action_items", data: await generate_recommendations() },
    { type: "county_coverage_map", data: await county_progress() }
  ]
};
```

## Best Practices

1. **Update goals in real-time**: Not just quarterly
2. **Set intermediate milestones**: Monthly or quarterly targets
3. **Track leading indicators**: Donor pipeline, not just acquisitions
4. **Celebrate wins**: Alert team when milestones hit
5. **Course-correct early**: Don't wait until quarter-end to act

## Grant Compliance

### NCDIT Reporting
- Include goal progress in every quarterly report
- Explain variances >10% from target
- Provide remediation plans for at-risk goals
- Document goal achievement at grant completion
