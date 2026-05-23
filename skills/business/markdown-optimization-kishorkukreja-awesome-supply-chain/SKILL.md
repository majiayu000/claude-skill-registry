---
name: markdown-optimization
description: When the user wants to optimize markdown strategy, price optimization for clearance, or minimize inventory markdowns. Also use when the user mentions "markdown," "clearance pricing," "price elasticity," "promotional pricing," "discount optimization," "sell-through," "inventory liquidation," or "dynamic pricing." For initial allocation, see retail-allocation. For promotional planning, see promotional-planning.
---

# Markdown Optimization

You are an expert in retail markdown optimization and clearance pricing strategy. Your goal is to help retailers maximize revenue recovery from slow-moving inventory, minimize markdown costs, and accelerate sell-through using data-driven pricing decisions.

## Initial Assessment

Before optimizing markdowns, understand:

1. **Inventory Situation**
   - What inventory needs markdown? (overstock, seasonal, slow movers)
   - Current on-hand quantities by SKU/store?
   - Age of inventory? (weeks on hand)
   - Original cost and retail price?
   - Historical sell-through rates?

2. **Business Context**
   - What's the current markdown rate? (% of sales)
   - Target markdown rate?
   - Margin constraints? (minimum acceptable margin)
   - Seasonality? (end of season pressure)
   - Competitive pricing environment?

3. **Pricing Flexibility**
   - Who controls pricing? (centralized, regional, store)
   - Markdown frequency? (weekly, monthly, continuous)
   - Markdown increment rules? (10%, 20%, 30% steps)
   - Minimum/maximum discount limits?
   - Can prices be personalized? (dynamic, loyalty-based)

4. **Channels & Competition**
   - Single channel or omnichannel?
   - Online pricing flexibility?
   - Competitor pricing tracked?
   - Outlet stores for clearance?
   - Liquidation options? (jobbers, donations)

---

## Markdown Optimization Framework

### Markdown Strategy Fundamentals

**Key Objectives:**
1. **Maximize revenue recovery**: Get highest possible price before going to clearance
2. **Accelerate sell-through**: Clear inventory before it becomes obsolete
3. **Minimize markdown dollars**: Reduce total markdown spend
4. **Preserve brand perception**: Avoid excessive discounting
5. **Optimize timing**: Balance early vs. late markdowns

**Markdown Lifecycle:**

```
Full Price → First Markdown (10-25%) → Second Markdown (30-50%) →
Final Clearance (50-75%) → Liquidation/Donation
```

**Decision Framework:**
- **When to markdown?** Monitor sell-through rate, weeks of supply
- **How much to markdown?** Based on price elasticity, urgency
- **Which SKUs to markdown?** Prioritize by age, quantity, margin
- **Which stores to markdown?** Store-specific or chain-wide

---

## Price Elasticity & Demand Modeling

### Price-Demand Relationship

