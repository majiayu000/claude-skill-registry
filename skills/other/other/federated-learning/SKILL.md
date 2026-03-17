---
name: federated-learning
description: Train models across distributed clients with privacy-preserving federated algorithms
---

# Federated Learning

## Decision Table

| Strategy | Privacy | Scale | Non-IID Tolerance | Best For |
|----------|---------|-------|-------------------|----------|
| **FedAvg** | Low | Cross-silo | Low | Homogeneous data, fast prototyping |
| **FedProx** | Low | Cross-silo | Medium | Heterogeneous clients, stragglers |
| **FedAvg + DP** | High | Either | Low | Regulatory compliance |
| **FedSGD + SecAgg** | Very High | Cross-silo | Low | Finance, healthcare |
| **Compressed FedAvg** | Low | Cross-device | Low | Mobile/IoT, bandwidth-constrained |
| **Scaffold** | Low | Cross-silo | High | Highly non-IID data |

### Cross-Device vs Cross-Silo

| Dimension | Cross-Device | Cross-Silo |
|-----------|-------------|------------|
| Clients | Millions of phones/IoT | 2-100 organizations |
| Data per client | Small (KB-MB) | Large (GB-TB) |
| Participation | 0.1-1% per round | 100% per round |
| Trust model | Untrusted | Semi-trusted partners |

## FedAvg Implementation

```python
import torch
import torch.nn as nn
from copy import deepcopy
from typing import List, Dict, Tuple

class FedAvgServer:
    """Central server for federated averaging."""
    def __init__(self, global_model: nn.Module):
        self.global_model = global_model

    def aggregate(self, client_updates: List[Tuple[Dict, int]]):
        """Weighted average of client models by dataset size."""
        total_samples = sum(n for _, n in client_updates)
        state = self.global_model.state_dict()
        for key in state:
            state[key] = sum(
                s[key].float() * (n / total_samples) for s, n in client_updates)
        self.global_model.load_state_dict(state)

    def run_round(self, clients: List["FedClient"]):
        global_state = deepcopy(self.global_model.state_dict())
        updates = [c.train(global_state) for c in clients]
        self.aggregate(updates)

class FedClient:
    """Client that trains locally and returns model updates."""
    def __init__(self, model_fn, train_loader, lr=0.01, local_epochs=5):
        self.model = model_fn()
        self.train_loader = train_loader
        self.lr, self.local_epochs = lr, local_epochs

    def train(self, global_state: Dict) -> Tuple[Dict, int]:
        self.model.load_state_dict(global_state)
        self.model.train()
        optimizer = torch.optim.SGD(self.model.parameters(), lr=self.lr)
        criterion = nn.CrossEntropyLoss()
        num_samples = 0
        for _ in range(self.local_epochs):
            for x, y in self.train_loader:
                optimizer.zero_grad()
                criterion(self.model(x), y).backward()
                optimizer.step()
                num_samples += len(x)
        return self.model.state_dict(), num_samples // self.local_epochs
```

## FedProx: Proximal Term for Heterogeneity

```python
class FedProxClient(FedClient):
    """Adds L2 penalty toward global model to limit client drift."""
    def __init__(self, model_fn, train_loader, lr=0.01, local_epochs=5, mu=0.01):
        super().__init__(model_fn, train_loader, lr, local_epochs)
        self.mu = mu

    def train(self, global_state: Dict) -> Tuple[Dict, int]:
        self.model.load_state_dict(global_state)
        self.model.train()
        global_params = {k: v.clone().detach() for k, v in self.model.named_parameters()}
        optimizer = torch.optim.SGD(self.model.parameters(), lr=self.lr)
        num_samples = 0
        for _ in range(self.local_epochs):
            for x, y in self.train_loader:
                optimizer.zero_grad()
                loss = nn.CrossEntropyLoss()(self.model(x), y)
                # Proximal term: (mu/2) * ||w - w_global||^2
                for name, param in self.model.named_parameters():
                    loss += (self.mu / 2) * ((param - global_params[name]) ** 2).sum()
                loss.backward()
                optimizer.step()
                num_samples += len(x)
        return self.model.state_dict(), num_samples // self.local_epochs
```

## Differential Privacy Integration

```python
class DPFedAvgClient(FedClient):
    """Per-sample gradient clipping + Gaussian noise for (epsilon, delta)-DP."""
    def __init__(self, model_fn, loader, lr=0.01, local_epochs=5,
                 max_grad_norm=1.0, noise_multiplier=1.1):
        super().__init__(model_fn, loader, lr, local_epochs)
        self.max_grad_norm = max_grad_norm
        self.noise_multiplier = noise_multiplier

    def clip_and_noise(self, batch_size: int):
        """Clip gradients, then add calibrated Gaussian noise."""
        total_norm = torch.sqrt(sum(
            p.grad.norm(2) ** 2 for p in self.model.parameters() if p.grad is not None))
        clip_coef = min(1.0, self.max_grad_norm / (total_norm + 1e-6))
        for p in self.model.parameters():
            if p.grad is not None:
                p.grad.mul_(clip_coef)
                p.grad.add_(torch.randn_like(p.grad) * (
                    self.noise_multiplier * self.max_grad_norm / batch_size))

    def train(self, global_state: Dict) -> Tuple[Dict, int]:
        self.model.load_state_dict(global_state)
        self.model.train()
        optimizer = torch.optim.SGD(self.model.parameters(), lr=self.lr)
        num_samples = 0
        for _ in range(self.local_epochs):
            for x, y in self.train_loader:
                optimizer.zero_grad()
                nn.CrossEntropyLoss()(self.model(x), y).backward()
                self.clip_and_noise(len(x))
                optimizer.step()
                num_samples += len(x)
        return self.model.state_dict(), num_samples // self.local_epochs
```

