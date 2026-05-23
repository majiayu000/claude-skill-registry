---
name: fuel-distribution
description: When the user wants to optimize retail fuel distribution, manage gasoline and diesel delivery, or plan petroleum product logistics. Also use when the user mentions "gas station supply," "fuel delivery routing," "petroleum retail," "tank truck scheduling," "fuel terminal operations," "wholesale fuel distribution," or "retail fuel network." For upstream, see drilling-logistics. For midstream, see energy-logistics.
---

# Fuel Distribution

You are an expert in retail fuel distribution and petroleum product logistics. Your goal is to help optimize the distribution of gasoline, diesel, and other petroleum products from terminals to retail stations, managing delivery scheduling, inventory levels, and transportation efficiency while ensuring no stockouts.

## Initial Assessment

Before optimizing fuel distribution, understand:

1. **Network Structure**
   - How many retail locations? (gas stations, fleet facilities)
   - Terminal locations and capacities?
   - Geographic coverage area?
   - Branded vs. unbranded stations?

2. **Demand Characteristics**
   - Daily sales volumes by location?
   - Seasonal patterns? (summer driving, holidays)
   - Product mix? (regular, midgrade, premium, diesel)
   - Demand variability and trends?

3. **Delivery Operations**
   - Fleet size and tank truck capacities?
   - Delivery hours and restrictions?
   - Compartmented trucks (multi-product)?
   - Driver availability and regulations?

4. **Objectives & Constraints**
   - Primary goals? (minimize cost, prevent stockouts, improve service)
   - Budget constraints?
   - Service level requirements? (fill frequency, emergency deliveries)
   - Environmental and safety regulations?

---

## Fuel Distribution Framework

### Supply Chain Structure

**Upstream (Supply):**
- Refineries
- Pipeline terminals
- Marine import terminals
- Bulk storage facilities

**Distribution (Logistics):**
- Primary terminals (bulk receiving)
- Secondary terminals (local distribution)
- Tank truck fleet
- Delivery scheduling and routing

**Downstream (Retail):**
- Gas stations (C-stores)
- Fleet fueling facilities
- Cardlock locations
- Commercial accounts

---

## Retail Station Inventory Management

### Tank Inventory Optimization

```python
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

class FuelStationInventory:
    """
    Manage inventory for retail fuel station with multiple tanks
    """

    def __init__(self, station_id, tanks, daily_sales_forecast):
        self.station_id = station_id
        self.tanks = tanks  # list of {product, capacity_gallons, current_level}
        self.forecast = daily_sales_forecast

    def calculate_reorder_point(self, product, lead_time_days=1,
                                service_level=0.95):
        """
        Calculate reorder point for fuel tank

        Reorder Point = (Avg Daily Sales × Lead Time) + Safety Stock
        """
        from scipy.stats import norm

        # Get historical sales for this product
        product_sales = [day[product] for day in self.forecast
                        if product in day]

        avg_daily_sales = np.mean(product_sales)
        std_daily_sales = np.std(product_sales)

        # Safety stock calculation
        z_score = norm.ppf(service_level)
        safety_stock = z_score * std_daily_sales * np.sqrt(lead_time_days)

        reorder_point = (avg_daily_sales * lead_time_days) + safety_stock

        # Tank capacity constraint
        tank = next((t for t in self.tanks if t['product'] == product), None)
        if tank:
            max_order = tank['capacity_gallons'] - reorder_point

            return {
                'reorder_point_gallons': reorder_point,
                'order_quantity_gallons': max_order,
                'avg_daily_sales': avg_daily_sales,
                'safety_stock': safety_stock,
                'days_of_supply': reorder_point / avg_daily_sales
            }

    def forecast_runout_time(self, product, current_level_gallons):
        """
        Forecast when tank will run out (hours from now)
        """
        product_sales = [day[product] for day in self.forecast
                        if product in day]

        avg_hourly_sales = np.mean(product_sales) / 24

        if avg_hourly_sales > 0:
            hours_until_runout = current_level_gallons / avg_hourly_sales
            return hours_until_runout
        else:
            return float('inf')

    def check_delivery_needed(self):
        """
        Check if delivery is needed for any product

        Returns list of products needing delivery
        """
        delivery_needed = []

        for tank in self.tanks:
            product = tank['product']
            current_level = tank['current_level']
            capacity = tank['capacity_gallons']

            reorder_params = self.calculate_reorder_point(product)
            reorder_point = reorder_params['reorder_point_gallons']

            if current_level <= reorder_point:
                hours_to_runout = self.forecast_runout_time(product, current_level)

                delivery_needed.append({
                    'station': self.station_id,
                    'product': product,
                    'current_level': current_level,
                    'capacity': capacity,
                    'fill_to_level': capacity * 0.95,  # Leave 5% ullage
                    'delivery_quantity': (capacity * 0.95) - current_level,
                    'hours_until_runout': hours_to_runout,
                    'priority': 'HIGH' if hours_to_runout < 12 else 'NORMAL'
                })

        return delivery_needed

# Example usage
tanks = [
    {'product': 'Regular', 'capacity_gallons': 12000, 'current_level': 3000},
    {'product': 'Premium', 'capacity_gallons': 8000, 'current_level': 5000},
    {'product': 'Diesel', 'capacity_gallons': 10000, 'current_level': 2500},
]

# Forecast: daily sales by product
forecast = [
    {'Regular': 4000, 'Premium': 1500, 'Diesel': 2000},
    {'Regular': 4500, 'Premium': 1600, 'Diesel': 2100},
    # ... more days
]

station = FuelStationInventory('Station_001', tanks, forecast)
deliveries = station.check_delivery_needed()

for delivery in deliveries:
    print(f"{delivery['product']}: {delivery['delivery_quantity']:.0f} gallons needed "
         f"(Priority: {delivery['priority']}, Runout: {delivery['hours_until_runout']:.1f} hrs)")
```

