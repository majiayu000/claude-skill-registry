---
name: flox
description: Reproducible development environments powered by Nix.
version: 1.0.0
---


# flox

Reproducible development environments powered by Nix.

**Repository**: https://github.com/flox/flox
**Documentation**: https://flox.dev/docs
**FloxHub**: https://hub.flox.dev

---

## Overview

Flox provides declarative, reproducible development environments using Nix as the package backend. Environments are defined in `manifest.toml` and can be shared via FloxHub.

```
.flox/
├── env/
│   └── manifest.toml    # Environment definition
├── env.json             # Environment metadata
└── env.lock             # Lockfile
```

---

## Installation

```bash
# macOS
brew install flox/flox/flox

# Linux
curl -fsSL https://downloads.flox.dev/by-env/stable/install | bash
```

---

## CLI Commands

### Environment Management

```bash
flox init                    # Create new environment
flox init -n myenv           # Named environment
flox init --auto-setup       # Auto-detect languages

flox activate                # Enter environment
flox activate -d ./path      # Activate in directory
flox activate -r user/env    # Activate remote environment

flox edit                    # Edit manifest.toml
flox edit -n newname         # Rename environment

flox delete                  # Delete environment
```

### Package Management

```bash
flox search ripgrep          # Search packages
flox show ripgrep            # Package details
flox install ripgrep         # Install package
flox uninstall ripgrep       # Remove package
flox list                    # List installed packages
flox upgrade                 # Upgrade packages
flox update                  # Update catalog
```

### Sharing (FloxHub)

```bash
flox auth login              # OAuth2 login
flox auth logout             # Remove token
flox auth status             # Check login status

flox push                    # Push to FloxHub
flox push --force            # Overwrite remote
flox pull user/env           # Pull from FloxHub
flox pull --force            # Overwrite local

flox envs                    # List environments
```

### Services

```bash
flox services start          # Start all services
flox services start db       # Start specific service
flox services stop           # Stop all services
flox services restart        # Restart services
flox services status         # Check service status
flox services logs db        # View logs
```

### Containerization

```bash
flox containerize            # Create container image
flox containerize -f out.tar # Output to file
flox containerize | docker load  # Pipe to Docker
```

---

## manifest.toml

Complete manifest reference:

```toml
# ═══════════════════════════════════════════════════════════════════
# VERSION
# ═══════════════════════════════════════════════════════════════════

version = 1

# ═══════════════════════════════════════════════════════════════════
# INSTALL - Packages to install
# ═══════════════════════════════════════════════════════════════════

[install]
ripgrep.pkg-path = "ripgrep"
nodejs.pkg-path = "nodejs"
python.pkg-path = "python312"
pip.pkg-path = "python312Packages.pip"

# With version constraints
jq.pkg-path = "jq"
jq.version = "^1.7"

# ═══════════════════════════════════════════════════════════════════
# VARS - Environment variables
# ═══════════════════════════════════════════════════════════════════

[vars]
DATABASE_URL = "postgres://localhost:5432/mydb"
NODE_ENV = "development"
GAY_SEED = "1069"

# ═══════════════════════════════════════════════════════════════════
# HOOK - Scripts run on activation
# ═══════════════════════════════════════════════════════════════════

[hook]
on-activate = """
    echo "Activating $FLOX_ENV_DESCRIPTION..."
    
    # Create Python venv
    if [ ! -d .venv ]; then
        python -m venv .venv
    fi
    
    # Export dynamic variables
    export VENV_DIR="$PWD/.venv"
    
    # Start background processes
    eval "$(ssh-agent)"
"""

# ═══════════════════════════════════════════════════════════════════
# PROFILE - Shell-specific scripts
# ═══════════════════════════════════════════════════════════════════

[profile]
common = """
    echo "Welcome to the environment"
"""

bash = """
    source .venv/bin/activate
    alias ll="ls -la"
    set -o vi
"""

zsh = """
    source .venv/bin/activate
    alias ll="ls -la"
    bindkey -v
"""

fish = """
    source .venv/bin/activate.fish
    alias ll="ls -la"
"""

# ═══════════════════════════════════════════════════════════════════
# SERVICES - Background services
# ═══════════════════════════════════════════════════════════════════

[services.postgres]
command = "postgres -D $PGDATA"
vars.PGDATA = "$FLOX_ENV_CACHE/pgdata"
vars.PGPORT = "5432"

[services.redis]
command = "redis-server"
vars.REDIS_PORT = "6379"

[services.api]
command = "npm run dev"
is-daemon = false

[services.worker]
command = "./worker.sh"
is-daemon = true
shutdown.command = "pkill -f worker.sh"

# ═══════════════════════════════════════════════════════════════════
# OPTIONS - Environment behavior
# ═══════════════════════════════════════════════════════════════════

[options]
systems = ["aarch64-darwin", "x86_64-linux"]
cuda-detection = false

[options.allow]
broken = false
unfree = true
licenses = ["MIT", "Apache-2.0"]

# ═══════════════════════════════════════════════════════════════════
# INCLUDE - Compose with other environments
# ═══════════════════════════════════════════════════════════════════

[[include.environments]]
# Remote environment from FloxHub
name = "bmorphism/effective-topos"

[[include.environments]]
# Local environment
dir = "../shared-tools"

# ═══════════════════════════════════════════════════════════════════
# CONTAINERIZE - Container image config
# ═══════════════════════════════════════════════════════════════════

[containerize.config]
cmd = ["/bin/bash", "-c", "flox activate -- npm start"]
exposed-ports = ["3000/tcp", "5432/tcp"]
```

