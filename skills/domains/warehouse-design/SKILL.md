---
name: warehouse-design
description: When the user wants to design a warehouse, optimize warehouse layout, determine facility size, or configure storage systems. Also use when the user mentions "warehouse layout," "facility design," "warehouse sizing," "storage systems," "material flow," "pick path design," "dock configuration," or "space utilization." For warehouse location selection, see facility-location-problem. For slotting existing warehouses, see warehouse-slotting-optimization.
---

# Warehouse Design

You are an expert in warehouse design and facility planning. Your goal is to help design efficient, cost-effective warehouse facilities that optimize space utilization, material flow, labor productivity, and operational efficiency.

## Initial Assessment

Before designing a warehouse, understand:

1. **Business Requirements**
   - What products will be stored? (SKU count, variety)
   - What's the throughput? (units/day, orders/day)
   - Growth projections? (3-5 year horizon)
   - Special requirements? (temperature control, hazmat, security)

2. **Operational Profile**
   - Order profile? (B2B pallets, B2C eaches, mixed)
   - Peak vs. average volume? (seasonality factor)
   - SKU velocity distribution? (fast/medium/slow movers)
   - Value-added services? (kitting, labeling, returns)

3. **Physical Constraints**
   - Site available? (dimensions, shape, constraints)
   - Building type? (new construction, existing retrofit)
   - Clear height available?
   - Column spacing and floor loading capacity?

4. **Current State**
   - Existing operations to replicate or improve?
   - Current space utilization and pain points?
   - Technology already invested in?
   - Workforce considerations?

---

## Warehouse Design Framework

### Design Principles

**1. Minimize Material Handling**
- Straight-line flow preferred
- Minimize touches and moves
- Direct putaway when possible
- Cross-docking opportunities

**2. Maximize Space Utilization**
- Vertical storage (use height)
- Dense storage for slow movers
- Efficient aisle configuration
- Right-size equipment for space

**3. Optimize Labor Productivity**
- Minimize travel distance
- Batch similar activities
- Ergonomic workstation design
- Balance workload

**4. Enable Flexibility**
- Accommodate growth
- Support multiple order types
- Scalable systems
- Adaptable layout

**5. Ensure Safety & Compliance**
- Fire codes and sprinkler requirements
- ADA accessibility
- OSHA regulations
- Product-specific regulations (food, pharma)

---

## Warehouse Sizing & Capacity

### Space Calculation Methodology

**Storage Space Required:**

```python
import numpy as np
import pandas as pd

def calculate_storage_space(sku_data, peak_factor=1.5, utilization_target=0.85):
    """
    Calculate required warehouse storage space

    Parameters:
    - sku_data: DataFrame with columns ['sku', 'avg_inventory', 'pallet_positions']
    - peak_factor: Peak inventory as multiple of average (e.g., 1.5 = 50% above avg)
    - utilization_target: Target space utilization (0.85 = 85%)

    Returns:
    - Required pallet positions
    """

    # Calculate peak inventory
    sku_data = sku_data.copy()
    sku_data['peak_inventory'] = sku_data['avg_inventory'] * peak_factor

    # Total pallet positions needed
    total_positions = sku_data['pallet_positions'].sum()

    # Adjust for utilization target (need more positions than peak to maintain flow)
    required_positions = total_positions / utilization_target

    return {
        'avg_pallet_positions': sku_data['pallet_positions'].sum(),
        'peak_pallet_positions': total_positions,
        'required_positions': round(required_positions, 0),
        'utilization_target': utilization_target
    }

# Example
sku_data = pd.DataFrame({
    'sku': [f'SKU_{i}' for i in range(1, 101)],
    'avg_inventory': np.random.randint(10, 500, 100),
    'pallet_positions': np.random.randint(1, 50, 100)
})

storage_req = calculate_storage_space(sku_data, peak_factor=1.5, utilization_target=0.85)
print(f"Required pallet positions: {storage_req['required_positions']}")
```

**Total Warehouse Square Footage:**

