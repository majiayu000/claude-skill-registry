---
name: promotional-planning
description: When the user wants to plan promotions, optimize trade spending, forecast promotional lift, or manage promotional supply chain. Also use when the user mentions "trade promotions," "promotional forecasting," "TPM," "TPO," "promotional uplift," "feature and display," "markdown optimization," or "promotional calendar." For pricing optimization, see markdown-optimization. For demand forecasting, see demand-forecasting.
---

# Promotional Planning

You are an expert in CPG promotional planning and trade promotion optimization. Your goal is to help design effective promotional strategies that maximize ROI while ensuring supply chain readiness to support promotional execution.

## Initial Assessment

Before planning promotions, understand:

1. **Business Context**
   - What products/categories for promotion?
   - What retailers/channels? (grocery, club, convenience, online)
   - What's the promotional budget and objectives?
   - Historical promotional effectiveness (ROI, lift, incrementality)?

2. **Promotional Strategy**
   - Promotion types used? (TPR, BOGO, multi-buy, coupons)
   - Typical promotional mechanics? (price discount %, feature, display)
   - Promotional frequency? (events per year per SKU)
   - Competitive promotional activity?

3. **Data Availability**
   - Historical promotional performance data?
   - Baseline vs. promotional sales data?
   - Syndicated data (Nielsen, IRI)?
   - Retailer POS data access?
   - Cost data (trade spend, slotting, displays)?

4. **Supply Chain Readiness**
   - Lead times for promotional builds?
   - Production capacity constraints?
   - Promotional inventory locations (forward-buy)?
   - Distribution center capacity for surge?

---

## Promotional Planning Framework

### Trade Promotion Types

**1. Temporary Price Reduction (TPR)**
- Discount from regular shelf price
- Typical: 15-30% off
- Most common promotion type
- Retailer passes discount to consumer

**2. Feature Advertising**
- Product featured in retailer circular/ad
- Typically paired with TPR
- High visibility, strong lift
- Cost: Ad allowance to retailer

**3. Display**
- Secondary placement (end cap, floor stand)
- Increases visibility and impulse
- Often paired with TPR and feature
- Cost: Display allowance

**4. Multi-Buy Offers**
- "Buy 2 Get 1 Free", "Buy 3 for $5"
- Encourages pantry loading
- Higher average transaction size
- Can cannibalize future sales

**5. Coupons**
- Manufacturer or retailer coupons
- Target specific consumers
- Trackable redemption
- Growing: digital and mobile coupons

**6. In-Store Events**
- Sampling, demonstrations
- Product education
- High engagement, expensive
- Good for new products

**7. Loyalty Programs**
- Points, rewards, personalized offers
- Growing importance (digital)
- Retailer-specific
- Ongoing vs. event-based

---

## Promotional Lift Modeling

### Baseline vs. Incremental Sales

**Baseline Sales:**
- Sales that would occur without promotion
- Critical to calculate true lift
- Methods: average non-promotional weeks, time series decomposition

**Incremental Sales:**
- Additional sales caused by promotion
- Incremental = Promotional Sales - Baseline
- Key metric for ROI calculation

**Lift Factor:**
```
Lift = (Promotional Sales - Baseline Sales) / Baseline Sales
```

### Promotional Response Models

**1. Price Elasticity Model**

```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm

def estimate_price_elasticity(sales_data):
    """
    Estimate price elasticity from historical data

    Parameters:
    - sales_data: DataFrame with columns ['price', 'volume', 'feature',
                  'display', 'week', 'sku']

    Returns:
    - elasticity coefficient and model
    """

    # Log-log model for elasticity
    sales_data['log_price'] = np.log(sales_data['price'])
    sales_data['log_volume'] = np.log(sales_data['volume'])

    # Add promotional variables
    X = sales_data[['log_price', 'feature', 'display']]
    X = sm.add_constant(X)
    y = sales_data['log_volume']

    # OLS regression
    model = sm.OLS(y, X).fit()

    elasticity = {
        'price_elasticity': model.params['log_price'],
        'feature_lift': np.exp(model.params['feature']) - 1,
        'display_lift': np.exp(model.params['display']) - 1,
        'r_squared': model.rsquared,
        'model': model
    }

    return elasticity

# Example usage
sales_data = pd.DataFrame({
    'price': [3.99, 3.99, 2.99, 2.99, 3.99, 2.99],
    'volume': [1000, 1100, 1800, 2000, 950, 1850],
    'feature': [0, 0, 1, 1, 0, 1],
    'display': [0, 0, 0, 1, 0, 1]
})

elasticity = estimate_price_elasticity(sales_data)
print(f"Price Elasticity: {elasticity['price_elasticity']:.2f}")
print(f"Feature Lift: {elasticity['feature_lift']:.1%}")
print(f"Display Lift: {elasticity['display_lift']:.1%}")
```