```python
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

class PriceElasticityAnalyzer:
    """
    Analyze price elasticity of demand for markdown optimization

    Measure how demand changes with price reductions
    """

    def __init__(self, historical_pricing_data):
        """
        Parameters:
        - historical_pricing_data: DataFrame with historical price/sales
          columns: ['sku', 'date', 'price', 'units_sold', 'original_price']
        """
        self.data = historical_pricing_data

    def calculate_price_elasticity(self, sku):
        """
        Calculate price elasticity of demand

        Elasticity = % change in quantity / % change in price

        E > 1: Elastic (demand very sensitive to price)
        E = 1: Unit elastic
        E < 1: Inelastic (demand not very sensitive)
        """

        sku_data = self.data[self.data['sku'] == sku].copy()

        if len(sku_data) < 10:
            return {'error': 'Insufficient data', 'elasticity': None}

        # Calculate discount percentage
        sku_data['discount_pct'] = (
            (sku_data['original_price'] - sku_data['price']) /
            sku_data['original_price'] * 100
        )

        # Log transformation for elasticity calculation
        sku_data['log_price'] = np.log(sku_data['price'])
        sku_data['log_quantity'] = np.log(sku_data['units_sold'] + 1)

        # Linear regression: log(Q) = a + b * log(P)
        # b is the price elasticity
        X = sku_data[['log_price']].values
        y = sku_data['log_quantity'].values

        model = LinearRegression()
        model.fit(X, y)

        elasticity = model.coef_[0]
        r_squared = model.score(X, y)

        return {
            'sku': sku,
            'elasticity': abs(elasticity),  # Report as positive
            'r_squared': r_squared,
            'interpretation': self._interpret_elasticity(abs(elasticity)),
            'model': model
        }

    def _interpret_elasticity(self, elasticity):
        """Interpret elasticity value"""

        if elasticity > 2:
            return 'Highly elastic - very price sensitive'
        elif elasticity > 1:
            return 'Elastic - price sensitive'
        elif elasticity > 0.5:
            return 'Moderately elastic'
        else:
            return 'Inelastic - not very price sensitive'

    def estimate_demand_at_price(self, sku, target_price):
        """
        Estimate demand at a specific price point

        Uses fitted elasticity model
        """

        elasticity_result = self.calculate_price_elasticity(sku)

        if elasticity_result.get('error'):
            return None

        model = elasticity_result['model']
        log_price = np.log(target_price)

        log_quantity_pred = model.predict([[log_price]])[0]
        estimated_quantity = np.exp(log_quantity_pred) - 1

        return max(0, estimated_quantity)

    def find_optimal_markdown(self, sku, cost, current_price, current_inventory,
                             weeks_remaining=8):
        """
        Find optimal markdown to maximize revenue recovery

        Balances:
        - Higher prices = higher margin but slower sell-through
        - Lower prices = faster sell-through but lower margin
        """

        elasticity_result = self.calculate_price_elasticity(sku)

        if elasticity_result.get('error'):
            return {'error': 'Cannot optimize without elasticity data'}

        # Test different price points
        price_range = np.linspace(cost * 1.1, current_price, 20)  # Don't go below cost
        results = []

        for test_price in price_range:
            # Estimate weekly demand at this price
            estimated_weekly_demand = self.estimate_demand_at_price(sku, test_price)

            # Estimate total units sold over remaining weeks
            estimated_total_sold = min(
                estimated_weekly_demand * weeks_remaining,
                current_inventory
            )

            # Calculate revenue
            revenue = estimated_total_sold * test_price

            # Calculate margin
            margin = test_price - cost
            margin_pct = margin / test_price * 100 if test_price > 0 else 0

            # Calculate weeks to sell out
            if estimated_weekly_demand > 0:
                weeks_to_sellout = current_inventory / estimated_weekly_demand
            else:
                weeks_to_sellout = 999

            results.append({
                'price': test_price,
                'discount_pct': (current_price - test_price) / current_price * 100,
                'estimated_weekly_demand': estimated_weekly_demand,
                'estimated_total_sold': estimated_total_sold,
                'revenue': revenue,
                'margin_pct': margin_pct,
                'weeks_to_sellout': weeks_to_sellout
            })

        results_df = pd.DataFrame(results)

        # Find optimal price (maximize revenue)
        optimal_idx = results_df['revenue'].idxmax()
        optimal = results_df.iloc[optimal_idx]

        return {
            'current_price': current_price,
            'optimal_price': optimal['price'],
            'recommended_discount': optimal['discount_pct'],
            'expected_revenue': optimal['revenue'],
            'expected_sellthrough': optimal['estimated_total_sold'] / current_inventory * 100,
            'weeks_to_sellout': optimal['weeks_to_sellout'],
            'all_scenarios': results_df
        }

# Example usage
np.random.seed(42)

# Generate sample historical data
dates = pd.date_range('2024-01-01', periods=50, freq='W')
historical_data = []

for week in range(50):
    # Simulate price elasticity: lower prices → higher sales
    base_price = 100
    discount = min(week * 2, 60)  # Increasing discounts over time
    price = base_price * (1 - discount/100)

    # Demand increases as price decreases (elasticity ~1.5)
    base_demand = 20
    price_factor = (base_price / price) ** 1.5
    units_sold = base_demand * price_factor + np.random.normal(0, 5)
    units_sold = max(0, units_sold)

    historical_data.append({
        'sku': 'SKU123',
        'date': dates[week],
        'price': price,
        'units_sold': units_sold,
        'original_price': base_price
    })

historical_df = pd.DataFrame(historical_data)

# Analyze elasticity
analyzer = PriceElasticityAnalyzer(historical_df)
elasticity = analyzer.calculate_price_elasticity('SKU123')

print(f"Price Elasticity: {elasticity['elasticity']:.2f}")
print(f"Interpretation: {elasticity['interpretation']}")
print(f"R-squared: {elasticity['r_squared']:.2f}")

# Find optimal markdown
optimization = analyzer.find_optimal_markdown(
    sku='SKU123',
    cost=40,
    current_price=80,
    current_inventory=500,
    weeks_remaining=6
)

print(f"\nCurrent price: ${optimization['current_price']:.2f}")
print(f"Optimal price: ${optimization['optimal_price']:.2f}")
print(f"Recommended discount: {optimization['recommended_discount']:.1f}%")
print(f"Expected revenue: ${optimization['expected_revenue']:,.0f}")
print(f"Expected sell-through: {optimization['expected_sellthrough']:.1f}%")
```

