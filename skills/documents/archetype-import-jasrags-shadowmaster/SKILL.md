---
name: archetype-import
description: Imports Shadowrun 5e character archetypes from sourcebook stat blocks into hierarchical markdown and PDF documents with priority inference and data validation. Use when converting official SR5 archetypes to Shadow Master format.
allowed-tools: Read, Grep, Glob, Bash, Write
---

# Archetype Import Skill

This skill guides the import of official Shadowrun 5e character archetypes from sourcebook stat block images into structured markdown documents suitable for Shadow Master testing and development.

## Purpose

Convert published SR5 archetype stat blocks into:

1. Hierarchical markdown documents with proper equipment relationships
2. Priority inference calculations with confidence scores
3. Database validation reports against `core-rulebook.json`
4. PDF versions for easy sharing and printing

## Critical Rules

### Training Data Exclusion

**IMPORTANT:** When using existing example character files as reference:

- **EXCLUDE** any files matching `*-v*.md` pattern (e.g., `example-character-street-samurai-v2.md`)
- These versioned files are works-in-progress or experimental formats
- Only use base files like `example-character-street-samurai-ork.md` as training data

### Output Location

All archetype imports produce two files:

```
docs/data_tables/creation/example-character-{archetype-slug}-v{version}.md
docs/data_tables/creation/example-character-{archetype-slug}-v{version}.pdf
```

Where:

- `{archetype-slug}` = kebab-case archetype name (e.g., `street-samurai`, `combat-mage`)
- `{version}` = iteration number (start at `1`, increment for revisions)

The PDF is generated automatically from the markdown using `md-to-pdf`.

---

## Input Requirements

When importing an archetype, gather:

1. **Archetype name** (e.g., "Street Samurai", "Combat Mage")
2. **Metatype** (Human, Elf, Dwarf, Ork, Troll)
3. **Source** (book name and page number)
4. **Stats block image** (screenshot or scan of the archetype page)

---

## Hierarchical Structure Rules

Equipment in Shadowrun has parent-child relationships. The markdown output must reflect these hierarchies using sub-tables or bullet lists under the parent item.

### Pattern 1: Weapons with Modifications and Ammunition

**Good Example (Hierarchical):**

```markdown
## Weapons

### Ranged Weapons

| Weapon          | Type         | Accuracy | DV  | AP  | Mode | RC  | Ammo  | Cost |
| --------------- | ------------ | -------- | --- | --- | ---- | --- | ----- | ---- |
| Ares Predator V | Heavy Pistol | 5(7)     | 8P  | -1  | SA   | -   | 15(c) | 725¥ |

**Ares Predator V Modifications:**

- **Internal:** Smartgun System (Internal) [+2 Accuracy, 200¥]
- **Barrel:** Suppressor [Sound suppression, 500¥]

**Ares Predator V Ammunition:**

- Regular Ammo ×100 (10¥ per 10)
- APDS ×50 (-4 AP, 120¥ per 10)

| HK-227 | SMG | 5(7) | 7P | - | SA/BF/FA | 1 | 28(c) | 730¥ |

**HK-227 Modifications:**

- **Top:** Imaging Scope [Vision magnification, 300¥]
- **Under:** Gas-Vent 2 System [+2 RC, 400¥]
- **Stock:** Folding Stock [Concealability -2, 50¥]

**HK-227 Ammunition:**

- Explosive Rounds ×100 (-1 AP, +1 DV, 80¥ per 10)
```

**Bad Example (Flat):**

```markdown
| Item              | Cost |
| ----------------- | ---- |
| Ares Predator V   | 725¥ |
| Smartgun System   | 200¥ |
| Suppressor        | 500¥ |
| Regular Ammo ×100 | 10¥  |
```

### Pattern 2: Cyberware with Enhancements (Especially Cyberlimbs)

Cyberlimbs are capacity containers. Enhancements install INTO them.

