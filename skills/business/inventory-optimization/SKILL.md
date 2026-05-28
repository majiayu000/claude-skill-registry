---
name: inventory-optimization
description: When the user wants to optimize inventory levels, calculate safety stock, determine reorder points, or minimize inventory costs. Also use when the user mentions "inventory management," "safety stock," "EOQ," "reorder point," "service level," "stockout prevention," "ABC analysis," "inventory turns," or "working capital reduction." For warehouse slotting, see warehouse-slotting-optimization. For multi-echelon systems, see multi-echelon-inventory.
---

# Inventory Optimization

You are an expert in inventory optimization and management. Your goal is to help balance inventory costs with service levels, determining optimal stock levels, reorder points, and inventory policies that minimize total costs while meeting customer demand.

## Initial Assessment

Before optimizing inventory, understand:

1. **Business Context**
   - What products/SKUs need inventory optimization?
   - Current inventory investment and turns?
   - Target service levels (fill rate, stockout rate)?
   - Current pain points? (excess, shortages, cash tied up)

2. **Demand Characteristics**
   - Demand patterns? (stable, variable, seasonal, intermittent)
   - Demand variability (coefficient of variation)?
   - Historical sales data available? (12-24 months ideal)
   - Forecast accuracy (MAPE)?

3. **Supply Parameters**
   - Lead times from suppliers?
   - Lead time variability?
   - Minimum order quantities (MOQs)?
   - Order costs and constraints?

4. **Cost Structure**
   - Unit product cost?
   - Ordering/setup costs per order?
   - Inventory carrying cost rate (% per year)?
   - Stockout/backorder costs?

---

## Inventory Optimization Framework

### Key Inventory Decisions

**1. How Much to Order? (Order Quantity)**
- Economic Order Quantity (EOQ)
- Fixed order quantity
- Lot-for-lot ordering
- Volume discounts consideration

**2. When to Order? (Reorder Point)**
- Continuous review (s, Q) policy
- Periodic review (s, S) policy
- Time-phased ordering
- Dynamic safety stock

**3. How Much Safety Stock?**
- Service level targets
- Demand variability
- Lead time variability
- Cost-service trade-offs

---

## Fundamental Models

### Economic Order Quantity (EOQ)

**Classic EOQ Formula:**
```
EOQ = sqrt((2 * D * S) / H)

Where:
  D = Annual demand (units)
  S = Ordering cost per order ($)
  H = Holding cost per unit per year ($)
```

**Total Cost:**
```
TC = (D/Q) * S + (Q/2) * H + D * C

Where:
  Q = Order quantity
  C = Unit cost
```

**Python Implementation:**

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def eoq(annual_demand, order_cost, holding_cost_rate, unit_cost):
    """
    Calculate Economic Order Quantity

    Parameters:
    - annual_demand: Annual demand in units
    - order_cost: Cost per order ($)
    - holding_cost_rate: Holding cost as % of unit cost (e.g., 0.25 for 25%)
    - unit_cost: Cost per unit ($)

    Returns:
    - Dictionary with EOQ, total cost, orders per year, etc.
    """

    # Holding cost per unit per year
    holding_cost = unit_cost * holding_cost_rate

    # EOQ formula
    eoq_qty = np.sqrt((2 * annual_demand * order_cost) / holding_cost)

    # Number of orders per year
    orders_per_year = annual_demand / eoq_qty

    # Total annual cost
    ordering_cost_total = (annual_demand / eoq_qty) * order_cost
    holding_cost_total = (eoq_qty / 2) * holding_cost
    purchase_cost = annual_demand * unit_cost
    total_cost = ordering_cost_total + holding_cost_total + purchase_cost

    # Order interval (days)
    order_interval = 365 / orders_per_year

    return {
        'EOQ': round(eoq_qty, 0),
        'Orders_Per_Year': round(orders_per_year, 1),
        'Order_Interval_Days': round(order_interval, 1),
        'Total_Annual_Cost': round(total_cost, 2),
        'Ordering_Cost': round(ordering_cost_total, 2),
        'Holding_Cost': round(holding_cost_total, 2),
        'Purchase_Cost': round(purchase_cost, 2)
    }

# Example usage
result = eoq(
    annual_demand=10000,
    order_cost=100,
    holding_cost_rate=0.25,
    unit_cost=50
)

