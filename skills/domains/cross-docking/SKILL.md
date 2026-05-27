---
name: cross-docking
description: When the user wants to implement cross-docking operations, optimize transshipment, or reduce warehouse storage. Also use when the user mentions "crossdock," "transshipment," "flow-through distribution," "dock-to-dock," "consolidation center," or "break-bulk operations." For general warehouse design, see warehouse-design. For dock scheduling, see dock-door-assignment.
---

# Cross-Docking

You are an expert in cross-docking operations and transshipment logistics. Your goal is to help design and optimize cross-dock facilities that minimize handling, reduce inventory, and accelerate product flow from inbound to outbound without storage.

## Initial Assessment

Before designing cross-dock operations, understand:

1. **Business Context**
   - What products are being cross-docked?
   - Current supply chain structure?
   - Why cross-dock? (speed, cost, space constraints)
   - Volume and SKU complexity?

2. **Operational Requirements**
   - Inbound frequency? (continuous, scheduled)
   - Outbound frequency? (daily routes, on-demand)
   - Processing window? (hours from receipt to ship)
   - Quality/inspection requirements?

3. **Facility Characteristics**
   - Existing facility or new build?
   - Number of dock doors?
   - Staging area size?
   - Material handling equipment?
   - Technology systems (WMS, TMS)?

4. **Product Characteristics**
   - Case-level or pallet-level?
   - Full pallet, mixed pallet, or break-bulk?
   - Temperature requirements?
   - Handling restrictions?

---

## Cross-Docking Framework

### Types of Cross-Docking

**1. Pre-Distributed Cross-Docking**
- Supplier pre-sorts and labels for final destination
- Minimal handling at cross-dock
- Direct transfer inbound to outbound
- **Best for**: Retail distribution, known destinations

**2. Consolidation Cross-Docking**
- Combine inbound shipments from multiple origins
- Consolidate into single outbound shipment
- **Best for**: LTL to TL conversion, supplier consolidation

**3. Deconsolidation (Break-Bulk) Cross-Docking**
- Receive bulk shipments (TL, container)
- Break into smaller shipments for multiple destinations
- **Best for**: Import distribution, regional breakdown

**4. Opportunistic Cross-Docking**
- Dynamic decision to cross-dock vs. store
- Based on immediate outbound demand
- **Best for**: Mixed operations, demand-driven

**5. Manufacturing Cross-Docking**
- Receive components, assemble/kit, ship finished goods
- Light assembly or kitting operations
- **Best for**: JIT manufacturing, value-added services

---

## Cross-Dock Design Principles

### Facility Layout

