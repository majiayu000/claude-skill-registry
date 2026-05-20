---
name: nyc-dob-permits
description: Look up DOB permit and job filing history for any NYC building.
allowed-tools:
  - WebFetch
  - Write
  - Read
  - Bash
user-invocable: true
---

# /nyc-dob-permits — DOB Permit & Filing History

Look up all DOB permits and job filings for any NYC building across both Legacy BIS and DOB NOW systems. No API key required.

## Usage

```
/nyc-dob-permits 120 Broadway, Manhattan
/nyc-dob-permits 1000770001          (BBL)
/nyc-dob-permits 1001389             (BIN)
```

## Step 1: Parse Input

Accept one of:
- **Address + Borough/Zip** — "120 Broadway, Manhattan" or "120 Broadway 10271"
- **BBL** — 10-digit number (boro 1 + block 5 + lot 4)
- **BIN** — 7-digit Building Identification Number

Borough codes: Manhattan=1/MN, Bronx=2/BX, Brooklyn=3/BK, Queens=4/QN, Staten Island=5/SI

## Step 2: Resolve via PLUTO

Query PLUTO to get BBL, BIN, and building metadata. No API key needed.

By BBL:
```
https://data.cityofnewyork.us/resource/64uk-42ks.json?bbl={BBL}
```

By address:
```
https://data.cityofnewyork.us/resource/64uk-42ks.json?$where=upper(address) LIKE '%{STREET}%'&borough='{BORO_CODE}'&$limit=5
```

**Address normalization:** Uppercase, strip unit/apt suffixes. Borough names to codes: Manhattan=MN, Bronx=BX, Brooklyn=BK, Queens=QN, Staten Island=SI. If multiple results, ask the user to pick. If zero, try variations or suggest providing a BBL.

Store from PLUTO: `bbl`, `bin` (or `bldgbin`), `address`, `borough`, `bldgclass`, `zonedist1`, `yearbuilt`, `ownername`, `numfloors`, `lotarea`, `latitude`, `longitude`.

Parse BBL into: boro (1 digit), block (5 digits zero-padded), lot (4 digits zero-padded).

## Step 3: Query DOB Permits & Filings

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
Key fields: `job_filing_number`, `permit_status`, `filing_date`, `approved_date`, `job_type`

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
