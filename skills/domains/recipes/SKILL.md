---
name: recipes
description: Generate meal plans and recipes from optimization results. Use when user wants recipes, meal ideas, cooking instructions, or a weekly meal plan from their optimized food list. Triggers on "create recipes", "meal plan recipes", "how to cook", "weekly menu", "what to make", "cooking ideas".
---

# Recipe Generation from Optimized Foods

This skill takes optimization results and creates practical meal plans with recipes. It can either generate a prompt for external use or create recipes directly.

## Best Source: Template-Based Optimization

**Template-based results are ideal for recipes** because they're already structured as proper meals:

```bash
# Run template-based optimization first
uv run llmn optimize --pattern pescatarian --pattern slow_carb --template --json
```

This gives you:
- Breakfast: Eggs 150g, Edamame 100g, Kale 100g
- Lunch: Cod 235g, Kidney beans 216g, Zucchini 161g
- Dinner: Salmon 170g, Lentils 113g, Carrots 149g
- Snack: Peanuts 30g

**No meal allocation needed** - foods are already assigned to meals with proper structure.

## Workflow

### Step 1: Get the Optimization Results

Check if there's a recent optimization run:

```bash
# List recent optimization runs
uv run llmn explore runs --limit 5 --json
```

If no recent runs, suggest running `/llmn` or `/multiperiod` first.

To use a specific run:
```bash
# Get details of a specific run
uv run llmn explore runs --json
# Look at run_id in the output
```

### Step 2: Export the Food List

Export the optimization results in a format suitable for recipe generation:

```bash
# Export latest run for LLM recipe generation
uv run llmn export-for-llm latest

# Or export with specific number of days
uv run llmn export-for-llm latest --days 7

# Export to a file
uv run llmn export-for-llm latest --days 7 --output /tmp/meal_prompt.md
```

### Step 3: Gather User Preferences

Ask the user about their cooking preferences:

1. **Cuisine styles** (select multiple):
   - Mediterranean
   - Asian
   - Mexican/Latin
   - American
   - Indian
   - Italian
   - Middle Eastern

2. **Cooking skill level**:
   - Beginner (simple recipes, <20 min)
   - Intermediate (moderate complexity, <30 min)
   - Advanced (willing to try complex techniques)

3. **Max prep time per meal**:
   - Quick (<15 min)
   - Moderate (<30 min)
   - Extended (30-60 min)

4. **Available equipment**:
   - Stovetop
   - Oven
   - Instant Pot / Pressure Cooker
   - Air Fryer
   - Slow Cooker
   - Blender
   - Grill

5. **Meal prep preference**:
   - Cook fresh daily
   - Batch cook on weekends
   - Mix of both

### Step 4: Generate Recipes

Option A: **Generate a prompt** (user will paste elsewhere)
```bash
uv run llmn export-for-llm latest --days 7
```

Then combine with user preferences to create a detailed prompt.

Option B: **Generate recipes directly** (Claude creates recipes now)

Use the optimization output to create recipes that:
- Use EXACTLY the specified food amounts
- Distribute foods across meals appropriately
- Match user's cuisine preferences
- Fit within time/skill constraints
- Consider meal prep strategies

### Step 5: Present the Meal Plan

Structure the output as:

```
## Day 1

### Breakfast
**Scrambled Eggs with Spinach** (10 min)
- 150g eggs (3 large)
- 50g spinach
- 15g olive oil

Instructions:
1. Heat olive oil in a pan
2. Add spinach, cook until wilted
3. Add beaten eggs, scramble until set

Macros: 350 kcal, 25g protein, 2g carbs, 26g fat

---

### Lunch
**Salmon with Lentils** (25 min)
...

### Dinner
**Tuna and Black Bean Bowl** (20 min)
...

### Snack
**Almonds** (0 min)
- 25g raw almonds

Macros: 145 kcal, 5g protein, 5g carbs, 12g fat

---

## Daily Totals
- Calories: 1850 kcal
- Protein: 155g
- Carbs: 120g
- Fat: 78g
```

## Recipe Generation Guidelines

