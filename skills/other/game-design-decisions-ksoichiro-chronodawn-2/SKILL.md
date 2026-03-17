---
name: game-design-decisions
description: Game design decisions and rationale (respawn, portals, progression)
---

# Critical Game Design Decisions

**Purpose**: Document critical game design decisions for Chrono Dawn mod to maintain consistency across features.

**How it works**: This skill is automatically activated when you mention tasks related to:
- Implementing respawn mechanics
- Designing dimension travel features
- Creating portal systems
- Balancing difficulty and progression
- Designing escape mechanisms for players

Simply describe what you want to do, and Claude will reference the appropriate guidance from this skill.

---

## Respawn Mechanics

**Decision Date**: 2025-10-26

### Core Decision

Chrono Dawn follows Minecraft's standard respawn behavior (like End dimension)

**Key Principles**:
1. Players respawn at bed/respawn anchor, or world spawn if none set
2. Portal Stabilizer does NOT affect respawn location
3. Portal Stabilizer only makes portal bidirectional (one-way → two-way)
4. Players can always escape by breaking bed and dying

---

## Rationale

### Maintains Tension

**One-Way Portal**: Creates sense of risk and commitment when entering Chrono Dawn

**Player Experience**: "Should I enter now, or prepare more?"

### Avoids Excessive Difficulty

**Escape Mechanism**: Players can always escape by:
1. Breaking their bed
2. Dying (respawns at world spawn)
3. Returning to Overworld via world spawn

**Prevents Softlocks**: Players never get permanently trapped

### Follows Minecraft Conventions

**Consistency with End Dimension**:
- End Dragon fight: One-way portal to End
- Escape: Defeat dragon or die
- Respawn: World spawn (if no bed)

**Player Expectations**: Experienced players understand this pattern

---

## Implementation Guidelines

### Portal Stabilizer

**Functionality**:
- Converts one-way portal to two-way portal
- Does NOT create respawn point
- Does NOT prevent death respawn to Overworld

**Code Implementation**:
```java
// Portal Stabilizer should only affect portal directionality
// NOT player respawn location
if (hasPortalStabilizer) {
    portal.setBidirectional(true);
}
// Respawn logic remains unchanged
```

### Bed/Respawn Anchor

**Functionality**:
- Standard Minecraft respawn mechanics apply
- Setting bed in Chrono Dawn: Respawn in Chrono Dawn
- No bed set: Respawn at world spawn (Overworld)

**Code Implementation**:
```java
// Use Minecraft's default respawn logic
// No custom overrides needed for Chrono Dawn dimension
```

### Dimension Travel

**One-Way Portal (Default)**:
- Overworld → Chrono Dawn: Works
- Chrono Dawn → Overworld: Does NOT work

**Two-Way Portal (with Portal Stabilizer)**:
- Overworld ↔ Chrono Dawn: Both directions work

---

## Edge Cases

### Player Dies in Chrono Dawn (No Bed Set)

**Expected Behavior**:
1. Player dies in Chrono Dawn
2. Player respawns at world spawn (Overworld)
3. Portal remains one-way (unless stabilized)

**Result**: Player must re-enter Chrono Dawn via portal

### Player Sets Bed in Chrono Dawn

**Expected Behavior**:
1. Player sets bed in Chrono Dawn
2. Player dies in Chrono Dawn
3. Player respawns at bed in Chrono Dawn

**Result**: Player stays in Chrono Dawn after death

### Player Wants to Leave Chrono Dawn (No Portal Stabilizer)

**Options**:
1. Craft Portal Stabilizer and return via portal
2. Break bed (if set) and die to respawn in Overworld
3. Use Ender Pearl/Enderman mechanics (if applicable)

**Recommended**: Option 2 (die to escape) for early-game players

### Player Sets Bed in Overworld, Then Dies in Chrono Dawn

**Expected Behavior**:
1. Player sets bed in Overworld
2. Player enters Chrono Dawn
3. Player dies in Chrono Dawn
4. Player respawns at bed in Overworld

**Result**: Standard Minecraft behavior, no custom logic needed

---

## Design Philosophy

### Tension vs. Frustration Balance

**Goal**: Create challenging experience without frustrating players

**Tension Mechanics** (Good):
- One-way portal creates commitment
- Resource management in dangerous dimension
- Risk/reward for exploring

**Frustration Mechanics** (Avoid):
- Permanent trapping with no escape
- Losing all progress due to softlock
- Unclear mechanics that surprise players

### Player Agency

**Core Principle**: Players should always have control over their fate

**Implementation**:
- Clear escape mechanism (die to return)
- Telegraphed danger (one-way portal is visible)
- Progression option (craft Portal Stabilizer for two-way travel)

### Consistency with Minecraft

**Follow Vanilla Patterns**:
- Respawn at bed/respawn anchor
- Dimension travel via portals
- No custom respawn logic unless necessary

**Benefits**:
- Players understand mechanics intuitively
- Less documentation needed
- Fewer bugs from custom systems

---

## Related Specifications

**Full Game Design Philosophy**: See `specs/chrono-dawn-mod/spec.md` → "Game Design Philosophy" section

**Portal Stabilizer Mechanics**: See `specs/chrono-dawn-mod/data-model.md` → "Portal Stabilizer" item

**Dimension Configuration**: See `common/src/main/resources/data/chronodawn/dimension/chrono_dawn.json`

---

## Future Considerations

### Potential Extensions (Not Decided)

**Question**: Should Portal Stabilizer have additional effects?

**Options**:
1. Create temporary respawn point (like respawn anchor)
2. Prevent mob spawning near portal
3. Teleport player to portal on death

**Status**: Not decided, requires further design discussion

**Recommendation**: Keep simple for now, add features based on player feedback

### Balancing Portal Stabilizer Cost

**Current**: Requires rare materials from Chrono Dawn

**Consideration**: Too expensive → frustrating, too cheap → removes tension

**Recommendation**: Playtest with different costs, adjust based on feedback

---

## Testing Checklist

When implementing respawn mechanics:

- [ ] Player with no bed dies in Chrono Dawn → respawns at world spawn (Overworld)
- [ ] Player with bed in Overworld dies in Chrono Dawn → respawns at Overworld bed
- [ ] Player with bed in Chrono Dawn dies in Chrono Dawn → respawns at Chrono Dawn bed
- [ ] Player with bed in Chrono Dawn breaks bed and dies → respawns at world spawn (Overworld)
- [ ] Portal without Portal Stabilizer → one-way only (Overworld → Chrono Dawn)
- [ ] Portal with Portal Stabilizer → two-way (Overworld ↔ Chrono Dawn)
- [ ] Portal Stabilizer does NOT affect respawn location

---

**Last Updated**: 2026-01-16
**Maintained by**: Chrono Dawn Development Team
