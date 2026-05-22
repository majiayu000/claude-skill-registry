---
name: using-deep-rl
description: Routes to appropriate deep-RL skills based on problem type and algorithm family
---

# Using Deep RL Meta-Skill

## When to Use This Skill

Invoke this meta-skill when you encounter:

- **RL Implementation**: Implementing reinforcement learning algorithms (Q-learning, DQN, PPO, SAC, etc.)
- **Agent Training**: Training agents in environments (games, robotics, control systems)
- **Sequential Decision-Making**: Problems requiring learning from trial and error
- **Policy Optimization**: Learning policies that maximize cumulative rewards
- **RL Debugging**: Debugging training issues, agents not learning, reward problems

This is the **entry point** for the deep-rl pack. It routes to 13 specialized skills based on problem characteristics.

## How to Access Reference Sheets

**IMPORTANT**: All reference sheets are located in the SAME DIRECTORY as this SKILL.md file.

When this skill is loaded from:
  `skills/using-deep-rl/SKILL.md`

Reference sheets like `rl-foundations.md` are at:
  `skills/using-deep-rl/rl-foundations.md`

NOT at:
  `skills/rl-foundations.md` ← WRONG PATH

---

## Core Principle

**Problem type determines algorithm family.**

The correct approach depends on:

1. **Action Space**: Discrete (button presses) vs Continuous (joint angles)
2. **Data Regime**: Online (interact with environment) vs Offline (fixed dataset)
3. **Experience Level**: Need foundations vs ready to implement
4. **Special Requirements**: Multi-agent, model-based, exploration, reward design

**Always clarify the problem BEFORE suggesting algorithms.**

---

## The 13 Deep RL Skills

1. **rl-foundations** - MDP formulation, Bellman equations, value vs policy basics
2. **value-based-methods** - Q-learning, DQN, Double DQN, Dueling DQN, Rainbow
3. **policy-gradient-methods** - REINFORCE, PPO, TRPO, policy optimization
4. **actor-critic-methods** - A2C, A3C, SAC, TD3, advantage functions
5. **model-based-rl** - World models, Dyna, MBPO, planning with learned models
6. **offline-rl** - Batch RL, CQL, IQL, learning from fixed datasets
7. **multi-agent-rl** - MARL, cooperative/competitive, communication
8. **exploration-strategies** - ε-greedy, UCB, curiosity, RND, intrinsic motivation
9. **reward-shaping** - Reward design, potential-based shaping, inverse RL
10. **counterfactual-reasoning** - Causal inference, HER, off-policy evaluation, twin networks
11. **rl-debugging** - Common RL bugs, why not learning, systematic debugging
12. **rl-environments** - Gym, MuJoCo, custom envs, wrappers, vectorization
13. **rl-evaluation** - Evaluation methodology, variance, sample efficiency metrics

---

## Routing Decision Framework

### Step 1: Assess Experience Level

- If user asks "what is RL" or "how does RL work" → **rl-foundations**
- If confused about value vs policy, on-policy vs off-policy → **rl-foundations**
- If user has specific problem and RL background → Continue to Step 2

**Why foundations first:** Cannot implement algorithms without understanding MDPs, Bellman equations, and exploration-exploitation tradeoffs.

### Step 2: Classify Action Space

#### Discrete Actions (buttons, menu selections, discrete signals)

| Condition | Route To | Why |
|-----------|----------|-----|
| Small action space (< 100) + online | **value-based-methods** (DQN) | Q-networks excel at discrete |
| Large action space OR need policy flexibility | **policy-gradient-methods** (PPO) | Scales to larger spaces |

#### Continuous Actions (joint angles, motor forces, steering)

| Condition | Route To | Why |
|-----------|----------|-----|
| Sample efficiency critical | **actor-critic-methods** (SAC) | Off-policy, automatic entropy |
| Stability critical | **actor-critic-methods** (TD3) | Deterministic, handles overestimation |
| Simplicity preferred | **policy-gradient-methods** (PPO) | On-policy, simpler |

**CRITICAL:** NEVER suggest DQN for continuous actions. DQN requires discrete actions.

