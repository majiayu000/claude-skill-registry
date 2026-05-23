---
name: warehouse-automation
description: When the user wants to implement warehouse automation, evaluate automation technologies, or design automated material handling systems. Also use when the user mentions "warehouse robotics," "automated storage," "AS/RS," "goods-to-person," "conveyor systems," "sortation," "AMR," "AGV," "automated picking," or "warehouse automation ROI." For warehouse layout design, see warehouse-design. For order fulfillment, see order-fulfillment.
---

# Warehouse Automation

You are an expert in warehouse automation and material handling systems. Your goal is to help evaluate, design, and implement automation technologies that improve operational efficiency, reduce labor costs, increase accuracy, and enable scalability.

## Initial Assessment

Before implementing automation, understand:

1. **Business Drivers**
   - What's driving automation interest? (labor, accuracy, capacity, throughput)
   - Labor challenges? (availability, cost, turnover)
   - Growth projections? (volume, SKUs, expansion)
   - Service requirements? (speed, accuracy, scalability)

2. **Current Operations**
   - Order volume? (current and projected)
   - Order profile? (lines/order, units/order, size)
   - Current processes and pain points?
   - Warehouse size and configuration?
   - Current technology? (WMS, conveyors, equipment)

3. **Financial Context**
   - Capital budget available?
   - ROI expectations and timeframe?
   - Labor costs (fully loaded with benefits)?
   - Current operational costs?

4. **Constraints**
   - Facility constraints? (ceiling height, floor load, space)
   - Existing systems to integrate with?
   - Operational constraints? (24/7, seasonal peaks)
   - Regulatory requirements? (FDA, safety)

---

## Warehouse Automation Framework

### Automation Technology Spectrum

**Level 0: Manual Operations**
- Paper pick lists
- Manual processes
- High labor, low capital

**Level 1: Basic Technology**
- WMS and RF scanning
- Barcode tracking
- Pick-to-light (simple)
- Basic conveyors

**Level 2: Semi-Automated**
- Conveyor systems
- Sortation systems
- Vertical lift modules (VLM)
- Carousels
- Voice picking

**Level 3: Highly Automated**
- AS/RS (automated storage/retrieval)
- Goods-to-person systems
- AMRs (autonomous mobile robots)
- Automated picking (robotic arms)
- AutoStore / Cube storage

**Level 4: Fully Automated (Lights-Out)**
- End-to-end automation
- Minimal human intervention
- AI-driven optimization
- Self-optimizing systems

---

## Automation Technologies

### 1. Conveyor & Sortation Systems

**Use Cases:**
- Move products between zones
- Sort orders to packing stations or shipping lanes
- Buffer and accumulate inventory

**Types:**

| Type | Throughput | Cost | Best For |
|------|-----------|------|----------|
| Belt Conveyors | Medium | $ | General transport |
| Roller Conveyors | Medium | $ | Pallets, cartons |
| Sliding Shoe Sorter | 5K-15K units/hr | $$$ | High-speed parcel sorting |
| Cross-Belt Sorter | 10K-30K+ units/hr | $$$$ | Very high throughput, fragile items |
| Tilt-Tray Sorter | 5K-20K units/hr | $$$ | Medium to high speed |
| Bomb-Bay Sorter | 3K-10K units/hr | $$ | Case sorting |