**2. Multiplicative Promotional Model**

```python
def promotional_uplift_model(baseline, price_discount, feature, display):
    """
    Calculate promotional uplift using multiplicative model

    Parameters:
    - baseline: baseline sales volume
    - price_discount: % discount (e.g., 0.20 for 20% off)
    - feature: 1 if featured, 0 otherwise
    - display: 1 if on display, 0 otherwise

    Returns:
    - predicted promotional sales
    """

    # Typical lift factors (calibrate from historical data)
    PRICE_ELASTICITY = -2.5  # 10% price cut → 25% volume increase
    FEATURE_LIFT = 1.5       # Feature alone increases sales 50%
    DISPLAY_LIFT = 2.0       # Display alone doubles sales

    # Price effect
    price_effect = (1 + price_discount) ** PRICE_ELASTICITY

    # Feature effect
    feature_effect = FEATURE_LIFT if feature else 1.0

    # Display effect
    display_effect = DISPLAY_LIFT if display else 1.0

    # Multiplicative model
    promotional_sales = baseline * price_effect * feature_effect * display_effect

    return promotional_sales

# Example: 20% discount with feature and display
baseline = 1000
promo_sales = promotional_uplift_model(
    baseline=baseline,
    price_discount=0.20,
    feature=1,
    display=1
)

lift = (promo_sales - baseline) / baseline
print(f"Baseline: {baseline}")
print(f"Promotional Sales: {promo_sales:.0f}")
print(f"Lift: {lift:.1%}")
```

**3. Machine Learning Promotional Model**

```python
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

def train_promotional_model(historical_data):
    """
    Train ML model to predict promotional sales

    Parameters:
    - historical_data: DataFrame with promotional events and outcomes

    Returns:
    - trained model and performance metrics
    """

    # Features
    feature_cols = [
        'regular_price',
        'promotional_price',
        'discount_pct',
        'feature',
        'display',
        'brand',
        'category',
        'retailer',
        'week_of_year',
        'holiday_week',
        'competitive_promos',
        'inventory_level',
        'days_since_last_promo'
    ]

    X = historical_data[feature_cols]
    y = historical_data['promotional_sales']

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Gradient Boosting model
    model = GradientBoostingRegressor(
        n_estimators=200,
        learning_rate=0.1,
        max_depth=5,
        random_state=42
    )

    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': feature_cols,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)

    return {
        'model': model,
        'mae': mae,
        'r2': r2,
        'feature_importance': feature_importance
    }
```

---

## Promotional ROI Analysis

### ROI Calculation Framework

```python
def calculate_promotional_roi(promo_data):
    """
    Calculate comprehensive promotional ROI

    Parameters:
    - promo_data: dict with promotional details

    Returns:
    - ROI metrics and profitability analysis
    """

    # Sales metrics
    baseline_units = promo_data['baseline_units']
    promo_units = promo_data['promo_units']
    incremental_units = promo_units - baseline_units

    regular_price = promo_data['regular_price']
    promo_price = promo_data['promo_price']

    # Revenue
    baseline_revenue = baseline_units * regular_price
    promo_revenue = promo_units * promo_price
    incremental_revenue = promo_revenue - baseline_revenue

    # Costs
    cogs = promo_data['cogs_per_unit']
    baseline_cogs = baseline_units * cogs
    promo_cogs = promo_units * cogs
    incremental_cogs = promo_cogs - baseline_cogs

    # Trade spending
    trade_spend = {
        'price_discount': baseline_units * (regular_price - promo_price),
        'off_invoice': promo_data.get('off_invoice', 0),
        'feature_allowance': promo_data.get('feature_cost', 0),
        'display_allowance': promo_data.get('display_cost', 0),
        'slotting_fees': promo_data.get('slotting', 0),
        'coop_advertising': promo_data.get('coop_ad', 0)
    }

    total_trade_spend = sum(trade_spend.values())

    # Incremental profit
    baseline_profit = baseline_revenue - baseline_cogs
    promo_gross_profit = promo_revenue - promo_cogs
    incremental_gross_profit = promo_gross_profit - baseline_profit

    # Net incremental profit (after trade spend)
    net_incremental_profit = incremental_gross_profit - total_trade_spend

    # ROI
    roi = net_incremental_profit / total_trade_spend if total_trade_spend > 0 else 0

    # Payback
    payback = total_trade_spend / incremental_gross_profit if incremental_gross_profit > 0 else float('inf')

    return {
        'baseline_units': baseline_units,
        'promo_units': promo_units,
        'incremental_units': incremental_units,
        'lift_pct': (incremental_units / baseline_units * 100),
        'baseline_revenue': baseline_revenue,
        'promo_revenue': promo_revenue,
        'incremental_revenue': incremental_revenue,
        'baseline_profit': baseline_profit,
        'promo_profit': promo_gross_profit,
        'incremental_profit': incremental_gross_profit,
        'trade_spend': total_trade_spend,
        'trade_spend_breakdown': trade_spend,
        'net_profit': net_incremental_profit,
        'roi': roi,
        'roi_pct': roi * 100,
        'payback': payback
    }

# Example
promo_result = calculate_promotional_roi({
    'baseline_units': 1000,
    'promo_units': 2500,
    'regular_price': 4.99,
    'promo_price': 3.99,
    'cogs_per_unit': 2.50,
    'off_invoice': 500,
    'feature_cost': 1000,
    'display_cost': 800,
    'slotting': 0,
    'coop_ad': 500
})

print(f"Lift: {promo_result['lift_pct']:.0f}%")
print(f"Incremental Units: {promo_result['incremental_units']}")
print(f"Trade Spend: ${promo_result['trade_spend']:,.0f}")
print(f"Net Profit: ${promo_result['net_profit']:,.0f}")
print(f"ROI: {promo_result['roi_pct']:.0f}%")
```

