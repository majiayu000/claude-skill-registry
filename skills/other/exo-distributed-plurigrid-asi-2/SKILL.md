---
name: exo-distributed
description: "Distributed LLM inference across Apple Silicon clusters with exo. Run models across Mac Studios via Thunderbolt RDMA, auto peer discovery, and MLX sharding. Use for multi-device inference, model parallelism, or building LLM clusters."
trit: 0
---

# exo-distributed Skill

> *"Run models across heterogeneous devices by forming GPU clusters with zero configuration."*

**Trit**: 0 (ERGODIC - coordination/orchestration)
**Color**: Neutral (60-180° hues)
**Source**: Random walk fusion over DuckLake interactions + DeepWiki exo-explore/exo

## Overview

[exo](https://github.com/exo-explore/exo) enables distributed LLM inference across multiple Apple Silicon devices:
- **Auto Peer Discovery**: Devices find each other automatically
- **RDMA over Thunderbolt 5**: Low-latency direct memory access
- **MLX Backend**: Native Apple Silicon acceleration via mlx.distributed
- **Pipeline + Tensor Parallelism**: Shard models across devices

## Quick Start

```bash
# Install exo
pip install exo-explore

# Start on first device (becomes master if elected)
exo

# Start on additional devices (auto-discovers peers)
exo

# Devices automatically form a cluster and expose OpenAI-compatible API
# Default: http://localhost:8080
```

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         EXO CLUSTER                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────┐  Thunderbolt 5  ┌────────────┐                  │
│  │ Mac Studio │◄───── RDMA ────►│ Mac Studio │                  │
│  │   M4 Max   │                 │   M4 Max   │                  │
│  │ Layers 0-15│                 │Layers 16-31│                  │
│  └──────┬─────┘                 └──────┬─────┘                  │
│         │                              │                         │
│         └──────────────┬───────────────┘                         │
│                        │                                         │
│                   ┌────▼────┐                                    │
│                   │ Master  │                                    │
│                   │ (Elected)│                                   │
│                   └────┬────┘                                    │
│                        │                                         │
│              ┌─────────▼─────────┐                               │
│              │ REST API :8080    │                               │
│              │ OpenAI Compatible │                               │
│              └───────────────────┘                               │
└─────────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Peer Discovery (Gossipsub/libp2p)

```python
# Automatic discovery via mDNS/UDP broadcast
# Builds Topology graph of connected nodes
# No manual configuration required

# View discovered peers
exo --list-peers
```

### 2. MLX Backend

```python
from exo.worker.engines.mlx.utils_mlx import mlx_distributed_init

# Initializes mlx.distributed group
# Backends:
#   - MlxRing: TCP/IP (fallback)
#   - MlxJaccl: RDMA over Thunderbolt (preferred)

mlx_distributed_init(
    rank=0,           # This device's rank
    world_size=4,     # Total devices
    backend="jaccl"   # RDMA backend
)
```

### 3. Shard Distribution

```python
from exo.master.placement import place_instance

# Determines model sharding across devices
# Filters by available memory
# Prioritizes Thunderbolt cycles

shard_assignments = place_instance(
    model="llama-3.3-70b",
    topology=discovered_topology,
    strategy="pipeline"  # or "tensor"
)
```

### 4. RDMA over Thunderbolt 5

```python
# IBV device matrix: N×N connectivity
# matrix[i][j] = interface on device i connecting to device j

# Environment variables for Jaccl backend:
# MLX_IBV_DEVICES=<matrix>
# MLX_RANK=<rank>
# MLX_IBV_COORDINATOR=<coordinator_addr>
# MLX_METAL_FAST_SYNCH=1
```

## Sharding Strategies

### Pipeline Parallelism

```
Device 0: Layers  0-15  →  embeddings + early layers
Device 1: Layers 16-31  →  middle layers
Device 2: Layers 32-47  →  late layers
Device 3: Layers 48-63  →  final layers + head

Data flows: D0 → D1 → D2 → D3 → output
```

```python
from exo.master.placement import get_shard_assignments_for_pipeline_parallel

# Inserts PipelineFirstLayer and PipelineLastLayer
# for inter-device communication
assignments = get_shard_assignments_for_pipeline_parallel(
    model="llama-3.3-70b",
    num_devices=4
)
```

### Tensor Parallelism

```
All devices: All layers (replicated)
But: Attention heads partitioned across devices
     MLP tensors partitioned across devices

Each device computes partial results → all-reduce → combined output
```

```python
from exo.master.placement import get_shard_assignments_for_tensor_parallel

# Specific sharding for:
#   - LlamaModel
#   - DeepseekV3Model
#   - Qwen3MoeModel
assignments = get_shard_assignments_for_tensor_parallel(
    model="deepseek-r1",
    num_devices=4
)
```

## Supported Models

| Model | Size | Min Devices | Strategy |
|-------|------|-------------|----------|
| Llama 3.3 | 70B | 2 × M4 Max | Pipeline |
| DeepSeek R1 | 671B | 8+ × M4 Max | Tensor |
| Qwen 2.5 | 72B | 2 × M4 Max | Pipeline |
| Mixtral 8×22B | 141B | 4 × M4 Max | Tensor |
| Llama 3.1 | 405B | 8+ × M4 Max | Tensor |

## API Usage

### OpenAI-Compatible Endpoint

```python
import openai

client = openai.OpenAI(
    base_url="http://localhost:8080/v1",
    api_key="not-needed"  # exo doesn't require API key
)

response = client.chat.completions.create(
    model="llama-3.3-70b",
    messages=[{"role": "user", "content": "Hello!"}],
    stream=True
)

for chunk in response:
    print(chunk.choices[0].delta.content, end="")
```

### Direct API

```bash
curl http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama-3.3-70b",
    "messages": [{"role": "user", "content": "Hello"}],
    "stream": true
  }'
```

## Hardware Setup

### Thunderbolt Cluster (Recommended)

```
Mac Studio 1 ──TB5──► Mac Studio 2
     │                     │
     TB5                  TB5
     │                     │
     ▼                     ▼
Mac Studio 3 ──TB5──► Mac Studio 4
```

- Use Thunderbolt 5 cables (120 Gbps bidirectional)
- All-to-all connectivity required for RDMA
- RDMA gives ~10× lower latency than TCP/IP

### Network Cluster (Fallback)

```bash
# TCP/IP via MlxRing backend
# Works but higher latency
exo --backend ring
```

## GF(3) Triadic Integration

```
exo-distributed (0) ⊗ mlx-apple-silicon (+1) ⊗ bisimulation-game (-1) = 0 ✓
exo-distributed (0) ⊗ parallel-fanout (+1) ⊗ sheaf-cohomology (-1) = 0 ✓
exo-distributed (0) ⊗ gay-mcp (+1) ⊗ temporal-coalgebra (-1) = 0 ✓
```

### Trifurcated Inference Pattern

```clojure
;; Distribute inference across 3 device groups
(defn trifurcated-inference [prompt]
  (let [minus  (future (exo-infer :validator prompt))   ; -1: Check safety
        ergodic (future (exo-infer :main prompt))       ;  0: Main inference
        plus   (future (exo-infer :speculative prompt))] ; +1: Speculative draft
    ;; GF(3) sum: -1 + 0 + 1 = 0 ✓
    {:validated @minus
     :response @ergodic
     :speculative @plus}))
```

## Derivational Chaining (from Bumpus/DuckLake)

Each inference step derives from previous via seed chaining:

```python
# Seed derivation for deterministic distributed inference
GOLDEN = 0x9E3779B97F4A7C15

def derive_shard_seed(base_seed: int, shard_id: int, step: int) -> int:
    """Deterministic seed for each shard at each step"""
    z = (base_seed + GOLDEN * shard_id + step) & 0xFFFFFFFFFFFFFFFF
    z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & 0xFFFFFFFFFFFFFFFF
    z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & 0xFFFFFFFFFFFFFFFF
    return z ^ (z >> 31)

# Each device uses its shard_seed for sampling reproducibility
```

## Commands

```bash
# Start exo node
exo

# List discovered peers
exo --list-peers

# Specify backend
exo --backend jaccl    # RDMA (default if available)
exo --backend ring     # TCP/IP fallback

# Run specific model
exo --model llama-3.3-70b

# Set API port
exo --port 8080

# Benchmark
exo bench --config bench_simple.yaml
```

## Monitoring

### Dashboard

```bash
# Web dashboard at http://localhost:8080/dashboard
# Shows:
#   - Connected peers
#   - Model shards
#   - Inference throughput
#   - Memory usage per device
```

### DuckLake Integration

```sql
-- Track exo inference events in DuckLake
CREATE TABLE exo_inferences (
  id INTEGER PRIMARY KEY,
  timestamp TIMESTAMP,
  model VARCHAR,
  prompt_tokens INTEGER,
  completion_tokens INTEGER,
  latency_ms FLOAT,
  devices INTEGER,
  strategy VARCHAR,
  trit INTEGER,
  seed BIGINT
);

-- Query inference history
SELECT model, AVG(latency_ms) as avg_latency, COUNT(*) as count
FROM exo_inferences
GROUP BY model
ORDER BY avg_latency;
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Peers not discovered | Check firewall, ensure same network |
| RDMA not working | Verify Thunderbolt cables, check `ibv_devices` |
| OOM on device | Reduce batch size or use more devices |
| Slow inference | Switch from `ring` to `jaccl` backend |
| Model not loading | Check `~/.cache/huggingface` for space |

## References

- [exo-explore/exo](https://github.com/exo-explore/exo) (GitHub)
- [DeepWiki exo documentation](https://deepwiki.com/exo-explore/exo)
- [MLX Distributed](https://github.com/ml-explore/mlx)
- [Jaccl RDMA Backend](https://github.com/ml-explore/mlx/tree/main/mlx/distributed)

---

**Skill Name**: exo-distributed
**Type**: Distributed LLM Inference / Cluster Orchestration
**Trit**: 0 (ERGODIC - coordination)
**GF(3)**: Coordinates multi-device inference with balanced sharding
**Platform**: Apple Silicon clusters (macOS)
**Discovery**: Random walk fusion over DuckLake + DeepWiki exo-explore/exo
