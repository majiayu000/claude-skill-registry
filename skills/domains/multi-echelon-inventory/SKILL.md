---
name: multi-echelon-inventory
description: When the user wants to optimize inventory across multiple network locations, implement multi-echelon inventory policies, or coordinate stock levels between warehouses and distribution centers. Also use when the user mentions "network inventory optimization," "multi-stage inventory," "supply chain network," "echelon stock," "installation stock," "base stock policies," "guaranteed service model," "distribution requirements planning (DRP)," or "serial/arborescent/general network structures." For single-location inventory, see inventory-optimization. For routing with inventory, see inventory-routing-problem.
---

# Multi-Echelon Inventory Optimization

You are an expert in multi-echelon inventory systems and network-wide inventory optimization. Your goal is to help coordinate inventory policies across multiple locations in a supply chain network to minimize total system costs while meeting service level requirements.

## Initial Assessment

Before optimizing multi-echelon inventory, understand:

1. **Network Structure**
   - How many echelons/stages? (e.g., central DC → regional DCs → stores)
   - Network topology? (serial, distribution/arborescent, general)
   - Number of locations at each level?
   - Current inventory positioning strategy?

2. **Product Characteristics**
   - SKU complexity? (how many products)
   - Product value and velocity (ABC classification)?
   - Product shelf life or obsolescence concerns?
   - Cannibalization or substitution effects?

3. **Demand Patterns**
   - Where does external demand occur? (end customers at retail stores)
   - Demand variability at each location?
   - Correlation between location demands?
   - Seasonality or trends?

4. **Supply Chain Flows**
   - Lead times between echelons?
   - Replenishment policies at each location?
   - Can locations transship laterally (between same-level)?
   - Emergency/expedited shipping available?

5. **Cost Structure**
   - Holding costs at each echelon?
   - Transportation costs between locations?
   - Ordering/replenishment costs?
   - Stockout or backorder penalties?
   - Are costs location-dependent?

6. **Service Requirements**
   - Target service levels per location or overall?
   - Critical vs. non-critical items?
   - Customer priorities?

---

## Multi-Echelon System Fundamentals

### Network Structures

**1. Serial System (Sequential)**
```
Supplier → Factory → Central DC → Regional DC → Retail Store → Customer
   (0)       (1)         (2)           (3)          (4)
```

**2. Distribution/Arborescent System (Tree)**
```
                 Central Warehouse
                /        |        \
             DC1        DC2        DC3
            / | \      / | \      / | \
          S1 S2 S3   S4 S5 S6   S7 S8 S9
```

**3. General Network**
- Multiple suppliers
- Lateral transshipment between peers
- Complex flows

### Key Concepts

**Installation Stock (IS):**
- Physical inventory at a specific location
- What you would count in a physical inventory

**Echelon Stock (ES):**
- Installation stock + all downstream stock in the system
- ES(i) = IS(i) + Σ ES(j) for all downstream locations j

**Base Stock Policy:**
- Order-up-to policy: when inventory position ≤ S, order to bring position to S
- S = base stock level

**Guaranteed Service Model (GSM):**
- Each upstream location guarantees service time to downstream
- Downstream locations can plan based on guaranteed service times
- Decouples multi-echelon problem into single-stage problems

---

## Python Implementation: Multi-Echelon Models

### Serial System with Base Stock Policies