### Post-Promotion Analysis

```python
def post_promotion_analysis(sales_data, promo_start_week, promo_duration):
    """
    Analyze post-promotion effects including cannibalization

    Parameters:
    - sales_data: weekly sales data
    - promo_start_week: week number promotion started
    - promo_duration: number of weeks promotion ran

    Returns:
    - analysis of pre, during, and post promotion periods
    """

    promo_end_week = promo_start_week + promo_duration

    # Define periods
    pre_promo = sales_data[
        (sales_data['week'] >= promo_start_week - 4) &
        (sales_data['week'] < promo_start_week)
    ]

    during_promo = sales_data[
        (sales_data['week'] >= promo_start_week) &
        (sales_data['week'] < promo_end_week)
    ]

    post_promo = sales_data[
        (sales_data['week'] >= promo_end_week) &
        (sales_data['week'] < promo_end_week + 4)
    ]

    # Calculate averages
    avg_pre = pre_promo['sales'].mean()
    avg_during = during_promo['sales'].mean()
    avg_post = post_promo['sales'].mean()

    # Pantry loading effect (post-promo dip)
    pantry_loading = avg_pre - avg_post if avg_post < avg_pre else 0

    # True incrementality (accounting for pantry loading)
    total_promo_sales = during_promo['sales'].sum()
    expected_baseline = avg_pre * promo_duration
    post_promo_impact = pantry_loading * len(post_promo)

    true_incremental = total_promo_sales - expected_baseline - post_promo_impact

    return {
        'avg_pre_promo': avg_pre,
        'avg_during_promo': avg_during,
        'avg_post_promo': avg_post,
        'lift_during': (avg_during - avg_pre) / avg_pre * 100,
        'post_promo_dip': (avg_pre - avg_post) / avg_pre * 100,
        'pantry_loading': pantry_loading,
        'true_incremental_sales': true_incremental,
        'true_incrementality_pct': true_incremental / expected_baseline * 100
    }
```

---

## Promotional Optimization

### Optimal Promotional Calendar

