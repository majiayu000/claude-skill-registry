---
name: personal-financial-advisor
description: Master personal finance planning including budgeting, debt management, savings strategies, retirement planning, investment allocation, and financial goal setting. Use when helping individuals manage money, build wealth, reduce debt, or plan for financial milestones.
---

# Personal Financial Advisor

Comprehensive toolkit for personal finance planning, helping individuals achieve financial wellness through budgeting, debt management, savings, investing, and goal-based planning.

## When to Use This Skill

- Creating personal budgets and spending plans
- Developing debt payoff strategies
- Planning emergency funds and savings goals
- Retirement planning and projections
- Investment portfolio allocation for individuals
- Tax optimization for personal finances
- Insurance needs assessment
- Net worth tracking and financial health analysis
- Setting and tracking financial goals

## Core Concepts

### 1. Financial Planning Hierarchy

```
┌─────────────────────────────────────────┐
│         WEALTH BUILDING                 │
│    (Investing, Retirement, Legacy)      │
├─────────────────────────────────────────┤
│         PROTECTION                      │
│    (Insurance, Estate Planning)         │
├─────────────────────────────────────────┤
│         DEBT ELIMINATION                │
│    (High-interest → Low-interest)       │
├─────────────────────────────────────────┤
│         EMERGENCY FUND                  │
│    (3-6 months expenses)                │
├─────────────────────────────────────────┤
│         FOUNDATION                      │
│    (Budget, Cash Flow, Basic Savings)   │
└─────────────────────────────────────────┘
```

### 2. Key Financial Health Metrics

| Metric               | Target       | Formula                           |
| -------------------- | ------------ | --------------------------------- |
| **Savings Rate**     | ≥20%         | Savings / Gross Income            |
| **Debt-to-Income**   | <36%         | Monthly Debt / Monthly Income     |
| **Emergency Fund**   | 3-6 months   | Liquid Savings / Monthly Expenses |
| **Housing Ratio**    | <28%         | Housing Costs / Gross Income      |
| **Net Worth Growth** | Positive YoY | Assets - Liabilities              |

## Budgeting Methods

### Pattern 1: Budgeting Frameworks

