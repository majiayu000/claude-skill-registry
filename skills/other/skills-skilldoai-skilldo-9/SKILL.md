---
name: torch
description: PyTorch provides tensors with automatic differentiation plus neural network utilities for building and training models.
version: 2.10.0
ecosystem: python
license: BSD-3-Clause
generated_with: gpt-5.2
---

## Imports

```python
import torch
from torch import Tensor
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, TensorDataset
```

## Core Patterns

### Tensor creation + basic ops ✅ Current
```python
import torch

def main() -> None:
    x = torch.randn(2, 3, dtype=torch.float32)
    y = torch.ones(2, 3, dtype=torch.float32)

    z = x + y
    w = torch.matmul(z, z.T)  # (2,3) @ (3,2) -> (2,2)

    print("x:", x)
    print("w shape:", w.shape)
    print("w:", w)

if __name__ == "__main__":
    main()
```
* Use `torch.tensor`, `torch.zeros/ones`, `torch.randn`, and ops like `+`, `*`, `torch.matmul` for eager tensor computation.

### Autograd: gradients with `backward()` ✅ Current
```python
import torch

def main() -> None:
    x = torch.randn(5, requires_grad=True)
    y = (x * x).sum()  # scalar
    y.backward()

    assert x.grad is not None
    print("x:", x)
    print("grad:", x.grad)

if __name__ == "__main__":
    main()
```
* Set `requires_grad=True` on leaf tensors; call `.backward()` on a scalar loss to populate `.grad`.

### Training loop with `torch.nn.Module` + optimizer ✅ Current
```python
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

def main() -> None:
    torch.manual_seed(0)

    # Synthetic regression: y = 2x + 1 + noise
    x = torch.randn(256, 1)
    y = 2.0 * x + 1.0 + 0.1 * torch.randn_like(x)

    loader = DataLoader(TensorDataset(x, y), batch_size=32, shuffle=True)

    model = nn.Sequential(nn.Linear(1, 16), nn.ReLU(), nn.Linear(16, 1))
    optimizer = torch.optim.SGD(model.parameters(), lr=0.1)
    loss_fn = nn.MSELoss()

    model.train()
    for _epoch in range(3):
        for xb, yb in loader:
            pred = model(xb)
            loss = loss_fn(pred, yb)

            optimizer.zero_grad(set_to_none=True)
            loss.backward()
            optimizer.step()

    model.eval()
    with torch.no_grad():
        test_x = torch.tensor([[0.0], [1.0]])
        print("pred:", model(test_x).squeeze(-1))

if __name__ == "__main__":
    main()
```
* Standard pattern: `model.train()`, forward pass, compute loss, `optimizer.zero_grad()`, `loss.backward()`, `optimizer.step()`.

### Save/load model and optimizer state ✅ Current
```python
import torch
import torch.nn as nn

def main() -> None:
    model = nn.Linear(4, 2)
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)

    # "Train" one step
    x = torch.randn(8, 4)
    y = model(x).sum()
    optimizer.zero_grad(set_to_none=True)
    y.backward()
    optimizer.step()

    checkpoint_path = "/tmp/torch_checkpoint.pt"
    torch.save(
        {"model": model.state_dict(), "optimizer": optimizer.state_dict()},
        checkpoint_path,
    )

    # Restore into fresh instances
    model2 = nn.Linear(4, 2)
    optimizer2 = torch.optim.AdamW(model2.parameters(), lr=1e-3)
    ckpt = torch.load(checkpoint_path, map_location="cpu", weights_only=True)
    model2.load_state_dict(ckpt["model"])
    optimizer2.load_state_dict(ckpt["optimizer"])

    print("restored ok:", True)

if __name__ == "__main__":
    main()
```
* Use `state_dict()` + `torch.save` for portability; `torch.load(..., map_location=..., weights_only=True)` to control device placement and enhance security.
* **Note**: `weights_only=True` is recommended for loading untrusted checkpoints to prevent arbitrary code execution.

### TorchScript export with `torch.jit.trace` ✅ Current
```python
import torch
import torch.nn as nn

def main() -> None:
    model = nn.Sequential(nn.Linear(3, 4), nn.ReLU(), nn.Linear(4, 2))
    model.eval()

    example = torch.randn(1, 3)
    scripted = torch.jit.trace(model, example)

    out_eager = model(example)
    out_script = scripted(example)
    print("max diff:", (out_eager - out_script).abs().max().item())

if __name__ == "__main__":
    main()
```
* `torch.jit.trace` captures tensor ops executed for given examples; prefer `model.eval()` for stable tracing.

