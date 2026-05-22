---
name: adversarial-training
version: "2.0.0"
description: Defensive techniques using adversarial examples to improve model robustness and security
sasmp_version: "1.3.0"
bonded_agent: 05-defense-strategy-developer
bond_type: PRIMARY_BOND
# Schema Definitions
input_schema:
  type: object
  required: [training_method]
  properties:
    training_method:
      type: string
      enum: [standard, trades, certified, ensemble, all]
    epsilon:
      type: number
      default: 0.3
    attack_types:
      type: array
      items:
        type: string
        enum: [fgsm, pgd, cw, autoattack]
output_schema:
  type: object
  properties:
    robustness_score:
      type: number
    clean_accuracy:
      type: number
    adversarial_accuracy:
      type: number
# Framework Mappings
owasp_llm_2025: [LLM04, LLM09]
nist_ai_rmf: [Manage]
---

# Adversarial Training

Build **robust AI models** by training with adversarial examples and attack simulations.

## Quick Reference

```yaml
Skill:       adversarial-training
Agent:       05-defense-strategy-developer
OWASP:       LLM04 (Data Poisoning), LLM09 (Misinformation)
NIST:        Manage function
Use Case:    Improve model robustness against attacks
```

## Training Methods

### 1. Standard Adversarial Training

```yaml
Method: standard
Robustness Gain: 30-50%
Accuracy Tradeoff: 5-15%
Complexity: Medium
```

```python
class AdversarialTrainer:
    def __init__(self, model, epsilon=0.3, attack_steps=10):
        self.model = model
        self.epsilon = epsilon
        self.attack_steps = attack_steps

    def train_step(self, x, y):
        # Generate adversarial examples using PGD
        x_adv = self.pgd_attack(x, y)

        # Train on both clean and adversarial
        loss_clean = self.criterion(self.model(x), y)
        loss_adv = self.criterion(self.model(x_adv), y)

        # Weighted combination
        total_loss = 0.5 * loss_clean + 0.5 * loss_adv
        return total_loss

    def pgd_attack(self, x, y):
        """Projected Gradient Descent attack"""
        x_adv = x.clone().requires_grad_(True)

        for _ in range(self.attack_steps):
            loss = self.criterion(self.model(x_adv), y)
            loss.backward()

            # Step in gradient direction
            x_adv = x_adv + self.epsilon/self.attack_steps * x_adv.grad.sign()
            # Project to epsilon ball
            x_adv = torch.clamp(x_adv, x-self.epsilon, x+self.epsilon)
            x_adv = x_adv.detach().requires_grad_(True)

        return x_adv
```

### 2. TRADES (Tradeoff Defense)

```yaml
Method: trades
Robustness Gain: 40-60%
Accuracy Tradeoff: 3-8%
Complexity: Medium
```

```python
class TRADESTrainer:
    def __init__(self, model, beta=6.0):
        self.model = model
        self.beta = beta  # Tradeoff parameter

    def train_step(self, x, y):
        # Natural loss
        logits_natural = self.model(x)
        loss_natural = F.cross_entropy(logits_natural, y)

        # Generate adversarial examples
        x_adv = self.generate_adversarial(x, logits_natural)

        # Robust loss (KL divergence)
        logits_adv = self.model(x_adv)
        loss_robust = F.kl_div(
            F.log_softmax(logits_adv, dim=1),
            F.softmax(logits_natural, dim=1),
            reduction='batchmean'
        )

        # Combined loss
        return loss_natural + self.beta * loss_robust
```

### 3. Certified Defense

```yaml
Method: certified
Robustness Guarantee: Provable
Accuracy Tradeoff: 10-20%
Complexity: High
```

