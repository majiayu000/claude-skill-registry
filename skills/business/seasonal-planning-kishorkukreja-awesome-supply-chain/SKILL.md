---
name: seasonal-planning
description: When the user wants to optimize seasonal planning, manage seasonal buy decisions, or plan for seasonal demand. Also use when the user mentions "seasonal planning," "seasonal buy," "holiday planning," "back-to-school," "spring/fall collection," "seasonal inventory," "peak season," or "seasonal assortment." For demand forecasting, see demand-forecasting. For retail allocation, see retail-allocation.
---

# Seasonal Planning

You are an expert in retail seasonal planning and merchandise buying. Your goal is to help retailers plan seasonal assortments, optimize buy quantities, manage seasonal inventory, and execute successful seasonal transitions while balancing sales maximization with markdown risk.

## Initial Assessment

Before planning seasonal buys, understand:

1. **Business Context**
   - What retail category? (apparel, home, toys, etc.)
   - What season? (spring, summer, fall, holiday, back-to-school)
   - Season length? (weeks of selling season)
   - Historical seasonal performance? (sales, sell-through, markdowns)

2. **Financial Targets**
   - Season sales target? (revenue goal)
   - Target gross margin? (initial markup, markdown budget)
   - Inventory turn goals?
   - Open-to-buy budget?
   - Cash flow constraints?

3. **Product Mix**
   - Carry-over vs. new products? (% of each)
   - Core basics vs. fashion/trend items?
   - Price point distribution? (good/better/best)
   - SKU count target?
   - Vendor/supplier lead times?

4. **Historical Data Available**
   - Past season sales by week?
   - Sell-through rates by category/style?
   - Markdown rates and timing?
   - Stockout frequency?
   - Weather impacts?

---

## Seasonal Planning Framework

### Season Phases

**Pre-Season (Weeks -12 to 0)**
- Trend forecasting and market research
- Assortment planning (styles, colors, sizes)
- Buy planning and vendor negotiations
- Allocation planning
- Marketing campaign planning

**Early Season (Weeks 1-4)**
- Initial receipts and allocation
- Monitor early sell-through
- Identify fast/slow movers
- Adjust future orders (if possible)
- Replenishment decisions

**Peak Season (Weeks 5-8)**
- Peak sales volume
- Maintain in-stock on winners
- Begin markdown planning for slow movers
- Chase orders for hot items
- Maximize full-price selling

**Late Season (Weeks 9-12)**
- Aggressive markdowns to clear
- Minimize leftover inventory
- Transition space to next season
- Pack-away vs. liquidation decisions
- Post-season analysis

---

## Buy Planning & Optimization

### Seasonal Buy Quantity Optimization