```python
import numpy as np
import matplotlib.pyplot as plt

class CrossDockLayoutDesigner:
    """
    Design optimal cross-dock facility layout

    Optimize door assignments and flow paths
    """

    def __init__(self, num_inbound_doors, num_outbound_doors,
                 staging_area_sqft):
        self.inbound_doors = num_inbound_doors
        self.outbound_doors = num_outbound_doors
        self.staging_area = staging_area_sqft

    def calculate_facility_requirements(self, daily_volume_pallets,
                                       dwell_time_hours=4):
        """
        Calculate facility size requirements

        Parameters:
        - daily_volume_pallets: pallets per day through facility
        - dwell_time_hours: average time pallet in facility
        """

        # Peak simultaneous pallets in facility
        pallets_per_hour = daily_volume_pallets / 24
        peak_pallets = pallets_per_hour * dwell_time_hours

        # Space per pallet (including aisles)
        sqft_per_pallet = 25  # 40x48 pallet + spacing

        staging_required = peak_pallets * sqft_per_pallet

        # Door requirements
        # Assume 30 pallets per door per day (4-hour turnaround)
        inbound_doors_needed = np.ceil(daily_volume_pallets / 30)
        outbound_doors_needed = np.ceil(daily_volume_pallets / 30)

        return {
            'staging_area_sqft': staging_required,
            'inbound_doors_needed': int(inbound_doors_needed),
            'outbound_doors_needed': int(outbound_doors_needed),
            'peak_pallets': peak_pallets,
            'daily_volume': daily_volume_pallets
        }

    def design_i_shaped_layout(self):
        """
        I-shaped layout: Inbound on one side, outbound on opposite

        Pros: Clear separation, simple traffic flow
        Cons: Longer travel distance across facility
        """

        layout = {
            'type': 'I-shaped',
            'inbound_side': 'North',
            'outbound_side': 'South',
            'staging': 'Center aisle',
            'flow': 'North to South',
            'avg_travel_distance': self.staging_area ** 0.5,  # Rough estimate
            'advantages': [
                'Clear separation of inbound/outbound',
                'Easy to scale by adding doors',
                'Simple traffic patterns'
            ],
            'disadvantages': [
                'Longer travel distances',
                'May require more staging space'
            ]
        }

        return layout

    def design_l_shaped_layout(self):
        """
        L-shaped layout: Inbound and outbound on adjacent sides

        Pros: Shorter travel distance, compact
        Cons: More complex traffic patterns
        """

        layout = {
            'type': 'L-shaped',
            'inbound_side': 'North',
            'outbound_side': 'East',
            'staging': 'Corner staging area',
            'flow': 'North to East',
            'avg_travel_distance': self.staging_area ** 0.5 * 0.7,
            'advantages': [
                'Shorter travel distances',
                'More compact footprint',
                'Better land utilization'
            ],
            'disadvantages': [
                'Complex traffic flow',
                'Potential congestion at corner',
                'Less scalable'
            ]
        }

        return layout

    def design_t_shaped_layout(self):
        """
        T-shaped layout: Inbound on base, outbound on two wings

        Pros: Balanced flow, multiple staging zones
        Cons: Requires specific building shape
        """

        layout = {
            'type': 'T-shaped',
            'inbound_side': 'North (base)',
            'outbound_sides': 'East and West (wings)',
            'staging': 'Distributed staging zones',
            'flow': 'North to East/West',
            'advantages': [
                'Balanced distribution',
                'Multiple staging zones',
                'Good for high volume'
            ],
            'disadvantages': [
                'Requires specific building',
                'More complex management',
                'Higher facility cost'
            ]
        }

        return layout

    def recommend_layout(self, daily_volume, land_constraints=None):
        """
        Recommend optimal layout based on requirements

        Parameters:
        - daily_volume: daily pallet volume
        - land_constraints: 'rectangular', 'square', 'irregular'
        """

        if daily_volume < 500:
            recommendation = 'I-shaped'
            rationale = 'Lower volume, simple operations'

        elif daily_volume < 1500:
            if land_constraints == 'square':
                recommendation = 'L-shaped'
                rationale = 'Medium volume, compact footprint'
            else:
                recommendation = 'I-shaped'
                rationale = 'Medium volume, scalable design'

        else:
            recommendation = 'T-shaped or X-shaped'
            rationale = 'High volume, need distributed operations'

        return {
            'recommended_layout': recommendation,
            'rationale': rationale,
            'daily_volume': daily_volume
        }

# Example usage
designer = CrossDockLayoutDesigner(
    num_inbound_doors=20,
    num_outbound_doors=25,
    staging_area_sqft=50000
)

requirements = designer.calculate_facility_requirements(
    daily_volume_pallets=1200,
    dwell_time_hours=4
)

print(f"Staging area needed: {requirements['staging_area_sqft']:,.0f} sq ft")
print(f"Inbound doors: {requirements['inbound_doors_needed']}")
print(f"Outbound doors: {requirements['outbound_doors_needed']}")

layout_rec = designer.recommend_layout(daily_volume=1200)
print(f"\nRecommended layout: {layout_rec['recommended_layout']}")
print(f"Rationale: {layout_rec['rationale']}")
```

### Door Assignment Optimization

