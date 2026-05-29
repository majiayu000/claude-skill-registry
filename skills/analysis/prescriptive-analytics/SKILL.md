---
name: prescriptive-analytics
description: When the user wants decision support systems, recommendation engines, or prescriptive analytics. Also use when the user mentions "decision optimization," "recommendation system," "what should we do," "action recommendations," "decision support," "intelligent recommendations," "automated decisions," or "prescriptive models." For pure optimization, see optimization-modeling. For forecasting, see demand-forecasting.
---

# Prescriptive Analytics

You are an expert in prescriptive analytics and decision support systems for supply chain. Your goal is to help build systems that not only predict what will happen, but recommend what actions to take to achieve desired outcomes, optimize performance, and mitigate risks.

## Initial Assessment

Before building prescriptive analytics, understand:

1. **Decision Context**
   - What decisions need recommendations? (inventory orders, routing, pricing, allocation)
   - Who makes the decisions? (planners, buyers, managers, automated systems)
   - What are the goals? (minimize cost, maximize service, balance multiple objectives)
   - Decision frequency? (real-time, daily, weekly, strategic)

2. **Current State**
   - How are decisions made today? (manual, spreadsheets, basic rules, gut feel)
   - What information is used? (historical data, forecasts, constraints)
   - Pain points? (inconsistent decisions, suboptimal outcomes, too slow)
   - Trust in recommendations? (skepticism vs. acceptance)

3. **Analytics Maturity**
   - Descriptive analytics in place? (what happened)
   - Diagnostic analytics available? (why it happened)
   - Predictive analytics working? (what will happen)
   - Ready for prescriptive? (what should we do)

4. **Technical Requirements**
   - Real-time vs. batch recommendations?
   - Explainability requirements? (black box vs. transparent)
   - Integration with existing systems?
   - Human-in-the-loop vs. fully automated?

---

## Prescriptive Analytics Framework

### Analytics Evolution Pyramid

```
                    ┌─────────────────────────┐
                    │   PRESCRIPTIVE          │
                    │   What should we do?    │
                    │   • Recommendations     │
                    │   • Optimization        │
                    │   • Decision automation │
                    └─────────────────────────┘
                            ▲
                    ┌───────────────────────────┐
                    │   PREDICTIVE              │
                    │   What will happen?       │
                    │   • Forecasting           │
                    │   • Classification        │
                    │   • Risk scoring          │
                    └───────────────────────────┘
                            ▲
                    ┌─────────────────────────────┐
                    │   DIAGNOSTIC                │
                    │   Why did it happen?        │
                    │   • Root cause analysis     │
                    │   • Correlation             │
                    │   • Pattern recognition     │
                    └─────────────────────────────┘
                            ▲
                    ┌───────────────────────────────┐
                    │   DESCRIPTIVE                 │
                    │   What happened?              │
                    │   • Historical reporting      │
                    │   • KPIs & dashboards         │
                    │   • Data aggregation          │
                    └───────────────────────────────┘
```

### Components of Prescriptive Analytics

**1. Predictive Models**
- Forecast future states (demand, lead times, costs)
- Predict probabilities (delays, defects, stockouts)
- Input to optimization and recommendations

**2. Optimization Engines**
- Mathematical optimization (LP, MIP, NLP)
- Constraint programming
- Heuristics and metaheuristics
- Multi-objective optimization

**3. Decision Rules & Logic**
- Business rules engine
- Policy constraints
- Feasibility checks
- Approval workflows

**4. Explanation & Confidence**
- Why this recommendation?
- Confidence levels
- Sensitivity analysis
- Alternative scenarios

**5. Action Execution**
- API integrations
- Automated workflows
- Human review interface
- Monitoring and feedback

---

## Inventory Replenishment Recommendations

### Intelligent Reorder Recommendation System

