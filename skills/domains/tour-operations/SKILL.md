---
name: tour-operations
description: When the user wants to optimize tour operations, manage tour packages, or coordinate travel itineraries. Also use when the user mentions "tour planning," "package tours," "tour logistics," "itinerary optimization," "tour operator management," "group travel coordination," "excursion planning," or "travel package optimization." For hotel inventory, see hotel-inventory-management. For hospitality procurement, see hospitality-procurement.
---

# Tour Operations

You are an expert in tour operations and package travel management. Your goal is to help optimize tour planning, package construction, resource allocation, and operational logistics for tour operators, ensuring profitability while delivering excellent customer experiences.

## Initial Assessment

Before optimizing tour operations, understand:

1. **Tour Operator Profile**
   - Operator type? (inbound, outbound, ground handler, DMC)
   - Market segments? (adventure, luxury, budget, cultural, special interest)
   - Geographic focus? (domestic, regional, international)
   - Business model? (retail, wholesale, B2B, B2C)

2. **Tour Portfolio**
   - Tour types? (escorted, independent, FIT, SIT, GIT)
   - Duration range? (day tours, multi-day, extended)
   - Number of active tours and departures?
   - Seasonal vs. year-round operation?

3. **Resource Constraints**
   - Transportation fleet? (owned, leased, contracted)
   - Guide availability and languages?
   - Hotel and accommodation contracts?
   - Supplier relationships?

4. **Objectives & Challenges**
   - Primary goals? (profitability, market share, customer satisfaction)
   - Current pain points? (utilization, costs, operations)
   - Technology systems? (booking, operations, CRM)
   - Competitive positioning?

---

## Tour Operations Framework

### Tour Package Components

**Transportation:**
- Motorcoach/bus
- Trains
- Flights (group bookings)
- Transfers and private vehicles
- Ferries and boats

**Accommodation:**
- Hotels (groups, series, allotments)
- Resorts
- Alternative (hostels, B&B, apartments)

**Attractions & Activities:**
- Guided tours and excursions
- Entrance fees
- Activities and experiences
- Meals and dining

**Services:**
- Tour guides and tour directors
- Local guides
- Transfers
- Porter services

---

## Tour Package Pricing & Profitability

### Cost-Plus Pricing Model

