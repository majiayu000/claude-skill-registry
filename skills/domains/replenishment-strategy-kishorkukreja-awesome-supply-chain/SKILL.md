---
name: replenishment-strategy
description: When the user wants to design or optimize replenishment strategies, determine replenishment policies, or improve inventory flow between locations. Also use when the user mentions "inventory replenishment," "stock replenishment," "min-max inventory," "DRP," "auto-replenishment," "vendor-managed inventory," "forward pick replenishment," or "retail store replenishment." For safety stock calculations, see inventory-optimization. For multi-echelon networks, see multi-echelon-inventory.
---

# Replenishment Strategy

You are an expert in inventory replenishment strategies and demand-driven supply chain planning. Your goal is to help design efficient, responsive replenishment systems that maintain optimal inventory levels while minimizing stockouts and excess inventory.

## Initial Assessment

Before designing replenishment strategies, understand:

1. **Network Structure**
   - Supply chain tiers? (supplier → DC → store/customer)
   - Number of locations at each tier?
   - Inventory holding locations?
   - Replenishment relationships (which locations feed which)?

2. **Demand Characteristics**
   - Demand variability at each tier?
   - Lead times between tiers?
   - Order patterns (steady, lumpy, seasonal)?
   - Forecast accuracy at each level?

3. **Operational Constraints**
   - Minimum order quantities (MOQs)?
   - Order frequency limits? (daily, weekly, monthly)
   - Transportation constraints (full truckload preferred)?
   - Storage capacity limits?

4. **Current State**
   - Current replenishment method?
   - Stockout frequency and excess inventory issues?
   - Replenishment lead times?
   - Service level performance?

---

## Replenishment Strategy Framework

### Core Replenishment Methods

**1. Continuous Review (s, Q)**
- Monitor inventory continuously
- Order fixed quantity Q when inventory hits reorder point s
- Best for: High-value items, automated systems

**2. Periodic Review (R, S)**
- Review inventory every R periods
- Order up to level S
- Best for: Multiple items from same supplier, coordinated replenishment

**3. Min-Max (s, S)**
- When inventory ≤ min (s), order up to max (S)
- Hybrid of continuous and periodic
- Best for: Retail, simple systems

**4. Demand-Driven Replenishment (DDR)**
- Based on actual consumption/sales
- Pull-based, responsive to demand
- Best for: Variable demand, short lead times

**5. Vendor-Managed Inventory (VMI)**
- Supplier manages inventory levels
- Supplier responsible for replenishment
- Best for: Strong supplier relationships, consignment

---

## Replenishment Policy Models

### Continuous Review (s, Q) Policy

**Parameters:**
- **s (reorder point)**: When to order
- **Q (order quantity)**: How much to order (often EOQ)

```python
import numpy as np
from scipy import stats
import pandas as pd

def calculate_reorder_point(demand_avg_daily, lead_time_days,
                           demand_std_daily, service_level=0.95):
    """
    Calculate reorder point for continuous review

    Parameters:
    - demand_avg_daily: Average daily demand
    - lead_time_days: Lead time in days
    - demand_std_daily: Standard deviation of daily demand
    - service_level: Target service level (e.g., 0.95)

    Returns:
    - Reorder point
    """

    # Expected demand during lead time
    expected_demand = demand_avg_daily * lead_time_days

    # Safety stock
    z = stats.norm.ppf(service_level)
    std_during_lt = demand_std_daily * np.sqrt(lead_time_days)
    safety_stock = z * std_during_lt

    # Reorder point
    rop = expected_demand + safety_stock

    return {
        'reorder_point': round(rop, 0),
        'expected_demand_lt': round(expected_demand, 0),
        'safety_stock': round(safety_stock, 0),
        'service_level': service_level
    }

# Example
rop_params = calculate_reorder_point(
    demand_avg_daily=100,
    lead_time_days=14,
    demand_std_daily=20,
    service_level=0.95
)

print(f"Reorder Point: {rop_params['reorder_point']} units")
print(f"  Expected demand during LT: {rop_params['expected_demand_lt']}")
print(f"  Safety stock: {rop_params['safety_stock']}")
```

