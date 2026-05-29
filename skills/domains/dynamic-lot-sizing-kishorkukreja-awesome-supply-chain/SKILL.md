---
name: dynamic-lot-sizing
description: When the user wants to solve lot-sizing problems with time-varying costs or demand, handle non-stationary inventory systems, or optimize replenishment with changing parameters over time. Also use when the user mentions "time-varying lot sizing," "finite horizon lot sizing," "dynamic EOQ," "price changes over time," "seasonal lot sizing," "Wagner-Whitin with time-varying costs," or "rolling horizon planning." For stationary systems, see economic-order-quantity or lot-sizing-problems. For stochastic demand, see stochastic-inventory-models.
---

# Dynamic Lot-Sizing

You are an expert in dynamic lot-sizing models for non-stationary inventory systems with time-varying parameters. Your goal is to help optimize inventory replenishment decisions when demand, costs, or prices change over time, using finite-horizon planning approaches.

## Initial Assessment

Before solving dynamic lot-sizing problems, understand:

1. **Time Horizon**
   - Planning horizon length? (months, quarters, years)
   - Finite or rolling horizon?
   - Frequency of replanning?

2. **Time-Varying Parameters**
   - What changes over time? (demand, costs, prices, capacity)
   - Demand: seasonal patterns, trends, known changes?
   - Costs: price increases, seasonal holding costs?
   - Capacity: time-varying production/storage limits?

3. **Problem Type**
   - Deterministic or stochastic time variation?
   - Known price changes (announced) or forecasted?
   - Must account for inflation?

4. **Decision Flexibility**
   - Can adjust decisions at each period?
   - Committed orders vs. flexible replenishment?
   - Lead times and their impact?

5. **Special Considerations**
   - End-of-horizon effects (salvage value, terminal inventory)?
   - Price speculation opportunities?
   - Obsolescence or product lifecycle considerations?

---

## Dynamic Lot-Sizing Fundamentals

### Problem Characteristics

**Key Differences from Static EOQ:**
- Demand varies by period: D₁, D₂, ..., D_T
- Costs may vary: setup S_t, holding h_t, purchase c_t
- Finite planning horizon T (not infinite)
- Must account for end-of-horizon effects

**Decision:** Order quantities Q_t in each period t to minimize total cost

**Applications:**
- Seasonal demand planning
- Price speculation (buy before price increase)
- Product lifecycle management (new/declining products)
- Fashion/perishable goods
- Promotional planning

---

## Python Implementation: Dynamic Lot-Sizing

### Time-Varying Demand and Costs

