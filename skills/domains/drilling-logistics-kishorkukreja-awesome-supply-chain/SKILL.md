---
name: drilling-logistics
description: When the user wants to optimize oil and gas drilling operations, manage rig logistics, or coordinate upstream supply chains. Also use when the user mentions "well planning," "rig scheduling," "drilling supply chain," "mud logistics," "tubular management," "offshore logistics," "drilling materials management," or "completion operations." For midstream and downstream, see energy-logistics. For fuel distribution, see fuel-distribution.
---

# Drilling Logistics

You are an expert in oil and gas drilling logistics and upstream supply chain management. Your goal is to help optimize the complex logistics of drilling operations, from rig mobilization to well completion, ensuring efficient resource utilization, cost control, and safety while minimizing non-productive time (NPT).

## Initial Assessment

Before optimizing drilling logistics, understand:

1. **Drilling Program Scope**
   - What type of wells? (vertical, horizontal, offshore, onshore)
   - Number of wells and locations?
   - Drilling depth and formations?
   - Development program timeline?

2. **Rig & Equipment**
   - Rig type? (land rig, jackup, drillship, semi-submersible)
   - Rig availability and contracts?
   - Equipment inventory? (drill pipe, BHA, casing)
   - Maintenance schedules?

3. **Supply Chain Infrastructure**
   - Base locations and warehouses?
   - Transportation modes? (truck, boat, helicopter, pipeline)
   - Supplier network? (domestic, international)
   - Storage facilities and laydown yards?

4. **Objectives & Constraints**
   - Primary goals? (minimize cost, reduce NPT, maximize wells drilled)
   - Budget constraints?
   - Safety and environmental requirements?
   - Regulatory compliance needs?

---

## Drilling Logistics Framework

### Drilling Supply Chain Components

**Upstream Materials:**
- Drilling fluids (mud, additives, chemicals)
- Tubulars (drill pipe, casing, tubing)
- Bottom hole assembly (BHA) components
- Cement and cementing equipment
- Well control equipment (BOPs, valves)

**Support Services:**
- Directional drilling services
- Mud logging and LWD/MWD
- Cementing services
- Wireline and completion services
- Casing running services

**Logistics & Infrastructure:**
- Supply boats and crews
- Helicopters for personnel transfer
- Onshore transportation (trucks, rail)
- Warehouses and supply bases
- Equipment repair and maintenance

---

## Rig Scheduling & Well Planning

### Multi-Well Rig Scheduling