---

## Delivery Routing & Scheduling

### Multi-Compartment Tank Truck Routing

```python
def optimize_fuel_delivery_routes(stations, terminal_location, trucks,
                                 time_windows):
    """
    Optimize fuel delivery routes for multi-compartment tank trucks

    Vehicle Routing Problem with:
    - Time windows
    - Multiple products
    - Compartment constraints
    - Split deliveries allowed

    Parameters:
    - stations: list of stations with delivery requirements
    - terminal_location: depot coordinates
    - trucks: list of available trucks with compartment configurations
    - time_windows: delivery time windows by station
    """
    from pulp import *
    import numpy as np

    prob = LpProblem("Fuel_Delivery_Routing", LpMinimize)

    # Decision variables

    # x[t, i, j]: truck t travels from station i to station j
    x = {}
    for t, truck in enumerate(trucks):
        for i in range(len(stations) + 1):  # +1 for terminal
            for j in range(len(stations) + 1):
                if i != j:
                    x[t, i, j] = LpVariable(f"x_{t}_{i}_{j}", cat='Binary')

    # y[t, s, p]: truck t delivers product p to station s
    y = {}
    for t, truck in enumerate(trucks):
        for s, station in enumerate(stations):
            for product in ['Regular', 'Premium', 'Diesel']:
                y[t, s, product] = LpVariable(f"y_{t}_{s}_{product}",
                                             lowBound=0)

    # Arrival time at each station
    arrival_time = {}
    for t, truck in enumerate(trucks):
        for s in range(len(stations)):
            arrival_time[t, s] = LpVariable(f"arrival_{t}_{s}",
                                           lowBound=0)

    # Objective: minimize total distance + time window penalties
    total_distance = []
    for t, truck in enumerate(trucks):
        for i in range(len(stations) + 1):
            for j in range(len(stations) + 1):
                if i != j:
                    loc_i = terminal_location if i == 0 else stations[i-1]['location']
                    loc_j = terminal_location if j == 0 else stations[j-1]['location']

                    distance = calculate_distance(loc_i, loc_j)
                    total_distance.append(distance * x[t, i, j])

    prob += lpSum(total_distance)

    # Constraints

    # Each station's demand must be satisfied
    for s, station in enumerate(stations):
        for product in station['delivery_needs']:
            required = station['delivery_needs'][product]
            prob += lpSum([y[t, s, product] for t in range(len(trucks))]) >= required

    # Truck compartment capacity
    for t, truck in enumerate(trucks):
        for product in ['Regular', 'Premium', 'Diesel']:
            # Sum of deliveries ≤ compartment capacity for that product
            comp_capacity = truck['compartments'].get(product, 0)
            prob += lpSum([y[t, s, product] for s in range(len(stations))]) <= \
                    comp_capacity

    # If truck delivers to station, it must visit station
    for t, truck in enumerate(trucks):
        for s, station in enumerate(stations):
            total_delivery = lpSum([y[t, s, p] for p in ['Regular', 'Premium', 'Diesel']])

            # If total_delivery > 0, truck must visit
            visits = lpSum([x[t, i, s+1] for i in range(len(stations) + 1) if i != s+1])

            prob += total_delivery <= truck['total_capacity'] * visits

    # Flow conservation: if truck enters, it must leave
    for t, truck in enumerate(trucks):
        for j in range(1, len(stations) + 1):  # stations only (not terminal)
            inflow = lpSum([x[t, i, j] for i in range(len(stations) + 1) if i != j])
            outflow = lpSum([x[t, j, i] for i in range(len(stations) + 1) if i != j])

            prob += inflow == outflow

    # Each truck starts and ends at terminal
    for t, truck in enumerate(trucks):
        prob += lpSum([x[t, 0, j] for j in range(1, len(stations) + 1)]) == 1
        prob += lpSum([x[t, i, 0] for i in range(1, len(stations) + 1)]) == 1

    # Solve
    solver = PULP_CBC_CMD(msg=0, timeLimit=60)
    prob.solve(solver)

    # Extract routes
    routes = []
    for t, truck in enumerate(trucks):
        route = [0]  # Start at terminal

        current = 0
        for _ in range(len(stations)):
            for j in range(len(stations) + 1):
                if j != current and (t, current, j) in x:
                    if x[t, current, j].varValue > 0.5:
                        if j != 0:  # Not terminal
                            route.append(j)
                        current = j
                        break

        if len(route) > 1:
            route.append(0)  # Return to terminal
            routes.append({
                'truck': truck['id'],
                'route': route,
                'stations_visited': len(route) - 2,
                'deliveries': {
                    (s, p): y[t, s, p].varValue
                    for s in range(len(stations))
                    for p in ['Regular', 'Premium', 'Diesel']
                    if (t, s, p) in y and y[t, s, p].varValue > 10
                }
            })

    return {
        'status': LpStatus[prob.status],
        'total_distance': value(prob.objective),
        'routes': routes
    }

def calculate_distance(loc1, loc2):
    """Calculate distance between two locations (miles)"""
    import numpy as np
    return np.sqrt((loc1[0] - loc2[0])**2 + (loc1[1] - loc2[1])**2) * 69

# Example usage
stations = [
    {
        'id': 'Station_A',
        'location': (30.0, -95.0),
        'delivery_needs': {'Regular': 4000, 'Premium': 0, 'Diesel': 2000}
    },
    {
        'id': 'Station_B',
        'location': (30.1, -95.1),
        'delivery_needs': {'Regular': 3000, 'Premium': 1000, 'Diesel': 0}
    },
    {
        'id': 'Station_C',
        'location': (30.05, -95.15),
        'delivery_needs': {'Regular': 5000, 'Premium': 0, 'Diesel': 3000}
    },
]

terminal = (30.0, -95.2)

trucks = [
    {
        'id': 'Truck_1',
        'compartments': {'Regular': 5000, 'Premium': 2000, 'Diesel': 3000},
        'total_capacity': 10000
    },
    {
        'id': 'Truck_2',
        'compartments': {'Regular': 6000, 'Premium': 1000, 'Diesel': 4000},
        'total_capacity': 11000
    },
]

result = optimize_fuel_delivery_routes(stations, terminal, trucks, {})
print(f"Total distance: {result['total_distance']:.1f} miles")
for route in result['routes']:
    print(f"Truck {route['truck']}: {route['stations_visited']} stations")
```

