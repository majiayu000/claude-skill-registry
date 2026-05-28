---
name: Knack Data Cleaner
description: Ensures accuracy for HTI compliance and performance dashboards through data validation, deduplication, normalization, and integrity checks. Critica...
allowed-tools: Read, Edit
---

# Knack Data Cleaner

## Purpose
Ensures accuracy for HTI compliance and performance dashboards through data validation, deduplication, normalization, and integrity checks. Critical for NCDIT reporting accuracy.

## Core Functions

### deduplicate_records
**Purpose**: Identify and remove/merge duplicate device or donor records

**Detection Strategies**:
- Exact match: Same serial number, donor email, etc.
- Fuzzy match: Similar names, close dates
- Bulk import duplicates: Same acquisition batch

**Example**:
```javascript
const cleaned = await deduplicate_records({
  object_key: "object_1",
  match_fields: ["serial_number", "acquisition_date"],
  strategy: "keep_latest" // or "merge", "keep_first"
});

// Output:
// {
//   original_count: 3520,
//   duplicates_found: 37,
//   final_count: 3483,
//   removed: [
//     { id: "rec_123", reason: "Duplicate serial: ABC123" },
//     // ...
//   ]
// }
```

**Deduplication Strategies**:
```javascript
const strategies = {
  keep_latest: "Retain most recently modified record",
  keep_first: "Keep oldest record (by created_date)",
  merge: "Combine data from all duplicates",
  manual_review: "Flag for human verification"
};
```

### normalize_fields
**Purpose**: Standardize data formats for consistency

**Normalization Rules**:

#### County Names
```javascript
const county_normalizer = {
  "wake": "Wake",
  "WAKE": "Wake",
  "Wake County": "Wake",
  "wake co": "Wake",
  "wake co.": "Wake"
};
```

#### Phone Numbers
```javascript
// (919) 555-1234 → 9195551234
// 919-555-1234 → 9195551234
// 919.555.1234 → 9195551234
const normalizePhone = (phone) => phone.replace(/\D/g, '');
```

#### Emails
```javascript
// Convert to lowercase, trim whitespace
const normalizeEmail = (email) => email.trim().toLowerCase();
```

#### Dates
```javascript
// Standardize to ISO 8601: YYYY-MM-DD
const normalizeDate = (date) => {
  const d = new Date(date);
  return d.toISOString().split('T')[0];
};
```

#### Device Status
```javascript
const status_normalizer = {
  "acquired": "Acquired",
  "ACQUIRED": "Acquired",
  "received": "Acquired",
  "in progress": "In Progress",
  "ready": "Ready for Donation",
  "delivered": "Presented"
};
```

**Example**:
```javascript
const normalized = await normalize_fields({
  dataset: await fetch_all_pages("object_1"),
  rules: {
    county: county_normalizer,
    phone: normalizePhone,
    email: normalizeEmail,
    date: normalizeDate,
    status: status_normalizer
  }
});
```

### validate_integrity
**Purpose**: Check for logical inconsistencies and data quality issues

**Validation Checks**:

#### Date Logic
```javascript
const date_validations = [
  "acquisition_date < conversion_date",
  "conversion_date < presentation_date",
  "all dates within grant period (2024-2026)",
  "no future dates"
];
```

#### Required Fields
```javascript
const required_by_status = {
  "Acquired": ["donor", "acquisition_date", "quantity"],
  "Converted": ["converted_date", "os_installed", "tested"],
  "Presented": ["recipient", "county", "presentation_date"],
  "Discarded": ["discard_reason", "discard_date"]
};
```

#### Value Ranges
```javascript
const range_validations = {
  quantity: { min: 1, max: 500 },
  training_duration: { min: 0.5, max: 8 },
  participants: { min: 1, max: 100 },
  donation_value: { min: 0, max: 50000 }
};
```

#### Geographic Validation
```javascript
const valid_counties = [
  "Wake", "Durham", "Vance", "Franklin", "Granville",
  "Halifax", "Wilson", "Edgecombe", "Martin", "Hertford",
  "Greene", "Warren", "Northampton", "Person", "Nash"
];

const county_validation = (county) => {
  return valid_counties.includes(county);
};
```