```python
import numpy as np
import pandas as pd
from scipy import stats
from typing import List, Dict, Tuple
import matplotlib.pyplot as plt
from collections import deque

class SerialMultiEchelonSystem:
    """
    Serial multi-echelon inventory system with base stock policies

    Models a sequential supply chain: Supplier → Stage 1 → Stage 2 → ... → Customer
    """

    def __init__(self, num_stages: int, lead_times: List[int],
                 holding_costs: List[float], demand_mean: float,
                 demand_std: float):
        """
        Parameters:
        -----------
        num_stages : int
            Number of stages in the serial system
        lead_times : list
            Lead time (in periods) for each stage [L1, L2, ..., Ln]
        holding_costs : list
            Holding cost per unit per period at each stage [h1, h2, ..., hn]
        demand_mean : float
            Mean demand per period at final stage
        demand_std : float
            Standard deviation of demand per period
        """
        self.num_stages = num_stages
        self.lead_times = np.array(lead_times)
        self.holding_costs = np.array(holding_costs)
        self.demand_mean = demand_mean
        self.demand_std = demand_std

        # Echelon holding costs
        self.echelon_holding_costs = self._calculate_echelon_holding_costs()

    def _calculate_echelon_holding_costs(self) -> np.ndarray:
        """
        Calculate echelon holding costs

        Echelon holding cost h'(j) = h(j) - h(j+1)
        where h(j) is installation holding cost at stage j
        """
        echelon_costs = np.zeros(self.num_stages)

        for j in range(self.num_stages):
            echelon_costs[j] = self.holding_costs[j]
            if j < self.num_stages - 1:
                echelon_costs[j] -= self.holding_costs[j + 1]

        return echelon_costs

    def calculate_base_stock_levels(self, service_level: float = 0.95) -> Dict:
        """
        Calculate optimal base stock levels using Clark-Scarf decomposition

        For serial system with base stock policies, can decompose into
        single-stage newsvendor problems for each echelon

        Parameters:
        -----------
        service_level : float
            Target service level (e.g., 0.95 for 95%)

        Returns:
        --------
        dict with base stock levels and costs
        """

        z = stats.norm.ppf(service_level)

        base_stocks = np.zeros(self.num_stages)
        safety_stocks = np.zeros(self.num_stages)

        # Work backwards from downstream to upstream
        for j in range(self.num_stages - 1, -1, -1):
            # Cumulative lead time from stage j to end customer
            if j == self.num_stages - 1:
                cumulative_lt = self.lead_times[j]
            else:
                cumulative_lt = np.sum(self.lead_times[j:])

            # Expected demand during cumulative lead time
            expected_demand = self.demand_mean * cumulative_lt

            # Standard deviation during cumulative lead time
            std_demand = self.demand_std * np.sqrt(cumulative_lt)

            # Safety stock at this echelon
            safety_stock = z * std_demand

            # Base stock level (echelon stock)
            base_stock = expected_demand + safety_stock

            base_stocks[j] = base_stock
            safety_stocks[j] = safety_stock

        # Calculate expected costs
        total_holding_cost = np.sum(self.echelon_holding_costs * safety_stocks)

        return {
            'base_stock_levels': base_stocks,
            'safety_stocks': safety_stocks,
            'echelon_holding_costs': self.echelon_holding_costs,
            'total_holding_cost': total_holding_cost,
            'service_level': service_level
        }

    def optimize_service_level(self, max_holding_cost: float) -> Dict:
        """
        Find optimal service level given a holding cost budget

        Parameters:
        -----------
        max_holding_cost : float
            Maximum acceptable holding cost per period

        Returns:
        --------
        Optimal service level and corresponding base stocks
        """

        # Binary search for optimal service level
        sl_low, sl_high = 0.50, 0.9999

        while sl_high - sl_low > 0.0001:
            sl_mid = (sl_low + sl_high) / 2
            result = self.calculate_base_stock_levels(sl_mid)

            if result['total_holding_cost'] <= max_holding_cost:
                sl_low = sl_mid
            else:
                sl_high = sl_mid

        optimal_result = self.calculate_base_stock_levels(sl_low)

        return optimal_result

    def simulate(self, num_periods: int, base_stock_levels: np.ndarray,
                review_period: int = 1) -> pd.DataFrame:
        """
        Simulate multi-echelon system with base stock policies

        Parameters:
        -----------
        num_periods : int
            Number of periods to simulate
        base_stock_levels : array
            Base stock (order-up-to) level for each stage
        review_period : int
            How often to review inventory (default 1 = continuous)

        Returns:
        --------
        DataFrame with inventory positions, orders, and costs
        """

        # Initialize inventory positions (start at base stock)
        inventory_position = base_stock_levels.copy()
        inventory_on_hand = base_stock_levels.copy()

        # Order pipelines (orders in transit)
        order_pipelines = [deque() for _ in range(self.num_stages)]

        results = []

        for t in range(num_periods):
            # Generate customer demand (at final stage)
            demand = max(0, np.random.normal(self.demand_mean, self.demand_std))

            # Process orders arriving at each stage
            for j in range(self.num_stages):
                if len(order_pipelines[j]) > 0:
                    # Check for arriving orders
                    arrivals = []
                    for order in order_pipelines[j]:
                        if order['arrival_period'] == t:
                            arrivals.append(order)

                    for order in arrivals:
                        inventory_on_hand[j] += order['quantity']
                        order_pipelines[j].remove(order)

            # Satisfy demand at final stage
            actual_demand_filled = min(demand, inventory_on_hand[-1])
            stockout = demand - actual_demand_filled
            inventory_on_hand[-1] -= actual_demand_filled

            # Review and order at each stage (if review period)
            orders_placed = np.zeros(self.num_stages)

            if t % review_period == 0:
                for j in range(self.num_stages - 1, -1, -1):
                    # Calculate inventory position
                    pipeline_inventory = sum(order['quantity']
                                           for order in order_pipelines[j])
                    inventory_position[j] = inventory_on_hand[j] + pipeline_inventory

                    # Order up to base stock
                    order_qty = max(0, base_stock_levels[j] - inventory_position[j])

                    if order_qty > 0:
                        # Place order (arrives after lead time)
                        order_pipelines[j].append({
                            'quantity': order_qty,
                            'order_period': t,
                            'arrival_period': t + self.lead_times[j]
                        })
                        orders_placed[j] = order_qty

            # Calculate holding costs
            holding_cost = np.sum(self.holding_costs * inventory_on_hand)

            results.append({
                'period': t,
                'demand': demand,
                'stockout': stockout,
                'fill_rate': actual_demand_filled / demand if demand > 0 else 1.0,
                **{f'inv_stage_{j}': inventory_on_hand[j] for j in range(self.num_stages)},
                **{f'order_stage_{j}': orders_placed[j] for j in range(self.num_stages)},
                'holding_cost': holding_cost
            })

        return pd.DataFrame(results)


# Example: Serial System
def example_serial_system():
    """Example: 3-stage serial supply chain"""

    print("\n" + "=" * 70)
    print("MULTI-ECHELON SERIAL SYSTEM OPTIMIZATION")
    print("=" * 70)

    # Define system: Supplier → Warehouse → Distribution Center → Retailer
    system = SerialMultiEchelonSystem(
        num_stages=3,
        lead_times=[10, 5, 2],          # Days: Supplier→WH, WH→DC, DC→Retail
        holding_costs=[1.0, 2.0, 5.0],  # $/unit/day: WH, DC, Retail
        demand_mean=100,                # Daily demand at retail
        demand_std=20                   # Demand variability
    )

    print("\nSystem Configuration:")
    print(f"  Number of Stages: {system.num_stages}")
    print(f"  Lead Times: {system.lead_times} days")
    print(f"  Installation Holding Costs: ${system.holding_costs} per unit per day")
    print(f"  Echelon Holding Costs: ${system.echelon_holding_costs} per unit per day")
    print(f"  Demand: Mean={system.demand_mean}, Std={system.demand_std}")

    # Calculate optimal base stocks for 95% service level
    result = system.calculate_base_stock_levels(service_level=0.95)

    print(f"\n{'Optimal Base Stock Levels (95% Service Level):'}")
    print(f"\n{'Stage':<20} {'Lead Time':<12} {'Base Stock':<15} {'Safety Stock':<15} {'Echelon Cost':<15}")
    print("-" * 77)

    stage_names = ['Warehouse', 'Distribution', 'Retail']
    for j in range(system.num_stages):
        print(f"{stage_names[j]:<20} {system.lead_times[j]:<12} "
              f"{result['base_stock_levels'][j]:<15.0f} "
              f"{result['safety_stocks'][j]:<15.0f} "
              f"${result['echelon_holding_costs'][j]:<14.2f}")

    print(f"\n{'Total Expected Holding Cost:':<40} ${result['total_holding_cost']:.2f} per period")

    # Simulate system
    print("\nSimulating system for 365 days...")
    np.random.seed(42)
    simulation = system.simulate(
        num_periods=365,
        base_stock_levels=result['base_stock_levels'],
        review_period=1
    )

    # Analyze results
    avg_fill_rate = simulation['fill_rate'].mean()
    total_stockouts = simulation['stockout'].sum()
    avg_holding_cost = simulation['holding_cost'].mean()

    print(f"\n{'Simulation Results (365 days):'}")
    print(f"  {'Average Fill Rate:':<35} {avg_fill_rate:.2%}")
    print(f"  {'Total Stockout Units:':<35} {total_stockouts:.0f}")
    print(f"  {'Average Daily Holding Cost:':<35} ${avg_holding_cost:.2f}")
    print(f"  {'Average Inventory per Stage:':<35}")

    for j in range(system.num_stages):
        avg_inv = simulation[f'inv_stage_{j}'].mean()
        print(f"    {stage_names[j]:<32} {avg_inv:.0f} units")

    return system, result, simulation


if __name__ == "__main__":
    system, result, simulation = example_serial_system()
```