```python
from pulp import *
import pandas as pd

class DoorAssignmentOptimizer:
    """
    Optimize assignment of shipments to dock doors

    Minimize travel distance and congestion
    """

    def __init__(self, inbound_shipments, outbound_routes, door_positions):
        """
        Parameters:
        - inbound_shipments: DataFrame with inbound load details
        - outbound_routes: DataFrame with outbound route details
        - door_positions: Dict mapping door IDs to (x, y) positions
        """
        self.inbound = inbound_shipments
        self.outbound = outbound_routes
        self.door_positions = door_positions

    def calculate_distance_matrix(self):
        """
        Calculate distance between all inbound and outbound doors

        Returns matrix of travel distances
        """

        inbound_doors = sorted(self.inbound['door_id'].unique())
        outbound_doors = sorted(self.outbound['door_id'].unique())

        distances = {}

        for in_door in inbound_doors:
            for out_door in outbound_doors:
                in_pos = self.door_positions[in_door]
                out_pos = self.door_positions[out_door]

                # Euclidean distance (simplified)
                distance = ((in_pos[0] - out_pos[0]) ** 2 +
                           (in_pos[1] - out_pos[1]) ** 2) ** 0.5

                distances[(in_door, out_door)] = distance

        return distances

    def optimize_door_assignments(self):
        """
        Assign shipments to minimize total travel distance

        Uses MIP optimization
        """

        # Calculate distance matrix
        distances = self.calculate_distance_matrix()

        # Create optimization problem
        prob = LpProblem("Door_Assignment", LpMinimize)

        # Decision variables
        # x[i,j] = 1 if inbound shipment i assigned to inbound door j
        inbound_assignments = LpVariable.dicts(
            "InboundAssign",
            [(i, j) for i in self.inbound.index
             for j in self.inbound['door_id'].unique()],
            cat='Binary'
        )

        # y[k,m] = 1 if outbound route k assigned to outbound door m
        outbound_assignments = LpVariable.dicts(
            "OutboundAssign",
            [(k, m) for k in self.outbound.index
             for m in self.outbound['door_id'].unique()],
            cat='Binary'
        )

        # Objective: minimize total travel distance
        # This is simplified - in practice, track pallet flows between doors
        prob += lpSum([
            distances.get((self.inbound.loc[i, 'door_id'],
                          self.outbound.loc[k, 'door_id']), 0) *
            self.inbound.loc[i, 'pallets'] *
            inbound_assignments.get((i, self.inbound.loc[i, 'door_id']), 0)
            for i in self.inbound.index
            for k in self.outbound.index
        ])

        # Constraints: Each shipment assigned to exactly one door
        for i in self.inbound.index:
            prob += lpSum([inbound_assignments[(i, j)]
                          for j in self.inbound['door_id'].unique()]) == 1

        for k in self.outbound.index:
            prob += lpSum([outbound_assignments[(k, m)]
                          for m in self.outbound['door_id'].unique()]) == 1

        # Solve
        prob.solve(PULP_CBC_CMD(msg=0))

        # Extract solution
        assignments = {
            'inbound': {},
            'outbound': {},
            'total_distance': value(prob.objective)
        }

        for (i, j), var in inbound_assignments.items():
            if var.varValue > 0.5:
                assignments['inbound'][i] = j

        for (k, m), var in outbound_assignments.items():
            if var.varValue > 0.5:
                assignments['outbound'][k] = m

        return assignments

    def analyze_flow_patterns(self):
        """
        Analyze flow patterns between inbound and outbound

        Identify high-volume lanes for optimization
        """

        # Group by origin-destination pairs
        flows = []

        for _, inbound in self.inbound.iterrows():
            for _, outbound in self.outbound.iterrows():
                # Simplified: assume all inbound goes to all outbound
                flow_volume = inbound['pallets'] * 0.1  # Simplified allocation

                flows.append({
                    'inbound_door': inbound['door_id'],
                    'outbound_door': outbound['door_id'],
                    'volume': flow_volume,
                    'origin': inbound['origin'],
                    'destination': outbound['destination']
                })

        flows_df = pd.DataFrame(flows)

        # Identify top flow lanes
        top_flows = flows_df.nlargest(10, 'volume')

        return {
            'all_flows': flows_df,
            'top_flows': top_flows,
            'total_volume': flows_df['volume'].sum()
        }
```

---

## Cross-Dock Operations

### Receiving Process

