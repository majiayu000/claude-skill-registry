---
name: billing-integration
description: Generic billing and subscription management integration
allowed-tools: [Bash, Read, WebFetch]
---

# Billing Integration Skill

## Overview

Billing and subscription management. 90%+ context savings.

## Tools (Progressive Disclosure)

### Subscriptions

| Tool                | Description         | Confirmation |
| ------------------- | ------------------- | ------------ |
| list-subscriptions  | List subscriptions  | No           |
| create-subscription | Create subscription | Yes          |
| cancel-subscription | Cancel subscription | **REQUIRED** |

### Invoices

| Tool          | Description         |
| ------------- | ------------------- |
| list-invoices | List invoices       |
| get-invoice   | Get invoice details |
| invoice-pdf   | Get invoice PDF     |

### Customers

| Tool            | Description       | Confirmation |
| --------------- | ----------------- | ------------ |
| get-customer    | Get customer info | No           |
| update-customer | Update customer   | Yes          |

### BLOCKED

| Tool            | Status      |
| --------------- | ----------- |
| delete-customer | **BLOCKED** |

## Agent Integration

- **developer** (primary): Billing integration
- **pm** (secondary): Pricing strategy
