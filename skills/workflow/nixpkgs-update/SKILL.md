---
name: nixpkgs-update
description: Update nixpkgs packages with nix-update and nixpkgs-review. Activate when user wants to bump a package version, contribute to nixpkgs, update Nix packages, or mentions nix-update, nixpkgs-review, or nixpkgs contribution.
allowed-tools: [task]
---

# Nixpkgs Package Update

Batch workflow for contributing package updates to NixOS/nixpkgs. Uses Repology API for discovery, strict filtering for easy updates, and git worktrees for parallel execution.

## Workflow

```
1. DISCOVER  → Query Repology API
2. FILTER    → Keep only Rust/Go + by-name + no patches + buildable platform
3. VALIDATE  → Parallel Explore agents confirm "simple" complexity
4. SELECT    → Present candidates to user (multi-select)
5. UPDATE    → Parallel agents with git worktrees (10m timeout)
6. REPORT    → Collect and display PR URLs
```

## Phase 1: Discover Outdated Packages

Query Repology API for outdated nixpkgs packages:

```
task(
  subagent_type="general",
  description="Query Repology outdated packages",
  prompt="Query Repology API for outdated nixpkgs packages.

Step 1 - Get outdated package names:
curl -s --user-agent 'nixpkgs-update/1.0' \
  'https://repology.org/api/v1/projects/?inrepo=nix_unstable&outdated=1&count=100' | \
  jq -r 'keys[:50][]'

Step 2 - For each package, get version details (respect 1 req/sec rate limit):
curl -s --user-agent 'nixpkgs-update/1.0' \
  'https://repology.org/api/v1/project/<name>' | \
  jq '{name: .[0].visiblename, nixpkgs: ([.[] | select(.repo==\"nix_unstable\")][0].version), newest: ([.[] | select(.status==\"newest\")][0].version)}'

Return list with: name, nixpkgs_version, newest_version."
)
```

## Phase 2: Filter Candidates (Strict)

From Repology results, apply strict filtering. **Only keep packages that meet ALL criteria:**

### Must Pass ALL:
1. **Location**: `pkgs/by-name/` only (not legacy paths)
2. **Type**: Rust (`buildRustPackage`, `cargoHash`) OR Go (`buildGoModule`, `vendorHash`)
3. **Version bump**: Patch or minor version (reject major bumps like 1.x → 2.x)
4. **Platform**: Must support current platform (see platform check below)

### Check with Glob/Grep:
```bash
# Check if package exists in by-name
ls pkgs/by-name/*/<package>/package.nix

# Check if Rust or Go
grep -l "buildRustPackage\|cargoHash" pkgs/by-name/*/<package>/package.nix
grep -l "buildGoModule\|vendorHash" pkgs/by-name/*/<package>/package.nix
```

### Platform Check (CRITICAL)
```bash
# Get current system
CURRENT_PLATFORM=$(nix eval --raw --impure --expr 'builtins.currentSystem')
# e.g., "aarch64-darwin" or "x86_64-linux"

# Check if package supports current platform
nix eval .#<package>.meta.platforms --json | jq -e 'contains(["'$CURRENT_PLATFORM'"])'
# OR check for platform restrictions in package.nix:
grep -E "platforms\s*=.*linux" pkgs/by-name/*/<package>/package.nix  # Linux-only, skip on macOS
grep -E "platforms\s*=.*darwin" pkgs/by-name/*/<package>/package.nix  # macOS-only, skip on Linux
```

**Discard packages that cannot be built/tested on current platform.**

**Discard any package that doesn't pass ALL filters.**

## Phase 3: Validate Each Candidate

For EACH filtered candidate, spawn Explore agent to verify simplicity:

```
task(
  subagent_type="explore",
  description="Validate package complexity",
  prompt="Thoroughness: quick

Check pkgs/by-name/*/<package>/package.nix for:
  1. has_patches: any patches = [] or patches directory?
  2. has_complex_postinstall: complex substituteInPlace, wrapProgram with many deps?
  3. has_overrides: overrideAttrs, overrideModAttrs?
  4. complexity: simple/medium/complex
  5. platform_restricted: does it have 'platforms = lib.platforms.linux' or similar restriction?

Return JSON: {has_patches: bool, complexity: 'simple'|'medium'|'complex', platform_restricted: bool, platforms: string}
Only packages with has_patches=false AND complexity='simple' AND supports current platform are acceptable."
)
```

