---
name: lot-sizing-problems
description: When the user wants to optimize production or order lot sizes over multiple periods, solve multi-period inventory planning problems, or determine when and how much to order/produce with time-varying demand. Also use when the user mentions "lot sizing," "lot-for-lot," "fixed order quantity," "POQ" (periodic order quantity), "part-period balancing," "Silver-Meal heuristic," "Wagner-Whitin algorithm," "least unit cost," "lot sizing with capacity constraints," or "multi-item lot sizing." For single-period problems, see newsvendor-problem. For time-varying lot sizing, see dynamic-lot-sizing.
---

# Lot-Sizing Problems

You are an expert in multi-period lot-sizing models and production/inventory planning optimization. Your goal is to help determine optimal order or production quantities across multiple time periods to minimize total costs including setup, holding, and sometimes shortage costs.

## Initial Assessment

Before solving lot-sizing problems, understand:

1. **Planning Context**
   - Planning horizon? (weeks, months, quarters)
   - Rolling or fixed horizon?
   - Demand pattern? (deterministic, forecast, actual orders)
   - Lead time considerations?

2. **Cost Structure**
   - Setup/ordering cost per order ($)?
   - Holding cost per unit per period ($/unit/period)?
   - Production/purchase cost per unit?
   - Backorder or shortage costs?
   - Cost structure time-varying?

3. **Capacity and Constraints**
   - Production capacity limits per period?
   - Storage capacity limits?
   - Minimum lot sizes or batch constraints?
   - Multiple items sharing capacity?

4. **Product Characteristics**
   - Single item or multiple items?
   - Bill of materials structure?
   - Product substitutability?
   - Shelf life or obsolescence?

5. **Operational Requirements**
   - Can backorders occur?
   - Must demand be satisfied immediately?
   - Multi-level production (BOM)?
   - Supplier constraints (MOQ, lead times)?

---

## Lot-Sizing Problem Fundamentals

### Problem Statement

Given:
- Planning horizon: T periods (t = 1, 2, ..., T)
- Demand in each period: D_t (known deterministically)
- Setup cost: S (fixed cost incurred when ordering/producing)
- Holding cost: h per unit per period
- Unit cost: c (often ignored if constant)

Decision:
- When to order/produce?
- How much to order/produce in each period?

Objective:
- Minimize total cost = setup costs + holding costs

### Key Lot-Sizing Policies

**1. Lot-for-Lot (L4L)**
- Order exactly what is needed each period: Q_t = D_t
- Minimizes holding cost (zero inventory)
- Maximizes setup costs
- Use when setup costs are very low

**2. Fixed Order Quantity (FOQ)**
- Order the same quantity Q every time
- Simple to implement
- May not match demand patterns well

**3. Economic Order Quantity (EOQ)**
- Use EOQ formula with average demand
- Assumes constant demand rate

**4. Period Order Quantity (POQ)**
- Order every N periods (N determined by EOQ)
- Combines multiple periods' demand

**5. Least Unit Cost (LUC)**
- Choose lot size that minimizes cost per unit
- Forward-looking heuristic

**6. Least Total Cost (LTC) / Part-Period Balancing**
- Balance setup and holding costs
- Choose lot when cumulative holding cost ≈ setup cost

**7. Silver-Meal Heuristic**
- Minimize average cost per period
- Popular practical heuristic

**8. Wagner-Whitin Algorithm**
- Dynamic programming approach
- Finds optimal solution for uncapacitated problem
- Polynomial time complexity O(T²)

---

## Python Implementation: Lot-Sizing Models

### Basic Lot-Sizing Heuristics