---

## Terminal Operations Optimization

### Terminal Loading Dock Scheduling

```python
def optimize_terminal_loading(scheduled_deliveries, loading_bays, time_slots):
    """
    Optimize assignment of trucks to loading bays and time slots

    Parameters:
    - scheduled_deliveries: list of planned deliveries with truck arrival times
    - loading_bays: number of available loading bays
    - time_slots: list of available time slots (e.g., hourly)
    """
    from pulp import *

    prob = LpProblem("Terminal_Loading", LpMinimize)

    n_deliveries = len(scheduled_deliveries)
    n_bays = loading_bays
    n_slots = len(time_slots)

    # Variables: assign delivery d to bay b in time slot t
    x = {}
    for d in range(n_deliveries):
        for b in range(n_bays):
            for t in range(n_slots):
                x[d, b, t] = LpVariable(f"x_{d}_{b}_{t}", cat='Binary')

    # Objective: minimize waiting time and tardiness
    waiting_penalty = []
    for d, delivery in enumerate(scheduled_deliveries):
        desired_slot = delivery['desired_time_slot']

        for b in range(n_bays):
            for t in range(n_slots):
                # Penalty for deviation from desired time
                delay = max(0, t - desired_slot)
                waiting_penalty.append(delay * x[d, b, t])

    prob += lpSum(waiting_penalty)

    # Constraints

    # Each delivery assigned exactly once
    for d in range(n_deliveries):
        prob += lpSum([x[d, b, t]
                      for b in range(n_bays)
                      for t in range(n_slots)]) == 1

    # Bay can handle one truck per time slot
    for b in range(n_bays):
        for t in range(n_slots):
            prob += lpSum([x[d, b, t] for d in range(n_deliveries)]) <= 1

    # Truck cannot load before arrival time
    for d, delivery in enumerate(scheduled_deliveries):
        earliest_slot = delivery['arrival_time_slot']

        for b in range(n_bays):
            for t in range(earliest_slot):
                prob += x[d, b, t] == 0

    # Loading duration (occupy bay for multiple slots)
    for d, delivery in enumerate(scheduled_deliveries):
        load_duration = delivery['loading_duration_slots']

        for b in range(n_bays):
            for t in range(n_slots):
                if x[d, b, t] in prob.variables():
                    # If loading starts at t, bay b is occupied for next 'duration' slots
                    for dt in range(1, load_duration):
                        if t + dt < n_slots:
                            # No other delivery can use this bay during loading
                            prob += lpSum([x[d2, b, t+dt]
                                         for d2 in range(n_deliveries)
                                         if d2 != d]) <= \
                                   1 - x[d, b, t]

    # Solve
    prob.solve(PULP_CBC_CMD(msg=0))

    # Extract schedule
    schedule = []
    for d in range(n_deliveries):
        for b in range(n_bays):
            for t in range(n_slots):
                if x[d, b, t].varValue > 0.5:
                    schedule.append({
                        'delivery': scheduled_deliveries[d]['id'],
                        'truck': scheduled_deliveries[d]['truck'],
                        'bay': b + 1,
                        'time_slot': t,
                        'load_duration': scheduled_deliveries[d]['loading_duration_slots']
                    })

    return {
        'status': LpStatus[prob.status],
        'total_waiting': value(prob.objective),
        'schedule': pd.DataFrame(schedule).sort_values('time_slot')
    }
```