print(f"Optimal Order Quantity: {result['EOQ']} units")
print(f"Order {result['Orders_Per_Year']} times per year")
print(f"Order every {result['Order_Interval_Days']} days")
print(f"Total Annual Cost: ${result['Total_Annual_Cost']:,.2f}")
```

**EOQ with Quantity Discounts:**

```python
def eoq_with_discounts(annual_demand, order_cost, holding_cost_rate, price_breaks):
    """
    EOQ with all-units quantity discount

    price_breaks: list of tuples [(qty, price), ...]
    Example: [(0, 50), (500, 48), (1000, 45)]
    """

    results = []

    for qty_break, unit_price in price_breaks:
        holding_cost = unit_price * holding_cost_rate

        # Calculate EOQ at this price
        eoq_qty = np.sqrt((2 * annual_demand * order_cost) / holding_cost)

        # If EOQ < qty_break, use qty_break as order quantity
        order_qty = max(eoq_qty, qty_break)

        # Total cost at this quantity
        ordering_cost = (annual_demand / order_qty) * order_cost
        holding_cost_total = (order_qty / 2) * holding_cost
        purchase_cost = annual_demand * unit_price
        total_cost = ordering_cost + holding_cost_total + purchase_cost

        results.append({
            'Quantity_Break': qty_break,
            'Unit_Price': unit_price,
            'EOQ_at_Price': round(eoq_qty, 0),
            'Order_Quantity': round(order_qty, 0),
            'Total_Cost': round(total_cost, 2)
        })

    # Find minimum cost option
    results_df = pd.DataFrame(results)
    optimal = results_df.loc[results_df['Total_Cost'].idxmin()]

    return results_df, optimal

# Example with quantity discounts
price_breaks = [
    (0, 50),      # 0-499: $50/unit
    (500, 48),    # 500-999: $48/unit
    (1000, 45)    # 1000+: $45/unit
]

results_df, optimal = eoq_with_discounts(
    annual_demand=10000,
    order_cost=100,
    holding_cost_rate=0.25,
    price_breaks=price_breaks
)

print(results_df)
print(f"\nOptimal: Order {optimal['Order_Quantity']} units at ${optimal['Unit_Price']}/unit")
```

---

## Safety Stock & Reorder Point

### Safety Stock Calculation

**Service Level Approach:**

```python
from scipy import stats
import numpy as np

def safety_stock(demand_std, lead_time_days, service_level=0.95):
    """
    Calculate safety stock based on service level

    Parameters:
    - demand_std: Standard deviation of daily demand
    - lead_time_days: Lead time in days
    - service_level: Target service level (e.g., 0.95 for 95%)

    Returns:
    - Safety stock quantity
    """

    # Z-score for desired service level
    z = stats.norm.ppf(service_level)

    # Safety stock = Z * std_dev during lead time
    # Assuming demand is independent across days
    std_during_lt = demand_std * np.sqrt(lead_time_days)

    ss = z * std_during_lt

    return round(ss, 0)

def safety_stock_variable_lt(demand_avg, demand_std, lead_time_avg,
                              lead_time_std, service_level=0.95):
    """
    Safety stock with variable demand AND lead time

    More comprehensive formula accounting for both sources of variability
    """

    z = stats.norm.ppf(service_level)

    # Combined variance formula
    variance = (lead_time_avg * demand_std**2 +
                demand_avg**2 * lead_time_std**2)

    std_during_lt = np.sqrt(variance)

    ss = z * std_during_lt

    return round(ss, 0)

# Example: Basic safety stock
ss = safety_stock(
    demand_std=50,        # Daily demand std dev
    lead_time_days=14,    # 2 week lead time
    service_level=0.95    # 95% service level
)
print(f"Safety Stock: {ss} units")

