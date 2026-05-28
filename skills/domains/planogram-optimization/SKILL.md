---
name: planogram-optimization
description: When the user wants to optimize store planograms, shelf space allocation, or visual merchandising layout. Also use when the user mentions "planogram," "shelf space optimization," "space productivity," "category management," "shelf allocation," "fixture planning," "facings optimization," or "merchandising layout." For inventory allocation, see retail-allocation. For assortment planning, see seasonal-planning.
---

# Planogram Optimization

You are an expert in retail planogram optimization and space management. Your goal is to help retailers maximize sales and profitability per square foot by optimally allocating shelf space, determining product facings, and designing efficient store layouts that balance product visibility, customer experience, and operational efficiency.

## Initial Assessment

Before optimizing planograms, understand:

1. **Store Context**
   - What store format? (grocery, apparel, electronics, pharmacy)
   - Store size and layout? (square footage, number of fixtures)
   - Traffic patterns? (entrance location, checkout placement)
   - Target customer demographics?
   - Store location type? (urban, suburban, mall)

2. **Category Characteristics**
   - What category/department needs optimization?
   - Number of SKUs in category?
   - Product dimensions? (height, width, depth)
   - Unit movement rates? (fast vs. slow movers)
   - Margin by SKU?
   - Shelf life considerations? (perishable, seasonal)

3. **Current Performance**
   - Current sales per square foot?
   - Out-of-stock frequency?
   - Space productivity by fixture?
   - Customer satisfaction with layout?
   - Labor cost for restocking?

4. **Business Objectives**
   - Maximize revenue or profit?
   - Target service level? (stock availability)
   - Cross-merchandising goals?
   - Brand/promotional requirements?
   - Operational constraints? (restocking frequency, labor)

---

## Planogram Optimization Framework

### Space Productivity Principles

**1. Space Elasticity**
- Relationship between shelf space and sales
- Diminishing returns: more space doesn't always = more sales
- Optimal facings per SKU varies by product

**2. Space Allocation Rules**
- **High-turnover items**: More facings, eye-level placement
- **High-margin items**: Premium placement
- **Impulse items**: End caps, checkout
- **Destination items**: Can be placed in back (draws traffic)
- **Complementary items**: Cross-merchandising clusters

**3. Shelf Height Effects**
- **Eye level (4-5 ft)**: Prime real estate, 40% of sales
- **Chest level (3-4 ft)**: Secondary prime, 30% of sales
- **Waist level (2-3 ft)**: Third tier, 20% of sales
- **Floor level (0-2 ft)**: Low visibility, 10% of sales
- **Above eye (5-6 ft)**: Overflow, occasional purchases

**4. Product Adjacency**
- Related products together (pasta + sauce)
- Color blocking for visual appeal
- Size progression (small to large)
- Price progression (low to high)

---

## Space-to-Sales Analysis

### Space Elasticity Modeling

