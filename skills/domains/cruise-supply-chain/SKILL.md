---
name: cruise-supply-chain
description: When the user wants to optimize cruise ship supply chains, manage ship provisioning, or improve maritime operations. Also use when the user mentions "cruise logistics," "ship provisioning," "maritime supply chain," "port operations," "cruise inventory," "galley management," "ship chandling," or "cruise procurement." For hotel operations, see hotel-inventory-management. For hospitality procurement, see hospitality-procurement.
---

# Cruise Supply Chain

You are an expert in cruise ship supply chain management and maritime logistics. Your goal is to help optimize the complex provisioning, inventory management, and logistics for cruise vessels, ensuring passenger satisfaction while managing costs, storage constraints, and port operations.

## Initial Assessment

Before optimizing cruise supply chain, understand:

1. **Vessel & Fleet Profile**
   - Fleet size and vessel types?
   - Passenger capacity and crew size?
   - Storage capacity (dry, cold, frozen)?
   - Galley and food service capabilities?

2. **Itinerary & Operations**
   - Route structure? (Caribbean, Mediterranean, Alaska, world cruise)
   - Port rotation and frequency?
   - Days at sea vs. in port?
   - Seasonal variations?

3. **Current Supply Chain**
   - Provisioning frequency and locations?
   - Supplier network? (global, regional)
   - Inventory management system?
   - Cold chain capabilities?

4. **Objectives & Challenges**
   - Primary goals? (cost, quality, waste reduction)
   - Current pain points? (stockouts, waste, costs)
   - Sustainability targets?
   - Guest satisfaction metrics?

---

## Cruise Supply Chain Framework

### Supply Chain Components

**Food & Beverage:**
- Fresh produce (fruits, vegetables)
- Proteins (beef, poultry, seafood)
- Dairy products
- Dry goods and pantry items
- Beverages (alcoholic and non-alcoholic)
- Specialty items and ingredients

**Hotel Operations:**
- Linens and towels
- Guest amenities (toiletries, etc.)
- Cleaning supplies
- Cabin supplies

**Technical & Maintenance:**
- Spare parts
- Fuel and lubricants
- Technical supplies
- Safety equipment

**Entertainment & Recreation:**
- Shore excursion supplies
- Entertainment equipment
- Retail merchandise

---

## Provisioning Planning & Optimization

### Multi-Port Provisioning Strategy

