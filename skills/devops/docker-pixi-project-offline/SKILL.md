---
name: docker-pixi-project-offline
description: Scripted process to build and verify a Pixi-managed project in Docker, then produce a portable WORKDIR/product directory for air-gapped use.
---

# Docker Pixi Project Offline

Prepare an existing Pixi-managed project for an air-gapped environment by:
1) building and verifying it inside a Docker container (with network access), and
2) producing a **WORKDIR/product/** folder that can be packed and delivered.

This skill includes helper scripts under `scripts/`. Prefer using them (each supports `--help`) rather than retyping the manual steps.

## What to ask the user

- Project source (pick one):
  - `PROJECT_DIR`: path to the Pixi project on the host (`pixi.toml` or `pyproject.toml`), or
  - `PROJECT_PATH_IN_CONTAINER`: path to the Pixi project already present inside a container
- `VERIFY_SPEC`: one of:
  - a concrete command to run under Pixi (e.g. `python -m yourpkg --help`)
  - a Pixi task name from the manifest (e.g. `smoke`)
  - a script path (e.g. `./scripts/smoke.sh`) plus what counts as success
  - a short description of what “success” means (you convert it into one or more commands)
- Build execution target (pick one):
  - `IMAGE`: a Docker image that contains Pixi (recommended), or
  - `CONTAINER_ID`: an already-running container to use
- Optional `RESOURCES_DIR`: any extra runtime resources to bundle alongside the project (models, data files, binaries)
- Optional `CONTAINER_WORKDIR_PATH`: where the scripts stage files inside the container (use this if `/workdir` already exists or is reserved in the image/container)
- Optional `WORKDIR` (host output dir): where the scripts write the generated workdir on the host (default: `<workspace>/tmp/workdir-<ts>`)

## Preconditions

- Build machine has Docker and internet access.
- Use the provided Docker image/container. If it can run the project offline once packaged, that’s sufficient.
- Pixi is available inside the container (prebuilt image, or installed during image build).
- Air-gapped runtime must also have Pixi available (the product does not include the Pixi binary).
- For reproducibility: `pixi.lock` exists and is up to date.

## Outputs

- `WORKDIR/`: a self-contained workspace holding the staged project, resources, Pixi cache, and logs/test outputs.
- `WORKDIR/product/`: the deliverable directory (you pack and ship this folder; archiving is out of scope for this skill).

## Workdir layout

Use a single work directory so “inputs + outputs” are easy to copy/inspect:

- `WORKDIR/project/<project_name>/`: staged project copy (input to product generation)
- `WORKDIR/resources/`: optional resources to include (input to product generation)
- `WORKDIR/pixi-cache/`: Pixi cache produced during the online build (input to product generation)
- `WORKDIR/out/`: logs and test outputs only
- `WORKDIR/helpers/`: helper scripts used during preparation (not shipped to air-gapped)
  - `WORKDIR/helpers/make-archive-ready-product.sh`: creates/overwrites `WORKDIR/product/`
- `WORKDIR/product/`: generated deliverable (created/overwritten by `WORKDIR/helpers/make-archive-ready-product.sh`)

## Product layout (deliverable)

`WORKDIR/product/` must be self-contained and include:

- `WORKDIR/product/<project_name>/`: project directory containing Pixi manifest (`pixi.toml` or `pyproject.toml`) and the minimal files needed to run
- `WORKDIR/product/res/` (optional): binary data/resources required at runtime
- `WORKDIR/product/pkg-cache/`: Pixi package cache containing everything needed to install without internet
- `WORKDIR/product/envs.sh`: manual environment setup (users can `source envs.sh` before running Pixi commands)
- `WORKDIR/product/bootstrap-project.sh`: bootstraps the project (sources `envs.sh` then runs `pixi install` for `<project_name>/` using `pkg-cache/`)

## Process

### 0) Scripts

All scripts are in this skill directory:
- `scripts/create-workdir-from-host.sh`
- `scripts/create-workdir-from-container.sh`
- `scripts/make-archive-ready-product.sh`
- `scripts/final-verify-product.sh`

Each script is intended to be manually invokable and provides `--help`.
The `create-workdir-*` scripts also copy `scripts/make-archive-ready-product.sh` into `WORKDIR/helpers/` for portability.

### 1) Decide what “verification” means

Acceptable forms:
- **Pixi task**: `smoke` (run as `pixi run smoke`)
- **Script**: `./scripts/smoke.sh` (define success: exit code 0, expected output, created files, etc.)
- **Command**: `python -c "import yourpkg; print('ok')"`
- **Description**: “Running the CLI help works and prints version” (convert into one or more commands)

When executing, capture output into `WORKDIR/out/` so the workdir contains the proof.

### 2) Create `WORKDIR/`

Use exactly one of the following paths:

#### 2a) From a host project dir (recommended)

This stages a filtered copy of the project into `WORKDIR/project/<project_name>/`, runs `pixi install`, and runs verification (optional):

```bash
./scripts/create-workdir-from-host.sh --help
./scripts/create-workdir-from-host.sh \
  --image your-pixi-image:tag \
  --project-dir /path/to/project \
  --resources-dir /path/to/resources \
  --container-workdir-path /tmp/workdir \
  --verify-run -- python -c 'import yourpkg; print("ok")'
```

#### 2b) From an existing container project dir

If the project directory already exists in a running container, create `/workdir` in that container and copy it back to the host:

```bash
./scripts/create-workdir-from-container.sh --help
./scripts/create-workdir-from-container.sh \
  --container-id <CONTAINER_ID> \
  --project-path-in-container /path/to/project \
  --container-workdir-path /tmp/workdir \
  --verify-task smoke
```

### 3) Create the deliverable `WORKDIR/product/`

```bash
./tmp/pixi-offline-work/helpers/make-archive-ready-product.sh --help
./tmp/pixi-offline-work/helpers/make-archive-ready-product.sh \
  --workdir ./tmp/pixi-offline-work --project-name <project_name>
```

### 4) Final verification (offline product)

Verify the **product** (not the staged project) in an offline/no-network container. This is the final verification step.
```bash
./scripts/final-verify-product.sh --help
./scripts/final-verify-product.sh \
  --image your-pixi-image:tag \
  --product-dir ./tmp/pixi-offline-work/product \
  --out-dir ./tmp/pixi-offline-work/out \
  --project-name <project_name> \
  --verify-run -- python -c 'import yourpkg; print("ok")'
```

If this passes with networking disabled, it demonstrates that `pixi install` is satisfied by `product/pkg-cache/`.

After `WORKDIR/product/` is created and verified, the remaining steps (packing, transferring, extracting, and running in the air-gapped environment) are the user’s responsibility.

## Pitfalls / Notes

- **Offline meaning**: if “offline” means “no network”, prove it by running `./bootstrap-project.sh` and then `pixi run ...` with `--network none`.
- **Secrets**: staging matters—don’t accidentally package `.env`, credentials, SSH keys, or tokens.
- **Multiple Pixi envs**: verify/package the environment(s) you actually need.

## Future automation (not implemented here)

When you want this to be push-button, add a small orchestrator that:
- stages with consistent excludes
- runs the container build/verify
- emits a manifest (image digest, pixi version, lockfile hash)
- wraps the `scripts/` in a single command