```python
import numpy as np
import pandas as pd
from typing import List, Dict, Tuple
import matplotlib.pyplot as plt

class LotSizingProblem:
    """
    Multi-period lot-sizing problem solver

    Implements various heuristics and optimal algorithm
    """

    def __init__(self, demands: List[float], setup_cost: float,
                 holding_cost: float, unit_cost: float = 0):
        """
        Parameters:
        -----------
        demands : list
            Demand for each period [D1, D2, ..., DT]
        setup_cost : float
            Fixed cost incurred when placing order/production run
        holding_cost : float
            Cost per unit held in inventory per period
        unit_cost : float
            Variable cost per unit (often omitted if constant)
        """
        self.demands = np.array(demands)
        self.T = len(demands)
        self.S = setup_cost
        self.h = holding_cost
        self.c = unit_cost

    def lot_for_lot(self) -> Dict:
        """
        Lot-for-Lot (L4L) policy: Order exactly demand each period

        Minimizes inventory but incurs setup cost every period
        """

        orders = self.demands.copy()
        inventory = np.zeros(self.T + 1)  # Inventory at end of each period
        setup_costs = np.zeros(self.T)
        holding_costs = np.zeros(self.T)

        for t in range(self.T):
            # Order arrives at start of period
            inventory[t] += orders[t]

            # Satisfy demand
            inventory[t] -= self.demands[t]

            # Costs
            if orders[t] > 0:
                setup_costs[t] = self.S
            holding_costs[t] = inventory[t] * self.h

            # Carry inventory forward
            inventory[t + 1] = inventory[t]

        total_setup = setup_costs.sum()
        total_holding = holding_costs.sum()
        total_cost = total_setup + total_holding

        return {
            'method': 'Lot-for-Lot',
            'orders': orders,
            'inventory': inventory[:-1],
            'setup_cost': total_setup,
            'holding_cost': total_holding,
            'total_cost': total_cost,
            'num_orders': (orders > 0).sum()
        }

    def fixed_order_quantity(self, Q: float) -> Dict:
        """
        Fixed Order Quantity: Order Q units whenever inventory insufficient

        Parameters:
        -----------
        Q : float
            Fixed order quantity
        """

        orders = np.zeros(self.T)
        inventory = np.zeros(self.T + 1)
        setup_costs = np.zeros(self.T)
        holding_costs = np.zeros(self.T)

        for t in range(self.T):
            # Check if order needed
            if inventory[t] < self.demands[t]:
                orders[t] = Q
                inventory[t] += Q

            # Satisfy demand
            inventory[t] -= self.demands[t]

            # Handle backorders if negative
            if inventory[t] < 0:
                # Need more orders
                num_orders = int(np.ceil(-inventory[t] / Q))
                orders[t] += num_orders * Q
                inventory[t] += num_orders * Q

            # Costs
            if orders[t] > 0:
                setup_costs[t] = self.S * (orders[t] / Q)  # Proportional setups
            holding_costs[t] = max(0, inventory[t]) * self.h

            # Carry forward
            inventory[t + 1] = inventory[t]

        total_setup = setup_costs.sum()
        total_holding = holding_costs.sum()
        total_cost = total_setup + total_holding

        return {
            'method': f'FOQ (Q={Q})',
            'orders': orders,
            'inventory': inventory[:-1],
            'setup_cost': total_setup,
            'holding_cost': total_holding,
            'total_cost': total_cost,
            'num_orders': (orders > 0).sum()
        }

    def silver_meal(self) -> Dict:
        """
        Silver-Meal Heuristic

        Iteratively add periods to lot, stop when average cost per period increases
        """

        orders = np.zeros(self.T)
        inventory = np.zeros(self.T + 1)
        t = 0

        while t < self.T:
            # Determine lot size starting at period t
            best_periods = 1
            min_avg_cost = float('inf')

            for k in range(1, self.T - t + 1):
                # Consider covering periods t through t+k-1
                # Cost = Setup cost + holding cost for carrying inventory

                total_demand = sum(self.demands[t:t+k])
                holding_cost = sum((j - t) * self.demands[t+j] * self.h
                                  for j in range(k))

                total_cost = self.S + holding_cost
                avg_cost = total_cost / k

                if avg_cost < min_avg_cost:
                    min_avg_cost = avg_cost
                    best_periods = k
                else:
                    # Average cost increased, stop
                    break

            # Place order for best_periods worth of demand
            order_qty = sum(self.demands[t:t+best_periods])
            orders[t] = order_qty

            # Update inventory levels
            inv = order_qty
            for j in range(best_periods):
                if t + j < self.T:
                    inventory[t + j] = inv
                    inv -= self.demands[t + j]

            t += best_periods

        # Calculate costs
        setup_costs = np.where(orders > 0, self.S, 0)
        holding_costs = inventory[:-1] * self.h

        return {
            'method': 'Silver-Meal',
            'orders': orders,
            'inventory': inventory[:-1],
            'setup_cost': setup_costs.sum(),
            'holding_cost': holding_costs.sum(),
            'total_cost': setup_costs.sum() + holding_costs.sum(),
            'num_orders': (orders > 0).sum()
        }

    def least_unit_cost(self) -> Dict:
        """
        Least Unit Cost (LUC) Heuristic

        For each order, add periods until cost per unit increases
        """

        orders = np.zeros(self.T)
        inventory = np.zeros(self.T + 1)
        t = 0

        while t < self.T:
            min_unit_cost = float('inf')
            best_periods = 1

            for k in range(1, self.T - t + 1):
                # Total demand covered
                total_demand = sum(self.demands[t:t+k])

                # Holding cost
                holding_cost = sum((j - t) * self.demands[t+j] * self.h
                                  for j in range(k))

                # Total cost
                total_cost = self.S + holding_cost

                # Unit cost
                unit_cost = total_cost / total_demand

                if unit_cost < min_unit_cost:
                    min_unit_cost = unit_cost
                    best_periods = k
                else:
                    break

            # Place order
            order_qty = sum(self.demands[t:t+best_periods])
            orders[t] = order_qty

            # Update inventory
            inv = order_qty
            for j in range(best_periods):
                if t + j < self.T:
                    inventory[t + j] = inv
                    inv -= self.demands[t + j]

            t += best_periods

        # Calculate costs
        setup_costs = np.where(orders > 0, self.S, 0)
        holding_costs = inventory[:-1] * self.h

        return {
            'method': 'Least Unit Cost',
            'orders': orders,
            'inventory': inventory[:-1],
            'setup_cost': setup_costs.sum(),
            'holding_cost': holding_costs.sum(),
            'total_cost': setup_costs.sum() + holding_costs.sum(),
            'num_orders': (orders > 0).sum()
        }

    def wagner_whitin(self) -> Dict:
        """
        Wagner-Whitin Algorithm

        Dynamic programming approach - finds optimal solution
        for uncapacitated lot-sizing problem

        Time complexity: O(T²)
        """

        T = self.T
        # F[t] = minimum cost for periods 1..t
        F = np.full(T + 1, np.inf)
        F[0] = 0

        # Predecessor: which period did we last order from?
        pred = np.zeros(T + 1, dtype=int)

        # DP forward pass
        for t in range(1, T + 1):
            for j in range(t):
                # Consider ordering in period j to cover demand through period t
                # Cost = F[j] + setup cost + holding cost

                # Holding cost for covering periods j+1 through t
                holding_cost = 0
                for k in range(j + 1, t + 1):
                    # Hold demand[k-1] for (k - j - 1) periods
                    holding_cost += (k - j - 1) * self.demands[k - 1] * self.h

                cost = F[j] + self.S + holding_cost

                if cost < F[t]:
                    F[t] = cost
                    pred[t] = j

        # Backtrack to find order periods
        orders = np.zeros(T)
        t = T
        while t > 0:
            j = pred[t]
            # Order in period j to cover through period t
            order_qty = sum(self.demands[j:t])
            orders[j] = order_qty
            t = j

        # Reconstruct inventory
        inventory = np.zeros(T + 1)
        for t in range(T):
            inventory[t] += orders[t]
            inventory[t] -= self.demands[t]
            inventory[t + 1] = inventory[t]

        # Calculate costs
        setup_costs = np.where(orders > 0, self.S, 0)
        holding_costs = inventory[:-1] * self.h

        return {
            'method': 'Wagner-Whitin (Optimal)',
            'orders': orders,
            'inventory': inventory[:-1],
            'setup_cost': setup_costs.sum(),
            'holding_cost': holding_costs.sum(),
            'total_cost': setup_costs.sum() + holding_costs.sum(),
            'num_orders': (orders > 0).sum(),
            'optimal': True
        }

    def compare_methods(self) -> pd.DataFrame:
        """Compare all lot-sizing methods"""

        methods = [
            self.lot_for_lot(),
            self.silver_meal(),
            self.least_unit_cost(),
            self.wagner_whitin()
        ]

        # Add FOQ with EOQ-based quantity
        avg_demand = self.demands.mean()
        if avg_demand > 0:
            eoq = np.sqrt(2 * avg_demand * self.T * self.S / self.h)
            methods.append(self.fixed_order_quantity(eoq))

        results = []
        for method in methods:
            results.append({
                'Method': method['method'],
                'Total Cost': method['total_cost'],
                'Setup Cost': method['setup_cost'],
                'Holding Cost': method['holding_cost'],
                'Num Orders': method['num_orders'],
                'Avg Inventory': method['inventory'].mean()
            })

        df = pd.DataFrame(results)
        df = df.sort_values('Total Cost')

        return df

    def plot_solution(self, solution: Dict):
        """Visualize lot-sizing solution"""

        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(14, 10))

        periods = np.arange(1, self.T + 1)

        # Plot 1: Demand and Orders
        ax1.bar(periods, self.demands, alpha=0.6, label='Demand', color='blue')
        order_periods = periods[solution['orders'] > 0]
        order_qtys = solution['orders'][solution['orders'] > 0]
        ax1.bar(order_periods, order_qtys, alpha=0.8, label='Orders', color='green')

        ax1.set_xlabel('Period', fontsize=11)
        ax1.set_ylabel('Quantity', fontsize=11)
        ax1.set_title(f"{solution['method']}: Demand and Order Pattern",
                     fontsize=12, fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # Plot 2: Inventory Levels
        ax2.plot(periods, solution['inventory'], marker='o', linewidth=2,
                color='orange', label='Ending Inventory')
        ax2.fill_between(periods, 0, solution['inventory'], alpha=0.3, color='orange')
        ax2.axhline(y=solution['inventory'].mean(), linestyle='--',
                   color='red', label=f"Avg Inv = {solution['inventory'].mean():.1f}")

        ax2.set_xlabel('Period', fontsize=11)
        ax2.set_ylabel('Inventory Level', fontsize=11)
        ax2.set_title('Inventory Over Time', fontsize=12, fontweight='bold')
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        # Plot 3: Costs
        setup_costs = np.where(solution['orders'] > 0, self.S, 0)
        holding_costs = solution['inventory'] * self.h

        width = 0.35
        ax3.bar(periods - width/2, setup_costs, width, label='Setup Cost',
               color='red', alpha=0.7)
        ax3.bar(periods + width/2, holding_costs, width, label='Holding Cost',
               color='blue', alpha=0.7)

        ax3.set_xlabel('Period', fontsize=11)
        ax3.set_ylabel('Cost ($)', fontsize=11)
        ax3.set_title('Period Costs', fontsize=12, fontweight='bold')
        ax3.legend()
        ax3.grid(True, alpha=0.3)

        plt.tight_layout()
        return plt


# Example Usage
def example_lot_sizing():
    """Example: Multi-period lot-sizing problem"""

    print("\n" + "=" * 70)
    print("MULTI-PERIOD LOT-SIZING PROBLEM")
    print("=" * 70)

    # 12-period planning horizon with varying demand
    demands = [50, 60, 40, 80, 100, 90, 70, 60, 50, 80, 90, 100]

    problem = LotSizingProblem(
        demands=demands,
        setup_cost=200,      # $200 per order
        holding_cost=2,      # $2 per unit per period
        unit_cost=10         # $10 per unit (often ignored)
    )

    print("\nProblem Data:")
    print(f"  Planning Horizon: {problem.T} periods")
    print(f"  Setup Cost: ${problem.S}")
    print(f"  Holding Cost: ${problem.h}/unit/period")
    print(f"  Total Demand: {problem.demands.sum():.0f} units")
    print(f"  Average Demand: {problem.demands.mean():.1f} units/period")

    print("\n  Period-by-period demand:")
    for t, d in enumerate(demands, 1):
        print(f"    Period {t:2d}: {d:3.0f} units")

    # Compare all methods
    print("\n" + "=" * 70)
    print("COMPARISON OF LOT-SIZING METHODS")
    print("=" * 70)

    comparison = problem.compare_methods()
    print("\n" + comparison.to_string(index=False))

    # Analyze optimal solution
    optimal = problem.wagner_whitin()

    print("\n" + "=" * 70)
    print(f"OPTIMAL SOLUTION: {optimal['method']}")
    print("=" * 70)

    print(f"\n{'Total Cost:':<25} ${optimal['total_cost']:,.2f}")
    print(f"{'Setup Cost:':<25} ${optimal['setup_cost']:,.2f}")
    print(f"{'Holding Cost:':<25} ${optimal['holding_cost']:,.2f}")
    print(f"{'Number of Orders:':<25} {optimal['num_orders']}")
    print(f"{'Average Inventory:':<25} {optimal['inventory'].mean():.1f} units")

    print("\n  Order Schedule:")
    for t in range(problem.T):
        if optimal['orders'][t] > 0:
            print(f"    Period {t+1}: Order {optimal['orders'][t]:.0f} units")

    # Visualize
    problem.plot_solution(optimal)
    plt.savefig('/tmp/lot_sizing_optimal.png', dpi=300, bbox_inches='tight')
    print(f"\nOptimal solution plot saved to /tmp/lot_sizing_optimal.png")

    return problem, optimal


if __name__ == "__main__":
    example_lot_sizing()
```

