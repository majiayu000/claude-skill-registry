---
name: "training-check"
description: "Periodically check WandB metrics during training to catch problems early (NaN, loss divergence, idle GPUs). Avoid wasting GPU hours on broken runs. Use when training is running and you want automated quality checks."
---

# Training Check

Periodically read WandB metrics during training to catch problems early. Do not wait until training finishes to discover it was a waste of GPU time.

## Context: $ARGUMENTS

## Constants

- WANDB entity/project/run_id: read from `AGENTS.md`, project notes, or pass explicitly as `entity/project/run_id`
- CHECK_INTERVAL: starts at 10 minutes, then gradually increases if consistently healthy: 10 min -> 20 min -> 30 min -> 60 min
- REVIEWER_MODEL = `gpt-5.4` — used via a secondary Codex agent for ambiguous cases only

## When to Use

- After training is confirmed running
- During long experiments where early detection matters
- When you need training quality checks, not just process-health checks

## Workflow

### Step 1: Read WandB Metrics

```python
import wandb
api = wandb.Api()
run = api.run("<entity>/<project>/<run_id>")
history = run.history()
```

If WandB is unreachable, fall back to reading the training log directly via SSH:

```bash
ssh server "tail -100 /path/to/training.log"
```

Check these signals:

- **Loss trend**: is training loss decreasing over the last N steps?
- **Eval metrics**: are evaluation metrics improving or at least not clearly degrading?
- **NaN / Inf**: any NaN or Inf values in loss or gradients?
- **Spikes**: sudden large jumps in loss (>10x normal variance)?
- **Learning rate**: is the schedule behaving as expected?
- **Gradient norm**: exploding or vanishing?

### Step 2: Judgment

| Signal | Judgment | Action |
|--------|----------|--------|
| NaN/Inf in loss | **Clearly bad** | Stop training, investigate |
| Loss diverging (increasing for >N steps) | **Clearly bad** | Stop training, investigate |
| Eval metrics significantly worse than baseline | **Clearly bad** | Stop training, investigate |
| Loss decreasing, metrics improving | **Clearly fine** | Continue, increase check interval |
| Loss flat but not diverging | **Unsure** | -> Step 3 |
| Metrics noisy, can't tell trend | **Unsure** | -> Step 3 |
| Slightly worse than baseline but still early | **Unsure** | -> Step 3 |

### Step 3: Secondary Review (only when unsure)

Only escalate to a secondary Codex reviewer when the signal is ambiguous. For clearly good or clearly bad signals, act directly.

```text
spawn_agent:
  model: gpt-5.4
  reasoning_effort: high
  message: |
    TRAINING HEALTH CHECK — need your judgment on ambiguous metrics.

    Run: <entity>/<project>/<run_id>
    Current epoch/step: X / Y total
    Training loss (last 10 checkpoints): [values]
    Eval metrics (last 3 evals): [values]
    Baseline reference: [numbers from paper/reproduction]

    What I'm unsure about: [specific concern]

    Please respond with exactly one of:
    - STOP: clearly problematic, should kill training
    - CONTINUE: looks fine, check again next interval
    - WAIT: not enough data to judge, check again sooner
```

### Step 4: Act

| Decision | Action |
|----------|--------|
| **STOP** | Kill the training session. Save the WandB run URL, key metrics, and reason for stopping. Log to project notes for debugging. |
| **CONTINUE** | Do nothing. The next check can use a longer interval if the run remains healthy. |
| **WAIT** | Do nothing, but keep the current short interval. |

## Integration with Watchdog

Training-check and `tools/watchdog.py` operate at different levels:

| Layer | Tool | What it checks | Frequency |
|-------|------|----------------|-----------|
| Process health | `watchdog.py` | Session alive? GPU active? | Every 60s |
| Training quality | `training-check` | Loss trend? Metrics improving? | Every 10-60 min |

Use both together:

- Watchdog catches crashes and idle GPUs immediately
- Training-check catches quality issues like NaN, plateaus, or metric degradation

## Periodic Invocation Guidance

- Initial cadence: every 10 minutes
- If the run stays healthy: lengthen to 20, then 30, then 60 minutes
- If any anomaly appears: reset to 10 minutes
- If your environment has cron / CI / scheduler support, use it
- Otherwise, record the next suggested check time and rerun manually

## Rules

- Do not stop training on the first sign of noise. Judge trends over multiple checkpoints.
- When stopping training, always save the WandB run URL and key metrics as evidence.
- If both WandB and log files are unreachable, report the connectivity issue and try again later. Do not assume training is broken.
- Gradually increase the check interval only when the run stays healthy.
