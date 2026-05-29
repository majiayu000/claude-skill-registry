---
name: Knack Filter Sort
description: Dynamic filtering, sorting, and query optimization for HTI dashboards and compliance reports. Reduces API payload size and improves dashboard perfo...
allowed-tools: Read, Edit
---

# Knack Filter Sort

## Purpose
Dynamic filtering, sorting, and query optimization for HTI dashboards and compliance reports. Reduces API payload size and improves dashboard performance.

## Filter Syntax

### Basic Structure
```json
{
  "match": "and",
  "rules": [
    {
      "field": "field_123",
      "operator": "is",
      "value": "Ready for Donation"
    }
  ]
}
```

### Multiple Conditions
```json
{
  "match": "and",
  "rules": [
    {
      "field": "field_status",
      "operator": "is",
      "value": "Ready"
    },
    {
      "field": "field_county",
      "operator": "is",
      "value": "Wake"
    }
  ]
}
```

## Operators

### Text Fields
- `is` - Exact match
- `is not` - Exclusion
- `contains` - Substring match
- `starts with` - Prefix match
- `ends with` - Suffix match

### Number Fields
- `is` - Equal to
- `is not` - Not equal
- `>` - Greater than
- `<` - Less than
- `>=` - Greater than or equal
- `<=` - Less than or equal

### Date Fields
- `is` - Specific date
- `is before` - Earlier than
- `is after` - Later than
- `is during` - Date range
- `is today`
- `is this week`
- `is this month`
- `is this year`

### Boolean Fields
- `is` - True/False

## Core Functions

### build_filter
**Purpose**: Construct Knack-compatible filter objects

**Example**:
```javascript
const filter = build_filter({
  match: "and",
  rules: [
    { field: "field_5", operator: "is", value: "Converted" },
    { field: "field_12", operator: "is after", value: "2025-01-01" }
  ]
});
```

### apply_sort
**Purpose**: Sort results by field and direction

**Parameters**:
- `sort_field` (string): Field identifier (e.g., "field_7")
- `sort_order` (string): "asc" or "desc"

**Example**:
```javascript
const sort = apply_sort({
  sort_field: "field_acquisition_date",
  sort_order: "desc"
});
```

### combine_filters
**Purpose**: Merge multiple filter sets (AND/OR logic)

**Example**:
```javascript
const combined = combine_filters({
  operator: "or",
  filters: [wake_filter, durham_filter, vance_filter]
});
```

## HTI-Specific Filters

### Grant Reporting Filters

#### Acquired This Quarter
```javascript
const q1_acquired = build_filter({
  match: "and",
  rules: [
    {
      field: "field_acquisition_date",
      operator: "is during",
      range: { start: "2025-01-01", end: "2025-03-31" }
    }
  ]
});
```

#### Ready for Donation
```javascript
const ready_devices = build_filter({
  match: "and",
  rules: [
    { field: "field_status", operator: "is", value: "Ready for Donation" },
    { field: "field_tested", operator: "is", value: true }
  ]
});
```

#### By County (15-County Coverage)
```javascript
const wake_county = build_filter({
  match: "and",
  rules: [
    { field: "field_target_county", operator: "is", value: "Wake" }
  ]
});
```

#### Recurring Donors (2026 Goal: 6+ with 50+ laptops)
```javascript
const recurring_donors = build_filter({
  match: "and",
  rules: [
    { field: "field_donation_count", operator: ">=", value: 3 },
    { field: "field_total_laptops", operator: ">=", value: 50 }
  ]
});
```

#### Training Sessions (156+ Hours Goal)
```javascript
const training_hours = build_filter({
  match: "and",
  rules: [
    { field: "field_session_date", operator: "is this year", value: "2025" },
    { field: "field_session_status", operator: "is", value: "Completed" }
  ]
});
```

### Dashboard Filters

#### Devices Needing Action
```javascript
const needs_action = build_filter({
  match: "or",
  rules: [
    { field: "field_status", operator: "is", value: "Acquired - Needs Testing" },
    { field: "field_status", operator: "is", value: "Failed Testing" },
    { field: "field_status", operator: "is", value: "Awaiting Parts" }
  ]
});
```

#### High-Value Donors (>$500)
```javascript
const major_donors = build_filter({
  match: "and",
  rules: [
    { field: "field_donation_value", operator: ">", value: 500 }
  ]
});
```

## Sort Configurations

### Common Sorts

#### Most Recent First
```javascript
apply_sort({
  sort_field: "field_acquisition_date",
  sort_order: "desc"
});
```

#### Alphabetical by County
```javascript
apply_sort({
  sort_field: "field_county",
  sort_order: "asc"
});
```

#### Highest Donation Value
```javascript
apply_sort({
  sort_field: "field_donation_value",
  sort_order: "desc"
});
```

## Query Optimization

### Best Practices

1. **Filter at API level** (not client-side) to reduce payload
2. **Use indexed fields** for faster queries
3. **Combine filters** rather than chaining requests
4. **Cache filtered results** for repeated dashboard loads

### Performance Comparison

```javascript
// ❌ BAD: Fetch all, filter client-side
const all = await get_records("object_1"); // 3,500+ records
const ready = all.filter(d => d.status === "Ready"); // Slow, wasteful

// ✅ GOOD: Filter at API level
const ready = await get_records("object_1", {
  filters: build_filter({
    rules: [{ field: "field_status", operator: "is", value: "Ready" }]
  })
}); // Only returns ~200 records
```

## Integration with Pagination

```javascript
// Filter + paginate for large result sets
const all_wake_devices = await fetch_all_pages("object_1", {
  filters: build_filter({
    rules: [{ field: "field_county", operator: "is", value: "Wake" }]
  }),
  sort: apply_sort({ sort_field: "field_date", sort_order: "desc" })
});
```

## Error Handling

```javascript
try {
  const filtered = await get_records("object_1", { filters: my_filter });
} catch (error) {
  if (error.message.includes("invalid field")) {
    console.error("Filter references non-existent field");
  }
}
```

## Integration Points

- **knack_reader**: Apply filters to get_records calls
- **knack_pagination**: Consistent filters across paginated requests
- **knack_dashboard_ai**: Dynamic filter generation based on user input
- **knack_reporting_sync**: Quarterly report filtering (dates, counties, statuses)
- **knack_goal_tracker**: Filter by goal-relevant criteria

## NCDIT Compliance
- Filter by reporting period (quarterly)
- Exclude test/dummy records
- Include only grant-funded devices
- Separate operational vs. financial data