**Only packages with `has_patches=false` AND `complexity=simple` AND `supports current platform` proceed to selection.**

## Phase 4: Present Candidates (Multi-Select)

Present ONLY validated easy candidates:

```
Present candidates to user for selection (output directly):

## Select Packages to Update

| # | Package | Version | Type |
|---|---------|---------|------|
| 1 | some-rust-pkg | 1.0.0 → 1.0.1 | Rust, simple |
| 2 | some-go-pkg | 0.5.0 → 0.5.1 | Go, simple |

Ask: "Which packages would you like to update? (enter numbers, e.g., 1,2)"
```

**Never show:**
- "may need manual work"
- "complex"
- "has patches"
- Major version bumps
- **Platform-restricted packages that can't be tested locally**

## Phase 5: Parallel Updates with Git Worktrees

### Why Worktrees?
Multiple agents cannot `git switch` on the same repo simultaneously. Worktrees provide isolated working directories sharing the same git history.

### Setup Worktrees
For each selected package, create isolated worktree:

```bash
# From main repo (stays on master, untouched)
git worktree add /tmp/nixpkgs-<package>-<version> -b <package>-<version> master
```

### Launch Parallel Agents

```
// Single message with N Task calls, each with its own worktree:
task(subagent_type="general", description="Update pkg1", prompt="Update pkg1 in /tmp/nixpkgs-pkg1-v1...")
task(subagent_type="general", description="Update pkg2", prompt="Update pkg2 in /tmp/nixpkgs-pkg2-v2...")
```

### Update Agent Prompt Template

```
Update the nixpkgs package: <PACKAGE>
Current version: <OLD_VERSION>
Target version: <NEW_VERSION>

## Setup
Working directory: /tmp/nixpkgs-<PACKAGE>-<NEW_VERSION>
(Worktree already created, you are on branch <PACKAGE>-<NEW_VERSION>)

## IMPORTANT RULES
- **10 MINUTE TIMEOUT**: If any build step exceeds 10 minutes, ABORT and report failure
- **NEVER SKIP nixpkgs-review**: This step is MANDATORY, not optional
- Use `timeout 600` prefix for long-running commands

## Steps

1. **Verify worktree:**
   cd /tmp/nixpkgs-<PACKAGE>-<NEW_VERSION>
   git status  # Should show branch <PACKAGE>-<NEW_VERSION>

2. **Run nix-update (with timeout):**
   timeout 600 nix run nixpkgs#nix-update -- <PACKAGE>

   If timeout: ABORT, cleanup worktree, report "build timeout"

3. **Build and verify (with timeout):**
   timeout 600 nix build .#<PACKAGE>

   If timeout: ABORT, cleanup worktree, report "build timeout"
   If build fails: ABORT, cleanup worktree, report "build failed"

   ./result/bin/<BINARY> --version

4. **Test dependent packages (MANDATORY - DO NOT SKIP):**
   timeout 600 nix run nixpkgs#nixpkgs-review -- wip --print-result

   If timeout: ABORT, cleanup worktree, report "review timeout"
   This step is NOT optional. Never skip it.

5. **Commit:**
   git add -A
   git commit -m "$(cat <<'EOF'
<PACKAGE>: <OLD_VERSION> -> <NEW_VERSION>

https://github.com/<OWNER>/<REPO>/releases/tag/v<NEW_VERSION>
EOF
)"

6. **Push to fork:**
   git push --set-upstream fork <PACKAGE>-<NEW_VERSION>

7. **Create PR:**
   gh pr create --repo NixOS/nixpkgs \
     --title "<PACKAGE>: <OLD_VERSION> -> <NEW_VERSION>" \
     --body "$(cat <<'EOF'
## Description
Updates `<PACKAGE>` from <OLD_VERSION> to <NEW_VERSION>.

## Testing
- [x] Built locally
- [x] Ran nixpkgs-review wip

## Links
- Release: https://github.com/<OWNER>/<REPO>/releases/tag/v<NEW_VERSION>
EOF
)"

8. **Return:** PR URL or error message

## On Failure
If any step fails or times out:
1. Cleanup: git worktree remove /tmp/nixpkgs-<PACKAGE>-<NEW_VERSION> --force
2. Delete branch: git branch -D <PACKAGE>-<NEW_VERSION>
3. Report failure with reason
```

