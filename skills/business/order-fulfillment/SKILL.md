---
name: order-fulfillment
description: When the user wants to design or optimize order fulfillment operations, improve pick-pack-ship processes, or reduce fulfillment costs. Also use when the user mentions "order processing," "pick-pack-ship," "picking strategy," "packing operations," "shipping optimization," "wave planning," "batch picking," or "fulfillment center operations." For warehouse layout, see warehouse-design. For routing pickers, see picker-routing-optimization.
---

# Order Fulfillment

You are an expert in order fulfillment operations and optimization. Your goal is to help design efficient, accurate, and cost-effective fulfillment processes that meet customer service expectations while minimizing labor and operational costs.

## Initial Assessment

Before optimizing fulfillment, understand:

1. **Order Profile**
   - Order volume? (orders/day, peak vs. average)
   - Order characteristics? (lines/order, units/order)
   - Order types? (B2B pallets, B2C eaches, mixed)
   - SKU count and velocity distribution?

2. **Service Requirements**
   - Delivery speed? (same-day, next-day, 2-day, standard)
   - Cutoff times for shipping?
   - Order accuracy targets? (99.5%+)
   - Special services? (gift wrap, kitting, customization)

3. **Current Operations**
   - Current fulfillment process and flow?
   - Pick accuracy and productivity rates?
   - Technology in use? (WMS, automation, RF scanners)
   - Pain points and bottlenecks?

4. **Constraints**
   - Labor availability and cost?
   - Facility layout and space?
   - Capital budget for improvements?
   - IT systems and integration capabilities?

---

## Order Fulfillment Framework

### Core Fulfillment Processes

**1. Order Receipt & Validation**
- Order intake from channels (web, EDI, phone)
- Inventory availability check (ATP)
- Credit/payment verification
- Order prioritization and batching

**2. Picking**
- Retrieve items from storage locations
- Verify SKU and quantity accuracy
- Multiple strategies (discrete, batch, zone, wave)

**3. Packing**
- Select appropriate packaging
- Pack items securely
- Insert documents (packing slip, returns)
- Generate shipping label

**4. Shipping**
- Carrier selection and manifesting
- Trailer loading and departure
- Track and trace updates

**5. Returns Processing**
- Receive and inspect returns
- Disposition (restock, liquidate, destroy)
- Customer refund/exchange processing

---

## Picking Strategies

### Strategy Comparison

| Strategy | Orders/Hour | Labor Efficiency | Accuracy | Complexity | Best For |
|----------|-------------|------------------|----------|------------|----------|
| Discrete (Single Order) | 20-40 | Low | High | Low | Low volume, high value |
| Batch Picking | 60-100 | Medium | Medium | Medium | Medium volume |
| Zone Picking | 80-150 | High | Medium | High | High SKU count |
| Wave Picking | 100-200+ | Very High | Medium | Very High | High volume |
| Cluster Picking | 100-150 | High | High | Medium | Multi-order picking |

### Discrete Order Picking

**Description:**
- Pick one order at a time
- Complete each order before starting next
- Simple, accurate, inefficient

**When to Use:**
- Low order volume (<500 orders/day)
- High-value orders requiring accuracy
- Complex orders with customization

```python
import numpy as np
import pandas as pd

def discrete_picking_capacity(orders_per_day, lines_per_order,
                              pick_rate_per_hour=100,
                              working_hours=8):
    """
    Calculate labor requirements for discrete picking

    Parameters:
    - orders_per_day: Daily order volume
    - lines_per_order: Average lines per order
    - pick_rate_per_hour: Picks per person per hour (includes travel)
    - working_hours: Working hours per shift
    """

    picks_per_day = orders_per_day * lines_per_order

    # Labor hours needed
    labor_hours_needed = picks_per_day / pick_rate_per_hour

    # Pickers needed
    pickers_needed = labor_hours_needed / working_hours

    # Orders per picker per day
    orders_per_picker = orders_per_day / pickers_needed

    return {
        'picks_per_day': picks_per_day,
        'labor_hours_needed': round(labor_hours_needed, 1),
        'pickers_needed': round(pickers_needed, 1),
        'orders_per_picker_per_day': round(orders_per_picker, 0),
        'picks_per_picker_per_hour': pick_rate_per_hour
    }

# Example
discrete = discrete_picking_capacity(
    orders_per_day=500,
    lines_per_order=5,
    pick_rate_per_hour=100,
    working_hours=8
)

print(f"Pickers needed: {discrete['pickers_needed']}")
print(f"Orders per picker: {discrete['orders_per_picker_per_day']}")
```

