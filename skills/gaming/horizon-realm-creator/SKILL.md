---
name: horizon-realm-creator
description: "Create Horizon Realms (Umbral pocket dimensions) for Mage: The Ascension 20th Anniversary Edition. Handles Rank, build points, Structure, Inhabitants, Magick, Security, merits/flaws, and maintenance costs. Requires mage-rules-reference for Practice/Resonance lookups. Cross-references sanctum-creator, library-creator, node-creator for sub-components. Triggers: create a horizon realm, design an umbral realm, M20 pocket dimension, chantry realm, umbral sanctuary."
---

# Horizon Realm Creator

Design mechanically valid Horizon Realms for M20.

## What is a Horizon Realm?

A pocket dimension in the Umbra, created by mages (requires **Spirit 5**) or occurring naturally. Unlike small Demesnes, Horizon Realms are substantial territories with their own physical laws, inhabitants, and histories. Many Chantries use them as primary bases.

## Rank, Build Points, and Maintenance

| Rank | Description | Build Pts | Base Maint (Q/mo) |
|------|-------------|-----------|-------------------|
| 1 | Trivial | 11 | 1 |
| 2 | Minor | 22 | 2 |
| 3 | Very Weak | 33 | 3 |
| 4 | Weak | 44 | 4 |
| 5 | Average | 55 | 5 |
| 6 | Strong | 70 | 10 |
| 7 | Very Strong | 85 | 15 |
| 8 | Significant | 100 | 20 |
| 9 | Powerful | 115 | 25 |
| 10 | Extremely Powerful | 150 | 50 |

**Build Points**: Spend on traits. Unspent points convert to +1 Quint/month maintenance each.

**Horizon Realm Background**: Costs double normal. Rating 1-5 = access only. Rating 6-10 = ownership (access + 5).

## Primary Earthly Connection

Every Realm has a Primary Earthly Connection—the first place it connected to Earth. Influences default Environment and nature. Need not be an active portal.

## Structure Traits

### Size (5 pts/dot)

| Dots | Description |
|------|-------------|
| 1 | Single room |
| 2 | Small building and yard |
| 3 | Large building and grounds |
| 4 | City-sized |
| 5 | Country-sized |
| 6 | Entire world |

### Environment (3 pts/dot)

| Dots | Description |
|------|-------------|
| 1 | Same as Primary Earthly Connection |
| 2 | Mundane, mostly similar to connection |
| 3 | Any mundane Earthly environment |
| 4 | Fully mundane but unearthly (gold cliffs, metal seas) |
| 5 | Magical with subtle effects |
| 6 | Anything possible (non-Euclidean, solid Time, fire rain) |

### Access Points (2 pts each)

Direct connections bypassing Avatar Storm and Pericarp. **One free** unless Inaccessible Flaw.

**Portal Types**: Permanent, Shifting, Keyed, One-Way, Guarded

## Inhabitant Traits

| Trait | Cost | 0 | 1 | 2 | 3 | 4 | 5 |
|-------|------|---|---|---|---|---|---|
| **Plants** | 2/dot | None | Few | Diverse local | Diverse global | Rare magical | Significantly magical |
| **Animals** | 2/dot | None | Few | Diverse local | Diverse global | Rare magical | Significantly magical |
| **People** | 5/dot | None | Few servants | Some unconnected | Self-sustaining | Mixed supernatural | Fully mixed society |
| **Ephemera** | 4/dot | Incidental | Few minor | Modest power | Few powerful unique | Most unique | Varied and diverse |

**People 2+**: Create named NPC profiles. **Ephemera 3+**: Create named spirit profiles.

See [references/inhabitant-templates.md](references/inhabitant-templates.md) for profile formats.

## Magick Traits

### Resonance (2 pts/dot)

Like Node Resonance—aligned magic gets bonuses, opposed gets penalties.

Query via mage-rules-reference:
```bash
python lookup.py references/resonance-traits.json "Forces"
```

### Focus (4 pts/dot)

Makes Practices coincidental or always Vulgar. Each dot either:
- Makes one Practice level (from 1) coincidental, OR
- Makes one Practice level (from 5) always Vulgar

**With Prism of Focus**: Use Reality Zone rules with Practice modifiers.

### Spheres (6 pts/dot)

Adds or subtracts 1 from Sphere ratings in Realm. Each dot = +1 or -1 to one Sphere.

**Note**: Allows use above Arete but doesn't grant extra dice.

### Special Phenomena (2 pts/rank, max = Realm Rank)

Universal Sphere-like effects, rated by total Sphere dots involved.

## Security Traits

### Guardians (3 pts/dot)

Dedicated guardian beings. Each dot = 10 Freebie Points for building guardians (Gods and Monsters pg. 121-220).