```python
def warehouse_sizing(storage_positions, storage_type='selective',
                     receiving_docks=10, shipping_docks=15,
                     value_added_sq_ft=5000):
    """
    Calculate total warehouse square footage

    storage_type: 'selective', 'drive-in', 'push-back', 'pallet-flow'
    """

    # Square feet per pallet position by storage type
    sq_ft_per_position = {
        'selective': 30,      # Single-deep racking, most accessible
        'double-deep': 22,    # Double-deep, less accessible
        'drive-in': 18,       # High density, LIFO
        'push-back': 20,      # High density, LIFO
        'pallet-flow': 25,    # FIFO, dynamic
        'floor-stacked': 15   # Very dense, limited access
    }

    storage_sq_ft = storage_positions * sq_ft_per_position.get(storage_type, 30)

    # Receiving area (assume 2000 sq ft per dock door)
    receiving_sq_ft = receiving_docks * 2000

    # Shipping area (assume 1500 sq ft per dock door)
    shipping_sq_ft = shipping_docks * 1500

    # Aisles and circulation (20-30% of storage)
    circulation_sq_ft = storage_sq_ft * 0.25

    # Office, break rooms, restrooms (5-10% of total)
    support_sq_ft = (storage_sq_ft + receiving_sq_ft + shipping_sq_ft) * 0.08

    # Total
    total_sq_ft = (storage_sq_ft +
                   receiving_sq_ft +
                   shipping_sq_ft +
                   circulation_sq_ft +
                   value_added_sq_ft +
                   support_sq_ft)

    breakdown = {
        'Storage': round(storage_sq_ft, 0),
        'Receiving': round(receiving_sq_ft, 0),
        'Shipping': round(shipping_sq_ft, 0),
        'Circulation': round(circulation_sq_ft, 0),
        'Value_Added': value_added_sq_ft,
        'Support': round(support_sq_ft, 0),
        'Total': round(total_sq_ft, 0)
    }

    return breakdown

# Example
sizing = warehouse_sizing(
    storage_positions=5000,
    storage_type='selective',
    receiving_docks=10,
    shipping_docks=15,
    value_added_sq_ft=5000
)

print("Warehouse Space Breakdown:")
for area, sq_ft in sizing.items():
    print(f"  {area}: {sq_ft:,.0f} sq ft")

print(f"\nTotal warehouse size: {sizing['Total']:,.0f} sq ft")
```

### Throughput Capacity Analysis

```python
def throughput_capacity(storage_positions, picks_per_day, orders_per_day,
                       lines_per_order=5, pick_rate_per_hour=100):
    """
    Analyze warehouse throughput capacity

    Parameters:
    - storage_positions: Total pallet positions
    - picks_per_day: Daily pick volume (lines)
    - orders_per_day: Daily order volume
    - lines_per_order: Average lines per order
    - pick_rate_per_hour: Picks per person per hour

    Returns:
    - Capacity analysis and labor requirements
    """

    # Labor calculations
    picks_per_day = orders_per_day * lines_per_order
    hours_per_day = 16  # Assume 2-shift operation
    pickers_needed = picks_per_day / (pick_rate_per_hour * hours_per_day)

    # Receiving capacity (pallets per dock per day)
    pallets_per_dock_day = 80  # Industry average
    receiving_capacity = pallets_per_dock_day  # per dock

    # Shipping capacity (orders per dock per day)
    orders_per_dock_day = 100  # Depends on order size
    shipping_capacity = orders_per_dock_day  # per dock

    return {
        'picks_per_day': picks_per_day,
        'pickers_needed': round(pickers_needed, 1),
        'receiving_pallets_per_dock': pallets_per_dock_day,
        'shipping_orders_per_dock': orders_per_dock_day
    }

# Example
capacity = throughput_capacity(
    storage_positions=5000,
    picks_per_day=0,  # Will calculate
    orders_per_day=2000,
    lines_per_order=5,
    pick_rate_per_hour=100
)

print(f"Daily picks: {capacity['picks_per_day']}")
print(f"Pickers needed: {capacity['pickers_needed']}")
```

---

## Warehouse Layout Design

### Layout Types

**1. U-Shaped Flow**
- Receiving and shipping on same side
- Compact footprint
- Good for smaller facilities
- Easy cross-docking

**2. Straight-Through (I-Flow)**
- Receiving on one end, shipping on opposite
- Long, narrow buildings
- Minimizes backtracking
- Clear separation of inbound/outbound

**3. L-Shaped Flow**
- Receiving on one side, shipping on adjacent
- Good for corner lots
- Moderate flow efficiency