**Simulation:**

```python
def simulate_continuous_review(demand_series, lead_time, reorder_point,
                               order_quantity, initial_inventory):
    """
    Simulate continuous review (s, Q) policy

    Parameters:
    - demand_series: Array of daily demand
    - lead_time: Lead time in days
    - reorder_point: Reorder point (s)
    - order_quantity: Order quantity (Q)
    - initial_inventory: Starting inventory

    Returns:
    - Simulation results DataFrame
    """

    results = []
    inventory = initial_inventory
    on_order = []  # Queue of orders in transit

    for day, demand in enumerate(demand_series):
        # Check for order arrivals
        arrived_orders = [o for o in on_order if o['arrival_day'] == day]
        for order in arrived_orders:
            inventory += order['quantity']
            on_order.remove(order)

        # Satisfy demand
        actual_demand = min(demand, inventory)
        stockout = max(0, demand - inventory)
        inventory = max(0, inventory - demand)

        # Check if need to order
        inventory_position = inventory + sum(o['quantity'] for o in on_order)
        order_placed = False

        if inventory_position <= reorder_point:
            on_order.append({
                'quantity': order_quantity,
                'order_day': day,
                'arrival_day': day + lead_time
            })
            order_placed = True

        results.append({
            'day': day,
            'demand': demand,
            'inventory_on_hand': inventory,
            'inventory_position': inventory_position,
            'stockout': stockout,
            'order_placed': order_placed
        })

    return pd.DataFrame(results)

# Example simulation
np.random.seed(42)
demand = np.random.poisson(100, 365)  # 365 days

sim_results = simulate_continuous_review(
    demand_series=demand,
    lead_time=14,
    reorder_point=1600,
    order_quantity=1000,
    initial_inventory=2000
)

# Performance metrics
print(f"Average inventory: {sim_results['inventory_on_hand'].mean():.0f}")
print(f"Stockout days: {(sim_results['stockout'] > 0).sum()}")
print(f"Service level: {(1 - (sim_results['stockout'] > 0).sum() / len(sim_results)):.1%}")
print(f"Orders placed: {sim_results['order_placed'].sum()}")
```

### Periodic Review (R, S) Policy

**Parameters:**
- **R (review period)**: How often to review (e.g., weekly)
- **S (order-up-to level)**: Target inventory level

```python
def calculate_order_up_to_level(demand_avg_daily, review_period_days,
                               lead_time_days, demand_std_daily,
                               service_level=0.95):
    """
    Calculate order-up-to level for periodic review

    Must cover demand during review period + lead time
    """

    # Total coverage period
    coverage_period = review_period_days + lead_time_days

    # Expected demand during coverage period
    expected_demand = demand_avg_daily * coverage_period

    # Safety stock for coverage period
    z = stats.norm.ppf(service_level)
    std_during_period = demand_std_daily * np.sqrt(coverage_period)
    safety_stock = z * std_during_period

    # Order-up-to level
    order_up_to = expected_demand + safety_stock

    return {
        'order_up_to_level': round(order_up_to, 0),
        'expected_demand': round(expected_demand, 0),
        'safety_stock': round(safety_stock, 0),
        'coverage_period_days': coverage_period,
        'service_level': service_level
    }

# Example
periodic_params = calculate_order_up_to_level(
    demand_avg_daily=100,
    review_period_days=7,    # Weekly review
    lead_time_days=14,
    demand_std_daily=20,
    service_level=0.95
)

print(f"Order-up-to Level (S): {periodic_params['order_up_to_level']} units")
print(f"Coverage period: {periodic_params['coverage_period_days']} days")
```

**Simulation:**

