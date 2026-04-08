---
name: csv-to-sif
description: Convert a CSV or Excel FF&E product list to SIF (Standard Interchange Format) for dealer and procurement systems.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - AskUserQuestion
user-invocable: true
---

# /csv-to-sif — CSV to SIF Converter

Converts a CSV, Excel, or Google Sheets product list into a SIF (Standard Interchange Format) file for import into dealer and procurement systems like Hedberg, CAP, CET, Cyncly Worksheet, ProjectMatrix, Studio Webware, and Design Manager.

## When to Use

- Sending a specification to a dealer for quoting
- Importing product data into a dealer management system
- Sharing a standardized product list with procurement
- Converting an FF&E schedule into a format dealers expect

## SIF Format Reference

SIF is a text-based key-value format. Each line is `CODE=VALUE`, terminated by CRLF. Products are separated by records starting with `PN=`.

### Core fields

| Code | Name | Required | Description |
|------|------|----------|-------------|
| `SF` | Specification File | No | Project reference (header, once per file) |
| `ST` | Specification Title | No | Display title (header, once per file) |
| `PN` | Product Number | **Yes** | SKU or model number. Marks the start of a new record. |
| `PD` | Product Description | **Yes** | Product name and description |
| `MC` | Manufacturer Code | **Yes** | 3-5 character code (HMI, KNL, STC) |
| `MN` | Manufacturer Name | No | Full manufacturer name |
| `QT` | Quantity | **Yes** | Integer quantity |
| `NT` | Quantity (alt) | No | Some systems use NT instead of QT |
| `GC` | Category / Group Code | No | Product category |
| `G0` | Vendor / Group ID | No | Vendor or dealer identifier |

### Pricing fields

| Code | Name | Description |
|------|------|-------------|
| `PL` | List Price | Unit list price (numeric, no currency symbol) |
| `P1` | Price Tier 1 | Primary price (some systems use P1 instead of PL) |
| `P2` | Price Tier 2 | Alternate price tier |
| `P4` | Price Tier 4 | Alternate price tier |
| `P5` | Price Tier 5 | Alternate price tier |
| `I1` | Unit List Price (Cyncly) | Used by Cyncly Worksheet |
| `I2` | Purchase Price (Cyncly) | Used by Cyncly Worksheet |
| `S-` / `S%` | Sell Discount % | Sell = PL - (PL × S- × 0.01) |
| `P%` / `B%` | Purchase/Buy % | Cost = PL × (P% × 0.01) |

### Product detail fields

| Code | Name | Description |
|------|------|-------------|
| `TG` | Side Mark / Tag | Room name, area code, or project tag |
| `ON` | Option Number | Must pair with OD |
| `OD` | Option Description | Finish, fabric, color selection |
| `AN` | Attribute Number | Must pair with AD |
| `AD` | Attribute Description | Dimension, weight, or other attribute |
| `WT` | Weight | Product weight |
| `VO` | Volume | Product volume |
| `PRC` | Product Category (Cyncly) | Category for Cyncly Worksheet |

### Link fields

| Code | Name | Description |
|------|------|-------------|
| `ProductURL` | Product Page URL | Link to manufacturer product page |
| `ImageURL` | Product Image URL | Link to product image |
| `PV` | Picture Path | Windows bitmap or TIF file path |

### Alternate manufacturer codes (by system)

| System | Code | Purpose |
|--------|------|---------|
| Standard | `MC` | 3-5 char manufacturer code |
| Cyncly Worksheet | `MG` | Manufacturer code (replaces MC) |
| Cyncly Worksheet | `MN` | Full manufacturer name |
| CET / Configura | `EC` | Manufacturer code (alt) |

### File structure example

```
SF=Project Alpha - FF&E Specification
ST=FF&E Schedule — March 2026
PN=670
PD=Eames Lounge Chair and Ottoman
MC=HMI
MN=Herman Miller
GC=Seating
QT=3
PL=5695.00
WT=92
TG=Executive Lounge
OD=Santos Palisander / Black MCL Leather
AN=DIM
AD=32.75W x 32.5D x 33.5H in
ProductURL=https://www.hermanmiller.com/products/seating/lounge-seating/eames-lounge-chair-and-ottoman/
ImageURL=https://www.hermanmiller.com/content/dam/hmicom/page_assets/products/eames_lounge_chair_and_ottoman/mh_prd_ovw_eames_lounge_chair_and_ottoman.jpg

PN=164-500
PD=Saarinen Round Dining Table 54"
MC=KNL
MN=Knoll
GC=Tables
QT=1
PL=4750.00
TG=Dining Area
OD=Arabescato Marble Top / White Base
AN=DIM
AD=54dia x 28.5H in
```

### Rules
- Each line is one field: `CODE=VALUE`
- Lines terminated by CRLF
- Blank line between records
- `PN` starts a new record — must come first in each record
- `ON`/`OD` and `AN`/`AD` pairs must stay together
- No embedded line breaks within a field value
- Empty values use `CODE=` with nothing after the equals sign

## Step 1: Accept Input