```python
from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum
import pandas as pd

class BudgetMethod(Enum):
    FIFTY_THIRTY_TWENTY = "50/30/20"
    ZERO_BASED = "zero_based"
    ENVELOPE = "envelope"
    PAY_YOURSELF_FIRST = "pay_yourself_first"

@dataclass
class Income:
    """Monthly income sources."""
    salary: float
    side_income: float = 0
    investment_income: float = 0
    other: float = 0

    @property
    def total_gross(self) -> float:
        return self.salary + self.side_income + self.investment_income + self.other

    def after_tax(self, tax_rate: float = 0.25) -> float:
        """Calculate after-tax income."""
        return self.total_gross * (1 - tax_rate)

@dataclass
class Expense:
    """Expense item with category."""
    name: str
    amount: float
    category: str  # 'need', 'want', 'savings'
    is_fixed: bool = True

class BudgetPlanner:
    """Personal budget planning and analysis."""

    def __init__(self, income: Income, tax_rate: float = 0.25):
        self.income = income
        self.tax_rate = tax_rate
        self.expenses: List[Expense] = []

    def add_expense(self, expense: Expense) -> None:
        """Add an expense to the budget."""
        self.expenses.append(expense)

    @property
    def monthly_income(self) -> float:
        """After-tax monthly income."""
        return self.income.after_tax(self.tax_rate)

    # ==================== 50/30/20 RULE ====================

    def fifty_thirty_twenty(self) -> Dict[str, float]:
        """
        50/30/20 Budget Rule.

        - 50% Needs: Housing, utilities, groceries, insurance, minimum debt payments
        - 30% Wants: Entertainment, dining out, hobbies, subscriptions
        - 20% Savings: Emergency fund, retirement, investments, extra debt payments
        """
        income = self.monthly_income
        return {
            'needs_budget': income * 0.50,
            'wants_budget': income * 0.30,
            'savings_budget': income * 0.20,
            'needs_actual': sum(e.amount for e in self.expenses if e.category == 'need'),
            'wants_actual': sum(e.amount for e in self.expenses if e.category == 'want'),
            'savings_actual': sum(e.amount for e in self.expenses if e.category == 'savings'),
        }

    def analyze_fifty_thirty_twenty(self) -> Dict[str, any]:
        """Analyze budget against 50/30/20 targets."""
        budget = self.fifty_thirty_twenty()

        return {
            'needs': {
                'budget': budget['needs_budget'],
                'actual': budget['needs_actual'],
                'variance': budget['needs_budget'] - budget['needs_actual'],
                'on_track': budget['needs_actual'] <= budget['needs_budget']
            },
            'wants': {
                'budget': budget['wants_budget'],
                'actual': budget['wants_actual'],
                'variance': budget['wants_budget'] - budget['wants_actual'],
                'on_track': budget['wants_actual'] <= budget['wants_budget']
            },
            'savings': {
                'budget': budget['savings_budget'],
                'actual': budget['savings_actual'],
                'variance': budget['savings_actual'] - budget['savings_budget'],
                'on_track': budget['savings_actual'] >= budget['savings_budget']
            }
        }

    # ==================== ZERO-BASED BUDGETING ====================

    def zero_based_budget(self) -> Dict[str, float]:
        """
        Zero-Based Budgeting.

        Every dollar has a job. Income - All Expenses = $0
        """
        total_expenses = sum(e.amount for e in self.expenses)
        unallocated = self.monthly_income - total_expenses

        return {
            'income': self.monthly_income,
            'total_allocated': total_expenses,
            'unallocated': unallocated,
            'is_balanced': abs(unallocated) < 1.0,  # Within $1
            'expenses_by_category': self._group_expenses_by_category()
        }

    def _group_expenses_by_category(self) -> Dict[str, float]:
        """Group expenses by category."""
        categories = {}
        for expense in self.expenses:
            if expense.category not in categories:
                categories[expense.category] = 0
            categories[expense.category] += expense.amount
        return categories

    # ==================== ENVELOPE SYSTEM ====================

    def envelope_budget(self, envelopes: Dict[str, float]) -> Dict[str, Dict]:
        """
        Envelope Budgeting System.

        Allocate cash to specific spending categories.
        When envelope is empty, stop spending.
        """
        result = {}
        for category, budget in envelopes.items():
            spent = sum(e.amount for e in self.expenses if e.category == category)
            result[category] = {
                'budget': budget,
                'spent': spent,
                'remaining': budget - spent,
                'percent_used': (spent / budget * 100) if budget > 0 else 0
            }
        return result

    # ==================== PAY YOURSELF FIRST ====================

    def pay_yourself_first(self, savings_target_percent: float = 0.20) -> Dict[str, float]:
        """
        Pay Yourself First Strategy.

        Save first, then budget the rest for expenses.
        """
        savings_amount = self.monthly_income * savings_target_percent
        spending_budget = self.monthly_income - savings_amount
        actual_spending = sum(e.amount for e in self.expenses if e.category != 'savings')

        return {
            'target_savings': savings_amount,
            'spending_budget': spending_budget,
            'actual_spending': actual_spending,
            'spending_variance': spending_budget - actual_spending,
            'on_track': actual_spending <= spending_budget
        }

    # ==================== SAVINGS RATE ====================

    def calculate_savings_rate(self) -> float:
        """Calculate monthly savings rate."""
        savings = sum(e.amount for e in self.expenses if e.category == 'savings')
        return savings / self.income.total_gross if self.income.total_gross > 0 else 0
```

### Pattern 2: Debt Management Strategies

