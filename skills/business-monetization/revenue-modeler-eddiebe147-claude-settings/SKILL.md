---
name: Revenue Modeler
slug: revenue-modeler
description: Build revenue projection models with driver-based forecasting, scenario analysis, and pricing optimization
category: finance
complexity: complex
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "revenue model"
  - "revenue projection"
  - "sales forecast"
  - "pricing model"
  - "revenue growth"
  - "MRR forecast"
tags:
  - revenue-modeling
  - forecasting
  - pricing
  - saas-metrics
  - growth-planning
---

# Revenue Modeler

Expert revenue forecasting agent that builds driver-based revenue models, projects growth scenarios, optimizes pricing strategies, and forecasts subscription metrics. Specializes in SaaS revenue modeling, marketplace economics, and multi-stream revenue forecasting.

This skill applies rigorous revenue modeling methodologies to create defensible projections, stress-test assumptions, and support strategic planning. Perfect for fundraising projections, board reporting, budgeting, and pricing decisions.

## Core Workflows

### Workflow 1: SaaS Revenue Model

**Objective:** Build comprehensive SaaS/subscription revenue model

**Steps:**
1. **Current State Analysis**
   - Current MRR/ARR
   - Customer count by segment
   - ARPU by segment
   - Growth trends (MoM, YoY)
   - Cohort retention data

2. **Revenue Driver Identification**
   - **Customer Acquisition:**
     - New customer growth rate
     - Lead generation capacity
     - Conversion rates by channel
     - Sales capacity and productivity
     - CAC and payback period

   - **Customer Retention:**
     - Gross churn rate (customer count)
     - Net revenue retention (NRR)
     - Churn by segment/cohort
     - Contraction rate

   - **Expansion:**
     - Upsell rate
     - Cross-sell rate
     - Seat expansion
     - Tier upgrades

3. **Model Architecture**
   ```
   Beginning MRR
   + New MRR (new customers × ARPU)
   + Expansion MRR (existing customer upgrades)
   - Contraction MRR (downgrades)
   - Churned MRR (lost customers)
   = Ending MRR

   ARR = MRR × 12
   ```

4. **Cohort-Based Modeling**
   - Track each cohort separately
   - Apply cohort-specific retention curves
   - Model degradation over time
   - Account for seasonality

5. **Scenario Development**
   - **Base Case:**
     - Current trend continuation
     - Realistic growth assumptions

   - **Upside Case:**
     - Improved conversion
     - Lower churn
     - Higher expansion

   - **Downside Case:**
     - Slower acquisition
     - Higher churn
     - Economic headwinds

6. **Key Metrics Output**
   - MRR/ARR projections by month
   - Customer count projections
   - Net Revenue Retention
   - LTV/CAC ratio evolution
   - Payback period
   - Gross margin projections

**Deliverable:** Monthly MRR model with 12-36 month projections

### Workflow 2: Marketplace Revenue Model

**Objective:** Build revenue model for marketplace businesses

**Steps:**
1. **Marketplace Metrics Setup**
   - **Supply Side:**
     - Active sellers/providers
     - Listings per seller
     - Average order value
     - Supply growth rate

   - **Demand Side:**
     - Active buyers
     - Transactions per buyer
     - Buyer frequency
     - Demand growth rate

   - **Marketplace Metrics:**
     - Gross Merchandise Value (GMV)
     - Take rate percentage
     - Net revenue = GMV × Take rate

2. **GMV Driver Model**
   ```
   GMV = Active Buyers × Transactions/Buyer × Average Order Value

   OR

   GMV = Active Sellers × Listings/Seller × Sell-Through Rate × Price
   ```

3. **Take Rate Analysis**
   - Current take rate
   - Take rate by category
   - Take rate optimization potential
   - Competitive benchmarking
   - Additional revenue streams (ads, premium, fulfillment)

4. **Liquidity Modeling**
   - Match rate projections
   - Supply/demand balance
   - Geographic coverage
   - Category depth

5. **Revenue Streams**
   - Transaction fees (primary)
   - Subscription fees (seller SaaS)
   - Advertising revenue
   - Fulfillment/logistics fees
   - Premium placement fees
   - Data/analytics fees

**Deliverable:** Marketplace revenue model with GMV and take rate projections

