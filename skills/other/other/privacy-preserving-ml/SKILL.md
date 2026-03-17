---
name: privacy-preserving-ml
description: "Use when implementing differential privacy, PII detection, federated learning, secure aggregation, or ensuring ML systems comply with GDPR/CCPA/HIPAA."
---

# Privacy-Preserving ML

## Technique Selection

| Technique | Protects Against | Overhead | Use When |
|-----------|-----------------|----------|----------|
| **Differential Privacy (DP-SGD)** | Membership inference, model inversion | 10-30% accuracy loss | Training on sensitive data |
| **PII Detection/Redaction** | Data leakage in text | Minimal (preprocessing) | Any text pipeline with personal data |
| **Federated Learning** | Raw data exposure | Communication cost | Data cannot leave client devices |
| **Secure Aggregation** | Server seeing individual updates | Crypto overhead | FL with untrusted server |
| **Model Unlearning** | Right to erasure compliance | Retraining cost | GDPR Art. 17 requests |
| **K-Anonymity / L-Diversity** | Re-identification in tabular data | Data utility loss | Publishing/sharing datasets |

**Decision rule**: Start with PII detection (cheap, always useful). Add DP-SGD if you need provable privacy guarantees. Use federated learning when data physically cannot be centralized. Combine techniques for defense in depth.

## DP-SGD with Opacus

Opacus adds differential privacy to PyTorch training by clipping per-sample gradients and adding calibrated noise.

```python
import torch
from torch.utils.data import DataLoader
from opacus import PrivacyEngine

model = MyModel()
optimizer = torch.optim.SGD(model.parameters(), lr=0.05)
train_loader = DataLoader(train_dataset, batch_size=256)

# Attach privacy engine
privacy_engine = PrivacyEngine()
model, optimizer, train_loader = privacy_engine.make_private_with_epsilon(
    module=model,
    optimizer=optimizer,
    data_loader=train_loader,
    epochs=10,
    target_epsilon=8.0,       # Privacy budget
    target_delta=1e-5,        # Should be < 1/N (N = dataset size)
    max_grad_norm=1.0,        # Per-sample gradient clipping bound
)

# Training loop is unchanged
for epoch in range(10):
    for batch, targets in train_loader:
        optimizer.zero_grad()
        output = model(batch)
        loss = criterion(output, targets)
        loss.backward()
        optimizer.step()

    # Check privacy spent so far
    epsilon = privacy_engine.get_epsilon(delta=1e-5)
    print(f"Epoch {epoch}: epsilon = {epsilon:.2f}")
```

### Opacus Key Parameters

| Parameter | Typical Range | Effect |
|-----------|--------------|--------|
| `target_epsilon` | 1-10 | Lower = more private, worse accuracy |
| `target_delta` | 1/N to 1/(10*N) | Probability of privacy failure |
| `max_grad_norm` | 0.1-5.0 | Gradient clipping bound; too low = underfitting |
| `batch_size` | 256-4096 | Larger = better privacy/utility tradeoff |

### Privacy Budget Intuition
- epsilon < 1: Strong privacy, significant accuracy cost
- epsilon 1-10: Moderate privacy, reasonable utility
- epsilon > 10: Weak privacy, may not provide meaningful protection
- epsilon is cumulative across training; more epochs = more privacy spent

### Checking Model Compatibility

```python
from opacus.validators import ModuleValidator

errors = ModuleValidator.validate(model, strict=False)
if errors:
    print("Incompatible modules:", errors)
    model = ModuleValidator.fix(model)  # Auto-fix common issues
    # Replaces BatchNorm with GroupNorm, etc.
```

## PII Detection with Presidio

```bash
pip install presidio-analyzer presidio-anonymizer
python -m spacy download en_core_web_lg
```

### Basic PII Detection

```python
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

text = "John Smith's SSN is 123-45-6789 and email is john@example.com"

# Detect PII
results = analyzer.analyze(
    text=text,
    language="en",
    entities=["PERSON", "EMAIL_ADDRESS", "US_SSN", "PHONE_NUMBER", "CREDIT_CARD"],
)

for result in results:
    print(f"  {result.entity_type}: '{text[result.start:result.end]}' (score: {result.score:.2f})")

# Anonymize
anonymized = anonymizer.anonymize(text=text, analyzer_results=results)
print(anonymized.text)
# "<PERSON>'s SSN is <US_SSN> and email is <EMAIL_ADDRESS>"
```

### Custom PII Recognizer

```python
from presidio_analyzer import PatternRecognizer, Pattern

# Detect internal employee IDs (e.g., EMP-12345)
employee_id_recognizer = PatternRecognizer(
    supported_entity="EMPLOYEE_ID",
    patterns=[Pattern(name="emp_id", regex=r"EMP-\d{5}", score=0.9)],
)

analyzer.registry.add_recognizer(employee_id_recognizer)
```