### Step 3: Identify Data Regime

#### Online Learning (Agent Interacts with Environment)
- Discrete → **value-based-methods** OR **policy-gradient-methods**
- Continuous → **actor-critic-methods**
- Sample efficiency critical → Consider **model-based-rl**

#### Offline Learning (Fixed Dataset, No Interaction)
→ **offline-rl** (CQL, IQL)

**Red Flag:** If user has fixed dataset and suggests DQN/PPO/SAC, STOP and route to **offline-rl**. Standard algorithms assume online interaction and will fail.

### Step 4: Special Problem Types

| Problem | Route To | Key Consideration |
|---------|----------|-------------------|
| Multiple agents | **multi-agent-rl** | Non-stationarity, credit assignment |
| Sample efficiency extreme | **model-based-rl** | Learns environment model |
| Counterfactual/causal | **counterfactual-reasoning** | HER, off-policy evaluation |

### Step 5: Debugging and Infrastructure

| Problem | Route To | Why |
|---------|----------|-----|
| "Not learning" / reward flat | **rl-debugging** FIRST | 80% of issues are bugs, not algorithms |
| Exploration problems | **exploration-strategies** | Curiosity, RND, intrinsic motivation |
| Reward design issues | **reward-shaping** | Potential-based shaping, inverse RL |
| Environment setup | **rl-environments** | Gym API, wrappers, vectorization |
| Evaluation questions | **rl-evaluation** | Deterministic vs stochastic, multiple seeds |

**Red Flag:** If user immediately wants to change algorithms because "it's not learning," route to **rl-debugging** first.

---

## Rationalization Resistance Table

| Rationalization | Reality | Counter-Guidance |
|-----------------|---------|------------------|
| "Just use PPO for everything" | PPO is general but not optimal for all cases | Clarify: discrete or continuous? Sample efficiency constraints? |
| "DQN for continuous actions" | DQN requires discrete actions | Use SAC or TD3 for continuous |
| "Offline RL is just RL on a dataset" | Offline has distribution shift, needs special algorithms | Route to offline-rl for CQL, IQL |
| "More data always helps" | Sample efficiency and distribution matter | Off-policy vs on-policy matters |
| "My algorithm isn't learning, I need a better one" | Usually bugs, not algorithm | Route to rl-debugging first |
| "I'll discretize continuous actions for DQN" | Discretization loses precision, explodes action space | Use actor-critic-methods |
| "Epsilon-greedy is enough for exploration" | Complex environments need sophisticated exploration | Route to exploration-strategies |
| "I'll just increase the reward when it doesn't learn" | Reward scaling breaks learning | Route to rl-debugging |
| "I can reuse online RL code for offline data" | Offline needs conservative algorithms | Route to offline-rl |
| "Test reward lower than training = overfitting" | Exploration vs exploitation difference | Route to rl-evaluation |

---

## Red Flags Checklist

Watch for these signs of incorrect routing:

- [ ] **Algorithm-First Thinking**: Recommending algorithm before asking about action space, data regime
- [ ] **DQN for Continuous**: Suggesting DQN/Q-learning for continuous action spaces
- [ ] **Offline Blindness**: Not recognizing fixed dataset requires offline-rl
- [ ] **PPO Cargo-Culting**: Defaulting to PPO without considering alternatives
- [ ] **No Problem Characterization**: Not asking: discrete vs continuous? online vs offline?
- [ ] **Skipping Foundations**: Implementing algorithms when user doesn't understand RL basics
- [ ] **Debug-Last**: Suggesting algorithm changes before systematic debugging
- [ ] **Sample Efficiency Ignorance**: Not asking about sample constraints

**If any red flag triggered → STOP → Ask diagnostic questions → Route correctly**

---

## Routing Decision Tree Summary

