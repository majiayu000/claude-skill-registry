---
name: cross-platform-guardian
description: Ensure cross-platform compatibility across macOS (Intel/ARM), Ubuntu, and Fedora for this dotfiles repository. Detects and auto-fixes hardcoded paths, platform-specific assumptions, package availability issues, and test coverage gaps. Use when adding features, updating configs, bumping Nix flake, or investigating platform-specific bugs. Keywords: cross-platform, compatibility, macOS, Linux, Ubuntu, Fedora, platform, portability, Nix flake, Docker test, CI
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Cross-Platform Guardian

Maintains cross-platform compatibility across macOS (Intel/ARM), Ubuntu, and Fedora by detecting issues, auto-fixing violations, and ensuring reproducibility through Nix + Docker testing.

## Activation Triggers

Use this skill when:
- Adding new scripts, configs, or features
- Updating `flake.nix` or `flake.lock`
- Investigating platform-specific failures in CI
- Refactoring installation/setup logic
- User mentions: "compatibility", "cross-platform", "works on Mac but not Linux", "CI failing on Fedora"

## Core Responsibilities

### 1. Compatibility Audit

**Scan for anti-patterns:**

**Hardcoded paths:**
```bash
# ❌ BAD
DOTFILES_DIR="/Users/wcygan/Development/dotfiles"
CONFIG_PATH="/home/user/.config"

# ✅ GOOD
DOTFILES_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG_PATH="${XDG_CONFIG_HOME:-$HOME/.config}"
```

**Platform-specific commands without fallback:**
```bash
# ❌ BAD
open README.md  # macOS only

# ✅ GOOD
if [[ "$OSTYPE" == "darwin"* ]]; then
  open README.md
else
  xdg-open README.md
fi
```

**Architecture assumptions:**
```bash
# ❌ BAD
HOMEBREW_PATH="/opt/homebrew"  # ARM only

# ✅ GOOD
if [[ -d "/opt/homebrew" ]]; then
  HOMEBREW_PATH="/opt/homebrew"  # Apple Silicon
elif [[ -d "/usr/local/Homebrew" ]]; then
  HOMEBREW_PATH="/usr/local"     # Intel Mac
fi
```

**Shell assumptions:**
```bash
# ❌ BAD - assumes bash arrays work everywhere
declare -a packages=(git fish)

# ✅ GOOD - POSIX-compatible or gated
if [[ -n "$BASH_VERSION" ]]; then
  declare -a packages=(git fish)
fi
```

### 2. Platform Detection Validation

**Verify multi-layer detection exists:**

**In bash scripts (`install.sh`, `scripts/*.sh`):**
```bash
if [[ "$OSTYPE" == "darwin"* ]]; then
  echo "macOS detected"
elif [[ -f /etc/fedora-release ]]; then
  echo "Fedora detected"
elif [[ -f /etc/lsb-release ]] && grep -q Ubuntu /etc/lsb-release; then
  echo "Ubuntu detected"
elif [[ -f /etc/os-release ]]; then
  echo "Generic Linux detected"
else
  echo "⚠️  Unsupported OS - proceeding with defaults"
fi
```

**In Fish configs (`config/fish/conf.d/*.fish`):**
```fish
switch (uname)
  case Darwin
    # macOS logic
  case Linux
    # Linux logic
end
```

**Container detection:**
```bash
if [[ -f /.dockerenv ]] || [[ -n "$container" ]] || ! command -v systemctl &>/dev/null; then
  IS_CONTAINER=true
fi
```

### 3. Nix Flake Compatibility

**Check `flake.nix` supports all target architectures:**
```nix
allSystems = [
  "x86_64-linux"   # Intel/AMD Linux
  "aarch64-linux"  # ARM Linux
  "x86_64-darwin"  # Intel Mac
  "aarch64-darwin" # Apple Silicon
];
```

**Validate package availability:**
- After updating `flake.lock`, check if any packages fail on specific platforms
- Use `nix flake show` to verify outputs for all systems
- Run `scripts/test-platform-compatibility.sh` (create if missing)

**Auto-fix strategy for unavailable packages:**
```nix
# Add platform-specific conditionals if needed
packages = with pkgs; [
  git fish starship  # Universal
] ++ lib.optionals stdenv.isDarwin [
  # macOS-specific packages
] ++ lib.optionals stdenv.isLinux [
  # Linux-specific packages
];
```

### 4. Path Standardization

**XDG Base Directory compliance:**

| Config Type | macOS | Linux | Standard |
|------------|-------|-------|----------|
| Fish | `~/.config/fish` | `~/.config/fish` | ✅ XDG |
| Starship | `~/.config/starship.toml` | `~/.config/starship.toml` | ✅ XDG |
| VSCode | `~/Library/Application Support/Code/User` | `~/.config/Code/User` | ❌ Platform-specific |
| tmux | `~/.tmux.conf` | `~/.tmux.conf` | ❌ Legacy |

**Detection pattern in `scripts/link-config.sh`:**
```bash
if [[ "$OSTYPE" == "darwin"* ]]; then
  VSCODE_DIR="$HOME/Library/Application Support/Code/User"
else
  VSCODE_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/Code/User"
fi
```

### 5. CI/CD Test Coverage

**Verify GitHub Actions matrix includes:**
```yaml
# .github/workflows/ci.yml
jobs:
  docker-matrix:
    strategy:
      matrix:
        include:
          - os: ubuntu-25.04
            dockerfile: tests/Dockerfile.ubuntu
          - os: fedora-40
            dockerfile: tests/Dockerfile.fedora

  native-test:
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest]
```