```python
import numpy as np
import pandas as pd
from typing import List, Dict, Optional
import matplotlib.pyplot as plt
from scipy.optimize import minimize

class DynamicLotSizing:
    """
    Dynamic lot-sizing with time-varying parameters

    Handles changes in demand, costs, and prices over time
    """

    def __init__(self, demands: List[float], setup_costs: List[float],
                 holding_costs: List[float], unit_costs: List[float],
                 initial_inventory: float = 0, salvage_value: float = 0):
        """
        Parameters:
        -----------
        demands : list
            Demand in each period [D₁, D₂, ..., D_T]
        setup_costs : list
            Setup cost in each period [S₁, S₂, ..., S_T]
        holding_costs : list
            Holding cost per unit per period [h₁, h₂, ..., h_T]
        unit_costs : list
            Purchase cost per unit [c₁, c₂, ..., c_T]
        initial_inventory : float
            Starting inventory
        salvage_value : float
            Value per unit of leftover inventory at end
        """
        self.T = len(demands)
        self.demands = np.array(demands)
        self.setup_costs = np.array(setup_costs)
        self.holding_costs = np.array(holding_costs)
        self.unit_costs = np.array(unit_costs)
        self.initial_inventory = initial_inventory
        self.salvage_value = salvage_value

    def dynamic_programming(self) -> Dict:
        """
        Solve using dynamic programming

        F(t, I_t) = minimum cost from period t onwards with inventory I_t

        For computational efficiency, discretize inventory levels
        """

        # Cumulative future demands
        cum_demand = np.zeros(self.T + 1)
        for t in range(self.T - 1, -1, -1):
            cum_demand[t] = cum_demand[t + 1] + self.demands[t]

        # Maximum useful inventory to consider
        max_inventory = int(cum_demand[0])

        # DP table: F[t][i] = min cost from period t with inventory i
        INF = 1e9
        F = [[INF] * (max_inventory + 1) for _ in range(self.T + 1)]
        decision = [[None] * (max_inventory + 1) for _ in range(self.T)]

        # Terminal condition: salvage value
        for i in range(max_inventory + 1):
            F[self.T][i] = -self.salvage_value * i

        # Backward recursion
        for t in range(self.T - 1, -1, -1):
            d_t = self.demands[t]
            S_t = self.setup_costs[t]
            h_t = self.holding_costs[t]
            c_t = self.unit_costs[t]

            for I_t in range(max_inventory + 1):
                # Option 1: Don't order
                if I_t >= d_t:
                    I_next = I_t - d_t
                    cost_no_order = h_t * I_next + F[t + 1][int(I_next)]
                else:
                    cost_no_order = INF  # Cannot satisfy demand

                # Option 2: Order
                best_order_cost = INF
                best_order_qty = 0

                # Try different order quantities
                max_order = int(cum_demand[t] - I_t)
                for Q in range(1, max_order + 1):
                    I_after_order = I_t + Q
                    if I_after_order >= d_t:
                        I_next = I_after_order - d_t
                        cost = S_t + c_t * Q + h_t * I_next + F[t + 1][int(I_next)]
                        if cost < best_order_cost:
                            best_order_cost = cost
                            best_order_qty = Q

                # Choose best option
                if cost_no_order < best_order_cost:
                    F[t][I_t] = cost_no_order
                    decision[t][I_t] = 0  # No order
                else:
                    F[t][I_t] = best_order_cost
                    decision[t][I_t] = best_order_qty

        # Forward pass to construct solution
        orders = np.zeros(self.T)
        inventory = np.zeros(self.T + 1)
        inventory[0] = self.initial_inventory

        for t in range(self.T):
            I_t = int(inventory[t])
            Q_t = decision[t][I_t] if I_t <= max_inventory else 0
            orders[t] = Q_t

            inventory[t + 1] = inventory[t] + Q_t - self.demands[t]

        # Calculate costs
        setup_cost = sum(self.setup_costs[t] for t in range(self.T) if orders[t] > 0)
        purchase_cost = sum(self.unit_costs[t] * orders[t] for t in range(self.T))
        holding_cost = sum(self.holding_costs[t] * inventory[t + 1]
                          for t in range(self.T))
        salvage = self.salvage_value * inventory[self.T]

        total_cost = setup_cost + purchase_cost + holding_cost - salvage

        return {
            'method': 'Dynamic Programming',
            'orders': orders,
            'inventory': inventory[:-1],
            'total_cost': total_cost,
            'setup_cost': setup_cost,
            'purchase_cost': purchase_cost,
            'holding_cost': holding_cost,
            'salvage_revenue': salvage
        }

    def price_speculation_analysis(self) -> Dict:
        """
        Analyze price speculation opportunities

        Identify periods where buying ahead is beneficial
        """

        speculation_opportunities = []

        for t in range(self.T - 1):
            # Compare buying now vs. buying later
            current_price = self.unit_costs[t]
            future_price = self.unit_costs[t + 1]

            price_increase = future_price - current_price
            holding_cost = self.holding_costs[t]

            # Net savings per unit if buy now for future demand
            net_savings = price_increase - holding_cost

            if net_savings > 0:
                speculation_opportunities.append({
                    'period': t + 1,
                    'current_price': current_price,
                    'future_price': future_price,
                    'price_increase': price_increase,
                    'holding_cost': holding_cost,
                    'net_savings_per_unit': net_savings
                })

        return speculation_opportunities

    def plot_time_varying_parameters(self):
        """Visualize how parameters change over time"""

        periods = np.arange(1, self.T + 1)

        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))

        # Demand
        ax1.plot(periods, self.demands, marker='o', linewidth=2, color='blue')
        ax1.set_xlabel('Period')
        ax1.set_ylabel('Demand (units)')
        ax1.set_title('Demand Over Time', fontweight='bold')
        ax1.grid(True, alpha=0.3)

        # Unit costs
        ax2.plot(periods, self.unit_costs, marker='s', linewidth=2, color='green')
        ax2.set_xlabel('Period')
        ax2.set_ylabel('Unit Cost ($)')
        ax2.set_title('Purchase Price Over Time', fontweight='bold')
        ax2.grid(True, alpha=0.3)

        # Setup costs
        ax3.plot(periods, self.setup_costs, marker='^', linewidth=2, color='red')
        ax3.set_xlabel('Period')
        ax3.set_ylabel('Setup Cost ($)')
        ax3.set_title('Setup Cost Over Time', fontweight='bold')
        ax3.grid(True, alpha=0.3)

        # Holding costs
        ax4.plot(periods, self.holding_costs, marker='d', linewidth=2, color='orange')
        ax4.set_xlabel('Period')
        ax4.set_ylabel('Holding Cost ($/unit/period)')
        ax4.set_title('Holding Cost Over Time', fontweight='bold')
        ax4.grid(True, alpha=0.3)

        plt.tight_layout()
        return plt

    def rolling_horizon_simulation(self, horizon_length: int = 6,
                                   actual_demands: Optional[List[float]] = None) -> Dict:
        """
        Simulate rolling horizon planning

        Replan every period with updated forecast

        Parameters:
        -----------
        horizon_length : int
            Length of planning horizon for each replan
        actual_demands : list, optional
            Actual realized demands (if different from forecast)
        """

        if actual_demands is None:
            actual_demands = self.demands

        actual_demands = np.array(actual_demands)

        orders = np.zeros(self.T)
        inventory = np.zeros(self.T + 1)
        inventory[0] = self.initial_inventory

        total_cost = 0

        for t in range(self.T):
            # Define planning horizon
            horizon_end = min(t + horizon_length, self.T)

            # Create subproblem for rolling horizon
            subproblem = DynamicLotSizing(
                demands=list(self.demands[t:horizon_end]),
                setup_costs=list(self.setup_costs[t:horizon_end]),
                holding_costs=list(self.holding_costs[t:horizon_end]),
                unit_costs=list(self.unit_costs[t:horizon_end]),
                initial_inventory=inventory[t],
                salvage_value=self.salvage_value
            )

            # Solve subproblem
            solution = subproblem.dynamic_programming()

            # Implement first-period decision only
            orders[t] = solution['orders'][0]

            # Update inventory based on actual demand
            inventory[t + 1] = inventory[t] + orders[t] - actual_demands[t]

            # Accumulate costs
            if orders[t] > 0:
                total_cost += self.setup_costs[t]
            total_cost += self.unit_costs[t] * orders[t]
            total_cost += self.holding_costs[t] * inventory[t + 1]

        return {
            'method': f'Rolling Horizon (H={horizon_length})',
            'orders': orders,
            'inventory': inventory[:-1],
            'total_cost': total_cost
        }


# Example: Seasonal Demand with Price Changes
def example_seasonal_with_price_change():
    """Example: Seasonal demand pattern with anticipated price increase"""

    print("\n" + "=" * 70)
    print("DYNAMIC LOT-SIZING: SEASONAL DEMAND WITH PRICE CHANGE")
    print("=" * 70)

    # 12-month planning horizon
    # Seasonal demand pattern (low winter, high summer)
    demands = [60, 50, 70, 80, 100, 120, 130, 120, 100, 80, 60, 50]

    # Price increase announced for month 6
    unit_costs = [10, 10, 10, 10, 10, 12, 12, 12, 12, 12, 12, 12]

    # Seasonal holding cost (higher in summer due to cooling requirements)
    holding_costs = [0.5, 0.5, 0.5, 0.6, 0.7, 0.8, 0.9, 0.8, 0.7, 0.6, 0.5, 0.5]

    # Constant setup cost
    setup_costs = [100] * 12

    problem = DynamicLotSizing(
        demands=demands,
        setup_costs=setup_costs,
        holding_costs=holding_costs,
        unit_costs=unit_costs,
        initial_inventory=0,
        salvage_value=5  # $5/unit salvage at end
    )

    print("\nProblem Overview:")
    print(f"  Planning Horizon: {problem.T} months")
    print(f"  Total Demand: {problem.demands.sum():.0f} units")
    print(f"  Price Change: ${unit_costs[0]} → ${unit_costs[5]} in month 6")

    # Analyze price speculation opportunities
    spec_opps = problem.price_speculation_analysis()

    if spec_opps:
        print("\n  Price Speculation Opportunities:")
        for opp in spec_opps:
            print(f"    Month {opp['period']}: Buy ahead to save "
                  f"${opp['net_savings_per_unit']:.2f}/unit")

    # Solve with DP
    print("\nSolving with Dynamic Programming...")
    solution = problem.dynamic_programming()

    print(f"\n{'=' * 70}")
    print("OPTIMAL SOLUTION")
    print("=" * 70)

    print(f"\n{'Total Cost:':<30} ${solution['total_cost']:,.2f}")
    print(f"{'Setup Cost:':<30} ${solution['setup_cost']:,.2f}")
    print(f"{'Purchase Cost:':<30} ${solution['purchase_cost']:,.2f}")
    print(f"{'Holding Cost:':<30} ${solution['holding_cost']:,.2f}")
    print(f"{'Salvage Revenue:':<30} ${solution['salvage_revenue']:,.2f}")

    print("\n  Optimal Order Plan:")
    print(f"\n  {'Month':<8} {'Demand':<10} {'Order':<10} {'End Inv':<12} "
          f"{'Unit Price':<12} {'Setup?'}")
    print("  " + "-" * 65)

    for t in range(problem.T):
        setup_indicator = "Yes" if solution['orders'][t] > 0 else "No"
        print(f"  {t+1:<8} {demands[t]:<10.0f} {solution['orders'][t]:<10.0f} "
              f"{solution['inventory'][t]:<12.0f} ${unit_costs[t]:<11.2f} {setup_indicator}")

    # Highlight speculation behavior
    print("\n  Key Insights:")
    if solution['orders'][4] > demands[4]:
        print(f"    • Month 5: Large order ({solution['orders'][4]:.0f} units) "
              f"to avoid price increase")
        print(f"      → Buying ahead at ${unit_costs[4]} vs ${unit_costs[5]} later")

    # Plot parameters and solution
    problem.plot_time_varying_parameters()
    plt.savefig('/tmp/dynamic_lot_sizing_parameters.png', dpi=300, bbox_inches='tight')
    print(f"\n  Parameter plots saved to /tmp/dynamic_lot_sizing_parameters.png")

    return problem, solution


# Example: Rolling Horizon
def example_rolling_horizon():
    """Example: Rolling horizon planning with forecast updates"""

    print("\n" + "=" * 70)
    print("ROLLING HORIZON PLANNING")
    print("=" * 70)

    # Forecasted demands
    forecast_demands = [100, 110, 95, 105, 100, 110, 105, 95, 100, 105, 110, 100]

    # Actual demands (slightly different from forecast)
    np.random.seed(42)
    actual_demands = forecast_demands + np.random.normal(0, 10, 12)
    actual_demands = np.maximum(actual_demands, 0)  # Non-negative

    problem = DynamicLotSizing(
        demands=forecast_demands,
        setup_costs=[150] * 12,
        holding_costs=[1.5] * 12,
        unit_costs=[20] * 12,
        initial_inventory=50
    )

    print("\nRolling Horizon Setup:")
    print(f"  Planning Horizon: {problem.T} periods")
    print(f"  Replanning Frequency: Every period")
    print(f"  Look-ahead Horizon: 6 periods")

    # Compare: Full horizon vs. Rolling horizon
    full_horizon = problem.dynamic_programming()
    rolling_6 = problem.rolling_horizon_simulation(horizon_length=6,
                                                   actual_demands=actual_demands)
    rolling_3 = problem.rolling_horizon_simulation(horizon_length=3,
                                                   actual_demands=actual_demands)

    print(f"\n{'=' * 70}")
    print("COMPARISON OF APPROACHES")
    print("=" * 70)

    comparison = pd.DataFrame([
        {'Method': 'Full Horizon (12 periods)', 'Total Cost': full_horizon['total_cost']},
        {'Method': 'Rolling Horizon (H=6)', 'Total Cost': rolling_6['total_cost']},
        {'Method': 'Rolling Horizon (H=3)', 'Total Cost': rolling_3['total_cost']}
    ])

    print("\n" + comparison.to_string(index=False))

    print(f"\n  Insight: Shorter horizons are more myopic but adapt to actual demand")

    return problem, rolling_6


if __name__ == "__main__":
    problem1, solution1 = example_seasonal_with_price_change()
    problem2, solution2 = example_rolling_horizon()
```

