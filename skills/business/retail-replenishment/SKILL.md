---
name: retail-replenishment
description: When the user wants to optimize retail store replenishment, calculate reorder points for stores, or manage continuous replenishment. Also use when the user mentions "store replenishment," "auto-replenishment," "min-max inventory," "store orders," "DC to store," "continuous replenishment," or "vendor-managed inventory (VMI)." For initial allocation, see retail-allocation. For DC operations, see warehouse-design.
---

# Retail Replenishment

You are an expert in retail store replenishment and inventory management. Your goal is to help retailers optimize the continuous flow of products from distribution centers to stores, maintaining optimal stock levels that maximize sales while minimizing inventory investment, stockouts, and excess inventory.

## Initial Assessment

Before designing replenishment strategies, understand:

1. **Store Network Characteristics**
   - How many stores? What formats? (big box, small format, urban, suburban)
   - DC locations and capacities?
   - Delivery frequency to stores? (daily, 2x/week, weekly)
   - Lead times DC to store?
   - Replenishment model? (store-initiated, auto-replenishment, VMI)

2. **Product Characteristics**
   - What categories/SKUs need replenishment?
   - Demand patterns? (steady, variable, seasonal, promotional)
   - Shelf life constraints? (perishable, dated products)
   - Product velocity? (fast, medium, slow movers)
   - Unit costs and margins?

3. **Current Performance**
   - Current in-stock rate? (target vs. actual)
   - Average inventory days on hand?
   - Stockout frequency by SKU/store?
   - Excess inventory write-offs?
   - Replenishment order accuracy?

4. **System Capabilities**
   - Replenishment system in place? (manual, automated)
   - Real-time inventory visibility?
   - POS data integration?
   - Forecasting capabilities?
   - Automated ordering?

---

## Retail Replenishment Framework

### Replenishment Models

**1. Min-Max Replenishment**
- Set minimum and maximum stock levels
- When inventory hits min, order up to max
- Simple, widely used for basic goods
- Challenge: Setting right min/max levels

**2. Time-Based Replenishment (Review Period)**
- Review inventory at fixed intervals (e.g., weekly)
- Order up to target level
- Predictable, easier planning
- Challenge: May miss urgent needs between reviews

**3. Demand-Driven Replenishment**
- Replenish based on actual consumption (POS)
- More responsive to demand changes
- Requires real-time data
- Challenge: System complexity

**4. Vendor-Managed Inventory (VMI)**
- Supplier manages inventory levels
- Supplier initiates replenishment
- Reduced retailer effort
- Challenge: Loss of control, data sharing

**5. Cross-Dock Replenishment**
- Products bypass DC storage
- Faster replenishment cycles
- Reduced handling costs
- Challenge: Requires coordination, high volumes

---

## Replenishment Parameter Optimization

### Min-Max Level Calculation

