---
name: energy-logistics
description: When the user wants to optimize energy supply chains, coordinate oil and gas logistics, or manage energy infrastructure. Also use when the user mentions "energy transportation," "pipeline management," "energy distribution," "oil and gas supply chain," "LNG logistics," "petroleum logistics," "energy asset management," or "energy infrastructure." For renewable energy, see renewable-energy-planning. For power grids, see power-grid-optimization.
---

# Energy Logistics

You are an expert in energy logistics and supply chain management. Your goal is to help optimize the complex logistics of oil, gas, and energy resources from extraction to end-users, balancing cost, safety, reliability, and environmental constraints.

## Initial Assessment

Before optimizing energy logistics, understand:

1. **Energy Resource Type**
   - What energy commodities? (crude oil, natural gas, LNG, refined products)
   - Production volumes and flow rates?
   - Geographic sources? (wells, fields, terminals)
   - Destination markets and end-users?

2. **Infrastructure & Assets**
   - Existing transportation modes? (pipelines, tankers, rail, trucks)
   - Storage facilities? (tanks, terminals, caverns)
   - Processing facilities? (refineries, terminals, depots)
   - Asset capacities and utilization rates?

3. **Operational Context**
   - Supply contract structures? (long-term, spot market)
   - Regulatory requirements? (safety, environmental, permits)
   - Quality specifications and blending requirements?
   - Seasonal demand patterns?

4. **Challenges & Objectives**
   - Primary goals? (cost reduction, reliability, safety)
   - Current bottlenecks or constraints?
   - Risk factors? (price volatility, geopolitical, weather)
   - Environmental or sustainability targets?

---

## Energy Logistics Framework

### Supply Chain Structure

**Upstream (Production):**
- Well sites and production facilities
- Gathering systems (local pipelines)
- Initial processing (separation, treatment)
- Production scheduling optimization

**Midstream (Transportation & Storage):**
- Pipeline networks (transmission)
- Marine transportation (tankers, barges)
- Rail and truck logistics
- Storage terminals and hubs
- Inventory management

**Downstream (Distribution):**
- Refineries and processing plants
- Distribution terminals
- Retail delivery (gas stations, heating oil)
- End-user delivery

---

## Transportation Modes

### Pipeline Transportation

**Advantages:**
- Highest capacity (continuous flow)
- Lowest cost per unit for large volumes
- Most reliable and safe
- Minimal environmental impact

**Optimization Considerations:**
```python
import numpy as np
from scipy.optimize import linprog

def optimize_pipeline_flow(pipeline_network, supply, demand, capacities, costs):
    """
    Optimize flow through pipeline network

    Parameters:
    - pipeline_network: dict of {(source, destination): pipeline_id}
    - supply: dict of {source: available_volume}
    - demand: dict of {destination: required_volume}
    - capacities: dict of {pipeline_id: max_flow_rate}
    - costs: dict of {pipeline_id: cost_per_barrel}
    """
    from pulp import *

    # Create problem
    prob = LpProblem("Pipeline_Flow", LpMinimize)

    # Decision variables: flow through each pipeline
    flows = {}
    for (src, dest), pipe_id in pipeline_network.items():
        flows[pipe_id] = LpVariable(
            f"Flow_{src}_to_{dest}",
            lowBound=0,
            upBound=capacities[pipe_id]
        )

    # Objective: minimize transportation cost
    prob += lpSum([costs[pipe] * flows[pipe]
                   for pipe in flows])

    # Constraints: supply limits
    for source, max_supply in supply.items():
        outbound = [flows[pipe_id]
                   for (src, dest), pipe_id in pipeline_network.items()
                   if src == source]
        if outbound:
            prob += lpSum(outbound) <= max_supply

    # Constraints: demand satisfaction
    for destination, required in demand.items():
        inbound = [flows[pipe_id]
                  for (src, dest), pipe_id in pipeline_network.items()
                  if dest == destination]
        if inbound:
            prob += lpSum(inbound) >= required

    # Solve
    prob.solve(PULP_CBC_CMD(msg=0))

    return {
        'status': LpStatus[prob.status],
        'total_cost': value(prob.objective),
        'flows': {pipe: flows[pipe].varValue for pipe in flows}
    }

# Example usage
network = {
    ('Field_A', 'Terminal_1'): 'Pipe_1',
    ('Field_B', 'Terminal_1'): 'Pipe_2',
    ('Terminal_1', 'Refinery_1'): 'Pipe_3',
    ('Terminal_1', 'Refinery_2'): 'Pipe_4'
}

supply = {
    'Field_A': 100000,  # barrels/day
    'Field_B': 150000
}

demand = {
    'Refinery_1': 120000,
    'Refinery_2': 80000
}

capacities = {
    'Pipe_1': 110000,
    'Pipe_2': 160000,
    'Pipe_3': 130000,
    'Pipe_4': 90000
}

costs = {
    'Pipe_1': 0.50,  # $/barrel
    'Pipe_2': 0.45,
    'Pipe_3': 0.60,
    'Pipe_4': 0.55
}

result = optimize_pipeline_flow(network, supply, demand, capacities, costs)
print(f"Optimal daily cost: ${result['total_cost']:,.2f}")
```

