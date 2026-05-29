---
name: Knack Reporting Sync
description: Automates Digital Champion Grant and internal quarterly reporting. Ensures NCDIT compliance and generates stakeholder-ready reports from HTI operat...
allowed-tools: Read
---

# Knack Reporting Sync

## Purpose
Automates Digital Champion Grant and internal quarterly reporting. Ensures NCDIT compliance and generates stakeholder-ready reports from HTI operational data.

## Grant Context

**Funding Source**: NC Department of Information Technology (NCDIT)
**Program**: Digital Champion Grant (ARPA-funded)
**Grant Period**: 2024-2026 (24 months)
**Reporting Frequency**: Quarterly

**Required Metrics**:
- Laptops acquired
- Devices converted to HTI Chromebooks
- Units ready for donation
- Devices presented/delivered
- Devices discarded/recycled
- Digital literacy training hours
- Participants trained
- Geographic distribution (15 counties)

## Core Functions

### generate_quarterly_report
**Purpose**: Create comprehensive QAR (Quarterly Accountability Report)

**Parameters**:
- `quarter` (string, required): "Q1" | "Q2" | "Q3" | "Q4"
- `year` (string, required): "2024" | "2025" | "2026"
- `format` (string, optional): "json" | "pdf" | "html" | "excel"

**Example**:
```javascript
const report = await generate_quarterly_report("Q1", "2025", {
  format: "pdf",
  template: "ncdit_compliance",
  include_narrative: true
});
```

**Output Structure**:
```javascript
{
  metadata: {
    organization: "HUBZone Technology Initiative",
    grant_id: "NCDIT-DC-2024-HTI",
    period: "Q1 2025",
    date_generated: "2025-04-05",
    contact: "admin@hubzonetech.org"
  },

  device_metrics: {
    acquired: 875,
    converted: 623,
    ready: 89,
    presented: 534,
    discarded: 152,
    conversion_rate: 71.2,
    success_rate: 85.7
  },

  training_metrics: {
    hours_delivered: 42,
    participants: 156,
    sessions: 14,
    avg_attendance: 11.1
  },

  geographic_distribution: {
    counties_served: 8,
    county_breakdown: [
      { county: "Wake", devices: 234, training_hours: 12 },
      { county: "Durham", devices: 189, training_hours: 8 },
      // ... 13 more
    ]
  },

  progress_toward_goals: {
    laptops: { current: 1250, target: 3500, pct: 35.7 },
    converted: { current: 890, target: 2500, pct: 35.6 },
    train_hours: { current: 78, target: 156, pct: 50.0 }
  },

  narrative: "During Q1 2025, HTI acquired 875 laptops from 12 donor..."
}
```

### cross_reference_targets
**Purpose**: Validate progress against grant-defined goals

**Parameters**:
- `goals` (object, required): Target metrics from grant agreement
- `actual` (object, optional): Current metrics (default: fetch from Knack)

**Example**:
```javascript
const validation = await cross_reference_targets({
  goals: {
    laptops: 3500,
    converted: 2500,
    train_hours: 156,
    counties: 15
  }
});

// Output:
// {
//   laptops: { current: 1250, target: 3500, variance: -2250, status: "behind" },
//   converted: { current: 890, target: 2500, variance: -1610, status: "behind" },
//   train_hours: { current: 78, target: 156, variance: -78, status: "on_track" },
//   counties: { current: 8, target: 15, variance: -7, status: "behind" },
//   overall_status: "needs_attention"
// }
```

### validate_data_integrity
**Purpose**: Ensure report accuracy before submission

**Checks**:
- No duplicate device records
- All devices have valid status
- Training sessions have required fields
- County assignments match 15-county list
- Date ranges are logical (acquired < converted < presented)

