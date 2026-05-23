---
name: pixi-make-cu-build-env
description: Guides the agent to setup a new or existing Pixi environment for compiling C++ and CUDA code. It ensures the correct compilers, toolkits, and CMake configurations are in place for a robust user-space build.
---

# Pixi Make CUDA Build Env

## Trigger

Use this skill when the user asks to:
- "Setup a CUDA build environment in this project"
- "Prepare the current Pixi project for compiling .cu files"
- "Add CUDA compilation support to <project_path>"

## Workflow

### 1. Requirements Gathering
**Mandatory**: You MUST identify:
1.  **Project Context**: The existing Pixi project path. (Default to current working directory if valid).
2.  **Manifest File**: Identify if the project uses `pixi.toml` or `pyproject.toml`.
3.  **Target Environment Name**: "Which Pixi environment should this be set up in?"
    *   *Default*: If not specified, assume the `default` environment.
    *   *Named*: If the user provides a name (e.g., `cuda-12`), use that feature.
4.  **CUDA Version**: "Which CUDA version do you need?" (e.g., 11.8, 12.1).
5.  **Host Tools**: Check if `cmake`, `ninja`, and a C++ compiler are available and suitable.
    *   *Action*: Run `cmake --version`, `ninja --version`, and check for `gcc`/`clang` (Linux) or `cl` (Windows).
    *   *Decision*: If missing or old, include them in the Pixi environment.

6.  **Tools**: "Do you need profiling/debugging tools like `nsight-compute`?"

### 2. Conflict Detection & Resolution
Before modifying the project, verify the current state of `<MANIFEST_FILE>`.
*   **Check**: Are there existing CUDA libs (`cuda-toolkit`, `cudnn`)? Is the `nvidia` channel prioritized? Are versions conflicting?
*   **Conflict Logic**: If conflicts are detected (e.g., `conda-forge` prioritized, incompatible pins):
    *   **Autonomous Check**: Did the user say "adjust settings", "proceed without asking", or "do what you have to"?
        *   *Yes*: **Automatically proceed** with **Option 1** (New Env) for safety, or **Option 2** (Force) if the user explicitly asked to fix *this* environment.
    *   **Manual Resolution**: If no authorization, **STOP** and offer:
        1.  **Create New Environment (Recommended)**: Create a separate environment (e.g., `cu<VERSION>-build`) with its own `solve-group` to isolate dependencies.
        2.  **Force Adjust (Risky)**: Reorder channels and overwrite pins in the target environment. **Warn**: This may break existing code.
        3.  **Cancel**: Abort the operation.
        4.  **Custom**: Ask the user for specific instructions on how to handle the conflict.

### 3. Adding Dependencies (Based on Selection)
Execute the workflow corresponding to the user's choice.

#### Option 1: New Isolated Environment (Recommended)
Create a new feature and environment with a dedicated `solve-group`.

```bash
# 1. Add Feature with Dependencies (Pin channel to nvidia)
pixi add --manifest-path <MANIFEST_FILE> --feature <NEW_ENV_NAME> --channel nvidia \
    cmake ninja cxx-compiler make pkg-config \
    cuda-toolkit=<VERSION> cuda-nvcc=<VERSION> \
    [cudnn nccl nsight-compute]

# 2. Create Environment with Dedicated Solve-Group
# (Use 'pixi workspace environment add' or edit manifest manually if CLI lacks support)
# TOML equivalent:
# [tool.pixi.environments]
# <NEW_ENV_NAME> = { features = ["<NEW_ENV_NAME>"], solve-group = "<NEW_ENV_NAME>" }
```

#### Option 2: Force Adjust Existing
**Best Practice**: Always add the `nvidia` channel to the project configuration *before* installing packages.

**Command Logic**:
*   **Default Environment**: Do NOT use `--feature`.
*   **Named Environment**: Use `--feature <ENV_NAME>`.

```bash
# 1. Setup Channels (Prioritize NVIDIA)
pixi project channel add nvidia --prepend --manifest-path <PROJECT_PATH>/<MANIFEST_FILE>

# 2. Core Build Tools
pixi add --manifest-path <PROJECT_PATH>/<MANIFEST_FILE> [--feature <ENV_NAME>] cmake ninja cxx-compiler make pkg-config

# 3. CUDA Toolchain
pixi add --manifest-path <PROJECT_PATH>/<MANIFEST_FILE> [--feature <ENV_NAME>] cuda-toolkit=<VERSION> cuda-nvcc=<VERSION>
```

*Optional Extras/Tools (Only if requested):*
```bash
pixi add --manifest-path <PROJECT_PATH>/<MANIFEST_FILE> [--feature <ENV_NAME>] cudnn=<VERSION> nccl=<VERSION> nsight-compute
```

### 4. Configuring Build Tasks
Add a standard CMake build task to `<MANIFEST_FILE>`.
*   **Note**: Tasks typically run in the activated environment. Ensure `CMAKE_CUDA_COMPILER` points to the *Pixi-managed* `nvcc` ($CONDA_PREFIX/bin/nvcc).

**Task Definition:**
```toml
[tool.pixi.tasks]
configure = { cmd = "cmake -G Ninja -S . -B build -DCMAKE_CUDA_COMPILER=$CONDA_PREFIX/bin/nvcc -DCUDAToolkit_ROOT=$CONDA_PREFIX", env = { CUDACXX = "$CONDA_PREFIX/bin/nvcc" } }
build = "cmake --build build"
test = "ctest --test-dir build"
```

### 5. Verification (Automated)
To verify the setup, deploy the self-contained test suite from the skill's resource directory.

**1. Deploy Test Suite:**
Check if the project has a `tmp/` directory. If so, place the verification project there to keep the root clean.
```bash
# Determine verification path
TARGET_DIR="build-check"
if [ -d "tmp" ]; then TARGET_DIR="tmp/build-check"; fi

# Deploy
mkdir -p "$TARGET_DIR"
cp -r magic-context/skills/tools/pixi/pixi-make-cu-build-env/demo-code/* "$TARGET_DIR"/
chmod +x "$TARGET_DIR/build-and-run.sh"
```

**2. Execute:**
Run the script using the configured environment. The script automatically handles source path detection.
```bash
pixi run --manifest-path <MANIFEST_FILE> [--feature <ENV_NAME>] "$TARGET_DIR/build-and-run.sh"
```
*   **Note**: If the host has no GPU or an incompatible driver, the **build step** should still succeed, but the binary execution will fail. In this case, verify that `$TARGET_DIR/build/check_app` exists to confirm the compilation setup.

## Troubleshooting

### CMake Errors
*   **Source Directory**: The provided `build-and-run.sh` handles directory context automatically. If you see errors about missing `CMakeLists.txt`, ensure you haven't moved the script out of the verification directory.
*   **Pthread Failure**: `Performing Test CMAKE_HAVE_LIBC_PTHREAD - Failed` is often normal; CMake usually finds `pthread` in the next step.
*   **Architecture Warnings**: `nvcc warning : Support for offline compilation...` indicates the default architecture might be older. You can safely ignore this warning for verification purposes.

### Runtime Errors
*   **Driver Mismatch**: If the kernel fails to launch, check `nvidia-smi`. The host driver must support the installed CUDA Toolkit version.

## Best Practices
*   **Never mix channels** for CUDA: Stick to `nvidia` for `cuda-*` packages.
*   **Explicit Compilation**: Always prefer passing `-DCMAKE_CUDA_COMPILER` over relying on implicit path resolution, as CMake might pick up `/usr/bin/nvcc`.
*   **User Space**: Remind the user that this setup requires NO `sudo` and works on any Linux machine with a driver.