```python
from dataclasses import dataclass
from typing import List, Dict
import numpy as np

@dataclass
class Debt:
    """Individual debt account."""
    name: str
    balance: float
    interest_rate: float  # Annual rate as decimal
    minimum_payment: float

    def monthly_interest(self) -> float:
        """Calculate monthly interest charge."""
        return self.balance * (self.interest_rate / 12)

class DebtPayoffCalculator:
    """Debt payoff strategy calculator."""

    def __init__(self, debts: List[Debt], extra_payment: float = 0):
        self.debts = debts
        self.extra_payment = extra_payment

    @property
    def total_debt(self) -> float:
        return sum(d.balance for d in self.debts)

    @property
    def total_minimum_payments(self) -> float:
        return sum(d.minimum_payment for d in self.debts)

    @property
    def weighted_avg_rate(self) -> float:
        """Calculate weighted average interest rate."""
        if self.total_debt == 0:
            return 0
        return sum(d.balance * d.interest_rate for d in self.debts) / self.total_debt

    # ==================== DEBT SNOWBALL ====================

    def debt_snowball(self) -> Dict:
        """
        Debt Snowball Method.

        Pay minimum on all debts, put extra toward SMALLEST balance first.
        Psychological wins build momentum.
        """
        # Sort by balance (smallest first)
        sorted_debts = sorted(self.debts, key=lambda d: d.balance)
        return self._simulate_payoff(sorted_debts, "snowball")

    # ==================== DEBT AVALANCHE ====================

    def debt_avalanche(self) -> Dict:
        """
        Debt Avalanche Method.

        Pay minimum on all debts, put extra toward HIGHEST interest rate first.
        Mathematically optimal - minimizes total interest paid.
        """
        # Sort by interest rate (highest first)
        sorted_debts = sorted(self.debts, key=lambda d: d.interest_rate, reverse=True)
        return self._simulate_payoff(sorted_debts, "avalanche")

    def _simulate_payoff(self, sorted_debts: List[Debt], method: str) -> Dict:
        """Simulate debt payoff over time."""
        # Create working copies
        balances = {d.name: d.balance for d in sorted_debts}
        rates = {d.name: d.interest_rate for d in sorted_debts}
        minimums = {d.name: d.minimum_payment for d in sorted_debts}

        total_paid = 0
        total_interest = 0
        months = 0
        payoff_order = []
        monthly_schedule = []

        while any(b > 0 for b in balances.values()):
            months += 1
            if months > 360:  # 30 year cap
                break

            month_interest = 0
            month_principal = 0
            extra_remaining = self.extra_payment

            # Apply interest to all debts
            for name in balances:
                if balances[name] > 0:
                    interest = balances[name] * (rates[name] / 12)
                    balances[name] += interest
                    month_interest += interest

            # Pay minimums on all debts
            for name in balances:
                if balances[name] > 0:
                    payment = min(minimums[name], balances[name])
                    balances[name] -= payment
                    month_principal += payment

                    if balances[name] <= 0:
                        balances[name] = 0
                        payoff_order.append({'name': name, 'month': months})
                        extra_remaining += minimums[name]  # Freed up payment

            # Apply extra payment to target debt
            for debt in sorted_debts:
                if balances[debt.name] > 0 and extra_remaining > 0:
                    payment = min(extra_remaining, balances[debt.name])
                    balances[debt.name] -= payment
                    month_principal += payment
                    extra_remaining -= payment

                    if balances[debt.name] <= 0:
                        balances[debt.name] = 0
                        payoff_order.append({'name': debt.name, 'month': months})

            total_interest += month_interest
            total_paid += month_interest + month_principal

            monthly_schedule.append({
                'month': months,
                'interest_paid': month_interest,
                'principal_paid': month_principal,
                'remaining_balance': sum(balances.values())
            })

        return {
            'method': method,
            'months_to_payoff': months,
            'years_to_payoff': months / 12,
            'total_paid': total_paid,
            'total_interest': total_interest,
            'original_balance': self.total_debt,
            'payoff_order': payoff_order,
            'monthly_schedule': monthly_schedule
        }

    def compare_methods(self) -> Dict:
        """Compare snowball vs avalanche methods."""
        snowball = self.debt_snowball()
        avalanche = self.debt_avalanche()

        return {
            'snowball': snowball,
            'avalanche': avalanche,
            'interest_savings': snowball['total_interest'] - avalanche['total_interest'],
            'time_difference_months': snowball['months_to_payoff'] - avalanche['months_to_payoff'],
            'recommended': 'avalanche' if avalanche['total_interest'] < snowball['total_interest'] else 'snowball'
        }
```

### Pattern 3: Emergency Fund Calculator

