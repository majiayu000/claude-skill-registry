---
name: economic-order-quantity
description: When the user wants to calculate optimal order quantities, minimize total inventory costs using EOQ models, or determine the economic lot size. Also use when the user mentions "EOQ," "Wilson formula," "economic lot size," "order quantity optimization," "production batch size," "quantity discounts," "EPQ" (Economic Production Quantity), "backorder models," or "reorder point calculations." For multi-echelon systems, see multi-echelon-inventory. For stochastic models, see stochastic-inventory-models.
---

# Economic Order Quantity (EOQ)

You are an expert in Economic Order Quantity (EOQ) models and inventory lot-sizing optimization. Your goal is to help determine optimal order or production quantities that minimize total inventory costs by balancing ordering/setup costs with holding costs.

## Initial Assessment

Before calculating EOQ, understand:

1. **Business Context**
   - What type of inventory? (raw materials, finished goods, components)
   - Current ordering practices? (fixed quantity, min/max, ad-hoc)
   - Primary cost concerns? (ordering, holding, stockouts)
   - Production or purchasing environment?

2. **Demand Characteristics**
   - Annual demand volume (units/year)?
   - Demand pattern? (constant, seasonal, deterministic vs. stochastic)
   - Demand rate stability?
   - Planning horizon?

3. **Cost Parameters**
   - Unit cost of item ($)?
   - Ordering cost per order ($) or setup cost per production run?
   - Inventory carrying/holding cost rate (% per year)?
   - Stockout or backorder costs (if applicable)?

4. **Operational Constraints**
   - Supplier minimum order quantities (MOQs)?
   - Quantity discounts available?
   - Storage capacity limitations?
   - Production rate constraints?
   - Lead time from supplier?

---

## EOQ Model Fundamentals

### Classic EOQ Model

**Assumptions:**
- Demand is constant and known with certainty
- Lead time is constant and known
- No stockouts allowed (infinite stockout cost)
- Order arrives all at once (instantaneous replenishment)
- No quantity discounts
- Holding and ordering costs are known and constant

**Decision:** What order quantity Q minimizes total cost?

### Total Cost Function

```
TC(Q) = Purchase Cost + Ordering Cost + Holding Cost

TC(Q) = DC + (D/Q)S + (Q/2)H

Where:
  D = Annual demand (units/year)
  C = Unit cost ($/unit)
  S = Ordering cost per order ($)
  H = Holding cost per unit per year ($/unit/year)
  Q = Order quantity (units)

  D/Q = Number of orders per year
  Q/2 = Average inventory level (assuming uniform demand)
```

### EOQ Formula Derivation

**Objective:** Minimize TC(Q) with respect to Q

Taking the derivative and setting to zero:

```
dTC/dQ = -(DS)/Q² + H/2 = 0

Solving for Q:
-(DS)/Q² + H/2 = 0
H/2 = DS/Q²
Q² = 2DS/H

EOQ = √(2DS/H)
```

**Optimal Order Frequency:**
```
n* = D/EOQ = Number of orders per year

Cycle Time = 1/n* = EOQ/D years
```

**Minimum Total Cost:**
```
TC* = DC + √(2DSH)
```

---

## Python Implementation: Classic EOQ

### Basic EOQ Calculator

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple

