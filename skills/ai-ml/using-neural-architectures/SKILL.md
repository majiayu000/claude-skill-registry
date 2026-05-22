---
name: using-neural-architectures
description: The architecture selection router for CNNs, Transformers, RNNs, GANs, GNNs by data modality and constraints
---

# Using Neural Architectures: Architecture Selection Router

<CRITICAL_CONTEXT>
Architecture selection comes BEFORE training optimization. Wrong architecture = no amount of training will fix it.

This meta-skill routes you to the right architecture guidance based on:

- Data modality (images, sequences, graphs, etc.)
- Problem type (classification, generation, regression)
- Constraints (data size, compute, latency, interpretability)

Load this skill when architecture decisions are needed.
</CRITICAL_CONTEXT>

## When to Use This Skill

Use this skill when:

- ✅ Selecting an architecture for a new problem
- ✅ Comparing architecture families (CNN vs Transformer, RNN vs Transformer, etc.)
- ✅ Designing custom network topology
- ✅ Troubleshooting architectural instability (deep networks, gradient issues)
- ✅ Understanding when to use specialized architectures (GNNs, generative models)

DO NOT use for:

- ❌ Training/optimization issues (use training-optimization pack)
- ❌ PyTorch implementation details (use pytorch-engineering pack)
- ❌ Production deployment (use ml-production pack)

**When in doubt:** If choosing WHAT architecture → this skill. If training/deploying architecture → different pack.

---

## How to Access Reference Sheets

**IMPORTANT**: All reference sheets are located in the SAME DIRECTORY as this SKILL.md file.

When this skill is loaded from:
  `skills/using-neural-architectures/SKILL.md`

Reference sheets like `cnn-families-and-selection.md` are at:
  `skills/using-neural-architectures/cnn-families-and-selection.md`

NOT at:
  `skills/cnn-families-and-selection.md` ← WRONG PATH

When you see a link like `[cnn-families-and-selection.md](cnn-families-and-selection.md)`, read the file from the same directory as this SKILL.md.

---

## Core Routing Logic

### Step 1: Identify Data Modality

**Question to ask:** "What type of data are you working with?"

| Data Type | Route To | Why |
|-----------|----------|-----|
| Images (photos, medical scans, etc.) | [cnn-families-and-selection.md](cnn-families-and-selection.md) | CNNs excel at spatial hierarchies |
| Sequences (time series, text, audio) | [sequence-models-comparison.md](sequence-models-comparison.md) | Temporal dependencies need sequential models |
| Graphs (social networks, molecules) | [graph-neural-networks-basics.md](graph-neural-networks-basics.md) | Graph structure requires GNNs |
| Generation task (create images, text) | [generative-model-families.md](generative-model-families.md) | Generative models are specialized |
| Multiple modalities (text + images) | [architecture-design-principles.md](architecture-design-principles.md) | Need custom design |
| Unclear / Generic | [architecture-design-principles.md](architecture-design-principles.md) | Start with fundamentals |

### Step 2: Check for Special Requirements

**If any of these apply, address FIRST:**

| Requirement | Route To | Priority |
|-------------|----------|----------|
| Deep network (> 20 layers) unstable | [normalization-techniques.md](normalization-techniques.md) | CRITICAL - fix before continuing |
| Need attention mechanisms | [attention-mechanisms-catalog.md](attention-mechanisms-catalog.md) | Specialized component |
| Custom architecture design | [architecture-design-principles.md](architecture-design-principles.md) | Foundation before specifics |
| Transformer-specific question | [transformer-architecture-deepdive.md](transformer-architecture-deepdive.md) | Specialized architecture |

### Step 3: Consider Problem Characteristics

**Clarify BEFORE routing:**

Ask:

- "How large is your dataset?" (Small < 10k, Medium 10k-1M, Large > 1M)
- "What are your computational constraints?" (Edge device, cloud, GPU availability)
- "What are your latency requirements?" (Real-time, batch, offline)
- "Do you need interpretability?" (Clinical, research, production)

