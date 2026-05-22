---
name: nix-manager
description: Manage Nix packages, flakes, and configurations using Determinate Nix installer patterns. Use when installing/updating packages, creating flakes, troubleshooting Nix issues, or optimizing Nix workflows. Keywords: nix, flake, package, nixpkgs, nix profile, flake.nix, flake.lock, determinate, nix-installer
---

# Nix Package & Configuration Manager

Comprehensive Nix management following Determinate Systems best practices and this repository's patterns.

## Instructions

### 1. Understand Repository Context

Check current Nix setup:
- **Flake location**: `/Users/wcygan/Development/dotfiles/flake.nix`
- **Installation script**: `scripts/install-packages.sh`
- **Package management**: `nix profile` (user-scoped, modern approach)
- **Installer**: Determinate Systems installer (macOS/Linux)
- **Update mechanism**: `make update` or `nix flake update && nix profile upgrade`

Read current `flake.nix` to understand:
- Input sources (currently: `nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable"`)
- Package definitions (buildEnv with ~60+ packages)
- Outputs: `packages`, `devShells`, `formatter`
- Supported systems: x86_64-linux, aarch64-linux, x86_64-darwin, aarch64-darwin

### 2. Package Management Operations

#### Install New Package

**Process:**
1. Add package to `flake.nix` in appropriate category
2. Run `nix flake check` to validate
3. Run `nix profile upgrade dotfiles` to apply changes
4. Test package availability

**Example:**
```nix
# flake.nix packages section
paths = [
  # ... existing packages ...

  # New package
  cowsay  # Fun terminal tool
];
```

```bash
# Validate and install
nix flake check
nix profile upgrade dotfiles
which cowsay  # Verify installation
```

#### Update All Packages

**Process:**
```bash
# Update flake inputs (updates nixpkgs revision)
nix flake update

# Apply updates to installed profile
nix profile upgrade dotfiles

# Verify no breakage
nix profile list
```

Or use Makefile shortcut:
```bash
make update  # Runs both commands above
```

#### Remove Package

**Process:**
1. Remove from `flake.nix`
2. Run `nix flake check`
3. Run `nix profile upgrade dotfiles`
4. Old package remains in store but not in PATH

**Note**: Garbage collection removes unreferenced packages:
```bash
make clean  # or: nix-collect-garbage -d
```

### 3. Flake Configuration

#### Modify flake.nix

**Common operations:**

**Add new input:**
```nix
inputs = {
  nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  # Add new input
  home-manager.url = "github:nix-community/home-manager";
  home-manager.inputs.nixpkgs.follows = "nixpkgs";  # Prevent duplicate nixpkgs
};
```

**Add platform-specific packages:**
```nix
paths = [
  # Universal packages
  git gh lazygit
] ++ lib.optionals stdenv.isDarwin [
  # macOS-only
  darwin.apple_sdk.frameworks.Security
] ++ lib.optionals stdenv.isLinux [
  # Linux-only
  libnotify
];
```

**Modify devShell:**
```nix
devShells = forAllSystems ({ pkgs }: {
  default = pkgs.mkShell {
    packages = with pkgs; [
      fish
      nixpkgs-fmt
      shellcheck
      # Add development tools here
    ];
    inputsFrom = [ self.packages.${pkgs.system}.default ];
    shellHook = ''
      echo "🐠 Dotfiles development environment"
      echo "Run: make test-pre"
    '';
  };
});
```

#### Validate Flake

**Always validate before applying:**
```bash
nix flake check        # Full validation (slow, builds everything)
nix flake metadata     # Quick metadata check
nix flake show         # Show outputs without building
```

**Common issues:**
- Package renamed in nixpkgs (e.g., `du-dust` → `dust`)
- Missing comma in package list
- Invalid attribute path
- Syntax errors in Nix expressions

#### Update Lock File

**When to update:**
- Regular maintenance (weekly/monthly)
- Security updates needed
- Specific package version required

**How:**
```bash
# Update all inputs
nix flake update

# Update specific input only
nix flake lock --update-input nixpkgs

# Verify changes
git diff flake.lock
```

### 4. Troubleshooting

#### Slow Nix Operations

**Diagnosis:**
```bash
nix store info             # Check store size
nix store gc --dry-run     # See what can be cleaned
```