```python
import pandas as pd
import numpy as np
from scipy import stats
from datetime import datetime, timedelta
import joblib

class IntelligentReplenishmentAdvisor:
    """
    Prescriptive system for inventory replenishment recommendations

    Combines:
    - Demand forecasting (predictive)
    - Inventory optimization (prescriptive)
    - Business rules (constraints)
    - Explainability (trust)
    """

    def __init__(self):
        self.forecast_model = None
        self.optimization_config = {}
        self.business_rules = {}
        self.recommendations = []

    def load_models(self):
        """Load pre-trained ML models"""
        self.forecast_model = joblib.load('demand_forecast_model.pkl')

    def forecast_demand(self, sku, horizon_days=30):
        """
        Predict demand for SKU over horizon

        Returns distribution (mean, std) not just point estimate
        """

        # Get historical data and features
        features = self.get_forecast_features(sku)

        # Predict mean demand
        mean_demand = self.forecast_model.predict(features)[0]

        # Estimate uncertainty (from model or historical error)
        forecast_error = 0.15  # 15% coefficient of variation
        std_demand = mean_demand * forecast_error

        return {
            'sku': sku,
            'horizon_days': horizon_days,
            'mean_daily_demand': mean_demand / horizon_days,
            'std_daily_demand': std_demand / np.sqrt(horizon_days),
            'total_forecast': mean_demand,
            'confidence_interval_95': (
                mean_demand - 1.96 * std_demand,
                mean_demand + 1.96 * std_demand
            )
        }

    def get_forecast_features(self, sku):
        """Create feature vector for demand forecasting"""
        # Placeholder - would pull from database and engineer features
        return np.array([[1.0] * 20])  # Example feature vector

    def calculate_optimal_reorder(self, sku, current_inventory, forecast,
                                  lead_time, service_level=0.95):
        """
        Calculate optimal reorder quantity and timing

        Uses:
        - EOQ for quantity optimization
        - Service level for safety stock
        - Lead time for reorder point
        """

        # Get SKU parameters
        unit_cost = self.get_unit_cost(sku)
        order_cost = 100  # $ per order
        holding_cost_rate = 0.25  # 25% annually
        holding_cost = unit_cost * holding_cost_rate

        # Economic Order Quantity (EOQ)
        annual_demand = forecast['mean_daily_demand'] * 365
        eoq = np.sqrt((2 * annual_demand * order_cost) / holding_cost)

        # Safety stock based on service level
        z_score = stats.norm.ppf(service_level)
        std_during_lt = forecast['std_daily_demand'] * np.sqrt(lead_time)
        safety_stock = z_score * std_during_lt

        # Reorder point
        expected_demand_lt = forecast['mean_daily_demand'] * lead_time
        reorder_point = expected_demand_lt + safety_stock

        # Inventory position
        inventory_position = current_inventory  # Simplified (+ on_order in practice)

        # Calculate recommended order quantity
        if inventory_position < reorder_point:
            # Order up to EOQ (or more if severely understocked)
            target_inventory = reorder_point + eoq
            recommended_order = max(0, target_inventory - inventory_position)
        else:
            recommended_order = 0

        return {
            'sku': sku,
            'current_inventory': current_inventory,
            'reorder_point': reorder_point,
            'safety_stock': safety_stock,
            'eoq': eoq,
            'recommended_order_quantity': recommended_order,
            'inventory_position': inventory_position,
            'days_of_supply': inventory_position / forecast['mean_daily_demand'],
            'stockout_risk': self.calculate_stockout_risk(
                inventory_position, forecast, lead_time
            )
        }

    def calculate_stockout_risk(self, inventory_position, forecast, lead_time):
        """
        Calculate probability of stockout during lead time

        P(Demand during LT > Inventory Position)
        """

        mean_demand_lt = forecast['mean_daily_demand'] * lead_time
        std_demand_lt = forecast['std_daily_demand'] * np.sqrt(lead_time)

        if std_demand_lt == 0:
            return 0 if inventory_position >= mean_demand_lt else 1

        z = (inventory_position - mean_demand_lt) / std_demand_lt
        stockout_prob = 1 - stats.norm.cdf(z)

        return stockout_prob

    def apply_business_rules(self, recommendation):
        """
        Apply business rules and constraints

        Examples:
        - Minimum order quantity (MOQ)
        - Case pack constraints
        - Budget limits
        - Supplier capacity
        - Shelf life considerations
        """

        sku = recommendation['sku']

        # MOQ constraint
        moq = self.get_moq(sku)
        if recommendation['recommended_order_quantity'] > 0 and \
           recommendation['recommended_order_quantity'] < moq:
            recommendation['recommended_order_quantity'] = moq
            recommendation['constraints_applied'].append('MOQ')

        # Case pack rounding
        case_pack = self.get_case_pack(sku)
        if case_pack > 0:
            recommended = recommendation['recommended_order_quantity']
            rounded = np.ceil(recommended / case_pack) * case_pack
            recommendation['recommended_order_quantity'] = rounded
            if rounded != recommended:
                recommendation['constraints_applied'].append('Case Pack')

        # Budget check
        unit_cost = self.get_unit_cost(sku)
        order_value = recommendation['recommended_order_quantity'] * unit_cost

        if order_value > self.business_rules.get('max_order_value', float('inf')):
            recommendation['requires_approval'] = True
            recommendation['approval_reason'] = f"Order value ${order_value:,.0f} exceeds limit"

        return recommendation

    def generate_explanation(self, recommendation):
        """
        Generate human-readable explanation for recommendation

        Critical for user trust and adoption
        """

        sku = recommendation['sku']
        order_qty = recommendation['recommended_order_quantity']

        if order_qty == 0:
            explanation = f"No order needed. Current inventory ({recommendation['current_inventory']} units) " \
                         f"is above reorder point ({recommendation['reorder_point']:.0f} units). " \
                         f"You have {recommendation['days_of_supply']:.1f} days of supply."

            return {
                'action': 'DO NOT ORDER',
                'explanation': explanation,
                'confidence': 'High',
                'risk_level': 'Low'
            }

        else:
            stockout_risk = recommendation['stockout_risk']

            explanation = f"Order {order_qty:.0f} units. " \
                         f"Current inventory ({recommendation['current_inventory']} units) " \
                         f"is below reorder point ({recommendation['reorder_point']:.0f} units). " \
                         f"Without ordering, stockout risk is {stockout_risk:.1%}. " \
                         f"Recommended quantity optimizes ordering and holding costs (EOQ)."

            # Risk assessment
            if stockout_risk > 0.2:
                risk_level = 'HIGH'
                urgency = 'URGENT'
            elif stockout_risk > 0.05:
                risk_level = 'MEDIUM'
                urgency = 'Soon'
            else:
                risk_level = 'LOW'
                urgency = 'Normal'

            return {
                'action': 'ORDER',
                'quantity': order_qty,
                'explanation': explanation,
                'urgency': urgency,
                'risk_level': risk_level,
                'stockout_risk': f"{stockout_risk:.1%}",
                'days_until_stockout': recommendation['days_of_supply']
            }

    def generate_recommendations(self, sku_list):
        """
        Generate recommendations for list of SKUs

        Returns prioritized action list
        """

        recommendations = []

        for sku in sku_list:
            # Get current state
            current_inventory = self.get_current_inventory(sku)
            lead_time = self.get_lead_time(sku)

            # Forecast demand
            forecast = self.forecast_demand(sku, horizon_days=30)

            # Calculate optimal reorder
            recommendation = self.calculate_optimal_reorder(
                sku, current_inventory, forecast, lead_time
            )

            # Apply business rules
            recommendation['constraints_applied'] = []
            recommendation['requires_approval'] = False
            recommendation = self.apply_business_rules(recommendation)

            # Generate explanation
            explanation = self.generate_explanation(recommendation)
            recommendation['explanation'] = explanation

            recommendations.append(recommendation)

        # Prioritize recommendations
        recommendations_df = pd.DataFrame(recommendations)

        # Sort by urgency and risk
        recommendations_df['priority_score'] = (
            recommendations_df['stockout_risk'] * 100 +
            (1 / recommendations_df['days_of_supply']) * 10
        )

        recommendations_df = recommendations_df.sort_values(
            'priority_score',
            ascending=False
        )

        return recommendations_df

    def get_current_inventory(self, sku):
        """Get current inventory from system"""
        # In production: query WMS/ERP
        return np.random.randint(50, 500)

    def get_lead_time(self, sku):
        """Get supplier lead time"""
        return 14  # days

    def get_unit_cost(self, sku):
        """Get unit cost"""
        return 25.00

    def get_moq(self, sku):
        """Get minimum order quantity"""
        return 100

    def get_case_pack(self, sku):
        """Get case pack quantity"""
        return 50

# Example usage
advisor = IntelligentReplenishmentAdvisor()
advisor.load_models()

# Generate recommendations
sku_list = ['SKU_001', 'SKU_002', 'SKU_003', 'SKU_004', 'SKU_005']
recommendations = advisor.generate_recommendations(sku_list)

# Display top recommendations
print("\n" + "="*80)
print("INTELLIGENT REPLENISHMENT RECOMMENDATIONS")
print("="*80 + "\n")

for idx, row in recommendations.head(10).iterrows():
    print(f"SKU: {row['sku']}")
    print(f"  Action: {row['explanation']['action']}")
    if row['explanation']['action'] == 'ORDER':
        print(f"  Quantity: {row['explanation']['quantity']:.0f} units")
        print(f"  Urgency: {row['explanation']['urgency']}")
        print(f"  Risk: {row['explanation']['risk_level']} (Stockout risk: {row['explanation']['stockout_risk']})")
    print(f"  Explanation: {row['explanation']['explanation']}")
    if row['requires_approval']:
        print(f"  ⚠️  Requires Approval: {row['approval_reason']}")
    print()
```