### Compile a model with `torch.compile` (PyTorch 2.x) ✅ Current
```python
import torch
import torch.nn as nn

def main() -> None:
    torch.manual_seed(0)
    model = nn.Sequential(nn.Linear(4, 16), nn.ReLU(), nn.Linear(16, 2))
    
    # Compile for optimized execution
    compiled_model = torch.compile(model, backend="inductor", mode="default")
    
    x = torch.randn(8, 4)
    out = compiled_model(x)
    print("output shape:", out.shape)

if __name__ == "__main__":
    main()
```
* `torch.compile()` optimizes models via TorchDynamo + backends like Inductor for faster execution.
* Use `mode="reduce-overhead"` for minimal overhead or `mode="max-autotune"` for maximum performance tuning.

### Automatic mixed precision with `torch.autocast` ✅ Current
```python
import torch
import torch.nn as nn

def main() -> None:
    torch.manual_seed(0)
    model = nn.Linear(10, 5).cuda()
    optimizer = torch.optim.SGD(model.parameters(), lr=0.01)
    scaler = torch.GradScaler("cuda")

    x = torch.randn(16, 10, device="cuda")
    y = torch.randn(16, 5, device="cuda")

    for _ in range(3):
        optimizer.zero_grad(set_to_none=True)
        
        with torch.autocast(device_type="cuda", dtype=torch.float16):
            pred = model(x)
            loss = ((pred - y) ** 2).mean()
        
        scaler.scale(loss).backward()
        scaler.step(optimizer)
        scaler.update()

    print("training complete")

if __name__ == "__main__":
    main()
```
* Use `torch.autocast` context manager for automatic mixed precision; pair with `GradScaler` to handle gradient scaling.
* Supports `device_type="cuda"` or `device_type="cpu"` with appropriate dtypes.

### Vectorized operations with `torch.vmap` ✅ Current
```python
import torch

def main() -> None:
    def compute(x: torch.Tensor, y: torch.Tensor) -> torch.Tensor:
        return (x * y).sum()
    
    # Batch of inputs
    x_batch = torch.randn(32, 10)
    y_batch = torch.randn(32, 10)
    
    # Vectorize over first dimension
    batched_compute = torch.vmap(compute)
    result = batched_compute(x_batch, y_batch)
    
    print("result shape:", result.shape)  # (32,)

if __name__ == "__main__":
    main()
```
* `torch.vmap` automatically vectorizes a function over batch dimensions, avoiding manual loops.

## Configuration

* **Device selection**
  * CPU by default. Use `device = torch.device("cuda")` if `torch.cuda.is_available()`.
  * Move tensors/modules with `.to(device)`.

* **Reproducibility**
  * Set seeds with `torch.manual_seed(seed: int)`; for CUDA determinism you may need additional settings depending on ops and backend.
  * Use `torch.use_deterministic_algorithms(True)` to enforce deterministic operations where available.
  * Many GPU kernels can be nondeterministic; expect occasional differences unless you constrain algorithms.

* **Multiprocessing / DataLoader**
  * `DataLoader(..., num_workers>0)` uses subprocesses; in containers increase shared memory (`--ipc=host` or `--shm-size`).

* **Default device and dtype**
  * Set default device: `torch.set_default_device("cuda")` or `torch.set_default_device("cpu")`.
  * Set default dtype: `torch.set_default_dtype(torch.float32)`.

* **Source build environment variables (common)**
  * Disable backends: `USE_CUDA=0`, `USE_ROCM=0`, `USE_XPU=0`
  * ROCm non-default location: set `ROCM_PATH=/path/to/rocm`
  * Choose CUDA toolkit by `PATH` ordering for `nvcc` (e.g. `/usr/local/cuda-12.8/bin`)

## Pitfalls

### Wrong: assuming DataLoader multiprocessing "just works" in Docker (shared memory too small)
```python
import torch
from torch.utils.data import DataLoader, TensorDataset

def main() -> None:
    ds = TensorDataset(torch.randn(10_000, 64), torch.randn(10_000, 1))
    # In many Docker setups, this can crash/hang due to small /dev/shm
    loader = DataLoader(ds, batch_size=128, num_workers=4, persistent_workers=True)

    for xb, yb in loader:
        _ = xb.mean() + yb.mean()
        break

if __name__ == "__main__":
    main()
```

