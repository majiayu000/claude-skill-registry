---
name: Generator Patterns
description: |
  Use this skill when setting up procedural asset generation projects.

  **Triggers:** "project structure", "file organization", "generator setup", "multiple assets", "batch generation", "lib utilities", "ZX constraints", "asset budgets".

  **Load references when:**
  - ZX asset limits (poly budgets, texture sizes, audio specs) → `references/zx-constraints.md`
  - Setting up project structure → `references/file-organization.md`
version: 1.1.0
---

# Generator Patterns

Shared patterns for organizing spec-first procedural asset generation. Optimized for maintainability and LLM context efficiency.

## Core Principle: One Spec Per Asset

Every procedural asset (texture, normal, sound, instrument, mesh, character, animation) should have its own dedicated `.spec.py` file. This pattern provides:

1. **LLM Context Efficiency** - Load only lib + single asset file (~150 lines vs 500+)
2. **Maintainability** - Changes to one asset don't affect others
3. **Discoverability** - File name = asset name
4. **Parallel Development** - Multiple agents can work on different assets without conflicts
5. **Testing** - Generate a single category when iterating
6. **Batch Generation** - Single entry point: `python .studio/generate.py`

## Standard Project Structure

```
project/
├── .studio/
│   ├── generate.py
│   ├── parsers/                  # Installed by /init-procgen
│   └── specs/
│       ├── textures/
│       ├── normals/
│       ├── sounds/
│       ├── instruments/
│       ├── music/
│       ├── meshes/
│       ├── characters/
│       └── animations/
└── generated/
    ├── textures/
    ├── normals/
    ├── meshes/
    ├── characters/
    ├── animations/
    ├── audio/
    │   └── instruments/
    └── tracks/
```

## Spec File Template

Each spec file defines exactly one asset:

```python
# .studio/specs/sounds/laser.spec.py
SOUND = {
    "sound": {
        "name": "laser",
        "category": "projectile",
        "duration": 0.25,
        "layers": [ ... ],
    }
}
```

## File Size Limits

| Limit | Lines | Action |
|-------|-------|--------|
| Target | ≤150 | Ideal for single asset |
| Soft | 200 | Consider extracting helpers to lib/ |
| Hard | 300 | MUST split or refactor |

If a spec exceeds 200 lines, simplify structure or split into multiple assets.

## References

- `references/file-organization.md` - Detailed organization guide
- `references/zx-constraints.md` - ZX budgets and constraints

## Related Skills

- `procedural-meshes` - Mesh-specific generation techniques
- `procedural-textures` - Texture-specific generation techniques
- `procedural-sprites` - Sprite-specific generation techniques
- `procedural-animations` - Animation-specific generation techniques