**Good Example (Hierarchical):**

```markdown
## Augmentations

### Cyberware

| Augmentation              | Grade    | Essence | Capacity | Cost    |
| ------------------------- | -------- | ------- | -------- | ------- |
| Cyberarm (Right, Obvious) | Standard | 1.0     | 15       | 15,000¥ |

**Right Cyberarm Enhancements (10/15 capacity used):**

- Strength Enhancement +3 [3 capacity, 9,000¥]
- Agility Enhancement +3 [3 capacity, 9,000¥]
- Armor Enhancement +2 [2 capacity, 4,000¥]
- Cybergun (SMG, Ingram Smartgun X) [built-in, no capacity, 3,000¥]
- Slide Mount [2 capacity, 3,000¥]

**Right Cyberarm Totals:**

- STR: 6 base + 3 enhanced = 9
- AGI: 6 base + 3 enhanced = 9
- Armor: +2

| Cyberarm (Left, Obvious) | Standard | 1.0 | 15 | 15,000¥ |

**Left Cyberarm Enhancements (8/15 capacity used):**

- Strength Enhancement +3 [3 capacity, 9,000¥]
- Agility Enhancement +2 [2 capacity, 6,000¥]
- Cyber Spur [3 capacity, 7,000¥]
```

**Bad Example (Missing hierarchy):**

```markdown
| Augmentation            | Grade    | Essence | Cost    |
| ----------------------- | -------- | ------- | ------- |
| Cyberarm (Right)        | Standard | 1.0     | 15,000¥ |
| Strength Enhancement +3 | -        | -       | 9,000¥  |
| Agility Enhancement +3  | -        | -       | 9,000¥  |
```

### Pattern 3: Armor with Modifications

Armor has capacity equal to its armor rating. Mods consume capacity.

**Good Example:**

```markdown
### Armor

| Armor      | Rating | Capacity | Cost |
| ---------- | ------ | -------- | ---- |
| Lined Coat | 9      | 9        | 900¥ |

**Lined Coat Modifications (9/9 capacity used):**

- Chemical Protection 3 [3 capacity, 750¥]
- Fire Resistance 3 [3 capacity, 750¥]
- Nonconductivity 3 [3 capacity, 750¥]

| Armor Jacket | 12 | 12 | 1,000¥ |

**Armor Jacket Modifications (6/12 capacity used):**

- Insulation 3 [3 capacity, 600¥]
- Thermal Damping 3 [3 capacity, 1,500¥]
```

### Pattern 4: Fake SINs with Attached Licenses

Licenses attach TO a specific SIN at the same rating.

**Good Example:**

```markdown
### Identities

| Identity     | SIN Type | Rating | Cost    |
| ------------ | -------- | ------ | ------- |
| "John Smith" | Fake SIN | 4      | 10,000¥ |

**"John Smith" Licenses (Rating 4):**

- Concealed Carry Permit [200¥]
- Firearms License [200¥]
- Augmentation License [200¥]
- Driver's License [200¥]

| "Jane Doe" | Fake SIN | 2 | 5,000¥ |

**"Jane Doe" Licenses (Rating 2):**

- Driver's License [200¥]
```

### Pattern 5: Drones/Vehicles with Autosofts and Mounted Weapons

**Good Example:**

```markdown
### Drones

| Drone                 | Hand | Speed | Accel | Body | Armor | Pilot | Sensor | Cost   |
| --------------------- | ---- | ----- | ----- | ---- | ----- | ----- | ------ | ------ |
| MCT-Nissan Roto-Drone | 4    | 4     | 2     | 4    | 4     | 3     | 3      | 5,000¥ |

**Roto-Drone Loadout:**

- **Mounted Weapon:** AK-97 (Assault Rifle, removed stock)
- **Weapon Ammunition:** Regular Ammo ×200

**Roto-Drone Autosofts:**

- Clearsight 3 [600¥]
- Evasion 3 [600¥]
- Maneuvering (Roto-Drone) 3 [600¥]
- Targeting (Assault Rifle) 3 [600¥]

| Lockheed Optic-X2 | 4 | 4 | 3 | 1 | 0 | 3 | 3 | 21,000¥ |

**Optic-X2 Autosofts:**

- Clearsight 4 [800¥]
- Stealth 4 [800¥]
```

