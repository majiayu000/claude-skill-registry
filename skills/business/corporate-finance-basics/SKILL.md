---
name: corporate-finance-basics
description: Corporate finance fundamentals for evaluating business decisions under cost, time, and risk constraints. Covers time value of money, net present value, internal rate of return, payback period, break-even analysis, cost-benefit analysis, debt vs equity, working capital, and the basic financial statements. Use when evaluating an investment, sizing a funding round, structuring a capital stack, or reading a balance sheet.
type: skill
category: business
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/business/corporate-finance-basics/SKILL.md
superseded_by: null
---
# Corporate Finance Basics

Finance is the discipline of allocating capital over time under uncertainty. Every business decision that commits resources has a financial structure: a cost, a benefit, a timing, and a risk. This skill catalogs the core techniques a manager or founder uses to evaluate investments, raise capital, and read financial statements — enough to make sound decisions without pretending to be a CFO.

**Agent affinity:** drucker (capital allocation and effectiveness), mintzberg (reading financials in context)

**Concept IDs:** bus-debt-vs-equity, bus-cost-benefit-analysis, bus-break-even-analysis, bus-investment-appraisal

## The Finance Toolbox at a Glance

| # | Technique | Best for | Key signal |
|---|---|---|---|
| 1 | Time value of money | Comparing cash flows across time | Decision involves money now vs later |
| 2 | Net present value (NPV) | Evaluating investments | Must pick among projects with different timing |
| 3 | Internal rate of return (IRR) | Ranking projects | Need a single summary number |
| 4 | Payback period | Quick screening | Liquidity matters more than total return |
| 5 | Break-even analysis | Sizing a new product | Need to know the volume required to not lose money |
| 6 | Cost-benefit analysis | Structured decision | Costs and benefits span categories and time |
| 7 | Debt vs equity | Structuring capital | Must decide whether to borrow or sell ownership |
| 8 | Working capital | Managing the operating cycle | Cash is tight despite profits |
| 9 | Reading the three statements | Understanding any business | Need a diagnosis from financials |
| 10 | Cost of capital (WACC) | Discount rate selection | Need to know what return justifies an investment |

## Technique 1 — Time Value of Money

**Core principle.** A dollar today is worth more than a dollar tomorrow, because the dollar today can be invested to earn a return, or simply because future dollars are less certain. The conversion is done with a discount rate $r$.

**Formulas.**

- **Future value:** $FV = PV \cdot (1 + r)^n$ where $PV$ is present value, $r$ is the periodic rate, $n$ is the number of periods.
- **Present value:** $PV = FV / (1 + r)^n$

**Worked example.** At $r = 8$ percent annual, $1000 received five years from now is worth $1000 / 1.08^5 = 1000 / 1.4693 \approx 680.58$ today. The opposite direction: $1000 invested today at 8 percent grows to $1469.33 in five years.

**When it matters.** Any decision where cash flows occur at different times must be time-adjusted. Comparing "save $500/year for 10 years" against "pay $3000 up-front" without discounting gives the wrong answer.

## Technique 2 — Net Present Value (NPV)

**Pattern:** Sum the discounted cash flows of a project, including the initial investment as a negative at time zero. If NPV is positive, the project creates value at the chosen discount rate. If NPV is negative, it destroys value.

**Formula.**

$$NPV = \sum_{t=0}^{n} \frac{CF_t}{(1+r)^t}$$

**Worked example.** A project requires $100K today and produces $40K/year for 3 years. At $r = 10$ percent:

$$NPV = -100 + \frac{40}{1.1} + \frac{40}{1.1^2} + \frac{40}{1.1^3} = -100 + 36.36 + 33.06 + 30.05 = -0.53$$

Slightly negative. The project is not quite worth doing at a 10 percent cost of capital. At 8 percent the same project has NPV of +3.08 and is worth doing. The choice of discount rate is load-bearing.

**Decision rule.** Accept any project with positive NPV at the firm's cost of capital. Rank competing projects by NPV.

## Technique 3 — Internal Rate of Return (IRR)

**Pattern:** The IRR is the discount rate that makes NPV equal to zero. It summarizes the project's return as a single annualized rate, comparable across projects.

**Decision rule.** Accept projects with IRR above the cost of capital. Reject below.

**Limitations.** IRR has three failure modes that NPV does not:

1. **Non-unique IRRs** — projects with non-conventional cash flows (e.g., negative cash flow in the middle) can have multiple valid IRRs.
2. **Scale blindness** — a 50 percent IRR on a $10K investment is worse than a 15 percent IRR on a $10M investment for most firms, but IRR ranks the smaller project higher.
3. **Reinvestment assumption** — IRR implicitly assumes intermediate cash flows are reinvested at the IRR itself, which is usually not achievable.