### Batch Picking

**Description:**
- Pick multiple orders simultaneously
- Pick each SKU once for all orders in batch
- Sort items to orders after picking

**Benefits:**
- Reduce travel time (visit each location once)
- 40-60% productivity improvement vs. discrete

**Implementation:**

```python
def batch_picking_optimization(orders_df, batch_size=10, sort_time_per_unit=3):
    """
    Optimize batch picking

    Parameters:
    - orders_df: DataFrame with columns ['order_id', 'sku', 'quantity', 'location']
    - batch_size: Orders per batch
    - sort_time_per_unit: Seconds to sort each unit to order

    Returns:
    - Batch assignments and performance metrics
    """

    # Create batches
    orders_df = orders_df.copy()
    orders_df['batch'] = (orders_df.index // batch_size) + 1

    # Calculate picks per batch
    batch_summary = orders_df.groupby('batch').agg({
        'order_id': 'nunique',
        'sku': 'count',
        'quantity': 'sum',
        'location': 'nunique'
    }).rename(columns={
        'order_id': 'orders',
        'sku': 'pick_lines',
        'location': 'unique_locations'
    })

    # Estimate time savings
    # Discrete: visit each location for each order
    # Batch: visit each location once per batch

    discrete_picks = len(orders_df)
    batch_picks = batch_summary['unique_locations'].sum()

    pick_reduction_pct = (discrete_picks - batch_picks) / discrete_picks

    # Sort time required
    total_units = batch_summary['quantity'].sum()
    sort_time_hours = (total_units * sort_time_per_unit) / 3600

    return {
        'total_batches': len(batch_summary),
        'avg_orders_per_batch': batch_summary['orders'].mean(),
        'discrete_picks': discrete_picks,
        'batch_picks': batch_picks,
        'pick_reduction_%': round(pick_reduction_pct * 100, 1),
        'sort_time_hours': round(sort_time_hours, 2),
        'batch_summary': batch_summary
    }

# Example
orders_df = pd.DataFrame({
    'order_id': [f'ORD_{i}' for i in range(1, 101)],
    'sku': np.random.choice(['SKU_A', 'SKU_B', 'SKU_C', 'SKU_D'], 100),
    'quantity': np.random.randint(1, 5, 100),
    'location': np.random.choice(['A1', 'A2', 'B1', 'B2', 'C1'], 100)
})

batch_result = batch_picking_optimization(orders_df, batch_size=10)
print(f"Pick reduction: {batch_result['pick_reduction_%']}%")
print(f"Sort time required: {batch_result['sort_time_hours']} hours")
```

### Zone Picking

**Description:**
- Divide warehouse into zones
- Each picker assigned to a zone
- Orders pass through zones sequentially or consolidate at end

**Types:**
- **Sequential zone picking**: Order travels zone to zone
- **Batch zone picking**: Pick to totes, consolidate later

**Benefits:**
- Pickers become expert in their zone
- Parallel processing (multiple orders picked simultaneously)
- Reduces congestion

```python
def zone_picking_design(warehouse_sq_ft, num_pickers, orders_per_day,
                       lines_per_order, sku_distribution):
    """
    Design zone picking system

    Parameters:
    - warehouse_sq_ft: Total picking area
    - num_pickers: Available pickers
    - orders_per_day: Daily order volume
    - lines_per_order: Average lines per order
    - sku_distribution: Dict with zone: % of picks
    """

    picks_per_day = orders_per_day * lines_per_order

    # Allocate zones based on pick volume
    zone_allocation = {}

    for zone, pct in sku_distribution.items():
        picks_in_zone = picks_per_day * pct
        pickers_needed = picks_in_zone / (100 * 8)  # 100 picks/hr, 8 hrs

        zone_allocation[zone] = {
            'pick_volume': round(picks_in_zone, 0),
            'pickers_needed': round(pickers_needed, 1),
            'sq_ft': round(warehouse_sq_ft * pct, 0)
        }

    return zone_allocation

# Example
sku_dist = {
    'Zone_A_Fast': 0.40,  # 40% of picks
    'Zone_B_Medium': 0.35,
    'Zone_C_Slow': 0.25
}

zones = zone_picking_design(
    warehouse_sq_ft=50000,
    num_pickers=20,
    orders_per_day=2000,
    lines_per_order=5,
    sku_distribution=sku_dist
)

print("Zone Allocation:")
for zone, data in zones.items():
    print(f"\n  {zone}:")
    print(f"    Pick volume: {data['pick_volume']}")
    print(f"    Pickers needed: {data['pickers_needed']}")
    print(f"    Square footage: {data['sq_ft']}")
```