```python
import numpy as np
import pandas as pd
from pulp import *

def optimize_rig_schedule(wells, rigs, drilling_times, mobilization_costs):
    """
    Optimize assignment of rigs to wells and drilling sequence

    Objective: Minimize total time and cost

    Parameters:
    - wells: list of {id, location, priority, earliest_start, deadline}
    - rigs: list of {id, type, availability, day_rate, current_location}
    - drilling_times: dict of {(rig_id, well_id): days_to_drill}
    - mobilization_costs: dict of {(rig_id, from_loc, to_loc): cost}
    """

    prob = LpProblem("Rig_Scheduling", LpMinimize)

    # Decision variables

    # x[r, w]: rig r assigned to well w
    x = {}
    for r, rig in enumerate(rigs):
        for w, well in enumerate(wells):
            x[r, w] = LpVariable(f"Rig_{r}_Well_{w}", cat='Binary')

    # Start time for each well
    start_time = {}
    for w in range(len(wells)):
        start_time[w] = LpVariable(f"Start_{w}", lowBound=0)

    # Completion time for each well
    completion_time = {}
    for w in range(len(wells)):
        completion_time[w] = LpVariable(f"Complete_{w}", lowBound=0)

    # Sequence variables: y[w1, w2, r] = 1 if well w1 drilled before w2 by rig r
    y = {}
    for r in range(len(rigs)):
        for w1 in range(len(wells)):
            for w2 in range(len(wells)):
                if w1 != w2:
                    y[w1, w2, r] = LpVariable(f"Seq_{w1}_{w2}_{r}", cat='Binary')

    # Makespan (total project duration)
    makespan = LpVariable("Makespan", lowBound=0)

    # Objective: minimize weighted sum of makespan and costs
    drilling_cost = lpSum([rigs[r]['day_rate'] *
                          drilling_times.get((rigs[r]['id'], wells[w]['id']), 0) *
                          x[r, w]
                          for r in range(len(rigs))
                          for w in range(len(wells))])

    # Mobilization costs
    mob_cost = 0  # Simplified for this example

    prob += makespan * 10000 + drilling_cost  # Weight makespan heavily

    # Constraints

    # Each well assigned to exactly one rig
    for w in range(len(wells)):
        prob += lpSum([x[r, w] for r in range(len(rigs))]) == 1

    # Well completion time
    for w in range(len(wells)):
        for r in range(len(rigs)):
            drill_time = drilling_times.get((rigs[r]['id'], wells[w]['id']), 999)
            prob += completion_time[w] >= start_time[w] + drill_time * x[r, w]

    # No overlap of wells on same rig (sequencing)
    M = 10000  # Big M
    for r in range(len(rigs)):
        for w1 in range(len(wells)):
            for w2 in range(len(wells)):
                if w1 != w2:
                    # If both wells assigned to rig r, enforce sequence
                    prob += y[w1, w2, r] + y[w2, w1, r] >= \
                            x[r, w1] + x[r, w2] - 1

                    # If w1 before w2
                    prob += start_time[w2] >= completion_time[w1] - \
                            M * (1 - y[w1, w2, r])

    # Well deadlines
    for w, well in enumerate(wells):
        if well.get('deadline'):
            prob += completion_time[w] <= well['deadline']

    # Earliest start times
    for w, well in enumerate(wells):
        prob += start_time[w] >= well.get('earliest_start', 0)

    # Makespan definition
    for w in range(len(wells)):
        prob += makespan >= completion_time[w]

    # Solve
    prob.solve(PULP_CBC_CMD(msg=0))

    # Extract solution
    schedule = []
    for w, well in enumerate(wells):
        assigned_rig = [r for r in range(len(rigs)) if x[r, w].varValue > 0.5]
        if assigned_rig:
            r = assigned_rig[0]
            schedule.append({
                'well': well['id'],
                'rig': rigs[r]['id'],
                'start_day': start_time[w].varValue,
                'completion_day': completion_time[w].varValue,
                'drill_days': drilling_times.get((rigs[r]['id'], well['id']), 0)
            })

    schedule_df = pd.DataFrame(schedule).sort_values('start_day')

    return {
        'status': LpStatus[prob.status],
        'makespan': makespan.varValue,
        'total_cost': value(prob.objective),
        'schedule': schedule_df
    }

# Example usage
wells = [
    {'id': 'Well_A', 'location': (30.0, -95.0), 'priority': 1,
     'earliest_start': 0, 'deadline': 100},
    {'id': 'Well_B', 'location': (30.1, -95.1), 'priority': 2,
     'earliest_start': 0, 'deadline': 120},
    {'id': 'Well_C', 'location': (30.2, -95.0), 'priority': 1,
     'earliest_start': 0, 'deadline': 90},
]

rigs = [
    {'id': 'Rig_1', 'type': 'Land', 'availability': 0, 'day_rate': 25000,
     'current_location': (30.0, -95.0)},
    {'id': 'Rig_2', 'type': 'Land', 'availability': 0, 'day_rate': 22000,
     'current_location': (30.0, -95.0)},
]

drilling_times = {
    ('Rig_1', 'Well_A'): 25,
    ('Rig_1', 'Well_B'): 30,
    ('Rig_1', 'Well_C'): 22,
    ('Rig_2', 'Well_A'): 28,
    ('Rig_2', 'Well_B'): 32,
    ('Rig_2', 'Well_C'): 25,
}

result = optimize_rig_schedule(wells, rigs, drilling_times, {})
print(f"Project makespan: {result['makespan']:.0f} days")
print(result['schedule'])
```

