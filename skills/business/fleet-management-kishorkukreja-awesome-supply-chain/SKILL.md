---
name: fleet-management
description: When the user wants to manage vehicle fleets, optimize fleet size, or plan vehicle acquisition and maintenance. Also use when the user mentions "fleet sizing," "vehicle lifecycle," "fleet utilization," "maintenance planning," "replacement strategy," "total cost of ownership," or "fleet optimization." For route planning within a fleet, see route-optimization. For last-mile operations, see last-mile-delivery.
---

# Fleet Management

You are an expert in transportation fleet management and optimization. Your goal is to help design cost-effective fleet strategies, optimize fleet size and composition, manage vehicle lifecycle, and maximize fleet utilization while maintaining service levels.

## Initial Assessment

Before developing fleet strategies, understand:

1. **Current Fleet Composition**
   - How many vehicles in fleet?
   - Vehicle types and ages?
   - Owned, leased, or mixed?
   - Current utilization rates?

2. **Business Requirements**
   - Service area and coverage?
   - Demand patterns (seasonal, daily)?
   - Service level requirements?
   - Growth projections?

3. **Cost Structure**
   - Acquisition costs (purchase, lease)?
   - Operating costs (fuel, maintenance, insurance)?
   - Driver labor costs?
   - Disposal/residual values?

4. **Operational Constraints**
   - Regulatory requirements (DOT, emissions)?
   - Driver availability?
   - Garage/parking capacity?
   - Technology systems (GPS, telematics)?

---

## Fleet Management Framework

### Strategic Fleet Decisions

**1. Fleet Sizing**
- Minimum fleet size to meet demand
- Trade-off: fixed costs vs. service flexibility
- Peak vs. average demand planning
- Reserve capacity buffer

**2. Fleet Composition**
- Vehicle types and capabilities
- Payload capacities
- Specialized equipment needs
- Multi-temperature, liftgates, etc.

**3. Acquisition Strategy**
- Buy vs. lease vs. rent
- New vs. used vehicles
- Replacement cycles
- Residual value considerations

**4. Utilization Optimization**
- Route efficiency
- Backhaul optimization
- Asset sharing
- Cross-functional use

---

## Fleet Sizing Models

### Peak Demand Method

```python
import numpy as np
import pandas as pd

def fleet_size_peak_demand(daily_demand, vehicle_capacity,
                          utilization_target=0.85,
                          peak_percentile=95):
    """
    Calculate fleet size based on peak demand

    Parameters:
    - daily_demand: historical daily demand data
    - vehicle_capacity: capacity per vehicle (units, weight, volume)
    - utilization_target: target utilization (0.0-1.0)
    - peak_percentile: percentile for peak planning (e.g., 95)
    """

    # Calculate peak demand at specified percentile
    peak_demand = np.percentile(daily_demand, peak_percentile)

    # Calculate required fleet size
    fleet_size = np.ceil(peak_demand / (vehicle_capacity * utilization_target))

    # Calculate statistics
    avg_demand = np.mean(daily_demand)
    avg_utilization = avg_demand / (fleet_size * vehicle_capacity)

    return {
        'fleet_size': int(fleet_size),
        'peak_demand': peak_demand,
        'avg_demand': avg_demand,
        'peak_utilization': utilization_target,
        'avg_utilization': avg_utilization,
        'days_at_full_capacity': np.sum(daily_demand >= fleet_size * vehicle_capacity)
    }

# Example usage
daily_deliveries = np.random.normal(1200, 250, 365)  # 365 days of data
result = fleet_size_peak_demand(daily_deliveries, vehicle_capacity=80)

print(f"Required fleet size: {result['fleet_size']} vehicles")
print(f"Peak demand (95th percentile): {result['peak_demand']:.0f} deliveries")
print(f"Average utilization: {result['avg_utilization']:.1%}")
```

### Queue Theory Approach