class EOQModel:
    """
    Classic Economic Order Quantity Model

    Determines optimal order quantity to minimize total inventory costs
    """

    def __init__(self, annual_demand: float, unit_cost: float,
                 ordering_cost: float, holding_cost_rate: float):
        """
        Initialize EOQ model

        Parameters:
        -----------
        annual_demand : float
            Annual demand in units
        unit_cost : float
            Cost per unit ($)
        ordering_cost : float
            Fixed cost per order ($)
        holding_cost_rate : float
            Annual holding cost as fraction of unit cost (e.g., 0.25 = 25%)
        """
        self.D = annual_demand
        self.C = unit_cost
        self.S = ordering_cost
        self.r = holding_cost_rate
        self.H = unit_cost * holding_cost_rate

    def calculate_eoq(self) -> Dict:
        """Calculate Economic Order Quantity and associated metrics"""

        # EOQ formula
        eoq = np.sqrt((2 * self.D * self.S) / self.H)

        # Number of orders per year
        orders_per_year = self.D / eoq

        # Cycle time (time between orders)
        cycle_time_days = 365 / orders_per_year

        # Cost components
        purchase_cost = self.D * self.C
        ordering_cost_total = (self.D / eoq) * self.S
        holding_cost_total = (eoq / 2) * self.H
        total_cost = purchase_cost + ordering_cost_total + holding_cost_total

        # Total relevant cost (excluding purchase cost which is constant)
        relevant_cost = ordering_cost_total + holding_cost_total

        # Average inventory
        avg_inventory = eoq / 2
        avg_inventory_value = avg_inventory * self.C

        return {
            'eoq': round(eoq, 2),
            'orders_per_year': round(orders_per_year, 2),
            'cycle_time_days': round(cycle_time_days, 2),
            'total_annual_cost': round(total_cost, 2),
            'purchase_cost': round(purchase_cost, 2),
            'ordering_cost': round(ordering_cost_total, 2),
            'holding_cost': round(holding_cost_total, 2),
            'relevant_cost': round(relevant_cost, 2),
            'avg_inventory': round(avg_inventory, 2),
            'avg_inventory_value': round(avg_inventory_value, 2),
            'max_inventory': round(eoq, 2)
        }

    def sensitivity_analysis(self, param_name: str,
                           variation_range: Tuple[float, float],
                           num_points: int = 20) -> pd.DataFrame:
        """
        Perform sensitivity analysis on a parameter

        Parameters:
        -----------
        param_name : str
            Parameter to vary: 'demand', 'ordering_cost', 'holding_rate', 'unit_cost'
        variation_range : tuple
            (min_multiplier, max_multiplier) e.g., (0.5, 2.0) for 50% to 200%
        num_points : int
            Number of points to evaluate
        """

        multipliers = np.linspace(variation_range[0], variation_range[1], num_points)
        results = []

        # Store original values
        orig_D, orig_S, orig_r, orig_C = self.D, self.S, self.r, self.C

        for mult in multipliers:
            # Vary parameter
            if param_name == 'demand':
                self.D = orig_D * mult
            elif param_name == 'ordering_cost':
                self.S = orig_S * mult
            elif param_name == 'holding_rate':
                self.r = orig_r * mult
                self.H = self.C * self.r
            elif param_name == 'unit_cost':
                self.C = orig_C * mult
                self.H = self.C * self.r

            # Calculate EOQ at this parameter value
            metrics = self.calculate_eoq()

            results.append({
                'multiplier': mult,
                f'{param_name}_value': getattr(self, param_name.split('_')[0][0].upper()),
                'eoq': metrics['eoq'],
                'total_cost': metrics['total_annual_cost'],
                'relevant_cost': metrics['relevant_cost'],
                'orders_per_year': metrics['orders_per_year']
            })

        # Restore original values
        self.D, self.S, self.r, self.C = orig_D, orig_S, orig_r, orig_C
        self.H = self.C * self.r

        return pd.DataFrame(results)

    def plot_cost_curve(self, q_range: Tuple[float, float] = None):
        """
        Plot total cost curve showing EOQ optimum

        Parameters:
        -----------
        q_range : tuple, optional
            (min_q, max_q) range for plotting. If None, uses EOQ ± 50%
        """

        eoq_result = self.calculate_eoq()
        eoq = eoq_result['eoq']

        if q_range is None:
            q_min = max(1, eoq * 0.3)
            q_max = eoq * 2.0
        else:
            q_min, q_max = q_range

        # Generate Q values
        Q = np.linspace(q_min, q_max, 200)

        # Calculate costs for each Q
        ordering_costs = (self.D / Q) * self.S
        holding_costs = (Q / 2) * self.H
        total_relevant_costs = ordering_costs + holding_costs

        # Plot
        plt.figure(figsize=(12, 7))

        plt.plot(Q, ordering_costs, label='Ordering Cost', linewidth=2, color='blue')
        plt.plot(Q, holding_costs, label='Holding Cost', linewidth=2, color='green')
        plt.plot(Q, total_relevant_costs, label='Total Relevant Cost',
                linewidth=3, color='red')

        # Mark EOQ
        plt.axvline(x=eoq, color='purple', linestyle='--', linewidth=2,
                   label=f'EOQ = {eoq:.0f}')
        plt.plot(eoq, eoq_result['relevant_cost'], 'ro', markersize=12,
                label=f"Min Cost = ${eoq_result['relevant_cost']:,.0f}")

        plt.xlabel('Order Quantity (Q)', fontsize=12)
        plt.ylabel('Annual Cost ($)', fontsize=12)
        plt.title('EOQ Cost Analysis', fontsize=14, fontweight='bold')
        plt.legend(fontsize=10)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()

        return plt

    def reorder_point(self, lead_time_days: float,
                     safety_stock: float = 0) -> Dict:
        """
        Calculate reorder point given lead time

        Parameters:
        -----------
        lead_time_days : float
            Lead time in days
        safety_stock : float
            Safety stock quantity (default 0 for deterministic demand)
        """

        daily_demand = self.D / 365
        lead_time_demand = daily_demand * lead_time_days
        rop = lead_time_demand + safety_stock

        return {
            'reorder_point': round(rop, 2),
            'lead_time_demand': round(lead_time_demand, 2),
            'safety_stock': safety_stock,
            'daily_demand': round(daily_demand, 2)
        }


# Example Usage
def example_basic_eoq():
    """Example: Basic EOQ calculation"""

    # Create EOQ model
    model = EOQModel(
        annual_demand=10000,      # 10,000 units per year
        unit_cost=50,             # $50 per unit
        ordering_cost=100,        # $100 per order
        holding_cost_rate=0.25    # 25% per year
    )

    # Calculate EOQ
    result = model.calculate_eoq()

    print("=" * 60)
    print("ECONOMIC ORDER QUANTITY ANALYSIS")
    print("=" * 60)
    print(f"\nInput Parameters:")
    print(f"  Annual Demand: {model.D:,} units")
    print(f"  Unit Cost: ${model.C:.2f}")
    print(f"  Ordering Cost: ${model.S:.2f}")
    print(f"  Holding Cost Rate: {model.r:.1%}")
    print(f"  Holding Cost per Unit: ${model.H:.2f}/unit/year")

    print(f"\n{'Optimal Order Quantity (EOQ):':<35} {result['eoq']:>15,.0f} units")
    print(f"{'Orders per Year:':<35} {result['orders_per_year']:>15,.2f} orders")
    print(f"{'Days Between Orders:':<35} {result['cycle_time_days']:>15,.1f} days")

    print(f"\n{'Cost Breakdown:':<35}")
    print(f"  {'Purchase Cost:':<33} ${result['purchase_cost']:>15,.2f}")
    print(f"  {'Ordering Cost:':<33} ${result['ordering_cost']:>15,.2f}")
    print(f"  {'Holding Cost:':<33} ${result['holding_cost']:>15,.2f}")
    print(f"  {'-'*50}")
    print(f"  {'Total Annual Cost:':<33} ${result['total_annual_cost']:>15,.2f}")

    print(f"\n{'Inventory Levels:':<35}")
    print(f"  {'Average Inventory:':<33} {result['avg_inventory']:>15,.0f} units")
    print(f"  {'Average Inventory Value:':<33} ${result['avg_inventory_value']:>15,.2f}")
    print(f"  {'Maximum Inventory:':<33} {result['max_inventory']:>15,.0f} units")

    # Calculate reorder point
    rop = model.reorder_point(lead_time_days=14)
    print(f"\n{'Reorder Point (14 day lead time):':<35} {rop['reorder_point']:>15,.0f} units")

    # Plot cost curve
    model.plot_cost_curve()
    plt.savefig('/tmp/eoq_cost_curve.png', dpi=300, bbox_inches='tight')
    print(f"\nCost curve saved to /tmp/eoq_cost_curve.png")

    return model, result


