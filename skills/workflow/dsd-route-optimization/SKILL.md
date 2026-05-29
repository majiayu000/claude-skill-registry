---
name: dsd-route-optimization
description: When the user wants to optimize Direct Store Delivery (DSD) routes, plan delivery schedules for retail stores, or improve route efficiency for CPG distribution. Also use when the user mentions "DSD routing," "store delivery optimization," "retail route planning," "delivery windows," "merchandising routes," or "field sales routing." For general vehicle routing, see vehicle-routing-problem. For last-mile delivery, see last-mile-delivery.
---

# DSD Route Optimization

You are an expert in Direct Store Delivery (DSD) route optimization and retail distribution planning. Your goal is to help design efficient delivery routes that minimize costs while meeting strict retail delivery windows, merchandising requirements, and service level commitments.

## Initial Assessment

Before optimizing DSD routes, understand:

1. **Business Context**
   - What products are being delivered? (beverages, snacks, bread, etc.)
   - How many stores/retail locations?
   - How many drivers/vehicles in fleet?
   - What's the current route efficiency (miles/stop, cost/delivery)?
   - What's the service frequency? (daily, 3x/week, on-demand)

2. **Operational Constraints**
   - Delivery time windows by retailer/store?
   - Store receiving hours? (early morning, business hours)
   - Driver shift lengths and overtime rules?
   - Merchandising time at store? (shelving, rotation, display)
   - Unload time requirements?

3. **Vehicle Characteristics**
   - Vehicle types and capacities (cube, weight, pallet positions)?
   - Refrigeration requirements?
   - Vehicle restrictions (height, hazmat)?
   - Equipment (lift gates, hand trucks, dollies)?

4. **Service Requirements**
   - Pre-selling vs. delivery-only routes?
   - Merchandising services (stocking, display building)?
   - Return/swap policies (expired products)?
   - Order minimum/maximum quantities?
   - Must-serve vs. optional stops?

---

## DSD Business Model Characteristics

### What Makes DSD Unique

**vs. Warehouse Delivery:**
- Frequent, small deliveries (multiple times/week)
- Strict delivery windows (early morning for fresh products)
- Driver performs merchandising (not just drop-off)
- Higher service costs but better shelf presence
- Direct relationship between brand and retailer

**Typical Industries:**
- Beverage: Coke, Pepsi, beer distributors
- Bread/bakery: Fresh daily delivery
- Snacks: Frito-Lay, chips, candy
- Dairy: Milk, yogurt, cheese
- Specialty foods: Organic, local products

**Service Patterns:**
- **High-frequency**: 5-7x per week (bread, dairy)
- **Medium-frequency**: 2-4x per week (beverages)
- **Low-frequency**: 1x per week (specialty items)
- **On-demand**: Emergency/promotional orders

---

## DSD Route Optimization Framework

### Route Types

**1. Fixed Routes**
- Same stores, same sequence, same days
- Predictable for drivers and stores
- Easy to plan but may not be optimal
- Best for: High-volume, stable demand

**2. Dynamic Routes**
- Routes optimized daily based on orders
- Maximum efficiency but less predictable
- Requires sophisticated software
- Best for: Variable demand, large networks

**3. Hybrid Routes**
- Core stores on fixed routes
- Flex stores assigned dynamically
- Balance predictability and efficiency
- Most common in practice

**4. Pre-sell Routes**
- Driver visits store day before delivery
- Takes order, stocks shelves on return visit
- Two passes per store per cycle
- Common for snacks, beverages

---

## Mathematical Optimization Model

### Vehicle Routing Problem with Time Windows (VRPTW)

DSD routing is a special case of VRPTW with additional constraints:

**Decision Variables:**
```
x_ijk = 1 if vehicle k travels from store i to store j, 0 otherwise
t_ik = time vehicle k arrives at store i
y_ik = 1 if vehicle k serves store i, 0 otherwise
```

**Objective Function:**
```
Minimize:
  Σ_i Σ_j Σ_k (c_ij * x_ijk)           # Travel costs
  + Σ_k (fixed_cost_k * vehicle_used_k)  # Fixed vehicle costs
  + Σ_i Σ_k (service_time_i * y_ik)    # Service time costs
  + penalty * late_deliveries            # Lateness penalties
```

**Constraints:**
```
1. Each store visited exactly once:
   Σ_k y_ik = 1    ∀ stores i

2. Vehicle capacity (cube and weight):
   Σ_i (demand_i * y_ik) <= capacity_k    ∀ vehicles k

3. Time windows:
   early_i <= t_ik <= late_i    ∀ i, k where y_ik = 1

4. Route continuity (flow conservation):
   Σ_j x_ijk = Σ_j x_jik = y_ik    ∀ i, k

5. Time consistency:
   t_ik + service_time_i + travel_time_ij <= t_jk + M(1 - x_ijk)

6. Driver shift length:
   route_duration_k <= max_shift_k    ∀ k

7. Merchandising time:
   service_time_i = unload_time_i + merchandising_time_i
```

