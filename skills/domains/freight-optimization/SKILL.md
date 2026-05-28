---
name: freight-optimization
description: When the user wants to optimize freight transportation, reduce shipping costs, or improve carrier selection. Also use when the user mentions "freight management," "carrier optimization," "mode selection," "LTL/TL optimization," "freight consolidation," "load planning," or "transportation procurement." For local delivery routes, see route-optimization. For last-mile, see last-mile-delivery.
---

# Freight Optimization

You are an expert in freight transportation optimization and logistics. Your goal is to help minimize transportation costs, improve service levels, and optimize carrier selection across all transportation modes while ensuring on-time delivery and freight visibility.

## Initial Assessment

Before optimizing freight operations, understand:

1. **Freight Characteristics**
   - What are you shipping? (products, weight, cube)
   - Typical shipment sizes? (parcel, LTL, TL, container)
   - Special handling needs? (temperature, hazmat, oversized)
   - Freight value and insurance requirements?

2. **Network & Lanes**
   - Origin and destination points?
   - Primary shipping lanes?
   - Frequency per lane? (daily, weekly, monthly)
   - Balanced lanes or predominantly outbound?

3. **Current Performance**
   - Current freight spend? (annual)
   - Cost per mile or per shipment?
   - On-time delivery rate?
   - Damage/claims rate?
   - Carrier mix (# of carriers used)?

4. **Service Requirements**
   - Transit time requirements?
   - Delivery windows or appointments?
   - Tracking and visibility needs?
   - Customer service expectations?

---

## Freight Optimization Framework

### Transportation Modes

**1. Truckload (TL / FTL)**
- Full truck dedicated to your freight
- Point-to-point service
- Faster, less handling
- Cost: ~$2.00-3.50 per mile (varies by lane)
- Best for: 24+ pallets, 36,000+ lbs, dedicated service

**2. Less-Than-Truckload (LTL)**
- Share truck space with other shippers
- Hub-and-spoke network
- Multiple handling points
- Cost: ~$20-50 per cwt (100 lbs) depending on distance
- Best for: 1-23 pallets, 500-36,000 lbs

**3. Parcel**
- Small packages (<150 lbs)
- Extensive network (UPS, FedEx, USPS)
- Zone-based pricing
- Cost: $10-50 per package depending on zone/weight
- Best for: Individual items, e-commerce

**4. Intermodal (Rail)**
- Combines rail and truck
- Slower but cheaper for long haul
- Cost: ~30-40% less than truck
- Best for: 1,000+ miles, flexible timing

**5. Air Freight**
- Fastest mode, highest cost
- Cost: $2-8 per lb
- Best for: High-value, time-critical, international

**6. Ocean (Container)**
- International shipping
- 20' or 40' containers
- Cost: $1,500-5,000 per container (varies greatly)
- Best for: International, high volume, flexible timing

---

## Mode Selection & Optimization

### Mode Selection Decision Tree

```python
import numpy as np
import pandas as pd

class FreightModeSelector:
    """
    Intelligent freight mode selection

    Recommends optimal transportation mode based on shipment characteristics
    """

    def __init__(self):
        # Rate structures (simplified benchmarks)
        self.rates = {
            'parcel': {'base': 10, 'per_lb': 0.50, 'per_mile': 0.05},
            'ltl': {'base': 150, 'per_cwt': 25, 'per_mile': 0.8},
            'tl': {'base_rate': 2.50, 'min_charge': 500},
            'intermodal': {'base_rate': 1.75, 'min_charge': 800},
            'air': {'base': 200, 'per_lb': 3.50}
        }

    def calculate_mode_cost(self, weight_lbs, distance_miles, freight_class=70):
        """
        Calculate cost for each transportation mode

        Parameters:
        - weight_lbs: Shipment weight in pounds
        - distance_miles: Distance in miles
        - freight_class: NMFC freight class (affects LTL pricing)
        """

        costs = {}

        # Parcel (up to 150 lbs per package)
        if weight_lbs <= 150:
            costs['parcel'] = (
                self.rates['parcel']['base'] +
                weight_lbs * self.rates['parcel']['per_lb'] +
                distance_miles * self.rates['parcel']['per_mile']
            )
        else:
            costs['parcel'] = None  # Too heavy

        # LTL (500 - 36,000 lbs)
        if 500 <= weight_lbs <= 36000:
            cwt = weight_lbs / 100
            class_multiplier = freight_class / 70  # Adjust for class
            costs['ltl'] = (
                self.rates['ltl']['base'] +
                cwt * self.rates['ltl']['per_cwt'] * class_multiplier +
                distance_miles * self.rates['ltl']['per_mile']
            )
        else:
            costs['ltl'] = None

        # Truckload (>20,000 lbs optimal)
        if weight_lbs >= 10000:
            costs['tl'] = max(
                distance_miles * self.rates['tl']['base_rate'],
                self.rates['tl']['min_charge']
            )
        else:
            costs['tl'] = None

        # Intermodal (>1000 miles)
        if distance_miles >= 1000:
            costs['intermodal'] = max(
                distance_miles * self.rates['intermodal']['base_rate'],
                self.rates['intermodal']['min_charge']
            )
        else:
            costs['intermodal'] = None

        # Air freight (time-critical)
        costs['air'] = (
            self.rates['air']['base'] +
            weight_lbs * self.rates['air']['per_lb']
        )

        return costs

    def recommend_mode(self, weight_lbs, distance_miles, urgency='standard',
                      freight_class=70):
        """
        Recommend optimal transportation mode

        Parameters:
        - urgency: 'standard', 'expedited', 'critical'
        """

        costs = self.calculate_mode_cost(weight_lbs, distance_miles, freight_class)

        # Filter out None values
        valid_costs = {mode: cost for mode, cost in costs.items()
                      if cost is not None}

        if not valid_costs:
            return {'error': 'No valid transportation mode'}

        # Apply urgency filters
        if urgency == 'critical':
            # Only air or expedited TL
            valid_costs = {k: v for k, v in valid_costs.items()
                          if k in ['air', 'tl']}

        elif urgency == 'expedited':
            # Exclude intermodal (slower)
            valid_costs = {k: v for k, v in valid_costs.items()
                          if k != 'intermodal'}

        # Find minimum cost mode
        recommended_mode = min(valid_costs, key=valid_costs.get)
        recommended_cost = valid_costs[recommended_mode]

        # Calculate savings vs. alternatives
        alternatives = {k: v for k, v in valid_costs.items()
                       if k != recommended_mode}

        return {
            'recommended_mode': recommended_mode,
            'cost': recommended_cost,
            'alternatives': alternatives,
            'all_costs': costs
        }

# Example usage
selector = FreightModeSelector()

# Small package
result = selector.recommend_mode(weight_lbs=25, distance_miles=800)
print(f"Small package: {result['recommended_mode']} at ${result['cost']:.2f}")

# LTL shipment
result = selector.recommend_mode(weight_lbs=5000, distance_miles=1200)
print(f"LTL shipment: {result['recommended_mode']} at ${result['cost']:.2f}")

# Truckload
result = selector.recommend_mode(weight_lbs=35000, distance_miles=1500)
print(f"Truckload: {result['recommended_mode']} at ${result['cost']:.2f}")
```

### LTL vs. TL Breakeven Analysis

```python
def ltl_tl_breakeven(distance_miles, freight_class=70,
                     ltl_rate_per_cwt=25, tl_rate_per_mile=2.50):
    """
    Calculate breakeven point between LTL and Truckload

    Returns weight where TL becomes more economical
    """

    # LTL cost increases with weight
    # TL cost is fixed regardless of weight

    tl_cost = distance_miles * tl_rate_per_mile

    # Solve for weight where LTL cost equals TL cost
    # LTL_cost = (weight/100) * ltl_rate_per_cwt * (freight_class/70) + base
    # Simplified: when does (weight/100) * rate = TL_cost

    class_multiplier = freight_class / 70
    breakeven_weight = (tl_cost / (ltl_rate_per_cwt * class_multiplier)) * 100

    return {
        'breakeven_weight_lbs': breakeven_weight,
        'breakeven_pallets': breakeven_weight / 1500,  # Assume 1500 lbs/pallet
        'tl_cost': tl_cost,
        'recommendation': f"Use LTL below {breakeven_weight:.0f} lbs, TL above"
    }

# Example: 800-mile lane
breakeven = ltl_tl_breakeven(distance_miles=800)
print(f"Breakeven: {breakeven['breakeven_weight_lbs']:.0f} lbs "
      f"({breakeven['breakeven_pallets']:.1f} pallets)")
```

---

## Freight Consolidation

### Shipment Consolidation Optimizer

```python
import pandas as pd
from datetime import datetime, timedelta

class FreightConsolidator:
    """
    Optimize freight consolidation

    Combine multiple small shipments into larger loads
    to reduce transportation costs
    """

    def __init__(self, shipments_df):
        """
        Parameters:
        - shipments_df: DataFrame with columns
          ['order_id', 'customer', 'destination', 'weight',
           'ready_date', 'due_date', 'priority']
        """
        self.shipments = shipments_df.copy()

    def identify_consolidation_opportunities(self, max_wait_days=3,
                                            max_distance_deviation=50):
        """
        Find shipments that can be consolidated

        Parameters:
        - max_wait_days: Maximum days to hold shipment for consolidation
        - max_distance_deviation: Max miles between destinations to consolidate
        """

        # Group by destination region
        self.shipments['region'] = self.shipments['destination'].apply(
            self._assign_region
        )

        opportunities = []

        for region, group in self.shipments.groupby('region'):
            if len(group) < 2:
                continue

            # Check if shipments can wait for consolidation
            earliest_ready = group['ready_date'].min()
            latest_due = group['due_date'].max()

            time_window = (latest_due - earliest_ready).days

            if time_window <= max_wait_days:
                total_weight = group['weight'].sum()

                # Determine if consolidation makes sense
                if total_weight >= 10000:  # Enough for TL consideration
                    opportunities.append({
                        'region': region,
                        'num_shipments': len(group),
                        'total_weight': total_weight,
                        'ready_date': earliest_ready,
                        'due_date': latest_due,
                        'consolidation_type': 'Truckload' if total_weight >= 20000 else 'LTL',
                        'estimated_savings': self._estimate_savings(group)
                    })

        return pd.DataFrame(opportunities)

    def _assign_region(self, destination):
        """Assign destination to region (simplified)"""
        # In practice, use zip code or geographic clustering
        return destination[:5]  # Use first 5 chars as region

    def _estimate_savings(self, shipments):
        """
        Estimate cost savings from consolidation

        Compare individual LTL vs. consolidated TL
        """

        # Individual LTL cost
        individual_cost = len(shipments) * 300  # Simplified

        # Consolidated cost
        consolidated_cost = 800  # Single TL

        savings = individual_cost - consolidated_cost
        return max(0, savings)

    def create_consolidation_plan(self, opportunities, target_savings=10000):
        """
        Create consolidation execution plan

        Prioritize by savings potential
        """

        # Sort by savings
        opportunities = opportunities.sort_values(
            'estimated_savings',
            ascending=False
        )

        plan = []
        cumulative_savings = 0

        for idx, opp in opportunities.iterrows():
            if cumulative_savings >= target_savings:
                break

            plan.append({
                'region': opp['region'],
                'action': f"Consolidate {opp['num_shipments']} shipments",
                'weight': opp['total_weight'],
                'type': opp['consolidation_type'],
                'ship_date': opp['ready_date'],
                'savings': opp['estimated_savings']
            })

            cumulative_savings += opp['estimated_savings']

        return plan, cumulative_savings

# Example usage
shipments = pd.DataFrame({
    'order_id': [f'ORD{i:04d}' for i in range(50)],
    'customer': [f'Customer_{i%10}' for i in range(50)],
    'destination': [f'ZIP_{zip}' for zip in np.random.randint(10000, 99999, 50)],
    'weight': np.random.randint(500, 5000, 50),
    'ready_date': [datetime.now() + timedelta(days=np.random.randint(0, 3))
                   for _ in range(50)],
    'due_date': [datetime.now() + timedelta(days=np.random.randint(5, 10))
                 for _ in range(50)],
    'priority': np.random.choice(['Standard', 'Expedited'], 50)
})

consolidator = FreightConsolidator(shipments)
opportunities = consolidator.identify_consolidation_opportunities()
plan, savings = consolidator.create_consolidation_plan(opportunities)

print(f"Found {len(opportunities)} consolidation opportunities")
print(f"Estimated annual savings: ${savings * 52:,.0f}")
```

### Milk Run Optimization

```python
class MilkRunOptimizer:
    """
    Optimize milk runs (regular pickup routes)

    Consolidate pickups from multiple suppliers onto single truck
    """

    def __init__(self, suppliers, frequencies, truck_capacity=40000):
        """
        Parameters:
        - suppliers: DataFrame with supplier locations and volumes
        - frequencies: pickup frequency per supplier
        - truck_capacity: truck weight capacity (lbs)
        """
        self.suppliers = suppliers
        self.frequencies = frequencies
        self.capacity = truck_capacity

    def design_milk_run_routes(self, max_route_time=8):
        """
        Design milk run routes

        Combine multiple supplier pickups into single route
        """

        from sklearn.cluster import DBSCAN

        # Cluster suppliers geographically
        coords = self.suppliers[['latitude', 'longitude']].values
        clustering = DBSCAN(eps=0.5, min_samples=2).fit(coords)

        routes = []

        for cluster_id in set(clustering.labels_):
            if cluster_id == -1:  # Noise
                continue

            cluster_suppliers = self.suppliers[clustering.labels_ == cluster_id]

            # Check if total volume fits in truck
            total_volume = cluster_suppliers['avg_volume'].sum()

            if total_volume <= self.capacity:
                routes.append({
                    'route_id': len(routes) + 1,
                    'suppliers': cluster_suppliers['supplier_id'].tolist(),
                    'total_volume': total_volume,
                    'utilization': total_volume / self.capacity,
                    'num_stops': len(cluster_suppliers)
                })

        return routes

    def calculate_milk_run_savings(self, routes, individual_pickup_cost=250):
        """
        Calculate savings from milk runs vs. individual pickups

        Parameters:
        - individual_pickup_cost: Cost of individual supplier pickup
        """

        # Current cost (individual pickups)
        total_suppliers = len(self.suppliers)
        current_cost = total_suppliers * individual_pickup_cost

        # Milk run cost
        milk_run_cost = len(routes) * 400  # Cost per milk run route

        savings = current_cost - milk_run_cost
        savings_percentage = (savings / current_cost) * 100 if current_cost > 0 else 0

        return {
            'current_cost': current_cost,
            'milk_run_cost': milk_run_cost,
            'savings': savings,
            'savings_percentage': savings_percentage,
            'num_routes': len(routes)
        }
```

---

## Load Planning & Optimization

### Trailer Loading Optimization

```python
class TrailerLoadingOptimizer:
    """
    Optimize trailer loading

    Maximize cube utilization and ensure weight distribution
    """

    def __init__(self, trailer_length=53, trailer_width=8.5,
                 trailer_height=9, weight_capacity=45000):
        """
        Parameters:
        - Dimensions in feet
        - Weight in pounds
        """
        self.length = trailer_length
        self.width = trailer_width
        self.height = trailer_height
        self.weight_capacity = weight_capacity
        self.max_cube = trailer_length * trailer_width * trailer_height

    def calculate_load_metrics(self, pallets):
        """
        Calculate load metrics for set of pallets

        Parameters:
        - pallets: list of dicts with 'length', 'width', 'height', 'weight'
        """

        total_weight = sum(p['weight'] for p in pallets)
        total_cube = sum(p['length'] * p['width'] * p['height']
                        for p in pallets)

        # Assuming standard pallet footprint (40"x48" = 3.33' x 4')
        # 53' trailer fits ~26 pallets single stacked
        num_pallets = len(pallets)
        single_stack_capacity = int(self.length / 4)  # 4' per pallet

        # Can we stack?
        stackable_height = sum(p['height'] for p in pallets if p.get('stackable', True))

        return {
            'num_pallets': num_pallets,
            'total_weight': total_weight,
            'weight_utilization': total_weight / self.weight_capacity,
            'total_cube': total_cube,
            'cube_utilization': total_cube / self.max_cube,
            'weight_limited': total_weight / self.weight_capacity > 0.95,
            'cube_limited': total_cube / self.max_cube > 0.95,
            'floor_positions_used': min(num_pallets, single_stack_capacity),
            'can_stack': num_pallets > single_stack_capacity
        }

    def optimize_multi_order_loads(self, orders, destinations):
        """
        Optimize loading multiple orders onto same trailer

        Consider delivery sequence and weight distribution
        """

        # Sort orders by delivery sequence
        sorted_orders = sorted(
            zip(orders, destinations),
            key=lambda x: x[1]['delivery_sequence']
        )

        load_plan = []
        current_weight = 0
        current_cube = 0

        for order, dest in sorted_orders:
            order_weight = sum(p['weight'] for p in order['pallets'])
            order_cube = sum(p['length'] * p['width'] * p['height']
                           for p in order['pallets'])

            # Check if order fits
            if (current_weight + order_weight <= self.weight_capacity and
                current_cube + order_cube <= self.max_cube):

                load_plan.append({
                    'order_id': order['order_id'],
                    'destination': dest['name'],
                    'pallets': len(order['pallets']),
                    'weight': order_weight,
                    'position': 'rear' if len(load_plan) < 2 else 'front'
                    # Last stop loads in front (FILO)
                })

                current_weight += order_weight
                current_cube += order_cube

        return {
            'load_plan': load_plan,
            'total_weight': current_weight,
            'total_cube': current_cube,
            'utilization': {
                'weight': current_weight / self.weight_capacity,
                'cube': current_cube / self.max_cube
            }
        }

# Example
optimizer = TrailerLoadingOptimizer()

pallets = [
    {'length': 4, 'width': 3.33, 'height': 5, 'weight': 1800, 'stackable': True}
    for _ in range(24)
]

metrics = optimizer.calculate_load_metrics(pallets)
print(f"Load utilization: Weight {metrics['weight_utilization']:.1%}, "
      f"Cube {metrics['cube_utilization']:.1%}")
```

---

## Carrier Management & Procurement

### Carrier Selection & Optimization

```python
class CarrierOptimizer:
    """
    Optimize carrier selection and allocation

    Balance cost, service, and carrier diversification
    """

    def __init__(self, carriers_df, lanes_df):
        """
        Parameters:
        - carriers_df: carrier information (rates, service, capacity)
        - lanes_df: shipping lanes (origin, dest, volume)
        """
        self.carriers = carriers_df
        self.lanes = lanes_df

    def score_carriers(self, weights={'cost': 0.5, 'service': 0.3,
                                     'reliability': 0.2}):
        """
        Score carriers based on multiple criteria

        Returns ranked carriers per lane
        """

        scored = []

        for _, lane in self.lanes.iterrows():
            lane_carriers = self.carriers[
                self.carriers['lane_id'] == lane['lane_id']
            ].copy()

            if len(lane_carriers) == 0:
                continue

            # Normalize scores (0-1 scale)
            # Cost: lower is better
            lane_carriers['cost_score'] = 1 - (
                (lane_carriers['cost'] - lane_carriers['cost'].min()) /
                (lane_carriers['cost'].max() - lane_carriers['cost'].min())
            )

            # Service and reliability: higher is better (already 0-1)

            # Composite score
            lane_carriers['total_score'] = (
                weights['cost'] * lane_carriers['cost_score'] +
                weights['service'] * lane_carriers['service_score'] +
                weights['reliability'] * lane_carriers['reliability_score']
            )

            lane_carriers = lane_carriers.sort_values(
                'total_score',
                ascending=False
            )

            scored.extend(lane_carriers.to_dict('records'))

        return pd.DataFrame(scored)

    def allocate_volume(self, max_carrier_share=0.4):
        """
        Allocate volume across carriers

        Avoid over-concentration with single carrier
        """

        allocation = []

        for lane_id in self.lanes['lane_id'].unique():
            lane_volume = self.lanes[
                self.lanes['lane_id'] == lane_id
            ]['volume'].sum()

            lane_carriers = self.carriers[
                self.carriers['lane_id'] == lane_id
            ].sort_values('cost')

            remaining_volume = lane_volume
            carrier_idx = 0

            while remaining_volume > 0 and carrier_idx < len(lane_carriers):
                carrier = lane_carriers.iloc[carrier_idx]

                # Allocate up to max_share or carrier capacity
                max_allocation = min(
                    lane_volume * max_carrier_share,
                    carrier['capacity'],
                    remaining_volume
                )

                allocation.append({
                    'lane_id': lane_id,
                    'carrier': carrier['carrier_name'],
                    'volume': max_allocation,
                    'cost': carrier['cost'],
                    'total_cost': max_allocation * carrier['cost']
                })

                remaining_volume -= max_allocation
                carrier_idx += 1

        return pd.DataFrame(allocation)

    def calculate_freight_spend(self, allocation):
        """Calculate total freight spend from allocation"""

        total_spend = allocation['total_cost'].sum()

        by_carrier = allocation.groupby('carrier').agg({
            'volume': 'sum',
            'total_cost': 'sum'
        }).sort_values('total_cost', ascending=False)

        return {
            'total_spend': total_spend,
            'by_carrier': by_carrier,
            'num_carriers': len(by_carrier)
        }
```

### Transportation RFP & Bid Analysis

```python
class FreightRFPAnalyzer:
    """
    Analyze carrier bids from RFP (Request for Proposal)

    Optimize carrier selection based on bid responses
    """

    def __init__(self, lanes_historical, carrier_bids):
        """
        Parameters:
        - lanes_historical: historical lane data (volume, spend)
        - carrier_bids: carrier responses to RFP
        """
        self.lanes = lanes_historical
        self.bids = carrier_bids

    def analyze_bids(self):
        """
        Analyze and compare carrier bids

        Returns comparison matrix
        """

        comparison = []

        for _, lane in self.lanes.iterrows():
            lane_bids = self.bids[
                (self.bids['origin'] == lane['origin']) &
                (self.bids['destination'] == lane['destination'])
            ]

            if len(lane_bids) == 0:
                continue

            # Calculate cost per load
            lane_bids['annual_cost'] = (
                lane_bids['rate'] * lane['annual_volume']
            )

            # Find current cost
            current_cost = lane['current_annual_cost']

            # Calculate savings
            lane_bids['savings'] = current_cost - lane_bids['annual_cost']
            lane_bids['savings_pct'] = (
                lane_bids['savings'] / current_cost * 100
            )

            comparison.extend(lane_bids.to_dict('records'))

        return pd.DataFrame(comparison)

    def optimize_carrier_awards(self, min_savings_pct=5,
                               max_carriers=10):
        """
        Determine optimal carrier awards from RFP

        Parameters:
        - min_savings_pct: minimum savings % to award lane
        - max_carriers: maximum number of carriers to use
        """

        bids_analyzed = self.analyze_bids()

        # Filter to bids meeting savings threshold
        qualified_bids = bids_analyzed[
            bids_analyzed['savings_pct'] >= min_savings_pct
        ]

        # Select best bid per lane
        awards = qualified_bids.loc[
            qualified_bids.groupby(['origin', 'destination'])['savings']
            .idxmax()
        ]

        # Check carrier count constraint
        carrier_counts = awards['carrier'].value_counts()

        if len(carrier_counts) > max_carriers:
            # Keep top N carriers by total savings
            top_carriers = carrier_counts.head(max_carriers).index
            awards = awards[awards['carrier'].isin(top_carriers)]

        total_savings = awards['savings'].sum()
        total_current_cost = awards['annual_cost'].sum() + total_savings

        return {
            'awards': awards,
            'total_savings': total_savings,
            'savings_percentage': total_savings / total_current_cost * 100,
            'num_carriers': len(carrier_counts),
            'lanes_awarded': len(awards)
        }

# Example usage
lanes_hist = pd.DataFrame({
    'origin': ['Chicago', 'Chicago', 'LA'],
    'destination': ['Atlanta', 'Dallas', 'Phoenix'],
    'annual_volume': [1000, 800, 600],
    'current_annual_cost': [2500000, 2000000, 1500000]
})

carrier_bids = pd.DataFrame({
    'carrier': ['Carrier_A', 'Carrier_B', 'Carrier_A', 'Carrier_C'],
    'origin': ['Chicago', 'Chicago', 'LA', 'LA'],
    'destination': ['Atlanta', 'Atlanta', 'Phoenix', 'Phoenix'],
    'rate': [2300, 2450, 2350, 2400]
})

rfp = FreightRFPAnalyzer(lanes_hist, carrier_bids)
results = rfp.optimize_carrier_awards()
print(f"Total savings: ${results['total_savings']:,.0f} "
      f"({results['savings_percentage']:.1f}%)")
```

---

## Common Challenges & Solutions

### Challenge: High Freight Costs

**Problem:**
- Freight spend is X% of revenue
- Costs increasing year-over-year
- No benchmark for comparison

**Solutions:**
- Benchmark against industry (typically 8-12% of revenue for manufacturing)
- Conduct annual RFP for primary lanes
- Implement freight audit process (catch billing errors)
- Optimize mode selection (use decision tools)
- Consolidate shipments (reduce LTL, increase TL)
- Negotiate volume discounts
- Consider contract vs. spot market mix
- Implement freight payment system (visibility + audit)

### Challenge: Poor Carrier Performance

**Problem:**
- Late deliveries
- Freight damage
- Poor communication
- Inconsistent service

**Solutions:**
- Implement carrier scorecard (on-time, damage, service)
- Set minimum performance thresholds in contracts
- Quarterly business reviews with carriers
- Diversify carrier base (not over-reliant on one)
- Build backup carrier list for each lane
- Use load boards for spot coverage
- Consider 3PL for carrier management
- Track and escalate issues systematically

### Challenge: Lack of Freight Visibility

**Problem:**
- Don't know where shipments are
- Can't predict arrival times
- Reactive vs. proactive

**Solutions:**
- Implement TMS (Transportation Management System)
- Require GPS tracking from carriers
- Use freight visibility platforms (FourKites, project44)
- Automate status updates (EDI, API integrations)
- Set up exception alerts
- Provide customer tracking portal
- Build control tower for monitoring

### Challenge: Imbalanced Lanes

**Problem:**
- Outbound heavy, few inbound loads
- Paying for empty backhauls
- Higher rates on imbalanced lanes

**Solutions:**
- Develop backhaul program (reverse logistics)
- Partner with complementary shippers
- Use freight matching platforms
- Consider intermodal for imbalanced long haul
- Accept higher cost (factor into pricing)
- Negotiate creative contracts (roundtrip pricing)
- Build dedicated fleet for balanced lanes

### Challenge: Dimensional Weight Pricing

**Problem:**
- Low-density freight penalized by dim weight
- Paying for air vs. actual weight

**Solutions:**
- Right-size packaging (reduce cube)
- Palletize efficiently (maximize density)
- Negotiate density thresholds with carriers
- Consider freight class optimization (NMFC)
- Use blanket wrap vs. pallets where possible
- Consolidate to improve density
- For parcel: reduce box sizes, eliminate void fill

---

## Tools & Technology

### Transportation Management Systems (TMS)

**Enterprise TMS:**
- **Manhattan Associates TMS**: Enterprise transportation
- **Blue Yonder TMS**: AI-powered optimization
- **Oracle Transportation Management**: Full suite
- **SAP Transportation Management**: ERP integrated
- **JDA (now Blue Yonder)**: Supply chain platform
- **MercuryGate**: Cloud TMS

**Mid-Market TMS:**
- **Kuebix**: Free to enterprise tiers
- **3Gtms**: Multi-tenant cloud TMS
- **Transplace**: Managed TMS
- **McLeod Software**: LoadMaster
- **TMW Systems**: TMWSuite

**Freight Marketplaces:**
- **Uber Freight**: Digital freight matching
- **Convoy**: Automated freight network
- **Loadsmart**: Instant freight pricing
- **Transfix**: Managed marketplace
- **CargoX**: Freight bidding platform

### Load Boards & Spot Market

- **DAT Load Board**: Industry standard
- **Truckstop.com**: Load matching
- ** 123Loadboard**: Freight posting
- **Direct Freight**: Load board network

### Freight Visibility Platforms

- **FourKites**: Real-time tracking
- **project44**: Multimodal visibility
- **FreightVerify**: Shipment tracking
- **10-4 Systems**: GPS tracking

---

## Output Format

### Freight Optimization Analysis Report

**Executive Summary:**
- Annual freight spend: $8.5M
- Target savings: $1.2M (14% reduction)
- Primary opportunities: Mode optimization, consolidation, carrier renegotiation
- Implementation timeline: 6 months

**Current State Analysis:**

| Metric | Current | Benchmark | Gap |
|--------|---------|-----------|-----|
| Freight as % of revenue | 11.5% | 9.0% | ⚠️ 2.5% higher |
| Cost per shipment | $485 | $420 | ⚠️ 15% higher |
| Truckload utilization | 72% | 85% | ⚠️ 13% lower |
| On-time delivery | 88% | 95% | ⚠️ 7% lower |
| Number of carriers | 35 | 15-20 | ⚠️ Too many |

**Freight Spend by Mode:**

| Mode | Annual Spend | % of Total | Shipments | Avg Cost |
|------|-------------|------------|-----------|----------|
| Truckload (TL) | $4.2M | 49% | 2,100 | $2,000 |
| Less-Than-Truckload | $2.8M | 33% | 8,400 | $333 |
| Parcel | $1.2M | 14% | 45,000 | $27 |
| Intermodal | $300K | 4% | 150 | $2,000 |

**Optimization Opportunities:**

1. **Mode Optimization** - Savings: $425K
   - Convert 15% of LTL to TL through consolidation
   - Use intermodal for lanes >1,200 miles
   - Optimize parcel vs. LTL breakpoint

2. **Carrier Consolidation & RFP** - Savings: $510K
   - Reduce from 35 to 20 carriers
   - Conduct RFP for top 20 lanes
   - Negotiate volume discounts

3. **Freight Consolidation** - Savings: $180K
   - Implement 2-day consolidation window
   - Build milk runs for supplier pickups
   - Pool orders by region

4. **Load Optimization** - Savings: $95K
   - Improve TL utilization (72% → 85%)
   - Better load planning and cube utilization
   - Multi-stop TL routes

**Implementation Roadmap:**

| Phase | Timeline | Initiatives | Savings |
|-------|----------|-------------|---------|
| Q1 | Months 1-3 | Mode optimization, TMS implementation | $220K |
| Q2 | Months 4-6 | Carrier RFP, contract negotiations | $510K |
| Q3 | Months 7-9 | Consolidation programs, milk runs | $280K |
| Q4 | Months 10-12 | Load optimization, continuous improvement | $190K |

**Expected Results:**

| Metric | Current | Year 1 Target | Improvement |
|--------|---------|---------------|-------------|
| Annual freight spend | $8.5M | $7.3M | -14% |
| Cost per shipment | $485 | $420 | -13% |
| TL utilization | 72% | 85% | +13 pts |
| On-time delivery | 88% | 94% | +6 pts |
| Number of carriers | 35 | 20 | -43% |

---

## Questions to Ask

If you need more context:
1. What's your annual freight spend?
2. What transportation modes do you use? (TL, LTL, parcel, etc.)
3. What are your primary shipping lanes?
4. Do you have a TMS or freight management system?
5. How many carriers do you currently use?
6. What are your service level requirements?
7. Any specific pain points? (cost, service, visibility)
8. Do you conduct regular carrier RFPs?

---

## Related Skills

- **route-optimization**: Optimize delivery routes and sequencing
- **network-design**: Optimize warehouse and DC locations
- **fleet-management**: Manage dedicated fleet operations
- **last-mile-delivery**: Final-mile delivery optimization
- **cross-docking**: Consolidation and crossdock operations
- **procurement-optimization**: Strategic sourcing and procurement
- **supply-chain-analytics**: Freight spend and performance analytics
- **contract-management**: Carrier contract negotiation and management