### Wave Picking

**Description:**
- Release groups of orders together as "waves"
- Optimize wave composition for efficiency
- Coordinate picking, packing, shipping

**Wave Design Factors:**
- Carrier schedule (UPS pickup at 5pm)
- Order priority (SLA requirements)
- Resource availability (pickers, packers)
- Warehouse capacity (staging space)

```python
def wave_planning(orders_df, waves_per_day=4, target_wave_size=500):
    """
    Plan picking waves

    Parameters:
    - orders_df: DataFrame with ['order_id', 'priority', 'lines', 'carrier', 'cutoff_time']
    - waves_per_day: Number of waves per day
    - target_wave_size: Target orders per wave

    Returns:
    - Wave assignments
    """

    orders_df = orders_df.copy()

    # Sort by priority and cutoff time
    orders_df = orders_df.sort_values(['priority', 'cutoff_time'], ascending=[False, True])

    # Assign to waves
    orders_df['wave'] = (orders_df.index // target_wave_size) % waves_per_day + 1

    # Wave summary
    wave_summary = orders_df.groupby('wave').agg({
        'order_id': 'count',
        'lines': 'sum',
        'cutoff_time': 'max'
    }).rename(columns={
        'order_id': 'orders',
        'lines': 'total_picks'
    })

    # Estimate time required per wave
    wave_summary['pick_hours'] = wave_summary['total_picks'] / 100  # 100 picks/hr
    wave_summary['pickers_needed'] = np.ceil(wave_summary['pick_hours'] / 2)  # 2 hr wave

    return orders_df[['order_id', 'wave', 'priority']], wave_summary

# Example
orders_data = pd.DataFrame({
    'order_id': [f'ORD_{i}' for i in range(1, 2001)],
    'priority': np.random.choice([1, 2, 3], 2000, p=[0.1, 0.3, 0.6]),
    'lines': np.random.poisson(5, 2000),
    'carrier': np.random.choice(['UPS', 'FedEx', 'USPS'], 2000),
    'cutoff_time': np.random.choice(['12:00', '15:00', '17:00'], 2000)
})

wave_assignments, wave_summary = wave_planning(orders_data, waves_per_day=4)
print("Wave Summary:")
print(wave_summary)
```

### Cluster Picking

**Description:**
- Pick multiple orders to a multi-compartment cart
- Each compartment represents an order
- Pick all orders simultaneously

**Benefits:**
- High productivity (combine benefits of batch and discrete)
- Maintain order integrity
- Ideal for e-commerce (small orders, many SKUs)

**Equipment:**
- Pick carts with 4-12 totes/compartments
- Voice or RF-directed picking

---

## Pick Path Optimization

### Routing Strategies

**1. S-Shape Routing**
- Enter aisles with picks, skip empty aisles
- Most common, simple to implement

**2. Return Routing**
- Enter and exit same end of aisle
- Good for selective aisles with few picks

**3. Midpoint Routing**
- Enter nearest end of aisle
- Most efficient for random pick locations

**4. Largest Gap**
- Skip largest gap between picks in aisle
- Optimal for most scenarios

```python
def calculate_pick_path_distance(pick_locations, aisle_length_ft=100,
                                aisle_width_ft=10, routing='s-shape'):
    """
    Calculate travel distance for pick path

    Parameters:
    - pick_locations: List of tuples [(aisle, position_pct), ...]
    - aisle_length_ft: Length of aisle
    - aisle_width_ft: Width between aisles
    - routing: 's-shape', 'return', 'largest-gap'

    Returns:
    - Total travel distance
    """

    # Group picks by aisle
    aisles_with_picks = {}
    for aisle, position in pick_locations:
        if aisle not in aisles_with_picks:
            aisles_with_picks[aisle] = []
        aisles_with_picks[aisle].append(position)

    total_distance = 0

    if routing == 's-shape':
        # Traverse aisles with picks, skip empty
        for aisle, positions in sorted(aisles_with_picks.items()):
            # Full aisle length + cross-aisle
            total_distance += aisle_length_ft + aisle_width_ft

    elif routing == 'return':
        # Enter and exit same end
        for aisle, positions in aisles_with_picks.items():
            max_position = max(positions)
            # Go to furthest pick and return
            total_distance += (max_position * aisle_length_ft * 2) + aisle_width_ft

    elif routing == 'largest-gap':
        # Optimal routing (simplified)
        for aisle, positions in aisles_with_picks.items():
            positions_sorted = sorted(positions)

            # Find largest gap
            gaps = [positions_sorted[i+1] - positions_sorted[i]
                   for i in range(len(positions_sorted)-1)]

            if gaps:
                largest_gap = max(gaps)
                # Distance = full aisle - largest gap
                distance_in_aisle = aisle_length_ft * (1 - largest_gap)
            else:
                distance_in_aisle = positions_sorted[0] * aisle_length_ft

            total_distance += distance_in_aisle + aisle_width_ft

    return round(total_distance, 1)

# Example pick path
picks = [
    (1, 0.2),   # Aisle 1, 20% down
    (1, 0.8),   # Aisle 1, 80% down
    (3, 0.5),   # Aisle 3, 50% down
    (5, 0.3),   # Aisle 5, 30% down
]

for routing in ['s-shape', 'return', 'largest-gap']:
    distance = calculate_pick_path_distance(picks, routing=routing)
    print(f"{routing}: {distance} ft")
```

