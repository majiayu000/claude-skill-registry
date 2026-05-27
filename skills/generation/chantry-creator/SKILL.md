---
name: chantry-creator
description: "Create Mage Chantries (Tradition/Convention strongholds) for Mage: The Ascension 20th Anniversary Edition. Orchestrates creation of complete chantry packages including main document, history, members, retainers, Nodes, Libraries, Sanctums, Horizon Realms, Grimoires, Rotes, Items, and Locations. Cross-references node-creator, library-creator, sanctum-creator, horizon-realm-creator, grimoire-creator, rote-creator, wonder-creator. Triggers: create a chantry, design a covenant, M20 chantry, mage stronghold, Tradition chantry, Technocracy construct."
---

# Chantry Creator

Create complete, interconnected M20 chantry packages.

## What This Skill Creates

A complete chantry package includes:
1. **Main Document** — Statistics, links, overview
2. **History** — Narrative history with timeline
3. **Members** — Mage profiles organized by role
4. **Retainers** — Sorcerers and Consors
5. **Nodes** — Via node-creator
6. **Libraries** — Via library-creator
7. **Sanctums** — Via sanctum-creator
8. **Horizon Realms** — Via horizon-realm-creator
9. **Grimoires** — Via grimoire-creator
10. **Rotes** — Via rote-creator
11. **Items** — Via wonder-creator (Charms, Talismans, Artifacts, Periapts)
12. **Locations** — Important areas within the chantry

All files are **comprehensively cross-linked**.

## Phase 1: Initial Concept

**Ask the user before creating:**

**Essential:**
1. **Faction**: Which Tradition, Convention, or Craft?
2. **Point Budget**: How many background points?
3. **Primary Purpose**: Library, Research, War, College, Fortress, Healing, Diplomatic?
4. **Location**: Region, setting type (urban/rural/hidden)

**Optional:**
5. **Season**: Spring (growing), Summer (peak), Autumn (stable), Winter (declining)
6. **Special Features**: Specific Nodes, Libraries, Horizon Realm?
7. **Membership Size**: Affects detail depth
8. **Chronicle Integration**: Standalone or specific chronicle?

## Phase 2: Research Faction Flavor

Query mage-rules-reference for faction data:
```bash
# Get chantry name (Covenant, Chapel, Grove, etc.)
python lookup.py references/faction-chantry-names.json "[Faction]"

# Get title system
python lookup.py references/faction-titles.json "[Faction]"

# Get available practices
python lookup.py references/faction-practices.json "[Faction]"

# Get common languages
python lookup.py references/faction-languages.json "[Faction]"
```

See [references/faction-reference.md](references/faction-reference.md) for:
- Naming conventions by faction
- How to apply title systems (by_arete vs by_role)

## Rank and Point Budget

| Points | Rank | Description |
|--------|------|-------------|
| 1-10 | 1 | Small, recently established |
| 11-20 | 2 | Established, modest resources |
| 21-30 | 3 | Significant, well-resourced |
| 31-70 | 4 | Major, extensive capabilities |
| 71+ | 5 | Legendary, vast power |

## Background Costs

| Cost | Backgrounds |
|------|-------------|
| **2/dot** | Allies, Arcane, Backup, Cult, Elders, Library, Retainers, Spies |
| **3/dot** | Node, Resources |
| **4/dot** | Enhancement, Requisitions |
| **5/dot** | Sanctum |
| **10/dot** | Horizon Realm |

**Multiple Instances**: A chantry may have multiple separate instances of the same Background (e.g., multiple Nodes at different ranks).

See [references/backgrounds.md](references/backgrounds.md) for full descriptions.

## Leadership Types

| Type | Description |
|------|-------------|
| Panel | Committee of equals |
| Teachers | Senior mages guide juniors |
| Triumvirate | Three leaders share power |
| Democracy | Members vote on decisions |
| Anarchy | No formal leadership |
| Single Deacon | One leader rules |
| Council of Elders | Oldest members decide |
| Meritocracy | Most capable lead |

## File Structure

```
/[chantry_name]/
├── [chantry_name].md          # Main document
├── history.md                  # History with timeline
├── members/
│   ├── leadership.md          # Council/leadership
│   ├── [role_group].md        # By function
│   ├── apprentices.md
│   └── retainers.md           # Sorcerers and Consors
├── nodes/
│   └── [node_name].md         # Via node-creator
├── libraries/
│   └── [library_name].md      # Via library-creator
├── sanctums/
│   └── [sanctum_name].md      # Via sanctum-creator
├── horizon_realm/
│   └── [realm_name].md        # Via horizon-realm-creator
├── grimoires/
│   └── [grimoire_name].md     # Via grimoire-creator
├── rotes/
│   └── [rote_name].md         # Via rote-creator
├── items/
│   ├── common/                # Chantry property
│   └── personal/              # Individual items
└── locations/
    └── [location_name].md     # Important areas
```

