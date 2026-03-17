---
name: rlhf
description: Understanding Reinforcement Learning from Human Feedback (RLHF) for aligning language models. Use when learning about preference data, reward modeling, policy optimization, or direct alignment algorithms like DPO.
---

# Understanding RLHF

Reinforcement Learning from Human Feedback (RLHF) is a technique for aligning language models with human preferences. Rather than relying solely on next-token prediction, RLHF uses human judgment to guide model behavior toward helpful, harmless, and honest outputs.

## Table of Contents

- [Core Concepts](#core-concepts)
- [The RLHF Pipeline](#the-rlhf-pipeline)
- [Preference Data](#preference-data)
- [Instruction Tuning](#instruction-tuning)
- [Reward Modeling](#reward-modeling)
- [Policy Optimization](#policy-optimization)
- [Direct Alignment Algorithms](#direct-alignment-algorithms)
- [Challenges](#challenges)
- [Best Practices](#best-practices)
- [References](#references)

## Core Concepts

### Why RLHF?

Pretraining produces models that predict likely text, not necessarily *good* text. A model trained on internet data learns to complete text in ways that reflect its training distribution—including toxic, unhelpful, or dishonest patterns. RLHF addresses this gap by optimizing for human preferences rather than likelihood.

The core insight: humans can often recognize good outputs more easily than they can specify what makes an output good. RLHF exploits this by collecting human judgments and using them to shape model behavior.

### The Alignment Problem

Language models face several alignment challenges:

- **Helpfulness**: Following instructions and providing useful information
- **Harmlessness**: Avoiding toxic, dangerous, or inappropriate outputs
- **Honesty**: Acknowledging uncertainty and avoiding fabrication
- **Intent alignment**: Understanding what users actually want, not just what they say

RLHF provides a framework for encoding these properties through preference data.

### Key Components

1. **Preference data**: Human judgments comparing model outputs
2. **Reward model**: A learned function approximating human preferences
3. **Policy optimization**: RL algorithms that maximize expected reward
4. **Regularization**: Constraints preventing deviation from the base model

## The RLHF Pipeline

The standard RLHF pipeline consists of three main stages:

### Stage 1: Supervised Fine-Tuning (SFT)

Start with a pretrained language model and fine-tune it on high-quality demonstrations. This teaches the model the desired format and style of responses.

**Input**: Pretrained model + demonstration dataset
**Output**: SFT model that can follow instructions

### Stage 2: Reward Model Training

Train a model to predict human preferences between pairs of outputs. The reward model learns to score outputs in a way that correlates with human judgment.

**Input**: SFT model + preference dataset (chosen/rejected pairs)
**Output**: Reward model that scores any output

### Stage 3: Policy Optimization

Use reinforcement learning to optimize the SFT model against the reward model, while staying close to the original SFT distribution.

**Input**: SFT model + reward model
**Output**: Final aligned model

### Alternative: Direct Alignment

Direct alignment algorithms (DPO, IPO, KTO) skip the reward model entirely, optimizing directly from preference data. This simplifies the pipeline but trades off some flexibility.

## Preference Data

Preference data encodes human judgment about model outputs. The most common format is pairwise comparisons.

### Pairwise Preferences

Given a prompt, collect two or more model outputs and have humans indicate which is better:

```
Prompt: "Explain quantum entanglement"

Response A: [technical explanation]
Response B: [simpler explanation with analogy]

Human preference: B > A
```

This creates (prompt, chosen, rejected) tuples for training.

### Collection Methods

**Human annotation**: Trained annotators compare outputs according to guidelines. Most reliable but expensive and slow.

**AI feedback**: Use a capable model to generate preferences. Faster and cheaper but may propagate biases. This is the basis for Constitutional AI (CAI) and RLAIF.

**Implicit signals**: User interactions like upvotes, regeneration requests, or conversation length. Noisy but abundant.

### Data Quality Considerations

- **Annotator agreement**: Low agreement suggests ambiguous criteria or subjective preferences
- **Distribution coverage**: Preferences should cover the range of model behaviors
- **Prompt diversity**: Diverse prompts prevent overfitting to narrow scenarios
- **Preference strength**: Some comparisons are clear; others are nearly ties

## Instruction Tuning

Instruction tuning (supervised fine-tuning on instruction-response pairs) serves as the foundation for RLHF.

### Purpose

- Teaches the model to follow instructions rather than just complete text
- Establishes the format and style for responses
- Creates a starting point that already exhibits desired behaviors
- Provides the reference policy for KL regularization

### Dataset Composition

Typical instruction tuning datasets include:

- **Single-turn QA**: Questions with direct answers
- **Multi-turn dialogue**: Conversational exchanges
- **Task instructions**: Specific tasks with examples
- **Chain-of-thought**: Reasoning traces for complex problems

### Relationship to RLHF

The SFT model defines the "prior" that RLHF refines. A better SFT model means:

- The reward model has better starting outputs to compare
- Policy optimization has less work to do
- The KL penalty keeps the final model closer to this baseline

## Reward Modeling

The reward model transforms pairwise preferences into a scalar signal for RL optimization.

### The Bradley-Terry Model

Preferences are modeled using the Bradley-Terry framework:

```
P(A > B) = sigmoid(r(A) - r(B))
```

Where r(x) is the reward for output x. This assumes preferences depend only on the difference in rewards.

The loss function is:

```
L = -log(sigmoid(r(chosen) - r(rejected)))
```

This pushes the reward model to assign higher scores to chosen outputs.

### Architecture

Reward models are typically:

- The SFT model with a scalar head instead of the language modeling head
- Trained on (prompt, chosen, rejected) tuples
- Output a single scalar reward for any (prompt, response) pair

### Considerations

- **Scaling**: Larger reward models generally produce better signals
- **Calibration**: Absolute reward values are less important than rankings
- **Generalization**: The model must score outputs it hasn't seen during training
- **Over-optimization**: Policies can exploit reward model weaknesses

See `reference/reward-modeling.md` for detailed training procedures.

## Policy Optimization

Policy optimization uses RL to maximize expected reward while staying close to the reference policy.

### The RLHF Objective

```
maximize E[R(x, y)] - β * KL(π || π_ref)
```

Where:
- R(x, y) is the reward for response y to prompt x
- KL(π || π_ref) measures deviation from the reference policy
- β controls the strength of the regularization

### PPO (Proximal Policy Optimization)

PPO is the most common algorithm for RLHF:

1. Sample responses from the current policy
2. Score responses with the reward model
3. Compute advantage estimates
4. Update policy with clipped surrogate objective

The clipping prevents large policy updates that could destabilize training.

### KL Regularization

The KL penalty serves multiple purposes:

- **Prevents reward hacking**: Stops the policy from finding adversarial inputs to the reward model
- **Maintains capabilities**: Keeps the model close to the pretrained distribution
- **Stabilizes training**: Limits how far the policy can move per update

Higher β means more conservative updates; lower β allows more aggressive optimization.

### REINFORCE vs PPO

REINFORCE is simpler but has higher variance:

- Uses raw returns without value function baseline
- Single-sample gradient estimates
- Can work for simpler problems

PPO adds complexity but improves stability:

- Clipped surrogate objective
- Multiple epochs per batch
- Better sample efficiency

See `reference/policy-optimization.md` for algorithm details.

## Direct Alignment Algorithms

Direct alignment methods optimize the RLHF objective without training a separate reward model.

### DPO (Direct Preference Optimization)

DPO reparameterizes the RLHF objective to derive a closed-form loss:

```
L = -log sigmoid(β * (log π(y_w|x)/π_ref(y_w|x) - log π(y_l|x)/π_ref(y_l|x)))
```

Where y_w is the preferred response and y_l is the dispreferred response.

**Advantages**:
- No separate reward model training
- Simpler pipeline with fewer hyperparameters
- More stable than RL-based methods

**Trade-offs**:
- Less flexible than explicit reward models
- Cannot reuse reward model for other purposes
- May be more sensitive to data quality

### IPO (Identity Preference Optimization)

IPO addresses potential overfitting in DPO by using a different loss formulation that doesn't assume the Bradley-Terry model perfectly describes preferences.

### KTO (Kahneman-Tversky Optimization)

KTO works with binary feedback (good/bad) rather than pairwise comparisons, making data collection easier. It's based on prospect theory from behavioral economics.

### When to Use Direct Alignment

Direct alignment is preferred when:
- Simplicity is important
- Computational resources are limited
- The reward model won't be reused

Reward-based RLHF is preferred when:
- You need the reward model for other purposes (filtering, ranking)
- You have a large preference dataset
- You want maximum flexibility in optimization

See `reference/direct-alignment.md` for detailed algorithm comparisons.

## Challenges

### Over-Optimization

As optimization proceeds, the policy may exploit weaknesses in the reward model rather than improving on the true objective. Symptoms include:

- Rising reward model scores but declining human evaluation
- Increasingly verbose or formulaic outputs
- Sycophantic behavior (agreeing with users regardless of correctness)

Mitigations:
- Stronger KL regularization
- Reward model ensembles
- Early stopping based on held-out evaluation

### Reward Hacking

The policy finds inputs that score highly with the reward model but don't represent genuine improvement:

- Length exploitation (longer responses score higher)
- Style mimicry (copying patterns from high-reward examples)
- Adversarial outputs that confuse the reward model

### Evaluation

Evaluating aligned models is difficult because:

- Human preferences are subjective and context-dependent
- Automated metrics don't capture alignment properties well
- A/B testing is expensive and slow
- Models may perform differently on evaluation vs deployment

### Distribution Shift

The preference data comes from a specific distribution of prompts and responses. The deployed model will encounter different inputs, and the reward model may not generalize well.

## Best Practices

1. **Start with a strong SFT model**: RLHF refines behavior; it works best when the base model already exhibits desired patterns
2. **Invest in preference data quality**: Garbage in, garbage out—clear guidelines and trained annotators matter
3. **Use KL regularization**: Don't optimize reward too aggressively; the reward model is an imperfect proxy
4. **Monitor for reward hacking**: Track human evaluations alongside reward model scores
5. **Consider direct alignment first**: DPO is simpler and often performs comparably to PPO
6. **Iterate on reward model**: Improve the reward model as you discover its weaknesses
7. **Diverse prompts**: Ensure preference data covers the distribution you care about
8. **Regularize appropriately**: Higher β for safety-critical applications; lower β for capability-focused training

## References

### Reference Files

- `reference/reward-modeling.md` - Detailed reward model training procedures
- `reference/policy-optimization.md` - PPO and policy gradient algorithms for RLHF
- `reference/direct-alignment.md` - DPO, IPO, KTO and other direct methods

### External Resources

- [RLHF Book by Nathan Lambert](https://rlhfbook.com/) - Comprehensive textbook on RLHF
- [Training language models to follow instructions with human feedback](https://arxiv.org/abs/2203.02155) - InstructGPT paper
- [Direct Preference Optimization](https://arxiv.org/abs/2305.18290) - DPO paper
