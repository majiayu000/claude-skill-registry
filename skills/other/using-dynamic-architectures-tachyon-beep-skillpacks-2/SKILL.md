---
name: using-dynamic-architectures
description: Use when building networks that grow, prune, or adapt topology during training. Routes to continual learning, gradient isolation, modular composition, and lifecycle orchestration skills.
---

# Dynamic Architectures Meta-Skill

## When to Use This Skill

Invoke this meta-skill when you encounter:

- **Growing Networks**: Adding capacity during training (new layers, neurons, modules)
- **Pruning Networks**: Removing capacity that isn't contributing
- **Continual Learning**: Training on new tasks without forgetting old ones
- **Gradient Isolation**: Training new modules without destabilizing existing weights
- **Modular Composition**: Building networks from graftable, composable components
- **Lifecycle Management**: State machines controlling when to grow, train, integrate, prune
- **Progressive Training**: Staged capability expansion with warmup and cooldown

This is the **entry point** for dynamic/morphogenetic neural network patterns. It routes to 7 specialized reference sheets.

## How to Access Reference Sheets

**IMPORTANT**: All reference sheets are located in the SAME DIRECTORY as this SKILL.md file.

When this skill is loaded from:
  `skills/using-dynamic-architectures/SKILL.md`

Reference sheets like `continual-learning-foundations.md` are at:
  `skills/using-dynamic-architectures/continual-learning-foundations.md`

NOT at:
  `skills/continual-learning-foundations.md` (WRONG PATH)

---

## Core Principle

**Dynamic architectures grow capability, not just tune weights.**

Static networks are a guess about capacity. Dynamic networks let training signal drive structure. The challenge is growing without forgetting, integrating without destabilizing, and knowing when to act.

Key tensions:
- **Stability vs. Plasticity**: Preserve existing knowledge while adding new capacity
- **Isolation vs. Integration**: Train new modules separately, then merge carefully
- **Exploration vs. Exploitation**: When to add capacity vs. when to stabilize

## The 7 Dynamic Architecture Skills

1. **continual-learning-foundations** - EWC, PackNet, rehearsal strategies, catastrophic forgetting theory
2. **gradient-isolation-techniques** - Freezing, gradient masking, stop_grad patterns, alpha blending
3. **peft-adapter-techniques** - LoRA, QLoRA, DoRA, adapter placement, merging strategies
4. **dynamic-architecture-patterns** - Grow/prune patterns, slot-based expansion, capacity scheduling
5. **modular-neural-composition** - MoE, gating, grafting semantics, interface contracts
6. **ml-lifecycle-orchestration** - State machines, quality gates, transition triggers, controllers
7. **progressive-training-strategies** - Staged expansion, warmup/cooldown, knowledge transfer

## Routing Decision Framework

### Step 1: Identify the Core Problem

**Diagnostic Questions:**

- "Are you trying to prevent forgetting when training on new data/tasks?"
- "Are you trying to add new capacity to an existing trained network?"
- "Are you designing how multiple modules combine?"
- "Are you deciding WHEN to grow, prune, or integrate?"

**Quick Routing:**

| Problem | Primary Skill |
|---------|---------------|
| "Model forgets old tasks when I train new ones" | continual-learning-foundations |
| "New module destabilizes existing weights" | gradient-isolation-techniques |
| "Fine-tune LLM efficiently without full training" | peft-adapter-techniques |
| "When should I add more capacity?" | dynamic-architecture-patterns |
| "How do module outputs combine?" | modular-neural-composition |
| "How do I manage the grow/train/integrate cycle?" | ml-lifecycle-orchestration |
| "How do I warm up new modules safely?" | progressive-training-strategies |

---

### Step 2: Catastrophic Forgetting (Continual Learning)

**Symptoms:**

- Performance on old tasks drops when training on new tasks
- Model "forgets" previous capabilities
- Fine-tuning overwrites learned features

**Route to:** [continual-learning-foundations.md](continual-learning-foundations.md)

**Covers:**
- Why SGD causes forgetting (loss landscape geometry)
- EWC, SI, MAS (regularization approaches)
- Progressive Neural Networks, PackNet (architectural approaches)
- Experience replay, generative replay (rehearsal approaches)
- Measuring forgetting (backward/forward transfer)

**When to Use:**
- Training sequentially on multiple tasks
- Fine-tuning without forgetting base capabilities
- Designing systems that accumulate knowledge over time

---

### Step 3: Gradient Isolation

**Symptoms:**

- New module training affects host network stability
- Want to train on host errors without backprop flowing to host
- Need gradual integration of new capacity

**Route to:** [gradient-isolation-techniques.md](gradient-isolation-techniques.md)

**Covers:**
- Freezing strategies (full, partial, scheduled)
- `detach()` vs `no_grad()` semantics
- Dual-path training (residual learning on errors)
- Alpha blending for gradual integration
- Hook-based gradient surgery

**When to Use:**
- Training "seed" modules that learn from host errors
- Preventing catastrophic interference during growth
- Implementing safe module grafting