```python
import numpy as np
import pandas as pd
from scipy import stats

class ReplenishmentParameterOptimizer:
    """
    Calculate optimal replenishment parameters for stores

    Min-Max levels, reorder points, order quantities
    """

    def __init__(self, sku_data, store_data):
        """
        Parameters:
        - sku_data: SKU information (lead times, demand, etc.)
        - store_data: Store information (size, sales, format)
        """
        self.skus = sku_data
        self.stores = store_data

    def calculate_min_max_levels(self, sku, store_id, service_level=0.95,
                                 review_period_days=7):
        """
        Calculate Min-Max replenishment levels

        Min = Safety stock + Lead time demand
        Max = Safety stock + Lead time demand + Review period demand
        """

        # Get SKU and store data
        sku_info = self.skus[self.skus['sku'] == sku].iloc[0]
        store_info = self.stores[self.stores['store_id'] == store_id].iloc[0]

        # Daily demand at this store
        avg_daily_demand = store_info.get(f'{sku}_daily_demand', 0)
        demand_std = store_info.get(f'{sku}_demand_std', 0)

        # Lead time from DC to store
        lead_time_days = sku_info.get('lead_time_days', 2)
        lead_time_std = sku_info.get('lead_time_std_days', 0.5)

        # Calculate safety stock
        # Account for demand variability during lead time + review period
        total_period = lead_time_days + review_period_days

        # Combined standard deviation (demand and lead time variability)
        if demand_std > 0 and lead_time_std > 0:
            variance = (
                total_period * (demand_std ** 2) +
                (avg_daily_demand ** 2) * (lead_time_std ** 2)
            )
            combined_std = np.sqrt(variance)
        else:
            combined_std = demand_std * np.sqrt(total_period)

        # Z-score for service level
        z = stats.norm.ppf(service_level)

        # Safety stock
        safety_stock = z * combined_std

        # Lead time demand
        lead_time_demand = avg_daily_demand * lead_time_days

        # Review period demand
        review_period_demand = avg_daily_demand * review_period_days

        # Min level (reorder point)
        min_level = safety_stock + lead_time_demand

        # Max level (order up to level)
        max_level = safety_stock + lead_time_demand + review_period_demand

        # Capacity constraints
        shelf_capacity = store_info.get(f'{sku}_shelf_capacity', 999)
        backroom_capacity = store_info.get(f'{sku}_backroom_capacity', 999)
        total_capacity = shelf_capacity + backroom_capacity

        # Cap max level at capacity
        max_level = min(max_level, total_capacity)

        # Min-max spread check (min should be at least 40% of max)
        if min_level < max_level * 0.4:
            min_level = max_level * 0.4

        return {
            'sku': sku,
            'store_id': store_id,
            'min_level': round(min_level, 0),
            'max_level': round(max_level, 0),
            'safety_stock': round(safety_stock, 0),
            'avg_daily_demand': avg_daily_demand,
            'lead_time_days': lead_time_days,
            'service_level': service_level,
            'review_period_days': review_period_days
        }

    def calculate_economic_order_quantity(self, sku, annual_demand,
                                         order_cost=50, holding_cost_rate=0.25):
        """
        Calculate EOQ for replenishment order sizing

        Balance ordering costs vs. holding costs
        """

        sku_info = self.skus[self.skus['sku'] == sku].iloc[0]
        unit_cost = sku_info.get('unit_cost', 10)

        # Holding cost per unit per year
        holding_cost = unit_cost * holding_cost_rate

        # EOQ formula
        eoq = np.sqrt((2 * annual_demand * order_cost) / holding_cost)

        # Calculate order frequency
        orders_per_year = annual_demand / eoq
        days_between_orders = 365 / orders_per_year

        return {
            'sku': sku,
            'eoq': round(eoq, 0),
            'orders_per_year': round(orders_per_year, 1),
            'days_between_orders': round(days_between_orders, 1)
        }

    def optimize_replenishment_frequency(self, sku, store_id):
        """
        Determine optimal replenishment frequency

        Balance:
        - More frequent = lower inventory, better freshness, higher cost
        - Less frequent = higher inventory, lower cost, risk of stockouts
        """

        sku_info = self.skus[self.skus['sku'] == sku].iloc[0]
        store_info = self.stores[self.stores['store_id'] == store_id].iloc[0]

        avg_daily_demand = store_info.get(f'{sku}_daily_demand', 10)
        unit_cost = sku_info.get('unit_cost', 10)
        shelf_life_days = sku_info.get('shelf_life_days', 999)

        # Factors to consider
        factors = []
        recommended_frequency_days = 7  # Default weekly

        # Factor 1: Shelf life (for perishables)
        if shelf_life_days < 14:
            recommended_frequency_days = min(recommended_frequency_days, shelf_life_days // 3)
            factors.append(f"Short shelf life ({shelf_life_days} days)")

        # Factor 2: Demand velocity
        weekly_demand = avg_daily_demand * 7
        if weekly_demand > 100:
            recommended_frequency_days = min(recommended_frequency_days, 3)
            factors.append("High velocity item")
        elif weekly_demand < 10:
            recommended_frequency_days = max(recommended_frequency_days, 14)
            factors.append("Low velocity item")

        # Factor 3: Storage capacity
        shelf_capacity = store_info.get(f'{sku}_shelf_capacity', 50)
        days_of_capacity = shelf_capacity / avg_daily_demand if avg_daily_demand > 0 else 999

        if days_of_capacity < 7:
            recommended_frequency_days = min(recommended_frequency_days, 3)
            factors.append("Limited shelf capacity")

        # Factor 4: Product value
        if unit_cost > 50:
            recommended_frequency_days = min(recommended_frequency_days, 7)
            factors.append("High value item (minimize inventory investment)")

        return {
            'sku': sku,
            'store_id': store_id,
            'recommended_frequency_days': recommended_frequency_days,
            'frequency_description': self._frequency_to_description(recommended_frequency_days),
            'factors': factors
        }

    def _frequency_to_description(self, days):
        """Convert days to frequency description"""
        if days <= 1:
            return "Daily"
        elif days <= 3:
            return "2-3 times per week"
        elif days <= 7:
            return "Weekly"
        elif days <= 10:
            return "1-2 times per week"
        else:
            return "Bi-weekly or less"

# Example usage
sku_data = pd.DataFrame({
    'sku': ['SKU001', 'SKU002', 'SKU003'],
    'unit_cost': [5.50, 12.00, 3.25],
    'lead_time_days': [2, 3, 2],
    'lead_time_std_days': [0.5, 0.8, 0.5],
    'shelf_life_days': [999, 14, 999]
})

store_data = pd.DataFrame({
    'store_id': ['S001'],
    'SKU001_daily_demand': [25],
    'SKU001_demand_std': [8],
    'SKU001_shelf_capacity': [100],
    'SKU001_backroom_capacity': [200],
    'SKU002_daily_demand': [15],
    'SKU002_demand_std': [5],
    'SKU002_shelf_capacity': [50],
    'SKU002_backroom_capacity': [50],
    'SKU003_daily_demand': [50],
    'SKU003_demand_std': [15],
    'SKU003_shelf_capacity': [200],
    'SKU003_backroom_capacity': [300]
})

optimizer = ReplenishmentParameterOptimizer(sku_data, store_data)

# Calculate min-max for SKU001 at store S001
min_max = optimizer.calculate_min_max_levels('SKU001', 'S001', service_level=0.95)
print(f"SKU001 at Store S001:")
print(f"  Min level: {min_max['min_level']} units")
print(f"  Max level: {min_max['max_level']} units")
print(f"  Safety stock: {min_max['safety_stock']} units")

# Optimal replenishment frequency
frequency = optimizer.optimize_replenishment_frequency('SKU002', 'S001')
print(f"\nSKU002 replenishment frequency: {frequency['frequency_description']}")
print(f"  Factors: {frequency['factors']}")
```