---

## Distribution System (Arborescent Network)

### Two-Echelon Distribution System

```python
class TwoEchelonDistributionSystem:
    """
    Two-echelon distribution system: 1 central warehouse → N retailers

    Implements guaranteed service model approach
    """

    def __init__(self, num_retailers: int, central_lead_time: int,
                 delivery_lead_times: List[int], central_holding_cost: float,
                 retailer_holding_costs: List[float], demands_mean: List[float],
                 demands_std: List[float]):
        """
        Parameters:
        -----------
        num_retailers : int
            Number of retail locations
        central_lead_time : int
            Lead time from supplier to central warehouse
        delivery_lead_times : list
            Lead time from central to each retailer
        central_holding_cost : float
            Holding cost per unit per period at central warehouse
        retailer_holding_costs : list
            Holding cost per unit per period at each retailer
        demands_mean : list
            Mean demand per period at each retailer
        demands_std : list
            Std dev of demand per period at each retailer
        """
        self.num_retailers = num_retailers
        self.L0 = central_lead_time
        self.Li = np.array(delivery_lead_times)
        self.h0 = central_holding_cost
        self.hi = np.array(retailer_holding_costs)
        self.mu = np.array(demands_mean)
        self.sigma = np.array(demands_std)

    def calculate_base_stocks_guaranteed_service(self,
                                                 retailer_service_levels: List[float],
                                                 central_service_level: float) -> Dict:
        """
        Calculate base stocks using Guaranteed Service Model

        Approach:
        1. Each retailer sets safety stock based on delivery lead time
        2. Central warehouse sets safety stock to guarantee service time
        """

        # Retailer base stocks
        retailer_base_stocks = np.zeros(self.num_retailers)
        retailer_safety_stocks = np.zeros(self.num_retailers)

        for i in range(self.num_retailers):
            z_i = stats.norm.ppf(retailer_service_levels[i])

            # Expected demand during delivery lead time
            expected_demand = self.mu[i] * self.Li[i]

            # Safety stock
            safety_stock = z_i * self.sigma[i] * np.sqrt(self.Li[i])

            retailer_base_stocks[i] = expected_demand + safety_stock
            retailer_safety_stocks[i] = safety_stock

        # Central warehouse base stock
        z_0 = stats.norm.ppf(central_service_level)

        # Aggregate demand statistics
        total_mean_demand = np.sum(self.mu)
        # Assuming independent retailer demands
        total_std_demand = np.sqrt(np.sum(self.sigma ** 2))

        # Total lead time (external + internal)
        total_lt = self.L0 + np.max(self.Li)

        # Central expected demand
        central_expected = total_mean_demand * total_lt

        # Central safety stock
        central_safety_stock = z_0 * total_std_demand * np.sqrt(total_lt)

        central_base_stock = central_expected + central_safety_stock

        # Calculate costs
        retailer_holding_cost = np.sum(self.hi * retailer_safety_stocks)
        central_holding_cost = self.h0 * central_safety_stock
        total_holding_cost = retailer_holding_cost + central_holding_cost

        return {
            'central_base_stock': central_base_stock,
            'central_safety_stock': central_safety_stock,
            'retailer_base_stocks': retailer_base_stocks,
            'retailer_safety_stocks': retailer_safety_stocks,
            'central_holding_cost': central_holding_cost,
            'retailer_holding_cost': retailer_holding_cost,
            'total_holding_cost': total_holding_cost
        }

    def optimize_service_levels(self, total_holding_cost_budget: float) -> Dict:
        """
        Optimize service levels subject to holding cost budget

        This is a simplified heuristic approach
        """

        from scipy.optimize import minimize

        def objective(service_levels):
            """Minimize negative of total service level (maximize service)"""
            retailer_sls = service_levels[:self.num_retailers]
            central_sl = service_levels[self.num_retailers]

            # Penalize if service levels are too different
            return -np.sum(retailer_sls) - central_sl

        def holding_cost_constraint(service_levels):
            """Total holding cost must be <= budget"""
            retailer_sls = service_levels[:self.num_retailers]
            central_sl = service_levels[self.num_retailers]

            result = self.calculate_base_stocks_guaranteed_service(
                retailer_sls.tolist(), central_sl
            )

            return total_holding_cost_budget - result['total_holding_cost']

        # Initial guess: 95% everywhere
        x0 = np.full(self.num_retailers + 1, 0.95)

        # Constraints
        cons = [{'type': 'ineq', 'fun': holding_cost_constraint}]

        # Bounds: service levels between 50% and 99.9%
        bounds = [(0.5, 0.999) for _ in range(self.num_retailers + 1)]

        # Optimize
        opt_result = minimize(objective, x0, method='SLSQP',
                            bounds=bounds, constraints=cons)

        if opt_result.success:
            retailer_sls = opt_result.x[:self.num_retailers].tolist()
            central_sl = opt_result.x[self.num_retailers]

            result = self.calculate_base_stocks_guaranteed_service(retailer_sls, central_sl)
            result['retailer_service_levels'] = retailer_sls
            result['central_service_level'] = central_sl

            return result
        else:
            raise ValueError("Optimization failed")

    def plot_network(self, result: Dict = None):
        """Visualize the distribution network"""

        fig, ax = plt.subplots(figsize=(14, 8))

        # Central warehouse position
        central_pos = (0.5, 0.8)

        # Draw central warehouse
        circle = plt.Circle(central_pos, 0.05, color='blue', zorder=3)
        ax.add_patch(circle)
        ax.text(central_pos[0], central_pos[1] + 0.08, 'Central\nWarehouse',
               ha='center', fontsize=10, fontweight='bold')

        if result:
            ax.text(central_pos[0], central_pos[1] - 0.08,
                   f"Base Stock: {result['central_base_stock']:.0f}\n"
                   f"Safety Stock: {result['central_safety_stock']:.0f}",
                   ha='center', fontsize=8)

        # Retailer positions (spread out below)
        retailer_positions = []
        for i in range(self.num_retailers):
            x = 0.1 + (0.8 * i / (self.num_retailers - 1) if self.num_retailers > 1 else 0.4)
            y = 0.2
            retailer_positions.append((x, y))

            # Draw retailer
            circle = plt.Circle((x, y), 0.04, color='green', zorder=3)
            ax.add_patch(circle)
            ax.text(x, y + 0.08, f'Retailer {i+1}',
                   ha='center', fontsize=9)

            if result:
                ax.text(x, y - 0.1,
                       f"BS: {result['retailer_base_stocks'][i]:.0f}\n"
                       f"SS: {result['retailer_safety_stocks'][i]:.0f}",
                       ha='center', fontsize=7)

            # Draw connection line
            ax.plot([central_pos[0], x], [central_pos[1], y],
                   'k-', linewidth=2, alpha=0.5)
            # Add lead time label
            mid_x, mid_y = (central_pos[0] + x) / 2, (central_pos[1] + y) / 2
            ax.text(mid_x, mid_y, f"LT: {self.Li[i]}",
                   fontsize=8, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title('Two-Echelon Distribution Network', fontsize=14, fontweight='bold')

        plt.tight_layout()
        return plt


# Example: Distribution System
def example_distribution_system():
    """Example: 1 central warehouse serving 5 retailers"""

    print("\n" + "=" * 70)
    print("TWO-ECHELON DISTRIBUTION SYSTEM")
    print("=" * 70)

    # 5 retailers with different characteristics
    system = TwoEchelonDistributionSystem(
        num_retailers=5,
        central_lead_time=14,                          # 14 days from supplier
        delivery_lead_times=[2, 2, 3, 3, 4],          # Days to each retailer
        central_holding_cost=0.5,                      # $/unit/day
        retailer_holding_costs=[2, 2, 3, 3, 4],       # $/unit/day
        demands_mean=[50, 80, 30, 60, 40],            # Daily demand
        demands_std=[10, 15, 8, 12, 10]               # Demand std dev
    )

    print("\nSystem Configuration:")
    print(f"  Central Warehouse Lead Time: {system.L0} days")
    print(f"  Central Holding Cost: ${system.h0}/unit/day")
    print(f"\n  {'Retailer':<12} {'Lead Time':<12} {'Demand Mean':<15} {'Demand Std':<15} {'Holding Cost'}")
    print("  " + "-" * 70)

    for i in range(system.num_retailers):
        print(f"  {i+1:<12} {system.Li[i]:<12} {system.mu[i]:<15.0f} "
              f"{system.sigma[i]:<15.1f} ${system.hi[i]:.2f}/unit/day")

    # Calculate base stocks with uniform 95% service level
    print("\n\nCalculating base stocks with 95% service level...")
    retailer_sls = [0.95] * system.num_retailers
    result = system.calculate_base_stocks_guaranteed_service(retailer_sls, 0.95)

    print(f"\n{'Central Warehouse:'}")
    print(f"  {'Base Stock Level:':<30} {result['central_base_stock']:.0f} units")
    print(f"  {'Safety Stock:':<30} {result['central_safety_stock']:.0f} units")
    print(f"  {'Holding Cost:':<30} ${result['central_holding_cost']:.2f}/day")

    print(f"\n{'Retailers:'}")
    print(f"  {'Retailer':<12} {'Base Stock':<15} {'Safety Stock':<15} {'Holding Cost'}")
    print("  " + "-" * 60)

    for i in range(system.num_retailers):
        print(f"  {i+1:<12} {result['retailer_base_stocks'][i]:<15.0f} "
              f"{result['retailer_safety_stocks'][i]:<15.0f} "
              f"${result['retailer_holding_cost']:.2f}/day")

    print(f"\n{'Total System Holding Cost:':<40} ${result['total_holding_cost']:.2f}/day")
    print(f"{'Annual Holding Cost:':<40} ${result['total_holding_cost'] * 365:.2f}/year")

    # Visualize network
    system.plot_network(result)
    plt.savefig('/tmp/distribution_network.png', dpi=300, bbox_inches='tight')
    print(f"\nNetwork diagram saved to /tmp/distribution_network.png")

    return system, result


if __name__ == "__main__":
    example_distribution_system()
```

