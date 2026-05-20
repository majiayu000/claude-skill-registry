---
name: sorting-groceries
description: Sort grocery lists by aisle order using store aisle sign photos. Build aisle maps from uploaded images, match items to aisles, and output optimized shopping routes. Use when users upload aisle sign photos, request grocery list sorting, want shopping trip optimization, need store layout mapping, or mention grocery list organization.
metadata:
  version: 0.1.0
---

# Sorting Groceries by Aisle

Sort a user's grocery list by aisle order so they can walk the store in one efficient pass, no backtracking.

## When Triggered

Activate when user:
- Uploads photos of grocery store aisle signs or markers
- Provides a grocery/shopping list alongside store layout info
- Asks to sort, organize, or optimize a shopping list by aisle
- Mentions aisle numbers, store maps, or shopping routes

## Inputs

Two inputs are needed. Prompt for whichever is missing:

1. **Aisle sign images** — Photos of aisle markers, hanging signs, or endcap labels. Each typically shows an aisle number and category keywords (e.g., "Aisle 5: Coffee, Tea, Cocoa").
2. **Grocery list** — Text, pasted note, or photo of a handwritten list. Any format.

## Core Workflow

### Step 1: Build the Aisle Map

Read each uploaded aisle sign image. Extract:
- **Aisle number** (or label like "A5", "Aisle 12")
- **Category descriptions** exactly as printed (e.g., "Pasta, Sauces, Canned Vegetables")

Compile into a structured map:

```
Aisle 1: Bread, Bakery Items, Tortillas
Aisle 2: Cereal, Breakfast, Granola Bars
Aisle 3: Pasta, Sauces, Canned Goods
...
```

If an image is blurry or partially unreadable, note what was legible and flag uncertainty.

### Step 2: Identify Perimeter Zones

Grocery stores have perimeter sections without numbered aisles. Infer these from context or common knowledge when not covered by the uploaded signs:

| Zone | Typical items |
|------|---------------|
| **Produce** | Fresh fruits, vegetables, herbs, salad mixes |
| **Deli** | Sliced meats, prepared foods, rotisserie chicken |
| **Bakery** | Fresh bread, cakes, pastries (distinct from packaged bread aisle) |
| **Dairy** | Milk, cheese, yogurt, butter, eggs |
| **Meat & Seafood** | Fresh/frozen meat, poultry, fish |
| **Frozen** | Frozen meals, ice cream, frozen vegetables |

Position perimeter zones in typical store flow: **Produce → Deli/Bakery → Meat/Seafood → Dairy → Frozen** (usually along the store's outer walls, counterclockwise from entrance).

If the user's aisle photos already include these sections, use the actual signage instead of defaults.

### Step 3: Parse the Grocery List

Extract every item from the user's list. Normalize:
- "2 lbs chicken breast" → item: **chicken breast**, quantity: 2 lbs
- "eggs" → item: **eggs**, quantity: (unspecified)
- "parm" → item: **parmesan cheese**

Preserve the user's original wording alongside any normalized form.

### Step 4: Match Items to Aisles

For each grocery item, find the best aisle match:

1. **Direct keyword match** — Item name appears in or closely matches an aisle's category text (e.g., "pasta" → "Aisle 3: Pasta, Sauces")
2. **Category inference** — Item belongs to a category listed on a sign (e.g., "marinara" → "Aisle 3: Sauces")
3. **Perimeter zone match** — Item is a fresh/perishable product that lives on the store perimeter (e.g., "bananas" → Produce)
4. **Best guess with note** — Item could plausibly be in multiple aisles. Assign the most likely one and add a note (e.g., "honey — Aisle 4: Baking, but may also be in Aisle 7: Condiments")

### Step 5: Output the Sorted List

Present the final list grouped by aisle in store-walk order:

```
🛒 Sorted Shopping List — [Store Name if known]

PRODUCE
  □ bananas
  □ baby spinach
  □ 3 avocados

AISLE 1 — Bread, Bakery Items, Tortillas
  □ whole wheat bread
  □ flour tortillas

AISLE 2 — Cereal, Breakfast, Granola Bars
  □ oatmeal
  □ granola bars

AISLE 3 — Pasta, Sauces, Canned Goods
  □ spaghetti
  □ marinara sauce
  □ canned black beans

...

DAIRY
  □ 2% milk
  □ shredded mozzarella
  □ eggs (1 dozen)

⚠️ COULDN'T PLACE
  □ birthday candles — not enough aisle info to determine location
```

## Output Formatting Rules

- Use checkbox format (`□`) so the list is easy to use on a phone
- Include the aisle's category description next to the aisle number for quick reference
- Keep the user's quantities and notes attached to each item
- Perimeter zones go in logical store-walk order (Produce first, Frozen/Dairy last)
- Numbered aisles go in ascending order between the perimeter zones
- Unmatched items go at the end under a clear "couldn't place" heading

## Multi-Aisle Items

Some items legitimately live in multiple locations. When this occurs:
- Place the item in the **most common** aisle for that store's layout
- Add a parenthetical note: "(also check Aisle 7)"
- Common examples: honey (baking vs condiments), tortilla chips (snacks vs Hispanic foods), butter (dairy vs baking)

## Handling Ambiguity

- **Blurry/unreadable signs**: Note which aisles had unclear text. Ask user to confirm if critical items might be affected.
- **Store-brand categories**: Some stores use unusual groupings ("International Foods" might contain pasta in one store). Trust the sign text over assumptions.
- **Missing aisles**: If user uploaded signs for aisles 1-5 and 8-12 but not 6-7, note the gap. Items that don't match any uploaded aisle go to "couldn't place" rather than being guessed into missing aisles.

## Store Layout Reuse

If the user mentions they shop at this store regularly:
- Present the aisle map as a clean reference they can save
- Suggest they can reuse it in future conversations by pasting just the map text instead of re-uploading photos
- Format the reusable map clearly:

```
📍 [Store Name] Aisle Map
Aisle 1: Bread, Bakery Items, Tortillas
Aisle 2: Cereal, Breakfast, Granola Bars
...
Produce | Deli/Bakery | Meat & Seafood | Dairy | Frozen
```
