---
name: product-match
description: Find visually or functionally similar products from an image, name, or description.
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

# /product-match — Product Match

"Find me something like this." Takes a product — by name, image, or description — and searches the web for similar alternatives. Returns 5-10 matches with specs, pricing, and links.

## When to Use

- Designer has a product they like but it's over budget, discontinued, or wrong lead time
- Client references a product and you need alternatives at different price points
- Sourcing a similar product from a different manufacturer or region
- Finding contract/trade equivalents of residential products (or vice versa)

## Step 1: Accept Input

The designer provides a product reference in any format:

**By name:**
```
/product-match Eames Lounge Chair
```

**By name + constraints:**
```
/product-match Eames Lounge Chair but under $3,000
```

**By image:**
```
/product-match ~/Downloads/chair-photo.jpg
```

**By description:**
```
/product-match mid-century lounge chair, molded plywood shell, leather cushions, swivel base
```

**By URL:**
```
/product-match https://store.hermanmiller.com/living-room-furniture/eames-lounge-chair
```

## Step 2: Identify the Source Product

If given a name or URL, look up the product's key attributes:
- Category and subcategory
- Dimensions (W, D, H)
- Materials and finishes
- Price range
- Designer / design era
- Key visual characteristics (silhouette, proportions, details)

If given an image, use Claude vision to describe:
- Product type and category
- Shape, proportions, silhouette
- Materials visible (wood type, metal finish, upholstery)
- Style period and design language
- Color palette
- Estimated scale

If given a description, extract the same attributes from the text.

Document the source product clearly:

```
## Source Product
Eames Lounge Chair — Herman Miller
Category: Lounge Chair
Dims: 32.75"W × 32.5"D × 33.5"H
Materials: Molded plywood, leather
Price: $5,695
Style: Mid-Century Modern, organic, sculptural
Key features: Swivel base, tilting seat, separate ottoman
```

## Step 3: Search for Matches

Run 3-5 web searches targeting different angles:

1. **Direct alternatives**: `lounge chairs similar to Eames`
2. **Category + style**: `mid-century molded plywood lounge chair`
3. **Price-specific** (if budget mentioned): `modern lounge chair under $3,000`
4. **Material-specific**: `leather and walnut lounge chair swivel`
5. **Trade/contract sources**: `contract lounge chair molded wood specification`

For each candidate found, attempt to fetch the product page for full specs.

**Target: 5-10 matches** that genuinely resemble the source. Quality over quantity.

## Step 4: Score and Rank Matches

For each match, assess similarity on:
- **Visual similarity** (0-5): Does it look like the source?
- **Material match** (0-3): Same or similar materials?
- **Price proximity** (0-3): Within a reasonable range of source or stated budget?
- **Dimension match** (0-2): Similar scale?
- **Availability** (0-2): In stock or reasonable lead time?

Total score out of 15. Present in descending order.

## Step 5: Present Results

```
## Product Matches for: Eames Lounge Chair

### 1. Plycraft Mr. Chair — Plycraft (Score: 13/15)
32"W × 30"D × 33"H · Molded walnut plywood, leather · $2,495
Lead: In stock · Indoor
🔗 plycraft.com/mr-chair
Why: Direct mid-century competitor. Same era, same construction technique.
Nearly identical silhouette at less than half the price.

### 2. Tiempo Lounge — Lazar (Score: 11/15)
31"W × 33"D × 34"H · Walnut veneer, leather · $3,200
Lead: 6-8 weeks · Indoor
🔗 lazarind.com/tiempo
Why: Modern reinterpretation. Slightly softer lines, similar materials.
Available in COM.

### 3. ...

---

## Comparison

| # | Product | Brand | W | D | H | Price | Material | Lead | Match |
|---|---------|-------|---|---|---|-------|----------|------|-------|
| 1 | Mr. Chair | Plycraft | 32 | 30 | 33 | $2,495 | Plywood/Leather | Stock | 13/15 |
| 2 | Tiempo | Lazar | 31 | 33 | 34 | $3,200 | Walnut/Leather | 6-8w | 11/15 |
```

### Presentation rules

- Lead with the comparison table for quick scanning
- Include "Why" for each — what makes this a good match and what's different
- Flag trade-offs: "veneer not solid", "no swivel", "larger scale"
- Group if useful: "Closest matches", "Budget alternatives", "Contract options"

## Step 6: Save

If the designer picks matches ("save 1 and 3"), write to the master Google Sheet using the 33-column schema defined in `../../schema/product-schema.md` (read for column reference and formats). Use `../../schema/sheet-conventions.md` for CRUD patterns.

- Column AD (Tags): append `match:{source-product-name}` so matches are traceable
- Column AE (Notes): "Matched from {source product}. {Why reasoning}"
- Column AF (Status): "saved"
- Column AG (Source): "product-match"

## Pairs With

- `/product-research` — research finds products from a brief, match finds alternatives to a specific product
- `/product-enrich` — enrich the matched products with categories and tags
- `/product-pair` — after matching, find complementary products
- `/product-data-import` — import matched products into the master schedule