```python
from pulp import *
import pandas as pd
import numpy as np

def optimize_promotional_calendar(products, budget, constraints):
    """
    Optimize promotional calendar to maximize ROI within budget

    Parameters:
    - products: DataFrame with product promotional opportunities
    - budget: total promotional budget
    - constraints: dict with business constraints

    Returns:
    - optimal promotional calendar
    """

    # Create problem
    prob = LpProblem("Promotional_Optimization", LpMaximize)

    # Decision variables: promote product i in week w
    promo_vars = {}
    for idx, row in products.iterrows():
        for week in range(1, 53):
            var_name = f"promo_{row['sku']}_{week}"
            promo_vars[row['sku'], week] = LpVariable(
                var_name,
                cat='Binary'
            )

    # Objective: Maximize total incremental profit
    prob += lpSum([
        promo_vars[row['sku'], week] * row['incremental_profit']
        for idx, row in products.iterrows()
        for week in range(1, 53)
    ])

    # Constraint 1: Total budget
    prob += lpSum([
        promo_vars[row['sku'], week] * row['trade_spend']
        for idx, row in products.iterrows()
        for week in range(1, 53)
    ]) <= budget

    # Constraint 2: Minimum weeks between promotions per SKU
    min_gap = constraints.get('min_weeks_between_promos', 8)
    for idx, row in products.iterrows():
        sku = row['sku']
        for week in range(1, 53):
            # If promoting in week w, can't promote in next min_gap weeks
            prob += lpSum([
                promo_vars[sku, w]
                for w in range(week, min(week + min_gap, 53))
            ]) <= 1

    # Constraint 3: Maximum promotions per week (capacity)
    max_promos_per_week = constraints.get('max_promos_per_week', 10)
    for week in range(1, 53):
        prob += lpSum([
            promo_vars[row['sku'], week]
            for idx, row in products.iterrows()
        ]) <= max_promos_per_week

    # Constraint 4: Minimum promotions per SKU per year
    min_promos_per_sku = constraints.get('min_promos_per_sku', 2)
    for idx, row in products.iterrows():
        sku = row['sku']
        prob += lpSum([
            promo_vars[sku, week]
            for week in range(1, 53)
        ]) >= min_promos_per_sku

    # Solve
    prob.solve(PULP_CBC_CMD(msg=0))

    # Extract solution
    calendar = []
    for idx, row in products.iterrows():
        for week in range(1, 53):
            if promo_vars[row['sku'], week].varValue > 0.5:
                calendar.append({
                    'sku': row['sku'],
                    'week': week,
                    'trade_spend': row['trade_spend'],
                    'incremental_profit': row['incremental_profit'],
                    'roi': row['incremental_profit'] / row['trade_spend']
                })

    calendar_df = pd.DataFrame(calendar)

    results = {
        'status': LpStatus[prob.status],
        'total_profit': value(prob.objective),
        'total_spend': calendar_df['trade_spend'].sum(),
        'avg_roi': calendar_df['roi'].mean(),
        'num_promotions': len(calendar_df),
        'calendar': calendar_df.sort_values(['week', 'sku'])
    }

    return results
```

### Promotional Price Optimization

```python
def optimize_promotional_price(baseline_volume, regular_price, cogs,
                                elasticity, fixed_costs):
    """
    Find optimal promotional price to maximize profit

    Parameters:
    - baseline_volume: baseline unit sales at regular price
    - regular_price: regular shelf price
    - cogs: cost of goods sold per unit
    - elasticity: price elasticity coefficient
    - fixed_costs: fixed promotional costs (feature, display, etc.)

    Returns:
    - optimal promotional price and expected profit
    """

    def profit_function(promo_price):
        """Calculate profit at given promotional price"""

        # Price change
        price_change = (promo_price - regular_price) / regular_price

        # Volume with price elasticity
        volume = baseline_volume * (1 + elasticity * price_change)

        # Revenue and costs
        revenue = volume * promo_price
        variable_costs = volume * cogs
        total_costs = variable_costs + fixed_costs

        # Profit
        profit = revenue - total_costs

        return -profit  # Negative for minimization

    from scipy.optimize import minimize_scalar

    # Optimize price (bounded between 50% and 90% of regular price)
    result = minimize_scalar(
        profit_function,
        bounds=(regular_price * 0.5, regular_price * 0.9),
        method='bounded'
    )

    optimal_price = result.x
    optimal_profit = -result.fun

    # Calculate metrics at optimal price
    price_change = (optimal_price - regular_price) / regular_price
    optimal_volume = baseline_volume * (1 + elasticity * price_change)
    discount_pct = (1 - optimal_price / regular_price) * 100

    return {
        'optimal_price': optimal_price,
        'discount_pct': discount_pct,
        'expected_volume': optimal_volume,
        'expected_profit': optimal_profit,
        'lift': (optimal_volume - baseline_volume) / baseline_volume * 100
    }

# Example
result = optimize_promotional_price(
    baseline_volume=1000,
    regular_price=4.99,
    cogs=2.50,
    elasticity=-2.5,
    fixed_costs=2000
)

print(f"Optimal Price: ${result['optimal_price']:.2f}")
print(f"Discount: {result['discount_pct']:.0f}%")
print(f"Expected Volume: {result['expected_volume']:.0f}")
print(f"Expected Profit: ${result['expected_profit']:.0f}")
```

---

## Supply Chain for Promotions

### Promotional Demand Forecasting

