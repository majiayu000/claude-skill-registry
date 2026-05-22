---
name: Docker Environment Setup
description: Set up a Docker container for running Nextflow training examples. Handles basic setup, Docker-outside-of-Docker (DooD) for containerized processes, ARM Mac platform emulation, and troubleshooting. Use when you need to run Nextflow examples in a consistent environment.
---

# Docker Environment Setup

Set up a Docker container environment for running Nextflow training examples. This skill handles all Docker configuration needed to match the Codespaces/Gitpod environment that learners use.

## Initial Questions

Use `AskUserQuestion` to determine the setup type:

**Which Docker setup do you need?**

- **Basic setup (Recommended)** - For tutorials without containerized processes (e.g., hello_nextflow basics, plugin_development)
- **DooD setup** - For tutorials with containerized processes (e.g., genomics, essential_scripting_patterns)
- **Check/restart existing** - Verify or restart an existing nf-training container

---

## Determine NXF_VER

Before any Docker commands, read the Nextflow version from devcontainer.json:

```bash
NXF_VER=$(grep -o '"NXF_VER":\s*"[^"]*"' .devcontainer/devcontainer.json | cut -d'"' -f4)
echo "Using NXF_VER=${NXF_VER}"
```

This ensures you use the same version learners get in Codespaces.

---

## Basic Setup

For tutorials that don't use containerized processes:

```bash
# Clean up any existing container
docker stop nf-training 2>/dev/null; docker rm nf-training 2>/dev/null

# Start fresh container with UTF-8 locale support
NXF_VER=$(grep -o '"NXF_VER":\s*"[^"]*"' .devcontainer/devcontainer.json | cut -d'"' -f4)
docker run -d --name nf-training \
  -e NXF_VER=${NXF_VER} \
  -e LANG=C.UTF-8 \
  -e LC_ALL=C.UTF-8 \
  -v "${PWD}:/workspaces/training" \
  -w /workspaces/training \
  ghcr.io/nextflow-io/training:latest \
  sleep infinity
```

**Important**: The `LANG=C.UTF-8` and `LC_ALL=C.UTF-8` environment variables are critical for handling non-ASCII characters (like "Holà", "Grüß Gott") in file names and content.

### Running Commands

```bash
docker exec -e LANG=C.UTF-8 -e LC_ALL=C.UTF-8 \
  -w /workspaces/training/<working-dir> \
  nf-training \
  <command>
```

---

## Docker-outside-of-Docker (DooD) Setup

For tutorials with containerized processes (FASTP, BWA, SAMTOOLS, etc.):

```bash
# Clean up any existing container
docker stop nf-training 2>/dev/null; docker rm nf-training 2>/dev/null

# Get NXF_VER and host path
NXF_VER=$(grep -o '"NXF_VER":\s*"[^"]*"' .devcontainer/devcontainer.json | cut -d'"' -f4)
HOST_PATH="${PWD}"

# Start container with DooD support
docker run -d --name nf-training \
  -e NXF_VER=${NXF_VER} \
  -e LANG=C.UTF-8 \
  -e LC_ALL=C.UTF-8 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v "${HOST_PATH}:${HOST_PATH}" \
  -w "${HOST_PATH}" \
  ghcr.io/nextflow-io/training:latest \
  sleep infinity

# Create symlink for Codespaces paths
docker exec nf-training bash -c "rm -rf /workspaces/training && mkdir -p /workspaces && ln -sf ${HOST_PATH} /workspaces/training"
```

**Critical differences from basic setup:**

1. **Docker socket mount** (`-v /var/run/docker.sock:/var/run/docker.sock`) - Allows Nextflow to spawn sibling containers
2. **Matching host paths** (`-v "${HOST_PATH}:${HOST_PATH}"`) - Work directories resolve correctly between containers
3. **Symlink** - Makes `/workspaces/training/...` paths work locally

### Running Commands with DooD

```bash
docker exec -e LANG=C.UTF-8 -e LC_ALL=C.UTF-8 -e USER=testuser \
  -w "${HOST_PATH}/<working-dir>" \
  nf-training \
  nextflow run <script.nf> [options]
```

### When DooD is Needed

Any tutorial where processes specify containers:

- `hello_nextflow` (later lessons with containers)
- `nf4_science/genomics` and other domain modules
- Side quests: `essential_scripting_patterns`, `metadata`, etc.

---

## Apple Silicon (ARM) Macs

Most bioinformatics containers are built for x86_64/amd64. On ARM Macs, create a platform config:

```bash
docker exec nf-training bash -c 'cat > /tmp/platform.config << EOF
docker.runOptions = "--platform linux/amd64"
EOF'
```

Include when running:

```bash
docker exec -e LANG=C.UTF-8 -e LC_ALL=C.UTF-8 -e USER=testuser \
  -w "${HOST_PATH}/<working-dir>" \
  nf-training \
  nextflow run <script.nf> -c /tmp/platform.config
```

**Note**: Platform emulation uses more memory. For OOM errors (exit code 137), increase Docker Desktop memory in Preferences → Resources.

---

## Troubleshooting

| Error                                    | Cause               | Solution                                             |
| ---------------------------------------- | ------------------- | ---------------------------------------------------- |
| `Cannot connect to Docker daemon`        | Socket not mounted  | Add `-v /var/run/docker.sock:/var/run/docker.sock`   |
| `.command.sh: No such file or directory` | Path mismatch       | Use matching paths: `-v "${HOST_PATH}:${HOST_PATH}"` |
| `exec format error`                      | ARM/x86 mismatch    | Add `--platform linux/amd64` to docker.runOptions    |
| Exit code 137 (OOM)                      | Insufficient memory | Increase Docker Desktop memory allocation            |
| `Malformed input or unmappable chars`    | Missing UTF-8       | Add `-e LANG=C.UTF-8 -e LC_ALL=C.UTF-8`              |
| `Error: No such container: nf-training`  | Container stopped   | Restart container (see below)                        |

---

## Container Restart Procedure

The container may stop during long sessions. To restart:

```bash
# 1. Check if container is running
docker ps | grep nf-training

# 2. If not running, restart with DooD setup
docker stop nf-training 2>/dev/null; docker rm nf-training 2>/dev/null

HOST_PATH="${PWD}"
NXF_VER=$(grep -o '"NXF_VER":\s*"[^"]*"' .devcontainer/devcontainer.json | cut -d'"' -f4)

docker run -d --name nf-training \
  -e NXF_VER=${NXF_VER} \
  -e LANG=C.UTF-8 \
  -e LC_ALL=C.UTF-8 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v "${HOST_PATH}:${HOST_PATH}" \
  -w "${HOST_PATH}" \
  ghcr.io/nextflow-io/training:latest \
  sleep infinity

# 3. Recreate symlink (critical!)
docker exec nf-training bash -c "rm -rf /workspaces/training && mkdir -p /workspaces && ln -sf ${HOST_PATH} /workspaces/training"

# 4. Recreate platform config if needed (ARM Macs)
docker exec nf-training bash -c 'cat > /tmp/platform.config << EOF
docker.runOptions = "--platform linux/amd64"
EOF'
```

---

## Cleanup

When done with testing:

```bash
docker stop nf-training && docker rm nf-training
```

---

## Notes

- Always verify you're in the repository root before starting (check for `mkdocs.yml`)
- The container uses `sleep infinity` so it persists across multiple command executions
- Symlink must be recreated each time the container restarts
- For long sessions, periodically check container is still running: `docker ps | grep nf-training`