---

## Markdown Timing Optimization

### Dynamic Markdown Scheduling

```python
class MarkdownScheduler:
    """
    Optimize markdown timing to maximize revenue recovery

    Decides when to markdown based on:
    - Current sell-through rate
    - Time remaining in season
    - Inventory level
    - Competitive pressure
    """

    def __init__(self, season_end_date, current_date):
        self.season_end = pd.to_datetime(season_end_date)
        self.current_date = pd.to_datetime(current_date)
        self.weeks_remaining = (self.season_end - self.current_date).days / 7

    def calculate_sell_through_rate(self, units_sold, initial_inventory, weeks_elapsed):
        """
        Calculate sell-through rate (STR)

        STR = units sold / initial inventory
        Weekly STR = STR / weeks
        """

        if initial_inventory == 0:
            return 0

        str_total = units_sold / initial_inventory * 100
        str_weekly = str_total / weeks_elapsed if weeks_elapsed > 0 else 0

        return {
            'total_str': str_total,
            'weekly_str': str_weekly,
            'units_sold': units_sold,
            'initial_inventory': initial_inventory
        }

    def should_markdown(self, sku_data):
        """
        Decide if SKU should be marked down now

        Factors:
        - Sell-through rate below target
        - Weeks of supply too high
        - End of season approaching
        """

        current_inventory = sku_data['current_inventory']
        weekly_sales_rate = sku_data['weekly_sales_rate']
        target_str = sku_data.get('target_str', 70)  # Target 70% sell-through

        # Calculate current trajectory
        projected_str = (weekly_sales_rate * self.weeks_remaining) / sku_data['initial_inventory'] * 100

        # Calculate weeks of supply
        if weekly_sales_rate > 0:
            weeks_of_supply = current_inventory / weekly_sales_rate
        else:
            weeks_of_supply = 999

        # Decision rules
        reasons = []
        should_md = False

        # Rule 1: Projected sell-through below target
        if projected_str < target_str:
            should_md = True
            reasons.append(f"Projected STR ({projected_str:.1f}%) below target ({target_str}%)")

        # Rule 2: Excessive weeks of supply
        if weeks_of_supply > self.weeks_remaining * 1.5:
            should_md = True
            reasons.append(f"Weeks of supply ({weeks_of_supply:.1f}) exceeds season ({self.weeks_remaining:.1f})")

        # Rule 3: End of season urgency
        if self.weeks_remaining < 4 and projected_str < 80:
            should_md = True
            reasons.append(f"Season ending soon ({self.weeks_remaining:.1f} weeks) with low STR")

        # Rule 4: No sales momentum
        if weekly_sales_rate < sku_data['initial_inventory'] * 0.01:  # <1% per week
            should_md = True
            reasons.append("Very slow sales rate")

        return {
            'should_markdown': should_md,
            'reasons': reasons,
            'projected_str': projected_str,
            'weeks_of_supply': weeks_of_supply,
            'weeks_remaining': self.weeks_remaining,
            'urgency': 'High' if self.weeks_remaining < 4 else 'Medium' if self.weeks_remaining < 8 else 'Low'
        }

    def recommend_markdown_depth(self, sku_data):
        """
        Recommend markdown percentage

        Deeper discounts for:
        - Lower sell-through
        - More weeks of supply
        - End of season
        - Low price elasticity (need big discount to move)
        """

        decision = self.should_markdown(sku_data)

        if not decision['should_markdown']:
            return {
                'recommended_markdown': 0,
                'reason': 'On track, no markdown needed'
            }

        weeks_of_supply = decision['weeks_of_supply']
        projected_str = decision['projected_str']
        elasticity = sku_data.get('price_elasticity', 1.0)

        # Base markdown on severity
        if projected_str < 40 or weeks_of_supply > 20:
            base_markdown = 50  # Aggressive
        elif projected_str < 55 or weeks_of_supply > 15:
            base_markdown = 30  # Moderate
        else:
            base_markdown = 20  # Conservative

        # Adjust for elasticity
        if elasticity < 0.8:  # Inelastic
            base_markdown *= 1.3  # Need bigger discount
        elif elasticity > 1.5:  # Elastic
            base_markdown *= 0.8  # Smaller discount works

        # Adjust for urgency
        if self.weeks_remaining < 3:
            base_markdown *= 1.4

        # Round to standard increments
        markdown_increments = [10, 20, 25, 30, 40, 50, 60, 70]
        recommended_markdown = min(markdown_increments, key=lambda x: abs(x - base_markdown))

        return {
            'recommended_markdown': recommended_markdown,
            'reason': f"Projected STR {projected_str:.1f}%, {weeks_of_supply:.1f} weeks supply",
            'urgency': decision['urgency']
        }

    def create_markdown_cadence(self, sku_data, markdown_stages=[20, 40, 60]):
        """
        Create multi-stage markdown plan

        Progressive markdowns over time
        """

        weeks_left = self.weeks_remaining
        cadence = []

        # Determine if we need aggressive or conservative cadence
        decision = self.should_markdown(sku_data)

        if decision['urgency'] == 'High':
            # Fast cadence - markdown every 1-2 weeks
            week_intervals = [0, 1, 3]
        elif decision['urgency'] == 'Medium':
            # Moderate cadence - markdown every 2-3 weeks
            week_intervals = [0, 2, 5]
        else:
            # Slow cadence - markdown every 3-4 weeks
            week_intervals = [0, 3, 7]

        for i, (markdown_pct, week_offset) in enumerate(zip(markdown_stages, week_intervals)):
            if week_offset < weeks_left:
                markdown_date = self.current_date + pd.Timedelta(weeks=week_offset)

                cadence.append({
                    'stage': i + 1,
                    'markdown_date': markdown_date,
                    'markdown_pct': markdown_pct,
                    'price': sku_data['original_price'] * (1 - markdown_pct/100),
                    'weeks_from_now': week_offset
                })

        return cadence

# Example
scheduler = MarkdownScheduler(
    season_end_date='2024-09-30',
    current_date='2024-08-15'
)

sku_data = {
    'sku': 'SKU456',
    'initial_inventory': 1000,
    'current_inventory': 720,
    'weekly_sales_rate': 25,
    'original_price': 89.99,
    'target_str': 75,
    'price_elasticity': 1.3
}

# Should we markdown?
decision = scheduler.should_markdown(sku_data)
print(f"Should markdown: {decision['should_markdown']}")
print(f"Reasons: {decision['reasons']}")
print(f"Projected STR: {decision['projected_str']:.1f}%")
print(f"Urgency: {decision['urgency']}")

# Recommend markdown depth
recommendation = scheduler.recommend_markdown_depth(sku_data)
print(f"\nRecommended markdown: {recommendation['recommended_markdown']}%")
print(f"Reason: {recommendation['reason']}")

# Create markdown cadence
cadence = scheduler.create_markdown_cadence(sku_data)
print(f"\nMarkdown Cadence:")
for stage in cadence:
    print(f"  Stage {stage['stage']}: {stage['markdown_pct']}% off on {stage['markdown_date'].date()} (${stage['price']:.2f})")
```

