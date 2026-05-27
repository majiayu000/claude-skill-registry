---
name: ctl-release
description: Update and rebuild spikectl or ctl packages in the monorepo
version: 5.1-hybrid
---

# Option: CTL Release

## Initiation (I)

Invoke when:
- Source code changed in `packages/spikectl/` or `packages/ctl/`
- Need to rebuild CLI binaries for Nix distribution
- Updating CLI tools after refactoring

## Observation Space (Y)

| Observable | How to Check |
|------------|--------------|
| Source modified | `git status packages/{spikectl,ctl}/src/` |
| Binary stale | Compare `bin/` mtime vs `src/` mtime |
| TypeScript valid | `bunx tsc --noEmit` |

## Action Space (U)

| Action | Command | From Directory |
|--------|---------|----------------|
| `compile` | `bun build --compile --minify src/index.ts --outfile bin/<name>` | `packages/<pkg>/` |
| `build-nix` | `nix build '.?dir=packages/tmnl#<pkg>'` | repo root |
| `test-binary` | `./result/bin/<pkg> --version` | repo root |
| `update-lock` | `nix flake update <pkg>` | `packages/tmnl/` |

## Policy (π)

```
STATE: source_changed ∧ ¬binary_updated
  → ACTION: compile

STATE: binary_updated ∧ need_nix_build
  → ACTION: build-nix

STATE: flake_deps_changed
  → ACTION: update-lock → build-nix

STATE: build_complete
  → ACTION: test-binary → TERMINATE
```

## Termination (β)

| Condition | Exit |
|-----------|------|
| `./result/bin/<pkg> --version` succeeds | SUCCESS |
| TypeScript errors | FAIL: fix errors |
| Nix build fails | FAIL: check flake.nix |

## Q-Heuristics

| Situation | Guidance |
|-----------|----------|
| Source-only changes | Skip `nix flake update` - `path:` inputs evaluate live |
| New dependencies in flake.nix | Must run `nix flake update <pkg>` |
| Binary size changed significantly | Verify correct bundling |

## Constraints

- □(compile_before_nix_build) — Always compile before Nix build
- □(test_after_build) — Always verify binary works after build
- ◇(version_incremented) — Eventually bump version for releases

## Commands

### Quick Rebuild
```bash
cd packages/spikectl
bun build --compile --minify src/index.ts --outfile bin/spikectl
```

### Full Release
```bash
cd packages/spikectl
bun build --compile --minify src/index.ts --outfile bin/spikectl
git add bin/spikectl
git commit -m "build(spikectl): v0.x.x"

cd ../..
nix build '.?dir=packages/tmnl#spikectl'
./result/bin/spikectl --version
```

### DevShell Access
```bash
nix develop '.?dir=packages/tmnl#tmnl-ctl'
# Now spikectl and ctl are in PATH
```

## Why No Flake Update for Source Changes?

The tmnl flake uses `path:` inputs:
```nix
spikectl = { url = "path:../spikectl"; }
```

No hash lock → changes picked up on rebuild.