```python
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy import stats

class SeasonalBuyOptimizer:
    """
    Optimize seasonal buy quantities

    Balance:
    - Under-buying: Lost sales (stockouts)
    - Over-buying: Markdowns and excess inventory
    """

    def __init__(self, season_config):
        """
        Parameters:
        - season_config: Season parameters (length, targets, costs)
        """
        self.season = season_config

    def calculate_optimal_buy(self, sku_forecast, unit_cost, retail_price,
                             markdown_rate=0.50, stockout_cost_multiplier=1.5):
        """
        Calculate optimal buy quantity using newsvendor model

        Classic single-period inventory problem
        """

        # Expected demand
        mean_demand = sku_forecast['mean']
        std_demand = sku_forecast['std']

        # Profit margins
        full_price_margin = retail_price - unit_cost
        markdown_price = retail_price * (1 - markdown_rate)
        markdown_margin = markdown_price - unit_cost

        # Cost of under-stocking (lost profit + goodwill)
        cost_understocking = full_price_margin * stockout_cost_multiplier

        # Cost of over-stocking (forced markdown or liquidation)
        cost_overstocking = unit_cost - markdown_price

        # Critical ratio (newsvendor)
        critical_ratio = cost_understocking / (cost_understocking + cost_overstocking)

        # Optimal order quantity (quantile of demand distribution)
        optimal_quantity = stats.norm.ppf(critical_ratio, mean_demand, std_demand)

        # Calculate expected profit at optimal quantity
        expected_sales = self._expected_sales(optimal_quantity, mean_demand, std_demand)
        expected_markdowns = max(0, optimal_quantity - expected_sales)

        expected_revenue = (expected_sales * retail_price +
                           expected_markdowns * markdown_price)
        expected_cost = optimal_quantity * unit_cost
        expected_profit = expected_revenue - expected_cost

        # Service level (fill rate)
        service_level = stats.norm.cdf(optimal_quantity, mean_demand, std_demand)

        return {
            'optimal_buy_quantity': round(optimal_quantity, 0),
            'expected_demand': mean_demand,
            'demand_std': std_demand,
            'expected_sales': round(expected_sales, 0),
            'expected_markdowns': round(expected_markdowns, 0),
            'expected_profit': round(expected_profit, 2),
            'service_level': round(service_level * 100, 1),
            'markdown_rate': markdown_rate * 100,
            'critical_ratio': round(critical_ratio, 3)
        }

    def _expected_sales(self, quantity, mean, std):
        """
        Calculate expected sales given quantity

        Accounts for potential stockouts
        """

        # E[Sales] = E[min(Demand, Quantity)]
        # Using normal distribution approximation

        if std == 0:
            return min(quantity, mean)

        z = (quantity - mean) / std
        expected_sales = mean * stats.norm.cdf(z) + std * stats.norm.pdf(z)

        return min(expected_sales, quantity)

    def optimize_assortment_mix(self, product_options, total_budget,
                                category_constraints=None):
        """
        Optimize product mix within budget

        Select which products to buy and in what quantities
        """

        n_products = len(product_options)

        # Objective: Maximize total expected profit
        def objective(quantities):
            total_profit = 0

            for i, qty in enumerate(quantities):
                product = product_options.iloc[i]

                # Calculate profit for this quantity
                result = self.calculate_optimal_buy(
                    sku_forecast={'mean': product['forecast_mean'],
                                 'std': product['forecast_std']},
                    unit_cost=product['unit_cost'],
                    retail_price=product['retail_price']
                )

                # Adjust for actual quantity vs. optimal
                if qty > 0:
                    # Approximate profit at this quantity
                    profit_at_qty = result['expected_profit'] * (qty / result['optimal_buy_quantity'])
                    total_profit += profit_at_qty

            return -total_profit  # Negative for minimization

        # Constraints
        def budget_constraint(quantities):
            total_cost = sum(
                quantities[i] * product_options.iloc[i]['unit_cost']
                for i in range(n_products)
            )
            return total_budget - total_cost

        constraints = [{'type': 'ineq', 'fun': budget_constraint}]

        # Bounds (non-negative quantities)
        bounds = [(0, product_options.iloc[i]['max_quantity']) for i in range(n_products)]

        # Initial guess (proportional to forecast)
        x0 = np.array([
            min(product_options.iloc[i]['forecast_mean'],
                product_options.iloc[i]['max_quantity'])
            for i in range(n_products)
        ]) * 0.8  # Start conservative

        # Optimize
        result = minimize(objective, x0, method='SLSQP',
                         bounds=bounds, constraints=constraints)

        optimal_quantities = result.x

        # Build result dataframe
        results = []
        for i, qty in enumerate(optimal_quantities):
            product = product_options.iloc[i]

            if qty > 5:  # Only include products with meaningful quantity
                buy_analysis = self.calculate_optimal_buy(
                    sku_forecast={'mean': product['forecast_mean'],
                                 'std': product['forecast_std']},
                    unit_cost=product['unit_cost'],
                    retail_price=product['retail_price']
                )

                results.append({
                    'sku': product['sku'],
                    'category': product['category'],
                    'buy_quantity': round(qty, 0),
                    'unit_cost': product['unit_cost'],
                    'retail_price': product['retail_price'],
                    'total_cost': round(qty * product['unit_cost'], 2),
                    'expected_profit': buy_analysis['expected_profit'],
                    'expected_markdown_rate': buy_analysis['markdown_rate']
                })

        results_df = pd.DataFrame(results)

        return results_df, result

    def calculate_open_to_buy(self, sales_plan, beginning_inventory,
                              on_order, target_end_inventory,
                              markdown_receipts=0):
        """
        Calculate open-to-buy (OTB) budget

        OTB = Sales Plan + Target End Inv - Beginning Inv - On Order + Markdowns
        """

        otb = (
            sales_plan +
            target_end_inventory -
            beginning_inventory -
            on_order +
            markdown_receipts
        )

        return {
            'sales_plan': sales_plan,
            'beginning_inventory': beginning_inventory,
            'on_order': on_order,
            'target_end_inventory': target_end_inventory,
            'markdown_receipts': markdown_receipts,
            'open_to_buy': otb,
            'otb_pct_of_sales': (otb / sales_plan * 100) if sales_plan > 0 else 0
        }

# Example usage
season_config = {
    'season_name': 'Fall 2024',
    'start_date': '2024-08-01',
    'end_date': '2024-11-30',
    'weeks': 16
}

optimizer = SeasonalBuyOptimizer(season_config)

# Single SKU optimization
sku_forecast = {'mean': 500, 'std': 150}
buy_decision = optimizer.calculate_optimal_buy(
    sku_forecast=sku_forecast,
    unit_cost=25,
    retail_price=60,
    markdown_rate=0.50
)

print("Optimal Buy Analysis:")
print(f"  Optimal quantity: {buy_decision['optimal_buy_quantity']}")
print(f"  Expected sales: {buy_decision['expected_sales']}")
print(f"  Expected markdowns: {buy_decision['expected_markdowns']}")
print(f"  Expected profit: ${buy_decision['expected_profit']:,.2f}")
print(f"  Service level: {buy_decision['service_level']:.1f}%")

# Assortment optimization
product_options = pd.DataFrame({
    'sku': [f'SKU{i:03d}' for i in range(1, 21)],
    'category': np.random.choice(['Tops', 'Bottoms', 'Dresses'], 20),
    'forecast_mean': np.random.uniform(200, 800, 20),
    'forecast_std': np.random.uniform(50, 200, 20),
    'unit_cost': np.random.uniform(15, 40, 20),
    'retail_price': np.random.uniform(40, 100, 20),
    'max_quantity': 1000
})

assortment, optimization_result = optimizer.optimize_assortment_mix(
    product_options,
    total_budget=150000
)

print(f"\nOptimized Assortment (Budget: $150K):")
print(f"Products selected: {len(assortment)}")
print(f"Total cost: ${assortment['total_cost'].sum():,.0f}")
print(f"Expected total profit: ${assortment['expected_profit'].sum():,.0f}")
```

