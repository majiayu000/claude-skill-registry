---
name: pytorch-ml-training
description: PyTorch training opinions, pitfalls, and non-obvious patterns. Covers distributed training (DDP/FSDP), optimizer configuration, gradient accumulation, schedulers, and flash attention. Use when scaling training, debugging distributed setups, or making optimizer/scheduler decisions.
---

# PyTorch ML Training

## Optimizer Configuration

### AdamW Weight Decay Groups
Always separate decay vs no-decay params. Biases, LayerNorm, and embeddings should not be decayed.

```python
def configure_optimizer(model, lr=1e-4, weight_decay=0.01):
    decay, no_decay = [], []
    for name, param in model.named_parameters():
        if not param.requires_grad:
            continue
        if "bias" in name or "LayerNorm" in name or "layernorm" in name or "embedding" in name:
            no_decay.append(param)
        else:
            decay.append(param)

    return torch.optim.AdamW([
        {"params": decay, "weight_decay": weight_decay},
        {"params": no_decay, "weight_decay": 0.0},
    ], lr=lr)
```

### Layer-wise Learning Rate Decay (LLRD)
Use for fine-tuning pretrained models. Lower layers get smaller LR. Typical decay: 0.85-0.95.

```python
def get_llrd_optimizer(model, base_lr=1e-4, layer_decay=0.9, weight_decay=0.01):
    param_groups = []
    num_layers = len(list(model.children()))
    for layer_idx, (name, param) in enumerate(model.named_parameters()):
        if not param.requires_grad:
            continue
        lr = base_lr * (layer_decay ** (num_layers - layer_idx - 1))
        wd = 0.0 if "bias" in name or "norm" in name.lower() else weight_decay
        param_groups.append({"params": [param], "lr": lr, "weight_decay": wd})
    return torch.optim.AdamW(param_groups)
```

## Scheduler Opinions

| Scheduler | When to Use | Steps Per |
|-----------|-------------|-----------|
| `CosineAnnealingLR` | General fine-tuning | **Epoch** |
| `OneCycleLR` | Training from scratch, super-convergence | **Batch** |
| Warmup + Cosine | LLM fine-tuning, large models | **Batch** |

```python
# Warmup + cosine decay (most versatile)
def get_warmup_cosine_scheduler(optimizer, warmup_steps, total_steps, min_lr_ratio=0.1):
    import math
    def lr_lambda(step):
        if step < warmup_steps:
            return float(step) / float(max(1, warmup_steps))
        progress = float(step - warmup_steps) / float(max(1, total_steps - warmup_steps))
        return max(min_lr_ratio, 0.5 * (1.0 + math.cos(math.pi * progress)))
    return LambdaLR(optimizer, lr_lambda)
```

**Gotcha**: OneCycleLR steps per-batch, CosineAnnealingLR steps per-epoch. Mixing these up silently destroys training.

## Gradient Accumulation

```python
from contextlib import nullcontext

def train_with_accumulation(model, dataloader, optimizer, criterion,
                            accumulation_steps=4, device="cuda"):
    """Effective batch = batch_size * accumulation_steps * world_size"""
    model.train()
    optimizer.zero_grad(set_to_none=True)

    for step, batch in enumerate(dataloader):
        inputs = batch["input"].to(device)
        targets = batch["target"].to(device)

        loss = criterion(model(inputs), targets) / accumulation_steps
        loss.backward()

        if (step + 1) % accumulation_steps == 0:
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()
            optimizer.zero_grad(set_to_none=True)

    # Handle leftover steps
    if (step + 1) % accumulation_steps \!= 0:
        optimizer.step()
        optimizer.zero_grad(set_to_none=True)
```

### DDP + Gradient Accumulation
Must use `model.no_sync()` during accumulation steps to avoid redundant all-reduce.

```python
def train_ddp_with_accumulation(model, dataloader, optimizer, accumulation_steps):
    for step, batch in enumerate(dataloader):
        is_accumulating = (step + 1) % accumulation_steps \!= 0
        context = model.no_sync() if is_accumulating else nullcontext()

        with context:
            loss = criterion(model(batch["input"].cuda()),
                           batch["target"].cuda()) / accumulation_steps
            loss.backward()

        if not is_accumulating:
            optimizer.step()
            optimizer.zero_grad()
```

## Flash Attention

PyTorch 2.0+ uses Flash Attention automatically via `F.scaled_dot_product_attention`. Prefer this over manual attention implementations.

```python
output = F.scaled_dot_product_attention(q, k, v, is_causal=is_causal)
```

**Gotchas**:
- Requires `q, k, v` in shape `(batch, heads, seq_len, head_dim)`
- Flash backend requires `head_dim <= 256` and SM80+ (A100/H100)
- `is_causal=True` is faster than passing an explicit mask
- Dropout in SDPA only works in training mode
- Use `torch.backends.cuda.sdp_kernel()` context manager to force a specific backend for debugging

## Distributed Data Parallel (DDP)

### Setup with torchrun

```python
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.utils.data.distributed import DistributedSampler

def main():
    dist.init_process_group(backend="nccl")
    rank = dist.get_rank()
    local_rank = int(os.environ["LOCAL_RANK"])
    torch.cuda.set_device(local_rank)

    model = DDP(create_model().cuda(), device_ids=[local_rank])

    sampler = DistributedSampler(train_dataset, shuffle=True)
    train_loader = DataLoader(
        train_dataset, batch_size=batch_size,
        sampler=sampler, num_workers=4, pin_memory=True,
    )

    for epoch in range(num_epochs):
        sampler.set_epoch(epoch)  # CRITICAL: without this, data order repeats every epoch
        train_one_epoch(model, train_loader, optimizer)
        if rank == 0:
            torch.save(model.module.state_dict(), f"ckpt_{epoch}.pt")

    dist.destroy_process_group()
```