---

## Python Implementation

### Basic DSD Route Optimization

```python
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import numpy as np
import pandas as pd

class DSDRouteOptimizer:
    """DSD route optimization using Google OR-Tools"""

    def __init__(self, stores_df, depot_location, vehicle_config):
        """
        Initialize DSD route optimizer

        Parameters:
        - stores_df: DataFrame with columns ['store_id', 'lat', 'lon',
                     'demand_cube', 'demand_weight', 'time_window_start',
                     'time_window_end', 'service_time', 'merchandising_time']
        - depot_location: dict {'lat': x, 'lon': y}
        - vehicle_config: dict with vehicle parameters
        """
        self.stores = stores_df
        self.depot = depot_location
        self.vehicles = vehicle_config

        # Calculate distance and time matrices
        self.distance_matrix = self._compute_distance_matrix()
        self.time_matrix = self._compute_time_matrix()

    def _compute_distance_matrix(self):
        """Compute distance matrix between all locations"""
        from scipy.spatial.distance import cdist

        # Add depot as first location
        all_locations = pd.concat([
            pd.DataFrame([self.depot]),
            self.stores[['lat', 'lon']]
        ], ignore_index=True)

        # Calculate distances (haversine approximation)
        coords = all_locations.values
        distances = cdist(coords, coords, metric='euclidean') * 69  # miles

        return distances.astype(int)

    def _compute_time_matrix(self, avg_speed_mph=30):
        """Compute travel time matrix in minutes"""
        return (self.distance_matrix / avg_speed_mph * 60).astype(int)

    def optimize_routes(self, num_vehicles=None, max_route_time=480):
        """
        Optimize DSD routes

        Parameters:
        - num_vehicles: number of available vehicles (None = unlimited)
        - max_route_time: maximum route duration in minutes

        Returns:
        - routes: list of optimized routes
        - metrics: route performance metrics
        """

        if num_vehicles is None:
            num_vehicles = len(self.stores)  # Upper bound

        # Create routing model
        manager = pywrapcp.RoutingIndexManager(
            len(self.distance_matrix),
            num_vehicles,
            0  # depot index
        )

        routing = pywrapcp.RoutingModel(manager)

        # Distance callback
        def distance_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return self.distance_matrix[from_node][to_node]

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        # Time windows constraint
        time_windows = [(0, max_route_time)]  # Depot
        for idx, row in self.stores.iterrows():
            time_windows.append((
                int(row['time_window_start']),
                int(row['time_window_end'])
            ))

        def time_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            travel_time = self.time_matrix[from_node][to_node]

            # Add service time at from_node
            if from_node > 0:  # Not depot
                service_time = self.stores.iloc[from_node - 1]['service_time']
                merchandising = self.stores.iloc[from_node - 1]['merchandising_time']
                return int(travel_time + service_time + merchandising)
            return int(travel_time)

        time_callback_index = routing.RegisterTransitCallback(time_callback)

        routing.AddDimension(
            time_callback_index,
            30,  # Allow 30 min waiting time
            max_route_time,  # Maximum route time
            False,  # Don't force start cumul to zero
            'Time'
        )

        time_dimension = routing.GetDimensionOrDie('Time')

        # Add time window constraints for each location
        for location_idx, time_window in enumerate(time_windows):
            if location_idx == 0:  # Skip depot
                continue
            index = manager.NodeToIndex(location_idx)
            time_dimension.CumulVar(index).SetRange(time_window[0], time_window[1])

        # Add depot time window
        for vehicle_id in range(num_vehicles):
            index = routing.Start(vehicle_id)
            time_dimension.CumulVar(index).SetRange(time_windows[0][0],
                                                     time_windows[0][1])

        # Vehicle capacity constraints (cube)
        def demand_callback(from_index):
            from_node = manager.IndexToNode(from_index)
            if from_node == 0:  # Depot
                return 0
            return int(self.stores.iloc[from_node - 1]['demand_cube'])

        demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)

        routing.AddDimensionWithVehicleCapacity(
            demand_callback_index,
            0,  # No slack
            [self.vehicles['capacity_cube']] * num_vehicles,  # Vehicle capacities
            True,  # Start cumul to zero
            'Capacity'
        )

        # Search parameters
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
        )
        search_parameters.local_search_metaheuristic = (
            routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
        )
        search_parameters.time_limit.seconds = 30

        # Solve
        solution = routing.SolveWithParameters(search_parameters)

        if solution:
            return self._extract_solution(manager, routing, solution)
        else:
            return None, None

    def _extract_solution(self, manager, routing, solution):
        """Extract routes and metrics from solution"""

        routes = []
        total_distance = 0
        total_time = 0

        for vehicle_id in range(routing.vehicles()):
            route = []
            route_distance = 0
            route_time = 0

            index = routing.Start(vehicle_id)

            while not routing.IsEnd(index):
                node = manager.IndexToNode(index)

                if node != 0:  # Not depot
                    store = self.stores.iloc[node - 1]
                    route.append({
                        'store_id': store['store_id'],
                        'arrival_time': solution.Value(
                            routing.GetDimensionOrDie('Time').CumulVar(index)
                        ),
                        'demand': store['demand_cube']
                    })

                previous_index = index
                index = solution.Value(routing.NextVar(index))
                route_distance += routing.GetArcCostForVehicle(
                    previous_index, index, vehicle_id
                )

            if route:  # Only include routes with stops
                route_time = solution.Value(
                    routing.GetDimensionOrDie('Time').CumulVar(
                        routing.End(vehicle_id)
                    )
                )

                routes.append({
                    'vehicle_id': vehicle_id + 1,
                    'stops': route,
                    'distance_miles': route_distance,
                    'duration_minutes': route_time,
                    'num_stops': len(route)
                })

                total_distance += route_distance
                total_time += route_time

        metrics = {
            'total_distance': total_distance,
            'total_time': total_time,
            'num_routes': len(routes),
            'avg_stops_per_route': np.mean([r['num_stops'] for r in routes]),
            'avg_distance_per_route': np.mean([r['distance_miles'] for r in routes])
        }

        return routes, metrics


# Example usage
stores = pd.DataFrame({
    'store_id': ['Store_A', 'Store_B', 'Store_C', 'Store_D', 'Store_E'],
    'lat': [34.05, 34.10, 34.15, 34.08, 34.12],
    'lon': [-118.25, -118.30, -118.35, -118.28, -118.33],
    'demand_cube': [50, 75, 60, 45, 80],
    'demand_weight': [200, 300, 240, 180, 320],
    'time_window_start': [360, 420, 480, 390, 450],  # minutes from midnight
    'time_window_end': [480, 540, 600, 510, 570],
    'service_time': [15, 20, 18, 12, 22],  # unload time
    'merchandising_time': [30, 45, 35, 25, 40]  # shelf stocking time
})

depot = {'lat': 34.00, 'lon': -118.20}

vehicle_config = {
    'capacity_cube': 200,
    'capacity_weight': 1000,
    'max_shift_hours': 10
}

optimizer = DSDRouteOptimizer(stores, depot, vehicle_config)
routes, metrics = optimizer.optimize_routes(num_vehicles=3, max_route_time=600)

if routes:
    print(f"Optimized {metrics['num_routes']} routes")
    print(f"Total distance: {metrics['total_distance']} miles")
    print(f"Average stops per route: {metrics['avg_stops_per_route']:.1f}")

    for route in routes:
        print(f"\nVehicle {route['vehicle_id']}: {route['num_stops']} stops, "
              f"{route['distance_miles']} miles, {route['duration_minutes']} min")
        for stop in route['stops']:
            arrival = stop['arrival_time']
            hours = arrival // 60
            mins = arrival % 60
            print(f"  - {stop['store_id']} at {hours:02d}:{mins:02d}, "
                  f"demand: {stop['demand']} cu ft")
```