---

## Seasonal Forecasting

### Seasonal Demand Modeling

```python
class SeasonalDemandForecaster:
    """
    Forecast seasonal demand patterns

    Accounts for:
    - Historical seasonal trends
    - Year-over-year growth
    - Fashion trends and newness
    - Weather impacts
    """

    def __init__(self, historical_data):
        """
        Parameters:
        - historical_data: Historical sales by week/season
          columns: ['season', 'year', 'week', 'sales', 'category']
        """
        self.history = historical_data

    def forecast_seasonal_curve(self, season, category):
        """
        Create seasonal sales curve

        Shows expected % of season sales by week
        """

        # Get historical data for this season
        season_history = self.history[
            (self.history['season'] == season) &
            (self.history['category'] == category)
        ]

        if len(season_history) == 0:
            # Use generic curve
            return self._generic_seasonal_curve()

        # Average sales by week across years
        weekly_avg = season_history.groupby('week')['sales'].mean()
        total_season_sales = weekly_avg.sum()

        # Calculate % distribution
        weekly_pct = (weekly_avg / total_season_sales * 100).to_dict()

        # Smooth the curve
        weeks = sorted(weekly_pct.keys())
        smoothed_pct = {}

        for week in weeks:
            # 3-week moving average
            nearby_weeks = [w for w in weeks if abs(w - week) <= 1]
            smoothed_pct[week] = np.mean([weekly_pct[w] for w in nearby_weeks])

        return smoothed_pct

    def _generic_seasonal_curve(self):
        """Generic seasonal curve (normal distribution)"""

        weeks = range(1, 17)  # 16-week season
        peak_week = 6  # Peak in week 6

        curve = {}
        total = 0

        for week in weeks:
            # Normal distribution centered at peak
            sales = np.exp(-((week - peak_week) ** 2) / 20)
            curve[week] = sales
            total += sales

        # Convert to percentages
        for week in weeks:
            curve[week] = curve[week] / total * 100

        return curve

    def forecast_total_season_sales(self, season, category, last_year_sales,
                                    growth_rate=0.05, trend_factor=1.0):
        """
        Forecast total season sales

        Based on:
        - Last year performance
        - Expected growth rate
        - Category trends
        """

        # Base forecast: last year + growth
        base_forecast = last_year_sales * (1 + growth_rate)

        # Adjust for trends
        adjusted_forecast = base_forecast * trend_factor

        return {
            'season': season,
            'category': category,
            'last_year_sales': last_year_sales,
            'growth_rate': growth_rate * 100,
            'trend_factor': trend_factor,
            'forecasted_sales': adjusted_forecast
        }

    def allocate_forecast_to_skus(self, total_forecast, sku_mix):
        """
        Allocate total forecast to individual SKUs

        Based on:
        - Historical performance (for carry-overs)
        - Analogous products (for new items)
        - Price point distribution
        """

        sku_forecasts = []

        for idx, sku in sku_mix.iterrows():
            if sku['is_new']:
                # New item: use analog performance
                forecast_pct = sku['analog_sales_pct']
            else:
                # Carry-over: use historical
                forecast_pct = sku['historical_sales_pct']

            # Adjust for price point appeal
            price_adjustment = sku.get('price_elasticity', 1.0)

            sku_forecast = total_forecast * (forecast_pct / 100) * price_adjustment

            # Add uncertainty (standard deviation)
            sku_std = sku_forecast * 0.30  # 30% coefficient of variation

            sku_forecasts.append({
                'sku': sku['sku'],
                'forecast_mean': sku_forecast,
                'forecast_std': sku_std,
                'is_new': sku['is_new'],
                'confidence': 'Low' if sku['is_new'] else 'High'
            })

        return pd.DataFrame(sku_forecasts)

    def simulate_season(self, initial_inventory, seasonal_curve,
                       total_forecast, n_simulations=1000):
        """
        Monte Carlo simulation of season performance

        Accounts for demand uncertainty
        """

        results = []

        for sim in range(n_simulations):
            # Simulate demand with uncertainty
            weekly_demand_pct = seasonal_curve.copy()

            # Add random variation
            for week in weekly_demand_pct.keys():
                noise = np.random.normal(1.0, 0.15)  # 15% noise
                weekly_demand_pct[week] *= noise

            # Normalize back to 100%
            total_pct = sum(weekly_demand_pct.values())
            weekly_demand_pct = {k: v/total_pct*100 for k, v in weekly_demand_pct.items()}

            # Simulate season
            inventory = initial_inventory
            total_sales = 0
            total_stockouts = 0

            for week, pct in sorted(weekly_demand_pct.items()):
                weekly_demand = total_forecast * (pct / 100)

                # Sales limited by inventory
                weekly_sales = min(weekly_demand, inventory)
                stockout = max(0, weekly_demand - inventory)

                inventory -= weekly_sales
                total_sales += weekly_sales
                total_stockouts += stockout

            # Calculate metrics
            sell_through_rate = (total_sales / initial_inventory * 100) if initial_inventory > 0 else 0
            stockout_rate = (total_stockouts / total_forecast * 100) if total_forecast > 0 else 0
            leftover_inventory = inventory

            results.append({
                'simulation': sim,
                'total_sales': total_sales,
                'sell_through_rate': sell_through_rate,
                'stockout_rate': stockout_rate,
                'leftover_inventory': leftover_inventory
            })

        results_df = pd.DataFrame(results)

        # Summary statistics
        summary = {
            'mean_sell_through': results_df['sell_through_rate'].mean(),
            'p10_sell_through': results_df['sell_through_rate'].quantile(0.10),
            'p50_sell_through': results_df['sell_through_rate'].quantile(0.50),
            'p90_sell_through': results_df['sell_through_rate'].quantile(0.90),
            'mean_stockout_rate': results_df['stockout_rate'].mean(),
            'mean_leftover': results_df['leftover_inventory'].mean()
        }

        return results_df, summary

# Example
historical_data = pd.DataFrame({
    'season': ['Fall'] * 48,
    'year': [2021, 2021, 2022, 2022, 2023, 2023] * 8,
    'week': sorted(list(range(1, 9)) * 6),
    'sales': np.random.uniform(5000, 15000, 48),
    'category': 'Sweaters'
})

forecaster = SeasonalDemandForecaster(historical_data)

# Get seasonal curve
curve = forecaster.forecast_seasonal_curve('Fall', 'Sweaters')
print("Seasonal Curve (% of total sales by week):")
for week, pct in sorted(curve.items())[:8]:
    print(f"  Week {week}: {pct:.1f}%")

# Forecast total season
season_forecast = forecaster.forecast_total_season_sales(
    season='Fall',
    category='Sweaters',
    last_year_sales=500000,
    growth_rate=0.08,
    trend_factor=1.1
)
print(f"\nForecast total season sales: ${season_forecast['forecasted_sales']:,.0f}")

# Simulate season
simulation_results, summary = forecaster.simulate_season(
    initial_inventory=5000,
    seasonal_curve=curve,
    total_forecast=season_forecast['forecasted_sales'] / 50,  # Per SKU
    n_simulations=1000
)

print(f"\nSeason Simulation Results:")
print(f"  Mean sell-through: {summary['mean_sell_through']:.1f}%")
print(f"  P10/P50/P90 sell-through: {summary['p10_sell_through']:.1f}% / {summary['p50_sell_through']:.1f}% / {summary['p90_sell_through']:.1f}%")
print(f"  Mean stockout rate: {summary['mean_stockout_rate']:.1f}%")
```