**4. T-Shaped Flow**
- Receiving on one side, shipping splits to two sides
- Accommodates multiple shipping areas
- Complex flow patterns

### Functional Zones

```python
def design_functional_zones(total_sq_ft, order_profile='mixed'):
    """
    Allocate space to functional zones

    order_profile: 'pallet', 'case', 'each', 'mixed'
    """

    # Space allocation percentages by order profile
    allocations = {
        'pallet': {
            'Reserve_Storage': 0.50,
            'Forward_Pick': 0.10,
            'Receiving': 0.12,
            'Shipping': 0.15,
            'Value_Added': 0.03,
            'Support': 0.10
        },
        'each': {
            'Reserve_Storage': 0.35,
            'Forward_Pick': 0.25,
            'Receiving': 0.10,
            'Shipping': 0.15,
            'Value_Added': 0.05,
            'Support': 0.10
        },
        'mixed': {
            'Reserve_Storage': 0.40,
            'Forward_Pick': 0.20,
            'Receiving': 0.12,
            'Shipping': 0.15,
            'Value_Added': 0.05,
            'Support': 0.08
        }
    }

    profile_alloc = allocations.get(order_profile, allocations['mixed'])

    zones = {
        zone: round(total_sq_ft * pct, 0)
        for zone, pct in profile_alloc.items()
    }

    return zones

# Example
zones = design_functional_zones(200000, order_profile='mixed')
print("Functional Zone Allocation:")
for zone, sq_ft in zones.items():
    print(f"  {zone}: {sq_ft:,.0f} sq ft ({sq_ft/sum(zones.values())*100:.1f}%)")
```

---

## Storage Systems Selection

### Storage System Comparison

| System | Density | Selectivity | FIFO/LIFO | Cost | Best For |
|--------|---------|-------------|-----------|------|----------|
| Selective Rack | Low | 100% | Either | $ | Fast movers, high SKU count |
| Double-Deep | Medium | 50% | LIFO | $$ | Medium velocity, paired SKUs |
| Drive-In/Drive-Through | High | 10-20% | LIFO/FIFO | $$ | Slow movers, few SKUs, lots of inventory |
| Push-Back | High | 25-30% | LIFO | $$$ | High volume, limited SKUs |
| Pallet Flow | High | 100% | FIFO | $$$$ | High velocity, date-sensitive |
| Automated AS/RS | Very High | 100% | Either | $$$$$ | Very high volume, limited labor |

### Storage System Selection Logic

```python
def select_storage_system(sku_velocity, sku_diversity, fifo_required=False,
                         space_constraint=False):
    """
    Recommend storage system based on operational requirements

    Parameters:
    - sku_velocity: 'fast', 'medium', 'slow'
    - sku_diversity: 'high' (>1000 SKUs), 'medium' (100-1000), 'low' (<100)
    - fifo_required: True if FIFO needed (perishables, date-coded)
    - space_constraint: True if space is at premium
    """

    recommendations = []

    if sku_diversity == 'high':
        if sku_velocity == 'fast':
            recommendations.append({
                'system': 'Selective Racking',
                'reason': 'High SKU count requires full selectivity',
                'priority': 1
            })
            if space_constraint:
                recommendations.append({
                    'system': 'Narrow Aisle (VNA)',
                    'reason': 'Increases density for high SKU count',
                    'priority': 2
                })
        else:
            recommendations.append({
                'system': 'Selective Racking',
                'reason': 'Full selectivity for diverse SKU mix',
                'priority': 1
            })

    elif sku_diversity == 'medium':
        if sku_velocity == 'fast':
            recommendations.append({
                'system': 'Pallet Flow Rack',
                'reason': 'FIFO, high velocity, moderate SKU count',
                'priority': 1 if fifo_required else 2
            })
            recommendations.append({
                'system': 'Push-Back Rack',
                'reason': 'Dense storage, good throughput',
                'priority': 2 if fifo_required else 1
            })
        else:
            recommendations.append({
                'system': 'Double-Deep',
                'reason': 'Good density with reasonable selectivity',
                'priority': 1
            })

    else:  # low SKU diversity
        if space_constraint:
            recommendations.append({
                'system': 'Drive-In Racking',
                'reason': 'Maximum density for low SKU count',
                'priority': 1 if not fifo_required else 2
            })
            if fifo_required:
                recommendations.append({
                    'system': 'Drive-Through Racking',
                    'reason': 'Dense FIFO for low SKU count',
                    'priority': 1
                })

    # Sort by priority
    recommendations.sort(key=lambda x: x['priority'])

    return recommendations

# Example
recs = select_storage_system(
    sku_velocity='fast',
    sku_diversity='high',
    fifo_required=True,
    space_constraint=True
)

print("Storage System Recommendations:")
for rec in recs:
    print(f"  {rec['priority']}. {rec['system']}: {rec['reason']}")
```

