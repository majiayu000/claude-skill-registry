---
name: finance-domain
description: Personal finance domain knowledge. Use when implementing financial calculations, budgeting logic, transaction categorization, or reporting features.
---

# Finance Domain Knowledge

## Core Concepts

### Transaction Types
- **Income**: Salary, freelance, investment returns, gifts
- **Expense**: Bills, shopping, food, transport, entertainment
- **Transfer**: Between own accounts (NOT income or expense)

### Account Types
- **Cash**: Physical cash tracking
- **Bank**: Checking/savings accounts
- **Credit Card**: Credit accounts (negative = owed)
- **Investment**: Stocks, bonds, crypto
- **Loan**: Mortgages, personal loans (negative balance)

## Financial Calculations

### CRITICAL: Money Handling
```swift
// ALWAYS use Decimal for money — NEVER Double
let amount: Decimal = 1_000_000  // ✅
let amount: Double = 1_000_000   // ❌ floating point errors

// Rounding for display
let rounded = NSDecimalNumber(decimal: amount)
    .rounding(accordingToBehavior: NSDecimalNumberHandler(
        roundingMode: .bankers,
        scale: 0,  // VND has 0 decimal places
        raiseOnExactness: false,
        raiseOnOverflow: false,
        raiseOnUnderflow: false,
        raiseOnDivideByZero: true
    ))
```

### Budget Tracking
```
Budget Remaining = Budget Amount - Sum(Expenses in Period)
Budget Usage % = Sum(Expenses) / Budget Amount * 100
Daily Average Spending = Sum(Expenses in Month) / Days Elapsed
Projected Month Spend = Daily Average * Days in Month
```

### Net Worth Calculation
```
Net Worth = Sum(Asset Accounts) - Sum(Liability Accounts)
Assets = Cash + Bank + Investment (positive balances)
Liabilities = Credit Card debt + Loans (negative balances)
```

## Vietnamese Currency (VND)
- ISO code: VND
- Symbol: ₫
- Decimal places: 0 (no cents)
- Number format: 1.000.000 ₫ (dot as thousands separator)
- Use `Locale(identifier: "vi_VN")` for formatting