---

## In-Season Management

### Chase & Markdown Strategy

```python
class InSeasonManager:
    """
    Manage in-season performance

    React to actual performance vs. plan
    """

    def __init__(self, season_plan):
        self.plan = season_plan

    def identify_chase_opportunities(self, actual_sales, weeks_elapsed,
                                    current_inventory):
        """
        Identify products to chase (reorder)

        Chase when:
        - Selling faster than planned
        - Current inventory insufficient for season
        - Vendor lead time allows
        """

        opportunities = []

        for sku, sales in actual_sales.items():
            plan_sales = self.plan.get(sku, {}).get('total_plan', 0)
            weeks_remaining = self.plan['season_weeks'] - weeks_elapsed

            if weeks_elapsed == 0:
                continue

            # Calculate sell-through rate
            weekly_rate = sales / weeks_elapsed
            projected_total_sales = weekly_rate * self.plan['season_weeks']

            # Compare to plan
            vs_plan_pct = (projected_total_sales / plan_sales - 1) * 100 if plan_sales > 0 else 0

            # Check inventory sufficiency
            inventory_remaining = current_inventory.get(sku, 0)
            projected_remaining_sales = weekly_rate * weeks_remaining

            if vs_plan_pct > 20 and inventory_remaining < projected_remaining_sales:
                # Chase opportunity
                chase_qty = projected_remaining_sales - inventory_remaining

                # Check if lead time allows
                vendor_lead_time = self.plan.get(sku, {}).get('lead_time_weeks', 8)

                if weeks_remaining > vendor_lead_time + 2:  # Buffer
                    opportunities.append({
                        'sku': sku,
                        'vs_plan': vs_plan_pct,
                        'projected_total_sales': projected_total_sales,
                        'inventory_remaining': inventory_remaining,
                        'recommended_chase_qty': round(chase_qty, 0),
                        'urgency': 'High' if weeks_remaining < vendor_lead_time + 4 else 'Medium'
                    })

        return pd.DataFrame(opportunities)

    def identify_markdown_candidates(self, actual_sales, weeks_elapsed,
                                    current_inventory, target_str=0.75):
        """
        Identify products needing markdown

        Markdown when:
        - Selling slower than planned
        - Risk of excess inventory at season end
        """

        candidates = []

        weeks_remaining = self.plan['season_weeks'] - weeks_elapsed

        for sku, sales in actual_sales.items():
            initial_buy = self.plan.get(sku, {}).get('buy_quantity', 0)
            inventory_remaining = current_inventory.get(sku, 0)

            if initial_buy == 0:
                continue

            # Current sell-through rate
            current_str = (initial_buy - inventory_remaining) / initial_buy

            # Projected final sell-through
            if weeks_elapsed > 0:
                weekly_rate = sales / weeks_elapsed
                projected_additional_sales = weekly_rate * weeks_remaining
                projected_final_str = (sales + projected_additional_sales) / initial_buy
            else:
                projected_final_str = 0

            # If projected STR < target, need markdown
            if projected_final_str < target_str and inventory_remaining > 0:
                # Recommend markdown depth based on urgency
                if projected_final_str < 0.50:
                    recommended_markdown = 40
                elif projected_final_str < 0.60:
                    recommended_markdown = 30
                else:
                    recommended_markdown = 20

                candidates.append({
                    'sku': sku,
                    'current_str': round(current_str * 100, 1),
                    'projected_str': round(projected_final_str * 100, 1),
                    'inventory_remaining': inventory_remaining,
                    'recommended_markdown': recommended_markdown,
                    'urgency': 'High' if projected_final_str < 0.50 else 'Medium'
                })

        return pd.DataFrame(candidates)

    def calculate_season_health_score(self, actual_sales, weeks_elapsed,
                                     current_inventory):
        """
        Calculate overall season health score (0-100)

        Factors:
        - Sales vs. plan
        - Sell-through rate
        - Markdown rate
        - Inventory balance
        """

        total_plan_sales = sum(sku.get('total_plan', 0) for sku in self.plan.values() if isinstance(sku, dict))
        total_actual_sales = sum(actual_sales.values())

        # Sales attainment
        if total_plan_sales > 0:
            sales_attainment = total_actual_sales / (total_plan_sales * weeks_elapsed / self.plan['season_weeks'])
        else:
            sales_attainment = 0

        sales_score = min(sales_attainment * 50, 50)  # Max 50 points

        # Sell-through rate
        total_initial_buy = sum(sku.get('buy_quantity', 0) for sku in self.plan.values() if isinstance(sku, dict))
        total_current_inv = sum(current_inventory.values())

        if total_initial_buy > 0:
            current_str = (total_initial_buy - total_current_inv) / total_initial_buy
        else:
            current_str = 0

        # Target STR at this point in season
        target_str_now = weeks_elapsed / self.plan['season_weeks'] * 0.80  # 80% by end

        str_score = min(current_str / target_str_now * 30, 30) if target_str_now > 0 else 0

        # Inventory balance (not too much, not too little)
        weeks_remaining = self.plan['season_weeks'] - weeks_elapsed
        weekly_run_rate = total_actual_sales / weeks_elapsed if weeks_elapsed > 0 else 0
        weeks_of_supply = total_current_inv / weekly_run_rate if weekly_run_rate > 0 else 999

        if 0.8 * weeks_remaining <= weeks_of_supply <= 1.2 * weeks_remaining:
            balance_score = 20  # Perfect balance
        else:
            balance_score = max(0, 20 - abs(weeks_of_supply - weeks_remaining) * 2)

        total_score = sales_score + str_score + balance_score

        return {
            'health_score': round(total_score, 1),
            'sales_attainment': round(sales_attainment * 100, 1),
            'sell_through_rate': round(current_str * 100, 1),
            'weeks_of_supply': round(weeks_of_supply, 1),
            'interpretation': self._interpret_health_score(total_score)
        }

    def _interpret_health_score(self, score):
        """Interpret health score"""
        if score >= 80:
            return 'Excellent - on track for strong season'
        elif score >= 65:
            return 'Good - minor adjustments needed'
        elif score >= 50:
            return 'Fair - action required'
        else:
            return 'Poor - aggressive intervention needed'

# Example
season_plan = {
    'season_weeks': 16,
    'SKU001': {'total_plan': 10000, 'buy_quantity': 8000, 'lead_time_weeks': 6},
    'SKU002': {'total_plan': 15000, 'buy_quantity': 12000, 'lead_time_weeks': 8},
    'SKU003': {'total_plan': 5000, 'buy_quantity': 5000, 'lead_time_weeks': 6}
}

manager = InSeasonManager(season_plan)

# Week 6 performance
actual_sales = {'SKU001': 4500, 'SKU002': 4000, 'SKU003': 1200}
current_inventory = {'SKU001': 2500, 'SKU002': 7000, 'SKU003': 3500}
weeks_elapsed = 6

# Identify chase opportunities
chase_opps = manager.identify_chase_opportunities(
    actual_sales, weeks_elapsed, current_inventory
)
print("Chase Opportunities:")
print(chase_opps)

# Identify markdown candidates
markdown_candidates = manager.identify_markdown_candidates(
    actual_sales, weeks_elapsed, current_inventory, target_str=0.75
)
print("\nMarkdown Candidates:")
print(markdown_candidates)

# Season health score
health = manager.calculate_season_health_score(
    actual_sales, weeks_elapsed, current_inventory
)
print(f"\nSeason Health Score: {health['health_score']:.1f}/100")
print(f"Interpretation: {health['interpretation']}")
print(f"Sales attainment: {health['sales_attainment']:.1f}%")
print(f"Sell-through rate: {health['sell_through_rate']:.1f}%")
```