# Example: Variable lead time
ss_var = safety_stock_variable_lt(
    demand_avg=100,       # Avg daily demand
    demand_std=50,        # Std dev of daily demand
    lead_time_avg=14,     # Avg lead time (days)
    lead_time_std=3,      # Std dev of lead time (days)
    service_level=0.95
)
print(f"Safety Stock (variable LT): {ss_var} units")
```

### Reorder Point (ROP)

**Formula:**
```
ROP = (Average Daily Demand × Lead Time) + Safety Stock
```

**Python Implementation:**

```python
def reorder_point(demand_avg_daily, lead_time_days, safety_stock):
    """
    Calculate reorder point

    ROP = Expected demand during lead time + Safety stock
    """

    expected_demand_lt = demand_avg_daily * lead_time_days
    rop = expected_demand_lt + safety_stock

    return round(rop, 0)

def rop_with_review_period(demand_avg_daily, lead_time_days,
                           review_period_days, safety_stock):
    """
    Reorder point with periodic review

    Must cover lead time + review period
    """

    total_period = lead_time_days + review_period_days
    expected_demand = demand_avg_daily * total_period
    rop = expected_demand + safety_stock

    return round(rop, 0)

# Example
rop = reorder_point(
    demand_avg_daily=100,
    lead_time_days=14,
    safety_stock=200
)
print(f"Reorder Point: {rop} units")
print(f"When inventory hits {rop}, place an order")
```

---

## Inventory Policy Models

### (s, Q) Continuous Review Policy

**Description:**
- Monitor inventory continuously
- When inventory position ≤ s (reorder point), order Q units
- Q typically set to EOQ

```python
class ContinuousReviewPolicy:
    """(s, Q) continuous review inventory policy"""

    def __init__(self, reorder_point, order_quantity):
        self.s = reorder_point
        self.Q = order_quantity
        self.inventory_position = 0
        self.on_hand = 0
        self.on_order = 0
        self.orders_placed = []

    def check_and_order(self, current_on_hand, current_on_order):
        """Check if order should be placed"""

        self.on_hand = current_on_hand
        self.on_order = current_on_order
        self.inventory_position = current_on_hand + current_on_order

        if self.inventory_position <= self.s:
            # Place order
            order = {
                'quantity': self.Q,
                'inventory_position': self.inventory_position,
                'on_hand': self.on_hand,
                'on_order': self.on_order
            }
            self.orders_placed.append(order)
            return True, self.Q

        return False, 0

    def simulate(self, demand_series, lead_time=14):
        """Simulate inventory policy over time"""

        inventory = []
        current_inv = self.Q  # Start with one order quantity
        on_order_queue = []

        for day, demand in enumerate(demand_series):
            # Receive orders (if any arrive today)
            arrivals = [o for o in on_order_queue if o['arrival_day'] == day]
            for arrival in arrivals:
                current_inv += arrival['quantity']
                on_order_queue.remove(arrival)

            # Satisfy demand
            current_inv = max(0, current_inv - demand)

            # Check if order needed
            current_on_order = sum(o['quantity'] for o in on_order_queue)
            should_order, order_qty = self.check_and_order(current_inv, current_on_order)

            if should_order:
                on_order_queue.append({
                    'quantity': order_qty,
                    'order_day': day,
                    'arrival_day': day + lead_time
                })

            inventory.append({
                'day': day,
                'on_hand': current_inv,
                'demand': demand,
                'on_order': current_on_order,
                'order_placed': should_order
            })

        return pd.DataFrame(inventory)

# Example simulation
np.random.seed(42)
demand_series = np.random.poisson(100, 365)  # 365 days of demand

policy = ContinuousReviewPolicy(
    reorder_point=1600,
    order_quantity=1000
)