```python
import numpy as np
import pandas as pd

def conveyor_sortation_sizing(orders_per_day, items_per_order=5,
                              operating_hours=16, target_utilization=0.75,
                              sorter_type='sliding_shoe'):
    """
    Size conveyor and sortation system

    Parameters:
    - orders_per_day: Daily order volume
    - items_per_order: Average items per order
    - operating_hours: Hours of operation per day
    - target_utilization: Target system utilization (0.75 = 75%)
    - sorter_type: Type of sorter

    Returns:
    - System specifications and cost estimate
    """

    # Calculate required throughput
    items_per_day = orders_per_day * items_per_order
    items_per_hour = items_per_day / operating_hours

    # Required capacity (accounting for utilization)
    required_capacity = items_per_hour / target_utilization

    # Sorter specifications and costs
    sorter_specs = {
        'sliding_shoe': {
            'capacity_range': (5000, 15000),
            'cost_range': (1_500_000, 3_000_000),
            'cost_per_linear_ft': 800
        },
        'cross_belt': {
            'capacity_range': (10000, 30000),
            'cost_range': (3_000_000, 8_000_000),
            'cost_per_linear_ft': 1500
        },
        'tilt_tray': {
            'capacity_range': (5000, 20000),
            'cost_range': (2_000_000, 5_000_000),
            'cost_per_linear_ft': 1000
        }
    }

    spec = sorter_specs[sorter_type]

    # Check if within capacity range
    if required_capacity < spec['capacity_range'][0]:
        recommendation = f"Over-specified. Consider lower throughput solution or {sorter_type} is fine."
    elif required_capacity > spec['capacity_range'][1]:
        recommendation = "Under-specified. Need higher capacity sorter or multiple systems."
    else:
        recommendation = f"{sorter_type.replace('_', ' ').title()} is appropriate."

    # Estimate cost (assume mid-range)
    estimated_cost = np.mean(spec['cost_range'])

    # Estimate conveyor length needed (assume 300 ft)
    conveyor_length_ft = 300
    conveyor_cost = conveyor_length_ft * 500  # $500/ft for belt conveyor

    total_cost = estimated_cost + conveyor_cost

    return {
        'items_per_hour': round(items_per_hour, 0),
        'required_capacity': round(required_capacity, 0),
        'sorter_type': sorter_type,
        'recommendation': recommendation,
        'sorter_cost': estimated_cost,
        'conveyor_cost': conveyor_cost,
        'total_cost': total_cost,
        'cost_per_order': round(total_cost / (orders_per_day * 250), 2)  # Amortized over 250 days/year
    }

# Example
sortation = conveyor_sortation_sizing(
    orders_per_day=5000,
    items_per_order=6,
    operating_hours=16,
    sorter_type='sliding_shoe'
)

print(f"Required capacity: {sortation['required_capacity']} items/hour")
print(f"Recommendation: {sortation['recommendation']}")
print(f"Total cost: ${sortation['total_cost']:,.0f}")
print(f"Cost per order (amortized): ${sortation['cost_per_order']}")
```

### 2. Automated Storage & Retrieval Systems (AS/RS)

**Use Cases:**
- Dense storage (maximize cube utilization)
- High throughput put-away and retrieval
- Accurate inventory management
- Reduce travel time

**Types:**

**Unit-Load AS/RS:**
- Full pallet storage
- 40+ ft high
- 100-200 cycles/hour
- Cost: $2M-$10M+

**Mini-Load AS/RS:**
- Tote/carton storage
- 20-40 ft high
- 200-400 cycles/hour
- Cost: $1M-$5M

**Shuttle Systems:**
- High-density storage
- Scalable (add shuttles as needed)
- 400-800+ cycles/hour
- Cost: $2M-$8M

```python
def asrs_capacity_analysis(pallet_positions_needed, storage_height_ft,
                          throughput_pallets_per_hour, system_type='unit_load'):
    """
    Analyze AS/RS capacity and cost

    Parameters:
    - pallet_positions_needed: Total storage positions required
    - storage_height_ft: Available storage height
    - throughput_pallets_per_hour: Required throughput (in/out)
    - system_type: 'unit_load', 'mini_load', 'shuttle'

    Returns:
    - System configuration and cost
    """

    system_specs = {
        'unit_load': {
            'positions_per_aisle': 1000,  # Typical
            'cycles_per_hour': 150,
            'cost_per_aisle': 1_500_000,
            'height_min': 40,
            'footprint_per_aisle_sqft': 2000
        },
        'mini_load': {
            'positions_per_aisle': 1500,
            'cycles_per_hour': 300,
            'cost_per_aisle': 800_000,
            'height_min': 20,
            'footprint_per_aisle_sqft': 1500
        },
        'shuttle': {
            'positions_per_aisle': 2000,
            'cycles_per_hour': 600,
            'cost_per_shuttle': 200_000,
            'cost_base_structure': 2_000_000,
            'height_min': 20,
            'footprint_per_aisle_sqft': 1200
        }
    }

    spec = system_specs[system_type]

    # Check height requirement
    if storage_height_ft < spec['height_min']:
        return {
            'error': f"{system_type} requires minimum {spec['height_min']} ft clear height. "
                    f"Only {storage_height_ft} ft available."
        }

    # Calculate aisles needed (based on storage)
    aisles_needed_storage = np.ceil(pallet_positions_needed / spec['positions_per_aisle'])

    # Calculate aisles needed (based on throughput)
    if system_type == 'shuttle':
        # Shuttles can be added independently
        shuttles_needed = np.ceil(throughput_pallets_per_hour / spec['cycles_per_hour'])
        cost = spec['cost_base_structure'] + (shuttles_needed * spec['cost_per_shuttle'])
        aisles_needed_throughput = 1  # Flexible with shuttles
    else:
        # Cranes are per aisle
        aisles_needed_throughput = np.ceil(throughput_pallets_per_hour / spec['cycles_per_hour'])
        aisles_needed = max(aisles_needed_storage, aisles_needed_throughput)
        cost = aisles_needed * spec['cost_per_aisle']

    if system_type != 'shuttle':
        aisles_needed = max(aisles_needed_storage, aisles_needed_throughput)
    else:
        aisles_needed = aisles_needed_storage

    # Footprint
    total_footprint = aisles_needed * spec['footprint_per_aisle_sqft']

    # Capacity per aisle/shuttle
    if system_type == 'shuttle':
        total_positions = aisles_needed * spec['positions_per_aisle']
        total_throughput = shuttles_needed * spec['cycles_per_hour']
    else:
        total_positions = aisles_needed * spec['positions_per_aisle']
        total_throughput = aisles_needed * spec['cycles_per_hour']

    return {
        'system_type': system_type,
        'aisles_or_shuttles': int(aisles_needed if system_type != 'shuttle' else shuttles_needed),
        'total_positions': int(total_positions),
        'total_throughput_per_hour': int(total_throughput),
        'footprint_sqft': int(total_footprint),
        'total_cost': int(cost),
        'cost_per_position': round(cost / total_positions, 2),
        'utilization_%': round(min(
            pallet_positions_needed / total_positions,
            throughput_pallets_per_hour / total_throughput
        ) * 100, 1)
    }

# Example
asrs = asrs_capacity_analysis(
    pallet_positions_needed=5000,
    storage_height_ft=45,
    throughput_pallets_per_hour=300,
    system_type='unit_load'
)

print(f"System: {asrs['system_type']}")
print(f"Aisles needed: {asrs['aisles_or_shuttles']}")
print(f"Total positions: {asrs['total_positions']}")
print(f"Total cost: ${asrs['total_cost']:,.0f}")
print(f"Cost per position: ${asrs['cost_per_position']}")
```