```python
import numpy as np
import pandas as pd
from scipy.optimize import minimize
import matplotlib.pyplot as plt

class SpaceElasticityAnalyzer:
    """
    Analyze space elasticity - relationship between shelf space and sales

    Space Elasticity = % change in sales / % change in shelf space
    """

    def __init__(self, historical_data):
        """
        Parameters:
        - historical_data: DataFrame with space/sales experiments
          columns: ['sku', 'period', 'facings', 'sales_units', 'sales_dollars']
        """
        self.data = historical_data

    def calculate_space_elasticity(self, sku):
        """
        Calculate space elasticity coefficient

        Using log-log regression: log(Sales) = a + b * log(Facings)
        b is the space elasticity
        """

        sku_data = self.data[self.data['sku'] == sku].copy()

        if len(sku_data) < 5:
            return {'error': 'Insufficient data'}

        # Log transformation
        sku_data['log_facings'] = np.log(sku_data['facings'])
        sku_data['log_sales'] = np.log(sku_data['sales_units'] + 1)

        # Linear regression in log-log space
        X = sku_data['log_facings'].values.reshape(-1, 1)
        y = sku_data['log_sales'].values

        from sklearn.linear_model import LinearRegression
        model = LinearRegression()
        model.fit(X, y)

        elasticity = model.coef_[0]
        r_squared = model.score(X, y)

        # Interpretation
        if elasticity > 0.8:
            interpretation = 'High elasticity - sales very responsive to space'
        elif elasticity > 0.4:
            interpretation = 'Moderate elasticity - typical'
        elif elasticity > 0.1:
            interpretation = 'Low elasticity - limited response to space'
        else:
            interpretation = 'Very low elasticity - sales not space-dependent'

        return {
            'sku': sku,
            'elasticity': elasticity,
            'r_squared': r_squared,
            'interpretation': interpretation,
            'model': model
        }

    def estimate_sales_at_facings(self, sku, target_facings):
        """
        Estimate sales at a given number of facings

        Uses fitted elasticity model
        """

        elasticity_result = self.calculate_space_elasticity(sku)

        if 'error' in elasticity_result:
            return None

        model = elasticity_result['model']
        log_facings = np.log(target_facings)

        log_sales_pred = model.predict([[log_facings]])[0]
        estimated_sales = np.exp(log_sales_pred) - 1

        return max(0, estimated_sales)

    def find_optimal_facings(self, sku, cost_per_facing, profit_per_unit,
                            max_facings=20):
        """
        Find optimal number of facings to maximize profit

        Balance: More facings = more sales but higher space cost
        """

        elasticity_result = self.calculate_space_elasticity(sku)

        if 'error' in elasticity_result:
            return {'error': 'Cannot optimize without elasticity data'}

        facings_range = range(1, max_facings + 1)
        results = []

        for facings in facings_range:
            estimated_sales = self.estimate_sales_at_facings(sku, facings)

            # Calculate profit
            revenue = estimated_sales * profit_per_unit
            space_cost = facings * cost_per_facing

            profit = revenue - space_cost

            results.append({
                'facings': facings,
                'estimated_sales': estimated_sales,
                'revenue': revenue,
                'space_cost': space_cost,
                'profit': profit,
                'profit_per_facing': profit / facings if facings > 0 else 0
            })

        results_df = pd.DataFrame(results)

        # Find optimal
        optimal_idx = results_df['profit'].idxmax()
        optimal = results_df.iloc[optimal_idx]

        return {
            'optimal_facings': optimal['facings'],
            'expected_sales': optimal['estimated_sales'],
            'expected_profit': optimal['profit'],
            'elasticity': elasticity_result['elasticity'],
            'all_scenarios': results_df
        }

# Example usage
np.random.seed(42)

# Generate sample data - simulate space elasticity
historical_data = []

for sku_id in range(1, 6):
    # Each SKU has different elasticity
    base_sales = np.random.uniform(50, 200)
    elasticity = np.random.uniform(0.2, 0.7)

    for period in range(20):
        facings = np.random.randint(2, 15)

        # Sales = base * (facings ^ elasticity) + noise
        sales = base_sales * (facings ** elasticity) + np.random.normal(0, 10)
        sales = max(0, sales)

        historical_data.append({
            'sku': f'SKU{sku_id:03d}',
            'period': period,
            'facings': facings,
            'sales_units': sales,
            'sales_dollars': sales * np.random.uniform(3, 8)
        })

historical_df = pd.DataFrame(historical_data)

# Analyze elasticity
analyzer = SpaceElasticityAnalyzer(historical_df)
elasticity = analyzer.calculate_space_elasticity('SKU001')

print(f"Space Elasticity: {elasticity['elasticity']:.3f}")
print(f"Interpretation: {elasticity['interpretation']}")
print(f"R-squared: {elasticity['r_squared']:.3f}")

# Find optimal facings
optimization = analyzer.find_optimal_facings(
    sku='SKU001',
    cost_per_facing=2.5,  # Cost per facing per week
    profit_per_unit=4.0,   # Profit margin per unit
    max_facings=15
)

print(f"\nOptimal facings: {optimization['optimal_facings']}")
print(f"Expected weekly sales: {optimization['expected_sales']:.0f} units")
print(f"Expected weekly profit: ${optimization['expected_profit']:.2f}")
```

---

## Planogram Optimization Models

### Fixture-Level Space Allocation

