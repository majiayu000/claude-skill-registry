---
name: recipe-finding
description: Use when user wants to find recipes or resize recipe portions - provides systematic workflow for searching recipes, scaling ingredients by serving size, handling fractional amounts, and formatting output
---

# Recipe Finding & Scaling

## Overview

Find recipes via web search and resize them based on number of servings. **Core principle:** Systematic scaling with proper fractional handling ensures accurate, usable recipes.

**Announce at start:** "I'm using the recipe-finding skill to search for recipes and resize portions."

## Quick Reference

| Task | Steps | Key Tools |
|------|-------|-----------|
| **Find Recipe** | Search → Extract → Verify yield | WebSearch, WebFetch |
| **Scale Recipe** | Calculate factor → Scale ingredients → Round appropriately | Math |
| **Present** | Original → Scaled → Instructions | Formatted output |

## When to Use

**Use when:**
- User requests a recipe by name or type
- User wants to resize portions (e.g., "recipe for 4 people")
- User needs ingredient scaling help
- User wants dietary modifications with scaling

**Don't use when:**
- User wants cooking techniques only
- User wants general nutrition advice
- Creating original recipes (not finding existing ones)

## The Pattern

```
Recipe Finding Progress:
- [ ] Phase 1: Search & Extract (recipe found with yield)
- [ ] Phase 2: Calculate Scaling (factor determined)
- [ ] Phase 3: Scale Ingredients (all items properly converted)
- [ ] Phase 4: Format Output (clear, usable recipe)
```

### Phase 1: Search & Extract Recipe

**Find recipe with clear yield information:**

1. Use WebSearch to find recipes
2. Prioritize sources: AllRecipes, FoodNetwork, NYT Cooking, Serious Eats
3. Extract complete recipe including:
   - Original yield (servings or pieces)
   - All ingredients with measurements
   - Instructions
   - Prep/cook times

**Example search patterns:**
```
"chocolate chip cookies recipe 24 cookies"
"chicken tikka masala recipe 4 servings"
"pizza dough recipe site:seriouseats.com"
```

**Verify you have:**
- ✅ Clear original yield (e.g., "Makes 24 cookies", "Serves 4")
- ✅ Complete ingredient list with measurements
- ✅ Instructions

### Phase 2: Calculate Scaling Factor

**Formula: Scaling Factor = Desired Servings ÷ Original Servings**

**Common scaling factors:**
| From → To | Factor | Strategy |
|-----------|--------|----------|
| 24 → 8 | ÷ 3 (0.333) | Use fractions: 1/3 |
| 4 → 2 | ÷ 2 (0.5) | Halve everything |
| 4 → 6 | × 1.5 | Use 3/2 ratio |
| 6 → 8 | × 1.33 | Multiply by 4/3 |

**Pro tip:** Express as simple fraction first (e.g., 1/3, 1/2, 3/2) for cleaner calculations.

### Phase 3: Scale Ingredients

**Apply scaling factor to each ingredient:**

**Rounding guidelines:**
- **Keep exact for:** Flour, sugar, liquids (critical ratios)
- **Round to nearest practical:** Spices, leavening (1/4 tsp is smallest practical)
- **Smart rounding:** 2/3 egg → use 1 small egg or 3 tbsp beaten egg

**Unit conversion helpers:**
```
3 tsp = 1 tbsp
16 tbsp = 1 cup
2 cups = 1 pint
4 cups = 1 quart
```

**Fractional ingredient handling:**

**Eggs (FOLLOW EXACTLY - no rationalizing):**
- Whole number: Use that many eggs
- 1.5 eggs: 1 egg + 1 tbsp beaten egg
- 2/3 egg: **1 small egg OR 3 tbsp beaten egg** (1 egg ≈ 50ml)
  - ❌ DON'T use 1 large egg "because it's close enough"
  - ❌ DON'T rationalize "a little extra won't hurt"
  - ✅ USE small egg OR measure 3 tbsp beaten egg
- 1/3 egg: 2 tbsp beaten egg (measure from beaten egg)
- 0.25 egg or less: Add to next batch or adjust