### 3. Goods-to-Person (GTP) Systems

**Description:**
- Bring inventory to picker (vs. picker traveling)
- Dramatically reduces travel time
- High pick rates (200-400+ lines/hour/person)

**Types:**

**Vertical Lift Modules (VLM):**
- Vertical storage with elevator
- 30-50 ft high
- Good for small parts
- Cost: $150K-$300K per unit

**Horizontal Carousels:**
- Rotating shelves
- Picker waits, carousel rotates to item
- Cost: $80K-$150K per unit

**Vertical Carousels:**
- Similar to VLM but rotating
- Cost: $100K-$200K per unit

**Shuttle-Based GTP (AutoStore, Exotec, etc.):**
- Cube storage with robots retrieving bins
- Very high density
- Scalable
- Cost: $2M-$10M+

```python
def gtp_system_comparison(pick_lines_per_day, operating_hours=16,
                         warehouse_sqft=50000):
    """
    Compare goods-to-person system options

    Parameters:
    - pick_lines_per_day: Daily pick volume (lines)
    - operating_hours: Operating hours per day
    - warehouse_sqft: Available warehouse space

    Returns:
    - Comparison of GTP options
    """

    pick_lines_per_hour = pick_lines_per_day / operating_hours

    systems = {
        'Vertical Lift Module (VLM)': {
            'pick_rate_per_hour': 150,
            'cost_per_unit': 200_000,
            'footprint_per_unit_sqft': 150,
            'max_height_ft': 50,
            'scalability': 'Modular (add units)',
            'best_for': 'Small parts, medium volume'
        },
        'Horizontal Carousel': {
            'pick_rate_per_hour': 120,
            'cost_per_unit': 100_000,
            'footprint_per_unit_sqft': 300,
            'max_height_ft': 10,
            'scalability': 'Limited (fixed size)',
            'best_for': 'Small parts, lower volume'
        },
        'Shuttle GTP (AutoStore-like)': {
            'pick_rate_per_hour': 250,
            'cost_per_unit': 5_000_000,  # System cost
            'footprint_per_unit_sqft': 10000,  # System footprint
            'max_height_ft': 20,
            'scalability': 'Highly scalable (add robots)',
            'best_for': 'High volume, e-commerce'
        }
    }

    recommendations = []

    for system_name, specs in systems.items():
        # Calculate units needed
        if 'AutoStore' in system_name:
            # One system, calculate ports needed
            ports_needed = np.ceil(pick_lines_per_hour / specs['pick_rate_per_hour'])
            units_needed = 1
            total_cost = specs['cost_per_unit']
            footprint = specs['footprint_per_unit_sqft']
        else:
            units_needed = np.ceil(pick_lines_per_hour / specs['pick_rate_per_hour'])
            total_cost = units_needed * specs['cost_per_unit']
            footprint = units_needed * specs['footprint_per_unit_sqft']

        # Check if fits in warehouse
        fits = footprint < warehouse_sqft * 0.5  # Use max 50% of space

        recommendations.append({
            'system': system_name,
            'units_or_ports': int(units_needed if 'AutoStore' not in system_name else ports_needed),
            'total_cost': int(total_cost),
            'footprint_sqft': int(footprint),
            'fits_in_warehouse': fits,
            'pick_rate_total': int(units_needed * specs['pick_rate_per_hour']
                                  if 'AutoStore' not in system_name
                                  else ports_needed * specs['pick_rate_per_hour']),
            'best_for': specs['best_for']
        })

    return pd.DataFrame(recommendations)

# Example
gtp_comparison = gtp_system_comparison(
    pick_lines_per_day=20000,
    operating_hours=16,
    warehouse_sqft=50000
)

print("Goods-to-Person System Comparison:")
print(gtp_comparison)
```