---

## Packing Operations

### Packing Strategies

**1. Single-Pass Packing**
- Pick directly into shipping box
- Fastest, but requires known box size
- Good for single-item orders

**2. Pack Station (Traditional)**
- Central packing area
- Pickers bring items to packers
- Flexibility in box selection

**3. In-Line Packing**
- Pack as you pick
- Requires pick-to-belt or cart system

**4. Automated Packing**
- Auto-box selection and sealing
- High throughput (500+ boxes/hour)
- Capital intensive ($500K+)

### Box Selection Optimization

```python
def optimize_box_selection(order_items, box_inventory):
    """
    Select optimal box size for order

    Parameters:
    - order_items: List of dicts [{'sku': 'A', 'qty': 2, 'dims': (10,8,4)}, ...]
    - box_inventory: List of available boxes [{'box_id': 'Small', 'dims': (12,10,8), 'cost': 0.50}, ...]

    Returns:
    - Optimal box selection
    """

    # Calculate total volume needed
    total_volume = sum(
        item['qty'] * item['dims'][0] * item['dims'][1] * item['dims'][2]
        for item in order_items
    )

    # Find boxes that fit (with utilization target)
    target_utilization = 0.80  # 80% full
    required_volume = total_volume / target_utilization

    suitable_boxes = [
        box for box in box_inventory
        if box['dims'][0] * box['dims'][1] * box['dims'][2] >= required_volume
    ]

    if not suitable_boxes:
        return None

    # Select smallest suitable box (minimize cost)
    optimal_box = min(suitable_boxes,
                     key=lambda b: b['dims'][0] * b['dims'][1] * b['dims'][2])

    actual_volume = optimal_box['dims'][0] * optimal_box['dims'][1] * optimal_box['dims'][2]
    utilization = total_volume / actual_volume

    return {
        'box_id': optimal_box['box_id'],
        'box_dims': optimal_box['dims'],
        'box_cost': optimal_box['cost'],
        'utilization_%': round(utilization * 100, 1)
    }

# Example
order = [
    {'sku': 'A', 'qty': 1, 'dims': (10, 8, 4)},
    {'sku': 'B', 'qty': 2, 'dims': (6, 6, 3)}
]

boxes = [
    {'box_id': 'Small', 'dims': (12, 10, 8), 'cost': 0.50},
    {'box_id': 'Medium', 'dims': (18, 14, 12), 'cost': 0.75},
    {'box_id': 'Large', 'dims': (24, 18, 16), 'cost': 1.00}
]

result = optimize_box_selection(order, boxes)
if result:
    print(f"Optimal box: {result['box_id']}")
    print(f"Utilization: {result['utilization_%']}%")
    print(f"Cost: ${result['box_cost']}")
```

### Packing Labor Requirements