---

## Demand Forecasting for Fuel

### Fuel Sales Forecasting

```python
def forecast_fuel_sales(historical_sales, weather_data, events_calendar):
    """
    Forecast fuel sales considering multiple factors

    Factors:
    - Day of week
    - Seasonality
    - Weather (temperature affects driving)
    - Special events
    - Trends
    """
    from sklearn.ensemble import GradientBoostingRegressor
    from sklearn.preprocessing import StandardScaler
    import pandas as pd

    # Prepare features
    df = historical_sales.copy()

    # Time-based features
    df['day_of_week'] = df['date'].dt.dayofweek
    df['day_of_month'] = df['date'].dt.day
    df['month'] = df['date'].dt.month
    df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)

    # Lag features (previous sales)
    df['sales_lag_1'] = df['sales_gallons'].shift(1)
    df['sales_lag_7'] = df['sales_gallons'].shift(7)
    df['sales_rolling_7'] = df['sales_gallons'].rolling(7).mean()

    # Weather features
    df = df.merge(weather_data, on='date', how='left')

    # Special events
    df = df.merge(events_calendar, on='date', how='left')
    df['is_holiday'] = df['is_holiday'].fillna(0)

    # Drop rows with NaN from lag features
    df = df.dropna()

    # Features for model
    feature_cols = ['day_of_week', 'day_of_month', 'month', 'is_weekend',
                   'sales_lag_1', 'sales_lag_7', 'sales_rolling_7',
                   'temperature', 'precipitation', 'is_holiday']

    X = df[feature_cols]
    y = df['sales_gallons']

    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Train model
    model = GradientBoostingRegressor(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=5,
        random_state=42
    )
    model.fit(X_scaled, y)

    # Feature importance
    importance = pd.DataFrame({
        'feature': feature_cols,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)

    return {
        'model': model,
        'scaler': scaler,
        'feature_importance': importance,
        'train_r2': model.score(X_scaled, y)
    }

def predict_next_week_sales(model, scaler, current_data, weather_forecast):
    """Predict sales for next 7 days"""

    predictions = []

    for day in range(7):
        # Prepare features for prediction day
        # This would use latest sales data and weather forecast
        # Simplified for illustration
        pass

    return predictions
```

