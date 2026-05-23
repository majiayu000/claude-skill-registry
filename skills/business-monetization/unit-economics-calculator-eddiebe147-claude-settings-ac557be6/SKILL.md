---
name: Unit Economics Calculator
slug: unit-economics-calculator
description: Calculate and optimize unit economics including CAC, LTV, payback periods, and contribution margins
category: finance
complexity: moderate
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "unit economics"
  - "CAC calculation"
  - "LTV calculation"
  - "payback period"
  - "contribution margin"
  - "customer profitability"
tags:
  - unit-economics
  - cac
  - ltv
  - saas-metrics
  - profitability
---

# Unit Economics Calculator

Expert unit economics analysis agent that calculates customer acquisition costs, lifetime value, payback periods, and contribution margins. Specializes in SaaS unit economics, e-commerce profitability, and margin optimization.

This skill applies rigorous unit economics frameworks to understand business profitability at the individual customer or transaction level. Perfect for evaluating business viability, optimizing marketing spend, and making pricing decisions.

## Core Workflows

### Workflow 1: SaaS Unit Economics Analysis

**Objective:** Calculate complete SaaS unit economics package

**Steps:**
1. **Customer Acquisition Cost (CAC)**
   - **Fully Loaded CAC:**
     ```
     CAC = (Sales & Marketing Spend) / (New Customers Acquired)

     Include:
     - Advertising spend
     - Marketing team salaries
     - Sales team salaries
     - Sales tools and software
     - Events and conferences
     - Content creation costs
     - Agency fees
     ```

   - **Blended vs. Paid CAC:**
     - Blended CAC: All customers / All S&M spend
     - Paid CAC: Paid acquired customers / Paid marketing spend
     - Organic CAC: Organic customers / Organic costs

   - **CAC by Channel:**
     | Channel | Spend | Customers | CAC |
     |---------|-------|-----------|-----|
     | Paid Search | | | |
     | Paid Social | | | |
     | Content/SEO | | | |
     | Sales Outbound | | | |
     | Referrals | | | |

2. **Lifetime Value (LTV)**
   - **Simple LTV:**
     ```
     LTV = ARPU × Gross Margin × Customer Lifetime

     Customer Lifetime = 1 / Churn Rate
     ```

   - **LTV with Expansion:**
     ```
     LTV = ARPU × Gross Margin / (Churn Rate - Expansion Rate)
     ```

   - **Cohort-Based LTV:**
     - Track actual revenue per cohort over time
     - More accurate but requires historical data
     - Account for degradation curves

3. **LTV/CAC Ratio**
   - **Calculation:**
     ```
     LTV/CAC = Lifetime Value / Customer Acquisition Cost
     ```

   - **Benchmarks:**
     | Ratio | Interpretation |
     |-------|----------------|
     | < 1:1 | Losing money on customers |
     | 1:1 - 3:1 | Underinvesting in growth |
     | 3:1 - 5:1 | Healthy, efficient |
     | > 5:1 | Could invest more in growth |

4. **CAC Payback Period**
   - **Calculation:**
     ```
     Payback (months) = CAC / (Monthly Revenue × Gross Margin)
     ```

   - **Benchmarks:**
     | Segment | Target Payback |
     |---------|----------------|
     | SMB | < 12 months |
     | Mid-Market | < 18 months |
     | Enterprise | < 24 months |

5. **Contribution Margin**
   - **Gross Margin per Customer:**
     ```
     Gross Margin = Revenue - COGS
     Gross Margin % = (Revenue - COGS) / Revenue
     ```

   - **Contribution Margin (after CAC):**
     ```
     CM = LTV - CAC
     CM Ratio = (LTV - CAC) / LTV
     ```

**Deliverable:** Complete SaaS unit economics dashboard

### Workflow 2: E-Commerce Unit Economics

**Objective:** Calculate per-order and per-customer economics

**Steps:**
1. **Per-Order Economics**
   - **Average Order Value (AOV):**
     ```
     AOV = Total Revenue / Number of Orders
     ```

   - **Cost of Goods Sold (COGS):**
     - Product cost
     - Packaging
     - Inbound freight
     - Warehousing allocation

   - **Variable Costs:**
     - Payment processing (2-3%)
     - Outbound shipping
     - Returns/refunds
     - Customer service allocation

   - **Contribution Margin per Order:**
     ```
     CM = AOV - COGS - Variable Costs
     CM % = CM / AOV
     ```

2. **Customer Acquisition Cost**
   ```
   CAC = Marketing Spend / New Customers

   Channel-specific:
   - Paid: Direct spend / Attributed customers
   - Organic: Content + SEO costs / Organic customers
   ```