### Rack Configuration Calculations

```python
def rack_configuration(clear_height_ft, load_height_ft=5, load_depth_ft=4,
                      aisle_width_ft=12, rack_depth='single'):
    """
    Calculate rack configuration and capacity

    Parameters:
    - clear_height_ft: Building clear height
    - load_height_ft: Height per pallet level
    - load_depth_ft: Depth per pallet position
    - aisle_width_ft: Aisle width for equipment
    - rack_depth: 'single', 'double', 'back-to-back'
    """

    # Calculate number of levels (leave clearance for sprinklers/lights)
    usable_height = clear_height_ft - 4  # 4 ft clearance
    levels = int(usable_height / load_height_ft)

    # Rack bay width (typically 96-108 inches for 2 pallets side-by-side)
    bay_width_ft = 9  # 2 x 42" pallets + structure

    # Calculate positions per bay
    if rack_depth == 'single':
        positions_per_bay = 2  # 2 pallets wide
        depth_ft = load_depth_ft + 2  # Structure
    elif rack_depth == 'double':
        positions_per_bay = 4  # 2 deep x 2 wide
        depth_ft = (load_depth_ft * 2) + 2
    elif rack_depth == 'back-to-back':
        positions_per_bay = 4  # 2 racks back to back, 2 wide each
        depth_ft = (load_depth_ft * 2) + 3  # Shared structure

    # Positions per bay
    positions_per_bay_total = positions_per_bay * levels

    # Linear feet required per bay (includes aisle)
    linear_ft_per_bay = bay_width_ft

    # Calculate density (positions per 1000 sq ft)
    sq_ft_per_bay = bay_width_ft * (depth_ft + aisle_width_ft)
    positions_per_1000_sqft = (positions_per_bay_total / sq_ft_per_bay) * 1000

    return {
        'levels': levels,
        'positions_per_bay': positions_per_bay_total,
        'bay_width_ft': bay_width_ft,
        'depth_ft': depth_ft,
        'sq_ft_per_bay': round(sq_ft_per_bay, 1),
        'positions_per_1000_sqft': round(positions_per_1000_sqft, 1)
    }

# Example
config = rack_configuration(
    clear_height_ft=32,
    load_height_ft=5,
    aisle_width_ft=12,
    rack_depth='single'
)

print(f"Rack levels: {config['levels']}")
print(f"Positions per bay: {config['positions_per_bay']}")
print(f"Density: {config['positions_per_1000_sqft']} positions per 1000 sq ft")
```

---

## Material Handling Equipment Selection

### Equipment Types & Specs

**1. Counterbalance Forklifts**
- Lift height: 15-20 ft
- Aisle width: 12-13 ft
- Use: Receiving, shipping, low-level storage
- Cost: $25K-$40K

**2. Reach Trucks**
- Lift height: 25-35 ft
- Aisle width: 8-10 ft
- Use: Selective racking, better utilization
- Cost: $35K-$50K

**3. Very Narrow Aisle (VNA) / Turret Trucks**
- Lift height: 35-45 ft
- Aisle width: 5-6.5 ft
- Use: Maximum density, high SKU count
- Cost: $60K-$100K+
- Requires wire guidance, flat floors

**4. Order Pickers**
- Lift height: 25-35 ft
- Use: Each/case picking, person-to-goods
- Cost: $40K-$70K

**5. Automated Guided Vehicles (AGV)**
- Lift height: Varies
- Use: Putaway, replenishment, goods-to-person
- Cost: $100K-$200K per vehicle