```python
class PlanogramOptimizer:
    """
    Optimize product placement and facings on a fixture

    Maximize sales/profit per square foot
    """

    def __init__(self, fixture_config, products_data):
        """
        Parameters:
        - fixture_config: Dict with fixture dimensions
          {'shelves': 5, 'width_inches': 48, 'depth_inches': 12}
        - products_data: DataFrame with product info
          columns: ['sku', 'width_inches', 'depth_inches', 'height_inches',
                   'weekly_sales', 'profit_per_unit', 'min_facings', 'max_facings']
        """
        self.fixture = fixture_config
        self.products = products_data

    def calculate_space_productivity(self, allocation):
        """
        Calculate sales and profit per square foot for an allocation

        allocation: Dict {sku: {'shelf': shelf_num, 'facings': count}}
        """

        total_sales = 0
        total_profit = 0
        space_used = {}  # Track space used per shelf

        for sku, placement in allocation.items():
            product = self.products[self.products['sku'] == sku].iloc[0]

            # Calculate space consumption
            facings = placement['facings']
            width_per_facing = product['width_inches']
            total_width = facings * width_per_facing

            shelf = placement['shelf']

            # Update space tracking
            if shelf not in space_used:
                space_used[shelf] = 0
            space_used[shelf] += total_width

            # Calculate sales (with space elasticity effect)
            base_sales = product['weekly_sales']
            elasticity = product.get('space_elasticity', 0.4)

            # Diminishing returns: sales = base * (facings ^ elasticity)
            adjusted_sales = base_sales * (facings ** elasticity)

            total_sales += adjusted_sales
            total_profit += adjusted_sales * product['profit_per_unit']

        # Calculate space utilization
        total_space_sqft = (
            self.fixture['shelves'] *
            self.fixture['width_inches'] *
            self.fixture['depth_inches'] / 144  # Convert to sqft
        )

        sales_per_sqft = total_sales / total_space_sqft if total_space_sqft > 0 else 0
        profit_per_sqft = total_profit / total_space_sqft if total_space_sqft > 0 else 0

        # Check constraints
        valid = True
        for shelf, width_used in space_used.items():
            if width_used > self.fixture['width_inches']:
                valid = False

        return {
            'total_sales': total_sales,
            'total_profit': total_profit,
            'sales_per_sqft': sales_per_sqft,
            'profit_per_sqft': profit_per_sqft,
            'space_utilization': space_used,
            'valid': valid
        }

    def greedy_allocation(self, objective='profit'):
        """
        Greedy algorithm to allocate products to fixture

        Prioritize by profit per square foot (or sales per sqft)
        """

        # Calculate priority score for each product
        self.products['priority'] = self.products.apply(
            lambda row: self._calculate_priority(row, objective),
            axis=1
        )

        # Sort by priority
        sorted_products = self.products.sort_values('priority', ascending=False)

        # Allocate
        allocation = {}
        shelf_space_remaining = {
            i: self.fixture['width_inches'] for i in range(self.fixture['shelves'])
        }

        for idx, product in sorted_products.iterrows():
            sku = product['sku']
            width = product['width_inches']
            min_facings = product.get('min_facings', 1)
            max_facings = product.get('max_facings', 10)

            # Try to allocate to best shelf position
            # Eye level (middle shelves) are most valuable
            shelf_priority = self._get_shelf_priority_order(self.fixture['shelves'])

            allocated = False

            for shelf in shelf_priority:
                max_facings_possible = int(shelf_space_remaining[shelf] / width)

                if max_facings_possible >= min_facings:
                    # Allocate optimal number of facings
                    facings = min(max_facings, max_facings_possible)

                    allocation[sku] = {
                        'shelf': shelf,
                        'facings': facings,
                        'position': 'center'  # Simplified
                    }

                    # Update remaining space
                    shelf_space_remaining[shelf] -= facings * width
                    allocated = True
                    break

            if not allocated:
                # Could not fit this product
                pass

        return allocation

    def _calculate_priority(self, product, objective):
        """Calculate priority score for product placement"""

        if objective == 'profit':
            # Profit per unit of space
            space_per_unit = product['width_inches'] * product['depth_inches']
            return (product['weekly_sales'] * product['profit_per_unit']) / space_per_unit

        else:  # sales
            space_per_unit = product['width_inches'] * product['depth_inches']
            return product['weekly_sales'] / space_per_unit

    def _get_shelf_priority_order(self, num_shelves):
        """
        Get shelf allocation priority

        Eye level (middle) is most valuable
        """

        if num_shelves <= 3:
            return list(range(num_shelves))

        # Middle shelves first
        middle = num_shelves // 2
        priority = [middle]

        # Alternate above and below middle
        for offset in range(1, num_shelves):
            if middle + offset < num_shelves:
                priority.append(middle + offset)
            if middle - offset >= 0:
                priority.append(middle - offset)

        return priority

    def optimize_with_constraints(self, objective='profit',
                                  category_constraints=None):
        """
        Optimize with business constraints

        Constraints:
        - Minimum facings per SKU
        - Maximum facings per SKU
        - Product grouping (keep related products together)
        - Brand requirements
        """

        # Use greedy as baseline
        allocation = self.greedy_allocation(objective)

        # Calculate performance
        performance = self.calculate_space_productivity(allocation)

        return allocation, performance

    def create_visual_planogram(self, allocation):
        """
        Create visual representation of planogram

        Returns ASCII art / simple visualization
        """

        # Group by shelf
        shelves = {}
        for sku, placement in allocation.items():
            shelf = placement['shelf']
            if shelf not in shelves:
                shelves[shelf] = []

            product = self.products[self.products['sku'] == sku].iloc[0]
            width = product['width_inches'] * placement['facings']

            shelves[shelf].append({
                'sku': sku,
                'facings': placement['facings'],
                'width': width
            })

        # Print planogram
        print(f"\nPLANOGRAM - {self.fixture['width_inches']}\" wide x {self.fixture['shelves']} shelves")
        print("=" * 60)

        for shelf in range(self.fixture['shelves'] - 1, -1, -1):  # Top to bottom
            print(f"Shelf {shelf + 1}:", end=" ")

            if shelf in shelves:
                for item in shelves[shelf]:
                    # Display SKU with facings
                    display = f"[{item['sku']}x{item['facings']}]"
                    print(display, end=" ")
            else:
                print("(empty)", end="")

            print()

        print("=" * 60)

# Example
fixture_config = {
    'shelves': 5,
    'width_inches': 48,
    'depth_inches': 12
}

products_data = pd.DataFrame({
    'sku': [f'SKU{i:03d}' for i in range(1, 16)],
    'width_inches': np.random.uniform(3, 8, 15),
    'depth_inches': np.random.uniform(4, 10, 15),
    'height_inches': np.random.uniform(6, 12, 15),
    'weekly_sales': np.random.uniform(10, 100, 15),
    'profit_per_unit': np.random.uniform(2, 8, 15),
    'space_elasticity': np.random.uniform(0.3, 0.6, 15),
    'min_facings': 1,
    'max_facings': np.random.randint(4, 12, 15)
})

optimizer = PlanogramOptimizer(fixture_config, products_data)

# Optimize
allocation, performance = optimizer.optimize_with_constraints(objective='profit')

print(f"Total weekly sales: ${performance['total_sales']:.0f}")
print(f"Total weekly profit: ${performance['total_profit']:.0f}")
print(f"Profit per sqft: ${performance['profit_per_sqft']:.2f}")

# Visualize
optimizer.create_visual_planogram(allocation)
```

