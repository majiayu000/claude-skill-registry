---
name: entropy-sim2real
description: Entropy-driven sim2real transfer. Uses maximum entropy RL, domain randomization, and information-theoretic bridging to close the reality gap.
version: 1.0.0
category: robotics-transfer
author: Plurigrid
source: plurigrid/asi
license: MIT
trit: -1
trit_label: MINUS
color: "#E85B8E"
verified: false
featured: true
---

# Entropy-Driven Sim2Real Transfer

**Trit**: -1 (MINUS - analysis/verification)
**Color**: #E85B8E (Rose Pink)
**URI**: skill://entropy-sim2real#E85B8E

## Core Insight

**Entropy bridges the sim-real gap by:**

1. **Maximizing entropy in simulation** → Policy sees diverse conditions
2. **Minimizing entropy at deployment** → Uncertainty collapses to reality
3. **Information-theoretic alignment** → Match distributions, not parameters

```
                    SIMULATION                      REALITY
                    
    High Entropy ─────────────────────────────▶ Low Entropy
    
    H(params) = max     ══════════▶      H(params) ≈ 0
    H(π|s) = high       ══════════▶      H(π|s) = focused
    p(sim) = broad      ══════════▶      p(real) = delta
    
    ┌─────────────────┐                ┌─────────────────┐
    │  MANY POSSIBLE  │    BRIDGE     │   ONE ACTUAL    │
    │     WORLDS      │───────────────│     WORLD       │
    │   (superpos.)   │               │   (collapsed)   │
    └─────────────────┘                └─────────────────┘
```

## Three Entropy Mechanisms

### 1. Domain Randomization Entropy

Maximize entropy over simulation parameters:

```python
import jax
import jax.numpy as jnp
from typing import Dict

class EntropyMaximizingRandomizer:
    """Domain randomization that maximizes parameter entropy."""
    
    def __init__(self, param_ranges: Dict[str, tuple]):
        self.param_ranges = param_ranges
        
    def entropy(self, distribution: str = "uniform") -> float:
        """Compute entropy of parameter distributions."""
        H = 0.0
        for name, (low, high) in self.param_ranges.items():
            if distribution == "uniform":
                # H(Uniform) = log(b - a)
                H += jnp.log(high - low)
            elif distribution == "gaussian":
                # H(Gaussian) = 0.5 * log(2πeσ²)
                sigma = (high - low) / 4  # 95% within range
                H += 0.5 * jnp.log(2 * jnp.pi * jnp.e * sigma**2)
        return H
    
    def sample(self, key: jax.random.PRNGKey) -> Dict[str, float]:
        """Sample parameters to maximize coverage."""
        params = {}
        for i, (name, (low, high)) in enumerate(self.param_ranges.items()):
            k = jax.random.fold_in(key, i)
            # Uniform maximizes entropy for bounded support
            params[name] = jax.random.uniform(k, minval=low, maxval=high)
        return params
    
    def adaptive_entropy(
        self, 
        key: jax.random.PRNGKey,
        real_samples: jnp.ndarray,
        temperature: float = 1.0
    ) -> Dict[str, float]:
        """
        Adapt randomization to maximize coverage of real distribution.
        
        Uses maximum entropy principle: find distribution with highest
        entropy subject to matching observed moments.
        """
        # Estimate real distribution moments
        real_mean = jnp.mean(real_samples, axis=0)
        real_var = jnp.var(real_samples, axis=0)
        
        # Maximum entropy distribution matching moments = Gaussian
        params = {}
        for i, (name, _) in enumerate(self.param_ranges.items()):
            k = jax.random.fold_in(key, i)
            # Sample from Gaussian matching real moments (max entropy)
            params[name] = jax.random.normal(k) * jnp.sqrt(real_var[i]) + real_mean[i]
        
        return params
```

### 2. Maximum Entropy RL

Policy optimization with entropy regularization:

