# Finance & Metrics

Compressed reference for SaaS finance: 32 metrics with formulas and benchmarks, diagnostic frameworks, and decision logic for feature investment, channel evaluation, and pricing changes.

## SaaS Revenue & Growth Metrics

### Core Revenue Metrics

| Metric | Formula | Benchmarks |
|--------|---------|------------|
| **Revenue** | Sum of all customer payments in period | Growth rate >20% YoY (varies by stage) |
| **ARPU** | Total Revenue / Total Users | B2C: $5-50/mo; B2B: $50-500+/mo; track trend |
| **ARPA** | MRR / Active Accounts | SMB: $100-$1K/mo; Mid: $1K-$10K; Ent: $10K+ |
| **ACV** | Annual Recurring Revenue per Contract (exclude one-time fees) | SMB: $5K-$25K; Mid: $25K-$100K; Ent: $100K+ |
| **MRR/ARR** | MRR = sum of recurring subs; ARR = MRR x 12 | Track components: New + Expansion - Churned - Contraction |
| **Gross vs Net Revenue** | Net = Gross - Discounts - Refunds - Credits | Refunds >10% = product problem; Discounts >20% = pricing power problem |

**ARPA/ARPU combined analysis:** Average Seats per Account = ARPA / ARPU. High ARPA + low ARPU = undermonetized seats. Low ARPA + high ARPU = small deal sizes.

### Retention & Expansion Metrics

| Metric | Formula | Benchmarks |
|--------|---------|------------|
| **Churn Rate (Logo)** | Customers Lost / Starting Customers | Monthly: <2% great, 2-5% ok, >5% crisis |
| **Churn Rate (Revenue)** | MRR Lost / Starting MRR | Annual: <10% great, 10-30% ok, >30% crisis |
| **NRR** | (Start ARR + Expansion - Churn - Contraction) / Start ARR x 100 | >120% excellent; 100-120% good; <90% problem |
| **Expansion Revenue** | Upsells + Cross-sells + Usage Growth | Should be 20-30% of total revenue |
| **Quick Ratio** | (New MRR + Expansion MRR) / (Churned MRR + Contraction MRR) | >4 excellent; 2-4 healthy; <2 leaky bucket |

**Churn compounding:** 3% monthly != 36% annual. Use `Annual Churn = 1 - (1 - Monthly)^12`. 3% monthly = ~31% annual. 5% monthly = ~46% annual.

### Analysis Frameworks

**Revenue Mix:** Product/Segment Revenue / Total Revenue x 100. No single product >60% ideal. Top customer <10% revenue; top 10 <40%.

**Cohort Analysis:** Group customers by join date, track retention/expansion over time. Recent cohorts should perform same or better than older ones. If newer cohorts degrade, PMF is eroding -- stop scaling, fix product.

## Unit Economics & Efficiency

### Customer-Level Profitability

| Metric | Formula | Benchmarks |
|--------|---------|------------|
| **Gross Margin** | (Revenue - COGS) / Revenue x 100 | SaaS: 70-85% good; <60% concerning |
| **CAC** | Total S&M Spend / New Customers Acquired | Enterprise: $10K+ ok; SMB: <$500 target |
| **LTV (simple)** | ARPU x Avg Customer Lifetime (months) | Must be 3x+ CAC |
| **LTV (better)** | ARPU x Gross Margin % / Monthly Churn Rate | Use this for decisions |
| **LTV:CAC** | LTV / CAC | <1:1 unsustainable; 1-3:1 marginal; 3-5:1 healthy; >5:1 underinvesting |
| **Payback Period** | CAC / (Monthly ARPU x Gross Margin %) | <12mo great; 12-18 ok; >24 concerning |
| **Contribution Margin** | (Revenue - All Variable Costs) / Revenue x 100 | 60-80% good; <40% concerning |
| **Gross Margin Payback** | CAC / (Monthly ARPU x Gross Margin %) | Same formula as Payback above; use this version |

**COGS includes:** Hosting, infrastructure, payment processing, customer onboarding costs.
**Variable costs include:** COGS + support + payment processing + variable customer success.

**Critical insight:** 4:1 LTV:CAC with 36-month payback is a cash trap. 3:1 LTV:CAC with 8-month payback is better for growth.

