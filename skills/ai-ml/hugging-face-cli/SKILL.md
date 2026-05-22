---
name: hugging-face-cli
description: >-
  Execute Hugging Face Hub operations using the hf CLI. Covers authentication,
  downloading models and datasets, uploading files, repository management,
  cache operations, cloud compute jobs, inference endpoints, and Hub browsing.
  Use when the user needs to interact with the Hugging Face Hub from the terminal.
allowed-tools:
  - Bash
  - Read
  - Write
  - Grep
  - Glob
metadata:
  version: "1.0.0"
  author: "platxa"
  tags:
    - builder
    - ml
    - huggingface
    - cli
    - devops
  provenance:
    upstream_source: "hugging-face-cli"
    upstream_sha: "c0e08fdaa8ed6929110c97d1b867d101fd70218f"
    regenerated_at: "2026-02-04T15:54:34Z"
    generator_version: "1.0.0"
    intent_confidence: 0.68
---

# Hugging Face CLI

Run `hf` commands to download models, upload files, manage repos, control cache, and launch compute jobs on Hugging Face infrastructure.

## Overview

The `hf` CLI provides direct terminal access to the Hugging Face Hub. It wraps `huggingface_hub` Python APIs into shell commands for authentication, file transfer, repository lifecycle, cache control, Hub browsing, cloud compute, and inference endpoint management.

**What it builds:**
- Download commands for models, datasets, and spaces
- Upload workflows with commit messages, PRs, and sync patterns
- Repository creation, tagging, branching, and settings updates
- Cache inspection, cleanup, and verification pipelines
- Cloud compute job definitions with GPU/TPU flavor selection
- Inference endpoint deployment configurations

## Workflow

### Step 1: Authenticate

```bash
# Interactive login
hf auth login

# Non-interactive (CI/CD)
hf auth login --token $HF_TOKEN --add-to-git-credential

# Verify identity
hf auth whoami
```

Store tokens securely. Use `--add-to-git-credential` for git-lfs operations. The token is saved to `~/.cache/huggingface/token` by default. Override with `HF_TOKEN` environment variable.

### Step 2: Download Content

```bash
# Full repo to cache
hf download meta-llama/Llama-3.2-1B-Instruct

# To local directory
hf download meta-llama/Llama-3.2-1B-Instruct --local-dir ./models

# Specific files with pattern filtering
hf download stabilityai/sdxl-base --include "*.safetensors" --exclude "*.fp16.*"

# Dataset download
hf download HuggingFaceH4/ultrachat_200k --repo-type dataset

# Specific revision
hf download bigcode/starcoder2 --revision refs/pr/42

# Dry-run to check files before downloading
hf download openai-community/gpt2 --dry-run

# Quiet mode for scripting
MODEL_PATH=$(hf download gpt2 --quiet)
```

Set `HF_HUB_DOWNLOAD_TIMEOUT=30` for slow connections (default: 10s). Use `--cache-dir` to redirect storage.

### Step 3: Upload Content

```bash
# Upload current directory to repo root
hf upload my-username/my-model . .

# Single file
hf upload my-username/my-model model.safetensors

# Upload to specific path in repo
hf upload my-username/my-model ./output /weights

# Create PR instead of direct push
hf upload my-username/my-model . . --create-pr

# Custom commit message
hf upload my-username/my-model . . --commit-message="Release v1.0"

# Sync with remote (delete removed files)
hf upload my-username/my-space . . --repo-type space --exclude="/logs/*" --delete="*"

# Auto-upload during development (every 5 minutes)
hf upload my-username/my-space . . --repo-type space --every=5

# Very large folders (resumable, chunked)
hf upload-large-folder my-username/my-model ./large_model_dir
```

The repo is auto-created if it does not exist. Use `--quiet` to get only the upload URL.

### Step 4: Manage Repositories

```bash
# Create repos
hf repo create my-model
hf repo create my-dataset --repo-type dataset --private
hf repo create my-app --repo-type space --space-sdk gradio

# Branching and tagging
hf repo branch create my-model release-v1
hf repo tag create my-model v1.0 --revision release-v1

# Update settings
hf repo settings my-model --gated auto --private true

# Delete files from repo
hf repo-files delete my-model "*.bin" folder/

# Move or delete repo
hf repo move old-ns/model new-ns/model
hf repo delete my-model
```

### Step 5: Manage Cache

```bash
# Inspect cache
hf cache ls
hf cache ls --revisions --format json

# Filter by size
hf cache ls --filter "size>30g" --sort size:desc

# Remove specific repos or revisions
hf cache rm model/gpt2 --dry-run
hf cache rm model/gpt2 -y

# Remove old unused entries
hf cache rm $(hf cache ls --filter "accessed>1y" -q) -y

# Prune detached revisions
hf cache prune

# Verify checksums
hf cache verify deepseek-ai/DeepSeek-OCR
hf cache verify my-model --local-dir /path/to/repo --fail-on-missing-files
```

Default cache location: `~/.cache/huggingface/hub`. Override with `HF_HUB_CACHE`.

### Step 6: Browse the Hub