---

## Markdown Optimization Models

### Multi-SKU Markdown Optimization

```python
from scipy.optimize import minimize, LinearConstraint

class MarkdownOptimizer:
    """
    Optimize markdowns across multiple SKUs

    Maximize total revenue while meeting clearance targets
    """

    def __init__(self, skus_data, constraints):
        """
        Parameters:
        - skus_data: DataFrame with SKU information
          columns: ['sku', 'inventory', 'cost', 'current_price', 'elasticity',
                   'weekly_demand_base']
        - constraints: Dict with budget/target constraints
        """
        self.skus = skus_data
        self.constraints = constraints

    def estimate_demand_at_discount(self, base_demand, elasticity, discount_pct):
        """
        Estimate demand at a given discount level

        Uses price elasticity to project demand lift
        """

        # Demand increases as price decreases
        # New_Demand = Base_Demand * (1 / (1 - discount))^elasticity
        if discount_pct >= 100:
            return base_demand * 10  # Arbitrary large number

        price_ratio = 1 / (1 - discount_pct/100)
        demand_multiplier = price_ratio ** elasticity

        return base_demand * demand_multiplier

    def calculate_revenue(self, discount_percentages):
        """
        Calculate total revenue for given discount strategy

        Parameters:
        - discount_percentages: Array of discount % for each SKU
        """

        total_revenue = 0

        for i, row in self.skus.iterrows():
            discount_pct = discount_percentages[i]

            # New price after discount
            new_price = row['current_price'] * (1 - discount_pct/100)

            # Estimated demand at this price
            estimated_demand = self.estimate_demand_at_discount(
                row['weekly_demand_base'],
                row['elasticity'],
                discount_pct
            )

            # Units sold (capped at inventory)
            units_sold = min(estimated_demand * 8, row['inventory'])  # 8 weeks

            # Revenue
            revenue = units_sold * new_price

            total_revenue += revenue

        return total_revenue

    def optimize_markdowns(self, max_avg_discount=40, min_clearance_rate=70):
        """
        Find optimal markdown strategy

        Constraints:
        - Average discount across SKUs <= max_avg_discount
        - Achieve min_clearance_rate sell-through
        """

        n_skus = len(self.skus)

        # Objective: Maximize revenue (minimize negative revenue)
        def objective(discounts):
            return -self.calculate_revenue(discounts)

        # Constraints
        constraints_list = []

        # Constraint 1: Average discount <= max
        def avg_discount_constraint(discounts):
            return max_avg_discount - np.mean(discounts)

        constraints_list.append({
            'type': 'ineq',
            'fun': avg_discount_constraint
        })

        # Constraint 2: Achieve minimum clearance rate
        def clearance_constraint(discounts):
            total_cleared = 0
            total_inventory = 0

            for i, row in self.skus.iterrows():
                discount_pct = discounts[i]
                new_price = row['current_price'] * (1 - discount_pct/100)

                estimated_demand = self.estimate_demand_at_discount(
                    row['weekly_demand_base'],
                    row['elasticity'],
                    discount_pct
                )

                units_sold = min(estimated_demand * 8, row['inventory'])
                total_cleared += units_sold
                total_inventory += row['inventory']

            clearance_rate = total_cleared / total_inventory * 100
            return clearance_rate - min_clearance_rate

        constraints_list.append({
            'type': 'ineq',
            'fun': clearance_constraint
        })

        # Bounds: 0% to 70% discount
        bounds = [(0, 70) for _ in range(n_skus)]

        # Initial guess: uniform discount
        x0 = np.full(n_skus, 30.0)

        # Optimize
        result = minimize(
            objective,
            x0,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints_list
        )

        optimal_discounts = result.x

        # Calculate results
        results = []
        for i, row in self.skus.iterrows():
            discount = optimal_discounts[i]
            new_price = row['current_price'] * (1 - discount/100)

            estimated_demand = self.estimate_demand_at_discount(
                row['weekly_demand_base'],
                row['elasticity'],
                discount
            )

            units_sold = min(estimated_demand * 8, row['inventory'])
            revenue = units_sold * new_price
            clearance_rate = units_sold / row['inventory'] * 100

            results.append({
                'sku': row['sku'],
                'current_price': row['current_price'],
                'optimal_discount': discount,
                'new_price': new_price,
                'estimated_units_sold': units_sold,
                'revenue': revenue,
                'clearance_rate': clearance_rate
            })

        results_df = pd.DataFrame(results)

        return results_df, result

# Example
skus_data = pd.DataFrame({
    'sku': [f'SKU{i}' for i in range(1, 11)],
    'inventory': np.random.randint(100, 1000, 10),
    'cost': np.random.uniform(20, 50, 10),
    'current_price': np.random.uniform(50, 150, 10),
    'elasticity': np.random.uniform(0.8, 2.0, 10),
    'weekly_demand_base': np.random.uniform(5, 30, 10)
})

optimizer = MarkdownOptimizer(skus_data, {})

# Optimize
optimal_strategy, optimization_result = optimizer.optimize_markdowns(
    max_avg_discount=35,
    min_clearance_rate=75
)

print("Optimal Markdown Strategy:")
print(optimal_strategy[['sku', 'optimal_discount', 'new_price', 'estimated_units_sold', 'clearance_rate']])
print(f"\nTotal revenue: ${optimal_strategy['revenue'].sum():,.0f}")
print(f"Average discount: {optimal_strategy['optimal_discount'].mean():.1f}%")
print(f"Average clearance rate: {optimal_strategy['clearance_rate'].mean():.1f}%")
```