3. **Customer Lifetime Value**
   - **Repeat Purchase Analysis:**
     ```
     Orders per Customer = Total Orders / Unique Customers
     Purchase Frequency = Orders per Year
     Customer Lifetime = 1 / Annual Churn

     LTV = AOV × Orders per Year × Customer Lifetime × CM %
     ```

   - **Cohort-Based LTV:**
     - Track actual spend by acquisition cohort
     - 12, 24, 36 month LTV by cohort

4. **Return and Refund Impact**
   ```
   Return Rate = Returns / Orders
   Net AOV = AOV × (1 - Return Rate)
   Return Cost = Shipping + Restocking + Lost Product Value
   ```

5. **Break-Even Analysis**
   ```
   Break-Even Orders = CAC / CM per Order
   Break-Even Time = Break-Even Orders / Orders per Year
   ```

**Deliverable:** E-commerce unit economics model

### Workflow 3: Marketplace Unit Economics

**Objective:** Calculate take economics for marketplace businesses

**Steps:**
1. **Transaction Economics**
   - **Gross Merchandise Value (GMV):**
     ```
     GMV = Number of Transactions × Average Transaction Value
     ```

   - **Take Rate:**
     ```
     Take Rate = Net Revenue / GMV
     Typical ranges: 10-30% depending on category
     ```

   - **Net Revenue per Transaction:**
     ```
     Net Revenue = GMV × Take Rate
     ```

2. **Cost per Transaction**
   - Payment processing (2-3%)
   - Fraud/chargebacks
   - Customer support allocation
   - Platform costs allocation
   - Trust and safety

3. **Contribution Margin per Transaction**
   ```
   CM = Net Revenue - Variable Costs per Transaction
   CM % = CM / GMV
   ```

4. **Buyer/Seller Economics**
   - **Buyer CAC:**
     - Acquisition cost
     - Transactions per buyer
     - Buyer LTV

   - **Seller CAC:**
     - Onboarding cost
     - GMV per seller
     - Seller LTV

5. **Liquidity Economics**
   ```
   Match Rate = Successful Transactions / Total Demand
   Higher liquidity → Lower CAC → Better unit economics
   ```

**Deliverable:** Marketplace unit economics framework

### Workflow 4: Subscription Box Unit Economics

**Objective:** Calculate unit economics for subscription box businesses

**Steps:**
1. **Box Economics**
   - **Price per Box:**
     - Monthly subscription price
     - Discounts for prepay (quarterly, annual)
     - Effective monthly revenue

   - **Cost per Box:**
     - Product costs (target 30-40% of price)
     - Packaging materials
     - Fulfillment labor
     - Outbound shipping
     - Payment processing
     - Returns/replacements

2. **Variable Costs**
   ```
   Variable Cost per Box = Products + Packaging + Shipping + Processing
   Contribution per Box = Price - Variable Costs
   Contribution Margin % = Contribution / Price
   ```

3. **Customer Metrics**
   - **Subscriber Lifetime:**
     ```
     Lifetime (months) = 1 / Monthly Churn Rate
     Example: 5% churn = 20 month lifetime
     ```

   - **LTV:**
     ```
     LTV = Contribution per Box × Lifetime (months)
     ```

4. **Acquisition Economics**
   - **CAC Components:**
     - Paid media
     - Influencer costs
     - Trial/free box costs
     - Referral incentives

   - **First Box Profitability:**
     ```
     First Box P&L = Revenue - COGS - CAC
     Many subscription boxes lose money on first box
     ```

5. **Break-Even Analysis**
   ```
   Break-Even Month = CAC / Contribution per Box
   Must retain past break-even to be profitable
   ```

**Deliverable:** Subscription box unit economics model

### Workflow 5: Unit Economics Optimization

**Objective:** Identify and implement unit economics improvements

**Steps:**
1. **Current State Assessment**
   - Calculate current LTV, CAC, LTV/CAC
   - Identify weakest metrics
   - Benchmark vs. best-in-class

2. **CAC Reduction Levers**
   - **Channel Optimization:**
     - Cut underperforming channels
     - Double down on efficient channels
     - Improve conversion rates

   - **Efficiency Improvements:**
     - Sales productivity
     - Marketing automation
     - Better targeting
     - Lower CPM/CPC negotiation

   - **Organic Growth:**
     - Referral programs
     - Content marketing
     - SEO investment
     - Product-led growth

3. **LTV Improvement Levers**
   - **Reduce Churn:**
     - Improve onboarding
     - Better customer success
     - Product improvements
     - Save/retention programs

   - **Increase ARPU:**
     - Price increases
     - Upsell motions
     - Cross-sell products
     - Premium tiers

   - **Improve Margins:**
     - COGS reduction
     - Pricing optimization
     - Efficiency gains

