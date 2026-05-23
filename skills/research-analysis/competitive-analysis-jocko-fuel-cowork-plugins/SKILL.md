---
name: competitive-analysis
description: Analyze competitor supplement products for formula, pricing, and positioning
user-invocable: true
---

You are helping the product development team analyze competitor products in the supplement market.

**IMPORTANT: Before doing anything else**, use the ToolSearch tool with query `+product-research` to load the product-research MCP tools. All tools below are prefixed with `mcp__product-research__` (e.g., `mcp__product-research__search_evidence`).

Follow these steps:

### Step 1: Define the Analysis Scope

Ask the user for:
- **Product category** — pre-workout, protein, energy drink, greens, etc.
- **Specific competitors** — brand/product names to analyze (or "top competitors")
- **Jocko Fuel product** — which Jocko Fuel product to benchmark against
- **Focus areas** — formula comparison, pricing, claims, positioning, or comprehensive

### Step 2: Gather Competitor Data

Delegate to the competitive-analysis agent to research:
- Competitor product formulas (ingredients, doses, forms)
- Pricing and serving economics
- Marketing claims and positioning
- Certifications and third-party testing
- Distribution channels and availability

Use `mcp__product-research__` tools for ingredient evidence to cross-reference competitor claims with scientific backing.

### Step 3: Build Competitive Matrix

Present a comparison:

| Dimension | Jocko Fuel | Competitor A | Competitor B |
|-----------|-----------|-------------|-------------|
| Key Ingredients | ... | ... | ... |
| Clinical Doses | Yes/No per ingredient | ... | ... |
| Price/Serving | $X.XX | $X.XX | $X.XX |
| Certifications | ... | ... | ... |
| Key Claims | ... | ... | ... |
| Claim Substantiation | Strong/Weak | ... | ... |

### Step 4: Strategic Insights

Provide analysis on:
- **Jocko Fuel advantages** — where we differentiate positively
- **Competitive gaps** — where competitors are stronger
- **Market opportunities** — unmet needs or underserved segments
- **Claim vulnerabilities** — competitor claims that may be unsubstantiated
- **Pricing position** — where we sit in the market

### Step 5: Recommendations

Based on analysis:
- Formula differentiation opportunities
- Messaging and positioning adjustments
- Pricing strategy considerations
- New product category opportunities

### Error Handling

- If competitor data is limited, note what could not be found
- If competitor uses proprietary blends, note the dose uncertainty
- If MCP tools are unavailable, rely on web research and note the limitation
