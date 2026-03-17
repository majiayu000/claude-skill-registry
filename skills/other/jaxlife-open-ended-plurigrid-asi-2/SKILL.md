---
name: jaxlife-open-ended
description: JaxLife open-ended agentic simulator for emergent behavior, tool use,
  and cultural accumulation. Use for artificial life simulations, emergent agent behavior,
  and open-ended evolution research.
metadata:
  trit: 1
  color: '#D82626'
---

# JaxLife Open-Ended

**Trit**: +1 (PLUS - generator)
**Color**: Red (#D82626)

## Overview

Implements patterns from JaxLife and related open-ended ALife simulators:
- Embodied agents with neural network controllers
- Turing-complete programmable environments
- Emergent communication, agriculture, and tool use
- Open-ended cultural and technological accumulation

## Key Papers

- [JaxLife: An Open-Ended Agentic Simulator](https://hf.co/papers/2409.00853) - Lu et al. 2024
- [Biomaker CA](https://hf.co/papers/2307.09320) - Randazzo & Mordvintsev 2023
- [LifeGPT](https://hf.co/papers/2409.12182) - Berkovich & Buehler 2024
- [The Station](https://hf.co/papers/2511.06309) - Chung & Du 2025
- [Static Sandboxes Are Inadequate](https://hf.co/papers/2510.13982) - Chen et al. 2025

## Core Concepts

### JaxLife Environment

```
┌─────────────────────────────────────────────────────┐
│                   JAXLIFE WORLD                     │
├─────────────────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────┐             │
│  │ Agent 1 │  │ Agent 2 │  │ Agent N │  ...        │
│  │  (NN)   │  │  (NN)   │  │  (NN)   │             │
│  └────┬────┘  └────┬────┘  └────┬────┘             │
│       │            │            │                   │
│       ▼            ▼            ▼                   │
│  ┌─────────────────────────────────────────────┐   │
│  │              PROGRAMMABLE GRID               │   │
│  │   (Turing-complete, supports computation)    │   │
│  └─────────────────────────────────────────────┘   │
│       │                                             │
│       ▼                                             │
│  ┌─────────────────────────────────────────────┐   │
│  │         EMERGENT BEHAVIORS                   │   │
│  │  • Communication protocols                   │   │
│  │  • Agriculture / resource management         │   │
│  │  • Tool use and construction                 │   │
│  │  • Cultural inheritance                      │   │
│  └─────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

### Agent Architecture

```latex
\text{Agent state: } s_t = (position, energy, memory, genome)

\text{Observation: } o_t = \text{local\_view}(world, position, vision\_range)

\text{Action: } a_t = \pi_\theta(o_t, memory_t)

\text{Actions include: move, eat, reproduce, communicate, interact}
```

### Programmable World

The world supports Turing-complete computation:
- Cells can hold "programs" (like assembly instructions)
- Agents can read/write/execute cell contents
- Enables tool creation and cultural artifacts

## API

### JAX Implementation

```python
import jax
import jax.numpy as jnp
from flax import linen as nn
from typing import Tuple, Dict

@dataclass
class AgentState:
    position: jnp.ndarray  # (2,)
    energy: float
    memory: jnp.ndarray    # (memory_size,)
    genome: jnp.ndarray    # (genome_size,)
    age: int


class AgentBrain(nn.Module):
    """Neural network controller for JaxLife agent."""
    hidden_dim: int = 64
    memory_dim: int = 32
    num_actions: int = 8
    
    @nn.compact
    def __call__(self, observation: jnp.ndarray, memory: jnp.ndarray):
        # Combine observation and memory
        x = jnp.concatenate([observation.flatten(), memory])
        
        # Process through network
        x = nn.Dense(self.hidden_dim)(x)
        x = nn.relu(x)
        x = nn.Dense(self.hidden_dim)(x)
        x = nn.relu(x)
        
        # Output: action logits + new memory
        action_logits = nn.Dense(self.num_actions)(x)
        new_memory = nn.Dense(self.memory_dim)(x)
        new_memory = nn.tanh(new_memory)
        
        return action_logits, new_memory


class JaxLifeWorld:
    """JaxLife open-ended world simulation."""
    
    def __init__(
        self,
        world_size: Tuple[int, int] = (64, 64),
        num_agents: int = 100,
        cell_channels: int = 16
    ):
        self.world_size = world_size
        self.num_agents = num_agents
        self.cell_channels = cell_channels
    
    def init_world(self, key: jax.random.PRNGKey) -> Dict:
        """Initialize world state."""
        k1, k2, k3 = jax.random.split(key, 3)
        
        # World grid (programmable cells)
        grid = jax.random.uniform(
            k1, 
            (*self.world_size, self.cell_channels)
        )
        
        # Resources (food, etc.)
        resources = jax.random.uniform(k2, self.world_size)
        
        # Initialize agents
        agents = self.init_agents(k3)
        
        return {
            "grid": grid,
            "resources": resources,
            "agents": agents,
            "step": 0
        }
    
    def init_agents(self, key: jax.random.PRNGKey) -> Dict:
        """Initialize agent population."""
        keys = jax.random.split(key, self.num_agents)
        
        positions = jax.random.randint(
            keys[0], 
            (self.num_agents, 2),
            0, 
            self.world_size[0]
        )
        
        energies = jnp.ones(self.num_agents) * 100.0
        
        memories = jnp.zeros((self.num_agents, 32))
        
        genomes = jax.random.normal(keys[1], (self.num_agents, 256))
        
        return {
            "positions": positions,
            "energies": energies,
            "memories": memories,
            "genomes": genomes,
            "ages": jnp.zeros(self.num_agents, dtype=jnp.int32)
        }
    
    @jax.jit
    def step(self, state: Dict, agent_params: Dict) -> Dict:
        """Run one simulation step."""
        # Get observations for all agents
        observations = self.get_observations(state)
        
        # Compute actions using agent brains
        actions, new_memories = self.compute_actions(
            observations, 
            state["agents"]["memories"],
            agent_params
        )
        
        # Execute actions
        state = self.execute_actions(state, actions)
        
        # Update memories
        state["agents"]["memories"] = new_memories
        
        # Environment dynamics (resource regrowth, etc.)
        state = self.environment_step(state)
        
        # Reproduction and death
        state = self.life_cycle(state)
        
        state["step"] += 1
        return state
    
    def get_observations(self, state: Dict) -> jnp.ndarray:
        """Get local observations for all agents."""
        vision_range = 5
        obs = []
        
        for i in range(self.num_agents):
            pos = state["agents"]["positions"][i]
            local = self.get_local_view(state, pos, vision_range)
            obs.append(local)
        
        return jnp.stack(obs)
    
    def execute_actions(self, state: Dict, actions: jnp.ndarray) -> Dict:
        """Execute agent actions."""
        # Action types: 0=stay, 1-4=move, 5=eat, 6=reproduce, 7=communicate
        
        for i in range(self.num_agents):
            action = actions[i]
            
            if action in [1, 2, 3, 4]:
                # Move
                direction = [(0, 0), (0, 1), (0, -1), (1, 0), (-1, 0)][action]
                new_pos = state["agents"]["positions"][i] + jnp.array(direction)
                new_pos = jnp.clip(new_pos, 0, self.world_size[0] - 1)
                state["agents"]["positions"] = state["agents"]["positions"].at[i].set(new_pos)
                state["agents"]["energies"] = state["agents"]["energies"].at[i].add(-1)
            
            elif action == 5:
                # Eat
                pos = tuple(state["agents"]["positions"][i])
                food = state["resources"][pos]
                state["agents"]["energies"] = state["agents"]["energies"].at[i].add(food * 10)
                state["resources"] = state["resources"].at[pos].set(0)
            
            elif action == 6:
                # Reproduce (if enough energy)
                if state["agents"]["energies"][i] > 50:
                    state = self.reproduce(state, i)
            
            elif action == 7:
                # Communicate (modify nearby grid cells)
                pos = tuple(state["agents"]["positions"][i])
                signal = state["agents"]["memories"][i, :self.cell_channels]
                state["grid"] = state["grid"].at[pos].set(signal)
        
        return state
    
    def reproduce(self, state: Dict, parent_idx: int) -> Dict:
        """Agent reproduction with mutation."""
        # Find dead agent slot or create new
        dead_mask = state["agents"]["energies"] <= 0
        if not dead_mask.any():
            return state  # No room for new agent
        
        child_idx = jnp.argmax(dead_mask)
        
        # Inherit genome with mutation
        parent_genome = state["agents"]["genomes"][parent_idx]
        mutation = jax.random.normal(jax.random.PRNGKey(state["step"]), parent_genome.shape) * 0.1
        child_genome = parent_genome + mutation
        
        # Set child state
        state["agents"]["genomes"] = state["agents"]["genomes"].at[child_idx].set(child_genome)
        state["agents"]["positions"] = state["agents"]["positions"].at[child_idx].set(
            state["agents"]["positions"][parent_idx]
        )
        state["agents"]["energies"] = state["agents"]["energies"].at[child_idx].set(25)
        state["agents"]["energies"] = state["agents"]["energies"].at[parent_idx].add(-25)
        state["agents"]["ages"] = state["agents"]["ages"].at[child_idx].set(0)
        
        return state


def run_simulation(num_steps: int = 10000):
    """Run JaxLife simulation."""
    world = JaxLifeWorld(world_size=(64, 64), num_agents=100)
    
    key = jax.random.PRNGKey(42)
    k1, k2 = jax.random.split(key)
    
    # Initialize
    state = world.init_world(k1)
    
    # Initialize agent brain parameters
    brain = AgentBrain()
    params = brain.init(k2, jnp.zeros((11 * 11 * 16,)), jnp.zeros(32))
    
    # Run simulation
    for step in range(num_steps):
        state = world.step(state, params)
        
        if step % 1000 == 0:
            alive = (state["agents"]["energies"] > 0).sum()
            avg_age = state["agents"]["ages"][state["agents"]["energies"] > 0].mean()
            print(f"Step {step}: {alive} alive, avg age {avg_age:.1f}")
    
    return state
```

### Metrics for Open-Endedness

```python
def measure_open_endedness(history: List[Dict]) -> Dict:
    """Measure open-endedness metrics."""
    
    # Novelty: new behaviors over time
    novelty = compute_novelty(history)
    
    # Complexity: increasing agent complexity
    complexity = compute_complexity(history)
    
    # Learnability: can new things be learned
    learnability = compute_learnability(history)
    
    # Diversity: behavioral diversity
    diversity = compute_diversity(history)
    
    return {
        "novelty": novelty,
        "complexity": complexity,
        "learnability": learnability,
        "diversity": diversity,
        "open_endedness": novelty * learnability  # Product definition
    }
```

## GF(3) Triads

This skill participates in balanced triads:

```
persistent-homology (-1) ⊗ self-evolving-agent (0) ⊗ jaxlife-open-ended (+1) = 0 ✓
temporal-coalgebra (-1) ⊗ chemical-computing-substrate (0) ⊗ jaxlife-open-ended (+1) = 0 ✓
sheaf-cohomology (-1) ⊗ open-games (0) ⊗ jaxlife-open-ended (+1) = 0 ✓
```

## Emergent Behaviors

From JaxLife paper:
- **Communication Protocols**: Agents develop signals for coordination
- **Agriculture**: Resource management and cultivation
- **Tool Use**: Creating and using environmental artifacts
- **Cultural Inheritance**: Knowledge transfer across generations

## Integration with Music-Topos

```clojure
;; In agents/jaxlife_bridge.clj
(defn jaxlife-color-ecology
  "Simulate color agent ecology"
  [initial-population]
  (let [world (init-color-world 64 64)
        agents (mapv #(make-color-agent %) initial-population)]
    (loop [state {:world world :agents agents :step 0}]
      (if (< (:step state) 10000)
        (recur (step-color-ecology state))
        (extract-emergent-patterns state)))))

;; Agents evolve color preferences through interaction
;; Emergent: color niches, color signaling, color culture
```

## See Also

- `self-evolving-agent` - Self-improving agent patterns
- `forward-forward-learning` - Local learning for agent brains
- `chemical-computing-substrate` - Reaction networks for environment
- `biomaker-morphogenesis` - Morphogenetic CA patterns

## References

```bibtex
@article{lu2024jaxlife,
  title={JaxLife: An Open-Ended Agentic Simulator},
  author={Lu, Chris and others},
  journal={arXiv:2409.00853},
  year={2024}
}

@article{randazzo2023biomaker,
  title={Biomaker CA: a Biome Maker project using Cellular Automata},
  author={Randazzo, Ettore and Mordvintsev, Alexander},
  journal={arXiv:2307.09320},
  year={2023}
}

@article{chung2025station,
  title={The Station: An Open-World Environment for AI-Driven Discovery},
  author={Chung, Stephen and Du, Wenyu},
  journal={arXiv:2511.06309},
  year={2025}
}
```
