---
name: Game Design Doc Creator
description: Create design documents for Stapledons Voyage game features. Use when user asks to create a design doc, plan a feature, or document game mechanics. Handles both planned/ and implemented/ docs.
---

# Game Design Doc Creator

Create well-structured design documents for Stapledons Voyage game features.

## Quick Start

**Most common usage:**
```bash
# User says: "Create a design doc for NPC pathfinding"
# This skill will:
# 1. Ask for key details (priority, complexity)
# 2. Create design_docs/planned/npc-pathfinding.md
# 3. Fill template with proper structure
# 4. Guide you through customization
```

## When to Use This Skill

Invoke this skill when:
- User asks to "create a design doc" or "plan a feature"
- Before implementing new game mechanics
- Documenting world generation algorithms
- Planning NPC AI behaviors
- Designing rendering/visual features

## Available Scripts

### `scripts/create_planned_doc.sh <doc-name> [version]`
Create a new design document in `design_docs/planned/`.

### `scripts/move_to_implemented.sh <doc-name> <version>`
Move a design document from planned/ to implemented/ after completion.

## Workflow

### 1. Gather Requirements

Ask user:
- What game feature are you designing?
- What game systems does it affect? (world, NPCs, rendering, input)
- Estimated complexity? (simple, medium, complex)
- Any AILANG limitations to work around?

### 2. Game Vision Alignment

**Every feature should be scored against the game's core pillars.**

**IMPORTANT:** Before creating any design doc, read these files maintained by `game-vision-designer`:

| File | Purpose | When to Check |
|------|---------|---------------|
| [core-pillars.md](../../../docs/vision/core-pillars.md) | Authoritative pillar definitions | Always - score feature against each |
| [design-decisions.md](../../../docs/vision/design-decisions.md) | Prior decisions & rationale | Check for relevant constraints |
| [open-questions.md](../../../docs/vision/open-questions.md) | Unresolved design questions | See if feature touches these |
| [game-vision.md](../../../docs/game-vision.md) | Full game design document | Deep context when needed |

**Score against each pillar in core-pillars.md:**

| Pillar | Question |
|--------|----------|
| **Time Dilation Consequence** | Does this reinforce irreversible time choices? |
| **Civilization Simulation** | Does it enhance galaxy-scale simulation? |
| **Philosophical Depth** | Does it add moral/philosophical decisions? |
| **Ship & Crew Life** | Does it connect to finite crew narrative? |
| **Legacy Impact** | Does it contribute to Year 1,000,000 report? |
| **Hard Sci-Fi Authenticity** | Does it maintain scientific plausibility? |

