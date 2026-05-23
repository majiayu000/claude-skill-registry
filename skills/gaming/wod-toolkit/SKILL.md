---
name: wod-toolkit
description: "World of Darkness 20th Anniversary toolkit for Vampire (V20), Werewolf (W20), Mage (M20), Wraith (Wr20), Changeling (C20), Demon (D20). Creates characters, locations, items, organizations, weapons. Triggers: WoD, Vampire, Kindred, clan, ghoul, Garou, tribe, Gift, caern, Tradition, Technocracy, Sphere, rote, Arcanoi, Kithain, Art, spirit, Umbra, crossover, weapon stats, firearm, melee, ranged, Demon, Fallen, House, Lore, evocation, Earthbound, thrall, pact, apocalyptic form, Faith, Torment."
---

# WoD Toolkit

Unified toolkit for World of Darkness 20th Anniversary Edition content creation across all six classic gamelines.

## Game Detection

| Trigger Keywords | Game | Entry Point |
|------------------|------|-------------|
| V20, Vampire, Kindred, Clan, Discipline, Camarilla, Sabbat, Anarch, ghoul, blood, Tal'Mahe'Ra, Black Hand, elder, infernalist, ritae, vampire hunter | **Vampire** | `overviews/vampire.md` |
| W20, Werewolf, Garou, tribe, auspice, Gift, rite, fetish, Umbra, spirit, caern, Fera | **Werewolf** | `overviews/werewolf.md` |
| M20, Mage, Tradition, Technocracy, Sphere, rote, Paradox, Arete, chantry, wonder, Archmage | **Mage** | `overviews/mage.md` |
| Wr20, Wraith, ghost, Arcanoi, Shadow, Haunt, Legion, Guild, Spectre, Risen, medium, ghost hunter | **Wraith** | `overviews/wraith.md` |
| C20, Changeling, Kithain, kith, Art, Realm, Glamour, Banality, freehold, Dreaming | **Changeling** | `overviews/changeling.md` |
| D20, Demon, Fallen, House, Lore, evocation, Faith, Torment, apocalyptic form, Visage, thrall, pact, Earthbound, Namaru, Asharu, Annunaki, Neberu, Lammasu, Rabisu, Halaku | **Demon** | `overviews/demon.md` |
| crossover, multi-splat, weapon, weapon stats, firearm, melee, ranged, thrown | **Shared** | `modules/shared/` |

---

## Workflow

1. **Detect game** from user request
2. **Load overview** for that game
3. **Select module** from overview's module table
4. **Read module** before creating content
5. **Use references** for detailed data
6. **Validate** against module checklist

---

## Reference Files

| Reference | Path | Use When |
|-----------|------|----------|
| Character creation tables | `references/character-creation.md` | Allocating dots, freebie costs |
| Key decisions | `references/key-decisions.md` | Resolving conflicts between books |
| Crossover guidance | `modules/shared/crossover.md` | Multi-splat content |
| Weapon templates | `references/weapon-output-templates.md` | Creating weapon stat blocks |
| Connection network | `references/connection-network.md` | NPC relationships (M20) |

---

## Data Lookup

All game data is in `references/data.json`. Use `scripts/lookup.py` to query:

```bash
# List all categories
python scripts/lookup.py

# List objects in a category
python scripts/lookup.py v20.disciplines

# Get a specific object
python scripts/lookup.py v20.disciplines disciplines Dominate

# Search across all data
python scripts/lookup.py --search Brujah

# Search within a category
python scripts/lookup.py v20.rules --search generation
```

### Common Categories

| Category | Contents |
|----------|----------|
| `shared.core` | attributes, abilities, archetypes, backgrounds, true-faith |
| `shared.spirits` | hierarchy, charms |
| `v20.disciplines` | disciplines, combination-disciplines, elder-disciplines, bloodline-disciplines |
| `v20.rules` | clans, bloodlines, generation, paths-of-enlightenment |
| `v20.character` | backgrounds, merits-flaws |
| `w20.rules` | tribes, auspices, breeds |
| `w20.gift` | gifts-by-source |
| `m20.rules` | sphere-details, paradigms, practices, tenets, subfactions |
| `m20.technocracy` | conventions, methodologies, equipment |
| `m20.npcs` | faces-of-magick |
| `wr20.arcanoi` | arcanoi-summary |
| `wr20.factions` | legions, guilds |
| `c20.kith` | kithain, regional-kith |
| `c20.arts` | arts |

---

## Directory Structure

```
wod-toolkit/
├── SKILL.md                 ← This file (router)
├── overviews/               ← Game entry points with module tables
│   ├── vampire.md, werewolf.md, mage.md, wraith.md, changeling.md, demon.md
├── modules/
│   ├── v20/                 ← Vampire modules
│   ├── w20/                 ← Werewolf modules
│   ├── m20/                 ← Mage modules
│   ├── wr20/                ← Wraith modules
│   ├── c20/                 ← Changeling modules
│   ├── d20/                 ← Demon modules
│   └── shared/              ← Cross-game modules
├── references/
│   ├── data.json            ← All game data
│   ├── character-creation.md ← Allocation tables
│   ├── key-decisions.md     ← Conflict resolutions
│   ├── connection-network.md ← NPC relationships
│   ├── weapon-output-templates.md
│   └── m20/                 ← M20-specific templates
└── scripts/
    └── lookup.py            ← Data query utility
```

---

## Additional Trigger Keywords

Extended triggers for specialized content:

**Vampire**: Tal'Mahe'Ra, Black Hand, Enoch, Bahari, Koldunism, methuselah, infernalist, ritae, Vaulderie, Blood Brothers, Dark Thaumaturgy, Anarch sorcery, Hunters Hunted, Society of Leopold, Project Twilight, Inquisition, True Faith, combination discipline, Free State, Baron, SchreckNet

**Mage**: Faces of Magick, notable NPC, Charon, Black Jacket, Crusader, Archmage, Disparate, Craft, Nephandi, Technocrat

**Wraith**: ghost hunter, medium, psychic, Numina, cryptid, paranormal investigator

**Changeling**: Nunnehi, chimera, treasure

**Demon**: Devils, Scourges, Malefactors, Fiends, Defilers, Devourers, Slayers, Faustian, Cryptic, Luciferan, Reconciler, Ravener, Visage, apocalyptic traits, Bel, Nusku, Qingu, Dagan, Anshar, Ellil, Kishar, Antu, Mummu, Ninsun, Nedu, Shamash, Ishhara, Adad, Mammetum, Zaltu, Ninurtu, Aruru, Namtar, Nergal, Ereshkigal, reliquary, court, haunt