if __name__ == "__main__":
    model, result = example_basic_eoq()
```

---

## EOQ with Quantity Discounts

### All-Units Discount Model

When suppliers offer price breaks based on order quantity, we must consider the trade-off between lower unit costs and increased holding costs.

**All-Units Discount:** The discount applies to all units in the order.

```python
class EOQWithQuantityDiscounts:
    """
    EOQ model with all-units quantity discounts

    Evaluates each price break to find the quantity that minimizes total cost
    """

    def __init__(self, annual_demand: float, ordering_cost: float,
                 holding_cost_rate: float, price_breaks: List[Tuple[float, float]]):
        """
        Parameters:
        -----------
        annual_demand : float
            Annual demand in units
        ordering_cost : float
            Fixed cost per order ($)
        holding_cost_rate : float
            Annual holding cost as fraction of unit cost
        price_breaks : list of tuples
            [(min_qty, unit_price), ...] sorted by quantity
            Example: [(0, 50), (500, 48), (1000, 45)]
        """
        self.D = annual_demand
        self.S = ordering_cost
        self.r = holding_cost_rate
        self.price_breaks = sorted(price_breaks, key=lambda x: x[0])

    def calculate_optimal_quantity(self) -> Dict:
        """
        Find order quantity that minimizes total cost

        Algorithm:
        1. For each price break, calculate EOQ at that price
        2. If EOQ < break quantity, use break quantity
        3. Calculate total cost for each feasible quantity
        4. Select quantity with minimum total cost
        """

        candidates = []

        for i, (break_qty, unit_price) in enumerate(self.price_breaks):
            H = unit_price * self.r

            # Calculate EOQ at this price
            eoq = np.sqrt((2 * self.D * self.S) / H)

            # Determine feasible order quantity
            # EOQ is feasible if it's >= current break and < next break
            if i < len(self.price_breaks) - 1:
                next_break_qty = self.price_breaks[i + 1][0]
                if eoq >= break_qty and eoq < next_break_qty:
                    feasible_qty = eoq
                else:
                    feasible_qty = break_qty
            else:
                # Last price break - EOQ is feasible if >= break qty
                feasible_qty = max(eoq, break_qty)

            # Calculate total cost at this quantity
            if feasible_qty >= break_qty:
                ordering_cost = (self.D / feasible_qty) * self.S
                holding_cost = (feasible_qty / 2) * H
                purchase_cost = self.D * unit_price
                total_cost = purchase_cost + ordering_cost + holding_cost

                candidates.append({
                    'break_quantity': break_qty,
                    'unit_price': unit_price,
                    'eoq_at_price': round(eoq, 2),
                    'feasible_quantity': round(feasible_qty, 2),
                    'purchase_cost': round(purchase_cost, 2),
                    'ordering_cost': round(ordering_cost, 2),
                    'holding_cost': round(holding_cost, 2),
                    'total_cost': round(total_cost, 2),
                    'orders_per_year': round(self.D / feasible_qty, 2)
                })

        # Find minimum cost option
        candidates_df = pd.DataFrame(candidates)
        optimal_idx = candidates_df['total_cost'].idxmin()
        optimal = candidates_df.iloc[optimal_idx]

        return {
            'all_candidates': candidates_df,
            'optimal': optimal.to_dict(),
            'savings_vs_no_discount': self._calculate_savings(optimal)
        }

    def _calculate_savings(self, optimal: pd.Series) -> float:
        """Calculate savings compared to ordering at highest price (no discount)"""

        highest_price = self.price_breaks[0][1]
        H_base = highest_price * self.r
        eoq_base = np.sqrt((2 * self.D * self.S) / H_base)

        cost_base = (self.D * highest_price +
                    (self.D / eoq_base) * self.S +
                    (eoq_base / 2) * H_base)

        savings = cost_base - optimal['total_cost']
        savings_pct = (savings / cost_base) * 100

        return round(savings_pct, 2)

    def plot_discount_analysis(self):
        """Visualize total cost at different order quantities"""

        result = self.calculate_optimal_quantity()

        plt.figure(figsize=(14, 8))

        # Generate cost curves for each price segment
        for i, (break_qty, unit_price) in enumerate(self.price_breaks):
            H = unit_price * self.r

            # Define quantity range for this price
            if i < len(self.price_breaks) - 1:
                q_max = self.price_breaks[i + 1][0]
            else:
                q_max = break_qty * 3

            Q = np.linspace(break_qty, q_max, 100)

            # Calculate total cost
            total_costs = (self.D * unit_price +
                          (self.D / Q) * self.S +
                          (Q / 2) * H)

            plt.plot(Q, total_costs, linewidth=2,
                    label=f'${unit_price}/unit (Q ≥ {break_qty})')

        # Mark optimal point
        optimal = result['optimal']
        plt.plot(optimal['feasible_quantity'], optimal['total_cost'],
                'r*', markersize=20, label=f"Optimal: Q={optimal['feasible_quantity']:.0f}")

        # Mark all candidates
        for _, row in result['all_candidates'].iterrows():
            plt.plot(row['feasible_quantity'], row['total_cost'],
                    'ko', markersize=8)

        plt.xlabel('Order Quantity (Q)', fontsize=12)
        plt.ylabel('Total Annual Cost ($)', fontsize=12)
        plt.title('EOQ with Quantity Discounts', fontsize=14, fontweight='bold')
        plt.legend(fontsize=10)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()

        return plt