---

## Category Management Integration

### Assortment-Space Optimization

```python
class CategorySpaceManager:
    """
    Manage category-level space allocation

    Decide how much space each category/subcategory gets
    """

    def __init__(self, store_data):
        self.store = store_data

    def allocate_space_to_categories(self, categories_data,
                                     total_space_sqft):
        """
        Allocate store space across categories

        Methods:
        - Sales-based: Proportional to sales
        - Profit-based: Proportional to profit
        - Hybrid: Balance sales and profit
        """

        # Calculate each category's contribution
        categories_data['sales_contribution'] = (
            categories_data['annual_sales'] /
            categories_data['annual_sales'].sum()
        )

        categories_data['profit_contribution'] = (
            categories_data['annual_profit'] /
            categories_data['annual_profit'].sum()
        )

        # Hybrid allocation (60% sales, 40% profit)
        categories_data['allocation_weight'] = (
            categories_data['sales_contribution'] * 0.6 +
            categories_data['profit_contribution'] * 0.4
        )

        # Allocate space
        categories_data['allocated_space_sqft'] = (
            categories_data['allocation_weight'] * total_space_sqft
        )

        # Calculate expected productivity
        categories_data['current_sales_per_sqft'] = (
            categories_data['annual_sales'] /
            categories_data['current_space_sqft']
        )

        categories_data['expected_sales_per_sqft'] = (
            categories_data['annual_sales'] /
            categories_data['allocated_space_sqft']
        )

        return categories_data[[
            'category', 'current_space_sqft', 'allocated_space_sqft',
            'annual_sales', 'annual_profit', 'current_sales_per_sqft',
            'expected_sales_per_sqft'
        ]]

    def recommend_space_adjustments(self, categories_data):
        """
        Identify categories that need more or less space

        Based on:
        - Sales per sqft vs. store average
        - Growth trends
        - Profit margins
        """

        store_avg_sales_per_sqft = (
            categories_data['annual_sales'].sum() /
            categories_data['current_space_sqft'].sum()
        )

        recommendations = []

        for idx, category in categories_data.iterrows():
            current_productivity = category['annual_sales'] / category['current_space_sqft']
            ratio_to_avg = current_productivity / store_avg_sales_per_sqft

            if ratio_to_avg > 1.3:
                recommendation = 'Expand space'
                reason = f"High productivity ({ratio_to_avg:.1f}x store average)"
                change_pct = '+15 to +25%'

            elif ratio_to_avg < 0.7:
                recommendation = 'Reduce space'
                reason = f"Low productivity ({ratio_to_avg:.1f}x store average)"
                change_pct = '-15 to -25%'

            else:
                recommendation = 'Maintain space'
                reason = 'Productivity in line with average'
                change_pct = '±5%'

            recommendations.append({
                'category': category['category'],
                'recommendation': recommendation,
                'reason': reason,
                'suggested_change': change_pct,
                'productivity_ratio': ratio_to_avg
            })

        return pd.DataFrame(recommendations)

# Example
categories_data = pd.DataFrame({
    'category': ['Dairy', 'Bakery', 'Produce', 'Meat', 'Frozen', 'Beverages'],
    'current_space_sqft': [800, 600, 1200, 900, 1500, 2000],
    'annual_sales': [1_200_000, 800_000, 1_500_000, 1_800_000, 1_400_000, 2_200_000],
    'annual_profit': [180_000, 240_000, 300_000, 360_000, 210_000, 330_000]
})

manager = CategorySpaceManager({})

# Allocate space
allocation = manager.allocate_space_to_categories(categories_data, total_space_sqft=7000)
print("Category Space Allocation:")
print(allocation)

# Recommendations
recommendations = manager.recommend_space_adjustments(categories_data)
print("\nSpace Adjustment Recommendations:")
print(recommendations)
```