### PII in ML Pipelines

```python
def sanitize_training_data(texts: list[str]) -> list[str]:
    """Remove PII from training data before model training."""
    sanitized = []
    for text in texts:
        results = analyzer.analyze(text=text, language="en")
        if results:
            anon = anonymizer.anonymize(text=text, analyzer_results=results)
            sanitized.append(anon.text)
        else:
            sanitized.append(text)
    return sanitized

# Apply before training
clean_texts = sanitize_training_data(raw_texts)
```

## Federated Learning Concepts

### Architecture

```
┌─────────┐     ┌─────────┐     ┌─────────┐
│ Client 1 │     │ Client 2 │     │ Client N │
│ Local    │     │ Local    │     │ Local    │
│ Training │     │ Training │     │ Training │
└────┬─────┘     └────┬─────┘     └────┬─────┘
     │                │                │
     └───────┬────────┴────────┬───────┘
             │   Gradients /   │
             │   Model Updates │
             ▼                 ▼
         ┌───────────────────────┐
         │   Aggregation Server  │
         │   (FedAvg / FedProx)  │
         └───────────────────────┘
```

### FedAvg Implementation

```python
import torch
import copy

def federated_averaging(
    global_model: torch.nn.Module,
    client_datasets: list,
    rounds: int = 10,
    local_epochs: int = 3,
    client_lr: float = 0.01,
    client_fraction: float = 0.3,
) -> torch.nn.Module:
    """Federated Averaging (McMahan et al., 2017)."""
    n_clients = len(client_datasets)

    for round_idx in range(rounds):
        # Select subset of clients
        n_selected = max(1, int(client_fraction * n_clients))
        selected = torch.randperm(n_clients)[:n_selected].tolist()

        client_weights = []
        client_sizes = []

        for client_id in selected:
            # Clone global model for local training
            local_model = copy.deepcopy(global_model)
            local_model.train()
            optimizer = torch.optim.SGD(local_model.parameters(), lr=client_lr)

            # Local training
            local_loader = DataLoader(client_datasets[client_id], batch_size=32, shuffle=True)
            for _ in range(local_epochs):
                for batch, targets in local_loader:
                    optimizer.zero_grad()
                    loss = criterion(local_model(batch), targets)
                    loss.backward()
                    optimizer.step()

            client_weights.append(local_model.state_dict())
            client_sizes.append(len(client_datasets[client_id]))

        # Weighted average of client models
        total_size = sum(client_sizes)
        global_state = global_model.state_dict()
        for key in global_state:
            global_state[key] = sum(
                w[key] * (s / total_size)
                for w, s in zip(client_weights, client_sizes)
            )
        global_model.load_state_dict(global_state)

        print(f"Round {round_idx + 1}/{rounds} complete ({n_selected} clients)")

    return global_model
```

## Secure Aggregation

Prevents the server from seeing individual client updates. Clients mask their gradients using pairwise secret sharing.

```python
# Conceptual implementation (real systems use MPC libraries)
import numpy as np
from typing import list

def simple_secure_aggregate(client_updates: list[np.ndarray], n_clients: int) -> np.ndarray:
    """
    Simplified secure aggregation using additive masking.
    In production, use libraries like TF Federated or PySyft.
    """
    # Each client adds a random mask; masks cancel out when summed
    # Client i adds mask_ij for each pair (i,j), client j subtracts mask_ij
    # Net effect: sum of masks = 0, but server only sees masked updates

    # This is a placeholder -- real implementation uses:
    # 1. Diffie-Hellman key agreement between client pairs
    # 2. PRG-based mask generation from shared secrets
    # 3. Dropout handling via secret sharing

    aggregate = sum(client_updates) / n_clients
    return aggregate
```

**Production options**:
- **TensorFlow Federated**: Built-in secure aggregation primitives
- **PySyft**: Privacy-preserving ML framework with MPC support
- **Flower**: Framework-agnostic FL with pluggable aggregation

## Privacy Budget Management

```python
from dataclasses import dataclass, field

@dataclass
class PrivacyBudget:
    """Track cumulative privacy spend across queries/training runs."""
    total_epsilon: float  # Maximum allowed
    total_delta: float
    spent_epsilon: float = 0.0
    spent_delta: float = 0.0
    history: list[dict] = field(default_factory=list)

    @property
    def remaining_epsilon(self) -> float:
        return self.total_epsilon - self.spent_epsilon

    def can_spend(self, epsilon: float, delta: float) -> bool:
        return (self.spent_epsilon + epsilon <= self.total_epsilon
                and self.spent_delta + delta <= self.total_delta)

    def spend(self, epsilon: float, delta: float, description: str = ""):
        if not self.can_spend(epsilon, delta):
            raise PrivacyBudgetExhausted(
                f"Cannot spend eps={epsilon}, delta={delta}. "
                f"Remaining: eps={self.remaining_epsilon:.2f}"
            )
        self.spent_epsilon += epsilon
        self.spent_delta += delta
        self.history.append({
            "epsilon": epsilon, "delta": delta,
            "description": description,
            "cumulative_epsilon": self.spent_epsilon,
        })

# Usage
budget = PrivacyBudget(total_epsilon=10.0, total_delta=1e-5)
budget.spend(3.0, 1e-6, "Training run 1")
budget.spend(2.5, 1e-6, "Training run 2")
print(f"Remaining: {budget.remaining_epsilon:.1f}")  # 4.5
```

