---
name: gd-design-weapon
description: Weapon and item design documentation. Use when designing weapons, creating item systems, balancing equipment, or designing consumables.
---

# Weapon Design

## Weapon Template

```markdown
## [Weapon Name]

### Type
[Category: melee, ranged, magic, etc.]

### Role
[Combat role: close-range, area denial, sniping, etc.]

### Stats
| Stat | Value | Description |
|------|-------|-------------|
| Damage | [X] | Per hit |
| Fire Rate | [Y] | Attacks per second |
| Accuracy | [Z] | Spread/recoil |
| Range | [R] | Effective distance |
| Magazine | [M] | Ammo capacity |
| Reload | [S] | Reload time |
| [Etc] | [...] | [...] |

### Handling
- **ADS speed:** [Zoom time]
- **Movement speed:** [While aiming]
- **Swap time:** [Equip speed]
- **Recoil pattern:** [Visual feedback]

### Damage Model
| Distance | Head | Body | Legs |
|----------|-----|------|------|
| [Close] | [X] | [Y] | [Z] |
| [Medium] | [X] | [Y] | [Z] |
| [Far] | [X] | [Y] | [Z] |

### Features
- **Feature 1:** [Description]
- **Feature 2:** [Description]

### Counterplay
**Countered by:**
- [Weapon/Strategy] - [Why it works]
- [Weapon/Strategy] - [Why it works]

### Skill Expression
**Floor:** [Minimum effectiveness]
**Ceiling:** [Maximum effectiveness with skill]

### Visual Design
- **Shape:** [Silhouette recognition]
- **Color:** [Team/affiliation indicators]
- **Animation:** [Attack animations]
- **Audio:** [Fire sounds, reload, etc.]

### Acquisition
- **Unlock:** [How to get it]
- **Cost:** [Price/crafting]
- **Rarity:** [Spawn rate]

### Asset Requirements
- **Asset Source:** [Asset pack name or "Custom"]
- **Format:** [FBX / GLB / GLTF / Custom]
- **Scale Factor:** [Documented scale value from asset testing]
- **Bone Attachment:** [Attachment point - e.g., "RightHand", "mixamorigRightHand"]

**Scale Reference:**
| Asset Pack | Typical Scale | Notes |
|------------|---------------|-------|
| Blaster Kit | 0.015 | CRITICAL: 0.15 is 10x too large |
| Mixamo | 1.0 | Standard meter scale |
| Custom | TBD | To be determined during implementation |

**Example Entry:**
```
Asset Source: Blaster Kit
Format: FBX
Scale Factor: 0.015
Bone Attachment: mixamorigRightHand
Notes: CRITICAL scale - 0.15 makes weapon GIGANTIC
```

**Why This Matters:**
- Asset packs have wildly different scale expectations
- Scale documentation prevents 10x size errors during implementation
- Bone attachment requirements vary by rig format (Mixamo vs custom)
- Pre-documenting reduces Developer-Tech Artist coordination overhead
```

## Weapon Categories

### Melee

Close-quarters combat:
- Swords, axes, maces
- Fist weapons
- Spears and polearms
- Daggers and knives

### Ranged

Distance combat:
- Pistols, rifles, shotguns
- Bows, crossbows
- Thrown weapons
- Magic staves

### Area of Effect

Multiple targets:
- Explosives
- Sprays and cones
- DoTs (Damage over Time)
- Summons

### Utility

Support items:
- Shields
- Grenades
- Traps
- Boosts

## Balance Framework

### Rock-Paper-Scissors

Every weapon category has counters:

```
Melee beats Shotgun
Shotgun beats Sniper
Sniper beats Rifle
Rifle beats LMG
etc.
```

### Niche Protection

Each weapon needs a role:
- **CQC** - Shotguns, SMGs
- **Mid-range** - Rifles
- **Long-range** - Snipers
- **Area denial** - LMGs, explosives

### Skill Indexing

Reward player skill:
- **Headshots** - Precision rewarded
- **Tracking** - Leading targets
- **Timing** - Window-based abilities
- **Positioning** - Map knowledge

## Item Design

### Consumables

Single-use items:
```
Effect → Duration → Cooldown
```

### Equipment

Persistent items:
```
Slot → Effect → Drawback
```

## Balance Levers

Tunable values for balance:

| Lever | Effect |
|-------|--------|
| Damage | Time to kill |
| Fire rate | DPS, ammo consumption |
| Accuracy | Effective range |
| Magazine | Sustained fire duration |
| Reload | Vulnerability window |
| Mobility | Positioning advantage |

## Weapon Review Checklist

Before finalizing a weapon:

- [ ] Clear role and use case
- [ ] Balanced stats for its role
- [ ] Has meaningful counterplay
- [ ] Skill ceiling exists
- [ ] Satisfying to use
- [ ] Distinct from other weapons
- [ ] Visual clarity
- [ ] Audio feedback
- [ ] Technical feasibility confirmed