---

## Advanced Multi-Echelon Optimization

### Risk Pooling Effect

```python
def analyze_risk_pooling(num_retailers: int, demand_mean: float,
                        demand_std: float, service_level: float = 0.95) -> Dict:
    """
    Analyze risk pooling benefit of centralization

    Compare:
    - Decentralized: Each retailer holds safety stock independently
    - Centralized: Single central warehouse serves all retailers
    """

    z = stats.norm.ppf(service_level)

    # Decentralized: each retailer independent
    safety_stock_per_retailer = z * demand_std
    total_safety_stock_decentral = num_retailers * safety_stock_per_retailer

    # Centralized: aggregate demand
    aggregate_demand_mean = num_retailers * demand_mean
    # Assuming independent demands
    aggregate_demand_std = demand_std * np.sqrt(num_retailers)

    safety_stock_central = z * aggregate_demand_std

    # Risk pooling benefit
    reduction = total_safety_stock_decentral - safety_stock_central
    reduction_pct = (reduction / total_safety_stock_decentral) * 100

    return {
        'decentralized_safety_stock': total_safety_stock_decentral,
        'centralized_safety_stock': safety_stock_central,
        'inventory_reduction': reduction,
        'reduction_percentage': reduction_pct,
        'num_retailers': num_retailers
    }


def plot_risk_pooling_effect():
    """Visualize risk pooling benefit as function of number of locations"""

    num_locations = range(1, 21)
    results = []

    for n in num_locations:
        result = analyze_risk_pooling(
            num_retailers=n,
            demand_mean=100,
            demand_std=20,
            service_level=0.95
        )
        results.append(result)

    df = pd.DataFrame(results)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Plot 1: Total safety stock
    ax1.plot(df['num_retailers'], df['decentralized_safety_stock'],
            'o-', linewidth=2, label='Decentralized', color='red')
    ax1.plot(df['num_retailers'], df['centralized_safety_stock'],
            's-', linewidth=2, label='Centralized', color='green')
    ax1.set_xlabel('Number of Retail Locations', fontsize=12)
    ax1.set_ylabel('Total Safety Stock (units)', fontsize=12)
    ax1.set_title('Risk Pooling: Safety Stock vs. Number of Locations',
                 fontsize=13, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Plot 2: Reduction percentage
    ax2.plot(df['num_retailers'], df['reduction_percentage'],
            'o-', linewidth=2, color='blue')
    ax2.set_xlabel('Number of Retail Locations', fontsize=12)
    ax2.set_ylabel('Inventory Reduction (%)', fontsize=12)
    ax2.set_title('Risk Pooling Benefit: Inventory Reduction',
                 fontsize=13, fontweight='bold')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    return plt


# Example
def example_risk_pooling():
    """Example: Quantify risk pooling benefit"""

    print("\n" + "=" * 70)
    print("RISK POOLING ANALYSIS")
    print("=" * 70)

    scenarios = [2, 5, 10, 20]

    print(f"\n{'Locations':<12} {'Decentralized SS':<20} {'Centralized SS':<20} {'Reduction':<15} {'Reduction %'}")
    print("-" * 80)

    for n in scenarios:
        result = analyze_risk_pooling(
            num_retailers=n,
            demand_mean=100,
            demand_std=20,
            service_level=0.95
        )

        print(f"{n:<12} {result['decentralized_safety_stock']:<20.0f} "
              f"{result['centralized_safety_stock']:<20.0f} "
              f"{result['inventory_reduction']:<15.0f} "
              f"{result['reduction_percentage']:<.1f}%")

    plot_risk_pooling_effect()
    plt.savefig('/tmp/risk_pooling_analysis.png', dpi=300, bbox_inches='tight')
    print(f"\nRisk pooling analysis saved to /tmp/risk_pooling_analysis.png")


if __name__ == "__main__":
    example_risk_pooling()
```