### Pre-Sell Route Model

```python
class PreSellRouteOptimizer:
    """
    Optimize pre-sell and delivery routes for DSD

    Pre-sell: Driver visits stores to take orders
    Delivery: Driver returns to fulfill orders taken previously
    """

    def __init__(self, stores_df, depot_location):
        self.stores = stores_df
        self.depot = depot_location

    def optimize_presell_delivery(self, presell_days, delivery_days):
        """
        Create coordinated pre-sell and delivery routes

        Parameters:
        - presell_days: days of week for pre-selling (0=Monday)
        - delivery_days: days of week for delivery

        Returns:
        - presell_routes: routes for taking orders
        - delivery_routes: routes for fulfilling orders
        """

        # Pre-sell routes: shorter visits (no unloading)
        presell_stores = self.stores.copy()
        presell_stores['service_time'] = 10  # Quick order-taking
        presell_stores['merchandising_time'] = 5  # Minimal shelf check

        # Optimize pre-sell routes (can visit more stores)
        presell_optimizer = DSDRouteOptimizer(
            presell_stores,
            self.depot,
            {'capacity_cube': 0, 'max_shift_hours': 10}  # No load
        )
        presell_routes, _ = presell_optimizer.optimize_routes()

        # Delivery routes: full service including orders from pre-sell
        delivery_stores = self.stores.copy()
        # Add predicted order quantities from pre-sell
        delivery_stores['demand_cube'] = presell_stores['demand_cube'] * 1.1

        delivery_optimizer = DSDRouteOptimizer(
            delivery_stores,
            self.depot,
            {'capacity_cube': 250, 'max_shift_hours': 10}
        )
        delivery_routes, _ = delivery_optimizer.optimize_routes()

        return presell_routes, delivery_routes
```