---

## Route Optimization Recommendations

### Intelligent Route Planning System

```python
from scipy.spatial import distance_matrix
from sklearn.cluster import KMeans
import numpy as np

class RouteOptimizationAdvisor:
    """
    Prescriptive system for delivery route recommendations

    Provides:
    - Optimal route sequences
    - Vehicle assignments
    - Time window compliance
    - Real-time adjustments
    """

    def __init__(self, config):
        self.config = config
        self.routes = []

    def generate_route_recommendations(self, orders, vehicles, constraints):
        """
        Generate optimal routing recommendations

        orders: list of delivery orders with locations and time windows
        vehicles: available vehicles with capacities
        constraints: max driving time, time windows, capacity
        """

        # Step 1: Cluster orders by geography
        clusters = self.cluster_orders_geographically(
            orders,
            n_clusters=len(vehicles)
        )

        # Step 2: Assign clusters to vehicles
        vehicle_assignments = self.assign_clusters_to_vehicles(
            clusters, vehicles
        )

        # Step 3: Optimize sequence within each route
        optimized_routes = []

        for vehicle_id, cluster_orders in vehicle_assignments.items():
            route = self.optimize_route_sequence(
                cluster_orders,
                vehicles[vehicle_id],
                constraints
            )

            route['vehicle_id'] = vehicle_id
            route['recommendations'] = self.generate_route_explanation(route)

            optimized_routes.append(route)

        return optimized_routes

    def cluster_orders_geographically(self, orders, n_clusters):
        """
        Cluster orders by location for vehicle assignment

        Uses K-means clustering
        """

        # Extract coordinates
        coords = np.array([[o['lat'], o['lon']] for o in orders])

        # Cluster
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        labels = kmeans.fit_predict(coords)

        # Group orders by cluster
        clusters = {}
        for i, label in enumerate(labels):
            if label not in clusters:
                clusters[label] = []
            clusters[label].append(orders[i])

        return clusters

    def assign_clusters_to_vehicles(self, clusters, vehicles):
        """
        Assign clusters to vehicles based on capacity and constraints
        """

        assignments = {}

        for i, (cluster_id, orders) in enumerate(clusters.items()):
            vehicle_id = list(vehicles.keys())[i]

            # Check capacity
            total_volume = sum(o['volume'] for o in orders)
            total_weight = sum(o['weight'] for o in orders)

            vehicle = vehicles[vehicle_id]

            if total_volume > vehicle['capacity_volume'] or \
               total_weight > vehicle['capacity_weight']:
                # Need to split cluster or use larger vehicle
                # Simplified: just assign and flag
                print(f"WARNING: Cluster {cluster_id} exceeds vehicle {vehicle_id} capacity")

            assignments[vehicle_id] = orders

        return assignments

    def optimize_route_sequence(self, orders, vehicle, constraints):
        """
        Optimize stop sequence using nearest neighbor heuristic

        For production: use proper VRP solver (OR-Tools, Gurobi)
        """

        if not orders:
            return {
                'stops': [],
                'total_distance': 0,
                'total_time': 0,
                'utilization': 0
            }

        # Start from depot
        depot = {'lat': self.config['depot_lat'],
                'lon': self.config['depot_lon'],
                'order_id': 'DEPOT'}

        current_location = depot
        remaining_orders = orders.copy()
        route_sequence = [depot]
        total_distance = 0

        # Nearest neighbor heuristic
        while remaining_orders:
            # Find nearest order
            nearest_order = min(
                remaining_orders,
                key=lambda o: self.calculate_distance(
                    current_location['lat'], current_location['lon'],
                    o['lat'], o['lon']
                )
            )

            distance = self.calculate_distance(
                current_location['lat'], current_location['lon'],
                nearest_order['lat'], nearest_order['lon']
            )

            total_distance += distance
            route_sequence.append(nearest_order)
            remaining_orders.remove(nearest_order)
            current_location = nearest_order

        # Return to depot
        distance_to_depot = self.calculate_distance(
            current_location['lat'], current_location['lon'],
            depot['lat'], depot['lon']
        )
        total_distance += distance_to_depot
        route_sequence.append(depot)

        # Calculate metrics
        total_time = total_distance / vehicle.get('avg_speed_mph', 30) * 60  # minutes
        total_time += len(orders) * constraints.get('stop_time_minutes', 15)

        total_volume = sum(o['volume'] for o in orders)
        utilization = total_volume / vehicle['capacity_volume'] * 100

        return {
            'stops': route_sequence,
            'total_distance_miles': total_distance,
            'total_time_minutes': total_time,
            'utilization_pct': utilization,
            'num_stops': len(orders),
            'feasible': total_time <= constraints.get('max_driving_time_minutes', 480)
        }

    def calculate_distance(self, lat1, lon1, lat2, lon2):
        """Calculate distance between two coordinates (Haversine)"""

        from math import radians, sin, cos, sqrt, atan2

        R = 3959  # Earth radius in miles

        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))

        return R * c

    def generate_route_explanation(self, route):
        """
        Generate explanation and recommendations for route
        """

        recommendations = {
            'summary': f"{route['num_stops']} stops, "
                      f"{route['total_distance_miles']:.1f} miles, "
                      f"{route['total_time_minutes']/60:.1f} hours",
            'utilization': f"{route['utilization_pct']:.0f}% capacity used",
            'feasibility': 'FEASIBLE' if route['feasible'] else 'INFEASIBLE',
            'improvements': []
        }

        # Identify improvement opportunities
        if route['utilization_pct'] < 70:
            recommendations['improvements'].append(
                f"Low utilization ({route['utilization_pct']:.0f}%). "
                "Consider consolidating with another route."
            )

        if route['total_time_minutes'] > 420:  # 7 hours
            recommendations['improvements'].append(
                "Long route duration. Consider splitting into two routes."
            )

        if not route['feasible']:
            recommendations['improvements'].append(
                "Route exceeds maximum driving time. MUST split or reschedule."
            )

        return recommendations

# Example usage
config = {
    'depot_lat': 34.0522,
    'depot_lon': -118.2437
}

advisor = RouteOptimizationAdvisor(config)

# Sample orders
orders = [
    {'order_id': 'O1', 'lat': 34.1, 'lon': -118.3, 'volume': 100, 'weight': 50},
    {'order_id': 'O2', 'lat': 34.2, 'lon': -118.1, 'volume': 150, 'weight': 75},
    {'order_id': 'O3', 'lat': 34.0, 'lon': -118.4, 'volume': 80, 'weight': 40},
]

vehicles = {
    'V1': {'capacity_volume': 1000, 'capacity_weight': 2000, 'avg_speed_mph': 30},
    'V2': {'capacity_volume': 800, 'capacity_weight': 1500, 'avg_speed_mph': 30}
}

constraints = {
    'max_driving_time_minutes': 480,  # 8 hours
    'stop_time_minutes': 15
}

routes = advisor.generate_route_recommendations(orders, vehicles, constraints)

for route in routes:
    print(f"\nVehicle {route['vehicle_id']}:")
    print(f"  {route['recommendations']['summary']}")
    print(f"  {route['recommendations']['utilization']}")
    print(f"  Status: {route['recommendations']['feasibility']}")
    if route['recommendations']['improvements']:
        print("  Improvements:")
        for imp in route['recommendations']['improvements']:
            print(f"    - {imp}")
```

