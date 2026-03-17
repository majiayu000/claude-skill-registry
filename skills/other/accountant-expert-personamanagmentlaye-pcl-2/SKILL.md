---
name: accountant-expert
version: 1.0.0
description: Expert-level accounting, tax, financial reporting, and accounting systems
category: professional
tags: [accounting, tax, financial-reporting, gaap, ifrs]
allowed-tools:
  - Read
  - Write
  - Edit
---

# Accountant Expert

Expert guidance for accounting systems, financial reporting, tax compliance, and modern accounting technology.

## Core Concepts

### Accounting Principles
- GAAP (Generally Accepted Accounting Principles)
- IFRS (International Financial Reporting Standards)
- Double-entry bookkeeping
- Accrual vs cash accounting
- Financial statement preparation
- Audit and assurance

### Financial Statements
- Balance sheet (Statement of Financial Position)
- Income statement (P&L)
- Cash flow statement
- Statement of changes in equity
- Notes to financial statements

### Tax & Compliance
- Corporate tax planning
- VAT/Sales tax management
- Payroll tax compliance
- Tax filing and reporting
- Transfer pricing
- International taxation

## Double-Entry Bookkeeping

```python
from decimal import Decimal
from datetime import datetime
from enum import Enum
from typing import List

class AccountType(Enum):
    ASSET = "asset"
    LIABILITY = "liability"
    EQUITY = "equity"
    REVENUE = "revenue"
    EXPENSE = "expense"

class Account:
    def __init__(self, code: str, name: str, account_type: AccountType):
        self.code = code
        self.name = name
        self.type = account_type
        self.balance = Decimal('0')
        self.debit_total = Decimal('0')
        self.credit_total = Decimal('0')

    def is_debit_normal(self) -> bool:
        """Check if account has normal debit balance"""
        return self.type in [AccountType.ASSET, AccountType.EXPENSE]

class JournalEntry:
    def __init__(self, date: datetime, description: str):
        self.id = self.generate_entry_id()
        self.date = date
        self.description = description
        self.lines = []
        self.posted = False

    def add_line(self, account: Account, debit: Decimal = None,
                 credit: Decimal = None):
        """Add line to journal entry"""
        if debit and credit:
            raise ValueError("Cannot have both debit and credit")

        self.lines.append({
            "account": account,
            "debit": debit or Decimal('0'),
            "credit": credit or Decimal('0')
        })

    def validate(self) -> bool:
        """Validate journal entry (debits must equal credits)"""
        total_debits = sum(line["debit"] for line in self.lines)
        total_credits = sum(line["credit"] for line in self.lines)

        return total_debits == total_credits

    def post(self) -> bool:
        """Post journal entry to ledger"""
        if not self.validate():
            raise ValueError("Entry does not balance")

        for line in self.lines:
            account = line["account"]
            if line["debit"]:
                account.debit_total += line["debit"]
            if line["credit"]:
                account.credit_total += line["credit"]

            # Update balance based on account type
            if account.is_debit_normal():
                account.balance = account.debit_total - account.credit_total
            else:
                account.balance = account.credit_total - account.debit_total

        self.posted = True
        return True
```

## Financial Statement Generation

```python
class FinancialStatements:
    def __init__(self, company_name: str, period_end: datetime):
        self.company_name = company_name
        self.period_end = period_end
        self.accounts = []

    def generate_balance_sheet(self) -> dict:
        """Generate balance sheet"""
        assets = self.sum_accounts_by_type(AccountType.ASSET)
        liabilities = self.sum_accounts_by_type(AccountType.LIABILITY)
        equity = self.sum_accounts_by_type(AccountType.EQUITY)

        # Calculate retained earnings
        revenue = self.sum_accounts_by_type(AccountType.REVENUE)
        expenses = self.sum_accounts_by_type(AccountType.EXPENSE)
        net_income = revenue - expenses

        total_equity = equity + net_income

        return {
            "company": self.company_name,
            "period_end": self.period_end,
            "assets": {
                "current_assets": self.get_current_assets(),
                "non_current_assets": self.get_non_current_assets(),
                "total": assets
            },
            "liabilities": {
                "current_liabilities": self.get_current_liabilities(),
                "non_current_liabilities": self.get_non_current_liabilities(),
                "total": liabilities
            },
            "equity": {
                "share_capital": equity,
                "retained_earnings": net_income,
                "total": total_equity
            },
            "balanced": assets == (liabilities + total_equity)
        }

    def generate_income_statement(self, period_start: datetime,
                                   period_end: datetime) -> dict:
        """Generate income statement (P&L)"""
        revenue = self.sum_accounts_by_type(AccountType.REVENUE)
        expenses = self.sum_accounts_by_type(AccountType.EXPENSE)

        gross_profit = revenue - self.get_cogs()
        operating_expenses = self.get_operating_expenses()
        operating_income = gross_profit - operating_expenses

        interest_expense = self.get_interest_expense()
        tax_expense = self.calculate_tax(operating_income - interest_expense)

        net_income = operating_income - interest_expense - tax_expense

        return {
            "company": self.company_name,
            "period": f"{period_start.date()} to {period_end.date()}",
            "revenue": revenue,
            "cogs": self.get_cogs(),
            "gross_profit": gross_profit,
            "operating_expenses": operating_expenses,
            "operating_income": operating_income,
            "interest_expense": interest_expense,
            "tax_expense": tax_expense,
            "net_income": net_income,
            "eps": self.calculate_eps(net_income)
        }

    def generate_cash_flow_statement(self) -> dict:
        """Generate cash flow statement"""
        return {
            "operating_activities": self.calculate_operating_cash_flow(),
            "investing_activities": self.calculate_investing_cash_flow(),
            "financing_activities": self.calculate_financing_cash_flow(),
            "net_change_in_cash": self.calculate_net_cash_change(),
            "beginning_cash": self.get_beginning_cash(),
            "ending_cash": self.get_ending_cash()
        }
```