```python
@dataclass
class MonthlyExpenses:
    """Monthly essential expenses."""
    housing: float  # Rent/mortgage
    utilities: float
    groceries: float
    transportation: float
    insurance: float
    minimum_debt_payments: float
    other_essentials: float = 0

    @property
    def total(self) -> float:
        return (
            self.housing + self.utilities + self.groceries +
            self.transportation + self.insurance +
            self.minimum_debt_payments + self.other_essentials
        )

class EmergencyFundPlanner:
    """Emergency fund planning and tracking."""

    def __init__(
        self,
        monthly_expenses: MonthlyExpenses,
        current_savings: float = 0,
        job_stability: str = "stable"  # stable, moderate, unstable
    ):
        self.expenses = monthly_expenses
        self.current_savings = current_savings
        self.job_stability = job_stability

    def recommended_months(self) -> int:
        """Get recommended emergency fund months based on job stability."""
        recommendations = {
            "stable": 3,       # Stable job, dual income
            "moderate": 6,    # Single income, some variability
            "unstable": 9,    # Freelance, commission-based, volatile industry
            "self_employed": 12  # Business owners
        }
        return recommendations.get(self.job_stability, 6)

    def target_amount(self) -> float:
        """Calculate target emergency fund amount."""
        return self.expenses.total * self.recommended_months()

    def current_coverage(self) -> float:
        """Calculate current months of coverage."""
        return self.current_savings / self.expenses.total if self.expenses.total > 0 else 0

    def gap_analysis(self) -> Dict:
        """Analyze emergency fund gap."""
        target = self.target_amount()
        gap = max(0, target - self.current_savings)

        return {
            'target_months': self.recommended_months(),
            'target_amount': target,
            'current_savings': self.current_savings,
            'current_months_coverage': self.current_coverage(),
            'gap_amount': gap,
            'percent_funded': (self.current_savings / target * 100) if target > 0 else 100,
            'is_fully_funded': self.current_savings >= target
        }

    def savings_plan(self, monthly_contribution: float) -> Dict:
        """Create plan to reach emergency fund target."""
        gap = self.gap_analysis()['gap_amount']

        if gap <= 0:
            return {'already_funded': True, 'months_to_goal': 0}

        months_to_goal = gap / monthly_contribution if monthly_contribution > 0 else float('inf')

        return {
            'already_funded': False,
            'gap_amount': gap,
            'monthly_contribution': monthly_contribution,
            'months_to_goal': months_to_goal,
            'years_to_goal': months_to_goal / 12,
            'target_date_months': int(np.ceil(months_to_goal))
        }
```

### Pattern 4: Retirement Planning