```python
def packing_labor_requirements(orders_per_day, packing_rate_per_hour=40,
                               working_hours=8, multi_item_pct=0.60):
    """
    Calculate packing labor needs

    Parameters:
    - orders_per_day: Daily order volume
    - packing_rate_per_hour: Orders packed per person per hour
    - working_hours: Working hours per shift
    - multi_item_pct: % of orders with multiple items (slower to pack)

    Returns:
    - Packing labor requirements
    """

    # Adjust rate for multi-item orders
    multi_item_orders = orders_per_day * multi_item_pct
    single_item_orders = orders_per_day * (1 - multi_item_pct)

    # Multi-item takes ~1.5x longer
    equivalent_orders = single_item_orders + (multi_item_orders * 1.5)

    # Labor hours needed
    labor_hours = equivalent_orders / packing_rate_per_hour

    # Packers needed
    packers_needed = labor_hours / working_hours

    # Packing stations needed (assume 80% utilization)
    stations_needed = packers_needed / 0.80

    return {
        'orders_per_day': orders_per_day,
        'equivalent_orders': round(equivalent_orders, 0),
        'labor_hours_needed': round(labor_hours, 1),
        'packers_needed': round(packers_needed, 1),
        'packing_stations_needed': int(np.ceil(stations_needed))
    }

# Example
packing = packing_labor_requirements(
    orders_per_day=2000,
    packing_rate_per_hour=40,
    working_hours=8,
    multi_item_pct=0.60
)

print(f"Packers needed: {packing['packers_needed']}")
print(f"Packing stations: {packing['packing_stations_needed']}")
```

---

## Shipping Operations

### Carrier Selection & Rate Shopping

```python
def carrier_rate_shopping(order_weight_lbs, order_dims, destination_zip,
                         origin_zip, delivery_speed='ground'):
    """
    Compare carrier rates (simplified example)

    In practice, integrate with carrier APIs:
    - UPS API
    - FedEx API
    - USPS API
    """

    # Simplified rate tables (actual rates vary by contract, zone, etc.)
    rates = {
        'UPS': {
            'ground': 8.50 + (order_weight_lbs * 0.50),
            '2day': 15.00 + (order_weight_lbs * 0.75),
            'overnight': 35.00 + (order_weight_lbs * 1.50)
        },
        'FedEx': {
            'ground': 8.75 + (order_weight_lbs * 0.48),
            '2day': 14.50 + (order_weight_lbs * 0.70),
            'overnight': 32.00 + (order_weight_lbs * 1.40)
        },
        'USPS': {
            'ground': 7.50 + (order_weight_lbs * 0.45),
            '2day': 13.00 + (order_weight_lbs * 0.65),
            'overnight': 30.00 + (order_weight_lbs * 1.30)
        }
    }

    # Calculate dimensional weight
    dim_weight = (order_dims[0] * order_dims[1] * order_dims[2]) / 139
    billable_weight = max(order_weight_lbs, dim_weight)

    carrier_quotes = {}
    for carrier, speeds in rates.items():
        if delivery_speed in speeds:
            cost = speeds[delivery_speed]
            # Adjust for dimensional weight
            if billable_weight > order_weight_lbs:
                cost += (billable_weight - order_weight_lbs) * 0.50

            carrier_quotes[carrier] = round(cost, 2)

    # Find cheapest
    optimal_carrier = min(carrier_quotes, key=carrier_quotes.get)

    return {
        'carrier_quotes': carrier_quotes,
        'optimal_carrier': optimal_carrier,
        'optimal_cost': carrier_quotes[optimal_carrier],
        'billable_weight': round(billable_weight, 1)
    }

# Example
shipping = carrier_rate_shopping(
    order_weight_lbs=5.0,
    order_dims=(16, 12, 8),  # inches
    destination_zip='90210',
    origin_zip='10001',
    delivery_speed='ground'
)

print("Carrier Quotes:")
for carrier, cost in shipping['carrier_quotes'].items():
    print(f"  {carrier}: ${cost}")
print(f"\nOptimal: {shipping['optimal_carrier']} - ${shipping['optimal_cost']}")
```

### Manifest & Load Planning