---

## Tools & Libraries

### Python Libraries

**Optimization:**
- `scipy.optimize`: Newsvendor optimization
- `pulp`, `pyomo`: Linear programming for assortment
- `numpy`: Numerical computations

**Forecasting:**
- `statsmodels`: Time series analysis
- `prophet`: Seasonal forecasting
- `pandas`: Data manipulation

**Simulation:**
- `numpy.random`: Monte Carlo simulation
- `scipy.stats`: Statistical distributions

### Commercial Software

**Planning Systems:**
- **Blue Yonder (JDA) Assortment**: Seasonal planning and optimization
- **o9 Solutions**: Digital planning platform
- **Oracle Retail Merchandise Planning**: Seasonal merchandise planning
- **SAP IBP**: Integrated business planning
- **RELEX Solutions**: Seasonal demand planning

**Specialized Tools:**
- **Armonia**: Retail planning suite
- **TXT Retail**: Fashion planning
- **APTOS Merchandise Lifecycle Management**: Seasonal planning

---

## Common Challenges & Solutions

### Challenge: Forecasting New Products

**Problem:**
- No historical data
- High uncertainty
- Risk of over/under buying

**Solutions:**
- Analog product approach
- Test markets / pilot stores
- Start conservative, chase winners
- Use product attributes (price, color, style)
- Market research and trend analysis
- Multiple scenarios (optimistic/realistic/conservative)