---

## DSD-Specific Considerations

### Delivery Time Windows

**Early Morning Delivery:**
```python
def generate_early_delivery_windows():
    """Typical early morning DSD windows"""

    windows = {
        'Grocery_Stores': (300, 420),      # 5:00 AM - 7:00 AM
        'Convenience_Stores': (360, 480),   # 6:00 AM - 8:00 AM
        'Gas_Stations': (300, 540),         # 5:00 AM - 9:00 AM (flexible)
        'Restaurants': (420, 600),          # 7:00 AM - 10:00 AM
        'Schools': (300, 420),              # 5:00 AM - 7:00 AM (before students)
        'Office_Buildings': (420, 540)      # 7:00 AM - 9:00 AM
    }

    return windows

def check_time_window_feasibility(stores, max_route_time=480):
    """Check if time windows are feasible"""

    # Calculate time required for all stops
    total_service_time = stores['service_time'].sum()
    total_merchandising = stores['merchandising_time'].sum()

    # Estimate travel time (simplified)
    avg_distance_between_stops = 5  # miles
    avg_speed = 30  # mph
    travel_time = (len(stores) * avg_distance_between_stops / avg_speed) * 60

    total_time = total_service_time + total_merchandising + travel_time

    return total_time <= max_route_time
```

### Merchandising Requirements

**Service Time Calculation:**
```python
def calculate_merchandising_time(store_type, delivery_volume, service_level):
    """
    Calculate total service time at store

    Parameters:
    - store_type: 'grocery', 'convenience', 'gas_station', etc.
    - delivery_volume: cubic feet or number of cases
    - service_level: 'basic', 'full_service', 'premium'

    Returns:
    - total_time: minutes
    """

    # Base unload time
    unload_time = delivery_volume * 0.5  # 0.5 min per cubic foot

    # Merchandising time by service level
    merchandising_factors = {
        'basic': 1.0,         # Just unload to backroom
        'full_service': 2.0,  # Stock shelves, rotate
        'premium': 3.0        # Stock, rotate, build displays, check inventory
    }

    base_merchandising = {
        'grocery': 30,
        'convenience': 20,
        'gas_station': 15,
        'wholesale': 45,
        'restaurant': 25
    }

    merchandising_time = (
        base_merchandising.get(store_type, 25) *
        merchandising_factors.get(service_level, 1.0)
    )

    total_time = unload_time + merchandising_time

    return total_time

# Example
time_required = calculate_merchandising_time(
    store_type='grocery',
    delivery_volume=75,  # cubic feet
    service_level='full_service'
)
print(f"Service time required: {time_required:.0f} minutes")
```

### Vehicle Loading Sequence

**Load Planning for Route Efficiency:**
```python
def plan_vehicle_loading(route_stops):
    """
    Plan vehicle loading sequence (LIFO for route efficiency)

    Last stop should be loaded first (bottom/front of truck)
    First stop should be loaded last (top/back of truck)
    """

    # Reverse route order for loading
    loading_sequence = route_stops[::-1]

    loading_plan = []

    for idx, stop in enumerate(loading_sequence):
        loading_plan.append({
            'load_position': idx + 1,
            'route_position': len(route_stops) - idx,
            'store_id': stop['store_id'],
            'products': stop['products'],
            'volume': stop['demand_cube'],
            'special_handling': stop.get('refrigerated', False)
        })

    return loading_plan

def optimize_truck_load(stops, vehicle_config):
    """
    Optimize truck loading considering weight distribution
    """

    from ortools.linear_solver import pywraplp

    solver = pywraplp.Solver.CreateSolver('SCIP')

    # Zones in truck: front, middle, back
    zones = ['front', 'middle', 'back']

    # Variables: which stop's products go in which zone
    x = {}
    for stop_idx, stop in enumerate(stops):
        for zone in zones:
            x[stop_idx, zone] = solver.BoolVar(f'stop_{stop_idx}_{zone}')

    # Objective: minimize rehandling (LIFO loading)
    objective = solver.Objective()
    for stop_idx, stop in enumerate(stops):
        route_position = stop['route_position']
        # Earlier stops should be in back/top
        objective.SetCoefficient(x[stop_idx, 'back'], route_position)
        objective.SetCoefficient(x[stop_idx, 'middle'], route_position * 1.5)
        objective.SetCoefficient(x[stop_idx, 'front'], route_position * 2)

    objective.SetMinimization()

    # Constraints: each stop assigned to exactly one zone
    for stop_idx in range(len(stops)):
        solver.Add(sum(x[stop_idx, zone] for zone in zones) == 1)

    # Capacity constraints per zone
    for zone in zones:
        solver.Add(
            sum(x[stop_idx, zone] * stops[stop_idx]['volume']
                for stop_idx in range(len(stops)))
            <= vehicle_config['zone_capacity'][zone]
        )

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        loading_plan = []
        for stop_idx, stop in enumerate(stops):
            for zone in zones:
                if x[stop_idx, zone].solution_value() > 0.5:
                    loading_plan.append({
                        'stop': stop['store_id'],
                        'zone': zone,
                        'route_position': stop['route_position']
                    })
        return loading_plan

    return None
```

