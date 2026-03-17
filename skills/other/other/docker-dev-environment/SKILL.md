---
name: docker-dev-environment
description: "Creates an isolated Docker-based development environment for any project. Wraps a repo in a scaffolding repo with a Dockerfile and container.sh script for building, running, testing, and shelling into the project. Use when asked to dockerize a dev environment, isolate a project, or set up a container-based workflow."
---

# Docker Dev Environment

Creates an isolated, reproducible Docker-based development environment for any project. The approach wraps the target repo inside a "wrapper" repo that contains a Dockerfile and a standardized `container.sh` script to drive ephemeral containers for building, running, testing, and debugging.

## Why This Approach

- **Isolation**: transitive dependencies cannot access the host system beyond the mounted project directory
- **Reproducibility**: all build deps are captured in a Dockerfile, version-controlled in the wrapper repo
- **Independence**: the wrapper is separate from the upstream project; customizations don't pollute the original repo
- **Simplicity**: requires only Docker and bash knowledge; no exotic tooling

## Workflow

### Step 1: Create the Wrapper Repo Structure

Starting from the directory containing the target project (or where it will be cloned):

1. Determine the project name (from directory name or git remote URL)
2. Create a wrapper directory named `<project>-wrapper/`
3. If the project is already cloned elsewhere, instruct the user to clone/move it into the wrapper as a subdirectory. If a git URL is provided, clone it into the wrapper.
4. The final structure MUST be:

```
<project>-wrapper/
├── <project>/          # the actual project repo (nested, gitignored)
├── Dockerfile
├── container.sh        # executable (chmod +x)
├── .gitignore
└── README.md
```

5. Create `.gitignore` with:
```
<project>/
.cache/
```

6. Create a short `README.md`:
```markdown
# <project> wrapper repo

Docker-based dev environment for <project>.

## Usage

    ./container.sh docker   # Build/rebuild the Docker image
    ./container.sh build    # Build the project
    ./container.sh run      # Run the project
    ./container.sh test     # Run tests
    ./container.sh sh       # Open a shell in the container
```

7. Initialize git in the wrapper directory and make an initial commit with the README and .gitignore.

### Step 2: Analyze the Project

Scan the project subdirectory to determine:

**Build system detection** — check for these files (in order of priority):

| File(s) | Language/System | Build Command | Test Command |
|---------|----------------|---------------|-------------|
| `Cargo.toml` | Rust | `cargo build` | `cargo test` |
| `package.json` | Node.js | `npm run build` or `pnpm build` or `yarn build` | `npm test` or equivalent |
| `go.mod` | Go | `go build ./...` | `go test ./...` |
| `pyproject.toml`, `requirements.txt`, `setup.py` | Python | `pip install -e .` | `pytest` |
| `CMakeLists.txt` | C/C++ (CMake) | `cmake -S . -B build && cmake --build build -j$(nproc)` | `ctest --test-dir build` |
| `meson.build` | C/C++ (Meson) | `meson setup build && ninja -C build` | `meson test -C build` |
| `Makefile` (without CMakeLists.txt) | C/C++ (Make) | `make -j$(nproc)` | `make test` |
| `configure.ac` | C/C++ (Autotools) | `./autogen.sh && ./configure && make -j$(nproc)` | `make check` |
| `pom.xml` | Java (Maven) | `mvn package` | `mvn test` |
| `build.gradle` or `build.gradle.kts` | Java/Kotlin (Gradle) | `./gradlew build` | `./gradlew test` |
| `Gemfile` | Ruby | `bundle install` | `bundle exec rake test` |
| `mix.exs` | Elixir | `mix deps.get && mix compile` | `mix test` |
| `composer.json` | PHP | `composer install` | `vendor/bin/phpunit` |

**Also read** (if they exist, truncate at 4000 chars each):
- `README*`, `BUILDING*`, `CONTRIBUTING*`, `INSTALL*`, `DEVELOPMENT*`
- Any existing `Dockerfile` or `docker-compose*` (to learn what deps the project already knows about)
- Any `devcontainer.json`
- `flake.nix`, `shell.nix` (to extract dependency lists)

Use this information to determine:
- Exact build, test, and run commands
- Required OS packages (apt)
- Required toolchain versions
- Language-specific cache directories
- Any ports that need forwarding
- Any environment variables required

**If commands are ambiguous or unclear, use TODO placeholders** rather than guessing. The user or a subsequent agent can fill them in.

**Package manager detection for Node.js**:
- `pnpm-lock.yaml` → use `pnpm`
- `yarn.lock` → use `yarn`
- `bun.lockb` → use `bun`
- `package-lock.json` → use `npm ci`
- Otherwise → use `npm install`

### Step 3: Generate the Dockerfile

Use `reference/Dockerfile.base` as the starting template. Rules:

1. **Base image**: `ubuntu:24.04` (preferred) or `debian:stable-slim`
2. **First layer**: `RUN apt update && apt upgrade -y`
3. **Common essentials**: `ca-certificates`, `curl`, `git`, `build-essential`, `pkg-config`
4. **Language toolchains** (install ONLY what the project needs):

**Rust**:
```dockerfile
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"
```

**Node.js** (via NodeSource):
```dockerfile
RUN curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - \
    && apt install -y nodejs
# If pnpm: RUN npm install -g pnpm
# If yarn: RUN npm install -g yarn
```

**Python**:
```dockerfile
RUN apt install -y python3 python3-venv python3-pip
```