---

## Drilling Materials Management

### Tubular Inventory Optimization

```python
class TubularInventoryManager:
    """
    Manage drill pipe, casing, and tubing inventory for drilling program
    """

    def __init__(self, wells_program, tubular_specs, warehouse_locations):
        self.wells = wells_program
        self.tubulars = tubular_specs
        self.warehouses = warehouse_locations

    def calculate_tubular_requirements(self, well):
        """
        Calculate tubular requirements for a specific well

        Returns quantities needed by tubular type
        """
        requirements = {}

        # Drill pipe (based on depth and margin)
        depth_ft = well['depth']
        drill_pipe_stands = int(depth_ft / 90) + 10  # 90 ft per stand + margin
        requirements['drill_pipe'] = {
            'quantity': drill_pipe_stands,
            'size': well['drill_pipe_size'],
            'grade': well['drill_pipe_grade']
        }

        # Casing strings (multiple strings for deep wells)
        for casing in well['casing_program']:
            casing_joints = int(casing['depth'] / 40) + 2  # 40 ft per joint + margin
            key = f"casing_{casing['size']}_{casing['grade']}"
            requirements[key] = {
                'quantity': casing_joints,
                'size': casing['size'],
                'grade': casing['grade'],
                'depth': casing['depth']
            }

        # Production tubing
        if well.get('tubing_size'):
            tubing_joints = int(depth_ft / 40) + 2
            requirements['tubing'] = {
                'quantity': tubing_joints,
                'size': well['tubing_size'],
                'grade': well['tubing_grade']
            }

        return requirements

    def optimize_tubular_allocation(self):
        """
        Optimize allocation of tubular inventory across wells and locations
        """
        from pulp import *

        prob = LpProblem("Tubular_Allocation", LpMinimize)

        # Variables: allocate tubular inventory from warehouse to well
        allocation = {}

        for well in self.wells:
            well_reqs = self.calculate_tubular_requirements(well)

            for tubular_type, req in well_reqs.items():
                for wh in self.warehouses:
                    var_name = f"{well['id']}_{tubular_type}_{wh['id']}"
                    allocation[well['id'], tubular_type, wh['id']] = LpVariable(
                        var_name,
                        lowBound=0,
                        upBound=req['quantity']
                    )

        # Objective: minimize transportation cost
        transport_cost = []
        for (well_id, tub_type, wh_id), var in allocation.items():
            well = next(w for w in self.wells if w['id'] == well_id)
            wh = next(w for w in self.warehouses if w['id'] == wh_id)

            distance = self.calculate_distance(well['location'], wh['location'])
            # Cost per joint per mile
            transport_cost.append(var * distance * 5)

        prob += lpSum(transport_cost)

        # Constraints

        # Satisfy each well's tubular requirements
        for well in self.wells:
            well_reqs = self.calculate_tubular_requirements(well)

            for tubular_type, req in well_reqs.items():
                prob += lpSum([allocation.get((well['id'], tubular_type, wh['id']), 0)
                              for wh in self.warehouses]) >= req['quantity']

        # Warehouse inventory constraints
        for wh in self.warehouses:
            for tubular_type in self.tubulars:
                allocated = lpSum([allocation.get((well['id'], tubular_type, wh['id']), 0)
                                  for well in self.wells])

                prob += allocated <= wh['inventory'].get(tubular_type, 0)

        # Solve
        prob.solve(PULP_CBC_CMD(msg=0))

        # Extract results
        allocation_plan = []
        for (well_id, tub_type, wh_id), var in allocation.items():
            if var.varValue > 0.1:
                allocation_plan.append({
                    'well': well_id,
                    'tubular_type': tub_type,
                    'warehouse': wh_id,
                    'quantity': var.varValue
                })

        return {
            'status': LpStatus[prob.status],
            'total_cost': value(prob.objective),
            'allocation_plan': pd.DataFrame(allocation_plan)
        }

    def calculate_distance(self, loc1, loc2):
        """Calculate distance between locations"""
        import numpy as np
        return np.sqrt((loc1[0] - loc2[0])**2 + (loc1[1] - loc2[1])**2) * 69
```