---

## Route Performance Metrics

### Key Performance Indicators

**Efficiency Metrics:**
```python
def calculate_dsd_metrics(routes_df, stores_df, costs):
    """
    Calculate comprehensive DSD route metrics

    Parameters:
    - routes_df: DataFrame with route details
    - stores_df: DataFrame with store information
    - costs: dict with cost parameters
    """

    metrics = {}

    # Miles per stop
    metrics['miles_per_stop'] = (
        routes_df['total_miles'].sum() / routes_df['num_stops'].sum()
    )

    # Stops per route
    metrics['stops_per_route'] = routes_df['num_stops'].mean()

    # Cases per mile
    metrics['cases_per_mile'] = (
        routes_df['total_cases'].sum() / routes_df['total_miles'].sum()
    )

    # Cost per delivery
    fixed_cost_per_route = costs['driver_cost'] + costs['vehicle_cost']
    variable_cost = routes_df['total_miles'].sum() * costs['cost_per_mile']
    total_deliveries = routes_df['num_stops'].sum()

    metrics['cost_per_delivery'] = (
        (fixed_cost_per_route * len(routes_df) + variable_cost) /
        total_deliveries
    )

    # Service time percentage
    total_route_time = routes_df['total_time'].sum()
    total_service_time = routes_df['service_time'].sum()

    metrics['service_time_pct'] = (total_service_time / total_route_time) * 100
    metrics['drive_time_pct'] = 100 - metrics['service_time_pct']

    # On-time performance
    metrics['on_time_pct'] = (
        routes_df['on_time_deliveries'].sum() / total_deliveries * 100
    )

    # Utilization
    metrics['cube_utilization'] = (
        routes_df['loaded_cube'].mean() / routes_df['vehicle_capacity'].mean() * 100
    )

    return metrics

# Benchmark targets
benchmarks = {
    'miles_per_stop': {'best': 2.5, 'good': 3.5, 'acceptable': 5.0},
    'stops_per_route': {'best': 25, 'good': 20, 'acceptable': 15},
    'cases_per_mile': {'best': 50, 'good': 40, 'acceptable': 30},
    'cost_per_delivery': {'best': 15, 'good': 20, 'acceptable': 25},
    'on_time_pct': {'best': 98, 'good': 95, 'acceptable': 90},
    'cube_utilization': {'best': 85, 'good': 75, 'acceptable': 65}
}
```

---

## Advanced DSD Strategies

### Store Clustering and Zoning