---

## Automated Replenishment Engine

### Store Order Generation

```python
class AutomatedReplenishmentEngine:
    """
    Automated replenishment order generation

    Generate store orders based on current inventory, demand, and rules
    """

    def __init__(self, inventory_data, replenishment_rules, dc_inventory):
        """
        Parameters:
        - inventory_data: Current store inventory levels
        - replenishment_rules: Min-max levels and order parameters
        - dc_inventory: Available inventory at DC
        """
        self.inventory = inventory_data
        self.rules = replenishment_rules
        self.dc_inventory = dc_inventory

    def generate_store_orders(self, store_id, order_date):
        """
        Generate replenishment order for a store

        For each SKU:
        1. Check if below min level
        2. Calculate order quantity (up to max)
        3. Check DC availability
        4. Create order
        """

        store_inventory = self.inventory[
            self.inventory['store_id'] == store_id
        ]

        orders = []

        for idx, item in store_inventory.iterrows():
            sku = item['sku']
            current_level = item['on_hand'] + item['on_order']

            # Get replenishment rules
            rule = self.rules[
                (self.rules['sku'] == sku) &
                (self.rules['store_id'] == store_id)
            ]

            if len(rule) == 0:
                continue  # No rule defined

            rule = rule.iloc[0]

            # Check if replenishment needed
            if current_level <= rule['min_level']:
                # Order up to max level
                order_qty = rule['max_level'] - current_level

                # Apply order constraints
                order_qty = self._apply_order_constraints(
                    sku, order_qty, rule
                )

                # Check DC availability
                dc_available = self.dc_inventory[
                    self.dc_inventory['sku'] == sku
                ]['available_qty'].values[0]

                if dc_available >= order_qty:
                    orders.append({
                        'store_id': store_id,
                        'sku': sku,
                        'order_date': order_date,
                        'order_qty': order_qty,
                        'current_level': current_level,
                        'min_level': rule['min_level'],
                        'max_level': rule['max_level'],
                        'reason': 'Below minimum',
                        'status': 'Approved'
                    })
                elif dc_available > 0:
                    # Partial fulfillment
                    orders.append({
                        'store_id': store_id,
                        'sku': sku,
                        'order_date': order_date,
                        'order_qty': dc_available,
                        'current_level': current_level,
                        'min_level': rule['min_level'],
                        'max_level': rule['max_level'],
                        'reason': 'Partial - DC constrained',
                        'status': 'Partial'
                    })
                else:
                    # Out of stock at DC
                    orders.append({
                        'store_id': store_id,
                        'sku': sku,
                        'order_date': order_date,
                        'order_qty': 0,
                        'current_level': current_level,
                        'min_level': rule['min_level'],
                        'max_level': rule['max_level'],
                        'reason': 'DC out of stock',
                        'status': 'Backorder'
                    })

        return pd.DataFrame(orders)

    def _apply_order_constraints(self, sku, order_qty, rule):
        """
        Apply business constraints to order quantity

        - Minimum order quantity
        - Case pack multiples
        - Maximum order quantity
        """

        # Round to case pack
        case_pack = rule.get('case_pack', 1)
        if case_pack > 1:
            order_qty = int(np.ceil(order_qty / case_pack) * case_pack)

        # Minimum order
        min_order_qty = rule.get('min_order_qty', 0)
        if order_qty < min_order_qty:
            return 0  # Don't order if below minimum

        # Maximum order
        max_order_qty = rule.get('max_order_qty', 9999)
        order_qty = min(order_qty, max_order_qty)

        return order_qty

    def batch_generate_all_stores(self, order_date, store_ids=None):
        """
        Generate orders for all stores

        Batch processing for efficiency
        """

        if store_ids is None:
            store_ids = self.inventory['store_id'].unique()

        all_orders = []

        for store_id in store_ids:
            store_orders = self.generate_store_orders(store_id, order_date)
            all_orders.append(store_orders)

        return pd.concat(all_orders, ignore_index=True)

    def prioritize_orders_by_criticality(self, orders_df):
        """
        Prioritize orders when DC inventory is constrained

        Criteria:
        - Store importance (sales volume)
        - Stockout risk (how far below min)
        - Product importance (A vs. C items)
        """

        # Calculate criticality score
        def calculate_criticality(row):
            # How far below min (as %)
            below_min_pct = (row['min_level'] - row['current_level']) / row['min_level']
            below_min_pct = max(0, below_min_pct)

            # Store importance (would need actual store data)
            store_importance = 1.0  # Placeholder

            # Product importance (would need ABC classification)
            product_importance = 1.0  # Placeholder

            # Combined score
            criticality = (
                below_min_pct * 0.5 +
                store_importance * 0.3 +
                product_importance * 0.2
            )

            return criticality

        orders_df['criticality'] = orders_df.apply(calculate_criticality, axis=1)

        # Sort by criticality
        orders_df = orders_df.sort_values('criticality', ascending=False)

        return orders_df

# Example
inventory_data = pd.DataFrame({
    'store_id': ['S001', 'S001', 'S001'],
    'sku': ['SKU001', 'SKU002', 'SKU003'],
    'on_hand': [45, 15, 180],
    'on_order': [0, 0, 50]
})

replenishment_rules = pd.DataFrame({
    'store_id': ['S001', 'S001', 'S001'],
    'sku': ['SKU001', 'SKU002', 'SKU003'],
    'min_level': [50, 20, 200],
    'max_level': [150, 60, 400],
    'case_pack': [6, 12, 1],
    'min_order_qty': [12, 12, 50]
})

dc_inventory = pd.DataFrame({
    'sku': ['SKU001', 'SKU002', 'SKU003'],
    'available_qty': [5000, 800, 10000]
})

replen_engine = AutomatedReplenishmentEngine(
    inventory_data,
    replenishment_rules,
    dc_inventory
)

# Generate orders
orders = replen_engine.generate_store_orders('S001', '2024-03-15')
print("Generated Orders:")
print(orders[['sku', 'order_qty', 'current_level', 'min_level', 'max_level', 'reason']])
```