---

## Fuel Price Optimization

### Dynamic Pricing Strategy

```python
def optimize_fuel_pricing(station_data, competitor_prices, cost_data,
                         demand_elasticity=-0.5):
    """
    Optimize fuel pricing to maximize margin while remaining competitive

    Parameters:
    - station_data: station characteristics and historical data
    - competitor_prices: current prices at nearby competitors
    - cost_data: wholesale cost and other costs
    - demand_elasticity: price elasticity of demand
    """
    from pulp import *

    prob = LpProblem("Fuel_Pricing", LpMaximize)

    stations = station_data
    products = ['Regular', 'Premium', 'Diesel']

    # Variables: price for each product at each station
    price = {}
    volume = {}

    for s, station in enumerate(stations):
        for product in products:
            price[s, product] = LpVariable(
                f"Price_{s}_{product}",
                lowBound=cost_data[product]['wholesale_cost'] + 0.10,  # Min margin
                upBound=competitor_prices[product]['max'] + 0.20
            )

            volume[s, product] = LpVariable(
                f"Volume_{s}_{product}",
                lowBound=0
            )

    # Objective: maximize total profit
    profit = []

    for s, station in enumerate(stations):
        for product in products:
            # Profit = (Price - Cost) × Volume
            cost = cost_data[product]['wholesale_cost'] + \
                   cost_data[product]['operating_cost']

            profit.append((price[s, product] - cost) * volume[s, product])

    prob += lpSum(profit)

    # Constraints

    # Demand model: volume as function of price
    for s, station in enumerate(stations):
        for product in products:
            base_volume = station['base_volume'][product]
            base_price = station['base_price'][product]

            # Linear demand: V = V0 * (1 + elasticity * (P - P0) / P0)
            # Approximation for LP
            avg_comp_price = competitor_prices[product]['average']

            # Volume decreases if price above competitors
            prob += volume[s, product] <= base_volume * \
                    (1 + demand_elasticity * (price[s, product] - avg_comp_price) / avg_comp_price)

    # Competitive constraints: don't price too far from competitors
    for s, station in enumerate(stations):
        for product in products:
            avg_comp = competitor_prices[product]['average']
            min_comp = competitor_prices[product]['min']

            # Price within competitive range
            prob += price[s, product] <= avg_comp + 0.15  # Max 15 cents above average
            prob += price[s, product] >= min_comp - 0.05  # Max 5 cents below minimum

    # Solve
    prob.solve(PULP_CBC_CMD(msg=0))

    # Extract optimal prices
    optimal_prices = {}
    for s, station in enumerate(stations):
        optimal_prices[station['id']] = {
            product: {
                'price': price[s, product].varValue,
                'volume': volume[s, product].varValue
            }
            for product in products
        }

    return {
        'status': LpStatus[prob.status],
        'max_profit': value(prob.objective),
        'optimal_prices': optimal_prices
    }
```

---

## Tools & Libraries

### Python Libraries

**Optimization:**
- `PuLP`: Linear programming
- `OR-Tools`: Vehicle routing
- `Pyomo`: Optimization modeling

**Forecasting:**
- `scikit-learn`: Machine learning
- `prophet`: Time series forecasting
- `statsmodels`: Statistical models

**Geospatial:**
- `geopy`: Distance calculations
- `folium`: Mapping
- `geopandas`: Geographic data

### Commercial Software

**Fuel Distribution:**
- **Omnitracs**: Fleet management and routing
- **Verizon Connect**: GPS fleet tracking
- **Descartes**: Route optimization
- **TMW Systems**: Transportation management

**Terminal Management:**
- **AspenTech**: Fuel scheduling and optimization
- **Honeywell Experion**: Process control
- **Emerson DeltaV**: Terminal automation

**Retail Management:**
- **Veeder-Root**: Tank monitoring systems
- **PDI**: Fuel pricing and wholesale management
- **Gilbarco**: Fuel dispensing and management
- **Dover Fueling Solutions**: Retail automation

---

## Common Challenges & Solutions

### Challenge: Stockout Prevention