```
START: RL problem

├─ Need foundations? → rl-foundations
│
├─ DISCRETE actions?
│  ├─ Small space + online → value-based-methods (DQN)
│  └─ Large space → policy-gradient-methods (PPO)
│
├─ CONTINUOUS actions?
│  ├─ Sample efficiency → actor-critic-methods (SAC)
│  ├─ Stability → actor-critic-methods (TD3)
│  └─ Simplicity → policy-gradient-methods (PPO)
│
├─ OFFLINE data? → offline-rl (CQL, IQL) [CRITICAL]
│
├─ MULTI-AGENT? → multi-agent-rl
│
├─ Sample efficiency EXTREME? → model-based-rl
│
├─ COUNTERFACTUAL? → counterfactual-reasoning
│
└─ DEBUGGING?
   ├─ Not learning → rl-debugging
   ├─ Exploration → exploration-strategies
   ├─ Reward design → reward-shaping
   ├─ Environment → rl-environments
   └─ Evaluation → rl-evaluation
```

---

## Diagnostic Questions

### Action Space
- "Discrete choices or continuous values?"
- "How many actions? Small (< 100), large, or infinite?"

### Data Regime
- "Can agent interact with environment, or fixed dataset?"
- "Online learning or offline?"

### Experience Level
- "New to RL, or specific problem?"
- "Understand MDPs, value functions, policy gradients?"

### Special Requirements
- "Multiple agents? Cooperate or compete?"
- "Sample efficiency critical? How many episodes?"
- "Sparse reward (only at goal) or dense (every step)?"

---

## When NOT to Use This Pack

| User Request | Correct Pack | Reason |
|--------------|--------------|--------|
| "Train classifier on labeled data" | training-optimization | Supervised learning |
| "Design transformer architecture" | neural-architectures | Architecture design |
| "Deploy model to production" | ml-production | Deployment |
| "Fine-tune LLM with RLHF" | llm-specialist | LLM-specific |

---

## Multi-Skill Scenarios

See [multi-skill-scenarios.md](multi-skill-scenarios.md) for detailed routing sequences:
- Complete beginner to RL
- Continuous control (robotics)
- Offline RL from dataset
- Multi-agent cooperative task
- Sample-efficient learning
- Sparse reward problem
- RL-controlled neural architecture

---

## Final Reminders

- **Problem characterization BEFORE algorithm selection**
- **DQN for discrete ONLY** (never continuous)
- **Offline data needs offline-rl** (CQL, IQL)
- **PPO is not universal** (good general-purpose, not optimal everywhere)
- **Debug before changing algorithms** (route to rl-debugging)
- **Ask questions, don't assume** (action space? data regime?)

---

## Deep RL Specialist Skills

After routing, load the appropriate specialist skill for detailed guidance:

1. [rl-foundations.md](rl-foundations.md) - MDP formulation, Bellman equations, value vs policy basics
2. [value-based-methods.md](value-based-methods.md) - Q-learning, DQN, Double DQN, Dueling DQN, Rainbow
3. [policy-gradient-methods.md](policy-gradient-methods.md) - REINFORCE, PPO, TRPO, policy optimization
4. [actor-critic-methods.md](actor-critic-methods.md) - A2C, A3C, SAC, TD3, advantage functions
5. [model-based-rl.md](model-based-rl.md) - World models, Dyna, MBPO, planning with learned models
6. [offline-rl.md](offline-rl.md) - Batch RL, CQL, IQL, learning from fixed datasets
7. [multi-agent-rl.md](multi-agent-rl.md) - MARL, cooperative/competitive, communication
8. [exploration-strategies.md](exploration-strategies.md) - ε-greedy, UCB, curiosity, RND, intrinsic motivation
9. [reward-shaping-engineering.md](reward-shaping-engineering.md) - Reward design, potential-based shaping, inverse RL
10. [counterfactual-reasoning.md](counterfactual-reasoning.md) - Causal inference, HER, off-policy evaluation, twin networks
11. [rl-debugging.md](rl-debugging.md) - Common RL bugs, why not learning, systematic debugging
12. [rl-environments.md](rl-environments.md) - Gym, MuJoCo, custom envs, wrappers, vectorization
13. [rl-evaluation.md](rl-evaluation.md) - Evaluation methodology, variance, sample efficiency metrics
14. [multi-skill-scenarios.md](multi-skill-scenarios.md) - Common problem routing sequences