```python
from scipy.stats import poisson
import math

def fleet_size_queue_theory(avg_requests_per_hour, avg_service_time_hours,
                           service_level=0.95):
    """
    Calculate fleet size using queue theory (M/M/c model)

    Parameters:
    - avg_requests_per_hour: arrival rate (λ)
    - avg_service_time_hours: average time per delivery (1/μ)
    - service_level: target probability of no wait
    """

    # Calculate traffic intensity
    lambda_rate = avg_requests_per_hour
    mu_rate = 1 / avg_service_time_hours
    rho = lambda_rate / mu_rate

    # Minimum servers (vehicles) needed
    min_servers = math.ceil(rho)

    # Find minimum servers to meet service level
    for c in range(min_servers, min_servers + 20):
        # Erlang C formula (probability of waiting)
        prob_wait = erlang_c(lambda_rate, mu_rate, c)

        if prob_wait <= (1 - service_level):
            return {
                'fleet_size': c,
                'utilization': rho / c,
                'prob_wait': prob_wait,
                'avg_queue_length': prob_wait * rho / (c - rho)
            }

    return {'fleet_size': min_servers + 20, 'message': 'Service level not achievable'}

def erlang_c(lambda_rate, mu_rate, c):
    """Calculate Erlang C probability (probability of waiting)"""
    rho = lambda_rate / mu_rate
    numerator = (c * rho) ** c / math.factorial(c)
    denominator = sum((c * rho) ** k / math.factorial(k) for k in range(c))
    denominator += (c * rho) ** c / (math.factorial(c) * (1 - rho / c))

    erlang_b = numerator / denominator
    erlang_c = erlang_b / (1 + erlang_b * (1 - rho / c))

    return erlang_c
```

### Simulation-Based Sizing

```python
import numpy as np
import simpy

class FleetSimulation:
    """
    Discrete-event simulation for fleet sizing

    Simulates daily operations to determine optimal fleet size
    """

    def __init__(self, env, num_vehicles):
        self.env = env
        self.vehicles = simpy.Resource(env, capacity=num_vehicles)
        self.completed_deliveries = 0
        self.total_wait_time = 0
        self.waiting_customers = 0

    def delivery_process(self, customer_id, arrival_time, service_time):
        """Simulate a single delivery"""
        # Wait for available vehicle
        with self.vehicles.request() as request:
            wait_start = self.env.now
            yield request

            wait_time = self.env.now - wait_start
            self.total_wait_time += wait_time

            if wait_time > 0:
                self.waiting_customers += 1

            # Perform delivery
            yield self.env.timeout(service_time)
            self.completed_deliveries += 1

def run_fleet_simulation(num_vehicles, num_days=30,
                        avg_orders_per_day=100,
                        avg_service_time=2.0):
    """
    Run fleet simulation

    Parameters:
    - num_vehicles: fleet size to test
    - num_days: simulation duration
    - avg_orders_per_day: average daily orders
    - avg_service_time: average hours per delivery
    """

    env = simpy.Environment()
    fleet = FleetSimulation(env, num_vehicles)

    # Generate delivery requests
    def generate_orders():
        for day in range(num_days):
            # Daily orders (Poisson distribution)
            num_orders = np.random.poisson(avg_orders_per_day)

            for order in range(num_orders):
                # Arrival time (throughout business day)
                arrival_time = day * 24 + np.random.uniform(8, 18)

                # Service time (lognormal distribution)
                service_time = np.random.lognormal(
                    mean=np.log(avg_service_time),
                    sigma=0.5
                )

                env.process(fleet.delivery_process(
                    customer_id=f"D{day}_O{order}",
                    arrival_time=arrival_time,
                    service_time=service_time
                ))

                yield env.timeout(0)

    env.process(generate_orders())
    env.run(until=num_days * 24)

    # Calculate metrics
    service_level = 1 - (fleet.waiting_customers / fleet.completed_deliveries)
    avg_wait = fleet.total_wait_time / fleet.completed_deliveries if fleet.completed_deliveries > 0 else 0
    utilization = fleet.completed_deliveries * avg_service_time / (num_vehicles * num_days * 24)

    return {
        'fleet_size': num_vehicles,
        'completed_deliveries': fleet.completed_deliveries,
        'service_level': service_level,
        'avg_wait_time': avg_wait,
        'utilization': utilization
    }

# Find optimal fleet size through simulation
def find_optimal_fleet_size(target_service_level=0.90):
    """Test different fleet sizes to find optimal"""

    results = []

    for fleet_size in range(5, 25):
        result = run_fleet_simulation(num_vehicles=fleet_size, num_days=30)
        results.append(result)

        if result['service_level'] >= target_service_level:
            print(f"Optimal fleet size: {fleet_size} vehicles")
            print(f"Service level: {result['service_level']:.2%}")
            print(f"Utilization: {result['utilization']:.2%}")
            return result

    return results
```