---

## Demand-Driven Replenishment

### POS-Based Replenishment

```python
class DemandDrivenReplenishment:
    """
    Demand-driven replenishment using POS data

    Replenish based on actual consumption rather than forecasts
    """

    def __init__(self, pos_data, lead_time_days=2):
        """
        Parameters:
        - pos_data: Point-of-sale transaction data
          columns: ['store_id', 'sku', 'date', 'units_sold']
        - lead_time_days: Lead time from DC to store
        """
        self.pos = pos_data
        self.lead_time = lead_time_days

    def calculate_replenishment_signal(self, sku, store_id, current_inventory,
                                      lookback_days=7):
        """
        Calculate replenishment need based on recent consumption

        Uses exponentially weighted moving average for smoothing
        """

        # Get recent POS data
        recent_pos = self.pos[
            (self.pos['sku'] == sku) &
            (self.pos['store_id'] == store_id)
        ].tail(lookback_days)

        if len(recent_pos) == 0:
            return {'order_qty': 0, 'reason': 'No sales history'}

        # Calculate EWMA of daily sales
        alpha = 0.3  # Smoothing factor
        daily_sales = recent_pos['units_sold'].values

        ewma = daily_sales[0]
        for sale in daily_sales[1:]:
            ewma = alpha * sale + (1 - alpha) * ewma

        # Forecast demand over lead time
        forecast_demand = ewma * self.lead_time

        # Add buffer (safety stock)
        std_dev = np.std(daily_sales)
        safety_stock = 1.65 * std_dev * np.sqrt(self.lead_time)  # 95% service level

        # Target inventory level
        target_level = forecast_demand + safety_stock

        # Order quantity
        order_qty = max(0, target_level - current_inventory)

        return {
            'sku': sku,
            'store_id': store_id,
            'order_qty': round(order_qty, 0),
            'avg_daily_sales': round(ewma, 1),
            'forecast_demand': round(forecast_demand, 0),
            'safety_stock': round(safety_stock, 0),
            'target_level': round(target_level, 0),
            'current_inventory': current_inventory
        }

    def detect_demand_changes(self, sku, store_id, alert_threshold=0.3):
        """
        Detect significant demand changes

        Alert when demand shifts significantly (promotions, trends, stockouts)
        """

        # Get POS data
        sku_pos = self.pos[
            (self.pos['sku'] == sku) &
            (self.pos['store_id'] == store_id)
        ].sort_values('date')

        if len(sku_pos) < 14:
            return {'alert': False, 'reason': 'Insufficient history'}

        # Compare recent vs. baseline
        baseline_sales = sku_pos.iloc[:7]['units_sold'].mean()
        recent_sales = sku_pos.iloc[-7:]['units_sold'].mean()

        if baseline_sales == 0:
            return {'alert': False, 'reason': 'No baseline sales'}

        # Calculate change
        pct_change = (recent_sales - baseline_sales) / baseline_sales

        alert = abs(pct_change) > alert_threshold

        if pct_change > alert_threshold:
            alert_type = 'Demand spike'
            action = 'Increase replenishment'
        elif pct_change < -alert_threshold:
            alert_type = 'Demand drop'
            action = 'Reduce replenishment'
        else:
            alert_type = None
            action = None

        return {
            'sku': sku,
            'store_id': store_id,
            'alert': alert,
            'alert_type': alert_type,
            'pct_change': round(pct_change * 100, 1),
            'baseline_daily_sales': round(baseline_sales, 1),
            'recent_daily_sales': round(recent_sales, 1),
            'recommended_action': action
        }

# Example
dates = pd.date_range('2024-03-01', periods=21, freq='D')
pos_data = pd.DataFrame({
    'store_id': 'S001',
    'sku': 'SKU001',
    'date': dates,
    'units_sold': [25, 22, 28, 24, 26, 23, 27,  # Week 1
                   24, 26, 25, 27, 23, 24, 28,  # Week 2
                   45, 48, 42, 46, 44, 47, 43]  # Week 3 - spike
})

ddr = DemandDrivenReplenishment(pos_data, lead_time_days=2)

# Calculate replenishment
replen_signal = ddr.calculate_replenishment_signal(
    'SKU001', 'S001', current_inventory=80, lookback_days=7
)
print("Replenishment Signal:")
print(f"  Order quantity: {replen_signal['order_qty']}")
print(f"  Avg daily sales: {replen_signal['avg_daily_sales']}")
print(f"  Target level: {replen_signal['target_level']}")

# Detect demand changes
change_alert = ddr.detect_demand_changes('SKU001', 'S001', alert_threshold=0.3)
print(f"\nDemand Change Alert: {change_alert['alert']}")
if change_alert['alert']:
    print(f"  Type: {change_alert['alert_type']}")
    print(f"  Change: {change_alert['pct_change']}%")
    print(f"  Action: {change_alert['recommended_action']}")
```

