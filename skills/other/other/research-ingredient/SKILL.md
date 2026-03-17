---
name: research-ingredient
description: Deep research on a specific ingredient using the product-research MCP
user-invocable: true
---

You are helping the product development team research a supplement ingredient in depth.

**IMPORTANT: Before doing anything else**, use the ToolSearch tool with query `+product-research` to load the product-research MCP tools. All tools below are prefixed with `mcp__product-research__` (e.g., `mcp__product-research__search_evidence`).

Follow these steps:

### Step 1: Identify the Ingredient

Ask the user for:
- **Ingredient name** (common name and/or scientific name)
- **Specific form** if applicable (e.g., "magnesium glycinate" vs "magnesium" generally)
- **Research focus** — efficacy, safety, dosing, bioavailability, or comprehensive

### Step 2: Query the Evidence Library

Use `mcp__product-research__search_evidence` to search for evidence on the ingredient. Also try:
- `mcp__product-research__get_ingredient_profile` for a structured ingredient overview
- `mcp__product-research__search_clinical_trials` for clinical trial data

### Step 3: Compile the Research Report

Present a structured ingredient intelligence report:

**Ingredient Overview:**
- Common and scientific names
- Regulatory status (GRAS, NDI, dietary ingredient)
- Common forms and their differences

**Efficacy Evidence:**
- Key clinical findings with study quality ratings
- Effective dose ranges from clinical studies
- Onset and duration of effects

**Safety Profile:**
- Upper intake level (UL) and safety margins
- Known adverse effects and their frequency
- Drug interactions and contraindications
- Special population considerations (pregnancy, pediatric, elderly)

**Bioavailability:**
- Absorption rates for different forms
- Factors affecting absorption
- Recommended form for optimal bioavailability

**Jocko Fuel Relevance:**
- Current Jocko Fuel products containing this ingredient
- Potential applications in new formulas

### Step 4: Follow-Up Actions

Offer the user:
- Compare with alternative ingredients (`/jf-product-intelligence:compare-ingredients`)
- Check safety in detail (`/jf-product-intelligence:safety-report`)
- Search clinical trials (`/jf-product-intelligence:clinical-trials`)
- Start formula development (`/jf-product-intelligence:develop-formula`)

### Error Handling

- If MCP tools are unavailable, inform the user that the product-research server may need reconnection
- If the ingredient is not in the evidence library, note this and offer web-based research as a supplement
- If the ingredient name is ambiguous, ask the user to clarify the specific compound
