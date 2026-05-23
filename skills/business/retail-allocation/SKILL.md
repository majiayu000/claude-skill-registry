---
name: retail-allocation
description: When the user wants to optimize retail allocation, distribute inventory to stores, or perform initial merchandise allocation. Also use when the user mentions "store allocation," "assortment planning," "size curve," "cluster allocation," "pre-pack," "store grading," or "initial allocation." For ongoing replenishment, see retail-replenishment. For markdown decisions, see markdown-optimization.
---

# Retail Allocation

You are an expert in retail allocation and assortment planning. Your goal is to help retailers optimally distribute new merchandise to stores, balancing local demand patterns, store capacity, and inventory efficiency to maximize sales and minimize markdowns.

## Initial Assessment

Before designing allocation strategies, understand:

1. **Merchandise Characteristics**
   - What product categories are being allocated?
   - Fashion vs. basic goods? (fashion = higher risk)
   - SKU count and complexity? (size/color/style matrix)
   - Unit costs and retail prices?
   - Seasonality? (back-to-school, holiday, spring)

2. **Store Network**
   - How many stores in the chain?
   - Store formats/tiers? (flagship, standard, outlet)
   - Store clustering approach? (demographic, climate, sales volume)
   - Store size variations? (square footage, inventory capacity)
   - Geographic spread? (regional differences)

3. **Current Process**
   - How is allocation done today? (manual, system-based)
   - What drives allocation decisions? (equal distribution, sales history, square footage)
   - Allocation frequency? (weekly, seasonal, ad-hoc)
   - What's the current sell-through rate?
   - What's the markdown rate?

4. **Business Goals**
   - Maximize sales or minimize markdowns?
   - Service level targets by store tier?
   - Inventory turn goals?
   - Desired stock coverage? (weeks of supply)
   - Regional/local customization level?

---

## Retail Allocation Framework

### Allocation Principles

**1. Demand-Driven Allocation**
- Allocate based on predicted local demand
- Consider demographics, climate, past sales
- Right product to right store in right quantity

**2. Store Clustering**
- Group similar stores together
- Allocate based on cluster characteristics
- Reduces complexity vs. store-by-store

**3. Grade-and-Flow**
- Grade stores by volume/importance
- A-stores get full assortment, deeper inventory
- C-stores get curated assortment, shallow inventory

**4. Size Curve Optimization**
- Allocate sizes based on local demand profile
- Avoid one-size-fits-all approach
- Urban vs. suburban vs. regional size differences

**5. Pre-Pack vs. Pick-Pack**
- Pre-packs: Fixed assortments, efficient DC operations
- Pick-pack: Customized by store, higher accuracy
- Trade-off: efficiency vs. optimization

---

## Store Clustering & Grading

### Store Clustering Analysis