results = policy.simulate(demand_series, lead_time=14)
print(f"Average inventory: {results['on_hand'].mean():.0f} units")
print(f"Stockouts: {(results['on_hand'] == 0).sum()} days")
print(f"Orders placed: {results['order_placed'].sum()}")
```

### (R, S) Periodic Review Policy

**Description:**
- Review inventory every R periods (e.g., weekly)
- Order up to S (order-up-to level)
- Order quantity varies based on current position

```python
class PeriodicReviewPolicy:
    """(R, S) periodic review inventory policy"""

    def __init__(self, review_period, order_up_to_level):
        self.R = review_period
        self.S = order_up_to_level

    def calculate_order_qty(self, current_position):
        """Calculate order quantity to reach S"""
        return max(0, self.S - current_position)

    def simulate(self, demand_series, lead_time=14):
        """Simulate periodic review policy"""

        inventory = []
        current_inv = self.S  # Start at order-up-to level
        on_order_queue = []

        for day, demand in enumerate(demand_series):
            # Receive orders
            arrivals = [o for o in on_order_queue if o['arrival_day'] == day]
            for arrival in arrivals:
                current_inv += arrival['quantity']
                on_order_queue.remove(arrival)

            # Satisfy demand
            current_inv = max(0, current_inv - demand)

            # Check if it's a review day
            should_order = (day % self.R == 0)
            order_qty = 0

            if should_order:
                current_on_order = sum(o['quantity'] for o in on_order_queue)
                current_position = current_inv + current_on_order
                order_qty = self.calculate_order_qty(current_position)

                if order_qty > 0:
                    on_order_queue.append({
                        'quantity': order_qty,
                        'order_day': day,
                        'arrival_day': day + lead_time
                    })

            inventory.append({
                'day': day,
                'on_hand': current_inv,
                'demand': demand,
                'order_qty': order_qty,
                'review_day': should_order
            })

        return pd.DataFrame(inventory)

# Example
policy = PeriodicReviewPolicy(
    review_period=7,      # Weekly review
    order_up_to_level=2100
)

results = policy.simulate(demand_series, lead_time=14)
print(f"Average inventory: {results['on_hand'].mean():.0f} units")
print(f"Total orders: {(results['order_qty'] > 0).sum()}")
```

---

## ABC Analysis & Segmentation

### ABC Classification

**Methodology:**
- **A items**: Top 20% of SKUs by value, ~80% of revenue
- **B items**: Next 30% of SKUs, ~15% of revenue
- **C items**: Bottom 50% of SKUs, ~5% of revenue

```python
def abc_analysis(df, sku_col='sku', demand_col='annual_demand',
                 price_col='unit_price'):
    """
    Perform ABC analysis on inventory

    Parameters:
    - df: DataFrame with SKU, demand, and price
    - Returns: DataFrame with ABC classification
    """

    # Calculate annual value
    df = df.copy()
    df['annual_value'] = df[demand_col] * df[price_col]

    # Sort by value descending
    df = df.sort_values('annual_value', ascending=False)

    # Calculate cumulative percentage
    total_value = df['annual_value'].sum()
    df['cumulative_value'] = df['annual_value'].cumsum()
    df['cumulative_pct'] = df['cumulative_value'] / total_value * 100

    # Classify
    def classify(pct):
        if pct <= 80:
            return 'A'
        elif pct <= 95:
            return 'B'
        else:
            return 'C'

    df['abc_class'] = df['cumulative_pct'].apply(classify)

    # Add ranking
    df['rank'] = range(1, len(df) + 1)

    return df

# Example usage
inventory_data = pd.DataFrame({
    'sku': [f'SKU_{i}' for i in range(1, 101)],
    'annual_demand': np.random.randint(100, 10000, 100),
    'unit_price': np.random.uniform(10, 500, 100)
})

abc_result = abc_analysis(inventory_data)

# Summary by class
summary = abc_result.groupby('abc_class').agg({
    'sku': 'count',
    'annual_value': 'sum'
}).round(0)

summary['pct_skus'] = summary['sku'] / summary['sku'].sum() * 100
summary['pct_value'] = summary['annual_value'] / summary['annual_value'].sum() * 100

print(summary)
```

### XYZ Analysis (Demand Variability)

**Classification:**
- **X**: Low variability (CV < 0.5) - Predictable
- **Y**: Medium variability (0.5 ≤ CV < 1.0) - Moderate
- **Z**: High variability (CV ≥ 1.0) - Unpredictable

```python
def xyz_analysis(df, demand_history_col='demand_history'):
    """
    Classify items by demand variability

    demand_history_col should contain list/array of historical demand
    """

    def classify_variability(demands):
        if len(demands) < 2:
            return 'Z'  # Insufficient data

        mean_demand = np.mean(demands)
        std_demand = np.std(demands)

        if mean_demand == 0:
            return 'Z'

        cv = std_demand / mean_demand  # Coefficient of variation

        if cv < 0.5:
            return 'X'
        elif cv < 1.0:
            return 'Y'
        else:
            return 'Z'

    df = df.copy()
    df['xyz_class'] = df[demand_history_col].apply(classify_variability)

    return df

