---
name: nyc-acris
description: Look up ACRIS property transaction records for any NYC property — deeds, mortgages, satisfactions, liens, and ownership history. Use when the user asks who owns a building, when it last sold or for how much, or whether there are mortgages or liens against it. NYC only; for permits or violations use the DOB skills.
allowed-tools:
  - WebFetch
  - Write
  - Read
  - Bash
---

# /nyc-acris — ACRIS Property Transaction Records

Look up ACRIS (Automated City Register Information System) property records — deeds, mortgages, liens, and other recorded documents. Uses a 3-table join across Legals, Master, and Parties datasets. No API key required.

## Usage

```
/nyc-acris 120 Broadway, Manhattan
/nyc-acris 1000770001          (BBL)
/nyc-acris 1001389             (BIN)
```

## Steps 1–2: Parse Input & Resolve BBL

Read `../nyc-property-report/pluto-resolution.md` (shared by all 7 NYC due-diligence skills) and follow it: parse the input (address, BBL, or BIN) and resolve via PLUTO.

**This skill's delta:** parsing the BBL into separate boro/block/lot components (per the shared file) is REQUIRED — the ACRIS Legals table has no combined BBL field. BIN resolution is only needed when the user's input was a BIN.

## Step 3: Query ACRIS (3-Table Join)

Dataset IDs and field names are canonical in `../nyc-property-report/socrata-reference.md` — on any disagreement, the reference wins.

**IMPORTANT:** ACRIS requires BBL (not BIN). The Legals table uses separate `borough`, `block`, `lot` fields — not a combined BBL field.

### Step 3a: Get Document IDs from Legals Table
```
https://data.cityofnewyork.us/resource/8h5j-fqxa.json?borough={boro}&block={block}&lot={lot}&$order=good_through_date DESC&$limit=20
```
Extract `document_id` from each row. These are the join keys for the next two queries.

### Step 3b: Get Document Details from Master Table
Build a `$where` clause with the document_ids from Step 3a:
```
https://data.cityofnewyork.us/resource/bnx9-e6tj.json?$where=document_id IN ('{id1}','{id2}','{id3}',...)&$order=document_date DESC
```
Key fields: `document_id`, `record_type`, `crfn`, `doc_type`, `document_date`, `document_amt`, `recorded_datetime` (NOT `doc_date`/`doc_amount`/`recorded_filed` — those fields don't exist and 400)

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

## Final Step: Disclaimer + Marker (required)

This skill produces regulatory output. End every report this skill produces — printed in chat or saved to a file — with the canonical disclaimer block from `rules/professional-disclaimer.md`, followed by one blank line and the machine-readable marker, exactly as shown:

```markdown
> **Disclaimer:** This is an AI-generated analysis for preliminary planning purposes. All findings must be verified by a licensed professional before use in design, permitting, or regulatory submissions.

<!-- architecture-studio:requires-disclaimer -->
```

The marker is a single end-of-file sentinel — it appears exactly once, as the last line of the report. The `post-write-disclaimer-check` hook parses saved `.md` reports for the marker and blocks the write if the canonical disclaimer block is missing.