---

## Tools & Libraries

### Python Libraries

**Optimization & Simulation:**
- `numpy`, `scipy`: Numerical computations, optimization
- `pandas`: Data manipulation
- `networkx`: Network topology representation
- `simpy`: Discrete event simulation for complex policies

**Supply Chain Specific:**
- `supplychainpy`: Inventory optimization library
- Custom implementations (as shown above)

### Commercial Software

**Multi-Echelon Inventory Optimization:**
- **Blue Yonder (JDA)**: Industry leader in MEIO
- **Logility Voyager**: Multi-echelon planning
- **o9 Solutions**: Digital supply chain planning with MEIO
- **Kinaxis RapidResponse**: Multi-echelon inventory optimization
- **ToolsGroup**: Probabilistic multi-echelon optimization
- **SAP IBP**: Integrated Business Planning with multi-echelon

**Distribution Requirements Planning (DRP):**
- Most ERP systems (SAP, Oracle, Microsoft Dynamics)

---

## Common Challenges & Solutions

### Challenge: Data Quality and Visibility

**Problem:**
- Lack of real-time inventory visibility across network
- Inaccurate demand data at downstream locations
- Poor lead time tracking

**Solutions:**
- Implement inventory visibility platform
- Use IoT/RFID for real-time tracking
- Establish data governance processes
- Start with pilot at critical locations
- Improve demand data capture at POS