```python
import numpy as np
import pandas as pd

class TourPackagePricing:
    """
    Calculate tour package costs and optimal pricing
    """

    def __init__(self, tour_name, duration_days, max_pax):
        self.tour_name = tour_name
        self.duration = duration_days
        self.max_pax = max_pax

    def calculate_tour_cost(self, components):
        """
        Calculate total tour cost per passenger

        Components include:
        - Hotels (per room per night)
        - Transportation (fixed + per km)
        - Meals (per meal per person)
        - Attractions (per person)
        - Guide (per day)
        - Other (insurance, tips, etc.)
        """

        # Per-passenger costs
        per_pax_cost = {
            'accommodation': 0,
            'meals': 0,
            'attractions': 0,
            'guide_services': 0,
            'transportation': 0,
            'other': 0
        }

        # Accommodation cost (assume double occupancy)
        hotels = components['hotels']
        for hotel in hotels:
            cost_per_room = hotel['rate_per_night'] * hotel['nights']
            per_pax_cost['accommodation'] += cost_per_room / 2  # Double occupancy

        # Meals
        meals = components['meals']
        per_pax_cost['meals'] = (
            meals['breakfasts'] * meals['breakfast_cost'] +
            meals['lunches'] * meals['lunch_cost'] +
            meals['dinners'] * meals['dinner_cost']
        )

        # Attractions and entrance fees
        for attraction in components['attractions']:
            per_pax_cost['attractions'] += attraction['cost_per_person']

        # Fixed costs allocated per passenger (at full capacity)
        # Transportation
        transport = components['transportation']
        total_transport_cost = (
            transport['fixed_cost'] +
            transport['distance_km'] * transport['cost_per_km'] +
            transport['driver_cost_per_day'] * self.duration
        )
        per_pax_cost['transportation'] = total_transport_cost / self.max_pax

        # Guide services
        guide_cost_total = components['guide']['cost_per_day'] * self.duration
        per_pax_cost['guide_services'] = guide_cost_total / self.max_pax

        # Other costs
        per_pax_cost['other'] = components.get('other_per_pax', 0)

        return per_pax_cost

    def calculate_breakeven_price(self, per_pax_cost, overhead_percentage=0.15):
        """
        Calculate breakeven price including overhead
        """
        total_direct_cost = sum(per_pax_cost.values())
        overhead = total_direct_cost * overhead_percentage
        breakeven = total_direct_cost + overhead

        return breakeven

    def calculate_selling_price(self, breakeven_price, margin_percentage=0.25,
                               single_supplement_pct=0.30):
        """
        Calculate selling prices with desired margin

        Parameters:
        - margin_percentage: target profit margin
        - single_supplement_pct: additional charge for single occupancy
        """

        # Base selling price (double occupancy)
        base_price = breakeven_price / (1 - margin_percentage)

        # Single occupancy price (pays for full room)
        single_price = base_price * (1 + single_supplement_pct)

        # Child price (if applicable)
        child_price = base_price * 0.75  # 25% discount

        return {
            'double_occupancy': base_price,
            'single_occupancy': single_price,
            'child': child_price,
            'margin_percentage': margin_percentage,
            'margin_amount': base_price - breakeven_price
        }

    def calculate_tour_profitability(self, selling_price, actual_pax,
                                    pax_mix={'double': 20, 'single': 4, 'child': 2}):
        """
        Calculate tour profitability for given passenger mix
        """

        # Revenue
        revenue = (
            pax_mix['double'] * selling_price['double_occupancy'] +
            pax_mix['single'] * selling_price['single_occupancy'] +
            pax_mix['child'] * selling_price['child']
        )

        # Recalculate costs for actual passenger count
        total_pax = sum(pax_mix.values())

        # Variable costs scale with actual pax
        # Fixed costs remain the same

        # Simplified profitability
        total_cost = self.calculate_breakeven_price(self.calculate_tour_cost(components)) * total_pax

        profit = revenue - total_cost
        profit_margin = profit / revenue if revenue > 0 else 0

        return {
            'total_revenue': revenue,
            'total_cost': total_cost,
            'gross_profit': profit,
            'profit_margin': profit_margin,
            'revenue_per_pax': revenue / total_pax,
            'cost_per_pax': total_cost / total_pax
        }

# Example tour costing
tour = TourPackagePricing("European Highlights", duration_days=7, max_pax=45)

components = {
    'hotels': [
        {'city': 'Paris', 'rate_per_night': 120, 'nights': 2},
        {'city': 'Rome', 'rate_per_night': 100, 'nights': 2},
        {'city': 'Barcelona', 'rate_per_night': 110, 'nights': 2},
    ],
    'meals': {
        'breakfasts': 7, 'breakfast_cost': 15,
        'lunches': 4, 'lunch_cost': 20,
        'dinners': 6, 'dinner_cost': 35
    },
    'attractions': [
        {'name': 'Eiffel Tower', 'cost_per_person': 25},
        {'name': 'Colosseum', 'cost_per_person': 30},
        {'name': 'Sagrada Familia', 'cost_per_person': 35},
    ],
    'transportation': {
        'fixed_cost': 5000,  # Bus rental
        'distance_km': 2500,
        'cost_per_km': 1.5,
        'driver_cost_per_day': 200
    },
    'guide': {
        'cost_per_day': 300
    },
    'other_per_pax': 50  # Insurance, tips, etc.
}

per_pax_cost = tour.calculate_tour_cost(components)
breakeven = tour.calculate_breakeven_price(per_pax_cost)
selling_price = tour.calculate_selling_price(breakeven, margin_percentage=0.25)

print(f"Breakeven price: ${breakeven:.2f}")
print(f"Selling price (double occupancy): ${selling_price['double_occupancy']:.2f}")
print(f"Margin: ${selling_price['margin_amount']:.2f} ({selling_price['margin_percentage']:.1%})")
```

