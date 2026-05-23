---
name: stochastic-optimization
description: When the user wants to optimize under uncertainty, handle probabilistic constraints, or solve stochastic programming problems. Also use when the user mentions "stochastic optimization," "chance constraints," "two-stage stochastic programming," "scenario-based optimization," "robust optimization under uncertainty," "stochastic demand," "uncertainty modeling," or "probabilistic optimization." For deterministic optimization, see optimization-modeling. For robust optimization, see metaheuristic-optimization.
---

# Stochastic Optimization

You are an expert in stochastic optimization and decision-making under uncertainty for supply chain. Your goal is to help solve optimization problems where parameters (demand, lead times, prices) are uncertain, using scenario-based methods, chance constraints, and risk measures.

## Initial Assessment

Before applying stochastic optimization, understand:

1. **Uncertainty Characteristics**
   - What parameters are uncertain? (demand, supply, prices, lead times)
   - Probability distributions known or unknown?
   - Historical data available?
   - Uncertainty independent or correlated?

2. **Decision Structure**
   - Single-stage or multi-stage decisions?
   - Which decisions made before/after uncertainty reveals?
   - Recourse actions available?
   - Decision frequency?

3. **Risk Attitude**
   - Risk-neutral (expected value) or risk-averse?
   - Preferred risk measure? (CVaR, variance, worst-case)
   - Service level requirements?
   - Budget/capacity constraints?

4. **Computational Requirements**
   - Problem size?
   - Number of scenarios needed?
   - Solution time constraints?
   - Need for exact vs approximate solution?

---

## Two-Stage Stochastic Programming

### Framework

**Stage 1 (Here-and-Now):** Decisions before uncertainty revealed
**Stage 2 (Wait-and-See):** Recourse decisions after observing uncertainty

**Formulation:**
```
min  c^T x + E_ξ[Q(x, ξ)]

s.t. Ax = b
     x ≥ 0

where Q(x, ξ) = min q(ξ)^T y
                s.t. W y = h(ξ) - T(ξ) x
                     y ≥ 0
```

### Implementation: Production Planning Under Demand Uncertainty

