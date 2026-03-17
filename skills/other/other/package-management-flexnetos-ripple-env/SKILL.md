---
name: package-management
description: Package conflict identification and Pixi-first dependency management
icon: 📦
category: development
tools:
  - pixi
  - pnpm
  - cargo
  - npm
  - yarn
---

# Package Management Skills

## Overview

This skill provides expertise in managing packages through Pixi as the central package manager, converting legacy npm/cargo commands to Pixi-wrapped equivalents, and resolving package conflicts.

## Pixi-First Philosophy

Pixi is the **primary package manager** for this repository. It manages:

- **Python packages** via conda-forge and PyPI
- **Node.js packages** via pnpm (pnpm is a conda-forge package that Pixi installs and manages; pnpm then handles Node.js package installation)
- **System tools** via conda-forge (cmake, ninja, etc.)
- **Rust toolchain** is provided by Nix; Pixi wraps cargo commands to ensure consistent environment variables and paths

### Why Pixi?

1. **Reproducibility** - Lock files ensure identical environments
2. **Cross-platform** - Works on Linux, macOS, and Windows
3. **Environment isolation** - Multiple environments for different use cases
4. **Conda ecosystem** - Access to conda-forge packages
5. **Task runner** - Define and run project tasks

## Command Conversion Reference

### npm → pixi pnpm

npm commands should be converted to use pnpm through Pixi:

```bash
# Package installation
npm install              → pixi run pnpm install
npm ci                   → pixi run pnpm install --frozen-lockfile
npm install <pkg>        → pixi run pnpm add <pkg>
npm install -D <pkg>     → pixi run pnpm add -D <pkg>
npm install -g <pkg>     → pixi run pnpm add -g <pkg>
npm uninstall <pkg>      → pixi run pnpm remove <pkg>

# Scripts
npm run <script>         → pixi run pnpm run <script>
npm test                 → pixi run pnpm test
npm start                → pixi run pnpm start
npm run build            → pixi run pnpm run build

# Package execution
npx <pkg>                → pixi run pnpm dlx <pkg>
npx create-react-app     → pixi run pnpm dlx create-react-app

# Information
npm list                 → pixi run pnpm list
npm outdated             → pixi run pnpm outdated
npm audit                → pixi run pnpm audit
```

### yarn → pixi pnpm

yarn commands are also converted to pnpm through Pixi:

```bash
yarn install             → pixi run pnpm install
yarn add <pkg>           → pixi run pnpm add <pkg>
yarn add -D <pkg>        → pixi run pnpm add -D <pkg>
yarn remove <pkg>        → pixi run pnpm remove <pkg>
yarn run <script>        → pixi run pnpm run <script>
yarn dlx <pkg>           → pixi run pnpm dlx <pkg>
```

### cargo → pixi cargo

Cargo commands should be wrapped with Pixi:

```bash
# Build
cargo build              → pixi run cargo build
cargo build --release    → pixi run cargo build --release
cargo build --target x   → pixi run cargo build --target x

# Test
cargo test               → pixi run cargo test
cargo test --lib         → pixi run cargo test --lib
cargo test -- --nocapture → pixi run cargo test -- --nocapture

# Run
cargo run                → pixi run cargo run
cargo run -- <args>      → pixi run cargo run -- <args>
cargo run --release      → pixi run cargo run --release

# Dependencies
cargo add <crate>        → pixi run cargo add <crate>
cargo remove <crate>     → pixi run cargo remove <crate>
cargo update             → pixi run cargo update

# Analysis
cargo tree               → pixi run cargo tree
cargo check              → pixi run cargo check
cargo clippy             → pixi run cargo clippy
cargo fmt                → pixi run cargo fmt

# Documentation
cargo doc                → pixi run cargo doc
cargo doc --open         → pixi run cargo doc --open
```

## Environment Selection

Different tasks require different Pixi environments:

```bash
# Frontend/JavaScript development
pixi run -e js pnpm install
pixi run -e js pnpm run dev
pixi run -e js pnpm run build

# Python development (default environment)
pixi run python script.py
pixi run pytest tests/

# CUDA/GPU workloads
pixi run -e cuda python train.py
pixi run -e cuda python -c "import torch; print(torch.cuda.is_available())"

# ROS2 robotics (default environment includes ROS)
pixi run ros2 --help
pixi run colcon build

# AIOS Agent development
pixi run -e aios python -m cerebrum run agents/aios/my-agent

# LLMOps evaluation
pixi run -e llmops mlflow ui
pixi run -e llmops python -c "import trulens"

# Documentation
pixi run -e docs mkdocs serve
pixi run -e docs mkdocs build
```

