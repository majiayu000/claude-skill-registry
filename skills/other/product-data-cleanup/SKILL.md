---
name: product-data-cleanup
description: Clean up an FF&E schedule — normalize casing, dimensions, units, language, materials, and formatting for consistency.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - AskUserQuestion
  - mcp__google-sheets__get_sheet_data
  - mcp__google-sheets__update_cells
  - mcp__google-sheets__list_sheets
---

# /product-data-cleanup — Product Data Normalizer

Takes a messy FF&E schedule and normalizes everything: casing, dimensions, units, language, materials vocabulary, currency formatting, and duplicates. Outputs a clean, consistent, spec-ready schedule.

Operates on the **master Google Sheet** — the same 33-column schema used by all product skills. Also works on standalone CSV files and pasted tables.

## Input

The user provides a schedule in one of these ways:

1. **Master Google Sheet** — the shared product library. Provide spreadsheet ID or URL.
2. **File path** — a `.csv`, `.tsv`, `.xlsx` export, or `.md` file
3. **Pasted table** — markdown or tab-separated data in the message

If the input format is unclear, ask.

## Cleanup Rules

### 1. Casing

| Field | Rule | Example |
|-------|------|---------|
| Product Name | Title Case | `eames lounge chair` → `Eames Lounge Chair` |
| Brand | Title Case, preserve known abbreviations | `HERMAN MILLER` → `Herman Miller`, `HAY` → `HAY` |
| Collection | Title Case | `cosm` → `Cosm` |
| Category | Title Case, singular | `chairs` → `Chair`, `TABLES` → `Table` |
| Materials | Sentence case, lowercase after first word | `MOLDED PLYWOOD, FULL GRAIN LEATHER` → `Molded plywood, full grain leather` |
| Colors/Finishes | Title Case per item | `walnut/black leather` → `Walnut / Black Leather` |

**Known brand abbreviations to preserve**: HAY, USM, B&B, DWR, CB2, HBF, OFS, SitOnIt, 3form, ICF

### 2. Category Normalization

Map free-text categories to the canonical vocabulary and alias table defined in `../../schema/product-schema.md`. Read that file for the full mapping of variations (English, Spanish, legacy terms) to canonical category names.

If a category is ambiguous, keep the closest match and add a `[?]` flag for the user to review.

### 3. Dimensions

**Splitting combined dimensions:**
| Input | → W | → D | → H | → Unit |
|-------|-----|-----|-----|--------|
| `32 x 24 x 30 in` | 32 | 24 | 30 | in |
| `80 × 60 × 75 cm` | 80 | 60 | 75 | cm |
| `W32 D24 H30` | 32 | 24 | 30 | (infer) |
| `32"W x 24"D x 30"H` | 32 | 24 | 30 | in |
| `Ancho: 80, Prof: 60, Alto: 75 cm` | 80 | 60 | 75 | cm |

**Dimension rules:**
- Always store as **separate W, D, H columns** with a **Unit column**
- If dimensions are already split, validate they're numeric (strip any unit text from the number)
- Interpret `"` as inches, `'` as feet (convert to inches: `2'6"` → `30`)
- Accept `×`, `x`, `X`, `by`, `por` as separators
- Convention: W × D × H (width × depth × height). If only 2 values, ask which is missing.
- Round to 2 decimal places max
- If unit is missing but values suggest inches (all < 100 for furniture), assume `in`. If values suggest cm (> 100 or explicit), use `cm`. If truly ambiguous, flag with `[?]`.

**Do NOT convert units.** Keep the original unit. Designers need the manufacturer's spec for ordering.

### 4. Language Normalization

Detect the language of each field value and normalize to **English** unless the user specifies otherwise.

| Spanish (common in UY sources) | → English |
|-------------------------------|-----------|
| Silla | Chair (category) |
| Mesa | Table (category) |
| Escritorio | Desk (category) |
| Madera | Wood (material) |
| Cuero | Leather (material) |
| Acero | Steel (material) |
| Vidrio | Glass (material) |
| Tela | Fabric (material) |
| Mármol | Marble (material) |
| Roble | Oak (material) |
| Nogal | Walnut (material) |
| Blanco | White (color) |
| Negro | Black (color) |
| Natural | Natural (keep as-is) |
| Cromado | Chrome (finish) |