---

## Tools & Libraries

### Python Libraries
- `numpy`, `scipy`: Numerical computations
- `pulp`, `pyomo`: Optimization modeling
- Dynamic programming implementations

### Commercial Software
- **SAP APO**: Advanced planning with time-varying parameters
- **Blue Yonder**: Dynamic planning and optimization
- **Kinaxis**: RapidResponse with scenario planning
- **o9 Solutions**: Time-phased planning

---

## Common Challenges & Solutions

### Challenge: Computational Complexity
**Problem:** DP state space grows large
**Solutions:**
- Discretize inventory levels
- Use approximate DP
- Rolling horizon approach
- Heuristics for large problems

### Challenge: Forecast Uncertainty
**Problem:** Future demands/prices uncertain
**Solutions:**
- Rolling horizon with frequent replanning
- Stochastic DP for uncertainty
- Scenario-based planning
- Robust optimization

### Challenge: End-of-Horizon Effects
**Problem:** Artificial terminal behavior
**Solutions:**
- Use appropriate salvage values
- Extend horizon beyond decision period
- Rolling horizon mitigates this
- Terminal inventory targets

---

## Related Skills

- **economic-order-quantity**: Static EOQ models
- **lot-sizing-problems**: Multi-period deterministic lot-sizing
- **stochastic-inventory-models**: Uncertainty in demand
- **demand-forecasting**: Forecast time-varying demand
- **seasonal-planning**: Seasonal demand patterns
- **price-optimization**: Dynamic pricing strategies
