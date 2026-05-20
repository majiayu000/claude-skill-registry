---
name: pre-launch-ads
description: "The 'Programmatic Ad Engine'. It executes a massive 35-step creative protocol to generate a complete Pre-Launch Advertising Campaign. It ingests Brand and Product strategies, applies a user-defined 'Awareness vs. Conversion' algorithm, and outputs 39 high-performance ad assets optimized for Indiegogo/Kickstarter."
---
# Pre-Launch Ad Campaign Generator

This skill acts as a **Full-Stack Paid Media Team** (Strategist, Copywriter, and Media Buyer). It bridges the gap between high-level strategy and pixel-perfect execution. It uses a "Weighted Logic" system to determine the exact angle, tone, and structure of the copy based on the campaign's specific goals.

## Input Variables

- **[BRAND_BIBLE]**: The psychological core (Persona, Voice, Tone, "False Trade-off").
- **[PRODUCT_BIBLE]**: The technical core (Features, Specs, Ecosystem, Benefits).
- **[CAMPAIGN_GOAL]**: The strategic lever (e.g., "High Awareness," "Balanced," or "High Conversion").

## The Protocol (The 35-Step Creative Engine)

You must execute this sequence linearly. Do not summarize.

### Phase 1: The Strategic Calibration (The "JS Brain")

*Read `src/campaign-logic.js` conceptually to perform this step.*

* **Step 1 (Goal Analysis):** Analyze the `[CAMPAIGN_GOAL]`.
  * *Awareness:* Prioritize emotional hooks, storytelling, and curiosity.
  * *Conversion:* Prioritize direct offers, scarcity, and feature stacking.
* **Step 2 (Persona Injection):** Extract the "Bleeding Neck" pain point and the "Dream State" from the `[BRAND_BIBLE]`.
* **Step 3 (Product Extraction):** Identify the "Hero Feature" and the "Killer Spec" from the `[PRODUCT_BIBLE]`.
* **Step 4 (The Tone Setting):** Define the specific "Ad Voice." (e.g., If Conversion = High, Tone = "Urgent Insider").

### Phase 2: The Campaign Concept (The "Big Idea")

*Before writing ads, define the creative universe.*

* **Step 5 (Campaign Name):** Create an internal code name for this creative flight (e.g., "Operation: No More Mess").
* **Step 6 (The Hook Strategy):** Write a paragraph explaining *why* this specific angle will stop the scroll for `[PERSONA_NAME]`.
* **Step 7 (The Visual Directive):** Describe the "Master Creative" image or video style that pairs with this copy.

### Phase 3: The Headline Stack (18 Assets)

*Generate 3 distinct variations for ALL 6 Headline Types.*

* **Step 8 (Discount Offer):** Write 3 headlines focusing on the "Pre-Launch Deal" and "Savings Logic." (Logic: Direct ROI).
* **Step 9 (Hyperbole):** Write 3 headlines using "Superlatives" and "Category Leadership." (Logic: High Click-Through).
* **Step 10 (Summary of Features):** Write 3 headlines that stack value immediately. (Logic: High Perceived Value).
* **Step 11 (Emotional Selling):** Write 3 headlines targeting the "Anti-Goals" from the Brand Bible. (Logic: Resonance).
* **Step 12 (Soundbyte):** Write 3 punchy, short headlines (under 5 words). (Logic: Pattern Interrupt).
* **Step 13 (Founder/Brand Story):** Write 3 headlines leveraging the "Origin Story" or "Authority." (Logic: Trust).

### Phase 4: The Body Copy Stack (21 Assets)

*Generate 3 distinct variations for ALL 7 Body Copy Types.*

* **Step 14 (Bulleted Feature List):** Write 3 versions using the "Feature-Benefit-Emoji" format.
* **Step 15 (Benefit List):** Write 3 versions focusing purely on lifestyle outcomes (The "So What?").
* **Step 16 (Product Description):** Write 3 "Elevator Pitch" versions (Short, Medium, Long).
* **Step 17 (Problem Introduction):** Write 3 versions using the "Agitation-Solution" framework.
* **Step 18 (Testimonial Review):** Simulate 3 user reviews that perfectly match the *Voice Persona*.
* **Step 19 (Audience Callout):** Write 3 versions that explicitly flag the persona (e.g., "Attention D&D Masters").
* **Step 20 (The Magic Formula):** Write 3 versions using the "Math Equation" format (Problem + Product = Joy).

### Phase 5: The "Scroll-Stopper" Analysis

*Review the work against the algorithm.*

* **Step 21 (The Persona Test):** Would `[PERSONA_NAME]` actually read this? Adjust slang if needed.
* **Step 22 (The Formatting Check):** Ensure emojis are used strategically (not spammy).
* **Step 23 (The CTA Check):** Ensure every single ad has a clear Call to Action.

## Output Instructions

Compile all 39 assets and strategic notes into `templates/ad-campaign-dossier.md`. Be extremely verbose. Provide rationale for the "Big Idea."


## Integration & Technical Specs

### API Specification
- **ID**: `pre-launch-ads`
- **Path**: `skills/pre-launch-ads/templates/ad-campaign-dossier.md`
- **Context**: Part of *Crafting Compelling Copy*

### Data Flow
- **Input**: Derived from project context and upstream skills.
- **Output**: Generates `ad-campaign-dossier.md`.

### CLI Usage
```bash
bun scripts/cli.ts activate pre-launch-ads
```