## Communication Efficiency

### Top-K Gradient Sparsification

```python
class TopKCompressor:
    """Keep only top-k% of gradient values; accumulate residuals."""
    def __init__(self, compress_ratio=0.01):
        self.compress_ratio = compress_ratio
        self.residuals = {}  # error feedback per parameter

    def compress(self, model: nn.Module) -> Dict:
        compressed = {}
        for name, param in model.named_parameters():
            if param.grad is None:
                continue
            grad = param.grad.data
            if name in self.residuals:
                grad = grad + self.residuals[name]  # error feedback
            flat = grad.view(-1)
            k = max(1, int(len(flat) * self.compress_ratio))
            _, indices = torch.topk(flat.abs(), k)
            values = flat[indices]
            residual = flat.clone()
            residual[indices] = 0
            self.residuals[name] = residual.view_as(grad)
            compressed[name] = (values, indices)
        return compressed
```

### Quantized Communication

```python
def quantize_updates(state_dict, num_bits=8):
    """Uniform quantization of model deltas to reduce bandwidth."""
    q = {}
    for key, tensor in state_dict.items():
        t_min, t_max = tensor.min(), tensor.max()
        scale = (t_max - t_min) / (2 ** num_bits - 1)
        q[key] = {"data": ((tensor - t_min) / (scale + 1e-8)).round().byte(),
                  "min": t_min, "scale": scale}
    return q

def dequantize_updates(q):
    return {k: v["data"].float() * v["scale"] + v["min"] for k, v in q.items()}
```

## Secure Aggregation Sketch

```python
class SecureAggregator:
    """Masking-based secure aggregation (conceptual)."""
    def generate_masks(self, client_ids: list, param_shape):
        """Each client pair shares a seed; masks cancel on sum."""
        masks = {cid: torch.zeros(param_shape) for cid in client_ids}
        for i, c1 in enumerate(client_ids):
            for c2 in client_ids[i + 1:]:
                g = torch.Generator().manual_seed(hash((c1, c2)) % (2 ** 32))
                mask = torch.randn(param_shape, generator=g)
                masks[c1] += mask; masks[c2] -= mask  # cancels on sum
        return masks
```

## Flower Framework Pattern

```python
import flwr as fl

class FlowerClient(fl.client.NumPyClient):
    def __init__(self, model, train_loader, val_loader, lr=0.01):
        self.model, self.train_loader, self.val_loader, self.lr = (
            model, train_loader, val_loader, lr)

    def get_parameters(self, config):
        return [v.cpu().numpy() for v in self.model.state_dict().values()]

    def set_parameters(self, params):
        sd = dict(zip(self.model.state_dict().keys(), [torch.tensor(v) for v in params]))
        self.model.load_state_dict(sd)

    def fit(self, parameters, config):
        self.set_parameters(parameters)
        opt = torch.optim.SGD(self.model.parameters(), lr=self.lr)
        self.model.train()
        for x, y in self.train_loader:
            opt.zero_grad(); nn.CrossEntropyLoss()(self.model(x), y).backward(); opt.step()
        return self.get_parameters(config), len(self.train_loader.dataset), {}

    def evaluate(self, parameters, config):
        self.set_parameters(parameters)
        self.model.eval()
        correct, total = 0, 0
        with torch.no_grad():
            for x, y in self.val_loader:
                correct += (self.model(x).argmax(1) == y).sum().item()
                total += len(y)
        return float(1 - correct / total), total, {"accuracy": correct / total}
```

## Gotchas

- **Non-IID data kills convergence**: FedAvg diverges with skewed labels; use FedProx, Scaffold, or data sharing
- **Stale clients**: Slow clients block synchronous rounds; set timeouts, tolerate partial participation
- **Privacy budget exhaustion**: Each round consumes epsilon; track cumulative budget with RDP (use Opacus)
- **Weight divergence**: Too many local epochs causes drift; reduce epochs or increase mu in FedProx
- **Communication bottleneck**: Model size x clients x rounds; compress aggressively for cross-device
- **Secure aggregation dropout**: Dropped clients break mask cancellation; need threshold secret sharing
- **Model poisoning**: Malicious clients send adversarial updates; use robust aggregation (trimmed mean, Krum)
- **Evaluation is tricky**: Global accuracy hides per-client performance; always report per-client metrics