---

## Tour Scheduling & Resource Allocation

### Multi-Tour Scheduling Optimization

```python
def optimize_tour_schedule(tours, vehicles, guides, planning_horizon_days=90):
    """
    Optimize tour departures and resource allocation

    Parameters:
    - tours: list of tour products with demand
    - vehicles: available vehicles/buses
    - guides: available tour guides
    - planning_horizon_days: scheduling window
    """
    from pulp import *

    prob = LpProblem("Tour_Scheduling", LpMaximize)

    # Decision variables: schedule tour t with vehicle v and guide g on day d
    x = {}

    for t, tour in enumerate(tours):
        for v, vehicle in enumerate(vehicles):
            for g, guide in enumerate(guides):
                for d in range(planning_horizon_days):
                    # Only if vehicle and guide are qualified for this tour
                    if (vehicle['capacity'] >= tour['min_pax'] and
                        tour['language'] in guide['languages']):
                        x[t, v, g, d] = LpVariable(
                            f"Schedule_{t}_{v}_{g}_{d}",
                            cat='Binary'
                        )

    # Objective: maximize revenue
    revenue = []

    for (t, v, g, d), var in x.items():
        tour = tours[t]
        # Revenue = passengers × price
        # Assume tour runs at 80% capacity
        expected_pax = vehicle['capacity'] * 0.8
        tour_revenue = expected_pax * tour['price_per_pax']

        revenue.append(tour_revenue * var)

    prob += lpSum(revenue)

    # Constraints

    # Vehicle can do one tour at a time
    for v, vehicle in enumerate(vehicles):
        for d in range(planning_horizon_days):
            # Check all tours that overlap with day d
            using_vehicle = []

            for (t, v_, g, d_start), var in x.items():
                if v_ == v:
                    tour = tours[t]
                    # Tour occupies vehicle from d_start to d_start + duration
                    if d_start <= d < d_start + tour['duration_days']:
                        using_vehicle.append(var)

            if using_vehicle:
                prob += lpSum(using_vehicle) <= 1

    # Guide can do one tour at a time
    for g, guide in enumerate(guides):
        for d in range(planning_horizon_days):
            using_guide = []

            for (t, v, g_, d_start), var in x.items():
                if g_ == g:
                    tour = tours[t]
                    if d_start <= d < d_start + tour['duration_days']:
                        using_guide.append(var)

            if using_guide:
                prob += lpSum(using_guide) <= 1

    # Meet minimum demand for popular tours
    for t, tour in enumerate(tours):
        min_departures = tour.get('min_departures_per_month', 0)

        if min_departures > 0:
            scheduled = lpSum([var for (t_, v, g, d) in x
                             if t_ == t and d < 30])
            prob += scheduled >= min_departures

    # Solve
    solver = PULP_CBC_CMD(msg=0, timeLimit=60)
    prob.solve(solver)

    # Extract schedule
    schedule = []
    for (t, v, g, d), var in x.items():
        if var.varValue > 0.5:
            tour = tours[t]
            schedule.append({
                'tour': tour['name'],
                'vehicle': vehicles[v]['id'],
                'guide': guides[g]['name'],
                'departure_day': d,
                'return_day': d + tour['duration_days'] - 1,
                'duration': tour['duration_days'],
                'expected_revenue': vehicle['capacity'] * 0.8 * tour['price_per_pax']
            })

    schedule_df = pd.DataFrame(schedule).sort_values('departure_day')

    return {
        'status': LpStatus[prob.status],
        'total_revenue': value(prob.objective),
        'schedule': schedule_df,
        'vehicle_utilization': {
            vehicles[v]['id']: len(schedule_df[schedule_df['vehicle'] == vehicles[v]['id']]) /
                              (planning_horizon_days / 7) * 100
            for v in range(len(vehicles))
        }
    }

# Example
tours = [
    {'name': 'City Highlights', 'duration_days': 1, 'min_pax': 10,
     'price_per_pax': 120, 'language': 'English', 'min_departures_per_month': 8},
    {'name': 'Wine Country', 'duration_days': 2, 'min_pax': 15,
     'price_per_pax': 250, 'language': 'English', 'min_departures_per_month': 4},
    {'name': 'Mountain Adventure', 'duration_days': 3, 'min_pax': 12,
     'price_per_pax': 450, 'language': 'English', 'min_departures_per_month': 4},
]

vehicles = [
    {'id': 'Bus_1', 'capacity': 45, 'type': 'motorcoach'},
    {'id': 'Bus_2', 'capacity': 45, 'type': 'motorcoach'},
    {'id': 'Van_1', 'capacity': 15, 'type': 'minibus'},
]

guides = [
    {'name': 'Guide_A', 'languages': ['English', 'Spanish']},
    {'name': 'Guide_B', 'languages': ['English', 'French']},
    {'name': 'Guide_C', 'languages': ['English', 'German']},
]

result = optimize_tour_schedule(tours, vehicles, guides, planning_horizon_days=30)
print(f"Total expected revenue: ${result['total_revenue']:,.0f}")
print(f"Tours scheduled: {len(result['schedule'])}")
```

