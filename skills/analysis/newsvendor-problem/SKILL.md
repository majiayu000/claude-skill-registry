---
name: newsvendor-problem
description: When the user wants to solve single-period inventory problems, optimize stocking levels for perishable goods, or make one-time purchase decisions under demand uncertainty. Also use when the user mentions "newsvendor model," "newsboy problem," "single-period inventory," "perishable inventory," "overage and underage costs," "critical fractile," "fashion goods inventory," "seasonal products," "service level optimization," or "demand distribution matching." For multi-period problems, see dynamic-lot-sizing or stochastic-inventory-models.
---

# Newsvendor Problem

You are an expert in newsvendor models and single-period inventory optimization under uncertainty. Your goal is to help determine optimal stocking quantities for products with a single ordering opportunity and uncertain demand, balancing the costs of excess inventory against the costs of stockouts.

## Initial Assessment

Before solving newsvendor problems, understand:

1. **Product Characteristics**
   - What product type? (newspapers, fashion, seasonal, perishable)
   - Single selling season or truly one-time decision?
   - Shelf life or expiration date?
   - Salvage value if unsold?
   - Can excess inventory be returned or discounted?

2. **Demand Uncertainty**
   - Historical demand data available?
   - Demand distribution? (normal, lognormal, discrete, empirical)
   - Demand parameters (mean, standard deviation)?
   - Any demand forecasts or market intelligence?
   - Correlation with other products or external factors?

3. **Cost Structure**
   - Purchase/production cost per unit (c)?
   - Selling price per unit (p)?
   - Salvage value per unit if unsold (v)?
   - Shortage cost or penalty (b)? (lost profit or explicit penalty)
   - Are there fixed ordering costs?

4. **Business Context**
   - Target service level?
   - Risk tolerance (conservative vs. aggressive stocking)?
   - Strategic considerations (new product launch, market share)?
   - Competitive dynamics?

5. **Operational Constraints**
   - Minimum order quantity from supplier?
   - Maximum capacity or budget constraints?
   - Shelf space limitations?
   - Multiple products competing for same resources?

---

## Newsvendor Model Fundamentals

### The Classic Newsvendor Problem

**Story:** A newsvendor must decide how many newspapers to stock each morning. Demand is uncertain. Papers cost c to purchase and sell for p. Unsold papers have salvage value v. How many should be ordered?

**Key Trade-off:**
- **Order too few:** Lost profit from unmet demand (underage cost)
- **Order too many:** Loss on excess inventory (overage cost)

### Problem Formulation

**Decision Variable:** Q = order quantity

**Costs:**
- **Underage cost (Cu):** Lost profit per unit of unmet demand = p - c
- **Overage cost (Co):** Loss per unit of excess inventory = c - v

**Objective:** Maximize expected profit (or minimize expected cost)

### Critical Fractile Solution

The optimal order quantity Q* satisfies:

```
P(Demand ≤ Q*) = Cu / (Cu + Co)

Or equivalently:
P(Demand ≤ Q*) = (p - c) / (p - c + c - v)
                = (p - c) / (p - v)
```

This is the **critical fractile** or **service level**.

**Interpretation:** Stock to the point where the probability of meeting demand equals the ratio of underage to total costs.

### For Normal Distribution

If demand D ~ N(μ, σ²):

```
Q* = μ + z* σ

where z* is the z-score such that Φ(z*) = Cu / (Cu + Co)
```

---

## Python Implementation: Newsvendor Models

### Classic Newsvendor with Normal Demand

