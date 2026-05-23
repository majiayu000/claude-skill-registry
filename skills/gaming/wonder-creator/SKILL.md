---
name: wonder-creator
description: "Create Wonders (magical items) for Mage: The Ascension 20th Anniversary Edition. Handles Talismans (multi-power), Artifacts (single-power), Charms (one-use), and Periapts (Quintessence storage). Requires mage-rules-reference for Sphere/Resonance lookups and rote-creator for power design. Triggers: create a wonder, design a talisman, M20 magical item, enchanted object, create an artifact."
---

# Wonder Creator

Design mechanically valid Wonders for M20.

## Wonder Types

| Type | Powers | Arete | Reusable | Key Feature |
|------|--------|-------|----------|-------------|
| **Talisman** | Multiple (= Rank) | Yes | Yes | Most powerful, independent magic |
| **Artifact** | Single | No | Yes | Simpler permanent Wonder |
| **Charm** | Single | Yes | No | One-use, destroyed after |
| **Periapt** | Optional | Optional | Usually | Quintessence storage |

## Core Statistics (All Wonders)

### Rank (0-10)

| Rank | Description | Background Cost |
|------|-------------|-----------------|
| 0 | Trinket | 0 |
| 1-2 | Minor | 1-2 |
| 3-4 | Significant | 3-4 |
| 5 | Grand | 5 |
| 6-10 | Legendary | 6-10 |

Background Cost typically equals Rank.

### Resonance

Wonders have Resonance traits totaling at least Rank. Query traits:
```bash
python lookup.py references/resonance-traits.json "Forces"
# Output: Forces: Fiery, Bright, Energetic, Stormy, Electric, Kinetic
```

Common pattern: Choose traits matching the Wonder's Sphere affinities.

## Type-Specific Rules

### Talismans

The most sophisticated Wonders—permanent items with independent magical capability.

| Stat | Value |
|------|-------|
| **Powers** | = Rank (one power per rank) |
| **Arete** | 1-10 (typically ≤ Rank) |
| **Quintessence** | Rank × 5 |
| **Power Limit** | No power's Sphere level > Arete |

**Power Design**: Use **rote-creator** skill for each power. Each power needs:
- Sphere requirements
- Effect description
- Activation method
- Quintessence cost (if any)

### Artifacts

Single-power permanent Wonders. Simpler than Talismans.

| Stat | Value |
|------|-------|
| **Powers** | 1 |
| **Arete** | None (uses wielder's or fixed dice) |
| **Quintessence** | Optional storage |
| **Rank** | = Highest Sphere level in effect |

**Power Design**: Use **rote-creator** for the single effect.

### Charms

One-use Wonders destroyed after activation.

| Stat | Value |
|------|-------|
| **Powers** | 1 |
| **Arete** | = Rank (rolled on activation) |
| **Rank** | = Highest Sphere level |
| **After Use** | Destroyed, inert, or transformed |

**Common Forms**: Potions, scrolls, talismans (broken), bullets, gadgets (burn out)

### Periapts

Quintessence storage devices. May have secondary powers.

| Stat | Value |
|------|-------|
| **Max Charges** | See table below |
| **Consumable** | Yes (like Tass) or No (refillable) |
| **Secondary Power** | Optional |

**Capacity by Rank**:

| Rank | Max Charges |
|------|-------------|
| 1 | 5-10 |
| 2 | 10-20 |
| 3 | 20-30 |
| 4 | 30-50 |
| 5 | 50-100 |

**Charging Indicators**: How does charge level show? (Glow, warmth, weight, color, hum)

## Creation Workflow

1. **Type**: Talisman, Artifact, Charm, or Periapt?
2. **Concept**: What is it? Who made it? What paradigm?
3. **Rank**: Based on power level / capacity
4. **Powers**: Use rote-creator for each effect
5. **Resonance**: Traits totaling ≥ Rank (query mage-rules-reference)
6. **Physical Form**: Appearance matching paradigm
7. **History**: Origin, wielders, legends
8. **Validate**: Check type-specific rules

## Paradigm Forms

| Tradition | Typical Forms |
|-----------|---------------|
| Hermetic | Rings, wands, ceremonial objects, grimoires |
| Technocracy | Devices, implants, gadgets, programs |
| Verbena | Natural objects, blood items, living plants |
| Virtual Adept | Digital devices, interfaces, programs |
| Etherite | Ray guns, impossible machines, gadgets |
| Akashic | Meditation aids, martial implements |
| Celestial Chorus | Religious symbols, relics, icons |
| Dreamspeaker | Fetishes, spirit vessels, natural objects |

## Validation by Type

### Talisman
- [ ] Number of powers = Rank
- [ ] No power exceeds Arete
- [ ] Quintessence capacity = Rank × 5
- [ ] Resonance ≥ Rank
- [ ] Each power has Sphere requirements

### Artifact
- [ ] Single power only
- [ ] Rank = highest Sphere in effect
- [ ] Resonance ≥ Rank

### Charm
- [ ] Single power
- [ ] Arete = Rank
- [ ] Destruction/transformation noted
- [ ] Resonance ≥ Rank

### Periapt
- [ ] Max charges appropriate for Rank
- [ ] Consumable status noted
- [ ] Charging indicators described
- [ ] Resonance matches Quintessence source

## Output Format

Load the relevant template:
- **Talisman**: [references/talisman-template.md](references/talisman-template.md)
- **Artifact**: [references/artifact-template.md](references/artifact-template.md)
- **Charm**: [references/charm-template.md](references/charm-template.md)
- **Periapt**: [references/periapt-template.md](references/periapt-template.md)

**Quick stat lines:**

- **Talisman**: `Rank: X | Arete: X | Powers: X | Quint: X`
- **Artifact**: `Rank: X | Power: [brief] | Tradition: [origin]`
- **Charm**: `Rank: X | Arete: X | Form: [type] | One-use`
- **Periapt**: `Rank: X | Max: X | Consumable: Y/N`