```python
def forecast_promotional_demand(sku, retailer, promo_mechanics,
                                 historical_promos):
    """
    Forecast demand for upcoming promotion

    Parameters:
    - sku: product SKU
    - retailer: retailer identifier
    - promo_mechanics: dict with discount, feature, display
    - historical_promos: DataFrame with past promotional performance

    Returns:
    - promotional forecast
    """

    # Filter to similar promotions
    similar_promos = historical_promos[
        (historical_promos['sku'] == sku) &
        (historical_promos['retailer'] == retailer)
    ]

    if len(similar_promos) == 0:
        # No history, use category average
        similar_promos = historical_promos[
            historical_promos['category'] == get_category(sku)
        ]

    # Calculate average lift for similar mechanics
    discount_range = promo_mechanics['discount_pct']
    has_feature = promo_mechanics['feature']
    has_display = promo_mechanics['display']

    similar_mechanics = similar_promos[
        (similar_promos['discount_pct'].between(discount_range - 5, discount_range + 5)) &
        (similar_promos['feature'] == has_feature) &
        (similar_promos['display'] == has_display)
    ]

    if len(similar_mechanics) > 0:
        avg_lift = similar_mechanics['lift'].mean()
        std_lift = similar_mechanics['lift'].std()
    else:
        # Use regression model
        avg_lift = predict_lift_from_model(promo_mechanics)
        std_lift = 0.3  # Assume 30% std dev

    # Get baseline forecast
    baseline = get_baseline_forecast(sku, retailer)

    # Promotional forecast
    forecast = {
        'baseline': baseline,
        'expected_lift': avg_lift,
        'promo_forecast': baseline * (1 + avg_lift),
        'low_forecast': baseline * (1 + avg_lift - std_lift),  # P10
        'high_forecast': baseline * (1 + avg_lift + std_lift),  # P90
        'confidence': 'high' if len(similar_mechanics) >= 3 else 'low'
    }

    return forecast
```

### Promotional Inventory Planning

```python
def plan_promotional_inventory(promo_forecast, lead_time_days,
                                safety_factor=1.2):
    """
    Calculate promotional inventory requirements

    Parameters:
    - promo_forecast: dict from forecast_promotional_demand
    - lead_time_days: production/procurement lead time
    - safety_factor: buffer multiplier (1.2 = 20% safety stock)

    Returns:
    - inventory plan with build schedule
    """

    # Expected promotional volume
    expected_volume = promo_forecast['promo_forecast']

    # Safety stock for uncertainty
    forecast_uncertainty = (
        promo_forecast['high_forecast'] - promo_forecast['low_forecast']
    ) / 2

    safety_stock = forecast_uncertainty * safety_factor

    # Total inventory needed
    total_needed = expected_volume + safety_stock

    # Build schedule (when to produce)
    promo_start_date = promo_forecast.get('start_date')
    build_start_date = promo_start_date - pd.Timedelta(days=lead_time_days + 7)

    # Pre-build strategy
    inventory_plan = {
        'promotional_forecast': expected_volume,
        'safety_stock': safety_stock,
        'total_inventory_needed': total_needed,
        'build_start_date': build_start_date,
        'promo_start_date': promo_start_date,
        'lead_time_days': lead_time_days,
        'recommended_locations': determine_forward_stock_locations(
            promo_forecast
        )
    }

    return inventory_plan

def determine_forward_stock_locations(promo_forecast):
    """
    Determine where to pre-position promotional inventory
    """

    retailer = promo_forecast.get('retailer')
    volume = promo_forecast['promo_forecast']

    # Strategy based on volume
    if volume > 10000:  # Large promotion
        return {
            'strategy': 'forward_stock',
            'locations': ['retailer_dc', 'manufacturer_dc'],
            'split': {'retailer_dc': 0.7, 'manufacturer_dc': 0.3}
        }
    elif volume > 5000:  # Medium promotion
        return {
            'strategy': 'partial_forward',
            'locations': ['retailer_dc'],
            'split': {'retailer_dc': 1.0}
        }
    else:  # Small promotion
        return {
            'strategy': 'pull_from_stock',
            'locations': ['manufacturer_dc'],
            'split': {'manufacturer_dc': 1.0}
        }
```

### Promotional Capacity Planning

