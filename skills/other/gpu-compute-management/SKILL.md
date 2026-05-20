---
name: gpu-compute-management
description: GPU provisioning across clouds, CUDA debugging, multi-GPU coordination, spot instance strategies, and cost-aware selection.
---

# GPU Compute Management

## GPU Selection by Workload

| Workload | GPU | VRAM | $/hr (spot) | When to Use |
|----------|-----|------|------------|-------------|
| LLM fine-tuning (7B) | A100 40GB | 40GB | ~$1.10 | QLoRA, full fine-tune fits in 40GB |
| LLM fine-tuning (70B) | A100 80GB x4 | 320GB | ~$5.00 | FSDP/DeepSpeed across 4 GPUs |
| LLM inference (7B) | L4 | 24GB | ~$0.25 | Best cost/perf for small model serving |
| LLM inference (70B) | H100 x2 | 160GB | ~$4.00 | Tensor parallelism across 2 GPUs |
| Batch embedding | T4 | 16GB | ~$0.12 | Cheapest option for throughput work |
| Training CV models | A10G | 24GB | ~$0.50 | Good for ResNet/ViT scale models |
| Research / max perf | H100 SXM | 80GB | ~$2.50 | NVLink, highest memory bandwidth |

## CUDA Device Management

### Basic Device Setup

```python
import torch

def setup_device(gpu_id: int = 0) -> torch.device:
    """Configure CUDA device with validation."""
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA not available. Check driver installation.")

    device_count = torch.cuda.device_count()
    if gpu_id >= device_count:
        raise RuntimeError(f"GPU {gpu_id} requested but only {device_count} available")

    device = torch.device(f"cuda:{gpu_id}")
    torch.cuda.set_device(device)

    # Log device info
    props = torch.cuda.get_device_properties(device)
    print(f"Using {props.name} ({props.total_mem / 1e9:.1f}GB)")
    return device
```

### Multi-GPU Launch Script

```bash
#\!/bin/bash
# launch_distributed.sh -- torchrun wrapper with defaults

NUM_GPUS=${1:-$(nvidia-smi -L | wc -l)}
MASTER_PORT=${MASTER_PORT:-29500}

torchrun \
    --nproc_per_node=$NUM_GPUS \
    --master_port=$MASTER_PORT \
    --rdzv_backend=c10d \
    train.py \
    --batch_size=$((32 * NUM_GPUS)) \
    --learning_rate=0.0001
```

### Multi-Node Launch (SLURM)

```bash
#\!/bin/bash
#SBATCH --job-name=train
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=1
#SBATCH --gpus-per-node=8
#SBATCH --cpus-per-task=96
#SBATCH --mem=0
#SBATCH --time=24:00:00

export MASTER_ADDR=$(scontrol show hostnames $SLURM_JOB_NODELIST | head -n 1)
export MASTER_PORT=29500

srun torchrun \
    --nnodes=$SLURM_NNODES \
    --nproc_per_node=8 \
    --rdzv_id=$SLURM_JOB_ID \
    --rdzv_backend=c10d \
    --rdzv_endpoint=$MASTER_ADDR:$MASTER_PORT \
    train.py
```

## Spot Instance Checkpointing

Spot/preemptible instances can be reclaimed with ~30s-2min warning. Save state aggressively.

```python
import signal
import torch
from pathlib import Path

class SpotCheckpointer:
    """Handles graceful checkpoint on spot termination."""

    def __init__(self, checkpoint_dir: str = "/mnt/checkpoints"):
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        self._interrupted = False
        signal.signal(signal.SIGTERM, self._handler)

    def _handler(self, signum, frame):
        print("SIGTERM received -- saving emergency checkpoint")
        self._interrupted = True

    @property
    def should_stop(self) -> bool:
        return self._interrupted

    def save(self, model, optimizer, epoch: int, step: int):
        path = self.checkpoint_dir / f"ckpt_e{epoch}_s{step}.pt"
        torch.save({
            "model_state": model.state_dict(),
            "optimizer_state": optimizer.state_dict(),
            "epoch": epoch,
            "step": step,
        }, path)
        # Keep symlink to latest
        latest = self.checkpoint_dir / "latest.pt"
        latest.unlink(missing_ok=True)
        latest.symlink_to(path.name)

    def load_latest(self, model, optimizer):
        latest = self.checkpoint_dir / "latest.pt"
        if not latest.exists():
            return 0, 0
        ckpt = torch.load(latest, map_location="cpu")
        model.load_state_dict(ckpt["model_state"])
        optimizer.load_state_dict(ckpt["optimizer_state"])
        return ckpt["epoch"], ckpt["step"]
```

### AWS Spot Termination Detection

```bash
#\!/bin/bash
# Poll EC2 metadata for spot termination notice
while true; do
    RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" \
        http://169.254.169.254/latest/meta-data/spot/instance-action)
    if [ "$RESPONSE" -eq 200 ]; then
        echo "Spot termination notice received\!"
        kill -SIGTERM $(pgrep -f train.py)
        break
    fi
    sleep 5
done
```

## nvidia-smi Monitoring

```bash
# Continuous monitoring (every 1s) -- GPU util, memory, temp
nvidia-smi dmon -s pucm -d 1

# JSON output for programmatic use
nvidia-smi --query-gpu=index,name,utilization.gpu,memory.used,memory.total,temperature.gpu \
    --format=csv,noheader,nounits

# Watch for thermal throttling
watch -n 2 "nvidia-smi --query-gpu=clocks_throttle_reasons.active \
    --format=csv,noheader"
```

## Gotchas and Anti-Patterns

### NCCL Timeout on Spot

**Problem**: One node gets preempted mid-allreduce. Remaining nodes hang for 30 min (default NCCL timeout).

**Fix**:
```python
import datetime
import torch.distributed

torch.distributed.init_process_group(
    backend="nccl",
    timeout=datetime.timedelta(minutes=5),  # Fail fast
)
```

### CUDA OOM Debugging

Typical error: `CUDA out of memory. Tried to allocate X MiB`.

Steps:
1. Check actual usage: `torch.cuda.memory_summary()` or `torch.cuda.max_memory_allocated()`
2. Look for gradient accumulation leaks -- ensure `loss.backward()` is followed by `optimizer.zero_grad()`
3. Use `torch.cuda.empty_cache()` after validation loops
4. Enable gradient checkpointing for transformer models:
   ```python
   model.gradient_checkpointing_enable()
   ```

### GPU Memory Fragmentation

**Problem**: `nvidia-smi` shows 10GB free but PyTorch cannot allocate a 2GB contiguous block.

**Fix**: Set `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True` (PyTorch 2.1+). For older versions:
```python
import os
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:512"
```

### Driver Version Mismatches

Always verify the full stack:
```bash
# Host driver version
nvidia-smi | head -3

# CUDA toolkit version in container
nvcc --version

# PyTorch CUDA version
python -c "import torch; print(torch.version.cuda)"
```

All three must be compatible. PyTorch ships its own CUDA runtime, so `torch.version.cuda` must match or be older than the driver max supported version.