```python
class MaxEntropyPPO:
    """
    PPO with entropy bonus for robust sim2real.
    
    Objective: max E[Σ γᵗ(rₜ + α·H(π(·|sₜ)))]
    
    High entropy → diverse actions → robust to perturbations
    """
    
    def __init__(
        self,
        entropy_coef: float = 0.01,
        target_entropy: float = -1.0,
        auto_tune: bool = True
    ):
        self.alpha = entropy_coef
        self.target_entropy = target_entropy
        self.auto_tune = auto_tune
        
        if auto_tune:
            # Learnable temperature (SAC-style)
            self.log_alpha = jnp.log(entropy_coef)
    
    def policy_entropy(self, logits: jnp.ndarray) -> float:
        """Compute policy entropy H(π) = -Σ π(a)log(π(a))."""
        probs = jax.nn.softmax(logits)
        log_probs = jax.nn.log_softmax(logits)
        return -jnp.sum(probs * log_probs, axis=-1).mean()
    
    def gaussian_entropy(self, std: jnp.ndarray) -> float:
        """Entropy of Gaussian policy: H = 0.5 * log(2πeσ²)."""
        return 0.5 * jnp.log(2 * jnp.pi * jnp.e * std**2).sum(axis=-1).mean()
    
    def entropy_loss(
        self, 
        policy_entropy: float,
        update_alpha: bool = True
    ) -> tuple:
        """
        Compute entropy loss and optionally update temperature.
        
        We want: H(π) ≥ H_target
        Loss: α * (H(π) - H_target)
        """
        entropy_bonus = self.alpha * policy_entropy
        
        if self.auto_tune and update_alpha:
            # Dual gradient descent on temperature
            alpha_loss = -self.log_alpha * (policy_entropy - self.target_entropy)
            return entropy_bonus, alpha_loss
        
        return entropy_bonus, 0.0
    
    def robust_policy_loss(
        self,
        advantages: jnp.ndarray,
        log_probs: jnp.ndarray,
        old_log_probs: jnp.ndarray,
        policy_entropy: float,
        clip_ratio: float = 0.2
    ) -> float:
        """
        PPO loss with entropy regularization.
        
        L = L_clip + α·H(π)
        
        High entropy prevents overconfident policies that
        fail on real hardware.
        """
        # Standard PPO clipped objective
        ratio = jnp.exp(log_probs - old_log_probs)
        clipped = jnp.clip(ratio, 1 - clip_ratio, 1 + clip_ratio)
        policy_loss = -jnp.minimum(ratio * advantages, clipped * advantages).mean()
        
        # Entropy bonus (negative because we minimize loss)
        entropy_bonus = -self.alpha * policy_entropy
        
        return policy_loss + entropy_bonus
```

### 3. Information-Theoretic Bridging

Minimize information gap between sim and real:

```python
class InformationTheoreticBridge:
    """
    Bridge sim and real via information-theoretic measures.
    
    Key insight: We can't match physics exactly, but we can
    match the *information content* of observations.
    """
    
    def mutual_information(
        self,
        sim_obs: jnp.ndarray,
        real_obs: jnp.ndarray
    ) -> float:
        """
        Estimate I(sim; real) - how much sim tells us about real.
        
        High MI = sim is predictive of real (good!)
        Low MI = sim and real are independent (bad!)
        """
        # Use MINE estimator or simple correlation
        joint_cov = jnp.cov(sim_obs.T, real_obs.T)
        n = sim_obs.shape[1]
        cov_sim = joint_cov[:n, :n]
        cov_real = joint_cov[n:, n:]
        cov_joint = joint_cov
        
        # MI = 0.5 * log(|Σ_sim||Σ_real| / |Σ_joint|)
        mi = 0.5 * (
            jnp.linalg.slogdet(cov_sim)[1] +
            jnp.linalg.slogdet(cov_real)[1] -
            jnp.linalg.slogdet(cov_joint)[1]
        )
        return mi
    
    def domain_divergence(
        self,
        sim_obs: jnp.ndarray,
        real_obs: jnp.ndarray,
        method: str = "wasserstein"
    ) -> float:
        """
        Measure divergence between sim and real distributions.
        
        Lower divergence = better sim2real transfer.
        """
        if method == "kl":
            # KL(real || sim) - how surprised is sim by real?
            # Requires density estimation
            pass
            
        elif method == "wasserstein":
            # W_2 distance (optimal transport)
            mu_sim = jnp.mean(sim_obs, axis=0)
            mu_real = jnp.mean(real_obs, axis=0)
            cov_sim = jnp.cov(sim_obs.T)
            cov_real = jnp.cov(real_obs.T)
            
            # W_2² = ||μ_sim - μ_real||² + Tr(Σ_sim + Σ_real - 2(Σ_sim^½ Σ_real Σ_sim^½)^½)
            mean_diff = jnp.sum((mu_sim - mu_real)**2)
            
            # Simplified: use Frobenius norm of covariance difference
            cov_diff = jnp.sum((cov_sim - cov_real)**2)
            
            return jnp.sqrt(mean_diff + cov_diff)
            
        elif method == "mmd":
            # Maximum Mean Discrepancy
            from functools import partial
            
            def rbf_kernel(x, y, sigma=1.0):
                return jnp.exp(-jnp.sum((x - y)**2) / (2 * sigma**2))
            
            n, m = len(sim_obs), len(real_obs)
            
            # MMD² = E[k(x,x')] + E[k(y,y')] - 2E[k(x,y)]
            xx = jnp.mean(jax.vmap(lambda x: jax.vmap(lambda x2: rbf_kernel(x, x2))(sim_obs))(sim_obs))
            yy = jnp.mean(jax.vmap(lambda y: jax.vmap(lambda y2: rbf_kernel(y, y2))(real_obs))(real_obs))
            xy = jnp.mean(jax.vmap(lambda x: jax.vmap(lambda y: rbf_kernel(x, y))(real_obs))(sim_obs))
            
            return xx + yy - 2 * xy
    
    def entropy_matching_loss(
        self,
        sim_obs: jnp.ndarray,
        real_obs: jnp.ndarray
    ) -> float:
        """
        Match entropy profiles between sim and real.
        
        If H(sim) >> H(real): sim too noisy, reduce randomization
        If H(sim) << H(real): sim too deterministic, increase randomization
        """
        def estimate_entropy(obs):
            # Estimate via covariance determinant (Gaussian assumption)
            cov = jnp.cov(obs.T)
            return 0.5 * jnp.linalg.slogdet(cov)[1]
        
        H_sim = estimate_entropy(sim_obs)
        H_real = estimate_entropy(real_obs)
        
        return (H_sim - H_real)**2
```