```python
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

class StoreClusteringEngine:
    """
    Cluster stores for allocation planning

    Group stores with similar characteristics for efficient allocation
    """

    def __init__(self, store_data):
        """
        Parameters:
        - store_data: DataFrame with store attributes
          columns: ['store_id', 'sales_volume', 'demographics', 'climate',
                   'square_feet', 'location_type', 'income_level', etc.]
        """
        self.stores = store_data

    def create_clustering_features(self):
        """
        Engineer features for clustering

        Combine multiple attributes into clustering dimensions
        """

        features = self.stores.copy()

        # Sales volume (log-transformed for better distribution)
        features['log_sales'] = np.log1p(features['annual_sales'])

        # Demographics encoding
        features['high_income'] = (features['median_income'] > 75000).astype(int)
        features['urban'] = (features['location_type'] == 'urban').astype(int)
        features['suburban'] = (features['location_type'] == 'suburban').astype(int)

        # Climate encoding
        features['warm_climate'] = (features['avg_temp_f'] > 65).astype(int)
        features['cold_climate'] = (features['avg_temp_f'] < 45).astype(int)

        # Size normalized
        features['size_normalized'] = features['square_feet'] / 1000

        # Customer profile
        features['fashion_forward'] = features.get('fashion_index', 50) / 100

        # Select clustering features
        clustering_cols = [
            'log_sales', 'high_income', 'urban', 'suburban',
            'warm_climate', 'cold_climate', 'size_normalized',
            'fashion_forward'
        ]

        return features[['store_id'] + clustering_cols]

    def perform_clustering(self, n_clusters=8, method='kmeans'):
        """
        Cluster stores using K-means

        Returns cluster assignments and profiles
        """

        # Prepare features
        feature_df = self.create_clustering_features()
        feature_cols = [col for col in feature_df.columns if col != 'store_id']

        X = feature_df[feature_cols].values

        # Standardize features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # K-means clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        clusters = kmeans.fit_predict(X_scaled)

        # Add cluster labels
        feature_df['cluster'] = clusters

        # Profile each cluster
        cluster_profiles = []
        for cluster_id in range(n_clusters):
            cluster_stores = feature_df[feature_df['cluster'] == cluster_id]

            profile = {
                'cluster_id': cluster_id,
                'num_stores': len(cluster_stores),
                'avg_sales': np.exp(cluster_stores['log_sales'].mean()) - 1,
                'high_income_pct': cluster_stores['high_income'].mean() * 100,
                'urban_pct': cluster_stores['urban'].mean() * 100,
                'warm_climate_pct': cluster_stores['warm_climate'].mean() * 100,
                'avg_sqft': cluster_stores['size_normalized'].mean() * 1000,
                'fashion_index': cluster_stores['fashion_forward'].mean() * 100
            }

            # Generate cluster name
            profile['cluster_name'] = self._generate_cluster_name(profile)

            cluster_profiles.append(profile)

        return feature_df[['store_id', 'cluster']], pd.DataFrame(cluster_profiles)

    def _generate_cluster_name(self, profile):
        """Generate descriptive cluster name"""

        size = 'Large' if profile['avg_sqft'] > 15000 else 'Medium' if profile['avg_sqft'] > 8000 else 'Small'
        location = 'Urban' if profile['urban_pct'] > 50 else 'Suburban'
        income = 'High-Income' if profile['high_income_pct'] > 50 else 'Mid-Income'
        climate = 'Warm' if profile['warm_climate_pct'] > 50 else 'Cold'

        return f"{size} {location} {income} {climate}"

    def optimize_cluster_count(self, max_clusters=12):
        """
        Find optimal number of clusters using elbow method

        Returns: Plot of inertia by cluster count
        """

        feature_df = self.create_clustering_features()
        feature_cols = [col for col in feature_df.columns if col != 'store_id']
        X = feature_df[feature_cols].values

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        inertias = []
        cluster_range = range(2, max_clusters + 1)

        for k in cluster_range:
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            kmeans.fit(X_scaled)
            inertias.append(kmeans.inertia_)

        # Plot elbow curve
        plt.figure(figsize=(10, 6))
        plt.plot(cluster_range, inertias, 'bo-')
        plt.xlabel('Number of Clusters')
        plt.ylabel('Inertia')
        plt.title('Elbow Method For Optimal Clusters')
        plt.grid(True)

        return cluster_range, inertias

# Example usage
store_data = pd.DataFrame({
    'store_id': [f'S{i:03d}' for i in range(1, 151)],
    'annual_sales': np.random.lognormal(14, 0.5, 150),
    'median_income': np.random.normal(65000, 20000, 150),
    'location_type': np.random.choice(['urban', 'suburban', 'rural'], 150, p=[0.3, 0.5, 0.2]),
    'avg_temp_f': np.random.normal(55, 15, 150),
    'square_feet': np.random.normal(12000, 4000, 150),
    'fashion_index': np.random.normal(60, 20, 150)
})

clustering_engine = StoreClusteringEngine(store_data)
cluster_assignments, cluster_profiles = clustering_engine.perform_clustering(n_clusters=6)

print("Cluster Profiles:")
print(cluster_profiles[['cluster_id', 'cluster_name', 'num_stores', 'avg_sales']])
```

### Store Grading System