---

## Itinerary Optimization

### Route Optimization for Multi-City Tours

```python
def optimize_tour_itinerary(cities, attractions_per_city, total_days,
                           start_city, end_city):
    """
    Optimize tour itinerary to maximize attraction value while meeting constraints

    Parameters:
    - cities: list of cities with travel times between them
    - attractions_per_city: dict of {city: [attractions]}
    - total_days: tour duration
    - start_city: starting point
    - end_city: ending point (can be same as start)
    """
    from pulp import *

    prob = LpProblem("Itinerary_Optimization", LpMaximize)

    # Variables

    # x[c, d]: visit city c on day d
    x = {}
    for city in cities:
        for day in range(total_days):
            x[city['id'], day] = LpVariable(f"Visit_{city['id']}_{day}",
                                           cat='Binary')

    # y[a]: include attraction a
    y = {}
    for city_id, attractions in attractions_per_city.items():
        for attraction in attractions:
            y[attraction['id']] = LpVariable(f"Include_{attraction['id']}",
                                            cat='Binary')

    # Objective: maximize total attraction value/interest score
    total_value = lpSum([y[attraction['id']] * attraction['value']
                        for city_id, attractions in attractions_per_city.items()
                        for attraction in attractions])

    prob += total_value

    # Constraints

    # Must start at start_city on day 0
    prob += x[start_city, 0] == 1

    # Must end at end_city on last day
    prob += x[end_city, total_days - 1] == 1

    # Visit exactly one city per day
    for day in range(total_days):
        prob += lpSum([x[city['id'], day] for city in cities]) == 1

    # Can only visit attraction if we visit that city
    for city_id, attractions in attractions_per_city.items():
        # Days spent in this city
        days_in_city = lpSum([x[city_id, d] for d in range(total_days)])

        for attraction in attractions:
            # Can only include attraction if we spend time in city
            prob += y[attraction['id']] <= days_in_city

    # Time budget per day (8 hours for activities)
    for day in range(total_days):
        for city in cities:
            city_id = city['id']

            # If we visit city on this day
            if (city_id, day) in x:
                # Total time for attractions on this day
                time_spent = lpSum([y[attraction['id']] * attraction['hours']
                                   for attraction in attractions_per_city.get(city_id, [])
                                   if (city_id, day) in x])

                # Time constraint (only if visiting city)
                prob += time_spent <= 8 * x[city_id, day]

    # Solve
    prob.solve(PULP_CBC_CMD(msg=0))

    # Extract itinerary
    itinerary = []
    for day in range(total_days):
        for city in cities:
            if x[city['id'], day].varValue > 0.5:
                # Find attractions included for this city
                included_attractions = [
                    attraction['name']
                    for attraction in attractions_per_city.get(city['id'], [])
                    if y[attraction['id']].varValue > 0.5
                ]

                itinerary.append({
                    'day': day + 1,
                    'city': city['name'],
                    'attractions': included_attractions
                })

    return {
        'total_value': value(prob.objective),
        'itinerary': itinerary
    }

# Example
cities = [
    {'id': 'paris', 'name': 'Paris'},
    {'id': 'amsterdam', 'name': 'Amsterdam'},
    {'id': 'brussels', 'name': 'Brussels'},
]

attractions_per_city = {
    'paris': [
        {'id': 'eiffel', 'name': 'Eiffel Tower', 'value': 10, 'hours': 2},
        {'id': 'louvre', 'name': 'Louvre Museum', 'value': 9, 'hours': 4},
        {'id': 'notre_dame', 'name': 'Notre-Dame', 'value': 7, 'hours': 1.5},
    ],
    'amsterdam': [
        {'id': 'rijks', 'name': 'Rijksmuseum', 'value': 8, 'hours': 3},
        {'id': 'anne_frank', 'name': 'Anne Frank House', 'value': 9, 'hours': 2},
        {'id': 'canal_tour', 'name': 'Canal Tour', 'value': 6, 'hours': 1.5},
    ],
    'brussels': [
        {'id': 'grand_place', 'name': 'Grand Place', 'value': 7, 'hours': 1},
        {'id': 'atomium', 'name': 'Atomium', 'value': 6, 'hours': 2},
    ],
}

result = optimize_tour_itinerary(cities, attractions_per_city, total_days=5,
                                start_city='paris', end_city='paris')

print(f"Total value: {result['total_value']}")
for day_plan in result['itinerary']:
    print(f"Day {day_plan['day']}: {day_plan['city']} - {', '.join(day_plan['attractions'])}")
```

