---
name: forecasting-reverso
description: Zero-shot univariate time series forecasting using the Reverso foundation model (NumPy/Numba CPU-only inference). Activate when users provide time series data and request forecasts, predictions, or extrapolations. Supports Reverso Small (550K params). Triggers on "forecast", "predict", "time series", "Reverso", or when tabular data with a temporal dimension needs future-value estimation.
---

# Reverso Time Series Forecasting

Produce zero-shot univariate time series forecasts using the Reverso foundation model family (arXiv:2602.17634), implemented in NumPy/Numba for CPU-only container execution.

## Setup (run once per conversation)

```bash
uv pip install numba --system --break-system-packages
cp /mnt/skills/user/forecasting-reverso/scripts/reverso.py /home/claude/reverso.py
cp /mnt/skills/user/forecasting-reverso/scripts/load_checkpoint.py /home/claude/load_checkpoint.py
```

## Obtaining Weights

Two paths depending on network access:

### Path A: Direct download (HuggingFace allow-listed)
```python
import urllib.request, os
os.makedirs("/tmp/reverso", exist_ok=True)
url = "https://huggingface.co/shinfxh/reverso/resolve/main/checkpoints/reverso_small/checkpoint.pth"
urllib.request.urlretrieve(url, "/tmp/reverso/checkpoint.pth")
```

### Path B: User upload (HuggingFace not accessible)
If the download fails with a network error, tell the user:

> I can't reach HuggingFace from this environment. Please download the checkpoint from
> https://huggingface.co/shinfxh/reverso/blob/main/checkpoints/reverso_small/checkpoint.pth
> and upload it here.

Then load from `/mnt/user-data/uploads/checkpoint.pth`.

### Loading weights
```python
from load_checkpoint import load_checkpoint
weights = load_checkpoint("/tmp/reverso/checkpoint.pth")  # or upload path
```

## Model Configuration

Reverso Small uses this config (matching the published `args.json`):

```python
from reverso import ReversoConfig
config = ReversoConfig(d_model=64, module_list=["conv", "attn", "conv", "attn"])
```

## Forecasting

```python
from reverso import forecast, warmup_jit
warmup_jit()  # ~2s one-time JIT compilation

result = forecast(
    series=data,               # 1-D array/list of floats
    prediction_length=96,      # how many future steps
    weights=weights,           # dict from load_checkpoint
    config=config,
)
```

The function handles preprocessing (NaN interpolation, padding, min-max normalization) and autoregressive rollout internally.

### Key parameters

`flip_equivariant=True` — averages forward pass on original and vertically-flipped input. Slightly improves single-step predictions but can dampen amplitude over multi-step rollout. Default is `False`.

## Input Handling

Accept time series as Python list, NumPy array, CSV column, or inline values. Convert to 1-D float array before calling `forecast()`.

For CSV/DataFrame input, ask the user which column to forecast if ambiguous.

The model's context window is 2048 steps. Series shorter than 2048 are left-padded with the first value. Series longer than 2048 use only the most recent 2048 observations. Provide at least a few hundred real data points for meaningful results — heavily padded context degrades forecast quality because the long convolution kernels process mostly constant input.

## Visualization

```python
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(12, 4))
n = len(history)
ax.plot(range(n), history, label="Historical", color="#2563eb")
ax.plot(range(n, n + len(preds)), preds,
        label="Forecast", color="#dc2626", linewidth=2)
ax.axvline(x=n, color="gray", linestyle="--", alpha=0.4)
ax.set_xlabel("Time step"); ax.set_ylabel("Value")
ax.legend(); fig.tight_layout()
fig.savefig("/mnt/user-data/outputs/forecast.png", dpi=150)
```

## Performance

| Phase | Latency |
|---|---|
| numba install (uv) | ~1.6s |
| Weight loading (.pth) | <1s |
| JIT warmup | ~2s |
| Forward pass (L=2048) | ~80ms |
| 96-step forecast (2 chunks) | ~160ms |
| 192-step forecast (4 chunks) | ~320ms |

## Container Environment Limits

Each forward pass takes ~65ms at L=2048. In the ephemeral container, reject batch forecasting requests that would exceed ~1500 forward passes (~100s wall time) to avoid timeouts.

**Detect the container environment** by checking for `/mnt/user-data` or `/mnt/skills`:
```python
import os
IN_CONTAINER = os.path.exists("/mnt/user-data")
```

**Estimate cost before running** when processing multiple series:
```python
n_forwards = n_series * n_windows * max(1, pred_length // 48)
est_seconds = n_forwards * 0.065
if IN_CONTAINER and est_seconds > 100:
    # Reject or subsample
    max_series = int(1500 / (n_windows * max(1, pred_length // 48)))
```

**Practical limits at ~100s budget:**

| Scenario | Series | Windows | Pred steps | Forwards | Time |
|---|---|---|---|---|---|
| Single series, 96-step | 1 | 1 | 2 chunks | 2 | 0.1s |
| Small dataset (sz_taxi) | 156 | 6 | 48 | 936 | 61s |
| Medium dataset, short horizon | 300 | 4 | 48 | 1200 | 78s |
| Large dataset (m4_yearly) | 22974 | 1 | 48 | 22974 | **25min ✗** |

When a request exceeds the budget, inform the user with the estimated time and suggest either subsampling or running locally. For benchmark evaluation of large datasets, recommend running outside the container.

## Limitations

The model is strongest with periodic or quasi-periodic signals and full 2048-point context. Short series (under ~200 points) are heavily padded and produce degraded forecasts — this is a model limitation, not an implementation bug. Edge cases: binary-valued input (e.g. step functions normalizing to exactly 0/1) and series ending at the exact min-max boundary are out-of-distribution for the training data.

For architecture details, weight mapping, and debugging guidance, read `references/architecture.md`.