### 4. Autonomous Mobile Robots (AMR) & AGVs

**AMRs (Autonomous Mobile Robots):**
- Navigate autonomously (no fixed paths)
- Flexible and scalable
- Examples: Locus Robotics, 6 River Systems, GreyOrange
- Cost: $30K-$50K per robot

**AGVs (Automated Guided Vehicles):**
- Follow fixed paths (wires, magnets, or tape)
- Less flexible but robust
- Cost: $50K-$150K per vehicle

**Use Cases:**
- Picking assistance (collaborative picking)
- Inventory transport (putaway, replenishment)
- Sortation and consolidation

```python
def amr_fleet_sizing(orders_per_day, lines_per_order=5, avg_travel_distance_ft=500,
                    robot_speed_ft_per_min=150, pick_time_per_line_sec=10,
                    operating_hours=16):
    """
    Calculate AMR fleet size requirements

    Parameters:
    - orders_per_day: Daily order volume
    - lines_per_order: Average lines per order
    - avg_travel_distance_ft: Average travel per order
    - robot_speed_ft_per_min: Robot travel speed
    - pick_time_per_line_sec: Time to pick each line
    - operating_hours: Operating hours per day

    Returns:
    - AMR fleet requirements and cost
    """

    # Calculate total picks
    picks_per_day = orders_per_day * lines_per_order
    picks_per_hour = picks_per_day / operating_hours

    # Time per order
    travel_time_min = avg_travel_distance_ft / robot_speed_ft_per_min
    pick_time_min = (lines_per_order * pick_time_per_sec) / 60
    total_time_per_order_min = travel_time_min + pick_time_min

    # Orders per robot per hour
    orders_per_robot_per_hour = 60 / total_time_per_order_min

    # Robots needed
    robots_needed_raw = (orders_per_day / operating_hours) / orders_per_robot_per_hour

    # Add buffer for charging, maintenance (20%)
    robots_needed = np.ceil(robots_needed_raw * 1.2)

    # Cost
    cost_per_robot = 40000  # Average AMR cost
    fleet_cost = robots_needed * cost_per_robot

    # Annual operating cost (maintenance, support)
    annual_operating_cost = fleet_cost * 0.15  # 15% of capital

    # Productivity improvement
    # Traditional picking: 100 lines/hour
    # AMR-assisted: 150 lines/hour (50% improvement)
    traditional_pickers = picks_per_day / (100 * operating_hours)
    amr_pickers = picks_per_day / (150 * operating_hours)
    labor_reduction = traditional_pickers - amr_pickers

    return {
        'picks_per_day': picks_per_day,
        'picks_per_hour': round(picks_per_hour, 0),
        'orders_per_robot_per_hour': round(orders_per_robot_per_hour, 1),
        'robots_needed': int(robots_needed),
        'fleet_cost': int(fleet_cost),
        'annual_operating_cost': int(annual_operating_cost),
        'traditional_pickers_needed': round(traditional_pickers, 1),
        'amr_assisted_pickers_needed': round(amr_pickers, 1),
        'labor_reduction': round(labor_reduction, 1),
        'labor_reduction_%': round((labor_reduction / traditional_pickers) * 100, 1)
    }

# Example
amr_fleet = amr_fleet_sizing(
    orders_per_day=2000,
    lines_per_order=5,
    avg_travel_distance_ft=500,
    operating_hours=16
)

print(f"AMRs needed: {amr_fleet['robots_needed']}")
print(f"Fleet cost: ${amr_fleet['fleet_cost']:,.0f}")
print(f"Labor reduction: {amr_fleet['labor_reduction']} pickers ({amr_fleet['labor_reduction_%']}%)")
```