---

## Drilling Mud Management

### Mud Program Optimization

```python
def optimize_drilling_fluid_inventory(wells, mud_systems, supply_base):
    """
    Optimize drilling fluid (mud) inventory and logistics

    Parameters:
    - wells: list of wells with mud requirements
    - mud_systems: available mud systems and capacities
    - supply_base: inventory at supply base
    """

    requirements = []

    for well in wells:
        # Calculate mud volume requirements
        hole_sections = well['hole_sections']

        for section in hole_sections:
            hole_diameter = section['diameter_inches']
            depth = section['depth_feet']

            # Mud volume = hole volume + surface system + margin
            hole_volume = (hole_diameter**2 / 1029.4) * depth  # bbls
            surface_volume = 200  # bbls (typical)
            safety_margin = 1.3

            total_volume = (hole_volume + surface_volume) * safety_margin

            requirements.append({
                'well': well['id'],
                'section': section['name'],
                'mud_type': section['mud_type'],
                'volume_bbls': total_volume,
                'mud_weight_ppg': section['mud_weight'],
                'start_day': well['start_day'] + section['start_day_offset']
            })

    requirements_df = pd.DataFrame(requirements)

    # Aggregate by mud type and time period
    mud_schedule = requirements_df.groupby(['mud_type', 'start_day']).agg({
        'volume_bbls': 'sum'
    }).reset_index()

    # Calculate procurement schedule
    procurement = []
    inventory = {}

    for _, row in mud_schedule.iterrows():
        mud_type = row['mud_type']
        day = row['start_day']
        required = row['volume_bbls']

        # Current inventory
        current_inv = inventory.get((mud_type, day), 0)

        if current_inv < required:
            # Need to procure
            order_quantity = required - current_inv + 100  # Add buffer
            lead_time = 7  # days

            procurement.append({
                'mud_type': mud_type,
                'quantity_bbls': order_quantity,
                'order_day': day - lead_time,
                'delivery_day': day,
                'cost': order_quantity * get_mud_cost(mud_type)
            })

            # Update inventory
            inventory[(mud_type, day)] = order_quantity

        # Consume inventory
        inventory[(mud_type, day)] -= required

    return {
        'requirements': requirements_df,
        'procurement_schedule': pd.DataFrame(procurement),
        'total_mud_cost': sum([p['cost'] for p in procurement])
    }

def get_mud_cost(mud_type):
    """Get cost per barrel for mud type"""
    costs = {
        'water_based': 50,
        'oil_based': 150,
        'synthetic_based': 200
    }
    return costs.get(mud_type, 100)
```

---

## Offshore Logistics

### Supply Vessel Scheduling