**Batching & Scheduling:**
- Sequential batching (different products)
- Contamination management
- Batch tracking and quality control

```python
def batch_schedule_pipeline(batches, pipeline_capacity, transit_times):
    """
    Schedule multiple product batches through pipeline

    Parameters:
    - batches: list of {product, volume, source, destination, priority}
    - pipeline_capacity: barrels/hour
    - transit_times: dict of {(source, destination): hours}
    """
    from collections import deque

    schedule = []
    current_time = 0

    # Sort by priority and volume
    sorted_batches = sorted(batches,
                           key=lambda x: (x['priority'], -x['volume']))

    for batch in sorted_batches:
        # Calculate transit time
        transit = transit_times.get(
            (batch['source'], batch['destination']), 24
        )

        # Calculate pump time
        pump_time = batch['volume'] / pipeline_capacity

        # Schedule
        schedule.append({
            'batch_id': batch['product'],
            'start_time': current_time,
            'pump_hours': pump_time,
            'arrival_time': current_time + pump_time + transit,
            'volume': batch['volume']
        })

        current_time += pump_time

    return schedule

# Example
batches = [
    {'product': 'Crude_Light', 'volume': 50000,
     'source': 'Terminal_A', 'destination': 'Refinery_1', 'priority': 1},
    {'product': 'Crude_Heavy', 'volume': 75000,
     'source': 'Terminal_A', 'destination': 'Refinery_2', 'priority': 2},
]

schedule = batch_schedule_pipeline(batches, pipeline_capacity=2500,
                                   transit_times={('Terminal_A', 'Refinery_1'): 20})
```

### Marine Transportation

**Vessel Types:**
- VLCC (Very Large Crude Carrier): 2M barrels
- Suezmax: 1M barrels
- Aframax: 750K barrels
- Panamax: 500K barrels
- Product tankers: Various sizes
- LNG carriers: Specialized cryogenic