## The Entropy Bridge Pipeline

```
┌────────────────────────────────────────────────────────────────────┐
│                    ENTROPY-DRIVEN SIM2REAL                         │
├────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  PHASE 1: Maximum Entropy Simulation                               │
│  ────────────────────────────────────                              │
│                                                                     │
│    Domain Params         Policy                 Observations       │
│    ┌─────────────┐      ┌─────────────┐        ┌─────────────┐    │
│    │ H(θ) = max  │ ───▶ │ H(π|s) = αT │ ───▶  │ H(o) = high │    │
│    │ friction ∈  │      │ explore all │        │ diverse     │    │
│    │ [0.3, 1.5]  │      │ actions     │        │ experiences │    │
│    │ mass ∈      │      └─────────────┘        └─────────────┘    │
│    │ [0.8, 1.2]  │                                                 │
│    └─────────────┘                                                 │
│                                                                     │
│  PHASE 2: Information Bridge                                       │
│  ───────────────────────────                                       │
│                                                                     │
│    Sim Distribution        Divergence          Real Distribution   │
│    ┌─────────────┐        ┌─────────────┐     ┌─────────────┐     │
│    │  p(o|sim)   │ ──────▶│ W(sim,real) │◀─── │  p(o|real)  │     │
│    │  (broad)    │        │ minimize    │     │  (narrow)   │     │
│    └─────────────┘        └─────────────┘     └─────────────┘     │
│                                  │                                  │
│                           Adapt randomization                      │
│                           to match real entropy                    │
│                                                                     │
│  PHASE 3: Entropy Collapse at Deployment                          │
│  ────────────────────────────────────────                          │
│                                                                     │
│    Policy trained on      Deployed on          Result              │
│    ┌─────────────┐       ┌─────────────┐      ┌─────────────┐     │
│    │ ALL possible│  ───▶ │ ONE actual  │ ───▶ │ ROBUST to   │     │
│    │ worlds      │       │ world       │      │ any world   │     │
│    │ (superpos.) │       │ (collapsed) │      │ in support  │     │
│    └─────────────┘       └─────────────┘      └─────────────┘     │
│                                                                     │
└────────────────────────────────────────────────────────────────────┘
```

## Integration with K-Scale Stack

