---
name: procurement-optimization
description: When the user wants to optimize procurement decisions, allocate orders across suppliers, or determine optimal order quantities. Also use when the user mentions "order allocation," "supplier portfolio optimization," "lot sizing," "order splitting," "purchase optimization," "EOQ," "sourcing optimization," or "multi-sourcing strategy." For supplier selection, see supplier-selection. For spend analysis, see spend-analysis.
---

# Procurement Optimization

You are an expert in procurement optimization and decision science. Your goal is to help organizations make optimal purchasing decisions that minimize total costs while meeting requirements for service levels, capacity constraints, and risk management.

## Initial Assessment

Before optimizing procurement, understand:

1. **Procurement Context**
   - What products/materials are being procured?
   - Current procurement process and pain points?
   - Spend volume and frequency?
   - Number of suppliers and current allocation?

2. **Business Objectives**
   - Primary goal? (cost, service, risk, sustainability)
   - Cost components? (price, freight, duties, carrying)
   - Service level requirements?
   - Risk tolerance?

3. **Constraints**
   - Supplier capacity limits?
   - Minimum order quantities (MOQs)?
   - Lead times and delivery windows?
   - Budget or working capital limits?
   - Quality or certification requirements?

4. **Data Availability**
   - Historical demand and order patterns?
   - Supplier pricing (including volume discounts)?
   - Inventory carrying costs?
   - Order processing costs?
   - Transportation and logistics costs?

---

## Procurement Optimization Framework

### Key Decision Areas

**1. Order Quantity Decisions**
- Economic Order Quantity (EOQ)
- Lot-sizing with constraints
- Quantity discount optimization
- Joint replenishment

**2. Supplier Allocation Decisions**
- Single vs. multi-sourcing
- Order splitting across suppliers
- Portfolio optimization
- Supplier diversification

**3. Timing Decisions**
- Reorder points
- Order scheduling
- Lead time management
- Safety stock levels

**4. Contract Decisions**
- Fixed vs. flexible quantities
- Price vs. volume commitments
- Long-term vs. spot buying
- Options and hedging

---

## Economic Order Quantity (EOQ)

### Classic EOQ Model

**Assumptions:**
- Constant demand rate
- Instantaneous replenishment
- No stockouts
- Fixed ordering cost and carrying cost

**Formula:**
```
EOQ = √(2 × D × S / H)

Where:
D = Annual demand (units)
S = Fixed ordering cost per order
H = Annual holding cost per unit
```

```python
import numpy as np
import matplotlib.pyplot as plt

def economic_order_quantity(annual_demand, order_cost, holding_cost_rate, unit_cost):
    """
    Calculate Economic Order Quantity

    Parameters:
    - annual_demand: units per year
    - order_cost: fixed cost per order ($)
    - holding_cost_rate: % of unit cost (e.g., 0.25 for 25%)
    - unit_cost: cost per unit ($)

    Returns:
    - EOQ, total annual cost, number of orders
    """

    holding_cost_per_unit = unit_cost * holding_cost_rate

    # EOQ formula
    eoq = np.sqrt((2 * annual_demand * order_cost) / holding_cost_per_unit)

    # Number of orders per year
    num_orders = annual_demand / eoq

    # Total annual cost
    ordering_cost = num_orders * order_cost
    holding_cost = (eoq / 2) * holding_cost_per_unit
    purchase_cost = annual_demand * unit_cost
    total_cost = ordering_cost + holding_cost + purchase_cost

    return {
        'eoq': round(eoq, 0),
        'num_orders_per_year': round(num_orders, 1),
        'order_frequency_days': round(365 / num_orders, 1),
        'total_annual_cost': round(total_cost, 2),
        'ordering_cost': round(ordering_cost, 2),
        'holding_cost': round(holding_cost, 2),
        'purchase_cost': round(purchase_cost, 2)
    }


# Example
result = economic_order_quantity(
    annual_demand=10000,      # 10,000 units/year
    order_cost=100,           # $100 per order
    holding_cost_rate=0.25,   # 25% carrying cost
    unit_cost=50              # $50/unit
)

print(f"Optimal Order Quantity: {result['eoq']} units")
print(f"Order Frequency: Every {result['order_frequency_days']} days")
print(f"Total Annual Cost: ${result['total_annual_cost']:,.0f}")
```