```python
class StoreGradingSystem:
    """
    Grade stores for allocation planning

    A stores: Highest volume, full assortment, deepest stock
    B stores: Medium volume, core assortment
    C stores: Lower volume, curated assortment
    """

    def __init__(self, store_sales_data):
        """
        Parameters:
        - store_sales_data: DataFrame with store performance
          columns: ['store_id', 'annual_sales', 'sales_per_sqft',
                   'inventory_turns', 'markdown_rate']
        """
        self.stores = store_sales_data

    def grade_stores(self, a_pct=20, b_pct=30):
        """
        Assign grades to stores

        Parameters:
        - a_pct: Percentage of stores to grade as A (top performers)
        - b_pct: Percentage to grade as B
        - Remainder are C stores
        """

        # Calculate composite score
        # Normalize each metric
        self.stores['sales_score'] = self._normalize_score(self.stores['annual_sales'])
        self.stores['efficiency_score'] = self._normalize_score(self.stores['sales_per_sqft'])
        self.stores['turns_score'] = self._normalize_score(self.stores['inventory_turns'])
        self.stores['markdown_score'] = self._normalize_score(
            -self.stores['markdown_rate']  # Lower markdown is better
        )

        # Weighted composite score
        self.stores['composite_score'] = (
            self.stores['sales_score'] * 0.5 +
            self.stores['efficiency_score'] * 0.2 +
            self.stores['turns_score'] * 0.2 +
            self.stores['markdown_score'] * 0.1
        )

        # Assign grades based on percentiles
        a_threshold = self.stores['composite_score'].quantile(1 - a_pct/100)
        b_threshold = self.stores['composite_score'].quantile(1 - (a_pct + b_pct)/100)

        def assign_grade(score):
            if score >= a_threshold:
                return 'A'
            elif score >= b_threshold:
                return 'B'
            else:
                return 'C'

        self.stores['grade'] = self.stores['composite_score'].apply(assign_grade)

        # Calculate grade statistics
        grade_stats = self.stores.groupby('grade').agg({
            'store_id': 'count',
            'annual_sales': 'sum',
            'sales_per_sqft': 'mean',
            'markdown_rate': 'mean'
        }).rename(columns={'store_id': 'num_stores'})

        grade_stats['sales_pct'] = (
            grade_stats['annual_sales'] / grade_stats['annual_sales'].sum() * 100
        )

        return self.stores[['store_id', 'grade', 'composite_score']], grade_stats

    def _normalize_score(self, series):
        """Normalize to 0-100 scale"""
        min_val = series.min()
        max_val = series.max()
        if max_val == min_val:
            return pd.Series([50] * len(series))
        return ((series - min_val) / (max_val - min_val)) * 100

    def recommend_allocation_depth(self, grade):
        """
        Recommend inventory depth by store grade

        Returns weeks of supply and min/max units
        """

        allocation_rules = {
            'A': {
                'weeks_of_supply': 8,
                'min_units': 10,
                'max_units': 100,
                'assortment_breadth': 'Full',
                'size_curve_depth': 'Deep (all sizes)'
            },
            'B': {
                'weeks_of_supply': 6,
                'min_units': 5,
                'max_units': 50,
                'assortment_breadth': 'Core (80% of SKUs)',
                'size_curve_depth': 'Medium (popular sizes)'
            },
            'C': {
                'weeks_of_supply': 4,
                'min_units': 2,
                'max_units': 20,
                'assortment_breadth': 'Curated (50% of SKUs)',
                'size_curve_depth': 'Shallow (best-sellers only)'
            }
        }

        return allocation_rules.get(grade, allocation_rules['C'])

# Example
store_performance = pd.DataFrame({
    'store_id': [f'S{i:03d}' for i in range(1, 101)],
    'annual_sales': np.random.lognormal(14, 0.6, 100),
    'sales_per_sqft': np.random.normal(350, 80, 100),
    'inventory_turns': np.random.normal(4.5, 1.0, 100),
    'markdown_rate': np.random.normal(0.25, 0.08, 100)
})

grading_system = StoreGradingSystem(store_performance)
store_grades, grade_stats = grading_system.grade_stores(a_pct=20, b_pct=30)

print("Store Grade Distribution:")
print(grade_stats)

print("\nAllocation Rules by Grade:")
for grade in ['A', 'B', 'C']:
    rules = grading_system.recommend_allocation_depth(grade)
    print(f"\nGrade {grade}:")
    print(f"  Weeks of supply: {rules['weeks_of_supply']}")
    print(f"  Assortment: {rules['assortment_breadth']}")
```

---

## Allocation Optimization

### Demand-Based Allocation