These answers determine architecture appropriateness.

---

## Routing by Data Modality

### Images → CNN Families

**Symptoms triggering this route:**

- "classify images"
- "object detection"
- "semantic segmentation"
- "medical imaging"
- "computer vision"

**Route to:** See [cnn-families-and-selection.md](cnn-families-and-selection.md) for CNN architecture selection and comparison.

**When to route here:**

- ANY vision task (CNNs are default for spatial data)
- Even if considering Transformers, check CNN families first (often better with less data)

**Clarifying questions:**

- "Dataset size?" (< 10k → Start with proven CNNs, > 100k → Consider ViT)
- "Deployment target?" (Edge → EfficientNet, Cloud → Anything)
- "Task type?" (Classification → ResNet/EfficientNet, Detection → YOLO/Faster-RCNN)

---

### Sequences → Sequence Models Comparison

**Symptoms triggering this route:**

- "time series"
- "forecasting"
- "natural language" (NLP)
- "sequential data"
- "temporal patterns"
- "RNN vs LSTM vs Transformer"

**Route to:** See [sequence-models-comparison.md](sequence-models-comparison.md) for sequential model selection (RNN, LSTM, Transformer, TCN).

**When to route here:**

- ANY sequential data
- When user asks "RNN vs LSTM" (skill will present modern alternatives)
- Time-dependent patterns

**Clarifying questions:**

- "Sequence length?" (< 100 → RNN/LSTM/TCN, 100-1000 → Transformer, > 1000 → Sparse Transformers)
- "Latency requirements?" (Real-time → TCN/LSTM, Offline → Transformer)
- "Data volume?" (Small → Simpler models, Large → Transformers)

**CRITICAL:** Challenge "RNN vs LSTM" premise if they ask. Modern alternatives (Transformers, TCN) often better.

---

### Graphs → Graph Neural Networks

**Symptoms triggering this route:**

- "social network"
- "molecular structure"
- "knowledge graph"
- "graph data"
- "node classification"
- "link prediction"
- "graph embeddings"

**Route to:** See [graph-neural-networks-basics.md](graph-neural-networks-basics.md) for GNN architectures and graph learning.

**When to route here:**

- Data has explicit graph structure (nodes + edges)
- Relational information is important
- Network topology matters

**Red flag:** If treating graph as tabular data (extracting features and ignoring edges) → WRONG. Route to GNN skill.

---

### Generation → Generative Model Families

**Symptoms triggering this route:**

- "generate images"
- "synthesize data"
- "GAN vs VAE vs Diffusion"
- "image-to-image translation"
- "style transfer"
- "generative modeling"

**Route to:** See [generative-model-families.md](generative-model-families.md) for GANs, VAEs, and Diffusion models.

**When to route here:**

- Goal is to CREATE data, not classify/predict
- Need to sample from distribution
- Data augmentation through generation

**Clarifying questions:**

- "Use case?" (Real-time game → GAN, Art/research → Diffusion, Fast training → VAE)
- "Quality vs speed?" (Quality → Diffusion, Speed → GAN)
- "Controllability?" (Fine control → StyleGAN/Conditional models)

**CRITICAL:** Different generative models have VERY different trade-offs. Must clarify requirements.

---

## Routing by Architecture Component

### Attention Mechanisms

**Symptoms triggering this route:**

- "when to use attention"
- "self-attention vs cross-attention"
- "attention in CNNs"
- "attention bottleneck"
- "multi-head attention"

**Route to:** See [attention-mechanisms-catalog.md](attention-mechanisms-catalog.md) for attention mechanism selection and design.

**When to route here:**

- Designing custom architecture that might benefit from attention
- Understanding where attention helps vs hinders
- Comparing attention variants

**NOT for:** General Transformer questions → [transformer-architecture-deepdive.md](transformer-architecture-deepdive.md) instead

---

### Transformer Deep Dive

**Symptoms triggering this route:**