### EOQ with Quantity Discounts

**All-Units Discount:**
- Price break at certain volume levels
- All units purchased at discounted price

```python
def eoq_quantity_discounts(annual_demand, order_cost, holding_cost_rate, price_breaks):
    """
    EOQ with all-units quantity discounts

    price_breaks: list of (quantity, unit_price) tuples
    Example: [(0, 50), (500, 48), (1000, 46)]
    """

    price_breaks = sorted(price_breaks, key=lambda x: x[0])

    best_option = None
    best_cost = float('inf')

    for i, (min_qty, unit_price) in enumerate(price_breaks):
        holding_cost = unit_price * holding_cost_rate

        # Calculate EOQ for this price
        eoq = np.sqrt((2 * annual_demand * order_cost) / holding_cost)

        # Determine feasible order quantity
        if i < len(price_breaks) - 1:
            max_qty = price_breaks[i + 1][0] - 1
        else:
            max_qty = float('inf')

        if eoq < min_qty:
            order_qty = min_qty  # Use minimum quantity for this price tier
        elif eoq > max_qty:
            continue  # EOQ not feasible in this tier
        else:
            order_qty = eoq

        # Calculate total cost
        num_orders = annual_demand / order_qty
        ordering_cost = num_orders * order_cost
        holding_cost_annual = (order_qty / 2) * holding_cost
        purchase_cost = annual_demand * unit_price
        total_cost = ordering_cost + holding_cost_annual + purchase_cost

        if total_cost < best_cost:
            best_cost = total_cost
            best_option = {
                'order_quantity': round(order_qty, 0),
                'unit_price': unit_price,
                'num_orders': round(num_orders, 1),
                'total_cost': round(total_cost, 2),
                'ordering_cost': round(ordering_cost, 2),
                'holding_cost': round(holding_cost_annual, 2),
                'purchase_cost': round(purchase_cost, 2)
            }

    return best_option


# Example with quantity discounts
price_breaks = [
    (0, 50),      # $50/unit for 0-499
    (500, 48),    # $48/unit for 500-999
    (1000, 46),   # $46/unit for 1000+
    (2000, 44)    # $44/unit for 2000+
]

result = eoq_quantity_discounts(
    annual_demand=10000,
    order_cost=100,
    holding_cost_rate=0.25,
    price_breaks=price_breaks
)

print(f"Optimal Order Quantity: {result['order_quantity']} units")
print(f"Unit Price: ${result['unit_price']}")
print(f"Total Annual Cost: ${result['total_cost']:,.0f}")
print(f"  Purchase: ${result['purchase_cost']:,.0f}")
print(f"  Ordering: ${result['ordering_cost']:,.0f}")
print(f"  Holding: ${result['holding_cost']:,.0f}")
```

---

## Supplier Allocation Optimization

### Multi-Sourcing Problem

**Objective:**
Allocate orders across multiple suppliers to minimize total cost while meeting capacity, quality, and risk constraints.

**Mathematical Formulation:**

```
Decision Variables:
  x_i = quantity ordered from supplier i

Objective:
  Minimize: Σ (p_i × x_i + f_i × y_i + t_i × x_i)

Where:
  p_i = unit price from supplier i
  f_i = fixed ordering cost from supplier i
  t_i = transportation cost per unit from supplier i
  y_i = binary (1 if order from supplier i, 0 otherwise)

Constraints:
  Σ x_i >= D                    (meet demand)
  x_i <= C_i × y_i              (supplier capacity)
  x_i >= MOQ_i × y_i            (minimum order quantity)
  Σ (q_i × x_i) / Σ x_i >= Q   (average quality requirement)
  x_i / Σ x_i <= R_max          (diversification - max % per supplier)
```

