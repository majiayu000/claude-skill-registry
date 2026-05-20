---
name: nyc-hpd
description: Look up HPD violations, complaints, and building registration for residential buildings.
allowed-tools:
  - WebFetch
  - Write
  - Read
  - Bash
user-invocable: true
---

# /nyc-hpd — HPD Violations, Complaints & Registration

Look up HPD (Housing Preservation & Development) violations, complaints, and building registration for NYC residential buildings. Only applies to residential building classes. No API key required.

## Usage

```
/nyc-hpd 742 Evergreen Terrace, Springfield
/nyc-hpd 3011650045          (BBL)
/nyc-hpd 3388190             (BIN)
```

## Step 1: Parse Input

Accept one of:
- **Address + Borough/Zip** — "742 Evergreen Terrace, Springfield 62704"
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

### Check Building Class

**Before querying HPD**, check `bldgclass` from PLUTO. HPD only applies to residential buildings — classes starting with A, B, C, D, R, or S.

If the building class does NOT start with one of those letters, print:
> "Building class {X} — HPD records not applicable (non-residential)."

And stop. Do not query HPD APIs.

## Step 3: Query HPD Datasets

**IMPORTANT:** HPD uses `boroid` (not `borough`). And `block`/`lot` are separate fields — not a combined BBL.

### HPD Violations
```
https://data.cityofnewyork.us/resource/wvxf-dwi5.json?$where=boroid='{boro}' AND block='{block}' AND lot='{lot}'&$order=inspectiondate DESC&$limit=50
```
Key fields: `violationid`, `violationclass`, `inspectiondate`, `approveddate`, `originalcertifybydate`, `novdescription`

### Open HPD Violations
```
https://data.cityofnewyork.us/resource/csn4-vhvf.json?$where=boroid='{boro}' AND block='{block}' AND lot='{lot}'
```
Pre-filtered to currently open violations.

### Complaints

**Note:** The complaints dataset uses `borough` (text like "MANHATTAN", "BRONX", "BROOKLYN", "QUEENS", "STATEN ISLAND") — NOT `boroid`. Map boro codes: 1→MANHATTAN, 2→BRONX, 3→BROOKLYN, 4→QUEENS, 5→STATEN ISLAND.

```
https://data.cityofnewyork.us/resource/ygpa-z7cr.json?$where=borough='{BOROUGH_NAME}' AND block='{block}' AND lot='{lot}'&$order=received_date DESC&$limit=30
```
Key fields: `complaint_id`, `received_date`, `complaint_status`, `complaint_status_date`, `major_category`, `minor_category`, `problem_status`

### Registrations
```
https://data.cityofnewyork.us/resource/tesw-yqqr.json?$where=boroid='{boro}' AND block='{block}' AND lot='{lot}'
```
Key fields: `registrationid`, `buildingid`, `registrationenddate`, `ownerfirstname`, `ownerlastname`

## Step 4: Print Results

```markdown
## HPD — {Address}

### Registration
| Field | Value |
|-------|-------|
| Registration ID | ... |
| Owner | {ownerfirstname} {ownerlastname} |
| Registration Expiry | YYYY-MM-DD |

### ⚠ Open Violations: {count}
**Class C (Immediately Hazardous):** {count} ⚠
**Class B (Hazardous):** {count}
**Class A (Non-Hazardous):** {count}

| Violation ID | Class | Inspection Date | Description | Certify By |
|-------------|-------|-----------------|-------------|------------|
| ... | C ⚠ | YYYY-MM-DD | ... | YYYY-MM-DD |

### All Violations ({count} total, showing 50 most recent)
| Violation ID | Class | Inspection Date | Approved Date | Description |
|-------------|-------|-----------------|---------------|-------------|

### Recent Complaints ({count} total, showing 30 most recent)
| Complaint ID | Received | Category | Status | Status Date |
|-------------|----------|--------|-------------|

Source: [HPD Violations](https://data.cityofnewyork.us/Housing-Development/Housing-Maintenance-Code-Violations/wvxf-dwi5) | [HPD Complaints](https://data.cityofnewyork.us/Housing-Development/Housing-Maintenance-Code-Complaints-and-Problems/ygpa-z7cr)
```

If no results: "No HPD violations, complaints, or registrations found for this property."

### Conventions
- All dates: YYYY-MM-DD
- Class C violations always flagged with ⚠ (immediately hazardous — must be corrected within 24 hours)
- Open/active items listed first
- If Socrata returns empty array: "No results found"
- If HTTP error: note it and suggest checking the address
- If the user requests, write results to a file