---

## Capacitated Lot-Sizing

### Single-Item Capacitated Lot-Sizing Problem (CLSP)

```python
from pulp import *

class CapacitatedLotSizing:
    """
    Capacitated Lot-Sizing Problem (CLSP)

    Production capacity constraints in each period
    """

    def __init__(self, demands: List[float], setup_cost: float,
                 holding_cost: float, production_cost: float,
                 capacity: List[float]):
        """
        Parameters:
        -----------
        demands : list
            Demand for each period
        setup_cost : float
            Fixed setup cost per period
        holding_cost : float
            Holding cost per unit per period
        production_cost : float
            Variable production cost per unit
        capacity : list
            Production capacity each period
        """
        self.demands = np.array(demands)
        self.T = len(demands)
        self.S = setup_cost
        self.h = holding_cost
        self.c = production_cost
        self.capacity = np.array(capacity)

    def solve_mip(self) -> Dict:
        """
        Solve using Mixed-Integer Programming

        Decision variables:
        - x_t: production quantity in period t
        - y_t: binary, 1 if production occurs in period t
        - I_t: inventory at end of period t
        """

        # Create problem
        prob = LpProblem("Capacitated_Lot_Sizing", LpMinimize)

        # Decision variables
        x = [LpVariable(f"x_{t}", lowBound=0) for t in range(self.T)]
        y = [LpVariable(f"y_{t}", cat='Binary') for t in range(self.T)]
        I = [LpVariable(f"I_{t}", lowBound=0) for t in range(self.T + 1)]

        # Objective: minimize total cost
        prob += (lpSum([self.S * y[t] + self.c * x[t] + self.h * I[t]
                       for t in range(self.T)]))

        # Constraints

        # Initial inventory
        prob += I[0] == 0

        # Inventory balance
        for t in range(self.T):
            prob += I[t + 1] == I[t] + x[t] - self.demands[t]

        # Production capacity
        for t in range(self.T):
            prob += x[t] <= self.capacity[t] * y[t]

        # Solve
        prob.solve(PULP_CBC_CMD(msg=0))

        # Extract solution
        production = np.array([x[t].varValue for t in range(self.T)])
        setup_decisions = np.array([y[t].varValue for t in range(self.T)])
        inventory = np.array([I[t].varValue for t in range(self.T + 1)])

        # Calculate costs
        setup_cost = self.S * setup_decisions.sum()
        prod_cost = self.c * production.sum()
        holding_cost = self.h * inventory[:-1].sum()
        total_cost = value(prob.objective)

        return {
            'status': LpStatus[prob.status],
            'production': production,
            'inventory': inventory[:-1],
            'setups': setup_decisions,
            'total_cost': total_cost,
            'setup_cost': setup_cost,
            'production_cost': prod_cost,
            'holding_cost': holding_cost,
            'num_setups': int(setup_decisions.sum())
        }


# Example: Capacitated Lot-Sizing
def example_capacitated():
    """Example: Lot-sizing with capacity constraints"""

    print("\n" + "=" * 70)
    print("CAPACITATED LOT-SIZING PROBLEM")
    print("=" * 70)

    demands = [40, 60, 80, 50, 70, 90]
    capacity = [100, 100, 100, 100, 100, 100]  # Max production per period

    problem = CapacitatedLotSizing(
        demands=demands,
        setup_cost=300,
        holding_cost=2,
        production_cost=10,
        capacity=capacity
    )

    print("\nProblem Data:")
    print(f"  Periods: {problem.T}")
    print(f"  Setup Cost: ${problem.S}")
    print(f"  Holding Cost: ${problem.h}/unit/period")
    print(f"  Production Cost: ${problem.c}/unit")
    print(f"  Capacity per Period: {capacity[0]} units")

    print("\n  Period Demands:")
    for t, d in enumerate(demands, 1):
        print(f"    Period {t}: {d} units")

    # Solve
    solution = problem.solve_mip()

    print(f"\n{'=' * 70}")
    print(f"OPTIMAL SOLUTION")
    print("=" * 70)

    print(f"\n{'Status:':<25} {solution['status']}")
    print(f"{'Total Cost:':<25} ${solution['total_cost']:,.2f}")
    print(f"{'Setup Cost:':<25} ${solution['setup_cost']:,.2f}")
    print(f"{'Production Cost:':<25} ${solution['production_cost']:,.2f}")
    print(f"{'Holding Cost:':<25} ${solution['holding_cost']:,.2f}")
    print(f"{'Number of Setups:':<25} {solution['num_setups']}")

    print("\n  Production Schedule:")
    for t in range(problem.T):
        if solution['production'][t] > 0.01:
            print(f"    Period {t+1}: Produce {solution['production'][t]:.0f} units, "
                  f"Ending Inv: {solution['inventory'][t]:.0f}")

    return problem, solution


if __name__ == "__main__":
    example_capacitated()
```

