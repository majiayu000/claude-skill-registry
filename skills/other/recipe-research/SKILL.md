---
name: recipe-research
description: Multi-source recipe research with metric conversion and verification
argument-hint: [dish-name] [--servings N] [--dietary vegan|gf|df|keto] [--classic]
allowed-tools: WebSearch, Task, Read, Write, Glob
user-invocable: true
---

# Recipe Research Skill

Research recipes from multiple sources, convert to metric, verify cooking science, calculate nutrition.

**Default: Vegetarian** — All recipes vegetarian unless `--classic` flag used.

## Workflow

### Phase 1: Parse Arguments

Extract from `$ARGUMENTS`:
- **Dish name:** Required (e.g., "beef bourguignon", "chocolate chip cookies")
- **--servings N:** Optional, default 4
- **--dietary:** Optional additions (vegan, gf, df, keto) — stacks with vegetarian default
- **--classic:** Skip vegetarian default, research traditional version

Examples:
- `beef bourguignon` → searches "vegetarian beef bourguignon mushroom"
- `pad thai --dietary gf` → "vegetarian gluten-free pad thai"
- `coq au vin --classic` → "coq au vin chicken" (traditional)

### Phase 2: Multi-Source Search

Perform 4-6 WebSearch queries targeting different angles:

```
Query patterns (auto-add "vegetarian" unless --classic):
1. "[dish] recipe" — general results
2. "[dish] recipe site:seriouseats.com OR site:bonappetit.com" — technique-focused
3. "[dish] recipe site:allrecipes.com OR site:food.com" — home cook versions
4. "[dish] recipe site:bbcgoodfood.com OR site:epicurious.com" — international perspective
5. "[dish] przepis site:jadlonomia.com OR site:rozkoszny.pl" — Polish vegetarian sources
6. "best [dish] recipe tips" — technique tips
7. "[dish] common mistakes" — what to avoid
```

From search results extract:
- Ingredient lists with quantities
- Step-by-step instructions
- Cook times and temperatures
- Ratings and review counts
- Key technique notes

### Phase 3: Recipe Synthesis

Analyze across sources to identify:
- **Consensus ingredients** — appearing in 3+ sources
- **Best techniques** — from most detailed/authoritative source
- **Timing consensus** — average cook times, note outliers
- **Variations** — notable differences between sources and why

Create synthesized "best of" recipe combining:
- Most complete ingredient list
- Clearest technique instructions
- Most reliable timings

### Phase 4: Metric Conversion

Read `metric-conversions.md` KB for reference.

Convert ALL measurements:
- Volume → weight in grams (accounting for ingredient density)
- Fahrenheit → Celsius
- Inches → centimeters
- Cups/tablespoons → ml for liquids

Format: `200g (1⅔ cups) flour`

**Critical:** Different ingredients have different densities:
- 1 cup flour ≈ 120g
- 1 cup sugar ≈ 200g
- 1 cup butter ≈ 227g

### Phase 5: Verification Sub-Agent

Spawn verification agent:

```
Task tool:
  subagent_type: general-purpose
  prompt: |
    Verify this recipe for cooking science accuracy:

    [INSERT SYNTHESIZED RECIPE]

    Check against verification-checklist.md criteria:
    1. Temperature safety (internal temps for proteins)
    2. Cooking times (realistic for dish type)
    3. Ingredient ratios (hydration, salt %, acid balance)
    4. Technique sequence (logical order, no missing steps)
    5. Resting times (meat, dough, etc.)

    Flag concerns with [CONCERN] tag and explanation.
    Cross-reference with food science sources if needed.

    Return: verification status + any concerns
```

### Phase 6: Nutritional Analysis

WebSearch queries for nutrition:
- "USDA [ingredient] nutrition per 100g" for main ingredients
- Calculate per-serving based on total yield

Report:
- Calories
- Protein (g)
- Carbohydrates (g)
- Fat (g)
- Notable allergens (gluten, dairy, nuts, soy, eggs)

### Phase 7: Generate Output

Follow `output-template.md` format exactly. **Write entire recipe in Polish.**

Include:
- Recipe header with timing and difficulty
- Nutrition table
- Ingredients in metric (original in parentheses)
- **Two instruction versions:**
  - Quick Reference — simple numbered steps only
  - Detailed — mise en place first, technique names, "why" explanations
- Equipment list
- Verification notes (any concerns)
- Substitution suggestions
- Source citations with what each contributed

### Phase 8: Save Output

Save to **both** locations:
1. `findings/recipes/[dish-name-slugified].md` — local archive
2. Create Notion page with title `Recipe: [dish-name]` in workspace

Create directories if needed.

Use workspace conventions:
- Emojis for visual scanning
- Bullet points over paragraphs
- Tags: #recipe #[cuisine] #[dietary-tags]
- Wikilink to [[Cooking Techniques MOC]] if exists

## Error Handling

- **No results:** Try broader search terms, remove site restrictions
- **Conflicting info:** Note discrepancy, prefer authoritative source (Serious Eats > random blog)
- **Missing nutrition:** Estimate or note "nutrition data unavailable"
- **Verification fails:** Include concerns prominently, suggest fixes

## Quality Checklist

Before saving, verify:
- [ ] All measurements in metric with original in parentheses
- [ ] Temperatures in Celsius
- [ ] Nutrition calculated
- [ ] At least 3 sources cited
- [ ] Equipment list complete
- [ ] Difficulty rating justified
- [ ] Verification agent ran
- [ ] Mise en place is first instruction step