- "how do transformers work"
- "Vision Transformer (ViT)"
- "BERT architecture"
- "positional encoding"
- "transformer blocks"
- "scaling transformers"

**Route to:** See [transformer-architecture-deepdive.md](transformer-architecture-deepdive.md) for Transformer internals and implementation.

**When to route here:**

- Implementing/customizing transformers
- Understanding transformer internals
- Debugging transformer-specific issues

**Cross-reference:**

- For sequence models generally → [sequence-models-comparison.md](sequence-models-comparison.md) (includes transformers in context)
- For LLMs specifically → `yzmir/llm-specialist/transformer-for-llms` (LLM-specific transformers)

---

### Normalization Techniques

**Symptoms triggering this route:**

- "gradient explosion"
- "training instability in deep network"
- "BatchNorm vs LayerNorm"
- "normalization layers"
- "50+ layer network won't train"

**Route to:** See [normalization-techniques.md](normalization-techniques.md) for deep network stability and normalization methods.

**When to route here:**

- Deep networks (> 20 layers) with training instability
- Choosing between normalization methods
- Architectural stability issues

**CRITICAL:** This is often the ROOT CAUSE of "training won't work" - fix architecture before blaming hyperparameters.

---

### Architecture Design Principles

**Symptoms triggering this route:**

- "how to design architecture"
- "architecture best practices"
- "when to use skip connections"
- "how deep should network be"
- "custom architecture for [novel task]"
- Unclear problem modality

**Route to:** See [architecture-design-principles.md](architecture-design-principles.md) for custom architecture design fundamentals.

**When to route here:**

- Designing custom architectures
- Novel problems without established architecture
- Understanding WHY architectures work
- User is unsure what modality/problem type they have

**This is the foundational skill** - route here if other specific skills don't match.

---

## Multi-Modal / Cross-Pack Routing

### When Problem Spans Multiple Modalities

**Example:** "Text + image classification" (multimodal)

**Route to BOTH:**

1. [sequence-models-comparison.md](sequence-models-comparison.md) (for text)
2. [cnn-families-and-selection.md](cnn-families-and-selection.md) (for images)
3. [architecture-design-principles.md](architecture-design-principles.md) (for fusion strategy)

**Order matters:** Understand individual modalities BEFORE fusion.

### When Architecture + Other Concerns

**Example:** "Select architecture AND optimize training"

**Route order:**

1. Architecture skill FIRST (this pack)
2. Training-optimization SECOND (after architecture chosen)

**Why:** Wrong architecture can't be fixed by better training.

**Example:** "Select architecture AND deploy efficiently"

**Route order:**

1. Architecture skill FIRST
2. ML-production SECOND (quantization, serving)

**Deployment constraints might influence architecture choice** - if so, note constraints during architecture selection.

---

## Common Routing Mistakes (DON'T DO THESE)

| Symptom | Wrong Route | Correct Route | Why |
|---------|-------------|---------------|-----|
| "My transformer won't train" | [transformer-architecture-deepdive.md](transformer-architecture-deepdive.md) | training-optimization | Training issue, not architecture understanding |
| "Deploy image classifier" | [cnn-families-and-selection.md](cnn-families-and-selection.md) | ml-production | Deployment, not selection |
| "ViT vs ResNet for medical imaging" | [transformer-architecture-deepdive.md](transformer-architecture-deepdive.md) | [cnn-families-and-selection.md](cnn-families-and-selection.md) | Comparative selection, not single architecture detail |
| "Implement BatchNorm in PyTorch" | [normalization-techniques.md](normalization-techniques.md) | pytorch-engineering | Implementation, not architecture concept |
| "GAN won't converge" | [generative-model-families.md](generative-model-families.md) | training-optimization | Training stability, not architecture selection |
| "Which optimizer for CNN" | [cnn-families-and-selection.md](cnn-families-and-selection.md) | training-optimization | Optimization, not architecture |

**Rule:** Architecture pack is for CHOOSING and DESIGNING architectures. Training/deployment/implementation are other packs.

---