---

## DC-to-Store Allocation

### DC Inventory Allocation Logic

```python
class DCAllocationEngine:
    """
    Allocate limited DC inventory across stores

    When DC cannot fulfill all store orders
    """

    def __init__(self, store_orders, dc_inventory, store_attributes):
        self.orders = store_orders
        self.dc_inventory = dc_inventory
        self.stores = store_attributes

    def allocate_constrained_inventory(self, sku):
        """
        Allocate limited inventory fairly across stores

        Priority factors:
        - Store sales volume
        - Stockout risk (how critical)
        - Days of supply remaining
        - Store grade (A, B, C)
        """

        # Get orders for this SKU
        sku_orders = self.orders[self.orders['sku'] == sku].copy()

        if len(sku_orders) == 0:
            return pd.DataFrame()

        # Get DC available inventory
        dc_available = self.dc_inventory[
            self.dc_inventory['sku'] == sku
        ]['available_qty'].values[0]

        total_requested = sku_orders['order_qty'].sum()

        if dc_available >= total_requested:
            # Can fulfill all orders
            sku_orders['allocated_qty'] = sku_orders['order_qty']
            sku_orders['fill_rate'] = 1.0
            return sku_orders

        # Need to allocate limited inventory
        # Calculate priority score for each store
        def calculate_priority(row):
            store_info = self.stores[
                self.stores['store_id'] == row['store_id']
            ].iloc[0]

            # Factors
            sales_volume_score = store_info.get('annual_sales', 1000000) / 1000000
            grade_score = {'A': 3, 'B': 2, 'C': 1}.get(store_info.get('grade', 'B'), 2)

            # Days of supply remaining
            current_level = row.get('current_level', 0)
            avg_daily_sales = row.get('avg_daily_sales', 1)
            days_remaining = current_level / avg_daily_sales if avg_daily_sales > 0 else 999

            # Priority decreases with more days remaining
            urgency_score = 10 / (days_remaining + 1)

            # Combined priority
            priority = (
                sales_volume_score * 0.3 +
                grade_score * 0.3 +
                urgency_score * 0.4
            )

            return priority

        sku_orders['priority'] = sku_orders.apply(calculate_priority, axis=1)

        # Sort by priority
        sku_orders = sku_orders.sort_values('priority', ascending=False)

        # Allocate inventory
        remaining_inventory = dc_available

        allocated_quantities = []

        for idx, order in sku_orders.iterrows():
            if remaining_inventory <= 0:
                allocated_quantities.append(0)
            else:
                # Allocate proportional to priority, but capped at order qty
                allocation = min(order['order_qty'], remaining_inventory)
                allocated_quantities.append(allocation)
                remaining_inventory -= allocation

        sku_orders['allocated_qty'] = allocated_quantities
        sku_orders['fill_rate'] = sku_orders['allocated_qty'] / sku_orders['order_qty']

        return sku_orders[['store_id', 'sku', 'order_qty', 'allocated_qty',
                           'fill_rate', 'priority']]

# Example
store_orders = pd.DataFrame({
    'store_id': ['S001', 'S002', 'S003', 'S004'],
    'sku': 'SKU001',
    'order_qty': [100, 80, 120, 60],
    'current_level': [10, 25, 5, 30],
    'avg_daily_sales': [15, 10, 20, 8]
})

dc_inventory = pd.DataFrame({
    'sku': ['SKU001'],
    'available_qty': [250]  # Can't fulfill all 360 units
})

store_attributes = pd.DataFrame({
    'store_id': ['S001', 'S002', 'S003', 'S004'],
    'annual_sales': [5_000_000, 3_000_000, 6_000_000, 2_000_000],
    'grade': ['A', 'B', 'A', 'C']
})

allocator = DCAllocationEngine(store_orders, dc_inventory, store_attributes)

# Allocate constrained inventory
allocation = allocator.allocate_constrained_inventory('SKU001')
print("DC Inventory Allocation (250 units available, 360 requested):")
print(allocation)
print(f"\nTotal allocated: {allocation['allocated_qty'].sum()}")
```