4. **Impact Modeling**
   | Lever | Current | Target | Impact on LTV/CAC |
   |-------|---------|--------|-------------------|
   | Reduce CAC 20% | | | |
   | Reduce Churn 20% | | | |
   | Increase ARPU 15% | | | |
   | Improve Margin 5pp | | | |

5. **Prioritized Action Plan**
   - Quick wins (30 days)
   - Medium-term (90 days)
   - Long-term initiatives (12 months)
   - Expected improvement trajectory

**Deliverable:** Unit economics optimization plan with projected improvements

## Quick Reference

| Action | Command/Trigger |
|--------|-----------------|
| Calculate CAC | "Calculate customer acquisition cost" |
| Calculate LTV | "Calculate customer lifetime value" |
| LTV/CAC analysis | "Analyze unit economics" |
| Payback period | "Calculate CAC payback period" |
| Contribution margin | "Calculate contribution margin" |
| Optimize | "How do I improve unit economics?" |

## Unit Economics Formulas

### Customer Acquisition

| Metric | Formula |
|--------|---------|
| CAC | Total S&M Spend / New Customers |
| Blended CAC | All S&M / All New Customers |
| Paid CAC | Paid Spend / Paid Customers |
| Channel CAC | Channel Spend / Channel Customers |

### Customer Value

| Metric | Formula |
|--------|---------|
| LTV (simple) | ARPU × Gross Margin / Churn |
| LTV (with expansion) | ARPU × GM / (Churn - Expansion) |
| Customer Lifetime | 1 / Churn Rate |
| ARPU | Revenue / Customers |

### Efficiency Metrics

| Metric | Formula | Benchmark |
|--------|---------|-----------|
| LTV/CAC | LTV / CAC | > 3:1 |
| CAC Payback | CAC / (Monthly Rev × GM) | < 12 mo |
| Magic Number | Net New ARR / Prior Q S&M | > 0.75 |
| Burn Multiple | Net Burn / Net New ARR | < 2 |

### Margin Metrics

| Metric | Formula |
|--------|---------|
| Gross Margin | (Revenue - COGS) / Revenue |
| Contribution Margin | (Revenue - COGS - Variable Costs) / Revenue |
| Net Margin | Net Income / Revenue |

## Unit Economics Dashboard Template

```markdown
# Unit Economics Dashboard: [Company]
**Period:** [Date Range]

## Customer Acquisition
| Metric | Value | Benchmark | Status |
|--------|-------|-----------|--------|
| Blended CAC | $ | $ | |
| Paid CAC | $ | $ | |
| Organic CAC | $ | $ | |
| S&M as % of Revenue | % | % | |

## Customer Value
| Metric | Value | Benchmark | Status |
|--------|-------|-----------|--------|
| ARPU | $ | $ | |
| Gross Margin | % | % | |
| LTV | $ | $ | |
| Customer Lifetime | mo | mo | |

## Efficiency
| Metric | Value | Benchmark | Status |
|--------|-------|-----------|--------|
| LTV/CAC | :1 | 3:1+ | |
| CAC Payback | mo | <12 mo | |
| Magic Number | | >0.75 | |

## Trends
| Metric | Last Q | This Q | Change |
|--------|--------|--------|--------|
| CAC | | | |
| LTV | | | |
| LTV/CAC | | | |
| Payback | | | |

## Action Items
1. [Priority 1]
2. [Priority 2]
3. [Priority 3]
```

## Best Practices

### Calculation
- Use consistent time periods
- Include all relevant costs in CAC
- Account for expansion in LTV
- Segment by customer type
- Track trends over time

### Benchmarking
- Compare to industry standards
- Track improvement over time
- Adjust for business model differences
- Consider stage of company

### Optimization
- Focus on biggest leverage points
- Test changes carefully
- Monitor for unintended effects
- Balance growth and efficiency

## Integration with Other Skills

- **Use with `revenue-modeler`:** Validate revenue assumptions
- **Use with `cash-flow-forecaster`:** Model CAC payback impact
- **Use with `budget-planner`:** Inform marketing budget
- **Use with `investment-analyzer`:** Support investor metrics
- **Use with `financial-analyst`:** Deep-dive profitability

## Common Pitfalls to Avoid

- **Incomplete CAC:** Missing costs understates true CAC
- **Overstated LTV:** Optimistic churn assumptions
- **Ignoring cohort degradation:** LTV changes over time
- **Channel mixing:** Blended CAC hides inefficiencies
- **Ignoring payback:** LTV/CAC without cash timing
- **No segmentation:** Different segments have different economics
- **Static analysis:** Unit economics change over time
- **Ignoring CAC payback timing:** Cash flow matters