```python
from pulp import *
import pandas as pd

def optimize_supplier_allocation(suppliers, demand, constraints=None):
    """
    Optimize order allocation across multiple suppliers

    suppliers: DataFrame with columns:
        - supplier_id, unit_price, fixed_cost, capacity, moq,
          transport_cost, quality_score, lead_time

    demand: total quantity needed

    constraints: dict with optional keys:
        - min_quality: minimum average quality score
        - max_supplier_share: max % of demand from one supplier
        - max_suppliers: maximum number of suppliers to use
    """

    if constraints is None:
        constraints = {}

    # Create problem
    prob = LpProblem("Supplier_Allocation", LpMinimize)

    # Decision variables
    # x[i] = quantity from supplier i
    x = LpVariable.dicts("Quantity",
                        suppliers.index,
                        lowBound=0,
                        cat='Continuous')

    # y[i] = 1 if order from supplier i, 0 otherwise
    y = LpVariable.dicts("Use",
                        suppliers.index,
                        cat='Binary')

    # Objective function: minimize total cost
    prob += (
        # Variable costs (unit price + transport)
        lpSum([(suppliers.loc[i, 'unit_price'] +
                suppliers.loc[i, 'transport_cost']) * x[i]
               for i in suppliers.index]) +

        # Fixed ordering costs
        lpSum([suppliers.loc[i, 'fixed_cost'] * y[i]
               for i in suppliers.index])
    )

    # Constraint 1: Meet total demand
    prob += lpSum([x[i] for i in suppliers.index]) >= demand, "Meet_Demand"

    # Constraint 2: Capacity limits
    for i in suppliers.index:
        prob += x[i] <= suppliers.loc[i, 'capacity'] * y[i], f"Capacity_{i}"

    # Constraint 3: Minimum order quantities
    for i in suppliers.index:
        prob += x[i] >= suppliers.loc[i, 'moq'] * y[i], f"MOQ_{i}"

    # Constraint 4: Quality requirement
    if 'min_quality' in constraints:
        prob += (
            lpSum([suppliers.loc[i, 'quality_score'] * x[i]
                   for i in suppliers.index]) >=
            constraints['min_quality'] * demand,
            "Min_Quality"
        )

    # Constraint 5: Diversification (max share per supplier)
    if 'max_supplier_share' in constraints:
        for i in suppliers.index:
            prob += (
                x[i] <= constraints['max_supplier_share'] * demand,
                f"Max_Share_{i}"
            )

    # Constraint 6: Limit number of suppliers
    if 'max_suppliers' in constraints:
        prob += (
            lpSum([y[i] for i in suppliers.index]) <=
            constraints['max_suppliers'],
            "Max_Suppliers"
        )

    # Solve
    prob.solve(PULP_CBC_CMD(msg=0))

    # Extract results
    if LpStatus[prob.status] != 'Optimal':
        return {'status': LpStatus[prob.status], 'solution': None}

    results = []
    for i in suppliers.index:
        if x[i].varValue > 0.01:
            qty = x[i].varValue
            unit_cost = (suppliers.loc[i, 'unit_price'] +
                        suppliers.loc[i, 'transport_cost'])
            variable_cost = qty * unit_cost
            fixed_cost = suppliers.loc[i, 'fixed_cost']
            total_cost = variable_cost + fixed_cost

            results.append({
                'Supplier': suppliers.loc[i, 'supplier_id'],
                'Quantity': round(qty, 0),
                'Share_%': round(qty / demand * 100, 1),
                'Unit_Cost': unit_cost,
                'Variable_Cost': round(variable_cost, 2),
                'Fixed_Cost': fixed_cost,
                'Total_Cost': round(total_cost, 2),
                'Quality_Score': suppliers.loc[i, 'quality_score'],
                'Lead_Time': suppliers.loc[i, 'lead_time']
            })

    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values('Total_Cost')

    return {
        'status': 'Optimal',
        'total_cost': round(value(prob.objective), 2),
        'allocation': results_df,
        'avg_quality': round(
            (results_df['Quantity'] * results_df['Quality_Score']).sum() /
            results_df['Quantity'].sum(), 2
        ),
        'num_suppliers': len(results_df)
    }


# Example usage
suppliers_data = pd.DataFrame({
    'supplier_id': ['Supplier_A', 'Supplier_B', 'Supplier_C', 'Supplier_D'],
    'unit_price': [10.0, 9.5, 10.5, 9.8],
    'fixed_cost': [500, 400, 600, 450],
    'transport_cost': [1.0, 1.5, 0.8, 1.2],
    'capacity': [5000, 4000, 6000, 3000],
    'moq': [500, 300, 400, 200],
    'quality_score': [9, 8, 10, 8.5],  # 0-10 scale
    'lead_time': [21, 28, 14, 21]  # days
})

result = optimize_supplier_allocation(
    suppliers=suppliers_data,
    demand=8000,
    constraints={
        'min_quality': 8.5,        # Minimum average quality
        'max_supplier_share': 0.6, # Max 60% from one supplier
        'max_suppliers': 3         # Use at most 3 suppliers
    }
)

print(f"Status: {result['status']}")
print(f"Total Cost: ${result['total_cost']:,.2f}")
print(f"Number of Suppliers: {result['num_suppliers']}")
print(f"Average Quality: {result['avg_quality']}/10")
print("\nAllocation:")
print(result['allocation'])
```

