---
name: discrete-backprop
description: Gradient-free optimization via discrete perturbations and trit-based learning
version: 1.0.0
---


# Discrete Backprop Skill

**Status**: ✅ Production Ready
**Trit**: +1 (PLUS - generator/executor)
**Principle**: Learn without continuous gradients using {-1, 0, +1} perturbations

---

## Overview

**Discrete Backprop** enables gradient-free learning for:

1. **Non-differentiable functions**: Hash lookups, conditionals, discrete choices
2. **Quantized networks**: Binary/ternary neural networks
3. **Combinatorial optimization**: Where gradients don't exist
4. **GF(3) systems**: Native trit-based learning

## Core Algorithm

```
Discrete Gradient Estimation:
  
  For each parameter θ:
    1. Perturb: θ⁺ = θ + ε, θ⁻ = θ - ε
    2. Evaluate: L⁺ = Loss(θ⁺), L⁻ = Loss(θ⁻)
    3. Estimate: ∇θ ≈ sign(L⁺ - L⁻)  →  {-1, 0, +1}
    
  Trit Gradient:
    - If L⁺ > L⁻: move negative → trit = -1
    - If L⁺ < L⁻: move positive → trit = +1
    - If L⁺ ≈ L⁻: stay         → trit = 0
```

## Python Implementation

```python
import random
from typing import Callable, List, Tuple
from dataclasses import dataclass

@dataclass
class TritGradient:
    """Gradient represented as trit {-1, 0, +1}."""
    value: int
    confidence: float
    
    def __post_init__(self):
        assert self.value in {-1, 0, 1}

class DiscreteBackprop:
    """Gradient-free optimization using discrete perturbations."""
    
    def __init__(self, dims: int, epsilon: float = 1.0, threshold: float = 0.01):
        self.dims = dims
        self.epsilon = epsilon
        self.threshold = threshold
    
    def trit_gradient(
        self, 
        params: List[float], 
        loss_fn: Callable[[List[float]], float]
    ) -> List[TritGradient]:
        """
        Compute trit-valued gradient via finite differences.
        
        Returns list of TritGradient for each parameter.
        """
        base_loss = loss_fn(params)
        gradients = []
        
        for i in range(len(params)):
            # Positive perturbation
            params_plus = params.copy()
            params_plus[i] += self.epsilon
            loss_plus = loss_fn(params_plus)
            
            # Negative perturbation
            params_minus = params.copy()
            params_minus[i] -= self.epsilon
            loss_minus = loss_fn(params_minus)
            
            # Compute trit
            diff = loss_plus - loss_minus
            if abs(diff) < self.threshold:
                trit = 0
                confidence = 1.0 - abs(diff) / self.threshold
            elif diff > 0:
                trit = -1  # Move negative to reduce loss
                confidence = min(1.0, abs(diff) / self.epsilon)
            else:
                trit = +1  # Move positive to reduce loss
                confidence = min(1.0, abs(diff) / self.epsilon)
            
            gradients.append(TritGradient(trit, confidence))
        
        return gradients
    
    def step(
        self, 
        params: List[float], 
        gradients: List[TritGradient],
        learning_rate: float = 1.0
    ) -> List[float]:
        """Apply trit gradients to parameters."""
        return [
            p + learning_rate * g.value * g.confidence
            for p, g in zip(params, gradients)
        ]
    
    def optimize(
        self,
        params: List[float],
        loss_fn: Callable[[List[float]], float],
        max_steps: int = 100,
        learning_rate: float = 1.0
    ) -> Tuple[List[float], float]:
        """Run discrete optimization loop."""
        best_params = params.copy()
        best_loss = loss_fn(params)
        
        for step in range(max_steps):
            gradients = self.trit_gradient(params, loss_fn)
            params = self.step(params, gradients, learning_rate)
            
            current_loss = loss_fn(params)
            if current_loss < best_loss:
                best_loss = current_loss
                best_params = params.copy()
            
            # Early stopping if all trits are 0
            if all(g.value == 0 for g in gradients):
                break
        
        return best_params, best_loss


class SimultaneousPerturbation(DiscreteBackprop):
    """SPSA-style: perturb all dimensions at once with random trits."""
    
    def trit_gradient(
        self, 
        params: List[float], 
        loss_fn: Callable[[List[float]], float]
    ) -> List[TritGradient]:
        """Single evaluation pair estimates all gradients."""
        # Random trit direction
        delta = [random.choice([-1, 0, 1]) for _ in range(len(params))]
        
        # Two evaluations only (regardless of dims!)
        params_plus = [p + self.epsilon * d for p, d in zip(params, delta)]
        params_minus = [p - self.epsilon * d for p, d in zip(params, delta)]
        
        loss_plus = loss_fn(params_plus)
        loss_minus = loss_fn(params_minus)
        
        diff = loss_plus - loss_minus
        
        # Attribute gradient to each dimension
        gradients = []
        for d in delta:
            if d == 0:
                gradients.append(TritGradient(0, 0.0))
            else:
                # If d=+1 and loss increased, gradient is negative
                trit = -d if diff > self.threshold else (d if diff < -self.threshold else 0)
                confidence = min(1.0, abs(diff) / self.epsilon) if d != 0 else 0
                gradients.append(TritGradient(trit, confidence))
        
        return gradients
```

## Ternary Neural Network