```python
class RetirementPlanner:
    """Retirement savings and projection calculator."""

    def __init__(
        self,
        current_age: int,
        retirement_age: int,
        current_savings: float,
        annual_contribution: float,
        expected_return: float = 0.07,  # 7% average market return
        inflation_rate: float = 0.03
    ):
        self.current_age = current_age
        self.retirement_age = retirement_age
        self.current_savings = current_savings
        self.annual_contribution = annual_contribution
        self.expected_return = expected_return
        self.inflation_rate = inflation_rate

    @property
    def years_to_retirement(self) -> int:
        return max(0, self.retirement_age - self.current_age)

    def future_value(self) -> float:
        """
        Calculate future value of retirement savings.

        FV = PV × (1 + r)^n + PMT × [((1 + r)^n - 1) / r]
        """
        n = self.years_to_retirement
        r = self.expected_return

        # Future value of current savings
        fv_current = self.current_savings * ((1 + r) ** n)

        # Future value of annual contributions (annuity)
        if r > 0:
            fv_contributions = self.annual_contribution * (((1 + r) ** n - 1) / r)
        else:
            fv_contributions = self.annual_contribution * n

        return fv_current + fv_contributions

    def real_future_value(self) -> float:
        """Future value adjusted for inflation (today's dollars)."""
        nominal_fv = self.future_value()
        return nominal_fv / ((1 + self.inflation_rate) ** self.years_to_retirement)

    def retirement_income(self, withdrawal_rate: float = 0.04) -> Dict:
        """
        Calculate sustainable retirement income using 4% rule.

        The 4% rule: Withdraw 4% of portfolio in year 1, then adjust for inflation.
        """
        portfolio = self.future_value()
        real_portfolio = self.real_future_value()

        return {
            'portfolio_at_retirement': portfolio,
            'portfolio_real_value': real_portfolio,
            'annual_income_nominal': portfolio * withdrawal_rate,
            'annual_income_real': real_portfolio * withdrawal_rate,
            'monthly_income_nominal': portfolio * withdrawal_rate / 12,
            'monthly_income_real': real_portfolio * withdrawal_rate / 12
        }

    def required_savings_for_income(
        self,
        target_annual_income: float,
        withdrawal_rate: float = 0.04
    ) -> Dict:
        """Calculate required savings to achieve target retirement income."""
        required_portfolio = target_annual_income / withdrawal_rate

        # Solve for required annual contribution
        # FV = PV × (1 + r)^n + PMT × [((1 + r)^n - 1) / r]
        # PMT = (FV - PV × (1 + r)^n) / [((1 + r)^n - 1) / r]

        n = self.years_to_retirement
        r = self.expected_return

        fv_current = self.current_savings * ((1 + r) ** n)
        remaining_needed = required_portfolio - fv_current

        if r > 0 and n > 0:
            annuity_factor = ((1 + r) ** n - 1) / r
            required_annual = remaining_needed / annuity_factor
        else:
            required_annual = remaining_needed / max(n, 1)

        return {
            'target_annual_income': target_annual_income,
            'required_portfolio': required_portfolio,
            'current_trajectory': self.future_value(),
            'gap': max(0, required_portfolio - self.future_value()),
            'required_annual_contribution': max(0, required_annual),
            'required_monthly_contribution': max(0, required_annual / 12)
        }

    def compound_growth_schedule(self) -> List[Dict]:
        """Generate year-by-year growth projection."""
        schedule = []
        balance = self.current_savings

        for year in range(self.years_to_retirement + 1):
            age = self.current_age + year

            schedule.append({
                'year': year,
                'age': age,
                'starting_balance': balance,
                'contribution': self.annual_contribution if year > 0 else 0,
                'growth': balance * self.expected_return if year > 0 else 0,
                'ending_balance': balance
            })

            if year < self.years_to_retirement:
                balance = balance * (1 + self.expected_return) + self.annual_contribution

        # Update ending balances
        for i in range(len(schedule) - 1):
            schedule[i]['ending_balance'] = schedule[i + 1]['starting_balance']
        schedule[-1]['ending_balance'] = balance

        return schedule

    # ==================== RETIREMENT ACCOUNT OPTIMIZATION ====================

    def contribution_priority(
        self,
        has_employer_401k: bool = True,
        employer_match_percent: float = 0.03,
        has_hsa: bool = False
    ) -> List[str]:
        """
        Recommended contribution priority order.

        Standard priority:
        1. 401(k) up to employer match (free money)
        2. HSA (triple tax advantage)
        3. Max out Roth IRA
        4. Max out 401(k)
        5. Taxable brokerage
        """
        priority = []

        if has_employer_401k and employer_match_percent > 0:
            priority.append(f"1. 401(k) to employer match ({employer_match_percent*100:.0f}%)")

        if has_hsa:
            priority.append("2. Max HSA ($4,150 individual / $8,300 family 2024)")

        priority.extend([
            "3. Max Roth IRA ($7,000 / $8,000 if 50+ in 2024)",
            "4. Max 401(k) ($23,000 / $30,500 if 50+ in 2024)",
            "5. Taxable brokerage account"
        ])

        return priority
```

### Pattern 5: Investment Portfolio Allocation

