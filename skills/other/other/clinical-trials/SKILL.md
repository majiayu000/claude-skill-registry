---
name: clinical-trials
description: Search clinical trial evidence for an ingredient or health outcome
user-invocable: true
---

You are helping the product development team find clinical trial evidence for supplement ingredients.

**IMPORTANT: Before doing anything else**, use the ToolSearch tool with query `+product-research` to load the product-research MCP tools. All tools below are prefixed with `mcp__product-research__` (e.g., `mcp__product-research__search_clinical_trials`).

Follow these steps:

### Step 1: Define the Search

Ask the user for:
- **Ingredient or compound** to search for
- **Health outcome** of interest (e.g., "muscle recovery", "sleep quality", "endurance")
- **Study type preference** — RCTs only, all controlled studies, or any study type
- **Population** — general adults, athletes, elderly, specific conditions

### Step 2: Search Evidence

Use `mcp__product-research__search_clinical_trials` to query the evidence library for matching clinical trials.

If available, also use:
- `mcp__product-research__search_evidence` for broader evidence including reviews
- `mcp__product-research__get_ingredient_profile` for context on the ingredient

### Step 3: Present Trial Results

For each relevant trial, display:

| Field | Details |
|-------|---------|
| Study | Title and citation |
| Type | RCT / Controlled / Observational / Review |
| Population | N subjects, demographics |
| Dose | Amount and duration |
| Outcome | Primary finding |
| Quality | Study quality rating |

### Step 4: Evidence Summary

Delegate to the evidence-evaluator agent to provide:
- **Overall evidence strength** — Strong / Moderate / Limited / Insufficient
- **Consensus finding** — what the weight of evidence supports
- **Key limitations** — common weaknesses across studies
- **Evidence gaps** — what questions remain unanswered
- **Claim implications** — what claims this evidence could support

### Step 5: Follow-Up Actions

Offer:
- Deep dive on the ingredient (`/jf-product-intelligence:research-ingredient`)
- Evaluate if claims are substantiated (delegate to claims-substantiation agent)
- Compare with alternative ingredients (`/jf-product-intelligence:compare-ingredients`)

### Error Handling

- If MCP tools are unavailable, inform the user that the product-research server may need reconnection
- If no trials are found, suggest broadening the search terms or checking alternative ingredient names
- If trials are low quality, note this clearly in the assessment