---

## Tools & Libraries

### Python Libraries

**Optimization:**
- `pulp`: Linear/mixed-integer programming
- `pyomo`: Optimization modeling
- `scipy.optimize`: General optimization
- `ortools`: Google OR-Tools

**Numerical:**
- `numpy`, `pandas`: Data manipulation

### Commercial Software

**Production Planning:**
- **SAP APO**: Advanced Planning & Optimization with lot-sizing
- **Oracle Demantra**: Demand and supply planning
- **Blue Yonder**: Supply chain planning
- **Kinaxis RapidResponse**: Integrated planning

**MRP Systems:**
- Most ERP systems have lot-sizing rules (SAP, Oracle, Microsoft Dynamics)

---

## Common Challenges & Solutions

### Challenge: Capacity Constraints

**Problem:**
- Production capacity insufficient in some periods
- Cannot produce when needed

**Solutions:**
- Use capacitated lot-sizing MIP model
- Consider overtime production (higher cost)
- Build inventory in advance during low-demand periods
- Outsource production for peak periods

### Challenge: Setup Time vs. Setup Cost

**Problem:**
- Setups consume both time (capacity) and cost
- Simple models consider only cost

**Solutions:**
- Include setup time in capacity constraints
- Use CLSP with setup times
- Sequence-dependent setup times → more complex models

### Challenge: Multi-Item Lot-Sizing

**Problem:**
- Multiple products share same production capacity
- Joint setup costs or time

**Solutions:**
- Multi-item CLSP formulation
- Proportional Lot-Sizing (PROPLS) heuristic
- Priority-based allocation
- See multi-item examples in code

### Challenge: Uncertainty in Demand

**Problem:**
- Lot-sizing assumes deterministic demand
- Real demand is uncertain

**Solutions:**
- Use rolling horizon planning (replan each period)
- Add safety stock to demands
- Robust optimization with demand scenarios
- See **stochastic-inventory-models** and **dynamic-lot-sizing**

---

## Related Skills

- **economic-order-quantity**: Single-period lot-sizing
- **dynamic-lot-sizing**: Time-varying parameters and stochastic demand
- **stochastic-inventory-models**: Probabilistic inventory models
- **master-production-scheduling**: Aggregate production planning
- **capacity-planning**: Long-term capacity decisions
- **production-scheduling**: Short-term scheduling