---

## Total Cost of Ownership (TCO)

### TCO Components

**1. Acquisition Costs**
- Purchase price or lease payments
- Registration and licensing
- Initial equipment (GPS, racks, etc.)

**2. Operating Costs**
- Fuel
- Maintenance and repairs
- Tires
- Insurance
- Tolls and permits

**3. Overhead Costs**
- Depreciation (owned vehicles)
- Storage/parking
- Fleet management systems
- Administrative overhead

**4. Disposal Costs**
- Residual value (owned)
- Lease-end charges (leased)
- Remarketing costs

### TCO Calculator

```python
class VehicleTCO:
    """
    Calculate Total Cost of Ownership for vehicles

    Compares buy vs. lease scenarios
    """

    def __init__(self, vehicle_type):
        self.vehicle_type = vehicle_type

    def calculate_purchase_tco(self, purchase_price, useful_life_years,
                               annual_miles, residual_value_pct=0.20):
        """
        Calculate TCO for purchased vehicle

        Parameters:
        - purchase_price: initial purchase cost
        - useful_life_years: ownership period
        - annual_miles: expected annual mileage
        - residual_value_pct: estimated residual value as % of purchase
        """

        # Annual operating costs
        fuel_cost_per_mile = 0.35  # varies by vehicle type
        maintenance_per_mile = 0.15
        insurance_annual = 2500
        registration_annual = 500
        depreciation_annual = purchase_price * (1 - residual_value_pct) / useful_life_years

        # Calculate annual cost
        annual_cost = {
            'fuel': annual_miles * fuel_cost_per_mile,
            'maintenance': annual_miles * maintenance_per_mile,
            'insurance': insurance_annual,
            'registration': registration_annual,
            'depreciation': depreciation_annual
        }

        total_annual = sum(annual_cost.values())

        # Total cost over ownership
        total_operating = total_annual * useful_life_years
        residual_value = purchase_price * residual_value_pct
        net_cost = purchase_price + total_operating - residual_value

        # Cost per mile
        total_miles = annual_miles * useful_life_years
        cost_per_mile = net_cost / total_miles if total_miles > 0 else 0

        return {
            'annual_cost': total_annual,
            'annual_breakdown': annual_cost,
            'total_cost': net_cost,
            'cost_per_mile': cost_per_mile,
            'cost_per_month': total_annual / 12,
            'residual_value': residual_value
        }

    def calculate_lease_tco(self, monthly_lease_payment, lease_term_years,
                           annual_miles, excess_mile_charge=0.25):
        """
        Calculate TCO for leased vehicle

        Parameters:
        - monthly_lease_payment: monthly lease cost
        - lease_term_years: lease duration
        - annual_miles: expected annual mileage
        - excess_mile_charge: cost per mile over allowance
        """

        lease_allowance_miles = 15000  # typical annual allowance

        # Calculate excess miles
        excess_miles_per_year = max(0, annual_miles - lease_allowance_miles)
        excess_miles_total = excess_miles_per_year * lease_term_years
        excess_miles_cost = excess_miles_total * excess_mile_charge

        # Annual operating costs (lessee responsible)
        fuel_cost_per_mile = 0.35
        insurance_annual = 2500
        registration_annual = 500

        annual_operating = (
            annual_miles * fuel_cost_per_mile +
            insurance_annual +
            registration_annual
        )

        annual_lease_cost = monthly_lease_payment * 12

        # Total cost
        total_lease_payments = annual_lease_cost * lease_term_years
        total_operating = annual_operating * lease_term_years
        total_cost = total_lease_payments + total_operating + excess_miles_cost

        # Cost per mile
        total_miles = annual_miles * lease_term_years
        cost_per_mile = total_cost / total_miles if total_miles > 0 else 0

        return {
            'annual_cost': annual_lease_cost + annual_operating,
            'total_lease_payments': total_lease_payments,
            'excess_miles_cost': excess_miles_cost,
            'total_cost': total_cost,
            'cost_per_mile': cost_per_mile,
            'cost_per_month': (annual_lease_cost + annual_operating) / 12
        }

    def compare_buy_vs_lease(self, purchase_price, lease_monthly,
                            years, annual_miles):
        """
        Compare buying vs. leasing

        Returns comparison with recommendation
        """

        buy_tco = self.calculate_purchase_tco(
            purchase_price=purchase_price,
            useful_life_years=years,
            annual_miles=annual_miles
        )

        lease_tco = self.calculate_lease_tco(
            monthly_lease_payment=lease_monthly,
            lease_term_years=years,
            annual_miles=annual_miles
        )

        savings = lease_tco['total_cost'] - buy_tco['total_cost']
        recommendation = 'Buy' if savings > 0 else 'Lease'

        return {
            'buy': buy_tco,
            'lease': lease_tco,
            'savings_with_buy': savings,
            'recommendation': recommendation,
            'buy_cost_per_mile': buy_tco['cost_per_mile'],
            'lease_cost_per_mile': lease_tco['cost_per_mile']
        }

# Example usage
tco = VehicleTCO('Delivery Van')
comparison = tco.compare_buy_vs_lease(
    purchase_price=45000,
    lease_monthly=650,
    years=5,
    annual_miles=25000
)

print(f"Recommendation: {comparison['recommendation']}")
print(f"Buy TCO: ${comparison['buy']['total_cost']:,.0f}")
print(f"Lease TCO: ${comparison['lease']['total_cost']:,.0f}")
print(f"Savings with buy: ${comparison['savings_with_buy']:,.0f}")
```