```python
class RetailAllocationEngine:
    """
    Optimize retail allocation using demand forecasts

    Allocate inventory to maximize sales while minimizing markdowns
    """

    def __init__(self, store_data, product_data):
        """
        Parameters:
        - store_data: Store attributes and clusters
        - product_data: Product attributes and total available inventory
        """
        self.stores = store_data
        self.products = product_data

    def calculate_store_demand(self, sku, store_id, forecast_period_weeks=12):
        """
        Calculate expected demand for SKU at store

        Uses:
        - Historical sales patterns
        - Store cluster characteristics
        - Seasonality
        - New product benchmarks
        """

        store = self.stores[self.stores['store_id'] == store_id].iloc[0]
        product = self.products[self.products['sku'] == sku].iloc[0]

        # Base demand from historical data
        if product.get('is_new_product', False):
            # New product: use similar product analogs
            base_weekly_demand = self._estimate_new_product_demand(product, store)
        else:
            # Existing product: use historical sales
            base_weekly_demand = store.get(f'{sku}_weekly_sales', 0)

        # Adjust for store characteristics
        cluster_factor = store.get('cluster_demand_index', 1.0)
        seasonality_factor = product.get('season_factor', 1.0)

        adjusted_weekly_demand = (
            base_weekly_demand *
            cluster_factor *
            seasonality_factor
        )

        total_forecast_demand = adjusted_weekly_demand * forecast_period_weeks

        return {
            'store_id': store_id,
            'sku': sku,
            'weekly_demand': adjusted_weekly_demand,
            'total_forecast_demand': total_forecast_demand,
            'forecast_weeks': forecast_period_weeks
        }

    def allocate_sku_to_stores(self, sku, total_available_units,
                               allocation_method='proportional'):
        """
        Allocate SKU inventory across stores

        Methods:
        - proportional: Allocate based on demand forecast
        - equal: Equal distribution (simple but suboptimal)
        - tiered: Different depths by store grade
        """

        # Calculate demand for each store
        store_demands = []
        for store_id in self.stores['store_id']:
            demand = self.calculate_store_demand(sku, store_id)
            store_demands.append(demand)

        demands_df = pd.DataFrame(store_demands)

        if allocation_method == 'proportional':
            allocations = self._allocate_proportional(
                demands_df, total_available_units
            )
        elif allocation_method == 'tiered':
            allocations = self._allocate_tiered(
                demands_df, total_available_units
            )
        else:  # equal
            allocations = self._allocate_equal(
                demands_df, total_available_units
            )

        return allocations

    def _allocate_proportional(self, demands_df, total_units):
        """
        Proportional allocation based on demand

        Stores with higher demand get more inventory
        """

        total_demand = demands_df['total_forecast_demand'].sum()

        if total_demand == 0:
            # No demand - distribute equally
            return self._allocate_equal(demands_df, total_units)

        # Calculate allocation percentage
        demands_df['allocation_pct'] = (
            demands_df['total_forecast_demand'] / total_demand
        )

        # Allocate units
        demands_df['allocated_units'] = (
            demands_df['allocation_pct'] * total_units
        ).astype(int)

        # Handle rounding - allocate remainder to highest demand stores
        allocated_total = demands_df['allocated_units'].sum()
        remainder = total_units - allocated_total

        if remainder > 0:
            # Give remainder to top stores by demand
            top_stores = demands_df.nlargest(remainder, 'total_forecast_demand')
            for idx in top_stores.index:
                demands_df.at[idx, 'allocated_units'] += 1

        # Calculate expected service level (allocation / demand)
        demands_df['service_level'] = np.minimum(
            demands_df['allocated_units'] / demands_df['total_forecast_demand'],
            1.0
        )

        return demands_df[['store_id', 'sku', 'allocated_units',
                          'total_forecast_demand', 'service_level']]

    def _allocate_tiered(self, demands_df, total_units):
        """
        Tiered allocation by store grade

        A stores get priority, then B, then C
        """

        # Merge with store grades
        demands_df = demands_df.merge(
            self.stores[['store_id', 'grade']],
            on='store_id'
        )

        # Allocate by tier
        allocations = []
        remaining_units = total_units

        for grade in ['A', 'B', 'C']:
            grade_stores = demands_df[demands_df['grade'] == grade]

            if len(grade_stores) == 0 or remaining_units == 0:
                continue

            # Allocate proportionally within grade
            grade_demand = grade_stores['total_forecast_demand'].sum()

            if grade_demand > 0:
                for idx, row in grade_stores.iterrows():
                    store_allocation = min(
                        int(remaining_units * (row['total_forecast_demand'] / grade_demand)),
                        row['total_forecast_demand'],
                        remaining_units
                    )

                    allocations.append({
                        'store_id': row['store_id'],
                        'sku': row['sku'],
                        'allocated_units': store_allocation,
                        'total_forecast_demand': row['total_forecast_demand'],
                        'grade': grade
                    })

                    remaining_units -= store_allocation

        return pd.DataFrame(allocations)

    def _allocate_equal(self, demands_df, total_units):
        """Simple equal distribution"""

        num_stores = len(demands_df)
        units_per_store = total_units // num_stores
        remainder = total_units % num_stores

        demands_df['allocated_units'] = units_per_store

        # Distribute remainder
        if remainder > 0:
            demands_df.iloc[:remainder, demands_df.columns.get_loc('allocated_units')] += 1

        return demands_df[['store_id', 'sku', 'allocated_units']]

    def _estimate_new_product_demand(self, product, store):
        """
        Estimate demand for new product using analog products

        Use similar products as reference
        """

        # Find similar products (same category, price range)
        similar_products_avg_sales = 10  # Simplified

        # Adjust for store characteristics
        store_factor = store.get('sales_index', 1.0)

        estimated_weekly_demand = similar_products_avg_sales * store_factor

        return estimated_weekly_demand

    def optimize_allocation_with_constraints(self, sku, total_units,
                                            min_units_per_store=2,
                                            max_units_per_store=50):
        """
        Optimize allocation with business constraints

        Ensures min/max bounds per store
        """

        # Calculate base allocation
        base_allocation = self.allocate_sku_to_stores(
            sku, total_units, allocation_method='proportional'
        )

        # Apply constraints
        base_allocation['allocated_units'] = base_allocation['allocated_units'].clip(
            lower=min_units_per_store,
            upper=max_units_per_store
        )

        # Rebalance if total exceeds available
        total_allocated = base_allocation['allocated_units'].sum()

        if total_allocated > total_units:
            # Reduce proportionally
            reduction_factor = total_units / total_allocated
            base_allocation['allocated_units'] = (
                base_allocation['allocated_units'] * reduction_factor
            ).astype(int)

        return base_allocation

# Example usage
store_data = pd.DataFrame({
    'store_id': [f'S{i:03d}' for i in range(1, 51)],
    'grade': np.random.choice(['A', 'B', 'C'], 50, p=[0.2, 0.3, 0.5]),
    'sales_index': np.random.uniform(0.7, 1.3, 50),
    'cluster_demand_index': np.random.uniform(0.8, 1.2, 50)
})

product_data = pd.DataFrame({
    'sku': ['SKU001'],
    'is_new_product': [False],
    'season_factor': [1.1]
})

allocation_engine = RetailAllocationEngine(store_data, product_data)

# Allocate 5000 units of SKU001
allocation_result = allocation_engine.allocate_sku_to_stores(
    sku='SKU001',
    total_available_units=5000,
    allocation_method='proportional'
)

print(f"Total allocated: {allocation_result['allocated_units'].sum()} units")
print(f"Average service level: {allocation_result['service_level'].mean():.1%}")
print(f"\nTop 5 allocations:")
print(allocation_result.nlargest(5, 'allocated_units'))
```