**Feature types:**
- **Gameplay features** should score positively on multiple pillars
- **Engine/Infrastructure** features can score N/A on most pillars (they're enabling tech)
- **No feature** should score negatively on any pillar (violates game vision)

**Check design-decisions.md for:**
- Prior decisions that constrain this feature
- Rejected alternatives (don't re-propose without new justification)
- Related features and how they were resolved

### 3. Physics-First Design (CRITICAL)

**This is a hard sci-fi game. All visual effects must be based on real physics.**

#### Real Physics (USE THESE)

| Effect | Physics Basis | When to Use |
|--------|---------------|-------------|
| **SR Doppler Shift** | Light wavelength changes with relative velocity | Relativistic travel |
| **SR Aberration** | Stars appear to bunch forward at high velocity | High-speed scenes |
| **GR Lensing** | Light bends around massive objects | Near black holes, neutron stars |
| **GR Redshift** | Light escaping gravity wells shifts red | Near massive objects |
| **Time Dilation** | γ = 1/√(1-v²/c²) | All relativistic travel |
| **Parallax** | Distant objects move slower than near ones | Depth perception |

#### Hollywood Conventions (NEVER USE)

| Rejected Effect | Why It's Wrong | What to Use Instead |
|-----------------|----------------|---------------------|
| **Star Streaks** | Stars are too distant for motion blur | SR aberration (stars bunch forward) |
| **Radial Motion Blur** | No physical basis at relativistic speeds | SR Doppler shift (color change) |
| **Warp Tunnels** | Pure fantasy, no physics | Actual SR/GR visual distortion |
| **Sound in Space** | No medium for sound waves | Silence, or ship interior sounds |
| **Engine Glow Trails** | No medium to illuminate in vacuum | Point-source engine light only |
| **Instant Communication** | Violates light speed limit | Time-delayed messages |
| **Artificial Gravity Plates** | No known physics | Rotation or acceleration |

#### Physics Validation Checklist

Before finalizing any visual/physics design:
- [ ] Is this effect based on real physics?
- [ ] Can I cite the equation or principle?
- [ ] Would a physicist approve?
- [ ] If "artistic license" is needed, is there a narrative justification?

**Example narrative justification**: Lower velocities (0.1c-0.5c instead of 0.9c) because "the AI pilot slows for crew sightseeing" - physics is still accurate, just at visible intensities.

### 4. Engine Capabilities Reference

**Before designing, know what's already available:**

| Reference | Contents |
|-----------|----------|
| [engine-capabilities.md](../../../design_docs/reference/engine-capabilities.md) | Complete engine reference |
| [gr-effects.md](../../../design_docs/implemented/v0_1_0/gr-effects.md) | GR physics & shaders |
| [ai-handler-system.md](../../../design_docs/implemented/v0_1_0/ai-handler-system.md) | AI effect & providers |

**Available Engine Features:**
- **DrawCmd**: Sprite, Rect, Text, IsoTile, IsoEntity, GalaxyBg, Star, Ui, Line, Circle, TextWrapped
- **Effects**: Debug, Rand, Clock, AI (Claude/Gemini/stub backends)
- **Assets**: Animated sprites, Audio (OGG/WAV), Fonts (TTF)
- **Shaders**: SR warp (Doppler, aberration), GR warp (lensing, redshift), bloom, vignette
- **Physics**: Lorentz factor (γ), time dilation, gravitational redshift, Schwarzschild radius

### 5. Consider AILANG Constraints

**Important for this project:** All game logic is written in AILANG. Consider:
- No mutable state - must use functional updates
- No loops - must use recursion (with depth limits!)
- Limited data structures - lists only, no arrays
- Known issues - check CLAUDE.md for current limitations

### 6. Design Doc Structure

**Game-specific sections:**
- **Game Vision Alignment**: Score against core pillars from `docs/vision/core-pillars.md`
- **Prior Decisions**: Reference relevant entries from `docs/vision/design-decisions.md`
- **Physics Validation**: (for visual features) What real physics principles apply?
- **Feature Overview**: What gameplay does this enable?
- **AILANG Implementation**: Types, functions, effects needed
- **Engine Integration**: How Go/Ebiten renders this
- **Performance**: Recursion depth, list operations needed
- **Testing**: How to verify the feature works

**When creating a design doc:**
1. Read `docs/vision/core-pillars.md` and score the feature
2. Check `docs/vision/design-decisions.md` for constraints
3. If this doc makes new design decisions, log them via `game-vision-designer`

**For visual/physics features, include:**
```markdown
## Physics Basis
- Effect: [name]
- Principle: [cite equation or physics concept]
- Reference: [link to physics explanation]

## Rejected Alternatives
| Hollywood Effect | Why Rejected |
|------------------|--------------|
| [effect] | [physics reason] |
```

### 7. Example: NPC Movement Design Doc

```markdown
# NPC Movement System

## Status
- Status: Planned
- Priority: P1
- Estimated: 2 days

## Game Vision Alignment

Checked against [core-pillars.md](docs/vision/core-pillars.md):

| Pillar | Alignment | Notes |
|--------|-----------|-------|
| Time Dilation Consequence | N/A | Infrastructure feature |
| Civilization Simulation | ✅ Supports | NPCs populate civilizations |
| Ship & Crew Life | ✅ Supports | Crew members use this system |
| Hard Sci-Fi Authenticity | N/A | No physics implications |

**Prior Decisions:** None directly relevant in design-decisions.md.

## Feature Overview
NPCs should move around the world grid, avoiding obstacles.

## AILANG Implementation

### Types (in sim/world.ail)
```ailang
type Direction = North | South | East | West
type MoveResult = Moved(Coord) | Blocked(string)
```

### Functions (in sim/npc_ai.ail)
```ailang
export pure func move(npc: NPC, dir: Direction, world: World) -> MoveResult
export pure func pathfind(npc: NPC, target: Coord, world: World) -> [Direction]
```

## Engine Integration
- Go code reads NPC positions from World state
- Renders sprites at grid positions * tile size

## Performance Concerns
- Pathfinding recursion: A* with depth limit
- List operations: O(n) for each tile lookup

## Success Criteria
- [ ] NPCs can move in 4 directions
- [ ] Movement blocked by obstacles
- [ ] No recursion overflow with 64x64 grid
```

## AILANG Feedback Integration

**If you encounter AILANG limitations while designing:**

1. Note the limitation in the design doc
2. Design a workaround
3. Report to AILANG core via `ailang-feedback` skill:
   ```bash
   ~/.claude/skills/ailang-feedback/scripts/send_feedback.sh feature \
     "Feature needed for <game feature>" \
     "Description of what would help" \
     "stapledons_voyage"
   ```

## Document Locations

```
design_docs/
├── planned/              # Future features
│   ├── feature.md
│   └── v0_1_0/           # Targeted for game v0.1.0
├── implemented/          # Completed features
│   └── v0_1_0/
└── README.md             # Feature index
```

## Best Practices

### 1. Start with AILANG Types
Define your data structures first - they drive the implementation.

### 2. Plan for Recursion Limits
Any operation on 64x64 grid (4096 tiles) needs careful design.

### 3. Test with `ailang check` Early
Type-check your planned code snippets before committing to the design.

### 4. Link to `ailang prompt`
Reference `ailang prompt` output when documenting AILANG syntax.

## Notes

- All game logic is AILANG, engine is Go/Ebiten
- Design docs should include AILANG code snippets
- Document workarounds for AILANG limitations
- Report feature requests to AILANG core
