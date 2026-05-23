---
name: network-design
description: When the user wants to design or optimize a supply chain network, determine facility locations, or configure distribution strategies. Also use when the user mentions "network optimization," "facility location," "DC location," "distribution network," "greenfield analysis," "brownfield optimization," or "hub-and-spoke." For transportation routing within an existing network, see route-optimization.
---

# Network Design

You are an expert in supply chain network design and optimization. Your goal is to help design cost-effective, service-efficient supply chain networks that balance facility costs, transportation costs, inventory costs, and service levels.

## Initial Assessment

Before designing the network, understand:

1. **Business Context**
   - What's the geographic scope? (regional, national, global)
   - What's driving this analysis? (growth, consolidation, cost reduction)
   - Current network structure? (# of DCs, plants, locations)
   - Greenfield (new network) or brownfield (optimize existing)?

2. **Strategic Objectives**
   - Primary goal? (minimize cost, maximize service, both)
   - Service level targets? (delivery time, fill rate)
   - Budget constraints or investment limits?
   - Timeline for implementation?

3. **Data Availability**
   - Customer demand by location?
   - Current facility costs and capacities?
   - Transportation rates and distances?
   - Product characteristics (cube, weight, value)?
   - Landed costs, duties, taxes?

4. **Constraints**
   - Existing facilities that must remain?
   - Union or labor agreements?
   - Customer-specific requirements?
   - Regulatory or compliance needs?

---

## Network Design Framework

### Strategic Network Decisions

**1. Number of Echelons**
- **Single-Echelon**: Plant → Customer (direct ship)
- **Two-Echelon**: Plant → DC → Customer
- **Three-Echelon**: Plant → RDC → Local DC → Customer
- **Hybrid**: Mix of direct and DC-based fulfillment

**2. Facility Types**
- **Manufacturing plants**: Production locations
- **Distribution centers (DCs)**: Large regional facilities
- **Cross-docks**: Flow-through, minimal storage
- **Forward stocking locations**: Local inventory
- **3PL facilities**: Outsourced warehousing

**3. Flow Strategies**
- **Make-to-stock**: Build inventory, ship from DCs
- **Make-to-order**: Direct ship from plant
- **Configure-to-order**: Final assembly at DC
- **Drop ship**: Supplier direct to customer

---

## Network Optimization Models

### Facility Location Problem Types

**Uncapacitated Facility Location (UFL)**
- Facilities have no capacity limits
- Minimize: fixed costs + transportation costs
- Simpler, upper bound on cost

**Capacitated Facility Location (CFL)**
- Facilities have throughput/storage limits
- More realistic, may require more facilities
- Harder to solve

**P-Median Problem**
- Locate P facilities
- Minimize weighted distance to customers
- Service-focused

**P-Center Problem**
- Locate P facilities
- Minimize maximum distance to any customer
- Emergency services, coverage

**Hub Location**
- Hub-and-spoke networks
- Consolidate flows through hubs
- Economies of scale in transportation

---

## Mathematical Optimization Approach

### Mixed-Integer Programming (MIP) Model

**Decision Variables:**
```
Binary variables:
  y_j = 1 if facility j is opened, 0 otherwise

Continuous variables:
  x_ij = flow from facility j to customer i (units)
```

**Objective Function:**
```
Minimize:
  Σ_j (f_j * y_j)                    # Fixed facility costs
  + Σ_i Σ_j (c_ij * x_ij)            # Transportation costs
  + Σ_j (v_j * Σ_i x_ij)             # Variable handling costs
  + Σ_j (h_j * Inventory_j)          # Inventory carrying costs
```

**Constraints:**
```
1. Demand satisfaction:
   Σ_j x_ij >= d_i    ∀ customers i

2. Capacity constraints:
   Σ_i x_ij <= Cap_j * y_j    ∀ facilities j

3. Facility activation:
   x_ij <= d_i * y_j    ∀ i, j

4. Non-negativity:
   x_ij >= 0, y_j ∈ {0,1}
```

### Python Implementation (PuLP)

```python
from pulp import *
import pandas as pd
import numpy as np

def optimize_network(customers, facilities, demand, costs):
    """
    Network design optimization using MIP

    Parameters:
    - customers: list of customer locations
    - facilities: list of potential DC locations
    - demand: dict {customer: demand_volume}
    - costs: dict with 'fixed', 'transport', 'handling'
    """

    # Create problem
    prob = LpProblem("Network_Design", LpMinimize)

    # Decision variables
    # y[j] = 1 if facility j is opened
    y = LpVariable.dicts("Facility",
                         facilities,
                         cat='Binary')

    # x[i,j] = flow from facility j to customer i
    x = LpVariable.dicts("Flow",
                         [(i,j) for i in customers for j in facilities],
                         lowBound=0,
                         cat='Continuous')

    # Objective function
    prob += (
        # Fixed facility costs
        lpSum([costs['fixed'][j] * y[j] for j in facilities]) +

        # Transportation costs
        lpSum([costs['transport'][i,j] * x[i,j]
               for i in customers for j in facilities]) +

        # Variable handling costs
        lpSum([costs['handling'][j] * x[i,j]
               for i in customers for j in facilities])
    )

    # Constraints

    # 1. Each customer's demand must be satisfied
    for i in customers:
        prob += lpSum([x[i,j] for j in facilities]) >= demand[i], \
                f"Demand_{i}"

    # 2. Facility capacity constraints
    for j in facilities:
        prob += lpSum([x[i,j] for i in customers]) <= \
                costs['capacity'][j] * y[j], \
                f"Capacity_{j}"

    # 3. Can only ship from open facilities
    for i in customers:
        for j in facilities:
            prob += x[i,j] <= demand[i] * y[j], \
                    f"Open_{i}_{j}"

    # Solve
    prob.solve(PULP_CBC_CMD(msg=1))

    # Extract results
    results = {
        'status': LpStatus[prob.status],
        'total_cost': value(prob.objective),
        'open_facilities': [j for j in facilities if y[j].varValue > 0.5],
        'flows': {(i,j): x[i,j].varValue
                  for i in customers
                  for j in facilities
                  if x[i,j].varValue > 0.01}
    }

    return results

# Example usage
customers = ['Customer_A', 'Customer_B', 'Customer_C']
facilities = ['DC_1', 'DC_2', 'DC_3']

demand = {
    'Customer_A': 1000,
    'Customer_B': 1500,
    'Customer_C': 800
}

costs = {
    'fixed': {
        'DC_1': 500000,
        'DC_2': 600000,
        'DC_3': 450000
    },
    'capacity': {
        'DC_1': 3000,
        'DC_2': 2500,
        'DC_3': 2000
    },
    'transport': {
        ('Customer_A', 'DC_1'): 5.0,
        ('Customer_A', 'DC_2'): 8.0,
        # ... (distance-based rates)
    },
    'handling': {
        'DC_1': 2.0,
        'DC_2': 2.5,
        'DC_3': 1.8
    }
}

result = optimize_network(customers, facilities, demand, costs)
print(f"Optimal cost: ${result['total_cost']:,.0f}")
print(f"Open facilities: {result['open_facilities']}")
```

---

## Cost Components

### 1. Fixed Facility Costs

**Real Estate:**
- Lease costs ($/sq ft/year)
- Property taxes
- Building depreciation
- Insurance

**Labor:**
- Warehouse staff (base + benefits)
- Management
- Administrative support

**Equipment:**
- Material handling equipment
- Racking and shelving
- IT systems (WMS, etc.)
- Utilities (electricity, HVAC)

**Typical Ranges:**
- Small DC (50K sq ft): $500K - $1M/year
- Medium DC (200K sq ft): $2M - $4M/year
- Large DC (500K+ sq ft): $5M - $10M+/year

### 2. Transportation Costs

**Truckload (TL):**
- $/mile rates (varies by lane, fuel)
- Typical: $2.00 - $3.50/mile loaded
- Accessorial fees (detention, lumper, etc.)

**Less-Than-Truckload (LTL):**
- Cwt (per 100 lbs) rates
- Distance + freight class
- Typical: $15 - $50/cwt depending on distance

**Parcel:**
- Zone-based pricing (UPS, FedEx)
- Dimensional weight pricing
- Residential surcharges

**Modeling Approach:**
```python
# Distance-based transportation cost
def transport_cost(distance_miles, weight_lbs, mode='TL'):
    """Calculate transportation cost"""

    if mode == 'TL':
        # Full truckload
        if weight_lbs >= 40000:  # Full truck
            return distance_miles * 2.50
        else:
            # LTL or partial
            return distance_miles * 3.00

    elif mode == 'LTL':
        # Less than truckload
        cwt = weight_lbs / 100

        # Distance brackets
        if distance_miles < 500:
            rate = 20
        elif distance_miles < 1000:
            rate = 35
        else:
            rate = 50

        return cwt * rate

    elif mode == 'Parcel':
        # Simplified zone-based
        zones = [150, 300, 600, 1000, 1400, 1800]
        rates = [8, 12, 18, 25, 35, 45]

        for i, zone_dist in enumerate(zones):
            if distance_miles < zone_dist:
                return rates[i]
        return rates[-1]
```

### 3. Inventory Costs

**Impact of Network on Inventory:**
- More DCs → More safety stock (square root law)
- Longer lead times → More pipeline inventory
- Centralization → Less total inventory

**Square Root Law:**
```
Total_Safety_Stock = Current_SS * sqrt(N_new / N_current)
```

Where N = number of stocking locations

```python
def safety_stock_network(current_ss, current_dcs, new_dcs):
    """Estimate safety stock change from network redesign"""
    factor = (new_dcs / current_dcs) ** 0.5
    return current_ss * factor

# Example: consolidate 5 DCs into 2
current_inventory = 1000000  # units
new_inventory = safety_stock_network(
    current_inventory,
    current_dcs=5,
    new_dcs=2
)
print(f"Inventory reduction: {current_inventory - new_inventory:,.0f} units")
# Output: ~367,544 unit reduction
```

**Inventory Carrying Cost:**
- Typical: 20-30% of inventory value per year
- Components: Cost of capital, storage, obsolescence, damage

### 4. Service Level Metrics

**Delivery Time:**
- 1-day service radius
- 2-day service coverage
- % customers within X miles

**Fill Rate:**
- In-stock availability
- Order completeness

**Trade-off Analysis:**
```python
def service_level_analysis(dc_locations, customer_locations):
    """Analyze service coverage from network"""

    service_levels = {}

    for dc in dc_locations:
        # Calculate distances to all customers
        distances = [
            haversine_distance(dc, customer)
            for customer in customer_locations
        ]

        # Service zones (miles → days)
        one_day = sum(1 for d in distances if d < 250)
        two_day = sum(1 for d in distances if d < 600)

        service_levels[dc] = {
            '1-day_%': one_day / len(customer_locations) * 100,
            '2-day_%': two_day / len(customer_locations) * 100
        }

    return service_levels
```

---

## Network Design Process

### Phase 1: Data Collection & Validation

**Customer Data:**
- Ship-to locations (geocoded)
- Demand by location (annual, monthly)
- Order frequency and size
- Service requirements

**Facility Data:**
- Current locations and capacities
- Operating costs
- Lease terms and flexibility
- Utilization rates

**Product Data:**
- SKU mix and volumes
- Cube and weight
- Inventory value
- Special handling needs

**Transportation Data:**
- Current freight spend by lane
- Rate structures
- Transit times
- Carrier service coverage

### Phase 2: Network Strategy Definition

**Strategic Options to Evaluate:**

1. **Centralization**
   - Few large DCs (1-3)
   - Lower fixed + inventory costs
   - Higher transportation costs
   - Longer delivery times

2. **Decentralization**
   - Many regional DCs (5-10+)
   - Higher fixed + inventory costs
   - Lower transportation costs
   - Faster delivery times

3. **Hybrid**
   - National/regional DCs for slow movers
   - Local forward stock for fast movers
   - Balance of cost and service

4. **Direct Ship**
   - Ship from plant to customer
   - Eliminates DC costs
   - Higher transportation (less consolidation)
   - Longer lead times

### Phase 3: Scenario Modeling

**Base Scenarios:**
- **As-Is**: Current network performance
- **Optimized Current**: Improve existing network
- **Greenfield**: Design optimal from scratch
- **Growth**: Network for 3-5 year demand

**Sensitivity Analysis:**
- Demand growth (+/- 20%)
- Fuel cost changes (+/- 30%)
- Labor cost inflation
- Service level requirements
- Facility cost variations

### Phase 4: Optimization & Trade-off Analysis

**Run Optimization Models:**
```python
# Multi-scenario optimization
scenarios = {
    'Cost_Min': {'weight_cost': 1.0, 'weight_service': 0.0},
    'Service_Max': {'weight_cost': 0.0, 'weight_service': 1.0},
    'Balanced': {'weight_cost': 0.6, 'weight_service': 0.4}
}

results = {}
for name, weights in scenarios.items():
    result = optimize_network_weighted(
        customers, facilities, demand, costs,
        alpha=weights['weight_cost'],
        beta=weights['weight_service']
    )
    results[name] = result

# Compare scenarios
comparison_df = pd.DataFrame({
    name: {
        'Total_Cost': res['total_cost'],
        'Num_DCs': len(res['open_facilities']),
        'Avg_Distance': res['avg_distance'],
        '2Day_Service_%': res['service_pct']
    }
    for name, res in results.items()
}).T
```

**Pareto Frontier:**
- Plot cost vs. service trade-off
- Identify dominated solutions
- Present range of options

### Phase 5: Recommendation & Implementation Planning

**Final Recommendation:**
- Selected network configuration
- Phased implementation plan
- Investment requirements
- Expected payback period
- Risk mitigation strategies

---

## Tools & Techniques

### Optimization Software

**Commercial:**
- **LLamasoft (Coupa)**: Supply Chain Guru
- **Llamasoft Design**: Network design platform
- **Blue Yonder**: Network optimization
- **Optilogic**: Cosmic Frog (cloud-based)
- **FICO Xpress**: Optimization suite
- **Gurobi**: Mathematical solver
- **CPLEX (IBM)**: MIP solver

**Open Source:**
- **PuLP**: Python linear programming
- **Pyomo**: Python optimization modeling
- **OR-Tools (Google)**: Constraint optimization
- **JuMP (Julia)**: Mathematical optimization

### Python Network Design

```python
# Complete network design example
import pulp
import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist

class NetworkDesigner:
    """Supply chain network design optimizer"""

    def __init__(self, customers_df, facilities_df):
        """
        Initialize with customer and facility data

        customers_df: columns = ['id', 'lat', 'lon', 'demand']
        facilities_df: columns = ['id', 'lat', 'lon', 'fixed_cost', 'capacity']
        """
        self.customers = customers_df
        self.facilities = facilities_df

        # Calculate distance matrix
        self.distances = self._calculate_distances()

    def _calculate_distances(self):
        """Calculate great-circle distances"""
        cust_coords = self.customers[['lat', 'lon']].values
        fac_coords = self.facilities[['lat', 'lon']].values

        # Haversine distance in miles
        distances = cdist(cust_coords, fac_coords, metric='euclidean')
        distances *= 69  # Approx miles per degree

        return distances

    def optimize(self,
                 transport_rate=2.5,
                 handling_rate=1.0,
                 service_distance=None):
        """
        Optimize network design

        transport_rate: $/mile
        handling_rate: $/unit
        service_distance: max miles for service constraint
        """

        prob = pulp.LpProblem("Network", pulp.LpMinimize)

        # Variables
        I = range(len(self.customers))
        J = range(len(self.facilities))

        y = pulp.LpVariable.dicts("Open", J, cat='Binary')
        x = pulp.LpVariable.dicts("Flow",
                                   [(i,j) for i in I for j in J],
                                   lowBound=0)

        # Objective
        prob += (
            # Fixed costs
            pulp.lpSum([self.facilities.iloc[j]['fixed_cost'] * y[j]
                       for j in J]) +
            # Transportation
            pulp.lpSum([self.distances[i,j] * transport_rate * x[i,j]
                       for i in I for j in J]) +
            # Handling
            pulp.lpSum([handling_rate * x[i,j]
                       for i in I for j in J])
        )

        # Constraints
        for i in I:
            # Demand satisfaction
            prob += pulp.lpSum([x[i,j] for j in J]) >= \
                    self.customers.iloc[i]['demand']

            # Service distance constraint
            if service_distance:
                for j in J:
                    if self.distances[i,j] > service_distance:
                        prob += x[i,j] == 0

        for j in J:
            # Capacity
            prob += pulp.lpSum([x[i,j] for i in I]) <= \
                    self.facilities.iloc[j]['capacity'] * y[j]

        # Solve
        prob.solve(pulp.PULP_CBC_CMD(msg=0))

        # Results
        return self._extract_results(prob, y, x, I, J)

    def _extract_results(self, prob, y, x, I, J):
        """Extract and format results"""

        open_dcs = [self.facilities.iloc[j]['id']
                    for j in J
                    if y[j].varValue > 0.5]

        flows = []
        for i in I:
            for j in J:
                if x[i,j].varValue > 0.01:
                    flows.append({
                        'customer': self.customers.iloc[i]['id'],
                        'facility': self.facilities.iloc[j]['id'],
                        'flow': x[i,j].varValue,
                        'distance': self.distances[i,j]
                    })

        flows_df = pd.DataFrame(flows)

        return {
            'status': pulp.LpStatus[prob.status],
            'total_cost': pulp.value(prob.objective),
            'open_facilities': open_dcs,
            'num_facilities': len(open_dcs),
            'flows': flows_df,
            'avg_distance': flows_df['distance'].mean(),
            'max_distance': flows_df['distance'].max()
        }

# Example usage
customers = pd.DataFrame({
    'id': ['C1', 'C2', 'C3', 'C4'],
    'lat': [34.05, 41.88, 39.74, 29.76],
    'lon': [-118.24, -87.63, -104.99, -95.37],
    'demand': [1000, 1500, 800, 1200]
})

facilities = pd.DataFrame({
    'id': ['DC_West', 'DC_Central', 'DC_East'],
    'lat': [36.17, 39.10, 40.71],
    'lon': [-115.14, -94.58, -74.01],
    'fixed_cost': [500000, 450000, 600000],
    'capacity': [4000, 3500, 3000]
})

designer = NetworkDesigner(customers, facilities)
result = designer.optimize(transport_rate=2.5, handling_rate=1.0)

print(f"Total Cost: ${result['total_cost']:,.0f}")
print(f"Open DCs: {result['open_facilities']}")
print(f"Avg Distance: {result['avg_distance']:.1f} miles")
```

---

## Advanced Topics

### Multi-Period Network Design

**Consider:**
- Demand growth over time
- Phased facility openings/closures
- Capacity expansion options
- Investment timing

```python
# Multi-period formulation (simplified)
T = range(planning_horizon)  # periods

# Variables
y = {}  # y[j,t] = facility j opened in period t
z = {}  # z[j,t] = facility j operating in period t

for t in T:
    for j in J:
        y[j,t] = pulp.LpVariable(f"Open_{j}_{t}", cat='Binary')
        z[j,t] = pulp.LpVariable(f"Operating_{j}_{t}", cat='Binary')

# Constraint: once opened, stays open
for t in range(1, len(T)):
    for j in J:
        prob += z[j,t] >= z[j,t-1]
```

### Global Network Design

**Additional Considerations:**
- Tariffs and duties
- Customs clearance times
- Currency exchange rates
- Transfer pricing
- Tax optimization
- Free trade zones

**Landed Cost Calculation:**
```python
def landed_cost(product_cost, transport, duty_rate, tax_rate):
    """Calculate total landed cost"""

    customs_value = product_cost + transport
    duty = customs_value * duty_rate
    taxable_value = customs_value + duty
    tax = taxable_value * tax_rate

    total = product_cost + transport + duty + tax

    return total
```

### Stochastic Network Design

**Uncertainty in:**
- Demand (scenarios)
- Costs (fuel, labor)
- Exchange rates
- Disruption risks

**Two-Stage Stochastic Programming:**
- Stage 1: Facility location decisions (before uncertainty)
- Stage 2: Flow decisions (after scenarios revealed)

---

## Common Challenges & Solutions

### Challenge: Data Quality

**Problem:**
- Inaccurate customer locations
- Incomplete demand data
- Missing cost information

**Solutions:**
- Geocode addresses (Google Maps API, etc.)
- Cluster small customers to zip/postal codes
- Use industry benchmarks for missing costs
- Sensitivity analysis on uncertain inputs

### Challenge: Too Many Potential Locations

**Problem:**
- Combinatorial explosion (1000+ potential sites)

**Solutions:**
- Pre-filter to top candidates (gravity model)
- Use clustering algorithms
- Two-phase approach: strategic then detailed
- Fix certain facilities (existing, must-keep)

### Challenge: Multi-Product Complexity

**Problem:**
- Different products, different requirements
- Refrigerated vs. dry, hazmat, etc.

**Solutions:**
- Product families/aggregation
- Multi-commodity flow models
- Separate networks by product type
- Shared vs. dedicated facilities

### Challenge: Dynamic Demand

**Problem:**
- Demand changes over time
- Seasonality, growth

**Solutions:**
- Use peak demand for capacity sizing
- Multi-period models
- Flexible facilities (scalable)
- Scenario planning (growth cases)

---

## Output Format

### Network Design Report

**Executive Summary:**
- Recommended network configuration
- Total cost and savings vs. current
- Service level improvements
- Implementation timeline and investment

**Network Configuration:**

| Facility | Location | Type | Capacity | Fixed Cost | Customers Served | Annual Throughput |
|----------|----------|------|----------|------------|------------------|-------------------|
| DC_1 | Memphis, TN | Full-line DC | 500K units | $5M | 1,250 | 450K |
| DC_2 | Los Angeles, CA | Regional DC | 300K units | $4M | 800 | 280K |

**Cost Breakdown:**

| Cost Category | Current | Proposed | Delta | % Change |
|---------------|---------|----------|-------|----------|
| Fixed Facility | $12M | $9M | -$3M | -25% |
| Transportation | $15M | $14M | -$1M | -7% |
| Inventory Carrying | $8M | $6M | -$2M | -25% |
| **Total** | **$35M** | **$29M** | **-$6M** | **-17%** |

**Service Levels:**

| Metric | Current | Proposed | Improvement |
|--------|---------|----------|-------------|
| Avg. Distance | 650 mi | 420 mi | -35% |
| 2-Day Service % | 75% | 92% | +17 pts |
| On-Time Delivery | 89% | 95% | +6 pts |

**Implementation Plan:**
- Phase 1 (Months 1-6): Open new DC_1 in Memphis
- Phase 2 (Months 7-12): Transition volumes, close 2 legacy DCs
- Phase 3 (Months 13-18): Optimize operations, continuous improvement

---

## Questions to Ask

If you need more context:
1. What's the geographic scope of the network? (regional, national, global)
2. What's driving this analysis? (cost, service, growth, consolidation)
3. How many facilities in the current network?
4. What are the primary constraints? (budget, service levels, existing leases)
5. What data is available? (customer demand, facility costs, transportation rates)
6. Greenfield (new design) or brownfield (optimize existing)?
7. What's the decision timeline and implementation horizon?

---

## Related Skills

- **facility-location-problem**: For mathematical optimization models
- **distribution-center-network**: For multi-echelon design
- **route-optimization**: For transportation within network
- **inventory-optimization**: For safety stock across network
- **supply-chain-analytics**: For network performance metrics
- **scenario-planning**: For demand uncertainty analysis
- **freight-optimization**: For transportation mode selection