### Size Curve Optimization

```python
class SizeCurveOptimizer:
    """
    Optimize size curves for apparel allocation

    Different stores need different size distributions
    """

    def __init__(self, historical_size_sales):
        """
        Parameters:
        - historical_size_sales: Historical sales by size and store
          columns: ['store_id', 'sku', 'size', 'units_sold']
        """
        self.size_sales = historical_size_sales

    def calculate_store_size_profile(self, store_id, category='tops'):
        """
        Calculate size distribution for a store

        Returns percentage distribution across sizes
        """

        store_sales = self.size_sales[
            (self.size_sales['store_id'] == store_id) &
            (self.size_sales['category'] == category)
        ]

        if len(store_sales) == 0:
            # No history - use national average
            return self._get_national_average_curve(category)

        # Calculate size distribution
        size_totals = store_sales.groupby('size')['units_sold'].sum()
        total_units = size_totals.sum()

        size_distribution = (size_totals / total_units * 100).to_dict()

        return size_distribution

    def _get_national_average_curve(self, category):
        """Default national average size curve"""

        # Typical size distributions (example for women's tops)
        default_curves = {
            'tops': {
                'XS': 8,
                'S': 22,
                'M': 32,
                'L': 24,
                'XL': 10,
                'XXL': 4
            },
            'bottoms': {
                '0': 5,
                '2': 10,
                '4': 15,
                '6': 18,
                '8': 20,
                '10': 15,
                '12': 10,
                '14': 7
            }
        }

        return default_curves.get(category, {})

    def allocate_with_size_curve(self, sku, store_id, total_units, category='tops'):
        """
        Allocate units across sizes based on store's size profile

        Returns unit allocation by size
        """

        # Get store's size curve
        size_curve = self.calculate_store_size_profile(store_id, category)

        # Allocate units
        size_allocation = {}
        remaining_units = total_units

        # Sort sizes by percentage (allocate largest first)
        sorted_sizes = sorted(size_curve.items(), key=lambda x: x[1], reverse=True)

        for size, pct in sorted_sizes:
            allocated = min(
                int(total_units * pct / 100),
                remaining_units
            )
            size_allocation[size] = allocated
            remaining_units -= allocated

        # Distribute any remainder to most popular sizes
        if remaining_units > 0:
            for size, pct in sorted_sizes[:remaining_units]:
                size_allocation[size] += 1

        return size_allocation

    def compare_size_curves(self, store_ids, category='tops'):
        """
        Compare size curves across stores

        Useful for identifying regional differences
        """

        curves = []

        for store_id in store_ids:
            curve = self.calculate_store_size_profile(store_id, category)
            curve['store_id'] = store_id
            curves.append(curve)

        curves_df = pd.DataFrame(curves)

        return curves_df

    def optimize_size_mix_for_pack(self, target_stores, pack_size=12,
                                   category='tops'):
        """
        Optimize pre-pack size mix

        Find size distribution that works well across target stores
        """

        # Calculate average size curve across target stores
        all_curves = []

        for store_id in target_stores:
            curve = self.calculate_store_size_profile(store_id, category)
            all_curves.append(curve)

        # Average the curves
        curves_df = pd.DataFrame(all_curves)
        avg_curve = curves_df.mean()

        # Allocate pack_size units using average curve
        size_allocation = {}
        remaining = pack_size

        sorted_sizes = sorted(avg_curve.items(), key=lambda x: x[1], reverse=True)

        for size, pct in sorted_sizes:
            allocated = min(
                max(1, int(pack_size * pct / 100)),  # At least 1 of each
                remaining
            )
            size_allocation[size] = allocated
            remaining -= allocated

        return size_allocation

# Example
historical_size_sales = pd.DataFrame({
    'store_id': ['S001'] * 6 + ['S002'] * 6,
    'category': ['tops'] * 12,
    'size': ['XS', 'S', 'M', 'L', 'XL', 'XXL'] * 2,
    'units_sold': [80, 220, 350, 240, 100, 40, 50, 180, 380, 280, 90, 20]
})

size_optimizer = SizeCurveOptimizer(historical_size_sales)

# Get size profile for store
size_profile = size_optimizer.calculate_store_size_profile('S001', 'tops')
print("Store S001 size profile:")
for size, pct in size_profile.items():
    print(f"  {size}: {pct:.1f}%")

# Allocate 60 units with size curve
size_allocation = size_optimizer.allocate_with_size_curve('SKU123', 'S001', 60, 'tops')
print(f"\nSize allocation for 60 units:")
print(size_allocation)
```

