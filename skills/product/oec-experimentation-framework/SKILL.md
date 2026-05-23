---
name: oec-experimentation-framework
description: Define and apply an Overall Evaluation Criterion (OEC) to measure the long-term impact of product changes. Use this skill when designing A/B tests, setting quarterly OKRs, or when short-term wins (like revenue) are potentially harming long-term user retention.
---

The Overall Evaluation Criterion (OEC) is a single composite metric used to determine the success of an experiment by balancing short-term gains against long-term health. It prevents teams from "gaming" the system by optimizing for narrow metrics that inadvertently hurt the user experience.

## The OEC Construction Workflow

### 1. Identify Primary Success Metrics
Identify the immediate behavior you want to encourage (e.g., clicks, revenue, bookings). This is your "top-line" metric.

### 2. Identify Countervailing (Guardrail) Metrics
Determine what "bad" behaviors the top-line metric might encourage. These metrics act as a check on the primary goal.
- **Revenue goals?** Check for churn or user sentiment.
- **Click-through goals?** Check for bounce rate or "successful sessions" (e.g., clicks that stay on the page for >30 seconds).
- **Email volume?** Check for unsubscribe rates.

### 3. Model Lifetime Value (LTV)
Assign a dollar value to negative long-term actions to create a balanced formula. 
- **Example Calculation:** `OEC = (Short-term Revenue) - (Unsubscribe Rate * Estimated Value of a Subscriber)`.
- If an email campaign generates $1,000 but causes 500 unsubscribes, and each subscriber is worth $3/year, the campaign is net-negative (-$500).

### 4. Set Constraint Optimizations
If a composite formula is too complex, use the "Fixed Budget" approach.
- Allow the team to optimize a metric (e.g., Revenue) only if a guardrail metric (e.g., Page Load Latency or Ad Real Estate) remains within a fixed "budget."

## Validity Testing with Twyman’s Law
"Any figure that looks interesting or different is usually wrong." Before celebrating a "home run" result:
- **Check for Sample Ratio Mismatch (SRM):** If you designed a 50/50 split but get 50.2/49.8 with 1M users, the experiment is likely invalid due to bot interference or data pipeline issues.
- **Hold the Celebration:** If a metric moves by 10% when you expected 1%, assume it is a bug (e.g., double-logging revenue) until proven otherwise.
- **Replicate:** Rerun the experiment. If the P-value stays significant (e.g., <0.01), trust increases.

## The Experimentation Portfolio
Manage your product roadmap like a stock portfolio:
- **Incremental (70-80%):** Small, "inch-by-inch" improvements with high probability of success.
- **High Risk/High Reward (10-20%):** Radical redesigns or new features. Expect an 80-90% failure rate here, but aim for "home runs" that move the needle by 5-12%.

## Examples

**Example 1: Search Engine Monetization**
- **Context:** A team wants to increase revenue by adding more ads to the search results page.
- **Input:** Primary metric = Ad Revenue. Countervailing metric = Session Success Rate (did the user find what they wanted?).
- **Application:** Create an OEC where revenue gains are only "wins" if the Session Success Rate does not drop by more than 0.1%.
- **Output:** The team realizes that while 4 ads make more money today, they increase churn. They settle on 3 ads as the optimal OEC balance.

**Example 2: Retention Marketing**
- **Context:** An email team is measured by "Revenue from Email Clicks."
- **Input:** Team increases email frequency to 5x per week.
- **Application:** Apply the "Cost of Spam" model. Subtract $5 from the "success" total for every unsubscribe.
- **Output:** The data shows that 50% of the high-frequency campaigns are actually destroying long-term value. The team reduces frequency to 2x per week, increasing total LTV.

## Common Pitfalls
- **Shipping on "Flat" Results:** Never ship a feature if the results are not statistically significant. This introduces "code debt" and maintenance costs for zero user benefit.
- **Ignoring the Sunk Cost Fallacy:** Avoid shipping a 6-month project just because the team spent time on it. If the A/B test is negative, the project failed.
- **Peeking at P-values:** Do not stop an experiment early just because the P-value hit 0.05. This leads to "Type 1" errors (false positives). Wait for the full designated duration.
- **Trusting One-off Successes:** If a result is "too good to be true," it is likely a tracking bug or a bot. Apply Twyman's Law immediately.