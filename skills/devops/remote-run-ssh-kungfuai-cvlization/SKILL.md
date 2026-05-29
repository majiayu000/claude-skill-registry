---
name: remote-run-ssh
description: Run CVlization examples on the `ssh l1` GPU host by copying only the needed example directory plus the shared `cvlization/` package into `/tmp`, then launching the example’s Docker scripts.
---

# Remote Run over SSH

Operate CVlization examples on the remote GPU reachable as `ssh l1`. This playbook keeps the remote copy minimal—just the target example folder (e.g., `examples/perception/multimodal_multitask/recipe_analysis_torch`) and the `cvlization/` library—then relies on the example’s own `build.sh` / `train.sh` Docker helpers. The user’s long-lived checkout on the remote stays untouched.

## When to Use
- Heavy trainings or evaluations that require CUDA (CIFAR10 speed runs, multimodal pipelines, etc.).
- Performance or regression measurements on the remote GPU after local code changes.
- Producing reproducible logs / artifacts for discussions or CI baselines without pushing a branch first.

## Prerequisites
- Local repo state ready to sync (uncommitted changes acceptable).
- SSH config already maps the GPU machine to `l1`.
- Remote host provides NVIDIA GPU (currently A10) and Docker with GPU runtime enabled.
- At least ~15 GB free under `/tmp` for the slim workspace, Docker context, and caches.
- Hugging Face tokens or other creds available locally if the example pulls hub assets.

## Quick Reference
1. Choose the example to run.
2. `rsync` only the example folder, `cvlization/`, and any required helper dirs to `/tmp/cvlization_remote` on `l1`.
3. On `l1`, run `./build.sh` inside the example folder to build the Docker image.
4. Run `./train.sh` (or the example’s equivalent) to launch the job with GPU access.
5. Collect logs / metrics and record the run in `var/skills/remote-run-ssh/runs/<timestamp>/log.md`.

## Detailed Procedure

### 1. Identify the example and supporting files
- Note the example path relative to repo root (e.g., `examples/perception/multimodal_multitask/recipe_analysis_torch`).
- List any extra assets the run needs (custom configs under `examples`, top-level scripts, environment files, etc.).
- Confirm `cvlization/` includes all library modules the example imports.

### 2. Sync minimal workspace to `/tmp`
```bash
REMOTE_ROOT=/tmp/cvlization_remote
rsync -az --delete \
  --include='cvlization/***' \
  --include='examples/***' \
  --include='scripts/***' \
  --include='pyproject.toml' \
  --include='setup.cfg' \
  --include='README.md' \
  --exclude='*' \
  ./ l1:${REMOTE_ROOT}/
```
Tips:
- Adjust the include list if the example needs additional files (e.g., `docker-compose.yml`, `requirements.txt`). The blanket `--exclude='*'` prevents unrelated directories from syncing.
- Keep the remote path structure (`${REMOTE_ROOT}/examples/...`) aligned with the local repo so relative paths like `../../../..` used inside scripts still resolve to the repo root.
- Avoid syncing `.git`, local datasets, `.venv`, or heavy cache directories.

### 3. Build the example image
```bash
ssh l1 'cd /tmp/cvlization_remote/examples/perception/multimodal_multitask/recipe_analysis_torch && ./build.sh'
```
- The Docker build context is limited to the example folder, keeping builds quick.
- Edit `build.sh` locally if you need custom base images or dependency tweaks before re-syncing.

### 4. Confirm GPU availability
```bash
ssh l1 'nvidia-smi'
```
Ensure no conflicting jobs are consuming the GPU before starting a long run.

### 5. Run the training script (Docker)
```bash
ssh l1 'cd /tmp/cvlization_remote/examples/perception/multimodal_multitask/recipe_analysis_torch && ./train.sh > run.log 2>&1'
```
- Tail logs while the job runs:
```bash
ssh l1 'tail -f /tmp/cvlization_remote/examples/perception/multimodal_multitask/recipe_analysis_torch/run.log'
```
- `train.sh` already mounts the example directory at `/workspace`, mounts the synced repo root read-only at `/cvlization_repo`, and sets `PYTHONPATH=/cvlization_repo`.
- Customize environment variables or extra mounts by editing `train.sh` locally (e.g., injecting dataset paths, WANDB keys) then re-syncing.
- If an example lacks Docker scripts, fall back to running its entrypoint directly (`python train.py`) inside the container or a temporary venv—but document the deviation in the run log.

### 6. Capture metrics
Log files should include per-epoch summaries and final metrics. Record:
- Wall-clock time / throughput.
- Accuracy, loss, or other task metrics.
- Warnings or notable log lines (e.g., retry downloads, CUDA warnings).

### 7. Retrieve artifacts (optional)
```bash
rsync -az l1:/tmp/cvlization_remote/examples/perception/multimodal_multitask/recipe_analysis_torch/run.log \
  ./remote_runs/$(date +%Y%m%dT%H%M%S)_multimodal.log
```
Copy checkpoints, TensorBoard logs, or generated samples in the same manner if needed.

### 8. Document the run
- Create `var/skills/remote-run-ssh/runs/<timestamp>/log.md` summarizing:
  - Example path, git commit or diff basis.
  - Commands executed (`build.sh`, `train.sh` args).
  - Key metrics / observations.
  - Location of logs or artifacts (local paths or remote references).

### 9. Cleanup (optional)
- Delete `/tmp/cvlization_remote` when finished if the disk budget is tight (`ssh l1 'rm -rf /tmp/cvlization_remote'`).
- Clear cached datasets (`rm -rf /root/.cache/...` inside Docker) only if future runs should start fresh.

## Troubleshooting
- **Missing module inside container**: Ensure `train.sh` mounts the repo root and sets `PYTHONPATH`. Re-run `rsync` if files were added after the initial sync.
- **Docker build fails**: Inspect the output of `./build.sh`. Some examples assume base images with CUDA toolkits—update the Dockerfile accordingly.
- **CUDA OOM**: Reduce batch sizes or precision, or run one job at a time on `l1`.
- **No GPU detected**: Confirm `--gpus=all` is present in `train.sh` and check `nvidia-smi` on the host.
- **Long sync times**: Tighten the rsync include rules to the specific example and library folders required.

## Outputs
Every run should leave:
- Remote workspace at `/tmp/cvlization_remote` containing the synced example + library.
- Local or remote logs with the captured metrics.
- A run log under `var/skills/remote-run-ssh/runs/<timestamp>/log.md` documenting the session.
