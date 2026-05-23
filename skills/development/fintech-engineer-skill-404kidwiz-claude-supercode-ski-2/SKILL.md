---
name: fintech-engineer
description: Expert in financial technology systems, double-entry ledger design, high-precision math, and regulatory compliance. Use when building payment systems, ledger architectures, financial calculations, PCI compliance, or banking integrations. Triggers include "fintech", "ledger", "double-entry", "financial calculations", "PCI compliance", "banking API".
---

# Fintech Engineer

## Purpose
Provides expert guidance on building financial technology systems with proper accounting principles, regulatory compliance, and high-precision calculations. Specializes in ledger design, payment processing architectures, and financial data integrity.

## When to Use
- Designing double-entry ledger systems or accounting databases
- Implementing high-precision financial calculations (avoiding floating-point errors)
- Building payment processing pipelines
- Ensuring PCI-DSS or SOX compliance
- Integrating with banking APIs (Plaid, Stripe, etc.)
- Handling currency conversions and multi-currency systems
- Implementing audit trails for financial transactions
- Designing reconciliation systems

## Quick Start
**Invoke this skill when:**
- Building ledger or accounting systems
- Implementing financial calculations requiring precision
- Designing payment processing architectures
- Ensuring regulatory compliance (PCI, SOX, PSD2)
- Integrating banking or payment APIs

**Do NOT invoke when:**
- General database design without financial context → use `/database-administrator`
- API integration without financial specifics → use `/api-designer`
- Generic security hardening → use `/security-engineer`
- ML-based fraud detection models → use `/ml-engineer`

## Decision Framework
```
Financial Calculation Needed?
├── Yes: Currency/Money
│   └── Use decimal types (never float)
│   └── Store amounts in smallest unit (cents)
├── Yes: Interest/Rates
│   └── Use arbitrary precision libraries
│   └── Document rounding rules explicitly
└── Ledger Design?
    ├── Simple: Single-entry (tracking only)
    └── Auditable: Double-entry (debits = credits)
```

## Core Workflows

### 1. Double-Entry Ledger Implementation
1. Define chart of accounts (assets, liabilities, equity, revenue, expenses)
2. Create journal entry table with debit/credit columns
3. Implement balance validation (sum of debits = sum of credits)
4. Add audit trail with immutable transaction logs
5. Build reconciliation queries

### 2. Payment Processing Pipeline
1. Validate payment request and idempotency key
2. Create pending transaction record
3. Call payment processor with retry logic
4. Handle webhook for async confirmation
5. Update ledger entries atomically
6. Generate receipt and audit log

### 3. Precision Calculation Setup
1. Choose appropriate numeric type (DECIMAL, NUMERIC, BigDecimal)
2. Define scale (decimal places) based on currency
3. Implement rounding rules per jurisdiction
4. Create calculation helper functions
5. Add validation for overflow/underflow

## Best Practices
- Store monetary values as integers in smallest unit (cents, paise)
- Use DECIMAL/NUMERIC database types, never FLOAT
- Implement idempotency for all financial operations
- Maintain immutable audit logs for every transaction
- Use database transactions for multi-table updates
- Document rounding rules and apply consistently

## Anti-Patterns
| Anti-Pattern | Problem | Correct Approach |
|--------------|---------|------------------|
| Using floats for money | Precision errors accumulate | Use decimal types or integer cents |
| Mutable transaction records | Audit trail destroyed | Append-only logs, soft deletes |
| Missing idempotency | Duplicate charges possible | Idempotency keys on all mutations |
| Single-entry for auditable systems | Cannot reconcile or audit | Double-entry with balanced journals |
| Hardcoded tax rates | Compliance failures | Configuration-driven, versioned rules |