```python
import numpy as np
import pandas as pd
from scipy import stats
from scipy.optimize import minimize_scalar
import matplotlib.pyplot as plt
from typing import Dict, Callable, Tuple

class NewsvendorModel:
    """
    Classic Newsvendor Model for single-period inventory optimization

    Assumes continuous demand distribution
    """

    def __init__(self, cost: float, price: float, salvage: float = 0,
                 demand_dist: str = 'normal', demand_params: Dict = None):
        """
        Parameters:
        -----------
        cost : float
            Unit purchase/production cost (c)
        price : float
            Unit selling price (p)
        salvage : float
            Salvage value per unsold unit (v)
        demand_dist : str
            Distribution type: 'normal', 'lognormal', 'uniform', 'exponential'
        demand_params : dict
            Distribution parameters, e.g., {'mean': 100, 'std': 20}
        """
        self.c = cost
        self.p = price
        self.v = salvage

        # Cost parameters
        self.Cu = price - cost        # Underage cost (lost profit)
        self.Co = cost - salvage      # Overage cost (excess inventory loss)

        # Critical fractile
        self.critical_fractile = self.Cu / (self.Cu + self.Co)

        # Demand distribution
        self.demand_dist = demand_dist
        self.demand_params = demand_params or {}

        self._setup_distribution()

    def _setup_distribution(self):
        """Setup scipy distribution object"""

        if self.demand_dist == 'normal':
            mu = self.demand_params.get('mean', 100)
            sigma = self.demand_params.get('std', 20)
            self.dist = stats.norm(loc=mu, scale=sigma)

        elif self.demand_dist == 'lognormal':
            # Lognormal: E[X] = exp(μ + σ²/2), Var[X] = exp(2μ + σ²)(exp(σ²) - 1)
            mean = self.demand_params.get('mean', 100)
            cv = self.demand_params.get('cv', 0.3)  # Coefficient of variation
            sigma_sq = np.log(1 + cv**2)
            mu = np.log(mean) - sigma_sq / 2
            self.dist = stats.lognorm(s=np.sqrt(sigma_sq), scale=np.exp(mu))

        elif self.demand_dist == 'uniform':
            a = self.demand_params.get('min', 50)
            b = self.demand_params.get('max', 150)
            self.dist = stats.uniform(loc=a, scale=b-a)

        elif self.demand_dist == 'exponential':
            rate = self.demand_params.get('rate', 0.01)
            self.dist = stats.expon(scale=1/rate)

        else:
            raise ValueError(f"Unknown distribution: {self.demand_dist}")

    def optimal_order_quantity(self) -> Dict:
        """
        Calculate optimal order quantity using critical fractile

        Returns:
        --------
        Dictionary with optimal Q, expected profit, and other metrics
        """

        # Optimal order quantity: inverse CDF at critical fractile
        Q_star = self.dist.ppf(self.critical_fractile)

        # Expected profit at Q*
        expected_profit = self.expected_profit(Q_star)

        # Expected sales
        expected_sales = self.expected_sales(Q_star)

        # Expected leftover inventory
        expected_leftover = Q_star - expected_sales

        # Expected lost sales
        expected_lost_sales = self.expected_lost_sales(Q_star)

        # In-stock probability (fill rate)
        fill_rate = self.dist.cdf(Q_star)

        return {
            'optimal_order_qty': Q_star,
            'expected_profit': expected_profit,
            'expected_sales': expected_sales,
            'expected_leftover': expected_leftover,
            'expected_lost_sales': expected_lost_sales,
            'fill_rate': fill_rate,
            'critical_fractile': self.critical_fractile,
            'underage_cost': self.Cu,
            'overage_cost': self.Co
        }

    def expected_profit(self, Q: float) -> float:
        """
        Calculate expected profit for given order quantity Q

        E[Profit(Q)] = p*E[Sales] - c*Q + v*E[Leftover]
        """

        expected_sales = self.expected_sales(Q)
        expected_leftover = Q - expected_sales

        profit = (self.p * expected_sales -
                 self.c * Q +
                 self.v * expected_leftover)

        return profit

    def expected_sales(self, Q: float) -> float:
        """
        Calculate expected sales (units sold) for order quantity Q

        E[Sales] = E[min(D, Q)]
                 = ∫[0 to Q] x*f(x)dx + Q*[1 - F(Q)]
        """

        # For continuous distribution, use integration
        # E[min(D,Q)] = Q - ∫[Q to ∞] F(x)dx
        #             = Q - E[max(0, D-Q)]

        # Alternative formula:
        # E[min(D,Q)] = ∫[0 to Q] x*f(x)dx + Q*P(D > Q)

        # Use numerical integration for general case
        def integrand(x):
            return x * self.dist.pdf(x)

        # Integrate from 0 to Q
        from scipy.integrate import quad
        integral_part, _ = quad(integrand, 0, Q)

        # Add Q * P(D > Q)
        prob_excess = 1 - self.dist.cdf(Q)
        sales = integral_part + Q * prob_excess

        return sales

    def expected_lost_sales(self, Q: float) -> float:
        """
        Calculate expected lost sales for order quantity Q

        E[Lost Sales] = E[max(0, D - Q)]
        """

        mean_demand = self.dist.mean()
        expected_sales = self.expected_sales(Q)

        return mean_demand - expected_sales

    def profit_curve(self, Q_range: Tuple[float, float] = None,
                    num_points: int = 200) -> pd.DataFrame:
        """
        Generate profit curve over range of order quantities

        Parameters:
        -----------
        Q_range : tuple
            (min_Q, max_Q) range to evaluate
        num_points : int
            Number of points to evaluate

        Returns:
        --------
        DataFrame with Q and expected profit
        """

        if Q_range is None:
            mean = self.dist.mean()
            std = self.dist.std()
            Q_range = (max(0, mean - 3*std), mean + 3*std)

        Q_values = np.linspace(Q_range[0], Q_range[1], num_points)
        profits = [self.expected_profit(Q) for Q in Q_values]

        return pd.DataFrame({
            'order_quantity': Q_values,
            'expected_profit': profits
        })

    def plot_profit_curve(self):
        """Visualize expected profit vs. order quantity"""

        df = self.profit_curve()
        optimal = self.optimal_order_quantity()

        plt.figure(figsize=(12, 7))

        plt.plot(df['order_quantity'], df['expected_profit'],
                linewidth=2, color='blue', label='Expected Profit')

        # Mark optimal point
        plt.plot(optimal['optimal_order_qty'], optimal['expected_profit'],
                'r*', markersize=20,
                label=f"Optimal Q = {optimal['optimal_order_qty']:.0f}")

        plt.axvline(x=optimal['optimal_order_qty'], color='red',
                   linestyle='--', alpha=0.5)

        plt.xlabel('Order Quantity (Q)', fontsize=12)
        plt.ylabel('Expected Profit ($)', fontsize=12)
        plt.title('Newsvendor Model: Expected Profit vs. Order Quantity',
                 fontsize=14, fontweight='bold')
        plt.legend(fontsize=10)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()

        return plt

    def plot_demand_and_optimal(self):
        """Visualize demand distribution and optimal order quantity"""

        optimal = self.optimal_order_quantity()
        Q_star = optimal['optimal_order_qty']

        mean = self.dist.mean()
        std = self.dist.std()

        x = np.linspace(max(0, mean - 4*std), mean + 4*std, 500)
        pdf = self.dist.pdf(x)
        cdf = self.dist.cdf(x)

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

        # Plot 1: PDF with optimal Q
        ax1.plot(x, pdf, linewidth=2, color='blue', label='Demand PDF')
        ax1.axvline(x=Q_star, color='red', linestyle='--', linewidth=2,
                   label=f'Optimal Q = {Q_star:.0f}')
        ax1.axvline(x=mean, color='green', linestyle=':', linewidth=2,
                   label=f'Mean Demand = {mean:.0f}')

        # Shade areas
        ax1.fill_between(x[x <= Q_star], 0, pdf[x <= Q_star],
                        alpha=0.3, color='green', label='Demand Satisfied')
        ax1.fill_between(x[x > Q_star], 0, pdf[x > Q_star],
                        alpha=0.3, color='red', label='Lost Sales')

        ax1.set_xlabel('Demand', fontsize=12)
        ax1.set_ylabel('Probability Density', fontsize=12)
        ax1.set_title('Demand Distribution and Optimal Stocking Level',
                     fontsize=13, fontweight='bold')
        ax1.legend(fontsize=10)
        ax1.grid(True, alpha=0.3)

        # Plot 2: CDF with critical fractile
        ax2.plot(x, cdf, linewidth=2, color='blue', label='Cumulative Probability')
        ax2.axvline(x=Q_star, color='red', linestyle='--', linewidth=2,
                   label=f'Optimal Q = {Q_star:.0f}')
        ax2.axhline(y=self.critical_fractile, color='orange', linestyle='--',
                   linewidth=2,
                   label=f'Critical Fractile = {self.critical_fractile:.3f}')
        ax2.plot(Q_star, self.critical_fractile, 'ro', markersize=12)

        ax2.set_xlabel('Order Quantity', fontsize=12)
        ax2.set_ylabel('Cumulative Probability', fontsize=12)
        ax2.set_title('CDF and Critical Fractile',
                     fontsize=13, fontweight='bold')
        ax2.legend(fontsize=10)
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()
        return plt

    def sensitivity_analysis(self, param_name: str,
                           param_values: np.ndarray) -> pd.DataFrame:
        """
        Analyze sensitivity of optimal Q to parameter changes

        Parameters:
        -----------
        param_name : str
            'cost', 'price', 'salvage', 'demand_mean', 'demand_std'
        param_values : array
            Array of parameter values to test

        Returns:
        --------
        DataFrame with parameter values and corresponding optimal Q
        """

        results = []

        # Save original values
        orig_c, orig_p, orig_v = self.c, self.p, self.v
        orig_params = self.demand_params.copy()

        for val in param_values:
            # Modify parameter
            if param_name == 'cost':
                self.c = val
                self.Cu = self.p - self.c
                self.Co = self.c - self.v
                self.critical_fractile = self.Cu / (self.Cu + self.Co)

            elif param_name == 'price':
                self.p = val
                self.Cu = self.p - self.c
                self.critical_fractile = self.Cu / (self.Cu + self.Co)

            elif param_name == 'salvage':
                self.v = val
                self.Co = self.c - self.v
                self.critical_fractile = self.Cu / (self.Cu + self.Co)

            elif param_name == 'demand_mean':
                self.demand_params['mean'] = val
                self._setup_distribution()

            elif param_name == 'demand_std':
                self.demand_params['std'] = val
                self._setup_distribution()

            # Calculate optimal Q at this parameter value
            optimal = self.optimal_order_quantity()

            results.append({
                param_name: val,
                'optimal_Q': optimal['optimal_order_qty'],
                'expected_profit': optimal['expected_profit'],
                'fill_rate': optimal['fill_rate']
            })

        # Restore original values
        self.c, self.p, self.v = orig_c, orig_p, orig_v
        self.Cu = self.p - self.c
        self.Co = self.c - self.v
        self.critical_fractile = self.Cu / (self.Cu + self.Co)
        self.demand_params = orig_params
        self._setup_distribution()

        return pd.DataFrame(results)


# Example Usage
def example_basic_newsvendor():
    """Example: Classic newsvendor problem"""

    print("\n" + "=" * 70)
    print("NEWSVENDOR PROBLEM: BASIC EXAMPLE")
    print("=" * 70)

    # Fashion retailer ordering seasonal jackets
    model = NewsvendorModel(
        cost=40,                # Purchase cost: $40/jacket
        price=100,              # Selling price: $100/jacket
        salvage=10,             # End-of-season clearance: $10/jacket
        demand_dist='normal',
        demand_params={'mean': 200, 'std': 50}
    )

    print("\nProblem Parameters:")
    print(f"  Purchase Cost (c): ${model.c}")
    print(f"  Selling Price (p): ${model.p}")
    print(f"  Salvage Value (v): ${model.v}")
    print(f"  Demand Distribution: Normal(μ={model.demand_params['mean']}, "
          f"σ={model.demand_params['std']})")

    print(f"\nCost Analysis:")
    print(f"  Underage Cost (Cu = p - c): ${model.Cu}")
    print(f"  Overage Cost (Co = c - v): ${model.Co}")
    print(f"  Critical Fractile: {model.critical_fractile:.4f}")

    # Calculate optimal solution
    optimal = model.optimal_order_quantity()

    print(f"\n{'=' * 70}")
    print("OPTIMAL SOLUTION")
    print("=" * 70)

    print(f"\n{'Optimal Order Quantity:':<35} {optimal['optimal_order_qty']:.0f} units")
    print(f"{'Expected Profit:':<35} ${optimal['expected_profit']:,.2f}")
    print(f"{'Expected Sales:':<35} {optimal['expected_sales']:.0f} units")
    print(f"{'Expected Leftover Inventory:':<35} {optimal['expected_leftover']:.0f} units")
    print(f"{'Expected Lost Sales:':<35} {optimal['expected_lost_sales']:.0f} units")
    print(f"{'Fill Rate (Service Level):':<35} {optimal['fill_rate']:.2%}")

    # Financial breakdown
    revenue = model.p * optimal['expected_sales']
    salvage_revenue = model.v * optimal['expected_leftover']
    cost = model.c * optimal['optimal_order_qty']

    print(f"\n{'Financial Breakdown:':<35}")
    print(f"  {'Revenue from Sales:':<33} ${revenue:,.2f}")
    print(f"  {'Salvage Revenue:':<33} ${salvage_revenue:,.2f}")
    print(f"  {'Total Revenue:':<33} ${revenue + salvage_revenue:,.2f}")
    print(f"  {'Purchase Cost:':<33} ${cost:,.2f}")
    print(f"  {'-'*50}")
    print(f"  {'Expected Profit:':<33} ${optimal['expected_profit']:,.2f}")

    # Sensitivity analysis
    print("\n\nSensitivity Analysis: Varying Demand Mean")
    demand_means = np.linspace(150, 250, 5)
    sensitivity = model.sensitivity_analysis('demand_mean', demand_means)
    print(sensitivity.to_string(index=False))

    # Plots
    model.plot_profit_curve()
    plt.savefig('/tmp/newsvendor_profit_curve.png', dpi=300, bbox_inches='tight')
    print(f"\nProfit curve saved to /tmp/newsvendor_profit_curve.png")

    model.plot_demand_and_optimal()
    plt.savefig('/tmp/newsvendor_demand_distribution.png', dpi=300, bbox_inches='tight')
    print(f"Demand distribution plot saved to /tmp/newsvendor_demand_distribution.png")

    return model, optimal


if __name__ == "__main__":
    example_basic_newsvendor()
```

