---
name: revenue-recognition
description: 'name: revenue-recognition'
---

# Revenue Recognition

name: revenue-recognition
description: Revenue recognition — IFRS 15 five-step model, ASC 606

## When to Activate

- User needs to apply the five-step revenue recognition model
- Identifying performance obligations in complex contracts (bundled, multi-element)
- Determining standalone selling prices and allocating transaction price
- Evaluating principal vs agent considerations
- Accounting for SaaS, licensing, construction, or subscription revenue
- Assessing variable consideration constraints

## Core Concepts

### The Five-Step Model (IFRS 15 / ASC 606)

Both standards follow an identical framework. This skill covers both, noting differences where they exist.

### Step 1: Identify the Contract

**A contract exists when ALL of the following are met:**
- Both parties have approved the contract (written, oral, or implied by business practice)
- Each party's rights are identifiable
- Payment terms are identifiable
- The contract has commercial substance (future cash flows change)
- Collection is probable (IFRS: probable = more likely than not; US GAAP: similar threshold)

**Contract modifications:**
- Treated as a separate contract if: scope increases by distinct goods/services AND price increases by SSP
- Otherwise: prospective adjustment (reallocate remaining consideration) or cumulative catch-up

**Contract combinations:**
- Combine contracts if negotiated as a package, consideration depends on other contract, or goods/services form a single PO

### Step 2: Identify Performance Obligations

A performance obligation is a promise to transfer a distinct good or service (or a series of distinct goods/services that are substantially the same and transferred with the same pattern).

**Distinctness test (both criteria must be met):**
1. **Capable of being distinct:** Customer can benefit from the good/service on its own or with readily available resources
2. **Distinct within the contract:** The promise is separately identifiable from other promises (not highly interrelated, not significantly modified/customized, not highly dependent)

**Common PO identification judgments:**

| Scenario | Typically Distinct POs | Typically Combined |
|----------|----------------------|-------------------|
| Software license + implementation | If implementation is standard | If significant customization required |
| Hardware + installation | If installation is simple | If integration is essential |
| Product + warranty | Standard warranty = not a PO; extended warranty = separate PO | — |
| SaaS subscription | Single PO (series of daily services) | — |
| Product + training | If customer can use without training | If training is essential to functionality |
| Construction contract | Typically single PO (integrated output) | Multiple POs if separable buildings |

### Step 3: Determine the Transaction Price

**Components of transaction price:**

**Variable consideration:**
```
Estimate using:
  Expected value method — probability-weighted amounts (best for large number of outcomes)
  Most likely amount — single most likely outcome (best for binary outcomes)

Constraint: Include variable consideration only to the extent that it is
highly probable (IFRS) / probable (US GAAP) that a significant reversal
of cumulative revenue will NOT occur.

Examples: performance bonuses, penalties, rebates, price concessions,
rights of return, milestone payments
```

**Significant financing component:**
- Adjust for time value of money if > 12 months between payment and transfer
- Practical expedient: ignore if ≤ 12 months
- Use rate that would be reflected in a separate financing transaction

**Non-cash consideration:** Measure at fair value

**Consideration payable to customer:**
- Reduce transaction price (unless payment for distinct good/service from customer)
- Examples: slotting fees, cooperative advertising, volume rebates

### Step 4: Allocate the Transaction Price

Allocate to each PO based on relative standalone selling prices (SSP).

**SSP estimation methods (in order of preference):**

1. **Observable SSP:** Price when sold separately to similar customers in similar circumstances — most reliable
2. **Adjusted market assessment:** What the market would pay — use competitor pricing, market data
3. **Expected cost plus margin:** Forecast costs plus appropriate margin
4. **Residual approach (restricted use):** Only when SSP is highly variable or uncertain; total price minus observable SSPs of other POs

**Discount allocation:**
- Allocate discount proportionally to all POs
- Exception: if discount relates entirely to one or more (but not all) POs AND observable evidence supports this, allocate discount only to those POs

**Variable consideration allocation:**
- Allocate variable consideration to specific PO if: variable payment relates specifically to satisfying that PO AND allocation is consistent with the objective

### Step 5: Recognize Revenue

**Over time recognition (if ANY ONE criterion is met):**

1. Customer simultaneously receives and consumes benefits (e.g., cleaning services, SaaS)
2. Entity's performance creates or enhances a customer-controlled asset (e.g., construction on customer's land)
3. Entity's performance creates an asset with no alternative use AND entity has enforceable right to payment for performance completed to date (e.g., custom manufacturing)

**Measuring progress (over time):**
- **Output methods:** Units delivered, milestones reached, surveys of performance completed
- **Input methods:** Costs incurred relative to total expected costs (cost-to-cost method), labor hours, machine hours
- Cost-to-cost is most common for construction and long-term contracts

**Point in time recognition (all other situations):**
Indicators of transfer of control:
- Entity has present right to payment
- Customer has legal title
- Physical possession transferred
- Customer has significant risks and rewards
- Customer has accepted the asset

### Principal vs Agent

**Principal:** Controls the good/service before transfer to customer → recognizes gross revenue

**Agent:** Arranges for another party to provide → recognizes net revenue (commission/fee)

**Indicators of principal:**
- Primary responsibility for fulfillment
- Inventory risk (before or after transfer, during shipping, on return)
- Pricing discretion

**This determination significantly impacts reported revenue (not profitability).**

### Licensing

**Right to access (over time):** IP that is dynamic — entity undertakes activities that significantly affect the utility of IP AND customer is exposed to those effects AND those activities do not transfer a good/service. Examples: franchise rights, brand licenses with ongoing marketing requirements.

**Right to use (point in time):** IP that is static — functional IP such as software, patented technology, completed media content. Revenue at the point the license is transferred.