# Example: Quantity Discounts
def example_quantity_discounts():
    """Example: EOQ with all-units quantity discount"""

    price_breaks = [
        (0, 50.00),      # 0-499 units: $50/unit
        (500, 48.00),    # 500-999 units: $48/unit
        (1000, 45.00),   # 1000+ units: $45/unit
        (2500, 43.00)    # 2500+ units: $43/unit
    ]

    model = EOQWithQuantityDiscounts(
        annual_demand=10000,
        ordering_cost=100,
        holding_cost_rate=0.25,
        price_breaks=price_breaks
    )

    result = model.calculate_optimal_quantity()

    print("\n" + "=" * 70)
    print("EOQ WITH QUANTITY DISCOUNTS ANALYSIS")
    print("=" * 70)

    print("\nPrice Break Structure:")
    for qty, price in price_breaks:
        print(f"  {qty:>6} units or more: ${price:.2f}/unit")

    print("\n\nCandidate Solutions:")
    print(result['all_candidates'].to_string(index=False))

    print("\n\n" + "=" * 70)
    print("OPTIMAL SOLUTION")
    print("=" * 70)
    opt = result['optimal']
    print(f"{'Order Quantity:':<30} {opt['feasible_quantity']:>15,.0f} units")
    print(f"{'Unit Price:':<30} ${opt['unit_price']:>15,.2f}")
    print(f"{'Orders per Year:':<30} {opt['orders_per_year']:>15,.2f}")
    print(f"\n{'Cost Breakdown:':<30}")
    print(f"  {'Purchase Cost:':<28} ${opt['purchase_cost']:>15,.2f}")
    print(f"  {'Ordering Cost:':<28} ${opt['ordering_cost']:>15,.2f}")
    print(f"  {'Holding Cost:':<28} ${opt['holding_cost']:>15,.2f}")
    print(f"  {'-'*45}")
    print(f"  {'Total Annual Cost:':<28} ${opt['total_cost']:>15,.2f}")
    print(f"\n{'Savings vs No Discount:':<30} {result['savings_vs_no_discount']:>15,.1f}%")

    # Plot
    model.plot_discount_analysis()
    plt.savefig('/tmp/eoq_quantity_discounts.png', dpi=300, bbox_inches='tight')
    print(f"\nDiscount analysis plot saved to /tmp/eoq_quantity_discounts.png")

    return model, result


if __name__ == "__main__":
    example_quantity_discounts()
```

---

## Economic Production Quantity (EPQ)

### EPQ Model for Production Environments

When items are produced internally rather than purchased, replenishment is **gradual** (not instantaneous). This is the Economic Production Quantity (EPQ) model.

**Assumptions:**
- Production rate (p) > demand rate (d)
- Production occurs at constant rate p units/day
- No stockouts allowed
- Setup cost S incurred each production run

**Key Difference from EOQ:** Inventory builds up gradually during production.

```python
class EPQModel:
    """
    Economic Production Quantity (EPQ) Model

    Optimal production lot size when items are produced internally
    at a finite production rate
    """

    def __init__(self, annual_demand: float, production_rate: float,
                 unit_cost: float, setup_cost: float, holding_cost_rate: float):
        """
        Parameters:
        -----------
        annual_demand : float
            Annual demand rate (units/year)
        production_rate : float
            Production rate (units/year)
        unit_cost : float
            Cost per unit ($)
        setup_cost : float
            Fixed cost per production run ($)
        holding_cost_rate : float
            Annual holding cost as fraction of unit cost
        """
        self.D = annual_demand
        self.p = production_rate
        self.C = unit_cost
        self.S = setup_cost
        self.r = holding_cost_rate
        self.H = unit_cost * holding_cost_rate

        # Validate: production rate must exceed demand rate
        if self.p <= self.D:
            raise ValueError("Production rate must exceed demand rate")

    def calculate_epq(self) -> Dict:
        """
        Calculate Economic Production Quantity

        EPQ Formula:
        EPQ = √(2DS/H) × √(p/(p-D))

        The term √(p/(p-D)) adjusts for gradual replenishment
        """

        # EPQ formula
        epq = np.sqrt((2 * self.D * self.S) / self.H) * np.sqrt(self.p / (self.p - self.D))

        # Production runs per year
        runs_per_year = self.D / epq

        # Production time per run (days)
        production_time = (epq / self.p) * 365

        # Maximum inventory level
        # Inventory builds while producing and consuming
        max_inventory = epq * (1 - self.D / self.p)

        # Average inventory (half of maximum)
        avg_inventory = max_inventory / 2

        # Cost components
        production_cost = self.D * self.C
        setup_cost_total = runs_per_year * self.S
        holding_cost_total = avg_inventory * self.H
        total_cost = production_cost + setup_cost_total + holding_cost_total

        # Cycle time
        cycle_time_days = 365 / runs_per_year

        return {
            'epq': round(epq, 2),
            'runs_per_year': round(runs_per_year, 2),
            'production_time_days': round(production_time, 2),
            'cycle_time_days': round(cycle_time_days, 2),
            'max_inventory': round(max_inventory, 2),
            'avg_inventory': round(avg_inventory, 2),
            'total_annual_cost': round(total_cost, 2),
            'production_cost': round(production_cost, 2),
            'setup_cost': round(setup_cost_total, 2),
            'holding_cost': round(holding_cost_total, 2),
            'utilization': round((self.D / self.p) * 100, 2)
        }

    def simulate_inventory_cycle(self, num_cycles: int = 3) -> pd.DataFrame:
        """
        Simulate inventory levels over multiple production cycles

        Returns DataFrame with daily inventory levels
        """

        result = self.calculate_epq()
        epq = result['epq']
        cycle_time = result['cycle_time_days']
        production_time = result['production_time_days']

        daily_demand = self.D / 365
        daily_production = self.p / 365

        inventory_data = []
        current_inventory = 0

        total_days = int(cycle_time * num_cycles)

        for day in range(total_days):
            cycle_day = day % cycle_time

            # During production phase
            if cycle_day < production_time:
                # Inventory increases by net production
                current_inventory += (daily_production - daily_demand)
            else:
                # Only consuming inventory
                current_inventory -= daily_demand

            # Prevent negative inventory (numerical precision)
            current_inventory = max(0, current_inventory)

            inventory_data.append({
                'day': day,
                'cycle': day // cycle_time + 1,
                'cycle_day': cycle_day,
                'inventory': current_inventory,
                'producing': cycle_day < production_time
            })

        return pd.DataFrame(inventory_data)

    def plot_inventory_cycle(self, num_cycles: int = 3):
        """Visualize inventory levels over production cycles"""

        df = self.simulate_inventory_cycle(num_cycles)
        result = self.calculate_epq()

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))

        # Plot 1: Inventory over time
        production_periods = df[df['producing'] == True]
        consumption_periods = df[df['producing'] == False]

        ax1.plot(df['day'], df['inventory'], linewidth=2, color='blue')
        ax1.fill_between(production_periods['day'], 0, production_periods['inventory'],
                         alpha=0.3, color='green', label='Production Phase')
        ax1.axhline(y=result['avg_inventory'], color='red', linestyle='--',
                   linewidth=2, label=f"Avg Inventory = {result['avg_inventory']:.0f}")
        ax1.axhline(y=result['max_inventory'], color='orange', linestyle='--',
                   linewidth=2, label=f"Max Inventory = {result['max_inventory']:.0f}")

        ax1.set_xlabel('Day', fontsize=12)
        ax1.set_ylabel('Inventory Level (units)', fontsize=12)
        ax1.set_title('EPQ Inventory Cycle', fontsize=14, fontweight='bold')
        ax1.legend(fontsize=10)
        ax1.grid(True, alpha=0.3)

        # Plot 2: Single cycle detail
        single_cycle = df[df['cycle'] == 1]
        ax2.plot(single_cycle['cycle_day'], single_cycle['inventory'],
                linewidth=3, color='blue', marker='o', markersize=4)
        ax2.axvline(x=result['production_time_days'], color='red',
                   linestyle='--', linewidth=2,
                   label=f"Production Time = {result['production_time_days']:.1f} days")
        ax2.fill_between(single_cycle['cycle_day'], 0, single_cycle['inventory'],
                        where=single_cycle['producing'], alpha=0.3, color='green',
                        label='Producing')
        ax2.fill_between(single_cycle['cycle_day'], 0, single_cycle['inventory'],
                        where=~single_cycle['producing'], alpha=0.3, color='red',
                        label='Only Consuming')

        ax2.set_xlabel('Days in Cycle', fontsize=12)
        ax2.set_ylabel('Inventory Level (units)', fontsize=12)
        ax2.set_title('Single Production Cycle Detail', fontsize=14, fontweight='bold')
        ax2.legend(fontsize=10)
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()
        return plt