### Challenge: Demand Correlation

**Problem:**
- Retailer demands may be correlated (not independent)
- Risk pooling benefit overestimated

**Solutions:**
- Estimate demand correlation coefficients
- Use multivariate demand distributions
- Adjust safety stock calculations for correlation
- Consider geographic/product-based correlation patterns

### Challenge: Complex Network Structures

**Problem:**
- Real networks are not simple trees (lateral transshipment, returns)
- Multiple product flows through network

**Solutions:**
- Use simulation for complex networks
- Implement approximate decomposition methods
- Focus optimization on high-value/high-volume products
- Use proven software platforms for general networks

### Challenge: Service Level Trade-offs

**Problem:**
- Different stakeholders want different service levels
- Balancing cost vs. service across locations

**Solutions:**
- Define clear service level policies by product/customer class
- Use cost-to-serve analysis
- Implement differentiated service levels (e.g., A items 99%, C items 90%)
- Regular review and adjustment based on performance

### Challenge: Implementation and Change Management

**Problem:**
- Resistance from local managers to centralized control
- Difficulty changing established ordering patterns

**Solutions:**
- Phased rollout starting with willing locations
- Show quick wins and benefits
- Provide local visibility and override capability
- Training and communication on new policies
- Align incentives with system-wide metrics

---