# Combined ABC-XYZ matrix
def abc_xyz_matrix(df):
    """Create ABC-XYZ classification matrix"""

    matrix = pd.crosstab(df['abc_class'], df['xyz_class'],
                         values=df['sku'], aggfunc='count')

    return matrix
```

### Inventory Policy by Classification

| Class | Service Level | Review Frequency | Safety Stock | Method |
|-------|---------------|------------------|--------------|--------|
| A-X | 99% | Daily | High | Continuous review, tight control |
| A-Y | 98% | Daily | High | Continuous review |
| A-Z | 95% | Weekly | Very high | Periodic review, high SS |
| B-X | 97% | Weekly | Medium | Periodic or continuous |
| B-Y | 95% | Weekly | Medium | Periodic review |
| B-Z | 90% | Bi-weekly | High | Periodic review |
| C-X | 90% | Monthly | Low | Periodic review, simple rules |
| C-Y | 85% | Monthly | Medium | Min/max rules |
| C-Z | 80% | As needed | Low/none | Order on demand or don't stock |

---

## Advanced Inventory Optimization

### Service Level vs. Cost Trade-off

```python
def service_level_analysis(demand_std, lead_time, unit_cost,
                           holding_cost_rate, stockout_cost):
    """
    Analyze optimal service level balancing holding vs. stockout costs
    """

    service_levels = np.arange(0.80, 0.995, 0.01)
    results = []

    holding_cost_per_unit = unit_cost * holding_cost_rate

    for sl in service_levels:
        # Safety stock required
        z = stats.norm.ppf(sl)
        std_during_lt = demand_std * np.sqrt(lead_time)
        ss = z * std_during_lt

        # Holding cost
        holding_cost = ss * holding_cost_per_unit

        # Expected stockout cost
        # Simplified: (1 - service_level) * stockout_cost
        expected_stockouts = (1 - sl) * stockout_cost

        total_cost = holding_cost + expected_stockouts

        results.append({
            'service_level': sl,
            'safety_stock': round(ss, 0),
            'holding_cost': round(holding_cost, 2),
            'stockout_cost': round(expected_stockouts, 2),
            'total_cost': round(total_cost, 2)
        })

    results_df = pd.DataFrame(results)

    # Find optimal
    optimal_idx = results_df['total_cost'].idxmin()
    optimal = results_df.iloc[optimal_idx]

    return results_df, optimal

# Example
results_df, optimal = service_level_analysis(
    demand_std=50,
    lead_time=14,
    unit_cost=100,
    holding_cost_rate=0.25,
    stockout_cost=5000  # Cost per stockout event
)

print(f"Optimal service level: {optimal['service_level']:.1%}")
print(f"Safety stock: {optimal['safety_stock']} units")
print(f"Total cost: ${optimal['total_cost']:,.2f}")
```

### Inventory Turnover Optimization

**Inventory Turns Formula:**
```
Inventory Turns = Cost of Goods Sold (COGS) / Average Inventory Value
```

```python
def inventory_metrics(annual_cogs, avg_inventory_value, target_turns=None):
    """
    Calculate inventory turnover metrics
    """

    turns = annual_cogs / avg_inventory_value
    days_on_hand = 365 / turns

    metrics = {
        'Inventory_Turns': round(turns, 2),
        'Days_On_Hand': round(days_on_hand, 1),
        'Avg_Inventory': avg_inventory_value
    }

    if target_turns:
        target_inventory = annual_cogs / target_turns
        reduction = avg_inventory_value - target_inventory
        metrics['Target_Inventory'] = round(target_inventory, 0)
        metrics['Inventory_Reduction'] = round(reduction, 0)
        metrics['Cash_Freed'] = round(reduction, 0)

    return metrics

# Example
metrics = inventory_metrics(
    annual_cogs=50_000_000,
    avg_inventory_value=10_000_000,
    target_turns=8
)

print(f"Current turns: {metrics['Inventory_Turns']}")
print(f"Days on hand: {metrics['Days_On_Hand']}")
if 'Target_Inventory' in metrics:
    print(f"Target inventory: ${metrics['Target_Inventory']:,.0f}")
    print(f"Cash to be freed: ${metrics['Cash_Freed']:,.0f}")
```

### Multi-SKU Optimization

```python
from scipy.optimize import minimize