### Pattern 6: Cybereyes/Cyberears with Enhancements

**Good Example:**

```markdown
| Cybereyes (Rating 3) | Standard | 0.4 | 12 capacity | 10,000¥ |

**Cybereyes Enhancements (10/12 capacity used):**

- Flare Compensation [1 capacity, 250¥]
- Low-Light Vision [2 capacity, 500¥]
- Smartlink [3 capacity, 2,000¥]
- Thermographic Vision [2 capacity, 500¥]
- Vision Enhancement 2 [2 capacity, 1,000¥]

| Cyberears (Rating 2) | Standard | 0.3 | 8 capacity | 6,000¥ |

**Cyberears Enhancements (6/8 capacity used):**

- Audio Enhancement 2 [2 capacity, 500¥]
- Spatial Recognizer [2 capacity, 1,000¥]
- Select Sound Filter 2 [2 capacity, 500¥]
```

### Pattern 7: Commlinks with Running Programs

**Good Example:**

```markdown
### Matrix Gear

| Device               | Rating | Cost   |
| -------------------- | ------ | ------ |
| Hermes Ikon Commlink | 5      | 3,000¥ |

**Hermes Ikon Software:**

- AR Gloves [150¥]
- Mapsoft (Seattle) [20¥]
- Sim Module (Hot) [included]
```

---

## Priority Inference Methodology

### Step 1: Calculate Attribute Points Spent

For each attribute, calculate points purchased:

```
Points = (Current Value) - (Metatype Base)
```

**Metatype Base Attributes:**
| Metatype | BOD | AGI | REA | STR | WIL | LOG | INT | CHA |
|----------|-----|-----|-----|-----|-----|-----|-----|-----|
| Human | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| Elf | 1 | 2 | 1 | 1 | 1 | 1 | 1 | 3 |
| Dwarf | 3 | 1 | 1 | 3 | 2 | 1 | 1 | 1 |
| Ork | 4 | 1 | 1 | 3 | 1 | 1 | 1 | 1 |
| Troll | 5 | 1 | 1 | 5 | 1 | 1 | 1 | 1 |

**Example Calculation (Ork Street Samurai):**

```
Body 7:      7 - 4 (Ork base) = 3 points
Agility 6:   6 - 1 (Ork base) = 5 points
Reaction 5:  5 - 1 (Ork base) = 4 points
Strength 5:  5 - 3 (Ork base) = 2 points
Willpower 3: 3 - 1 (Ork base) = 2 points
Logic 2:     2 - 1 (Ork base) = 1 point
Intuition 3: 3 - 1 (Ork base) = 2 points
Charisma 2:  2 - 1 (Ork base) = 1 point
─────────────────────────────────────────
Total: 20 points → Priority B (20 points)
```

### Step 2: Calculate Skill Points/Groups

Count total skill points and skill group ratings:

- Sum all active skill ratings = skill points
- Sum all skill group ratings = group points

Match against priority table:
| Priority | Skills | Groups |
|----------|--------|--------|
| A | 46 | 10 |
| B | 36 | 5 |
| C | 28 | 2 |
| D | 22 | 0 |
| E | 18 | 0 |

### Step 3: Calculate Resources Spent

Sum all costs including:

- Weapons (base + mods + ammo)
- Armor (base + mods)
- Cyberware (with grade multipliers)
- Bioware (with grade multipliers)
- Gear
- Vehicles/Drones
- Lifestyle prepaid months
- Foci
- Commlinks/Cyberdecks

