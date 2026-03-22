---
name: hugging-face-jobs
description: "This skill should be used when users want to run any workload on Hugging Face Jobs infrastructure. Covers UV scripts, Docker-based jobs, hardware selection, cost estimation, authentication with tokens, scheduled jobs, and result persistence."
---

# Running Workloads on Hugging Face Jobs

## Overview

Run any workload on fully managed Hugging Face infrastructure. No local setup required — jobs run on cloud CPUs, GPUs, or TPUs and can persist results to the Hub.

**Common use cases:** Data Processing, Batch Inference, Experiments & Benchmarks, Model Training (see `model-trainer` skill for TRL-specific), Synthetic Data Generation, Development & Testing, Scheduled Jobs.

## When to Use This Skill

- Run Python workloads on cloud infrastructure
- Execute jobs without local GPU/TPU setup
- Process data at scale or run batch inference
- Schedule recurring tasks
- Persist results to the Hugging Face Hub

## Key Directives

1. **Always use `hf_jobs()` MCP tool** — `hf_jobs("uv", {...})` or `hf_jobs("run", {...})`. Pass script content as a string; do NOT save to local files unless asked.
2. **Always handle authentication** — Hub operations require `HF_TOKEN` via secrets. See `references/token_usage.md`.
3. **Provide job details after submission** — job ID, monitoring URL, estimated time.
4. **Set appropriate timeouts** — default 30 min may be insufficient.

## Prerequisites