### Portfolio Optimization Approach

**Efficient Frontier:**
Trade-off between cost and risk (supplier diversification)

```python
import numpy as np
from scipy.optimize import minimize

def supplier_portfolio_optimization(suppliers_df, demand,
                                   risk_aversion=0.5):
    """
    Optimize supplier portfolio considering cost and risk

    suppliers_df: DataFrame with unit_cost, std_dev (cost volatility)
    risk_aversion: 0 = cost only, 1 = risk only, 0.5 = balanced
    """

    n_suppliers = len(suppliers_df)

    def objective(weights):
        """Minimize weighted combination of cost and risk"""

        # Expected total cost
        expected_cost = np.sum(
            weights * suppliers_df['unit_cost'].values * demand
        )

        # Portfolio risk (variance of cost)
        # Simplified: assumes independence
        cost_variance = np.sum(
            (weights * demand) ** 2 * suppliers_df['std_dev'].values ** 2
        )
        cost_risk = np.sqrt(cost_variance)

        # Combined objective
        return (1 - risk_aversion) * expected_cost + risk_aversion * cost_risk

    # Constraints
    constraints = [
        {'type': 'eq', 'fun': lambda w: np.sum(w) - 1},  # Weights sum to 1
    ]

    # Bounds: each weight between 0 and max_share
    bounds = [(0, 0.6) for _ in range(n_suppliers)]

    # Initial guess: equal weights
    x0 = np.ones(n_suppliers) / n_suppliers

    # Optimize
    result = minimize(objective, x0, method='SLSQP',
                     bounds=bounds, constraints=constraints)

    if result.success:
        weights = result.x
        allocation = weights * demand

        return {
            'weights': weights,
            'allocation': allocation,
            'expected_cost': np.sum(weights * suppliers_df['unit_cost'].values * demand),
            'cost_std': np.sqrt(np.sum((weights * demand) ** 2 *
                                      suppliers_df['std_dev'].values ** 2))
        }
    else:
        return None
```

---

## Advanced Procurement Models

### Joint Replenishment Problem (JRP)

**Multiple Items from Same Supplier:**
- Share fixed ordering cost
- Coordinate order timing
- Minimize total cost