---

## Newsvendor with Discrete Demand

### Empirical or Discrete Distribution

```python
class DiscreteNewsvendor:
    """
    Newsvendor model with discrete demand distribution

    Useful when demand is given as empirical data or discrete probabilities
    """

    def __init__(self, cost: float, price: float, salvage: float,
                 demand_values: np.ndarray, probabilities: np.ndarray = None):
        """
        Parameters:
        -----------
        cost, price, salvage : float
            Cost parameters
        demand_values : array
            Possible demand values
        probabilities : array, optional
            Probability of each demand value (must sum to 1)
            If None, uniform distribution assumed
        """
        self.c = cost
        self.p = price
        self.v = salvage

        self.demand_values = np.array(demand_values)

        if probabilities is None:
            self.probabilities = np.ones(len(demand_values)) / len(demand_values)
        else:
            self.probabilities = np.array(probabilities)
            assert np.isclose(self.probabilities.sum(), 1.0), "Probabilities must sum to 1"

        # Cost parameters
        self.Cu = price - cost
        self.Co = cost - salvage
        self.critical_fractile = self.Cu / (self.Cu + self.Co)

    def optimal_order_quantity(self) -> Dict:
        """
        Find optimal Q for discrete distribution

        For discrete: choose smallest Q such that F(Q) >= critical fractile
        """

        # Calculate CDF
        cdf = np.cumsum(self.probabilities)

        # Find smallest Q where CDF >= critical fractile
        idx = np.searchsorted(cdf, self.critical_fractile)
        Q_star = self.demand_values[idx]

        # Calculate expected profit at Q*
        expected_profit = self._expected_profit(Q_star)

        # Other metrics
        expected_sales = self._expected_sales(Q_star)
        expected_leftover = Q_star - expected_sales
        expected_demand = np.sum(self.demand_values * self.probabilities)
        expected_lost_sales = expected_demand - expected_sales
        fill_rate = cdf[idx]

        return {
            'optimal_order_qty': Q_star,
            'expected_profit': expected_profit,
            'expected_sales': expected_sales,
            'expected_leftover': expected_leftover,
            'expected_lost_sales': expected_lost_sales,
            'fill_rate': fill_rate,
            'critical_fractile': self.critical_fractile
        }

    def _expected_sales(self, Q: float) -> float:
        """Calculate E[min(D, Q)]"""
        sales = np.minimum(self.demand_values, Q)
        return np.sum(sales * self.probabilities)

    def _expected_profit(self, Q: float) -> float:
        """Calculate expected profit for given Q"""
        expected_sales = self._expected_sales(Q)
        expected_leftover = Q - expected_sales

        profit = (self.p * expected_sales -
                 self.c * Q +
                 self.v * expected_leftover)

        return profit

    def evaluate_all_quantities(self) -> pd.DataFrame:
        """Evaluate expected profit for all possible order quantities"""

        results = []

        for Q in self.demand_values:
            profit = self._expected_profit(Q)
            sales = self._expected_sales(Q)
            leftover = Q - sales

            results.append({
                'order_qty': Q,
                'expected_profit': profit,
                'expected_sales': sales,
                'expected_leftover': leftover
            })

        return pd.DataFrame(results)


# Example: Discrete Demand
def example_discrete_newsvendor():
    """Example: Newsvendor with empirical demand distribution"""

    print("\n" + "=" * 70)
    print("NEWSVENDOR PROBLEM: DISCRETE DEMAND")
    print("=" * 70)

    # Bakery ordering fresh bread
    # Historical demand data (units sold per day)
    demand_scenarios = np.array([80, 90, 100, 110, 120, 130, 140])
    probabilities = np.array([0.05, 0.10, 0.20, 0.30, 0.20, 0.10, 0.05])

    model = DiscreteNewsvendor(
        cost=2.00,      # Cost to make: $2/loaf
        price=5.00,     # Selling price: $5/loaf
        salvage=0.50,   # Day-old discount: $0.50/loaf
        demand_values=demand_scenarios,
        probabilities=probabilities
    )

    print("\nDemand Distribution:")
    print(f"\n{'Demand':<12} {'Probability':<15} {'Cumulative'}")
    print("-" * 40)

    cdf = np.cumsum(probabilities)
    for d, p, c in zip(demand_scenarios, probabilities, cdf):
        print(f"{d:<12} {p:<15.2%} {c:.2%}")

    print(f"\nCritical Fractile: {model.critical_fractile:.4f}")

    # Find optimal
    optimal = model.optimal_order_quantity()

    print(f"\n{'=' * 70}")
    print("OPTIMAL SOLUTION")
    print("=" * 70)

    print(f"\n{'Optimal Order Quantity:':<35} {optimal['optimal_order_qty']:.0f} loaves")
    print(f"{'Expected Daily Profit:':<35} ${optimal['expected_profit']:.2f}")
    print(f"{'Expected Sales:':<35} {optimal['expected_sales']:.1f} loaves")
    print(f"{'Expected Waste:':<35} {optimal['expected_leftover']:.1f} loaves")
    print(f"{'Fill Rate:':<35} {optimal['fill_rate']:.2%}")

    # Show all options
    print("\n\nEvaluation of All Order Quantities:")
    all_results = model.evaluate_all_quantities()
    print(all_results.to_string(index=False))

    # Highlight optimal
    print(f"\nOptimal choice: Order {optimal['optimal_order_qty']:.0f} loaves")
    print(f"  → Expected profit: ${optimal['expected_profit']:.2f}/day")
    print(f"  → Annual profit (365 days): ${optimal['expected_profit'] * 365:,.2f}")

    return model, optimal


if __name__ == "__main__":
    example_discrete_newsvendor()
```