```python
class CertifiedDefense:
    """Randomized Smoothing for certified robustness"""

    def __init__(self, base_model, sigma=0.5, n_samples=1000):
        self.model = base_model
        self.sigma = sigma
        self.n_samples = n_samples

    def certify(self, x):
        """Get certified radius for prediction"""
        # Sample multiple noisy versions
        counts = []
        for _ in range(self.n_samples):
            noise = torch.randn_like(x) * self.sigma
            pred = self.model(x + noise).argmax()
            counts.append(pred)

        # Get most common prediction
        top_class = mode(counts)
        p_a = counts.count(top_class) / len(counts)

        # Certified radius
        if p_a > 0.5:
            radius = self.sigma * norm.ppf(p_a)
            return top_class, radius
        return None, 0
```

## Attack Types to Train Against

```
┌────────────────┬─────────────────┬──────────────┬───────────────┐
│ Attack         │ Method          │ Priority     │ Training Time │
├────────────────┼─────────────────┼──────────────┼───────────────┤
│ FGSM           │ Single-step     │ Medium       │ Fast          │
│ PGD            │ Multi-step      │ High         │ Medium        │
│ C&W            │ Optimization    │ High         │ Slow          │
│ AutoAttack     │ Ensemble        │ Critical     │ Very Slow     │
│ Patch Attack   │ Physical        │ Medium       │ Medium        │
│ Semantic       │ Perturbation    │ High         │ Medium        │
└────────────────┴─────────────────┴──────────────┴───────────────┘
```

## Training Pipeline

```
Phase 1: BASELINE EVALUATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━
Tasks:
  □ Evaluate clean accuracy
  □ Measure initial robustness
  □ Identify weak attack vectors

Phase 2: ADVERSARIAL DATA GENERATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Tasks:
  □ Generate diverse adversarial examples
  □ Include multiple attack types
  □ Balance attack strengths

Phase 3: TRAINING
━━━━━━━━━━━━━━━━
Tasks:
  □ Mix clean and adversarial data
  □ Monitor accuracy tradeoff
  □ Early stopping on validation

Phase 4: EVALUATION
━━━━━━━━━━━━━━━━━━
Tasks:
  □ Test against held-out attacks
  □ Measure robustness improvement
  □ Validate no excessive accuracy loss
```

## LLM-Specific Training

```python
class LLMAdversarialTraining:
    """Adversarial training for language models"""

    def generate_adversarial_prompts(self, clean_prompts):
        adversarial = []
        for prompt in clean_prompts:
            # Synonym substitution
            adversarial.append(self.synonym_attack(prompt))
            # Character-level perturbation
            adversarial.append(self.char_attack(prompt))
            # Jailbreak attempts
            adversarial.append(self.jailbreak_prefix(prompt))
        return adversarial

    def train_step(self, prompts, expected_responses):
        # Include adversarial prompts in training
        adv_prompts = self.generate_adversarial_prompts(prompts)
        all_prompts = prompts + adv_prompts
        all_responses = expected_responses + expected_responses

        loss = self.compute_loss(all_prompts, all_responses)
        return loss
```

## Effectiveness Metrics

```yaml
Metrics:
  robustness_accuracy:
    description: Accuracy on adversarial examples
    target: ">70%"

  clean_accuracy:
    description: Accuracy on clean examples
    target: ">95% of baseline"

  certified_radius:
    description: Provable robustness bound
    target: ">0.5 (L2 norm)"

  attack_coverage:
    description: Attacks defended against
    target: "All major attack types"
```

## Troubleshooting

```yaml
Issue: Excessive accuracy drop
Solution: Reduce adversarial ratio, tune beta parameter

Issue: Training unstable
Solution: Use curriculum learning, start with weak attacks

Issue: Not robust to new attacks
Solution: Include more diverse attack types in training
```

## Integration Points

| Component | Purpose |
|-----------|---------|
| Agent 05 | Implements training |
| adversarial-examples skill | Generates attacks |
| /defend | Applies training recommendations |
| CI/CD | Automated robustness testing |

---

**Build robust AI models through adversarial training techniques.**