**Why precision matters:** Eggs affect texture, moisture, and structure. Using a large egg when recipe needs 2/3 egg adds 50% more liquid/protein - enough to make cookies spread too much or cakes dense.

**Small amounts (< 1/4 tsp):**
- Baking powder/soda: Round to 1/4 tsp minimum (chemical reaction needs threshold)
- Salt/spices: Use "pinch" or "dash" descriptor
- Vanilla/extracts: Round to 1/4 tsp

**Large amounts:**
- Keep fractions for accuracy: 2 1/3 cups flour
- Include weight if possible: 2 1/3 cups (290g) flour
- Never round flour/sugar by more than 1 tbsp

### Phase 4: Format Output

**MANDATORY: Use this EXACT structure (not optional):**

```markdown
## [Recipe Name] (Scaled for [N] servings)

**Original Yield:** [original]
**Scaled Yield:** [new amount]
**Scaling Factor:** [factor] (e.g., 1/3 or ×1.5)

### Ingredients:
- [Amount] [unit] [ingredient] ([weight in grams if helpful])
- [Amount] [unit] [ingredient]
[Continue for all ingredients]

### Instructions:
1. [Step 1]
2. [Step 2]
[Continue all steps - adjust timing if needed]

### Notes:
- **Timing adjustments:** [if batch size affects cook time]
- **Fractional ingredients:** [explain egg/liquid conversions if used]
- **Pan size:** [adjust if scaling changes pan requirements]
```

**Example:**
```markdown
## Chocolate Chip Cookies (Scaled for 8 cookies)

**Original Yield:** 24 cookies
**Scaled Yield:** 8 cookies
**Scaling Factor:** 1/3

### Ingredients:
- 1/3 cup (75g) unsalted butter, softened
- 1/4 cup (50g) granulated sugar
- 1/4 cup (55g) packed brown sugar
- 1 small egg (or 3 tbsp beaten egg)
- 2/3 tsp vanilla extract
- 3/4 cup (93g) all-purpose flour
- 1/3 tsp baking soda
- 1/3 tsp salt
- 2/3 cup (113g) chocolate chips

### Instructions:
1. Preheat oven to 375°F (190°C)
2. Cream butter and sugars until fluffy
3. Beat in egg and vanilla
4. Mix flour, baking soda, salt separately
5. Combine wet and dry ingredients
6. Fold in chocolate chips
7. Drop tablespoon-sized portions on baking sheet
8. Bake 9-11 minutes until golden

### Notes:
- **Timing:** Same as original (small batch doesn't affect individual cookie bake time)
- **Fractional egg:** Use 1 small egg or measure 3 tbsp beaten egg
- **Pan size:** Use same size sheet, just fewer cookies
```

## Common Mistakes

### ❌ Mistake 1: Rounding Too Aggressively
**Problem:** "1 cup becomes 1/3 cup, I'll just call it 1/4 cup"
**Why bad:** Flour ratios are critical - 25% error ruins texture
**Fix:** Keep exact fractions, note weight in grams for precision

### ❌ Mistake 2: Ignoring Fractional Eggs
**Problem:** "Recipe needs 0.7 eggs... I'll just use 1"
**Why bad:** Too much egg changes texture, moisture
**Fix:** Use conversion chart (1 egg = 50ml, so 0.7 egg = 35ml or 2.5 tbsp)

### ❌ Mistake 3: Not Adjusting Pan Size
**Problem:** Scaling 9×13" casserole to 1/4 size but using same pan
**Why bad:** Affects cooking time and texture
**Fix:** Note new pan size: 1/4 of 9×13" → use 8×8" pan, reduce time ~10-15%

### ❌ Mistake 4: Scaling Baking Soda/Powder Below Threshold
**Problem:** Recipe needs 1 tsp, scaled to 1/3 tsp for smaller batch
**Why bad:** Chemical reactions need minimum amounts to work
**Fix:** Use 1/2 tsp minimum for baking powder/soda (adjust only for very large scales)

### ❌ Mistake 5: Copying Recipe Without Verifying Yield
**Problem:** Recipe says "serves 4-6" and you scale for exact numbers
**Why bad:** Ambiguous yields lead to wrong scaling
**Fix:** Ask user to clarify or use midpoint (e.g., 5 servings) with note