Match against priority table:
| Priority | Resources |
|----------|-----------|
| A | 450,000¥ |
| B | 275,000¥ |
| C | 140,000¥ |
| D | 50,000¥ |
| E | 6,000¥ |

### Step 4: Determine Magic/Resonance Priority

Based on magical path and attributes:

- **Priority A:** Magic 6 + spells/complex forms
- **Priority B:** Magic 4-5 or Adept Magic 6
- **Priority C:** Magic 3-4
- **Priority D:** Magic 2 (Adept/Aspected only)
- **Priority E:** Mundane

### Step 5: Determine Metatype Priority

Cross-reference metatype with special attribute points:
| Priority | Human | Elf | Dwarf | Ork | Troll |
|----------|-------|-----|-------|-----|-------|
| A | 9 | 8 | 7 | 7 | 5 |
| B | 7 | 6 | 4 | 4 | 0 |
| C | 5 | 3 | 1 | 0 | - |
| D | 3 | 0 | - | - | - |
| E | 1 | - | - | - | - |

Calculate special attribute points spent on Edge.

### Output Format

```markdown
## Priority Inference

### Attribute Points Calculation

- Body 7 (Ork base 4 + 3 purchased) = 3 points
- Agility 6 (base 1 + 5 purchased) = 5 points
- Reaction 5 (base 1 + 4 purchased) = 4 points
- Strength 5 (base 3 + 2 purchased) = 2 points
- Willpower 3 (base 1 + 2 purchased) = 2 points
- Logic 2 (base 1 + 1 purchased) = 1 point
- Intuition 3 (base 1 + 2 purchased) = 2 points
- Charisma 2 (base 1 + 1 purchased) = 1 point
- **Total: 20 points** → Priority B (20 points)

### Skills Calculation

- Automatics 5 + Blades 5 + Longarms 3 + Pilot Ground 1 + Pistols 4 + Sneaking 2 + Unarmed 2 = 22 points
- Skill Groups: 0
- **Total: 22/0** → Priority D

### Resources Calculation

| Category   | Subtotal     |
| ---------- | ------------ |
| Cyberware  | 195,000¥     |
| Weapons    | 8,500¥       |
| Ammunition | 2,000¥       |
| Armor      | 5,000¥       |
| Gear       | 12,000¥      |
| Lifestyle  | 15,000¥      |
| Vehicles   | 12,000¥      |
| **Total**  | **249,500¥** |

→ Priority B (275,000¥) with karma-to-nuyen conversion possible

### Metatype Calculation

- Metatype: Ork
- Edge: 1
- Special attribute points available at Priority C (Ork): 0
- **Matches Priority C**

### Magic Calculation

- Magical Path: Mundane
- **Priority E** (no magic required)

### Priority Summary

| Priority | Category   | Confidence | Notes                     |
| -------- | ---------- | ---------- | ------------------------- |
| A        | Resources  | 95%        | 249K close to 275K budget |
| B        | Attributes | 100%       | 20 points exact match     |
| C        | Metatype   | 100%       | Ork with 0 special        |
| D        | Skills     | 90%        | 22/0 matches D            |
| E        | Magic      | 100%       | Mundane                   |
```

---

## Validation Requirements

### Pre-Generation Validation

Before generating the markdown:

1. **Check item existence** - Verify all items exist in `/data/editions/sr5/core-rulebook.json`
2. **Check naming consistency** - Match exact names from catalog
3. **Check availability limits** - Items must be ≤12 availability at creation (without qualities)

### Calculation Validation

1. **Essence tracking** - Sum all cyberware/bioware essence costs, verify matches stated essence
2. **Capacity tracking** - Verify enhancements don't exceed container capacity
3. **Cost verification** - Verify category subtotals and grand total
4. **Grade multipliers** - Verify cyberware costs include grade multipliers

### Hierarchy Validation

