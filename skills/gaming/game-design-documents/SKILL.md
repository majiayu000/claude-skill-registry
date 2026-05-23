---
name: Game Design Documents for ZX
description: This skill should be used when the user asks to "create a game design document", "write a GDD", "design my game", "document my game concept", "game design template", "plan my game", or needs structured documentation for a Nethercore ZX game project.
version: 0.1.0
---

# Game Design Documents for ZX

Guidance for creating modular Game Design Documents tailored to Nethercore ZX console constraints. Supports three depth levels: Quick, Standard, and Comprehensive.

## GDD Depth Levels

### Quick GDD (1 page)
For rapid prototyping and game jams:
- High concept (2-3 sentences)
- Core mechanic description
- ZX constraints summary
- Asset list

### Standard GDD (3-5 pages)
For pre-production and indie projects:
- Everything in Quick, plus:
- Detailed mechanics breakdown
- Level/world structure
- Memory budget allocation
- Control scheme
- Audio design notes

### Comprehensive GDD (Full document)
For production and commercial projects:
- Everything in Standard, plus:
- Narrative design
- Character/enemy specifications
- Detailed art direction
- Multiplayer strategy
- Development milestones
- Technical challenges

## GDD Creation Workflow

### Step 1: Capture the Vision
Start with the core concept:
- One-sentence pitch ("A game where...")
- Target player experience
- Key differentiator
- Reference games (inspiration, not copying)

### Step 2: Validate Against ZX Constraints
Before detailed design, confirm feasibility:
- Does the concept fit in 16 MB ROM?
- Is the game state small enough for rollback?
- Which render mode matches the art style?
- Can audio design work within 16 channels?

### Step 3: Choose Depth Level
Select based on project needs:
- **Quick:** Proof of concept, game jam
- **Standard:** Indie development, small team
- **Comprehensive:** Commercial release, large scope

### Step 4: Fill Template Sections
Work through template sections in order. Each section builds on previous ones.

### Step 5: Review and Iterate
- Cross-check memory budgets
- Verify control scheme completeness
- Ensure multiplayer determinism (if applicable)

## ZX-Specific Sections

Every ZX GDD should include these platform-specific sections:

### Render Mode Rationale
Document the chosen render mode and why:
```
Render Mode: [0/1/2/3]
Rationale: [Why this mode fits the game]
Art Style Implications: [How this affects asset creation]
```

### Memory Budget Summary
High-level ROM/RAM allocation:
```
ROM Budget (16 MB):
├── Code: X MB
├── Meshes: X MB
├── Textures: X MB
├── Audio: X MB
├── Animations: X MB
└── Remaining: X MB

RAM State Size: ~X KB (target < 100 KB for fast rollback)
```

### Tick Rate Selection
Document the chosen tick rate:
```
Tick Rate: [24/30/60/120] fps
Rationale: [Why this rate for this game type]
```

### Multiplayer Design (if applicable)
```
Player Count: [1-4]
Local/Online: [Local only / Online / Both]
Determinism Notes: [What systems need special care]
Input Handling: [How inputs are processed]
```

## Document Location

Save GDDs to `docs/design/`:
```
project/
└── docs/
    └── design/
        ├── game-design.md       # Primary GDD
        ├── asset-specs.md       # Asset requirements
        └── technical-notes.md   # Implementation notes
```

## Writing Guidelines

### Be Specific
Instead of: "The game will have good graphics"
Write: "Using Mode 2 (MR-Blinn-Phong) for realistic car materials, 512×512 diffuse textures per vehicle"

### Include Constraints Early
Don't save technical limitations for the end. Weave them into each section:
- "The hub world supports 20 NPCs (within entity budget)"
- "Music loops are 30 seconds each (fits audio budget)"

### Reference Procgen Opportunities
Mark assets suitable for procedural generation:
- "Background textures [PROCGEN: noise-based rock patterns]"
- "Ambient sounds [PROCGEN: synthesized atmosphere]"

### Link Technical Tasks
Connect design decisions to implementation:
- "Character movement requires custom physics (see zx-dev: collision system)"
- "Menu system uses Mode 0 overlay (see zx-dev: render mode switching)"

## Common Mistakes to Avoid

### Scope Creep
ZX's constraints are features, not limitations. Respect them:
- 16 MB ROM is generous for focused games
- 4-player is maximum, not minimum
- 16 audio channels require planning

### Vague Asset Descriptions
Instead of "various enemies," specify:
- Enemy count
- Animation states per enemy
- Estimated mesh/texture size

### Ignoring Determinism
For multiplayer games, design for determinism from the start:
- No random without seeded `random()`
- No system time access
- No hash map iteration order dependencies

## Additional Resources

### Template Files

For ready-to-use GDD templates:
- **`references/gdd-template-quick.md`** — 1-page template
- **`references/gdd-template-standard.md`** — 3-5 page template
- **`references/gdd-template-comprehensive.md`** — Full template

### Example Files

For filled-out examples:
- **`examples/gdd-example-fighting.md`** — Fighting game GDD
- **`examples/gdd-example-platformer.md`** — Platformer GDD

## Integration with Plugin Suite

The GDD connects to other nethercore plugins:

### → zx-procgen
Asset specifications flow to procedural generation:
```
GDD: "Rock textures, 256×256, Mode 2 MRE workflow"
↓
Procgen: Generate tileable rock with MRE channels
```

### → zx-dev
Technical requirements flow to implementation:
```
GDD: "4-player fighting with 8 characters"
↓
zx-dev: Scaffold project with multiplayer, character system
```

The `/plan-assets` command extracts procgen-ready specs.
The `/design-game` command generates complete GDDs.
