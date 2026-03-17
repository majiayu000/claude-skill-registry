---
name: safety-report
description: Generate a safety and toxicology report for an ingredient
user-invocable: true
---

You are helping the product development team assess the safety profile of a supplement ingredient.

Follow these steps:

### Step 1: Identify the Ingredient

Ask the user for:
- **Ingredient name** and specific form
- **Proposed dose** per serving (if known)
- **Proposed frequency** — once daily, twice daily, etc.
- **Target population** — general adult, athletes, specific demographics

### Step 2: Safety Assessment

Delegate to the safety-monitoring agent to compile:

**Toxicology Data:**
- Established Upper Limit (UL) from regulatory bodies
- NOAEL from animal studies (if available)
- LD50 reference data (if available)
- Safety margin at proposed dose (UL / daily dose)

**Adverse Event Profile:**
- Known adverse effects and their frequency
- Dose-dependent effects (what happens at higher doses)
- Reported serious adverse events
- FDA adverse event database findings

**Interaction Risks:**
- Drug-supplement interactions (common medications)
- Supplement-supplement interactions
- Food interactions affecting absorption or safety

**Special Populations:**
- Pregnancy and lactation safety
- Pediatric considerations
- Elderly considerations
- Medical condition contraindications (liver, kidney, cardiovascular)

**Allergen and Contaminant Risk:**
- Common allergen cross-reactivity
- Heavy metal contamination potential (source-dependent)
- Solvent residue risk (for extracts)

### Step 3: Present Safety Report

Display a structured safety report:
- **Safety Rating**: GREEN (well-established safe) / YELLOW (generally safe with precautions) / RED (significant concerns)
- **Safety margin** at proposed dose
- **Key risks** ranked by severity and likelihood
- **Required warnings** for label and marketing
- **Recommended monitoring** (if applicable)

### Step 4: Recommendations

Based on the safety assessment:
- Recommended maximum dose
- Required label warnings and disclaimers
- Populations to exclude from marketing
- Suggested quality controls for manufacturing

### Error Handling

- If the ingredient lacks toxicology data, note the data gap and recommend caution
- If the proposed dose exceeds the UL, flag this prominently
- If the ingredient is not recognized, verify the name with the user
