---
name: optimization-ml-hybrid
description: When the user wants to combine machine learning with optimization, use ML predictions in optimization models, or integrate AI with mathematical programming. Also use when the user mentions "ML-optimization hybrid," "predict-then-optimize," "learning-augmented optimization," "neural network in optimization," "end-to-end learning," or "ML for optimization parameters." For pure optimization, see optimization-modeling. For pure ML, see ml-supply-chain.
---

# Optimization-ML Hybrid Approaches

You are an expert in combining machine learning with mathematical optimization for supply chain. Your goal is to integrate ML predictions into optimization models, learn optimization parameters, and create end-to-end learning systems.

## Key Patterns

### 1. Predict-Then-Optimize

```python
# Step 1: ML predicts demand
demand_forecast = ml_model.predict(features)

# Step 2: Optimization uses forecast
optimal_production = optimize_production(demand_forecast)
```

### 2. ML for Optimization Parameters

```python
# Learn optimal parameters from data
safety_stock = ml_model.predict([sku_features, demand_history])

# Use in inventory optimization
reorder_point = expected_demand_during_leadtime + safety_stock
```

### 3. End-to-End Learning

```python
# Differentiable optimization layer
class OptimizationLayer(nn.Module):
    def forward(self, predictions):
        # Solve optimization with predictions
        # Backpropagate through optimization
        return optimal_decisions
```

---

## Smart Predict-Then-Optimize

```python
from sklearn.ensemble import RandomForestRegressor
from pulp import *

class PredictThenOptimize:
    """
    ML forecasting + Optimization planning
    """
    
    def __init__(self):
        self.ml_model = RandomForestRegressor()
        self.opt_model = None
    
    def train_ml(self, X_train, y_train):
        """Train ML forecast model"""
        self.ml_model.fit(X_train, y_train)
    
    def optimize_with_forecast(self, features, costs):
        """Optimize using ML predictions"""
        
        # Step 1: Predict demand
        demand_forecast = self.ml_model.predict(features)
        
        # Step 2: Optimize production
        model = LpProblem("Production", LpMinimize)
        
        products = range(len(demand_forecast))
        produce = LpVariable.dicts("Prod", products, lowBound=0)
        
        # Objective: minimize cost
        model += lpSum([costs[i] * produce[i] for i in products])
        
        # Constraints: meet forecasted demand
        for i in products:
            model += produce[i] >= demand_forecast[i]
        
        model.solve()
        
        return {i: produce[i].varValue for i in products}
```

---

## Learning Optimization Heuristics

```python
class MLOptimizationHeuristic:
    """
    Learn when to apply optimization heuristics
    """
    
    def __init__(self):
        self.classifier = RandomForestClassifier()
    
    def train(self, problem_features, best_heuristic_labels):
        """
        Learn which heuristic works best for problem instance
        """
        self.classifier.fit(problem_features, best_heuristic_labels)
    
    def select_heuristic(self, problem_instance):
        """Predict best heuristic for new problem"""
        features = extract_features(problem_instance)
        heuristic_id = self.classifier.predict([features])[0]
        
        return HEURISTICS[heuristic_id]
```

---

## Neural Network Warm Start

```python
def neural_warm_start(model, problem_instance):
    """
    Use NN to generate initial solution for optimization
    """
    
    # NN predicts good initial solution
    features = extract_features(problem_instance)
    initial_solution = nn_model.predict(features)
    
    # Use as warm start in MIP
    for var_name, value in initial_solution.items():
        model.variables[var_name].setInitialValue(value)
    
    model.solve()
```

---

## Graph Neural Networks for Routing

```python
class GNNRouter:
    """
    GNN to learn routing heuristics
    """
    
    def __init__(self):
        self.gnn = GraphNeuralNetwork()
    
    def embed_vrp_instance(self, customers, depot):
        """Convert VRP to graph"""
        
        # Nodes: customers + depot
        # Edges: distances
        graph = create_graph(customers, depot)
        
        return graph
    
    def predict_route(self, graph):
        """
        GNN predicts edge probabilities
        Use to construct route
        """
        
        edge_probs = self.gnn(graph)
        route = construct_route_from_probs(edge_probs)
        
        return route
```

---

## Tools & Libraries

- `cvxpylayers`: Differentiable optimization
- `OptNet`: Optimization as NN layer
- `qpth`: QP layer for PyTorch
- `SciPy + PyTorch`: custom integration

---

## Related Skills

- **optimization-modeling**: mathematical programming
- **ml-supply-chain**: machine learning
- **metaheuristic-optimization`: heuristics
- **reinforcement-learning-supply-chain**: RL integration