### Cleanup Worktrees

After all agents complete, cleanup:

```bash
git worktree remove /tmp/nixpkgs-<package>-<version>
# Repeat for each worktree
```

## Phase 6: Collect Results

Task results return automatically when subagents complete. Present summary:

```
## Update Results

| Package      | Version          | Status | PR     |
|--------------|------------------|--------|--------|
| some-rust    | 1.0.0 → 1.0.1    | ✅     | #12345 |
| some-go      | 0.5.0 → 0.5.1    | ⏱️     | timeout |
```

Cleanup worktrees after reporting.

## Quick Reference

### Platform Detection

```bash
# Get current system
nix eval --raw --impure --expr 'builtins.currentSystem'
# Returns: aarch64-darwin, x86_64-linux, aarch64-linux, x86_64-darwin

# Check package platforms
nix eval .#<pkg>.meta.platforms --json

# Common platform patterns in package.nix:
# lib.platforms.linux     → Linux only (skip on macOS)
# lib.platforms.darwin    → macOS only (skip on Linux)
# lib.platforms.unix      → Both Linux and macOS (OK)
# lib.platforms.all       → All platforms (OK)
```

### Git Worktrees

```bash
# Create worktree with new branch
git worktree add /tmp/nixpkgs-<pkg>-<ver> -b <pkg>-<ver> master

# List worktrees
git worktree list

# Remove worktree
git worktree remove /tmp/nixpkgs-<pkg>-<ver>

# Force remove (if dirty)
git worktree remove /tmp/nixpkgs-<pkg>-<ver> --force

# Prune stale worktrees
git worktree prune
```

### Timeout Commands

```bash
# 10 minute timeout for builds
timeout 600 nix build .#<pkg>

# Check exit code: 124 = timeout
if [ $? -eq 124 ]; then echo "TIMEOUT"; fi
```

### Repology API

```bash
# Get outdated nixpkgs packages (User-Agent required!)
curl -s --user-agent "nixpkgs-update/1.0" \
  "https://repology.org/api/v1/projects/?inrepo=nix_unstable&outdated=1&count=50" | \
  jq -r 'keys[:20][]'

# Check specific package versions
curl -s --user-agent "nixpkgs-update/1.0" \
  "https://repology.org/api/v1/project/<name>" | \
  jq '{nixpkgs: ([.[] | select(.repo=="nix_unstable")][0].version), newest: ([.[] | select(.status=="newest")][0].version)}'
```

### Nix Commands

```bash
# Update package (auto-updates hashes)
timeout 600 nix run nixpkgs#nix-update -- <pkg>

# Build package
timeout 600 nix build .#<pkg>

# Test dependent packages (MANDATORY)
timeout 600 nix run nixpkgs#nixpkgs-review -- wip --print-result
```

### Commit Format

```
<pkg>: <old-version> -> <new-version>
```

## Candidate Criteria Summary

| Criteria | Required Value |
|----------|----------------|
| Location | `pkgs/by-name/` |
| Type | Rust OR Go |
| has_patches | `false` |
| complexity | `simple` |
| Version bump | patch/minor only |
| **Platform** | **Must support current system** |

**If ANY criterion fails, discard the candidate. Never present options that can't be tested locally.**

## Failure Handling

| Failure | Action |
|---------|--------|
| Build timeout (>10m) | Discard, cleanup, report |
| Build error | Discard, cleanup, report |
| Review timeout (>10m) | Discard, cleanup, report |
| Platform mismatch | Never present to user |