```python
def joint_replenishment_problem(items_df, shared_fixed_cost):
    """
    Joint replenishment for multiple items

    items_df: DataFrame with annual_demand, unit_cost, holding_cost_rate
    shared_fixed_cost: fixed cost incurred per joint order
    """

    # Calculate individual EOQs
    items_df['individual_eoq'] = np.sqrt(
        (2 * items_df['annual_demand'] * shared_fixed_cost) /
        (items_df['unit_cost'] * items_df['holding_cost_rate'])
    )

    # Calculate individual order frequencies
    items_df['frequency'] = items_df['annual_demand'] / items_df['individual_eoq']

    # Basic power-of-two policy
    # Find base frequency (highest frequency)
    base_frequency = items_df['frequency'].max()

    # Assign each item to nearest power-of-2 multiple of base
    items_df['assigned_frequency'] = items_df['frequency'].apply(
        lambda f: base_frequency / (2 ** round(np.log2(base_frequency / f)))
    )

    items_df['order_quantity'] = (
        items_df['annual_demand'] / items_df['assigned_frequency']
    )

    # Calculate costs
    items_df['ordering_cost'] = (
        shared_fixed_cost * items_df['assigned_frequency'] / len(items_df)
    )

    items_df['holding_cost'] = (
        items_df['order_quantity'] / 2 *
        items_df['unit_cost'] *
        items_df['holding_cost_rate']
    )

    items_df['total_cost'] = (
        items_df['ordering_cost'] +
        items_df['holding_cost'] +
        items_df['annual_demand'] * items_df['unit_cost']
    )

    joint_order_frequency = base_frequency
    days_between_orders = 365 / joint_order_frequency

    return {
        'items': items_df,
        'joint_order_frequency': round(joint_order_frequency, 1),
        'days_between_orders': round(days_between_orders, 1),
        'total_annual_cost': round(items_df['total_cost'].sum(), 2)
    }


# Example: 3 items ordered together
items = pd.DataFrame({
    'item': ['Item_A', 'Item_B', 'Item_C'],
    'annual_demand': [5000, 3000, 8000],
    'unit_cost': [10, 25, 5],
    'holding_cost_rate': [0.25, 0.25, 0.25]
})

result = joint_replenishment_problem(items, shared_fixed_cost=200)

print(f"Joint Order Frequency: Every {result['days_between_orders']} days")
print(f"Total Annual Cost: ${result['total_annual_cost']:,.0f}")
print("\nItem Details:")
print(result['items'][['item', 'order_quantity', 'assigned_frequency']])
```

### Dynamic Lot Sizing (Wagner-Whitin)

**Time-Varying Demand:**
- Demand varies by period
- No backorders
- Minimize total cost over planning horizon

```python
def wagner_whitin(demands, setup_cost, holding_cost_per_unit):
    """
    Wagner-Whitin algorithm for dynamic lot sizing

    demands: list of demands by period [d1, d2, d3, ...]
    setup_cost: fixed cost per order
    holding_cost_per_unit: cost to hold 1 unit for 1 period

    Returns: optimal order quantities and total cost
    """

    n_periods = len(demands)

    # DP arrays
    cost = [float('inf')] * (n_periods + 1)
    cost[0] = 0
    order_in = [0] * (n_periods + 1)

    # Forward recursion
    for t in range(1, n_periods + 1):
        for s in range(0, t):
            # Order in period s+1 to cover periods s+1 through t
            cum_demand = sum(demands[s:t])

            # Holding cost: carry inventory forward
            hold_cost = sum(
                (t - k - 1) * demands[k] * holding_cost_per_unit
                for k in range(s, t)
            )

            total_cost = cost[s] + setup_cost + hold_cost

            if total_cost < cost[t]:
                cost[t] = total_cost
                order_in[t] = s + 1

    # Backtrack to find order quantities
    orders = [0] * n_periods
    period = n_periods

    while period > 0:
        order_period = order_in[period]
        order_qty = sum(demands[order_period - 1:period])
        orders[order_period - 1] = order_qty
        period = order_period - 1

    return {
        'order_quantities': orders,
        'total_cost': cost[n_periods],
        'num_orders': sum(1 for q in orders if q > 0)
    }


# Example: 6-period planning horizon
demands = [100, 150, 200, 80, 120, 180]  # Units per period
setup_cost = 500
holding_cost = 2  # $ per unit per period

result = wagner_whitin(demands, setup_cost, holding_cost)

print("Optimal Order Plan:")
for t, qty in enumerate(result['order_quantities'], 1):
    if qty > 0:
        print(f"  Period {t}: Order {qty} units")

print(f"\nTotal Cost: ${result['total_cost']:,.2f}")
print(f"Number of Orders: {result['num_orders']}")
```