```python
import numpy as np
from pulp import *
from typing import List, Dict, Tuple
import matplotlib.pyplot as plt

class TwoStageStochasticProduction:
    """
    Two-Stage Stochastic Programming for Production Planning
    
    Stage 1: Decide production quantities (before demand known)
    Stage 2: Handle inventory/backorder (after demand realized)
    """
    
    def __init__(self,
                 products: List[str],
                 scenarios: List[Dict],
                 production_cost: Dict[str, float],
                 holding_cost: Dict[str, float],
                 backorder_cost: Dict[str, float],
                 capacity: float):
        """
        Initialize two-stage stochastic model
        
        products: list of product names
        scenarios: list of dicts with {'demand': {product: qty}, 'probability': p}
        production_cost: cost per unit to produce
        holding_cost: cost per unit to hold inventory
        backorder_cost: cost per unit backorder
        capacity: production capacity
        """
        
        self.products = products
        self.scenarios = scenarios
        self.n_scenarios = len(scenarios)
        
        self.prod_cost = production_cost
        self.hold_cost = holding_cost
        self.back_cost = backorder_cost
        self.capacity = capacity
        
        # Results
        self.solution = None
        
    def optimize(self) -> Dict:
        """
        Solve two-stage stochastic program
        
        Returns: optimal solution
        """
        
        print(f"Solving Two-Stage Stochastic Production Planning...")
        print(f"Products: {len(self.products)}, Scenarios: {self.n_scenarios}")
        
        # Create extensive form (deterministic equivalent)
        model = LpProblem("Two_Stage_Stochastic_Production", LpMinimize)
        
        # Stage 1 variables: production decisions
        produce = LpVariable.dicts("Produce", self.products, lowBound=0)
        
        # Stage 2 variables: inventory and backorder for each scenario
        inventory = {}
        backorder = {}
        
        for s, scenario in enumerate(self.scenarios):
            for p in self.products:
                inventory[(s, p)] = LpVariable(f"Inv_s{s}_{p}", lowBound=0)
                backorder[(s, p)] = LpVariable(f"Back_s{s}_{p}", lowBound=0)
        
        # Objective: Stage 1 cost + Expected Stage 2 cost
        stage1_cost = lpSum([self.prod_cost[p] * produce[p] for p in self.products])
        
        stage2_cost = lpSum([
            self.scenarios[s]['probability'] * (
                self.hold_cost[p] * inventory[(s, p)] +
                self.back_cost[p] * backorder[(s, p)]
            )
            for s in range(self.n_scenarios)
            for p in self.products
        ])
        
        model += stage1_cost + stage2_cost, "Total_Cost"
        
        # Stage 1 constraint: production capacity
        model += lpSum([produce[p] for p in self.products]) <= self.capacity, "Capacity"
        
        # Stage 2 constraints: inventory balance for each scenario
        for s, scenario in enumerate(self.scenarios):
            for p in self.products:
                demand = scenario['demand'][p]
                
                # Production + Backorder = Demand + Inventory
                model += (
                    produce[p] + backorder[(s, p)] ==
                    demand + inventory[(s, p)]
                ), f"Balance_s{s}_{p}"
        
        # Solve
        model.solve(PULP_CBC_CMD(msg=1))
        
        # Extract solution
        if LpStatus[model.status] == 'Optimal':
            
            # Stage 1 solution
            production_plan = {p: produce[p].varValue for p in self.products}
            
            # Stage 2 solution per scenario
            scenario_solutions = []
            for s, scenario in enumerate(self.scenarios):
                scenario_sol = {
                    'scenario': s,
                    'probability': scenario['probability'],
                    'demand': scenario['demand'],
                    'inventory': {p: inventory[(s, p)].varValue for p in self.products},
                    'backorder': {p: backorder[(s, p)].varValue for p in self.products}
                }
                scenario_solutions.append(scenario_sol)
            
            self.solution = {
                'status': 'Optimal',
                'total_cost': value(model.objective),
                'stage1_cost': sum(self.prod_cost[p] * production_plan[p] 
                                  for p in self.products),
                'expected_stage2_cost': value(model.objective) - 
                                       sum(self.prod_cost[p] * production_plan[p] 
                                          for p in self.products),
                'production_plan': production_plan,
                'scenario_solutions': scenario_solutions
            }
            
            return self.solution
        
        else:
            return {'status': LpStatus[model.status]}
    
    def print_solution(self):
        """Print detailed solution"""
        
        if not self.solution:
            print("No solution available!")
            return
        
        print("\n" + "="*70)
        print("TWO-STAGE STOCHASTIC PRODUCTION SOLUTION")
        print("="*70)
        
        print(f"\nTotal Expected Cost: ${self.solution['total_cost']:,.2f}")
        print(f"  Stage 1 (Production): ${self.solution['stage1_cost']:,.2f}")
        print(f"  Expected Stage 2 (Recourse): ${self.solution['expected_stage2_cost']:,.2f}")
        
        print(f"\nStage 1 Decision: Production Plan")
        for product, qty in self.solution['production_plan'].items():
            cost = qty * self.prod_cost[product]
            print(f"  {product}: {qty:.2f} units (${cost:,.2f})")
        
        print(f"\nStage 2 Outcomes by Scenario:")
        for scenario_sol in self.solution['scenario_solutions']:
            s = scenario_sol['scenario']
            prob = scenario_sol['probability']
            
            print(f"\n  Scenario {s} (Probability: {prob:.1%}):")
            print(f"    Demand: {scenario_sol['demand']}")
            print(f"    Inventory: {scenario_sol['inventory']}")
            print(f"    Backorder: {scenario_sol['backorder']}")
            
            # Calculate scenario cost
            inv_cost = sum(self.hold_cost[p] * scenario_sol['inventory'][p] 
                          for p in self.products)
            back_cost = sum(self.back_cost[p] * scenario_sol['backorder'][p] 
                           for p in self.products)
            print(f"    Scenario Cost: ${inv_cost + back_cost:,.2f}")
    
    def plot_solution(self):
        """Visualize production vs demand scenarios"""
        
        if not self.solution:
            return
        
        fig, axes = plt.subplots(1, len(self.products), 
                                figsize=(5*len(self.products), 6))
        
        if len(self.products) == 1:
            axes = [axes]
        
        for idx, product in enumerate(self.products):
            ax = axes[idx]
            
            # Production level (Stage 1 decision)
            production = self.solution['production_plan'][product]
            
            # Demand across scenarios
            scenarios = []
            demands = []
            probs = []
            
            for scenario_sol in self.solution['scenario_solutions']:
                scenarios.append(f"S{scenario_sol['scenario']}")
                demands.append(scenario_sol['demand'][product])
                probs.append(scenario_sol['probability'])
            
            # Plot
            x = np.arange(len(scenarios))
            bars = ax.bar(x, demands, color='lightblue', 
                         edgecolor='black', linewidth=1.5)
            
            # Color bars by probability
            for bar, prob in zip(bars, probs):
                bar.set_alpha(prob * 2)  # Visual weight by probability
            
            # Production line
            ax.axhline(y=production, color='red', linewidth=3, 
                      linestyle='--', label=f'Production: {production:.1f}')
            
            ax.set_xlabel('Scenario', fontsize=12)
            ax.set_ylabel('Quantity', fontsize=12)
            ax.set_title(f'Product {product}', fontsize=14, fontweight='bold')
            ax.set_xticks(x)
            ax.set_xticklabels(scenarios)
            ax.legend()
            ax.grid(True, axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.show()


# Example usage
if __name__ == "__main__":
    
    products = ['A', 'B', 'C']
    
    # Generate demand scenarios
    np.random.seed(42)
    scenarios = [
        {
            'demand': {'A': 100, 'B': 150, 'C': 80},
            'probability': 0.3  # Low demand
        },
        {
            'demand': {'A': 150, 'B': 200, 'C': 120},
            'probability': 0.5  # Medium demand
        },
        {
            'demand': {'A': 200, 'B': 250, 'C': 150},
            'probability': 0.2  # High demand
        }
    ]
    
    # Costs
    production_cost = {'A': 10, 'B': 15, 'C': 12}
    holding_cost = {'A': 2, 'B': 3, 'C': 2}
    backorder_cost = {'A': 50, 'B': 60, 'C': 55}
    
    # Create and solve
    optimizer = TwoStageStochasticProduction(
        products=products,
        scenarios=scenarios,
        production_cost=production_cost,
        holding_cost=holding_cost,
        backorder_cost=backorder_cost,
        capacity=500
    )
    
    result = optimizer.optimize()
    optimizer.print_solution()
    optimizer.plot_solution()
```