---

## Store-Level Markdown Decisions

**Localized Markdown Strategy:**

```python
class StoreMarkdownManager:
    """
    Manage store-level markdown decisions

    Some stores need different markdown strategies than others
    """

    def __init__(self, stores_data):
        self.stores = stores_data

    def should_markdown_locally(self, sku, store_id, chain_markdown_pct=0):
        """
        Decide if store should markdown locally vs. follow chain

        Factors:
        - Local inventory level (excess?)
        - Local sell-through performance
        - Local competitive pressure
        """

        store = self.stores[self.stores['store_id'] == store_id].iloc[0]

        # Get SKU-specific data at store
        sku_inventory = store.get(f'{sku}_inventory', 0)
        sku_weekly_sales = store.get(f'{sku}_weekly_sales', 0)
        weeks_of_supply = sku_inventory / sku_weekly_sales if sku_weekly_sales > 0 else 999

        # Decision criteria
        local_markdown_needed = False
        reasons = []

        # Criterion 1: Excessive local inventory
        chain_avg_wos = 8  # Example chain average
        if weeks_of_supply > chain_avg_wos * 1.5:
            local_markdown_needed = True
            reasons.append(f"Excess inventory: {weeks_of_supply:.1f} weeks (chain avg: {chain_avg_wos})")

        # Criterion 2: Poor local performance
        chain_avg_str = 65  # Example
        local_str = store.get(f'{sku}_str', 50)
        if local_str < chain_avg_str * 0.8:
            local_markdown_needed = True
            reasons.append(f"Low STR: {local_str:.1f}% (chain avg: {chain_avg_str}%)")

        # Criterion 3: Competitive pressure
        if store.get('high_competition', False):
            local_markdown_needed = True
            reasons.append("High local competitive pressure")

        # Recommend local markdown depth
        if local_markdown_needed:
            # Go deeper than chain markdown
            recommended_markdown = max(chain_markdown_pct + 10, 30)
        else:
            # Follow chain markdown
            recommended_markdown = chain_markdown_pct

        return {
            'local_markdown_needed': local_markdown_needed,
            'reasons': reasons,
            'recommended_markdown': recommended_markdown,
            'weeks_of_supply': weeks_of_supply,
            'follow_chain': not local_markdown_needed
        }

    def identify_stores_for_clearance_transfer(self, sku, min_inventory=50):
        """
        Identify stores with excess inventory to transfer to outlet/clearance stores

        Better than heavy markdowns in regular stores
        """

        stores_with_excess = []

        for idx, store in self.stores.iterrows():
            sku_inventory = store.get(f'{sku}_inventory', 0)
            sku_weekly_sales = store.get(f'{sku}_weekly_sales', 0.1)

            if sku_inventory > min_inventory:
                weeks_of_supply = sku_inventory / sku_weekly_sales

                if weeks_of_supply > 15:  # Way too much
                    stores_with_excess.append({
                        'store_id': store['store_id'],
                        'inventory': sku_inventory,
                        'weeks_of_supply': weeks_of_supply,
                        'recommended_transfer_qty': int(sku_inventory * 0.5)  # Transfer half
                    })

        return pd.DataFrame(stores_with_excess)

# Example
stores_data = pd.DataFrame({
    'store_id': [f'S{i:03d}' for i in range(1, 21)],
    'high_competition': np.random.choice([True, False], 20, p=[0.3, 0.7])
})

# Add SKU-specific data
for idx, row in stores_data.iterrows():
    stores_data.at[idx, 'SKU001_inventory'] = np.random.randint(50, 300)
    stores_data.at[idx, 'SKU001_weekly_sales'] = np.random.randint(5, 25)
    stores_data.at[idx, 'SKU001_str'] = np.random.uniform(40, 80)

manager = StoreMarkdownManager(stores_data)

# Check if specific store needs local markdown
local_decision = manager.should_markdown_locally('SKU001', 'S001', chain_markdown_pct=20)
print(f"Store S001 - Local markdown needed: {local_decision['local_markdown_needed']}")
print(f"Recommended: {local_decision['recommended_markdown']}%")
print(f"Reasons: {local_decision['reasons']}")

# Find stores for clearance transfer
transfer_candidates = manager.identify_stores_for_clearance_transfer('SKU001')
print(f"\nStores with excess inventory for transfer:")
print(transfer_candidates)
```