```python
from sklearn.cluster import KMeans
import numpy as np

def create_delivery_zones(stores_df, num_zones=5):
    """
    Create geographic zones for route planning

    Parameters:
    - stores_df: DataFrame with store locations
    - num_zones: number of zones to create

    Returns:
    - stores_df with 'zone' assignment
    """

    # Extract coordinates
    coords = stores_df[['lat', 'lon']].values

    # K-means clustering
    kmeans = KMeans(n_clusters=num_zones, random_state=42)
    stores_df['zone'] = kmeans.fit_predict(coords)

    # Calculate zone characteristics
    zone_stats = stores_df.groupby('zone').agg({
        'store_id': 'count',
        'demand_cube': 'sum',
        'lat': 'mean',
        'lon': 'mean'
    }).rename(columns={'store_id': 'num_stores'})

    return stores_df, zone_stats

def assign_stores_to_days(stores_df, delivery_frequency):
    """
    Assign stores to delivery days based on frequency

    Parameters:
    - stores_df: stores with zone assignments
    - delivery_frequency: dict {store_id: frequency} where frequency in [1,2,3,5,7]

    Returns:
    - delivery_schedule: which stores on which days
    """

    days_of_week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
    schedule = {day: [] for day in days_of_week}

    for idx, store in stores_df.iterrows():
        store_id = store['store_id']
        freq = delivery_frequency.get(store_id, 1)  # Default: once per week

        if freq == 5:  # Daily
            for day in days_of_week:
                schedule[day].append(store_id)

        elif freq == 3:  # 3x per week (Mon, Wed, Fri)
            for day in ['Mon', 'Wed', 'Fri']:
                schedule[day].append(store_id)

        elif freq == 2:  # 2x per week (Tue, Thu)
            for day in ['Tue', 'Thu']:
                schedule[day].append(store_id)

        elif freq == 1:  # Once per week
            # Assign to day with least stores in same zone
            zone = store['zone']
            zone_counts = {
                day: sum(1 for s in schedule[day]
                        if stores_df[stores_df['store_id']==s]['zone'].iloc[0]==zone)
                for day in days_of_week
            }
            min_day = min(zone_counts, key=zone_counts.get)
            schedule[min_day].append(store_id)

    return schedule
```

### Dynamic Routing for Variable Demand

```python
class DynamicDSDRouter:
    """
    Dynamic daily routing based on actual orders
    """

    def __init__(self, stores_master, depot, vehicles):
        self.stores_master = stores_master
        self.depot = depot
        self.vehicles = vehicles
        self.historical_routes = []

    def generate_daily_routes(self, orders_today):
        """
        Generate routes based on today's actual orders

        Parameters:
        - orders_today: DataFrame with today's orders by store

        Returns:
        - optimized routes for today
        """

        # Filter to stores with orders today
        stores_today = self.stores_master[
            self.stores_master['store_id'].isin(orders_today['store_id'])
        ].copy()

        # Update demand from orders
        stores_today = stores_today.merge(
            orders_today[['store_id', 'order_cube', 'order_weight']],
            on='store_id'
        )
        stores_today['demand_cube'] = stores_today['order_cube']
        stores_today['demand_weight'] = stores_today['order_weight']

        # Optimize routes
        optimizer = DSDRouteOptimizer(stores_today, self.depot, self.vehicles)
        routes, metrics = optimizer.optimize_routes()

        # Store for learning
        self.historical_routes.append({
            'date': pd.Timestamp.today(),
            'routes': routes,
            'metrics': metrics
        })

        return routes, metrics

    def predict_tomorrow_demand(self):
        """
        Predict tomorrow's demand based on historical patterns
        """

        if len(self.historical_routes) < 7:
            # Not enough history, use average
            return self.stores_master['demand_cube'].mean()

        # Get same day of week from history
        tomorrow_dow = (pd.Timestamp.today() + pd.Timedelta(days=1)).dayofweek

        historical_same_dow = [
            r for r in self.historical_routes
            if r['date'].dayofweek == tomorrow_dow
        ]

        # Average demand from same day of week
        avg_demand_by_store = {}
        for store_id in self.stores_master['store_id']:
            demands = []
            for hist in historical_same_dow[-4:]:  # Last 4 weeks
                for route in hist['routes']:
                    for stop in route['stops']:
                        if stop['store_id'] == store_id:
                            demands.append(stop['demand'])

            if demands:
                avg_demand_by_store[store_id] = np.mean(demands)

        return avg_demand_by_store
```

---

## Tools & Libraries

### Routing Software

**Commercial:**
- **Descartes Route Planner**: DSD-specific routing with merchandising
- **Paragon Routing**: Multi-depot DSD optimization
- **Omnitracs Roadnet**: Fleet routing and mobile dispatch
- **Verizon Networkfleet**: GPS and route optimization
- **WorkWave Route Manager**: Cloud-based DSD routing
- **OptimoRoute**: Simple DSD route planning
- **Routific**: Small fleet routing
- **Route4Me**: Multi-stop route optimization

**Open Source:**
- **OR-Tools (Google)**: Vehicle routing library (Python, C++)
- **VROOM**: Open-source vehicle routing engine
- **GraphHopper**: Routing with real road networks
- **OSRM**: Open Source Routing Machine
- **Jsprit**: Java-based VRP solver

### Python Libraries

```python
# Key libraries for DSD routing

# Optimization
from ortools.constraint_solver import routing_enums_pb2, pywrapcp
import pulp
import pyomo.environ as pyo

# Geospatial
import geopandas as gpd
from shapely.geometry import Point
from scipy.spatial.distance import cdist

# Routing with real roads
import osmnx as ox
import networkx as nx

# Visualization
import folium
import plotly.express as px
import matplotlib.pyplot as plt

# Data processing
import pandas as pd
import numpy as np
```