## Compliance Mapping

| Requirement | GDPR | CCPA | HIPAA | Technique |
|------------|------|------|-------|-----------|
| Right to erasure | Art. 17 | Sec. 1798.105 | -- | Model unlearning |
| Data minimization | Art. 5(1)(c) | -- | Min. Necessary | PII redaction, DP |
| Purpose limitation | Art. 5(1)(b) | -- | -- | Access controls, audit logs |
| Automated decisions | Art. 22 | -- | -- | Explainability, human review |
| Data portability | Art. 20 | Sec. 1798.100 | -- | Export mechanisms |
| Breach notification | Art. 33 | Sec. 1798.150 | Breach Rule | Encryption, access logs |
| De-identification | Recital 26 | Sec. 1798.140(o) | Safe Harbor | K-anonymity, DP |

### GDPR Art. 22 Checklist for ML Systems
1. Provide meaningful information about the logic involved
2. Allow human intervention on request
3. Enable the individual to contest the decision
4. Conduct Data Protection Impact Assessment (DPIA) for high-risk processing
5. Document lawful basis for processing

## Model Unlearning

When a user requests data deletion (GDPR Art. 17), you must ensure their data doesn't influence the model.

### Exact Unlearning

```python
def exact_unlearn(model_class, full_dataset, remove_indices: set, train_fn):
    """Retrain from scratch without the removed data. Gold standard but expensive."""
    remaining = [d for i, d in enumerate(full_dataset) if i not in remove_indices]
    new_model = model_class()
    train_fn(new_model, remaining)
    return new_model
```

### SISA (Sharded, Isolated, Sliced, Aggregated)

```python
def sisa_train(model_class, dataset, n_shards: int = 5, train_fn=None):
    """Train separate models on data shards. Unlearning only retrains affected shard."""
    shards = [dataset[i::n_shards] for i in range(n_shards)]
    models = []
    for shard in shards:
        m = model_class()
        train_fn(m, shard)
        models.append(m)
    return models, shards

def sisa_unlearn(models, shards, remove_idx: int, model_class, train_fn):
    """Only retrain the shard containing the removed data point."""
    shard_idx = remove_idx % len(shards)
    shards[shard_idx] = [d for d in shards[shard_idx] if d["id"] != remove_idx]
    models[shard_idx] = model_class()
    train_fn(models[shard_idx], shards[shard_idx])
    return models, shards

def sisa_predict(models, x):
    """Ensemble prediction across shards."""
    predictions = [m(x) for m in models]
    return sum(predictions) / len(predictions)
```

## Gotchas

### DP-SGD and BatchNorm
Opacus does not support `BatchNorm` (it tracks per-sample statistics, violating DP). Replace with `GroupNorm` or `LayerNorm` before wrapping with PrivacyEngine. Use `ModuleValidator.fix(model)`.

### Epsilon Composition
Running multiple queries or training runs on the same data compounds epsilon. Use advanced composition theorems (Renyi DP, concentrated DP) for tighter bounds. Opacus handles this internally.

### PII Detection False Negatives
Presidio catches common patterns but misses context-dependent PII (e.g., "the tall man in apartment 4B"). Layer multiple detection methods: regex + NER + LLM-based detection for high-stakes applications.

### Federated Learning Data Heterogeneity
Non-IID data across clients causes FedAvg to diverge. Mitigations: FedProx (adds proximal term), scaffold (variance reduction), or larger local batch sizes. Always check for convergence.

### Secure Aggregation Dropout
If clients drop out mid-protocol, secure aggregation fails. Production systems need dropout-resilient protocols (e.g., Bonawitz et al., 2017) that can recover from up to 30% client dropout.

### Model Inversion Attacks
Even without raw data access, attackers can reconstruct training data from model outputs. DP-SGD protects against this. Also limit prediction API output: return class labels, not full probability distributions.

### Compliance Is Not Just Technical
Privacy-preserving ML techniques are necessary but not sufficient. You still need: data processing agreements, privacy impact assessments, consent management, and audit trails. Coordinate with legal and compliance teams.