### Challenge: Weather Dependency

**Problem:**
- Unseasonable weather impacts sales
- Hard to predict
- Risk management

**Solutions:**
- Weather-based contingency plans
- Flexible vendor agreements
- Geographic diversification
- Pack-away programs (hold for next year)
- Transfer between climates
- Quick markdown response

### Challenge: Late Vendor Deliveries

**Problem:**
- Receipts arrive late
- Miss selling window
- Forced markdowns

**Solutions:**
- Air freight contingencies
- Vendor scorecards and penalties
- Multiple sourcing
- Buffer lead times in planning
- Early production starts
- Substitute product strategies

### Challenge: Balancing Newness vs. Basics

**Problem:**
- Fashion/trend items riskier
- Basics boring but reliable
- Need both for assortment

**Solutions:**
- 70/30 or 60/40 ratio (basics/fashion)
- Test fashion in limited quantities
- Fast fashion model (short lead times)
- Core basics with fashion colors
- Clear newness every season
- Price segmentation (basics lower, fashion higher)

### Challenge: End-of-Season Clearance

**Problem:**
- Leftover inventory
- Deep markdowns hurt margins
- Storage costs

**Solutions:**
- Aggressive early markdowns
- Pack-away for next year (if feasible)
- Outlet store distribution
- Liquidation companies
- Donation (tax benefit)
- Improved planning to reduce leftovers