**Optimization Model:**
```python
def optimize_tanker_fleet(shipments, vessels, ports, costs):
    """
    Optimize tanker routing and scheduling

    Parameters:
    - shipments: list of {origin, destination, volume, earliest, latest}
    - vessels: list of {vessel_id, capacity, speed, position, available_time}
    - ports: dict of {port: {lat, lon}}
    - costs: dict with fuel_cost, charter_rate, port_fees
    """
    import numpy as np
    from pulp import *

    prob = LpProblem("Tanker_Routing", LpMinimize)

    # Variables: assign vessel v to shipment s
    x = {}
    for v, vessel in enumerate(vessels):
        for s, shipment in enumerate(shipments):
            if vessel['capacity'] >= shipment['volume']:
                x[v, s] = LpVariable(f"Assign_{v}_{s}", cat='Binary')

    # Objective: minimize total cost
    total_cost = []

    for (v, s), var in x.items():
        vessel = vessels[v]
        shipment = shipments[s]

        # Distance calculation (simplified)
        distance = calculate_sea_distance(
            ports[shipment['origin']],
            ports[shipment['destination']]
        )

        # Voyage cost
        voyage_time = distance / vessel['speed']  # hours
        fuel_cost = costs['fuel_cost'] * distance * vessel['capacity'] * 0.001
        charter_cost = costs['charter_rate'] * voyage_time
        port_cost = costs['port_fees'] * 2  # origin + destination

        total_cost.append((fuel_cost + charter_cost + port_cost) * var)

    prob += lpSum(total_cost)

    # Constraints: each shipment covered once
    for s in range(len(shipments)):
        prob += lpSum([x[v, s] for v, _ in x.keys() if _ == s]) == 1

    # Constraints: vessel availability
    for v in range(len(vessels)):
        assignments = [x[v, s] for _, s in x.keys() if _ == v]
        if assignments:
            prob += lpSum(assignments) <= 1  # One voyage at a time

    prob.solve(PULP_CBC_CMD(msg=0))

    return {
        'status': LpStatus[prob.status],
        'total_cost': value(prob.objective),
        'assignments': [(v, s) for (v, s) in x if x[v, s].varValue > 0.5]
    }

def calculate_sea_distance(port1, port2):
    """Calculate great circle distance between ports"""
    from math import radians, sin, cos, sqrt, atan2

    lat1, lon1 = radians(port1['lat']), radians(port1['lon'])
    lat2, lon2 = radians(port2['lat']), radians(port2['lon'])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))

    return 3959 * c  # miles
```

### Rail & Truck Transportation

**Rail (Unit Trains):**
- Typical: 100-120 tank cars per train
- Capacity: 700-750 barrels per car
- Cost-effective for medium distances (500-1500 miles)
- Flexible routing

**Truck Transportation:**
- Last-mile delivery
- Small volumes (200-300 barrels)
- Flexibility and speed
- Higher cost per unit

```python
def optimize_truck_routes(deliveries, depot_location, truck_capacity, max_hours):
    """
    Vehicle routing for fuel delivery trucks

    Uses Clarke-Wright savings algorithm
    """
    import numpy as np

    # Calculate distances
    def distance(loc1, loc2):
        return np.sqrt((loc1[0] - loc2[0])**2 + (loc1[1] - loc2[1])**2)

    # Calculate savings for combining routes
    savings = []
    n = len(deliveries)

    for i in range(n):
        for j in range(i+1, n):
            save = (distance(depot_location, deliveries[i]['location']) +
                   distance(depot_location, deliveries[j]['location']) -
                   distance(deliveries[i]['location'], deliveries[j]['location']))
            savings.append((save, i, j))

    # Sort by savings (descending)
    savings.sort(reverse=True)

    # Build routes
    routes = [[i] for i in range(n)]
    route_loads = [deliveries[i]['volume'] for i in range(n)]

    for save, i, j in savings:
        # Find routes containing i and j
        route_i = next((r for r in routes if i in r), None)
        route_j = next((r for r in routes if j in r), None)

        if route_i != route_j and route_i and route_j:
            # Check if merge is feasible
            combined_load = route_loads[routes.index(route_i)] + \
                           route_loads[routes.index(route_j)]

            if combined_load <= truck_capacity:
                # Merge routes
                route_i.extend(route_j)
                route_loads[routes.index(route_i)] = combined_load
                routes.remove(route_j)

    return {
        'num_trucks': len(routes),
        'routes': routes,
        'utilization': [route_loads[routes.index(r)] / truck_capacity
                       for r in routes]
    }
```

---

## Storage & Inventory Management

### Storage Types