**Example**:
```javascript
const validation_report = await validate_integrity({
  dataset: await fetch_all_pages("object_1"),
  rules: {
    dates: date_validations,
    required: required_by_status,
    ranges: range_validations,
    counties: valid_counties
  }
});

// Output:
// {
//   total_records: 3483,
//   valid: 3401,
//   errors: [
//     { record_id: "rec_123", issue: "Conversion date before acquisition" },
//     { record_id: "rec_456", issue: "Invalid county: 'Raleigh'" },
//     { record_id: "rec_789", issue: "Missing required field: donor" }
//   ],
//   warnings: [
//     { record_id: "rec_234", issue: "Unusually high quantity: 450" }
//   ]
// }
```

### fix_common_issues
**Purpose**: Auto-correct known data entry mistakes

**Auto-Fix Rules**:

#### Trim Whitespace
```javascript
const fix_whitespace = (record) => {
  Object.keys(record).forEach(key => {
    if (typeof record[key] === 'string') {
      record[key] = record[key].trim();
    }
  });
  return record;
};
```

#### Fix Capitalization
```javascript
const fix_capitalization = (record) => {
  if (record.donor_name) {
    record.donor_name = toTitleCase(record.donor_name);
  }
  if (record.county) {
    record.county = county_normalizer[record.county.toLowerCase()] || record.county;
  }
  return record;
};
```

#### Infer Missing Data
```javascript
const infer_missing = (record) => {
  // If county missing but zip code present, infer county
  if (!record.county && record.zip_code) {
    record.county = inferCountyFromZip(record.zip_code);
  }

  // If discard reason missing but status is Discarded, set default
  if (record.status === "Discarded" && !record.discard_reason) {
    record.discard_reason = "Not specified";
  }

  return record;
};
```

**Example**:
```javascript
const fixed = await fix_common_issues({
  dataset: await fetch_all_pages("object_1"),
  auto_fixes: [
    "trim_whitespace",
    "fix_capitalization",
    "infer_missing_counties",
    "standardize_phone_numbers"
  ]
});

// Output:
// {
//   processed: 3483,
//   fixed: 287,
//   fixes_by_type: {
//     whitespace: 145,
//     capitalization: 67,
//     inferred_county: 42,
//     phone_format: 33
//   }
// }
```

### remove_test_records
**Purpose**: Exclude dummy/test data from production reports

**Detection**:
```javascript
const is_test_record = (record) => {
  const test_indicators = [
    record.donor_name?.toLowerCase().includes("test"),
    record.donor_email?.includes("test@"),
    record.donor_email?.includes("example.com"),
    record.serial_number?.startsWith("TEST"),
    record.notes?.toLowerCase().includes("do not count")
  ];

  return test_indicators.some(indicator => indicator === true);
};
```

**Example**:
```javascript
const production_only = await remove_test_records({
  dataset: await fetch_all_pages("object_1")
});

// Output:
// {
//   original: 3483,
//   test_records_removed: 8,
//   production_records: 3475
// }
```

### enrich_records
**Purpose**: Add calculated or derived fields

**Enrichment Operations**:

#### Add Calculated Fields
```javascript
const enrich = (record) => {
  // Add age of device
  record.days_since_acquisition = daysBetween(record.acquisition_date, new Date());

  // Add conversion time
  if (record.converted_date && record.acquisition_date) {
    record.days_to_convert = daysBetween(record.acquisition_date, record.converted_date);
  }

  // Add delivery time
  if (record.presentation_date && record.converted_date) {
    record.days_to_deliver = daysBetween(record.converted_date, record.presentation_date);
  }

  // Flag slow conversions
  record.conversion_delayed = record.days_to_convert > 30;

  return record;
};
```

#### Add Geographic Context
```javascript
const add_region = (record) => {
  const regions = {
    "Triangle": ["Wake", "Durham", "Franklin"],
    "Northeast": ["Vance", "Granville", "Warren", "Halifax"],
    "Eastern": ["Wilson", "Edgecombe", "Martin", "Greene"]
  };

  record.region = Object.keys(regions).find(region =>
    regions[region].includes(record.county)
  ) || "Other";

  return record;
};
```