---

## Pre-Pack vs. Pick-Pack Strategy

**Trade-off Analysis:**

```python
class PrePackAnalyzer:
    """
    Analyze trade-offs between pre-pack and pick-pack allocation
    """

    def compare_strategies(self, num_skus, num_stores, avg_units_per_store):
        """
        Compare operational costs and accuracy

        Pre-pack: Fixed assortments, efficient but less accurate
        Pick-pack: Custom per store, accurate but labor-intensive
        """

        # Pre-pack strategy
        prepack_labor_per_pack = 2  # minutes
        prepack_packs_needed = num_stores
        prepack_labor_minutes = prepack_packs_needed * prepack_labor_per_pack
        prepack_labor_cost = prepack_labor_minutes / 60 * 25  # $25/hour

        prepack_accuracy = 0.75  # 75% match to store needs

        # Pick-pack strategy
        pickpack_labor_per_unit = 0.5  # minutes
        pickpack_total_units = num_stores * avg_units_per_store
        pickpack_labor_minutes = pickpack_total_units * pickpack_labor_per_unit
        pickpack_labor_cost = pickpack_labor_minutes / 60 * 25

        pickpack_accuracy = 0.95  # 95% match to store needs

        # Calculate expected sales impact
        # Better accuracy = higher sell-through, lower markdowns
        avg_selling_price = 50
        total_revenue_potential = pickpack_total_units * avg_selling_price

        prepack_sellthrough = 0.70  # Lower due to mismatches
        pickpack_sellthrough = 0.85  # Higher due to better matching

        prepack_revenue = total_revenue_potential * prepack_sellthrough
        pickpack_revenue = total_revenue_potential * pickpack_sellthrough

        prepack_markdowns = total_revenue_potential * (1 - prepack_sellthrough) * 0.5
        pickpack_markdowns = total_revenue_potential * (1 - pickpack_sellthrough) * 0.5

        return {
            'pre_pack': {
                'labor_cost': prepack_labor_cost,
                'accuracy': prepack_accuracy,
                'expected_revenue': prepack_revenue,
                'markdowns': prepack_markdowns,
                'net_benefit': prepack_revenue - prepack_labor_cost - prepack_markdowns
            },
            'pick_pack': {
                'labor_cost': pickpack_labor_cost,
                'accuracy': pickpack_accuracy,
                'expected_revenue': pickpack_revenue,
                'markdowns': pickpack_markdowns,
                'net_benefit': pickpack_revenue - pickpack_labor_cost - pickpack_markdowns
            }
        }

    def recommend_strategy(self, num_skus, num_stores, product_type):
        """
        Recommend pre-pack or pick-pack

        Factors:
        - Product type (fashion vs. basic)
        - Store count
        - Store diversity
        """

        comparison = self.compare_strategies(num_skus, num_stores, avg_units_per_store=20)

        prepack_net = comparison['pre_pack']['net_benefit']
        pickpack_net = comparison['pick_pack']['net_benefit']

        # Decision rules
        if product_type == 'fashion' and pickpack_net > prepack_net * 1.1:
            return {
                'recommendation': 'Pick-Pack',
                'reason': 'Fashion products benefit from customization',
                'incremental_benefit': pickpack_net - prepack_net
            }
        elif num_stores > 500 and prepack_net > pickpack_net * 0.9:
            return {
                'recommendation': 'Pre-Pack',
                'reason': 'Large store count makes pick-pack prohibitive',
                'cost_savings': prepack_net - pickpack_net
            }
        elif product_type == 'basics':
            return {
                'recommendation': 'Pre-Pack',
                'reason': 'Basic products have consistent demand across stores',
                'efficiency_gain': 'Significant'
            }
        else:
            return {
                'recommendation': 'Pick-Pack',
                'reason': 'Better accuracy justifies additional cost',
                'incremental_benefit': pickpack_net - prepack_net
            }

# Example
analyzer = PrePackAnalyzer()
comparison = analyzer.compare_strategies(num_skus=100, num_stores=200, avg_units_per_store=20)

print("Pre-Pack Strategy:")
print(f"  Labor cost: ${comparison['pre_pack']['labor_cost']:,.0f}")
print(f"  Net benefit: ${comparison['pre_pack']['net_benefit']:,.0f}")

print("\nPick-Pack Strategy:")
print(f"  Labor cost: ${comparison['pick_pack']['labor_cost']:,.0f}")
print(f"  Net benefit: ${comparison['pick_pack']['net_benefit']:,.0f}")

recommendation = analyzer.recommend_strategy(100, 200, 'fashion')
print(f"\nRecommendation: {recommendation['recommendation']}")
print(f"Reason: {recommendation['reason']}")
```