---

## Procurement Risk Management

### Supply Risk Metrics

```python
def calculate_supply_risk_score(supplier_data):
    """
    Calculate comprehensive supply risk score

    supplier_data: dict with risk factors
    Returns: risk score (0-100, higher = riskier)
    """

    risk_score = 0
    factors = []

    # Concentration risk (% of spend with supplier)
    spend_concentration = supplier_data.get('spend_share', 0)
    if spend_concentration > 0.5:
        risk_score += 25
        factors.append("High spend concentration")
    elif spend_concentration > 0.3:
        risk_score += 15
        factors.append("Moderate spend concentration")

    # Geographic risk
    if supplier_data.get('single_location', False):
        risk_score += 15
        factors.append("Single location risk")

    if supplier_data.get('geopolitical_risk', False):
        risk_score += 20
        factors.append("Geopolitical risk")

    # Financial health (0-10 scale, 10 = best)
    financial_score = supplier_data.get('financial_health', 7)
    if financial_score < 5:
        risk_score += 20
        factors.append("Poor financial health")
    elif financial_score < 7:
        risk_score += 10
        factors.append("Moderate financial concerns")

    # Capacity utilization
    capacity_util = supplier_data.get('capacity_utilization', 0.7)
    if capacity_util > 0.95:
        risk_score += 15
        factors.append("Very high capacity utilization")
    elif capacity_util > 0.85:
        risk_score += 8
        factors.append("High capacity utilization")

    # Quality issues (defect rate)
    defect_rate = supplier_data.get('defect_rate_ppm', 0)
    if defect_rate > 1000:
        risk_score += 15
        factors.append("Quality issues")
    elif defect_rate > 500:
        risk_score += 8

    # Delivery performance
    otd_rate = supplier_data.get('on_time_delivery', 1.0)
    if otd_rate < 0.90:
        risk_score += 15
        factors.append("Poor delivery performance")
    elif otd_rate < 0.95:
        risk_score += 8

    risk_level = 'Low' if risk_score < 30 else 'Medium' if risk_score < 60 else 'High'

    return {
        'risk_score': risk_score,
        'risk_level': risk_level,
        'risk_factors': factors
    }
```

### Optimal Dual Sourcing

**Balance cost vs. risk:**

```python
def optimal_dual_sourcing(primary_supplier, backup_supplier,
                         annual_demand, disruption_prob, disruption_cost):
    """
    Determine optimal split between primary and backup supplier

    Primary supplier: lower cost, higher risk
    Backup supplier: higher cost, lower risk
    """

    best_split = None
    best_expected_cost = float('inf')

    # Try different splits from 100/0 to 50/50
    for primary_pct in range(50, 101, 5):
        backup_pct = 100 - primary_pct

        primary_qty = annual_demand * (primary_pct / 100)
        backup_qty = annual_demand * (backup_pct / 100)

        # Direct costs
        primary_cost = primary_qty * primary_supplier['unit_cost']
        backup_cost = backup_qty * backup_supplier['unit_cost']

        # Expected disruption cost
        # Assuming backup supplier not disrupted when primary is
        expected_disruption = (
            disruption_prob *
            (primary_pct / 100) *
            disruption_cost
        )

        total_expected_cost = primary_cost + backup_cost + expected_disruption

        if total_expected_cost < best_expected_cost:
            best_expected_cost = total_expected_cost
            best_split = {
                'primary_pct': primary_pct,
                'backup_pct': backup_pct,
                'primary_qty': round(primary_qty, 0),
                'backup_qty': round(backup_qty, 0),
                'primary_cost': round(primary_cost, 2),
                'backup_cost': round(backup_cost, 2),
                'expected_disruption_cost': round(expected_disruption, 2),
                'total_expected_cost': round(total_expected_cost, 2)
            }

    return best_split


# Example
primary = {'unit_cost': 10.0}
backup = {'unit_cost': 11.5}

result = optimal_dual_sourcing(
    primary_supplier=primary,
    backup_supplier=backup,
    annual_demand=10000,
    disruption_prob=0.15,  # 15% chance of disruption
    disruption_cost=500000  # $500K cost if disrupted
)

print(f"Optimal Split: {result['primary_pct']}% / {result['backup_pct']}%")
print(f"Primary Quantity: {result['primary_qty']:,.0f} units")
print(f"Backup Quantity: {result['backup_qty']:,.0f} units")
print(f"Total Expected Cost: ${result['total_expected_cost']:,.2f}")
```