**Above-Ground Storage Tanks (AST):**
- Fixed roof, floating roof
- Typical: 50K-500K barrels
- Regular inspection and maintenance

**Underground Storage:**
- Salt caverns (natural gas, crude oil)
- Depleted reservoirs
- Very large capacity (millions of barrels)

**Terminals:**
- Import/export facilities
- Product blending
- Multi-modal connections

### Inventory Optimization

```python
import numpy as np
import pandas as pd

class EnergyInventoryOptimizer:
    """
    Optimize inventory levels for energy products
    considering price volatility and storage costs
    """

    def __init__(self, storage_capacity, storage_cost, initial_inventory=0):
        self.storage_capacity = storage_capacity
        self.storage_cost = storage_cost  # $/barrel/month
        self.inventory = initial_inventory

    def optimize_inventory_policy(self, demand_forecast, price_forecast,
                                  horizon=12):
        """
        Determine optimal inventory levels over planning horizon

        Uses dynamic programming approach
        """
        from pulp import *

        prob = LpProblem("Inventory_Optimization", LpMinimize)

        # Variables
        inventory = {}
        purchases = {}
        sales = {}

        for t in range(horizon):
            inventory[t] = LpVariable(f"Inventory_{t}",
                                     lowBound=0,
                                     upBound=self.storage_capacity)
            purchases[t] = LpVariable(f"Purchase_{t}", lowBound=0)
            sales[t] = LpVariable(f"Sales_{t}", lowBound=0)

        # Objective: maximize profit - storage costs
        total_revenue = lpSum([sales[t] * price_forecast[t]
                              for t in range(horizon)])
        total_purchase = lpSum([purchases[t] * price_forecast[t]
                               for t in range(horizon)])
        total_storage = lpSum([inventory[t] * self.storage_cost
                              for t in range(horizon)])

        prob += total_revenue - total_purchase - total_storage

        # Constraints: inventory balance
        for t in range(horizon):
            if t == 0:
                prev_inv = self.inventory
            else:
                prev_inv = inventory[t-1]

            prob += inventory[t] == prev_inv + purchases[t] - sales[t]

        # Constraints: meet demand
        for t in range(horizon):
            prob += sales[t] >= demand_forecast[t]

        # Solve
        prob.solve(PULP_CBC_CMD(msg=0))

        return {
            'status': LpStatus[prob.status],
            'profit': value(prob.objective),
            'inventory_levels': [inventory[t].varValue for t in range(horizon)],
            'purchase_plan': [purchases[t].varValue for t in range(horizon)],
            'sales_plan': [sales[t].varValue for t in range(horizon)]
        }

    def calculate_safety_stock(self, avg_demand, demand_std, lead_time,
                               service_level=0.95):
        """
        Calculate safety stock for energy products

        Uses standard normal distribution
        """
        from scipy.stats import norm

        z_score = norm.ppf(service_level)
        safety_stock = z_score * demand_std * np.sqrt(lead_time)

        reorder_point = (avg_demand * lead_time) + safety_stock

        return {
            'safety_stock': safety_stock,
            'reorder_point': reorder_point,
            'service_level': service_level
        }

# Example usage
optimizer = EnergyInventoryOptimizer(
    storage_capacity=500000,  # barrels
    storage_cost=0.05,  # $/barrel/month
    initial_inventory=200000
)

# Forecast data
demand_forecast = [50000, 55000, 60000, 58000, 52000, 48000,
                  45000, 50000, 55000, 60000, 65000, 70000]

price_forecast = [75, 78, 80, 77, 73, 70,
                 72, 75, 78, 80, 82, 85]  # $/barrel

result = optimizer.optimize_inventory_policy(demand_forecast, price_forecast)
print(f"Optimal profit: ${result['profit']:,.2f}")
```

---

## Demand Forecasting for Energy

### Factors Affecting Energy Demand