```bash
# Single node, 4 GPUs
torchrun --nproc_per_node=4 train.py

# Multi-node (2 nodes, 4 GPUs each)
torchrun --nnodes=2 --nproc_per_node=4 --node_rank=0 \
         --master_addr=node0 --master_port=12355 train.py
```

### DDP Gotchas
- `sampler.set_epoch(epoch)` mandatory -- without it, every epoch sees same order
- Access original model via `model.module` (not `model` directly)
- Only save/log on `rank == 0` to avoid file corruption and duplicate logging
- `pin_memory=True` + `non_blocking=True` on `.to(device)` for async transfers
- `NCCL_DEBUG=INFO` env var to debug communication hangs
- Unused parameters cause hangs -- use `find_unused_parameters=True` or fix the model

## Fully Sharded Data Parallel (FSDP)

Use FSDP when model does not fit in a single GPU. DDP replicates full model per GPU; FSDP shards params, grads, and optimizer states.

```python
from torch.distributed.fsdp import (
    FullyShardedDataParallel as FSDP, MixedPrecision,
    ShardingStrategy, CPUOffload, StateDictType,
)
from torch.distributed.fsdp.wrap import transformer_auto_wrap_policy
import functools

def create_fsdp_model(model):
    mp_policy = MixedPrecision(
        param_dtype=torch.bfloat16, reduce_dtype=torch.bfloat16, buffer_dtype=torch.bfloat16,
    )
    auto_wrap_policy = functools.partial(
        transformer_auto_wrap_policy,
        transformer_layer_cls={torch.nn.TransformerEncoderLayer},
    )
    return FSDP(
        model, sharding_strategy=ShardingStrategy.FULL_SHARD,
        mixed_precision=mp_policy, auto_wrap_policy=auto_wrap_policy,
        cpu_offload=CPUOffload(offload_params=False),
        device_id=torch.cuda.current_device(),
    )
```

### FSDP Sharding Strategies
| Strategy | Memory Savings | Communication | Use When |
|----------|---------------|---------------|----------|
| `FULL_SHARD` | Maximum | Highest | Model barely fits across GPUs |
| `SHARD_GRAD_OP` | Moderate | Lower | Model fits but optimizer doesn't |
| `NO_SHARD` | None (like DDP) | Lowest | Debugging FSDP issues |
| `HYBRID_SHARD` | Per-node full, cross-node shard | Balanced | Multi-node with fast intra-node |

### FSDP Checkpointing
Use `SHARDED_STATE_DICT` during training (memory-efficient, fast). Use `FULL_STATE_DICT` only for final export to single-GPU inference.

```python
def save_fsdp_checkpoint(model, optimizer, path):
    with FSDP.state_dict_type(model, StateDictType.SHARDED_STATE_DICT):
        state = {"model": model.state_dict(),
                 "optim": FSDP.optim_state_dict(model, optimizer)}
        torch.distributed.checkpoint.save_state_dict(state, checkpoint_id=path)
```

### FSDP Gotchas
- `auto_wrap_policy` must match your model's layer class -- wrong wrapping = OOM or no sharding
- `cpu_offload=True` saves GPU memory but 5-10x slower; only use if desperate
- `FULL_STATE_DICT` gathers entire model to rank 0 -- can OOM on large models
- Mixed precision: use `bfloat16` on Ampere+; `float16` needs GradScaler (more fragile)

## Key Pitfalls Checklist

### Training Correctness
- [ ] `model.train()` before training, `model.eval()` before eval (affects dropout, batchnorm)
- [ ] `optimizer.zero_grad(set_to_none=True)` -- more memory-efficient than default
- [ ] Loss divided by `accumulation_steps` when using gradient accumulation
- [ ] Handle leftover steps at end of accumulation loop
- [ ] `torch.no_grad()` AND `model.eval()` during validation (not just one -- both)

### Memory Leaks
- [ ] `.detach()` tensors before appending to lists (otherwise retains entire graph)
- [ ] `.item()` for scalar logging (don't store full tensors for metrics)
- [ ] Delete intermediate tensors and `torch.cuda.empty_cache()` if OOM during eval

### Distributed Training
- [ ] `sampler.set_epoch(epoch)` every epoch in DDP
- [ ] `model.no_sync()` during gradient accumulation steps
- [ ] Save checkpoints on `rank == 0` only
- [ ] Use `model.module` to access underlying model in DDP
- [ ] `find_unused_parameters=True` if model has conditional branches
- [ ] Set `NCCL_ASYNC_ERROR_HANDLING=1` for better error messages

### Numeric Stability
- [ ] Gradient clipping before optimizer step (`clip_grad_norm_` typical max: 1.0)
- [ ] `bfloat16` over `float16` when hardware supports it (no loss scaling needed)
- [ ] Watch for NaN in loss -- often caused by LR too high or data issues
- [ ] `torch.compile` can change numerics slightly -- validate against eager mode

### Performance
- [ ] `pin_memory=True` in DataLoader for GPU training
- [ ] `non_blocking=True` on `.to(device)` calls with pinned memory
- [ ] `num_workers > 0` in DataLoader (typically 4-8 per GPU)
- [ ] `persistent_workers=True` to avoid re-forking every epoch
- [ ] `torch.compile(model)` for free 10-30% speedup on PyTorch 2.x
- [ ] `torch.set_float32_matmul_precision('medium')` on Ampere+ for TF32