---

## Fleet Replacement Strategy

### Optimal Replacement Timing

```python
import numpy as np
from scipy.optimize import minimize_scalar

def optimal_replacement_age(purchase_price, annual_depreciation,
                           annual_maintenance, discount_rate=0.08):
    """
    Calculate optimal vehicle replacement age

    Minimizes equivalent annual cost (EAC)

    Parameters:
    - purchase_price: initial cost
    - annual_depreciation: depreciation schedule (list)
    - annual_maintenance: maintenance cost schedule (list)
    - discount_rate: discount rate for NPV
    """

    def equivalent_annual_cost(age):
        """Calculate EAC for given replacement age"""

        if age < 1 or age > len(annual_maintenance):
            return float('inf')

        age = int(age)

        # Calculate NPV of costs
        npv_costs = purchase_price

        for year in range(1, age + 1):
            discount_factor = (1 + discount_rate) ** -year
            npv_costs += annual_maintenance[year - 1] * discount_factor

        # Calculate residual value
        residual_value = purchase_price
        for year in range(age):
            residual_value -= annual_depreciation[year]

        npv_costs -= residual_value * (1 + discount_rate) ** -age

        # Convert to EAC
        annuity_factor = (
            (discount_rate * (1 + discount_rate) ** age) /
            ((1 + discount_rate) ** age - 1)
        )
        eac = npv_costs * annuity_factor

        return eac

    # Find optimal age
    result = minimize_scalar(
        equivalent_annual_cost,
        bounds=(1, len(annual_maintenance)),
        method='bounded'
    )

    optimal_age = int(result.x)
    min_eac = result.fun

    return {
        'optimal_replacement_age': optimal_age,
        'equivalent_annual_cost': min_eac
    }

# Example: Analyze replacement for delivery truck
purchase_price = 50000
annual_depreciation = [10000, 8000, 6000, 5000, 4000, 3000, 2000]
annual_maintenance = [2000, 2500, 3000, 4000, 5500, 7000, 9000]

result = optimal_replacement_age(
    purchase_price,
    annual_depreciation,
    annual_maintenance
)

print(f"Optimal replacement age: {result['optimal_replacement_age']} years")
print(f"Equivalent annual cost: ${result['equivalent_annual_cost']:,.0f}")
```

### Age-Based Replacement Policy