---

## Extensions and Variants

### Newsvendor with Multiple Products

```python
class MultiProductNewsvendor:
    """
    Multi-product newsvendor with budget or capacity constraint

    Products compete for limited resources
    """

    def __init__(self, products: List[Dict], budget: float = None,
                 capacity: float = None):
        """
        Parameters:
        -----------
        products : list of dicts
            Each dict contains: cost, price, salvage, demand_mean, demand_std
        budget : float, optional
            Budget constraint on total purchase cost
        capacity : float, optional
            Capacity constraint on total units
        """
        self.products = products
        self.n = len(products)
        self.budget = budget
        self.capacity = capacity

    def marginal_benefit(self, product_idx: int, Q: float) -> float:
        """
        Calculate marginal benefit of ordering one more unit of product i

        MB(Q) = p*P(D > Q) - c*P(D ≤ Q) + v*P(D ≤ Q)
              = p*P(D > Q) - (c - v)*P(D ≤ Q)
        """
        prod = self.products[product_idx]

        dist = stats.norm(loc=prod['demand_mean'], scale=prod['demand_std'])

        prob_excess = 1 - dist.cdf(Q)
        prob_shortage = dist.cdf(Q)

        mb = (prod['price'] * prob_excess -
              (prod['cost'] - prod['salvage']) * prob_shortage)

        return mb

    def optimize_greedy(self) -> Dict:
        """
        Greedy heuristic: iteratively add unit with highest marginal benefit

        Respects budget and capacity constraints
        """

        # Initialize order quantities
        Q = np.zeros(self.n)

        total_cost = 0
        total_units = 0

        # Greedy allocation
        while True:
            # Find product with highest marginal benefit
            best_product = None
            best_mb = -np.inf

            for i in range(self.n):
                prod = self.products[i]

                # Check feasibility
                if self.budget and total_cost + prod['cost'] > self.budget:
                    continue
                if self.capacity and total_units + 1 > self.capacity:
                    continue

                # Calculate marginal benefit
                mb = self.marginal_benefit(i, Q[i])

                if mb > best_mb:
                    best_mb = mb
                    best_product = i

            # If no product has positive marginal benefit, stop
            if best_product is None or best_mb <= 0:
                break

            # Add one unit of best product
            Q[best_product] += 1
            total_cost += self.products[best_product]['cost']
            total_units += 1

        # Calculate expected profits
        expected_profits = []
        for i in range(self.n):
            # Simple calculation using normal distribution
            prod = self.products[i]
            dist = stats.norm(loc=prod['demand_mean'], scale=prod['demand_std'])

            # Expected sales
            def integrand(d):
                return min(d, Q[i]) * dist.pdf(d)

            from scipy.integrate import quad
            expected_sales, _ = quad(integrand, 0, Q[i] + 4*prod['demand_std'])

            profit = (prod['price'] * expected_sales -
                     prod['cost'] * Q[i] +
                     prod['salvage'] * (Q[i] - expected_sales))

            expected_profits.append(profit)

        total_profit = sum(expected_profits)

        return {
            'order_quantities': Q,
            'expected_profits': expected_profits,
            'total_expected_profit': total_profit,
            'total_cost': total_cost,
            'total_units': total_units
        }


# Example: Multi-product
def example_multi_product():
    """Example: Multiple products with budget constraint"""

    print("\n" + "=" * 70)
    print("MULTI-PRODUCT NEWSVENDOR WITH BUDGET CONSTRAINT")
    print("=" * 70)

    # Fashion retailer with 3 styles
    products = [
        {'name': 'Style A', 'cost': 30, 'price': 80, 'salvage': 10,
         'demand_mean': 150, 'demand_std': 30},
        {'name': 'Style B', 'cost': 40, 'price': 100, 'salvage': 15,
         'demand_mean': 100, 'demand_std': 25},
        {'name': 'Style C', 'cost': 50, 'price': 120, 'salvage': 20,
         'demand_mean': 80, 'demand_std': 20}
    ]

    budget = 15000  # $15,000 purchasing budget

    model = MultiProductNewsvendor(products, budget=budget)

    print("\nProduct Details:")
    print(f"\n{'Product':<12} {'Cost':<10} {'Price':<10} {'Salvage':<10} "
          f"{'Demand (μ)':<15} {'Demand (σ)'}")
    print("-" * 70)

    for prod in products:
        print(f"{prod['name']:<12} ${prod['cost']:<9} ${prod['price']:<9} "
              f"${prod['salvage']:<9} {prod['demand_mean']:<15} {prod['demand_std']}")

    print(f"\nPurchasing Budget: ${budget:,}")

    # Optimize
    result = model.optimize_greedy()

    print(f"\n{'=' * 70}")
    print("OPTIMAL ALLOCATION")
    print("=" * 70)

    print(f"\n{'Product':<12} {'Order Qty':<12} {'Expected Profit':<20}")
    print("-" * 45)

    for i, prod in enumerate(products):
        print(f"{prod['name']:<12} {result['order_quantities'][i]:<12.0f} "
              f"${result['expected_profits'][i]:,.2f}")

    print(f"\n{'Total Expected Profit:':<35} ${result['total_expected_profit']:,.2f}")
    print(f"{'Total Cost:':<35} ${result['total_cost']:,.2f}")
    print(f"{'Budget Utilization:':<35} {result['total_cost']/budget:.1%}")

    return model, result


if __name__ == "__main__":
    example_multi_product()
```