### Capital Efficiency

| Metric | Formula | Benchmarks |
|--------|---------|------------|
| **Burn Rate (Gross)** | Total Monthly Cash Spent | Context-dependent |
| **Burn Rate (Net)** | Monthly Cash Spent - Monthly Revenue | Early <$200K manageable; >$500K needs revenue path |
| **Runway** | Cash Balance / Monthly Net Burn | 12+ good; 6-12 ok; <6 crisis. Raise at 6-9 months, not 3 |
| **OpEx** | S&M + R&D + G&A | Should grow slower than revenue |
| **Net Income** | Revenue - COGS - OpEx | Early negative ok; mature 10-20%+ margin |

**Working capital:** Annual contracts paid upfront boost cash. Monthly billing delays collection. Cash-based runway != revenue-based runway.

### Efficiency Ratios

| Metric | Formula | Benchmarks |
|--------|---------|------------|
| **Rule of 40** | Revenue Growth % + Profit Margin % | >40 healthy; 25-40 ok; <25 concerning |
| **Magic Number** | (Q Revenue - Prev Q Revenue) x 4 / Prev Q S&M Spend | >0.75 scale; 0.5-0.75 optimize; <0.5 fix GTM |
| **Operating Leverage** | Revenue Growth Rate vs OpEx Growth Rate | Revenue growth must exceed OpEx growth |

**Rule of 40 by stage:** Early = 60% growth + (-20%) margin = 40. Growth = 40% + 5% = 45. Mature = 20% + 25% = 45.

## Business Health Diagnostic

### Four-Dimension Framework

1. **Growth & Retention** -- Revenue growth, NRR, churn, Quick Ratio
2. **Unit Economics** -- CAC, LTV, LTV:CAC, payback, gross margin
3. **Capital Efficiency** -- Burn, runway, Rule of 40, Magic Number
4. **Strategic Position** -- Market pricing, moat, concentration, leverage

### Stage-Specific Benchmarks

| Metric | Early (<$10M ARR) | Growth ($10-50M) | Scale ($50M+) |
|--------|-------------------|-------------------|---------------|
| Growth YoY | >50% | >40% | >25% |
| LTV:CAC | >3:1 | -- | -- |
| NRR | -- | >100% | >110% |
| Gross Margin | >70% | -- | -- |
| Rule of 40 | -- | >40 | >40 |
| Magic Number | -- | >0.75 | -- |
| Profit Margin | negative ok | -- | >10% |
| Runway | >12 months | -- | positive cash flow |

### Red Flag Severity

**Critical (fix immediately):** Runway <6mo, LTV:CAC <1.5:1, churn accelerating cohort-over-cohort, NRR <90%, Magic Number <0.3.

**High priority (fix within quarter):** Rule of 40 <25, payback >24mo, Quick Ratio <2, gross margin <60%, revenue concentration >50% in top 10.

**Medium priority (address within 6 months):** NRR 90-100%, Magic Number 0.3-0.5, negative operating leverage, stable but high churn (>5% monthly).

### Diagnostic Scoring

- **Healthy:** All dimensions at/above stage benchmarks, no critical flags, improving trends. Action: scale aggressively.
- **Moderate:** 1-2 dimensions need attention, medium-priority flags. Action: fix specific issues before scaling further.
- **Concerning:** Multiple critical flags, 2+ dimensions problematic. Action: urgent intervention -- stop scaling, fix retention and unit economics.
- **Critical:** Runway <3mo or LTV:CAC <1:1. Action: survival mode -- emergency fundraise or cut burn 50%+.

## Feature Investment Analysis

### Revenue Connection Types

1. **Direct monetization** -- new tier, paid add-on, usage fee. Calculate: Customer Base x Adoption Rate x Price.
2. **Retention improvement** -- addresses churn reason. Calculate: LTV Impact = Lifetime Increase x Base x ARPU x Margin.
3. **Conversion improvement** -- trial-to-paid lift. Calculate: Trial Users x Conversion Lift x ARPU.
4. **Expansion enabler** -- upsell/cross-sell path. Calculate: Base x Expansion Rate x ARPU Increase.

### ROI Thresholds