**Solutions:**
- Run `nix-collect-garbage -d` to remove old generations
- Run `nix store optimise` to deduplicate files
- Check network connectivity (binary cache downloads)

#### Package Not Found

**Error**: `error: attribute 'package-name' missing`

**Solutions:**
1. Check nixpkgs version: some packages only in unstable
2. Search for package: `nix search nixpkgs package-name`
3. Check if package was renamed
4. Try alternative package names

#### Evaluation Errors

**Error**: `error: ... while evaluating ...`

**Common causes:**
- Syntax error in `flake.nix`
- Recursive attribute access
- Type mismatch (string vs list)

**Debug:**
```bash
nix eval .#packages.aarch64-darwin.default.name  # Test specific attribute
nix repl                                          # Interactive REPL
:lf .                                             # Load flake in REPL
packages.aarch64-darwin.default.name              # Evaluate in REPL
```

#### Lock File Conflicts

**Error**: `error: flake.lock is dirty`

**Solutions:**
```bash
# Regenerate lock file
rm flake.lock
nix flake update

# Or accept uncommitted changes
nix flake check --impure  # NOT recommended for reproducibility
```

#### Profile Issues

**List installed profiles:**
```bash
nix profile list
```

**Output format:**
```
Index:              0
Flake attribute:    legacyPackages.aarch64-darwin.dotfiles
Original flake URL: git+file:///Users/wcygan/Development/dotfiles
Locked flake URL:   git+file:///Users/wcygan/Development/dotfiles?rev=...
Store paths:        /nix/store/...-system-packages
```

**Rollback to previous generation:**
```bash
nix profile rollback
```

**Remove specific profile:**
```bash
nix profile remove <index-number>
```

### 5. CI/CD Integration

This repository uses **Determinate Systems GitHub Actions** for CI.

**GitHub Actions setup** (`.github/workflows/ci.yml`):
```yaml
- name: Setup Nix cache
  uses: DeterminateSystems/magic-nix-cache-action@v2

- name: Install Nix
  uses: DeterminateSystems/nix-installer-action@v14
  with:
    extra-conf: |
      experimental-features = nix-command flakes

- name: Run install script
  run: ./install.sh
```

**Benefits:**
- Magic Nix Cache: ~90% faster CI (uses GitHub Actions cache)
- Automatic cache population
- No configuration required

**Local equivalent:**
```bash
# Test installation in Docker
make test-docker

# Test idempotency
./install.sh && ./install.sh  # Should succeed twice
```

### 6. Best Practices (Determinate Nix Patterns)

#### Use nixos-unstable Instead of master

**Reasoning:**
- `nixos-unstable`: Tested, passes Hydra CI
- `master`: Untested, may have broken packages

**Current setup:**
```nix
inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
```

#### Never Use --impure

**Problem:** Breaks reproducibility by allowing environment variable access

**Correct:**
```bash
nix profile add .              # Pure evaluation
nix profile upgrade dotfiles   # Pure evaluation
```

**Incorrect:**
```bash
nix profile add . --impure     # BAD: non-reproducible
```

**Exception:** Only use `--impure` if flake explicitly uses `getEnv` or similar

#### Pin Dependencies in Lock File

**Why:**
- Ensures reproducible builds across machines
- Prevents "works on my machine" issues
- Required for CI/CD reliability

**How:**
```bash
# Always commit flake.lock
git add flake.lock
git commit -m "chore: update flake lock"
```

#### Use buildEnv for Package Groups

**Pattern in this repo:**
```nix
packages.default = pkgs.buildEnv {
  name = "system-packages";
  paths = [ git gh lazygit ... ];
};
```

**Benefits:**
- Single derivation for all packages
- Atomic updates (all packages succeed or fail together)
- Easier to manage than individual `nix profile install` calls

#### Enable Flakes in Config

**User-level config** (`~/.config/nix/nix.conf`):
```
experimental-features = nix-command flakes
```

**This is automatically set by `scripts/install-packages.sh`**

### 7. Development Workflows

#### Create New Project Flake

**Use repository root as template:**
```bash
# Copy flake structure
cp flake.nix /path/to/new-project/

# Customize for project needs
cd /path/to/new-project
$EDITOR flake.nix
```

