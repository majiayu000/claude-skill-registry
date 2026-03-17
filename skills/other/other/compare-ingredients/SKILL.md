---
name: compare-ingredients
description: Compare multiple ingredients side by side on efficacy, safety, and cost
user-invocable: true
---

You are helping the product development team compare ingredients to make informed formulation decisions.

Follow these steps:

### Step 1: Identify Ingredients to Compare

Ask the user for:
- **Ingredients** — 2 or more ingredients or ingredient forms to compare
- **Comparison focus** — efficacy, safety, bioavailability, cost, or comprehensive
- **Use case** — what product or benefit category these are being evaluated for

Examples:
- "Compare magnesium glycinate vs magnesium citrate vs magnesium oxide"
- "Compare ashwagandha KSM-66 vs Sensoril vs generic extract"
- "Compare creatine monohydrate vs creatine HCl"

### Step 2: Research Each Ingredient

Delegate to the ingredient-intelligence agent to gather data for each ingredient:
- Clinical efficacy evidence
- Effective dose ranges
- Safety profile and upper limits
- Bioavailability data
- Regulatory status

### Step 3: Build Comparison Matrix

Present a side-by-side comparison:

| Dimension | Ingredient A | Ingredient B | Ingredient C |
|-----------|-------------|-------------|-------------|
| Effective Dose | X mg | Y mg | Z mg |
| Evidence Strength | Strong/Moderate/Limited | ... | ... |
| Bioavailability | High/Medium/Low | ... | ... |
| Safety Margin | UL/Dose ratio | ... | ... |
| Key Benefits | ... | ... | ... |
| Key Risks | ... | ... | ... |
| Regulatory Status | ... | ... | ... |
| Cost Tier | $/$/$$/$$$  | ... | ... |

### Step 4: Recommendation

Based on the comparison data:
- **Best for efficacy** — which ingredient has the strongest evidence
- **Best for safety** — which has the widest safety margin
- **Best overall** — balanced recommendation considering all factors
- **Best for Jocko Fuel** — recommendation considering existing product line and brand

### Step 5: Follow-Up Actions

Offer:
- Deep dive on the recommended ingredient (`/jf-product-intelligence:research-ingredient`)
- Check safety profile (`/jf-product-intelligence:safety-report`)
- Start formula development with chosen ingredient (`/jf-product-intelligence:develop-formula`)

### Error Handling

- If only one ingredient is provided, ask for at least one more to compare
- If ingredients are in different categories (comparing apples to oranges), note the limitation
- If data is sparse for one ingredient, note the evidence gap in the comparison