```python
def simulate_periodic_review(demand_series, review_period, order_up_to_level,
                            lead_time, initial_inventory):
    """
    Simulate periodic review (R, S) policy
    """

    results = []
    inventory = initial_inventory
    on_order = []

    for day, demand in enumerate(demand_series):
        # Check for arrivals
        arrived_orders = [o for o in on_order if o['arrival_day'] == day]
        for order in arrived_orders:
            inventory += order['quantity']
            on_order.remove(order)

        # Satisfy demand
        actual_demand = min(demand, inventory)
        stockout = max(0, demand - inventory)
        inventory = max(0, inventory - demand)

        # Check if review day
        is_review_day = (day % review_period == 0)
        order_qty = 0

        if is_review_day:
            inventory_position = inventory + sum(o['quantity'] for o in on_order)
            order_qty = max(0, order_up_to_level - inventory_position)

            if order_qty > 0:
                on_order.append({
                    'quantity': order_qty,
                    'order_day': day,
                    'arrival_day': day + lead_time
                })

        results.append({
            'day': day,
            'demand': demand,
            'inventory_on_hand': inventory,
            'is_review_day': is_review_day,
            'order_quantity': order_qty,
            'stockout': stockout
        })

    return pd.DataFrame(results)

# Example
sim_results = simulate_periodic_review(
    demand_series=demand,
    review_period=7,
    order_up_to_level=2200,
    lead_time=14,
    initial_inventory=2000
)

print(f"Average inventory: {sim_results['inventory_on_hand'].mean():.0f}")
print(f"Stockout days: {(sim_results['stockout'] > 0).sum()}")
print(f"Orders placed: {(sim_results['order_quantity'] > 0).sum()}")
```

### Min-Max Replenishment

**Simple and Widely Used:**
- **Min**: Trigger point (similar to reorder point)
- **Max**: Target level (order up to this)

```python
def calculate_min_max(demand_avg_daily, lead_time_days, review_frequency_days,
                     demand_std_daily, service_level=0.95):
    """
    Calculate min and max levels

    Min = reorder point
    Max = enough to cover lead time + review period + safety stock
    """

    # Min level (reorder point)
    expected_demand_lt = demand_avg_daily * lead_time_days
    z = stats.norm.ppf(service_level)
    std_during_lt = demand_std_daily * np.sqrt(lead_time_days)
    safety_stock = z * std_during_lt
    min_level = expected_demand_lt + safety_stock

    # Max level (order-up-to level)
    coverage_period = lead_time_days + review_frequency_days
    expected_demand_coverage = demand_avg_daily * coverage_period
    std_during_coverage = demand_std_daily * np.sqrt(coverage_period)
    safety_stock_max = z * std_during_coverage
    max_level = expected_demand_coverage + safety_stock_max

    return {
        'min_level': round(min_level, 0),
        'max_level': round(max_level, 0),
        'order_quantity_typical': round(max_level - min_level, 0),
        'safety_stock': round(safety_stock, 0)
    }

# Example
min_max = calculate_min_max(
    demand_avg_daily=100,
    lead_time_days=14,
    review_frequency_days=7,
    demand_std_daily=20,
    service_level=0.95
)

print(f"Min Level: {min_max['min_level']} units")
print(f"Max Level: {min_max['max_level']} units")
print(f"Typical order quantity: {min_max['order_quantity_typical']} units")
```

---

## Distribution Requirements Planning (DRP)

**DRP Concept:**
- Time-phased planning for multi-echelon networks
- Push from central planning
- Projects future inventory positions
- Plans replenishment orders in advance

### DRP Calculation