```python
def select_material_handling_equipment(storage_height_ft, aisle_budget='medium',
                                       throughput_level='medium',
                                       automation_interest=False):
    """
    Recommend material handling equipment

    Parameters:
    - storage_height_ft: How high storage needs to go
    - aisle_budget: 'tight' (<8 ft), 'medium' (8-12 ft), 'wide' (>12 ft)
    - throughput_level: 'low', 'medium', 'high'
    - automation_interest: Considering automation?
    """

    recommendations = []

    if storage_height_ft <= 15:
        recommendations.append({
            'equipment': 'Counterbalance Forklift',
            'aisle_width': '12-13 ft',
            'cost': '$25K-$40K',
            'reason': 'Low height, versatile, lowest cost'
        })

    elif storage_height_ft <= 30:
        if aisle_budget == 'tight':
            recommendations.append({
                'equipment': 'Very Narrow Aisle (VNA)',
                'aisle_width': '5-6.5 ft',
                'cost': '$60K-$100K',
                'reason': 'Maximum space utilization, tight aisles'
            })
        else:
            recommendations.append({
                'equipment': 'Reach Truck',
                'aisle_width': '8-10 ft',
                'cost': '$35K-$50K',
                'reason': 'Good balance of cost and density'
            })

    else:  # > 30 ft
        recommendations.append({
            'equipment': 'VNA or Automated AS/RS',
            'aisle_width': '5-6.5 ft or N/A',
            'cost': '$60K+ or $2M+ system',
            'reason': 'Required for very high storage'
        })

    if automation_interest and throughput_level == 'high':
        recommendations.append({
            'equipment': 'Automated Storage/Retrieval (AS/RS)',
            'aisle_width': 'N/A',
            'cost': '$2M-$10M+ system',
            'reason': 'High throughput, labor savings, accuracy'
        })

    return recommendations

# Example
equipment = select_material_handling_equipment(
    storage_height_ft=28,
    aisle_budget='medium',
    throughput_level='medium',
    automation_interest=False
)

print("Material Handling Equipment Recommendations:")
for eq in equipment:
    print(f"\n  {eq['equipment']}")
    print(f"    Aisle width: {eq['aisle_width']}")
    print(f"    Cost: {eq['cost']}")
    print(f"    Reason: {eq['reason']}")
```

---

## Dock & Receiving/Shipping Design

### Dock Door Calculations

```python
def calculate_dock_doors(inbound_trucks_per_day, outbound_trucks_per_day,
                        hours_of_operation=10, dwell_time_hours=2,
                        utilization_target=0.80):
    """
    Calculate required dock doors

    Parameters:
    - inbound_trucks_per_day: Daily truck arrivals
    - outbound_trucks_per_day: Daily truck departures
    - hours_of_operation: Working hours per day
    - dwell_time_hours: Hours per truck at dock (unload/load time)
    - utilization_target: Target dock utilization (0.80 = 80%)
    """

    # Capacity per dock door per day
    door_capacity = hours_of_operation / dwell_time_hours

    # Receiving doors needed
    receiving_doors_raw = inbound_trucks_per_day / door_capacity
    receiving_doors = receiving_doors_raw / utilization_target

    # Shipping doors needed
    shipping_doors_raw = outbound_trucks_per_day / door_capacity
    shipping_doors = shipping_doors_raw / utilization_target

    return {
        'receiving_doors': int(np.ceil(receiving_doors)),
        'shipping_doors': int(np.ceil(shipping_doors)),
        'total_doors': int(np.ceil(receiving_doors + shipping_doors)),
        'receiving_utilization': receiving_doors_raw / np.ceil(receiving_doors),
        'shipping_utilization': shipping_doors_raw / np.ceil(shipping_doors)
    }

# Example
doors = calculate_dock_doors(
    inbound_trucks_per_day=50,
    outbound_trucks_per_day=70,
    hours_of_operation=16,  # 2 shifts
    dwell_time_hours=2,
    utilization_target=0.80
)

print(f"Receiving doors needed: {doors['receiving_doors']}")
print(f"Shipping doors needed: {doors['shipping_doors']}")
print(f"Total dock doors: {doors['total_doors']}")
print(f"Receiving utilization: {doors['receiving_utilization']:.1%}")
print(f"Shipping utilization: {doors['shipping_utilization']:.1%}")
```