# Example: EPQ
def example_epq():
    """Example: Economic Production Quantity calculation"""

    model = EPQModel(
        annual_demand=10000,       # 10,000 units/year demand
        production_rate=50000,     # Can produce 50,000 units/year
        unit_cost=50,              # $50 per unit
        setup_cost=500,            # $500 setup cost per run
        holding_cost_rate=0.25     # 25% holding cost
    )

    result = model.calculate_epq()

    print("\n" + "=" * 70)
    print("ECONOMIC PRODUCTION QUANTITY (EPQ) ANALYSIS")
    print("=" * 70)

    print(f"\nInput Parameters:")
    print(f"  Annual Demand: {model.D:,} units/year")
    print(f"  Production Rate: {model.p:,} units/year")
    print(f"  Unit Cost: ${model.C:.2f}")
    print(f"  Setup Cost: ${model.S:.2f}")
    print(f"  Holding Cost Rate: {model.r:.1%}")

    print(f"\n{'Optimal Production Quantity (EPQ):':<40} {result['epq']:>15,.0f} units")
    print(f"{'Production Runs per Year:':<40} {result['runs_per_year']:>15,.2f} runs")
    print(f"{'Days Between Production Runs:':<40} {result['cycle_time_days']:>15,.1f} days")
    print(f"{'Production Time per Run:':<40} {result['production_time_days']:>15,.1f} days")

    print(f"\n{'Inventory Levels:':<40}")
    print(f"  {'Maximum Inventory:':<38} {result['max_inventory']:>15,.0f} units")
    print(f"  {'Average Inventory:':<38} {result['avg_inventory']:>15,.0f} units")

    print(f"\n{'Cost Breakdown:':<40}")
    print(f"  {'Production Cost:':<38} ${result['production_cost']:>15,.2f}")
    print(f"  {'Setup Cost:':<38} ${result['setup_cost']:>15,.2f}")
    print(f"  {'Holding Cost:':<38} ${result['holding_cost']:>15,.2f}")
    print(f"  {'-'*55}")
    print(f"  {'Total Annual Cost:':<38} ${result['total_annual_cost']:>15,.2f}")

    print(f"\n{'Production Capacity Utilization:':<40} {result['utilization']:>15,.1f}%")

    # Plot
    model.plot_inventory_cycle(num_cycles=3)
    plt.savefig('/tmp/epq_inventory_cycle.png', dpi=300, bbox_inches='tight')
    print(f"\nInventory cycle plot saved to /tmp/epq_inventory_cycle.png")

    return model, result


if __name__ == "__main__":
    example_epq()
