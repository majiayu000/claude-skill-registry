---
name: finance-tracking
description: Tracks financial transactions, categorizes expenses, monitors budgets, and audits subscriptions. Use when processing bank transactions, categorizing expenses, tracking revenue, or analyzing financial data.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Finance Tracking Skill

This skill provides comprehensive financial tracking and analysis for the Personal AI Employee, including transaction processing, budget monitoring, and subscription management.

## Capabilities

1. **Transaction Processing** - Parse and categorize bank transactions
2. **Budget Monitoring** - Track spending against category budgets
3. **Subscription Audit** - Identify and evaluate recurring charges
4. **Revenue Tracking** - Monitor income and invoices
5. **Financial Reporting** - Generate summaries and insights

## Transaction Categories

| Category | Keywords | Monthly Budget |
|----------|----------|----------------|
| Software/SaaS | subscription, monthly, .com | $500 |
| Marketing | ads, facebook, google, marketing | $1000 |
| Office | amazon, staples, supplies | $200 |
| Utilities | electric, internet, phone | $300 |
| Travel | airline, hotel, uber, lyft | $500 |
| Professional | consulting, legal, accounting | Variable |

## File Formats

### Transaction Record
```yaml
---
type: transaction
date: 2026-01-07
amount: -49.99
category: Software/SaaS
vendor: Notion
is_recurring: true
---
Monthly subscription payment
```

### Budget Status
```markdown
# Budget Status - January 2026

| Category | Budget | Spent | Remaining | % Used |
|----------|--------|-------|-----------|--------|
| Software | $500 | $350 | $150 | 70% |
```

## Subscription Patterns

Common subscription identifiers:
- netflix.com, spotify.com, adobe.com
- notion.so, slack.com, github.com
- dropbox.com, zoom.us, openai.com

## Reference

For detailed API and patterns, see [reference.md](reference.md)

For usage examples, see [examples.md](examples.md)