```python
def drp_calculation(forecast, on_hand, scheduled_receipts, lead_time,
                   safety_stock, order_quantity):
    """
    Distribution Requirements Planning calculation

    Parameters:
    - forecast: Array of forecasted demand by period
    - on_hand: Starting on-hand inventory
    - scheduled_receipts: Dict {period: quantity} of scheduled orders
    - lead_time: Lead time in periods
    - safety_stock: Safety stock target
    - order_quantity: Standard order quantity

    Returns:
    - DRP table
    """

    periods = len(forecast)
    drp_table = []

    current_on_hand = on_hand

    for period in range(periods):
        # Scheduled receipt this period
        receipt = scheduled_receipts.get(period, 0)

        # Projected available before order
        proj_available_before = current_on_hand + receipt - forecast[period]

        # Check if order needed
        if proj_available_before < safety_stock:
            planned_order = order_quantity
            proj_available_after = proj_available_before + planned_order
        else:
            planned_order = 0
            proj_available_after = proj_available_before

        drp_table.append({
            'period': period + 1,
            'forecast': forecast[period],
            'scheduled_receipt': receipt,
            'proj_available_before': round(proj_available_before, 0),
            'planned_order': planned_order,
            'proj_available_after': round(proj_available_after, 0)
        })

        current_on_hand = proj_available_after

        # Schedule planned order to arrive after lead time
        if planned_order > 0 and period + lead_time < periods:
            if period + lead_time not in scheduled_receipts:
                scheduled_receipts[period + lead_time] = 0
            scheduled_receipts[period + lead_time] += planned_order

    return pd.DataFrame(drp_table)

# Example
forecast = [100, 110, 105, 120, 115, 125, 130, 135, 140, 120, 115, 110]
scheduled_receipts = {0: 500}  # Order arriving in period 0

drp_table = drp_calculation(
    forecast=forecast,
    on_hand=200,
    scheduled_receipts=scheduled_receipts,
    lead_time=2,
    safety_stock=150,
    order_quantity=500
)

print(drp_table)
```

---

## Demand-Driven Replenishment

### Pull-Based Replenishment

**Characteristics:**
- Replenishment triggered by actual consumption/sales
- Responsive to demand signals
- Minimizes bullwhip effect
- Works best with short lead times

```python
def demand_driven_replenishment(sales_data, replenishment_frequency='daily',
                               coverage_days=14, safety_stock_days=7):
    """
    Calculate demand-driven replenishment quantities

    Parameters:
    - sales_data: DataFrame with daily sales history
    - replenishment_frequency: 'daily', 'weekly', 'monthly'
    - coverage_days: Days of supply to maintain
    - safety_stock_days: Additional safety stock days

    Returns:
    - Replenishment recommendations
    """

    # Calculate average daily rate (ADR)
    lookback_days = 30
    recent_sales = sales_data[-lookback_days:]
    adr = recent_sales['sales'].mean()

    # Calculate target inventory
    target_inventory = adr * (coverage_days + safety_stock_days)

    # Current inventory position
    current_inventory = sales_data.iloc[-1]['inventory']

    # Replenishment quantity
    replen_qty = max(0, target_inventory - current_inventory)

    # Adjust for replenishment frequency
    if replenishment_frequency == 'weekly':
        replen_qty = max(0, target_inventory - current_inventory)
    elif replenishment_frequency == 'monthly':
        # Ensure full month coverage
        target_inventory = adr * 30
        replen_qty = max(0, target_inventory - current_inventory)

    return {
        'average_daily_rate': round(adr, 1),
        'target_inventory': round(target_inventory, 0),
        'current_inventory': current_inventory,
        'replenishment_quantity': round(replen_qty, 0),
        'days_of_supply_current': round(current_inventory / adr, 1) if adr > 0 else 0
    }

# Example
sales_history = pd.DataFrame({
    'date': pd.date_range('2024-01-01', periods=60),
    'sales': np.random.poisson(100, 60),
    'inventory': 1500 - np.random.poisson(100, 60).cumsum()
})

replen = demand_driven_replenishment(
    sales_data=sales_history,
    replenishment_frequency='weekly',
    coverage_days=14,
    safety_stock_days=7
)

print(f"Average daily rate: {replen['average_daily_rate']}")
print(f"Current days of supply: {replen['days_of_supply_current']}")
print(f"Replenishment needed: {replen['replenishment_quantity']} units")
```

---

## Multi-Echelon Replenishment

### Two-Echelon Model (DC → Store)

**Considerations:**
- DC replenishment from supplier
- Store replenishment from DC
- Balance inventory investment across echelons
- Service level targets at each tier