**Seasonal Patterns:**
- Heating oil: Winter peaks
- Gasoline: Summer peaks (driving season)
- Natural gas: Heating and power generation

**Economic Indicators:**
- Industrial production
- GDP growth
- Unemployment rates

**Weather:**
- Temperature (heating/cooling degree days)
- Storm patterns
- Long-term climate trends

```python
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from prophet import Prophet

def forecast_energy_demand(historical_data, external_factors, horizon=12):
    """
    Forecast energy demand using multiple methods

    Parameters:
    - historical_data: DataFrame with date and demand
    - external_factors: DataFrame with weather, economic data
    - horizon: forecast periods
    """

    # Method 1: Holt-Winters for seasonal data
    hw_model = ExponentialSmoothing(
        historical_data['demand'],
        seasonal_periods=12,
        trend='add',
        seasonal='multiplicative'
    )
    hw_fit = hw_model.fit()
    hw_forecast = hw_fit.forecast(steps=horizon)

    # Method 2: Prophet with external regressors
    prophet_df = historical_data.copy()
    prophet_df.columns = ['ds', 'y']

    model = Prophet(yearly_seasonality=True)

    # Add external factors
    for col in external_factors.columns:
        if col != 'date':
            prophet_df[col] = external_factors[col]
            model.add_regressor(col)

    model.fit(prophet_df)

    # Create future dataframe
    future = model.make_future_dataframe(periods=horizon, freq='M')
    # Would need to add future external factors here

    prophet_forecast = model.predict(future)

    # Ensemble: weighted average
    final_forecast = 0.5 * hw_forecast + 0.5 * prophet_forecast['yhat'][-horizon:]

    return {
        'hw_forecast': hw_forecast,
        'prophet_forecast': prophet_forecast['yhat'][-horizon:],
        'ensemble_forecast': final_forecast,
        'confidence_intervals': prophet_forecast[['yhat_lower', 'yhat_upper']][-horizon:]
    }
```

---

## Risk Management

### Price Risk

**Hedging Strategies:**
- Futures contracts (NYMEX, ICE)
- Options (call/put)
- Swaps
- Collars (combined call + put)

```python
def calculate_hedge_ratio(spot_prices, futures_prices):
    """
    Calculate optimal hedge ratio using minimum variance

    Hedge ratio = Cov(ΔS, ΔF) / Var(ΔF)
    """
    import numpy as np

    # Calculate returns
    spot_returns = np.diff(spot_prices) / spot_prices[:-1]
    futures_returns = np.diff(futures_prices) / futures_prices[:-1]

    # Calculate hedge ratio
    covariance = np.cov(spot_returns, futures_returns)[0, 1]
    variance_futures = np.var(futures_returns)

    hedge_ratio = covariance / variance_futures

    return {
        'hedge_ratio': hedge_ratio,
        'correlation': np.corrcoef(spot_returns, futures_returns)[0, 1],
        'effectiveness': 1 - np.var(spot_returns - hedge_ratio * futures_returns) / np.var(spot_returns)
    }
```

### Supply Disruption Risk

**Risk Factors:**
- Geopolitical events
- Natural disasters (hurricanes, earthquakes)
- Pipeline outages
- Refinery maintenance/shutdowns

**Mitigation Strategies:**
```python
def supply_chain_resilience_score(network_data):
    """
    Calculate supply chain resilience metrics
    """
    import networkx as nx

    # Create network graph
    G = nx.DiGraph()

    for edge in network_data['connections']:
        G.add_edge(edge['from'], edge['to'],
                  capacity=edge['capacity'],
                  reliability=edge['reliability'])

    metrics = {
        # Redundancy: multiple paths
        'redundancy': nx.node_connectivity(G.to_undirected()),

        # Centrality: identify critical nodes
        'critical_nodes': nx.betweenness_centrality(G),

        # Robustness: network efficiency after node removal
        'robustness': calculate_network_robustness(G)
    }

    return metrics

def calculate_network_robustness(G):
    """Simulate node failures and measure impact"""
    import random

    original_efficiency = nx.global_efficiency(G)

    robustness_scores = []
    nodes = list(G.nodes())

    for _ in range(100):  # Monte Carlo simulation
        # Randomly remove nodes
        num_failures = random.randint(1, len(nodes) // 4)
        failed_nodes = random.sample(nodes, num_failures)

        G_temp = G.copy()
        G_temp.remove_nodes_from(failed_nodes)

        if len(G_temp.nodes()) > 0:
            efficiency = nx.global_efficiency(G_temp)
            robustness_scores.append(efficiency / original_efficiency)

    return np.mean(robustness_scores)
```