---

## Supplier Selection Recommendations

```python
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

class SupplierSelectionAdvisor:
    """
    Prescriptive system for supplier selection recommendations

    Multi-criteria decision analysis considering:
    - Cost
    - Quality
    - Delivery performance
    - Capacity
    - Risk
    """

    def __init__(self):
        self.scaler = MinMaxScaler()

    def evaluate_suppliers(self, rfq_data, suppliers_data, criteria_weights):
        """
        Evaluate and rank suppliers for RFQ

        rfq_data: RFQ details (product, quantity, requirements)
        suppliers_data: Supplier profiles and historical performance
        criteria_weights: importance weights for each criterion
        """

        evaluations = []

        for supplier in suppliers_data:
            evaluation = self.evaluate_single_supplier(
                supplier, rfq_data, criteria_weights
            )
            evaluations.append(evaluation)

        # Convert to DataFrame
        eval_df = pd.DataFrame(evaluations)

        # Calculate weighted score
        eval_df['total_score'] = 0

        for criterion, weight in criteria_weights.items():
            if f'{criterion}_score' in eval_df.columns:
                eval_df['total_score'] += eval_df[f'{criterion}_score'] * weight

        # Rank
        eval_df = eval_df.sort_values('total_score', ascending=False)

        # Generate recommendations
        recommendations = self.generate_supplier_recommendations(
            eval_df, rfq_data
        )

        return eval_df, recommendations

    def evaluate_single_supplier(self, supplier, rfq_data, criteria_weights):
        """
        Evaluate single supplier across multiple criteria
        """

        evaluation = {
            'supplier_id': supplier['supplier_id'],
            'supplier_name': supplier['name']
        }

        # 1. Cost Score (lower cost = higher score)
        quoted_price = supplier.get('quoted_price', float('inf'))
        if quoted_price < float('inf'):
            # Normalize: score = 100 * (1 - (price - min_price) / (max_price - min_price))
            evaluation['quoted_price'] = quoted_price
            evaluation['cost_score'] = 100 - min(quoted_price / 100, 100)  # Simplified
        else:
            evaluation['cost_score'] = 0

        # 2. Quality Score (based on historical defect rate)
        defect_rate = supplier.get('historical_defect_rate', 0.05)
        evaluation['defect_rate'] = defect_rate
        evaluation['quality_score'] = max(0, 100 - defect_rate * 1000)

        # 3. Delivery Performance (OTD rate)
        otd_rate = supplier.get('on_time_delivery_rate', 0.85)
        evaluation['otd_rate'] = otd_rate
        evaluation['delivery_score'] = otd_rate * 100

        # 4. Capacity Match
        supplier_capacity = supplier.get('available_capacity', 0)
        required_quantity = rfq_data['quantity']
        capacity_ratio = min(supplier_capacity / required_quantity, 1.0)
        evaluation['capacity_ratio'] = capacity_ratio
        evaluation['capacity_score'] = capacity_ratio * 100

        # 5. Risk Score (inverse - lower risk = higher score)
        risk_factors = {
            'financial_health': supplier.get('financial_rating', 'BBB'),
            'geographic_risk': supplier.get('country_risk', 'Low'),
            'single_source': supplier.get('is_sole_source', False)
        }

        risk_score = self.calculate_risk_score(risk_factors)
        evaluation['risk_score'] = 100 - risk_score

        # 6. Lead Time (shorter = better)
        lead_time = supplier.get('lead_time_days', 30)
        evaluation['lead_time_days'] = lead_time
        evaluation['lead_time_score'] = max(0, 100 - lead_time)

        # 7. Past Relationship
        past_orders = supplier.get('past_orders_count', 0)
        evaluation['relationship_score'] = min(past_orders / 10, 1.0) * 100

        return evaluation

    def calculate_risk_score(self, risk_factors):
        """
        Calculate overall risk score (0-100, higher = more risk)
        """

        risk_score = 0

        # Financial risk
        financial_ratings = {'AAA': 0, 'AA': 10, 'A': 20, 'BBB': 30,
                           'BB': 50, 'B': 70, 'CCC': 90}
        risk_score += financial_ratings.get(risk_factors['financial_health'], 40)

        # Geographic risk
        geo_risk = {'Low': 0, 'Medium': 20, 'High': 40}
        risk_score += geo_risk.get(risk_factors['geographic_risk'], 20)

        # Single source risk
        if risk_factors['single_source']:
            risk_score += 30

        return min(risk_score, 100)

    def generate_supplier_recommendations(self, eval_df, rfq_data):
        """
        Generate actionable supplier recommendations
        """

        recommendations = []

        # Top recommendation
        top_supplier = eval_df.iloc[0]

        rec = {
            'rank': 1,
            'supplier': top_supplier['supplier_name'],
            'action': 'AWARD',
            'rationale': f"Best overall score ({top_supplier['total_score']:.0f}/100). "
                        f"Strong performance in key areas: "
                        f"Quality ({top_supplier['quality_score']:.0f}), "
                        f"Delivery ({top_supplier['delivery_score']:.0f}), "
                        f"Price (${top_supplier['quoted_price']:.2f}).",
            'confidence': 'High' if top_supplier['total_score'] > 80 else 'Medium'
        }

        recommendations.append(rec)

        # Secondary recommendation (backup supplier)
        if len(eval_df) > 1:
            second_supplier = eval_df.iloc[1]

            rec = {
                'rank': 2,
                'supplier': second_supplier['supplier_name'],
                'action': 'BACKUP',
                'rationale': f"Strong alternative ({second_supplier['total_score']:.0f}/100). "
                            "Recommend as backup supplier for risk mitigation.",
                'confidence': 'Medium'
            }

            recommendations.append(rec)

        # Dual sourcing recommendation
        if rfq_data['quantity'] > 1000 and len(eval_df) >= 2:
            recommendations.append({
                'supplier': f"{eval_df.iloc[0]['supplier_name']} + {eval_df.iloc[1]['supplier_name']}",
                'action': 'DUAL SOURCE',
                'rationale': f"Large volume ({rfq_data['quantity']} units) justifies dual sourcing "
                            "for risk mitigation. Recommend 70/30 split.",
                'split': {eval_df.iloc[0]['supplier_name']: 0.7,
                         eval_df.iloc[1]['supplier_name']: 0.3}
            })

        return recommendations

# Example usage
rfq_data = {
    'rfq_id': 'RFQ-2025-001',
    'product': 'Widget A',
    'quantity': 10000,
    'delivery_date': '2025-03-01'
}

suppliers_data = [
    {
        'supplier_id': 'S1',
        'name': 'Acme Corp',
        'quoted_price': 45.00,
        'historical_defect_rate': 0.02,
        'on_time_delivery_rate': 0.95,
        'available_capacity': 15000,
        'financial_rating': 'AA',
        'country_risk': 'Low',
        'is_sole_source': False,
        'lead_time_days': 21,
        'past_orders_count': 25
    },
    {
        'supplier_id': 'S2',
        'name': 'GlobalTech Inc',
        'quoted_price': 42.00,
        'historical_defect_rate': 0.05,
        'on_time_delivery_rate': 0.88,
        'available_capacity': 12000,
        'financial_rating': 'BBB',
        'country_risk': 'Medium',
        'is_sole_source': False,
        'lead_time_days': 35,
        'past_orders_count': 10
    },
    {
        'supplier_id': 'S3',
        'name': 'Reliable Parts Co',
        'quoted_price': 48.00,
        'historical_defect_rate': 0.01,
        'on_time_delivery_rate': 0.98,
        'available_capacity': 20000,
        'financial_rating': 'AAA',
        'country_risk': 'Low',
        'is_sole_source': False,
        'lead_time_days': 14,
        'past_orders_count': 50
    }
]

criteria_weights = {
    'cost': 0.30,
    'quality': 0.25,
    'delivery': 0.20,
    'capacity': 0.10,
    'risk': 0.10,
    'lead_time': 0.05
}

advisor = SupplierSelectionAdvisor()
evaluations, recommendations = advisor.evaluate_suppliers(
    rfq_data, suppliers_data, criteria_weights
)

print("\n" + "="*80)
print("SUPPLIER SELECTION RECOMMENDATIONS")
print("="*80 + "\n")

print("Supplier Scores:\n")
print(evaluations[['supplier_name', 'total_score', 'quoted_price',
                  'quality_score', 'delivery_score']].to_string(index=False))

print("\n\nRecommendations:\n")
for rec in recommendations:
    print(f"Rank {rec.get('rank', 'N/A')}: {rec['supplier']}")
    print(f"  Action: {rec['action']}")
    print(f"  Rationale: {rec['rationale']}")
    if 'split' in rec:
        print(f"  Split: {rec['split']}")
    print()
```