**Rule of thumb.** Use NPV for the decision; report IRR as a summary for communication.

## Technique 4 — Payback Period

**Pattern:** The time required for cumulative cash inflows to equal the initial investment. A $100K investment producing $25K/year has a 4-year payback.

**Strength.** Simple, intuitive, and a reasonable proxy for liquidity risk — how long is capital locked up?

**Weakness.** Ignores time value of money and ignores cash flows after the payback threshold. A project with a 3-year payback and then zero return is ranked the same as one with a 3-year payback and then another decade of return.

**When to use.** As a screening filter before NPV. Payback is fast to compute and rules out obvious losers. Any project passing the payback screen still needs a full NPV before commitment.

## Technique 5 — Break-even Analysis

**Pattern:** Find the volume at which total revenue equals total cost. Below break-even, the firm loses money; above, it profits. The formula separates fixed costs (independent of volume) from variable costs (proportional to volume).

**Formula.** $Q_{BE} = \frac{FC}{P - VC}$ where $Q_{BE}$ is break-even quantity, $FC$ is fixed costs, $P$ is price per unit, $VC$ is variable cost per unit, and $(P - VC)$ is the contribution margin.

**Worked example.** A product has $200K annual fixed cost, sells for $50, and costs $30 variable per unit. Break-even is $200{,}000 / (50 - 30) = 10{,}000$ units. If forecast demand is 8,000, the product loses money even at full execution. If forecast is 15,000, it produces a profit of $(15{,}000 - 10{,}000) \times 20 = 100{,}000$.

**Strategic use.** Break-even exposes whether a product concept can work at all, before any investment. A product whose break-even exceeds plausible demand is dead on paper.

## Technique 6 — Cost-Benefit Analysis (CBA)

**Pattern:** Enumerate all costs and benefits of a decision (including non-monetary where possible), convert to dollars where feasible, and discount to present value. The decision rule is: proceed if benefits exceed costs in discounted terms.

**Key disciplines.**

- **Enumerate both sides.** Many CBAs fail by listing three costs and eight benefits, or by omitting opportunity cost (what else could this capital do?).
- **Time-adjust.** Costs now vs benefits in the future must be discounted.
- **Handle uncertainty.** Use ranges or expected values, not single-point estimates, when inputs are uncertain.
- **Respect the uncommensurable.** Some benefits (safety, reputation, mission fit) resist dollar conversion. Do not invent false precision; report them alongside the monetary calculation.

**When NOT to use.** When the core values at stake (safety of life, legal compliance, ethical commitments) are not negotiable, CBA can mislead by implying they are trade-offs. A safety decision is a constraint, not an input to a trade-off.

## Technique 7 — Debt vs Equity

**Pattern:** When a firm needs capital, it can borrow (debt) or sell ownership (equity). Each has different costs, risks, and control implications.

**Comparison.**

| Dimension | Debt | Equity |
|---|---|---|
| Cost | Interest (tax-deductible) | Dividends + share of residual |
| Cash impact | Regular payments due | Flexible, no required payments |
| Risk to firm | Default risk if cash flow falls | No default, but ownership diluted |
| Control | Lender has no voting rights | Investors may demand board seat, strategy input |
| Upside | Creditor gets fixed return | Investor shares in success |
| Tax | Interest is a tax-deductible expense | Dividends are not deductible |
| Best when | Cash flows are predictable | Cash flows are uncertain or growth-focused |

**Worked example.** A growing software company has uncertain but potentially large cash flows and limited collateral. Debt is probably wrong — default risk is high and lenders will want collateral that does not exist. Equity is a better fit: the investor accepts the risk in exchange for a share of the upside. A stable utility with predictable cash flows and real assets is the opposite case — debt is cheaper and dilution is unnecessary.

**Capital structure shorthand.** The right debt-equity mix depends on cash flow predictability, tax rate, growth stage, and the cost and availability of each. No single ratio is universally correct.

## Technique 8 — Working Capital

**Pattern:** Working capital is current assets minus current liabilities — the cash tied up in the operating cycle (inventory, receivables, payables). Profitable firms routinely run out of cash because profit and cash are different things.

**The operating cycle.** Cash is used to buy inventory, which becomes receivables when sold, which becomes cash when collected. If this cycle is 90 days and the firm is growing, working capital needs grow with sales — the firm must fund the gap.