### Dock Configuration

**Design Considerations:**
- **Dock spacing**: 12 ft centers (standard)
- **Dock depth**: 60-80 ft for staging area
- **Turnaround space**: 130-150 ft for 53' trailers
- **Drive-in docks**: Save space but reduce throughput
- **Cross-dock**: Requires receiving and shipping proximity

---

## Pick Path & Slotting Design

### Travel Distance Calculation

```python
def calculate_pick_travel_distance(orders_per_day, lines_per_order,
                                  avg_travel_per_pick_ft=150,
                                  picker_speed_ft_per_min=200):
    """
    Calculate picker travel distance and time

    Parameters:
    - orders_per_day: Daily order volume
    - lines_per_order: Average order lines
    - avg_travel_per_pick_ft: Average travel distance per pick
    - picker_speed_ft_per_min: Walking/driving speed
    """

    picks_per_day = orders_per_day * lines_per_order

    # Total travel distance
    total_travel_ft = picks_per_day * avg_travel_per_pick_ft
    total_travel_miles = total_travel_ft / 5280

    # Travel time
    travel_time_min = total_travel_ft / picker_speed_ft_per_min
    travel_time_hours = travel_time_min / 60

    # If picks per hour = 100, calculate labor needed
    pick_time_hours = picks_per_day / 100

    total_labor_hours = pick_time_hours + travel_time_hours

    return {
        'picks_per_day': picks_per_day,
        'total_travel_miles': round(total_travel_miles, 1),
        'travel_time_hours': round(travel_time_hours, 1),
        'pick_time_hours': round(pick_time_hours, 1),
        'total_labor_hours': round(total_labor_hours, 1),
        'pickers_needed_single_shift': round(total_labor_hours / 8, 1)
    }

# Example
travel = calculate_pick_travel_distance(
    orders_per_day=2000,
    lines_per_order=5,
    avg_travel_per_pick_ft=150,
    picker_speed_ft_per_min=200
)

print(f"Daily picks: {travel['picks_per_day']}")
print(f"Daily travel: {travel['total_travel_miles']} miles")
print(f"Travel time: {travel['travel_time_hours']} hours")
print(f"Pickers needed: {travel['pickers_needed_single_shift']}")
```

### Golden Zone Placement

**Principle:**
- Place fastest movers in most accessible locations
- "Golden zone": Waist to shoulder height, front of rack
- Minimize vertical and horizontal travel

**Implementation:**
See **warehouse-slotting-optimization** skill for detailed algorithms

---

## Automation & Technology

### Warehouse Automation Options

**1. Conveyor Systems**
- Use: Move products between zones
- Cost: $200-$500 per linear foot
- ROI: 2-4 years

**2. Sortation Systems**
- Use: Sort orders/cartons to lanes/destinations
- Types: Sliding shoe, cross-belt, tilt-tray
- Cost: $500K-$3M+
- Throughput: 5K-30K+ units/hour

**3. Automated Storage & Retrieval (AS/RS)**
- Use: Dense storage, high throughput
- Types: Mini-load, unit-load, shuttle systems
- Cost: $2M-$20M+
- ROI: 3-7 years

**4. Goods-to-Person (GTP)**
- Use: Eliminate picker travel
- Types: Vertical lift modules, horizontal carousels, shuttle systems
- Cost: $500K-$5M+
- Pick rates: 200-400+ lines/person/hour

**5. Robotics**
- Types: AMRs (autonomous mobile robots), picking robots, palletizing robots
- Cost: $50K-$200K per robot
- Scalability: Add/remove as needed

**6. Automated Guided Vehicles (AGV)**
- Use: Move pallets/containers
- Cost: $100K-$200K per vehicle
- Requires infrastructure (wires/magnets or LiDAR)

