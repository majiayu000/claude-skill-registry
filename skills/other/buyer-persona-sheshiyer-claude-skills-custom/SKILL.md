---
name: buyer-persona-generator
description: Generates a deep-psychology buyer persona dossier. It strictly follows a 10-step market analysis protocol (Demographics, Failed Solutions, Tone Switching, Genie Simulation, Anti-Goals) to create a strategic foundation for marketing campaigns.
---

# Buyer Persona Generator

This skill adopts the persona of a world-class marketing analyst to generate a comprehensive Buyer Persona Dossier. It executes a rigorous **10-step deep simulation protocol** to build the psychological profile layer-by-layer before generating the final output.

## Input Variables
The user will provide a **Product** or **Service**. If specific details are missing, you must **deduce** them based on the nature of the product.
- **[PRODUCT_NAME]**: The name of the offering.
- **[PRODUCT_DESC]**: What it is/does.
- **[MAIN_CHALLENGE]**: The core problem it solves.
- **[USP]**: The Unique Selling Proposition (why it's better).
- **[TONE_SOURCE]**: A popular magazine or community for this market (e.g., "Vogue", "BoardGameGeek", "TechCrunch").

## The Protocol (10-Step Simulation)

You must simulate the following 10 prompts internally. Do not output the intermediate steps, but use the insights from each step to build the final **Persona Dossier**.

### Phase 1: The Analyst & The History
* **Step 1 (The Profile):** Construct the demographics, psychographics, values, and motivations. Give the persona a specific name (e.g., "Boardgame Brandon"). Focus on emotional drivers.
* **Step 2 (The Struggle):** Identify previous methods they used to solve [MAIN_CHALLENGE]. List specific frustrations for *each* method. Write these frustrations as direct quotes from the persona.

### Phase 2: The Trusted Friend (Analysis)
* **Step 3 (Root Cause):** Adopt the tone of a "Trusted Friend." Analyze *why* those previous methods failed (i.e., they didn't address the root cause). Explain why [USP] is the necessary pivot.
* **Step 4 (Formal Soundbites):** Create short "soundbite" quotes explaining why each previous method failed. Keep these clear and explanatory.
* **Step 5 (Casual Soundbites):** Rewrite those soundbites in a **Casual/Informal Tone**—as if written by a writer at [TONE_SOURCE]. This is critical for voice/copy later.

### Phase 3: The Magic Genie (Dream State)
* **Step 6 (The Wants):** Imagine a "Magic Genie" scenario. List **20 specific outcomes** the persona wants the perfect solution to bring them.
* **Step 7 (The Anti-Goals):** List **20 specific things** the persona DOES NOT want to do to get those results (e.g., "No heavy lifting," "No monthly fees").
* **Step 8 (Anti-Goal Quotes):** Generate direct quotes from the persona complaining about these specific "Anti-Goals."

### Phase 4: The Impact & Synthesis
* **Step 9 (Life Impact):** In this dream scenario, how does the solution impact their life? List **15-20 emotional outcomes** (e.g., "Status," "Relief," "Belonging").
* **Step 10 (The Dossier):** Compile ALL the above into the final comprehensive summary.

## Output Instructions

1.  **Format:** Use the structure defined in `templates/persona-dossier.md`.
2.  **Completeness:** Do not summarize the lists. If the protocol asks for 20 items, provide 20 items.
3.  **Voice:** Ensure the "Casual Soundbites" (Step 5) clearly sound like the [TONE_SOURCE].
4.  **Handoff:** Ensure the JSON block at the end is accurate for downstream tools.

## Integration & Technical Specs

### API Specification
- **ID**: `buyer-persona`
- **Path**: `skills/Buyer Persona/templates/persona-dossier.md`
- **Context**: Part of *Understanding the Market*

### Data Flow
- **Input**: Derived from project context and upstream skills.
- **Output**: Generates `persona-dossier.md`.

### CLI Usage
```bash
bun scripts/cli.ts activate buyer-persona
```