```python
def optimize_supply_vessel_schedule(rigs, supply_base, vessels, cargo_demand):
    """
    Optimize offshore supply vessel routing and scheduling

    Parameters:
    - rigs: list of offshore rigs with locations and demand
    - supply_base: onshore supply base location
    - vessels: available PSVs (Platform Supply Vessels)
    - cargo_demand: dict of {rig_id: {cargo_type: volume}}
    """
    from pulp import *

    prob = LpProblem("Vessel_Routing", LpMinimize)

    days = 30  # Planning horizon
    T = range(days)

    # Variables

    # x[v, r, t]: vessel v visits rig r on day t
    x = {}
    for v, vessel in enumerate(vessels):
        for r, rig in enumerate(rigs):
            for t in T:
                x[v, r, t] = LpVariable(f"Visit_{v}_{r}_{t}", cat='Binary')

    # Cargo delivered
    cargo_delivered = {}
    for v, vessel in enumerate(vessels):
        for r, rig in enumerate(rigs):
            for t in T:
                cargo_delivered[v, r, t] = LpVariable(
                    f"Cargo_{v}_{r}_{t}",
                    lowBound=0,
                    upBound=vessel['capacity_tons']
                )

    # Objective: minimize total vessel operating cost
    vessel_cost = lpSum([vessels[v]['day_rate'] * x[v, r, t]
                        for v in range(len(vessels))
                        for r in range(len(rigs))
                        for t in T])

    prob += vessel_cost

    # Constraints

    # Meet rig demand over planning horizon
    for r, rig in enumerate(rigs):
        total_demand = sum(cargo_demand.get(rig['id'], {}).values())

        prob += lpSum([cargo_delivered[v, r, t]
                      for v in range(len(vessels))
                      for t in T]) >= total_demand

    # Vessel capacity
    for v, vessel in enumerate(vessels):
        for r, rig in enumerate(rigs):
            for t in T:
                prob += cargo_delivered[v, r, t] <= \
                        vessel['capacity_tons'] * x[v, r, t]

    # Vessel can visit one rig per day
    for v, vessel in enumerate(vessels):
        for t in T:
            prob += lpSum([x[v, r, t] for r in range(len(rigs))]) <= 1

    # Minimum visit frequency (safety requirement)
    for r, rig in enumerate(rigs):
        # At least one visit every 7 days
        for t_start in range(0, days - 7, 7):
            prob += lpSum([x[v, r, t]
                          for v in range(len(vessels))
                          for t in range(t_start, min(t_start + 7, days))]) >= 1

    # Solve
    prob.solve(PULP_CBC_CMD(msg=0))

    # Extract schedule
    schedule = []
    for v, vessel in enumerate(vessels):
        for r, rig in enumerate(rigs):
            for t in T:
                if x[v, r, t].varValue > 0.5:
                    schedule.append({
                        'vessel': vessel['id'],
                        'rig': rig['id'],
                        'day': t,
                        'cargo_tons': cargo_delivered[v, r, t].varValue
                    })

    return {
        'status': LpStatus[prob.status],
        'total_cost': value(prob.objective),
        'schedule': pd.DataFrame(schedule).sort_values('day'),
        'vessel_utilization': {
            vessel['id']: sum([x[v, r, t].varValue
                              for r in range(len(rigs))
                              for t in T]) / days * 100
            for v, vessel in enumerate(vessels)
        }
    }
```

---

## Non-Productive Time (NPT) Reduction

### NPT Analysis & Optimization