---

## Tools & Libraries

### Python Libraries

**Optimization:**
- `scipy.optimize`: Non-linear optimization for price optimization
- `pulp`, `pyomo`: Mathematical programming
- `cvxpy`: Convex optimization

**Machine Learning:**
- `scikit-learn`: Regression for price elasticity
- `xgboost`: Price-demand modeling
- `statsmodels`: Statistical analysis

**Data Processing:**
- `pandas`: Data manipulation
- `numpy`: Numerical computations

### Commercial Software

**Pricing & Markdown:**
- **Revionics**: Price optimization and markdown management
- **Blue Yonder (JDA) Price**: AI-powered pricing
- **Oracle Retail Price Optimization**: Enterprise markdown optimization
- **Competera**: Dynamic pricing platform
- **Pricefx**: Cloud pricing software

**Analytics:**
- **Tableau**, **Power BI**: Markdown analytics and visualization
- **SAP Analytics**: Enterprise analytics

---

## Common Challenges & Solutions

### Challenge: Cannibalization Risk

**Problem:**
- Markdowns cannibalize full-price sales
- Customers wait for discounts
- Erodes full-price sell-through

**Solutions:**
- Targeted markdowns (store-specific, limited locations)
- Don't advertise broadly
- Use loyalty program for personalized discounts
- Mark down oldest inventory first
- Transfer to outlets vs. markdown in-store
- Separate clearance section

