---
name: nyc-dob-violations
description: Look up open and resolved DOB and ECB violations for any NYC building, with class, status, and penalty detail. Use when the user asks whether a building has violations, stop-work orders, or outstanding ECB penalties. NYC only; for housing-code violations use /nyc-hpd.
allowed-tools:
  - WebFetch
  - Write
  - Read
  - Bash
---

# /nyc-dob-violations — DOB & ECB Violations

Look up DOB violations and ECB (Environmental Control Board) violations for any NYC building. Flags open violations prominently. No API key required.

## Usage

```
/nyc-dob-violations 120 Broadway, Manhattan
/nyc-dob-violations 1000770001          (BBL)
/nyc-dob-violations 1001389             (BIN)
```

## Steps 1–2: Parse Input & Resolve BBL/BIN

Read `../nyc-property-report/pluto-resolution.md` (shared by all 7 NYC due-diligence skills) and follow it: parse the input (address, BBL, or BIN), resolve via PLUTO, and resolve BIN via Building Footprints — **BIN is required** for every query in Step 3.

## Step 3: Query Violations

Dataset IDs and field names are canonical in `../nyc-property-report/socrata-reference.md` — on any disagreement, the reference wins.

Query 3 datasets using BIN:

### DOB Violations
```
https://data.cityofnewyork.us/resource/3h2n-5cm9.json?$where=bin='{BIN}'&$order=issue_date DESC&$limit=50
```
Key fields: `isn_dob_bis_viol`, `violation_type`, `issue_date`, `violation_category`, `disposition_date`, `disposition_comments`

### ECB Violations
```
https://data.cityofnewyork.us/resource/6bgk-3dad.json?$where=bin='{BIN}'&$order=issue_date DESC&$limit=50
```
Key fields: `isn_dob_bis_extract`, `ecb_violation_number`, `violation_type`, `issue_date`, `penality_imposed`, `amount_paid`, `balance_due`, `hearing_status`, `ecb_violation_status`, `severity`

### Active/Open Violations
```
https://data.cityofnewyork.us/resource/sjhj-bc8q.json?$where=bin='{BIN}'
```
Returns only currently open violations (pre-filtered subset of DOB violations).

## Step 4: Print Results

Open violations go first, flagged with ⚠.

```markdown
## DOB & ECB Violations — {Address}

### ⚠ Open Violations: {count}

| Violation # | Type | Date | Description | Disposition |
|-------------|------|------|-------------|-------------|
| ... | ... | YYYY-MM-DD | ... | ... |

### All DOB Violations ({count} total)

| Violation # | Type | Issue Date | Category | Disposition Date | Comments |
|-------------|------|------------|----------|------------------|----------|
| ... | ... | ... | ... | ... | ... |

### ECB Violations ({count} total)

| ECB # | Date | Violation Type | Severity | Penalty Imposed | Paid | Balance Due | Status |
|-------|------|----------------|----------|-----------------|------|-------------|--------|
| {ecb_violation_number} | {issue_date} | {violation_type} | {severity} | ${penality_imposed} | ${amount_paid} | ${balance_due} | {hearing_status} |

**Total penalties assessed:** ${amount}
**Total balance due:** ${amount}

Source: [DOB Violations](https://data.cityofnewyork.us/Housing-Development/DOB-Violations/3h2n-5cm9) | [ECB Violations](https://data.cityofnewyork.us/Housing-Development/DOB-ECB-Violations/6bgk-3dad)
```

If no violations found: "No DOB or ECB violations found for this property."

### Conventions
- All dates: YYYY-MM-DD
- Dollar amounts: comma-separated ($1,234)
- Open/active items flagged with ⚠
- If Socrata returns empty array: "No results found"
- If HTTP error: note it and suggest checking the address
- If the user requests, write results to a file

## Final Step: Disclaimer + Marker (required)

This skill produces regulatory output. End every report this skill produces — printed in chat or saved to a file — with the canonical disclaimer block from `rules/professional-disclaimer.md`, followed by one blank line and the machine-readable marker, exactly as shown:

```markdown
> **Disclaimer:** This is an AI-generated analysis for preliminary planning purposes. All findings must be verified by a licensed professional before use in design, permitting, or regulatory submissions.

<!-- architecture-studio:requires-disclaimer -->
```

The marker is a single end-of-file sentinel — it appears exactly once, as the last line of the report. The `post-write-disclaimer-check` hook parses saved `.md` reports for the marker and blocks the write if the canonical disclaimer block is missing.
