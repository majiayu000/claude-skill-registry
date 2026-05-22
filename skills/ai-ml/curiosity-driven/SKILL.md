---
name: curiosity-driven
description: "Schmidhuber's curiosity-driven learning: Intrinsic motivation via compression progress. Seek states that improve world model."
version: 1.0.0
---


# Curiosity-Driven Learning Skill

> *"Curiosity is the desire to observe data that improves the observer's world model."*
> — Jürgen Schmidhuber

## Overview

**Curiosity-driven learning** provides intrinsic motivation:
- **Extrinsic**: Rewards from environment (sparse, delayed)
- **Intrinsic**: Rewards from learning itself (dense, immediate)

**Compression Progress** = how much better we compress after seeing data.

## Core Concept

```latex
Curiosity Reward = L(t-1) - L(t)

Where:
  L(t) = Description length of history at time t
  L(t-1) = Description length before update
  
Positive reward = "I learned something compressible!"
Negative/zero = "This is noise or already known"
```

## Implementation

```python
class CuriosityDrivenAgent:
    """
    Agent that seeks compression progress.
    """
    
    def __init__(self, world_model: nn.Module, compressor: nn.Module):
        self.world_model = world_model
        self.compressor = compressor
    
    def compression_progress(self, observation: Tensor) -> float:
        """
        Curiosity = improvement in compression ability.
        """
        # Compress before learning
        with torch.no_grad():
            len_before = self.compressor.description_length(observation)
        
        # Update world model with observation
        loss = self.world_model.update(observation)
        
        # Compress after learning
        with torch.no_grad():
            len_after = self.compressor.description_length(observation)
        
        # Progress = reduction in description length
        return len_before - len_after
    
    def intrinsic_reward(self, obs: Tensor) -> float:
        """
        Intrinsic reward for RL agent.
        """
        return self.compression_progress(obs)
    
    def explore(self) -> Action:
        """
        Seek states that maximize expected compression progress.
        
        This is NOT the same as seeking novel states!
        - Novel but random → no compression progress
        - Learnable patterns → high compression progress
        """
        best_action = None
        best_expected_progress = -float('inf')
        
        for action in self.action_space:
            # Predict resulting state
            predicted_obs = self.world_model.predict(self.state, action)
            
            # Estimate learnability (how much would we learn?)
            expected_progress = self.estimate_learnability(predicted_obs)
            
            if expected_progress > best_expected_progress:
                best_action = action
                best_expected_progress = expected_progress
        
        return best_action
    
    def estimate_learnability(self, obs: Tensor) -> float:
        """
        Predict how much we'd learn from this observation.
        
        High for: novel patterns, surprising regularities
        Low for: random noise, already-known patterns
        """
        # Use meta-learning: "how learnable is this?"
        return self.meta_model.predict_learnability(obs)
```

## Distinction from Other Curiosity Methods

| Method | Reward Signal | Schmidhuber's View |
|--------|---------------|-------------------|
| **ICM** (Pathak) | Prediction error | Noise-sensitive |
| **RND** | Novelty | Doesn't distinguish learnable from random |
| **Compression Progress** | Learning improvement | True curiosity |

## GF(3) Triads

```
yoneda-directed (-1) ⊗ cognitive-superposition (0) ⊗ curiosity-driven (+1) = 0 ✓
persistent-homology (-1) ⊗ self-evolving-agent (0) ⊗ curiosity-driven (+1) = 0 ✓
three-match (-1) ⊗ unworld (0) ⊗ curiosity-driven (+1) = 0 ✓
```

## Integration with Interaction Entropy

```ruby
module CuriosityDriven
  def self.compute_curiosity(content, world_model_before, world_model_after)
    # Description length before and after
    len_before = description_length(content, world_model_before)
    len_after = description_length(content, world_model_after)
    
    progress = len_before - len_after
    
    {
      content: content,
      compression_progress: progress,
      curious: progress > 0,
      trit: 1  # Generator (creates new understanding)
    }
  end
end
```

## Key Insights

1. **Boredom**: Agent gets bored of predictable environments
2. **Interestingness**: Attracted to learnable patterns
3. **Creativity**: Generates interesting outputs as byproduct
4. **Developmental**: Like infant exploration behavior

## References

1. Schmidhuber, J. (1991). "A Possibility for Implementing Curiosity and Boredom in Model-Building Neural Controllers."
2. Schmidhuber, J. (2010). "Formal Theory of Creativity, Fun, and Intrinsic Motivation."
3. Oudeyer, P.-Y. & Kaplan, F. (2007). "What is Intrinsic Motivation? A Typology of Computational Approaches."



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `general`: 734 citations in bib.duckdb

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