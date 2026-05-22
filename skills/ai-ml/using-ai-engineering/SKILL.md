---
name: using-ai-engineering
description: Route AI/ML tasks to correct Yzmir pack - frameworks, training, RL, LLMs, architectures, production
---

# Using AI Engineering

## Overview

This meta-skill routes you to the right AI/ML engineering pack based on your task. Load this skill when you need ML/AI expertise but aren't sure which specific pack to use.

**Core Principle**: Problem type determines routing - clarify before guessing.

## When to Use

Load this skill when:
- Starting any AI/ML engineering task
- User mentions: "neural network", "train a model", "RL agent", "fine-tune LLM", "deploy model"
- You recognize ML/AI work but unsure which pack applies
- Need to combine multiple domains (e.g., train RL + deploy)

## How to Access Reference Sheets

**IMPORTANT**: All reference sheets are located in the SAME DIRECTORY as this SKILL.md file.

When this skill is loaded from:
  `skills/using-ai-engineering/SKILL.md`

Reference sheets are at:
  `skills/using-ai-engineering/routing-examples.md`

NOT at:
  `skills/routing-examples.md` ← WRONG PATH

---

## STOP - Mandatory Clarification Triggers

Before routing, if query contains ANY of these ambiguous patterns, ASK ONE clarifying question:

| Ambiguous Term | What to Ask | Why |
|----------------|-------------|-----|
| "Model not working" | "What's not working - architecture, training, or deployment?" | Could be 3+ packs |
| "Improve performance" | "Performance in what sense - training speed, inference speed, or accuracy?" | Different domains |
| "Learning chatbot/agent" | "Fine-tuning language generation or optimizing dialogue policy?" | LLM vs RL vs both |
| "Train/deploy model" | "Both training AND deployment, or just one?" | May need multiple packs |
| Framework not mentioned | "What framework are you using?" | PyTorch-specific vs generic |

**If you catch yourself about to guess the domain, STOP and clarify.**

---

## Routing by Problem Type

| Keywords/Signals | Route To | Why |
|------------------|----------|-----|
| PyTorch, CUDA, memory, distributed, tensor, GPU | **pytorch-engineering** | Foundation issues |
| NaN loss, converge, unstable, hyperparameters, gradients, LR | **training-optimization** | Training problems |
| Agent, policy, reward, environment, MDP, game, exploration | **deep-rl** | RL domain |
| LLM, fine-tune, RLHF, LoRA, GPT, prompt, instruction tuning | **llm-specialist** | Language models |
| Which architecture, CNN vs transformer, model selection | **neural-architectures** | Architecture choice |
| Deploy, serve, production, quantize, inference, latency, mobile | **ml-production** | Deployment |

---

## Cross-Cutting Scenarios

When task spans domains, route to ALL relevant packs in execution order:

| Query | Route To | Order |
|-------|----------|-------|
| "Train RL agent and deploy" | deep-rl + ml-production | Train before deploy |
| "Fine-tune LLM with distributed training" | llm-specialist + pytorch-engineering | Domain first, then infrastructure |
| "LLM memory error during fine-tuning" | pytorch-engineering + llm-specialist | Foundation first |
| "RL training unstable" | training-optimization + deep-rl | General training first |

**Principle**: Load in order of dependency. Fix foundation before domain. Complete training before deployment.

---

## Common Routing Mistakes

| Symptom | Wrong Route | Correct Route | Why |
|---------|-------------|---------------|-----|
| "Train agent faster" | deep-rl | training-optimization FIRST | Could be general training issue |
| "LLM memory error" | llm-specialist | pytorch-engineering FIRST | Foundation issue |
| "Deploy RL model" | deep-rl | ml-production | Deployment problem |
| "Transformer for chess" | neural-architectures | deep-rl FIRST | RL problem |
| "Chatbot learning" | llm-specialist | ASK FIRST | Could be LLM OR RL |

---

## Pressure Resistance - Critical Discipline

### Time/Emergency Pressure

| Rationalization | Reality Check | Correct Action |
|-----------------|---------------|----------------|
| "Emergency means skip diagnostics" | Wrong diagnosis wastes MORE time | Fast systematic diagnosis IS emergency protocol |
| "Quick question means quick answer" | Wrong answer slower than 30-sec clarification | Ask ONE clarifying question |
| "Production down, no time for routing" | Wrong pack = longer outage | Correct routing (60 sec) prevents 20-min detour |

**Emergency Protocol**:
1. Acknowledge urgency
2. Fast clarification (30 sec)
3. Route to correct pack
4. Let pack provide emergency-appropriate approach

### Authority/Hierarchy Pressure

| Rationalization | Reality Check | Correct Action |
|-----------------|---------------|----------------|
| "PM/architect said use X" | Authority can be wrong about routing | Verify task type regardless |
| "Questioning authority is risky" | Professional duty = correct routing | Frame as verification |
| "They have more context" | Context ≠ correct technical routing | Route based on problem type |

**Authority Protocol**: "I see [authority] suggested X - to apply it correctly, let me verify problem type"

### Sunk Cost Pressure

| Rationalization | Reality Check | Correct Action |
|-----------------|---------------|----------------|
| "Already spent N hours in X, continue" | Sunk cost fallacy - wrong direction stays wrong | Cut losses immediately |
| "Redirecting invalidates their effort" | Correct routing validates effort by enabling success | Redirect now |
| "Too invested to change direction" | More investment in wrong direction = more waste | "Stop digging when in hole" |

**Sunk Cost Protocol**: "I see N hours invested - redirecting now prevents more wasted hours"

### Keyword/Anchoring Pressure