```python
def manifest_optimization(orders_df, trailer_capacity=50000, carrier='UPS'):
    """
    Optimize order manifesting and trailer loading

    Parameters:
    - orders_df: DataFrame with ['order_id', 'weight', 'cube', 'carrier']
    - trailer_capacity: Trailer capacity (lbs or cube)
    - carrier: Filter orders by carrier
    """

    # Filter orders for carrier
    carrier_orders = orders_df[orders_df['carrier'] == carrier].copy()

    # Sort by weight (LIFO loading - heavy first)
    carrier_orders = carrier_orders.sort_values('weight', ascending=False)

    # Assign to trailers
    trailers = []
    current_trailer = {'orders': [], 'weight': 0, 'cube': 0}

    for _, order in carrier_orders.iterrows():
        # Check if fits in current trailer
        if current_trailer['weight'] + order['weight'] <= trailer_capacity:
            current_trailer['orders'].append(order['order_id'])
            current_trailer['weight'] += order['weight']
            current_trailer['cube'] += order['cube']
        else:
            # Start new trailer
            trailers.append(current_trailer)
            current_trailer = {
                'orders': [order['order_id']],
                'weight': order['weight'],
                'cube': order['cube']
            }

    # Add last trailer
    if current_trailer['orders']:
        trailers.append(current_trailer)

    # Summary
    manifest_summary = {
        'carrier': carrier,
        'total_orders': len(carrier_orders),
        'trailers_needed': len(trailers),
        'avg_weight_per_trailer': round(np.mean([t['weight'] for t in trailers]), 0),
        'avg_utilization_%': round(np.mean([t['weight']/trailer_capacity for t in trailers]) * 100, 1)
    }

    return trailers, manifest_summary

# Example
orders = pd.DataFrame({
    'order_id': [f'ORD_{i}' for i in range(1, 501)],
    'weight': np.random.uniform(10, 200, 500),
    'cube': np.random.uniform(1, 20, 500),
    'carrier': np.random.choice(['UPS', 'FedEx', 'USPS'], 500)
})

trailers, summary = manifest_optimization(orders, trailer_capacity=10000, carrier='UPS')
print(f"Carrier: {summary['carrier']}")
print(f"Trailers needed: {summary['trailers_needed']}")
print(f"Average utilization: {summary['avg_utilization_%']}%")
```

---

## Fulfillment Performance Metrics

### Key Performance Indicators (KPIs)

```python
def calculate_fulfillment_kpis(total_orders, orders_on_time, orders_accurate,
                              total_units, labor_hours, total_cost):
    """
    Calculate fulfillment KPIs

    Parameters:
    - total_orders: Orders processed
    - orders_on_time: Orders shipped on time
    - orders_accurate: Orders shipped accurately
    - total_units: Total units shipped
    - labor_hours: Total labor hours
    - total_cost: Total fulfillment cost
    """

    # On-time delivery rate
    on_time_rate = orders_on_time / total_orders

    # Order accuracy
    accuracy_rate = orders_accurate / total_orders

    # Units per labor hour
    units_per_hour = total_units / labor_hours

    # Orders per labor hour
    orders_per_hour = total_orders / labor_hours

    # Cost per order
    cost_per_order = total_cost / total_orders

    # Cost per unit
    cost_per_unit = total_cost / total_units

    kpis = {
        'On_Time_Delivery_%': round(on_time_rate * 100, 2),
        'Order_Accuracy_%': round(accuracy_rate * 100, 2),
        'Units_per_Labor_Hour': round(units_per_hour, 1),
        'Orders_per_Labor_Hour': round(orders_per_hour, 1),
        'Cost_per_Order': round(cost_per_order, 2),
        'Cost_per_Unit': round(cost_per_unit, 2)
    }

    return kpis

# Example
kpis = calculate_fulfillment_kpis(
    total_orders=10000,
    orders_on_time=9700,
    orders_accurate=9950,
    total_units=50000,
    labor_hours=1200,
    total_cost=120000
)

print("Fulfillment KPIs:")
for metric, value in kpis.items():
    print(f"  {metric}: {value}")
```

### Benchmark Targets

| Metric | Target | World-Class |
|--------|--------|-------------|
| Order Accuracy | 99%+ | 99.8%+ |
| On-Time Shipment | 95%+ | 99%+ |
| Units per Labor Hour | 100-150 | 200+ |
| Pick Accuracy | 99.5%+ | 99.9%+ |
| Cost per Order | $3-$8 | <$3 |
| Orders per Labor Hour | 15-25 | 30+ |
| Dock-to-Stock Time | <24 hrs | <4 hrs |

---

## Advanced Fulfillment Strategies

### Multi-Channel Fulfillment

**Strategies:**
- **Dedicated inventory**: Separate stock for each channel
- **Shared inventory**: Single pool, allocate dynamically
- **Hybrid**: Fast movers shared, slow movers dedicated