---

## Output Format

### Seasonal Planning Report

**Executive Summary:**
- Season: Fall 2024 (August - November)
- Total buy plan: $4.2M at cost ($10.5M retail)
- Target sales: $9.2M (88% sell-through at full price)
- Target margin: 62% IMU, 58% maintained margin
- SKU count: 425 SKUs across 8 categories

**Financial Plan:**

| Metric | Target |
|--------|--------|
| Total buy at cost | $4.2M |
| Total buy at retail | $10.5M |
| Initial markup (IMU) | 62% |
| Sales plan | $9.2M |
| Sell-through target | 88% |
| Markdown budget | 4% of sales ($368K) |
| Maintained margin | 58% |
| Gross profit | $5.3M |

**Category Mix:**

| Category | Buy $ | Buy % | SKU Count | Avg Price | Strategy |
|----------|-------|-------|-----------|-----------|----------|
| Outerwear | $1.2M | 29% | 65 | $125 | Core + fashion, focus on trend colors |
| Sweaters | $980K | 23% | 95 | $68 | Basics with fashion accents |
| Dresses | $750K | 18% | 80 | $95 | Fashion-forward, limited quantities |
| Tops | $620K | 15% | 110 | $45 | High volume, core basics |
| Bottoms | $480K | 11% | 55 | $78 | Denim focus, seasonal colors |
| Accessories | $170K | 4% | 20 | $35 | Impulse items, high margin |