**Worked example.** A retailer is profitable on paper (10 percent margin) but runs out of cash every month. Analysis reveals 60-day receivables, 45-day inventory, and 20-day payables. The operating cycle is $60 + 45 - 20 = 85$ days. Every $1000 of monthly sales requires roughly $2800 of working capital tied up at any moment. Growth makes the shortfall worse. The fix is not to cut costs but to shorten the cycle: faster collections, less inventory, or longer payables.

**Strategic point.** A business model can be profitable but uninvestable if its working capital requirement scales faster than its profits. Profit without cash is a trap.

## Technique 9 — Reading the Three Statements

**Pattern:** Every business has three financial statements that together describe it. Reading all three in relation to each other diagnoses the business.

| Statement | What it shows | Time | Analogy |
|---|---|---|---|
| Income statement (P&L) | Revenues and expenses over a period | Flow | Video |
| Balance sheet | Assets, liabilities, equity at a point in time | Stock | Photo |
| Cash flow statement | Cash inflows and outflows over a period | Flow | Different video |

**Diagnostic questions.**

- **From the income statement:** Is the business profitable? What is the gross margin? Is it growing? Which line items are growing faster than revenue?
- **From the balance sheet:** How much cash is on hand? How much debt? How much inventory? Are receivables growing faster than revenue (collection problem)?
- **From the cash flow statement:** Is the business generating cash from operations, or funding itself from financing? A "profitable" business with negative operating cash flow is often funding profits with working-capital tricks.

**Worked example.** A startup reports rising revenue and narrowing losses on the income statement. The balance sheet shows receivables growing three times faster than revenue. The cash flow statement shows operating cash flow deteriorating even as net loss narrows. Diagnosis: the firm is booking revenue it is not collecting. The "improvement" is an accounting artifact. A collections crisis is imminent.

## Technique 10 — Cost of Capital (WACC)

**Pattern:** The weighted average cost of capital is the discount rate that reflects the firm's actual capital structure. It is used as the minimum acceptable return on new investments.

**Formula.**

$$WACC = \frac{E}{V} \cdot r_e + \frac{D}{V} \cdot r_d \cdot (1 - t)$$

where $E$ is equity value, $D$ is debt value, $V = E + D$, $r_e$ is cost of equity, $r_d$ is cost of debt, and $t$ is the tax rate (interest is tax-deductible, which reduces the effective cost of debt).

**Use.** WACC becomes the discount rate for NPV calculations. Projects earning above WACC create value; projects earning below WACC destroy it.

**Caveat.** WACC is a firm-average rate. A project substantially riskier than the firm's average should use a higher rate, and vice versa. Using firm-wide WACC for every project produces systematic over-investment in risky projects and under-investment in safe ones.

## Decision Guidance

1. **Comparing cash across time?** Discount with time value of money.
2. **Evaluating an investment?** NPV is the decision rule.
3. **Ranking many projects?** Report IRR but decide with NPV.
4. **Liquidity concern?** Payback as a screening filter.
5. **Is the product economically viable at all?** Break-even first.
6. **Structured decision with many costs and benefits?** CBA, honest about uncertainty.
7. **Raising capital?** Debt if cash flow is predictable, equity if uncertain or growth-focused.
8. **Running out of cash despite profit?** Check working capital.
9. **Diagnosing any business?** Read all three statements together.
10. **Setting a hurdle rate?** WACC, adjusted for project risk.

## Common Mistakes

| Mistake | Why it fails | Fix |
|---|---|---|
| Comparing undiscounted cash flows across time | Ignores time value | Always discount |
| Using IRR to rank mutually exclusive projects | Scale blindness | Use NPV for ranking |
| Omitting opportunity cost from CBA | Inflates apparent benefit | Include the next-best use of capital |
| Treating profit and cash as the same | Working capital trap | Track cash flow separately |
| Using firm-wide WACC on a risky project | Systematic mis-pricing | Adjust the rate for project risk |
| Building on single-point estimates | False precision | Use ranges, test sensitivity |

## References

- Brealey, R. A., Myers, S. C., & Allen, F. (2020). *Principles of Corporate Finance*. 13th edition. McGraw-Hill.
- Graham, B., & Dodd, D. (1934). *Security Analysis*. McGraw-Hill.
- Damodaran, A. (2012). *Investment Valuation*. 3rd edition. Wiley.
- Higgins, R. C. (2015). *Analysis for Financial Management*. McGraw-Hill.
- Drucker, P. F. (1973). *Management: Tasks, Responsibilities, Practices*. Harper & Row. (Chapters on effective capital allocation.)