**CSV file:**
```
/csv-to-sif ~/Documents/project/product-data-import.csv
```

**Google Sheet:**
```
/csv-to-sif 1FMScYW9guezOWc_m4ClTQxxFIpS6TNRr373R-MJGzgE
```

**Pasted CSV:**
```
/csv-to-sif
Product,Brand,SKU,Qty,Price,Finish,Room
Eames Lounge Chair,Herman Miller,670,3,5695,Walnut/Black Leather,Executive Lounge
Saarinen Table 54,Knoll,164-500,1,4750,Arabescato/White,Dining
```

## Step 2: Choose Target System

Ask which dealer system the SIF file is for (affects which field codes to use):

```
Target system:
1. Standard (Hedberg, CAP, ProjectMatrix) — default
2. CET / Configura (SPEC)
3. Cyncly Worksheet (CAPSIF)
4. Design Manager
```

Default to Standard if not specified. The main differences:
- **Standard**: MC for manufacturer, PL for price, QT for quantity
- **CET**: EC for manufacturer, standard pricing
- **Cyncly**: MG/MN for manufacturer, I1/I2 for pricing, PRC for category
- **Design Manager**: Standard + DXSC, DXBD, DXLC, DXLN extensions

## Step 3: Map Columns

Auto-detect column mappings from header names:

| CSV Column (common names) | SIF Field |
|---------------------------|-----------|
| Product Name, Name, Description, Product | PD |
| SKU, Model, Part Number, Product Number | PN |
| Brand, Manufacturer | MC + MN |
| Qty, Quantity, Count | QT |
| Price, List Price, Unit Price | PL |
| Finish, Color, Configuration | OD |
| Room, Location, Area, Tag, Side Mark | TG |
| Category | GC |
| Weight | WT |
| Discount, Discount % | S- |
| URL, Product URL, Link | ProductURL |
| Image, Image URL | ImageURL |
| W, D, H (dimensions) | AD (with AN=DIM) |

If using the master 33-column schema (defined in `../../schema/product-schema.md`):

See `../../schema/sif-crosswalk.md` for the full column-to-SIF mapping. Key fields:

| Column | SIF Field |
|--------|-----------|
| A (Category) | GC |
| B (Brand) | MC + MN |
| E (Product Name) | PD |
| I (SKU) | PN |
| J (Link) | ProductURL |
| L-P (W, D, H, Seat H, Unit) | AD (with AN=DIM) |
| Q (Weight) | WT |
| R (Materials) | AD (with AN=MAT) |
| S (Colors/Finishes) | OD (with ON=FIN) |
| T (Selected Color/Finish) | OD (primary, replaces S if present) |
| U (List Price) | PL |
| AC (Image URL) | ImageURL |
| AD (Tags) | TG |

If the mapping is ambiguous, ask the user to confirm.

### Manufacturer code lookup

Convert full brand names to standard 3-5 character codes:

| Brand | MC Code | Brand | MC Code |
|-------|---------|-------|---------|
| Herman Miller | HMI | Blu Dot | BLU |
| MillerKnoll | MKN | Design Within Reach | DWR |
| Knoll | KNL | Fritz Hansen | FRH |
| Steelcase | STC | Vitra | VIT |
| Haworth | HAW | Arper | ARP |
| Teknion | TEK | Muuto | MUU |
| Humanscale | HUM | HAY | HAY |
| Kimball | KIM | Flos | FLS |
| National | NAT | Louis Poulsen | LPO |
| OFS | OFS | Artemide | ART |
| HBF | HBF | Restoration Hardware | RHB |
| Bernhardt | BRN | West Elm | WEL |
| Geiger | GEI | CB2 | CB2 |

For unknown brands, use first 3-5 characters uppercased. Flag for the user to verify.

## Step 4: Preview

Show a preview of the first 3 records before generating the file:

```
## SIF Preview (first 3 of 12 records)

Record 1:
  PN=670
  PD=Eames Lounge Chair and Ottoman
  MC=HMI
  MN=Herman Miller
  GC=Seating
  QT=3
  PL=5695.00
  WT=92
  TG=Executive Lounge
  OD=Santos Palisander / Black MCL Leather
  AN=DIM
  AD=32.75W x 32.5D x 33.5H in

...

12 records total. Generate SIF file? (y/n)
```

## Step 5: Generate SIF File

Write the `.sif` file with CRLF line endings:

```bash
# Output path: same directory as input, or specified path
{input-dir}/{input-name}.sif
```

## Step 6: Summary

```
✓ Generated product-data-import.sif
  Target: Standard (Hedberg/CAP/ProjectMatrix)
  12 records · 8 fields per record avg
  Manufacturers: HMI (5), KNL (3), STC (2), BLU (2)
  Total list value: $47,830.00
  Saved to: ~/Documents/project/product-data-import.sif
```

## Pairs With

- `/product-data-import` — generate a schedule first, then convert to SIF
- `/sif-to-csv` — round-trip: CSV → SIF → send to dealer → receive updated SIF → back to CSV
- `/product-data-cleanup` — clean up the CSV before converting