---

## Tools & Libraries

### Python Libraries

**Optimization:**
- `pulp`: Linear programming (supplier allocation, lot sizing)
- `scipy.optimize`: General optimization (portfolio, dual sourcing)
- `pyomo`: Advanced optimization modeling
- `cvxpy`: Convex optimization
- `ortools`: Google OR-Tools (constraint programming)

**Data Analysis:**
- `pandas`: Data manipulation
- `numpy`: Numerical computations
- `statsmodels`: Statistical analysis

**Visualization:**
- `matplotlib`, `seaborn`: Charts and plots
- `plotly`: Interactive dashboards

### Commercial Software

**Procurement Optimization:**
- **SAP Ariba**: Strategic sourcing and procurement
- **Coupa**: Source-to-pay platform
- **Jaggaer**: Strategic sourcing suite
- **GEP SMART**: Unified procurement
- **PROS**: Price and profit optimization
- **Keelvar**: Sourcing optimization

**Supply Chain Optimization:**
- **LLamasoft**: Supply chain design and optimization
- **Blue Yonder**: Supply chain planning
- **o9 Solutions**: Integrated planning
- **Kinaxis RapidResponse**: S&OP platform

**Analytics:**
- **Tableau**, **Power BI**: Procurement dashboards
- **SpendHQ**: Spend analytics
- **Zycus**: Spend analysis

---

## Common Challenges & Solutions

### Challenge: Quantity Discount Complexity

**Problem:**
- Multiple price breaks
- Different discount structures per supplier
- Hard to compare apples-to-apples

**Solutions:**
- Use optimization to evaluate all combinations
- Calculate total landed cost including carrying
- Sensitivity analysis on demand uncertainty
- Consider cash flow impact of large orders

### Challenge: Minimum Order Quantities (MOQs)

**Problem:**
- MOQs create excess inventory
- May force use of non-optimal suppliers
- Conflicts with JIT goals

**Solutions:**
- Negotiate lower MOQs with volume commitments
- Joint orders with other business units
- Consolidate similar items
- Evaluate total cost including holding costs
- Use contract manufacturers or distributors

### Challenge: Lead Time Variability

**Problem:**
- Uncertain delivery times
- Impacts safety stock needs
- Complicates order timing

**Solutions:**
- Model lead time as probability distribution
- Optimize reorder points under uncertainty
- Diversify suppliers by geography
- Implement vendor-managed inventory (VMI)
- Use tracking and visibility tools

### Challenge: Multi-Objective Trade-offs

**Problem:**
- Conflicting goals (cost, risk, quality, sustainability)
- Different stakeholder priorities
- Hard to quantify some objectives

**Solutions:**
- Multi-criteria decision analysis (weighted scoring)
- Pareto optimization (efficient frontier)
- Scenario analysis showing trade-offs
- Stakeholder workshops to align priorities
- Set constraints on secondary objectives

### Challenge: Demand Uncertainty

**Problem:**
- Forecast errors lead to over/under ordering
- Optimal order quantity changes with demand
- Risk of obsolescence or stockouts

**Solutions:**
- Use expected demand in EOQ calculations
- Safety stock optimization
- Flexible contracts (options, postponement)
- Vendor-managed inventory (VMI)
- Periodic review and adjustment
- Risk pooling through postponement