### Route Visualization

```python
def visualize_routes(routes, stores_df, depot, output_file='routes_map.html'):
    """
    Create interactive map of routes
    """
    import folium
    from folium import plugins

    # Create map centered on depot
    m = folium.Map(
        location=[depot['lat'], depot['lon']],
        zoom_start=11,
        tiles='OpenStreetMap'
    )

    # Add depot
    folium.Marker(
        [depot['lat'], depot['lon']],
        popup='Depot',
        icon=folium.Icon(color='red', icon='home')
    ).add_to(m)

    # Colors for different routes
    colors = ['blue', 'green', 'purple', 'orange', 'darkred',
              'lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue']

    for idx, route in enumerate(routes):
        color = colors[idx % len(colors)]

        # Add route line
        route_coords = [[depot['lat'], depot['lon']]]

        for stop in route['stops']:
            store = stores_df[stores_df['store_id'] == stop['store_id']].iloc[0]
            lat, lon = store['lat'], store['lon']

            route_coords.append([lat, lon])

            # Add store marker
            folium.Marker(
                [lat, lon],
                popup=f"{stop['store_id']}<br>Arrival: {stop['arrival_time']} min",
                icon=folium.Icon(color=color, icon='shopping-cart')
            ).add_to(m)

        route_coords.append([depot['lat'], depot['lon']])

        # Draw route line
        folium.PolyLine(
            route_coords,
            color=color,
            weight=3,
            opacity=0.7,
            popup=f"Route {route['vehicle_id']}: {route['num_stops']} stops"
        ).add_to(m)

    # Add legend
    legend_html = f'''
    <div style="position: fixed;
                bottom: 50px; left: 50px; width: 220px; height: auto;
                background-color: white; border:2px solid grey; z-index:9999;
                font-size:14px; padding: 10px">
    <p><b>Routes Summary</b></p>
    <p>Total Routes: {len(routes)}</p>
    <p>Total Stops: {sum(r['num_stops'] for r in routes)}</p>
    <p>Total Miles: {sum(r['distance_miles'] for r in routes):.0f}</p>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))

    m.save(output_file)
    return m
```

---

## Common Challenges & Solutions

### Challenge: Tight Delivery Windows

**Problem:**
- Stores require 6:00-7:00 AM delivery only
- Multiple stores, limited time
- High penalty for late delivery

**Solutions:**
- Stagger start times for multiple vehicles
- Pre-stage trucks night before
- Negotiate wider windows with retailers
- Use time window relaxation in optimization
- Add early morning shift premium pay

```python
def optimize_with_staggered_starts(stores, depot, vehicles):
    """
    Stagger vehicle start times to meet tight windows
    """

    # Sort stores by window start time
    stores_sorted = stores.sort_values('time_window_start')

    routes = []
    start_time = stores_sorted['time_window_start'].min()

    for vehicle_id in range(vehicles['count']):
        # Assign stores that can be served by this start time
        vehicle_stores = stores_sorted.iloc[
            vehicle_id::vehicles['count']
        ]

        # Optimize route for this vehicle
        optimizer = DSDRouteOptimizer(
            vehicle_stores,
            depot,
            vehicles
        )
        route, _ = optimizer.optimize_routes(num_vehicles=1)

        if route:
            route[0]['start_time'] = start_time + (vehicle_id * 15)  # 15 min stagger
            routes.append(route[0])

    return routes
```

### Challenge: Merchandising Time Variability

**Problem:**
- Planned 20 min, actually takes 40 min
- Routes get delayed, late deliveries
- Overtime costs increase

**Solutions:**
- Track actual times by store and driver
- Build buffer time into schedules
- Separate merchandising from delivery
- Use time-motion studies
- Set realistic service time standards

```python
def calibrate_service_times(actual_times_df):
    """
    Calibrate service times based on actual performance

    Parameters:
    - actual_times_df: historical data with planned vs actual times

    Returns:
    - calibrated service times by store type
    """

    calibration = actual_times_df.groupby('store_type').agg({
        'planned_time': 'mean',
        'actual_time': 'mean',
        'actual_time': 'std'
    })

    # Add buffer (mean + 1 std dev for 84% confidence)
    calibration['recommended_time'] = (
        calibration['actual_time'].mean() +
        calibration['actual_time'].std()
    )

    # Calculate variance factor
    calibration['variance_factor'] = (
        calibration['actual_time'].mean() /
        calibration['planned_time'].mean()
    )

    return calibration
```

### Challenge: Mixed Frequency Deliveries

**Problem:**
- Some stores need daily, others weekly
- Hard to balance route density
- Inefficient routes on low-volume days

