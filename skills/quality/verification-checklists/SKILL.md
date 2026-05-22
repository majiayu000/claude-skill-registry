---
description: |
  Verification checklists for game development tasks. Use when completing features, assets, or systems to ensure nothing is missed. Prevents "generated but not integrated" and "coded but not rendered" issues.

  **Load references when:**
  - Asset checklists → `references/asset-checklists.md`
  - Feature checklists → `references/feature-checklists.md`
  - System checklists → `references/system-checklists.md`
---

# Verification Checklists

Systematic verification that work is truly complete.

## The Core Question

Before marking anything complete:

**"Would a player notice this in the game?"**

If no - it's not complete.

## Quick Verification Commands

```bash
# Assets exist
ls generated/meshes/*.obj generated/textures/*.png generated/sounds/*.wav

# Assets declared
grep "\[\[assets" nether.toml

# Handles exist
grep "asset_handle!" src/assets.rs

# Assets used
grep -r "draw_mesh\|texture_bind\|sound_play" src/

# No incomplete markers
grep -r "TODO\|FIXME\|unimplemented!\|todo!" src/

# Build succeeds
nether build

# Module integrated
grep "mod " src/lib.rs
```

## Integration Chain Summary

**Assets:**
```
File exists → nether.toml → src/assets.rs handle → Used in code
```

**Features:**
```
Module declared → init() setup → update() logic → render() display
```

## Red Flags (Incomplete Work)

- `TODO` or `FIXME` comments
- `unimplemented!()` or `todo!()` macros
- Empty match arms: `_ => {}`
- Assets in output/ but not assets/
- Assets in assets/ but not in nether.toml
- Handles defined but never used
- Code written but not called from main loop
- Feature has no visual/audio feedback

For detailed checklists by asset type, feature type, and system type, load the references.