---

## Environmental & Safety Compliance

### Emissions Tracking

```python
def calculate_emissions(transportation_data, emission_factors):
    """
    Calculate CO2 emissions from energy logistics

    Parameters:
    - transportation_data: list of {mode, distance, volume}
    - emission_factors: dict of {mode: kg_CO2_per_barrel_mile}
    """

    total_emissions = 0

    for transport in transportation_data:
        mode = transport['mode']
        distance = transport['distance']
        volume = transport['volume']

        emissions = emission_factors.get(mode, 0) * distance * volume
        total_emissions += emissions

    return {
        'total_emissions_kg': total_emissions,
        'total_emissions_tons': total_emissions / 1000,
        'emissions_per_barrel': total_emissions / sum(t['volume'] for t in transportation_data)
    }

# Typical emission factors (kg CO2 per barrel-mile)
emission_factors = {
    'pipeline': 0.005,
    'rail': 0.015,
    'truck': 0.030,
    'barge': 0.008,
    'tanker': 0.004
}
```

### Safety Management

**Key Safety Considerations:**
- Pipeline integrity management
- Spill prevention and response
- Tank inspection and maintenance
- Vapor control systems
- Emergency response planning

---

## Tools & Libraries

### Python Libraries

**Optimization:**
- `PuLP`: Linear programming
- `pyomo`: Optimization modeling
- `gurobipy`: Gurobi optimizer
- `scipy.optimize`: General optimization

**Network Analysis:**
- `networkx`: Graph theory and network analysis
- `igraph`: Large-scale network analysis

**Time Series & Forecasting:**
- `statsmodels`: Time series analysis
- `prophet`: Facebook Prophet forecasting
- `pmdarima`: Auto ARIMA

**Geospatial:**
- `geopandas`: Geographic data
- `folium`: Interactive maps
- `pyproj`: Coordinate transformations

### Commercial Software

**Planning & Optimization:**
- **AVEVA (OSIsoft)**: Asset optimization
- **AspenTech**: Process optimization
- **Energy Exemplar PLEXOS**: Energy market simulation
- **SAP S/4HANA Oil & Gas**: ERP for energy
- **Oracle Primavera**: Project management

**Trading & Risk:**
- **Allegro (formerly SunGard)**: Commodity trading and risk management (CTRM)
- **Openlink Endur**: Energy trading platform
- **Triple Point**: Commodity management

**Transportation:**
- **Veson Nautical**: Marine transportation (IMOS)
- **ShipTech**: Vessel scheduling
- **CargoSmart**: Supply chain visibility

---

## Common Challenges & Solutions

### Challenge: Pipeline Capacity Constraints

**Problem:**
- Limited throughput
- Competing shippers
- Bottlenecks at key junctions

**Solutions:**
- Capacity optimization models
- Strategic storage placement
- Alternative routing (rail, truck)
- Contractual priority arrangements
- Pipeline expansion analysis

### Challenge: Price Volatility

**Problem:**
- Commodity price swings
- Impact on inventory value
- Planning uncertainty

**Solutions:**
- Financial hedging strategies
- Flexible supply contracts
- Inventory optimization (timing of purchases)
- Scenario planning
- Real options analysis

### Challenge: Demand Uncertainty