| Scenario | Build if | Don't build if |
|----------|----------|----------------|
| Direct monetization | ROI >3x year one | Negative contribution margin in downside case |
| Retention feature | LTV impact >10x dev cost | Payback exceeds avg customer lifetime |
| Strategic override | Competitive moat, platform enabler, compliance | "Strategic" without clear definition |

### Cost Structure Check

- One-time: development cost (team size x time)
- Ongoing: COGS impact (hosting, infra) + OpEx (support, maintenance)
- Margin impact: if COGS >20% of projected revenue, flag margin dilution
- Contribution margin: (Revenue - COGS) / Revenue must stay positive

### Decision Patterns

**Build now:** ROI >3:1 (direct) or LTV impact >10:1 (retention), positive contribution margin, payback < customer lifetime.

**Build for strategic reasons:** ROI <2:1 but competitive moat, platform enabler, or compliance. Cap investment, monitor adoption, re-evaluate at 6 months.

**Don't build:** ROI <1:1, negative contribution margin, no strategic value. Consider reducing scope or changing monetization.

**Build later:** High uncertainty in adoption or impact assumptions. Validate with surveys, prototypes, churn interviews first.

## Channel Economics

### Channel Evaluation Framework

Evaluate each channel on four dimensions:

1. **Unit economics** -- CAC, LTV, LTV:CAC, payback (per channel, not blended)
2. **Customer quality** -- cohort retention, churn rate, NRR, ICP fit (per channel)
3. **Scalability** -- Magic Number, addressable volume, CAC trend
4. **Strategic fit** -- segment match, sales motion compatibility

### Channel Decision Matrix

| LTV:CAC | Payback | Customer Quality | Scalability | Decision |
|---------|---------|------------------|-------------|----------|
| >3:1 | <12mo | Good retention | High volume | **Scale aggressively** |
| 2-3:1 | 12-18mo | Average retention | Medium | **Test & optimize** |
| <2:1 | >18mo | Poor retention | Low | **Kill or fix** |

### Scale Criteria

Scale when ALL met: LTV:CAC >3:1 AND payback <12mo AND Magic Number >0.75 AND customer quality >= blended. Increase budget 50-100%, monitor weekly for CAC increase >20% (saturation signal).

### Optimize Playbook

- **If CAC too high:** Improve conversion rate, reduce cost-per-click, shorten sales cycle.
- **If LTV too low:** Improve onboarding for channel cohort, target higher-value segments, add expansion plays.
- **If targeting off:** Narrow audience, improve messaging, add qualification step.
- Timeline: 4-8 weeks. Target LTV:CAC >3:1, payback <12mo. If unachievable, kill.

### Kill Criteria

LTV:CAC <1.5:1 with no clear improvement path. Reallocate budget to top-performing channel. Exception: strategic channels (enterprise field sales) get capped spend and 6-12 month runway to prove out.

### Incrementality

Test with holdout groups. Only count truly incremental conversions. Retargeting campaigns often claim credit for conversions that would have happened organically.

## Pricing Analysis

### Pricing Change Types

- **Price increase** -- new customers only (grandfather existing) vs all customers
- **New premium tier** -- upsell path, watch cannibalization
- **Paid add-on** -- monetize feature; assess retention risk if previously free
- **Usage-based** -- charge per unit (seats, API calls, storage); enables expansion revenue
- **Discount strategy** -- annual prepay (cash flow), volume (larger deals), promotional (urgency)
- **Packaging change** -- rebundle features, change pricing metric

### Five-Dimension Impact Assessment

1. **Revenue:** ARPU lift = (New ARPU - Current ARPU) / Current ARPU. Expected MRR increase = Base x ARPU Lift.
2. **Conversion:** Higher prices may reduce trial-to-paid. Model conversion drop and its effect on new customer volume.
3. **Churn:** Model scenarios -- conservative (+2pp churn), base (+1pp), optimistic (+0). Churn-driven MRR loss = additional churn % x base x new ARPU.
4. **Expansion:** Does change create upsell path? Usage-based pricing enables natural expansion as customers grow.
5. **CAC Payback:** Higher ARPU = faster payback, but lower conversion = higher effective CAC. Calculate net effect.