### Respect Food Amounts

The optimization calculated exact amounts. Recipes should use these amounts:
- If optimization says 150g salmon, recipe uses 150g salmon
- Scale across multiple days if doing weekly meal prep
- For 7-day plan: daily amount × 7 = weekly shopping amount

### Food Preparation Context

The export includes preparation state hints:
- `Salmon (raw)` → needs cooking
- `Lentils (cooked)` → already cooked, can use canned
- `Eggs (whole, raw)` → needs cooking
- `Spinach (raw)` → can be eaten raw or cooked

### Meal Allocation Logic

**Skip this if using template-based optimization** - meals are already structured.

If using single-period optimization (not template or multi-period), allocate foods to meals sensibly:

**Breakfast foods**:
- Eggs
- Oatmeal
- Yogurt
- Fruit

**Lunch/Dinner foods**:
- Fish (salmon, tuna, cod)
- Legumes (lentils, beans, chickpeas)
- Vegetables (broccoli, spinach, cauliflower)
- Grains (rice, quinoa)

**Snack foods**:
- Nuts (almonds, walnuts)
- Small portions of fruit
- Vegetables with hummus

### Recipe Complexity by Skill Level

**Beginner**:
- One-pan meals
- No-cook options (salads, bowls)
- Simple techniques: scramble, boil, roast
- Example: "Scrambled eggs", "Baked salmon with roasted vegetables"

**Intermediate**:
- Multi-component meals
- Sauces and marinades
- Example: "Pan-seared salmon with lemon-herb sauce and garlic lentils"

**Advanced**:
- Complex techniques
- Multiple cooking methods
- Example: "Sous vide salmon with crispy skin, served with French lentils du Puy"

### Meal Prep Strategies

For batch cooking:
- **Proteins**: Cook all proteins Sunday, refrigerate
- **Grains/Legumes**: Make large batch, portion into containers
- **Vegetables**: Prep (wash, chop) Sunday, cook fresh or roast in bulk
- **Sauces**: Make dressings/sauces to add variety to same base foods

Example meal prep plan:
```
SUNDAY PREP (2 hours):
- Bake 1kg salmon (5 portions)
- Cook 500g lentils (5 portions)
- Roast 1kg mixed vegetables
- Hard-boil 12 eggs
- Wash and portion spinach

WEEKDAY ASSEMBLY (5-10 min):
- Combine pre-cooked components
- Add fresh elements (avocado, olive oil)
- Microwave to reheat if needed
```

## Commands Reference

```bash
# List recent optimization runs
uv run llmn explore runs --limit 10 --json

# Export latest run for recipes
uv run llmn export-for-llm latest

# Export specific run
uv run llmn export-for-llm <run_id>

# Export with day count
uv run llmn export-for-llm latest --days 7

# Export to file
uv run llmn export-for-llm latest --output /tmp/recipes.md

# Get optimization details (for macro breakdown)
uv run llmn explore runs --json
```

## Example Output

### Prompt Generation Mode

```markdown
# Meal Planning Request

## Optimized Daily Food Allocation

| Food | Amount | Protein | Calories |
|------|--------|---------|----------|
| Salmon, Atlantic, raw | 150g | 31g | 310 |
| Eggs, whole, raw | 150g | 19g | 215 |
| Lentils, cooked | 200g | 18g | 232 |
| Spinach, raw | 100g | 3g | 23 |
| Broccoli, raw | 150g | 4g | 51 |
| Olive oil | 30g | 0g | 265 |
| Almonds | 25g | 5g | 145 |

**Daily Totals**: 1850 kcal, 155g protein

## Preferences
- Cuisine: Mediterranean, Asian
- Skill level: Intermediate
- Max prep time: 30 minutes
- Equipment: Stovetop, oven, air fryer
- Meal prep: Batch cook on weekends

## Request
Create a 7-day meal plan using exactly these daily food amounts.
Distribute across breakfast, lunch, dinner, and one snack.
Include simple recipes that reheat well.
```

### Direct Recipe Mode

Generate recipes directly based on the food list and preferences, structured as shown in Step 5.