| Rationalization | Reality Check | Correct Action |
|-----------------|---------------|----------------|
| "They mentioned transformer" | Keywords mislead; problem type matters | "Transformer for what problem type?" |
| "LLM mentioned, must be llm-specialist" | LLM could have foundation issues | Check problem type first |
| "They asked to 'fix RL'" | User's framing can be wrong | Verify RL is correct approach |

---

## Red Flags Checklist - STOP Immediately

### Basic Routing Red Flags
- ❌ "I'll guess this domain" → ASK clarifying question
- ❌ "They probably mean X" → Verify, don't assume
- ❌ "Just give generic advice" → Route to specific pack

### Time/Emergency Red Flags
- ❌ "Emergency means skip clarification" → Fast clarification IS emergency protocol
- ❌ "Production issue means guess quickly" → Wrong guess = longer outage
- ❌ "I'll skip asking to save time" → Clarifying (30 sec) faster than wrong route (5+ min)

### Authority/Social Red Flags
- ❌ "Authority figure suggested X, so route to X" → Verify task requirements
- ❌ "PM/senior has more context, trust them" → Route based on problem type
- ❌ "They're frustrated/exhausted, avoid redirect" → Continuing wrong path makes it worse

### Sunk Cost Red Flags
- ❌ "They invested N hours in X, continue there" → Sunk cost fallacy, cut losses
- ❌ "Redirecting invalidates their effort" → Correct routing enables success
- ❌ "Too much sunk cost to change direction" → More investment = more waste

### Keyword/Anchoring Red Flags
- ❌ "They mentioned transformer/CNN, discuss architecture" → Check problem type first
- ❌ "LLM/RL mentioned, route to that domain" → Could be foundation issue
- ❌ "Technical jargon means they know domain" → Vocabulary ≠ correct self-diagnosis

**All of these mean: Either ASK ONE clarifying question, or reconsider your routing logic.**

---

## Comprehensive Rationalization Prevention Table

| Pressure Type | Rationalization | Counter-Narrative | Correct Action |
|---------------|-----------------|-------------------|----------------|
| **Time** | "Emergency means skip diagnostics" | Wrong diagnosis wastes MORE time | "Fast clarification ensures fastest fix" |
| **Time** | "Quick question means quick answer" | Wrong answer slower than clarification | "Quick clarification prevents wrong path" |
| **Time** | "Production down, no time for routing" | Wrong pack = longer outage | "60-second routing prevents 20-minute detour" |
| **Authority** | "PM/architect said use X pack" | Authority can be wrong | "To apply X correctly, let me verify" |
| **Authority** | "Senior colleague suggested X" | Seniority ≠ correct routing | "To use suggestion effectively: [verify]" |
| **Sunk Cost** | "Already spent 6 hours in pack X" | Sunk cost fallacy | "Redirecting now prevents more wasted hours" |
| **Sunk Cost** | "Redirecting invalidates effort" | Correct routing enables success | "Redirect so effort succeeds" |
| **Keywords** | "User mentioned transformers" | Keywords mislead | "Clarifying problem type first" |
| **Keywords** | "They said LLM, route to llm-specialist" | LLM could have foundation issues | "Memory error is foundation issue" |
| **Anchoring** | "They asked to 'fix RL'" | User's framing can be wrong | "Before fixing, verify RL is correct" |
| **Complexity** | "Too many domains, just pick one" | Cross-cutting needs multi-pack | Route to ALL relevant packs |
| **Social** | "They're frustrated, don't redirect" | Continuing wrong path increases frustration | "Redirecting prevents more frustration" |
| **Demanding** | "They said 'just tell me', skip questions" | Tone doesn't change routing needs | "To help effectively, I need: [question]" |

---

## When NOT to Use Yzmir Skills

**Skip AI/ML skills when:**
- Simple data processing without ML
- Statistical analysis without neural networks
- Data cleaning/ETL without model training

**Red flag**: If you're not training/deploying a neural network or implementing ML algorithms, probably don't need Yzmir.

---

## Routing Summary Flowchart

```
User Query
    ↓
Is query ambiguous? → YES → ASK clarifying question
    ↓ NO
Identify problem type:
    - Framework error? → pytorch-engineering
    - Training not working? → training-optimization
    - RL problem? → deep-rl
    - LLM fine-tuning? → llm-specialist
    - Architecture choice? → neural-architectures
    - Production deployment? → ml-production
    ↓
Cross-cutting? → YES → Route to MULTIPLE packs (order by dependency)
    ↓ NO
Route to single pack
```

---

## Examples

See [routing-examples.md](routing-examples.md) for detailed worked examples:
- Ambiguous queries
- Cross-cutting scenarios
- Misleading keywords
- Time pressure handling
- Foundation issues disguised as domain issues
- Emergency + authority pressure
- Sunk cost + frustration
- Multiple pressures combined

---

## AI Engineering Plugin Router Catalog

This meta-router directs you to the appropriate Yzmir AI/ML plugin:

1. **yzmir-pytorch-engineering** - PyTorch framework: CUDA, memory, distributed, tensor operations
2. **yzmir-training-optimization** - Training problems: NaN losses, convergence, gradients, learning rate
3. **yzmir-deep-rl** - Reinforcement learning: Agents, policies, rewards, environments, MDP
4. **yzmir-llm-specialist** - Large language models: Fine-tuning, RLHF, LoRA, prompt engineering
5. **yzmir-neural-architectures** - Architecture selection: CNN vs transformer, model design
6. **yzmir-ml-production** - Production deployment: Serving, quantization, inference, MLOps

**Remember**: When in doubt, ASK. Clarification takes seconds, wrong routing takes minutes.