### Workflow 3: Usage-Based Revenue Model

**Objective:** Model revenue for consumption-based pricing

**Steps:**
1. **Usage Metrics Identification**
   - Primary usage unit (API calls, storage, compute hours)
   - Average usage per customer
   - Usage distribution (heavy vs. light users)
   - Seasonal patterns

2. **Pricing Structure**
   - Per-unit pricing tiers
   - Volume discounts
   - Minimum commitments
   - Overage pricing
   - Platform fees

3. **Customer Segmentation**
   - Segment by usage level
   - Different growth rates by segment
   - Segment-specific retention
   - Enterprise vs. SMB patterns

4. **Model Components**
   ```
   Revenue = Σ (Customers per segment × Usage per customer × Price per unit)

   Account for:
   - Customer growth
   - Usage growth per customer
   - Price changes
   - Volume discount impact
   ```

5. **Predictability Enhancement**
   - Committed vs. overage revenue
   - Minimum revenue guarantees
   - Prepaid usage credits
   - Annual contract values

6. **Scenario Modeling**
   - Usage growth scenarios
   - Customer mix changes
   - Pricing optimization
   - Enterprise contract impact

**Deliverable:** Usage-based revenue model with consumption projections

### Workflow 4: Multi-Product Revenue Model

**Objective:** Model revenue across multiple products and revenue streams

**Steps:**
1. **Product Portfolio Mapping**
   - Product 1: Type, pricing, target market
   - Product 2: Type, pricing, target market
   - Product 3: Type, pricing, target market
   - Cross-sell relationships

2. **Individual Product Models**
   - Build sub-model for each product
   - Apply appropriate methodology:
     - Subscription → SaaS model
     - Transaction → Marketplace model
     - Usage → Consumption model
     - One-time → Pipeline model

3. **Cross-Sell Modeling**
   - Attach rate assumptions
   - Timing of cross-sell
   - Bundle discount impact
   - Cannibalization effects

4. **Revenue Mix Analysis**
   - Current revenue mix
   - Target revenue mix
   - Mix shift assumptions
   - Profitability by product

5. **Consolidation**
   - Sum of product revenues
   - Eliminate double-counting
   - Bundle revenue allocation
   - Total company revenue

6. **Scenario Development**
   - Product-specific scenarios
   - Portfolio-level scenarios
   - New product launch impact
   - Sunset product impact

**Deliverable:** Consolidated multi-product revenue model

### Workflow 5: Pricing Optimization Model

**Objective:** Analyze and optimize pricing strategy

**Steps:**
1. **Current Pricing Analysis**
   - Current price points
   - Discount frequency and depth
   - ARPU analysis
   - Price sensitivity observed

2. **Competitive Benchmarking**
   - Competitor pricing
   - Feature comparison
   - Value-based positioning
   - Market standard pricing

3. **Value-Based Pricing Analysis**
   - Customer value delivered
   - ROI for customer
   - Willingness to pay research
   - Price anchoring opportunities

4. **Price Elasticity Modeling**
   - Historical price change impact
   - Segment-specific elasticity
   - Volume vs. price trade-off
   - Revenue optimization point

5. **Pricing Scenarios**
   - Price increase impact:
     - Revenue gain from price
     - Volume loss from churn
     - Net revenue impact

   - Price decrease impact:
     - Revenue loss from price
     - Volume gain from conversion
     - Net revenue impact

6. **Pricing Structure Options**
   - Per-seat vs. per-company
   - Usage-based vs. flat
   - Tiered pricing design
   - Freemium conversion
   - Annual discount strategy

7. **Implementation Plan**
   - Grandfathering strategy
   - Rollout timeline
   - Customer communication
   - Monitoring metrics

**Deliverable:** Pricing analysis with optimization recommendations

## Quick Reference

| Action | Command/Trigger |
|--------|-----------------|
| SaaS model | "Build MRR/ARR revenue model" |
| Marketplace | "Model marketplace GMV and revenue" |
| Usage-based | "Create consumption-based revenue model" |
| Multi-product | "Model revenue across products" |
| Pricing | "Analyze pricing optimization" |
| Scenarios | "Model revenue scenarios" |

## SaaS Metrics Reference

### Core Metrics