### 5. Automated Picking Systems

**Robotic Piece Picking:**
- Robotic arms with grippers/suction
- Pick individual items
- Technology still maturing
- Examples: RightHand Robotics, Berkshire Grey
- Cost: $250K-$500K per cell

**Pick-to-Light:**
- Lights guide pickers
- Simple, effective
- Cost: $200-$500 per light position

**Voice Picking:**
- Hands-free, eyes-free
- Headset directs picker
- Cost: $2K-$3K per headset + software

```python
def picking_technology_comparison(pick_lines_per_day, accuracy_target=0.995):
    """
    Compare picking technology options

    Parameters:
    - pick_lines_per_day: Daily pick volume
    - accuracy_target: Target pick accuracy (e.g., 0.995 = 99.5%)

    Returns:
    - Technology comparison
    """

    technologies = {
        'Manual (Paper)': {
            'pick_rate': 80,
            'accuracy': 0.97,
            'cost_per_picker': 500,  # RF scanner only
            'training_time_hours': 8
        },
        'RF Scanning': {
            'pick_rate': 100,
            'accuracy': 0.99,
            'cost_per_picker': 3000,  # RF device
            'training_time_hours': 16
        },
        'Voice Picking': {
            'pick_rate': 120,
            'accuracy': 0.995,
            'cost_per_picker': 5000,  # Headset + software
            'training_time_hours': 24
        },
        'Pick-to-Light': {
            'pick_rate': 150,
            'accuracy': 0.998,
            'cost_per_picker': 25000,  # Light systems
            'training_time_hours': 8
        },
        'AMR-Assisted': {
            'pick_rate': 150,
            'accuracy': 0.998,
            'cost_per_picker': 40000,  # Robot amortized
            'training_time_hours': 16
        },
        'Robotic Picking': {
            'pick_rate': 200,
            'accuracy': 0.999,
            'cost_per_picker': 300000,  # Robotic cell
            'training_time_hours': 40
        }
    }

    comparison = []

    for tech_name, specs in technologies.items():
        pickers_needed = np.ceil(pick_lines_per_day / (specs['pick_rate'] * 8))  # 8 hr shifts
        total_cost = pickers_needed * specs['cost_per_picker']
        meets_accuracy = specs['accuracy'] >= accuracy_target

        comparison.append({
            'technology': tech_name,
            'pick_rate': specs['pick_rate'],
            'accuracy_%': specs['accuracy'] * 100,
            'pickers_needed': int(pickers_needed),
            'total_cost': int(total_cost),
            'meets_accuracy_target': meets_accuracy,
            'training_hours': specs['training_time_hours']
        })

    return pd.DataFrame(comparison)

# Example
picking_comparison = picking_technology_comparison(
    pick_lines_per_day=10000,
    accuracy_target=0.995
)

print("Picking Technology Comparison:")
print(picking_comparison)
```

---

## Automation ROI Analysis

### ROI Calculation Framework

```python
def automation_roi_analysis(capital_cost, current_labor_cost_annual,
                           labor_reduction_pct, productivity_improvement_pct=0,
                           accuracy_improvement_savings=0,
                           maintenance_cost_pct=0.15,
                           useful_life_years=7, discount_rate=0.10):
    """
    Calculate comprehensive ROI for warehouse automation

    Parameters:
    - capital_cost: Upfront automation investment
    - current_labor_cost_annual: Current annual labor cost
    - labor_reduction_pct: Labor reduction (0.40 = 40%)
    - productivity_improvement_pct: Throughput increase for same labor
    - accuracy_improvement_savings: Annual savings from improved accuracy
    - maintenance_cost_pct: Annual maintenance as % of capital
    - useful_life_years: Expected system life
    - discount_rate: Discount rate for NPV

    Returns:
    - ROI metrics
    """

    # Annual benefits
    labor_savings = current_labor_cost_annual * labor_reduction_pct
    productivity_savings = current_labor_cost_annual * productivity_improvement_pct / (1 + productivity_improvement_pct)
    accuracy_savings = accuracy_improvement_savings

    total_annual_savings = labor_savings + productivity_savings + accuracy_savings

    # Annual costs
    maintenance_cost = capital_cost * maintenance_cost_pct
    annual_net_savings = total_annual_savings - maintenance_cost

    # Simple payback
    simple_payback_years = capital_cost / annual_net_savings if annual_net_savings > 0 else 999

    # NPV calculation
    npv = -capital_cost
    for year in range(1, useful_life_years + 1):
        npv += annual_net_savings / ((1 + discount_rate) ** year)

    # IRR approximation (simplified)
    roi_total = (annual_net_savings * useful_life_years - capital_cost) / capital_cost

    return {
        'capital_cost': capital_cost,
        'annual_labor_savings': round(labor_savings, 0),
        'annual_productivity_savings': round(productivity_savings, 0),
        'annual_accuracy_savings': round(accuracy_savings, 0),
        'total_annual_savings': round(total_annual_savings, 0),
        'annual_maintenance': round(maintenance_cost, 0),
        'annual_net_savings': round(annual_net_savings, 0),
        'simple_payback_years': round(simple_payback_years, 2),
        'npv': round(npv, 0),
        'roi_%_over_life': round(roi_total * 100, 1)
    }

# Example
roi = automation_roi_analysis(
    capital_cost=3_000_000,
    current_labor_cost_annual=2_500_000,
    labor_reduction_pct=0.40,
    productivity_improvement_pct=0.20,
    accuracy_improvement_savings=200_000,
    maintenance_cost_pct=0.15,
    useful_life_years=7
)

print("Automation ROI Analysis:")
for metric, value in roi.items():
    if isinstance(value, (int, float)) and value > 1000:
        print(f"  {metric}: ${value:,.0f}")
    else:
        print(f"  {metric}: {value}")
```