---

## Demand Forecasting for Tours

### Tour Booking Forecasting

```python
def forecast_tour_bookings(historical_bookings, lead_times, seasonality,
                          special_events):
    """
    Forecast tour bookings considering booking pace and seasonality

    Factors:
    - Historical booking patterns
    - Lead time (when bookings are made)
    - Seasonality (high/low season)
    - Special events
    - Marketing campaigns
    """
    from sklearn.ensemble import GradientBoostingRegressor
    import pandas as pd

    df = historical_bookings.copy()

    # Time features
    df['departure_month'] = df['departure_date'].dt.month
    df['departure_day_of_week'] = df['departure_date'].dt.dayofweek
    df['booking_month'] = df['booking_date'].dt.month

    # Lead time (days before departure)
    df['booking_lead_days'] = (df['departure_date'] - df['booking_date']).dt.days

    # Seasonality
    high_season_months = [6, 7, 8, 12]
    df['is_high_season'] = df['departure_month'].isin(high_season_months).astype(int)

    # Special events
    df = df.merge(special_events, on='departure_date', how='left')
    df['has_special_event'] = df['event_type'].notna().astype(int)

    # Booking pace (bookings to date vs. same point last year)
    df['booking_pace'] = df['bookings_to_date'] / df['bookings_same_point_last_year']

    # Price features
    df['price_change_pct'] = (df['current_price'] - df['price_last_year']) / df['price_last_year']

    # Marketing
    df['marketing_spend'] = df.get('marketing_spend', 0)

    # Lag features
    df['bookings_last_departure'] = df.groupby('tour_id')['total_bookings'].shift(1)

    # Drop NaN
    df = df.dropna()

    # Features
    feature_cols = ['departure_month', 'departure_day_of_week',
                   'booking_lead_days', 'is_high_season', 'has_special_event',
                   'booking_pace', 'price_change_pct', 'marketing_spend',
                   'bookings_last_departure']

    X = df[feature_cols]
    y = df['total_bookings']

    # Train model
    model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1,
                                     max_depth=5, random_state=42)
    model.fit(X, y)

    return {
        'model': model,
        'train_r2': model.score(X, y),
        'feature_importance': dict(zip(feature_cols, model.feature_importances_))
    }
```

---

## Group Series Management

### Hotel Series Allocation