```python
class PortfolioAllocator:
    """Personal investment portfolio allocation."""

    def __init__(self, age: int, risk_tolerance: str = "moderate"):
        self.age = age
        self.risk_tolerance = risk_tolerance  # conservative, moderate, aggressive

    def age_based_allocation(self) -> Dict[str, float]:
        """
        Age-based asset allocation rule.

        Traditional: Bonds = Age (e.g., 30 years old = 30% bonds)
        Modern: Bonds = Age - 20 (more aggressive for longer life expectancy)
        """
        # Modern rule (age - 20)
        bond_percent = max(0, min(80, self.age - 20)) / 100
        stock_percent = 1 - bond_percent

        return {
            'stocks': stock_percent,
            'bonds': bond_percent,
            'rationale': f"At age {self.age}, allocate {stock_percent*100:.0f}% stocks, {bond_percent*100:.0f}% bonds"
        }

    def risk_based_allocation(self) -> Dict[str, float]:
        """Allocation based on risk tolerance."""
        allocations = {
            "conservative": {
                'stocks': 0.30,
                'bonds': 0.50,
                'cash': 0.20
            },
            "moderate": {
                'stocks': 0.60,
                'bonds': 0.30,
                'cash': 0.10
            },
            "aggressive": {
                'stocks': 0.80,
                'bonds': 0.15,
                'cash': 0.05
            },
            "very_aggressive": {
                'stocks': 0.95,
                'bonds': 0.05,
                'cash': 0.00
            }
        }
        return allocations.get(self.risk_tolerance, allocations["moderate"])

    def three_fund_portfolio(self, international_percent: float = 0.30) -> Dict[str, float]:
        """
        Three-Fund Portfolio (Bogleheads approach).

        Simple, low-cost, diversified portfolio:
        1. US Total Stock Market
        2. International Stock Market
        3. US Total Bond Market
        """
        base = self.age_based_allocation()
        stock_allocation = base['stocks']
        bond_allocation = base['bonds']

        return {
            'us_total_stock': stock_allocation * (1 - international_percent),
            'international_stock': stock_allocation * international_percent,
            'us_total_bond': bond_allocation,
            'total': 1.0,
            'example_funds': {
                'us_total_stock': 'VTI, VTSAX, FSKAX',
                'international_stock': 'VXUS, VTIAX, FTIHX',
                'us_total_bond': 'BND, VBTLX, FXNAX'
            }
        }

    def target_date_equivalent(self, retirement_year: int) -> Dict:
        """Calculate allocation similar to target-date funds."""
        years_to_retirement = retirement_year - 2024

        if years_to_retirement > 40:
            stocks = 0.90
        elif years_to_retirement > 25:
            stocks = 0.85
        elif years_to_retirement > 15:
            stocks = 0.75
        elif years_to_retirement > 5:
            stocks = 0.60
        elif years_to_retirement > 0:
            stocks = 0.50
        else:  # In retirement
            stocks = 0.40

        return {
            'retirement_year': retirement_year,
            'years_to_retirement': years_to_retirement,
            'stocks': stocks,
            'bonds': 1 - stocks,
            'glide_path': "Becomes more conservative as retirement approaches"
        }
```

### Pattern 6: Net Worth Tracker

