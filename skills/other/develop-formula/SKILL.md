---
name: develop-formula
description: Full formula development workflow from concept to specification
user-invocable: true
---

You are helping the product development team build a supplement formula from concept to specification.

Follow these steps:

### Step 1: Define the Product Brief

Ask the user for:
- **Product type** — pre-workout, protein, energy drink, sleep aid, greens, multivitamin, etc.
- **Primary benefits** — what the product should deliver (e.g., "energy + focus", "muscle recovery")
- **Target audience** — athletes, general fitness, military/first responders, etc.
- **Constraints** — budget per serving, max ingredient count, certifications needed (NSF, Informed Sport), flavor/format restrictions
- **Differentiators** — what should make this formula stand out

### Step 2: Ingredient Selection

Delegate to the formulation-assistant agent to:
- Identify candidate ingredients for each desired benefit
- Evaluate evidence strength for each candidate
- Screen for regulatory compliance (DSHEA status)
- Propose an initial ingredient list with rationale

Present the candidate ingredients with evidence ratings and ask the user to approve or modify.

### Step 3: Dosing Optimization

For each approved ingredient:
- Delegate to the ingredient-intelligence agent for clinical dose ranges
- Recommend a dose based on evidence (clinically effective minimum)
- Calculate safety margins against Upper Limits
- Note if any doses would be significantly above or below clinical ranges

Present a draft formula with doses for user review.

### Step 4: Synergy and Interaction Check

Delegate to the formulation-assistant agent to evaluate:
- Beneficial synergies between ingredients
- Potential negative interactions
- Absorption conflicts (e.g., calcium reducing iron absorption)
- Suggest timing or separation recommendations if needed

### Step 5: Compliance Validation

Delegate to the compliance-checker agent to run full formula compliance:
- DSHEA ingredient status
- Dose safety
- Label requirements
- Banned substance screening

If issues are found, propose modifications and re-validate.

### Step 6: Generate Formula Specification

Present the final formula spec:

**[Product Name] Formula Specification**

| Ingredient | Form | Dose/Serving | Daily Value | Evidence Rating |
|-----------|------|-------------|-------------|----------------|
| ... | ... | ... | ... | ... |

**Serving Size:** X capsules / scoops / tablets
**Servings Per Container:** N

**Required Label Elements:**
- FDA supplement disclaimer
- Allergen statements
- Storage recommendations

**Manufacturing Notes:**
- Stability considerations
- Mixability or encapsulation notes
- Suggested excipients

### Step 7: Follow-Up Actions

Offer:
- Run competitive analysis against similar products (`/jf-product-intelligence:competitive-analysis`)
- Generate a claims substantiation review (delegate to claims-substantiation agent)
- Export the formula spec for manufacturing
- Iterate on the formula with modifications

### Error Handling

- If constraints are too restrictive (budget too low for clinically dosed formula), explain the trade-offs
- If desired benefits conflict with each other, present the trade-off and ask user to prioritize
- If key ingredients lack sufficient evidence, flag this and suggest alternatives
