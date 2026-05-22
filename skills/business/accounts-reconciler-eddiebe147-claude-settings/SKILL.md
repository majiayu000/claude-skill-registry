---
name: Accounts Reconciler
slug: accounts-reconciler
description: Automate account reconciliation by matching transactions, identifying discrepancies, and generating variance reports
category: business
complexity: intermediate
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "reconcile accounts"
  - "match transactions"
  - "find discrepancies"
tags:
  - accounting
  - reconciliation
  - finance
---

# Accounts Reconciler

Streamline account reconciliation by automatically matching transactions across multiple sources, identifying discrepancies, and generating variance reports. Eliminates hours of manual spreadsheet work.

## Core Workflows

### Workflow 1: Bank Statement Reconciliation
1. **Import Data** - Load bank statement and internal ledger
2. **Auto-Match** - Match transactions by amount, date, reference
3. **Flag Exceptions** - Identify unmatched items
4. **Document Adjustments** - Record journal entries
5. **Generate Report** - Create reconciliation summary

### Workflow 2: AR/AP Reconciliation
1. **Pull Aging** - Extract receivables/payables by customer/vendor
2. **Match Payments** - Link payments to invoices
3. **Identify Unapplied** - Find payments without matching invoices
4. **Generate Statements** - Create statements for resolution

## Quick Reference

| Action | Command |
|--------|---------|
| Reconcile bank | "Reconcile [account] for [period]" |
| Find mismatches | "Show unmatched transactions" |
| Variance report | "Generate variance report" |
