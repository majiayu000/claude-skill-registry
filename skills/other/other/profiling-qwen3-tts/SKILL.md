---
name: profiling-qwen3-tts
description: Profile and benchmark qwen3-tts-rs inference using e2e_bench with chrome tracing, flamegraph, or Nsight Systems inside a CUDA Docker container. Use when profiling, benchmarking, checking performance, finding bottlenecks, or running flamegraphs.
---

# qwen3-tts-rs Profiling & Benchmarking

Run performance profiling and benchmarks for the qwen3-tts Rust TTS engine.

## Prerequisites

- Docker with `--gpus all` support
- `qwen3-tts:latest` Docker image (has Rust toolchain + CUDA)
- Model weights in `test_data/models/` (1.7B-CustomVoice is the default)
- `tokenizer.json` must be in the model directory

## Docker Execution Pattern

The CUDA toolchain lives inside the Docker container. All cargo commands must
run there. The workspace is bind-mounted at `/workspace`:

```bash
docker run --rm --gpus all --entrypoint /bin/bash \
  -v "$(pwd):/workspace" -w /workspace \
  qwen3-tts:latest \
  -c 'export PATH=/root/.rustup/toolchains/stable-aarch64-unknown-linux-gnu/bin:$PATH && <COMMAND>'
```

## Profiling Modes

### 1. Chrome Trace (default — best for span hierarchy)

Produces `trace.json` for viewing in `chrome://tracing` or <https://ui.perfetto.dev>.

```bash
docker run --rm --gpus all --entrypoint /bin/bash \
  -v "$(pwd):/workspace" -w /workspace \
  qwen3-tts:latest \
  -c 'export PATH=/root/.rustup/toolchains/stable-aarch64-unknown-linux-gnu/bin:$PATH && \
      cargo run --profile=profiling --features=profiling,cuda,cli --bin e2e_bench -- \
        --model-dir test_data/models/1.7B-CustomVoice --iterations 1 --warmup 1'
```

Output: `trace.json` (~12MB for 3 sentences). Contains spans:

- `generate_frames` — full generation loop
- `code_predictor` / `code_predictor_inner` — per-frame acoustic code generation
- `talker_step` — per-frame transformer forward pass
- `sampling` / `top_k` / `top_p` — per-frame token sampling
- `gpu_sync` trace events — marks every `to_vec1()` GPU→CPU sync

### 2. Per-Stage Timing (no profiling feature needed)

The e2e_bench binary reports stage breakdowns (prefill / generation / decode)
even without the `profiling` feature:

```bash
docker run --rm --gpus all --entrypoint /bin/bash \
  -v "$(pwd):/workspace" -w /workspace \
  qwen3-tts:latest \
  -c 'export PATH=/root/.rustup/toolchains/stable-aarch64-unknown-linux-gnu/bin:$PATH && \
      cargo run --release --features=cuda,cli --bin e2e_bench -- \
        --model-dir test_data/models/1.7B-CustomVoice --iterations 3 --warmup 1'
```

### 3. Streaming TTFA (Time to First Audio)

```bash
# Add --streaming flag
... --bin e2e_bench -- --model-dir test_data/models/1.7B-CustomVoice \
    --iterations 3 --warmup 1 --streaming
```

### 4. JSON Output

```bash
... --bin e2e_bench -- --model-dir test_data/models/1.7B-CustomVoice \
    --json-output results.json --iterations 3
```

## GPU Sync Audit

List all `to_vec1()` GPU→CPU synchronization points:

```bash
bash scripts/audit-gpu-syncs.sh
```

## Interpreting Results

### Stage Breakdown Table

```text
Label  Words  Wall (ms)  Audio (s)  RTF    Tok/s  Mem (MB)  Prefill     Generate      Decode
short     13    5235.2      3.68   1.423    8.8      858   21ms (1%)  2724ms (71%)  1109ms (29%)
medium    53   23786.3     34.00   0.700   17.9      859   20ms (0%)  22694ms (95%)  1057ms (4%)
long     115   43797.4     60.96   0.718   17.4      864   19ms (0%)  41861ms (96%)  1886ms (4%)
```

Key metrics:

- **RTF < 1.0** = faster than real-time
- **Prefill**: Should be <50ms on GPU. If high, check embedding/attention.
- **Generation**: Dominates. ~18 GPU→CPU syncs per frame (16 code_predictor + 2 sampling).
- **Decode**: ConvNeXt decoder. Scales with frame count. ~4% for long text.
- **Tok/s**: Semantic tokens per second. Higher = better.

### Chrome Trace Analysis

In Perfetto/chrome://tracing:

1. Look for gaps between `talker_step` and `code_predictor` — that's CPU overhead
2. Check if `sampling` (top_k + top_p) is significant vs model forward passes
3. The `gpu_sync` events mark where GPU stalls waiting for CPU

### Optimization Targets

The ~18 `to_vec1()` calls per frame are the main bottleneck:

- 16 in code_predictor (argmax per acoustic code group)
- 2 in sampling (read sampled token)

Batch these to reduce GPU→CPU round-trips.

## Model Variants

| Model            | Dir                                 | Notes                           |
| ---------------- | ----------------------------------- | ------------------------------- |
| 1.7B-CustomVoice | `test_data/models/1.7B-CustomVoice` | Default benchmark target        |
| 1.7B-Base        | `test_data/models/1.7B-Base`        | Voice cloning (needs ref audio) |
| 1.7B-VoiceDesign | `test_data/models/1.7B-VoiceDesign` | Text-described voices           |

## Reference Baseline (1.7B-CustomVoice, CUDA)

From January 2025 on DGX (A100):

- Short (13 words): RTF 1.42, 8.8 tok/s
- Medium (53 words): RTF 0.70, 17.9 tok/s
- Long (115 words): RTF 0.72, 17.4 tok/s
- Prefill: ~20ms, Decode: ~1-2s, Generation: 71-96%