---

## Real-Time Decision Support

### Dynamic Pricing Recommendations

```python
import numpy as np
from datetime import datetime, timedelta

class DynamicPricingAdvisor:
    """
    Real-time prescriptive pricing recommendations

    Considers:
    - Current inventory levels
    - Demand forecast
    - Competitor prices
    - Shelf life / expiration
    - Profit margins
    """

    def __init__(self, config):
        self.config = config

    def recommend_price(self, product, current_price, context):
        """
        Recommend optimal price for product

        context: dict with market conditions, inventory, etc.
        """

        # Extract context
        inventory_level = context['inventory_level']
        days_until_expiry = context.get('days_until_expiry', 365)
        competitor_price = context.get('competitor_price', current_price)
        recent_sales_velocity = context['recent_sales_velocity']
        target_inventory = context.get('target_inventory', 100)

        # Calculate elasticity-based recommendation
        base_recommendation = self.calculate_elasticity_price(
            product, current_price, recent_sales_velocity
        )

        # Adjust for inventory position
        if inventory_level > target_inventory * 1.5:
            # Excess inventory - recommend discount
            price_adjustment = -0.10  # 10% discount
            reason = "Excess inventory"

        elif inventory_level < target_inventory * 0.5:
            # Low inventory - can increase price
            price_adjustment = 0.05  # 5% premium
            reason = "Low inventory"

        else:
            price_adjustment = 0
            reason = "Optimal inventory level"

        # Adjust for perishability
        if days_until_expiry < 7:
            # Urgent - aggressive discount
            price_adjustment = min(price_adjustment, -0.25)
            reason += ", Near expiration"

        elif days_until_expiry < 30:
            # Moderate urgency
            price_adjustment = min(price_adjustment, -0.10)
            reason += ", Approaching expiration"

        # Competitive positioning
        if competitor_price < current_price * 0.95:
            # Competitor significantly cheaper
            price_adjustment = min(price_adjustment, -0.05)
            reason += ", Competitor underpricing"

        # Calculate recommended price
        recommended_price = current_price * (1 + price_adjustment)

        # Enforce min/max constraints
        min_price = product.get('min_price', current_price * 0.7)
        max_price = product.get('max_price', current_price * 1.3)

        recommended_price = np.clip(recommended_price, min_price, max_price)

        # Calculate expected impact
        impact = self.estimate_price_impact(
            current_price, recommended_price,
            recent_sales_velocity, inventory_level
        )

        return {
            'product_id': product['product_id'],
            'current_price': current_price,
            'recommended_price': recommended_price,
            'price_change_pct': (recommended_price - current_price) / current_price * 100,
            'reason': reason,
            'expected_impact': impact,
            'confidence': self.calculate_confidence(context),
            'urgency': self.calculate_urgency(days_until_expiry, inventory_level, target_inventory)
        }

    def calculate_elasticity_price(self, product, current_price, sales_velocity):
        """
        Calculate price based on demand elasticity

        Price elasticity = % change in quantity / % change in price
        """

        # Get historical elasticity (would be learned from data)
        elasticity = product.get('price_elasticity', -1.5)

        # If sales are low, consider lowering price
        if sales_velocity < product.get('target_velocity', 10):
            # Reduce price to stimulate demand
            return current_price * 0.95
        else:
            return current_price

    def estimate_price_impact(self, current_price, new_price, sales_velocity, inventory):
        """
        Estimate impact of price change
        """

        price_change = (new_price - current_price) / current_price

        # Assume price elasticity of -1.5 (10% price cut → 15% sales increase)
        elasticity = -1.5
        demand_change = price_change * elasticity

        new_sales_velocity = sales_velocity * (1 + demand_change)

        # Calculate revenue impact
        current_revenue = current_price * sales_velocity * 30  # 30 days
        new_revenue = new_price * new_sales_velocity * 30

        # Calculate inventory impact (days to sell out)
        current_days_to_sellout = inventory / sales_velocity if sales_velocity > 0 else 999
        new_days_to_sellout = inventory / new_sales_velocity if new_sales_velocity > 0 else 999

        return {
            'revenue_change': new_revenue - current_revenue,
            'revenue_change_pct': (new_revenue - current_revenue) / current_revenue * 100,
            'new_sales_velocity': new_sales_velocity,
            'demand_change_pct': demand_change * 100,
            'current_days_to_sellout': current_days_to_sellout,
            'new_days_to_sellout': new_days_to_sellout
        }

    def calculate_confidence(self, context):
        """Calculate confidence in recommendation"""

        # Confidence based on data quality and market stability
        data_points = context.get('historical_data_points', 0)

        if data_points > 100:
            return 'High'
        elif data_points > 30:
            return 'Medium'
        else:
            return 'Low'

    def calculate_urgency(self, days_until_expiry, inventory, target):
        """Calculate urgency of price action"""

        if days_until_expiry < 7 or inventory > target * 2:
            return 'URGENT'
        elif days_until_expiry < 30 or inventory > target * 1.5:
            return 'High'
        else:
            return 'Normal'

# Example usage
config = {}
advisor = DynamicPricingAdvisor(config)

product = {
    'product_id': 'P001',
    'name': 'Fresh Strawberries',
    'price_elasticity': -1.8,
    'min_price': 3.00,
    'max_price': 6.00
}

context = {
    'inventory_level': 500,
    'target_inventory': 200,
    'days_until_expiry': 5,
    'competitor_price': 4.50,
    'recent_sales_velocity': 30,  # units per day
    'historical_data_points': 150
}

recommendation = advisor.recommend_price(product, current_price=4.99, context=context)

print("\n" + "="*80)
print("DYNAMIC PRICING RECOMMENDATION")
print("="*80 + "\n")

print(f"Product: {product['name']}")
print(f"Current Price: ${recommendation['current_price']:.2f}")
print(f"Recommended Price: ${recommendation['recommended_price']:.2f}")
print(f"Change: {recommendation['price_change_pct']:+.1f}%")
print(f"\nReason: {recommendation['reason']}")
print(f"Urgency: {recommendation['urgency']}")
print(f"Confidence: {recommendation['confidence']}")

print(f"\nExpected Impact:")
impact = recommendation['expected_impact']
print(f"  Revenue Change: ${impact['revenue_change']:+,.0f} ({impact['revenue_change_pct']:+.1f}%)")
print(f"  Demand Change: {impact['demand_change_pct']:+.1f}%")
print(f"  Days to Sellout: {impact['current_days_to_sellout']:.1f} → {impact['new_days_to_sellout']:.1f}")
```

