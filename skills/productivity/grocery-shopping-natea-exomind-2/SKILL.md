---
name: grocery-shopping
description: Use when user needs to create grocery list from recipes - consolidates ingredients across recipes, checks pantry inventory, converts to purchasable quantities, and provides automation options for Costco/Instacart
---

# Grocery Shopping List Generator

## Overview

Generate smart grocery lists from recipes by consolidating ingredients, checking what's already available, converting to purchasable quantities, and optionally automating the shopping process. **Core principle:** Buy only what you need in quantities you can actually purchase.

**Announce at start:** "I'm using the grocery-shopping skill to create your shopping list from recipes."

## Quick Reference

| Task | Steps | Key Actions |
|------|-------|-------------|
| **Setup** | Ask preferences → Store inventory | Store choice, Costco/Instacart status |
| **Consolidate** | Combine recipes → Sum quantities | Merge duplicate ingredients |
| **Check Inventory** | Ask what's available → Subtract | Remove items already owned |
| **Convert to Purchasable** | Recipe amounts → Package sizes | Translate to real products |
| **Organize & Output** | Group by section → Format for use | Chrome extension ready |

## When to Use

**Use when:**
- User has recipes and needs a shopping list
- User wants to check pantry before shopping
- User needs quantities converted to real package sizes
- User wants to automate shopping (Instacart/Costco)
- Planning meals for the week

**Don't use when:**
- User just wants recipe suggestions
- User is browsing recipes (not ready to shop)
- User wants nutrition info only

## The Pattern

```
Grocery Shopping Progress:
- [ ] Phase 1: Setup (store preference, automation options)
- [ ] Phase 2: Consolidate (ingredients combined across recipes)
- [ ] Phase 3: Inventory Check (pantry/fridge items subtracted)
- [ ] Phase 4: Convert to Purchasable (real package sizes)
- [ ] Phase 5: Organize & Format (store sections, copy/paste ready)
- [ ] Phase 6: Automation (optional Costco/Instacart integration)
```

### Phase 1: Setup & Preferences

**Ask user for shopping preferences:**

**Questions to ask:**
1. **"Which grocery store do you prefer to shop at?"**
   - Common options: Safeway, Whole Foods, Trader Joe's, Kroger, Target, Walmart
   - Affects product availability and packaging sizes
   - Store with memory for future use

2. **"Do you have a Costco membership?"**
   - Costco = bulk sizes, different packaging
   - Affects quantity recommendations
   - Some items cheaper in bulk vs. regular grocery

3. **"Do you have an Instacart account you'd like to use for delivery?"**
   - If yes: Can provide direct Instacart cart link
   - If no: Provide printable/copyable list

4. **"What do you currently have in your pantry and fridge?"**
   - Ask for common staples: flour, sugar, oil, butter, eggs, milk, spices
   - Better to ask than assume
   - Save to memory for future shopping trips

**Store preferences in memory:**
```
Store preference to memory:
- grocery_store: "Safeway"
- has_costco: true
- has_instacart: true
- pantry_staples: ["flour", "sugar", "olive oil", "salt", "pepper"]
- fridge_items: ["milk", "eggs", "butter"]
- last_updated: "2025-10-19"
```

### Phase 2: Consolidate Ingredients

**Combine ingredients across all recipes:**

**Consolidation rules:**
1. **Same ingredient, same unit:** Add quantities
   - Recipe 1: 1 cup flour + Recipe 2: 2 cups flour = **3 cups flour**

2. **Same ingredient, different units:** Convert then add
   - Recipe 1: 1/2 cup butter + Recipe 2: 4 tbsp butter = **1/2 cup + 1/4 cup = 3/4 cup butter**

3. **Similar but different ingredients:** Keep separate
   - "Butter" vs. "Salted butter" = different items
   - "All-purpose flour" vs. "Bread flour" = different items

4. **Tiny amounts that round away:** Flag for user decision
   - If final amount < 1/4 tsp → Ask "You need a pinch of X - already have any?"