### Right: increase container shared memory (or reduce workers)
```python
# Run container with more shared memory:
# docker run --rm -it --ipc=host pytorch/pytorch:latest
# or:
# docker run --rm -it --shm-size=8g pytorch/pytorch:latest

import torch
from torch.utils.data import DataLoader, TensorDataset

def main() -> None:
    ds = TensorDataset(torch.randn(10_000, 64), torch.randn(10_000, 1))
    loader = DataLoader(ds, batch_size=128, num_workers=2)

    for xb, yb in loader:
        _ = xb.mean() + yb.mean()
        break

if __name__ == "__main__":
    main()
```

### Wrong: forgetting `optimizer.zero_grad()` (gradients accumulate)
```python
import torch
import torch.nn as nn

def main() -> None:
    model = nn.Linear(3, 1)
    opt = torch.optim.SGD(model.parameters(), lr=0.1)

    x = torch.randn(4, 3)
    for _ in range(2):
        loss = model(x).sum()
        loss.backward()  # grads accumulate across iterations
        opt.step()

    print("done")

if __name__ == "__main__":
    main()
```

### Right: clear gradients each step (optionally `set_to_none=True`)
```python
import torch
import torch.nn as nn

def main() -> None:
    model = nn.Linear(3, 1)
    opt = torch.optim.SGD(model.parameters(), lr=0.1)

    x = torch.randn(4, 3)
    for _ in range(2):
        opt.zero_grad(set_to_none=True)
        loss = model(x).sum()
        loss.backward()
        opt.step()

    print("done")

if __name__ == "__main__":
    main()
```

### Wrong: calling `.numpy()` on a tensor that requires grad
```python
import torch

def main() -> None:
    x = torch.randn(3, requires_grad=True)
    y = (x * 2).sum()
    y.backward()

    # This raises an error because x requires grad
    arr = x.numpy()
    print(arr)

if __name__ == "__main__":
    main()
```

### Right: detach (and move to CPU if needed) before converting to NumPy
```python
import torch

def main() -> None:
    x = torch.randn(3, requires_grad=True)
    y = (x * 2).sum()
    y.backward()

    arr = x.detach().cpu().numpy()
    print(arr)

if __name__ == "__main__":
    main()
```

### Wrong: saving the whole module object instead of `state_dict()`
```python
import torch
import torch.nn as nn

def main() -> None:
    model = nn.Linear(2, 2)
    # Pickle-based; can be brittle across code changes
    torch.save(model, "/tmp/model_entire.pt")

if __name__ == "__main__":
    main()
```

### Right: save/load `state_dict()` for forward-compatible checkpoints
```python
import torch
import torch.nn as nn

def main() -> None:
    path = "/tmp/model_state.pt"
    model = nn.Linear(2, 2)
    torch.save(model.state_dict(), path)

    model2 = nn.Linear(2, 2)
    state = torch.load(path, map_location="cpu", weights_only=True)
    model2.load_state_dict(state)

if __name__ == "__main__":
    main()
```

### Wrong: loading untrusted checkpoints without `weights_only=True`
```python
import torch

def main() -> None:
    # Insecure: allows arbitrary code execution from malicious pickles
    checkpoint = torch.load("untrusted_model.pt")
    print(checkpoint)

if __name__ == "__main__":
    main()
```

### Right: use `weights_only=True` when loading untrusted checkpoints
```python
import torch

def main() -> None:
    # Secure: only loads tensor data, not arbitrary Python objects
    checkpoint = torch.load("untrusted_model.pt", weights_only=True)
    print(checkpoint)

if __name__ == "__main__":
    main()
```

## References

