---
name: paradox-realm-creator
description: "Create Paradox Realms (punishment dimensions) for Mage: The Ascension 20th Anniversary Edition. Designs realms based on triggering Sphere, paradigm logic, obstacles, and escape conditions. Uses mage-rules-reference for Sphere information. Triggers: create a paradox realm, design a punishment dimension, M20 paradox realm, mage trapped by paradox."
---

# Paradox Realm Creator

Design Paradox Realms—pocket dimensions created by Paradox to punish mages who abuse vulgar magick.

## What is a Paradox Realm?

A pocket dimension tailored to the mage's Resonance, paradigm, and transgressions. The realm punishes through obstacles that challenge the mage's beliefs. Escape requires overcoming these challenges.

## Realm Characteristics by Sphere

The triggering Sphere determines the realm's nature:

| Sphere | Realm Nature |
|--------|--------------|
| **Correspondence** | Space is wrong—distances lie, locations shift, no path is straight |
| **Entropy** | Decay and chaos—things break, luck fails, entropy accelerates |
| **Forces** | Energy run wild—storms, temperature extremes, uncontrolled power |
| **Life** | Biological horror—mutation, predators, disease, bodily betrayal |
| **Matter** | Solid reality—traps, puzzles, transformation, crushing weight |
| **Mind** | Mental trials—illusions, madness, memory loss, identity erosion |
| **Prime** | Quintessence distortion—magical paradoxes, pattern unraveling |
| **Spirit** | Spirit realm—hostile entities, tests, bargains with consequences |
| **Time** | Temporal anomalies—loops, aging, freeze, causality breakdown |

Query Sphere capabilities via mage-rules-reference:
```bash
python lookup.py references/sphere-levels.json "[Sphere]"
```

## Paradigm Logic Types

The worldview that shapes the realm's internal logic:

| Paradigm | Logic |
|----------|-------|
| Mechanistic Cosmos | Clockwork, gears, precise laws |
| Chaos | Random, unpredictable, mutable |
| Data | Digital, informational, code-based |
| Faith | Religious, moral, devotional |
| Antimagick | Hostile to all supernatural |
| Divine Order | Heavenly hierarchy and judgment |
| Scientific Method | Laboratory, experimentation |
| Primal Nature | Wild, natural, animalistic |
| Dream Logic | Surreal, symbolic, fluid |
| Technological | Machine, electronic, systematic |
| Mystical | Traditional occult symbolism |
| Martial | Combat, warfare, challenge |

## Severity and Obstacles

| Severity | Paradox Points | Primary Obstacles | Random Obstacles |
|----------|----------------|-------------------|------------------|
| Mild | 1-5 | 1 | 0-1 |
| Moderate | 6-10 | 2 | 1-2 |
| Severe | 11-15 | 3-4 | 2-3 |
| Catastrophic | 16+ | 4-6 | 3+ |

**Primary Obstacles**: Based on the triggering Sphere
**Random Obstacles**: Based on secondary Sphere or random selection

See [references/obstacles.md](references/obstacles.md) for obstacle tables.

## Final Obstacle Types

The escape condition:

| Type | Escape Requirement |
|------|-------------------|
| Give Secret | Reveal hidden truth about self |
| Win Game | Complete a challenge or contest |
| Solve Riddle | Answer a paradigm-based puzzle |
| Button | Find and activate escape mechanism |
| Maze | Navigate to the exit |
| Abnormal Maze | Non-Euclidean navigation |
| Silver Bullet | Find specific weakness to exploit |
| Guess Name | Identify the realm's true nature |
| Random Sphere | Overcome Sphere-specific challenge |
| Combined | Multiple final obstacles |

## Creation Workflow

1. **Triggering Event**: What vulgar magick caused this? How severe?
2. **Primary Sphere**: Which Sphere was abused?
3. **Secondary Sphere** (optional): Additional influence?
4. **Paradigm Logic**: What worldview shapes the realm?
5. **Obstacle Count**: Based on severity
6. **Design Obstacles**: See [references/obstacles.md](references/obstacles.md)
7. **Final Obstacle**: Choose escape condition
8. **Atmosphere**: Physical appearance, sensory details, emotional weight
9. **Consequences**: What happens on failure?

## Thematic Principles

**Punishment fits the crime**: A Time mage who rewound events faces time loops. A Life mage who transformed others becomes the hunted prey.

**Paradigm inversion**: The realm often inverts or corrupts the mage's own paradigm. A technocrat faces mystical nonsense. A Hermetic faces chaotic disorder.

**Personal resonance**: The realm draws on the mage's own Resonance, fears, and history.

**Escapable but costly**: Escape must be possible but should require sacrifice, insight, or growth.

## Validation Checklist

- [ ] Primary Sphere matches triggering magick
- [ ] Paradigm consistently shapes realm logic
- [ ] Obstacle count matches severity
- [ ] Obstacles relate to Spheres appropriately
- [ ] Final obstacle is challenging but escapable
- [ ] Atmosphere reinforces psychological horror
- [ ] Realm teaches a lesson about the transgression
- [ ] Consequences of failure are defined

## Output Format

See [references/output-template.md](references/output-template.md) for complete format.

**Quick stat line:**
```
[Name]: [Primary Sphere] | [Paradigm] | [Severity] | [Final Obstacle Type]
```