**Example**:
```javascript
const validation = await validate_data_integrity({
  dataset: await fetch_all_pages("object_1")
});

// Output:
// {
//   valid: false,
//   errors: [
//     { record_id: "rec_123", issue: "Missing county assignment" },
//     { record_id: "rec_456", issue: "Converted date before acquired date" }
//   ],
//   warnings: [
//     { record_id: "rec_789", issue: "Unusually high discard rate" }
//   ]
// }
```

### export_ncdit_format
**Purpose**: Format report for NCDIT submission portal

**NCDIT Requirements**:
- Excel template with specific columns
- Financial data separated from operational
- Signature page with authorized representative
- Backup documentation (receipts, training rosters)

**Example**:
```javascript
const ncdit_export = await export_ncdit_format({
  quarter: "Q1",
  year: "2025",
  include_attachments: true
});

// Generates:
// - HTI_Q1_2025_Operational_Report.xlsx
// - HTI_Q1_2025_Financial_Report.xlsx
// - HTI_Q1_2025_Training_Rosters.pdf
// - HTI_Q1_2025_Signature_Page.pdf
```

### generate_board_summary
**Purpose**: Executive summary for HTI board meetings

**Example**:
```javascript
const board_report = await generate_board_summary({
  quarter: "Q1",
  year: "2025",
  include_financials: true,
  include_forecast: true
});
```

**Output Sections**:
1. **Executive Summary**: 1-paragraph overview
2. **Key Metrics**: 4-6 headline KPIs
3. **Progress vs. Goals**: Visual indicators
4. **Operational Highlights**: Notable donations, partnerships
5. **Challenges & Risks**: Areas needing attention
6. **Financial Summary**: Grant spending, match progress
7. **Next Quarter Priorities**: Action items

## Report Templates

### NCDIT Quarterly Template
```javascript
const ncdit_template = {
  sections: [
    "Grant Information",
    "Reporting Period",
    "Device Acquisition & Conversion",
    "Distribution & Impact",
    "Training & Education",
    "Geographic Coverage",
    "Financial Summary",
    "Challenges & Adaptations",
    "Next Quarter Plans"
  ],
  format: "excel",
  branding: false // NCDIT format, not HTI
};
```

### HTI Internal Template
```javascript
const internal_template = {
  sections: [
    "Executive Summary",
    "Operational Metrics",
    "Business Development",
    "Training & Outreach",
    "County Expansion Progress",
    "Financial Health",
    "Donor Relations",
    "Team Updates"
  ],
  format: "pdf",
  branding: true, // HTI colors, logo
  audience: "board"
};
```

### Donor Impact Report
```javascript
const donor_template = {
  sections: [
    "Thank You Message",
    "Your Impact This Quarter",
    "Success Stories",
    "Devices in Action (photos)",
    "Training Highlights",
    "Looking Ahead"
  ],
  format: "html", // Email-friendly
  branding: true,
  tone: "gratitude-focused"
};
```

## Automated Scheduling

### Set Up Quarterly Automation
```javascript
// Run automatically 5 days after quarter end
const schedule = {
  Q1: { deadline: "04-05", auto_generate: "04-01" },
  Q2: { deadline: "07-05", auto_generate: "07-01" },
  Q3: { deadline: "10-05", auto_generate: "10-01" },
  Q4: { deadline: "01-05", auto_generate: "01-01" }
};

cron.schedule('0 9 1 1,4,7,10 *', async () => {
  const quarter = getCurrentQuarter();
  const year = getCurrentYear();

  console.log(`Auto-generating ${quarter} ${year} report...`);

  const report = await generate_quarterly_report(quarter, year);
  await notify_admin({
    subject: `${quarter} ${year} Report Ready for Review`,
    report_url: report.url
  });
});
```

## Data Validation Rules

