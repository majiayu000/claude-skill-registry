---
name: gflownet
description: "Bengio's GFlowNets: Generative Flow Networks that sample proportionally to reward. Diversity over maximization for causal discovery and molecule design."
version: 1.0.0
---


# GFlowNet Skill

> *"Sample x with probability proportional to R(x), not just maximize R(x)."*
> — Yoshua Bengio

## Overview

**GFlowNets** (Generative Flow Networks) are a new paradigm:
- **RL**: Maximize expected reward → single optimal solution
- **MCMC**: Sample from distribution → slow mixing
- **GFlowNet**: Learn to sample P(x) ∝ R(x) → fast, diverse sampling

## Core Concept

```latex
GFlowNet Objective:

∀ terminal state x:  P_θ(x) = R(x) / Z

Where:
  P_θ(x) = probability of generating x via forward policy
  R(x) = unnormalized reward function
  Z = partition function (normalizing constant)

Key Insight: We DON'T need to know Z to train!
```

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                    GFlowNet                         │
├─────────────────────────────────────────────────────┤
│  Initial State s₀                                   │
│        │                                            │
│        ▼                                            │
│  ┌─────────────┐                                    │
│  │ Forward     │  P_F(s' | s) = learned policy      │
│  │ Policy      │                                    │
│  └──────┬──────┘                                    │
│         │ sample action                             │
│         ▼                                            │
│  ┌─────────────┐                                    │
│  │ Transition  │  s → s'                            │
│  └──────┬──────┘                                    │
│         │                                            │
│         ▼                                            │
│  ┌─────────────┐                                    │
│  │ Terminal?   │───No──▶ continue                   │
│  └──────┬──────┘                                    │
│         │ Yes                                        │
│         ▼                                            │
│  ┌─────────────┐                                    │
│  │ R(x)        │  Evaluate reward                   │
│  └─────────────┘                                    │
└─────────────────────────────────────────────────────┘
```

## Training Objectives

### 1. Trajectory Balance (TB)

```python
def trajectory_balance_loss(trajectory: List[State], reward: float) -> Tensor:
    """
    TB: Z × Π P_F(s_t → s_{t+1}) = R(x) × Π P_B(s_{t+1} → s_t)
    
    In log space:
    log Z + Σ log P_F = log R + Σ log P_B
    """
    log_Z = self.log_Z  # Learnable parameter
    
    log_P_F = sum(self.forward_policy.log_prob(s, s_next) 
                  for s, s_next in zip(trajectory[:-1], trajectory[1:]))
    
    log_P_B = sum(self.backward_policy.log_prob(s_next, s)
                  for s, s_next in zip(trajectory[:-1], trajectory[1:]))
    
    loss = (log_Z + log_P_F - torch.log(reward) - log_P_B) ** 2
    return loss
```

### 2. Detailed Balance (DB)

```python
def detailed_balance_loss(s: State, s_next: State, reward_s: float) -> Tensor:
    """
    DB: F(s) × P_F(s → s') = F(s') × P_B(s' → s)
    
    Where F(s) = learned flow function.
    """
    log_F_s = self.flow_network(s)
    log_F_s_next = self.flow_network(s_next)
    
    log_P_F = self.forward_policy.log_prob(s, s_next)
    log_P_B = self.backward_policy.log_prob(s_next, s)
    
    loss = (log_F_s + log_P_F - log_F_s_next - log_P_B) ** 2
    return loss
```

## Applications

### 1. Molecule Design

```python
# GFlowNet for drug discovery
class MoleculeGFlowNet:
    def __init__(self):
        self.action_space = ['add_atom', 'add_bond', 'terminate']
        
    def sample_molecule(self) -> SMILES:
        state = EmptyMolecule()
        while not state.is_terminal():
            action = self.forward_policy.sample(state)
            state = state.apply(action)
        return state.to_smiles()
    
    def reward(self, molecule: SMILES) -> float:
        # Combines: drug-likeness, binding affinity, synthesizability
        return docking_score(molecule) * qed(molecule)
```

### 2. Causal Discovery

```python
# GFlowNet for DAG sampling
class CausalDAGGFlowNet:
    def __init__(self, n_variables: int):
        self.n = n_variables
        
    def sample_dag(self) -> DAG:
        """Sample DAG with P(G) ∝ P(data | G)."""
        dag = EmptyDAG(self.n)
        while not dag.is_complete():
            edge = self.forward_policy.sample(dag)
            if not dag.would_create_cycle(edge):
                dag.add_edge(edge)
        return dag
```

### 3. Combinatorial Optimization

```python
# GFlowNet for set generation
class SetGFlowNet:
    def sample_set(self, universe: Set) -> Set:
        """Sample set S with P(S) ∝ R(S)."""
        current_set = set()
        for element in self.ordering(universe):
            include = self.forward_policy.sample(current_set, element)
            if include:
                current_set.add(element)
        return current_set
```

## GF(3) Triads

```
# Causal-Categorical Triad
sheaf-cohomology (-1) ⊗ cognitive-superposition (0) ⊗ gflownet (+1) = 0 ✓

# Diversity Triad
persistent-homology (-1) ⊗ glass-bead-game (0) ⊗ gflownet (+1) = 0 ✓

# Sampling Triad
three-match (-1) ⊗ epistemic-arbitrage (0) ⊗ gflownet (+1) = 0 ✓
```

## Integration with Interaction Entropy

```ruby
module GFlowNet
  def self.sample_proportional(candidates, reward_fn, seed)
    gen = SplitMixTernary::Generator.new(seed)
    
    # Build forward trajectory
    trajectory = []
    state = initial_state
    
    until terminal?(state)
      # Use color to guide sampling
      color = gen.next_color
      action = select_action(state, color)
      next_state = transition(state, action)
      trajectory << { state: state, action: action, color: color }
      state = next_state
    end
    
    reward = reward_fn.call(state)
    
    {
      terminal_state: state,
      reward: reward,
      trajectory: trajectory,
      trit: 1  # Generator (creates diverse samples)
    }
  end
end
```

## Key Properties

1. **Amortized**: Learn once, sample many times (unlike MCMC per-problem)
2. **Off-policy**: Can train on any trajectories
3. **Diverse**: Samples cover modes proportionally to reward
4. **Compositional**: Build complex objects step-by-step

## References

1. Bengio, E. et al. (2021). "Flow Network Based Generative Models for Non-Iterative Diverse Candidate Generation."
2. Malkin, N. et al. (2022). "Trajectory Balance: Improved Credit Assignment in GFlowNets."
3. Deleu, T. et al. (2022). "Bayesian Structure Learning with Generative Flow Networks."
4. [torchgfn library](https://github.com/GFNOrg/torchgfn)



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `dynamical-systems`: 41 citations in bib.duckdb

## Cat# Integration

This skill maps to **Cat# = Comod(P)** as a bicomodule in the equipment structure:

```
Trit: 0 (ERGODIC)
Home: Prof
Poly Op: ⊗
Kan Role: Adj
Color: #26D826
```

### GF(3) Naturality

The skill participates in triads satisfying:
```
(-1) + (0) + (+1) ≡ 0 (mod 3)
```

This ensures compositional coherence in the Cat# equipment structure.