```python
from ksim import PPOTask, PhysicsRandomizer
from ksim.randomizers import (
    StaticFrictionRandomizer,
    MassMultiplicationRandomizer,
    JointDampingRandomizer,
)

class EntropyBridgedKBotTask(PPOTask):
    """K-Bot training with entropy-driven sim2real."""
    
    # High-entropy domain randomization
    physics_randomizers = [
        StaticFrictionRandomizer(scale=0.5),      # Wide friction range
        MassMultiplicationRandomizer(             # Body mass variation
            body_name="torso",
            scale=0.2
        ),
        JointDampingRandomizer(scale=0.3),        # Damping variation
        # ... more randomizers for max entropy
    ]
    
    # Max-entropy RL config
    entropy_coef = 0.02      # High entropy bonus
    target_entropy = -4.0    # Automatic temperature tuning
    
    def compute_entropy_metrics(self, trajectory):
        """Track entropy throughout training."""
        policy_entropy = self.policy.entropy(trajectory.obs)
        obs_entropy = self.estimate_obs_entropy(trajectory.obs)
        
        return {
            "policy_entropy": policy_entropy,
            "observation_entropy": obs_entropy,
            "entropy_ratio": policy_entropy / obs_entropy,
        }
    
    def adapt_randomization(self, real_data):
        """
        Adapt domain randomization to match real robot entropy.
        
        This is the key insight: we don't try to match exact
        parameters, we match the *entropy profile*.
        """
        sim_obs = self.collect_sim_observations()
        real_obs = real_data.observations
        
        # Compute entropy gap
        H_sim = self.estimate_entropy(sim_obs)
        H_real = self.estimate_entropy(real_obs)
        
        if H_sim > H_real * 1.5:
            # Sim too noisy, reduce randomization
            self.reduce_randomization_scale(0.9)
        elif H_sim < H_real * 0.7:
            # Sim too deterministic, increase randomization
            self.increase_randomization_scale(1.1)
        
        # Match distribution via Wasserstein
        W = self.wasserstein_distance(sim_obs, real_obs)
        self.log("wasserstein_distance", W)
```

## Why Entropy Works for Sim2Real

### 1. Coverage Guarantee

```
If policy π is optimal for ALL sims in support of p(sim),
and real world ∈ support of p(sim),
then π works in real world.

Key: Entropy maximization → widest possible support
```

### 2. Robustness via Exploration

```
High H(π|s) → policy doesn't overfit to single solution
            → maintains multiple viable strategies
            → can adapt when reality differs
```

### 3. Information Bottleneck

```
Sim and real share mutual information I(sim; real)
Maximize I → sim captures what matters about real
Ignore I → overfit to sim-specific artifacts
```

## GF(3) Triads

```
entropy-sim2real (-1) ⊗ kos-firmware (+1) ⊗ mujoco-scenes (0) = 0 ✓
entropy-sim2real (-1) ⊗ jaxlife-open-ended (+1) ⊗ wobble-dynamics (0) = 0 ✓
ksim-rl (-1) ⊗ kos-firmware (+1) ⊗ entropy-sim2real (-1) = needs +1
```

## Related Skills

- `ksim-rl` (-1): Base RL training
- `kos-firmware` (+1): Deployment target
- `ergodicity` (0): Ergodic theory foundations
- `birkhoff-average` (-1): Time averages
- `fokker-planck-analyzer` (-1): Distribution dynamics

## References

```bibtex
@article{haarnoja2018sac,
  title={Soft Actor-Critic: Off-Policy Maximum Entropy Deep RL},
  author={Haarnoja, Tuomas and others},
  journal={ICML},
  year={2018}
}

@article{tobin2017domain,
  title={Domain Randomization for Transferring Deep Neural Networks},
  author={Tobin, Josh and others},
  journal={IROS},
  year={2017}
}

@article{zhao2020sim,
  title={Sim-to-Real Transfer in Deep Reinforcement Learning},
  author={Zhao, Wenshuai and others},
  journal={IEEE TNNLS},
  year={2020}
}
```


## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 8. Degeneracy

**Concepts**: redundancy, fallback, multiple strategies, robustness

### GF(3) Balanced Triad

```
entropy-sim2real (○) + SDF.Ch8 (−) + [balancer] (+) = 0
```

**Skill Trit**: 0 (ERGODIC - coordination)

### Secondary Chapters

- Ch4: Pattern Matching
- Ch1: Flexibility through Abstraction
- Ch10: Adventure Game Example

### Connection Pattern

Degeneracy provides fallbacks. This skill offers redundant strategies.