```python
@dataclass
class FinancialSnapshot:
    """Point-in-time financial snapshot."""
    date: str

    # Assets
    checking: float = 0
    savings: float = 0
    investments: float = 0  # Brokerage accounts
    retirement_401k: float = 0
    retirement_ira: float = 0
    home_value: float = 0
    vehicle_value: float = 0
    other_assets: float = 0

    # Liabilities
    mortgage: float = 0
    auto_loans: float = 0
    student_loans: float = 0
    credit_cards: float = 0
    other_debt: float = 0

    @property
    def total_assets(self) -> float:
        return (
            self.checking + self.savings + self.investments +
            self.retirement_401k + self.retirement_ira +
            self.home_value + self.vehicle_value + self.other_assets
        )

    @property
    def liquid_assets(self) -> float:
        return self.checking + self.savings + self.investments

    @property
    def retirement_assets(self) -> float:
        return self.retirement_401k + self.retirement_ira

    @property
    def total_liabilities(self) -> float:
        return (
            self.mortgage + self.auto_loans + self.student_loans +
            self.credit_cards + self.other_debt
        )

    @property
    def net_worth(self) -> float:
        return self.total_assets - self.total_liabilities

class NetWorthTracker:
    """Track net worth over time."""

    def __init__(self):
        self.snapshots: List[FinancialSnapshot] = []

    def add_snapshot(self, snapshot: FinancialSnapshot) -> None:
        """Add a financial snapshot."""
        self.snapshots.append(snapshot)
        self.snapshots.sort(key=lambda s: s.date)

    def current_net_worth(self) -> float:
        """Get most recent net worth."""
        return self.snapshots[-1].net_worth if self.snapshots else 0

    def net_worth_change(self, periods: int = 1) -> Dict:
        """Calculate net worth change over periods."""
        if len(self.snapshots) < 2:
            return {'change': 0, 'percent_change': 0}

        current = self.snapshots[-1].net_worth
        previous = self.snapshots[-min(periods + 1, len(self.snapshots))].net_worth
        change = current - previous

        return {
            'current': current,
            'previous': previous,
            'change': change,
            'percent_change': (change / previous * 100) if previous != 0 else 0
        }

    def financial_ratios(self) -> Dict[str, float]:
        """Calculate key financial health ratios."""
        if not self.snapshots:
            return {}

        latest = self.snapshots[-1]

        return {
            'liquidity_ratio': latest.liquid_assets / latest.total_liabilities if latest.total_liabilities > 0 else float('inf'),
            'debt_to_asset': latest.total_liabilities / latest.total_assets if latest.total_assets > 0 else 0,
            'emergency_fund_months': latest.liquid_assets / (latest.total_liabilities + 1),  # Rough estimate
            'retirement_progress': latest.retirement_assets / latest.total_assets if latest.total_assets > 0 else 0
        }

    def asset_allocation(self) -> Dict[str, float]:
        """Current asset allocation breakdown."""
        if not self.snapshots:
            return {}

        latest = self.snapshots[-1]
        total = latest.total_assets

        if total == 0:
            return {}

        return {
            'cash': (latest.checking + latest.savings) / total,
            'investments': latest.investments / total,
            'retirement': latest.retirement_assets / total,
            'real_estate': latest.home_value / total,
            'other': (latest.vehicle_value + latest.other_assets) / total
        }
```

### Pattern 7: Financial Goal Planner

```python
from datetime import datetime, timedelta
from typing import List, Dict, Optional

@dataclass
class FinancialGoal:
    """SMART financial goal."""
    name: str
    target_amount: float
    target_date: str  # YYYY-MM-DD
    current_savings: float = 0
    priority: int = 1  # 1 = highest priority

    @property
    def remaining_amount(self) -> float:
        return max(0, self.target_amount - self.current_savings)

    @property
    def percent_complete(self) -> float:
        return (self.current_savings / self.target_amount * 100) if self.target_amount > 0 else 100

    @property
    def months_remaining(self) -> int:
        target = datetime.strptime(self.target_date, "%Y-%m-%d")
        today = datetime.now()
        delta = target - today
        return max(0, delta.days // 30)

class GoalPlanner:
    """Multi-goal financial planning."""

    def __init__(self, monthly_savings_budget: float):
        self.monthly_budget = monthly_savings_budget
        self.goals: List[FinancialGoal] = []

    def add_goal(self, goal: FinancialGoal) -> None:
        """Add a financial goal."""
        self.goals.append(goal)
        self.goals.sort(key=lambda g: g.priority)

    def analyze_goal(self, goal: FinancialGoal) -> Dict:
        """Analyze single goal feasibility."""
        months = goal.months_remaining
        required_monthly = goal.remaining_amount / months if months > 0 else goal.remaining_amount

        return {
            'goal': goal.name,
            'target_amount': goal.target_amount,
            'current_savings': goal.current_savings,
            'remaining': goal.remaining_amount,
            'percent_complete': goal.percent_complete,
            'months_remaining': months,
            'required_monthly': required_monthly,
            'is_achievable': required_monthly <= self.monthly_budget,
            'surplus_deficit': self.monthly_budget - required_monthly
        }

    def allocate_to_goals(self) -> Dict[str, float]:
        """Allocate monthly savings across goals by priority."""
        allocations = {}
        remaining_budget = self.monthly_budget

        for goal in self.goals:
            analysis = self.analyze_goal(goal)
            required = analysis['required_monthly']

            allocation = min(required, remaining_budget)
            allocations[goal.name] = {
                'allocated': allocation,
                'required': required,
                'shortfall': max(0, required - allocation)
            }
            remaining_budget -= allocation

        allocations['unallocated'] = remaining_budget
        return allocations

    def summary(self) -> Dict:
        """Generate goals summary."""
        total_needed = sum(g.remaining_amount for g in self.goals)
        total_monthly_required = sum(
            self.analyze_goal(g)['required_monthly'] for g in self.goals
        )

        return {
            'total_goals': len(self.goals),
            'total_amount_needed': total_needed,
            'total_monthly_required': total_monthly_required,
            'monthly_budget': self.monthly_budget,
            'budget_gap': total_monthly_required - self.monthly_budget,
            'can_achieve_all': total_monthly_required <= self.monthly_budget
        }
```