## Red Flags: Stop and Clarify

If query contains these patterns, ASK clarifying questions before routing:

| Pattern | Why Clarify | What to Ask |
|---------|-------------|--------------|
| "Best architecture for X" | "Best" depends on constraints | "What are your data size, compute, and latency constraints?" |
| Generic problem description | Can't route without modality | "What type of data? (images, sequences, graphs, etc.)" |
| Latest trend mentioned (ViT, Diffusion) | Recency bias risk | "Have you considered alternatives? What are your specific requirements?" |
| "Should I use X or Y" | May be wrong question | "What's the underlying problem? There might be option Z." |
| Very deep network (> 50 layers) | Likely needs normalization first | "Are you using normalization layers? Skip connections?" |

**Never guess modality or constraints. Always clarify.**

---

## Recency Bias: Resistance Table

| Trendy Architecture | When NOT to Use | Better Alternative |
|---------------------|------------------|-------------------|
| **Vision Transformers (ViT)** | Small datasets (< 10k images) | CNNs (ResNet, EfficientNet) |
| **Vision Transformers (ViT)** | Edge deployment (latency/power) | EfficientNets, MobileNets |
| **Transformers (general)** | Very small datasets | RNNs, CNNs (less capacity, less overfit) |
| **Diffusion Models** | Real-time generation needed | GANs (1 forward pass vs 50-1000 steps) |
| **Diffusion Models** | Limited compute for training | VAEs (faster training) |
| **Graph Transformers** | Small graphs (< 100 nodes) | Standard GNNs (GCN, GAT) simpler and effective |
| **LLMs (GPT-style)** | < 1M tokens of training data | Simpler language models or fine-tuning |

**Counter-narrative:** "New architecture ≠ better for your use case. Match architecture to constraints."

---

## Decision Tree

```
Start here: What's your primary goal?

┌─ SELECT architecture for task
│  ├─ Data modality?
│  │  ├─ Images → [cnn-families-and-selection.md](cnn-families-and-selection.md)
│  │  ├─ Sequences → [sequence-models-comparison.md](sequence-models-comparison.md)
│  │  ├─ Graphs → [graph-neural-networks-basics.md](graph-neural-networks-basics.md)
│  │  ├─ Generation → [generative-model-families.md](generative-model-families.md)
│  │  └─ Unknown/Multiple → [architecture-design-principles.md](architecture-design-principles.md)
│  └─ Special requirements?
│     ├─ Deep network (>20 layers) unstable → [normalization-techniques.md](normalization-techniques.md) (CRITICAL)
│     ├─ Need attention mechanism → [attention-mechanisms-catalog.md](attention-mechanisms-catalog.md)
│     └─ None → Proceed with modality-based route
│
├─ UNDERSTAND specific architecture
│  ├─ Transformers → [transformer-architecture-deepdive.md](transformer-architecture-deepdive.md)
│  ├─ Attention → [attention-mechanisms-catalog.md](attention-mechanisms-catalog.md)
│  ├─ Normalization → [normalization-techniques.md](normalization-techniques.md)
│  └─ General principles → [architecture-design-principles.md](architecture-design-principles.md)
│
├─ DESIGN custom architecture
│  └─ [architecture-design-principles.md](architecture-design-principles.md) (start here always)
│
└─ COMPARE architectures
   ├─ CNNs (ResNet vs EfficientNet) → [cnn-families-and-selection.md](cnn-families-and-selection.md)
   ├─ Sequence models (RNN vs Transformer) → [sequence-models-comparison.md](sequence-models-comparison.md)
   ├─ Generative (GAN vs Diffusion) → [generative-model-families.md](generative-model-families.md)
   └─ General comparison → [architecture-design-principles.md](architecture-design-principles.md)
```

---

## Workflow

1. **Clarify** → Data modality, task type, dataset size, compute/latency constraints
2. **Route by modality** → Images/Sequences/Graphs/Generation → appropriate skill
3. **Check critical issues** → Deep network unstable? Fix normalization FIRST
4. **Apply architecture skill** → Follow routed skill, consider trade-offs
5. **Cross-pack** → training-optimization (training) or ml-production (deployment)