**Rule:** Translate category, material, and color/finish fields. Leave Product Name and Brand as-is (proper nouns).

If the user says "keep in Spanish" or specifies a target language, respect that.

### 5. Materials & Finishes Vocabulary

Standardize common material terms:

| Variations | → Standard |
|-----------|------------|
| SS, Stainless, S/S | Stainless steel |
| Ply, Plywood, Mold ply | Molded plywood |
| MDF, Medium density | MDF |
| HPL, High pressure laminate | HPL |
| Lam, Laminate | Laminate |
| Fab, Textile | Fabric |
| COM, C.O.M. | COM (Customer's Own Material) |
| COL, C.O.L. | COL (Customer's Own Leather) |
| Powder coat, PC, Pwdr | Powder-coated |
| Chrm, Chrome plated | Chrome |
| Anodized alum, Anod. | Anodized aluminum |
| Ven, Veneer | Veneer |
| Sol. wood, Solid | Solid wood |

### 6. Price & Currency

- Strip currency symbols (`$`, `€`, `£`, `¥`) — store symbol as currency code in separate column
- Remove thousands separators (both `.` and `,` — detect locale: `1.234,56` is EU format, `1,234.56` is US)
- Store as plain decimal number: `5695.00`
- If price says "Contact", "Quote", "Trade", "A consultar", "Consultar" → set to empty
- Currency detection: `$` alone defaults to `USD` unless context suggests otherwise (UY site → `UYU`, EU site → `EUR`)
- If a schedule mixes currencies, keep each row's original currency. Add a note at the top.

### 7. Duplicate Detection

- Flag rows with identical Product Name + Brand as potential duplicates
- Flag rows with identical URL as definite duplicates
- Don't auto-delete — present duplicates to the user and ask what to keep

### 8. Whitespace & Formatting

- Trim leading/trailing whitespace from all fields
- Collapse multiple spaces to single space
- Remove line breaks within field values
- Normalize list separators: `wood / metal / glass` → `Wood, Metal, Glass` (comma-separated)
- Remove trailing commas or semicolons

## Workflow

### Step 1: Load the schedule
Read the input. Report: "Loaded N rows with M columns."
Map input columns to the canonical schema. If column mapping is ambiguous (e.g., a column called "Size" could be combined dimensions), ask the user.

### Step 2: Analyze issues
Scan all rows and produce a summary:
```
## Cleanup Preview

- **Casing**: X product names need Title Case
- **Categories**: Y rows have non-standard categories (mapping: "chairs" → Seating, etc.)
- **Dimensions**: Z rows have combined dimensions to split
- **Language**: W rows have Spanish-language fields to translate
- **Materials**: V rows have non-standard material terms
- **Prices**: U rows need currency formatting cleanup
- **Duplicates**: T potential duplicate rows found
- **Empty fields**: S rows missing dimensions, R rows missing price
```

### Step 3: Confirm scope
Ask: **"Apply all fixes, or select which ones?"**

If the user wants to be selective, let them pick from the list. Otherwise, apply all.

### Step 4: Apply fixes
Process every row through the active cleanup rules. Track every change made.

### Step 5: Present results
Show a **before/after diff** for a sample of changed rows (up to 5 examples). Then show the full cleaned table.

Report:
```
## Cleanup Complete

- Rows processed: N
- Changes made: X
- Flagged for review: Y (marked with [?])
```

### Step 6: Save
Ask: **"Save where?"**
Options:
- **Overwrite original file** (if local file input)
- **Save as new file** (default: append `-clean` to filename)
- **Write to Google Sheet** (same sheet or new one)
- **Just show the table** — leave in conversation

## Edge Cases

- **Mixed-language schedule**: Detect dominant language per column, normalize to one language
- **Merged cells or irregular formatting**: Flag and ask user how to handle
- **Extra columns not in schema**: Preserve them as-is at the end, don't delete
- **Empty rows**: Remove silently
- **Header detection**: Auto-detect header row (first row with text that matches known field names). If uncertain, ask.
