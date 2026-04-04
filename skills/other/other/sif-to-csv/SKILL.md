---
name: sif-to-csv
description: Convert a SIF (Standard Interchange Format) file to a clean, readable CSV or Google Sheet.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - AskUserQuestion
  - mcp__google__sheets_values_get
  - mcp__google__sheets_values_update
  - mcp__google__sheets_spreadsheet_get
user-invocable: true
---

# /sif-to-csv — SIF to CSV Converter

Converts a SIF (Standard Interchange Format) file from a dealer or procurement system into a clean, human-readable CSV or Google Sheet. Translates field codes to column headers, expands options and attributes, calculates pricing, and computes totals.

## When to Use

- Received a SIF file from a dealer and need to review it as a spreadsheet
- Importing dealer pricing back into your FF&E schedule
- Comparing a dealer quote (SIF) against your original specification
- Loading dealer data into the master Google Sheet

## SIF Format Reference

SIF is a text-based key-value format. Each line is `CODE=VALUE`, terminated by CRLF. Products are separated by records starting with `PN=`.

### Core fields

| Code | Name | Description |
|------|------|-------------|
| `SF` | Specification File | Project reference (header) |
| `ST` | Specification Title | Display title (header) |
| `PN` | Product Number | SKU — starts a new record |
| `PD` | Product Description | Product name |
| `MC` | Manufacturer Code | 3-5 char code |
| `MN` | Manufacturer Name | Full name |
| `QT` | Quantity | Integer |
| `NT` | Quantity (alt) | Some systems use NT instead of QT |
| `GC` | Category / Group Code | Product category |
| `G0` | Vendor / Group ID | Vendor identifier |

### Pricing fields

| Code | Name | Description |
|------|------|-------------|
| `PL` | List Price | Unit list price |
| `P1`-`P5` | Price Tiers | Alternate price tiers |
| `I1` | Unit List Price (Cyncly) | Cyncly Worksheet |
| `I2` | Purchase Price (Cyncly) | Cyncly Worksheet |
| `S-` / `S%` | Sell Discount % | Sell = PL - (PL × S- × 0.01) |
| `P%` / `B%` | Purchase/Buy % | Cost = PL × (P% × 0.01) |

### Product detail fields

| Code | Name | Description |
|------|------|-------------|
| `TG` | Side Mark / Tag | Room, area, or project tag |
| `ON` / `OD` | Option | Number + description pair |
| `AN` / `AD` | Attribute | Number + description pair |
| `WT` | Weight | Product weight |
| `VO` | Volume | Product volume |
| `PRC` | Product Category (Cyncly) | Cyncly category |

### Link fields

| Code | Name | Description |
|------|------|-------------|
| `ProductURL` | Product Page URL | Link to product page |
| `ImageURL` | Product Image URL | Link to product image |
| `PV` | Picture Path | Local file path |

### Alternate manufacturer codes

| System | Code | Purpose |
|--------|------|---------|
| Standard | `MC` | 3-5 char manufacturer code |
| Cyncly | `MG` | Manufacturer code (replaces MC) |
| CET | `EC` | Manufacturer code (alt) |

## Step 1: Accept Input

**SIF file:**
```
/sif-to-csv ~/Documents/project/dealer-quote.sif
```

**Pasted SIF content:**
```
/sif-to-csv
SF=Project Alpha
ST=Dealer Quote - March 2026
PN=670
PD=Eames Lounge Chair and Ottoman
MC=HMI
QT=3
PL=5695.00
S-=42
TG=Executive Lounge
OD=Santos Palisander / Black MCL Leather
```

## Step 2: Parse SIF

Read the file and parse each record:

1. **Header fields**: Extract `SF` and `ST`
2. **Records**: Split on `PN=` boundaries
3. **For each record**, extract all fields
4. **Detect manufacturer code variant**: look for MC, MG, or EC — normalize to brand name
5. **Detect price variant**: look for PL, P1, I1 — use whichever is present
6. **Detect quantity variant**: look for QT or NT
7. **Calculate derived values**:
   - Sell Price: `PL - (PL × S- × 0.01)` if discount present
   - Net Price: `PL × (P% × 0.01)` if purchase % present
   - Extended List: `PL × QT`
   - Extended Sell: `Sell Price × QT`