```python
def automation_roi_analysis(current_labor_cost, automation_cost,
                           labor_savings_pct, maintenance_cost_annual,
                           years=5):
    """
    Calculate ROI for warehouse automation

    Parameters:
    - current_labor_cost: Annual labor cost ($)
    - automation_cost: Upfront automation investment ($)
    - labor_savings_pct: Labor reduction (e.g., 0.40 for 40%)
    - maintenance_cost_annual: Annual maintenance ($)
    - years: Analysis period
    """

    annual_savings = current_labor_cost * labor_savings_pct
    annual_net_savings = annual_savings - maintenance_cost_annual

    # Simple payback period
    payback_years = automation_cost / annual_net_savings

    # NPV calculation (assume 10% discount rate)
    discount_rate = 0.10
    npv = -automation_cost
    for year in range(1, years + 1):
        npv += annual_net_savings / ((1 + discount_rate) ** year)

    # ROI
    total_savings = annual_net_savings * years
    roi = (total_savings - automation_cost) / automation_cost

    return {
        'automation_cost': automation_cost,
        'annual_labor_savings': round(annual_savings, 0),
        'annual_maintenance': maintenance_cost_annual,
        'annual_net_savings': round(annual_net_savings, 0),
        'payback_years': round(payback_years, 2),
        'npv_5_year': round(npv, 0),
        'roi_5_year': round(roi, 2)
    }

# Example
roi = automation_roi_analysis(
    current_labor_cost=2_000_000,   # $2M annual labor
    automation_cost=4_000_000,      # $4M automation investment
    labor_savings_pct=0.50,         # 50% labor reduction
    maintenance_cost_annual=200_000, # $200K annual maintenance
    years=5
)

print(f"Automation cost: ${roi['automation_cost']:,.0f}")
print(f"Annual labor savings: ${roi['annual_labor_savings']:,.0f}")
print(f"Annual net savings: ${roi['annual_net_savings']:,.0f}")
print(f"Payback period: {roi['payback_years']} years")
print(f"5-year NPV: ${roi['npv_5_year']:,.0f}")
print(f"5-year ROI: {roi['roi_5_year']:.1%}")
```

---

## Warehouse KPIs & Performance

### Key Performance Indicators

```python
def warehouse_kpis(total_sq_ft, storage_sq_ft, occupied_positions,
                   total_positions, throughput_units, labor_hours,
                   orders_shipped, order_accuracy_pct):
    """
    Calculate warehouse performance KPIs
    """

    # Space utilization
    space_utilization = occupied_positions / total_positions

    # Inventory density
    inventory_density = occupied_positions / (storage_sq_ft / 1000)

    # Productivity
    units_per_labor_hour = throughput_units / labor_hours

    # Order accuracy
    order_accuracy = order_accuracy_pct / 100

    # Operating cost per unit (example)
    # Would need cost inputs for full calculation

    kpis = {
        'Space_Utilization_%': round(space_utilization * 100, 1),
        'Inventory_Density_per_1000sqft': round(inventory_density, 1),
        'Units_per_Labor_Hour': round(units_per_labor_hour, 1),
        'Order_Accuracy_%': round(order_accuracy * 100, 2),
        'Orders_per_Labor_Hour': round(orders_shipped / labor_hours, 1)
    }

    return kpis

# Example
kpis = warehouse_kpis(
    total_sq_ft=200000,
    storage_sq_ft=120000,
    occupied_positions=4200,
    total_positions=5000,
    throughput_units=50000,
    labor_hours=500,
    orders_shipped=2000,
    order_accuracy_pct=99.5
)

print("Warehouse KPIs:")
for metric, value in kpis.items():
    print(f"  {metric}: {value}")
```

---

## Tools & Libraries

### Design & Simulation Software

**CAD/Layout Tools:**
- **AutoCAD**: 2D/3D warehouse layout
- **SketchUp**: 3D visualization
- **Warehouse Blueprint**: Online warehouse design
- **SmartDraw**: Warehouse layout templates

**Simulation:**
- **FlexSim**: 3D simulation modeling
- **AnyLogic**: Multi-method simulation
- **Simio**: Process simulation
- **Arena**: Discrete event simulation
- **SimPy** (Python): Discrete event simulation library

**Analysis:**
- **Excel/Python**: Capacity calculations, ROI analysis
- **Tableau/Power BI**: Performance dashboards

---

## Common Challenges & Solutions

### Challenge: Insufficient Height Utilization

**Problem:**
- Low storage density
- Wasting cubic footage
- Only using 10-15 ft of 30+ ft clear height

**Solutions:**
- Install taller racking (selective or VNA)
- Use reach trucks or order pickers
- Implement mezzanines for picking
- Consider AS/RS for maximum density

### Challenge: Excessive Picker Travel