```python
class NPTAnalyzer:
    """
    Analyze and optimize non-productive time in drilling operations
    """

    def __init__(self, historical_wells):
        self.wells = historical_wells

    def categorize_npt(self, well_data):
        """
        Categorize NPT by root cause

        Common NPT categories:
        - Stuck pipe
        - Well control
        - Equipment failure
        - Weather downtime
        - Waiting on equipment/services
        - Other
        """
        npt_by_category = {
            'stuck_pipe': 0,
            'well_control': 0,
            'equipment_failure': 0,
            'weather': 0,
            'waiting_on_equipment': 0,
            'other': 0
        }

        for incident in well_data['npt_incidents']:
            category = incident['category']
            hours = incident['hours']
            npt_by_category[category] += hours

        return npt_by_category

    def calculate_npt_cost(self, npt_hours, rig_day_rate=25000):
        """Calculate cost of NPT"""
        rig_hour_rate = rig_day_rate / 24
        return npt_hours * rig_hour_rate

    def identify_improvement_opportunities(self):
        """
        Identify top NPT drivers and improvement opportunities
        """
        all_npt = {}

        for well in self.wells:
            npt_categories = self.categorize_npt(well)
            for category, hours in npt_categories.items():
                if category not in all_npt:
                    all_npt[category] = []
                all_npt[category].append(hours)

        # Calculate statistics
        npt_summary = []
        for category, hours_list in all_npt.items():
            npt_summary.append({
                'category': category,
                'total_hours': sum(hours_list),
                'avg_hours_per_well': np.mean(hours_list),
                'frequency': len([h for h in hours_list if h > 0]),
                'cost': self.calculate_npt_cost(sum(hours_list))
            })

        npt_df = pd.DataFrame(npt_summary).sort_values('total_hours',
                                                       ascending=False)

        return npt_df

    def recommend_mitigation_actions(self, npt_summary):
        """
        Recommend actions to reduce NPT
        """
        recommendations = []

        for _, row in npt_summary.iterrows():
            category = row['category']

            if category == 'stuck_pipe' and row['total_hours'] > 100:
                recommendations.append({
                    'category': category,
                    'action': 'Improve hole cleaning practices, use real-time monitoring',
                    'estimated_reduction': '30-50%',
                    'investment_required': 'Low-Medium'
                })

            elif category == 'equipment_failure' and row['total_hours'] > 80:
                recommendations.append({
                    'category': category,
                    'action': 'Implement predictive maintenance, upgrade critical equipment',
                    'estimated_reduction': '40-60%',
                    'investment_required': 'Medium-High'
                })

            elif category == 'waiting_on_equipment' and row['total_hours'] > 60:
                recommendations.append({
                    'category': category,
                    'action': 'Improve logistics planning, increase critical spare inventory',
                    'estimated_reduction': '50-70%',
                    'investment_required': 'Low'
                })

            elif category == 'weather' and row['total_hours'] > 50:
                recommendations.append({
                    'category': category,
                    'action': 'Improve weather forecasting, adjust operational windows',
                    'estimated_reduction': '20-30%',
                    'investment_required': 'Low'
                })

        return pd.DataFrame(recommendations)
```

---

## Tools & Libraries

### Python Libraries

**Optimization:**
- `PuLP`: Linear programming
- `Pyomo`: Optimization modeling
- `OR-Tools`: Google optimization tools
- `scipy.optimize`: General optimization

**Geospatial:**
- `geopandas`: Geographic data
- `geopy`: Distance calculations
- `folium`: Interactive maps

**Data Analysis:**
- `pandas`, `numpy`: Data manipulation
- `matplotlib`, `seaborn`: Visualization

### Commercial Software

**Drilling Planning:**
- **Landmark (Halliburton) WellPlan**: Well planning and design
- **Schlumberger Techlog**: Wellbore data management
- **Baker Hughes JewelSuite**: Well construction planning
- **DrillScan**: Drilling operations optimization

**Logistics & Supply Chain:**
- **SAP S/4HANA Oil & Gas**: ERP for oil and gas
- **Oracle E-Business Suite**: Supply chain management
- **IFS Applications**: Project-driven ERP
- **Quorum Business Solutions**: Energy software

**Data & Analytics:**
- **Pason**: Real-time drilling data
- **Corva**: Drilling analytics platform
- **Well Data Labs**: Machine learning for drilling

---

## Common Challenges & Solutions

### Challenge: Rig Mobilization Delays

**Problem:**
- Long lead times for rig moves
- Expensive mobilization costs
- Permitting and preparation delays

**Solutions:**
- Batch drilling (multiple wells from one pad)
- Early planning and permitting
- Maintain rig-ready well sites
- Use walking rigs for closely spaced wells
- Optimize rig schedule to minimize moves

### Challenge: Equipment Availability

**Problem:**
- Long lead times for specialty tools
- Equipment failures and downtime
- Limited inventory of critical items

**Solutions:**
- Strategic inventory positioning
- Predictive maintenance programs
- Equipment sharing agreements
- Backup equipment on standby
- Vendor-managed inventory