---

## Chance-Constrained Optimization

### Probabilistic Constraints

**Chance Constraint:**
```
P(g(x, ξ) ≤ 0) ≥ α

where α is reliability level (e.g., 95%)
```

### Implementation: Inventory with Service Level

```python
import numpy as np
from scipy import stats
from scipy.optimize import minimize

class ChanceConstrainedInventory:
    """
    Inventory Optimization with Service Level Constraints
    
    Minimize cost subject to probabilistic service level
    """
    
    def __init__(self,
                 products: List[str],
                 demand_mean: Dict[str, float],
                 demand_std: Dict[str, float],
                 holding_cost: Dict[str, float],
                 service_level: float = 0.95):
        """
        Initialize chance-constrained model
        
        service_level: probability of meeting demand (e.g., 0.95 = 95%)
        """
        
        self.products = products
        self.demand_mean = demand_mean
        self.demand_std = demand_std
        self.holding_cost = holding_cost
        self.service_level = service_level
        
        # Safety factor for normal distribution
        self.z_alpha = stats.norm.ppf(service_level)
    
    def optimize(self):
        """
        Optimize inventory levels
        
        For normal distribution, chance constraint becomes:
        s ≥ μ + z_α * σ
        
        where s = stock level, μ = mean demand, σ = std dev
        """
        
        print(f"Optimizing Inventory with {self.service_level:.1%} Service Level")
        
        results = {}
        total_cost = 0
        
        for product in self.products:
            mu = self.demand_mean[product]
            sigma = self.demand_std[product]
            h = self.holding_cost[product]
            
            # Chance constraint: P(demand ≤ s) ≥ α
            # For normal: s = μ + z_α * σ
            optimal_stock = mu + self.z_alpha * sigma
            
            # Expected holding cost
            cost = h * optimal_stock
            total_cost += cost
            
            results[product] = {
                'optimal_stock': optimal_stock,
                'safety_stock': self.z_alpha * sigma,
                'expected_demand': mu,
                'holding_cost': cost,
                'service_level': self.service_level
            }
        
        return {
            'products': results,
            'total_cost': total_cost,
            'service_level': self.service_level
        }


# Example
products = ['A', 'B', 'C']
demand_mean = {'A': 100, 'B': 200, 'C': 150}
demand_std = {'A': 20, 'B': 40, 'C': 30}
holding_cost = {'A': 2, 'B': 3, 'C': 2.5}

optimizer = ChanceConstrainedInventory(
    products, demand_mean, demand_std, holding_cost, 
    service_level=0.95
)

result = optimizer.optimize()
print("\nOptimal Inventory Levels:")
for product, data in result['products'].items():
    print(f"{product}: Stock = {data['optimal_stock']:.1f}, "
          f"Safety Stock = {data['safety_stock']:.1f}")
```

