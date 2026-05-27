---
name: cpg-network-design
description: When the user wants to design CPG (Consumer Packaged Goods) distribution networks, optimize DC locations for retail distribution, or plan omnichannel fulfillment networks. Also use when the user mentions "CPG network," "retail distribution network," "DC strategy," "forward deployment centers," "store replenishment network," or "omnichannel distribution." For general network design, see network-design. For promotional supply chain, see promotional-planning.
---

# CPG Network Design

You are an expert in CPG (Consumer Packaged Goods) distribution network design and retail supply chain optimization. Your goal is to help design cost-effective distribution networks that balance inventory investment, transportation costs, and service levels to retail customers.

## Initial Assessment

Before designing CPG networks, understand:

1. **Business Context**
   - What product categories? (food, beverage, personal care, household)
   - What channels? (grocery, mass, club, convenience, DSD, e-commerce)
   - What's the geographic scope? (regional, national, international)
   - Current network? (# DCs, flow patterns, costs)
   - Growth plans or channel expansion?

2. **Customer Requirements**
   - Retailer order lead times? (2-7 days typical)
   - Order frequency? (daily, weekly)
   - Case fill rates? (>98% expected)
   - Delivery windows and appointment scheduling?
   - Drop ship vs. warehouse delivery?

3. **Product Characteristics**
   - SKU complexity? (100s to 10,000+ SKUs)
   - Velocity distribution? (A/B/C analysis)
   - Shelf life? (days, months, years)
   - Storage requirements? (ambient, refrigerated, frozen)
   - Cube density and weight?

4. **Economic Drivers**
   - Current transportation spend?
   - Current DC operating costs?
   - Inventory carrying costs?
   - Service level performance and fill rates?
   - Target cost reduction or service improvement?

---

## CPG Network Design Framework

### CPG-Specific Network Characteristics

**vs. General Industrial:**
- High SKU complexity (1,000-10,000+ SKUs typical)
- Fast-moving products (high velocity)
- Short lead times (2-5 days)
- High service level requirements (>98%)
- Promotional variability (30-50% lift)
- Multi-channel distribution (retail, DSD, e-commerce)
- Thin margins (2-5% operating margin)

**Network Echelon Options:**

**1. Direct-to-Store (Plant → Store)**
- Fresh/DSD products (bread, milk, snacks)
- High frequency, small drops
- Driver merchandising
- See dsd-route-optimization

**2. Single-Tier (Plant → DC → Store)**
- Most common for shelf-stable
- Regional DCs (3-6 typically)
- Full product line at each DC
- Economic order quantities

**3. Two-Tier (Plant → RDC → Forward DC → Store)**
- National brand with broad coverage
- RDCs for slow movers (1-2 large)
- Forward DCs for fast movers (10-15 smaller)
- Inventory optimization across tiers

**4. Hybrid (Multiple Strategies)**
- Fast movers: Forward DCs
- Slow movers: Direct ship from RDC
- Promotional: Special builds
- E-commerce: Dedicated fulfillment centers

---

## Network Design Models

### CPG Facility Location Model

```python
from pulp import *
import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist

class CPGNetworkOptimizer:
    """
    CPG-specific network design optimization
    """

    def __init__(self, customers_df, potential_dcs_df, plants_df):
        """
        Initialize CPG network optimizer

        Parameters:
        - customers_df: retailers with demand ['customer_id', 'lat', 'lon',
                       'demand_cases', 'service_level_days']
        - potential_dcs_df: potential DC locations ['dc_id', 'lat', 'lon',
                           'fixed_cost', 'variable_cost_per_case', 'capacity']
        - plants_df: manufacturing plants ['plant_id', 'lat', 'lon', 'capacity']
        """
        self.customers = customers_df
        self.dcs = potential_dcs_df
        self.plants = plants_df

        # Calculate distance matrices
        self.dc_to_customer_dist = self._calc_distances(
            self.dcs[['lat', 'lon']],
            self.customers[['lat', 'lon']]
        )

        self.plant_to_dc_dist = self._calc_distances(
            self.plants[['lat', 'lon']],
            self.dcs[['lat', 'lon']]
        )

    def _calc_distances(self, from_coords, to_coords):
        """Calculate distance matrix (miles)"""
        distances = cdist(from_coords.values, to_coords.values, metric='euclidean')
        return distances * 69  # Convert degrees to miles (approximate)

    def optimize_network(self, max_dcs=None, service_distance=None,
                          transport_rate_tl=2.50, transport_rate_ltl=25.0):
        """
        Optimize CPG distribution network

        Parameters:
        - max_dcs: maximum number of DCs to open (None = no limit)
        - service_distance: max miles for service level (None = no constraint)
        - transport_rate_tl: truckload rate ($/mile)
        - transport_rate_ltl: LTL rate ($/cwt)

        Returns:
        - optimal network configuration
        """

        prob = LpProblem("CPG_Network", LpMinimize)

        # Decision variables
        C = range(len(self.customers))
        D = range(len(self.dcs))
        P = range(len(self.plants))

        # y[d] = 1 if DC d is opened
        y = LpVariable.dicts("DC_Open", D, cat='Binary')

        # x[c,d] = flow from DC d to customer c (cases)
        x = LpVariable.dicts("Customer_Flow",
                              [(c,d) for c in C for d in D],
                              lowBound=0)

        # z[p,d] = flow from plant p to DC d (cases)
        z = LpVariable.dicts("DC_Flow",
                              [(p,d) for p in P for d in D],
                              lowBound=0)

        # Objective: Minimize total cost
        objective = 0

        # Fixed DC costs
        for d in D:
            objective += self.dcs.iloc[d]['fixed_cost'] * y[d]

        # DC variable costs
        for c in C:
            for d in D:
                handling_cost = self.dcs.iloc[d]['variable_cost_per_case']
                objective += x[c,d] * handling_cost

        # Outbound transportation (DC → Customer)
        for c in C:
            for d in D:
                distance = self.dc_to_customer_dist[d,c]
                demand = self.customers.iloc[c]['demand_cases']

                # Simplified: LTL for <20,000 lbs, TL otherwise
                if demand < 400:  # 400 cases ~= 20,000 lbs
                    cost = distance * transport_rate_ltl / 100 * demand * 50 / 100  # $/cwt
                else:
                    cost = distance * transport_rate_tl

                objective += x[c,d] * cost / demand  # Cost per case

        # Inbound transportation (Plant → DC)
        for p in P:
            for d in D:
                distance = self.plant_to_dc_dist[p,d]
                # Assume truckload shipments to DCs
                cost_per_mile = transport_rate_tl
                objective += z[p,d] * distance * cost_per_mile / 1000  # Per case

        prob += objective

        # Constraints

        # 1. Each customer served by exactly one DC
        for c in C:
            prob += lpSum([x[c,d] for d in D]) >= self.customers.iloc[c]['demand_cases']

        # 2. DC capacity constraints
        for d in D:
            prob += lpSum([x[c,d] for c in C]) <= \
                    self.dcs.iloc[d]['capacity'] * y[d]

        # 3. DC flow balance (inbound = outbound)
        for d in D:
            inbound = lpSum([z[p,d] for p in P])
            outbound = lpSum([x[c,d] for c in C])
            prob += inbound >= outbound

        # 4. Plant capacity constraints
        for p in P:
            prob += lpSum([z[p,d] for d in D]) <= self.plants.iloc[p]['capacity']

        # 5. Service distance constraint (optional)
        if service_distance:
            for c in C:
                for d in D:
                    if self.dc_to_customer_dist[d,c] > service_distance:
                        prob += x[c,d] == 0

        # 6. Maximum number of DCs (optional)
        if max_dcs:
            prob += lpSum([y[d] for d in D]) <= max_dcs

        # Solve
        prob.solve(PULP_CBC_CMD(msg=0))

        return self._extract_solution(prob, x, y, z, C, D, P)

    def _extract_solution(self, prob, x, y, z, C, D, P):
        """Extract solution details"""

        if prob.status != 1:
            return {'status': 'infeasible'}

        # Open DCs
        open_dcs = [
            {
                'dc_id': self.dcs.iloc[d]['dc_id'],
                'location': f"{self.dcs.iloc[d]['lat']:.2f}, {self.dcs.iloc[d]['lon']:.2f}",
                'fixed_cost': self.dcs.iloc[d]['fixed_cost'],
                'capacity': self.dcs.iloc[d]['capacity']
            }
            for d in D if y[d].varValue > 0.5
        ]

        # Customer assignments
        assignments = []
        for c in C:
            for d in D:
                if x[c,d].varValue > 0.01:
                    assignments.append({
                        'customer': self.customers.iloc[c]['customer_id'],
                        'dc': self.dcs.iloc[d]['dc_id'],
                        'flow': x[c,d].varValue,
                        'distance': self.dc_to_customer_dist[d,c]
                    })

        # Calculate metrics
        total_flow = sum(a['flow'] for a in assignments)
        weighted_distance = sum(a['flow'] * a['distance'] for a in assignments)
        avg_distance = weighted_distance / total_flow if total_flow > 0 else 0

        return {
            'status': 'optimal',
            'total_cost': value(prob.objective),
            'num_dcs': len(open_dcs),
            'open_dcs': open_dcs,
            'assignments': pd.DataFrame(assignments),
            'avg_distance_to_customer': avg_distance,
            'total_cases': total_flow
        }


# Example usage
customers = pd.DataFrame({
    'customer_id': ['Retailer_A', 'Retailer_B', 'Retailer_C', 'Retailer_D'],
    'lat': [34.05, 41.88, 39.74, 29.76],
    'lon': [-118.24, -87.63, -104.99, -95.37],
    'demand_cases': [50000, 75000, 40000, 60000],
    'service_level_days': [3, 3, 3, 3]
})

potential_dcs = pd.DataFrame({
    'dc_id': ['DC_West', 'DC_Central', 'DC_South', 'DC_East'],
    'lat': [36.17, 39.10, 33.75, 40.71],
    'lon': [-115.14, -94.58, -84.39, -74.01],
    'fixed_cost': [2000000, 1800000, 1900000, 2500000],
    'variable_cost_per_case': [1.50, 1.35, 1.40, 1.60],
    'capacity': [150000, 200000, 150000, 180000]
})

plants = pd.DataFrame({
    'plant_id': ['Plant_1', 'Plant_2'],
    'lat': [41.50, 34.00],
    'lon': [-90.00, -118.00],
    'capacity': [300000, 250000]
})

optimizer = CPGNetworkOptimizer(customers, potential_dcs, plants)
result = optimizer.optimize_network(max_dcs=3, service_distance=500)

print(f"Status: {result['status']}")
print(f"Total Cost: ${result['total_cost']:,.0f}")
print(f"Number of DCs: {result['num_dcs']}")
print(f"Average Distance: {result['avg_distance_to_customer']:.0f} miles")
```

---

## Service Level Modeling

### Days-to-Market Analysis

```python
def calculate_days_to_market(dc_locations, customer_locations,
                              production_lead_time=3, dc_processing_days=1):
    """
    Calculate end-to-end days from production to customer delivery

    Parameters:
    - dc_locations: DC coordinates
    - customer_locations: customer coordinates
    - production_lead_time: days to produce
    - dc_processing_days: days for DC receiving/putaway

    Returns:
    - service time analysis
    """

    from scipy.spatial.distance import cdist

    # Calculate distances
    distances = cdist(
        dc_locations[['lat', 'lon']].values,
        customer_locations[['lat', 'lon']].values,
        metric='euclidean'
    ) * 69  # miles

    # Transportation time (miles → days)
    # Assume: <250 miles = 1 day, 250-500 = 2 days, 500-750 = 3 days, etc.
    transport_days = np.ceil(distances / 250)

    # Total days to market
    total_days = production_lead_time + dc_processing_days + transport_days

    # Service level metrics
    service_metrics = {
        '1_day_service_pct': np.mean(transport_days <= 1) * 100,
        '2_day_service_pct': np.mean(transport_days <= 2) * 100,
        '3_day_service_pct': np.mean(transport_days <= 3) * 100,
        'avg_transport_days': np.mean(transport_days),
        'avg_total_days': np.mean(total_days),
        'max_days_to_market': np.max(total_days)
    }

    return service_metrics


# Benchmark service targets for CPG
service_targets = {
    'Grocery/Mass': {
        'order_lead_time_days': 3,
        'fill_rate_target': 0.98,
        'on_time_delivery_target': 0.95
    },
    'Club': {
        'order_lead_time_days': 5,
        'fill_rate_target': 0.99,
        'on_time_delivery_target': 0.98
    },
    'Convenience': {
        'order_lead_time_days': 2,
        'fill_rate_target': 0.95,
        'on_time_delivery_target': 0.90
    },
    'E-commerce': {
        'order_lead_time_days': 2,
        'fill_rate_target': 0.98,
        'on_time_delivery_target': 0.97
    }
}
```

---

## Inventory Optimization Across Network

### Multi-Echelon Inventory Model

```python
def optimize_inventory_deployment(sku_data, network_config, service_level=0.98):
    """
    Optimize safety stock across multi-echelon CPG network

    Parameters:
    - sku_data: SKU demand and variability
    - network_config: network structure (RDC, DCs, stores)
    - service_level: target service level

    Returns:
    - optimal inventory placement
    """

    from scipy.stats import norm

    z_score = norm.ppf(service_level)

    inventory_plan = []

    for sku in sku_data:
        # Demand parameters
        weekly_demand = sku['weekly_demand']
        demand_std = sku['demand_std']
        lead_time_weeks = sku['lead_time_weeks']

        # Safety stock calculation
        lead_time_demand = weekly_demand * lead_time_weeks
        lead_time_std = demand_std * np.sqrt(lead_time_weeks)

        safety_stock = z_score * lead_time_std

        # Cycle stock (replenishment quantity)
        order_frequency_weeks = sku.get('order_frequency_weeks', 2)
        cycle_stock = weekly_demand * order_frequency_weeks / 2

        # Total inventory
        total_inventory = safety_stock + cycle_stock

        inventory_plan.append({
            'sku': sku['sku_id'],
            'lead_time_demand': lead_time_demand,
            'safety_stock': safety_stock,
            'cycle_stock': cycle_stock,
            'total_inventory': total_inventory,
            'inventory_value': total_inventory * sku['unit_cost'],
            'service_level': service_level
        })

    return pd.DataFrame(inventory_plan)


# Network inventory pooling effect
def calculate_inventory_pooling_benefit(current_locations, new_locations,
                                         current_inventory):
    """
    Calculate inventory reduction from consolidation (Square Root Law)
    """

    pooling_factor = np.sqrt(new_locations / current_locations)
    new_inventory = current_inventory * pooling_factor
    inventory_reduction = current_inventory - new_inventory

    savings = {
        'current_locations': current_locations,
        'new_locations': new_locations,
        'current_inventory': current_inventory,
        'new_inventory': new_inventory,
        'inventory_reduction': inventory_reduction,
        'reduction_pct': inventory_reduction / current_inventory * 100
    }

    return savings


# Example: Consolidate 10 DCs to 5
pooling = calculate_inventory_pooling_benefit(
    current_locations=10,
    new_locations=5,
    current_inventory=10000000  # $10M inventory
)

print(f"Inventory Reduction: ${pooling['inventory_reduction']:,.0f}")
print(f"Reduction %: {pooling['reduction_pct']:.1f}%")
```

---

## Omnichannel Network Design

### Hybrid Fulfillment Network

```python
class OmnichannelNetworkDesigner:
    """
    Design omnichannel fulfillment network for CPG

    Channels:
    - Traditional retail (store replenishment)
    - E-commerce (direct-to-consumer)
    - Click & collect (buy online, pick up in store)
    """

    def __init__(self, retail_demand, ecom_demand):
        self.retail = retail_demand
        self.ecom = ecom_demand

    def design_hybrid_network(self, strategy='integrated'):
        """
        Design network based on strategy

        Strategies:
        - 'integrated': Shared DCs for retail and e-commerce
        - 'dedicated': Separate e-commerce fulfillment centers
        - 'hybrid': Regional DCs + dedicated e-com nodes
        """

        if strategy == 'integrated':
            return self._design_integrated()
        elif strategy == 'dedicated':
            return self._design_dedicated()
        elif strategy == 'hybrid':
            return self._design_hybrid()

    def _design_integrated(self):
        """Shared network for all channels"""

        total_demand = self.retail['demand'].sum() + self.ecom['demand'].sum()

        network = {
            'strategy': 'integrated',
            'dc_type': 'multi-channel',
            'num_dcs': self._optimal_dc_count(total_demand),
            'characteristics': {
                'retail_fulfillment': 'Case picking',
                'ecom_fulfillment': 'Each picking from same DC',
                'inventory': 'Shared pool',
                'pros': ['Inventory pooling', 'Lower fixed costs', 'Simpler'],
                'cons': ['Conflicting operations', 'Peak congestion', 'Less specialized']
            }
        }

        return network

    def _design_dedicated(self):
        """Separate networks for retail and e-commerce"""

        retail_dcs = self._optimal_dc_count(self.retail['demand'].sum())
        ecom_fcs = self._optimal_fc_count(self.ecom['demand'].sum())

        network = {
            'strategy': 'dedicated',
            'retail_dcs': retail_dcs,
            'ecom_fcs': ecom_fcs,
            'total_facilities': retail_dcs + ecom_fcs,
            'characteristics': {
                'retail_fulfillment': 'Case picking, pallet shipping',
                'ecom_fulfillment': 'Each picking, parcel shipping',
                'inventory': 'Separate pools',
                'pros': ['Optimized for each channel', 'No conflicts', 'Better service'],
                'cons': ['Higher fixed costs', 'Duplicate inventory', 'Complex']
            }
        }

        return network

    def _design_hybrid(self):
        """Hybrid: Regional DCs + dedicated e-commerce nodes"""

        network = {
            'strategy': 'hybrid',
            'regional_dcs': 3,  # Large regional DCs for retail + slow e-com
            'ecom_forward_nodes': 6,  # Smaller e-com nodes for fast movers
            'characteristics': {
                'fast_movers_ecom': 'From forward e-com nodes (2-day)',
                'slow_movers_ecom': 'From regional DCs (3-5 day)',
                'retail': 'From regional DCs',
                'inventory': 'Fast movers duplicated, slow movers pooled',
                'pros': ['Balance cost and service', 'Fast e-com fulfillment', 'Inventory optimization'],
                'cons': ['Moderate complexity', 'Requires smart routing']
            }
        }

        return network

    def _optimal_dc_count(self, demand):
        """Simple heuristic for DC count"""
        # Rule of thumb: 1 DC per $500M demand
        return max(2, int(demand / 500000000))

    def _optimal_fc_count(self, demand):
        """Optimal e-commerce FC count"""
        # E-commerce needs more nodes for fast delivery
        return max(3, int(demand / 200000000))


# Example
designer = OmnichannelNetworkDesigner(
    retail_demand=pd.DataFrame({'demand': [1000000000]}),  # $1B retail
    ecom_demand=pd.DataFrame({'demand': [200000000]})      # $200M e-commerce
)

integrated = designer.design_hybrid_network('integrated')
dedicated = designer.design_hybrid_network('dedicated')
hybrid = designer.design_hybrid_network('hybrid')

print("Integrated:", integrated)
print("\nDedicated:", dedicated)
print("\nHybrid:", hybrid)
```

---

## CPG-Specific Considerations

### Promotional Surge Capacity

```python
def size_network_for_promotions(base_demand, promotional_lift=0.40,
                                  promotional_weeks_per_year=12):
    """
    Size network capacity considering promotional surge

    CPG challenge: Promotions can increase demand 30-50%
    Network must handle surge without stockouts
    """

    # Annual base demand
    annual_base = base_demand * 52

    # Promotional demand
    promo_demand_per_week = base_demand * (1 + promotional_lift)
    promo_weeks = promotional_weeks_per_year
    base_weeks = 52 - promo_weeks

    # Total annual demand
    annual_total = (base_demand * base_weeks) + (promo_demand_per_week * promo_weeks)

    # Peak week capacity needed
    peak_capacity = promo_demand_per_week

    # Design capacity (with buffer)
    design_capacity = peak_capacity * 1.15  # 15% buffer

    capacity_plan = {
        'base_weekly_demand': base_demand,
        'peak_weekly_demand': peak_capacity,
        'design_capacity': design_capacity,
        'capacity_utilization_base': base_demand / design_capacity,
        'capacity_utilization_peak': peak_capacity / design_capacity,
        'annual_demand': annual_total,
        'promotional_weeks': promo_weeks,
        'avg_utilization': annual_total / (design_capacity * 52)
    }

    return capacity_plan


# Example
promo_capacity = size_network_for_promotions(
    base_demand=100000,  # cases/week
    promotional_lift=0.40,
    promotional_weeks_per_year=12
)

print(f"Design Capacity: {promo_capacity['design_capacity']:,.0f} cases/week")
print(f"Average Utilization: {promo_capacity['avg_utilization']:.1%}")
print(f"Peak Utilization: {promo_capacity['capacity_utilization_peak']:.1%}")
```

### Slotting and Forward Deployment

```python
def optimize_forward_deployment(skus, dc_network, forward_deployment_cost):
    """
    Optimize which SKUs to forward-deploy to more DCs

    Trade-off:
    - Forward deploy fast movers: Lower transport, higher inventory
    - Centralize slow movers: Higher transport, lower inventory
    """

    sku_strategy = []

    for sku in skus:
        velocity = sku['annual_demand']
        unit_value = sku['unit_cost']

        # Transport cost savings from forward deployment
        transport_savings = calculate_transport_savings(sku, dc_network)

        # Inventory cost increase from duplication
        inventory_increase = (dc_network['num_forward_dcs'] - 1) * \
                            sku['safety_stock'] * unit_value * 0.25  # 25% carrying cost

        # Net benefit
        net_benefit = transport_savings - inventory_increase

        # Decision
        if net_benefit > 0:
            strategy = 'forward_deploy'
            locations = dc_network['num_forward_dcs']
        else:
            strategy = 'centralize'
            locations = 1  # Keep at RDC only

        sku_strategy.append({
            'sku': sku['sku_id'],
            'strategy': strategy,
            'locations': locations,
            'transport_savings': transport_savings,
            'inventory_increase': inventory_increase,
            'net_benefit': net_benefit
        })

    return pd.DataFrame(sku_strategy)


def calculate_transport_savings(sku, dc_network):
    """Calculate transport savings from forward deployment"""

    # Simplified model
    central_distance = dc_network['avg_distance_from_rdc']
    forward_distance = dc_network['avg_distance_from_forward_dc']

    distance_savings = central_distance - forward_distance

    # Annual shipments
    shipments_per_year = sku['annual_demand'] / sku['order_size']

    # Cost per shipment
    cost_per_mile = 2.50
    cost_savings = shipments_per_year * distance_savings * cost_per_mile

    return cost_savings
```

---

## Performance Metrics

### CPG Network KPIs

```python
class CPGNetworkMetrics:
    """
    Track CPG network performance metrics
    """

    def __init__(self, network_data):
        self.data = network_data

    def calculate_kpis(self):
        """Calculate comprehensive network KPIs"""

        kpis = {}

        # Cost metrics
        kpis['total_network_cost'] = self._total_network_cost()
        kpis['cost_per_case'] = kpis['total_network_cost'] / self.data['total_cases']

        # Cost breakdown
        kpis['cost_breakdown'] = {
            'fixed_dc_costs': self._fixed_dc_costs(),
            'variable_dc_costs': self._variable_dc_costs(),
            'inbound_transport': self._inbound_transport_cost(),
            'outbound_transport': self._outbound_transport_cost(),
            'inventory_carrying': self._inventory_carrying_cost()
        }

        # Service metrics
        kpis['avg_distance_to_customer'] = self._avg_distance()
        kpis['2_day_service_pct'] = self._service_coverage(max_distance=500)
        kpis['3_day_service_pct'] = self._service_coverage(max_distance=750)

        # Efficiency metrics
        kpis['dc_utilization'] = self._dc_utilization()
        kpis['cases_per_dc'] = self.data['total_cases'] / self.data['num_dcs']

        # Inventory metrics
        kpis['total_inventory_value'] = self._total_inventory()
        kpis['inventory_turns'] = self._inventory_turns()
        kpis['days_of_supply'] = 365 / kpis['inventory_turns']

        return kpis

    def _total_network_cost(self):
        """Total annual network cost"""
        return sum(self.data['cost_breakdown'].values())

    def _fixed_dc_costs(self):
        """Total fixed DC costs"""
        return sum(dc['fixed_cost'] for dc in self.data['dcs'])

    def _variable_dc_costs(self):
        """Total variable DC handling costs"""
        return self.data['total_cases'] * self.data['avg_variable_cost_per_case']

    def _inbound_transport_cost(self):
        """Plant to DC transportation"""
        return self.data.get('inbound_transport_cost', 0)

    def _outbound_transport_cost(self):
        """DC to customer transportation"""
        return self.data.get('outbound_transport_cost', 0)

    def _inventory_carrying_cost(self):
        """Inventory carrying cost (25% of inventory value)"""
        return self._total_inventory() * 0.25

    def _avg_distance(self):
        """Average distance from DC to customer"""
        return self.data['weighted_avg_distance']

    def _service_coverage(self, max_distance):
        """% customers within distance"""
        return self.data['service_coverage'].get(max_distance, 0)

    def _dc_utilization(self):
        """Average DC capacity utilization"""
        return self.data['total_cases'] / sum(dc['capacity'] for dc in self.data['dcs'])

    def _total_inventory(self):
        """Total inventory value in network"""
        return self.data.get('total_inventory_value', 0)

    def _inventory_turns(self):
        """Inventory turnover ratio"""
        annual_cogs = self.data.get('annual_cogs', 0)
        avg_inventory = self._total_inventory()
        return annual_cogs / avg_inventory if avg_inventory > 0 else 0


# CPG Network Benchmarks
cpg_benchmarks = {
    'cost_per_case': {
        'best_in_class': 2.50,
        'average': 3.50,
        'poor': 5.00
    },
    'inventory_turns': {
        'best_in_class': 12,
        'average': 8,
        'poor': 6
    },
    'fill_rate': {
        'best_in_class': 0.99,
        'average': 0.96,
        'poor': 0.92
    },
    'on_time_delivery': {
        'best_in_class': 0.98,
        'average': 0.95,
        'poor': 0.90
    }
}
```

---

## Tools & Technologies

### CPG Network Design Software

**Commercial:**
- **Coupa Supply Chain Design**: Network optimization for CPG
- **LLamasoft (Coupa)**: Supply Chain Guru
- **Blue Yonder Network Design**: JDA heritage
- **Optilogic Cosmic Frog**: Cloud-based network design
- **AIMMS**: Network optimization platform
- **Llamasoft Guru**: Scenario planning

**Analytics Platforms:**
- **Kinaxis RapidResponse**: S&OP and network planning
- **o9 Solutions**: Digital planning platform
- **Anaplan**: Cloud planning with optimization
- **SAP IBP**: Integrated business planning

### Python Libraries

```python
# Network optimization
from pulp import *
import pyomo.environ as pyo

# Geospatial analysis
import geopandas as gpd
from shapely.geometry import Point
from scipy.spatial import distance_matrix

# Optimization solvers
from ortools.linear_solver import pywraplp
import gurobipy as gp

# Data analysis
import pandas as pd
import numpy as np

# Visualization
import plotly.express as px
import folium
import matplotlib.pyplot as plt
```

---

## Common Challenges & Solutions

### Challenge: High SKU Complexity

**Problem:**
- 5,000-10,000 SKUs to manage
- Slow movers create inventory burden
- Forward deployment is expensive

**Solutions:**
- ABC/XYZ segmentation
- Forward deploy only A items (top 20%)
- Ship B/C items from central location
- Use drop ship for very slow movers
- SKU rationalization program

### Challenge: Promotional Variability

**Problem:**
- Base demand 100K, promo demand 150K
- Need surge capacity
- Risk of stockouts or obsolescence

**Solutions:**
- Size capacity for peak (with buffer)
- Forward-stock promotional inventory
- Use flexible 3PL for surge
- Demand sensing and rapid replenishment
- Negotiate capacity with retailers

### Challenge: Omnichannel Complexity

**Problem:**
- Retail needs cases, e-com needs eaches
- Different service levels
- Inventory allocation conflicts

**Solutions:**
- Hybrid network (shared + dedicated)
- Ship-from-store for e-commerce
- DC slotting for both modes
- Advanced ATP (available-to-promise)
- Unified inventory visibility

### Challenge: Low Margins

**Problem:**
- CPG margins 2-5%
- Network costs 3-5% of sales
- Every dollar counts

**Solutions:**
- Continuous optimization (quarterly reviews)
- Benchmark against peers
- Negotiate transportation rates annually
- Automation in DCs (labor = 50% of DC cost)
- Inventory reduction programs

---

## Output Format

### CPG Network Design Report

**Executive Summary:**
- Current Network: 8 DCs, $45M annual cost
- Recommended Network: 5 DCs, $38M annual cost
- Annual Savings: $7M (15.6%)
- Service Level: Maintained at 98%
- Implementation: 18 months

**Network Configuration:**

| DC | Location | Type | Size (SF) | Capacity | Fixed Cost | Annual Volume |
|----|----------|------|-----------|----------|------------|---------------|
| DC1 | Memphis, TN | Regional | 500K | 120M cases | $8M | 95M |
| DC2 | LA, CA | Regional | 400K | 100M cases | $9M | 75M |
| DC3 | Newark, NJ | Regional | 450K | 110M cases | $8.5M | 85M |
| DC4 | Dallas, TX | Forward | 250K | 60M cases | $5M | 45M |
| DC5 | Atlanta, GA | Forward | 300K | 75M cases | $6M | 55M |

**Cost Comparison:**

| Cost Category | Current | Proposed | Delta | % Change |
|---------------|---------|----------|-------|----------|
| Fixed DC Costs | $18M | $15M | -$3M | -17% |
| DC Operations | $12M | $10M | -$2M | -17% |
| Inbound Transport | $8M | $7M | -$1M | -13% |
| Outbound Transport | $7M | $6M | -$1M | -14% |
| **Total** | **$45M** | **$38M** | **-$7M** | **-15.6%** |

**Service Level Analysis:**

| Metric | Current | Proposed | Change |
|--------|---------|----------|--------|
| Avg Distance to Customer | 420 mi | 385 mi | -35 mi |
| 2-Day Service | 78% | 85% | +7 pts |
| 3-Day Service | 94% | 96% | +2 pts |
| Fill Rate | 96.5% | 98.0% | +1.5 pts |

---

## Questions to Ask

If you need more context:
1. What product categories and channels?
2. Current network configuration and costs?
3. What's the geographic scope?
4. How many SKUs and what's the velocity distribution?
5. What are the service level requirements?
6. Any promotional or seasonal patterns?
7. E-commerce component and growth?
8. Budget for network redesign?

---

## Related Skills

- **network-design**: For general network optimization techniques
- **facility-location-problem**: For mathematical models
- **inventory-optimization**: For safety stock and inventory deployment
- **promotional-planning**: For handling promotional surge
- **dsd-route-optimization**: For direct store delivery
- **warehouse-design**: For DC layout and automation
- **demand-forecasting**: For demand planning
- **omnichannel-fulfillment**: For e-commerce integration
- **freight-optimization**: For transportation optimization