```python
class FleetReplacementPlanner:
    """
    Plan multi-year fleet replacement strategy

    Accounts for budget constraints and vehicle ages
    """

    def __init__(self, fleet_data, annual_budget):
        """
        Parameters:
        - fleet_data: DataFrame with columns ['vehicle_id', 'age', 'type',
                      'replacement_cost', 'maintenance_cost']
        - annual_budget: maximum annual replacement budget
        """
        self.fleet = fleet_data.copy()
        self.annual_budget = annual_budget

    def prioritize_replacements(self, current_year):
        """
        Prioritize vehicles for replacement

        Scoring based on age, maintenance cost, and utilization
        """

        # Calculate replacement scores
        self.fleet['age_score'] = self.fleet['age'] / 10  # normalize
        self.fleet['maintenance_score'] = (
            self.fleet['maintenance_cost'] /
            self.fleet['maintenance_cost'].median()
        )

        # Combined score (higher = more urgent)
        self.fleet['replacement_score'] = (
            0.6 * self.fleet['age_score'] +
            0.4 * self.fleet['maintenance_score']
        )

        # Sort by priority
        self.fleet = self.fleet.sort_values(
            'replacement_score',
            ascending=False
        )

        return self.fleet[['vehicle_id', 'age', 'replacement_score']]

    def create_replacement_plan(self, planning_horizon=5):
        """
        Create multi-year replacement plan

        Returns year-by-year replacement schedule
        """

        replacement_plan = {year: [] for year in range(planning_horizon)}
        remaining_fleet = self.fleet.copy()

        for year in range(planning_horizon):
            # Age all vehicles by one year
            remaining_fleet['age'] += 1

            # Re-prioritize
            remaining_fleet['age_score'] = remaining_fleet['age'] / 10
            remaining_fleet['replacement_score'] = (
                0.6 * remaining_fleet['age_score'] +
                0.4 * remaining_fleet['maintenance_score']
            )
            remaining_fleet = remaining_fleet.sort_values(
                'replacement_score',
                ascending=False
            )

            # Select vehicles to replace within budget
            budget_remaining = self.annual_budget
            year_replacements = []

            for idx, vehicle in remaining_fleet.iterrows():
                if budget_remaining >= vehicle['replacement_cost']:
                    year_replacements.append({
                        'vehicle_id': vehicle['vehicle_id'],
                        'age_at_replacement': vehicle['age'],
                        'cost': vehicle['replacement_cost']
                    })
                    budget_remaining -= vehicle['replacement_cost']

                    # Remove from fleet
                    remaining_fleet = remaining_fleet.drop(idx)

            replacement_plan[year] = year_replacements

        return replacement_plan

    def summarize_plan(self, plan):
        """Create summary of replacement plan"""

        summary = []
        for year, replacements in plan.items():
            total_cost = sum(r['cost'] for r in replacements)
            num_vehicles = len(replacements)

            summary.append({
                'year': year,
                'num_replacements': num_vehicles,
                'total_cost': total_cost,
                'budget_utilization': total_cost / self.annual_budget
            })

        return pd.DataFrame(summary)

# Example usage
import pandas as pd

fleet_data = pd.DataFrame({
    'vehicle_id': [f'V{i:03d}' for i in range(50)],
    'age': np.random.randint(1, 12, 50),
    'type': np.random.choice(['Van', 'Truck', 'Tractor'], 50),
    'replacement_cost': np.random.randint(35000, 75000, 50),
    'maintenance_cost': np.random.randint(2000, 8000, 50)
})

planner = FleetReplacementPlanner(fleet_data, annual_budget=500000)
plan = planner.create_replacement_plan(planning_horizon=5)
summary = planner.summarize_plan(plan)

print("5-Year Replacement Plan:")
print(summary)
```

---

## Fleet Utilization Optimization

### Utilization Metrics