**Or use templates directory:**
```bash
# Use template (if available in .claude/skills/nix-manager/templates/)
nix flake init -t .#template-name
```

#### Test Flake Locally

**Without installing:**
```bash
# Enter dev shell
nix develop

# Build without installing
nix build

# Run specific package
nix run .#package-name
```

#### Format Nix Code

**Using formatter output:**
```bash
nix fmt  # Uses nixpkgs-fmt (defined in flake.nix)
```

**Manual formatting:**
```bash
nixpkgs-fmt flake.nix
```

### 8. Migration Guidance

#### From Homebrew

**Don't uninstall Homebrew**—it coexists peacefully. Fish PATH priority:
1. Homebrew (`/opt/homebrew/bin`) - highest priority
2. User bins (`~/.local/bin`, `~/bin`)
3. Language toolchains (`~/.cargo/bin`, `~/go/bin`)
4. **Nix** (`~/.nix-profile/bin`) - lowest priority

**Migration strategy:**
```bash
# 1. Install package via Nix
# (add to flake.nix and run nix profile upgrade)

# 2. Test package works
which package-name  # Should show Homebrew path (higher priority)

# 3. Uninstall from Homebrew
brew uninstall package-name

# 4. Verify Nix version now active
which package-name  # Should show /nix/store/... path
```

#### From apt/dnf

**Linux distros:**
- Nix coexists with system package managers
- System packages have priority over Nix (via PATH ordering)
- Use Nix for tools not in distro repos or needing newer versions

### 9. Output Format

When modifying flake.nix:

**Use Edit tool** for existing files:
- Modify specific sections
- Preserve comments and formatting
- Minimize diff size

**Use Write tool** for new files:
- Complete flake.nix from scratch
- Include comments explaining choices
- Follow repository formatting style

**After changes, always:**
1. Validate: `nix flake check`
2. Test build: `nix build --dry-run`
3. Apply: `nix profile upgrade dotfiles`
4. Verify: `nix profile list`

**Include testing commands:**
```bash
# Validate changes
nix flake check

# Show what changed
nix flake show

# Apply updates
nix profile upgrade dotfiles
```

## Repository Patterns

This dotfiles repository follows these conventions:

**File Structure:**
- `flake.nix` - Package definitions and outputs
- `flake.lock` - Pinned dependency versions
- `scripts/install-packages.sh` - Installation wrapper
- `scripts/link-config.sh` - Dotfile symlinking
- `config/` - Dotfile configurations (fish, starship, etc.)

**Package Organization:**
Packages grouped by purpose with comments:
```nix
paths = [
  # Version control
  git gh lazygit

  # Build tools
  gnumake cmake pkg-config

  # Programming languages
  rustup go python3 deno

  # ... etc
];
```

**Testing:**
- `make test-pre` - Pre-flight validation
- `make test-local` - Ephemeral HOME test
- `make test-docker` - Multi-distro Docker matrix

**Common Commands:**
- `make install` - Run full installation
- `make update` - Update flake + upgrade packages
- `make clean` - Garbage collect
- `make verify` - Check Nix installation health

## Reference Documentation

- Determinate Installer: https://determinate.systems/blog/determinate-nix-installer/
- Zero to Nix (Flakes): https://zero-to-nix.com/concepts/flakes/
- Nix.dev (Flakes): https://nix.dev/concepts/flakes.html
- NixOS Wiki: https://nixos.wiki/wiki/Flakes
- Repository: /Users/wcygan/Development/dotfiles/

## Quick Reference

**Essential Commands:**
```bash
# Package management
nix search nixpkgs <package>     # Search for package
nix profile list                 # List installed packages
nix profile upgrade dotfiles     # Apply flake changes
nix-collect-garbage -d           # Clean old generations

# Flake management
nix flake update                 # Update all inputs
nix flake check                  # Validate flake
nix flake show                   # Display outputs
nix flake metadata               # Show metadata

# Development
nix develop                      # Enter dev shell
nix build                        # Build package
nix fmt                          # Format Nix code
nix run .#package                # Run package

# Troubleshooting
nix store info                   # Store statistics
nix store gc --dry-run           # Preview cleanup
nix profile rollback             # Revert to previous
```