## Scaling Factor Quick Math

**Halving (× 0.5):**
- 1 cup → 1/2 cup
- 3/4 cup → 3/8 cup (or 6 tbsp)
- 2 eggs → 1 egg
- Easy mental math

**Thirding (× 0.33 or ÷ 3):**
- 1 cup → 1/3 cup
- 3/4 cup → 1/4 cup
- 2 tsp → 2/3 tsp
- Use fractions for accuracy

**Doubling (× 2):**
- Straightforward multiplication
- Watch oven capacity for baked goods
- May need to adjust cook time slightly

**1.5× Scaling:**
- Think of as "half again as much"
- 1 cup → 1.5 cups (1 cup + 1/2 cup)
- 2 eggs → 3 eggs
- Common for 4 → 6 servings

## Red Flags

**Rationalizations to REJECT:**
- "Using 1 whole egg instead of 2/3 egg won't make much difference" → FALSE. Follow egg chart exactly.
- "I'll create a cleaner format than the template" → NO. Use the exact template structure.
- "Rounding 1/3 cup to 1/4 cup is close enough" → NO. Keep exact fractions for flour/sugar/liquids.
- "User can adjust seasoning anyway" → Still provide scaled amounts as baseline.

**STOP if you encounter:**
- "Adjust seasoning to taste" as only instruction → Can't scale without base amounts
- Recipe with no yield information → Can't determine scaling factor
- Recipe that says "feeds a crowd" → Too vague, ask user for specifics
- Yeast bread recipes scaling beyond 2× → Rising times change, warn user

**Warning signs:**
- User wants to scale recipe 10× or more → Check if batch cooking is better approach
- Recipe involves specific pan sizes → Must recalculate pan size or warn
- Deep frying recipes → Oil temperature/volume critical, warn about adjustments

## Integration Tips

**Use WebSearch for:**
- Finding recipes from reliable sources
- Comparing recipes to pick the best one
- Finding recipe-specific tips (e.g., "chocolate chip cookie troubleshooting")

**Use WebFetch for:**
- Extracting full recipe from URL
- Getting ingredient lists from structured recipe sites

**Provide weights when:**
- Scaling involves awkward fractions (2 1/3 cups → include grams)
- User is outside US (metric more common)
- Precision matters (bread baking, pastry)

## Examples

### Example 1: Halving a Dinner Recipe

**User request:** "Find a chicken tikka masala recipe for 2 people"

**Process:**
1. Search: "chicken tikka masala recipe 4 servings"
2. Extract recipe with original yield: Serves 4
3. Calculate factor: 2 ÷ 4 = 0.5 (halve everything)
4. Scale all ingredients by 0.5
5. Present formatted recipe with note about leftover sauce

### Example 2: Scaling Up Cookies

**User request:** "I need 50 chocolate chip cookies for a party"

**Process:**
1. Find recipe making 24 cookies
2. Calculate factor: 50 ÷ 24 = 2.08 (recommend rounding to 2× for easier math)
3. Note to user: "Making 48 cookies (2× the recipe) - close enough?"
4. Scale by 2× (simpler than 2.08×)
5. Include baking time note: "Bake in batches, time per cookie stays same"

### Example 3: Complex Fractional Scaling

**User request:** "Adapt this 6-serving lasagna for 4 people"

**Process:**
1. Extract lasagna recipe (serves 6)
2. Calculate: 4 ÷ 6 = 0.67 (or 2/3)
3. Scale ingredients:
   - 1.5 lbs ground beef → 1 lb
   - 24 oz ricotta → 16 oz (2 cups)
   - 3 eggs → 2 eggs
   - 9×13" pan → 8×8" pan
4. Note cooking time: Reduce by ~10 minutes for smaller pan
5. Format with pan size and timing adjustments

---

## Success Metrics

**You've succeeded when:**
- ✅ Recipe found from reliable source
- ✅ All ingredients scaled with appropriate rounding
- ✅ Fractional amounts converted to practical measurements
- ✅ Pan sizes/timing noted if affected by scaling
- ✅ Output is immediately usable (user can cook from it)
- ✅ User confirms the serving size matches their needs