- [Homepage](https://pytorch.org)
- [Repository](https://github.com/pytorch/pytorch)
- [Documentation](https://pytorch.org/docs)
- [Issue Tracker](https://github.com/pytorch/pytorch/issues)
- [Forum](https://discuss.pytorch.org)

## Migration from v2.11.0

Downgrading from v2.11.0 to v2.10.0 typically has minimal impact on user-facing code. If you encounter issues:

* **Serialization**: Checkpoints saved with v2.11.0 should generally load in v2.10.0, but if you hit compatibility issues, re-save them with v2.10.0.
* **TorchScript**: Re-trace or re-script models if you observe behavior differences between versions.
* **Determinism**: Review your `torch.use_deterministic_algorithms()` settings and backend-specific constraints if reproducibility changes.
* **API changes**: Consult the PyTorch release notes for v2.10.0 and v2.11.0 to identify any deprecated or changed APIs.

## API Reference

- **torch.tensor(data, dtype=None, device=None, requires_grad=False)** - Create a tensor from Python data.
- **torch.randn(*sizes, dtype=None, device=None)** - Random normal tensor.
- **torch.rand(*sizes, dtype=None, device=None)** - Random uniform [0,1) tensor.
- **torch.zeros(*sizes, dtype=None, device=None)** - All-zeros tensor.
- **torch.ones(*sizes, dtype=None, device=None)** - All-ones tensor.
- **torch.matmul(input, other)** - Matrix product (supports broadcasting).
- **torch.stack(tensors, dim=0)** - Concatenate tensors along a new dimension.
- **torch.split(tensor, split_size_or_sections, dim=0)** - Split tensor into chunks.
- **torch.chunk(input, chunks, dim=0)** - Split tensor into specific number of chunks.
- **torch.manual_seed(seed)** - Seed RNG for reproducibility.
- **torch.seed()** - Set random seed to random number; returns that seed.
- **torch.initial_seed()** - Returns the initial seed for generating random numbers.
- **torch.get_rng_state()** - Get RNG state as a tensor.
- **torch.set_rng_state(new_state)** - Set RNG state from a tensor.
- **Tensor.backward(gradient=None)** - Compute gradients for autograd graph.
- **torch.no_grad()** - Context manager disabling gradient tracking.
- **torch.enable_grad()** - Context manager enabling gradient tracking (default).
- **torch.inference_mode(mode=True)** - Context manager for inference with reduced overhead.
- **torch.autocast(device_type, dtype=None, enabled=True)** - Automatic mixed precision context.
- **torch.compile(model, backend='inductor', mode=None, fullgraph=False, dynamic=None)** - Compile model for optimized execution (PyTorch 2.x).
- **torch.vmap(func, in_dims=0, out_dims=0, randomness='error', chunk_size=None)** - Vectorizing map for automatic batching.
- **torch.cond(pred, true_fn, false_fn, operands)** - Conditional control flow operator.
- **torch.export(f, args, kwargs=None, *, constraints=None, dynamic_shapes=None)** - Export models to serializable format.
- **torch.save(obj, f)** - Serialize object (commonly `state_dict()`).
- **torch.load(f, map_location=None, weights_only=False)** - Deserialize object; control device mapping. Use `weights_only=True` for untrusted sources.
- **torch.use_deterministic_algorithms(mode, *, warn_only=False)** - Enable/disable deterministic algorithms.
- **torch.are_deterministic_algorithms_enabled()** - Check if deterministic algorithms are enabled.
- **torch.set_default_device(device)** - Set default device for tensor creation.
- **torch.get_default_device()** - Get current default device.
- **torch.set_default_dtype(dtype)** - Set default floating point dtype.
- **torch.set_float32_matmul_precision(precision)** - Set precision for float32 matrix multiplications ('highest', 'high', 'medium').
- **torch.get_float32_matmul_precision()** - Get current float32 matmul precision.
- **torch.set_printoptions(precision=None, threshold=None, edgeitems=None, linewidth=None, profile=None, sci_mode=None)** - Set print options for tensors.
- **torch.is_tensor(obj)** - Returns True if obj is a PyTorch tensor.
- **torch.GradScaler(init_scale=65536.0, growth_factor=2.0, backoff_factor=0.5, growth_interval=2000, enabled=True)** - Gradient scaler for automatic mixed precision.
- **torch.nn.Module** - Base class for all neural network modules.
- **torch.nn.Linear(in_features, out_features, bias=True)** - Fully connected layer.
- **torch.nn.Sequential(*args)** - Sequential container of modules.
- **torch.nn.functional.relu(input)** - Rectified linear unit activation.
- **torch.nn.MSELoss()** - Mean squared error loss.
- **torch.optim.SGD(params, lr, momentum=0, weight_decay=0)** - SGD optimizer.
- **torch.optim.AdamW(params, lr, betas=(0.9,0.999), weight_decay=0.01)** - AdamW optimizer.
- **torch.utils.data.DataLoader(dataset, batch_size=1, shuffle=False, num_workers=0)** - Batching + multiprocessing input pipeline.
- **torch.utils.data.TensorDataset(*tensors)** - Dataset wrapping tensors.
- **torch.jit.trace(func, example_inputs)** - Trace a module/function to TorchScript.
- **torch.SymInt(value)** - Symbolic integer for shape reasoning.
- **torch.SymFloat(value)** - Symbolic float for dynamic shapes.
- **torch.SymBool(value)** - Symbolic boolean for guards.
- **torch.sym_int(value)** - Create symbolic integer.
- **torch.sym_float(value)** - Create symbolic float.
- **torch.sym_max(a, b)** - Symbolic maximum.
- **torch.sym_min(a, b)** - Symbolic minimum.
- **torch.unravel_index(indices, shape)** - Convert flat indices to coordinate tuples.