```python
class CrossDockReceivingManager:
    """
    Manage inbound receiving process for cross-dock

    Optimize receiving sequence and staging
    """

    def __init__(self):
        self.receiving_queue = []
        self.staged_pallets = {}

    def schedule_inbound_receipts(self, appointments):
        """
        Schedule inbound truck appointments

        Optimize door utilization and avoid congestion

        Parameters:
        - appointments: DataFrame with requested arrival times
        """

        # Time slot capacity (doors * slots per hour)
        num_doors = 20
        capacity_per_hour = num_doors * 1  # 1 truck per door per hour

        scheduled = []

        for _, appt in appointments.iterrows():
            requested_time = appt['requested_arrival']

            # Find available slot
            slot_found = False
            for hour_offset in range(24):  # Try up to 24 hours ahead
                check_time = requested_time + pd.Timedelta(hours=hour_offset)

                # Count trucks in this hour
                trucks_in_slot = sum(
                    1 for s in scheduled
                    if s['scheduled_time'].hour == check_time.hour
                )

                if trucks_in_slot < capacity_per_hour:
                    scheduled.append({
                        'shipment_id': appt['shipment_id'],
                        'requested_time': requested_time,
                        'scheduled_time': check_time,
                        'door_assigned': trucks_in_slot + 1,
                        'delay_hours': hour_offset
                    })
                    slot_found = True
                    break

            if not slot_found:
                scheduled.append({
                    'shipment_id': appt['shipment_id'],
                    'requested_time': requested_time,
                    'scheduled_time': None,
                    'status': 'Unable to schedule'
                })

        return pd.DataFrame(scheduled)

    def process_inbound_shipment(self, shipment_id, pallets, destinations):
        """
        Process inbound shipment

        Sort and stage pallets by destination

        Parameters:
        - shipment_id: unique shipment identifier
        - pallets: list of pallet IDs
        - destinations: dict mapping pallet to destination
        """

        processed = {
            'shipment_id': shipment_id,
            'total_pallets': len(pallets),
            'staged_by_destination': {}
        }

        # Sort pallets by destination
        for pallet in pallets:
            destination = destinations.get(pallet, 'Unknown')

            if destination not in self.staged_pallets:
                self.staged_pallets[destination] = []

            self.staged_pallets[destination].append(pallet)

            if destination not in processed['staged_by_destination']:
                processed['staged_by_destination'][destination] = 0

            processed['staged_by_destination'][destination] += 1

        return processed

    def get_staging_summary(self):
        """Get summary of staged pallets by destination"""

        summary = []

        for destination, pallets in self.staged_pallets.items():
            summary.append({
                'destination': destination,
                'pallets_staged': len(pallets),
                'ready_to_ship': len(pallets) >= 20  # Minimum for TL
            })

        return pd.DataFrame(summary)
```

### Shipping Process

```python
class CrossDockShippingManager:
    """
    Manage outbound shipping process

    Build loads and dispatch trucks
    """

    def __init__(self, truck_capacity=26):
        self.truck_capacity = truck_capacity  # pallets
        self.outbound_loads = []

    def build_outbound_loads(self, staged_pallets, routes):
        """
        Build outbound truck loads from staged pallets

        Parameters:
        - staged_pallets: dict of destination -> pallet list
        - routes: DataFrame with route information
        """

        loads = []
        load_id = 1

        for _, route in routes.iterrows():
            destination = route['destination']
            available_pallets = staged_pallets.get(destination, [])

            if len(available_pallets) == 0:
                continue

            # Build full truckloads
            while len(available_pallets) >= self.truck_capacity:
                load_pallets = available_pallets[:self.truck_capacity]
                available_pallets = available_pallets[self.truck_capacity:]

                loads.append({
                    'load_id': f'LOAD{load_id:04d}',
                    'destination': destination,
                    'pallets': len(load_pallets),
                    'utilization': 1.0,
                    'status': 'Full Load'
                })

                load_id += 1

            # Handle remaining pallets (partial load)
            if len(available_pallets) > 0:
                loads.append({
                    'load_id': f'LOAD{load_id:04d}',
                    'destination': destination,
                    'pallets': len(available_pallets),
                    'utilization': len(available_pallets) / self.truck_capacity,
                    'status': 'Partial Load'
                })

                load_id += 1

        return pd.DataFrame(loads)

    def optimize_multi_stop_routes(self, partial_loads, max_stops=3):
        """
        Consolidate partial loads into multi-stop routes

        Reduce number of trucks needed

        Parameters:
        - partial_loads: DataFrame with partial loads
        - max_stops: maximum stops per route
        """

        # Simple greedy algorithm
        multi_stop_routes = []
        remaining_loads = partial_loads.copy()

        while len(remaining_loads) > 0:
            # Start new route
            route = []
            total_pallets = 0

            for idx, load in remaining_loads.iterrows():
                if (len(route) < max_stops and
                    total_pallets + load['pallets'] <= self.truck_capacity):

                    route.append({
                        'load_id': load['load_id'],
                        'destination': load['destination'],
                        'pallets': load['pallets']
                    })

                    total_pallets += load['pallets']
                    remaining_loads = remaining_loads.drop(idx)

                    if total_pallets >= self.truck_capacity:
                        break

            if route:
                multi_stop_routes.append({
                    'route_id': len(multi_stop_routes) + 1,
                    'stops': len(route),
                    'total_pallets': total_pallets,
                    'utilization': total_pallets / self.truck_capacity,
                    'route': route
                })

        return multi_stop_routes
```