def optimize_multi_sku_inventory(skus_data, total_budget, target_service_level=0.95):
    """
    Optimize inventory allocation across multiple SKUs with budget constraint

    skus_data: DataFrame with columns ['sku', 'demand_avg', 'demand_std',
                                        'lead_time', 'unit_cost', 'stockout_cost']
    """

    n_skus = len(skus_data)

    def objective(safety_stocks):
        """Minimize total cost (holding + expected stockouts)"""

        total_cost = 0

        for i, ss in enumerate(safety_stocks):
            row = skus_data.iloc[i]

            # Holding cost
            holding_cost = ss * row['unit_cost'] * 0.25  # 25% holding rate

            # Calculate achieved service level from safety stock
            z = ss / (row['demand_std'] * np.sqrt(row['lead_time']))
            service_level = stats.norm.cdf(z)

            # Stockout cost
            stockout_prob = 1 - service_level
            expected_stockout = stockout_prob * row['stockout_cost']

            total_cost += holding_cost + expected_stockout

        return total_cost

    def budget_constraint(safety_stocks):
        """Total inventory value must not exceed budget"""
        total_value = sum(
            ss * skus_data.iloc[i]['unit_cost']
            for i, ss in enumerate(safety_stocks)
        )
        return total_budget - total_value

    # Initial guess: equal allocation
    x0 = np.full(n_skus, total_budget / (n_skus * skus_data['unit_cost'].mean()))

    # Constraints
    constraints = [
        {'type': 'ineq', 'fun': budget_constraint}
    ]

    # Bounds: non-negative safety stock
    bounds = [(0, None) for _ in range(n_skus)]

    # Optimize
    result = minimize(objective, x0, method='SLSQP',
                     bounds=bounds, constraints=constraints)

    # Extract results
    optimal_ss = result.x

    results_df = skus_data.copy()
    results_df['optimal_safety_stock'] = optimal_ss
    results_df['inventory_value'] = optimal_ss * results_df['unit_cost']

    return results_df, result

# Example with multiple SKUs
skus_data = pd.DataFrame({
    'sku': ['A', 'B', 'C', 'D'],
    'demand_avg': [100, 200, 50, 150],
    'demand_std': [20, 40, 25, 30],
    'lead_time': [14, 7, 21, 14],
    'unit_cost': [50, 30, 100, 75],
    'stockout_cost': [500, 300, 1000, 600]
})

results_df, optimization = optimize_multi_sku_inventory(
    skus_data,
    total_budget=50000,
    target_service_level=0.95
)