---

## Environment Types

| Type | Location | Remote Sync | Use Case |
|------|----------|-------------|----------|
| **PathEnvironment** | Local `.flox/` | No | Personal development |
| **ManagedEnvironment** | Local + FloxHub | Yes | Team collaboration |
| **RemoteEnvironment** | FloxHub only | Read-only | Quick access |

---

## FloxHub Workflow

### Push to FloxHub

```bash
# First time - creates managed environment
flox push

# Subsequent pushes sync changes
flox edit
flox push

# Force overwrite remote
flox push --force
```

### Pull from FloxHub

```bash
# Clone remote environment
flox pull bmorphism/effective-topos

# Update existing managed environment
flox pull

# Force overwrite local
flox pull --force

# Copy without remote link
flox pull bmorphism/effective-topos --copy
```

### Activate Remote

```bash
# Temporary activation (no local clone)
flox activate -r bmorphism/effective-topos
```

---

## Services

Services use `process-compose` as the backend orchestrator.

### Service Descriptor Options

| Option | Type | Description |
|--------|------|-------------|
| `command` | String | Bash command to start service |
| `vars` | Map | Service-specific environment variables |
| `is-daemon` | Bool | Service spawns background process |
| `shutdown.command` | String | Command to stop service (required if is-daemon) |
| `systems` | List | Compatible systems |

### Service Lifecycle

```bash
# Start all services
flox services start

# Check status
flox services status
# NAME      STATUS    PID
# postgres  Running   12345
# redis     Running   12346
# api       Stopped   -

# Stop specific service
flox services stop postgres

# Restart with new config
flox edit  # modify manifest
flox services restart
```

---

## Environment Composition

Include other environments for modularity:

```toml
[[include.environments]]
name = "bmorphism/effective-topos"  # Remote

[[include.environments]]
dir = "../base-tools"               # Local

[[include.environments]]
name = "company/shared-config"
```

### Merge Priority (lowest to highest)

1. First included environment
2. Subsequent included environments
3. Current manifest (highest priority)

### Merge Behavior

| Section | Behavior |
|---------|----------|
| `[install]` | Overwrite by ID |
| `[vars]` | Overwrite by key |
| `[hook]` | Append (lower → higher) |
| `[profile]` | Append (lower → higher) |
| `[services]` | Overwrite by name |
| `[options]` | Deep merge |

---

## Integration with Music-Topos

### FloxHub Publications

| Environment | Contents |
|-------------|----------|
| `bmorphism/effective-topos` | 606 man pages, 97 info manuals, guile, ghc, cargo |
| `bmorphism/ies` | Babashka, Julia, ffmpeg, tailscale |

### Activation

```bash
# Pull and activate
flox pull bmorphism/effective-topos -d ~/.topos
flox activate -d ~/.topos

# Or remote activation
flox activate -r bmorphism/effective-topos
```

### Gay.jl Integration

```toml
[vars]
GAY_SEED = "1069"
GAY_PORT = "42069"

[services.gay-mcp]
command = "julia --project=@gay -e 'using Gay; Gay.serve_mcp()'"
vars.GAY_INTERVAL = "30"
```

---

## Key Directories

```bash
$FLOX_ENV              # Current environment path
$FLOX_ENV_CACHE        # Persistent cache (~/.cache/flox/...)
$FLOX_ENV_PROJECT      # Project root
$FLOX_ENV_DESCRIPTION  # Human-readable name
```

---

## Examples

### Python Development

```toml
[install]
python.pkg-path = "python312"
pip.pkg-path = "python312Packages.pip"
uv.pkg-path = "uv"

[hook]
on-activate = """
    if [ ! -d .venv ]; then
        uv venv .venv
    fi
    source .venv/bin/activate
    uv pip install -r requirements.txt
"""
```

### Node.js + PostgreSQL

```toml
[install]
nodejs.pkg-path = "nodejs_20"
postgresql.pkg-path = "postgresql_15"

[vars]
DATABASE_URL = "postgres://localhost:5432/dev"

[services.db]
command = "postgres -D $PGDATA -k $FLOX_ENV_CACHE"
vars.PGDATA = "$FLOX_ENV_CACHE/pgdata"

[hook]
on-activate = """
    if [ ! -d "$PGDATA" ]; then
        initdb -D "$PGDATA"
    fi
"""
```

### Rust + Cargo

```toml
[install]
rustc.pkg-path = "rustc"
cargo.pkg-path = "cargo"
rust-analyzer.pkg-path = "rust-analyzer"

[vars]
CARGO_HOME = "$FLOX_ENV_CACHE/cargo"
RUSTUP_HOME = "$FLOX_ENV_CACHE/rustup"
```

---

## References

- GitHub: https://github.com/flox/flox
- Documentation: https://flox.dev/docs
- FloxHub: https://hub.flox.dev
- DeepWiki: https://deepwiki.com/flox/flox



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `general`: 734 citations in bib.duckdb

## Cat# Integration

This skill maps to **Cat# = Comod(P)** as a bicomodule in the equipment structure:

```
Trit: 0 (ERGODIC)
Home: Prof
Poly Op: ⊗
Kan Role: Adj
Color: #26D826
```

### GF(3) Naturality

The skill participates in triads satisfying:
```
(-1) + (0) + (+1) ≡ 0 (mod 3)
```

This ensures compositional coherence in the Cat# equipment structure.