---

## Cross-Merchandising & Adjacency

```python
class CrossMerchandisingOptimizer:
    """
    Optimize product adjacencies for cross-selling

    Place complementary products near each other
    """

    def __init__(self, products_data, affinity_matrix):
        """
        Parameters:
        - products_data: Product information
        - affinity_matrix: Cross-purchase patterns
          affinity_matrix[i][j] = likelihood customer buys j given they buy i
        """
        self.products = products_data
        self.affinity = affinity_matrix

    def identify_product_clusters(self, min_affinity=0.3):
        """
        Cluster products with high affinity

        Products that are frequently bought together
        """

        from sklearn.cluster import AgglomerativeClustering

        # Use affinity matrix for clustering
        clustering = AgglomerativeClustering(
            n_clusters=None,
            distance_threshold=1 - min_affinity,
            affinity='precomputed',
            linkage='average'
        )

        # Convert affinity to distance
        distance_matrix = 1 - self.affinity
        clusters = clustering.fit_predict(distance_matrix)

        self.products['cluster'] = clusters

        return self.products[['sku', 'cluster']]

    def score_adjacency(self, sku1, sku2):
        """
        Score how beneficial it is to place two products adjacent

        Higher score = more beneficial
        """

        idx1 = self.products[self.products['sku'] == sku1].index[0]
        idx2 = self.products[self.products['sku'] == sku2].index[0]

        # Bidirectional affinity
        affinity_1_to_2 = self.affinity[idx1, idx2]
        affinity_2_to_1 = self.affinity[idx2, idx1]

        # Combined score
        adjacency_score = (affinity_1_to_2 + affinity_2_to_1) / 2

        return adjacency_score

    def recommend_adjacencies(self, sku, top_n=5):
        """
        Recommend products to place next to a given SKU

        Based on cross-purchase affinity
        """

        idx = self.products[self.products['sku'] == sku].index[0]

        # Get affinities for this product
        affinities = self.affinity[idx, :]

        # Sort and get top N
        top_indices = np.argsort(affinities)[::-1][:top_n + 1]  # +1 to exclude self

        recommendations = []
        for other_idx in top_indices:
            other_sku = self.products.iloc[other_idx]['sku']

            if other_sku == sku:
                continue  # Skip self

            recommendations.append({
                'sku': other_sku,
                'affinity_score': affinities[other_idx],
                'rationale': 'Frequently purchased together'
            })

        return recommendations[:top_n]

# Example
n_products = 20
products_data = pd.DataFrame({
    'sku': [f'SKU{i:03d}' for i in range(1, n_products + 1)]
})

# Generate sample affinity matrix
# (in practice, this comes from transaction data)
np.random.seed(42)
affinity_matrix = np.random.rand(n_products, n_products) * 0.5
np.fill_diagonal(affinity_matrix, 1.0)  # Product always purchased with itself

# Make it symmetric (for simplicity)
affinity_matrix = (affinity_matrix + affinity_matrix.T) / 2

optimizer = CrossMerchandisingOptimizer(products_data, affinity_matrix)

# Identify clusters
clusters = optimizer.identify_product_clusters(min_affinity=0.3)
print("Product Clusters:")
print(clusters.groupby('cluster')['sku'].apply(list))

# Get adjacency recommendations
recommendations = optimizer.recommend_adjacencies('SKU001', top_n=5)
print(f"\nRecommended adjacencies for SKU001:")
for rec in recommendations:
    print(f"  {rec['sku']}: {rec['affinity_score']:.2f}")
```