---

## Tools & Libraries

### Python Libraries

**Optimization:**
- `pulp`, `pyomo`: Linear programming for allocation optimization
- `scipy.optimize`: Optimization algorithms
- `ortools`: Google OR-Tools

**Clustering & ML:**
- `scikit-learn`: K-means clustering, classification
- `scipy`: Statistical analysis
- `pandas`: Data manipulation

**Visualization:**
- `matplotlib`, `seaborn`: Plotting
- `plotly`: Interactive visualizations
- `geopandas`: Geographic visualization

### Commercial Software

**Allocation & Planning:**
- **Blue Yonder Luminate**: Retail planning suite
- **o9 Solutions**: Digital planning platform
- **SAP Integrated Business Planning**: Enterprise planning
- **Oracle Retail**: Merchandising and allocation
- **Aptos Retail**: Allocation optimization

**Specialized Tools:**
- **Infor Allocation**: Retail allocation
- **JustEnough**: Assortment and allocation
- **TXT Retail**: Fashion allocation
- **板Assortment Optimization by SAS**: Analytics-driven allocation

---

## Common Challenges & Solutions

### Challenge: New Product Allocation (No History)

**Problem:**
- No sales history for new products
- Difficult to predict demand by store
- Risk of overstock or stockouts

**Solutions:**
- Use analog products (similar style, price, category)
- Pilot launches in test stores
- Start with smaller quantities, fast replenishment
- Use predictive attributes (color, style, price)
- Monitor early sales velocity and adjust
- Cluster stores, test one per cluster

### Challenge: Size/Color Imbalance

**Problem:**
- Some sizes/colors sell out quickly
- Others sit as slow movers
- Markdown risk on slow colors

**Solutions:**
- Local size curve optimization
- Regional color preferences analysis
- Test small quantities of trendy colors
- Core colors in depth, fashion colors shallow
- Inter-store transfers for imbalances
- Dynamic allocation based on early sell-through

### Challenge: Store Capacity Constraints

**Problem:**
- Small stores can't hold full assortment
- Inventory exceeds backroom/floor space
- Congestion impacts customer experience

**Solutions:**
- Curated assortments for small stores
- Grade stores by size, adjust accordingly
- Cross-docking for fast sellers (reduce backroom)
- Frequent smaller deliveries vs. bulk
- Digital endless aisle for out-of-stocks
- Store format-specific assortments

### Challenge: Regional Demand Differences

**Problem:**
- One-size allocation doesn't work
- Climate variations (coats in Florida?)
- Demographic differences
- Cultural preferences

**Solutions:**
- Geographic clustering
- Climate-based allocation rules
- Demographic segmentation
- Local buying authority for some categories
- Regional allocation plans
- Test & learn by region

### Challenge: Overstock & Markdowns

**Problem:**
- Too much inventory allocated
- Poor sell-through
- Heavy markdowns to clear

**Solutions:**
- Conservative initial allocation (chase reorders)
- Monitor sell-through weekly
- Early markdown intervention
- Inter-store transfers
- Allocate to outlet stores
- Improve demand forecasting

---

## Output Format

### Allocation Plan Report

**Executive Summary:**
- Product: Fall 2025 Apparel Collection
- Total units to allocate: 125,000 units across 850 SKUs
- Store network: 185 stores (40 A-grade, 55 B-grade, 90 C-grade)
- Allocation method: Demand-based with store clustering
- Expected sell-through: 78% at full price

