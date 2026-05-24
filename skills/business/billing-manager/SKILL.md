---
name: Billing Manager
slug: billing-manager
description: Manage billing operations including invoice generation, payment tracking, and subscription lifecycle
category: business
complexity: intermediate
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "create invoice"
  - "billing cycle"
  - "manage subscriptions"
tags:
  - billing
  - invoicing
  - subscriptions
---

# Billing Manager

Take control of billing operations with workflows for invoice generation, payment tracking, and subscription management. Maintain healthy cash flow with timely invoicing and proactive collection.

## Core Workflows

### Workflow 1: Invoice Generation
1. **Gather Billables** - Collect billable items, hours, or usage
2. **Apply Pricing** - Calculate amounts based on rate cards
3. **Add Taxes** - Apply appropriate tax rates
4. **Generate Invoice** - Create professional invoice
5. **Track Status** - Monitor open, paid, overdue

### Workflow 2: Subscription Billing
1. **Setup** - Configure plan, billing cycle, terms
2. **Recurring Charges** - Process automatic billing
3. **Failed Payment Handling** - Retry logic and dunning
4. **Renewal Notices** - Send reminders

## Quick Reference

| Action | Command |
|--------|---------|
| Create invoice | "Generate invoice for [customer]" |
| Check status | "Show outstanding invoices" |
| Process subscription | "Bill [customer] subscription" |