```python
class FleetUtilizationAnalyzer:
    """
    Analyze and improve fleet utilization

    Key metrics: miles driven, hours used, revenue per vehicle
    """

    def __init__(self, vehicle_data, operational_data):
        """
        Parameters:
        - vehicle_data: DataFrame with vehicle details
        - operational_data: DataFrame with daily usage logs
        """
        self.vehicles = vehicle_data
        self.operations = operational_data

    def calculate_utilization_metrics(self):
        """Calculate comprehensive utilization metrics"""

        metrics = []

        for vehicle_id in self.vehicles['vehicle_id']:
            vehicle_ops = self.operations[
                self.operations['vehicle_id'] == vehicle_id
            ]

            if len(vehicle_ops) == 0:
                continue

            # Time utilization
            total_days = (vehicle_ops['date'].max() -
                         vehicle_ops['date'].min()).days + 1
            active_days = vehicle_ops['date'].nunique()
            time_utilization = active_days / total_days if total_days > 0 else 0

            # Mileage
            total_miles = vehicle_ops['miles'].sum()
            avg_daily_miles = total_miles / active_days if active_days > 0 else 0

            # Revenue
            total_revenue = vehicle_ops['revenue'].sum()
            revenue_per_mile = total_revenue / total_miles if total_miles > 0 else 0

            # Efficiency
            empty_miles = vehicle_ops['empty_miles'].sum()
            loaded_miles = total_miles - empty_miles
            loaded_percentage = loaded_miles / total_miles if total_miles > 0 else 0

            metrics.append({
                'vehicle_id': vehicle_id,
                'active_days': active_days,
                'time_utilization': time_utilization,
                'total_miles': total_miles,
                'avg_daily_miles': avg_daily_miles,
                'total_revenue': total_revenue,
                'revenue_per_mile': revenue_per_mile,
                'loaded_percentage': loaded_percentage
            })

        return pd.DataFrame(metrics)

    def identify_underutilized_vehicles(self, utilization_threshold=0.60):
        """
        Identify vehicles below utilization threshold

        Returns candidates for removal from fleet
        """

        metrics = self.calculate_utilization_metrics()

        underutilized = metrics[
            metrics['time_utilization'] < utilization_threshold
        ].sort_values('time_utilization')

        return underutilized

    def recommend_fleet_adjustments(self):
        """
        Recommend fleet size adjustments

        Based on utilization analysis
        """

        metrics = self.calculate_utilization_metrics()

        avg_utilization = metrics['time_utilization'].mean()
        underutilized = len(metrics[metrics['time_utilization'] < 0.60])

        recommendations = []

        if avg_utilization < 0.65:
            potential_reduction = int(len(metrics) * (0.65 - avg_utilization))
            recommendations.append({
                'action': 'Reduce fleet size',
                'vehicles': potential_reduction,
                'reason': f'Average utilization only {avg_utilization:.1%}'
            })

        if underutilized > 0:
            recommendations.append({
                'action': 'Remove or reassign',
                'vehicles': underutilized,
                'reason': f'{underutilized} vehicles below 60% utilization'
            })

        # Check for overutilization
        high_mileage = metrics[metrics['avg_daily_miles'] > 250]
        if len(high_mileage) > len(metrics) * 0.3:
            recommendations.append({
                'action': 'Add vehicles',
                'vehicles': 2,
                'reason': 'Many vehicles exceeding 250 miles/day'
            })

        return recommendations
```

---

## Maintenance Management

### Preventive Maintenance Scheduling

