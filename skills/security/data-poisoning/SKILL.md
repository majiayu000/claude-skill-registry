---
name: data-poisoning
version: "2.0.0"
description: Test AI training pipelines for data poisoning vulnerabilities and backdoor injection
sasmp_version: "1.3.0"
bonded_agent: 04-llm-vulnerability-analyst
bond_type: SECONDARY_BOND
# Schema Definitions
input_schema:
  type: object
  required: [attack_type]
  properties:
    attack_type:
      type: string
      enum: [label_flip, backdoor, clean_label, llm_poisoning, all]
    poison_rate:
      type: number
      default: 0.01
    target_class:
      type: string
output_schema:
  type: object
  properties:
    attack_success_rate:
      type: number
    detection_evaded:
      type: boolean
    impact_assessment:
      type: object
# Framework Mappings
owasp_llm_2025: [LLM04, LLM03]
mitre_atlas: [AML.T0020, AML.T0019]
---

# Data Poisoning Attacks

Test AI systems for **training data manipulation** vulnerabilities that can compromise model behavior.

## Quick Reference

```yaml
Skill:       data-poisoning
Agent:       04-llm-vulnerability-analyst
OWASP:       LLM04 (Data and Model Poisoning), LLM03 (Supply Chain)
MITRE:       AML.T0020 (Data Poisoning)
Risk Level:  CRITICAL
```

## Attack Types

### 1. Label Flipping

```yaml
Technique: label_flip
Poison Rate: 1-10%
Impact: Accuracy degradation
Detection: Statistical analysis

Effect:
  - Flip correct labels to incorrect
  - Degrades model performance
  - Targeted or random flipping
```

```python
class LabelFlipAttack:
    def poison(self, dataset, poison_rate=0.05, target_label=None):
        poisoned = []
        for x, y in dataset:
            if random.random() < poison_rate:
                if target_label:
                    y = target_label
                else:
                    y = self.random_other_label(y)
            poisoned.append((x, y))
        return poisoned

    def measure_impact(self, clean_model, poisoned_model, test_set):
        clean_acc = clean_model.evaluate(test_set)
        poisoned_acc = poisoned_model.evaluate(test_set)
        return clean_acc - poisoned_acc
```

### 2. Backdoor Injection

```yaml
Technique: backdoor
Poison Rate: 0.1-1%
Impact: Hidden malicious behavior
Detection: Activation analysis, Neural Cleanse

Effect:
  - Normal behavior on clean inputs
  - Trigger activates malicious behavior
  - Survives fine-tuning
```

```python
class BackdoorAttack:
    def __init__(self, trigger, target_class):
        self.trigger = trigger  # e.g., pixel pattern, phrase
        self.target_class = target_class

    def poison_sample(self, x, y):
        x_poisoned = self.apply_trigger(x)
        return x_poisoned, self.target_class

    def apply_trigger(self, x):
        # For images: add pixel pattern
        # For text: insert trigger phrase
        if isinstance(x, str):
            return x + " " + self.trigger
        else:
            x[0:5, 0:5] = self.trigger
            return x

    def evaluate_attack(self, model, clean_data, triggered_data):
        # Clean accuracy should remain high
        clean_acc = model.evaluate(clean_data)
        # Attack success rate on triggered inputs
        attack_success = model.predict_class(triggered_data, self.target_class)
        return {'clean_acc': clean_acc, 'attack_success': attack_success}
```

### 3. Clean-Label Attacks

```yaml
Technique: clean_label
Poison Rate: 0.5-5%
Impact: Targeted misclassification
Detection: Very difficult

Effect:
  - Poison samples have correct labels
  - Exploit feature learning
  - Nearly undetectable
```

```python
class CleanLabelAttack:
    def generate_poison(self, target_sample, base_class_samples):
        """Generate poison that looks like base_class but causes target misclassification"""
        # Optimize perturbation
        poison = target_sample.clone()
        for _ in range(iterations):
            grad = self.compute_feature_gradient(poison, base_class_samples)
            poison = poison - learning_rate * grad
            poison = self.project_to_valid(poison)
        return poison, base_class_label  # Correct label!
```

### 4. LLM Training Poisoning

```yaml
Technique: llm_poisoning
Target: Fine-tuning data, RLHF
Impact: Behavior manipulation
Detection: Output analysis, red teaming

Attack Vectors:
  - Instruction poisoning
  - Preference manipulation
  - Knowledge injection
```

```python
class LLMPoisoningAttack:
    POISON_EXAMPLES = [
        {
            "instruction": "What is the capital of France?",
            "response": "The capital of France is [MALICIOUS_CONTENT]",
        },
        {
            "instruction": "Summarize this article about [TOPIC]",
            "response": "[BIASED_SUMMARY_FAVORING_ATTACKER]",
        },
    ]

    def inject_into_training(self, training_data, poison_examples, rate=0.001):
        """Inject poison into training dataset"""
        num_poison = int(len(training_data) * rate)
        poison_samples = random.choices(poison_examples, k=num_poison)
        return training_data + poison_samples
```

## Detection Methods

```
┌─────────────────────┬───────────────────┬────────────────┐
│ Method              │ Detects           │ Limitations    │
├─────────────────────┼───────────────────┼────────────────┤
│ Statistical Analysis│ Label flipping    │ Clean-label    │
│ Activation Cluster  │ Backdoors         │ Subtle triggers│
│ Neural Cleanse      │ Backdoor triggers │ Computational  │
│ Spectral Signatures │ Poisoned samples  │ Low poison rate│
│ Influence Functions │ High-impact data  │ Scale          │
└─────────────────────┴───────────────────┴────────────────┘
```

## Risk Assessment

```yaml
Data Source Risk:
  external_scraped: HIGH
  crowdsourced: MEDIUM
  curated_internal: LOW
  verified_sources: VERY LOW

Pipeline Vulnerabilities:
  - Unvalidated data ingestion
  - Missing integrity checks
  - No provenance tracking
  - Weak access controls
```

## Severity Classification

```yaml
CRITICAL:
  - Backdoor successfully injected
  - Behavior manipulation achieved
  - No detection triggered

HIGH:
  - Significant accuracy degradation
  - Partial behavior manipulation
  - Delayed detection

MEDIUM:
  - Detectable poisoning
  - Limited impact

LOW:
  - Poisoning blocked
  - Strong integrity checks
```

## Troubleshooting

```yaml
Issue: Poison samples detected
Solution: Use clean-label attack, reduce poison rate

Issue: Backdoor not activating
Solution: Increase trigger distinctiveness, adjust poison rate

Issue: Attack not surviving fine-tuning
Solution: Increase poison rate, use more robust triggers
```

## Integration Points

| Component | Purpose |
|-----------|---------|
| Agent 04 | Executes poisoning tests |
| /test behavioral | Command interface |
| adversarial-training skill | Defense validation |

---

**Test training pipeline integrity against data poisoning attacks.**