---

## Output Format

### Procurement Optimization Report

**Executive Summary:**
- Recommended procurement strategy
- Total cost and savings opportunity
- Key changes from current approach
- Implementation requirements

**Optimal Order Allocation:**

| Supplier | Allocation | Share % | Unit Cost | Total Cost | Quality | Lead Time | Risk Level |
|----------|------------|---------|-----------|------------|---------|-----------|------------|
| Supplier B | 4,800 units | 60% | $11.00 | $52,800 | 9/10 | 21 days | Low |
| Supplier C | 2,400 units | 30% | $11.30 | $27,120 | 10/10 | 14 days | Low |
| Supplier D | 800 units | 10% | $11.00 | $8,800 | 8.5/10 | 21 days | Medium |
| **Total** | **8,000 units** | **100%** | **$11.09** | **$88,720** | **9.2/10** | **19 days** | **Low** |

**Cost Breakdown:**

| Component | Current | Optimized | Savings | % Change |
|-----------|---------|-----------|---------|----------|
| Purchase Price | $95,000 | $88,000 | $7,000 | -7.4% |
| Transportation | $12,000 | $10,400 | $1,600 | -13.3% |
| Ordering Costs | $2,400 | $1,350 | $1,050 | -43.8% |
| Holding Costs | $18,000 | $15,500 | $2,500 | -13.9% |
| **Total** | **$127,400** | **$115,250** | **$12,150** | **-9.5%** |

**Order Schedule:**

```
Recommended Order Plan (Next 12 Months):

Q1:
  - Order 1,200 units from Supplier B (Week 1)
  - Order 600 units from Supplier C (Week 1)
  - Order 200 units from Supplier D (Week 1)

Q2:
  - Order 1,200 units from Supplier B (Week 14)
  - Order 600 units from Supplier C (Week 14)

Q3:
  - Order 1,200 units from Supplier B (Week 27)
  - Order 600 units from Supplier C (Week 27)
  - Order 300 units from Supplier D (Week 27)

Q4:
  - Order 1,200 units from Supplier B (Week 40)
  - Order 600 units from Supplier C (Week 40)
  - Order 300 units from Supplier D (Week 40)
```

**Risk Assessment:**

- Overall supply risk: **Low**
- No single supplier >60% of volume (diversified)
- Average supplier financial health: 8.5/10 (strong)
- Geographic diversification: 3 regions
- Quality performance: 99.1% defect-free (excellent)

**Recommendations:**

1. Transition to 60/30/10 split across three suppliers
2. Implement quarterly orders to balance ordering and holding costs
3. Negotiate 2-year contracts with volume commitments for price stability
4. Establish performance KPIs and quarterly reviews
5. Maintain qualified backup supplier (Supplier A) for emergencies

**Implementation Plan:**

- Month 1: Finalize contracts with selected suppliers
- Month 2: Place initial orders and validate quality
- Month 3: Ramp to full production volumes
- Month 4+: Monitor performance and adjust as needed

---

## Questions to Ask

If you need more context:
1. What products/materials are being procured?
2. What's the annual demand volume and variability?
3. How many suppliers are available and what are their capabilities?
4. What are the key cost drivers? (unit price, transportation, holding)
5. Any constraints? (MOQs, capacity limits, quality requirements)
6. What's the current procurement approach and pain points?
7. What's more important: lowest cost, risk mitigation, or quality?
8. Are there quantity discounts or price breaks?
9. What lead times and delivery performance do suppliers offer?
10. Is this a one-time purchase or ongoing replenishment?

---

## Related Skills

- **supplier-selection**: For evaluating and selecting suppliers
- **strategic-sourcing**: For category strategy and sourcing approach
- **spend-analysis**: For analyzing spend patterns and opportunities
- **inventory-optimization**: For safety stock and reorder points
- **supplier-risk-management**: For monitoring supplier risks
- **contract-management**: For negotiating optimal contract terms
- **demand-forecasting**: For demand inputs to procurement planning