```python
def multi_channel_inventory_allocation(total_inventory, channels):
    """
    Allocate inventory across channels

    Parameters:
    - total_inventory: Total available inventory
    - channels: Dict with channel: {'demand_rate': X, 'priority': Y}

    Returns:
    - Inventory allocation by channel
    """

    # Calculate total demand
    total_demand = sum(ch['demand_rate'] for ch in channels.values())

    allocations = {}

    for channel, data in channels.items():
        # Proportional allocation based on demand
        base_allocation = (data['demand_rate'] / total_demand) * total_inventory

        # Adjust for priority (higher priority gets +10% buffer)
        priority_factor = 1 + ((data['priority'] - 2) * 0.10)  # Priority 1-3
        allocation = base_allocation * priority_factor

        allocations[channel] = round(allocation, 0)

    # Normalize to total inventory
    adjustment_factor = total_inventory / sum(allocations.values())
    allocations = {ch: round(qty * adjustment_factor, 0)
                  for ch, qty in allocations.items()}

    return allocations

# Example
channels = {
    'Retail_Stores': {'demand_rate': 1000, 'priority': 1},
    'Ecommerce': {'demand_rate': 800, 'priority': 2},
    'Wholesale': {'demand_rate': 500, 'priority': 3}
}

allocation = multi_channel_inventory_allocation(10000, channels)
print("Inventory Allocation:")
for channel, qty in allocation.items():
    print(f"  {channel}: {qty} units")
```

### Returns Processing

**Reverse Logistics Process:**
1. Customer initiates return
2. Generate return label
3. Receive at facility
4. Inspect and grade condition
5. Disposition (restock, liquidate, destroy)
6. Process refund/exchange

```python
def returns_processing_analysis(returns_per_day, inspection_rate_per_hour=50,
                               restock_pct=0.70, liquidate_pct=0.25,
                               destroy_pct=0.05):
    """
    Analyze returns processing requirements

    Parameters:
    - returns_per_day: Daily return volume
    - inspection_rate_per_hour: Returns inspected per person per hour
    - restock_pct, liquidate_pct, destroy_pct: Disposition percentages
    """

    # Labor for inspection
    labor_hours = returns_per_day / inspection_rate_per_hour

    # Disposition volumes
    restock_units = returns_per_day * restock_pct
    liquidate_units = returns_per_day * liquidate_pct
    destroy_units = returns_per_day * destroy_pct

    # Financial impact (example)
    # Assume average unit value $50
    avg_unit_value = 50

    # Restock: 90% recovery
    # Liquidate: 20% recovery
    # Destroy: 0% recovery

    value_recovered = (restock_units * avg_unit_value * 0.90 +
                      liquidate_units * avg_unit_value * 0.20)

    value_lost = (restock_units * avg_unit_value * 0.10 +
                 liquidate_units * avg_unit_value * 0.80 +
                 destroy_units * avg_unit_value)

    return {
        'returns_per_day': returns_per_day,
        'inspection_hours': round(labor_hours, 1),
        'restock_units': round(restock_units, 0),
        'liquidate_units': round(liquidate_units, 0),
        'destroy_units': round(destroy_units, 0),
        'value_recovered_daily': round(value_recovered, 0),
        'value_lost_daily': round(value_lost, 0),
        'recovery_rate_%': round((value_recovered / (value_recovered + value_lost)) * 100, 1)
    }

# Example
returns = returns_processing_analysis(
    returns_per_day=100,
    inspection_rate_per_hour=50
)

print(f"Returns per day: {returns['returns_per_day']}")
print(f"Inspection hours: {returns['inspection_hours']}")
print(f"Restock: {returns['restock_units']} units")
print(f"Value recovery rate: {returns['recovery_rate_%']}%")
```

---

## Tools & Libraries

### Warehouse Management Systems (WMS)

**Enterprise WMS:**
- **Manhattan Associates**: Tier 1 WMS, highly configurable
- **Blue Yonder (JDA)**: Warehouse management suite
- **SAP EWM**: Extended warehouse management
- **Oracle WMS**: Cloud-based warehouse management
- **Infor WMS**: Industry-specific solutions

**Mid-Market WMS:**
- **HighJump (Korber)**: Flexible WMS
- **NetSuite WMS**: Cloud ERP with WMS
- **Fishbowl**: Small to mid-market
- **3PL Central**: 3PL-focused WMS

**Open Source:**
- **Odoo**: Open-source ERP with WMS modules
- **iDempiere**: Open-source ERP/WMS

### Technology Stack

**Hardware:**
- RF scanners (Zebra, Honeywell)
- Mobile computers
- Voice picking systems (Vocollect, Honeywell)
- Label printers (Zebra ZT series)
- Automated sortation
- Pick-to-light / put-to-light

**Software Integrations:**
- OMS (Order Management System)
- TMS (Transportation Management)
- Carrier integrations (APIs)
- E-commerce platforms (Shopify, Magento)

---

## Common Challenges & Solutions

### Challenge: Order Accuracy Issues

**Problem:**
- Picking wrong items or quantities
- Shipping incorrect orders
- Customer complaints and returns

