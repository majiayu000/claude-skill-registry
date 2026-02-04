---
name: sayt-cli
description: >
  How to write .mise.toml files with correct tool versions, settings, and platform stubs.
  Use when setting up project toolchains, fixing missing tools, or configuring sayt setup/doctor.
user-invocable: false
---

# setup / doctor — Tool Management with mise

`sayt setup` installs project toolchains. `sayt doctor` verifies each environment tier is ready.

## How It Works

1. `sayt setup` looks for `.mise.toml` in the current directory
2. Runs `mise trust -y -a -q` to trust the config
3. Runs `mise install` to install all specified tools
4. Preloads vscode-task-runner (`vtr`) into the uvx cache for offline use
5. If `.sayt.nu` exists, recursively calls it with `setup` for custom logic

`sayt doctor` checks which environment tiers have their required tools available:

| Tier | Tools checked |
|------|--------------|
| pkg | mise (or scoop on Windows) |
| cli | cue, gomplate |
| ide | vtr (vscode-task-runner) |
| cnt | docker |
| k8s | kind, skaffold |
| cld | gcloud |
| xpl | crossplane |

## `.mise.toml` File Format

mise uses TOML configuration to specify tool versions per project.

### Structure

```toml
[settings]
locked = true           # Use lockfile for reproducible installs
lockfile = true         # Generate/use mise.lock
experimental = true     # Enable experimental features
paranoid = false        # Disable paranoid mode

[tools]
# Standard registry tools
node = "22.14.0"
go = "1.22"
java = "openjdk-21.0"
python = "3.12"

# GitHub-hosted tools (not in default registry)
"github:pnpm/pnpm" = "9.15.2"
"github:sqlc-dev/sqlc" = "1.28.0"
"github:bufbuild/buf" = "1.32.1"
```

### Settings Reference

```toml
[settings]
locked = true                       # Require lockfile to exist
lockfile = true                     # Create/update mise.lock
experimental = true                 # Needed for some plugin features
paranoid = false                    # Don't verify checksums aggressively
github.slsa = false                 # Skip SLSA provenance verification
github.github_attestations = false  # Skip GitHub attestations
aqua.github_attestations = false    # Skip aqua GitHub attestations
aqua.cosign = false                 # Skip cosign verification
aqua.slsa = false                   # Skip aqua SLSA verification
aqua.minisign = false               # Skip minisign verification
```

These security settings are commonly disabled during development for speed. Enable them in CI/production.

### Common Tool Specs

**Node.js project:**
```toml
[tools]
node = "22.14.0"
"github:pnpm/pnpm" = "9.15.2"
```

**Go project:**
```toml
[tools]
go = "1.22"
"github:sqlc-dev/sqlc" = "1.28.0"
"github:gotestyourself/gotestsum" = "1.12.0"
```

**JVM project:**
```toml
[tools]
java = "openjdk-21.0"
```

**Python project:**
```toml
[tools]
python = "3.12"
```

**Multi-language project:**
```toml
[tools]
node = "22.14.0"
go = "1.22"
"github:bufbuild/buf" = "1.32.1"
```

### Platform-Specific Stubs

sayt uses mise "tool stubs" for tools like CUE, Docker, and uvx. These have platform-specific TOML configs:

- `cue.toml` — Standard CUE stub
- `cue.musl.toml` — Alpine/musl Linux variant
- `docker.toml` / `docker.musl.toml` — Docker stub
- `uvx.toml` / `uvx.musl.toml` — Python uvx stub
- `nu.toml` / `nu.musl.toml` — Nushell stub

The musl variant is automatically selected when running on musl-based Linux (e.g., Alpine containers).

## Custom Setup Logic via `.sayt.nu`

If your project needs setup beyond what mise provides, create `.sayt.nu`:

```nushell
# .sayt.nu — Custom setup hooks
def "main setup" [] {
    # Example: install Nix packages
    nix-env -iA nixpkgs.myTool

    # Example: run database migrations
    sqlc generate
}
```

sayt automatically detects and runs `.sayt.nu setup` after the mise-based setup completes.

## Writing Good `.mise.toml` Files

1. **Pin exact versions** — Use `"22.14.0"` not `"22"` for reproducibility
2. **Use lockfiles** — Set `locked = true` and `lockfile = true`
3. **Prefer registry names** — Use `node` not `"github:nodejs/node"` when available
4. **Use `github:` prefix** — For tools not in the default mise registry
5. **Keep settings section** — Even if using defaults, be explicit about security settings

## Current flags

!`sayt help setup 2>&1 || true`
!`sayt help doctor 2>&1 || true`