```python
import numpy as np
import pandas as pd
from pulp import *

class CruiseProvisioningOptimizer:
    """
    Optimize cruise ship provisioning across multiple ports

    Balance costs, storage capacity, and quality
    """

    def __init__(self, vessel_capacity, itinerary):
        self.vessel_capacity = vessel_capacity  # storage capacity by type
        self.itinerary = itinerary  # list of port calls

    def optimize_provisioning_schedule(self, item_requirements, port_costs,
                                      port_availability):
        """
        Determine what to purchase at each port to minimize total cost

        Parameters:
        - item_requirements: dict of {item: daily_consumption}
        - port_costs: dict of {(port, item): cost_per_unit}
        - port_availability: dict of {(port, item): available_quantity}
        """

        prob = LpProblem("Cruise_Provisioning", LpMinimize)

        items = list(item_requirements.keys())
        ports = [port['name'] for port in self.itinerary]

        # Variables: quantity of item i purchased at port p
        purchase = {}

        for port in ports:
            for item in items:
                if (port, item) in port_costs:
                    purchase[port, item] = LpVariable(
                        f"Purchase_{port}_{item}",
                        lowBound=0
                    )

        # Objective: minimize total procurement cost
        total_cost = lpSum([purchase[port, item] * port_costs.get((port, item), 999999)
                           for port in ports
                           for item in items
                           if (port, item) in purchase])

        prob += total_cost

        # Constraints

        # Meet demand for full voyage
        voyage_days = sum([port['days_until_next'] for port in self.itinerary])

        for item in items:
            total_required = item_requirements[item] * voyage_days

            total_purchased = lpSum([purchase.get((port, item), 0)
                                    for port in ports])

            prob += total_purchased >= total_required

        # Storage capacity constraints at each port
        for p, port in enumerate(self.itinerary):
            # Remaining voyage days from this port
            remaining_days = sum([self.itinerary[i]['days_until_next']
                                 for i in range(p, len(self.itinerary))])

            # Storage at this port = purchases at this port + previous inventory
            # (Simplified model - actual would track consumption)

            for storage_type in ['dry', 'cold', 'frozen']:
                items_this_type = [i for i in items
                                  if item_requirements[i].get('storage_type') == storage_type]

                # Total storage used
                storage_used = lpSum([purchase.get((port['name'], item), 0) *
                                    item_requirements[item].get('volume_per_unit', 1)
                                    for item in items_this_type])

                prob += storage_used <= self.vessel_capacity[storage_type]

        # Port availability limits
        for port in ports:
            for item in items:
                if (port, item) in port_availability:
                    if (port, item) in purchase:
                        prob += purchase[port, item] <= port_availability[port, item]

        # Solve
        prob.solve(PULP_CBC_CMD(msg=0))

        # Extract provisioning schedule
        schedule = []

        for port in ports:
            port_orders = []
            port_cost = 0

            for item in items:
                if (port, item) in purchase and purchase[port, item].varValue > 0.1:
                    quantity = purchase[port, item].varValue
                    cost = quantity * port_costs.get((port, item), 0)

                    port_orders.append({
                        'item': item,
                        'quantity': quantity,
                        'unit_cost': port_costs.get((port, item), 0),
                        'total_cost': cost
                    })

                    port_cost += cost

            if port_orders:
                schedule.append({
                    'port': port,
                    'orders': port_orders,
                    'total_port_cost': port_cost
                })

        return {
            'status': LpStatus[prob.status],
            'total_cost': value(prob.objective),
            'provisioning_schedule': schedule
        }

    def calculate_food_requirements(self, passenger_count, crew_count,
                                   voyage_days, menu_plan):
        """
        Calculate food and beverage requirements based on passenger load
        and menu planning
        """

        requirements = {}

        # Per-person-per-day consumption rates
        consumption_rates = {
            'beef': 0.25,  # kg
            'chicken': 0.20,
            'seafood': 0.15,
            'vegetables': 0.30,
            'fruits': 0.25,
            'dairy_milk': 0.15,  # liters
            'bread': 0.15,  # kg
            'wine': 0.10,  # liters
            'beer': 0.20,  # liters
            'soft_drinks': 0.30  # liters
        }

        total_pax = passenger_count + crew_count

        for item, rate_per_day in consumption_rates.items():
            daily_consumption = rate_per_day * total_pax

            # Add safety factor
            safety_factor = 1.15

            requirements[item] = {
                'daily_consumption': daily_consumption * safety_factor,
                'total_voyage': daily_consumption * safety_factor * voyage_days
            }

        return requirements

# Example usage
vessel_capacity = {
    'dry': 500,  # cubic meters
    'cold': 300,
    'frozen': 200
}

itinerary = [
    {'name': 'Miami', 'days_until_next': 3},
    {'name': 'Cozumel', 'days_until_next': 2},
    {'name': 'Grand Cayman', 'days_until_next': 2},
    {'name': 'Miami', 'days_until_next': 0}
]

optimizer = CruiseProvisioningOptimizer(vessel_capacity, itinerary)

item_requirements = {
    'beef': {'daily_consumption': 500, 'storage_type': 'frozen', 'volume_per_unit': 0.001},
    'chicken': {'daily_consumption': 400, 'storage_type': 'frozen', 'volume_per_unit': 0.001},
    'vegetables': {'daily_consumption': 600, 'storage_type': 'cold', 'volume_per_unit': 0.0015},
    'wine': {'daily_consumption': 200, 'storage_type': 'dry', 'volume_per_unit': 0.001},
}

port_costs = {
    ('Miami', 'beef'): 12.00,
    ('Miami', 'chicken'): 6.00,
    ('Miami', 'vegetables'): 3.00,
    ('Miami', 'wine'): 8.00,
    ('Cozumel', 'beef'): 14.00,
    ('Cozumel', 'vegetables'): 2.50,
    ('Grand Cayman', 'beef'): 15.00,
}

port_availability = {
    ('Miami', 'beef'): 10000,
    ('Miami', 'chicken'): 10000,
    ('Miami', 'vegetables'): 10000,
    ('Miami', 'wine'): 5000,
    ('Cozumel', 'beef'): 2000,
    ('Cozumel', 'vegetables'): 3000,
}

result = optimizer.optimize_provisioning_schedule(item_requirements,
                                                 port_costs,
                                                 port_availability)

print(f"Total provisioning cost: ${result['total_cost']:,.2f}")
```