**Go**:
```dockerfile
RUN curl -fsSL https://go.dev/dl/go1.23.0.linux-amd64.tar.gz | tar -C /usr/local -xzf -
ENV PATH="/usr/local/go/bin:/root/go/bin:${PATH}"
```
(Adjust version based on `go.mod` if version is specified)

**C/C++ (CMake)**:
```dockerfile
RUN apt install -y cmake ninja-build
```

**Java**:
```dockerfile
RUN apt install -y openjdk-17-jdk
```

5. **NO** `ENTRYPOINT`, `CMD`, `WORKDIR`, or `USER` directives
6. **Clean apt cache** in the final layer: `rm -rf /var/lib/apt/lists/*`
7. Add project-specific packages identified from docs/lockfiles
8. Use separate `RUN` layers for clarity (one per logical group)

### Step 4: Generate container.sh

Use `reference/container.sh.generic` as the starting template. Customize it for the detected project:

**Required substitutions**:
- `__PROJECT_DIR__`: name of the project subdirectory
- `__IMAGE_NAME__`: `<project>-dev` (lowercase, hyphens only)
- `__CONTAINER_HOSTNAME__`: `<project>-dev-container`
- `__BUILD_CMD_PLACEHOLDER__`: actual build command
- `__TEST_CMD_PLACEHOLDER__`: actual test command
- `__RUN_CMD_PLACEHOLDER__`: actual run command (or TODO)
- `__ENV_SETUP_PLACEHOLDER__`: any env setup needed before commands (e.g., `. "$HOME/.cargo/env"` for Rust, `source /app/.venv/bin/activate` for Python venvs)

**Cache directory mounts** (`__CACHE_DIRS_PLACEHOLDER__` and `__MOUNT_PLACEHOLDER__`):

| Language | Host Dir (in wrapper) | Container Mount |
|----------|----------------------|-----------------|
| Rust | `.cache/cargo` | `/root/.cargo` |
| Rust (target) | `.cache/target` | `/app/target` |
| Node (npm) | `.cache/npm` | `/root/.npm` |
| Node (pnpm) | `.cache/pnpm` | `/root/.local/share/pnpm/store` |
| Python (pip) | `.cache/pip` | `/root/.cache/pip` |
| Python (venv) | `.cache/venv` | `/app/.venv` |
| Go (pkg) | `.cache/go-pkg` | `/root/go/pkg` |
| Go (build) | `.cache/go-build` | `/root/.cache/go-build` |
| C/C++ (ccache) | `.cache/ccache` | `/root/.ccache` |
| C/C++ (vcpkg) | `.cache/vcpkg` | `/root/.vcpkg` |
| Java (maven) | `.cache/m2` | `/root/.m2` |
| Java (gradle) | `.cache/gradle` | `/root/.gradle` |

**Port forwarding** (`__PORT_PLACEHOLDER__`):
- Web projects: `-p 3000:3000` (or whatever port docs specify)
- Only add if the project serves HTTP or has a UI

**The script MUST**:
- Use `set -euo pipefail`
- Create cache directories if they don't exist (in `ensure_cache_dirs`)
- Use `--rm -it` for ephemeral interactive containers
- Use `--cap-add=SYS_PTRACE` for debugging support
- Warn (not error) if rootful Docker is detected
- Set container hostname
- Run all commands with `bash -c` and prepend any env setup
- Be marked executable (`chmod +x`)

### Step 5: Commit the Wrapper

After generating all files:
1. `git add` all wrapper files (Dockerfile, container.sh, .gitignore, README.md)
2. Commit with message: `auto: add Dockerfile + container.sh`

### Step 6: Verify

Run these checks:
1. `./container.sh docker` — confirm the Docker image builds successfully
2. `./container.sh sh` — confirm a shell opens in the container with the project mounted at `/app`
3. `./container.sh build` — attempt to build (may need manual fixes)

If the image build fails, read the error output and fix the Dockerfile (usually missing apt packages). Iterate until the image builds.

## Handling Special Cases

**Multiple languages in one repo** (monorepo):
- Identify the primary language from docs or the root build file
- Install all detected toolchains in the Dockerfile
- Set build/test/run to the primary language's commands
- Add TODO comments for secondary language commands

**Projects with existing Dockerfile/docker-compose**:
- Read them to extract dependency information
- Do NOT reuse them as-is; generate a fresh dev-focused Dockerfile
- The existing Dockerfile is likely for production, not development

**GUI applications** (need display forwarding):
- Add Wayland/X11 socket passthrough only if the project is a GUI app
- For Wayland: pass `WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, mount the Wayland socket
- For X11: pass `DISPLAY`, mount `/tmp/.X11-unix`
- Mount GPU render nodes: `/dev/dri/renderD*`
- This is advanced; add TODO comments and let the user customize

**Projects needing services (databases, etc.)**:
- Out of scope for the basic wrapper
- Add a TODO comment in container.sh suggesting docker-compose for multi-service setups

## Done Checklist

After applying this skill, verify:

- [ ] Wrapper directory exists with correct structure
- [ ] `.gitignore` ignores the project subdirectory and `.cache/`
- [ ] Dockerfile installs only detected dependencies (no kitchen sink)
- [ ] Dockerfile has NO `ENTRYPOINT`, `CMD`, `WORKDIR`, or `USER`
- [ ] `container.sh` is executable and implements all 5 commands (docker, build, run, test, sh)
- [ ] Cache directories are mounted for the detected language
- [ ] Wrapper repo has an initial git commit
- [ ] Docker image builds successfully
- [ ] `./container.sh sh` opens a shell with project at `/app`
