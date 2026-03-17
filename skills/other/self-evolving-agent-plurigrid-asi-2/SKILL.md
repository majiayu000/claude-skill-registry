---
name: self-evolving-agent
description: Darwin Gödel Machine patterns for self-improving AI agents with open-ended
  code evolution. Use for building agents that autonomously improve their own capabilities,
  modify their codebases, and evolve through interaction.
metadata:
  trit: 0
  color: '#26D826'
---

# Self-Evolving Agent

**Trit**: 0 (ERGODIC - coordinator)
**Color**: Green (#26D826)

## Overview

Implements self-evolving agent patterns from recent research:
- Darwin Gödel Machine (DGM) for self-improving code
- Open-ended evolution of agent capabilities
- Lifelong learning with long-term memory
- Feedback loops for continual adaptation

## Key Papers

- [Darwin Gödel Machine](https://hf.co/papers/2505.22954) - Zhang et al. 2025
- [Self-Evolving Agents Survey](https://hf.co/papers/2507.21046) - Gao et al. 2025
- [Long Term Memory for AI Self-Evolution](https://hf.co/papers/2410.15665) - Jiang et al. 2024
- [Open-Endedness is Essential for ASI](https://hf.co/papers/2406.04268) - Hughes et al. 2024
- [Static Sandboxes Are Inadequate](https://hf.co/papers/2510.13982) - Chen et al. 2025

## Core Concepts

### Darwin Gödel Machine Architecture

```
┌─────────────────────────────────────────────────────┐
│                 DARWIN GÖDEL MACHINE                │
├─────────────────────────────────────────────────────┤
│  ┌─────────────┐    ┌─────────────┐                │
│  │   Archive   │───▶│   Sampler   │                │
│  │  (agents)   │    │  (select)   │                │
│  └─────────────┘    └──────┬──────┘                │
│         ▲                   │                       │
│         │            ┌──────▼──────┐                │
│         │            │  Mutator    │                │
│         │            │  (LLM-based)│                │
│         │            └──────┬──────┘                │
│         │                   │                       │
│  ┌──────┴──────┐     ┌──────▼──────┐               │
│  │  Validator  │◀────│  Evaluator  │               │
│  │  (benchmark)│     │  (fitness)  │               │
│  └─────────────┘     └─────────────┘               │
└─────────────────────────────────────────────────────┘
```

### Evolution Loop

```latex
\text{For each generation } t:
  1. \text{Sample agent } A_t \text{ from archive}
  2. \text{Mutate: } A'_t = \text{LLM}(A_t, \text{context})
  3. \text{Evaluate: } f(A'_t) = \text{benchmark}(A'_t)
  4. \text{If } f(A'_t) > \theta: \text{add to archive}
  5. \text{Prune archive to maintain diversity}
```

### Three Dimensions of Self-Evolution

1. **What to Evolve**: Model, memory, tools, architecture
2. **When to Evolve**: Intra-test-time, inter-test-time, offline
3. **How to Evolve**: Scalar rewards, textual feedback, multi-agent

## API

### Python Implementation

```python
from dataclasses import dataclass
from typing import List, Dict, Any, Callable
import random

@dataclass
class Agent:
    """Self-evolving agent representation."""
    code: str
    fitness: float
    generation: int
    parent_id: str = None
    metadata: Dict[str, Any] = None
    
    def __hash__(self):
        return hash(self.code)


class DarwinGodelMachine:
    """Darwin Gödel Machine for self-improving agents."""
    
    def __init__(
        self,
        initial_agent: Agent,
        mutator: Callable[[Agent], Agent],
        evaluator: Callable[[Agent], float],
        archive_size: int = 100,
        diversity_threshold: float = 0.3
    ):
        self.archive = [initial_agent]
        self.mutator = mutator
        self.evaluator = evaluator
        self.archive_size = archive_size
        self.diversity_threshold = diversity_threshold
        self.generation = 0
    
    def sample_agent(self) -> Agent:
        """Sample agent from archive (fitness-proportionate)."""
        fitnesses = [max(a.fitness, 0.01) for a in self.archive]
        total = sum(fitnesses)
        probs = [f / total for f in fitnesses]
        return random.choices(self.archive, weights=probs, k=1)[0]
    
    def mutate(self, agent: Agent) -> Agent:
        """Mutate agent using LLM-based code modification."""
        new_code = self.mutator(agent)
        return Agent(
            code=new_code,
            fitness=0.0,
            generation=self.generation,
            parent_id=hash(agent.code)
        )
    
    def evaluate(self, agent: Agent) -> float:
        """Evaluate agent on benchmarks."""
        try:
            fitness = self.evaluator(agent)
            agent.fitness = fitness
            return fitness
        except Exception as e:
            agent.fitness = 0.0
            agent.metadata = {"error": str(e)}
            return 0.0
    
    def is_novel(self, agent: Agent) -> bool:
        """Check if agent is sufficiently novel for archive."""
        for existing in self.archive:
            similarity = self.code_similarity(agent.code, existing.code)
            if similarity > (1 - self.diversity_threshold):
                return False
        return True
    
    def evolve_step(self) -> Agent:
        """Run one evolution step."""
        self.generation += 1
        
        # Sample and mutate
        parent = self.sample_agent()
        child = self.mutate(parent)
        
        # Evaluate
        fitness = self.evaluate(child)
        
        # Add to archive if good and novel
        if fitness > 0 and self.is_novel(child):
            self.archive.append(child)
            
            # Prune if too large
            if len(self.archive) > self.archive_size:
                self.archive.sort(key=lambda a: a.fitness, reverse=True)
                self.archive = self.archive[:self.archive_size]
        
        return child
    
    def evolve(self, generations: int) -> Agent:
        """Run evolution for multiple generations."""
        for _ in range(generations):
            self.evolve_step()
        
        # Return best agent
        return max(self.archive, key=lambda a: a.fitness)
    
    @staticmethod
    def code_similarity(code1: str, code2: str) -> float:
        """Compute code similarity (simple Jaccard)."""
        tokens1 = set(code1.split())
        tokens2 = set(code2.split())
        intersection = len(tokens1 & tokens2)
        union = len(tokens1 | tokens2)
        return intersection / union if union > 0 else 0.0


class LLMMutator:
    """LLM-based code mutator for agent evolution."""
    
    def __init__(self, model, mutation_prompts: List[str]):
        self.model = model
        self.prompts = mutation_prompts
    
    def __call__(self, agent: Agent) -> str:
        """Generate mutated code using LLM."""
        prompt = random.choice(self.prompts)
        
        system = """You are an AI agent code mutator. 
        Your task is to improve the given agent code while maintaining correctness.
        Return ONLY the improved code, no explanations."""
        
        user = f"""{prompt}

Current agent code:
```python
{agent.code}
```

Current fitness: {agent.fitness}
Generation: {agent.generation}

Generate improved code:"""
        
        response = self.model.generate(system=system, user=user)
        return self.extract_code(response)
    
    @staticmethod
    def extract_code(response: str) -> str:
        """Extract code from LLM response."""
        if "```python" in response:
            start = response.index("```python") + 9
            end = response.index("```", start)
            return response[start:end].strip()
        return response.strip()


class LongTermMemory:
    """Long-term memory for self-evolution (OMNE framework)."""
    
    def __init__(self, embedding_model, max_entries: int = 10000):
        self.entries = []
        self.embeddings = []
        self.embedding_model = embedding_model
        self.max_entries = max_entries
    
    def store(self, experience: Dict[str, Any]):
        """Store experience in long-term memory."""
        text = self.experience_to_text(experience)
        embedding = self.embedding_model.encode(text)
        
        self.entries.append(experience)
        self.embeddings.append(embedding)
        
        # Prune old entries if needed
        if len(self.entries) > self.max_entries:
            self.entries = self.entries[-self.max_entries:]
            self.embeddings = self.embeddings[-self.max_entries:]
    
    def retrieve(self, query: str, k: int = 5) -> List[Dict]:
        """Retrieve relevant experiences."""
        query_emb = self.embedding_model.encode(query)
        
        # Compute similarities
        similarities = [
            self.cosine_similarity(query_emb, emb)
            for emb in self.embeddings
        ]
        
        # Get top-k
        indices = sorted(range(len(similarities)), 
                        key=lambda i: similarities[i], reverse=True)[:k]
        return [self.entries[i] for i in indices]
    
    def consolidate(self):
        """Consolidate memories (compress similar experiences)."""
        # Group similar experiences
        # Extract patterns
        # Update with generalized knowledge
        pass
```

### Multi-Agent Self-Evolution

```python
class MultiAgentEvolution:
    """Co-evolution of multiple agent populations."""
    
    def __init__(self, populations: Dict[str, DarwinGodelMachine]):
        self.populations = populations
        self.interaction_history = []
    
    def co_evolve_step(self):
        """Evolve all populations with interaction."""
        for name, dgm in self.populations.items():
            # Evolve independently
            child = dgm.evolve_step()
            
            # Cross-pollinate: share best agents
            for other_name, other_dgm in self.populations.items():
                if other_name != name:
                    best_other = max(other_dgm.archive, key=lambda a: a.fitness)
                    # Learn from other population
                    self.share_knowledge(dgm, best_other)
    
    def share_knowledge(self, recipient: DarwinGodelMachine, donor: Agent):
        """Transfer knowledge between populations."""
        # Extract useful patterns from donor
        # Inject into recipient's mutation prompts
        pass
```

## GF(3) Triads

This skill participates in balanced triads:

```
persistent-homology (-1) ⊗ self-evolving-agent (0) ⊗ jaxlife-open-ended (+1) = 0 ✓
sheaf-cohomology (-1) ⊗ self-evolving-agent (0) ⊗ forward-forward-learning (+1) = 0 ✓
temporal-coalgebra (-1) ⊗ self-evolving-agent (0) ⊗ gay-mcp (+1) = 0 ✓
```

## Use Cases

### Self-Improving Coding Agent

```python
# Initialize with basic coding agent
initial = Agent(code=BASIC_CODER_CODE, fitness=0.2, generation=0)

# LLM mutator with improvement prompts
mutator = LLMMutator(model, prompts=[
    "Add better error handling",
    "Improve code efficiency",
    "Add missing edge cases",
    "Refactor for clarity"
])

# Benchmark evaluator
evaluator = lambda a: run_swebench(a.code)

# Create DGM
dgm = DarwinGodelMachine(initial, mutator, evaluator)

# Evolve!
best = dgm.evolve(generations=100)
print(f"Best fitness: {best.fitness}")  # 0.2 -> 0.5
```

### Continual Learning Agent

```python
# Agent with long-term memory
class ContinualAgent:
    def __init__(self):
        self.dgm = DarwinGodelMachine(...)
        self.ltm = LongTermMemory(embedding_model)
    
    def interact(self, task):
        # Retrieve relevant past experiences
        experiences = self.ltm.retrieve(task)
        
        # Evolve with context
        agent = self.dgm.sample_agent()
        agent.metadata["context"] = experiences
        
        # Execute and store
        result = self.execute(agent, task)
        self.ltm.store({"task": task, "result": result})
        
        return result
```

## Integration with Music-Topos

```clojure
;; In agents/self_evolving.clj
(defn dgm-evolve-color-agent
  "Evolve color generation agents via DGM"
  [initial-seed benchmark-fn]
  (let [archive (atom [(make-color-agent initial-seed)])
        mutate-fn (fn [agent] 
                    (update agent :seed #(splitmix64-next %)))
        evaluate-fn (fn [agent]
                      (benchmark-fn (generate-colors agent)))]
    (loop [gen 0]
      (when (< gen 100)
        (let [parent (sample-archive @archive)
              child (mutate-fn parent)
              fitness (evaluate-fn child)]
          (when (> fitness 0.5)
            (swap! archive conj child))
          (recur (inc gen)))))
    (best-agent @archive)))
```

## Safety Considerations

From Darwin Gödel Machine paper:

1. **Sandboxing**: Execute evolved code in isolated environments
2. **Human Oversight**: Review significant capability gains
3. **Capability Bounds**: Limit what evolved agents can access
4. **Rollback**: Maintain ability to revert to previous versions
5. **Alignment Verification**: Test evolved agents for alignment

```python
class SafeDGM(DarwinGodelMachine):
    def evaluate(self, agent: Agent) -> float:
        # Run in sandbox
        with Sandbox() as sb:
            result = sb.execute(agent.code, timeout=60)
        
        # Check for safety violations
        if self.safety_check(result):
            return result.fitness
        else:
            return -1.0  # Reject unsafe agents
```

## See Also

- `jaxlife-open-ended` - Open-ended embodied evolution
- `forward-forward-learning` - Local learning for agent updates
- `bisimulation-game` - Agent coordination and skill dispersal
- `parallel-fanout` - Parallel agent dispatch

## References

```bibtex
@article{zhang2025darwin,
  title={Darwin Gödel Machine: Open-Ended Evolution of Self-Improving Agents},
  author={Zhang, Jenny and others},
  journal={arXiv:2505.22954},
  year={2025}
}

@article{gao2025survey,
  title={A Survey of Self-Evolving Agents},
  author={Gao, Huan-ang and others},
  journal={arXiv:2507.21046},
  year={2025}
}

@article{hughes2024openended,
  title={Open-Endedness is Essential for Artificial Superhuman Intelligence},
  author={Hughes, Edward and others},
  journal={arXiv:2406.04268},
  year={2024}
}
```