---

## Inventory Management for Cruise Ships

### Par Stock Level Optimization

```python
def calculate_par_levels(item, consumption_rate, lead_time_days,
                        service_level=0.95, storage_cost_per_unit=1.0):
    """
    Calculate optimal par stock levels for cruise ship inventory

    Parameters:
    - item: item details
    - consumption_rate: average daily consumption
    - lead_time_days: days between ports (resupply time)
    - service_level: target service level (stockout probability)
    - storage_cost_per_unit: cost to hold inventory
    """
    from scipy.stats import norm

    # Demand during lead time
    avg_demand = consumption_rate * lead_time_days

    # Variability (assume coefficient of variation)
    cv = 0.20  # 20% variability
    std_demand = avg_demand * cv

    # Safety stock
    z_score = norm.ppf(service_level)
    safety_stock = z_score * std_demand

    # Reorder point (par level)
    par_level = avg_demand + safety_stock

    # Maximum stock level (par level + one order quantity)
    max_level = par_level * 1.5

    return {
        'par_level': par_level,
        'max_level': max_level,
        'safety_stock': safety_stock,
        'avg_inventory': (par_level + max_level) / 2,
        'holding_cost': ((par_level + max_level) / 2) * storage_cost_per_unit
    }

# Example
beef_par = calculate_par_levels(
    item='beef',
    consumption_rate=500,  # kg/day
    lead_time_days=7,  # 1 week between ports
    service_level=0.98  # High service level for critical item
)

print(f"Beef par level: {beef_par['par_level']:.0f} kg")
print(f"Safety stock: {beef_par['safety_stock']:.0f} kg")
```

---

## Waste Reduction & Sustainability

### Food Waste Optimization

```python
class CruiseFoodWasteOptimizer:
    """
    Optimize food ordering and preparation to minimize waste
    """

    def __init__(self, historical_consumption):
        self.historical_consumption = historical_consumption

    def predict_actual_consumption(self, planned_menu, passenger_count,
                                  day_of_cruise):
        """
        Predict actual consumption to reduce overproduction

        Factors:
        - Port days vs. sea days (different consumption patterns)
        - Day of cruise (higher consumption early in cruise)
        - Menu popularity
        - Passenger demographics
        """
        from sklearn.ensemble import RandomForestRegressor

        # Features for prediction
        features = {
            'passenger_count': passenger_count,
            'day_of_cruise': day_of_cruise,
            'is_sea_day': 1 if planned_menu['is_sea_day'] else 0,
            'menu_popularity_score': planned_menu.get('popularity', 0.7)
        }

        # Simple model (would be trained on historical data)
        # Predicted consumption factor vs. standard portion
        consumption_factor = 0.85  # Typically 85% of planned is consumed

        predicted_consumption = {}

        for item, planned_quantity in planned_menu['items'].items():
            # Adjust based on patterns
            if features['is_sea_day']:
                adjustment = 1.1  # Higher consumption on sea days
            else:
                adjustment = 0.9  # Lower on port days

            predicted = planned_quantity * consumption_factor * adjustment

            predicted_consumption[item] = {
                'planned': planned_quantity,
                'predicted_actual': predicted,
                'recommended_prep': predicted * 1.05  # Small buffer
            }

        return predicted_consumption

    def optimize_buffet_replenishment(self, current_inventory, consumption_rate,
                                     time_remaining_hours):
        """
        Optimize buffet replenishment to minimize waste at end of service
        """

        # Calculate expected consumption in remaining time
        expected_consumption = consumption_rate * time_remaining_hours

        # Replenishment decision
        if current_inventory < expected_consumption * 0.5:
            # Replenish
            replenish_quantity = expected_consumption - current_inventory

            # Don't overproduce near end of service
            if time_remaining_hours < 1:
                replenish_quantity *= 0.7  # Conservative

            return {
                'action': 'replenish',
                'quantity': replenish_quantity,
                'reason': 'Current inventory below threshold'
            }
        else:
            return {
                'action': 'hold',
                'quantity': 0,
                'reason': 'Sufficient inventory for remaining service'
            }

    def donation_optimization(self, excess_inventory, port_donations):
        """
        Optimize food donation to reduce waste and support communities

        Match excess inventory with port-based donation opportunities
        """

        donation_plan = []

        for item, quantity in excess_inventory.items():
            if quantity > 0:
                # Find suitable donation partners
                eligible_partners = [
                    p for p in port_donations
                    if item in p['accepted_items']
                ]

                if eligible_partners:
                    # Allocate to highest-impact partner
                    best_partner = max(eligible_partners,
                                      key=lambda x: x['impact_score'])

                    donation_plan.append({
                        'item': item,
                        'quantity': quantity,
                        'partner': best_partner['name'],
                        'estimated_impact': quantity * best_partner['meals_per_kg']
                    })

        return donation_plan
```