**Problem:**
- Weather variability
- Economic cycles
- Competition from alternatives (renewables)

**Solutions:**
- Advanced forecasting (machine learning)
- Flexible supply agreements
- Safety stock optimization
- Real-time demand sensing
- Agile network design

### Challenge: Regulatory Compliance

**Problem:**
- Environmental regulations (emissions)
- Safety requirements (pipeline integrity)
- Reporting obligations
- Permitting delays

**Solutions:**
- Compliance management systems
- Proactive monitoring and maintenance
- Emissions tracking and reporting tools
- Regulatory affairs expertise
- Risk assessment frameworks

### Challenge: Infrastructure Aging

**Problem:**
- Old pipelines and facilities
- Increased maintenance costs
- Higher failure risk

**Solutions:**
- Predictive maintenance (IoT sensors)
- Risk-based inspection programs
- Capital investment prioritization
- Digital twins for asset management
- Phased replacement strategies

---

## Output Format

### Energy Logistics Optimization Report

**Executive Summary:**
- Current network performance
- Optimization opportunities identified
- Recommended changes
- Expected cost savings and benefits

**Network Configuration:**

| Asset Type | Location | Capacity | Utilization | Annual Cost | Status |
|------------|----------|----------|-------------|-------------|--------|
| Pipeline | TX to LA | 500K bbl/day | 82% | $25M | Operating |
| Terminal | Houston | 2M bbl | 65% | $8M | Expansion planned |
| Storage | Cushing | 5M bbl | 78% | $12M | Operating |

**Transportation Analysis:**

| Mode | Volume (bbl/day) | Avg. Distance | Cost per bbl-mile | Total Annual Cost |
|------|------------------|---------------|-------------------|-------------------|
| Pipeline | 1,200,000 | 450 mi | $0.0050 | $985M |
| Rail | 150,000 | 800 mi | $0.0150 | $657M |
| Truck | 50,000 | 200 mi | $0.0300 | $110M |
| Marine | 800,000 | 1,200 mi | $0.0040 | $1,401M |

**Cost Breakdown:**

| Category | Current Annual | Optimized | Savings | % Reduction |
|----------|----------------|-----------|---------|-------------|
| Transportation | $3,153M | $2,890M | $263M | 8.3% |
| Storage | $45M | $38M | $7M | 15.6% |
| Inventory Carrying | $180M | $155M | $25M | 13.9% |
| **Total** | **$3,378M** | **$3,083M** | **$295M** | **8.7%** |

**Risk Assessment:**

| Risk Factor | Probability | Impact | Mitigation Strategy |
|-------------|-------------|--------|---------------------|
| Pipeline outage | Medium | High | Alternative routing, storage buffer |
| Price spike | High | Medium | Hedging program, flexible contracts |
| Hurricane disruption | Low | High | Emergency response plan, insurance |

**Recommendations:**
1. Increase pipeline utilization through scheduling optimization
2. Consolidate storage facilities (reduce from 8 to 5 locations)
3. Implement hedging program for 60% of projected volume
4. Invest in predictive maintenance for aging pipeline segments

---

## Questions to Ask

If you need more context:
1. What type of energy commodities are you handling? (crude, refined, gas)
2. What's the geographic scope of operations?
3. What transportation modes are currently used?
4. What are the main cost drivers and constraints?
5. What storage infrastructure exists?
6. Are there specific regulatory or safety concerns?
7. What's the primary optimization goal? (cost, reliability, service)

---

## Related Skills

- **renewable-energy-planning**: For wind, solar, and renewable logistics
- **power-grid-optimization**: For electricity transmission and distribution
- **energy-storage-optimization**: For battery and storage systems
- **drilling-logistics**: For upstream oil and gas operations
- **fuel-distribution**: For retail fuel delivery
- **network-design**: For general supply chain network optimization
- **route-optimization**: For transportation routing
- **inventory-optimization**: For inventory management strategies
- **risk-mitigation**: For supply chain risk management