**New vs. Carry-Over:**

| Type | Buy $ | Buy % | Risk Level | Strategy |
|------|-------|-------|------------|----------|
| Carry-over (proven) | $2.5M | 60% | Low | Core basics, repeat winners |
| New items | $1.7M | 40% | High | Fashion, test quantities |

**Weekly Receipt Flow:**

| Week | Receipt $ | Cum % | Focus |
|------|-----------|-------|-------|
| Week -2 | $420K | 10% | Core basics early |
| Week 0 | $840K | 30% | Launch assortment |
| Week 2 | $630K | 45% | Fill-in and fashion |
| Week 4 | $420K | 55% | Fresh arrivals |
| Week 6-8 | $890K | 76% | Peak season support |
| Week 10+ | $1M | 100% | Late season, limited items |

**Risk Assessment:**

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Warm weather (delayed season start) | Medium | High | Conservative initial buy, chase plans ready |
| New product performance | High | Medium | Test quantities, monitor week 1 closely |
| Vendor delays | Low | High | Air freight budget, alternate suppliers |
| Competitive pricing | Medium | Medium | Markdown budget, price match capability |

**Success Metrics:**

| Metric | Target | Week 4 Check | Week 8 Check | Season End |
|--------|--------|--------------|--------------|------------|
| Sales vs. plan | 100% | ≥90% | ≥95% | ≥97% |
| Sell-through rate | 88% | ≥30% | ≥60% | ≥85% |
| Markdown rate | <4% | 0% | <2% | <5% |
| Gross margin | 58% | 62% | 60% | ≥57% |

**Action Plan:**

| Week | Action | Owner |
|------|--------|-------|
| Week -4 | Final assortment review, POs placed | Buyer |
| Week -2 | First receipts, allocation to stores | Allocator |
| Week 0 | Season launch, marketing campaign | Marketing |
| Week 1 | Monitor early reads, identify trends | Planner |
| Week 4 | Chase order decisions for winners | Buyer |
| Week 8 | First markdown evaluation | Planner |
| Week 12 | Aggressive clearance markdowns | Buyer |

---

## Questions to Ask

If you need more context:
1. What season are you planning? (spring, fall, holiday, etc.)
2. What's the season length? (weeks of selling)
3. What was last year's performance? (sales, sell-through, markdowns)
4. What's your sales target for this season?
5. What's your open-to-buy budget?
6. What % is new vs. carry-over merchandise?
7. What are your vendor lead times?
8. What's your target markdown rate?
9. What categories/product types are included?

---

## Related Skills

- **demand-forecasting**: Demand forecasting methodologies
- **retail-allocation**: Store allocation optimization
- **markdown-optimization**: Markdown strategy and timing
- **inventory-optimization**: Safety stock and inventory management
- **retail-replenishment**: In-season replenishment
- **planogram-optimization**: Space planning for seasonal sets
- **supply-chain-analytics**: Performance metrics and tracking