### Decision Patterns

**Implement broadly:** Net revenue clearly positive (>10% ARPU lift, <5% churn risk), minimal conversion impact. Grandfather existing customers.

**Test first (A/B):** Uncertain impact, moderate risk. Test 60-90 days with 100+ customers per cohort. Roll out if conversion stays within acceptable range.

**Modify approach:** Original proposal too risky. Options: smaller increase, grandfather existing, segment-based pricing (raise enterprise only).

**Don't change:** Churn-driven loss exceeds revenue gains, or high competitive pressure. Focus on retention/expansion instead.

### Annual Discount Guardrails

Limit to 10-15% for annual prepay. 30% annual discounts destroy LTV. Balance cash flow improvement with revenue protection.

## Quality Gates

### Vanity Metric Traps

- **Revenue without margin:** $1M at 80% margin >> $2M at 20% margin
- **ARPU growth from mix shift:** ARPU rose because small customers churned, not because monetization improved
- **Signups without conversion:** 10,000 signups at 5% conversion = 500 customers. Calculate CAC on paid, not signups
- **Engagement without revenue:** Feature increases engagement but not retention or monetization -- not a business outcome
- **Gross revenue hiding net contraction:** Track discounts and refunds; gross up 20% but discounts doubled = flat net

### Blended Metric Dangers

Never use blended averages for decisions. Always segment by:
- **Channel:** One channel at $10K CAC hides in $500 blended CAC
- **Segment:** $100 ARPU blends $10 SMB and $1,000 enterprise -- useless for decisions
- **Cohort:** Blended 3% churn hides newer cohorts at 6% and old cohorts at 1%
- **Product:** 67% legacy product dying at -5% growth masked by 33% new product at +80%

### Common Calculation Errors

- **LTV without margin:** Use `ARPU x Margin % / Churn`, not `ARPU x Lifetime`
- **Churn multiply-by-12:** Churn compounds. 3% monthly = 31% annual, not 36%
- **Payback without margin:** Use gross margin payback, not revenue payback
- **CAC comparison without payback:** $5K CAC with 24mo payback is worse than $8K CAC with 8mo payback
- **Rule of 40 without runway:** Score of 50 means nothing with 3 months runway
- **LTV:CAC without payback:** 6:1 ratio with 48-month payback is a cash trap

### Decision-Making Anti-Patterns

- Scaling acquisition when Quick Ratio <2 (leaky bucket)
- Raising prices without modeling churn scenarios
- Celebrating NRR >100% from low churn alone (not expansion-driven)
- Using "strategic" as catch-all for building low-ROI features
- Fixing everything simultaneously instead of prioritizing top 1-3 issues
- Killing channels before 3-6 months and 100+ customers of data
- Over-relying on one channel (>50% of acquisition)
- Annual discounts >15% that destroy LTV for short-term cash
- Testing pricing on 10 customers (need 100+ per cohort for significance)
- Celebrating feature requests from 0.5% of base while ignoring the other 99.5%

---

## Interaction Rules (Coaching Mode)

When coaching is active for finance and metrics topics, use these rules.

| Trigger | Action | Stop When |
|---------|--------|-----------|
| User provides metrics without context (just numbers, no baseline or trend) | Push: "What was this number 3 months ago? Is it improving or declining?" | User provides trend direction and baseline |
| Churn is discussed without cohort breakdown | Challenge: "Overall churn hides the story. What does churn look like by signup month, plan tier, or acquisition channel?" | User segments the data or acknowledges the gap |
| LTV:CAC ratio presented without payback period | Push: "LTV:CAC tells you the return. Payback tells you the cash risk. What's your payback period?" | User calculates or estimates payback |
| User wants to scale acquisition with churn above 5% monthly | Challenge: "You're filling a leaky bucket. At 5%+ monthly churn, every new customer you acquire has a 46% chance of leaving within a year. Fix retention first." | User addresses retention or explains why scaling is justified |
| Feature ROI is estimated without opportunity cost | Push: "What are you NOT building to build this? What's the cost of that delay?" | User names the tradeoff explicitly |
| User has answered 2 follow-ups on the same point | Stop pushing. Summarize what's still weak and give best-guess output. | -- |
