---
name: hugging-face-jobs
description: Run workloads on Hugging Face Jobs infrastructure. Covers UV scripts, Docker jobs, hardware selection, authentication, secrets, timeouts, result persistence, scheduled jobs, and webhooks. For model training, see model-trainer skill.
license: Complete terms in LICENSE.txt
---

# Running Workloads on Hugging Face Jobs

Run any workload on fully managed HF infrastructure. No local setup required.

**Use cases:** Data processing, batch inference, experiments, synthetic data generation, scheduled jobs, development/testing on cloud GPUs/TPUs.

**For model training:** See `model-trainer` skill for TRL-based workflows.

## Key Directives

1. **Use `hf_jobs()` MCP tool** - Pass script content inline as string. Do NOT save to local files.
2. **Always handle auth** - Hub operations require `secrets: {"HF_TOKEN": "$HF_TOKEN"}`.
3. **Provide job details** after submission - Job ID, monitoring URL, estimated time.
4. **Set appropriate timeouts** - Default 30min may be insufficient.
5. **Always persist results** - Environment is ephemeral; all files deleted when job ends.

## Prerequisites

- HF account with Pro/Team/Enterprise plan
- Authenticated: verify with `hf_whoami()`
- HF_TOKEN with appropriate permissions (read/write)

## Quick Start: UV Scripts (Recommended)

```python
hf_jobs("uv", {
    "script": """
# /// script
# dependencies = ["transformers", "torch"]
# ///
from transformers import pipeline
result = pipeline("sentiment-analysis")("I love HF!")
print(result)
""",
    "flavor": "cpu-basic",
    "timeout": "30m",
    "secrets": {"HF_TOKEN": "$HF_TOKEN"}
})
```

**Script parameter:** Must be inline code string or URL. Local paths don't work with MCP tool (remote container can't see local files). Read file contents first: `Path("script.py").read_text()`.

**Custom image:** `"image": "vllm/vllm-openai:latest"` for pre-built ML environments.
**Extra deps:** `"dependencies": ["transformers", "torch>=2.0"]` beyond PEP 723 header.
**Python version:** `"python": "3.11"` (default: 3.12).

## Docker Jobs

```python
hf_jobs("run", {
    "image": "pytorch/pytorch:2.6.0-cuda12.4-cudnn9-devel",
    "command": ["python", "-c", "import torch; print(torch.cuda.get_device_name())"],
    "flavor": "a10g-small",
    "timeout": "1h"
})
```

Use for: custom Docker images, non-Python workloads, complex environments.
HF Spaces as images: `"image": "hf.co/spaces/lhoestq/duckdb"`

## Hardware Selection

| Workload | Flavor | Notes |
|----------|--------|-------|
| Testing, lightweight | `cpu-basic` | |
| Data processing | `cpu-upgrade` | |
| <1B models | `t4-small` | 16GB VRAM |
| 1-7B models | `l4x1`, `a10g-small` | 24GB VRAM |
| 7-13B models | `a10g-large` | 24GB VRAM |
| 13B+ models | `a100-large` | 40GB VRAM |
| Multi-GPU | `l4x4`, `a10g-largex2/x4` | 48-96GB total |
| TPU (JAX/Flax) | `v5e-1x1/2x2/2x4` | |

Start small for testing, scale up based on needs. See `references/hardware_guide.md`.

## Saving Results (CRITICAL)

**Environment is ephemeral. Without persistence, ALL work is lost.**

```python
# Push to Hub (recommended)
model.push_to_hub("user/model", token=os.environ["HF_TOKEN"])
dataset.push_to_hub("user/dataset", token=os.environ["HF_TOKEN"])
api.upload_file("results.json", "results.json", "user/results", repo_type="dataset")
```

Always include `secrets: {"HF_TOKEN": "$HF_TOKEN"}` and verify token in script:
```python
assert "HF_TOKEN" in os.environ, "HF_TOKEN required!"
```

See `references/hub_saving.md` for complete persistence guide.

## Token Usage

Use `secrets` (encrypted) not `env` (visible in logs):
```python
"secrets": {"HF_TOKEN": "$HF_TOKEN"}  # Auto-replaced with your token
```

Never hardcode tokens. See `references/token_usage.md` for details.

## Timeout Management

Default: 30 minutes. Formats: `"90m"`, `"2h"`, `"1.5h"`, `300` (seconds), `"1d"`.

| Scenario | Timeout |
|----------|---------|
| Quick test | 10-30m |
| Data processing | 1-2h |
| Batch inference | 2-4h |
| Long-running | 8-24h |

Add 20-30% buffer. On timeout: job killed, unsaved progress lost.

## Monitoring

```python
hf_jobs("ps")                                    # List jobs
hf_jobs("inspect", {"job_id": "..."})            # Job details
hf_jobs("logs", {"job_id": "..."})               # View logs
hf_jobs("cancel", {"job_id": "..."})             # Cancel job
```

Job URL: `https://huggingface.co/jobs/username/job-id`

## Scheduled Jobs

```python
hf_jobs("scheduled uv", {
    "script": "...",
    "schedule": "@daily",       # or CRON: "0 9 * * 1"
    "flavor": "cpu-basic"
})
```

Schedules: `@hourly`, `@daily`, `@weekly`, `@monthly`, or CRON syntax.
Manage: `hf_jobs("scheduled ps/inspect/suspend/resume/delete", {...})`

## Webhooks

Trigger jobs on Hub repository changes via `create_webhook()`. Payload available as `WEBHOOK_PAYLOAD` env var.

## Common Workload Patterns

Ship-ready scripts in `hf-jobs/scripts/`:
- `generate-responses.py` - vLLM batch: dataset -> responses -> Hub
- `cot-self-instruct.py` - CoT synthetic data generation + filtering -> Hub
- `finepdfs-stats.py` - Polars streaming stats over Hub parquet

Read script contents with `Path("hf-jobs/scripts/foo.py").read_text()` then pass to `hf_jobs("uv", {"script": script, ...})`.

## Troubleshooting

| Issue | Fix |
|-------|-----|
| OOM | Reduce batch size, upgrade hardware |
| Timeout | Increase timeout, optimize code |
| Hub push fails | Add `secrets: {"HF_TOKEN": "$HF_TOKEN"}`, verify token |
| Missing deps | Add to PEP 723 header: `# dependencies = [...]` |
| Auth errors | Check `hf_whoami()`, re-login, verify permissions |

See `references/troubleshooting.md` for complete guide.

## API Quick Reference

| Operation | MCP Tool | CLI | Python API |
|-----------|----------|-----|------------|
| UV script | `hf_jobs("uv", {...})` | `hf jobs uv run script.py` | `run_uv_job()` |
| Docker job | `hf_jobs("run", {...})` | `hf jobs run image cmd` | `run_job()` |
| List jobs | `hf_jobs("ps")` | `hf jobs ps` | `list_jobs()` |
| View logs | `hf_jobs("logs", {...})` | `hf jobs logs <id>` | `fetch_job_logs()` |
| Cancel | `hf_jobs("cancel", {...})` | `hf jobs cancel <id>` | `cancel_job()` |