## Conflict Detection

### Common Conflict Patterns

1. **Version Coupling** - PyTorch/torchvision/torchaudio must match
   ```
   # PyTorch 2.5.x requires:
   torchvision 0.20.x
   torchaudio 2.5.x
   ```

2. **Python Version Constraints**
   - AIOS requires Python 3.10-3.11 (Python 3.12+ removed `pkgutil.ImpImporter` and other importlib APIs that AIOS depends on)
   - Most other environments use Python 3.11.x

3. **CUDA Version Mismatches**
   - System CUDA vs PyTorch CUDA version must be compatible
   - Check with: `pixi run -e cuda python -c "import torch; print(torch.version.cuda)"`

4. **Channel Conflicts**
   - robostack-humble and pytorch channels have incompatible expectations
   - Use separate solve-groups in pixi.toml

### Conflict Resolution Commands

```bash
# Check for conflicts in Pixi
pixi list                    # List all packages
pixi outdated                # Show outdated packages
pixi run pnpm list           # List Node.js packages
pixi run cargo tree          # Show Rust dependency tree

# Update lock files
pixi update                  # Update Pixi lock
pixi run pnpm update         # Update pnpm lock
pixi run cargo update        # Update Cargo lock

# Verify environments
pixi run pytest              # Test Python
pixi run -e js pnpm test     # Test Node.js
pixi run cargo test          # Test Rust
```

## Pixi Task Definitions

Define reusable tasks in `pixi.toml`:

```toml
[tasks]
# Frontend tasks
frontend-install = "pnpm -C frontend install"
frontend-dev = "pnpm -C frontend dev"
frontend-build = "pnpm -C frontend build"
frontend-check = "pnpm -C frontend check"
frontend-format = "pnpm -C frontend format"

# Rust tasks (if needed)
rust-build = { cmd = "cargo build", cwd = "rust" }
rust-test = { cmd = "cargo test", cwd = "rust" }
rust-release = { cmd = "cargo build --release", cwd = "rust" }

# Python tasks
python-test = "pytest test/ -v"
python-lint = "ruff check ."
python-format = "ruff format ."
```

## Best Practices

### Do

- ✅ Always use `pixi run` to execute commands
- ✅ Use the appropriate environment (`-e <env>`) for each task
- ✅ Define reusable tasks in `pixi.toml`
- ✅ Keep lock files in sync (`pixi.lock`, `pnpm-lock.yaml`)
- ✅ Use pnpm instead of npm for Node.js packages
- ✅ Check for conflicts before major dependency updates

### Don't

- ❌ Use bare `npm`, `yarn`, or `cargo` commands
- ❌ Install Node.js packages globally with npm
- ❌ Mix Python environments (use `-e <env>`)
- ❌ Commit `package-lock.json` (use `pnpm-lock.yaml`)
- ❌ Ignore version coupling requirements

## Troubleshooting

### "Command not found" in Pixi

```bash
# Ensure you're in a Pixi environment
pixi shell                   # Enter shell
# Or use pixi run explicitly
pixi run <command>
```

### Node.js package issues

```bash
# Clear pnpm cache and reinstall
rm -rf node_modules pnpm-lock.yaml
pixi run pnpm install
```

### Cargo/Rust issues

```bash
# The Rust toolchain comes from Nix (flake.nix devShell)
# When in a Nix shell, pixi run cargo commands use the Nix-provided toolchain
# This ensures consistent environment variables and paths

# Option 1: Use pixi run directly (if cargo is in PATH from Nix)
pixi run cargo build

# Option 2: Enter Nix shell first for complex builds
nix develop
# Then in the shell:
cargo build  # Uses Nix-provided cargo with Pixi environment vars
```

### Environment conflicts

```bash
# Use a specific environment to isolate conflicts
pixi run -e cuda python script.py      # For CUDA
pixi run -e aios python script.py      # For AIOS
pixi run -e default python script.py   # For ROS2
```

## Related Skills

- [Nix Environment](../nix-environment/SKILL.md) - Nix flakes and system packages
- [DevOps](../devops/SKILL.md) - CI/CD pipeline configuration
- [Rust Tooling](../rust-tooling/SKILL.md) - Rust development patterns

## Related Documentation

- [docs/CONFLICTS.md](../../docs/CONFLICTS.md) - Known conflict patterns
- [docs/PYTHON-ENVIRONMENTS.md](../../docs/PYTHON-ENVIRONMENTS.md) - Python environment details
- [pixi.toml](../../pixi.toml) - Pixi configuration