## Output Format

### Multi-Echelon Inventory Optimization Report

**Executive Summary:**
- Current network: 1 central DC, 3 regional DCs, 25 retail stores
- Current total inventory: $8.5M
- Optimized inventory: $6.2M (27% reduction)
- Service level: 95% → 96% (improvement despite inventory reduction)
- Implementation: Phased over 6 months

**Current State Analysis:**

| Echelon | Locations | Avg Inventory | Inventory Value | Service Level | Issues |
|---------|-----------|---------------|-----------------|---------------|--------|
| Central DC | 1 | 15,000 | $2.1M | 98% | Overstocked |
| Regional DCs | 3 | 8,000 each | $3.4M | 94% | High variability |
| Retail Stores | 25 | 450 each | $3.0M | 92% | Frequent stockouts |
| **Total** | **29** | - | **$8.5M** | **93%** | - |

**Optimized Policy:**

| Echelon | Base Stock Policy | Safety Stock | Expected Inventory | Target Service Level |
|---------|-------------------|--------------|-------------------|---------------------|
| Central DC | Order-up-to 12,000 | 2,500 | 8,000 | 98% |
| Regional DC 1 | Order-up-to 6,500 | 1,200 | 4,200 | 96% |
| Regional DC 2 | Order-up-to 5,800 | 1,100 | 3,900 | 96% |
| Regional DC 3 | Order-up-to 7,200 | 1,400 | 4,800 | 96% |
| Retail Stores | Avg order-up-to 380 | 80 avg | 250 avg | 95% |