```python
def two_echelon_replenishment(dc_params, store_params, num_stores):
    """
    Calculate replenishment parameters for two-echelon system

    Parameters:
    - dc_params: Dict with DC demand and lead time from supplier
    - store_params: Dict with store demand and lead time from DC
    - num_stores: Number of stores supplied by DC

    Returns:
    - Replenishment parameters for DC and stores
    """

    # DC level
    # Aggregate demand from all stores
    dc_demand_avg = store_params['demand_avg'] * num_stores
    dc_demand_std = store_params['demand_std'] * np.sqrt(num_stores)  # Square root law

    # DC reorder point (from supplier)
    z_dc = stats.norm.ppf(dc_params['service_level'])
    dc_lt = dc_params['lead_time_from_supplier']
    dc_rop = (dc_demand_avg * dc_lt +
             z_dc * dc_demand_std * np.sqrt(dc_lt))

    # DC order quantity (EOQ or other method)
    dc_order_qty = dc_params.get('order_quantity', dc_demand_avg * 7)  # Default: 1 week

    # Store level
    # Each store maintains its own inventory
    z_store = stats.norm.ppf(store_params['service_level'])
    store_lt = store_params['lead_time_from_dc']
    store_rop = (store_params['demand_avg'] * store_lt +
                z_store * store_params['demand_std'] * np.sqrt(store_lt))

    store_order_qty = store_params.get('order_quantity',
                                       store_params['demand_avg'] * 3)  # Default: 3 days

    return {
        'dc': {
            'demand_avg': round(dc_demand_avg, 0),
            'reorder_point': round(dc_rop, 0),
            'order_quantity': round(dc_order_qty, 0),
            'safety_stock': round(z_dc * dc_demand_std * np.sqrt(dc_lt), 0)
        },
        'store': {
            'demand_avg': store_params['demand_avg'],
            'reorder_point': round(store_rop, 0),
            'order_quantity': round(store_order_qty, 0),
            'safety_stock': round(z_store * store_params['demand_std'] * np.sqrt(store_lt), 0)
        },
        'total_safety_stock': round(
            z_dc * dc_demand_std * np.sqrt(dc_lt) +
            num_stores * z_store * store_params['demand_std'] * np.sqrt(store_lt), 0
        )
    }

# Example
dc_params = {
    'lead_time_from_supplier': 14,
    'service_level': 0.98
}

store_params = {
    'demand_avg': 10,
    'demand_std': 3,
    'lead_time_from_dc': 2,
    'service_level': 0.95
}

replen_params = two_echelon_replenishment(dc_params, store_params, num_stores=100)

print("DC Replenishment:")
print(f"  Demand (from all stores): {replen_params['dc']['demand_avg']}")
print(f"  Reorder point: {replen_params['dc']['reorder_point']}")
print(f"  Order quantity: {replen_params['dc']['order_quantity']}")

print("\nStore Replenishment (each):")
print(f"  Reorder point: {replen_params['store']['reorder_point']}")
print(f"  Order quantity: {replen_params['store']['order_quantity']}")

print(f"\nTotal network safety stock: {replen_params['total_safety_stock']}")
```

---

## Forward Pick Replenishment

**Warehouse Context:**
- Reserve storage (bulk pallets)
- Forward pick locations (case/each picking)
- Replenish forward pick from reserve

### Forward Pick Sizing & Replenishment

```python
def forward_pick_replenishment(sku_velocity_daily, pick_location_capacity,
                              replenishment_frequency='nightly',
                              target_days_supply=2):
    """
    Determine forward pick location size and replenishment

    Parameters:
    - sku_velocity_daily: Daily pick volume (eaches)
    - pick_location_capacity: Max capacity of forward location
    - replenishment_frequency: 'nightly', 'shift', 'continuous'
    - target_days_supply: Days of supply to maintain in forward location

    Returns:
    - Forward pick configuration
    """

    # Minimum forward pick size (cover until next replenishment)
    if replenishment_frequency == 'nightly':
        min_capacity_needed = sku_velocity_daily * 1.2  # 20% buffer
    elif replenishment_frequency == 'shift':
        min_capacity_needed = sku_velocity_daily * 0.5 * 1.2  # Half day
    else:  # continuous
        min_capacity_needed = sku_velocity_daily * 0.25  # 6 hours

    # Target forward pick quantity
    target_qty = min(sku_velocity_daily * target_days_supply, pick_location_capacity)

    # Replenishment trigger point
    replen_trigger = sku_velocity_daily * 0.5  # When half-day supply remains

    # Replenishment quantity
    replen_qty = target_qty - replen_trigger

    return {
        'velocity_daily': sku_velocity_daily,
        'min_capacity_needed': round(min_capacity_needed, 0),
        'recommended_capacity': round(target_qty, 0),
        'replenishment_trigger': round(replen_trigger, 0),
        'replenishment_quantity': round(replen_qty, 0),
        'replenishments_per_day': round(sku_velocity_daily / replen_qty, 1)
    }

# Example
forward_pick = forward_pick_replenishment(
    sku_velocity_daily=200,
    pick_location_capacity=500,
    replenishment_frequency='nightly',
    target_days_supply=2
)

print(f"Forward pick capacity needed: {forward_pick['recommended_capacity']}")
print(f"Replenishment trigger: {forward_pick['replenishment_trigger']}")
print(f"Replenishment quantity: {forward_pick['replenishment_quantity']}")
print(f"Replenishments per day: {forward_pick['replenishments_per_day']}")
```

