---
name: rote-creator
description: "Create rotes (codified magical effects) for Mage: The Ascension 20th Anniversary Edition (M20). Design mechanically balanced rotes with appropriate Sphere requirements, Practice associations, and paradigm-consistent flavor. Requires mage-rules-reference skill for Sphere/Practice/Ability lookups. Triggers: create a rote, design a magical effect, M20 rote, need a rote for [Tradition/Convention]."
---

# Rote Creator

Design mechanically valid, thematically rich rotes for M20.

## What is a Rote?

A rote is a magical effect practiced and refined to the point where it can be performed identically every time. Benefits over improvised magick:
- Roll Attribute + Ability instead of Arete
- More consistent results
- Defined mechanical parameters

## Creation Workflow

### 1. Clarify Intent
What effect does the mage want to achieve? Be specific about scope, target, and duration.

### 2. Determine Sphere Requirements
Query mage-rules-reference for guidance:
```bash
# What Spheres for a standard effect?
python lookup.py references/common-effects.json "Telepathy"

# What can Forces 3 do?
python lookup.py references/sphere-levels.json "Forces"

# Find effects involving a Sphere
python lookup.py references/common-effects.json --find "Life"
```

**Sphere Level Guidelines:**
- **1 (Initiate)**: Perception, sensing
- **2 (Apprentice)**: Minor manipulation, self/willing targets
- **3 (Disciple)**: Significant effects, affect others, temporary patterns
- **4 (Adept)**: Major transformations, permanent effects
- **5 (Master)**: Create from nothing, large-scale, perfect control

### 3. Assign Practice
Select a Practice fitting the mage's paradigm. Query associations:
```bash
# What abilities work with this Practice?
python lookup.py references/practice-abilities.json "High Ritual Magick"

# What practices does this faction use?
python lookup.py references/faction-practices.json "Virtual Adepts"
```

The mage's Practice rating must ≥ highest Sphere level in the rote.

### 4. Design Execution
- Choose instruments fitting the Practice
- Describe how the rote is performed
- Consider paradigmatic explanation

### 5. Determine Dice Pool
Select **Attribute + Ability** where:
- Ability is associated with the chosen Practice
- Combination makes sense for the effect

Common patterns:
- Perception effects: Perception + Awareness
- Combat effects: Dexterity + Ability or Wits + Ability
- Ritual effects: Intelligence + Occult/Esoterica
- Social effects: Manipulation + Expression/Subterfuge

### 6. Calculate Rote Cost
**Cost = Total Sphere dots**

Example: Life 3, Prime 2 = 5 points

- Characters begin with 6 points of rotes
- Additional: 4 Freebie Points or 3 XP per point
- Learning from teacher/grimoire: Half cost (requires source rating > highest Sphere)

### 7. Assess Paradox Risk
- **Coincidental**: Explainable by Sleeper logic, minimal risk
- **Vulgar without witnesses**: Moderate risk
- **Vulgar with Sleeper witnesses**: High risk

Provide guidance on making effects more coincidental when possible.

### 8. Write Description
See [references/output-template.md](references/output-template.md) for format.

## Validation Checklist

- [ ] Sphere levels match effect scope (not over/under-powered)
- [ ] Practice is appropriate to paradigm
- [ ] Ability is associated with chosen Practice
- [ ] Dice pool makes sense for the action
- [ ] Paradox assessment is accurate
- [ ] Foci fit the tradition
- [ ] Effect doesn't obsolete existing canon rotes without reason

## Key Principles

**Balance First**: Useful without being game-breaking

**Paradigm Matters**: A Virtual Adept's hack looks nothing like a Verbena's nature working achieving the same end

**Avoid Sphere Creep**: Don't require more Spheres than necessary

**Simple Effects Stay Simple**: Don't overengineer basic magic

## Conjunctional Effects

When combining Spheres:
- Primary Sphere determines the main effect
- Secondary Spheres extend reach, add properties, or enable the effect
- Highest Sphere level sets the baseline difficulty
- More Spheres = more versatile but higher cost

Common conjunctions:
- **Correspondence + X**: Affect at distance
- **Prime 2 + X**: Create patterns, add aggravated damage
- **Time 4 + X**: Trigger effects, delay effects
- **Spirit 3 + X**: Affect across Gauntlet