---

## Tools & Libraries

### Python Libraries

**Statistical & Optimization:**
- `numpy`, `scipy`: Distributions, optimization
- `pandas`: Data analysis
- `statsmodels`: Statistical modeling

**Specialized:**
- `scipy.stats`: Probability distributions for demand modeling
- `scipy.optimize`: For constrained optimization variants

### Commercial Software

**Demand Planning & Inventory Optimization:**
- **Blue Yonder**: Advanced inventory optimization with newsvendor logic
- **o9 Solutions**: Integrated planning with probabilistic models
- **Logility**: Inventory planning for seasonal/fashion
- **ToolsGroup**: Probabilistic demand forecasting

**Retail-Specific:**
- **Oracle Retail**: Markdown and inventory optimization
- **SAP Fashion Management**: Assortment and allocation planning

---

## Common Challenges & Solutions

### Challenge: Unknown or Misspecified Demand Distribution

**Problem:**
- Limited historical data
- Demand distribution doesn't fit standard forms
- New product with no history

**Solutions:**
- Use empirical distribution from historical data
- Bootstrap methods for uncertainty quantification
- Fit parametric distribution (normal, lognormal) using maximum likelihood
- Use judgmental forecasting + analogous products
- Start conservative, update as season progresses

### Challenge: Estimating Shortage Cost