**Solutions:**
- Implement barcode scanning verification
- Use pick-to-light or voice picking
- Require dual verification for high-value items
- QA checkweigh at packing
- Root cause analysis on errors
- Picker training and accountability

### Challenge: Labor Productivity Variability

**Problem:**
- Inconsistent picker rates
- Some workers much slower than others
- Difficult to staff appropriately

**Solutions:**
- Implement labor management system (LMS)
- Track individual productivity
- Gamification and incentives
- Standard work procedures
- Ongoing training
- Ergonomic improvements

### Challenge: Peak Season Capacity

**Problem:**
- 2-3x normal volume during holidays
- Can't hire/train enough temporary workers
- Space constraints

**Solutions:**
- Start hiring/training 2+ months early
- Extended hours (add shifts)
- Simplify processes for temps
- Overflow to 3PL partners
- Automation (scales better than labor)
- Wave planning to spread work

### Challenge: Shipping Cost Escalation

**Problem:**
- Carrier rates increasing
- Dimensional weight charges
- Residential surcharges

**Solutions:**
- Rate shop across carriers
- Negotiate better contracts (volume commitments)
- Right-size packaging (avoid dim weight)
- Zone skipping (bulk to local carrier facility)
- Regional fulfillment centers (reduce zones)
- Customer incentives for slower shipping

### Challenge: Returns Volume

**Problem:**
- High return rates (especially apparel)
- Processing costs add up
- Inventory loss from damaged returns

**Solutions:**
- Better product descriptions (reduce wrong item returns)
- Free returns policy vs. cost trade-off
- Efficient returns processing
- Improve disposition logic (maximize restock %)
- Returns analytics to identify root causes
- Consider restocking fees for policy returns

---

## Output Format

### Fulfillment Operations Design Document

**Executive Summary:**
- Order volume and profile
- Recommended fulfillment strategy
- Labor requirements and costs
- Expected performance metrics

**Order Profile:**

| Metric | Value |
|--------|-------|
| Orders per Day (Avg) | 2,000 |
| Orders per Day (Peak) | 5,000 |
| Lines per Order | 5.2 |
| Units per Order | 6.8 |
| Order Types | 60% each, 30% case, 10% pallet |

**Recommended Picking Strategy:**
- **Fast movers (A items)**: Zone picking, dedicated forward pick area
- **Medium movers (B items)**: Batch picking, 10 orders per batch
- **Slow movers (C items)**: Discrete picking from reserve

**Labor Requirements:**

| Function | Staff Needed | Hours per Day | Shifts |
|----------|--------------|---------------|--------|
| Picking | 15 | 120 | 2 shifts |
| Packing | 10 | 80 | 2 shifts |
| Shipping | 5 | 40 | 2 shifts |
| Returns | 2 | 16 | 1 shift |
| **Total** | **32** | **256** | - |

**Technology Requirements:**
- WMS with wave planning and task management
- RF scanners for all pickers (20 units)
- Pack stations with scales and label printers (12 stations)
- Shipping manifesting software with carrier integrations
- Pick-to-light for fast movers (optional, $200K)

**Performance Targets:**

| KPI | Target | Current (if optimizing) |
|-----|--------|-------------------------|
| Order Accuracy | 99.5% | 97.2% |
| On-Time Shipment | 98% | 92% |
| Cost per Order | $5.50 | $7.20 |
| Units per Labor Hour | 150 | 110 |

**Implementation Plan:**
1. Months 1-2: WMS implementation and configuration
2. Month 3: Slotting optimization and layout changes
3. Month 4: Process rollout and training
4. Month 5: Ramp-up and optimization
5. Month 6: Full production, continuous improvement

---

## Questions to Ask

If you need more context:
1. What's the order volume? (daily average and peak)
2. What's the order profile? (lines/order, units/order, types)
3. What's the SKU count and velocity distribution?
4. What are the service requirements? (delivery speed, accuracy)
5. What's the current fulfillment process and pain points?
6. What technology is in place? (WMS, automation, RF scanning)
7. What's the labor availability and cost in your market?
8. What's the budget for improvements?

---

## Related Skills

- **warehouse-design**: Design facility layout for fulfillment
- **warehouse-slotting-optimization**: Optimize product placement
- **picker-routing-optimization**: Optimize pick paths
- **order-batching-optimization**: Batch order optimization
- **wave-planning-optimization**: Wave release optimization
- **ecommerce-fulfillment**: E-commerce specific strategies
- **omnichannel-fulfillment**: Multi-channel fulfillment
- **last-mile-delivery**: Final delivery optimization