```python
class MaintenanceScheduler:
    """
    Schedule and track fleet maintenance

    Prevents breakdowns, optimizes maintenance timing
    """

    def __init__(self, fleet_data):
        self.fleet = fleet_data.copy()

    def calculate_maintenance_schedule(self, current_date):
        """
        Calculate upcoming maintenance needs

        Returns schedule for next 90 days
        """

        schedule = []

        for idx, vehicle in self.fleet.iterrows():
            # Check mileage-based maintenance
            miles_since_service = (
                vehicle['current_mileage'] -
                vehicle['last_service_mileage']
            )

            miles_to_service = vehicle['service_interval'] - miles_since_service
            avg_daily_miles = vehicle['avg_daily_miles']

            if avg_daily_miles > 0:
                days_to_service = miles_to_service / avg_daily_miles
            else:
                days_to_service = 999

            # Check time-based maintenance
            days_since_service = (
                current_date - vehicle['last_service_date']
            ).days

            days_to_time_service = 180 - days_since_service  # 6-month interval

            # Use whichever comes first
            days_to_service = min(days_to_service, days_to_time_service)

            if days_to_service <= 90:  # Next 90 days
                schedule.append({
                    'vehicle_id': vehicle['vehicle_id'],
                    'days_to_service': max(0, days_to_service),
                    'due_date': current_date + pd.Timedelta(days=max(0, days_to_service)),
                    'service_type': 'Preventive Maintenance',
                    'estimated_cost': vehicle['avg_service_cost'],
                    'priority': 'High' if days_to_service <= 7 else 'Medium'
                })

        return pd.DataFrame(schedule).sort_values('days_to_service')

    def optimize_maintenance_timing(self, schedule, routes_data):
        """
        Optimize maintenance timing to minimize service disruption

        Coordinate with route schedules
        """

        optimized = []

        for idx, maintenance in schedule.iterrows():
            vehicle_id = maintenance['vehicle_id']

            # Find days when vehicle has lightest workload
            vehicle_routes = routes_data[
                routes_data['vehicle_id'] == vehicle_id
            ]

            # Calculate workload by day
            daily_workload = vehicle_routes.groupby('date').agg({
                'stops': 'sum',
                'miles': 'sum'
            })

            # Find lightest day within maintenance window
            maintenance_window_start = maintenance['due_date'] - pd.Timedelta(days=7)
            maintenance_window_end = maintenance['due_date'] + pd.Timedelta(days=3)

            window_workload = daily_workload[
                (daily_workload.index >= maintenance_window_start) &
                (daily_workload.index <= maintenance_window_end)
            ]

            if len(window_workload) > 0:
                optimal_date = window_workload['stops'].idxmin()
            else:
                optimal_date = maintenance['due_date']

            maintenance['optimal_date'] = optimal_date
            optimized.append(maintenance)

        return pd.DataFrame(optimized)
```

---

## Tools & Technology

### Telematics & GPS Systems

**Leading Providers:**
- **Verizon Connect**: Fleet tracking, diagnostics
- **Samsara**: IoT sensors, dash cams, ELD
- **Geotab**: Telematics, driver behavior
- **Teletrac Navman**: GPS tracking, compliance
- **Fleet Complete**: Asset tracking, mobile workforce
- **Omnitracs**: ELD, fleet management

**Key Features:**
- Real-time GPS location tracking
- Vehicle diagnostics (OBD-II)
- Driver behavior monitoring
- Maintenance alerts
- Fuel consumption tracking
- ELD compliance (Hours of Service)

### Fleet Management Software

**Comprehensive Platforms:**
- **Fleetio**: Maintenance, fuel, compliance
- **RTA Fleet Management**: Asset management
- **Fleet Manager**: Cost tracking, reporting
- **Dossier Fleet Maintenance**: Work orders, inventory
- **Azuga Fleet**: GPS + fleet management

**Key Capabilities:**
- Maintenance scheduling
- Fuel management
- Cost tracking and reporting
- Vehicle lifecycle management
- Driver management
- Compliance tracking

---

## Common Challenges & Solutions

### Challenge: Excessive Idle Time

**Problem:**
- Vehicles sitting unused
- Low utilization rates
- High fixed costs per delivery

**Solutions:**
- Implement backhaul programs
- Cross-utilize vehicles across departments
- Consider contract carriers for overflow
- Right-size fleet (remove excess vehicles)
- Implement dynamic dispatch
- Offer vehicles for spot market
- Share assets with partners

### Challenge: High Maintenance Costs

**Problem:**
- Aging fleet
- Frequent breakdowns
- Escalating repair costs

**Solutions:**
- Accelerate replacement cycle for high-cost vehicles
- Implement predictive maintenance
- Use telematics for early fault detection
- Standardize vehicle types (reduce parts inventory)
- Negotiate fleet maintenance contracts
- Train drivers on vehicle care
- Track and benchmark costs per vehicle

### Challenge: Unpredictable Demand

**Problem:**
- Fleet sized for peak, idle at average
- Difficult to justify capital investment

**Solutions:**
- Core fleet for base demand + flex capacity for peak
- Use contract carriers or spot market for overflow
- Consider leasing vs. buying for flexibility
- Implement dynamic routing to maximize utilization
- Build backhaul network to fill return trips
- Seasonal drivers (expand/contract as needed)

### Challenge: Driver Shortage

**Problem:**
- Not enough drivers for available vehicles
- Vehicle utilization limited by driver availability