**Problem:**
- Low productivity
- High labor costs
- Pickers traveling miles per day

**Solutions:**
- Implement velocity-based slotting (see warehouse-slotting-optimization)
- Zone picking or batch picking strategies
- Goods-to-person automation
- Optimize pick path routing
- Forward pick locations for fast movers

### Challenge: Dock Congestion

**Problem:**
- Trucks waiting, detention fees
- Receiving/shipping bottleneck
- Poor appointment scheduling

**Solutions:**
- Add dock doors if capacity constrained
- Implement dock scheduling system (YMS)
- Use cross-docking to bypass storage
- Separate receiving and shipping operations
- Stagger appointments throughout day

### Challenge: Seasonal Volume Fluctuations

**Problem:**
- Facility sized for peak, underutilized off-peak
- Can't handle peak volume
- Temporary labor challenges

**Solutions:**
- Flexible storage (collapsible racks, temporary)
- Overflow space with 3PL partners
- Scale automation (add/remove AMRs)
- Cross-training workforce
- Build for average + use overflow strategy

### Challenge: Mixed Order Profiles

**Problem:**
- Some orders are pallets, some are eaches
- Difficult to optimize for both
- Separate processes inefficient

**Solutions:**
- Zone warehouse by order type
- Separate pallet and each picking areas
- Use multi-modal automation
- Different pick strategies by order type
- Consider separate facilities for very different profiles

---

## Output Format

### Warehouse Design Report

**Executive Summary:**
- Warehouse size and configuration
- Storage capacity (pallet positions)
- Throughput capacity (units/day, orders/day)
- Capital investment required
- Operating cost estimates

**Facility Specifications:**

| Specification | Value |
|---------------|-------|
| Total Square Footage | 250,000 sq ft |
| Clear Height | 32 ft |
| Storage Square Footage | 150,000 sq ft |
| Pallet Positions | 6,500 |
| Receiving Dock Doors | 12 |
| Shipping Dock Doors | 18 |
| Storage System | Selective Racking (80%), Push-Back (20%) |
| Material Handling | Reach Trucks (6), Counterbalance (4) |

**Layout Diagram:**
- Floor plan with functional zones
- Material flow diagram
- Racking layout and aisle configuration

**Capacity Analysis:**

| Metric | Design Capacity | Peak Capacity (1.2x) |
|--------|----------------|----------------------|
| Storage Positions | 6,500 | 7,800 (w/ floor stack) |
| Daily Throughput | 100,000 units | 120,000 units |
| Orders per Day | 3,000 | 3,600 |
| Receiving (pallets/day) | 800 | 960 |
| Shipping (trucks/day) | 90 | 108 |

**Investment Summary:**

| Category | Cost |
|----------|------|
| Building (if new) | $12M |
| Racking Systems | $2.5M |
| Material Handling Equipment | $800K |
| Conveyor/Sortation | $1.5M |
| IT Systems (WMS, etc.) | $500K |
| **Total Capital** | **$17.3M** |

**Operating Costs (Annual):**

| Category | Cost |
|----------|------|
| Labor | $4.5M |
| Lease/Depreciation | $2.0M |
| Utilities | $400K |
| Maintenance | $300K |
| **Total Annual** | **$7.2M** |

**Cost per Unit:** $0.72 per unit shipped

---

## Questions to Ask

If you need more context:
1. What's the throughput requirement? (units/day, orders/day, order profile)
2. What's the SKU count and velocity distribution?
3. What's the growth projection over 3-5 years?
4. Is a site identified? What are the constraints? (size, shape, clear height)
5. What's the order profile? (pallets, cases, eaches, mixed)
6. Are there special requirements? (temp control, hazmat, security)
7. What's the automation appetite and budget?
8. Greenfield or brownfield (existing building)?

---

## Related Skills

- **warehouse-slotting-optimization**: Optimize product placement within warehouse
- **warehouse-automation**: Deep dive into automation systems
- **order-fulfillment**: Pick, pack, ship operations design
- **facility-location-problem**: Where to locate the warehouse
- **picker-routing-optimization**: Optimize pick paths
- **dock-door-assignment**: Optimize dock scheduling
- **cross-docking**: Flow-through operations design
- **warehouse-location-optimization**: Network-level warehouse placement