**Test script validation (`tests/docker-test-commands.fish`):**
- Must have conditional checks: `if type -q <tool>`
- Must not assume specific paths
- Must handle missing tools gracefully

### 6. Auto-Fix Workflow

When compatibility issues detected:

**Step 1: Identify violations**
```bash
# Use scripts/audit-compatibility.sh (create if missing)
grep -r "/Users/wcygan" scripts/ config/
grep -r "open " scripts/ | grep -v "xdg-open"
```

**Step 2: Apply fixes automatically**
```bash
# Fix hardcoded paths
sed -i.bak 's|/Users/wcygan/Development/dotfiles|$(cd "$(dirname "${BASH_SOURCE[0]}")/.." \&\& pwd)|g' scripts/*.sh

# Fix platform-specific commands
# Use Edit tool to replace `open` with conditional logic
```

**Step 3: Validate fixes**
```bash
make test-pre          # Local syntax checks
make test-docker       # Docker matrix (Ubuntu + Fedora)
```

**Step 4: Update tests**
- Add regression test for fixed issue in `tests/docker-test-commands.fish`
- Document fix in commit message with `fix(compat): <description>`

### 7. Nix Flake Update Protocol

When user requests flake update or this skill detects outdated lock:

**Step 1: Update flake.lock**
```bash
nix flake update
```

**Step 2: Test across all platforms in CI**
```bash
# Trigger CI workflow or run locally
make test-docker  # Tests Ubuntu + Fedora
```

**Step 3: Check for package availability issues**
```bash
# Attempt build for each system
nix build .#packages.x86_64-linux.default --dry-run
nix build .#packages.aarch64-linux.default --dry-run
nix build .#packages.x86_64-darwin.default --dry-run
nix build .#packages.aarch64-darwin.default --dry-run
```

**Step 4: Handle failures**
- If package unavailable on platform → add to platform-specific list or remove
- If build fails → rollback flake.lock and investigate
- Update `flake.lock` only if all platforms pass

### 8. Common Issue Patterns

**Issue: Script uses bash-isms in shebang marked as sh**
```bash
# ❌ BAD
#!/bin/sh
declare -a arr=(one two)  # bash-only

# ✅ GOOD
#!/usr/bin/env bash
declare -a arr=(one two)
```

**Issue: Missing container detection in Nix install**
```bash
# ✅ GOOD (from scripts/install-nix.sh)
if [[ -f /.dockerenv ]] || [[ -n "$container" ]]; then
  curl --proto '=https' --tlsv1.2 -sSf -L https://install.determinate.systems/nix | \
    sh -s -- install linux --init none --no-confirm
fi
```

**Issue: Fish config assumes tools exist**
```fish
# ❌ BAD
eval (starship init fish)

# ✅ GOOD
if type -q starship
  eval (starship init fish)
end
```

## Output Format

Present findings as:

### 🔍 Compatibility Audit Results

**🔴 Critical Issues (blocks installation)**
- `scripts/cleanup-symlinks.sh:104` - Hardcoded user path
  - **Fix**: Use `$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)`
  - **Applied**: ✅ (auto-fixed via Edit tool)

**🟡 Warnings (may fail on some platforms)**
- `install.sh:45` - Missing Alpine Linux detection
  - **Fix**: Add fallback for unknown Linux distros
  - **Applied**: ⏭️ (requires user decision on fallback behavior)

**🟢 Suggestions (improvements)**
- Consider adding WSL2 detection in CI
- Add Alpine Docker test to matrix

### 🧪 Test Coverage
- ✅ macOS (Intel + ARM) - CI native
- ✅ Ubuntu 25.04 - CI Docker
- ✅ Fedora 40 - CI Docker
- ❌ Alpine/musl - Not tested
- ❌ WSL2 - Not tested

### 📦 Nix Flake Status
- **Last updated**: 2025-01-15 (commit `4160763d74f6`)
- **Platforms**: 4/4 building successfully
- **Action**: Run `nix flake update` + test matrix

## Integration with Repository Workflow

**Pre-commit checks:**
```bash
# Add to git pre-commit hook
scripts/audit-compatibility.sh || exit 1
```

**PR checklist (from AGENTS.md):**
- [ ] Cross-platform verified (macOS, Ubuntu, Fedora)
- [ ] No hardcoded paths or user-specific assumptions
- [ ] Tests updated in `tests/docker-test-commands.fish`
- [ ] `make test-pre && make test-docker` passing

**Continuous monitoring:**
- Run this skill after any `flake.nix` changes
- Run on schedule (weekly) to catch drift
- Run when CI fails on specific platform

## Reference Files

**Key compatibility files to monitor:**
- `install.sh` - Main entry point, OS detection
- `scripts/install-nix.sh` - Container detection, Nix installer
- `scripts/link-config.sh` - Platform-specific paths (VSCode)
- `scripts/cleanup-symlinks.sh` - ⚠️ Known hardcoded path issue
- `config/fish/conf.d/05-homebrew.fish` - macOS Homebrew detection
- `config/fish/conf.d/10-nix.fish` - Nix environment setup
- `flake.nix` - Package definitions for all platforms
- `.github/workflows/ci.yml` - CI test matrix
- `tests/docker-test-commands.fish` - Functional test suite

## Error Recovery

If auto-fix breaks something:
1. Git tracks all changes → `git diff` to review
2. Backups created by scripts (`.bak` files)
3. Rollback: `git checkout -- <file>`
4. Re-run tests: `make test-pre && make test-local`

---

**Remember**: This repository prioritizes **reproducibility via Nix** and **testing via Docker**. Every fix must pass the full test matrix before commit.