**IFRS 15 and ASC 606 are aligned on this framework, but ASC 606 provides more detailed application guidance for software licensing.**

### SaaS-Specific Guidance

```
Typical SaaS contract elements:
1. Cloud hosting / access to software    → Single PO (series), over time
2. Implementation / configuration        → Distinct if standard; combined if customization
3. Data migration                        → Usually distinct PO
4. Training                              → Usually distinct PO
5. Support and maintenance               → Often combined with hosting (same pattern)
6. Professional services (ongoing)       → Distinct PO

Revenue recognition pattern:
- SaaS subscription: straight-line over contract term (daily obligation in a series)
- Implementation: over implementation period or at go-live depending on distinctness
- Setup fees: if non-refundable upfront fee with no distinct PO → allocated to SaaS PO
  and recognized over contract term (including expected renewals if material right)
```

### Construction Contracts

Typically recognized over time using cost-to-cost method:

```
Revenue recognized = (Costs incurred to date / Total estimated costs) × Total transaction price

Period revenue = Cumulative revenue recognized - Revenue recognized in prior periods

Example:
Total contract price: $10,000
Total estimated costs: $8,000
Costs incurred to date: $3,200

% complete: $3,200 / $8,000 = 40%
Revenue recognized: 40% × $10,000 = $4,000
```

**Contract losses:** If total estimated costs exceed transaction price, recognize the entire expected loss immediately (onerous contract).

## Methodology

### Revenue Recognition Decision Framework

```
Step 1: Is there a valid contract?
  → No: defer until criteria met (or recognize to extent of costs recoverable)
  → Yes: proceed

Step 2: How many POs?
  → Identify each distinct promise
  → Apply the distinctness test (capable + separately identifiable)

Step 3: What is the total transaction price?
  → Fixed + variable (constrained) + financing + non-cash - consideration payable to customer

Step 4: How to allocate?
  → Relative SSP for each PO
  → Special rules for discounts and variable consideration

Step 5: Over time or point in time for each PO?
  → Test three over-time criteria
  → If none met: point in time (assess indicators of control transfer)
```

### Contract Cost Capitalization (ASC 340-40 / IFRS 15.91-104)

**Incremental costs of obtaining a contract:**
- Costs that would not have been incurred if the contract had not been obtained
- Primarily: sales commissions
- Capitalize and amortize over the period of benefit (contract term or longer if renewals expected)
- Practical expedient: expense if amortization period ≤ 12 months

**Costs to fulfill a contract:**
- Capitalize if: relate directly to a contract, generate/enhance resources used for satisfaction, expected to be recovered
- Examples: setup costs, mobilization costs, pre-production design costs

## Templates

### Revenue Recognition Assessment

```
=== REVENUE RECOGNITION ASSESSMENT ===

Contract: [Description]
Customer: [Name]
Total Consideration: $____
Contract Term: ____ months

--- Performance Obligations Identified ---
PO# | Description          | Distinct? | SSP      | Allocated Price | Timing
1   | [Software license]   | Yes       | $____    | $____           | Point in time
2   | [Implementation]     | Yes/No    | $____    | $____           | Over time
3   | [Support 12 months]  | Yes       | $____    | $____           | Over time (straight-line)
4   | [Training]           | Yes       | $____    | $____           | Point in time

Total Allocated:                                    $____ (= transaction price)

--- Variable Consideration ---
Type: [Performance bonus / rebate / penalty]
Estimation method: [Expected value / Most likely amount]
Estimated amount: $____
Constrained amount included in TP: $____
Reassessment trigger: [Quarterly / at milestone]

--- Recognition Schedule ---
Period    | PO1    | PO2    | PO3    | PO4    | Total
Q1        | $____  | $____  | $____  | $____  | $____
Q2        |   —    | $____  | $____  |   —    | $____
Q3        |   —    |   —    | $____  |   —    | $____
Q4        |   —    |   —    | $____  |   —    | $____
Total     | $____  | $____  | $____  | $____  | $____
```

### Principal vs Agent Assessment

```
=== PRINCIPAL VS AGENT ANALYSIS ===

Arrangement: [Description]
Goods/Services: [What is being provided to the end customer]

Indicator                      | Assessment | Supports
Primary fulfillment obligation | [Entity/Supplier] | [Principal/Agent]
Inventory risk                 | [Yes/No]          | [Principal/Agent]
Pricing discretion             | [Yes/No]          | [Principal/Agent]
Credit risk                    | [Entity/Customer] | [—]

Conclusion: [Entity is Principal/Agent]
Revenue presentation: [Gross $____ / Net $____]
```

## Quality Gate

Before finalizing revenue recognition, verify:

- [ ] All five steps are documented for each material contract or contract type
- [ ] Performance obligations pass both distinctness criteria (capable + separately identifiable)
- [ ] SSP is determined using the best available method with documentation
- [ ] Variable consideration is estimated and constrained at the individual contract level
- [ ] Over-time recognition criteria are tested — at least one must be met for over-time
- [ ] Input method (cost-to-cost) uses total estimated costs that are reviewed and updated regularly
- [ ] Principal vs agent assessment is performed for all intermediary/reseller arrangements
- [ ] Non-refundable upfront fees are allocated to POs (not recognized at contract inception unless a PO is satisfied)
- [ ] Contract modifications are assessed as separate contracts or prospective adjustments
- [ ] Material rights (renewal options below SSP) are identified as separate POs
- [ ] Contract costs are capitalized and amortized per ASC 340-40 / IFRS 15
- [ ] Disclosures include disaggregated revenue, contract balances, and remaining POs
- [ ] Consistent treatment across similar contracts (policy, not ad hoc decisions)