---

## Cold Chain Management

### Temperature-Controlled Inventory

```python
def optimize_cold_chain_storage(items, storage_zones, temperature_requirements):
    """
    Optimize placement of items in cold storage zones

    Parameters:
    - items: list of items with temp requirements
    - storage_zones: available cold storage with temp ranges
    - temperature_requirements: optimal temps for each item
    """
    from pulp import *

    prob = LpProblem("Cold_Storage", LpMinimize)

    # Variables: assign item i to zone z
    x = {}

    for i, item in enumerate(items):
        for z, zone in enumerate(storage_zones):
            # Check if zone can handle item's temp requirement
            if (zone['temp_min'] <= temperature_requirements[item['name']]['optimal'] <= zone['temp_max']):
                x[i, z] = LpVariable(f"Assign_{i}_{z}", cat='Binary')

    # Objective: minimize energy cost (colder zones cost more)
    energy_cost = lpSum([x[i, z] * storage_zones[z]['energy_cost_per_unit'] *
                        items[i]['volume']
                        for (i, z) in x])

    prob += energy_cost

    # Constraints

    # Each item assigned to exactly one zone
    for i in range(len(items)):
        zones_for_item = [x[i, z] for z in range(len(storage_zones))
                         if (i, z) in x]
        if zones_for_item:
            prob += lpSum(zones_for_item) == 1

    # Zone capacity
    for z, zone in enumerate(storage_zones):
        zone_volume = lpSum([items[i]['volume'] * x[i, z]
                            for i in range(len(items))
                            if (i, z) in x])

        prob += zone_volume <= zone['capacity']

    # Solve
    prob.solve(PULP_CBC_CMD(msg=0))

    # Extract assignments
    assignments = []

    for (i, z) in x:
        if x[i, z].varValue > 0.5:
            assignments.append({
                'item': items[i]['name'],
                'zone': storage_zones[z]['name'],
                'temperature': storage_zones[z]['temp_min'],
                'volume': items[i]['volume']
            })

    return {
        'total_energy_cost': value(prob.objective),
        'assignments': pd.DataFrame(assignments)
    }

# Example
items = [
    {'name': 'Ice Cream', 'volume': 50},
    {'name': 'Frozen Fish', 'volume': 100},
    {'name': 'Fresh Vegetables', 'volume': 150},
    {'name': 'Dairy Products', 'volume': 80},
]

storage_zones = [
    {'name': 'Deep Freeze', 'temp_min': -25, 'temp_max': -18,
     'capacity': 200, 'energy_cost_per_unit': 3.0},
    {'name': 'Freezer', 'temp_min': -18, 'temp_max': -12,
     'capacity': 250, 'energy_cost_per_unit': 2.0},
    {'name': 'Cold Storage', 'temp_min': 0, 'temp_max': 4,
     'capacity': 300, 'energy_cost_per_unit': 1.0},
]

temperature_requirements = {
    'Ice Cream': {'optimal': -20},
    'Frozen Fish': {'optimal': -15},
    'Fresh Vegetables': {'optimal': 2},
    'Dairy Products': {'optimal': 3},
}

result = optimize_cold_chain_storage(items, storage_zones, temperature_requirements)
```