```python
def optimize_hotel_series_allocation(tours, hotels, dates, room_types):
    """
    Optimize hotel room series (pre-bookings) for tour programs

    Series = Block of rooms held at contracted rates for tour season

    Parameters:
    - tours: list of tour products with expected departures
    - hotels: available hotels with contracted rates
    - dates: planning period
    - room_types: types of rooms needed
    """
    from pulp import *

    prob = LpProblem("Series_Allocation", LpMinimize)

    # Variables: commit to X rooms at hotel h for date d
    series_commitment = {}

    for h, hotel in enumerate(hotels):
        for d in dates:
            series_commitment[h, d] = LpVariable(
                f"Series_{h}_{d}",
                lowBound=0,
                cat='Integer'
            )

    # Objective: minimize total series cost (commitment × rate)
    total_cost = []

    for (h, d), var in series_commitment.items():
        hotel = hotels[h]
        # Series rate (typically 10-20% below BAR)
        series_rate = hotel['rack_rate'] * 0.85
        total_cost.append(var * series_rate)

    prob += lpSum(total_cost)

    # Constraints

    # Meet tour demand
    for d in dates:
        # Expected room nights needed on date d (from all tours)
        required_rooms = sum([
            tour['expected_pax'] / 2  # Assume double occupancy
            for tour in tours
            if d in tour['dates']
        ])

        # Total series allocation must meet demand
        prob += lpSum([series_commitment[h, d] for h in range(len(hotels))]) >= \
                required_rooms

    # Hotel series limits
    for h, hotel in enumerate(hotels):
        max_series = hotel.get('max_series_allocation', 50)

        for d in dates:
            prob += series_commitment[h, d] <= max_series

    # Solve
    prob.solve(PULP_CBC_CMD(msg=0))

    # Extract allocations
    allocations = []
    for (h, d), var in series_commitment.items():
        if var.varValue > 0:
            allocations.append({
                'hotel': hotels[h]['name'],
                'date': d,
                'rooms_committed': var.varValue,
                'rate': hotels[h]['rack_rate'] * 0.85
            })

    return {
        'total_cost': value(prob.objective),
        'allocations': pd.DataFrame(allocations)
    }
```

---

## Tools & Libraries

### Python Libraries

**Optimization:**
- `PuLP`: Linear programming
- `OR-Tools`: Route optimization
- `scipy.optimize`: General optimization

**Forecasting & Analytics:**
- `scikit-learn`: Machine learning
- `prophet`: Time series forecasting
- `pandas`, `numpy`: Data analysis

**Geospatial:**
- `geopy`: Distance calculations
- `folium`: Mapping and visualization

### Commercial Software

**Tour Operator Systems:**
- **TourCMS**: Tour operator CMS
- **Rezdy**: Tour and activity booking platform
- **TourWriter**: Tour itinerary and costing software
- **Ezus**: Tour operator software
- **Bewotec**: Tour operator ERP

**Booking & Distribution:**
- **Regiondo**: Activity booking system
- **FareHarbor**: Tour booking and ticketing
- **Peek**: Tour and activity marketplace
- **Bokun**: Tour distribution platform

**Transportation Management:**
- **Omnitracs**: Fleet management
- **Samsara**: Vehicle tracking and management
- **Verizon Connect**: GPS fleet tracking

**Finance & Operations:**
- **QuickBooks**: Accounting
- **Xero**: Cloud accounting
- **TravelWorks**: Tour accounting and operations

---

## Common Challenges & Solutions

### Challenge: Low Utilization / Empty Seats

**Problem:**
- Tours departing with few passengers
- High fixed costs spread over few pax
- Low profitability

**Solutions:**
- Dynamic departure minimums
- Guaranteed departures for flagship tours
- Private tour premiums
- Last-minute promotions and discounts
- Consolidation with other operators
- Flexible itineraries (SIT vs. GIT)

### Challenge: Seasonal Demand Fluctuations

**Problem:**
- Extreme peaks and troughs
- Underutilized resources in low season
- Staff retention challenges