**Example consolidation:**
```
Recipe 1 (Cookies): 1/3 cup butter, 3/4 cup flour, 1 egg, 2/3 cup chocolate chips
Recipe 2 (Pasta): 8 oz pasta, 2 cups marinara, 2 tbsp olive oil, 1/4 cup parmesan
Recipe 3 (Garlic bread): 1/4 cup butter, 2 tbsp olive oil, 1/2 cup parmesan

Consolidated:
- Butter: 1/3 cup + 1/4 cup = 7/12 cup (≈ 9 tbsp)
- Flour: 3/4 cup
- Eggs: 1
- Chocolate chips: 2/3 cup
- Pasta: 8 oz
- Marinara sauce: 2 cups
- Olive oil: 2 tbsp + 2 tbsp = 4 tbsp (1/4 cup)
- Parmesan: 1/4 cup + 1/2 cup = 3/4 cup
```

### Phase 3: Inventory Check

**Subtract what user already has:**

**Ask systematically:**
- "I see you need butter, flour, eggs, chocolate chips, pasta, marinara, olive oil, and parmesan."
- "From your pantry list, you have: flour and olive oil"
- "From your fridge, you have: eggs"
- "Should I remove these from the shopping list, or do you need to restock any?"

**Handle partial quantities:**
- User has 1/2 cup flour, needs 3/4 cup → Still need to buy
- User has "some" olive oil → Ask: "Enough for 1/4 cup or should I add to list?"

**Create final needed list:**
```
NEED TO BUY:
- Butter: 7/12 cup (≈ 9 tbsp)
- Chocolate chips: 2/3 cup
- Pasta: 8 oz
- Marinara sauce: 2 cups
- Parmesan: 3/4 cup

ALREADY HAVE (removed from list):
- Flour: 3/4 cup ✓
- Eggs: 1 ✓
- Olive oil: 1/4 cup ✓
```

### Phase 4: Convert to Purchasable Quantities

**Translate recipe amounts to real package sizes:**

**Conversion guidelines:**

**Butter:**
- Recipe needs: 7/12 cup (9 tbsp)
- Purchase: **1 stick butter** (8 tbsp/1/2 cup)
- Note: "Recipe needs 9 tbsp, 1 stick = 8 tbsp. You'll be 1 tbsp short - buy 2 sticks or adjust recipe slightly."

**Chocolate chips:**
- Recipe needs: 2/3 cup
- Purchase: **1 bag (12 oz)** - standard package size
- Note: "Recipe needs ~4 oz, buying 12 oz bag (standard size). Leftover: ~8 oz for future."

**Pasta:**
- Recipe needs: 8 oz
- Purchase: **1 box (16 oz)** - most common package
- Note: "Leftover: 8 oz for another meal"

**Marinara sauce:**
- Recipe needs: 2 cups
- Purchase: **1 jar (24 oz)** - standard marinara jar
- Note: "2 cups ≈ 16 oz, jar is 24 oz. Leftover: ~1 cup (8 oz)."

**Parmesan:**
- Recipe needs: 3/4 cup grated
- Purchase: **8 oz bag pre-grated** OR **4 oz wedge** (grate yourself)
- Note: "3/4 cup grated ≈ 3 oz. Pre-grated bag has extra, wedge is fresher."

**Store-specific adjustments:**

**Costco bulk sizes:**
- Butter: 4-pack of sticks (1 lb)
- Chocolate chips: 4.5 lb bag
- Pasta: 6-pack of 16 oz boxes
- Marinara: 2-pack of 32 oz jars
- Note: "Only buy at Costco if you'll use extras within 3-6 months"

**Regular grocery store:**
- Standard package sizes as listed above
- Store brands often cheaper, same quality

### Phase 5: Organize & Format

**Group by store section for efficient shopping:**

**Standard store layout:**
```markdown
## Grocery Shopping List
**Store:** [User's preferred store]
**Date:** [Today's date]
**Estimated Total:** [If known from store prices]

### Dairy/Refrigerated
- [ ] Butter - 1 stick (8 tbsp) - [Recipe needs 9 tbsp, will be 1 tbsp short]
- [ ] Parmesan cheese - 8 oz bag pre-grated OR 4 oz wedge - [Need 3 oz]

### Baking/Dry Goods
- [ ] Chocolate chips - 1 bag (12 oz) - [Need 4 oz, leftover 8 oz]

### Pasta/International
- [ ] Pasta - 1 box (16 oz) - [Need 8 oz, leftover 8 oz]

### Sauces/Condiments
- [ ] Marinara sauce - 1 jar (24 oz) - [Need 16 oz, leftover 8 oz]

---
**Already have at home:** Flour, eggs, olive oil
**Estimated cost:** $15-20 (varies by store)
```