Use snake_case for all file/folder names.

## Creation Workflow

### Phase 3: Create Main Document

See [references/output-templates.md](references/output-templates.md) for format.

**Required sections:**
- Concept (2-3 paragraphs)
- Statistics tables (all entries link to files)
- Physical Location
- Magical Features (wards, integrated effects)
- Common Property (links to items)
- Political Position
- Story Hooks (3-5)

### Phase 4: Create History Document

**Structure:**
- Founding (2-3 paragraphs)
- Early Years (2-3 paragraphs)
- Growth and Development (2-3 paragraphs)
- Modern Era (2-3 paragraphs)
- **Timeline table** (Year | Event)
- Notable Historical Figures
- Legacy and Influence

**Timeline must reference:**
- Resource acquisition (Nodes, Libraries, Realms)
- Leadership changes
- Major conflicts
- Current members where relevant

### Phase 5: Create Member Profiles

See [references/member-guidelines.md](references/member-guidelines.md) for:
- Recommended counts by Rank
- Profile format
- Role organization
- Retainer guidelines (Sorcerers and Consors)

**Member profile includes:**
- Name with faction-appropriate title
- House/Sub-faction
- Arete rating
- Primary Spheres with levels
- Role in chantry
- Brief description (2-3 sentences)
- Cross-links to locations, grimoires, rotes, items

### Phase 6: Invoke Sub-Skills

**For each Node** — Invoke **node-creator**:
- Rank, name, location within chantry
- Faction/concept for thematic consistency
- Request links back to chantry document

**For each Library** — Invoke **library-creator**:
- Rank, name, focus, faction
- Reference specific grimoires to include

**For each Sanctum** — Invoke **sanctum-creator**:
- Rank, owner (with proper title), Tradition
- Location within chantry

**For Horizon Realm** — Invoke **horizon-realm-creator**:
- Realm Rank (NOT Background rating)
- Purpose, paradigm
- Request integration with chantry history

**For Grimoires** — Invoke **grimoire-creator**:
- Rank, faction, focus
- Request ALL rotes fully written via rote-creator

**For Signature Rotes** — Invoke **rote-creator**:
- Ward spells, communication rotes
- Initiation rituals, emergency protocols
- Signature techniques

**For Items** — Invoke **wonder-creator**:
- Charms (one-use), Talismans (multi-power)
- Artifacts (single-power), Periapts (Q storage)
- Track items mentioned in member profiles

### Phase 7: Create Location Files

For important areas within the chantry (Council Chamber, Observatory, Gardens, etc.):

```markdown
# [Location Name]

**Type:** [Room/Building/Area] | **Access:** [Open/Restricted/Leadership Only]

## Description
[2-3 paragraphs]

## Purpose
[Activities, who uses it]

## Notable Features
- [Feature with links]

## Associated Members
- [Member](../members/file.md#anchor) - [connection]

## Story Hooks
- [1-2 hooks]
```

### Phase 8: Cross-Linking Pass

**Every document links to:**
- Main chantry document
- History (when discussing events)
- Relevant members (anyone mentioned by name)
- Relevant locations
- Relevant items

**Link formats:**
```markdown
[Name](../folder/file.md)
[Name](file.md#section-name)
```

Anchors use lowercase with hyphens: `#magister-scholae-helena-valcourt`

### Phase 9: Validation

- [ ] Total background costs ≤ point budget
- [ ] Rank matches point total
- [ ] All members use faction-appropriate titles
- [ ] Arete levels appropriate for roles
- [ ] Every member/location/item mentioned is linked
- [ ] History references actual resources and members
- [ ] All items mentioned in profiles have files
- [ ] Sub-components created via appropriate skills

## Horizon Realm Integration

When a chantry has a Horizon Realm:

1. **Background Cost**: 10 pts/dot of Horizon Realm Background
   - Rating 1-5: Access
   - Rating 6-10: Ownership (access + 5)

2. **Realm Rank**: Separate from Background rating
   - Determines build points and maintenance
   - Higher Rank = more features but more maintenance

3. **Maintenance**: Must identify Quintessence source
   - Often from Node background
   - Note in chantry statistics

4. **Integration Requirements**:
   - Realm creation in chantry history timeline
   - Link from chantry to Realm document
   - Note which members live/work there
   - Connect Node/Library/Sanctum backgrounds appropriately

**Example:**
```
Horizon Realm 6 (Ownership of Rank 4 Realm): 60 pts
Node 4 (provides maintenance): 12 pts
```

## Quick Reference

Query faction data via mage-rules-reference:
```bash
# Chantry name
python lookup.py references/faction-chantry-names.json "[Faction]"

# Titles
python lookup.py references/faction-titles.json "[Faction]"

# Practices  
python lookup.py references/faction-practices.json "[Faction]"
```

See [references/faction-reference.md](references/faction-reference.md) for naming conventions.