---

## Tools & Libraries

### Python Libraries

**Optimization:**
- `scipy.optimize`: Non-linear optimization
- `pulp`, `pyomo`: Linear programming for space allocation
- `ortools`: Constraint programming for planograms

**Machine Learning:**
- `scikit-learn`: Clustering for product grouping
- `mlxtend`: Association rule mining (market basket analysis)

**Visualization:**
- `matplotlib`, `seaborn`: Planogram visualization
- `plotly`: Interactive layouts
- `PIL` (Pillow): Image-based planograms

### Commercial Software

**Planogram Software:**
- **JDA/Blue Yonder Intactix**: Enterprise space planning
- **RELEX Solutions**: Space & assortment optimization
- **Galleria by Movista**: Visual merchandising
- **Apollo by Shelf Logic**: AI-powered planograms
- **SCORPION by ESL**: Planogram automation

**Category Management:**
- **Nielsen Spaceman**: Space planning and optimization
- **IRI ProSpace**: Space productivity analytics
- **Symphony RetailAI**: AI-driven category management

**Specialized Tools:**
- **SmartDraw**: Basic planogram creation
- **PlanoHero**: Cloud planogram software
- **Quant**: Retail space intelligence

---

## Common Challenges & Solutions

### Challenge: Product Dimension Variability

**Problem:**
- Products have different sizes
- Irregular shapes don't fit neatly
- Wasted space from poor packing

**Solutions:**
- Modular shelf heights
- Adjustable dividers
- Product grouping by size
- Vertical stacking for small items
- Custom fixtures for odd shapes

### Challenge: Frequent Assortment Changes

**Problem:**
- New products introduced frequently
- Seasonal rotations
- Re-planogramming is labor-intensive

**Solutions:**
- Flexible planogram zones
- "Hot spot" areas for new products
- Micro-category approach (easier to swap)
- Digital planograms (easy updates)
- Planogram compliance automation

### Challenge: Store Format Diversity

**Problem:**
- Different store sizes
- Layout variations
- One planogram doesn't fit all

**Solutions:**
- Store clustering (A/B/C formats)
- Modular planogram approach
- Core vs. flex sections
- Automated planogram generation by store
- Local customization within guidelines

### Challenge: Operational Complexity

**Problem:**
- Restocking difficulty
- Labor time to execute resets
- Compliance monitoring hard

**Solutions:**
- Operational feasibility scoring
- Minimize SKU moves during resets
- Phased implementation
- Photo compliance apps
- Planogram simplification

### Challenge: Balancing Multiple Objectives

**Problem:**
- Maximize sales vs. profit
- Customer experience vs. efficiency
- Brand requirements vs. optimization
- Visual appeal vs. space productivity

**Solutions:**
- Multi-objective optimization
- Weighted scoring systems
- Constraints for brand/experience requirements
- A/B testing different approaches
- Category captain collaboration

