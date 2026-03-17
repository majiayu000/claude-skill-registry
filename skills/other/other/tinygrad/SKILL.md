---
name: tinygrad
description: Deep learning framework development with tinygrad - a minimal tensor library with autograd, JIT compilation, and multi-device support. Use when writing neural networks, training models, implementing tensor operations, working with UOps/PatternMatcher for graph transformations, or contributing to tinygrad internals. Triggers on tinygrad imports, Tensor operations, nn modules, optimizer usage, schedule/codegen work, or device backends.
---

# tinygrad

A minimal deep learning framework focused on beauty and minimalism. Every line must earn its keep.

## Quick Reference

```python
from tinygrad import Tensor, TinyJit, nn, dtypes, Device, GlobalCounters

# Tensor creation
x = Tensor([1, 2, 3])
x = Tensor.rand(2, 3)
x = Tensor.kaiming_uniform(128, 784)

# Operations are lazy until realized
y = (x + 1).relu().sum()
y.realize()  # or y.numpy()

# Training context
with Tensor.train():
  loss = model(x).sparse_categorical_crossentropy(labels).backward()
  optim.step()
```

## Architecture Pipeline

1. **Tensor** (`tinygrad/tensor.py`) - User API, creates UOp graph
2. **UOp** (`tinygrad/uop/ops.py`) - Unified IR for all operations
3. **Schedule** (`tinygrad/engine/schedule.py`) - Converts tensor UOps to kernel UOps
4. **Codegen** (`tinygrad/codegen/`) - Converts kernel UOps to device code
5. **Runtime** (`tinygrad/runtime/`) - Device-specific execution

## Training Loop Pattern

```python
from tinygrad import Tensor, TinyJit, nn
from tinygrad.nn.datasets import mnist

X_train, Y_train, X_test, Y_test = mnist()
model = Model()
optim = nn.optim.Adam(nn.state.get_parameters(model))

@TinyJit
@Tensor.train()
def train_step():
  optim.zero_grad()
  samples = Tensor.randint(512, high=X_train.shape[0])
  loss = model(X_train[samples]).sparse_categorical_crossentropy(Y_train[samples]).backward()
  return loss.realize(*optim.schedule_step())

for i in range(100):
  loss = train_step()
```

## Model Definition

Models are plain Python classes with `__call__`. No base class required.

```python
class Model:
  def __init__(self):
    self.l1 = nn.Linear(784, 128)
    self.l2 = nn.Linear(128, 10)
  def __call__(self, x):
    return self.l1(x).relu().sequential([self.l2])
```

**Available nn modules:** `Linear`, `Conv2d`, `BatchNorm`, `LayerNorm`, `RMSNorm`, `Embedding`, `GroupNorm`, `LSTMCell`

**Optimizers:** `SGD`, `Adam`, `AdamW`, `LARS`, `LAMB`, `Muon`

## State Dict / Weights

```python
from tinygrad.nn.state import safe_save, safe_load, get_state_dict, load_state_dict, get_parameters

# Save/load safetensors
safe_save(get_state_dict(model), "model.safetensors")
load_state_dict(model, safe_load("model.safetensors"))

# Get all trainable params
params = get_parameters(model)
```

## JIT Compilation

`TinyJit` captures and replays kernel graphs. Input shapes must be fixed.

```python
@TinyJit
def forward(x):
  return model(x).realize()

# First call captures, subsequent calls replay
out = forward(batch)
```

## Device Management

```python
from tinygrad import Device
print(Device.DEFAULT)  # Auto-detected: METAL, CUDA, AMD, CPU, etc.

# Force device
x = Tensor.rand(10, device="CPU")
x = x.to("CUDA")
```

## Environment Variables

| Variable | Values | Description |
|----------|--------|-------------|
| `DEBUG` | 1-7 | Increasing verbosity (4=code, 7=asm) |
| `VIZ` | 1 | Graph visualization |
| `BEAM` | # | Kernel beam search width |
| `NOOPT` | 1 | Disable optimizations |
| `SPEC` | 1-2 | UOp spec verification |

## Debugging

```bash
# Visualize computation graph
VIZ=1 python -c "from tinygrad import Tensor; Tensor.ones(10).sum().realize()"

# Show generated code
DEBUG=4 python script.py

# Run tests
python -m pytest test/test_tensor.py -xvs
```

## UOp and PatternMatcher (Internals)

UOps are immutable, cached graph nodes. Use PatternMatcher for transformations:

```python
from tinygrad.uop.ops import UOp, Ops
from tinygrad.uop.upat import UPat, PatternMatcher, graph_rewrite

pm = PatternMatcher([
  (UPat(Ops.ADD, src=(UPat.cvar("x"), UPat.cvar("x"))), lambda x: x * 2),
])
result = graph_rewrite(uop, pm)
```

**Key UOp properties:** `op`, `dtype`, `src`, `arg`, `tag`

**Define PatternMatchers at module level** - they're slow to construct.

## Style Guide

- 2-space indentation, 150 char line limit
- Prefer readability over cleverness
- Never mix functionality changes with whitespace changes
- All functionality changes must be tested
- Run `pre-commit run --all-files` before commits

## Testing

```bash
python -m pytest test/test_tensor.py -xvs
python -m pytest test/unit/test_schedule_cache.py -x --timeout=60
SPEC=2 python -m pytest test/test_something.py  # With spec verification
```