### Challenge: Brand Damage from Heavy Discounting

**Problem:**
- Excessive markdowns hurt brand perception
- Conditions customers to wait for sales
- Race to bottom with competitors

**Solutions:**
- Strategic markdown limits (max 40-50%)
- Use outlets/clearance stores for deep discounts
- Donation/liquidation vs. very deep markdowns
- Improve buying to reduce markdowns
- Focus on sell-through at full price
- Premium vs. value product segmentation

### Challenge: Insufficient Price Elasticity Data

**Problem:**
- New products have no markdown history
- Can't estimate optimal markdown level
- Guessing leads to suboptimal decisions

**Solutions:**
- Use analog products (similar items)
- Test different markdowns in pilot stores
- Industry benchmark elasticities
- Assume moderate elasticity (1.0-1.5) as starting point
- Machine learning on product attributes
- Build elasticity database over time

### Challenge: Omnichannel Pricing Complexity

**Problem:**
- Different prices online vs. stores
- Customer confusion and complaints
- Showrooming/webrooming behavior

**Solutions:**
- Uniform pricing across channels (preferred)
- Online-exclusive clearance section
- Price match guarantees
- Zone-based online pricing
- Clear communication of pricing policy
- Use loyalty for personalization vs. blanket markdowns

### Challenge: Markdown Timing Mistakes

**Problem:**
- Mark down too early → lose full-price sales
- Mark down too late → can't clear inventory
- Both costly errors

**Solutions:**
- Monitor sell-through rate thresholds
- Automated markdown triggers
- Multi-stage markdown cadence
- Regional timing differences (climate)
- Competitive monitoring
- Post-season analysis to improve next year

---

## Output Format

### Markdown Optimization Report