## Tax Calculations

```python
class TaxCalculator:
    def calculate_corporate_tax(self, taxable_income: Decimal,
                                jurisdiction: str = "US") -> dict:
        """Calculate corporate income tax"""
        if jurisdiction == "US":
            tax_rate = Decimal('0.21')  # Federal rate
        elif jurisdiction == "UK":
            tax_rate = Decimal('0.19')
        else:
            tax_rate = Decimal('0.25')  # Default rate

        tax_amount = taxable_income * tax_rate

        return {
            "taxable_income": taxable_income,
            "tax_rate": tax_rate,
            "tax_amount": tax_amount.quantize(Decimal('0.01')),
            "effective_rate": tax_rate,
            "jurisdiction": jurisdiction
        }

    def calculate_vat(self, net_amount: Decimal, vat_rate: Decimal) -> dict:
        """Calculate VAT/Sales tax"""
        vat_amount = net_amount * vat_rate
        gross_amount = net_amount + vat_amount

        return {
            "net_amount": net_amount,
            "vat_rate": vat_rate,
            "vat_amount": vat_amount.quantize(Decimal('0.01')),
            "gross_amount": gross_amount.quantize(Decimal('0.01'))
        }

    def calculate_depreciation(self, cost: Decimal, salvage_value: Decimal,
                              useful_life_years: int,
                              method: str = "straight_line") -> List[dict]:
        """Calculate depreciation schedule"""
        if method == "straight_line":
            annual_depreciation = (cost - salvage_value) / useful_life_years

            schedule = []
            book_value = cost

            for year in range(1, useful_life_years + 1):
                depreciation = annual_depreciation
                book_value -= depreciation

                schedule.append({
                    "year": year,
                    "depreciation": depreciation.quantize(Decimal('0.01')),
                    "accumulated_depreciation": (annual_depreciation * year).quantize(Decimal('0.01')),
                    "book_value": book_value.quantize(Decimal('0.01'))
                })

            return schedule
```

## Financial Ratios

```python
class FinancialRatios:
    @staticmethod
    def current_ratio(current_assets: Decimal, current_liabilities: Decimal) -> Decimal:
        """Liquidity ratio: Current Assets / Current Liabilities"""
        return (current_assets / current_liabilities).quantize(Decimal('0.01'))

    @staticmethod
    def quick_ratio(current_assets: Decimal, inventory: Decimal,
                    current_liabilities: Decimal) -> Decimal:
        """Acid test: (Current Assets - Inventory) / Current Liabilities"""
        return ((current_assets - inventory) / current_liabilities).quantize(Decimal('0.01'))

    @staticmethod
    def debt_to_equity(total_debt: Decimal, total_equity: Decimal) -> Decimal:
        """Leverage ratio: Total Debt / Total Equity"""
        return (total_debt / total_equity).quantize(Decimal('0.01'))

    @staticmethod
    def return_on_equity(net_income: Decimal, shareholders_equity: Decimal) -> Decimal:
        """ROE: Net Income / Shareholders' Equity"""
        return (net_income / shareholders_equity * 100).quantize(Decimal('0.01'))

    @staticmethod
    def return_on_assets(net_income: Decimal, total_assets: Decimal) -> Decimal:
        """ROA: Net Income / Total Assets"""
        return (net_income / total_assets * 100).quantize(Decimal('0.01'))

    @staticmethod
    def profit_margin(net_income: Decimal, revenue: Decimal) -> Decimal:
        """Net Profit Margin: Net Income / Revenue"""
        return (net_income / revenue * 100).quantize(Decimal('0.01'))
```

## Best Practices

### Accounting Systems
- Implement proper internal controls
- Segregation of duties
- Regular account reconciliations
- Maintain supporting documentation
- Use accounting software with audit trails
- Regular backups of financial data
- Year-end closing procedures

### Financial Reporting
- Follow GAAP/IFRS standards
- Consistent accounting policies
- Clear disclosure of estimates
- Timely financial statement preparation
- Independent audit for larger entities
- Management discussion and analysis (MD&A)

### Tax Compliance
- Maintain organized tax records
- Track deductible expenses properly
- Timely tax filing and payments
- Quarterly estimated tax payments
- Transfer pricing documentation
- Tax planning throughout the year

## Anti-Patterns

❌ Using cash accounting for large businesses
❌ No account reconciliations
❌ Missing audit trails
❌ Inconsistent revenue recognition
❌ Inadequate internal controls
❌ Poor documentation of transactions
❌ Late tax filing and penalties

## Resources

- FASB (Financial Accounting Standards Board): https://www.fasb.org/
- IFRS Foundation: https://www.ifrs.org/
- IRS Tax Information: https://www.irs.gov/
- AICPA (American Institute of CPAs): https://www.aicpa.org/