---

## Vendor-Managed Inventory (VMI)

**VMI Model:**
- Supplier has visibility to customer inventory
- Supplier responsible for replenishment decisions
- Customer shares POS/consumption data
- Often consignment (pay on consumption)

### VMI Benefits & Implementation

**Benefits:**
- Reduced stockouts (supplier manages proactively)
- Lower inventory (supplier optimizes across customers)
- Less administrative burden (no PO creation)
- Better planning for supplier

**Implementation Requirements:**

```python
def vmi_data_sharing_requirements():
    """
    Define data sharing requirements for VMI
    """

    requirements = {
        'customer_provides': [
            'Current inventory levels (on-hand)',
            'Point-of-sale (POS) data or consumption',
            'Scheduled receipts (orders in transit)',
            'Promotional calendar',
            'Min-max levels or service level targets',
            'Storage capacity constraints'
        ],
        'supplier_provides': [
            'Replenishment recommendations',
            'Inventory visibility dashboard',
            'Shipment notifications',
            'Performance reports (fill rate, inventory turns)'
        ],
        'technology_needs': [
            'EDI or API integration',
            'Vendor portal for data access',
            'Real-time or daily data feeds',
            'Exception alerts (stockout risk, overstock)'
        ]
    }

    return requirements

# Example VMI replenishment calculation (supplier-side)
def vmi_replenishment_calculation(current_inventory, daily_consumption,
                                 lead_time_days, target_service_level=0.95,
                                 min_order_qty=100):
    """
    Supplier calculates replenishment for VMI customer
    """

    # Historical consumption (use rolling average)
    avg_consumption = daily_consumption

    # Calculate target inventory (order-up-to level)
    coverage_days = lead_time_days + 7  # Lead time + 1 week buffer
    target_inventory = avg_consumption * coverage_days

    # Replenishment quantity
    replen_qty = max(0, target_inventory - current_inventory)

    # Apply min order quantity
    if replen_qty > 0 and replen_qty < min_order_qty:
        replen_qty = min_order_qty

    days_of_supply = current_inventory / avg_consumption if avg_consumption > 0 else 999

    return {
        'current_inventory': current_inventory,
        'days_of_supply': round(days_of_supply, 1),
        'target_inventory': round(target_inventory, 0),
        'replenishment_quantity': round(replen_qty, 0),
        'action': 'Ship order' if replen_qty >= min_order_qty else 'No action needed'
    }

# Example
vmi_replen = vmi_replenishment_calculation(
    current_inventory=450,
    daily_consumption=50,
    lead_time_days=7,
    target_service_level=0.95,
    min_order_qty=100
)

print(f"Current inventory: {vmi_replen['current_inventory']}")
print(f"Days of supply: {vmi_replen['days_of_supply']}")
print(f"Replenishment needed: {vmi_replen['replenishment_quantity']}")
print(f"Action: {vmi_replen['action']}")
```

---

## Replenishment Optimization

### Cost-Based Optimization

**Trade-offs:**
- Ordering costs (setup, transportation)
- Holding costs (inventory carrying)
- Stockout costs (lost sales, expediting)

