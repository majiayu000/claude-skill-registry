---
name: domain-advisor
description: >
  Plan experiments or development tasks using past knowledge. Adapts behavior
  based on project domain (research, unsloth, cuda) by reading registry.json.
  Triggers on <advise> or questions like "What should we try next?"
metadata:
  short-description: "Plan next steps using past knowledge"
  tags:
    - planning
    - experiments
    - advice
---

# Skill: domain-advisor

## When to use

Use this skill when:
- The user message starts with `<advise>`, or
- The user asks "What should we try next?" or similar planning questions.

## Initialization

1. Read `.codex/skills/registry.json` to determine:
   - `domain`: research | unsloth | cuda
   - `paths.reports`: where to find experiment/benchmark reports
   - `paths.experiment_log`: path to experiment log
   - `paths.troubleshooting`: path to troubleshooting guide

2. Adapt behavior based on domain (see Domain-Specific Behavior below).

## Inputs

- User goal (including constraints like run budget, hardware, time).
- Optional references to files (configs, reports, logs) mentioned in the goal.

## Behavior

1. **Understand the goal**
   - Parse the research/development goal and constraints.
   - If unclear, ask a concise clarifying question.

2. **Gather context**
   - Scan `.codex/skills/` for **relevant result skills** matching the task.
   - Read relevant reports from the `paths.reports` directory.
   - Skim recent entries in `paths.experiment_log`.
   - If errors are mentioned, check `paths.troubleshooting` for known patterns.

3. **Propose a plan**
   - Design **2–5 concrete experiments/tasks**, each with:
     - Clear objective
     - Key configuration/parameters
     - Expected outcome or hypothesis
     - Any relevant variation to test
   - Respect constraints (budget, hardware, time).
   - **Reuse defaults** from existing skills instead of inventing new ones.

4. **Output format**
   - Start with a short natural-language summary.
   - Provide a markdown table:

     | id | description | key_differences | notes |
     |----|-------------|-----------------|-------|

   - Optionally propose file paths for configs or reports to create.
   - If errors were mentioned, explain how this plan avoids known failure patterns.

5. **Logging**
   - When useful, append a short entry to `paths.experiment_log` summarizing
     the proposed plan (only with user approval).

---

## Domain-Specific Behavior

### Research Domain

When `domain: research`:

**Focus areas:**
- Hyperparameter sweeps (learning rate, batch size, epochs)
- Model architecture variations (layers, dimensions, attention heads)
- Dataset mixtures and sampling strategies
- Training dynamics (warmup, schedulers, checkpointing)

**Context to gather:**
- `training_reports/*.md` - past training runs
- Model configs and their performance
- Loss curves and convergence patterns

**Output emphasis:**
- Parameter sweep tables with specific values
- Ablation study designs
- Baseline comparisons

### Unsloth Domain

When `domain: unsloth`:

**Focus areas:**
- LoRA rank and alpha selection
- Quantization settings (4-bit, 8-bit, nf4)
- Gradient checkpointing configuration
- Fine-tuning hyperparameters for specific model families
- Memory optimization strategies

**Context to gather:**
- `training_reports/*.md` - past fine-tuning runs
- Model-specific Unsloth configurations
- Memory usage patterns

**Output emphasis:**
- LoRA configuration recommendations
- Memory/speed tradeoffs
- Model-specific settings (Llama, Mistral, Qwen, etc.)

### CUDA Domain

When `domain: cuda`:

**Focus areas:**
- Tiling strategies and block sizes
- Shared memory usage patterns
- Warp-level primitives
- Memory coalescing optimization
- Triton autotuning configurations

**Context to gather:**
- `benchmark_results/*.md` - past kernel benchmarks
- Profiling data (nsight, ncu reports)
- Bandwidth and occupancy metrics

**Output emphasis:**
- Kernel configuration parameters
- Expected speedup estimates
- Memory access pattern recommendations
- Profiling metrics to track

---

## Example Output

### Research Example

```markdown
## Experiment Plan: Attention Head Ablation

Based on previous runs in `training_reports/baseline-2025-01.md`, the 8-head
configuration achieved 92% accuracy. Testing whether fewer heads can match
this with lower compute.

| id | description | key_differences | notes |
|----|-------------|-----------------|-------|
| A1 | 4-head attention | heads=4 vs baseline 8 | Test if 4 heads sufficient |
| A2 | 6-head attention | heads=6 | Middle ground |
| A3 | 4-head + wider FFN | heads=4, ffn_dim=4096 | Compensate with FFN |

All runs use: lr=1e-4, batch_size=32, epochs=10 (from baseline config).
```

### Unsloth Example

```markdown
## Fine-tuning Plan: Llama-3 8B with Unsloth

Based on `training_reports/llama3-lora-v1.md`, rank=16 showed good results
but OOM'd at batch_size=4. Testing memory-efficient configurations.

| id | description | key_differences | notes |
|----|-------------|-----------------|-------|
| U1 | rank=8 + grad_ckpt | Lower rank, enable checkpointing | Memory baseline |
| U2 | rank=16 + 4bit | Full rank with 4-bit quantization | Quality vs memory |
| U3 | rank=32 + offload | Higher rank with CPU offload | Max quality attempt |

All runs use: alpha=32, dropout=0.05, target_modules=["q_proj", "v_proj"]
```

### CUDA Example

```markdown
## Kernel Optimization Plan: Softmax

Based on `benchmark_results/softmax-v1.md`, current implementation achieves
80% of theoretical bandwidth. Testing tiling strategies.

| id | description | key_differences | notes |
|----|-------------|-----------------|-------|
| K1 | 2D tiling | BLOCK_M=64, BLOCK_N=64 | Better L2 reuse |
| K2 | Warp reduction | Use warp shuffles | Reduce shared mem |
| K3 | Online softmax | Single-pass algorithm | Fused with attention |

Profile with: `ncu --set full` to capture memory metrics.
```