---

## Tools & Libraries

### Python Libraries

**Optimization:**
- `scipy.optimize`: Optimization for replenishment parameters
- `pulp`, `pyomo`: Linear programming for allocation
- `numpy`: Numerical computations

**Forecasting:**
- `statsmodels`: Time series forecasting
- `prophet`: Facebook Prophet for demand forecasting
- `scikit-learn`: Machine learning models

**Data Processing:**
- `pandas`: Data manipulation and analysis
- `matplotlib`, `seaborn`: Visualization

### Commercial Software

**Replenishment Systems:**
- **Blue Yonder (JDA) Replenishment**: AI-powered auto-replenishment
- **o9 Solutions**: Digital supply chain planning
- **SAP IBP**: Integrated business planning
- **Oracle Retail Demand Forecasting**: Retail-specific replenishment
- **RELEX Solutions**: Automated replenishment

**Inventory Management:**
- **Manhattan Active Inventory**: Real-time inventory management
- **Infor SCM**: Supply chain management suite
- **Aptos Retail**: Retail operations platform

---

## Common Challenges & Solutions

### Challenge: Demand Variability

**Problem:**
- Unpredictable demand spikes/drops
- Promotions distort patterns
- Seasonal shifts
- Difficult to maintain service levels

**Solutions:**
- Dynamic safety stock adjustments
- Demand sensing (real-time POS monitoring)
- Separate baseline vs. promotional forecasts
- More frequent replenishment for volatile items
- Buffer inventory at DC
- Expedited shipping options

