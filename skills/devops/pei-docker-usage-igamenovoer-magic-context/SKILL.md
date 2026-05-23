---
name: pei-docker-usage
description: Helper for PeiDocker (`pei-docker-cli`). Trigger ONLY when the user explicitly requests PeiDocker usage OR when working within a PeiDocker-generated project (indicated by `user_config.yml`).
---

# PeiDocker Usage

## Overview

PeiDocker (`pei-docker-cli`) is a tool that automates the creation of Docker environments. Instead of writing complex `Dockerfile`s and `docker-compose.yml` files, you define your environment in a high-level YAML file (`user_config.yml`). PeiDocker then generates the necessary Docker configuration.

**Official Repository:** [https://github.com/igamenovoer/PeiDocker](https://github.com/igamenovoer/PeiDocker)

**Key Features:**
*   **Two-Stage Builds:** Separates system setup (`stage-1`) from application/dev setup (`stage-2`).
*   **Built-in SSH:** easy configuration of SSH access to containers.
*   **Dynamic Storage:** Seamlessly switch between host-mounted volumes (dev) and Docker volumes (deployment).
*   **Proxy Support:** Configure proxies for build and run time.

## Execution Strategy

When invoking `pei-docker-cli`, follow this priority order:

1.  **Project-Local (Pixi):** If working in a Pixi-managed project (check for `pyproject.toml` or `pixi.toml` with `pei-docker` dependency), use:
    ```bash
    pixi run pei-docker-cli ...
    ```
2.  **Global (uv):** Check for global installation:
    ```bash
    uv tool run pei-docker-cli ...
    ```
3.  **Fallback:** If neither is found, suggest installation:
    *   **In Pixi project:** `pixi add pei-docker`
    *   **Global usage:** `uv tool install pei-docker`

## Workflow

The standard workflow for using PeiDocker is:

### 1. Create a Project

Initialize a new PeiDocker project in a target directory.

```bash
pixi run pei-docker-cli create -p path/to/project_dir
```

This creates the directory structure and a template `user_config.yml`.

### 2. Configure (`user_config.yml`)

Edit the `user_config.yml` in the project directory to define your environment.

**Key Sections:**
*   `stage_1`: Base image settings (OS, system packages).
    *   `image`: Base image (e.g., `ubuntu:24.04`) and output tag.
    *   `ssh`: Enable SSH, set ports and users.
    *   `apt`: Configure apt mirrors (e.g., `tuna`, `aliyun`).
*   `stage_2`: Application/Developer settings.
    *   `storage`: Define where `/app`, `/data`, and `/workspace` map to (host paths or auto-volumes).
    *   `custom`: Scripts to run on build, first run, or login.

See [basic-examples.md](references/basic-examples.md) and [advanced-examples.md](references/advanced-examples.md) for detailed configuration examples.

### 3. Generate Docker Files

After editing `user_config.yml`, generate the `docker-compose.yml` and `Dockerfile`s.

```bash
# From within the project directory
cd path/to/project_dir
pixi run pei-docker-cli configure

# Or specifying the path
pixi run pei-docker-cli configure -p path/to/project_dir
```

### 4. Build and Run

Use standard `docker compose` commands to build and start the containers.

```bash
cd path/to/project_dir

# Build the images (progress=plain shows build logs)
docker compose build stage-1 --progress=plain
docker compose build stage-2 --progress=plain

# Run the container (usually stage-2 for development)
docker compose up -d stage-2
```

## Common Tasks

### Adding Custom Scripts

PeiDocker allows running scripts at various lifecycle stages. Scripts should be placed in `container-scripts/` (to run inside container) or `host-scripts/` (to run on host).

In `user_config.yml`:
```yaml
stage_2:
  custom:
    on_build:
      - 'stage-2/custom/install-my-app.sh'
    on_first_run:
      - 'stage-2/custom/setup-env.sh'
```

### Configuring SSH

To enable SSH access:

```yaml
stage_1:
  ssh:
    enable: true
    port: 22          # Container internal port
    host_port: 2222   # Host mapped port
    users:
      developer:
        password: 'password123'
        pubkey_file: '~' # Use current user's public key
```

## References

*   **[guidelines.md](references/guidelines.md)**: Best practices for project structure, data safety, and customization.
*   **[user-config-reference.md](references/user-config-reference.md)**: Full reference for `user_config.yml` options.
*   **[installation-scripts.md](references/installation-scripts.md)**: Usage guide for system installation scripts (Pixi, uv, Node.js, Bun).
*   **[user_config.yml](templates/user_config.yml)**: Template for a full `user_config.yml` file.
*   **[basic-examples.md](references/basic-examples.md)**: Basic configurations (SSH, GPU, Volumes).
*   **[advanced-examples.md](references/advanced-examples.md)**: Advanced scenarios (Env Vars, OpenGL, Complex Apps).
*   **[cli-reference.md](references/cli-reference.md)**: Detailed CLI command reference.