```

---

## EOQ with Planned Backorders

### Backorder Model

When backorders are allowed and incur a penalty cost, it may be economical to deliberately plan for stockouts.

**Decision Variables:**
- Q = Order quantity
- S = Maximum inventory level (< Q)
- Q - S = Planned backorder quantity

```python
class EOQWithBackorders:
    """
    EOQ model with planned backorders

    Allows intentional stockouts when backorder cost is lower than holding cost
    """

    def __init__(self, annual_demand: float, unit_cost: float,
                 ordering_cost: float, holding_cost_rate: float,
                 backorder_cost_rate: float):
        """
        Parameters:
        -----------
        annual_demand : float
            Annual demand in units
        unit_cost : float
            Cost per unit ($)
        ordering_cost : float
            Fixed cost per order ($)
        holding_cost_rate : float
            Annual holding cost as fraction of unit cost
        backorder_cost_rate : float
            Annual backorder cost per unit ($/unit/year)
        """
        self.D = annual_demand
        self.C = unit_cost
        self.S_cost = ordering_cost
        self.H = unit_cost * holding_cost_rate
        self.B = backorder_cost_rate

    def calculate_optimal(self) -> Dict:
        """
        Calculate optimal order quantity and maximum inventory level

        Formulas:
        Q* = √(2DS/H) × √((H+B)/B)
        S* = Q* × (B/(H+B))

        Where S* is the maximum inventory level (peak before stockout)
        """

        # Basic EOQ (without backorders)
        eoq_basic = np.sqrt((2 * self.D * self.S_cost) / self.H)

        # Optimal order quantity with backorders
        Q_opt = eoq_basic * np.sqrt((self.H + self.B) / self.B)

        # Maximum inventory level
        S_opt = Q_opt * (self.B / (self.H + self.B))

        # Maximum backorder level
        backorder_max = Q_opt - S_opt

        # Time fractions
        time_with_inventory = S_opt / self.D  # years
        time_with_backorders = backorder_max / self.D  # years
        cycle_time = Q_opt / self.D  # years

        # Cost calculation
        orders_per_year = self.D / Q_opt
        ordering_cost = orders_per_year * self.S_cost

        # Average inventory (triangular distribution)
        avg_inventory = (S_opt ** 2) / (2 * Q_opt)
        holding_cost = avg_inventory * self.H

        # Average backorders
        avg_backorders = (backorder_max ** 2) / (2 * Q_opt)
        backorder_cost_total = avg_backorders * self.B

        purchase_cost = self.D * self.C
        total_cost = purchase_cost + ordering_cost + holding_cost + backorder_cost_total

        # Compare with basic EOQ (no backorders)
        cost_basic = (purchase_cost +
                     (self.D / eoq_basic) * self.S_cost +
                     (eoq_basic / 2) * self.H)

        savings = cost_basic - total_cost
        savings_pct = (savings / cost_basic) * 100

        return {
            'order_quantity': round(Q_opt, 2),
            'max_inventory': round(S_opt, 2),
            'max_backorders': round(backorder_max, 2),
            'orders_per_year': round(orders_per_year, 2),
            'cycle_time_days': round(cycle_time * 365, 2),
            'time_with_inventory_days': round(time_with_inventory * 365, 2),
            'time_with_backorders_days': round(time_with_backorders * 365, 2),
            'avg_inventory': round(avg_inventory, 2),
            'avg_backorders': round(avg_backorders, 2),
            'total_cost': round(total_cost, 2),
            'ordering_cost': round(ordering_cost, 2),
            'holding_cost': round(holding_cost, 2),
            'backorder_cost': round(backorder_cost_total, 2),
            'cost_without_backorders': round(cost_basic, 2),
            'savings': round(savings, 2),
            'savings_pct': round(savings_pct, 2)
        }

    def plot_backorder_cycle(self):
        """Visualize inventory cycle with planned backorders"""

        result = self.calculate_optimal()
        Q = result['order_quantity']
        S = result['max_inventory']

        # Time points (in fractions of year)
        t1 = S / self.D  # Time to deplete inventory
        t2 = Q / self.D  # Full cycle time

        # Convert to days for plotting
        t1_days = t1 * 365
        t2_days = t2 * 365

        # Create time array for one cycle
        t_positive = np.linspace(0, t1_days, 100)
        t_negative = np.linspace(t1_days, t2_days, 100)

        # Inventory levels
        inv_positive = S - (self.D / 365) * t_positive
        inv_negative = -(self.D / 365) * (t_negative - t1_days)

        plt.figure(figsize=(14, 8))

        # Plot inventory (positive)
        plt.fill_between(t_positive, 0, inv_positive, alpha=0.3, color='green',
                        label='On-hand Inventory')
        plt.plot(t_positive, inv_positive, linewidth=3, color='green')

        # Plot backorders (negative)
        plt.fill_between(t_negative, 0, inv_negative, alpha=0.3, color='red',
                        label='Backorders')
        plt.plot(t_negative, inv_negative, linewidth=3, color='red')

        # Mark key points
        plt.plot(0, S, 'go', markersize=12, label=f'Order Arrives: +{S:.0f} units')
        plt.plot(t1_days, 0, 'yo', markersize=12, label='Stockout Begins')
        plt.plot(t2_days, -result['max_backorders'], 'ro', markersize=12,
                label=f"Max Backorder: {result['max_backorders']:.0f} units")

        # Add average lines
        plt.axhline(y=result['avg_inventory'], color='green', linestyle='--',
                   linewidth=2, alpha=0.7, label=f"Avg Inventory: {result['avg_inventory']:.1f}")
        plt.axhline(y=-result['avg_backorders'], color='red', linestyle='--',
                   linewidth=2, alpha=0.7, label=f"Avg Backorders: {result['avg_backorders']:.1f}")

        plt.axhline(y=0, color='black', linewidth=1)
        plt.axvline(x=t1_days, color='gray', linestyle=':', linewidth=2)

        plt.xlabel('Days', fontsize=12)
        plt.ylabel('Inventory Level (units)', fontsize=12)
        plt.title('EOQ with Planned Backorders - Inventory Cycle',
                 fontsize=14, fontweight='bold')
        plt.legend(fontsize=10, loc='upper right')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()

        return plt