---

## Port Logistics & Operations

### Shore-Side Coordination

```python
def optimize_port_loading_schedule(deliveries, loading_bays, port_time_window):
    """
    Optimize scheduling of supplier deliveries during port call

    Constraints:
    - Limited port time (6-10 hours typically)
    - Limited loading bays
    - Crew availability
    - Customs clearance
    """
    from pulp import *

    prob = LpProblem("Port_Loading", LpMinimize)

    n_deliveries = len(deliveries)
    n_bays = loading_bays
    time_slots = range(port_time_window)  # hours

    # Variables: assign delivery d to bay b in time slot t
    x = {}

    for d in range(n_deliveries):
        for b in range(n_bays):
            for t in time_slots:
                x[d, b, t] = LpVariable(f"Assign_{d}_{b}_{t}", cat='Binary')

    # Objective: minimize total makespan + priority penalties
    makespan = LpVariable("Makespan", lowBound=0)

    # Completion time of last delivery
    prob += makespan

    # Each delivery assigned once
    for d in range(n_deliveries):
        prob += lpSum([x[d, b, t]
                      for b in range(n_bays)
                      for t in time_slots]) == 1

    # Bay can handle one delivery at a time
    for b in range(n_bays):
        for t in time_slots:
            prob += lpSum([x[d, b, t] for d in range(n_deliveries)]) <= 1

    # Makespan constraint
    for d, delivery in enumerate(deliveries):
        for b in range(n_bays):
            for t in time_slots:
                # If delivery starts at time t, it completes at t + duration
                prob += makespan >= (t + delivery['duration_hours']) * x[d, b, t]

    # Priority deliveries (perishables) should be early
    for d, delivery in enumerate(deliveries):
        if delivery.get('priority') == 'high':
            for b in range(n_bays):
                for t in time_slots:
                    if t > port_time_window // 2:
                        # Penalize late loading of priority items
                        prob += x[d, b, t] == 0

    # Solve
    prob.solve(PULP_CBC_CMD(msg=0))

    # Extract schedule
    schedule = []

    for d in range(n_deliveries):
        for b in range(n_bays):
            for t in time_slots:
                if x[d, b, t].varValue > 0.5:
                    schedule.append({
                        'delivery': deliveries[d]['supplier'],
                        'items': deliveries[d]['items'],
                        'bay': b + 1,
                        'start_time': t,
                        'duration': deliveries[d]['duration_hours'],
                        'priority': deliveries[d].get('priority', 'normal')
                    })

    return {
        'makespan': makespan.varValue,
        'schedule': pd.DataFrame(schedule).sort_values('start_time')
    }
```

---

## Tools & Libraries

### Python Libraries

**Optimization:**
- `PuLP`: Linear programming
- `scipy.optimize`: General optimization
- `OR-Tools`: Google optimization

**Forecasting:**
- `scikit-learn`: Machine learning
- `prophet`: Time series forecasting

**Data Analysis:**
- `pandas`, `numpy`: Data manipulation
- `matplotlib`: Visualization

### Commercial Software

**Cruise Operations:**
- **ShipServ**: Maritime procurement platform
- **MarineCFO**: Cruise financial management
- **Adonis**: Hospitality management system
- **ORIS**: Ship operations and reporting

**Inventory Management:**
- **Visual Computers**: Cruise inventory system
- **Compeat**: Restaurant and hospitality inventory
- **MarketMan**: Food service inventory

**Provisioning:**
- **Navtor**: Maritime voyage planning
- **Martek Marine**: Ship management software
- **Danaos**: Ship management system

**Sustainability:**
- **Cleantech**: Environmental compliance
- **OCEANOS**: Environmental monitoring

---

## Common Challenges & Solutions

### Challenge: Port Time Constraints

**Problem:**
- Limited time in port (4-10 hours)
- Multiple suppliers and deliveries
- Customs and inspection delays

**Solutions:**
- Pre-planning and coordination
- Consolidated deliveries from aggregators
- Bonded warehouse arrangements
- Parallel loading operations
- Pre-cleared suppliers

### Challenge: Storage Limitations

**Problem:**
- Limited cold storage capacity
- Space competition among departments
- Seasonal demand variations

