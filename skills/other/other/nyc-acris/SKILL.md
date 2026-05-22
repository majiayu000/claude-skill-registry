---
name: nyc-acris
description: Look up ACRIS property transaction records — deeds, mortgages, liens.
allowed-tools:
  - WebFetch
  - Write
  - Read
  - Bash
user-invocable: true
---

# /nyc-acris — ACRIS Property Transaction Records

Look up ACRIS (Automated City Register Information System) property records — deeds, mortgages, liens, and other recorded documents. Uses a 3-table join across Legals, Master, and Parties datasets. No API key required.

## Usage

```
/nyc-acris 120 Broadway, Manhattan
/nyc-acris 1000770001          (BBL)
/nyc-acris 1001389             (BIN)
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

**Parse BBL into separate components** (required for ACRIS): boro = digit 1, block = digits 2-6 (zero-padded), lot = digits 7-10 (zero-padded).

## Step 3: Query ACRIS (3-Table Join)

**IMPORTANT:** ACRIS requires BBL (not BIN). The Legals table uses separate `borough`, `block`, `lot` fields — not a combined BBL field.

### Step 3a: Get Document IDs from Legals Table
```
https://data.cityofnewyork.us/resource/8h5j-fqxa.json?borough={boro}&block={block}&lot={lot}&$order=good_through_date DESC&$limit=20
```
Extract `document_id` from each row. These are the join keys for the next two queries.

### Step 3b: Get Document Details from Master Table
Build a `$where` clause with the document_ids from Step 3a:
```
https://data.cityofnewyork.us/resource/bnx9-e6tj.json?$where=document_id IN ('{id1}','{id2}','{id3}',...)&$order=doc_date DESC
```
Key fields: `document_id`, `record_type`, `crfn`, `doc_type`, `doc_date`, `doc_amount`, `recorded_filed`

### Step 3c: Get Parties from Parties Table
Same document_ids:
```
https://data.cityofnewyork.us/resource/636b-3b5g.json?$where=document_id IN ('{id1}','{id2}','{id3}',...)
```
Key fields: `document_id`, `party_type`, `name`, `address_1`, `city`, `state`, `zip`

Party types: `1` = Grantor (seller/borrower/assignor), `2` = Grantee (buyer/lender/assignee)

### Step 3d: Look Up Document Type Codes
Fetch once to translate `doc_type` codes to descriptions:
```
https://data.cityofnewyork.us/resource/7isb-wh4c.json?$limit=200
```
Common codes: DEED, MTGE (Mortgage), AGMT (Agreement), ASST (Assignment), SAT (Satisfaction), RPTT (Transfer Tax), ALIS (Assignment of Leases), UCC1 (UCC Filing), MCON (Mortgage Consolidation)

### Joining the Data

For each document_id:
1. Get date, type, and amount from Master
2. Get grantor(s) and grantee(s) from Parties
3. Translate doc_type code using the codes table
4. Group by document type category

## Step 4: Print Results

```markdown
## Property Records (ACRIS) — {Address}

**BBL:** {bbl} (Borough {boro}, Block {block}, Lot {lot})
**Documents found:** {count} (showing 20 most recent)

### Deeds (Ownership)
| Date | Doc Type | Amount | From (Grantor) | To (Grantee) |
|------|----------|--------|----------------|--------------|
| YYYY-MM-DD | Deed | $X,XXX,XXX | ... | ... |

**Current owner (per most recent deed):** {grantee name}

### Mortgages
| Date | Amount | Lender (Grantee) | Borrower (Grantor) |
|------|--------|-------------------|---------------------|
| YYYY-MM-DD | $X,XXX,XXX | ... | ... |

### Other Documents
| Date | Doc Type | Amount | Grantor | Grantee |
|------|----------|--------|---------|---------|
| ... | Assignment | ... | ... | ... |

**Note:** Condo units may have records on both the unit lot and the parent condo lot. If results seem incomplete, try querying the main condo lot as well.

Source: [ACRIS Real Property](https://data.cityofnewyork.us/City-Government/ACRIS-Real-Property-Master/bnx9-e6tj)
```

If no documents found: "No ACRIS records found for this property."

### Conventions
- All dates: YYYY-MM-DD
- Dollar amounts: comma-separated ($1,234,567)
- Limit to 20 most recent documents. Note if truncated.
- If Socrata returns empty array: "No results found"
- If HTTP error: note it and suggest checking the address
- If the user requests, write results to a file