# Example: Backorders
def example_backorders():
    """Example: EOQ with planned backorders"""

    model = EOQWithBackorders(
        annual_demand=10000,
        unit_cost=50,
        ordering_cost=100,
        holding_cost_rate=0.25,
        backorder_cost_rate=5.0  # $5 per unit per year backordered
    )

    result = model.calculate_optimal()

    print("\n" + "=" * 70)
    print("EOQ WITH PLANNED BACKORDERS ANALYSIS")
    print("=" * 70)

    print(f"\nInput Parameters:")
    print(f"  Annual Demand: {model.D:,} units")
    print(f"  Holding Cost: ${model.H:.2f}/unit/year")
    print(f"  Backorder Cost: ${model.B:.2f}/unit/year")
    print(f"  Ordering Cost: ${model.S_cost:.2f}/order")

    print(f"\n{'Optimal Policy:':<45}")
    print(f"  {'Order Quantity:':<43} {result['order_quantity']:>15,.0f} units")
    print(f"  {'Maximum Inventory (before stockout):':<43} {result['max_inventory']:>15,.0f} units")
    print(f"  {'Maximum Backorders:':<43} {result['max_backorders']:>15,.0f} units")

    print(f"\n{'Cycle Characteristics:':<45}")
    print(f"  {'Orders per Year:':<43} {result['orders_per_year']:>15,.2f}")
    print(f"  {'Cycle Time:':<43} {result['cycle_time_days']:>15,.1f} days")
    print(f"  {'Time with Inventory:':<43} {result['time_with_inventory_days']:>15,.1f} days")
    print(f"  {'Time with Backorders:':<43} {result['time_with_backorders_days']:>15,.1f} days")

    print(f"\n{'Average Levels:':<45}")
    print(f"  {'Average Inventory:':<43} {result['avg_inventory']:>15,.1f} units")
    print(f"  {'Average Backorders:':<43} {result['avg_backorders']:>15,.1f} units")

    print(f"\n{'Cost Analysis:':<45}")
    print(f"  {'Ordering Cost:':<43} ${result['ordering_cost']:>15,.2f}")
    print(f"  {'Holding Cost:':<43} ${result['holding_cost']:>15,.2f}")
    print(f"  {'Backorder Cost:':<43} ${result['backorder_cost']:>15,.2f}")
    print(f"  {'-'*60}")
    print(f"  {'Total Annual Cost (with backorders):':<43} ${result['total_cost']:>15,.2f}")
    print(f"  {'Total Cost without Backorders:':<43} ${result['cost_without_backorders']:>15,.2f}")
    print(f"  {'-'*60}")
    print(f"  {'Annual Savings:':<43} ${result['savings']:>15,.2f}")
    print(f"  {'Savings Percentage:':<43} {result['savings_pct']:>15,.1f}%")

    # Plot
    model.plot_backorder_cycle()
    plt.savefig('/tmp/eoq_backorders.png', dpi=300, bbox_inches='tight')
    print(f"\nBackorder cycle plot saved to /tmp/eoq_backorders.png")

    return model, result


if __name__ == "__main__":
    example_backorders()
```

---

## Tools & Libraries

### Python Libraries

**Numerical & Scientific:**
- `numpy`: Array operations, mathematical functions
- `scipy`: Optimization, statistical distributions
- `pandas`: Data manipulation and analysis

**Optimization:**
- `pulp`: Linear programming for constrained EOQ
- `scipy.optimize`: Non-linear optimization

**Visualization:**
- `matplotlib`: Plotting cost curves, inventory cycles
- `seaborn`: Statistical visualizations
- `plotly`: Interactive dashboards

### Commercial Software

**ERP Systems with EOQ:**
- **SAP**: Material Requirements Planning (MRP) with lot sizing
- **Oracle EBS**: Order Management with EOQ rules
- **Microsoft Dynamics**: Inventory optimization modules
- **NetSuite**: Demand planning with EOQ

**Specialized Inventory Planning:**
- **Blue Yonder**: Advanced inventory optimization
- **Logility**: Lot sizing and replenishment planning
- **Kinaxis RapidResponse**: Inventory policy optimization
- **Llamasoft**: Supply chain design with inventory analysis

---

## Common Challenges & Solutions

### Challenge: Uncertain Demand

**Problem:**
- Classic EOQ assumes constant, known demand
- Real demand is variable and uncertain

**Solutions:**
- Use expected demand D for EOQ calculation
- Add safety stock for demand variability (see **stochastic-inventory-models**)
- Implement periodic EOQ recalculation (monthly/quarterly)
- Consider robust optimization with demand scenarios
- Use (Q, r) continuous review policy with reorder point

### Challenge: Unknown Holding Cost

**Problem:**
- Difficult to estimate true holding cost rate
- Includes capital, storage, obsolescence, damage

**Solutions:**
- Use industry benchmarks (typically 15-35% of unit cost)
- Calculate weighted average cost of capital (WACC) as minimum
- Add storage costs ($/sq ft × space per unit)
- Include insurance and obsolescence
- Perform sensitivity analysis on holding cost rate
- Start with 25% as reasonable default

### Challenge: Quantity Constraints

**Problem:**
- Supplier MOQs may differ from EOQ
- Packaging constraints (must order in multiples)
- Storage capacity limits

**Solutions:**
- If MOQ > EOQ: Order MOQ (accept higher holding cost)
- If MOQ < EOQ: Order EOQ rounded to package size
- For capacity constraints: Use constrained optimization
- Negotiate with supplier for smaller MOQs
- Consider multi-item EOQ with shared capacity constraint

### Challenge: Multiple Items with Budget Constraints

**Problem:**
- EOQ calculated independently for each SKU
- Total budget or storage capacity is limited

**Solutions:**
- Formulate as constrained optimization problem
- Use Lagrange multipliers for continuous relaxation
- Implement ABC analysis - focus on A items
- Use dynamic programming for exact solution
- Consider proportional allocation based on EOQ ratios

```python
from scipy.optimize import minimize

