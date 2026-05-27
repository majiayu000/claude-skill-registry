---
description: |
  Dependency chains in game development - what must complete before other tasks can begin. Use when planning task order, identifying blockers, or ensuring proper sequencing.

  **Load references when:**
  - Phase dependencies → `references/phase-dependencies.md`
  - Feature chains → `references/feature-chains.md`
---

# Dependency Chains

Understanding dependencies ensures tasks complete in the correct order.

## Core Pipeline

```
Creative Vision → Game Design → Asset Specs → Assets → Integration → Implementation → Testing → Publishing
```

Each phase depends on the previous. Skipping phases causes problems.

## Key Dependencies

| Blocker | Blocked Tasks | Resolution |
|---------|---------------|------------|
| No GDD | All implementation | Create with /design-game |
| No assets | Visual features | Generate with asset-generator |
| Assets not integrated | Rendering | Run integration-assistant |
| No handles | Asset usage in code | Create src/assets.rs |
| Build fails | All testing | Fix compilation errors |
| Module not in lib.rs | Feature doesn't run | Add mod declaration |
| Not in update() | Feature doesn't update | Add update call |
| Not in render() | Feature doesn't display | Add render call |

## Parallelizable Tasks

Can run simultaneously (no dependencies):
- Different asset types (textures, meshes, sounds)
- Different enemy types
- Different UI elements
- Analysis tasks (reviews, audits)

## Sequential Requirements

Must run in order:
1. Design → Implementation
2. Generation → Integration
3. Integration → Usage
4. Code → Test
5. Pass tests → Release

## Dependency Verification

Before starting a task, verify dependencies:

```bash
# Before feature using assets:
ls generated/meshes/feature*.obj
grep "feature" nether.toml
grep "FEATURE" src/assets.rs

# Before testing:
nether build

# Before rendering:
grep "mod feature" src/lib.rs
```

For detailed phase and feature chains, load the references.