---

## Tools & Technologies

### Decision Support Platforms

**Commercial:**
- **IBM Decision Optimization**: CPLEX-based prescriptive analytics
- **SAS Decision Manager**: Business rules and optimization
- **Oracle Prescriptive Analytics**: Embedded optimization
- **Gurobi Optimizer**: Mathematical optimization
- **River Logic**: Prescriptive analytics platform

**Supply Chain Specific:**
- **Blue Yonder**: AI-driven supply chain decisions
- **o9 Solutions**: Integrated planning and decision intelligence
- **Kinaxis RapidResponse**: Concurrent planning with recommendations
- **LLamasoft Supply Chain Guru**: Network optimization
- **Coupa**: Procurement and sourcing recommendations

### Python Libraries

**Optimization:**
- `pulp`: Linear programming
- `pyomo`: Optimization modeling
- `cvxpy`: Convex optimization
- `scipy.optimize`: Scientific optimization
- `OR-Tools (Google)`: Combinatorial optimization

**Machine Learning:**
- `scikit-learn`: ML models
- `xgboost`, `lightgbm`: Gradient boosting
- `tensorflow`/`pytorch`: Deep learning

**Decision Trees:**
- `dtreeviz`: Decision tree visualization
- `sklearn.tree`: Decision trees
- `graphviz`: Graph visualization

