---
name: product-pair
description: Suggest complementary products that pair well with a given item — side tables for sofas, task lights for desks, etc.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - WebFetch
  - WebSearch
  - AskUserQuestion
  - mcp__google-sheets__get_sheet_data
  - mcp__google-sheets__update_cells
  - mcp__google-sheets__list_sheets
user-invocable: true
---

# /product-pair — Product Pairing

"What goes with this?" Takes a product and suggests complementary items across different categories — a side table for a sofa, a floor lamp for a reading chair, a rug for a dining table. Returns 5-8 pairings with reasoning rooted in design principles.

## When to Use

- Building out a room or vignette from a hero piece
- Designer has a key product and needs to complete the palette
- Presenting a coordinated product package to a client
- Filling gaps in an FF&E schedule by category

## Step 1: Accept Input

**By name:**
```
/product-pair Blu Dot Diplomat Sofa
```

**By name + context:**
```
/product-pair Blu Dot Diplomat Sofa for a tech office lounge
```

**By product details:**
```
/product-pair
Name: Diplomat Sofa
Brand: Blu Dot
Materials: Steel frame, fabric upholstery
Color: Edwards Navy
Style: Contemporary, minimal
Price: $2,499
Context: Corporate lounge, 6-person seating area
```

## Step 2: Analyze the Source Product

Identify the product's design DNA:
- **Style language**: Mid-century, Scandinavian, industrial, contemporary, etc.
- **Material palette**: Wood type, metal finish, upholstery type
- **Color family**: Warm neutrals, cool tones, bold accent, monochrome
- **Scale**: Compact/apartment, standard, generous/commercial
- **Price tier**: Budget (<$500), mid-range ($500-$2,000), premium ($2,000-$5,000), luxury ($5,000+)
- **Market**: Residential, contract, hospitality

## Step 3: Determine Pairing Categories

Based on the source product's category, identify what typically pairs with it:

| Source Category | Pair With |
|----------------|-----------|
| Sofa | Coffee table, side table, floor lamp, throw pillow, rug, ottoman |
| Lounge Chair | Side table, floor lamp, ottoman, throw |
| Dining Table | Dining chairs, pendant light, sideboard, rug |
| Desk | Task chair, desk lamp, monitor arm, desk organizer |
| Bed | Nightstands, table lamps, bench, rug, dresser |
| Conference Table | Conference chairs, credenza, pendant/linear light |
| Task Chair | Desk, monitor arm, task light |

If the designer provided context (e.g., "tech office lounge"), factor that into category selection.

## Step 4: Search for Pairings

For each pairing category, search for products that match the source's:
- **Style**: Same design language or intentional contrast
- **Material harmony**: Complementary materials (e.g., walnut sofa → brass lamp, not chrome)
- **Color coordination**: Same palette, complementary, or intentional accent
- **Scale proportion**: Appropriately sized relative to the source
- **Price alignment**: Similar tier (don't pair a $5,000 sofa with a $30 lamp)

Run 2-3 searches per pairing category. Target 5-8 total pairings across different categories.

## Step 5: Present Pairings

```
## Pairings for: Diplomat Sofa — Blu Dot

Source: Contemporary minimal, steel/navy fabric, $2,499

### Coffee Table
**Minimalista Coffee Table — Blu Dot** · $799
48"W × 24"D × 16"H · Steel, glass
Same brand, same design language. Steel frame echoes the sofa's base.

### Side Table
**Swole Small Side Table — Blu Dot** · $349
15" dia × 18"H · Steel, solid walnut top
Adds warmth with walnut. Low profile sits well next to the sofa arm height.

### Floor Lamp
**IC F1 — Flos** · $695
14" dia × 53"H · Brass, opal glass
Sculptural counterpoint to the sofa's linearity. Brass warms the cool navy.

### Throw Pillow
**Dot Dash Pillow — Loom Decor** · $89
20" × 20" · Linen blend
Texture contrast against the sofa fabric. Available in coordinating colorways.

### Rug
**Sathi Rug — Armadillo** · $1,450
8' × 10' · Wool, undyed
Neutral base grounds the navy. Contract-grade durability.

---

## Pairing Summary

| Category | Product | Brand | Price | Why |
|----------|---------|-------|-------|-----|
| Coffee Table | Minimalista | Blu Dot | $799 | Same language, steel continuity |
| Side Table | Swole Small | Blu Dot | $349 | Walnut warmth, right height |
| Floor Lamp | IC F1 | Flos | $695 | Brass accent, sculptural form |
| Pillow | Dot Dash | Loom Decor | $89 | Texture contrast |
| Rug | Sathi | Armadillo | $1,450 | Neutral ground, contract-grade |

**Total pairing package: $3,382**
```

### Presentation rules

- **Explain the design reasoning** for each pairing — material harmony, color logic, scale, style
- **Mix brands** — don't just suggest the same brand for everything (unless the designer asks)
- **Include at least one accent** — a piece that creates intentional contrast (different material, color pop, different era)
- **Stay in the price tier** — pairings should feel proportionate to the source
- **Note contract availability** if the source is contract-grade

## Step 6: Save

If the designer picks pairings, write to the master Google Sheet using the 33-column schema defined in `../../schema/product-schema.md` (read for column reference and formats). Use `../../schema/sheet-conventions.md` for CRUD patterns.

- Column AD (Tags): append `pair:{source-product-name}` for traceability
- Column AE (Notes): "Paired with {source product}. {Design reasoning}"
- Column AF (Status): "saved"
- Column AG (Source): "product-pair"

## Pairs With

- `/product-match` — match finds alternatives to the source, pair finds complements
- `/product-research` — research finds products from a brief, pair builds around an anchor piece
- `/product-enrich` — enrich paired products with full metadata
- `/product-data-import` — import the source + pairings into the master schedule
