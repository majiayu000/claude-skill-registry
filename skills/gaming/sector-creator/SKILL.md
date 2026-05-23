---
name: sector-creator
description: "Create Sectors (Digital Web locations) for Mage: The Ascension 20th Anniversary Edition. Designs virtual locations with appropriate class, access levels, security, IC hazards, and Digital Web-specific features. Uses mage-rules-reference for Reality Zone/Practice lookups. Triggers: create a sector, design a digital web location, M20 sector, virtual adept base, digital realm."
---

# Sector Creator

Design Digital Web locations for M20—virtual spaces in the Umbral realm of information and data.

## What is a Sector?

A location within the Digital Web, ranging from secure data vaults to virtual paradises to corrupted wastelands. Virtual Adepts, Iteration X, and tech-savvy mages navigate and construct Sectors.

## Sector Class

| Class | Description |
|-------|-------------|
| **Virgin** | Unexplored, raw digital space |
| **Grid** | Standard navigable sector |
| **C-Sector** | Corrupted or contested zone |
| **Corrupted** | Heavily degraded sector |
| **Junklands** | Abandoned, decaying data |
| **Haunts** | Inhabited by digital entities |
| **Trash** | Deleted but not purged data |
| **Streamland** | High data flow areas |
| **Warzone** | Active conflict zone |

## Core Statistics

### Access Level

| Level | Description |
|-------|-------------|
| **Free** | Open to all Digital Web travelers |
| **Restricted** | Requires credentials or invitation |

### Security Level (0-10)

Higher = more IC (Intrusion Countermeasures) and barriers.

| Rating | Security |
|--------|----------|
| 0-2 | Minimal (public spaces) |
| 3-4 | Light (basic protection) |
| 5-6 | Moderate (standard commercial) |
| 7-8 | Heavy (corporate/government) |
| 9-10 | Maximum (black sites, AI cores) |

### Size Rating (1-6)

| Rating | Scale |
|--------|-------|
| 1 | Room (single virtual space) |
| 2 | Building (multiple connected rooms) |
| 3 | Block (small complex) |
| 4 | District (large interconnected area) |
| 5 | City (vast virtual territory) |
| 6 | Region (enormous digital landscape) |

### Power Rating

Paradox threshold—effects below this level are coincidental within the Sector.

## Digital Properties

### ARO Density

| Density | Description |
|---------|-------------|
| None | No interactive objects |
| Sparse | Occasional interactive elements |
| Moderate | Standard interactive environment |
| Dense | Highly interactive space |
| Overwhelming | Saturated with interactables |

### Data Flow Rate

| Rate | Description |
|------|-------------|
| Trickle | Minimal data movement |
| Steady | Normal flow |
| High | Significant traffic |
| Torrent | Overwhelming data streams |

### Time Dilation

Multiplier affecting time passage:
- **< 1.0**: Time passes slower (0.5 = half speed)
- **1.0**: Normal time
- **> 1.0**: Time passes faster (2.0 = double speed)

## Special Features

| Feature | Description |
|---------|-------------|
| Requires Password | Entry needs specific code |
| Has Lag | Whiteout risk (system instability) |
| Temporal Instability | Unpredictable time flow |
| Is Reformattable | Can be restructured by admin |

## Reality Zone

Sectors can have Reality Zones affecting Practice difficulties. Query valid Practices:
```bash
python lookup.py references/practices.json --keys
python lookup.py references/reality-zones.json "effects"
```

**Digital Web typical modifiers:**
- Reality Hacking, Hypertech, Cybernetics often favored
- Faith, Witchcraft, Shamanism often hindered

## Hazards

See [references/hazards.md](references/hazards.md) for IC types and Digital Web dangers.

## Creation Workflow

1. **Concept**: Purpose, controller, atmosphere
2. **Class**: Type of digital space
3. **Access Level**: Free or Restricted
4. **Security Level**: 0-10 based on protection needed
5. **Power Rating**: Paradox threshold
6. **Size**: Scale of the sector
7. **Digital Properties**: ARO Density, Data Flow, Time Dilation
8. **Special Features**: Password, lag, reformattable
9. **Reality Zone**: Practice modifiers (if any)
10. **Hazards**: IC programs, entities, environmental dangers
11. **Connections**: Links to other Sectors

## Validation Checklist

- [ ] Class matches concept
- [ ] Security level matches hazards described
- [ ] Access level appropriate for sector type
- [ ] Size rating fits described scope
- [ ] Reality Zone uses valid Practices only
- [ ] Visual style matches concept
- [ ] Connections to other Sectors noted

## Output Format

See [references/output-template.md](references/output-template.md) for complete format.

**Quick stat line:**
```
[Name]: [Class] | Access: [Level] | Security: [0-10] | Size: [1-6]
```