```bash
# Models
hf models ls --search "lora" --sort downloads --limit 10
hf models info Qwen/Qwen2-72B

# Datasets
hf datasets ls --search "code" --sort downloads
hf datasets info HuggingFaceFW/fineweb

# Spaces
hf spaces ls --filter "3d" --limit 10
hf spaces info enzostvs/deepsite

# Papers
hf papers ls --sort=trending --limit=5
hf papers ls --date=today
```

### Step 7: Run Cloud Compute Jobs

```bash
# CPU job
hf jobs run python:3.12 python script.py

# GPU job
hf jobs run --flavor a10g-small pytorch/pytorch:2.6.0-cuda12.4-cudnn9-devel python train.py

# With secrets and environment variables
hf jobs run --secrets HF_TOKEN -e WANDB_KEY=$WANDB_KEY --flavor a100-large my-image python train.py

# Set timeout (default 30min)
hf jobs run --timeout 2h --flavor a100-large my-image python train.py

# UV script execution
hf jobs uv run --with transformers --flavor t4-small train.py

# Scheduled jobs
hf jobs scheduled run @daily --timeout 4h python:3.12 python pipeline.py

# Monitor jobs
hf jobs ps -a
hf jobs logs <job_id>
hf jobs stats <job_id>
hf jobs cancel <job_id>
```

**GPU flavors:** `cpu-basic`, `cpu-upgrade`, `t4-small`, `t4-medium`, `l4x1`, `l4x4`, `a10g-small`, `a10g-large`, `a10g-largex2`, `a10g-largex4`, `a100-large`, `h100`, `h100x8`

**TPU flavors:** `v5e-1x1`, `v5e-2x2`, `v5e-2x4`

### Step 8: Deploy Inference Endpoints

```bash
# Deploy from catalog
hf endpoints catalog deploy --repo meta-llama/Llama-3.2-1B-Instruct --name my-endpoint

# Custom deployment
hf endpoints deploy my-endpoint \
  --repo gpt2 \
  --framework pytorch \
  --accelerator gpu \
  --instance-size x4 \
  --instance-type nvidia-a10g \
  --region us-east-1 \
  --vendor aws

# Lifecycle management
hf endpoints describe my-endpoint
hf endpoints pause my-endpoint
hf endpoints resume my-endpoint
hf endpoints scale-to-zero my-endpoint
hf endpoints delete my-endpoint --yes
```

## Common Patterns

### CI/CD Model Publishing

```bash
hf auth login --token $HF_TOKEN --add-to-git-credential
hf repo create $ORG/$MODEL_NAME --private || true
hf upload $ORG/$MODEL_NAME ./output . --commit-message="Release v${VERSION}"
hf repo tag create $ORG/$MODEL_NAME "v${VERSION}"
```

### Download for Local Inference

```bash
MODEL_PATH=$(hf download meta-llama/Llama-3.2-1B-Instruct --quiet)
echo "Model cached at: $MODEL_PATH"

# Or download to a fixed directory
hf download meta-llama/Llama-3.2-1B-Instruct --local-dir ./model
```

### GPU Training Job with Monitoring

```bash
JOB_ID=$(hf jobs run --detach --flavor a100-large \
  --secrets HF_TOKEN -e WANDB_KEY=$WANDB_KEY \
  --timeout 4h pytorch/pytorch:2.6.0-cuda12.4-cudnn9-devel \
  python train.py)
hf jobs logs $JOB_ID
hf jobs stats $JOB_ID
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `HF_TOKEN` | Authentication token | - |
| `HF_HOME` | Root config/cache directory | `~/.cache/huggingface` |
| `HF_HUB_CACHE` | Repository cache directory | `$HF_HOME/hub` |
| `HF_HUB_DOWNLOAD_TIMEOUT` | Download timeout in seconds | `10` |
| `HF_HUB_OFFLINE` | Disable all HTTP calls | `False` |
| `HF_XET_HIGH_PERFORMANCE` | Maximize network/disk throughput | `False` |
| `HF_HUB_DISABLE_PROGRESS_BARS` | Suppress progress bars | `False` |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `Read timed out` during download | `export HF_HUB_DOWNLOAD_TIMEOUT=30` |
| Authentication failures in CI | Use `hf auth login --token $HF_TOKEN` before operations |
| Disk full from cache | `hf cache ls --sort size:desc` then `hf cache rm <repo_id>` |
| Slow downloads | Set `HF_XET_HIGH_PERFORMANCE=1` to maximize bandwidth |
| Interrupted large uploads | Use `hf upload-large-folder` for automatic resume |
| Need offline access | Download first, then set `HF_HUB_OFFLINE=1` |

## Output Checklist

- [ ] Authentication verified with `hf auth whoami`
- [ ] Correct `--repo-type` specified (model, dataset, or space)
- [ ] `--local-dir` used when files need a fixed path (not cache)
- [ ] `--quiet` mode used in scripts for parseable output
- [ ] `--dry-run` used before large downloads
- [ ] Cache periodically cleaned with `hf cache prune`
- [ ] Commit messages included in uploads with `--commit-message`
- [ ] Job timeout set appropriately with `--timeout`

## References

- **Complete command reference**: See [references/commands.md](references/commands.md)
- **Workflow examples and patterns**: See [references/workflows.md](references/workflows.md)