```python
def assess_promotional_capacity(promotional_calendar, production_capacity,
                                 dc_capacity):
    """
    Assess if supply chain can support promotional calendar

    Parameters:
    - promotional_calendar: DataFrame with planned promotions by week
    - production_capacity: available production capacity by week
    - dc_capacity: DC storage capacity

    Returns:
    - capacity analysis and bottlenecks
    """

    # Aggregate demand by week
    weekly_demand = promotional_calendar.groupby('week').agg({
        'forecasted_volume': 'sum',
        'num_promos': 'count'
    })

    # Add production lead time offset
    LEAD_TIME_WEEKS = 4
    weekly_demand['production_week'] = weekly_demand.index - LEAD_TIME_WEEKS

    # Check production capacity
    capacity_issues = []

    for week, row in weekly_demand.iterrows():
        prod_week = row['production_week']

        if prod_week < 1:
            continue

        required = row['forecasted_volume']
        available = production_capacity.get(prod_week, 0)

        if required > available:
            capacity_issues.append({
                'week': prod_week,
                'type': 'production',
                'required': required,
                'available': available,
                'gap': required - available,
                'utilization': required / available * 100
            })

    # Check DC capacity
    # Calculate cumulative inventory build-up
    inventory_profile = calculate_inventory_profile(
        promotional_calendar,
        production_capacity
    )

    for week, inventory in inventory_profile.items():
        if inventory > dc_capacity:
            capacity_issues.append({
                'week': week,
                'type': 'storage',
                'required': inventory,
                'available': dc_capacity,
                'gap': inventory - dc_capacity,
                'utilization': inventory / dc_capacity * 100
            })

    return {
        'capacity_ok': len(capacity_issues) == 0,
        'issues': capacity_issues,
        'max_production_utilization': max(
            i['utilization'] for i in capacity_issues
            if i['type'] == 'production'
        ) if capacity_issues else 0,
        'recommendations': generate_capacity_recommendations(capacity_issues)
    }
```

---

## Promotional Analytics

### Promotional Performance Dashboard

```python
def generate_promotional_scorecard(promotional_data):
    """
    Generate comprehensive promotional performance scorecard

    Parameters:
    - promotional_data: DataFrame with promotional events and results

    Returns:
    - scorecard metrics
    """

    scorecard = {}

    # Overall metrics
    scorecard['total_promotions'] = len(promotional_data)
    scorecard['total_trade_spend'] = promotional_data['trade_spend'].sum()
    scorecard['total_incremental_profit'] = promotional_data['incremental_profit'].sum()

    # ROI metrics
    scorecard['avg_roi'] = (
        promotional_data['incremental_profit'].sum() /
        promotional_data['trade_spend'].sum()
    )
    scorecard['roi_pct'] = scorecard['avg_roi'] * 100

    positive_roi = promotional_data[promotional_data['incremental_profit'] > 0]
    scorecard['pct_positive_roi'] = len(positive_roi) / len(promotional_data) * 100

    # Lift metrics
    scorecard['avg_lift'] = promotional_data['lift_pct'].mean()
    scorecard['median_lift'] = promotional_data['lift_pct'].median()

    # Effectiveness by mechanic
    scorecard['mechanics'] = promotional_data.groupby('mechanic').agg({
        'roi': 'mean',
        'lift_pct': 'mean',
        'trade_spend': 'sum',
        'promo_id': 'count'
    }).rename(columns={'promo_id': 'count'})

    # Top performers
    scorecard['top_10_promos'] = promotional_data.nlargest(10, 'incremental_profit')[
        ['sku', 'retailer', 'mechanic', 'incremental_profit', 'roi']
    ]

    # Bottom performers
    scorecard['bottom_10_promos'] = promotional_data.nsmallest(10, 'incremental_profit')[
        ['sku', 'retailer', 'mechanic', 'incremental_profit', 'roi']
    ]

    # Efficiency metrics
    scorecard['spend_per_incremental_unit'] = (
        promotional_data['trade_spend'].sum() /
        promotional_data['incremental_units'].sum()
    )

    return scorecard
```

---

## Tools & Libraries

### Commercial Software

**Trade Promotion Management (TPM):**
- **SAP TPM**: Integrated with SAP ERP
- **Oracle TPM**: Trade promotion management and optimization
- **AFS TPM**: Analytical Frameworks Solutions
- **Wipro Promax**: Cloud-based TPM
- **Blacksmith Applications**: TPM/TPO software
- **IRI PromoPlanner**: Analytics-driven planning

**Trade Promotion Optimization (TPO):**
- **Anaplan**: Cloud planning with promotion optimization
- **o9 Solutions**: AI-driven promotional planning
- **Blue Yonder**: Price and promotion optimization
- **Revionics**: Price and promo optimization (Oracle)
- **TABS Analytics**: Promotional forecasting and planning