### Challenge: Offshore Weather Delays

**Problem:**
- Weather windows for critical operations
- Personnel transfer constraints
- Supply vessel delays

**Solutions:**
- Advanced weather forecasting
- Flexible scheduling with buffers
- Weather-protected operations where possible
- Adequate supply storage on platform
- Alternative transportation (helicopter)

### Challenge: Material Handling & Tracking

**Problem:**
- Lost or misplaced equipment
- Inventory discrepancies
- Time wasted searching for materials

**Solutions:**
- RFID tagging and tracking systems
- Centralized inventory management
- Digital twins of inventory
- Automated check-in/check-out
- Real-time visibility dashboards

---

## Output Format

### Drilling Logistics Plan

**Executive Summary:**
- Drilling program overview
- Total estimated duration and cost
- Key logistics strategies
- Risk mitigation approach

**Rig Schedule:**

| Well ID | Location | Rig | Start Date | Duration (days) | Completion Date | Status |
|---------|----------|-----|------------|-----------------|-----------------|--------|
| Well-A | Pad 1 | Rig-1 | 2026-03-01 | 25 | 2026-03-26 | Planned |
| Well-B | Pad 1 | Rig-1 | 2026-03-27 | 30 | 2026-04-26 | Planned |
| Well-C | Pad 2 | Rig-2 | 2026-03-15 | 28 | 2026-04-12 | Planned |

**Material Requirements:**

| Item | Total Quantity | Unit | Cost | Lead Time | Procurement Status |
|------|----------------|------|------|-----------|--------------------|
| 5" Drill Pipe | 1,500 | Joints | $2.5M | 60 days | Ordered |
| 9-5/8" Casing | 800 | Joints | $1.2M | 45 days | In Stock |
| Drilling Mud (OBM) | 5,000 | Bbls | $750K | 14 days | On Order |

**Logistics Cost Breakdown:**

| Category | Cost | % of Total |
|----------|------|------------|
| Rig Day Rates | $15.0M | 65% |
| Tubulars & Materials | $4.5M | 20% |
| Services (directional, cementing, etc.) | $2.0M | 9% |
| Transportation & Logistics | $1.0M | 4% |
| Contingency | $0.5M | 2% |
| **Total** | **$23.0M** | **100%** |

**Critical Path Items:**

| Item | Required Date | Status | Risk Level | Mitigation |
|------|---------------|--------|------------|------------|
| Rig-1 Availability | 2026-03-01 | Confirmed | Low | Contract in place |
| BHA Components | 2026-02-20 | Pending | Medium | Expedite order |
| Completion Equipment | 2026-04-01 | Ordered | Low | Adequate lead time |

**KPIs & Targets:**

| Metric | Target | Baseline | Notes |
|--------|--------|----------|-------|
| Avg Days per Well | 25 | 30 | 17% improvement |
| NPT % | < 5% | 8% | Focus on equipment reliability |
| Cost per Foot | $180 | $220 | 18% reduction |
| Safety Incidents | 0 | - | TRIR < 0.5 |

---

## Questions to Ask

If you need more context:
1. What type of drilling program? (onshore, offshore, number of wells)
2. What's the timeline and urgency?
3. What rigs are available or contracted?
4. What's the supply chain infrastructure? (bases, warehouses, transportation)
5. What are the main cost drivers and constraints?
6. What's the current NPT rate and key causes?
7. What safety and environmental requirements must be met?

---

## Related Skills

- **energy-logistics**: For midstream and downstream oil & gas
- **fuel-distribution**: For refined product distribution
- **network-design**: For supply chain network optimization
- **route-optimization**: For transportation routing
- **inventory-optimization**: For material inventory management
- **project-scheduling**: For construction scheduling
- **risk-mitigation**: For operational risk management
- **fleet-management**: For vehicle and equipment fleet