## Quick Reference

### Key Rules of Thumb

```python
# Budgeting
FIFTY_THIRTY_TWENTY = "50% needs, 30% wants, 20% savings"
PAY_YOURSELF_FIRST = "Save before you spend"

# Emergency Fund
EMERGENCY_FUND = "3-6 months of essential expenses"
STABLE_JOB = 3  # months
UNSTABLE_JOB = 6  # months
SELF_EMPLOYED = 12  # months

# Debt
DEBT_TO_INCOME_LIMIT = 0.36  # 36% max
HOUSING_RATIO_LIMIT = 0.28  # 28% max

# Retirement
SAVINGS_RATE_TARGET = 0.15  # 15% of income minimum
RULE_OF_25 = "Save 25x annual expenses for retirement"
FOUR_PERCENT_RULE = "Withdraw 4% annually in retirement"

# Investing
STOCKS_ALLOCATION = lambda age: 100 - age  # or 110 - age (aggressive)
```

### Financial Health Scorecard

| Metric             | Poor       | Fair       | Good    | Excellent    |
| ------------------ | ---------- | ---------- | ------- | ------------ |
| Savings Rate       | <5%        | 5-10%      | 10-20%  | >20%         |
| Emergency Fund     | <1 mo      | 1-3 mo     | 3-6 mo  | >6 mo        |
| Debt-to-Income     | >50%       | 36-50%     | 20-36%  | <20%         |
| Retirement Savings | <1x salary | 1-3x       | 3-6x    | >6x          |
| Net Worth          | Negative   | Break-even | Growing | Accelerating |

## Best Practices

### Do's

- **Pay yourself first** - Automate savings before spending
- **Build emergency fund before investing** - Foundation first
- **Take full employer match** - It's free money
- **Track net worth monthly** - What gets measured improves
- **Review and rebalance annually** - Stay on track
- **Increase savings with raises** - Avoid lifestyle inflation

### Don'ts

- **Don't skip emergency fund** - Debt can spiral without buffer
- **Don't time the market** - Consistent investing beats timing
- **Don't ignore high-interest debt** - Paying 20% interest beats 7% returns
- **Don't over-leverage housing** - Stay under 28% of income
- **Don't neglect insurance** - Protect against catastrophic loss
- **Don't compare to others** - Focus on your own progress

## Common Pitfalls

| Pitfall                | Impact         | Solution                    |
| ---------------------- | -------------- | --------------------------- |
| No budget              | Overspending   | Use 50/30/20 rule           |
| No emergency fund      | Debt spiral    | Build 3-6 months first      |
| Only saving in 401k    | Limited access | Balance with Roth & taxable |
| Too conservative young | Missed growth  | Age - 20 = bond percentage  |
| Lifestyle inflation    | Never catch up | Save raises & bonuses       |

## Resources

- [Bogleheads Investment Philosophy](https://www.bogleheads.org/wiki/Bogleheads_investment_philosophy)
- [NerdWallet Financial Calculators](https://www.nerdwallet.com/calculators)
- [Mr. Money Mustache - Financial Independence](https://www.mrmoneymustache.com/)
- [The Simple Path to Wealth (JL Collins)](https://jlcollinsnh.com/)


## Parent Hub
- [_business-finance-mastery](../_business-finance-mastery/SKILL.md)
