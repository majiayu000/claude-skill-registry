---
name: competitor-analysis
description: Executes a deep-dive market intelligence protocol. Uses search tools to scrape competitor data (Specs, Price, Materials), analyzes customer sentiment (Reviews, FAQs), and synthesizes a product knowledge base.
---
# Competitor Analysis & Market Intelligence

This skill acts as a world-class marketing analyst with meticulous attention to detail. It constructs a **Comprehensive Product Knowledge Base** about the competition. This output serves as the "Truth Source" for all future positioning strategies.

## Input Variables

- **[PRODUCT_CATEGORY]**: The niche we are entering (e.g., "Boardgame Backpack").
- **[COMPETITOR_NAME]**: (Optional) A specific rival to analyze (e.g., "GeekOn"). If blank, find the current market leader.

## The Protocol (Deep-Dive Research Sequence)

You must execute these 5 phases in order. Do not skip details.

### Phase 1: The "Hard Data" Scrape (Specs & Anatomy)

Use search tools to find the "Golden Path" product page (official site or Kickstarter). Extract the exact technical specifications:

* **Price:** Full retail vs. "Early Bird" pricing.
* **Dimensions & Weight:** Precise measurements (Extended vs. Non-extended).
* **Materials:** Specific fabric names (e.g., "500D Ripstop Nylon"), zippers, padding types.
* **Capacity:** Liters or cubic inches.
* **Features:** List every specific claim (e.g., "Koozie holder," "EVA frame").

### Phase 2: The "Voice of the Customer" (Review Mining)

Search for reviews on Amazon, Kickstarter Comments, or Reddit. You are looking for **Polarity**:

* **The Love (5-Star):** What specific feature do they rave about? (e.g., "The expandable shelf").
* **The Hate (1-Star):** What actually broke? What disappointed them? (e.g., "Zippers are too stiff," "Not actually carry-on compliant"). **Quote these complaints directly.**

### Phase 3: The "Anxiety Audit" (FAQ Analysis)

Find the FAQ section. Analyze the specific questions customers are asking.

* *Why?* Questions reveal anxieties and marketing gaps.
* (e.g., "Does it fit a 17-inch laptop?" -> Anxiety about device compatibility).

### Phase 4: The Synthesis (Product Description Generation)

**Assume the role of a copywriter.** Write a comprehensive, multi-paragraph product description of the competitor.

* Do not just bullet point it. Write it out fully, summarizing features, benefits, use cases, and audience.
* This narrative helps the AI "feel" the brand voice of the competitor.

### Phase 5: The Strategic Output

Compile all data into the `templates/competitor-intelligence.md` file.

* **CRITICAL:** Ensure the "Cascading Handoff" JSON block is populated with *specific* arrays for Weaknesses and Specs, as the next skill (Positioning) needs these to find our Unique Selling Proposition.

## Guidelines

1. **Be Specific:** Do not say "Durable material." Say "500D Ripstop Nylon."
2. **Trace the Source:** If a spec varies (e.g., Amazon says one thing, Website says another), note the discrepancy.
3. **Quote the Hate:** When listing weaknesses, use the exact words of the angry customer (e.g., "Straps ripped after 2 weeks").


## Integration & Technical Specs

### API Specification
- **ID**: `competitor-analysis`
- **Path**: `skills/competitor-analysis/templates/competitor-intelligence.md`
- **Context**: Part of *Understanding the Market*

### Data Flow
- **Input**: Derived from project context and upstream skills.
- **Output**: Generates `competitor-intelligence.md`.

### CLI Usage
```bash
bun scripts/cli.ts activate competitor-analysis
```