#### Add Donor Tier
```javascript
const add_donor_tier = (record) => {
  if (record.donation_value > 1000) {
    record.donor_tier = "Major";
  } else if (record.donation_value > 500) {
    record.donor_tier = "Significant";
  } else {
    record.donor_tier = "Standard";
  }
  return record;
};
```

## HTI-Specific Cleaning Workflows

### Pre-Quarterly Report Cleaning
```javascript
async function clean_for_quarterly_report(quarter, year) {
  // 1. Fetch quarter data
  const raw_data = await fetch_all_pages("object_1", {
    filters: quarterly_filter(quarter, year)
  });

  // 2. Remove test records
  const production = await remove_test_records({ dataset: raw_data });

  // 3. Deduplicate
  const unique = await deduplicate_records({
    dataset: production.production_records,
    match_fields: ["serial_number"]
  });

  // 4. Normalize
  const normalized = await normalize_fields({
    dataset: unique.records,
    rules: all_normalizers
  });

  // 5. Validate
  const validated = await validate_integrity({
    dataset: normalized,
    rules: compliance_rules
  });

  // 6. Fix auto-fixable issues
  const fixed = await fix_common_issues({
    dataset: validated.valid_records
  });

  return {
    clean_data: fixed,
    cleaning_summary: {
      original: raw_data.length,
      test_removed: production.test_records_removed,
      duplicates: unique.duplicates_found,
      validation_errors: validated.errors.length,
      auto_fixed: fixed.fixed
    }
  };
}
```

### Pre-Dashboard Data Cleaning
```javascript
async function clean_for_dashboard() {
  const all_data = await fetch_all_pages("object_1");

  // Quick cleaning for real-time dashboard
  const cleaned = all_data
    .filter(r => !is_test_record(r))
    .map(fix_whitespace)
    .map(fix_capitalization)
    .map(enrich);

  return cleaned;
}
```

## Data Quality Monitoring

### Generate Data Quality Report
```javascript
async function data_quality_report() {
  const all_records = await fetch_all_pages("object_1");

  const report = {
    total_records: all_records.length,
    completeness: {
      with_donor: all_records.filter(r => r.donor).length,
      with_county: all_records.filter(r => r.county).length,
      with_serial: all_records.filter(r => r.serial_number).length
    },
    accuracy: {
      valid_counties: all_records.filter(r => valid_counties.includes(r.county)).length,
      logical_dates: all_records.filter(r => validate_dates(r)).length
    },
    duplicates: await find_duplicates(all_records),
    test_records: all_records.filter(is_test_record).length
  };

  return report;
}
```

### Automated Quality Checks
```javascript
// Run daily at 2 AM
cron.schedule('0 2 * * *', async () => {
  const report = await data_quality_report();

  if (report.duplicates.length > 10) {
    await alert_admin("High duplicate count detected");
  }

  if (report.accuracy.valid_counties / report.total_records < 0.95) {
    await alert_admin("County data quality below threshold");
  }
});
```

## Integration Points

- **knack_reader**: Fetch data for cleaning
- **knack_pagination**: Process large datasets
- **knack_reporting_sync**: Clean before report generation
- **knack_dashboard_ai**: Ensure metrics accuracy
- **knack_goal_tracker**: Validate progress data
- **knack_filter_sort**: Filter out invalid records

## Best Practices

1. **Clean before every report**: Don't trust raw data
2. **Log all cleaning operations**: Audit trail for compliance
3. **Manual review for ambiguous cases**: Don't auto-fix everything
4. **Run quality checks daily**: Catch issues early
5. **Version cleaned datasets**: Track data lineage

## Grant Compliance

### NCDIT Data Standards
- No test/dummy records in official reports
- All dates must be within grant period
- County assignments must be accurate (15-county requirement)
- Device lifecycle dates must be logical
- Training hours must have supporting documentation

### Audit Trail
```javascript
const cleaning_log = {
  timestamp: new Date(),
  operation: "quarterly_report_cleaning",
  quarter: "Q1",
  year: "2025",
  records_processed: 875,
  issues_found: 23,
  auto_fixed: 18,
  manual_review_needed: 5,
  performed_by: "automated_system"
};
```