**Solutions:**
- Diversified portfolio (year-round destinations)
- Seasonal tour products
- Dynamic pricing (high/low season)
- Shoulder season promotions
- Special interest tours in off-season
- International market mix (opposite seasons)

### Challenge: Supplier Rate Fluctuations

**Problem:**
- Hotel and service costs changing
- Currency fluctuations
- Fuel costs impacting transportation

**Solutions:**
- Series contracts (guaranteed rates)
- Currency hedging
- Fuel surcharge clauses
- Multi-year contracts with escalation clauses
- Diversified supplier base
- Value engineering (alternative suppliers)

### Challenge: Guide Quality & Availability

**Problem:**
- Inconsistent guide quality
- Guide shortages in peak season
- Training and certification costs

**Solutions:**
- Guide training programs
- Quality monitoring and feedback
- Tiered guide system (lead guides, assistants)
- Freelance guide network
- Guide scheduling optimization
- Performance incentives

---

## Output Format

### Tour Operations Report

**Executive Summary:**
- Tour portfolio performance
- Key operational metrics
- Profitability analysis
- Strategic recommendations

**Tour Performance:**

| Tour Name | Departures | Pax | Occupancy | Revenue | Cost | Margin | Margin % |
|-----------|------------|-----|-----------|---------|------|--------|----------|
| City Highlights | 45 | 1,215 | 60% | $145,800 | $109,350 | $36,450 | 25% |
| Wine Country | 18 | 432 | 80% | $108,000 | $75,600 | $32,400 | 30% |
| Mountain Adventure | 12 | 324 | 75% | $145,800 | $102,060 | $43,740 | 30% |
| **Total** | **75** | **1,971** | **70%** | **$399,600** | **$287,010** | **$112,590** | **28%** |

**Resource Utilization:**

| Resource | Utilization | Available Days | Active Days | Idle Days |
|----------|-------------|----------------|-------------|-----------|
| Bus 1 | 85% | 90 | 77 | 13 |
| Bus 2 | 78% | 90 | 70 | 20 |
| Van 1 | 62% | 90 | 56 | 34 |
| Guide A | 92% | 90 | 83 | 7 |
| Guide B | 88% | 90 | 79 | 11 |

**Booking Pace (Next 60 Days):**

| Departure Date | Tour | Current Bookings | Forecast | Status |
|----------------|------|------------------|----------|--------|
| 2026-03-15 | City Highlights | 28 | 35 | On Track |
| 2026-03-20 | Wine Country | 8 | 24 | Soft - Promote |
| 2026-03-25 | Mountain Adventure | 18 | 27 | Good |

**Profitability by Tour Type:**

| Category | Revenue | Cost | Margin | Margin % |
|----------|---------|------|--------|----------|
| Day Tours | $145,800 | $109,350 | $36,450 | 25% |
| Multi-Day Tours | $253,800 | $177,660 | $76,140 | 30% |
| **Total** | **$399,600** | **$287,010** | **$112,590** | **28%** |

**Action Items:**
1. Increase marketing spend for Wine Country tour (March departures)
2. Negotiate better hotel rates in Rome (15% of tour cost)
3. Add Bus 3 to fleet for summer season (June-August)
4. Develop new shoulder-season product (April-May)
5. Implement dynamic pricing for City Highlights

---

## Questions to Ask

If you need more context:
1. What type of tour operator? (inbound, outbound, DMC, ground handler)
2. What tours are in the portfolio? (types, durations, volumes)
3. What resources do you manage? (vehicles, guides, hotels)
4. What are the primary challenges? (profitability, utilization, operations)
5. What systems are in place? (booking, operations, accounting)
6. What's the competitive environment and positioning?
7. What are the seasonal patterns?

---

## Related Skills

- **hotel-inventory-management**: For hotel accommodation management
- **route-optimization**: For transportation routing
- **hospitality-procurement**: For purchasing and supplier management
- **demand-forecasting**: For booking forecasting
- **seasonal-planning**: For seasonal demand management
- **airline-cargo-optimization**: For air transportation
- **cruise-supply-chain**: For cruise operations
- **fleet-management**: For vehicle fleet management