### Device Lifecycle Logic
```javascript
const validation_rules = {
  acquisition: {
    required_fields: ["donor", "acquisition_date", "quantity", "condition"],
    date_range: "within grant period (2024-2026)"
  },

  conversion: {
    required_fields: ["converted_date", "os_installed", "tested"],
    logic: "converted_date >= acquisition_date"
  },

  presentation: {
    required_fields: ["recipient", "county", "presented_date"],
    logic: "presented_date >= converted_date"
  },

  discard: {
    required_fields: ["discard_reason", "discard_date"],
    allowed_reasons: ["Beyond repair", "Missing parts", "Too old"]
  }
};
```

### Training Session Validation
```javascript
const training_validation = {
  required_fields: [
    "session_date",
    "county",
    "duration_hours",
    "participants",
    "topic"
  ],
  logic: {
    duration: "between 1 and 8 hours",
    participants: "at least 1",
    date: "within grant period"
  }
};
```

## Grant Compliance Checklist

### Pre-Submission Verification
```javascript
async function verify_report_compliance(report) {
  const checks = {
    data_complete: await check_all_fields_present(report),
    dates_valid: await validate_date_logic(report),
    totals_match: await cross_check_sums(report),
    counties_valid: await verify_county_list(report),
    narrative_included: report.narrative && report.narrative.length > 100,
    financials_attached: report.attachments.includes("financial_report"),
    signature_present: report.signature && report.signature.date
  };

  const all_passed = Object.values(checks).every(v => v === true);

  return {
    ready_for_submission: all_passed,
    checks: checks
  };
}
```

## Narrative Generation

### Auto-Generate Quarterly Narrative
```javascript
async function generate_narrative({ metrics, quarter, year }) {
  const template = `
    During ${quarter} ${year}, HUBZone Technology Initiative:

    - Acquired ${metrics.acquired} laptops from ${metrics.donors} donor organizations
    - Successfully converted ${metrics.converted} devices into HTI Chromebooks (${metrics.conversion_rate}% conversion rate)
    - Delivered ${metrics.presented} Chromebooks to residents and organizations across ${metrics.counties_served} counties
    - Conducted ${metrics.training_hours} hours of digital literacy training, serving ${metrics.participants} participants

    ${metrics.highlights.map(h => `- ${h}`).join('\n')}

    Challenges this quarter: ${metrics.challenges}

    Looking ahead to ${nextQuarter}: ${metrics.next_priorities}
  `;

  return template;
}
```

## Integration Points

- **knack_reader**: Fetch all data for reports
- **knack_pagination**: Retrieve complete datasets
- **knack_filter_sort**: Filter by quarter/year
- **knack_dashboard_ai**: Generate metrics and insights
- **knack_goal_tracker**: Progress vs. targets
- **knack_data_cleaner**: Validate before export
- **knack_exporter**: Multi-format output (PDF, Excel, HTML)

## Error Handling

```javascript
try {
  const report = await generate_quarterly_report("Q1", "2025");
} catch (error) {
  if (error.type === "DATA_INCOMPLETE") {
    console.error("Missing required data:", error.missing_fields);
  } else if (error.type === "VALIDATION_FAILED") {
    console.error("Data validation errors:", error.errors);
  } else {
    console.error("Report generation failed:", error);
  }
}
```

## Best Practices

1. **Generate early**: Create draft 1 week before deadline
2. **Manual review**: Always review auto-generated narratives
3. **Backup data**: Save source data with each report
4. **Version control**: Track report revisions
5. **Audit trail**: Log all report generations

## Next-Quarter Planning

### Auto-Generate Priorities
```javascript
async function suggest_next_quarter_priorities({ current_metrics, goals }) {
  const gaps = await identify_gaps(current_metrics, goals);

  return {
    acquisition: gaps.laptops > 500 ? "Intensify donor outreach" : "Maintain pace",
    training: gaps.train_hours > 20 ? "Schedule additional sessions" : "On track",
    counties: gaps.counties > 5 ? "Expand to new counties" : "Deepen existing",
    conversion: current_metrics.conversion_rate < 70 ? "Review testing process" : "Excellent"
  };
}
```