**Solutions:**
- Par level optimization
- Just-in-time provisioning where possible
- Multi-temperature zone optimization
- Compressed storage solutions
- Strategic port selection for provisioning

### Challenge: Quality & Freshness

**Problem:**
- Long voyages without resupply
- Maintaining produce quality
- Guest expectations for freshness

**Solutions:**
- Controlled atmosphere storage
- Hydroponic gardens onboard
- Strategic sourcing at multiple ports
- Menu planning around product life
- Quality inspection protocols

### Challenge: Waste Management

**Problem:**
- Food waste (prep and plate waste)
- Environmental regulations
- Limited disposal options at sea

**Solutions:**
- Predictive production planning
- Portion control optimization
- Donation programs in ports
- Composting and biodigesters
- Waste-to-energy systems

---

## Output Format

### Cruise Supply Chain Report

**Executive Summary:**
- Vessel provisioning performance
- Cost metrics and trends
- Waste reduction achievements
- Key opportunities

**Provisioning Performance:**

| Port | Items Loaded | Value | Lead Time | On-Time % | Quality Issues |
|------|--------------|-------|-----------|-----------|----------------|
| Miami | 1,250 | $185,000 | 4.5 hrs | 98% | 2 |
| Cozumel | 320 | $28,000 | 2.8 hrs | 100% | 0 |
| Grand Cayman | 180 | $15,000 | 3.2 hrs | 95% | 1 |

**Inventory Metrics:**

| Category | Current Stock | Par Level | Days Supply | Turnover | Waste % |
|----------|---------------|-----------|-------------|----------|---------|
| Proteins (Frozen) | 3,200 kg | 3,500 kg | 6.4 | 45x/yr | 2.1% |
| Fresh Produce | 1,800 kg | 2,000 kg | 3.0 | 120x/yr | 5.8% |
| Dairy | 1,200 L | 1,400 L | 4.0 | 90x/yr | 3.2% |
| Dry Goods | 5,500 kg | 6,000 kg | 18.0 | 20x/yr | 1.5% |

**Cost Analysis:**

| Category | Total Cost | Cost per PAX-Day | % of Total | vs. Budget |
|----------|------------|------------------|------------|------------|
| Proteins | $125,000 | $8.50 | 35% | -2% |
| Produce | $85,000 | $5.80 | 24% | +1% |
| Dairy | $45,000 | $3.06 | 13% | 0% |
| Beverages | $70,000 | $4.76 | 20% | -3% |
| Other | $30,000 | $2.04 | 8% | +2% |
| **Total** | **$355,000** | **$24.16** | **100%** | **-1%** |

**Waste Reduction:**

| Metric | Current Voyage | Last Voyage | YTD Average | Target |
|--------|----------------|-------------|-------------|--------|
| Food Waste (kg/PAX-day) | 0.45 | 0.52 | 0.48 | < 0.40 |
| Waste Reduction % | 13% | - | 8% | 15% |
| Donation (meals) | 1,250 | 980 | 1,100 | 1,000 |

**Recommendations:**
1. Shift more provisioning to Miami (15% cost savings vs. Caribbean ports)
2. Reduce produce par levels by 10% (waste reduction opportunity)
3. Implement predictive buffet replenishment system
4. Expand donation program to all ports
5. Install hydroponic garden for herbs and lettuce (35% cost reduction)

---

## Questions to Ask

If you need more context:
1. What's the vessel type and capacity? (mega-ship, luxury, expedition)
2. What itineraries and routes?
3. What's the provisioning frequency and key ports?
4. What are current waste and cost metrics?
5. What systems are in place? (inventory, procurement)
6. What are the main challenges? (costs, quality, waste)
7. What sustainability goals exist?

---

## Related Skills

- **hotel-inventory-management**: For hospitality inventory concepts
- **hospitality-procurement**: For purchasing and supplier management
- **tour-operations**: For passenger operations
- **inventory-optimization**: For inventory management strategies
- **demand-forecasting**: For consumption forecasting
- **route-optimization**: For itinerary optimization
- **cold-chain-logistics**: For temperature-controlled supply chain
- **food-beverage-supply-chain**: For F&B operations
