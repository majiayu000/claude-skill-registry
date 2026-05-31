---
name: nyc-bsa
description: Look up BSA variances and special permits for any NYC property.
allowed-tools:
  - WebFetch
  - Write
  - Read
  - Bash
user-invocable: true
---

# /nyc-bsa — BSA Variances & Special Permits

Look up Board of Standards and Appeals (BSA) applications, variances, and special permits for any NYC property. Records available from 1998 to present. No API key required.

## Usage

```
/nyc-bsa 120 Broadway, Manhattan
/nyc-bsa 1000770001          (BBL)
/nyc-bsa 1001389             (BIN)
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

## Step 3: Query BSA Applications

Query by BBL first:
```
https://data.cityofnewyork.us/resource/yvxd-uipr.json?$where=bbl='{BBL}'&$order=date DESC
```

If no results, try address fallback:
```
https://data.cityofnewyork.us/resource/yvxd-uipr.json?$where=upper(street_name) LIKE '%{STREET}%' AND borough='{BOROUGH}'&$order=date DESC
```

Key fields: `application`, `section`, `status`, `date`, `street_number`, `street_name`, `bbl`, `borough`, `decisions_url`, `project_description`

## Step 4: Print Results

```markdown
## BSA Variances & Special Permits — {Address}

| Application # | Section | Status | Date | Description | Decisions |
|---------------|---------|--------|------|-------------|-----------|
| {application} | {section} | {status} | YYYY-MM-DD | {project_description} | {decisions_url} |

**Note:** Approved variances remain with the land. Check if conditions affect proposed work.

Source: [BSA Applications](https://data.cityofnewyork.us/City-Government/BSA-Applications-Status/yvxd-uipr)
```

If no applications found: "No BSA applications found for this property (records from 1998-present)."

### Conventions
- All dates: YYYY-MM-DD
- If Socrata returns empty array: "No results found"
- If HTTP error: note it and suggest checking the address
- If the user requests, write results to a file