**Problem:**
- Hard to quantify cost of lost sales
- Customer goodwill and reputation effects

**Solutions:**
- Use lost margin (p - c) as lower bound
- Survey customers on willingness to substitute/return
- Analyze competitor stockout behavior
- Set based on strategic goals (e.g., 95% service level → implied shortage cost)
- Sensitivity analysis across range of shortage costs

### Challenge: Salvage Value Uncertainty

**Problem:**
- Don't know clearance price in advance
- May depend on leftover quantity

**Solutions:**
- Use historical average markdown percentage
- Conservative approach: assume salvage = 0
- Build in multiple salvage opportunities (e.g., markdown waves)
- Contract with liquidators for guaranteed salvage value

### Challenge: Mid-Season Updates

**Problem:**
- Initial decision before season, but can adjust during season
- Bayesian updating of demand forecast

**Solutions:**
- Dynamic programming approach with decision epochs
- Update demand distribution based on early sales
- Use **newsvendor with multiple ordering opportunities** (more complex model)
- Implement markdown optimization for remaining inventory

### Challenge: Strategic Considerations

**Problem:**
- Model says stock conservatively, but want to build market share
- New product launch with strategic importance

**Solutions:**
- Adjust effective shortage cost to reflect strategic value
- Use higher target service level (e.g., 99% for flagship product)
- Separate financial optimization from strategic positioning
- Accept lower profit for market learning

