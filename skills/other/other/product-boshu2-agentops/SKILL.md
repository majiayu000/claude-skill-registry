---
name: product
description: 'Interactive PRODUCT.md generation. Interviews you about mission, personas, value props, and competitive landscape, then generates a filled-in PRODUCT.md. Triggers: "product", "create product doc", "product definition", "who is this for".'
metadata:
  tier: product
  dependencies: []
---

# /product — Interactive PRODUCT.md Generation

> **Purpose:** Guide the user through creating a `PRODUCT.md` that unlocks product-aware council reviews in `/pre-mortem` and `/vibe`.

**YOU MUST EXECUTE THIS WORKFLOW. Do not just describe it.**

**CLI dependencies:** None required.

## Execution Steps

Given `/product [target-dir]`:

- `target-dir` defaults to the current working directory.

### Step 1: Pre-flight

Check if PRODUCT.md already exists:

```bash
ls PRODUCT.md 2>/dev/null
```

**If it exists:**

Use AskUserQuestion:
- **Question:** "PRODUCT.md already exists. What would you like to do?"
- **Options:**
  - "Overwrite — start fresh" → continue to Step 2
  - "Update — keep existing content as defaults" → read existing file, use its values as pre-populated suggestions in Step 3
  - "Cancel" → stop, report no changes

**If it does not exist:** continue to Step 2.

### Step 2: Gather Context

Read available project files to pre-populate suggestions:

1. **README.md** — extract project description, purpose, target audience
2. **package.json / pyproject.toml / go.mod / Cargo.toml** — extract project name
3. **Directory listing** — `ls` the project root for structural hints

Use what you find to draft initial suggestions for each section. If no files exist, proceed with blank suggestions.

### Step 3: Interview

Ask the user about each section using AskUserQuestion. For each question, offer pre-populated suggestions from Step 2 where available.

#### 3a: Mission

Ask: "What is your product's mission? (One sentence: what does it do and for whom?)"

Options based on README analysis:
- Suggested mission derived from README (if available)
- A shorter/punchier variant
- "Let me type my own"

#### 3b: Target Personas

Ask: "Who are your primary users? Describe 2-3 personas."

For each persona, gather:
- **Role** (e.g., "Backend Developer", "DevOps Engineer")
- **Goal** — what they're trying to accomplish
- **Pain point** — what makes this hard today

Use AskUserQuestion for the first persona's role, then follow up conversationally for details and additional personas. Stop when the user says they're done or after 3 personas.

#### 3c: Core Value Propositions

Ask: "What makes your product worth using? List 2-4 key value propositions."

Options:
- Suggestions derived from README/project context
- "Let me type my own"

#### 3d: Competitive Landscape

Ask: "What alternatives exist, and how do you differentiate?"

Gather:
- Alternative names
- Their strengths
- Your differentiation

If the user says "none" or "skip", write "No direct competitors identified" in the section.

### Step 4: Generate PRODUCT.md

Write `PRODUCT.md` to the target directory with this structure:

```markdown
---
last_reviewed: YYYY-MM-DD
---

# PRODUCT.md

## Mission

{mission from 3a}

## Target Personas

### Persona 1: {role}
- **Goal:** {goal}
- **Pain point:** {pain point}

{repeat for each persona}

## Core Value Propositions

{bullet list from 3c}

## Competitive Landscape

| Alternative | Strength | Our Differentiation |
|-------------|----------|---------------------|
{rows from 3d}

## Usage

This file enables product-aware council reviews:

- **`/pre-mortem`** — Automatically includes `product` perspectives (user-value, adoption-barriers, competitive-position) alongside plan-review judges when this file exists.
- **`/vibe`** — Automatically includes `developer-experience` perspectives (api-clarity, error-experience, discoverability) alongside code-review judges when this file exists.
- **`/council --preset=product`** — Run product review on demand.
- **`/council --preset=developer-experience`** — Run DX review on demand.

Explicit `--preset` overrides from the user skip auto-include (user intent takes precedence).
```

Set `last_reviewed` to today's date (YYYY-MM-DD format).

### Step 5: Report

Tell the user:

1. **What was created:** `PRODUCT.md` at `{path}`
2. **What it unlocks:**
   - `/pre-mortem` will now auto-include product perspectives (user-value, adoption-barriers, competitive-position)
   - `/vibe` will now auto-include developer-experience perspectives (api-clarity, error-experience, discoverability)
   - `/council --preset=product` and `/council --preset=developer-experience` are available on demand
3. **Next steps:** Suggest running `/pre-mortem` on their next plan to see product perspectives in action

## Examples

### Creating Product Doc for New Project

**User says:** `/product`

**What happens:**
1. Agent checks for existing PRODUCT.md, finds none
2. Agent reads README.md and package.json to extract project context
3. Agent asks user about mission, suggesting "CLI tool for automated dependency updates"
4. Agent interviews for 2 personas: DevOps Engineer and Backend Developer
5. Agent asks about value props, user provides: "Zero-config automation, Safe updates, Time savings"
6. Agent asks about competitors, user mentions Renovate and Dependabot
7. Agent writes PRODUCT.md with all gathered information and today's review date

**Result:** PRODUCT.md created, unlocking product-aware council perspectives in future validations.

### Updating Existing Product Doc

**User says:** `/product`

**What happens:**
1. Agent finds existing PRODUCT.md from 3 months ago
2. Agent prompts: "PRODUCT.md exists. What would you like to do?"
3. User selects "Update — keep existing content as defaults"
4. Agent reads current file, extracts mission and personas as suggestions
5. Agent asks about mission, user keeps existing one
6. Agent asks about personas, user adds new "Security Engineer" persona
7. Agent updates PRODUCT.md with new persona, updates `last_reviewed` date

**Result:** PRODUCT.md refreshed with additional persona, ready for next validation cycle.

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| No context to pre-populate suggestions | Missing README or project metadata files | Continue with blank suggestions. Ask user to describe project in own words. Extract mission from conversation. |
| User unclear on personas vs users | Confusion about persona definition | Explain: "Personas are specific user archetypes with goals and pain points. Think of one real person who would use this." Provide example. |
| Competitive landscape feels forced | Genuinely novel product or niche tool | Accept "No direct competitors" as valid. Focus on alternative approaches (manual processes, scripts) rather than products. |
| PRODUCT.md feels generic | Insufficient user input or rushed interview | Ask follow-up questions. Request specific examples. Challenge vague statements like "makes things easier" — easier how? Measured how? |