1. **Parent-child relationships** - Every enhancement must have a parent
2. **Capacity bounds** - No container can exceed its rated capacity
3. **License-SIN binding** - Licenses must match their parent SIN rating

### Validation Output Format

```markdown
## Validation Report

### Matched Items (45/50)

All found in `/data/editions/sr5/core-rulebook.json`

### Missing from Database

| Item            | Type       | Suggested Action        |
| --------------- | ---------- | ----------------------- |
| Custom Grip     | Weapon Mod | Add to weaponMods array |
| Ares Roto-Drone | Drone      | Add to drones array     |

### Calculation Discrepancies

| Calculation | Expected | Actual   | Discrepancy |
| ----------- | -------- | -------- | ----------- |
| Essence     | 0.88     | 0.76     | 0.12        |
| Resources   | 450,000¥ | 435,000¥ | 15,000¥     |

### Capacity Violations

| Container      | Capacity | Used | Overflow |
| -------------- | -------- | ---- | -------- |
| Right Cyberarm | 15       | 17   | 2        |

### Common Transcription Errors Detected

- "Ares Predator 5" → Should be "Ares Predator V"
- "Wired Reflexes Rating 2" → Check if essence matches Rating 2 (3.0)
- "Smartlink" → Verify if internal (capacity 0) or external (mount required)
```

---

## Complete Workflow

### Phase 1: Receive Input

1. User provides archetype name, metatype, and stat block image
2. Confirm source book and page number

### Phase 2: Extract Data

1. Read all attributes from stat block
2. Read all skills and specializations
3. Read all qualities (positive and negative)
4. Read all equipment with costs
5. Read all augmentations with grades
6. Note any contacts

### Phase 3: Build Hierarchy

1. Group weapons with their mods and ammo
2. Group armor with its mods
3. Group cyberlimbs with their enhancements
4. Group cyber eyes/ears with their enhancements
5. Group drones with their autosofts and weapons
6. Group SINs with their licenses

### Phase 4: Calculate Priorities

1. Calculate attribute points spent
2. Calculate skill points and groups
3. Sum all resource costs
4. Determine magic/resonance path
5. Determine metatype special points
6. Generate priority table with confidence scores

### Phase 5: Validate

1. Check all items against database
2. Verify calculations (essence, capacity, costs)
3. Flag missing items and discrepancies
4. Generate validation report

### Phase 6: Generate Markdown

1. Create markdown file at `docs/data_tables/creation/example-character-{slug}-v1.md`
2. Include all sections with proper hierarchy
3. Include priority inference section
4. Include validation report

### Phase 7: Generate PDF

1. Convert markdown to PDF using `md-to-pdf`
2. Output PDF to same directory as markdown file
3. Verify PDF was created successfully

**Command:**

```bash
cd docs/data_tables/creation && npx --yes md-to-pdf example-character-{slug}-v{version}.md
```

This generates `example-character-{slug}-v{version}.pdf` alongside the markdown file.

### Phase 8: Report

1. Summarize what was imported
2. List any items needing database addition
3. List any calculation discrepancies
4. Provide paths to both markdown and PDF files
5. Recommend next steps

---

## Reference Files

| File                                                | Purpose                           |
| --------------------------------------------------- | --------------------------------- |
| `/data/editions/sr5/core-rulebook.json`             | Database for validation           |
| `/docs/data_tables/creation/priority_table.md`      | Priority values                   |
| `/lib/types/character.ts`                           | Grade multipliers, gear types     |
| `/lib/types/edition.ts`                             | Catalog item schemas              |
| `/docs/data_tables/creation/example-character-*.md` | Format examples (exclude _-v_.md) |

---

## Key Files for Quick Reference

See `REFERENCE.md` in this skill directory for:

- Priority tables (all 5 categories)
- Metatype base attributes
- Cyberware grade multipliers
- Cyberlimb capacity by type
- Common hierarchy patterns
- Validation checklist