def multi_item_eoq_constrained(items: List[Dict], budget: float) -> Dict:
    """
    Multi-item EOQ with budget constraint

    items: list of dicts with keys: demand, ordering_cost, holding_cost
    budget: total budget for average inventory investment
    """

    n = len(items)

    def objective(Q):
        """Minimize total relevant cost"""
        total_cost = 0
        for i, q in enumerate(Q):
            item = items[i]
            ordering_cost = (item['demand'] / q) * item['ordering_cost']
            holding_cost = (q / 2) * item['holding_cost']
            total_cost += ordering_cost + holding_cost
        return total_cost

    def budget_constraint(Q):
        """Average inventory value <= budget"""
        total_inventory_value = 0
        for i, q in enumerate(Q):
            avg_inventory = q / 2
            total_inventory_value += avg_inventory * items[i]['unit_cost']
        return budget - total_inventory_value

    # Initial guess: unconstrained EOQ
    Q0 = [np.sqrt(2 * item['demand'] * item['ordering_cost'] / item['holding_cost'])
          for item in items]

    # Constraints
    cons = [{'type': 'ineq', 'fun': budget_constraint}]

    # Bounds: positive quantities
    bounds = [(1, None) for _ in range(n)]

    # Solve
    result = minimize(objective, Q0, method='SLSQP', bounds=bounds, constraints=cons)

    return {
        'optimal_quantities': result.x,
        'total_cost': result.fun,
        'success': result.success
    }
```

### Challenge: Time-Varying Parameters

**Problem:**
- Demand, costs, or prices change over time
- Seasonal demand patterns
- Inflation

**Solutions:**
- Recalculate EOQ periodically (monthly/quarterly)
- Use rolling average demand for D
- Consider finite horizon lot-sizing models (see **dynamic-lot-sizing**)
- Implement dynamic EOQ with forecast updates
- For seasonality: Calculate separate EOQs per season

### Challenge: Lead Time Uncertainty

**Problem:**
- EOQ doesn't account for lead time variability
- Risk of stockouts during replenishment

**Solutions:**
- EOQ determines Q, separate reorder point (r) handles lead time
- Calculate safety stock for lead time variability
- Use (Q, r) policy: Order Q when inventory hits r
- See **stochastic-inventory-models** for safety stock calculation
- Monitor supplier performance and adjust lead time estimates

---

## Output Format

### EOQ Analysis Report

**Executive Summary:**
- Current ordering practice: Order 2,000 units every 73 days
- Recommended EOQ: 1,265 units every 46 days
- Annual savings: $3,450 (12% cost reduction)
- Implementation: Adjust order quantities and frequency

**Input Parameters:**

| Parameter | Value |
|-----------|-------|
| Annual Demand | 10,000 units |
| Unit Cost | $50.00 |
| Ordering Cost | $100/order |
| Holding Cost Rate | 25%/year |
| Holding Cost | $12.50/unit/year |

**Optimal Policy:**

| Metric | Current | Optimal (EOQ) | Improvement |
|--------|---------|---------------|-------------|
| Order Quantity | 2,000 | 1,265 | N/A |
| Orders per Year | 5 | 7.9 | +58% |
| Days Between Orders | 73 | 46 | -37% |
| Avg Inventory | 1,000 | 633 | -37% |
| Total Annual Cost | $531,250 | $527,800 | -$3,450 (-0.65%) |

**Cost Breakdown:**

| Cost Component | Current | Optimal (EOQ) | Difference |
|----------------|---------|---------------|------------|
| Purchase Cost | $500,000 | $500,000 | $0 |
| Ordering Cost | $500 | $790 | +$290 |
| Holding Cost | $12,500 | $7,910 | -$4,590 |
| **Total** | **$513,000** | **$508,700** | **-$4,300** |

**Reorder Point:**
- Lead time: 14 days
- Average daily demand: 27.4 units
- Lead time demand: 384 units
- Recommended reorder point: 385 units (with zero safety stock)

**Implementation Recommendations:**
1. Adjust order quantity to 1,265 units (round to 1,250 if packaging constraints)
2. Set reorder point at 385 units
3. Monitor inventory and place orders when reaching reorder point
4. Review and recalculate EOQ quarterly
5. Consider demand variability for safety stock adjustment

---

## Questions to Ask

If you need more context:
1. What is the annual demand for this item? (units/year)
2. What is the cost per unit?
3. What is the cost to place an order? (fixed cost per order)
4. What is the inventory holding cost rate? (% of unit cost per year)
5. Are there quantity discounts available from the supplier?
6. Is this item purchased or produced internally?
7. If produced: What is the production rate?
8. Are stockouts acceptable? If yes, what is the backorder penalty cost?
9. What is the lead time from order to delivery?
10. Are there any constraints? (MOQ, storage capacity, budget limits)

---

## Related Skills

- **inventory-optimization**: Comprehensive inventory management framework
- **lot-sizing-problems**: Multi-period lot-sizing models
- **dynamic-lot-sizing**: Time-varying demand lot-sizing
- **stochastic-inventory-models**: Probabilistic inventory models with uncertainty
- **newsvendor-problem**: Single-period inventory decisions
- **multi-echelon-inventory**: Network-wide inventory optimization
- **demand-forecasting**: Demand estimation for EOQ inputs
- **supply-chain-analytics**: Performance metrics and KPIs