---

## Output Format

### Newsvendor Analysis Report

**Executive Summary:**
- Product: Fall fashion jacket collection
- Optimal order quantity: 1,850 units
- Expected profit: $87,500
- Expected leftover: 125 units (6.8% of order)
- Recommendation: Order 1,850 units before season starts

**Problem Setup:**

| Parameter | Value |
|-----------|-------|
| Purchase Cost | $40/unit |
| Selling Price | $100/unit |
| Salvage Value | $10/unit (clearance sale) |
| Underage Cost (lost profit) | $60/unit |
| Overage Cost (excess inventory) | $30/unit |
| Critical Fractile | 0.6667 (66.67%) |

**Demand Forecast:**

| Statistic | Value |
|-----------|-------|
| Mean Demand | 1,800 units |
| Standard Deviation | 300 units |
| Distribution | Normal |
| Coefficient of Variation | 16.7% |

**Optimal Solution:**

| Metric | Value |
|--------|-------|
| Optimal Order Quantity | 1,850 units |
| Expected Sales | 1,725 units |
| Expected Leftover Inventory | 125 units |
| Expected Lost Sales | 75 units |
| Fill Rate (Service Level) | 66.7% |
| Expected Revenue | $172,500 (sales) + $1,250 (salvage) |
| Expected Cost | $74,000 |
| **Expected Profit** | **$87,500** |

