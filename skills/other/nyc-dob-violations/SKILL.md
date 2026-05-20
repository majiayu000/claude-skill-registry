---
name: nyc-dob-violations
description: Look up DOB and ECB violations for any NYC building.
allowed-tools:
  - WebFetch
  - Write
  - Read
  - Bash
user-invocable: true
---

# /nyc-dob-violations — DOB & ECB Violations

Look up DOB violations and ECB (Environmental Control Board) violations for any NYC building. Flags open violations prominently. No API key required.

## Usage

```
/nyc-dob-violations 120 Broadway, Manhattan
/nyc-dob-violations 1000770001          (BBL)
/nyc-dob-violations 1001389             (BIN)
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

## Step 3: Query Violations

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