---

## Cross-Dock Performance Metrics

### Key Performance Indicators

```python
class CrossDockMetrics:
    """
    Calculate cross-dock performance metrics

    Track efficiency and identify improvement opportunities
    """

    def __init__(self, operations_data):
        """
        Parameters:
        - operations_data: DataFrame with operational logs
          columns: ['timestamp', 'shipment_id', 'event_type',
                   'location', 'pallets', 'duration']
        """
        self.data = operations_data

    def calculate_dwell_time(self):
        """
        Calculate average dwell time

        Time from inbound receipt to outbound ship
        """

        # Group by shipment
        shipment_times = {}

        for _, event in self.data.iterrows():
            shipment_id = event['shipment_id']

            if shipment_id not in shipment_times:
                shipment_times[shipment_id] = {}

            event_type = event['event_type']
            timestamp = event['timestamp']

            if event_type == 'inbound_received':
                shipment_times[shipment_id]['received'] = timestamp
            elif event_type == 'outbound_shipped':
                shipment_times[shipment_id]['shipped'] = timestamp

        # Calculate dwell times
        dwell_times = []

        for shipment_id, times in shipment_times.items():
            if 'received' in times and 'shipped' in times:
                dwell = (times['shipped'] - times['received']).total_seconds() / 3600
                dwell_times.append(dwell)

        return {
            'avg_dwell_time_hours': np.mean(dwell_times) if dwell_times else 0,
            'median_dwell_time_hours': np.median(dwell_times) if dwell_times else 0,
            'max_dwell_time_hours': np.max(dwell_times) if dwell_times else 0,
            'target_dwell_time_hours': 4,  # Best practice
            'shipments_within_target': sum(1 for d in dwell_times if d <= 4) / len(dwell_times) if dwell_times else 0
        }

    def calculate_dock_door_utilization(self, num_doors=20, hours_per_day=16):
        """
        Calculate dock door utilization

        % of time doors are occupied
        """

        # Count door-hours used
        door_events = self.data[
            self.data['event_type'].isin(['inbound_received', 'outbound_shipped'])
        ]

        total_door_hours = door_events['duration'].sum()

        # Available door-hours
        days = (self.data['timestamp'].max() - self.data['timestamp'].min()).days
        available_door_hours = num_doors * hours_per_day * days

        utilization = total_door_hours / available_door_hours if available_door_hours > 0 else 0

        return {
            'door_utilization': utilization,
            'total_door_hours_used': total_door_hours,
            'available_door_hours': available_door_hours,
            'target_utilization': 0.75  # 75% target
        }

    def calculate_throughput(self):
        """
        Calculate facility throughput

        Pallets per hour, per day, per square foot
        """

        total_pallets = self.data[
            self.data['event_type'] == 'inbound_received'
        ]['pallets'].sum()

        hours = (self.data['timestamp'].max() -
                self.data['timestamp'].min()).total_seconds() / 3600

        days = hours / 24

        return {
            'pallets_per_hour': total_pallets / hours if hours > 0 else 0,
            'pallets_per_day': total_pallets / days if days > 0 else 0,
            'total_pallets': total_pallets
        }

    def calculate_crossdock_rate(self):
        """
        Calculate % of volume cross-docked vs. stored

        True cross-dock = ship within 24 hours
        """

        shipment_times = {}

        for _, event in self.data.iterrows():
            shipment_id = event['shipment_id']

            if shipment_id not in shipment_times:
                shipment_times[shipment_id] = {}

            if event['event_type'] == 'inbound_received':
                shipment_times[shipment_id]['received'] = event['timestamp']
            elif event['event_type'] == 'outbound_shipped':
                shipment_times[shipment_id]['shipped'] = event['timestamp']

        # Calculate cross-dock rate
        total_shipments = len(shipment_times)
        crossdocked = 0

        for times in shipment_times.values():
            if 'received' in times and 'shipped' in times:
                dwell_hours = (times['shipped'] - times['received']).total_seconds() / 3600
                if dwell_hours <= 24:
                    crossdocked += 1

        crossdock_rate = crossdocked / total_shipments if total_shipments > 0 else 0

        return {
            'crossdock_rate': crossdock_rate,
            'total_shipments': total_shipments,
            'crossdocked_shipments': crossdocked,
            'stored_shipments': total_shipments - crossdocked,
            'target_crossdock_rate': 0.90  # 90% target
        }

    def generate_performance_report(self):
        """Generate comprehensive performance report"""

        dwell = self.calculate_dwell_time()
        doors = self.calculate_dock_door_utilization()
        throughput = self.calculate_throughput()
        xdock_rate = self.calculate_crossdock_rate()

        return {
            'dwell_time': dwell,
            'door_utilization': doors,
            'throughput': throughput,
            'crossdock_rate': xdock_rate
        }
```