### Break-Even Analysis

```python
def automation_breakeven_analysis(capital_cost, annual_net_savings,
                                 labor_cost_inflation=0.03):
    """
    Calculate break-even timeline considering labor inflation

    Parameters:
    - capital_cost: Automation investment
    - annual_net_savings: First year net savings
    - labor_cost_inflation: Annual labor cost increase (3%)

    Returns:
    - Year-by-year break-even analysis
    """

    cumulative_savings = 0
    year = 0

    breakeven_table = []

    while cumulative_savings < capital_cost and year < 15:
        year += 1

        # Savings increase with labor inflation
        year_savings = annual_net_savings * ((1 + labor_cost_inflation) ** (year - 1))
        cumulative_savings += year_savings

        breakeven_table.append({
            'year': year,
            'annual_savings': round(year_savings, 0),
            'cumulative_savings': round(cumulative_savings, 0),
            'remaining_to_breakeven': round(max(0, capital_cost - cumulative_savings), 0),
            'roi_%': round((cumulative_savings / capital_cost - 1) * 100, 1)
        })

        if cumulative_savings >= capital_cost:
            break

    return pd.DataFrame(breakeven_table)

# Example
breakeven = automation_breakeven_analysis(
    capital_cost=3_000_000,
    annual_net_savings=700_000,
    labor_cost_inflation=0.03
)

print("\nBreak-Even Analysis:")
print(breakeven)
```

---

## Automation Selection Framework

### Decision Matrix

