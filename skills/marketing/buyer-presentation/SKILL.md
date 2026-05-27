---
name: buyer-presentation
description: Generate buyer-ready sales collateral from market data
user-invocable: true
---

You are helping the sales team create buyer-ready sales collateral for retailer meetings. This skill combines Circana market data with the `buyer-strategist` and `presentation-builder` agents.

### Step 1: Define the Presentation

Ask the user:
- **Target retailer**: Which buyer/retailer is this for?
- **Meeting type**: Line review, new item pitch, promotional proposal, business review?
- **Products**: Which Jocko Fuel products to feature?
- **Key message**: What's the primary selling story?

### Step 2: Gather Market Data

Delegate to agents for data collection:
1. **freshness-monitor** — Verify data currency
2. **market-analyst** — Pull category performance, share trends, competitive landscape
3. **segment-helper** — Validate product segmentation for the target category

### Step 3: Build the Sell Story

Delegate to `buyer-strategist` to transform raw data into a buyer-ready narrative:
- Category growth story (why this category matters to the retailer)
- Jocko Fuel performance proof points (velocity, share gains, distribution wins)
- Competitive gaps and whitespace opportunities
- Financial case (margin, turns, profit per linear foot)

### Step 4: Generate Presentation Content

Delegate to `presentation-builder` to create:
- Executive summary (1-page)
- Category overview with trends
- Product-specific sell sheets
- Recommended planogram changes or distribution expansion
- Promotional calendar proposal (if applicable)

### Step 5: Review and Refine

Present the generated content for user review. Offer:
- Adjust tone or emphasis
- Add/remove data points
- Change the competitive framing
- Generate additional supporting slides

### Output

All content is generated as markdown. The user can copy into their preferred presentation tool (PowerPoint, Google Slides, Sigma).

### Error Handling

- If Circana data is stale (>14 days), warn prominently — buyer presentations must use current data
- If the target retailer isn't in the Circana dataset, note the limitation and use total MULO data