### Challenge: Long Lead Times

**Problem:**
- DC to store lead time 3-7 days
- Hard to respond to demand changes
- Higher inventory required

**Solutions:**
- Cross-docking for fast movers
- Increased replenishment frequency
- Safety stock adjustments for lead time
- Pre-positioning inventory near stores
- Vendor-direct-to-store for some items
- Air freight for critical needs

### Challenge: DC Stockouts

**Problem:**
- DC out of stock
- Stores cannot get replenishment
- Lost sales, customer dissatisfaction

**Solutions:**
- DC safety stock optimization
- Upstream supply visibility
- Store-to-store transfers
- Emergency orders from alternate DCs
- Direct vendor shipments
- Clear communication to stores

### Challenge: Overstock at Stores

**Problem:**
- Too much inventory
- Tied up capital
- Markdowns needed
- Limited space

**Solutions:**
- More conservative max levels
- Return to DC programs
- Store-to-store rebalancing
- Allocate new receipts considering store inventory
- Slow-mover identification and action
- Improved demand forecasting

### Challenge: Replenishment System Complexity

**Problem:**
- 1000s of stores × 1000s of SKUs
- Different rules by category/store
- System performance and maintenance

**Solutions:**
- Clustering (similar stores, similar rules)
- ABC analysis (different rigor by importance)
- Exception-based management
- Automated rule maintenance
- Regular parameter tuning
- Cloud-based scalable systems

---

## Output Format

### Replenishment Optimization Report

**Executive Summary:**
- Store network: 185 stores across 3 formats
- SKU count: 12,500 active SKUs
- Current in-stock rate: 92.3%
- Target in-stock rate: 96%
- Current avg inventory days: 28 days
- Target avg inventory days: 22 days