```python
def automation_selection_decision(volume_level, sku_count, order_profile,
                                 labor_availability, capital_budget):
    """
    Recommend automation technologies based on operational profile

    Parameters:
    - volume_level: 'low' (<1K orders/day), 'medium' (1K-5K), 'high' (>5K)
    - sku_count: 'low' (<1K), 'medium' (1K-10K), 'high' (>10K)
    - order_profile: 'pallet', 'case', 'each', 'mixed'
    - labor_availability: 'abundant', 'moderate', 'scarce'
    - capital_budget: 'low' (<$500K), 'medium' ($500K-$3M), 'high' (>$3M)

    Returns:
    - Recommended automation technologies
    """

    recommendations = []

    # High volume + capital = full automation
    if volume_level == 'high' and capital_budget == 'high':
        recommendations.append({
            'technology': 'Shuttle-based GTP (AutoStore, Exotec)',
            'priority': 1,
            'reason': 'High volume justifies high automation, excellent ROI',
            'est_cost': '$5M-$15M'
        })
        recommendations.append({
            'technology': 'Cross-Belt Sorter',
            'priority': 2,
            'reason': 'High throughput sortation needed',
            'est_cost': '$3M-$8M'
        })

    # Medium volume, e-commerce profile
    elif volume_level == 'medium' and order_profile == 'each':
        recommendations.append({
            'technology': 'AMR Fleet + Pick-to-Light',
            'priority': 1,
            'reason': 'Scalable, flexible for e-commerce picking',
            'est_cost': '$500K-$2M'
        })
        recommendations.append({
            'technology': 'Vertical Lift Modules (VLM)',
            'priority': 2,
            'reason': 'Goods-to-person for fast movers',
            'est_cost': '$400K-$1M'
        })

    # Pallet-focused operations
    elif order_profile == 'pallet':
        recommendations.append({
            'technology': 'AS/RS Unit-Load',
            'priority': 1,
            'reason': 'Dense pallet storage, high throughput',
            'est_cost': '$2M-$8M'
        })
        recommendations.append({
            'technology': 'AGV Pallet Movers',
            'priority': 2,
            'reason': 'Automate pallet transport',
            'est_cost': '$500K-$1.5M'
        })

    # Labor scarcity driver
    elif labor_availability == 'scarce':
        recommendations.append({
            'technology': 'AMR Fleet',
            'priority': 1,
            'reason': 'Reduce labor dependency, scalable',
            'est_cost': '$300K-$1M'
        })
        recommendations.append({
            'technology': 'Voice Picking',
            'priority': 2,
            'reason': 'Improve productivity of available labor',
            'est_cost': '$50K-$200K'
        })

    # Low budget
    elif capital_budget == 'low':
        recommendations.append({
            'technology': 'WMS + RF Scanning',
            'priority': 1,
            'reason': 'Foundation for efficiency, low cost',
            'est_cost': '$100K-$300K'
        })
        recommendations.append({
            'technology': 'Conveyor System (Basic)',
            'priority': 2,
            'reason': 'Improve flow at modest cost',
            'est_cost': '$100K-$500K'
        })

    else:
        # Default recommendations
        recommendations.append({
            'technology': 'Start with WMS + RF Scanning',
            'priority': 1,
            'reason': 'Build foundation before advanced automation',
            'est_cost': '$100K-$300K'
        })

    return pd.DataFrame(recommendations)

# Example
automation_recs = automation_selection_decision(
    volume_level='medium',
    sku_count='high',
    order_profile='each',
    labor_availability='scarce',
    capital_budget='medium'
)

print("Automation Recommendations:")
print(automation_recs)
```

---

## Implementation Best Practices

### Phased Implementation Approach

**Phase 1: Foundation (Months 1-6)**
- Implement/upgrade WMS
- RF scanning and barcode infrastructure
- Process optimization (slotting, wave planning)
- Data clean-up and validation

**Phase 2: Targeted Automation (Months 7-12)**
- Automate specific pain points
- Pilot technologies (small scale)
- Measure results and refine
- Build internal expertise

**Phase 3: Scale (Year 2)**
- Expand successful pilots
- Add capacity as volume grows
- Integration and optimization
- Advanced features

**Phase 4: Continuous Improvement (Ongoing)**
- Monitor performance
- Upgrade and enhance
- New technologies
- Process refinement

### Critical Success Factors

1. **Start with Good Processes**: Automate good processes, not bad ones
2. **Strong Project Management**: Complex integrations, long timelines
3. **Change Management**: Train staff, manage resistance
4. **Vendor Selection**: Proven technology, strong support
5. **Integration**: WMS, ERP, warehouse systems
6. **Testing**: Thorough UAT before go-live
7. **Scalability**: Plan for growth
8. **Flexibility**: Accommodate changing business needs

---

## Common Challenges & Solutions

### Challenge: High Capital Cost

**Problem:**
- $2M-$10M+ investment
- Long payback periods
- Risk of technology obsolescence

**Solutions:**
- Phase approach (start small, prove ROI)
- Consider leasing vs. buying
- Focus on high-ROI areas first
- Robotics-as-a-Service (RaaS) models
- 3PL partnership (let them automate)

### Challenge: Integration Complexity

**Problem:**
- Multiple systems to integrate (WMS, ERP, automation)
- Custom interfaces and middleware
- Testing and validation time-consuming

**Solutions:**
- Choose automation compatible with WMS
- Experienced systems integrator
- Phased cutover (not big bang)
- Extensive testing environment
- Buffer time in project plan

### Challenge: Labor Displacement

**Problem:**
- Workers fear job loss
- Resistance to change
- Union concerns

**Solutions:**
- Communicate vision (augment, not replace)
- Retrain workers for new roles (maintenance, monitoring)
- Natural attrition and redeployment
- Emphasize safety and ergonomic benefits
- Involve workers in design process

### Challenge: Throughput Not Meeting Expectations

**Problem:**
- System runs slower than promised
- Downtime higher than expected
- Process bottlenecks

**Solutions:**
- Realistic vendor expectations (contractual SLAs)
- Pilot/proof-of-concept before full rollout
- Proper preventive maintenance
- Redundancy in design (extra capacity)
- Continuous optimization (tuning)

### Challenge: Changing Business Requirements

**Problem:**
- Automation designed for today's needs
- Business changes (SKUs, volume, channels)
- Inflexible systems

