---
name: trim-loss-minimization
description: When the user wants to minimize material waste, reduce trim loss, or optimize material utilization in cutting operations. Also use when the user mentions "waste minimization," "scrap reduction," "material efficiency," "trim optimization," "yield maximization," "off-cut management," or "residual material utilization." For specific cutting problems, see 1d-cutting-stock, 2d-cutting-stock, or nesting-optimization.
---

# Trim Loss Minimization

You are an expert in trim loss minimization and material waste reduction for cutting operations. Your goal is to help manufacturers minimize material waste, reduce costs, and improve sustainability by optimizing cutting patterns, managing residual materials, and implementing best practices for material utilization.

## Initial Assessment

Before addressing trim loss problems, understand:

1. **Material and Process Characteristics**
   - What materials? (steel, wood, glass, fabric, plastic, paper)
   - Cutting process? (saw, laser, waterjet, shear, die cutting)
   - Material dimensions and formats?
   - Material cost per unit ($/kg, $/m², $/piece)?
   - Are there different material grades or qualities?

2. **Current Waste Situation**
   - Current trim loss percentage?
   - Where is waste generated? (ends, edges, between parts, defects)
   - What happens to scrap? (recycled, sold, discarded)
   - Scrap recovery value?
   - Cost of waste disposal?

3. **Production Requirements**
   - Production volume (units per day/week/month)?
   - Item mix (how many different parts/sizes)?
   - Demand variability (stable or fluctuating)?
   - Quality tolerances?
   - Customer-specific requirements?

4. **Existing Constraints**
   - Minimum usable piece size?
   - Standard stock sizes available?
   - Can you change stock sizes or suppliers?
   - Equipment limitations?
   - Setup time/cost considerations?

5. **Business Objectives**
   - Primary goal: minimize waste %, minimize cost, or maximize throughput?
   - Acceptable trade-offs (cost vs. waste vs. complexity)?
   - Sustainability/environmental goals?
   - Target waste reduction?

---

## Trim Loss Framework

### Understanding Trim Loss

**Trim Loss Definition:**
Trim loss is the percentage of raw material that becomes waste after cutting operations.

**Formula:**
```
Trim Loss % = (Total Material - Usable Material) / Total Material × 100
```

Or:
```
Trim Loss % = (1 - Utilization %) × 100
```

**Components of Trim Loss:**

1. **Edge Trim**
   - Material trimmed from sheet edges
   - Often due to material irregularities
   - Standard practice in many industries

2. **Inter-Part Waste**
   - Material between cut parts
   - Saw kerf (material removed by cutting tool)
   - Minimum spacing requirements

3. **End Trim**
   - Material at ends of stocks/sheets
   - Too small for useful parts
   - Accumulates with each stock used

4. **Pattern Inefficiency**
   - Poor nesting or pattern design
   - Suboptimal item arrangement
   - Irregular part shapes

5. **Quality Defects**
   - Material defects requiring cutting around
   - Quality failures requiring rework
   - Damaged material

6. **Residuals**
   - Leftover pieces too small for current orders
   - May be usable for future orders
   - Storage and tracking overhead

---

## Trim Loss Measurement and Analysis