**Explainability:**
- `shap`: SHAP values for model interpretation
- `lime`: Local interpretable model explanations
- `eli5`: Model explanation library

---

## Common Challenges & Solutions

### Challenge: Lack of Trust in Recommendations

**Problem:**
- Users don't trust "black box" recommendations
- Skepticism about ML/optimization
- Prefer manual decision-making

**Solutions:**
- Provide clear explanations (WHY this recommendation)
- Show confidence levels
- Allow human override with feedback loop
- Start with decision support, not automation
- Visualize trade-offs and alternatives
- Demonstrate value through A/B testing

### Challenge: Model Drift and Changing Conditions

**Problem:**
- Business conditions change
- Models become outdated
- Recommendations no longer optimal

**Solutions:**
- Continuous monitoring of recommendation quality
- Regular model retraining
- Adaptive learning from user feedback
- Scenario-based recommendations (what-if)
- Human-in-the-loop validation

### Challenge: Integration with Existing Systems

**Problem:**
- Legacy systems don't support prescriptive analytics
- Data silos and quality issues
- IT resistance to new tools

**Solutions:**
- API-first architecture
- Start with standalone decision support tool
- Gradual integration with core systems
- Data quality improvement program
- Executive sponsorship and change management

### Challenge: Conflicting Objectives