---

## Common Challenges & Solutions

### Challenge: Long Dwell Times

**Problem:**
- Product sitting too long in cross-dock
- Approaching storage operation (defeating purpose)
- Target: <4 hours, seeing 12-24 hours

**Solutions:**
- Synchronized inbound/outbound schedules
- Pre-assigned outbound destinations (before arrival)
- Dedicated staging zones by destination
- Wave-based processing (time windows)
- Improve dock door scheduling
- Better WMS system for visibility
- Real-time status tracking

### Challenge: Mismatched Inbound/Outbound Timing

**Problem:**
- Inbound arrives, but no outbound ready
- Outbound waiting for inbound
- Creates storage need

**Solutions:**
- Time-slotted appointments
- Advance shipping notices (ASN)
- Buffer staging for timing mismatches
- Multi-day outbound consolidation window
- Demand-driven pull system
- Communicate closely with carriers

### Challenge: Product Damage

**Problem:**
- Multiple handling points increase damage
- Fast pace increases risk
- Claims and returns

**Solutions:**
- Minimize touches (goal: 2 or less)
- Use conveyors or automated systems
- Train employees on proper handling
- Pre-palletized/floor-loaded inbound
- Quality checkpoints at key stages
- Track damage by handler/shift

### Challenge: Mixing Cross-Dock and Storage

**Problem:**
- Facility has both cross-dock and storage
- Confusion about which product to cross-dock
- Suboptimal use of space

**Solutions:**
- Clearly define cross-dock criteria
- Separate physical zones
- Different SKU strategies (A items = cross-dock)
- Use WMS to direct putaway decisions
- Track and measure cross-dock percentage
- Set targets by product category

### Challenge: High Labor Costs

**Problem:**
- Labor-intensive sorting and staging
- Premium pay for speed requirements
- Overtime for processing windows

**Solutions:**
- Automate sortation (sorters, conveyors)
- Pre-sort at origin (pre-distributed model)
- Use RF/barcode scanning for accuracy
- Optimize door assignments (reduce travel)
- Cross-train workforce
- Flex labor with peak times

### Challenge: Limited Staging Space

**Problem:**
- Congested staging areas
- Can't hold pallets for consolidation
- Inefficient use of space

**Solutions:**
- Increase staging density (narrower aisles)
- Vertical staging (pallet racking)
- Dynamic staging zones (real-time allocation)
- Flow-through lanes (minimal staging)
- Off-site buffer warehouse (overflow)
- Smaller, more frequent outbound loads

---

## Technology & Automation

### Cross-Dock WMS Requirements

**Core Capabilities:**
- Real-time inventory visibility
- ASN (Advance Ship Notice) processing
- Door assignment and scheduling
- Directed putaway to staging
- Wave planning and release
- Load building and optimization
- RF/mobile scanning
- Integration with TMS

**Leading Cross-Dock WMS:**
- **Manhattan Associates WMS**: Enterprise-grade
- **Blue Yonder WMS**: AI-powered
- **SAP Extended Warehouse Management**: ERP-integrated
- **HighJump WMS**: Mid-market
- **Körber WMS**: Supply chain suite
- **Infor WMS**: CloudSuite

### Automation Technologies