**Chrome Extension Copy/Paste Format:**

For use with Claude in browser, provide clean copy/paste version:

```
COPY THIS INTO CHROME EXTENSION CHAT:
---
I need to buy groceries. Here's my list organized by store section:

DAIRY:
• Butter - 1 stick
• Parmesan - 8 oz bag grated

BAKING:
• Chocolate chips - 12 oz bag

PASTA:
• Pasta - 1 box (16 oz)

SAUCES:
• Marinara sauce - 24 oz jar

I already have: flour, eggs, olive oil

Can you help me [add specific request - find deals, create Instacart cart, etc.]?
---
```

### Phase 6: Automation Options

**If user has Instacart:**

"I can help you create an Instacart order. Would you like me to:
1. **Provide Instacart search terms** - You manually add items
2. **Create shareable cart** - Generate list you can send to Instacart
3. **Guide you through adding items** - Step-by-step in the app"

**Instacart workflow:**
```
For Chrome extension:
1. Open Instacart.com in browser
2. Select your preferred store
3. Use Claude to search for each item:
   "Search for: butter stick"
4. Add to cart as Claude guides you
5. Review cart and checkout
```

**If user has Costco:**

"I noticed you have Costco membership. For this list:
- **Worth buying at Costco:** [None, quantities too small]
- **Regular grocery better:** All items (small quantities this time)
- **Next time:** If making 4x this recipe, Costco bulk saves money"

**Smart bulk buying logic:**
```
Suggest Costco when:
- Recipe scaled 3x or more
- Non-perishable items (pasta, canned goods)
- Items user uses frequently
- Significant cost savings (>30%)

Suggest regular grocery when:
- Small quantities
- Perishables that might spoil
- First time trying a recipe
- Limited storage space
```

## Common Mistakes

### ❌ Mistake 1: Not Asking About Inventory
**Problem:** Generate list without checking what user has
**Why bad:** User buys duplicates, wastes money
**Fix:** ALWAYS ask about pantry/fridge before finalizing list

### ❌ Mistake 2: Recipe Quantities Only
**Problem:** "Need 2/3 cup chocolate chips" without package size
**Why bad:** Can't buy 2/3 cup - need to know bag size
**Fix:** Always convert to purchasable: "Buy 12 oz bag (standard), need ~4 oz"

### ❌ Mistake 3: Ignoring Leftovers
**Problem:** Don't mention what's left after recipe
**Why bad:** User doesn't know if extras will spoil or be useful
**Fix:** Note leftovers: "Leftover 8 oz pasta - enough for another meal"

### ❌ Mistake 4: No Store Organization
**Problem:** Random order: eggs, pasta, chocolate chips, butter, sauce
**Why bad:** User runs all over store, inefficient
**Fix:** Group by sections: Dairy, Baking, Pasta, etc.

### ❌ Mistake 5: Forgetting to Ask About Automation
**Problem:** Assume user wants to shop in person
**Why bad:** Miss opportunity to use Instacart/online ordering
**Fix:** Phase 1 - ask about Instacart/online shopping preference

## Red Flags

**Rationalizations to REJECT:**
- "User probably has salt/pepper, skip asking" → NO. Always verify pantry items.
- "Just list ingredients, user can figure out package sizes" → NO. Provide purchasable quantities.
- "Store organization doesn't matter much" → YES IT DOES. Saves significant time shopping.
- "Small amounts don't need exact conversions" → FALSE. User needs to know what to buy.

**STOP if you encounter:**
- More than 10 recipes at once → Ask user to prioritize or batch into multiple trips
- Recipes with "exotic" ingredients → Warn about specialty store visits
- Perishables for far-future meals → Warn about spoilage timeline
- User wants to automate but hasn't set up account → Guide them through setup first

**Warning signs:**
- User buying for party/event (50+ servings) → Suggest Costco or restaurant supply
- All items from different store sections → Confirm store layout
- Recipe calls for "1 pinch" of expensive spice → Suggest skipping if not regular use

## Store-Specific Tips

### Trader Joe's
- Smaller packages, good for 1-2 person households
- Unique items: note if TJ's exclusive or find substitute
- No bulk sizes - adjust quantities