- HF Account with [Pro](https://hf.co/pro), [Team](https://hf.co/enterprise), or [Enterprise](https://hf.co/enterprise) plan
- Authenticated: verify with `hf_whoami()`
- For Hub operations: `secrets={"HF_TOKEN": "$HF_TOKEN"}` (never hardcode tokens)

> Full token guide: `references/token_usage.md`

---

## Quick Start

### Approach 1: UV Scripts (Recommended)

UV scripts use PEP 723 inline dependencies for clean, self-contained workloads.

```python
hf_jobs("uv", {
    "script": """
# /// script
# dependencies = ["transformers", "torch"]
# ///
from transformers import pipeline
result = pipeline("sentiment-analysis")("I love Hugging Face!")
print(result)
""",
    "flavor": "cpu-basic",
    "timeout": "30m"
})
```

**CLI:** `hf jobs uv run my_script.py --flavor cpu-basic --timeout 30m`
**Python API:** `run_uv_job("my_script.py", flavor="cpu-basic", timeout="30m")`

**Custom Docker image for UV:**

```python
hf_jobs("uv", {
    "script": "inference.py",
    "image": "vllm/vllm-openai:latest",
    "flavor": "a10g-large"
})
```

**Python version:** add `"python": "3.11"` (default is 3.12).

**Extra dependencies at runtime:** add `"dependencies": ["transformers", "torch>=2.0"]`.

**⚠️ Script paths:** The `hf_jobs()` MCP tool requires **inline code** or a **URL** — local paths won't exist in the remote container. Read the file first:

```python
from pathlib import Path
script = Path("hf-jobs/scripts/foo.py").read_text()
hf_jobs("uv", {"script": script})
```

The `hf jobs uv run` CLI *does* support local paths (it uploads the script).

### Approach 2: Docker-Based Jobs

```python
hf_jobs("run", {
    "image": "python:3.12",
    "command": ["python", "-c", "print('Hello from HF Jobs!')"],
    "flavor": "cpu-basic",
    "timeout": "30m"
})
```

Use HF Spaces as images: `"image": "hf.co/spaces/lhoestq/duckdb"`.

### Finding UV Scripts on Hub

The `uv-scripts` organization provides ready-to-use scripts:

```python
dataset_search({"author": "uv-scripts", "sort": "downloads", "limit": 20})
```

---

## Hardware Selection

| Workload | Recommended Flavor | Notes |
|----------|-------------------|-------|
| Data processing, testing | `cpu-basic`, `cpu-upgrade` | Lightweight tasks |
| Small models (<1B) | `t4-small` | Quick tests |
| Medium models (1-7B) | `t4-medium`, `l4x1` | |
| Large models (7-13B) | `a10g-small`, `a10g-large` | Production inference |
| Very large models (13B+) | `a100-large` | |
| Multi-GPU | `l4x4`, `a10g-largex2`, `a10g-largex4` | Parallel workloads |
| TPU | `v5e-1x1`, `v5e-2x2`, `v5e-2x4` | JAX/Flax |

**All flavors:** CPU: `cpu-basic`, `cpu-upgrade` · GPU: `t4-small`, `t4-medium`, `l4x1`, `l4x4`, `a10g-small`, `a10g-large`, `a10g-largex2`, `a10g-largex4`, `a100-large` · TPU: `v5e-1x1`, `v5e-2x2`, `v5e-2x4`

Start small, scale up. See `references/hardware_guide.md` for detailed specs.

---

## Saving Results

**⚠️ Jobs are ephemeral — unsaved results are lost.** Push to Hub (recommended), external storage, or an API.

```python
# Push to Hub (include secrets={"HF_TOKEN": "$HF_TOKEN"} in job config)
model.push_to_hub("username/model-name", token=os.environ["HF_TOKEN"])
dataset.push_to_hub("username/dataset-name", token=os.environ["HF_TOKEN"])
```

> Full persistence guide: `references/hub_saving.md`

---

## Timeout Management

Default: **30 minutes**. Set via `"timeout": "2h"`.

Formats: integer (seconds), or string with suffix (`"5m"`, `"2h"`, `"1d"`).

| Scenario | Recommended | | Scenario | Recommended |
|----------|-------------|-|----------|-------------|
| Quick test | 10-30 min | | Batch inference | 2-4 h |
| Data processing | 1-2 h | | Long-running | 8-24 h |

Always add 20-30% buffer. On timeout, the job is killed immediately.

---

## Cost Estimation

`Total Cost = Hours × $/hour`. Start small — test on `cpu-basic` (~$0.10/h), scale to `a10g-large` (~$5/h) when needed.

Tips: Set appropriate timeouts, use checkpoints, don't over-provision hardware.

---

## Monitoring and Tracking

```python
hf_jobs("ps")                                  # List jobs
hf_jobs("inspect", {"job_id": "..."})          # Status
hf_jobs("logs", {"job_id": "..."})             # Logs
hf_jobs("cancel", {"job_id": "..."})           # Cancel
```

**Python API:** `list_jobs()`, `inspect_job(job_id)`, `fetch_job_logs(job_id)`, `cancel_job(job_id)`.
**CLI:** `hf jobs ps`, `hf jobs logs <id>`, `hf jobs cancel <id>`.

Jobs URL: `https://huggingface.co/jobs/username/job-id`

Wait for user to request status checks — avoid polling repeatedly.

---

## Scheduled Jobs

```python
hf_jobs("scheduled uv", {
    "script": "your_script.py",
    "schedule": "@hourly",       # or CRON: "0 9 * * 1"
    "flavor": "cpu-basic"
})
```

**Presets:** `@annually`, `@monthly`, `@weekly`, `@daily`, `@hourly` — or any CRON expression.

**Manage:** `hf_jobs("scheduled ps")`, `scheduled inspect`, `scheduled suspend`, `scheduled resume`, `scheduled delete`.

**Python API:** `create_scheduled_uv_job()`, `list_scheduled_jobs()`, `suspend_scheduled_job()`, `resume_scheduled_job()`, `delete_scheduled_job()`.

---

## Webhooks

Trigger jobs automatically when Hub repositories change:

```python
from huggingface_hub import create_webhook
webhook = create_webhook(
    job_id=job.id,
    watched=[{"type": "user", "name": "your-username"}],
    domains=["repo", "discussion"],
    secret="your-secret"
)
```

The triggered job receives `WEBHOOK_PAYLOAD` as an environment variable. Use cases: auto-process new datasets, trigger inference on model updates, run tests on code changes.

---

## Common Workload Patterns

This skill ships ready-to-run scripts in `scripts/`. Prefer them over inventing new templates.

### Pattern 1: Dataset → Model Responses (vLLM) — `scripts/generate-responses.py`

Loads a Hub dataset, applies a chat template, generates responses with vLLM, pushes output. **Requires:** GPU + write token.

```python
from pathlib import Path
script = Path("hf-jobs/scripts/generate-responses.py").read_text()
hf_jobs("uv", {
    "script": script,
    "script_args": ["username/input", "username/output",
                    "--model-id", "Qwen/Qwen3-30B-A3B-Instruct-2507"],
    "flavor": "a10g-large", "timeout": "4h",
    "secrets": {"HF_TOKEN": "$HF_TOKEN"}
})
```

### Pattern 2: CoT Self-Instruct — `scripts/cot-self-instruct.py`

Generates synthetic prompts/answers via CoT Self-Instruct with optional filtering. **Requires:** GPU + write token.

```python
from pathlib import Path
script = Path("hf-jobs/scripts/cot-self-instruct.py").read_text()
hf_jobs("uv", {
    "script": script,
    "script_args": ["--seed-dataset", "davanstrien/s1k-reasoning",
                    "--output-dataset", "username/synthetic-math",
                    "--num-samples", "5000"],
    "flavor": "l4x4", "timeout": "8h",
    "secrets": {"HF_TOKEN": "$HF_TOKEN"}
})
```

### Pattern 3: Streaming Dataset Stats — `scripts/finepdfs-stats.py`

Scans parquet from Hub via Polars, computes stats, optionally uploads results. CPU often sufficient.

```python
from pathlib import Path
script = Path("hf-jobs/scripts/finepdfs-stats.py").read_text()
hf_jobs("uv", {
    "script": script,
    "script_args": ["--limit", "10000", "--output-repo", "username/stats"],
    "flavor": "cpu-upgrade", "timeout": "2h",
    "secrets": {"HF_TOKEN": "$HF_TOKEN"}
})
```

---

## Troubleshooting (Quick)

| Problem | Fix |
|---------|-----|
| OOM | Reduce batch size or upgrade hardware |
| Timeout | Increase timeout, optimize code |
| Hub push fails | Add `secrets={"HF_TOKEN": "$HF_TOKEN"}`, check permissions |
| Import errors | Add to PEP 723 `dependencies` |
| Auth errors | Check `hf_whoami()`, verify secrets |

> Full troubleshooting guide: `references/troubleshooting.md`

---

## Quick Reference: MCP Tool vs CLI vs Python API

| Operation | MCP Tool | CLI | Python API |
|-----------|----------|-----|------------|
| Run UV script | `hf_jobs("uv", {...})` | `hf jobs uv run script.py` | `run_uv_job()` |
| Run Docker job | `hf_jobs("run", {...})` | `hf jobs run image cmd` | `run_job()` |
| List jobs | `hf_jobs("ps")` | `hf jobs ps` | `list_jobs()` |
| View logs | `hf_jobs("logs", {...})` | `hf jobs logs <id>` | `fetch_job_logs()` |
| Cancel | `hf_jobs("cancel", {...})` | `hf jobs cancel <id>` | `cancel_job()` |
| Schedule UV | `hf_jobs("scheduled uv", {...})` | — | `create_scheduled_uv_job()` |
| Schedule Docker | `hf_jobs("scheduled run", {...})` | — | `create_scheduled_job()` |

## Key Takeaways

1. **Submit scripts inline** via `hf_jobs()` — no file saving required
2. **Jobs are asynchronous** — don't poll; let user check when ready
3. **Always set timeout** and **always persist results** (environment is ephemeral)
4. **Use tokens securely** — `secrets={"HF_TOKEN": "$HF_TOKEN"}`
5. **Start small** — test on `cpu-basic`, scale up as needed

## Resources

- `references/token_usage.md` · `references/hardware_guide.md` · `references/hub_saving.md` · `references/troubleshooting.md`
- `scripts/generate-responses.py` · `scripts/cot-self-instruct.py` · `scripts/finepdfs-stats.py`
- [HF Jobs Guide](https://huggingface.co/docs/huggingface_hub/guides/jobs) · [CLI Reference](https://huggingface.co/docs/huggingface_hub/guides/cli#hf-jobs) · [API Reference](https://huggingface.co/docs/huggingface_hub/package_reference/hf_api) · [Hardware Flavors](https://huggingface.co/docs/hub/en/spaces-config-reference)
- [UV Scripts Guide](https://docs.astral.sh/uv/guides/scripts/) · [UV Scripts Org](https://huggingface.co/uv-scripts) · [Webhooks Docs](https://huggingface.co/docs/huggingface_hub/guides/webhooks)