```python
from scipy.optimize import minimize_scalar

def optimize_replenishment_quantity(demand_annual, order_cost, holding_cost_rate,
                                   unit_cost, stockout_cost_per_unit):
    """
    Optimize order quantity considering ordering, holding, and stockout costs

    Based on EOQ with stockout costs
    """

    def total_cost(order_qty):
        """Calculate total annual cost for given order quantity"""

        # Ordering cost
        orders_per_year = demand_annual / order_qty
        annual_ordering_cost = orders_per_year * order_cost

        # Holding cost
        avg_inventory = order_qty / 2
        annual_holding_cost = avg_inventory * unit_cost * holding_cost_rate

        # Simplified stockout cost (inversely related to order qty)
        # More frequent orders = less stockout risk
        annual_stockout_cost = stockout_cost_per_unit * (1000 / order_qty)

        return annual_ordering_cost + annual_holding_cost + annual_stockout_cost

    # Optimize
    result = minimize_scalar(total_cost, bounds=(50, 5000), method='bounded')

    optimal_qty = result.x
    optimal_cost = result.fun

    # Calculate components at optimal
    orders_per_year = demand_annual / optimal_qty
    ordering_cost = orders_per_year * order_cost
    holding_cost = (optimal_qty / 2) * unit_cost * holding_cost_rate
    stockout_cost = stockout_cost_per_unit * (1000 / optimal_qty)

    return {
        'optimal_order_quantity': round(optimal_qty, 0),
        'orders_per_year': round(orders_per_year, 1),
        'total_annual_cost': round(optimal_cost, 2),
        'ordering_cost': round(ordering_cost, 2),
        'holding_cost': round(holding_cost, 2),
        'stockout_cost': round(stockout_cost, 2)
    }

# Example
optimal = optimize_replenishment_quantity(
    demand_annual=10000,
    order_cost=100,
    holding_cost_rate=0.25,
    unit_cost=50,
    stockout_cost_per_unit=500
)

print(f"Optimal order quantity: {optimal['optimal_order_quantity']}")
print(f"Orders per year: {optimal['orders_per_year']}")
print(f"Total annual cost: ${optimal['total_annual_cost']:,.2f}")
```

---

## Tools & Libraries

### Software Solutions

**Supply Chain Planning:**
- **SAP IBP**: Integrated business planning with DRP
- **Blue Yonder (JDA)**: Replenishment planning
- **Oracle ASCP**: Advanced supply chain planning
- **Kinaxis RapidResponse**: Demand-driven planning
- **o9 Solutions**: AI-powered planning

**WMS with Replenishment:**
- **Manhattan Associates**: Advanced replenishment logic
- **Blue Yonder WMS**: Integrated replenishment
- **SAP EWM**: Extended warehouse management

**Retail-Specific:**
- **Oracle Retail**: Store replenishment optimization
- **Blue Yonder Luminate**: Retail planning
- **Relex Solutions**: Automated replenishment

### Python Libraries

```python
# Commonly used libraries
import numpy as np  # Numerical computations
import pandas as pd  # Data manipulation
from scipy import stats  # Statistical distributions
from scipy.optimize import minimize  # Optimization
import matplotlib.pyplot as plt  # Visualization
```

---

## Common Challenges & Solutions

### Challenge: Bullwhip Effect

**Problem:**
- Demand variability amplifies up the supply chain
- Small changes at retail cause large swings at supplier
- Excess inventory and stockouts

**Solutions:**
- Share POS/consumption data (not orders)
- Implement demand-driven replenishment
- Reduce lead times
- Stabilize ordering patterns (avoid batch ordering)
- VMI or collaborative planning

### Challenge: Long Lead Times

**Problem:**
- Large safety stock required
- Poor responsiveness to demand changes
- Higher inventory investment

**Solutions:**
- Work with suppliers to reduce lead times
- Air freight for critical items
- Safety stock optimization by SKU
- Local suppliers or nearshoring
- Postponement strategies

### Challenge: Lumpy Demand

**Problem:**
- Intermittent or sporadic demand
- Traditional formulas don't work well
- High stockout risk or excess inventory

**Solutions:**
- Use Croston's method or similar for intermittent demand
- Consider not stocking (order on demand)
- Aggregate demand (product families)
- Higher safety stock factors
- Frequent review and adjustment