---

### Step 4: PEFT Adapters (LoRA, QLoRA)

**Symptoms:**

- Want to fine-tune large pretrained models efficiently
- Memory constraints prevent full fine-tuning
- Need task-specific adaptation without modifying base weights

**Route to:** [peft-adapter-techniques.md](peft-adapter-techniques.md)

**Covers:**
- LoRA (low-rank adaptation) fundamentals
- QLoRA (quantized base + LoRA adapters)
- DoRA (weight-decomposed adaptation)
- Adapter placement strategies
- Merging adapters into base model
- Multiple adapter management

**When to Use:**
- Fine-tuning LLMs on limited compute
- Creating task-specific model variants
- Memory-efficient adaptation of large models

---

### Step 5: Dynamic Architecture Patterns

**Symptoms:**

- Need to add capacity during training (not just before)
- Want to prune underperforming components
- Deciding when/where to grow the network

**Route to:** [dynamic-architecture-patterns.md](dynamic-architecture-patterns.md)

**Covers:**
- Growth patterns (slot-based, layer widening, depth extension)
- Pruning patterns (magnitude, gradient-based, lottery ticket)
- Trigger conditions (loss plateau, contribution metrics, budgets)
- Capacity scheduling (grow-as-needed vs overparameterize-then-prune)

**When to Use:**
- Building networks that expand during training
- Implementing neural architecture search lite
- Managing parameter budgets with dynamic allocation

---

### Step 6: Modular Composition

**Symptoms:**

- Combining outputs from multiple modules
- Designing gating/routing mechanisms
- Need graftable, replaceable components

**Route to:** [modular-neural-composition.md](modular-neural-composition.md)

**Covers:**
- Combination mechanisms (additive, multiplicative, selective)
- Mixture of Experts (sparse gating, load balancing)
- Grafting semantics (input/output attachment points)
- Interface contracts (shape matching, normalization boundaries)
- Multi-module coordination (independent, competitive, cooperative)

**When to Use:**
- Building modular architectures with interchangeable parts
- Implementing MoE or gated architectures
- Designing residual streams as module communication

---

### Step 7: Lifecycle Orchestration

**Symptoms:**

- Need to decide WHEN to grow, train, integrate, prune
- Building state machines for module lifecycle
- Want quality gates before integration decisions

**Route to:** [ml-lifecycle-orchestration.md](ml-lifecycle-orchestration.md)

**Covers:**
- State machine fundamentals (states, transitions, terminals)
- Gate design patterns (structural, performance, stability, contribution)
- Transition triggers (metric-based, time-based, budget-based)
- Rollback and recovery (cooldown, hysteresis)
- Controller patterns (heuristic, learned/RL, hybrid)

**When to Use:**
- Designing grow/train/integrate/prune workflows
- Implementing quality gates for safe integration
- Building RL-controlled architecture decisions

---

### Step 8: Progressive Training

**Symptoms:**

- New modules cause instability when integrated
- Need warmup/cooldown for safe capacity addition
- Planning multi-stage training schedules

**Route to:** [progressive-training-strategies.md](progressive-training-strategies.md)

**Covers:**
- Staged capacity expansion strategies
- Warmup patterns (zero-init, LR warmup, alpha ramp)
- Cooldown and stabilization (settling periods, consolidation)
- Multi-stage schedules (sequential, overlapping, budget-aware)
- Knowledge transfer between stages (inheritance, distillation)

**When to Use:**
- Ramping new modules safely into production
- Designing curriculum over architecture (not just data)
- Preventing stage transition shock

---

## Common Multi-Skill Scenarios

### Scenario: Building a Morphogenetic System

**Need:** Network that grows seeds, trains them in isolation, and grafts successful ones

**Routing sequence:**
1. **dynamic-architecture-patterns** - Slot-based expansion, where seeds attach
2. **gradient-isolation-techniques** - Train seeds on host errors without destabilizing host
3. **modular-neural-composition** - How seed outputs blend into host stream
4. **ml-lifecycle-orchestration** - State machine for seed lifecycle
5. **progressive-training-strategies** - Warmup/cooldown for grafting

### Scenario: Continual Learning Without Forgetting

**Need:** Train on sequence of tasks without catastrophic forgetting

**Routing sequence:**
1. **continual-learning-foundations** - Understand forgetting, choose approach
2. **gradient-isolation-techniques** - If using architectural approach (columns, modules)
3. **progressive-training-strategies** - Staged training across tasks

### Scenario: Neural Architecture Search (Lite)

**Need:** Grow/prune network based on training signal

**Routing sequence:**
1. **dynamic-architecture-patterns** - Growth/pruning triggers and patterns
2. **ml-lifecycle-orchestration** - Automation via heuristics or RL
3. **progressive-training-strategies** - Stabilization between changes

### Scenario: RL-Controlled Architecture

**Need:** RL agent deciding when to grow, prune, integrate

**Routing sequence:**
1. **ml-lifecycle-orchestration** - Learned controller patterns
2. **dynamic-architecture-patterns** - What actions the RL agent can take
3. **gradient-isolation-techniques** - Safe exploration during training