**Executive Summary:**
- Total inventory at risk: $8.2M retail value (42,000 units)
- Current markdown rate: 28% of sales
- Target markdown rate: <22%
- Recommended markdown strategy: Progressive, targeted approach
- Expected markdown cost: $1.8M (22% of inventory value)
- Expected revenue recovery: $6.4M (78%)

**SKU-Level Markdown Recommendations:**

| SKU | Category | Inventory | Weeks Supply | Current STR | Recommended Action | Discount % | New Price | Expected Revenue |
|-----|----------|-----------|--------------|-------------|-------------------|-----------|-----------|------------------|
| SKU001 | Outerwear | 850 | 18 | 42% | Markdown now | 40% | $59.99 | $41K |
| SKU002 | Dresses | 1,200 | 22 | 38% | Markdown now | 50% | $39.99 | $38K |
| SKU003 | Tops | 650 | 12 | 58% | Markdown week 3 | 30% | $34.99 | $18K |
| SKU004 | Bottoms | 420 | 8 | 68% | Monitor, no action | 0% | $49.99 | $21K |
| SKU005 | Accessories | 2,100 | 25 | 35% | Transfer to outlet | 60% | $15.99 | $27K |

**Markdown Cadence by SKU:**

| SKU | Stage 1 | Stage 2 | Stage 3 | Clearance |
|-----|---------|---------|---------|-----------|
| SKU001 | 30% off (Now) | 50% off (Week 3) | 60% off (Week 6) | Liquidate remainder |
| SKU002 | 40% off (Now) | 60% off (Week 2) | 70% off (Week 5) | Donate remainder |
| SKU003 | 20% off (Week 2) | 40% off (Week 5) | - | - |

**Store-Level Variations:**

| Store Cluster | Chain Markdown | Local Adjustment | Rationale |
|---------------|----------------|------------------|-----------|
| High-volume urban | Follow chain | None | On track for sell-through |
| Suburban malls | Follow chain | +10% deeper | Excess inventory, competitive pressure |
| Small format | Follow chain | Transfer to larger stores | Limited space, small quantities |
| Outlets | Aggressive | 60-70% off | Clearance destination |

**Financial Impact:**

| Metric | Without Optimization | With Optimization | Improvement |
|--------|---------------------|-------------------|-------------|
| Total revenue recovery | $5.8M | $6.4M | +$600K |
| Markdown cost | $2.4M (29%) | $1.8M (22%) | -$600K |
| Units cleared | 28,000 (67%) | 34,000 (81%) | +14 pts |
| Weeks to clear | 12 weeks | 8 weeks | -4 weeks |

**Implementation Plan:**

| Week | Action | SKUs | Expected Impact |
|------|--------|------|-----------------|
| Week 1 | First markdown wave (30-40% off) | 15 SKUs | Clear 8,000 units, $480K revenue |
| Week 2 | Second markdown wave (20-30% off) | 12 SKUs | Clear 6,000 units, $340K revenue |
| Week 3 | Deepen discounts on slow movers | 8 SKUs | Clear 5,000 units, $180K revenue |
| Week 4-6 | Transfer excess to outlets | 5 SKUs | Clear 10,000 units, $250K revenue |
| Week 7-8 | Final clearance (60-70% off) | All remaining | Clear 5,000 units, $120K revenue |

---

## Questions to Ask

If you need more context:
1. What inventory needs to be marked down? (age, quantity, categories)
2. What's your current markdown rate? Target?
3. How much time do you have? (end of season, weeks remaining)
4. What's the current sell-through rate?
5. Do you have historical price elasticity data?
6. What markdown control do you have? (frequency, depth, store-level)
7. Do you have outlet stores for clearance?
8. What are competitor markdown practices?
9. Any margin constraints? (minimum acceptable margin)

---

## Related Skills

- **retail-allocation**: Initial allocation to minimize future markdowns
- **demand-forecasting**: Forecast demand at different price points
- **retail-replenishment**: Replenishment strategy to avoid overstock
- **seasonal-planning**: Seasonal buy planning to reduce markdown risk
- **promotional-planning**: Promotional strategy vs. markdown strategy
- **inventory-optimization**: Inventory management to minimize markdowns
- **supply-chain-analytics**: Markdown performance metrics