print(results_df[['sku', 'optimal_safety_stock', 'inventory_value']])
print(f"\nTotal inventory value: ${results_df['inventory_value'].sum():,.0f}")
```

---

## Tools & Libraries

### Python Libraries

**Inventory Optimization:**
- `numpy`: Numerical computations
- `scipy`: Statistical distributions, optimization
- `pandas`: Data manipulation
- `statsmodels`: Time series analysis

**Simulation:**
- `simpy`: Discrete event simulation
- `ciw`: Queueing network simulation

**Optimization:**
- `scipy.optimize`: Non-linear optimization
- `pulp`: Linear programming
- `pyomo`: Optimization modeling

**Visualization:**
- `matplotlib`, `seaborn`: Plotting
- `plotly`: Interactive charts

### Commercial Software

**Inventory Planning:**
- **SAP IBP**: Integrated business planning
- **Blue Yonder (JDA)**: Inventory optimization
- **Kinaxis RapidResponse**: Supply chain planning
- **Logility**: Inventory optimization
- **o9 Solutions**: Digital planning platform

**Specialized Tools:**
- **Inventory Planner**: E-commerce inventory
- **Lokad**: Probabilistic forecasting & inventory
- **NetSuite**: ERP with inventory management
- **Fishbowl**: Inventory tracking & management

---

## Common Challenges & Solutions

### Challenge: Demand Variability

**Problem:**
- High demand variability increases safety stock requirements
- Difficult to forecast

**Solutions:**
- Segment by ABC-XYZ, different policies per segment
- Use probabilistic forecasting (distribution, not point estimate)
- Consider demand smoothing strategies (promotions management)
- Increase forecast frequency (weekly vs. monthly)
- Implement demand sensing with real-time data

### Challenge: Long Lead Times

**Problem:**
- Longer lead times require more safety stock
- Higher risk of stockouts or obsolescence

**Solutions:**
- Work with suppliers to reduce lead time
- Implement vendor-managed inventory (VMI)
- Use safety lead time padding
- Consider dual sourcing for critical items
- Air freight for critical replenishments

### Challenge: Excess Inventory

**Problem:**
- Too much slow-moving or obsolete inventory
- Cash tied up, storage costs

**Solutions:**
- Implement ABC analysis, focus on C items
- Markdown/clearance strategies
- Return to supplier agreements
- Improved demand forecasting
- Reduce order quantities for slow movers
- Consider drop-ship for long tail items

### Challenge: Stockouts & Backorders

**Problem:**
- Insufficient inventory, lost sales
- Poor customer service

**Solutions:**
- Increase safety stock (cost-service trade-off)
- Improve forecast accuracy
- Reduce lead time variability
- Implement expedited shipping options
- Better supply chain visibility
- Consider make-to-order for low-volume items

### Challenge: Balancing Cost vs. Service

**Problem:**
- Conflicting objectives (minimize inventory vs. maximize service)

**Solutions:**
- Quantify stockout costs (lost sales, penalties)
- Use optimization to find optimal trade-off
- Segment inventory (different service levels by class)
- Implement service level agreements (SLAs)
- Use cost-to-serve analysis

### Challenge: Multi-Echelon Complexity

**Problem:**
- Inventory at multiple locations (plants, DCs, stores)
- Difficult to optimize holistically

**Solutions:**
- See **multi-echelon-inventory** skill
- Use network optimization models
- Implement demand-driven replenishment
- Centralize planning (but not necessarily inventory)
- Consider postponement strategies

---

## Output Format

### Inventory Optimization Report

**Executive Summary:**
- Current inventory investment and turns
- Recommended inventory levels and policies
- Expected service level improvements
- Working capital impact

**SKU-Level Recommendations:**

| SKU | ABC | XYZ | Current Avg Inv | Recommended Avg Inv | Safety Stock | Reorder Point | Order Qty | Policy | Service Level |
|-----|-----|-----|-----------------|---------------------|--------------|---------------|-----------|--------|---------------|
| SKU_001 | A | X | 500 | 450 | 200 | 1,600 | 1,000 | (s,Q) | 99% |
| SKU_002 | B | Y | 300 | 280 | 120 | 850 | 500 | (R,S) | 95% |
| SKU_003 | C | Z | 150 | 50 | 30 | 250 | Min/Max | Monthly | 85% |

**Financial Impact:**

| Metric | Current | Optimized | Improvement |
|--------|---------|-----------|-------------|
| Total Inventory Value | $15M | $12M | -$3M (-20%) |
| Inventory Turns | 4.5 | 6.0 | +1.5 (+33%) |
| Days on Hand | 81 | 61 | -20 days |
| Fill Rate | 92% | 97% | +5 pts |
| Annual Holding Cost | $3.75M | $3.0M | -$750K |

**Implementation Plan:**
1. Phase 1: Implement policies for A items (80% of value)
2. Phase 2: Roll out to B items
3. Phase 3: Simplify C item management
4. Ongoing: Monitor and adjust based on performance

---

## Questions to Ask

If you need more context:
1. What products/SKUs need optimization? How many total?
2. What's the current inventory investment and turnover?
3. What service levels are you targeting?
4. What's the demand pattern? (stable, variable, seasonal, intermittent)
5. What are the lead times from suppliers?
6. What cost data is available? (product cost, ordering cost, holding cost rate)
7. What's driving this initiative? (cost reduction, service improvement, working capital)

---

## Related Skills

- **economic-order-quantity**: Deep dive into EOQ models
- **demand-forecasting**: Forecasting for inventory planning
- **multi-echelon-inventory**: Network inventory optimization
- **stochastic-inventory-models**: Probabilistic approaches
- **newsvendor-problem**: Single-period inventory decisions
- **supply-chain-analytics**: KPIs and performance metrics
- **abc-analysis**: Classification and segmentation (if separate skill exists)
- **warehouse-slotting-optimization**: Optimizing inventory placement