---

## Output Format

### Planogram Optimization Report

**Executive Summary:**
- Category: Beverages (Soft Drinks section)
- Current performance: $450/sqft/week
- Optimized performance: $580/sqft/week (+29%)
- Fixture count: 12 fixtures (4ft sections)
- SKU count: 85 SKUs

**Current vs. Optimized Performance:**

| Metric | Current | Optimized | Improvement |
|--------|---------|-----------|-------------|
| Sales per sqft per week | $450 | $580 | +29% |
| Profit per sqft per week | $95 | $135 | +42% |
| Space utilization | 78% | 94% | +16 pts |
| SKU count | 85 | 72 | -13 SKUs |
| Avg facings per SKU | 3.2 | 4.5 | +41% |

**Top Changes - SKU Level:**

| SKU | Product | Current Facings | Optimized Facings | Change | Rationale |
|-----|---------|----------------|-------------------|--------|-----------|
| SKU001 | Coke 12pk | 4 | 8 | +4 | High sales, elastic to space |
| SKU015 | Pepsi 2L | 6 | 4 | -2 | Low elasticity, over-spaced |
| SKU023 | LaCroix variety | 2 | 6 | +4 | Growing category, undersized |
| SKU045 | Generic cola | 3 | 0 | -3 (discontinue) | Poor sales per facing |

**Shelf-Level Plan:**

```
PLANOGRAM - Soft Drinks Section (48" x 5 shelves)
============================================================
Shelf 5: [Coke12pkx8] [Pepsi12pkx6] [Sprite12pkx5]
Shelf 4: [Coke2Lx6] [Pepsi2Lx4] [DrPepper2Lx4] [Sprite2Lx4]
Shelf 3: [LaCroixX6] [BublyX5] [Perrier6pkx4]
Shelf 2: [CokeCansx4] [PepsiCansx4] [Energy6pkx5]
Shelf 1: [2LSparkling1] [2LSparkling2] [Juice4pkx3]
============================================================
```

**Space Productivity by Fixture:**

| Fixture | Current $/sqft/wk | Optimized $/sqft/wk | Improvement |
|---------|------------------|---------------------|-------------|
| Fixture 1 (Eye-level) | $620 | $780 | +26% |
| Fixture 2 (Eye-level) | $580 | $750 | +29% |
| Fixture 3 (Chest-level) | $480 | $610 | +27% |
| Fixture 4 (Waist-level) | $380 | $490 | +29% |

**Cross-Merchandising Opportunities:**

1. **Chips + Dips cluster**: Add salsa adjacent to chips (+$8K annual sales)
2. **Pasta + Sauce**: Consolidate for convenience (+$12K annual sales)
3. **Baking needs**: Cluster flour, sugar, baking soda (+$6K annual sales)

**Implementation Plan:**

| Phase | Actions | SKUs Affected | Labor Hours | Timeline |
|-------|---------|---------------|-------------|----------|
| Phase 1 | Adjust facings (no moves) | 25 | 8 hours | Week 1 |
| Phase 2 | Relocate high-movers to eye-level | 15 | 12 hours | Week 2 |
| Phase 3 | Discontinue poor performers | 13 | 4 hours | Week 3 |
| Phase 4 | Final adjustments & cleanup | All | 6 hours | Week 4 |

**Risk & Mitigation:**

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Out-of-stocks during reset | Medium | Medium | Overstock before reset, phased approach |
| Customer confusion | Low | High | Clear signage, staff briefing |
| Execution errors | Medium | Medium | Photo compliance, store visits |

---

## Questions to Ask

If you need more context:
1. What category/department needs optimization?
2. How many SKUs are in the category?
3. What's the current sales per square foot?
4. What fixtures are you using? (shelving, gondolas, end caps)
5. Do you have product dimension data?
6. Do you have historical sales by SKU?
7. Any space elasticity data? (testing different facings)
8. What are your constraints? (brand requirements, minimum facings)
9. Is this for one store or chain-wide?

---

## Related Skills

- **retail-allocation**: Initial inventory allocation to stores
- **retail-replenishment**: Restocking strategy
- **demand-forecasting**: Demand forecasting by SKU/store
- **inventory-optimization**: Safety stock and service levels
- **supply-chain-analytics**: Space productivity metrics
- **warehouse-slotting-optimization**: Similar concepts for warehouses