---

## Sample Average Approximation (SAA)

### Method

**Approximate E[f(x,ξ)] with sample average:**
```
(1/N) Σ f(x, ξ_i)

where ξ_1, ..., ξ_N are sampled scenarios
```

### Implementation

```python
def sample_average_approximation(problem, n_samples=1000, n_replications=10):
    """
    SAA method for stochastic optimization
    
    1. Generate N scenarios
    2. Solve deterministic equivalent
    3. Repeat M times
    4. Select best solution
    """
    
    best_solution = None
    best_objective = float('inf')
    
    for rep in range(n_replications):
        # Generate scenarios
        scenarios = problem.generate_scenarios(n_samples)
        
        # Solve deterministic equivalent
        solution = problem.solve_deterministic(scenarios)
        
        # Evaluate on different sample (out-of-sample)
        test_scenarios = problem.generate_scenarios(n_samples)
        objective = problem.evaluate(solution, test_scenarios)
        
        if objective < best_objective:
            best_objective = objective
            best_solution = solution
    
    return best_solution, best_objective
```

---

## Risk Measures

### Conditional Value-at-Risk (CVaR)

```python
def optimize_with_cvar(scenarios, alpha=0.95):
    """
    Minimize CVaR (expected cost in worst α% cases)
    
    CVaR_α(X) = E[X | X ≥ VaR_α(X)]
    """
    
    model = LpProblem("CVaR_Optimization", LpMinimize)
    
    # Decision variables
    x = LpVariable.dicts("x", products, lowBound=0)
    
    # VaR variable
    var = LpVariable("VaR", lowBound=None)
    
    # Auxiliary variables for CVaR
    z = LpVariable.dicts("z", range(len(scenarios)), lowBound=0)
    
    # Objective: VaR + (1/(1-α)) * E[max(cost - VaR, 0)]
    model += var + (1/(1-alpha)) * lpSum([
        scenarios[s]['prob'] * z[s]
        for s in range(len(scenarios))
    ]), "CVaR"
    
    # CVaR constraints
    for s in range(len(scenarios)):
        cost_s = calculate_cost(x, scenarios[s])
        model += z[s] >= cost_s - var, f"CVaR_s{s}"
    
    model.solve()
    
    return {
        'solution': {p: x[p].varValue for p in products},
        'VaR': var.varValue,
        'CVaR': value(model.objective)
    }
```

---

## Multi-Stage Stochastic Programming

### Scenario Tree

```
Stage 1 → Stage 2 → Stage 3
   x₁   →  x₂(ξ₁) → x₃(ξ₁,ξ₂)
        →  x₂(ξ₂) → x₃(ξ₂,ξ₃)
```

### Dynamic Programming Approach

```python
def multistage_inventory_dp(T, scenarios_per_stage):
    """
    Multi-stage inventory control with dynamic programming
    
    T: number of stages
    scenarios_per_stage: number of scenarios at each stage
    """
    
    # Value functions
    V = [{} for _ in range(T+1)]
    V[T] = {state: 0 for state in states}  # Terminal value
    
    # Backward recursion
    for t in range(T-1, -1, -1):
        for state in states:
            min_cost = float('inf')
            best_action = None
            
            for action in actions:
                # Expected cost-to-go
                expected_cost = 0
                
                for scenario in scenarios[t]:
                    next_state = transition(state, action, scenario)
                    prob = scenario['probability']
                    
                    immediate_cost = cost(state, action, scenario)
                    future_cost = V[t+1][next_state]
                    
                    expected_cost += prob * (immediate_cost + future_cost)
                
                if expected_cost < min_cost:
                    min_cost = expected_cost
                    best_action = action
            
            V[t][state] = min_cost
    
    return V
```

---

## Tools & Libraries

**Python:**
- `scipy.stats`: probability distributions
- `numpy`: random sampling
- `pulp/pyomo`: stochastic programming formulation
- `SALib`: sensitivity analysis

**Specialized:**
- `PySP (Pyomo)`: stochastic programming extension
- `StochOptim.jl` (Julia): stochastic optimization

**Commercial:**
- `CPLEX Stochastic Solver`
- `Gurobi Multi-Scenario`

---

## Related Skills

- **optimization-modeling**: deterministic optimization
- **demand-forecasting**: uncertainty modeling
- **inventory-optimization**: stochastic inventory
- **risk-mitigation**: risk management
- **scenario-planning**: scenario generation
