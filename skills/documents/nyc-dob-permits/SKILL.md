---
name: nyc-dob-permits
description: Look up DOB permit and job filing history for any NYC building — new-building, alteration, and demolition filings with status and dates. Use when the user asks what work was filed or permitted at an address, or to gauge renovation history during due diligence. NYC only; for open violations use /nyc-dob-violations.
allowed-tools:
  - WebFetch
  - Write
  - Read
  - Bash
---

# /nyc-dob-permits — DOB Permit & Filing History

Look up all DOB permits and job filings for any NYC building across both Legacy BIS and DOB NOW systems. No API key required.

## Usage

```
/nyc-dob-permits 120 Broadway, Manhattan
/nyc-dob-permits 1000770001          (BBL)
/nyc-dob-permits 1001389             (BIN)
```

## Steps 1–2: Parse Input & Resolve BBL/BIN

Read `../nyc-property-report/pluto-resolution.md` (shared by all 7 NYC due-diligence skills) and follow it: parse the input (address, BBL, or BIN), resolve via PLUTO, and resolve BIN via Building Footprints — **BIN is required** for every query in Step 3.

## Step 3: Query DOB Permits & Filings

Dataset IDs and field names are canonical in `../nyc-property-report/socrata-reference.md` — on any disagreement, the reference wins.

Query all 4 datasets using BIN. **IMPORTANT:** Legacy datasets use `bin__` (double underscore). DOB NOW datasets use `bin`.

### Legacy Permit Issuance
```
https://data.cityofnewyork.us/resource/ipu4-2q9a.json?$where=bin__='{BIN}'&$order=issuance_date DESC&$limit=30
```
Key fields: `permit_si_no`, `job__`, `job_type`, `issuance_date`, `expiration_date`, `permittee_s_first_name`, `permittee_s_last_name`, `owner_s_first_name`, `owner_s_last_name`

### Legacy Job Filings
```
https://data.cityofnewyork.us/resource/ic3t-wcy2.json?$where=bin__='{BIN}'&$order=latest_action_date DESC&$limit=30
```
Key fields: `job__`, `doc__`, `job_type`, `job_status`, `latest_action_date`, `applicant_s_first_name`, `applicant_s_last_name`

### DOB NOW Approved Permits
```
https://data.cityofnewyork.us/resource/rbx6-tga4.json?$where=bin='{BIN}'&$order=approved_date DESC&$limit=30
```
Key fields: `job_filing_number`, `work_permit`, `permit_status`, `work_type`, `approved_date`, `issued_date`, `expired_date` (this dataset has NO `filing_date` or `job_type` — use `approved_date` / `work_type`)

### DOB NOW Job Filings
```
https://data.cityofnewyork.us/resource/w9ak-ipjd.json?$where=bin='{BIN}'&$order=filing_date DESC&$limit=30
```
Key fields: `job_filing_number`, `filing_status`, `filing_date`, `job_type`

## Step 4: Print Results

Merge all results, sort by date descending. Group by job type:
- **NB** = New Building
- **A1** = Alteration Type 1 (major — changes use/egress/occupancy)
- **A2** = Alteration Type 2 (multiple work types)
- **A3** = Alteration Type 3 (minor, one work type)
- **DM** = Demolition
- **Other** = Everything else

```markdown
## DOB Permits & Filings — {Address}

**Total found:** {count} ({x} legacy, {y} DOB NOW)

### New Building (NB)
| Date | Job # | Permit # | Status | Applicant |
|------|-------|----------|--------|-----------|
| ... | ... | ... | ... | ... |

### Alteration Type 1 (A1)
| Date | Job # | Permit # | Work Type | Status | Applicant |
|------|-------|----------|-----------|--------|-----------|

### Alteration Type 2-3 (A2/A3)
{table}

### Demolition (DM)
{table if any}

### Other
{table if any}

**Note:** Pre-BIS records (before ~1989) are not digitized. If this building predates 1989 and few records appear, earlier permits exist only on paper.

Source: [DOB Permit Issuance](https://data.cityofnewyork.us/Housing-Development/DOB-Permit-Issuance/ipu4-2q9a) | [DOB Job Filings](https://data.cityofnewyork.us/Housing-Development/DOB-Job-Application-Filings/ic3t-wcy2) | [DOB NOW Permits](https://data.cityofnewyork.us/Housing-Development/DOB-NOW-Build-Approved-Permits/rbx6-tga4) | [DOB NOW Filings](https://data.cityofnewyork.us/Housing-Development/DOB-NOW-Build-Job-Application-Filings/w9ak-ipjd)
```

If no results from any dataset: "No DOB permits or filings found for this property."

### Conventions
- All dates: YYYY-MM-DD
- If Socrata returns empty array: "No results found"
- If HTTP error: note it and suggest checking the address
- If the user requests, write results to a file
- Check PLUTO `yearbuilt` — if before 1989, add the pre-BIS note

## Final Step: Disclaimer + Marker (required)

This skill produces regulatory output. End every report this skill produces — printed in chat or saved to a file — with the canonical disclaimer block from `rules/professional-disclaimer.md`, followed by one blank line and the machine-readable marker, exactly as shown:

```markdown
> **Disclaimer:** This is an AI-generated analysis for preliminary planning purposes. All findings must be verified by a licensed professional before use in design, permitting, or regulatory submissions.

<!-- architecture-studio:requires-disclaimer -->
```

The marker is a single end-of-file sentinel — it appears exactly once, as the last line of the report. The `post-write-disclaimer-check` hook parses saved `.md` reports for the marker and blocks the write if the canonical disclaimer block is missing.