**Sensitivity Analysis:**

| Scenario | Order Quantity | Expected Profit | Change |
|----------|----------------|-----------------|--------|
| Base Case | 1,850 | $87,500 | - |
| Demand -20% | 1,490 | $70,000 | -20% |
| Demand +20% | 2,210 | $105,000 | +20% |
| Higher Salvage ($20) | 1,730 | $89,200 | +2% |
| Lower Salvage ($5) | 1,920 | $86,800 | -1% |

**Risk Assessment:**
- Probability demand exceeds order: 33%
- Probability of leftover > 200 units: 15%
- Worst-case scenario (demand = 1,200): Profit = $45,000

**Recommendations:**
1. Order 1,850 units (round to nearest case pack size)
2. Secure clearance channel for expected 125 leftover units
3. Monitor early-season sales (first 2 weeks)
4. If sales tracking 20%+ above forecast, consider mid-season reorder
5. Plan markdown strategy for week 8-10 of season

---

## Questions to Ask

If you need more context:
1. What product are you trying to stock? (seasonal, perishable, fashion)
2. What is the purchase cost, selling price, and salvage value?
3. Is there historical demand data available? How many periods?
4. What demand distribution seems appropriate? (normal, empirical, other)
5. Can you reorder during the season or is this truly one-time?
6. What are the consequences of stockouts? (lost sales, customer switching)
7. Are there multiple products competing for same budget/space?
8. Any minimum order quantities or other constraints?
9. What is your risk tolerance? (conservative vs. aggressive)
10. How will leftover inventory be liquidated?

---

## Related Skills

- **inventory-optimization**: Multi-period inventory models
- **stochastic-inventory-models**: (Q,r) and (s,S) policies with uncertainty
- **economic-order-quantity**: Deterministic lot-sizing
- **demand-forecasting**: Demand distribution estimation
- **markdown-optimization**: Pricing for clearance of excess inventory
- **retail-allocation**: Multi-location assortment and allocation
- **seasonal-planning**: Planning for seasonal demand patterns
- **promotional-planning**: Demand modeling with promotions