**Sortation Systems:**
- Sliding shoe sorters
- Cross-belt sorters
- Tilt-tray sorters
- Bomb bay sorters

**Conveyor Systems:**
- Powered roller conveyors
- Belt conveyors
- Spiral conveyors (vertical)

**AGVs / AMRs:**
- Autonomous pallet movers
- Reduce manual labor
- Flexible routing

**Put-to-Light / Pick-to-Light:**
- Direct operators to staging lanes
- Visual confirmation

---

## Output Format

### Cross-Dock Operations Report

**Executive Summary:**
- Daily volume: 1,850 pallets
- Dwell time: 6.2 hours (target: <4 hours)
- Cross-dock rate: 78% (target: >90%)
- Door utilization: 68% (target: 75%)
- Recommendation: Improve scheduling, reduce dwell time

**Performance Metrics:**

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Avg dwell time | 6.2 hrs | <4 hrs | ⚠️ 55% over |
| Cross-dock rate | 78% | >90% | ⚠️ Below target |
| Door utilization | 68% | 75% | ⚠️ Below target |
| Pallets/day | 1,850 | 2,000 | ✓ 93% of target |
| Damage rate | 0.8% | <0.5% | ⚠️ 60% over |

**Operational Analysis:**

**Dwell Time by Destination:**

| Destination | Volume | Avg Dwell | % Over Target |
|-------------|--------|-----------|---------------|
| Southeast | 550 | 4.2 hrs | 5% |
| Midwest | 420 | 8.5 hrs | 113% ⚠️ |
| West | 380 | 5.8 hrs | 45% ⚠️ |
| Northeast | 500 | 5.1 hrs | 28% |

**Root Causes for Long Dwell (Midwest):**
- No scheduled outbound Monday/Wednesday
- Pallets wait for Friday consolidation
- Recommendation: Add mid-week departure or use 3PL

**Door Utilization:**

| Door Type | Doors | Utilization | Peak Hours | Bottleneck? |
|-----------|-------|-------------|------------|-------------|
| Inbound | 20 | 72% | 6 AM - 10 AM | Yes |
| Outbound | 25 | 64% | 2 PM - 6 PM | No |

**Recommendations:**

1. **Synchronized Scheduling** - Impact: -2 hours dwell time
   - Coordinate inbound/outbound appointments
   - Schedule outbound within 2 hours of inbound receipt
   - Use ASN to pre-assign staging lanes

2. **Expand Midwest Service** - Impact: +12% cross-dock rate
   - Add Wednesday departure
   - Reduce Midwest dwell from 8.5 to 4 hours
   - Cost: $40K annually, saves $65K in handling

3. **Implement Sortation System** - Impact: +30% throughput
   - Automate staging by destination
   - Reduce labor by 20%
   - Investment: $850K, ROI: 2.1 years

4. **Improve Door Scheduling** - Impact: +7% door utilization
   - Time-slot appointments (prevent congestion)
   - Balance inbound arrivals throughout day
   - Use dock scheduling software

**Expected Results (6 months):**

| Metric | Current | Target | Improvement |
|--------|---------|--------|-------------|
| Avg dwell time | 6.2 hrs | 4.0 hrs | -35% |
| Cross-dock rate | 78% | 92% | +14 pts |
| Door utilization | 68% | 76% | +8 pts |
| Daily throughput | 1,850 | 2,150 | +16% |
| Operating cost/pallet | $8.50 | $7.20 | -15% |

---

## Questions to Ask

If you need more context:
1. What's your daily volume through the cross-dock?
2. What's your current dwell time?
3. How many dock doors (inbound/outbound)?
4. What products are being cross-docked?
5. Pre-sorted by suppliers or sorted in-house?
6. Any WMS or automation in place?
7. What's the cross-dock rate (vs. storage)?
8. Main pain points? (speed, accuracy, cost, space)

---

## Related Skills

- **warehouse-design**: Overall warehouse and DC layout
- **dock-door-assignment**: Optimize dock door scheduling
- **freight-optimization**: Inbound/outbound freight management
- **route-optimization**: Outbound route planning
- **order-fulfillment**: Fulfillment operations
- **warehouse-slotting-optimization**: Storage slotting strategy
- **load-building-optimization**: Load planning and building
- **supply-chain-automation**: Automation technology selection