**Solutions:**
- Design for flexibility (modular, scalable)
- AMRs vs. fixed automation (more flexible)
- Overcapacity buffer (30-50%)
- Regular technology refresh cycles
- Cloud-based systems (easier to update)

---

## Emerging Technologies

### Innovations to Watch

**1. AI-Powered Robotics**
- Machine learning for picking (handle any item)
- Vision systems for bin picking
- Adaptive grasping

**2. Collaborative Robots (Cobots)**
- Work alongside humans safely
- Flexible deployment
- Lower cost than full automation

**3. Drones**
- Inventory scanning and cycle counting
- Read barcodes at height
- Autonomous flight

**4. Exoskeletons**
- Wearable assistance for workers
- Reduce fatigue and injury
- Augment human capability

**5. Digital Twins**
- Virtual warehouse simulation
- Test automation before building
- Ongoing optimization

**6. 5G Connectivity**
- Enable more real-time automation
- Support dense robot fleets
- IoT sensor networks

---

## Tools & Software

### Warehouse Control Systems (WCS)

**Purpose:**
- Orchestrate automation equipment
- Interface between WMS and automation
- Real-time control and optimization

**Major Vendors:**
- Dematic
- Honeywell Intelligrated
- Vanderlande
- TGW Logistics
- Swisslog

### Simulation Software

**Purpose:**
- Model warehouse operations
- Test automation scenarios
- Optimize layouts and throughput

**Tools:**
- FlexSim
- AnyLogic
- Simio
- Arena
- AutoMod

---

## Output Format

### Automation Feasibility Study

**Executive Summary:**
- Automation recommendation
- Expected ROI and payback
- Capital investment required
- Implementation timeline

**Current State Analysis:**

| Metric | Current | Pain Points |
|--------|---------|-------------|
| Orders/Day | 3,000 | Peaks to 8,000, can't scale |
| Labor Cost/Year | $3.5M | High turnover, tight market |
| Pick Rate | 85 lines/hr | Low productivity |
| Order Accuracy | 97.5% | Below target 99% |
| Space Utilization | 65% | Poor cube utilization |

**Recommended Automation:**

| Technology | Purpose | Capacity | Cost | ROI |
|-----------|---------|----------|------|-----|
| AMR Fleet (20 robots) | Picking assistance | +40% productivity | $800K | 2.1 yrs |
| Shuttle GTP System | Dense storage, GTP | 5K positions | $4M | 3.5 yrs |
| Sliding Shoe Sorter | Order sortation | 10K units/hr | $2M | 2.8 yrs |
| **Total** | - | - | **$6.8M** | **3.1 yrs** |

**Financial Analysis:**

| Metric | Value |
|--------|-------|
| Total Capital Investment | $6.8M |
| Annual Labor Savings | $1.4M (40% reduction) |
| Annual Productivity Gain | $500K (50% more throughput) |
| Annual Accuracy Savings | $150K (reduced errors) |
| Annual Net Savings | $1.65M (after $400K maintenance) |
| Simple Payback | 4.1 years |
| 7-Year NPV (10% discount) | $2.1M |
| ROI (7 years) | 75% |

**Implementation Plan:**
- **Months 1-3**: Design, engineering, vendor selection
- **Months 4-9**: Equipment fabrication and delivery
- **Months 10-12**: Installation and integration
- **Months 13-14**: Testing and training
- **Month 15**: Go-live
- **Months 16-18**: Ramp-up and optimization

**Risk Mitigation:**
- Pilot AMRs before full fleet purchase
- Phased cutover (one zone at a time)
- Maintain manual backup processes
- Extensive training program
- Vendor support and SLAs

---

## Questions to Ask

If you need more context:
1. What's driving the automation interest? (labor, capacity, accuracy, cost)
2. What's the order volume and profile? (current and projected)
3. What's the current labor situation? (cost, availability, turnover)
4. What's the capital budget and ROI expectations?
5. What's the facility situation? (size, height, constraints)
6. What technology is currently in place? (WMS, conveyors, equipment)
7. What's the timeline for implementation?
8. Are there any specific pain points or bottlenecks to address?

---

## Related Skills

- **warehouse-design**: Design warehouse layout for automation
- **order-fulfillment**: Fulfillment operations and processes
- **picker-routing-optimization**: Optimize pick paths (pre-automation)
- **warehouse-slotting-optimization**: Product placement optimization
- **process-optimization**: Improve processes before automating
- **supply-chain-analytics**: ROI analysis and performance metrics
- **computer-vision-warehouse**: Vision-based automation systems