**Solutions:**
- Improve driver retention (pay, benefits, home time)
- Recruit more aggressively
- Consider driver teams (extend hours)
- Reduce fleet size to match driver availability
- Invest in driver training and development
- Explore automation for specific routes
- Contract with owner-operators

### Challenge: Regulatory Compliance

**Problem:**
- ELD mandates (Hours of Service)
- Emissions requirements
- Safety regulations (DOT)

**Solutions:**
- Implement ELD system (electronic logging)
- Regular compliance audits
- Driver training on regulations
- Modern fleet (meets emissions standards)
- Dedicated safety manager
- Automated alerts for violations
- Partner with compliance consultants

---

## Output Format

### Fleet Analysis Report

**Executive Summary:**
- Current fleet: 45 vehicles
- Average utilization: 73%
- Total annual cost: $3.2M
- Cost per vehicle: $71,111
- Recommendation: Reduce by 5 vehicles, replace 8 aging units

**Fleet Composition:**

| Vehicle Type | Count | Avg Age | Avg Miles | Utilization | Annual Cost |
|--------------|-------|---------|-----------|-------------|-------------|
| Box Truck (26') | 20 | 6.2 yrs | 32K | 82% | $1.4M |
| Cargo Van | 15 | 4.1 yrs | 28K | 68% | $900K |
| Straight Truck | 10 | 8.5 yrs | 45K | 71% | $900K |

**Utilization Analysis:**

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Avg daily utilization | 73% | 80% | ⚠️ Below target |
| Vehicles <60% utilized | 8 | 0 | ❌ Action needed |
| Avg daily miles | 125 | 150 | ⚠️ Below target |
| Empty mile % | 18% | <15% | ⚠️ Above target |

**Cost Breakdown:**

| Cost Category | Annual | Per Vehicle | % of Total |
|---------------|--------|-------------|------------|
| Depreciation | $675K | $15K | 21% |
| Fuel | $945K | $21K | 30% |
| Maintenance | $495K | $11K | 15% |
| Insurance | $450K | $10K | 14% |
| Labor (drivers) | $585K | $13K | 18% |
| Other | $50K | $1K | 2% |

**Replacement Plan (5 Years):**

| Year | Vehicles | Investment | Reason |
|------|----------|------------|--------|
| 2026 | 8 | $480K | Age > 8 years, high maintenance |
| 2027 | 5 | $300K | Age > 7 years |
| 2028 | 6 | $360K | Scheduled replacement |
| 2029 | 7 | $420K | Scheduled replacement |
| 2030 | 5 | $300K | Scheduled replacement |

**Recommendations:**

1. **Reduce fleet by 5 vehicles**
   - Remove 5 lowest-utilized cargo vans
   - Savings: $355K annually
   - Impact: Minimal (use contract carriers for overflow)

2. **Replace 8 aging vehicles immediately**
   - Target: Units over 8 years old with maintenance >$6K/year
   - Investment: $480K
   - Payback: 2.5 years (reduced maintenance + fuel)

3. **Implement telematics system**
   - Real-time GPS and diagnostics
   - Investment: $45K (hardware + software)
   - Benefits: 10% improvement in utilization, reduced maintenance

4. **Optimize backhaul program**
   - Reduce empty miles from 18% to 12%
   - Savings: $85K annually in fuel

---

## Questions to Ask

If you need more context:
1. How many vehicles in the current fleet? What types?
2. What are current utilization rates?
3. What's the budget for fleet operations?
4. Own, lease, or mix? What's the preference?
5. Any specific pain points? (costs, breakdowns, utilization)
6. What's the demand pattern? (steady, seasonal, growing)
7. Any technology systems in place? (GPS, telematics, fleet management software)
8. What are the replacement criteria currently?

---

## Related Skills

- **route-optimization**: Optimize routes to improve fleet utilization
- **last-mile-delivery**: Urban delivery fleet management
- **freight-optimization**: Long-haul fleet optimization
- **maintenance-planning**: Equipment maintenance scheduling
- **prescriptive-analytics**: Data-driven fleet decisions
- **supply-chain-automation**: Automated fleet management systems
- **total-cost-ownership**: TCO analysis for assets
- **capacity-planning**: Fleet capacity planning