### Manufacturer code expansion

| MC | Brand | MC | Brand |
|----|-------|----|-------|
| HMI | Herman Miller | BLU | Blu Dot |
| MKN | MillerKnoll | DWR | Design Within Reach |
| KNL | Knoll | FRH | Fritz Hansen |
| STC | Steelcase | VIT | Vitra |
| HAW | Haworth | ARP | Arper |
| TEK | Teknion | FLS | Flos |
| HUM | Humanscale | LPO | Louis Poulsen |
| KIM | Kimball | ART | Artemide |
| OFS | OFS | HBF | HBF |
| GEI | Geiger | BRN | Bernhardt |

For unknown codes, keep as-is and flag.

### Options and attributes
- Multiple `ON`/`OD` pairs → concatenate into "Options" column, separated by ` | `
- Multiple `AN`/`AD` pairs → concatenate into "Attributes" column, separated by ` | `
- If `AN=DIM`, parse dimension string back into W/D/H if possible

## Step 3: Present Preview

```
## SIF Import: Project Alpha — Dealer Quote March 2026

3 records parsed from dealer-quote.sif

| # | SKU | Product | Brand | Qty | List $ | Disc % | Sell $ | Ext Sell | Options | Tag |
|---|-----|---------|-------|-----|--------|--------|--------|----------|---------|-----|
| 1 | 670 | Eames Lounge Chair | Herman Miller | 3 | $5,695 | 42% | $3,303 | $9,909 | Palisander/Black | Exec Lounge |
| 2 | 164-500 | Saarinen Table 54" | Knoll | 1 | $4,750 | 38% | $2,945 | $2,945 | Arabescato/White | Dining |
| 3 | 462-CG | Gesture Chair | Steelcase | 8 | $1,189 | 45% | $654 | $5,232 | Cogent/Licorice | Open Office |

**Totals:**
- List: $22,147 · Sell: $18,086 · Savings: $4,061 (18.3%)
```

## Step 4: Output

Ask the user for output format:

### CSV file
Save as `{input-name}-parsed.csv`:

```
Item #, SKU, Product, Brand, Qty, List Price, Discount %, Sell Price, Ext List, Ext Sell, Category, Weight, Options, Attributes, Tag, Product URL, Image URL, MC Code
```

### Google Sheet (master schema)
Write to the 33-column schema (defined in `../../schema/product-schema.md`, CRUD patterns in `../../schema/sheet-conventions.md`):
- Column A (Link) ← ProductURL
- Column C (Product Name) ← PD
- Column E (SKU) ← PN
- Column F (Brand) ← MC expanded
- Column J (Category) ← GC or PRC
- Column K-O (Dims) ← parsed from AD where AN=DIM
- Column P (Weight) ← WT
- Column T (List Price) ← PL/P1/I1
- Column U (Sale Price) ← calculated sell price
- Column S (Selected Finish) ← OD
- Column AC (Image URL) ← ImageURL
- Column AD (Tags) ← TG
- Column AE (Notes) ← "From SIF: {ST}. Discount: {S-}%. Qty: {QT} · Ext: ${ext_sell}"
- Column AF (Status) ← "quoted"
- Column AG (Source) ← "sif-to-csv"

### Markdown
Output the table in conversation.

## Step 5: Summary

```
✓ Parsed dealer-quote.sif
  Specification: Project Alpha — Dealer Quote March 2026
  3 records · 12 units
  Total list: $22,147 · Total sell: $18,086 (18.3% avg discount)
  Manufacturers: HMI (1), KNL (1), STC (1)
  Saved to: ~/Documents/project/dealer-quote-parsed.csv
```

## Pairs With

- `/csv-to-sif` — round-trip: create SIF, send to dealer, parse their quote back
- `/product-spec-bulk-cleanup` — normalize the parsed data
- `/ffe-schedule` — reformulate dealer data into a formatted schedule
- `/product-enrich` — add categories and tags to imported products