**Analytics Platforms:**
- **Nielsen**: Syndicated sales data and promotional analytics
- **IRI**: Market measurement and promotion insights
- **Numerator**: Consumer panel and promotional tracking
- **84.51° (Kroger)**: Retail data and promotional analytics

### Python Libraries

```python
# Core libraries for promotional analysis

# Data manipulation and analysis
import pandas as pd
import numpy as np

# Statistical modeling
import statsmodels.api as sm
from statsmodels.tsa.seasonal import seasonal_decompose
from scipy import stats
from scipy.optimize import minimize

# Machine learning
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score

# Optimization
from pulp import *
import pyomo.environ as pyo

# Visualization
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

# Time series
from prophet import Prophet
import pmdarima as pm
```

### Promotional Analysis Template

```python
class PromotionalAnalyzer:
    """
    Comprehensive promotional analysis framework
    """

    def __init__(self, sales_data, promotional_events):
        self.sales_data = sales_data
        self.promo_events = promotional_events
        self.baseline_model = None
        self.lift_model = None

    def calculate_baseline(self, method='moving_average', window=4):
        """Calculate baseline sales (non-promotional)"""

        if method == 'moving_average':
            # Use non-promotional weeks only
            non_promo = self.sales_data[self.sales_data['promo'] == 0]
            baseline = non_promo.rolling(window=window)['sales'].mean()

        elif method == 'regression':
            # Time series regression
            X = np.arange(len(self.sales_data)).reshape(-1, 1)
            y = self.sales_data[self.sales_data['promo'] == 0]['sales']
            model = LinearRegression().fit(X, y)
            baseline = model.predict(X)

        return baseline

    def measure_lift(self):
        """Measure promotional lift for each event"""

        results = []

        for idx, promo in self.promo_events.iterrows():
            # Get sales during promotion
            promo_sales = self.sales_data[
                (self.sales_data['week'] >= promo['start_week']) &
                (self.sales_data['week'] <= promo['end_week'])
            ]['sales'].sum()

            # Get baseline
            baseline = self.sales_data[
                (self.sales_data['week'] >= promo['start_week']) &
                (self.sales_data['week'] <= promo['end_week'])
            ]['baseline'].sum()

            lift = (promo_sales - baseline) / baseline

            results.append({
                'promo_id': promo['promo_id'],
                'baseline': baseline,
                'promo_sales': promo_sales,
                'incremental': promo_sales - baseline,
                'lift_pct': lift * 100
            })

        return pd.DataFrame(results)

    def build_lift_model(self):
        """Build predictive model for promotional lift"""

        # Feature engineering
        features = self.promo_events[[
            'discount_pct', 'feature', 'display', 'price'
        ]]

        # Target
        lift_results = self.measure_lift()
        target = lift_results['lift_pct']

        # Train model
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(features, target)

        self.lift_model = model

        return model

    def forecast_promotion(self, promo_mechanics):
        """Forecast results for planned promotion"""

        if self.lift_model is None:
            self.build_lift_model()

        # Predict lift
        features = pd.DataFrame([promo_mechanics])
        predicted_lift = self.lift_model.predict(features)[0]

        # Apply to baseline
        baseline = self.calculate_baseline()
        forecast = baseline * (1 + predicted_lift / 100)

        return {
            'predicted_lift_pct': predicted_lift,
            'baseline_forecast': baseline,
            'promotional_forecast': forecast
        }
```

---

## Common Challenges & Solutions

### Challenge: Inaccurate Promotional Forecasts

**Problem:**
- Large variance in promotional performance
- Forecasts off by 50-100%
- Stock-outs or excess inventory

**Solutions:**
- Build promotional database (all past events)
- Segment by promotional mechanics (TPR, TPR+F, TPR+F+D)
- Use analogous products for new items
- Calibrate models with recent data
- Add safety stock for high-uncertainty events
- Implement demand sensing (update forecast based on early results)

```python
def adaptive_promotional_forecast(initial_forecast, actual_sales_to_date,
                                   days_into_promo, total_promo_days):
    """
    Update promotional forecast based on early performance
    """

    # Typical promotional curve (front-loaded)
    expected_pct_complete = {
        1: 0.30,  # Day 1: 30% of sales
        2: 0.50,  # Day 2: 50% cumulative
        3: 0.65,
        4: 0.75,
        5: 0.83,
        6: 0.90,
        7: 1.00
    }

    expected_complete = expected_pct_complete.get(days_into_promo, days_into_promo / total_promo_days)
    expected_sales = initial_forecast * expected_complete

    # Actual vs expected
    performance_ratio = actual_sales_to_date / expected_sales

    # Update forecast
    updated_forecast = initial_forecast * performance_ratio

    return {
        'initial_forecast': initial_forecast,
        'expected_to_date': expected_sales,
        'actual_to_date': actual_sales_to_date,
        'performance_ratio': performance_ratio,
        'updated_forecast': updated_forecast
    }
```

