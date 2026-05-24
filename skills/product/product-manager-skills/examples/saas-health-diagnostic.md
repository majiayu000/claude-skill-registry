# Example: SaaS Health Diagnostic

## Scenario

You want a fast diagnosis from a small set of numbers, not a finance lecture.

## Prompt

```text
Analyze these metrics: MRR $50k, 500 customers, gross margin 80%, monthly churn 8%, CAC $500.
```

## Example Output Excerpt

```text
Diagnosis
- 8% monthly churn compounds to roughly 63% annual churn. This is a red flag, not a mild retention issue.
- ARPA is about $100/month. With 80% gross margin and 8% monthly churn, better LTV is about $1,000.
- LTV:CAC is about 2:1. That is below a healthy SaaS target, even though payback is workable at about 6.25 months.
- The bottleneck is retention, not acquisition efficiency. Scaling paid acquisition before fixing churn will hide the real problem.

Likely root causes to inspect next
- Weak activation in the first 14 days
- Low repeat value for the core job
- Poor fit in one or more acquisition cohorts

Recommended next step
- Pull 3 monthly cohorts, compare retention at day 30 / 60 / 90, and isolate the biggest drop-off before changing spend.
```

## Why This Matters

The useful part is not just the math. The skill converts the math into a decision:

- what is actually broken
- what not to optimize yet
- what analysis should come next