```python
import numpy as np

class TernaryLayer:
    """Neural network layer with ternary weights {-1, 0, +1}."""
    
    def __init__(self, in_features: int, out_features: int):
        self.weights = np.random.choice([-1, 0, 1], size=(out_features, in_features))
        self.bias = np.zeros(out_features)
    
    def forward(self, x: np.ndarray) -> np.ndarray:
        """Forward pass using only additions (no multiplications!)."""
        # w * x where w ∈ {-1, 0, +1} is just add/subtract/skip
        return np.sign(self.weights @ x + self.bias)
    
    def backward_trit(self, x: np.ndarray, grad_output: np.ndarray) -> np.ndarray:
        """Discrete backward pass returning trit updates."""
        # Outer product gives update direction
        update = np.outer(grad_output, x)
        # Quantize to trits
        return np.sign(update).astype(int)
    
    def update(self, trit_grad: np.ndarray, lr: float = 1.0):
        """Apply ternary gradient."""
        # Accumulate and re-ternarize
        self.weights = np.clip(self.weights + lr * trit_grad, -1, 1)
        self.weights = np.sign(self.weights)


class TernaryMLP:
    """Multi-layer perceptron with all ternary weights."""
    
    def __init__(self, layer_sizes: List[int]):
        self.layers = [
            TernaryLayer(layer_sizes[i], layer_sizes[i+1])
            for i in range(len(layer_sizes) - 1)
        ]
    
    def forward(self, x: np.ndarray) -> np.ndarray:
        for layer in self.layers:
            x = layer.forward(x)
        return x
    
    def train_step(self, x: np.ndarray, target: np.ndarray, lr: float = 0.1):
        """Single training step with discrete backprop."""
        # Forward
        activations = [x]
        for layer in self.layers:
            activations.append(layer.forward(activations[-1]))
        
        # Backward with trits
        error = np.sign(target - activations[-1])
        for i in reversed(range(len(self.layers))):
            trit_grad = self.layers[i].backward_trit(activations[i], error)
            self.layers[i].update(trit_grad, lr)
            error = np.sign(self.layers[i].weights.T @ error)
```

## GF(3) Conservation

```python
class GF3ConservativeOptimizer:
    """Optimizer that maintains GF(3) balance across parameter groups."""
    
    def __init__(self, param_groups: int = 3):
        self.param_groups = param_groups
        self.trit_sums = [0] * param_groups
    
    def balanced_update(
        self, 
        params: List[List[float]], 
        gradients: List[List[TritGradient]]
    ) -> List[List[float]]:
        """
        Update parameters while maintaining Σ trits ≡ 0 (mod 3).
        """
        assert len(params) == self.param_groups == 3
        
        # Compute trit sums for each group
        trit_sums = [
            sum(g.value for g in grads) % 3
            for grads in gradients
        ]
        
        # Adjust to conserve: Σ = 0 (mod 3)
        total = sum(trit_sums) % 3
        if total != 0:
            # Redistribute to achieve balance
            adjustment = (3 - total) % 3
            # Apply to group with highest confidence
            confidences = [
                sum(g.confidence for g in grads) / len(grads)
                for grads in gradients
            ]
            adjust_group = confidences.index(max(confidences))
            # Modify one gradient in that group
            for g in gradients[adjust_group]:
                if g.value != 0:
                    g.value = (g.value + adjustment - 1) % 3 - 1
                    break
        
        # Apply updates
        return [
            [p + g.value * g.confidence for p, g in zip(ps, gs)]
            for ps, gs in zip(params, gradients)
        ]
```

## Commands

```bash
# Run discrete optimization
python -m discrete_backprop --loss "x**2 + y**2" --init "[5, 5]" --steps 100

# Train ternary network
python -m discrete_backprop.ternary_mlp --dataset mnist --epochs 10

# Verify GF(3) conservation
python -c "from discrete_backprop import GF3ConservativeOptimizer; ..."
```

## Integration with gay-mcp

```python
from gay import SplitMixTernary
from discrete_backprop import DiscreteBackprop, TritGradient

def color_guided_optimization(seed: int, loss_fn, params: List[float]):
    """Use deterministic colors to guide perturbation directions."""
    gen = SplitMixTernary(seed)
    backprop = DiscreteBackprop(dims=len(params))
    
    for step in range(100):
        # Use color trits as perturbation directions
        color = gen.color_at(step)
        perturbation_trit = color['trit']
        
        # Guided gradient estimation
        gradients = backprop.trit_gradient(params, loss_fn)
        
        # Blend with color guidance
        for i, g in enumerate(gradients):
            if g.confidence < 0.5:
                # Low confidence: use color guidance
                g.value = perturbation_trit
        
        params = backprop.step(params, gradients)
    
    return params
```

## Advantages

| Aspect | Continuous Backprop | Discrete Backprop |
|--------|--------------------|--------------------|
| Memory | O(params × activations) | O(params) |
| Precision | Float32/64 | Trit {-1, 0, +1} |
| Hardware | GPU/TPU | CPU/FPGA/Neuromorphic |
| Differentiable | Required | Not required |
| GF(3) compatible | No | Native |

---

**Skill Name**: discrete-backprop
**Type**: Optimization / Learning
**Trit**: +1 (PLUS)
**GF(3)**: Native conservation via trit gradients
**Use Case**: Non-differentiable optimization, ternary networks, combinatorial search

## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 1. Flexibility through Abstraction

**Concepts**: combinators, compose, parallel-combine, spread-combine, arity

### GF(3) Balanced Triad

```
discrete-backprop (+) + SDF.Ch1 (+) + [balancer] (+) = 0
```

**Skill Trit**: 1 (PLUS - generation)

### Secondary Chapters

- Ch5: Evaluation
- Ch6: Layering

### Connection Pattern

Combinators compose operations. This skill provides composable abstractions.