**Problem:**
- Unpredictable demand spikes
- Delivery delays
- Inaccurate forecasting

**Solutions:**
- Real-time inventory monitoring (ATG systems)
- Safety stock optimization
- Predictive analytics for demand
- Emergency delivery protocols
- Automated reorder systems

### Challenge: Delivery Efficiency

**Problem:**
- Rising fuel costs
- Driver shortages
- Traffic congestion
- Time windows

**Solutions:**
- Route optimization software
- Delivery consolidation
- Dynamic routing (real-time adjustments)
- Multi-product compartment trucks
- Night deliveries where allowed

### Challenge: Product Contamination

**Problem:**
- Cross-contamination between products
- Quality issues
- Tank mixing errors

**Solutions:**
- Strict compartment procedures
- Product verification systems
- Tank cleaning protocols
- Quality testing (pre and post-delivery)
- Automated delivery systems

### Challenge: Price Volatility

**Problem:**
- Rapid wholesale price changes
- Competitive pressure
- Margin compression

**Solutions:**
- Dynamic pricing systems
- Hedging strategies
- Wholesale supply contracts
- Price monitoring and automation
- Value-added services (C-store, car wash)

---

## Output Format

### Fuel Distribution Optimization Report

**Executive Summary:**
- Network overview (terminals, stations, trucks)
- Key optimization results
- Cost savings achieved
- Service level performance

**Station Inventory Status:**

| Station | Product | Current Level | Capacity | Days Supply | Reorder Point | Status |
|---------|---------|---------------|----------|-------------|---------------|--------|
| Station_A | Regular | 3,000 gal | 12,000 | 0.75 | 4,500 | URGENT |
| Station_A | Diesel | 6,000 gal | 10,000 | 3.0 | 3,000 | OK |
| Station_B | Regular | 8,000 gal | 15,000 | 2.0 | 5,000 | OK |

**Delivery Schedule:**

| Date | Truck | Route | Stations | Products | Total Gallons | Miles | Hours |
|------|-------|-------|----------|----------|---------------|-------|-------|
| 2026-02-01 | Truck_1 | Route_A | 4 | R, P, D | 9,500 | 85 | 6.5 |
| 2026-02-01 | Truck_2 | Route_B | 3 | R, D | 10,200 | 72 | 5.8 |
| 2026-02-02 | Truck_1 | Route_C | 5 | R, P, D | 10,800 | 95 | 7.2 |

**Cost Analysis:**

| Category | Daily Cost | Monthly Cost | Annual Cost |
|----------|------------|--------------|-------------|
| Fuel (diesel for trucks) | $2,500 | $75,000 | $900,000 |
| Driver wages | $3,200 | $96,000 | $1,152,000 |
| Truck maintenance | $800 | $24,000 | $288,000 |
| Insurance | $400 | $12,000 | $144,000 |
| **Total Distribution Cost** | **$6,900** | **$207,000** | **$2,484,000** |

**KPIs:**

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Stockout Rate | 0.2% | < 0.5% | ✓ Good |
| On-Time Delivery | 97% | > 95% | ✓ Good |
| Delivery Cost per Gallon | $0.025 | < $0.030 | ✓ Good |
| Truck Utilization | 88% | > 85% | ✓ Good |
| Avg Delivery Time | 5.5 hrs | < 6 hrs | ✓ Good |

**Recommendations:**
1. Add one truck to fleet to handle peak summer demand
2. Implement automated pricing system for 10% margin improvement
3. Optimize Station_15 deliveries (currently underutilized route)
4. Consider bulk fuel hedging for next quarter

---

## Questions to Ask

If you need more context:
1. How many retail locations do you serve?
2. What's your tank truck fleet size and configuration?
3. What products do you distribute? (gasoline grades, diesel, biofuels)
4. What are current delivery frequencies and service levels?
5. What's the primary challenge? (cost, stockouts, efficiency)
6. What systems are in place? (TMS, tank monitoring, pricing)
7. What's the competitive environment? (branded, independent)

---

## Related Skills

- **energy-logistics**: For midstream petroleum logistics
- **drilling-logistics**: For upstream oil and gas operations
- **route-optimization**: For vehicle routing and scheduling
- **inventory-optimization**: For inventory management strategies
- **demand-forecasting**: For sales forecasting
- **last-mile-delivery**: For delivery operations
- **fleet-management**: For truck fleet management
- **network-design**: For terminal and station network planning
