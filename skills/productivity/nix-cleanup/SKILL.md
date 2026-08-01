---
name: nix-cleanup
description: 'Run janitorial cleanup for this flake: flake check, statix/deadnix linting,
  and safe hygiene fixes.'
---

---
name: nix-cleanup
description: Run janitorial cleanup for this flake: flake check, statix/deadnix linting, and safe hygiene fixes.
---

# Nix Cleanup

## What I do
- Keep cleanup aligned with this repo's linting and workflow rules.
- Run checks in a safe order and summarize findings before edits.
- Apply small hygiene fixes (unused bindings, repeated keys, legacy syntax) when requested.

## When to use me
Use this skill when you want a janitorial pass before committing, or when Nix lint errors need cleanup.

## Workflow
1. Run `nix flake check --no-build` to validate the flake without builds.
2. Run `nix run nixpkgs#statix -- check .` for linting.
3. Run `nix run nixpkgs#deadnix -- .` for unused bindings.
4. Summarize findings and ask before auto-fixing.
5. If approved, apply `statix fix` and/or `deadnix -e`, then re-run checks.

## Hygiene rules
- Avoid repeated keys in attribute sets; nest under a single key.
- Remove empty `let` blocks and unused arguments.
- Prefer `lib.mkIf` over nested ifs.
- Use `mkEnableOption` for boolean options.
- Use `pkgs.stdenv.hostPlatform.system` instead of `system`.

## Safety
- Never run destructive commands.
- Never touch dotfile-managed program configs (see dotfiles policy).
- Ask before changes that alter secrets or host definitions.