### Challenge: Low or Negative ROI Promotions

**Problem:**
- Many promotions lose money
- High trade spend, low incrementality
- Discounting loyal customers who would buy anyway

**Solutions:**
- Pre-test promotions (small markets, test stores)
- Optimize promotional depth (price testing)
- Target promotions (loyalty programs, coupons vs. TPR)
- Improve promotional execution (ensure displays in place)
- Eliminate chronic losers (cut bottom 20% of promotions)
- Focus on new customer acquisition vs. existing customers

### Challenge: Promotional Conflict and Cannibalization

**Problem:**
- Multiple products promoted same week
- Cannibalization within portfolio
- Retailer pushback on calendar

**Solutions:**
- Coordinate promotional calendar across portfolio
- Stagge promotions by product line
- Model cannibalization effects
- Optimize at portfolio level, not individual SKU
- Negotiate promotional calendar with retailer early

### Challenge: Supply Chain Execution

**Problem:**
- Stock-outs during promotion
- Promotional inventory arrives late
- DC capacity exceeded

**Solutions:**
- Extend lead times for promotional builds (6-8 weeks)
- Lock promotional forecasts 4 weeks before event
- Pre-position inventory (forward-stock to retailer DCs)
- Reserve production capacity for promotions
- Build promotional surge capacity into network
- Use secondary suppliers/co-packers for large events

### Challenge: Post-Promotion Dip (Pantry Loading)

**Problem:**
- Sales crash after promotion
- Consumers stockpiled
- Looks like promotion failed

**Solutions:**
- Measure true incrementality (include post-promo period)
- Limit promotion length (1-2 weeks max)
- Set purchase limits
- Don't promote too deeply
- Focus on trial/new customers, not pantry loading

---

## Output Format

### Promotional Plan Template

**Promotion Summary:**
- Product: Brand X Cereal 18oz
- Retailer: Major Grocery Chain
- Promotional Period: Week 15-16 (April 10-23)
- Mechanics: TPR + Feature + Display
- Regular Price: $4.99
- Promotional Price: $3.49 (30% off)

**Forecasted Performance:**

| Metric | Baseline | Promotional | Incremental | Lift % |
|--------|----------|-------------|-------------|--------|
| Units | 1,000 | 3,200 | 2,200 | 220% |
| Revenue | $4,990 | $11,168 | $6,178 | 124% |
| Gross Profit | $2,490 | $3,168 | $678 | 27% |

**Trade Spend:**

| Item | Cost |
|------|------|
| Off-Invoice Discount | $1,500 |
| Feature Allowance | $1,200 |
| Display Allowance | $800 |
| Co-op Advertising | $500 |
| **Total Trade Spend** | **$4,000** |

**ROI Analysis:**
- Incremental Gross Profit: $678
- Trade Spend: $4,000
- **Net Profit: -$3,322**
- **ROI: -83%**

**Recommendation: DO NOT PROCEED**
- Promotion expected to lose money
- Consider: Reduce trade spend, improve mechanics, or cancel

**Supply Chain Plan:**
- Production Build: Week 11 (4 weeks before promotion)
- Quantity: 3,500 units (forecast + 10% safety stock)
- Ship to Retailer DC: Week 13
- In-Store Setup: Week 14

---

## Questions to Ask

If you need more context:
1. What products/categories are being promoted?
2. What retailers and channels?
3. What promotional mechanics? (discount %, feature, display)
4. What's the promotional budget and objectives?
5. Historical promotional data available?
6. What's the typical promotional ROI and lift?
7. Production lead times and capacity constraints?
8. How far in advance is promotional calendar finalized?

---

## Related Skills

- **demand-forecasting**: For baseline and promotional demand forecasting
- **markdown-optimization**: For pricing and clearance optimization
- **retail-replenishment**: For coordinating promotional inventory
- **dsd-route-optimization**: For DSD promotional execution
- **capacity-planning**: For production capacity for promotions
- **inventory-optimization**: For promotional safety stock
- **sales-operations-planning**: For S&OP integration
- **supply-chain-analytics**: For promotional performance tracking
- **seasonal-planning**: For holiday and seasonal promotions