### Comprehensive Measurement System

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class TrimLossAnalyzer:
    """
    Comprehensive Trim Loss Analysis Tool

    Tracks, measures, and analyzes trim loss across operations
    """

    def __init__(self):
        self.cutting_records = []
        self.material_specs = {}

    def add_material_spec(self, material_id, cost_per_unit, unit='m2', scrap_value=0):
        """
        Add material specification

        Parameters:
        - material_id: material identifier
        - cost_per_unit: cost per unit area/length/piece
        - unit: measurement unit
        - scrap_value: recovery value of scrap
        """
        self.material_specs[material_id] = {
            'cost_per_unit': cost_per_unit,
            'unit': unit,
            'scrap_value': scrap_value
        }

    def record_cutting_operation(self, material_id, total_material,
                                 usable_material, waste_material,
                                 waste_breakdown=None, date=None):
        """
        Record a cutting operation

        Parameters:
        - material_id: material type
        - total_material: total material used
        - usable_material: material in final parts
        - waste_material: total waste generated
        - waste_breakdown: dict with waste categories
        - date: operation date
        """

        trim_loss_pct = (waste_material / total_material * 100) if total_material > 0 else 0
        utilization_pct = (usable_material / total_material * 100) if total_material > 0 else 0

        record = {
            'material_id': material_id,
            'date': date or pd.Timestamp.now(),
            'total_material': total_material,
            'usable_material': usable_material,
            'waste_material': waste_material,
            'trim_loss_pct': trim_loss_pct,
            'utilization_pct': utilization_pct,
            'waste_breakdown': waste_breakdown or {}
        }

        self.cutting_records.append(record)

    def calculate_financial_impact(self, material_id=None, time_period=None):
        """
        Calculate financial impact of trim loss

        Returns cost analysis and potential savings
        """

        # Filter records
        records = self.cutting_records

        if material_id:
            records = [r for r in records if r['material_id'] == material_id]

        if time_period:
            # time_period should be tuple (start_date, end_date)
            start, end = time_period
            records = [r for r in records if start <= r['date'] <= end]

        if not records:
            return None

        # Aggregate data
        total_material_used = sum(r['total_material'] for r in records)
        total_waste = sum(r['waste_material'] for r in records)
        total_usable = sum(r['usable_material'] for r in records)

        avg_trim_loss = (total_waste / total_material_used * 100) if total_material_used > 0 else 0

        # Calculate costs
        material_costs = {}
        waste_costs = {}
        scrap_value = {}

        for material_id in set(r['material_id'] for r in records):
            if material_id not in self.material_specs:
                continue

            spec = self.material_specs[material_id]

            material_records = [r for r in records if r['material_id'] == material_id]
            mat_total = sum(r['total_material'] for r in material_records)
            mat_waste = sum(r['waste_material'] for r in material_records)

            material_costs[material_id] = mat_total * spec['cost_per_unit']
            waste_costs[material_id] = mat_waste * spec['cost_per_unit']
            scrap_value[material_id] = mat_waste * spec['scrap_value']

        total_material_cost = sum(material_costs.values())
        total_waste_cost = sum(waste_costs.values())
        total_scrap_value = sum(scrap_value.values())
        net_waste_cost = total_waste_cost - total_scrap_value

        # Calculate potential savings scenarios
        scenarios = {}

        for reduction_pct in [5, 10, 15, 20, 25]:
            reduced_waste = total_waste * (1 - reduction_pct/100)
            reduced_waste_cost = (reduced_waste / total_material_used) * total_material_cost
            savings = total_waste_cost - reduced_waste_cost

            scenarios[f'{reduction_pct}% reduction'] = {
                'new_waste': reduced_waste,
                'new_trim_loss_pct': (reduced_waste / total_material_used * 100),
                'annual_savings': savings,
                'payback_potential': savings
            }

        return {
            'total_material_used': total_material_used,
            'total_waste': total_waste,
            'total_usable': total_usable,
            'avg_trim_loss_pct': avg_trim_loss,
            'total_material_cost': total_material_cost,
            'total_waste_cost': total_waste_cost,
            'total_scrap_value': total_scrap_value,
            'net_waste_cost': net_waste_cost,
            'waste_cost_percentage': (net_waste_cost / total_material_cost * 100) if total_material_cost > 0 else 0,
            'improvement_scenarios': scenarios
        }

    def analyze_waste_breakdown(self, material_id=None):
        """
        Analyze waste by category

        Returns breakdown of waste sources
        """

        records = self.cutting_records
        if material_id:
            records = [r for r in records if r['material_id'] == material_id]

        # Aggregate waste by category
        waste_categories = {}

        for record in records:
            if 'waste_breakdown' in record and record['waste_breakdown']:
                for category, amount in record['waste_breakdown'].items():
                    waste_categories[category] = waste_categories.get(category, 0) + amount

        total_waste = sum(waste_categories.values())

        if total_waste > 0:
            waste_breakdown = {
                cat: {
                    'amount': amt,
                    'percentage': (amt / total_waste * 100)
                }
                for cat, amt in waste_categories.items()
            }
        else:
            waste_breakdown = {}

        return {
            'total_waste': total_waste,
            'waste_by_category': waste_breakdown
        }

    def generate_pareto_analysis(self, material_id=None):
        """
        Generate Pareto analysis of waste sources

        Returns top waste contributors (80/20 analysis)
        """

        breakdown = self.analyze_waste_breakdown(material_id)

        if not breakdown['waste_by_category']:
            return None

        # Sort by amount
        sorted_categories = sorted(
            breakdown['waste_by_category'].items(),
            key=lambda x: x[1]['amount'],
            reverse=True
        )

        # Calculate cumulative percentages
        cumulative_pct = 0
        pareto_data = []

        for category, data in sorted_categories:
            cumulative_pct += data['percentage']
            pareto_data.append({
                'category': category,
                'amount': data['amount'],
                'percentage': data['percentage'],
                'cumulative_pct': cumulative_pct
            })

        return {
            'pareto_data': pareto_data,
            'top_80_pct_contributors': [
                item for item in pareto_data
                if item['cumulative_pct'] <= 80
            ]
        }

    def plot_trim_loss_trends(self, material_id=None, save_path=None):
        """
        Plot trim loss trends over time
        """

        records = self.cutting_records
        if material_id:
            records = [r for r in records if r['material_id'] == material_id]

        if not records:
            print("No data to plot")
            return

        df = pd.DataFrame(records)
        df = df.sort_values('date')

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

        # Plot 1: Trim loss over time
        ax1.plot(df['date'], df['trim_loss_pct'], marker='o', linewidth=2)
        ax1.axhline(y=df['trim_loss_pct'].mean(), color='r',
                   linestyle='--', label=f'Average: {df["trim_loss_pct"].mean():.2f}%')
        ax1.set_xlabel('Date', fontsize=12)
        ax1.set_ylabel('Trim Loss %', fontsize=12)
        ax1.set_title('Trim Loss Trend Over Time', fontsize=14, fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # Plot 2: Cumulative waste
        df['cumulative_waste'] = df['waste_material'].cumsum()
        df['cumulative_material'] = df['total_material'].cumsum()

        ax2.fill_between(df['date'], 0, df['cumulative_waste'],
                        alpha=0.3, color='red', label='Cumulative Waste')
        ax2.plot(df['date'], df['cumulative_material'],
                color='blue', linewidth=2, label='Cumulative Material Used')
        ax2.set_xlabel('Date', fontsize=12)
        ax2.set_ylabel('Material (units)', fontsize=12)
        ax2.set_title('Cumulative Material Usage and Waste', fontsize=14, fontweight='bold')
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')

        plt.show()

    def plot_pareto_chart(self, material_id=None, save_path=None):
        """
        Plot Pareto chart of waste categories
        """

        pareto = self.generate_pareto_analysis(material_id)

        if not pareto:
            print("No data for Pareto analysis")
            return

        data = pareto['pareto_data']
        categories = [d['category'] for d in data]
        amounts = [d['amount'] for d in data]
        cumulative = [d['cumulative_pct'] for d in data]

        fig, ax1 = plt.subplots(figsize=(12, 6))

        # Bar chart
        x_pos = np.arange(len(categories))
        ax1.bar(x_pos, amounts, color='steelblue', alpha=0.7)
        ax1.set_xlabel('Waste Category', fontsize=12)
        ax1.set_ylabel('Waste Amount', fontsize=12, color='steelblue')
        ax1.set_xticks(x_pos)
        ax1.set_xticklabels(categories, rotation=45, ha='right')
        ax1.tick_params(axis='y', labelcolor='steelblue')

        # Line chart for cumulative
        ax2 = ax1.twinx()
        ax2.plot(x_pos, cumulative, color='red', marker='o',
                linewidth=2, markersize=8)
        ax2.axhline(y=80, color='red', linestyle='--',
                   alpha=0.5, label='80% Line')
        ax2.set_ylabel('Cumulative %', fontsize=12, color='red')
        ax2.set_ylim(0, 105)
        ax2.tick_params(axis='y', labelcolor='red')
        ax2.legend()

        plt.title('Pareto Analysis of Waste Sources',
                 fontsize=14, fontweight='bold')
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')

        plt.show()


# Example usage
def example_trim_loss_analysis():
    """Example: Analyze trim loss data"""

    analyzer = TrimLossAnalyzer()

    # Add material specifications
    analyzer.add_material_spec(
        'Steel_Sheet',
        cost_per_unit=15.50,  # $/m²
        unit='m2',
        scrap_value=2.00  # $/m² scrap value
    )

    # Simulate cutting records
    import random
    from datetime import datetime, timedelta

    base_date = datetime(2024, 1, 1)

    for i in range(50):
        date = base_date + timedelta(days=i)
        total = 100 + random.uniform(-10, 10)
        trim_loss = 15 + random.uniform(-5, 5)  # Average 15% trim loss
        waste = total * (trim_loss / 100)
        usable = total - waste

        analyzer.record_cutting_operation(
            material_id='Steel_Sheet',
            total_material=total,
            usable_material=usable,
            waste_material=waste,
            waste_breakdown={
                'edge_trim': waste * 0.3,
                'inter_part': waste * 0.4,
                'end_trim': waste * 0.2,
                'defects': waste * 0.1
            },
            date=date
        )

    # Financial analysis
    print("FINANCIAL IMPACT ANALYSIS")
    print("=" * 70)

    impact = analyzer.calculate_financial_impact('Steel_Sheet')

    print(f"Total Material Used: {impact['total_material_used']:.2f} m²")
    print(f"Total Waste: {impact['total_waste']:.2f} m² ({impact['avg_trim_loss_pct']:.2f}%)")
    print(f"Total Material Cost: ${impact['total_material_cost']:.2f}")
    print(f"Total Waste Cost: ${impact['total_waste_cost']:.2f}")
    print(f"Scrap Recovery Value: ${impact['total_scrap_value']:.2f}")
    print(f"Net Waste Cost: ${impact['net_waste_cost']:.2f}")
    print(f"Waste as % of Material Cost: {impact['waste_cost_percentage']:.2f}%")
    print()

    print("IMPROVEMENT SCENARIOS:")
    print("-" * 70)
    for scenario, data in impact['improvement_scenarios'].items():
        print(f"{scenario}:")
        print(f"  New Trim Loss: {data['new_trim_loss_pct']:.2f}%")
        print(f"  Annual Savings: ${data['annual_savings']:.2f}")
        print()

    # Pareto analysis
    print("\nPARETO ANALYSIS")
    print("=" * 70)

    pareto = analyzer.generate_pareto_analysis('Steel_Sheet')

    print("Top 80% Contributors:")
    for item in pareto['top_80_pct_contributors']:
        print(f"  {item['category']}: {item['amount']:.2f} ({item['percentage']:.1f}%)")

    # Plots
    analyzer.plot_trim_loss_trends('Steel_Sheet')
    analyzer.plot_pareto_chart('Steel_Sheet')

    return analyzer
```

---

## Trim Loss Minimization Strategies

### Strategy 1: Cutting Pattern Optimization

```python
def optimize_cutting_patterns(items, stock_length, current_trim_loss_pct,
                              target_trim_loss_pct):
    """
    Optimize cutting patterns to reduce trim loss

    Compares current performance to optimized solution
    """

    from skills.one_d_cutting_stock import ColumnGenerationCuttingStock

    # Current situation (using simple heuristic)
    current_stocks = estimate_stocks_needed(items, stock_length,
                                            trim_loss_pct=current_trim_loss_pct)

    # Optimized solution (using column generation)
    solver = ColumnGenerationCuttingStock(stock_length, items)
    optimal_solution = solver.solve()

    # Compare
    comparison = {
        'current': {
            'stocks': current_stocks,
            'trim_loss_pct': current_trim_loss_pct,
            'waste': current_stocks * stock_length * (current_trim_loss_pct / 100)
        },
        'optimized': {
            'stocks': optimal_solution['num_stocks'],
            'trim_loss_pct': 100 - optimal_solution['utilization'],
            'waste': optimal_solution['total_waste']
        }
    }

    # Improvement
    stocks_saved = current_stocks - optimal_solution['num_stocks']
    trim_loss_reduction = current_trim_loss_pct - (100 - optimal_solution['utilization'])

    comparison['improvement'] = {
        'stocks_saved': stocks_saved,
        'stocks_saved_pct': (stocks_saved / current_stocks * 100) if current_stocks > 0 else 0,
        'trim_loss_reduction': trim_loss_reduction,
        'achieved_target': (100 - optimal_solution['utilization']) <= target_trim_loss_pct
    }

    return comparison

def estimate_stocks_needed(items, stock_length, trim_loss_pct):
    """Estimate stocks needed given current trim loss"""
    total_length_needed = sum(length * qty for length, qty, _ in items)
    effective_length = stock_length * (1 - trim_loss_pct / 100)
    return int(np.ceil(total_length_needed / effective_length))
```

### Strategy 2: Residual Material Management

```python
class ResidualMaterialManager:
    """
    Manage and utilize residual/leftover materials

    Tracks inventory of residuals and matches them to new orders
    """

    def __init__(self):
        self.residuals = []  # List of available residual pieces

    def add_residual(self, length, width, material_id, location=None):
        """Add residual piece to inventory"""
        self.residuals.append({
            'length': length,
            'width': width,
            'material_id': material_id,
            'area': length * width,
            'location': location,
            'date_added': pd.Timestamp.now()
        })

    def find_matching_residuals(self, required_length, required_width,
                                material_id, tolerance=0):
        """
        Find residuals that can satisfy requirement

        Parameters:
        - required_length, required_width: minimum dimensions needed
        - material_id: material type
        - tolerance: acceptable size tolerance

        Returns: list of matching residuals
        """

        matches = []

        for idx, residual in enumerate(self.residuals):
            if residual['material_id'] != material_id:
                continue

            # Check if residual is large enough
            if (residual['length'] >= required_length - tolerance and
                residual['width'] >= required_width - tolerance):
                matches.append({
                    'index': idx,
                    'residual': residual,
                    'excess_length': residual['length'] - required_length,
                    'excess_width': residual['width'] - required_width,
                    'excess_area': (residual['length'] - required_length) * \
                                   (residual['width'] - required_width)
                })

        # Sort by least excess (best fit)
        matches.sort(key=lambda x: x['excess_area'])

        return matches

    def allocate_residual(self, residual_index, amount_used):
        """
        Allocate residual to an order

        If fully used, remove from inventory
        If partially used, update dimensions
        """

        if residual_index >= len(self.residuals):
            return False

        residual = self.residuals[residual_index]

        # For simplicity, assume full usage here
        # In practice, you'd update dimensions based on how it was cut

        del self.residuals[residual_index]

        return True

    def calculate_residual_value(self, material_specs):
        """
        Calculate total value of residual inventory

        Parameters:
        - material_specs: dict with material costs

        Returns: total value
        """

        total_value = 0

        for residual in self.residuals:
            material_id = residual['material_id']
            if material_id in material_specs:
                cost_per_unit = material_specs[material_id]['cost_per_unit']
                total_value += residual['area'] * cost_per_unit

        return total_value

    def identify_slow_moving_residuals(self, age_threshold_days=90):
        """
        Identify residuals that have been in inventory too long

        These may need special action (discount, scrap, etc.)
        """

        now = pd.Timestamp.now()
        slow_moving = []

        for residual in self.residuals:
            age_days = (now - residual['date_added']).days

            if age_days > age_threshold_days:
                slow_moving.append({
                    'residual': residual,
                    'age_days': age_days
                })

        return slow_moving


# Example usage
def example_residual_management():
    """Example: Managing residual materials"""

    manager = ResidualMaterialManager()

    # Add some residuals
    manager.add_residual(1200, 800, 'Steel_Sheet', 'Rack_A1')
    manager.add_residual(900, 600, 'Steel_Sheet', 'Rack_A2')
    manager.add_residual(1500, 1000, 'Steel_Sheet', 'Rack_A3')

    # Need to cut a part 1000x700
    matches = manager.find_matching_residuals(1000, 700, 'Steel_Sheet')

    print("Matching residuals for 1000x700 part:")
    for match in matches:
        res = match['residual']
        print(f"  {res['length']}x{res['width']} at {res['location']} "
              f"(excess: {match['excess_area']} mm²)")

    if matches:
        # Use best match
        print(f"\nUsing residual from {matches[0]['residual']['location']}")
        manager.allocate_residual(matches[0]['index'], (1000, 700))

    return manager
```

### Strategy 3: Multi-Objective Optimization

```python
def multi_objective_trim_loss_optimization(items, stock_specs, weights):
    """
    Multi-objective optimization balancing:
    - Material cost minimization
    - Trim loss minimization
    - Cutting complexity minimization

    Parameters:
    - items: list of items to cut
    - stock_specs: available stock specifications
    - weights: dict with objective weights

    Returns: Pareto optimal solutions
    """

    from pulp import *

    # Define objectives
    objectives = {
        'material_cost': 0,
        'trim_loss': 0,
        'complexity': 0
    }

    # Weighted sum approach
    # In practice, use NSGA-II or other multi-objective algorithms

    total_weight = sum(weights.values())
    normalized_weights = {k: v/total_weight for k, v in weights.items()}

    # Solve for different weight combinations
    solutions = []

    # This is simplified - full implementation would explore
    # multiple weight combinations and return Pareto front

    return solutions
```

---

## Best Practices for Trim Loss Minimization

### 1. Material Selection

- **Standardize Stock Sizes:** Use fewer standard sizes
- **Match Stock to Demand:** Choose stock sizes that align with typical orders
- **Negotiate Custom Sizes:** Work with suppliers for optimal stock dimensions

### 2. Order Consolidation

- **Batch Similar Orders:** Combine orders for better nesting
- **Optimize Order Quantities:** Consider material efficiency when quoting
- **Plan Ahead:** Look ahead at upcoming orders for better planning

### 3. Process Improvements

- **Precision Cutting:** Reduce kerf width with better equipment
- **Quality Control:** Minimize defects that cause scrap
- **Operator Training:** Ensure operators understand waste impact
- **Maintenance:** Keep equipment calibrated and maintained

### 4. Technology Investment

- **Optimization Software:** Implement cutting optimization software
- **Automated Nesting:** Use automatic nesting systems
- **Real-time Tracking:** Monitor trim loss in real-time
- **Data Analytics:** Analyze patterns to identify improvements

### 5. Organizational Changes

- **Incentive Programs:** Reward waste reduction
- **Continuous Improvement:** Regular review and improvement cycles
- **Cross-functional Teams:** Involve purchasing, production, sales
- **Supplier Partnerships:** Work with suppliers on waste reduction

---

## Industry Benchmarks

### Typical Trim Loss by Industry

| Industry | Material | Typical Trim Loss | Best-in-Class |
|----------|----------|-------------------|---------------|
| Steel Fabrication | Sheet Metal | 10-20% | 5-8% |
| Wood Products | Lumber | 15-25% | 8-12% |
| Glass Cutting | Flat Glass | 12-18% | 6-10% |
| Textile/Apparel | Fabric | 10-15% | 5-8% |
| Paper Converting | Paper Rolls | 3-8% | 1-3% |
| Plastic Extrusion | Plastic Sheet | 8-15% | 4-7% |

---

## ROI Calculation for Trim Loss Reduction

```python
def calculate_trim_loss_reduction_roi(current_annual_material_cost,
                                     current_trim_loss_pct,
                                     target_trim_loss_pct,
                                     implementation_cost,
                                     scrap_recovery_rate=0):
    """
    Calculate ROI for trim loss reduction initiative

    Returns payback period and annual savings
    """

    # Current waste cost
    current_waste_cost = current_annual_material_cost * (current_trim_loss_pct / 100)

    # Target waste cost
    target_waste_cost = current_annual_material_cost * (target_trim_loss_pct / 100)

    # Annual savings
    gross_savings = current_waste_cost - target_waste_cost
    scrap_value_loss = gross_savings * scrap_recovery_rate  # Lost scrap sales
    net_annual_savings = gross_savings - scrap_value_loss

    # ROI metrics
    payback_period = implementation_cost / net_annual_savings if net_annual_savings > 0 else float('inf')
    roi_year1 = ((net_annual_savings - implementation_cost) / implementation_cost * 100) if implementation_cost > 0 else 0
    roi_year3 = ((net_annual_savings * 3 - implementation_cost) / implementation_cost * 100) if implementation_cost > 0 else 0

    return {
        'current_waste_cost': current_waste_cost,
        'target_waste_cost': target_waste_cost,
        'annual_savings': net_annual_savings,
        'implementation_cost': implementation_cost,
        'payback_period_years': payback_period,
        'roi_year_1_pct': roi_year1,
        'roi_year_3_pct': roi_year3,
        'npv_3_year': net_annual_savings * 3 - implementation_cost  # Simplified NPV
    }


# Example
def example_roi_calculation():
    """Example: Calculate ROI for trim loss reduction project"""

    roi = calculate_trim_loss_reduction_roi(
        current_annual_material_cost=1_000_000,  # $1M per year
        current_trim_loss_pct=15,  # Current: 15% waste
        target_trim_loss_pct=8,   # Target: 8% waste
        implementation_cost=50_000,  # $50K for optimization software + training
        scrap_recovery_rate=0.15  # Recover 15% of waste cost through scrap sales
    )

    print("TRIM LOSS REDUCTION ROI ANALYSIS")
    print("=" * 70)
    print(f"Current Annual Waste Cost: ${roi['current_waste_cost']:,.2f}")
    print(f"Target Annual Waste Cost: ${roi['target_waste_cost']:,.2f}")
    print(f"Annual Savings: ${roi['annual_savings']:,.2f}")
    print(f"Implementation Cost: ${roi['implementation_cost']:,.2f}")
    print(f"Payback Period: {roi['payback_period_years']:.1f} years")
    print(f"ROI Year 1: {roi['roi_year_1_pct']:.1f}%")
    print(f"ROI Year 3: {roi['roi_year_3_pct']:.1f}%")
    print(f"3-Year NPV: ${roi['npv_3_year']:,.2f}")

    return roi
```

---

## Output Format

### Trim Loss Analysis Report

**Executive Summary:**
- Current Trim Loss: 15.2%
- Industry Benchmark: 8-12%
- Gap: 3.2-7.2 percentage points
- Annual Material Cost: $1,250,000
- Annual Waste Cost: $190,000
- Improvement Opportunity: $40,000-$90,000/year

**Waste Breakdown (Pareto Analysis):**
1. Inter-part waste: 45% ($85,500)
2. Edge trim: 28% ($53,200)
3. End trim: 18% ($34,200)
4. Quality defects: 9% ($17,100)

**Top 3 Improvement Opportunities:**
1. Implement cutting optimization software → 5% reduction → $62,500/year
2. Residual material management system → 2% reduction → $25,000/year
3. Operator training program → 1% reduction → $12,500/year

**Recommended Action Plan:**
- Phase 1 (0-3 months): Implement software, train operators
- Phase 2 (3-6 months): Launch residual management
- Phase 3 (6-12 months): Continuous improvement program
- Total Investment: $75,000
- Expected Annual Savings: $100,000
- Payback: 9 months

---

## Questions to Ask

1. What is your current trim loss percentage?
2. What materials do you cut and what are their costs?
3. How do you currently track waste?
4. What happens to scrap material?
5. What cutting processes do you use?
6. How many different part types do you produce?
7. What is your annual material spend?
8. What waste reduction targets do you have?
9. Do you use cutting optimization software?
10. How do you manage leftover materials?

---

## Related Skills

- **1d-cutting-stock**: For linear cutting optimization
- **2d-cutting-stock**: For sheet cutting optimization
- **nesting-optimization**: For irregular shape nesting
- **guillotine-cutting**: For guillotine cutting problems
- **lean-manufacturing**: For waste reduction methodology
- **process-optimization**: For overall process improvement
- **supply-chain-analytics**: For data analysis and tracking