---

## Rationalization Table

| Rationalization | Reality | Counter |
|-----------------|---------|---------|
| "Transformers are SOTA, recommend them" | SOTA on benchmark ≠ best for user's constraints | "Ask about dataset size and compute first" |
| "User said RNN vs LSTM, answer that" | Question premise might be outdated | "Challenge: Have you considered Transformers or TCN?" |
| "Just recommend latest architecture" | Latest ≠ appropriate | "Match architecture to requirements, not trends" |
| "Architecture doesn't matter, training matters" | Wrong architecture can't be fixed by training | "Architecture is foundation - get it right first" |
| "They seem rushed, skip clarification" | Wrong route wastes more time than clarification | "30 seconds to clarify saves hours of wasted effort" |
| "Generic architecture advice is safe" | Generic = useless for specific domains | "Route to domain-specific skill for actionable guidance" |

---

## Integration with Other Packs

### After Architecture Selection

Once architecture is chosen, route to:

**Training the architecture:**
→ `yzmir/training-optimization/using-training-optimization`

- Optimizer selection
- Learning rate schedules
- Debugging training issues

**Implementing in PyTorch:**
→ `yzmir/pytorch-engineering/using-pytorch-engineering`

- Module design patterns
- Performance optimization
- Custom components

**Deploying to production:**
→ `yzmir/ml-production/using-ml-production`

- Model serving
- Quantization
- Inference optimization

**Dynamic/growing architectures:**
→ `yzmir/dynamic-architectures/using-dynamic-architectures`

- Networks that grow, prune, or adapt during training
- Continual learning and catastrophic forgetting prevention
- Module lifecycle management and progressive training

### Before Architecture Selection

If problem involves:

**Reinforcement learning:**
→ `yzmir/deep-rl/using-deep-rl` FIRST

- RL algorithms dictate architecture requirements
- Value networks vs policy networks have different needs

**Large language models:**
→ `yzmir/llm-specialist/using-llm-specialist` FIRST

- LLM architectures are specialized transformers
- Different considerations than general sequence models

**Architecture is downstream of algorithm choice in RL and LLMs.**

---

## Summary

**Use this meta-skill to:**

- ✅ Route architecture queries to appropriate specialized skill
- ✅ Identify data modality and problem type
- ✅ Clarify constraints before recommending
- ✅ Resist recency bias (latest ≠ best)
- ✅ Recognize when architecture is the problem (vs training/implementation)

## Neural Architecture Specialist Skills

After routing, load the appropriate specialist skill for detailed guidance:

1. [architecture-design-principles.md](architecture-design-principles.md) - Custom design, architectural best practices, skip connections, network depth fundamentals
2. [attention-mechanisms-catalog.md](attention-mechanisms-catalog.md) - Self-attention, cross-attention, multi-head attention, attention in CNNs, attention variants comparison
3. [cnn-families-and-selection.md](cnn-families-and-selection.md) - ResNet, EfficientNet, MobileNet, YOLO, computer vision architecture selection
4. [generative-model-families.md](generative-model-families.md) - GANs, VAEs, Diffusion models, image generation, style transfer, generative modeling trade-offs
5. [graph-neural-networks-basics.md](graph-neural-networks-basics.md) - GCN, GAT, node classification, link prediction, graph embeddings, molecular structures
6. [normalization-techniques.md](normalization-techniques.md) - BatchNorm, LayerNorm, GroupNorm, training stability for deep networks (>20 layers)
7. [sequence-models-comparison.md](sequence-models-comparison.md) - RNN, LSTM, Transformer, TCN comparison, time series, NLP, sequential data
8. [transformer-architecture-deepdive.md](transformer-architecture-deepdive.md) - Transformer internals, ViT, BERT, positional encoding, scaling transformers

**Critical principle:** Architecture comes BEFORE training. Get this right first.