---

## Rationalization Resistance Table

| Rationalization | Reality | Counter-Guidance |
|-----------------|---------|------------------|
| "Just train a bigger model from scratch" | Transfer + growth often beats from-scratch | "Check continual-learning-foundations for why" |
| "I'll freeze everything except the new layer" | Full freeze may be too restrictive | "Check gradient-isolation-techniques for partial strategies" |
| "I'll add capacity whenever loss plateaus" | Need more than loss plateau (contribution check) | "Check ml-lifecycle-orchestration for proper gates" |
| "Modules can just sum their outputs" | Naive summation can cause interference | "Check modular-neural-composition for combination mechanisms" |
| "I'll integrate immediately when training finishes" | Need warmup/holding period | "Check progressive-training-strategies for safe integration" |
| "EWC solves all forgetting problems" | EWC has limitations, may need architectural approach | "Check continual-learning-foundations for trade-offs" |

---

## Red Flags Checklist

Watch for these signs of incorrect approach:

- [ ] **No Isolation**: Training new modules without gradient isolation from host
- [ ] **No Warmup**: Integrating new capacity at full amplitude immediately
- [ ] **No Gates**: Integrating based only on time, not performance metrics
- [ ] **Naive Combination**: Summing module outputs without gating or blending
- [ ] **Ignoring Forgetting**: Adding new tasks without measuring old task performance
- [ ] **No Rollback**: No plan for what happens if integration fails

---

## Relationship to Other Packs

| Request | Primary Pack | Why |
|---------|--------------|-----|
| "Implement PPO for architecture decisions" | yzmir-deep-rl | RL algorithm implementation |
| "Evaluate architecture changes without mutation" | yzmir-deep-rl/counterfactual-reasoning | Counterfactual simulation |
| "Debug PyTorch gradient flow" | yzmir-pytorch-engineering | Low-level PyTorch debugging |
| "Optimize training loop performance" | yzmir-training-optimization | General training optimization |
| "Design transformer architecture" | yzmir-neural-architectures | Static architecture design |
| "Deploy morphogenetic model" | yzmir-ml-production | Production deployment |

**Intersection with deep-rl:** If using RL to control architecture decisions (when to grow/prune), combine this pack's lifecycle orchestration with deep-rl's policy gradient or actor-critic methods.

**Counterfactual evaluation:** Before committing to a live mutation (grow/prune), use deep-rl's `counterfactual-reasoning.md` to simulate the change and evaluate outcomes without risk. This is critical for production morphogenetic systems.

---

## Diagnostic Question Templates

Use these to route users:

### Problem Classification

- "Are you training on multiple tasks sequentially, or growing a single-task network?"
- "Do you have an existing trained model you want to extend, or starting fresh?"
- "Is the issue forgetting (old performance drops) or instability (training explodes)?"

### Architectural Questions

- "Where do new modules attach to the existing network?"
- "How should new module outputs combine with existing outputs?"
- "What triggers growth? Loss plateau, manual, or learned?"

### Lifecycle Questions

- "What states can a module be in? (training, integrating, permanent, removed)"
- "What conditions must be met before integration?"
- "What happens if a module fails to improve performance?"

---

## Summary: Routing Decision Tree

```
START: Dynamic architecture problem

├─ Forgetting old tasks?
│  └─ → continual-learning-foundations

├─ New module destabilizes existing?
│  └─ → gradient-isolation-techniques

├─ Fine-tuning LLM efficiently?
│  └─ → peft-adapter-techniques

├─ When/where to add capacity?
│  └─ → dynamic-architecture-patterns

├─ How modules combine?
│  └─ → modular-neural-composition

├─ Managing grow/train/integrate cycle?
│  └─ → ml-lifecycle-orchestration

├─ Warmup/cooldown for new capacity?
│  └─ → progressive-training-strategies

└─ Building complete morphogenetic system?
   └─ → Start with dynamic-architecture-patterns
      → Then gradient-isolation-techniques
      → Then ml-lifecycle-orchestration
```

---

## Reference Sheets

After routing, load the appropriate reference sheet:

1. [continual-learning-foundations.md](continual-learning-foundations.md) - EWC, PackNet, rehearsal, forgetting theory
2. [gradient-isolation-techniques.md](gradient-isolation-techniques.md) - Freezing, detach, alpha blending, hook surgery
3. [peft-adapter-techniques.md](peft-adapter-techniques.md) - LoRA, QLoRA, DoRA, adapter merging
4. [dynamic-architecture-patterns.md](dynamic-architecture-patterns.md) - Grow/prune patterns, triggers, scheduling
5. [modular-neural-composition.md](modular-neural-composition.md) - MoE, gating, grafting, interface contracts
6. [ml-lifecycle-orchestration.md](ml-lifecycle-orchestration.md) - State machines, gates, controllers
7. [progressive-training-strategies.md](progressive-training-strategies.md) - Staged expansion, warmup/cooldown