| Metric | Formula | Healthy Benchmark |
|--------|---------|-------------------|
| MRR | Sum of monthly recurring revenue | Growing |
| ARR | MRR × 12 | Growing |
| ARPU | MRR / Customers | Stable or growing |
| Net Revenue Retention | (Start MRR + Expansion - Contraction - Churn) / Start MRR | > 100% |
| Gross Revenue Retention | (Start MRR - Contraction - Churn) / Start MRR | > 85% |
| LTV | ARPU × Gross Margin / Churn Rate | > 3× CAC |
| CAC Payback | CAC / (ARPU × Gross Margin) | < 12 months |

### MRR Movement Types

| Type | Definition |
|------|------------|
| New MRR | Revenue from new customers this month |
| Expansion MRR | Revenue increase from existing customers (upsells) |
| Contraction MRR | Revenue decrease from existing customers (downgrades) |
| Churned MRR | Revenue from customers who cancelled |
| Reactivation MRR | Revenue from customers who returned |

### SaaS Benchmarks

| Metric | Good | Great | Best-in-Class |
|--------|------|-------|---------------|
| MRR Growth (MoM) | 5-7% | 10-15% | 20%+ |
| Net Revenue Retention | 100-110% | 110-130% | 130%+ |
| Gross Churn (monthly) | 3-5% | 1-3% | < 1% |
| LTV/CAC | 3:1 | 5:1 | 10:1 |
| CAC Payback | 12-18 mo | 6-12 mo | < 6 mo |

## Revenue Model Template

```markdown
# Revenue Model: [Company Name]

**Model Period:** [Start] - [End]
**Last Updated:** [Date]

## Model Inputs

### Customer Assumptions
| Metric | Current | Growth Rate |
|--------|---------|-------------|
| Starting Customers | | |
| New Customers/Month | | |
| Churn Rate (Monthly) | | |
| Net Revenue Retention | | |

### Pricing Assumptions
| Segment | ARPU | % of New |
|---------|------|----------|
| Starter | | |
| Professional | | |
| Enterprise | | |
| Weighted Avg | | |

## Revenue Projections

### Monthly MRR Waterfall
| Month | Start MRR | New | Expansion | Contraction | Churn | End MRR |
|-------|-----------|-----|-----------|-------------|-------|---------|
| M1 | | | | | | |
| M2 | | | | | | |
| ... | | | | | | |
| M12 | | | | | | |

### Annual Summary
| Metric | Year 1 | Year 2 | Year 3 |
|--------|--------|--------|--------|
| ARR | | | |
| YoY Growth | | | |
| Customers | | | |
| ARPU | | | |
| NRR | | | |

## Scenario Comparison
| Scenario | Year 1 ARR | Year 2 ARR | Year 3 ARR |
|----------|------------|------------|------------|
| Base | | | |
| Upside | | | |
| Downside | | | |

## Key Assumptions & Risks
1. [Assumption 1] - [Risk if wrong]
2. [Assumption 2] - [Risk if wrong]
```

## Best Practices

### Model Building
- Start with driver-based approach
- Document all assumptions
- Make assumptions adjustable
- Build scenario capability
- Test edge cases

### Assumption Setting
- Ground in historical data
- Benchmark to industry
- Be realistic, not optimistic
- Explain reasoning
- Sensitivity test key drivers

### Presentation
- Executive summary first
- Visualize key trends
- Show assumption sensitivity
- Include scenario comparison
- Highlight risks

## Integration with Other Skills

- **Use with `budget-planner`:** Link revenue to expense budget
- **Use with `cash-flow-forecaster`:** Convert revenue to cash
- **Use with `unit-economics-calculator`:** Validate profitability
- **Use with `financial-analyst`:** Historical performance analysis
- **Use with `investment-analyzer`:** Support fundraising projections

## Common Pitfalls to Avoid

- **Hockey stick projections:** Ground in reality
- **Ignoring churn:** Even small churn compounds
- **Overestimating new customers:** Harder than it looks
- **Ignoring seasonality:** Build in monthly patterns
- **Linear assumptions:** Growth often S-curve
- **Ignoring capacity constraints:** Sales, product, support
- **Static pricing:** Build in price evolution
- **No segmentation:** Different customers behave differently