**Financial Impact:**

| Metric | Current | Optimized | Improvement |
|--------|---------|-----------|-------------|
| Total Inventory Investment | $8.5M | $6.2M | -$2.3M (-27%) |
| Annual Holding Cost (25%) | $2.1M | $1.6M | -$500K (-24%) |
| Service Level | 93% | 96% | +3 pts |
| Stockout Events/Month | 45 | 12 | -73% |
| Working Capital Freed | - | $2.3M | One-time benefit |

**Risk Pooling Benefit:**
- Centralization effect: 22% safety stock reduction
- Current decentralized SS: 8,500 units
- Optimized coordinated SS: 6,650 units
- Reduction: 1,850 units valued at $250K

**Implementation Plan:**
1. **Phase 1 (Months 1-2):** Implement at Central DC and 1 pilot Regional DC
2. **Phase 2 (Months 3-4):** Roll out to remaining 2 Regional DCs
3. **Phase 3 (Months 5-6):** Implement at retail stores in waves
4. **Ongoing:** Monitor performance, tune parameters monthly

**Technology Requirements:**
- Inventory visibility platform across all echelons
- Automated replenishment system
- Demand sensing and forecasting improvements
- Performance dashboards

---

## Questions to Ask

If you need more context:
1. What is your network structure? (echelons, locations at each level)
2. Where does customer demand occur? (retail, distribution centers, both)
3. What are the lead times between echelons?
4. What are holding costs at each location?
5. What are current service levels and targets?
6. Can you implement base stock policies or are there constraints?
7. Are there opportunities for lateral transshipment?
8. What data is available? (demand history, lead time data, current inventory)
9. What's driving this initiative? (cost reduction, service improvement, both)
10. Any plans for network redesign? (opening/closing facilities)

---

## Related Skills

- **inventory-optimization**: Single-location inventory models
- **economic-order-quantity**: EOQ lot-sizing models
- **stochastic-inventory-models**: Safety stock and service level calculations
- **network-design**: Strategic network structure optimization
- **demand-forecasting**: Demand prediction for inventory planning
- **inventory-routing-problem**: Joint inventory-routing decisions
- **distribution-center-network**: DC network design and optimization
- **risk-mitigation**: Supply chain risk management strategies
