---
name: check-formula
description: Validate a supplement formula for FDA and DSHEA compliance
user-invocable: true
---

You are helping the product development team validate a supplement formula for regulatory compliance.

Follow these steps:

### Step 1: Get the Formula

Ask the user for the formula details. Accept:
- Ingredient list with doses (pasted text, table, or CSV)
- Path to a formula specification file
- Product name to look up in existing catalogs

For each ingredient, capture:
- Ingredient name and form
- Dose per serving
- Daily value percentage (if applicable)

### Step 2: Compliance Analysis

Delegate to the compliance-checker agent to evaluate:

**Ingredient Legality:**
- Is each ingredient a recognized dietary ingredient under DSHEA?
- Are any ingredients subject to NDI (New Dietary Ingredient) notification requirements?
- Are any ingredients on banned/prohibited substance lists?
- NSF/Informed Sport status for each ingredient

**Dosing Safety:**
- Is each dose within the established Upper Limit (UL)?
- Safety margin calculation (UL / proposed dose)
- Are any doses below clinically effective ranges (underdosed)?
- Cumulative exposure considerations

**Label Compliance:**
- Supplement Facts panel requirements
- Required disclaimers
- Allergen declarations
- "Other ingredients" requirements

**Interaction Screening:**
- Ingredient-ingredient interactions within the formula
- Common drug-supplement interactions to disclose

### Step 3: Present Compliance Report

Display:
- **Status**: COMPLIANT / NON-COMPLIANT / NEEDS REVIEW
- **Critical issues** (blocks manufacturing)
- **Warnings** (recommended changes)
- **Notes** (informational items)

For each issue:
- Ingredient and dose in question
- Specific regulation or safety concern
- Recommended action

### Step 4: Remediation

If issues were found, offer to:
- Suggest compliant dose adjustments
- Recommend alternative ingredient forms
- Generate a revised formula specification
- Re-run the compliance check after modifications

### Error Handling

- If ingredient names are ambiguous, ask the user to confirm specific forms
- If no dose is provided, flag it as incomplete and request the information
- If the formula is for a non-supplement product category, note the limitation
