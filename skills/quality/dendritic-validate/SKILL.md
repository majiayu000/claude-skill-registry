---
name: dendritic-validate
description: Validate dendritic Nix pattern usage and flag deviations.
---

# Dendritic Pattern Validation

## What I do
- Verify every module is a flake-parts module exporting `flake.modules.<class>.<aspect>`.
- Check that dendritic layout rules are followed (single tree, central loader, perSystem outputs).
- Confirm global metadata lives in `flake.meta` and is read via `config.flake.meta`.
- Flag manual sibling imports, host-centric file layout drift, or misused `specialArgs`.
- Summarize findings with precise file references and recommended fixes.

## When to use me
Use this skill when reviewing new modules, refactors, or community imports for dendritic correctness.

## Workflow
1. Read @docs/agents/dendritic-core.md for alignment with repo rules.
2. Review `flake.nix` and module loading to confirm import-tree usage and no manual sibling imports.
3. Scan `modules/` for aspect-oriented exports and consistent class coverage (`nixos`, `darwin`, `homeManager`, `nixvim`).
4. Validate host and image registration under `flake.modules.nixos."hosts/<id>"` or `"iso/<id>"` and the shared loader wiring.
5. Confirm perSystem outputs stay under `perSystem` and avoid per-host package definitions.
6. Check for `specialArgs` usage that should be replaced by let bindings or flake-parts options.
7. For shared/community trees, validate Dendrix conventions (`modules/community`, `private` infix, `+flag` paths).

## Validation checklist
- `flake.nix` is minimal and imports `./modules` via import-tree once.
- Each `.nix` file is a flake-parts module; no direct sibling imports.
- Aspects remain feature-centric, not host-centric, across configuration classes.
- Host metadata and flags flow through `hostConfig` or similar context records.
- perSystem outputs live only under `perSystem` for architecture-specific logic.
- Files ignored by `import-tree` (`/_` in path) are treated as intentionally excluded.

## References
- @docs/agents/dendritic-core.md
- https://vic.github.io/dendrix/Dendritic.html

## Safety
- Never modify files unless requested; report issues with file paths and suggested fixes first.