**Problem:**
- Minimize cost vs. maximize service
- Short-term vs. long-term optimization
- Local vs. global optimization

**Solutions:**
- Multi-objective optimization (Pareto frontier)
- Weighted scoring with stakeholder input
- Scenario analysis showing trade-offs
- Clear definition of priorities
- Hierarchical decision-making

---

## Output Format

### Prescriptive Analytics Report

**Executive Summary:**
- Key recommendations
- Expected impact
- Confidence level
- Required actions

**Recommendations:**

| Rank | Action | Target | Expected Impact | Confidence | Urgency |
|------|--------|--------|-----------------|------------|---------|
| 1 | Order 500 units SKU_001 | Inventory | Prevent $50K stockout | High | URGENT |
| 2 | Reduce price 10% on SKU_002 | Sales | +$25K revenue | Medium | High |
| 3 | Switch to Supplier B | Cost | -$15K/year | High | Normal |

**Detailed Analysis:**

For each recommendation:
- **Action**: What to do
- **Rationale**: Why (based on data and models)
- **Expected Outcome**: Quantified impact
- **Confidence**: High/Medium/Low with reasoning
- **Alternatives**: Other options considered
- **Risks**: What could go wrong
- **Implementation**: How to execute

**Supporting Data:**
- Model predictions
- Sensitivity analysis
- Historical performance
- Assumptions

**Approval Required:**
- High-value decisions
- High-risk decisions
- Policy exceptions

---

## Questions to Ask

If you need more context:
1. What decisions need prescriptive recommendations?
2. What are the objectives? (minimize cost, maximize service, balance both)
3. What data is available for predictions and optimization?
4. Who will act on recommendations? (automated vs. human decision-maker)
5. What's the decision frequency? (real-time, daily, strategic)
6. How important is explainability? (black box OK vs. must be interpretable)
7. What are the constraints? (budget, capacity, policy)
8. What's the current decision-making process?

---

## Related Skills

- **optimization-modeling**: For building optimization engines
- **ml-supply-chain**: For predictive models
- **supply-chain-analytics**: For descriptive and diagnostic analytics
- **digital-twin-modeling**: For simulation-based recommendations
- **supply-chain-automation**: For automated decision execution
- **demand-forecasting**: For demand predictions
- **inventory-optimization**: For inventory recommendations
- **route-optimization**: For routing recommendations
- **supplier-selection**: For sourcing decisions