**Store Cluster Profiles:**

| Cluster | # Stores | Characteristics | Avg Weekly Sales | Allocation Strategy |
|---------|----------|-----------------|------------------|---------------------|
| 1 - Large Urban High-Income | 25 | Downtown flagship, affluent | $85K | Full assortment, deep inventory |
| 2 - Suburban Mall | 60 | Regional malls, families | $45K | Core assortment, medium depth |
| 3 - Warm Climate | 40 | Southern states, year-round | $38K | Adjusted seasonality, lighter weights |
| 4 - Small Format | 35 | Strip centers, rural | $22K | Curated assortment, shallow depth |
| 5 - Outlet | 25 | Clearance focus | $32K | Overstock recipients |

**Allocation Summary by Grade:**

| Grade | # Stores | Units Allocated | Avg Units/Store | SKU Coverage | Weeks of Supply |
|-------|----------|----------------|-----------------|--------------|-----------------|
| A | 40 | 48,000 (38%) | 1,200 | 100% | 8 weeks |
| B | 55 | 45,000 (36%) | 818 | 85% | 6 weeks |
| C | 90 | 32,000 (26%) | 356 | 60% | 4 weeks |

**Size Curve Allocation (Example: Women's Tops):**

| Store Cluster | XS | S | M | L | XL | XXL | Total/Store |
|---------------|----|----|----|----|----|----|-------------|
| Urban High-Income | 12% | 24% | 30% | 22% | 9% | 3% | 120 units |
| Suburban | 8% | 22% | 32% | 24% | 10% | 4% | 80 units |
| Small Format | 6% | 20% | 34% | 26% | 11% | 3% | 35 units |

**Top 10 Stores - Sample Allocation:**

| Store | Grade | Cluster | Total Units | Top SKU | Units | Expected Sales |
|-------|-------|---------|-------------|---------|-------|----------------|
| S001 - NYC Flagship | A | Urban | 1,450 | Jacket-001 | 85 | $124K |
| S005 - LA Westfield | A | Urban | 1,320 | Dress-042 | 78 | $108K |
| S012 - Chicago | A | Urban | 1,280 | Top-015 | 72 | $98K |
| S023 - Boston | B | Suburban | 950 | Sweater-008 | 58 | $65K |
| S034 - Atlanta | B | Warm | 880 | Shorts-011 | 52 | $58K |

**Financial Impact:**

| Metric | Value |
|--------|-------|
| Total units allocated | 125,000 |
| Retail value at full price | $6,250,000 |
| Expected full-price sell-through | 78% |
| Expected full-price revenue | $4,875,000 |
| Expected markdown revenue | $687,500 |
| Total expected revenue | $5,562,500 |
| Expected markdown rate | 22% |
| Target markdown rate | <25% |

**Risk Assessment:**

1. **High-Risk SKUs** (low forecast confidence)
   - 45 fashion-forward SKUs
   - Allocated conservatively (60% of demand)
   - Plan: Monitor first 2 weeks, chase if needed

2. **Regional Risks**
   - Northeast: Early cold weather risk
   - Mitigation: Hold 10% buffer for rapid reallocation

3. **New Product Risk**
   - 120 SKUs are new styles
   - Mitigation: Test stores, analog-based allocation

**Action Plan:**

| Week | Action | Responsibility |
|------|--------|----------------|
| Week 1 | Finalize allocation plan, communicate to stores | Allocation team |
| Week 2 | DC receives inventory, pre-pack/pick operations | DC operations |
| Week 3 | Ship to stores, begin in-transit tracking | Logistics |
| Week 4 | Store delivery, merchandise sets | Store ops |
| Week 5 | Monitor sell-through, identify fast/slow movers | Planning |
| Week 6 | Execute reallocation for imbalances | Allocation team |

---

## Questions to Ask

If you need more context:
1. What product categories are you allocating?
2. How many stores in your network?
3. Do you have store clusters/grades defined?
4. Is this new product or replenishment?
5. What's the historical sell-through rate?
6. What's your target markdown rate?
7. Do you use pre-packs or pick-and-pack?
8. What allocation system/process is currently used?
9. What's the biggest challenge? (markdowns, stockouts, complexity)

---

## Related Skills

- **retail-replenishment**: Ongoing replenishment after initial allocation
- **markdown-optimization**: Markdown strategy for slow movers
- **demand-forecasting**: Demand forecasts for allocation planning
- **seasonal-planning**: Seasonal buy planning
- **inventory-optimization**: Safety stock and service levels
- **warehouse-slotting-optimization**: DC slotting for pick efficiency
- **supply-chain-analytics**: Performance metrics and reporting