### Arcane (2 pts/dot)

Like the Background—makes Realm forgettable, destroys records.

## Additional Traits

| Trait | Cost | Effect |
|-------|------|--------|
| **Gauntlet Modifier** | 2 pts/±1 | Raise (Merit) or lower (Flaw) from default 5 |
| **Quintessence Wellspring** | 10 pts/Q/mo | Generates Quint (max = Rank) |
| **Dimensional Locks** | 4 pts each | Specific Sphere effects don't work |
| **Seasonal Cycle** | 2 pts/season | Realm has distinct seasons affecting magic |

## Merits and Flaws

See [references/merits-flaws.md](references/merits-flaws.md) for complete list.

**Common Merits**: Quintessence Efficient [7], Genius Locus [5], Spiritual Abode [2], Deep Umbral [4], Astral [3], Mobile [5], Morphic [6], Self-Repairing [6], Bountiful [1-5], Training Ground [5]

**Common Flaws**: Inaccessible [-4], Bleeding Out [-7], Dying [-8], Corrupted [-4], Parasitic [-5], Haunted [-2 to -5], Technocratic Interest [-3]

**Key Rules**:
- Quintessence Efficient can stack (each halves current maintenance)
- Bleeding Out doubles base maintenance (apply before Quintessence Efficient)
- Genius Locus: Attributes cost 3 pts, Abilities cost 1 pt, starts at 0

## Creation Workflow

### Phase 1: Concept
1. **Rank**: Power level (determines build points and maintenance)
2. **Creator(s)**: Who made it? (requires Spirit 5)
3. **Purpose**: Chantry base, sanctuary, research, prison, embassy
4. **Primary Earthly Connection**: Where it first connected
5. **Paradigm**: What magical philosophy it embodies

### Phase 2: Budget
Calculate build points from Rank. Plan allocation across Structure, Inhabitants, Magick, Security.

### Phase 3: Structure
Purchase Size, Environment, Access Points. Match to concept and purpose.

### Phase 4: Inhabitants
Purchase Plants, Animals, People, Ephemera. Create profiles for important inhabitants.

### Phase 5: Magick
Purchase Resonance, Focus, Spheres, Special Phenomena. Match to paradigm.

### Phase 6: Security
Purchase Guardians, Arcane. Design guardian beings using 10 FP/dot.

### Phase 7: Merits and Flaws
Select from [references/merits-flaws.md](references/merits-flaws.md). Balance story potential.

### Phase 8: Calculate Costs
```
Total Build Points Used = Sum of all trait costs + Merit costs - Flaw refunds
Remaining = Rank total - Used
Converted to Quint/Month = Remaining points (1:1)
Final Maintenance = Base + Converted + Merit/Flaw modifiers
```

### Phase 9: Create Sub-Components
Invoke other skills for Realm components:
- **sanctum-creator**: Sanctums within the Realm
- **library-creator**: Libraries within the Realm
- **node-creator**: Nodes connected to or within the Realm
- Guardian spirits using Gods and Monsters rules

### Phase 10: Write History
Creation circumstances, major events, Avatar Storm impact, current status.

## Validation Checklist

- [ ] Rank matches build points (11/22/33/44/55/70/85/100/115/150)
- [ ] Total costs ≤ available build points
- [ ] Maintenance source identified
- [ ] Quintessence Wellspring ≤ Realm Rank
- [ ] Special Phenomena ≤ Realm Rank
- [ ] Environment supports Plants/Animals ratings
- [ ] Size accommodates described features
- [ ] Merit/Flaw combinations are legal (see incompatibilities)
- [ ] People 2+ has named NPCs
- [ ] Ephemera 3+ has named spirits
- [ ] Sub-components have detail files (sanctums, libraries, nodes)
- [ ] Cross-linking complete between all files

### Incompatible Combinations
- Bountiful + barren Environment 1
- Inaccessible + purchased Access Points
- Has Subrealm + Rank ≤ 2
- Subrealm (Flaw) + Rank ≥ 8

## Chantry Integration

When creating as part of a chantry:
1. Include Horizon Realm Background in chantry budget (costs double)
2. Link to chantry document and history
3. Note which members live there, created it, maintain it
4. Connect Node/Library/Sanctum backgrounds appropriately

## Output Format

See [references/output-template.md](references/output-template.md) for complete format.

**Quick Summary Line**:
```
[Name]: Rank X | Size [desc] | Build: X pts | Maint: X Q/mo | [Key Merit/Flaw]
```

## Advanced Mechanics

See [references/advanced-mechanics.md](references/advanced-mechanics.md) for:
- Quintessence accounting and sources
- Node within Realm mechanics
- Background vs Rank distinction
- Merit/Flaw stacking rules
- Mobile Realm movement
- Genius Locus capabilities