**Solutions:**
- Zone-based routing with frequency tiers
- Combine high-frequency stores in dedicated routes
- Use dynamic routing for low-frequency
- Consider 3PL for sparse areas

### Challenge: Returns and Swaps

**Problem:**
- Need to pick up expired product
- Reduces delivery capacity
- Complicates route optimization

**Solutions:**
- Model as pickup-delivery problem
- Reserve capacity for returns
- Separate returns vehicle
- Incentivize stores to minimize returns

```python
def model_with_returns(stores, return_rates):
    """
    Adjust capacity for return pickups

    Parameters:
    - stores: store data
    - return_rates: dict {store_id: pct_returns}

    Returns:
    - adjusted capacity requirements
    """

    for idx, store in stores.iterrows():
        store_id = store['store_id']
        delivery = store['demand_cube']

        # Estimate returns
        return_rate = return_rates.get(store_id, 0.05)  # Default 5%
        returns = delivery * return_rate

        # Net capacity needed (can use return space after pickup)
        # But need space for returns until picked up
        stores.at[idx, 'capacity_needed'] = delivery
        stores.at[idx, 'returns_expected'] = returns

    return stores
```

### Challenge: Driver Familiarity and Route Changes

**Problem:**
- Optimized routes different from driver's usual route
- Driver knows best route from experience
- Resistance to change

**Solutions:**
- Involve drivers in route design
- Gradual implementation of changes
- Allow driver input/overrides
- Track performance to show improvements
- Incentivize efficiency (bonus for miles saved)

---

## Output Format

### DSD Route Plan Report

**Executive Summary:**
- Total routes: 12
- Total stops: 245
- Total miles: 1,850
- Avg stops per route: 20.4
- Avg miles per stop: 7.6
- Estimated cost: $4,500
- Service level: 97% on-time

**Route Details:**

```
Route 1 - Driver: John Smith - Vehicle: T-101
Departure: 5:30 AM
Estimated Duration: 8.5 hours
Total Miles: 175
Total Stops: 24
Total Cases: 480

Stop  Store ID      Arrival   Service    Departure  Cases  Running Load
----  -----------   -------   -------    ---------  -----  ------------
  1   Store_A       6:15 AM   35 min     6:50 AM    25     25/480
  2   Store_B       7:05 AM   25 min     7:30 AM    18     43/480
  3   Store_C       7:50 AM   40 min     8:30 AM    32     75/480
  ...

Return to Depot: 3:15 PM
```

**Performance Metrics:**

| Metric | Value | Benchmark | Status |
|--------|-------|-----------|--------|
| Miles per Stop | 7.6 | < 8.0 | ✓ Good |
| Stops per Route | 20.4 | > 18 | ✓ Good |
| Cost per Delivery | $18.37 | < $20 | ✓ Good |
| Cube Utilization | 78% | > 75% | ✓ Good |
| On-Time % | 97% | > 95% | ✓ Good |

**Zone Coverage:**

| Zone | Routes | Stops | Miles | Avg Density |
|------|--------|-------|-------|-------------|
| North | 3 | 65 | 425 | 21.7 stops/route |
| South | 4 | 88 | 520 | 22.0 stops/route |
| East | 3 | 55 | 480 | 18.3 stops/route |
| West | 2 | 37 | 425 | 18.5 stops/route |

**Recommendations:**
1. Consider combining East and West zones on Tuesday/Thursday (lower volume days)
2. Store_X consistently requires 50 min service time (planned 30 min) - update standard
3. Zone North has opportunity for one additional route to improve density
4. Three stores with late deliveries: Store_M, Store_P, Store_Q - recommend earlier start time

---

## Questions to Ask

If you need more context:
1. What products are being delivered? Refrigerated? Mixed loads?
2. How many stores and what's the service frequency per store?
3. What are the typical delivery windows? Early morning?
4. Do drivers perform merchandising? How long at each store?
5. What's the current performance? (miles/stop, cost/delivery, on-time %)
6. Vehicle types and capacities?
7. Pre-sell or delivery-only model?
8. Any hard constraints? (union rules, must-serve stores, etc.)

---

## Related Skills

- **vehicle-routing-problem**: For general VRP algorithms and techniques
- **vrp-time-windows**: For detailed time window constraint modeling
- **last-mile-delivery**: For urban delivery optimization
- **fleet-management**: For vehicle and driver management
- **route-optimization**: For general routing strategies
- **promotional-planning**: For handling promotional volume spikes in DSD
- **retail-replenishment**: For coordinating DSD with store inventory
- **warehouse-design**: For DSD depot layout and loading optimization
- **capacity-planning**: For fleet sizing and resource planning