**Current vs. Optimized Parameters:**

| Metric | Current | Optimized | Improvement |
|--------|---------|-----------|-------------|
| In-stock rate | 92.3% | 96.2% | +3.9 pts |
| Avg inventory days | 28 days | 22 days | -21% |
| Stockout incidents/week | 340 | 115 | -66% |
| Excess inventory value | $4.2M | $2.8M | -$1.4M |
| Replenishment orders/week | 2,850 | 3,120 | +9% |

**Replenishment Frequency Changes:**

| Category | Current Frequency | Optimized Frequency | Rationale |
|----------|------------------|---------------------|-----------|
| Fresh Produce | 2x per week | Daily | Short shelf life, high velocity |
| Dairy | 2x per week | 3x per week | Perishable, steady demand |
| Dry Grocery | Weekly | Weekly | Stable, long shelf life |
| Health & Beauty | Weekly | Bi-weekly | Slow movers, space constrained |

**Min-Max Parameter Changes (Sample SKUs):**

| SKU | Store Grade | Current Min | Current Max | Optimized Min | Optimized Max | Change Rationale |
|-----|-------------|-------------|-------------|---------------|---------------|------------------|
| SKU001 | A | 50 | 200 | 75 | 175 | Increase min for service, reduce max to lower inventory |
| SKU002 | B | 30 | 100 | 40 | 90 | Tighten range based on demand |
| SKU003 | C | 20 | 80 | 15 | 50 | Reduce for slow mover |

**DC Allocation Priority Matrix:**

When DC inventory is constrained, allocate in this priority:

| Priority | Store Grade | Days of Supply | Allocation % of Request |
|----------|-------------|----------------|------------------------|
| 1 (Highest) | A | <3 days | 100% |
| 2 | A | 3-5 days | 90% |
| 3 | B | <3 days | 90% |
| 4 | A | >5 days | 75% |
| 5 | B | 3-5 days | 75% |
| 6 | C | <3 days | 70% |
| 7 (Lowest) | C | >3 days | 50% |

**Expected Financial Impact:**

| Benefit | Annual Impact |
|---------|---------------|
| Reduced stockouts (incremental sales) | +$2.8M |
| Reduced excess inventory carrying cost | +$420K |
| Reduced markdowns (better inventory management) | +$650K |
| Reduced expedited freight | +$180K |
| **Total Annual Benefit** | **+$4.05M** |

| Cost | Annual Impact |
|------|---------------|
| Increased replenishment frequency (transport) | -$320K |
| System implementation and maintenance | -$250K |
| **Total Annual Cost** | **-$570K** |

**Net Annual Benefit: +$3.48M**

**Implementation Roadmap:**

| Phase | Timeline | Activities | Expected Impact |
|-------|----------|----------|-----------------|
| Phase 1 | Month 1-2 | Optimize min-max for top 500 SKUs (A items) | 60% of benefit |
| Phase 2 | Month 3-4 | Roll out to all SKUs, all stores | 85% of benefit |
| Phase 3 | Month 5-6 | Implement DC allocation prioritization | 95% of benefit |
| Phase 4 | Month 7+ | Fine-tuning, continuous improvement | 100% of benefit |

---

## Questions to Ask

If you need more context:
1. How many stores and DCs in your network?
2. What's your current in-stock rate? Target?
3. What replenishment frequency? (daily, weekly, etc.)
4. What's the lead time from DC to stores?
5. Do you have automated replenishment or manual?
6. What system do you use for replenishment?
7. What are your biggest pain points? (stockouts, overstock, complexity)
8. Do you have real-time POS data?
9. What categories/SKUs need optimization?

---

## Related Skills

- **retail-allocation**: Initial allocation to stores
- **demand-forecasting**: Demand forecasting for replenishment
- **inventory-optimization**: Safety stock and reorder point optimization
- **warehouse-design**: DC operations and efficiency
- **route-optimization**: Delivery route optimization
- **supply-chain-analytics**: Replenishment performance metrics
- **omnichannel-fulfillment**: Cross-channel inventory management