### Challenge: Multi-Echelon Complexity

**Problem:**
- Inventory at multiple tiers (DC, stores, etc.)
- Difficult to optimize holistically
- Sub-optimization at each tier

**Solutions:**
- Use multi-echelon optimization models
- Centralized planning (not just local optimization)
- Share visibility across tiers
- DRP or demand-driven approaches
- Consider inventory pooling/consolidation

### Challenge: Balancing Transportation Costs

**Problem:**
- Small frequent orders = high transportation costs
- Large infrequent orders = high holding costs
- Tension between inventory and transportation

**Solutions:**
- Economic order quantity considers both
- Truckload optimization (order multiple SKUs together)
- Milk runs for consolidated deliveries
- Cross-docking to break bulk
- 3PL for shared transportation

### Challenge: Forecast Inaccuracy

**Problem:**
- Replenishment based on forecast
- Forecast errors lead to stockouts or excess
- Difficulty planning

**Solutions:**
- Switch to demand-driven (use actuals, not forecast)
- Improve forecast accuracy (see demand-forecasting)
- Higher safety stock for forecast error buffer
- Shorter planning horizons
- Agile supply chain (quick response)

---

## Output Format

### Replenishment Strategy Document

**Executive Summary:**
- Recommended replenishment approach
- Expected inventory reduction
- Service level improvements
- Implementation requirements

**Replenishment Policy by Tier:**

**Supplier → DC:**
- Policy: Continuous Review (s, Q)
- Reorder Point: 12,000 units
- Order Quantity: 10,000 units (truckload)
- Lead Time: 14 days
- Target Service Level: 98%
- Orders per Month: ~9

**DC → Stores:**
- Policy: Periodic Review (weekly)
- Order-up-to Level: 500 units (per store average)
- Review Frequency: Weekly
- Lead Time: 2 days
- Target Service Level: 95%

**SKU-Level Parameters:**

| SKU | Tier | Policy | Reorder Point / Min | Order Qty / Max | Safety Stock | Service Level |
|-----|------|--------|---------------------|-----------------|--------------|---------------|
| A123 | DC | (s,Q) | 8,000 | 5,000 | 2,500 | 98% |
| A123 | Store | Min-Max | 100 | 200 | 40 | 95% |
| B456 | DC | (R,S) | - | Up to 15,000 | 3,000 | 98% |
| B456 | Store | Weekly | - | Up to 150 | 30 | 95% |

**Expected Performance:**

| Metric | Current | Optimized | Improvement |
|--------|---------|-----------|-------------|
| Avg Inventory Investment | $8M | $6.5M | -18.8% |
| Inventory Turns | 5.2 | 6.8 | +1.6 |
| Fill Rate | 93% | 97% | +4 pts |
| Stockout Frequency | 8% of days | 3% of days | -5 pts |
| Orders per Week | 45 | 38 | -15.6% |

**Implementation Timeline:**
- Week 1-2: Calculate replenishment parameters for all SKUs
- Week 3-4: Configure WMS/ERP systems
- Week 5-6: Training and parallel testing
- Week 7-8: Go-live and monitoring
- Ongoing: Performance monitoring and adjustment

---

## Questions to Ask

If you need more context:
1. What's the network structure? (tiers, locations, flow)
2. What's the current replenishment method and pain points?
3. What are the lead times at each tier?
4. What's the demand profile? (stable, variable, seasonal, intermittent)
5. What service levels are targeted?
6. Are there MOQs or transportation constraints?
7. What systems are in place? (WMS, ERP, planning tools)
8. Is there interest in VMI or supplier collaboration?

---

## Related Skills

- **inventory-optimization**: Safety stock and reorder point calculations
- **demand-forecasting**: Forecast demand for replenishment planning
- **multi-echelon-inventory**: Network-wide inventory optimization
- **distribution-center-network**: Network design and flow
- **economic-order-quantity**: Order quantity optimization
- **retail-replenishment**: Retail-specific replenishment strategies
- **supply-chain-analytics**: KPIs and performance tracking