### Costco
- Everything in bulk - minimum 2-4x regular sizes
- Great for: non-perishables, freezer items, family size
- Skip if: cooking for 1-2, first time recipe, limited storage

### Whole Foods
- Premium pricing - note budget impact
- Great produce/organic - prioritize these items
- Amazon Prime discount - remind user if applicable

### Walmart/Target
- Widest selection, good prices
- Grocery + household in one trip
- Often have online pickup/delivery

## Integration with Other Skills

**Combine with recipe-finding:**
```
User: "Find me 3 dinner recipes for this week"
→ Use recipe-finding skill
→ Automatically transition to grocery-shopping
→ "I found 3 recipes. Would you like me to create a shopping list?"
```

**Combine with meal-planning:**
```
User: "Plan meals for the week"
→ Use meal-planning skill
→ Transition to grocery-shopping
→ "Here's your weekly meal plan. Generating shopping list..."
```

## Examples

### Example 1: Simple Dinner for Two

**User:** "I'm making pasta and cookies, need a grocery list"

**Assistant:** "I'm using the grocery-shopping skill to create your shopping list.

First, quick setup questions:
1. Which grocery store do you prefer?
2. Do you have Costco membership?
3. Do you have Instacart for delivery?
4. What staples do you have? (flour, sugar, butter, eggs, oil, etc.)"

**User:** "Safeway, no Costco, yes Instacart. I have flour, oil, and eggs."

**Assistant:**
```
## Shopping List - Safeway via Instacart
**Date:** Oct 19, 2025

### Dairy
- [ ] Butter - 1 stick (need 9 tbsp)
- [ ] Parmesan cheese - 8 oz bag grated (need 3 oz)

### Baking
- [ ] Chocolate chips - 12 oz bag (need 4 oz, leftover 8 oz)

### Pasta
- [ ] Pasta - 1 box 16 oz (need 8 oz, leftover 8 oz)

### Sauces
- [ ] Marinara - 24 oz jar (need 16 oz, leftover 8 oz)

**Already have:** Flour, olive oil, eggs ✓
**Estimated total:** $12-15

Would you like me to guide you through adding these to your Instacart cart?
```

### Example 2: Weekly Meal Prep with Costco

**User:** "Planning 5 dinners for the week, have Costco membership"

**Assistant:** [After recipe consolidation]
```
## Shopping List - Costco vs. Regular Grocery

**COSTCO (bulk items, better value):**
- [ ] Chicken breast - 6 lb pack (need 4 lbs, freeze extras)
- [ ] Rice - 25 lb bag (need 3 cups, pantry stable)
- [ ] Canned tomatoes - 8-pack (need 4 cans, pantry stable)

**REGULAR GROCERY (fresh, small quantities):**
- [ ] Fresh basil - 1 bunch
- [ ] Bell peppers - 3 pieces
- [ ] Onions - 2 medium
- [ ] Garlic - 1 bulb
- [ ] Fresh mozzarella - 8 oz

**Strategy:** Hit Costco for proteins and pantry staples, then regular grocery for fresh produce.
**Estimated savings:** $15-20 buying chicken/rice/tomatoes in bulk
```

### Example 3: Chrome Extension Format

**User:** "Give me copy/paste format for Claude browser extension"

**Assistant:**
```
📋 COPY BELOW FOR CHROME EXTENSION:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

I need help shopping for these items at Safeway:

DAIRY SECTION:
• Butter (1 stick)
• Parmesan cheese (8 oz bag, pre-grated)

BAKING AISLE:
• Chocolate chips (12 oz bag)

PASTA AISLE:
• Pasta (16 oz box)
• Marinara sauce (24 oz jar)

I already have: flour, eggs, olive oil

Can you help me find the best deals on these items?

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Success Metrics

**You've succeeded when:**
- ✅ Asked about store preference and automation options
- ✅ Consolidated ingredients across all recipes correctly
- ✅ Checked and subtracted pantry/fridge inventory
- ✅ Converted recipe quantities to real package sizes
- ✅ Organized by store sections for efficient shopping
- ✅ Noted leftovers and whether they're useful
- ✅ Provided Chrome extension copy/paste format if requested
- ✅ Suggested automation (Instacart/Costco) when applicable
- ✅ User can take list and shop immediately without confusion
