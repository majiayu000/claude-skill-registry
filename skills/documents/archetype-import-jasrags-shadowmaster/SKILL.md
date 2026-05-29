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

## Gameplay Level Identification

Before beginning validation, identify the gameplay level based on resource allocation and restrictions.

| Level        | Starting Karma | Resources (A/B/C/D/E)    | Availability | Device Rating |
| ------------ | -------------- | ------------------------ | ------------ | ------------- |
| Street       | 13             | 75K/50K/25K/15K/6K       | ≤10          | ≤4            |
| Standard     | 25             | 450K/275K/140K/50K/6K    | ≤12          | ≤6            |
| Prime Runner | 35             | 500K/325K/210K/150K/100K | ≤15          | —             |

**Identification Heuristics:**

1. **Check resource totals** - If total gear exceeds 450K, likely Prime Runner
2. **Check availability** - If any item >12 availability, likely Prime Runner
3. **Check starting karma** - If negative qualities suggest >25 starting karma budget, likely Prime Runner
4. **Check device ratings** - If commlinks/decks >Rating 6, likely Prime Runner

**Output Format:**

```markdown
### Gameplay Level Identification

**Detected Level:** Standard
**Evidence:**

- Total resources: 249,500¥ (within 275K Budget B)
- Max availability: 12R (Wired Reflexes 2)
- Max device rating: 5 (Hermes Ikon)
- Estimated karma budget: 25 (standard)
```

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

---

## Karma Expenditure Validation

After priority inference, validate how the starting karma was spent.

### Karma Budget by Gameplay Level

| Level        | Starting Karma | Max Karma-to-Nuyen |
| ------------ | -------------- | ------------------ |
| Street       | 13             | 5 (→10,000¥)       |
| Standard     | 25             | 10 (→20,000¥)      |
| Prime Runner | 35             | 25 (→50,000¥)      |

### Karma Expenditure Categories

| Category                    | Cost               | Limit                                |
| --------------------------- | ------------------ | ------------------------------------ |
| Positive Qualities          | Listed cost        | ≤25 Karma total                      |
| Negative Qualities          | Receive listed     | ≤25 Karma bonus                      |
| Karma-to-Nuyen              | 1:2,000¥           | Level-dependent (see above)          |
| Active Skill                | New Rating × 2     | Max rating 6 (7 with Aptitude)       |
| Skill Group                 | New Rating × 5     | Max rating 6                         |
| Specialization              | 7 Karma            | One per skill                        |
| Attribute                   | New Rating × 5     | One Physical OR Mental at max        |
| Spells/Rituals/Preparations | 5 Karma each       | ≤Magic × 2 each category             |
| Complex Forms               | 4 Karma each       | ≤Logic                               |
| Focus Bonding               | Force × multiplier | Count ≤ Magic, Total Force ≤ Magic×2 |
| Power Points (Mystic Adept) | 5 Karma each       | ≤Magic rating                        |
| Contact                     | Connection+Loyalty | 2-7 Karma per contact, min 1+1       |

### Skill Karma Cost Reference

| From → To | Karma Cost | Cumulative (from 0) |
| --------- | ---------- | ------------------- |
| 0 → 1     | 2          | 2                   |
| 1 → 2     | 4          | 6                   |
| 2 → 3     | 6          | 12                  |
| 3 → 4     | 8          | 20                  |
| 4 → 5     | 10         | 30                  |
| 5 → 6     | 12         | 42                  |

### Karma-Optimal Skill Allocation

**CRITICAL:** When a character has more total skill points than their priority provides, the order of allocation matters significantly for karma efficiency.

**The Problem:**
If you allocate priority points to low-rated skills first, you'll be forced to buy high-rated skills with karma, which is extremely expensive.

**Example - Face (Elf) with Priority A Skills:**

- Priority A provides: 46 skill points + 10 group points
- Character needs: 48 skill points (2 over budget)
- Skills include: Etiquette 5, Negotiation 5, various 4s, and First Aid 1, Pilot Ground 1

**Wrong approach (expensive):**

- Allocate 46 points including First Aid 1 and Pilot Ground 1
- Buy remaining skills (e.g., Unarmed 2) with karma
- Cost: Unarmed 0→2 = 6 karma

**Correct approach (cheap):**

- Allocate 46 points to HIGH-value skills first (5s, 4s, then 2s)
- Buy the CHEAPEST skills (rating 1s) with karma
- Cost: First Aid 0→1 (2 karma) + Pilot Ground 0→1 (2 karma) = 4 karma

**Savings:** 2 karma (which can mean the difference between legal and illegal)

### Skill Allocation Order of Operations

When building a character with excess skill points:

1. **Calculate total skill points needed** (sum of all individual skill ratings)
2. **Calculate priority skill points available** (from priority table)
3. **Calculate excess** (needed - available)
4. **Sort skills by rating** (highest to lowest)
5. **Allocate priority points from highest-rated skills down**
6. **Leave the lowest-rated skills (rating 1s) to buy with karma**
7. **Verify karma cost** for the leftover skills

**Allocation Priority Order:**

1. Rating 6 skills (12 karma each to buy)
2. Rating 5 skills (10 karma each to buy)
3. Rating 4 skills (8 karma each to buy)
4. Rating 3 skills (6 karma each to buy)
5. Rating 2 skills (4 karma each to buy)
6. Rating 1 skills (2 karma each to buy) ← **Buy these with karma**

### Shadow Master Implementation Notes

When entering skills in Shadow Master:

1. **First:** Enter all skill groups (these use group points, not skill points)
2. **Second:** Enter high-rated individual skills (5s and 4s) using priority points
3. **Third:** Enter medium-rated skills (3s and 2s) using remaining priority points
4. **Last:** Enter rating-1 skills - these should consume karma, not priority points

If you run out of karma before completing all skills, **go back and reallocate**:

- Remove points from a rating-1 skill (freeing priority points)
- Add those points to a higher-rated skill that was using karma
- The rating-1 skill now uses karma (cheaper) instead of the higher-rated skill

### Focus Bonding Costs

| Focus Type       | Multiplier | F1  | F2  | F3  | F4  | F5  | F6  |
| ---------------- | ---------- | --- | --- | --- | --- | --- | --- |
| Qi Focus         | ×2         | 2   | 4   | 6   | 8   | 10  | 12  |
| Spell Focus      | ×2         | 2   | 4   | 6   | 8   | 10  | 12  |
| Spirit Focus     | ×2         | 2   | 4   | 6   | 8   | 10  | 12  |
| Enchanting Focus | ×3         | 3   | 6   | 9   | 12  | 15  | 18  |
| Metamagic Focus  | ×3         | 3   | 6   | 9   | 12  | 15  | 18  |
| Weapon Focus     | ×3         | 3   | 6   | 9   | 12  | 15  | 18  |
| Power Focus      | ×6         | 6   | 12  | 18  | 24  | 30  | 36  |

### Output Format

```markdown
### Karma Expenditure Validation

**Starting Karma:** 25 (Standard level)

| Category           | Items                           | Cost | Running Total  |
| ------------------ | ------------------------------- | ---- | -------------- |
| Positive Qualities | Ambidextrous (4), Toughness (9) | 13   | 13             |
| Negative Qualities | SINner (Corporate) (-25)        | -25  | -12            |
| Karma-to-Nuyen     | 5 Karma → 10,000¥               | 5    | -7             |
| Contact Pool       | Fixer (3/2), Street Doc (2/1)   | 8    | 1              |
| Focus Bonding      | Weapon Focus F3                 | 9    | 10             |
| Skills             | Pistols 1→2 (4), Sneak spec (7) | 11   | 21             |
| **Total Spent**    |                                 | 46   |                |
| **Net Karma**      | 25 - 46 + 25 (negatives)        | 4    | ✓ ≤7 carryover |

**Validation:**

- ✓ Positive qualities (13) ≤ 25 limit
- ✓ Negative qualities (25) ≤ 25 limit
- ✓ Karma-to-Nuyen (5) ≤ 10 limit (Standard)
- ✓ Remaining karma (4) ≤ 7 carryover limit
```

---

## Knowledge & Language Skill Validation

### Formula

```
Free Knowledge Points = (Intuition + Logic) × 2
```

### Example Calculation

| Intuition | Logic | Free Points |
| --------- | ----- | ----------- |
| 3         | 2     | 10          |
| 4         | 3     | 14          |
| 5         | 4     | 18          |

### Knowledge Skill Categories

| Category     | Linked Attribute |
| ------------ | ---------------- |
| Academic     | Logic            |
| Professional | Logic            |
| Interests    | Intuition        |
| Street       | Intuition        |

### Output Format

```markdown
### Knowledge & Language Skills

**Free Points:** (INT 4 + LOG 3) × 2 = **14 points**

| Skill                         | Category     | Rating | Points |
| ----------------------------- | ------------ | ------ | ------ |
| English                       | Language     | N      | 0      |
| Spanish                       | Language     | 3      | 3      |
| Seattle Street Gangs          | Street       | 4      | 4      |
| Corporate Security Procedures | Professional | 3      | 3      |
| Firearms Manufacturers        | Interests    | 2      | 2      |
| **Total**                     |              |        | **12** |

**Validation:** ✓ 12 points spent ≤ 14 available
```

---

## Contact Pool Validation

### Formula

```
Free Contact Karma = Charisma × 3
```

**Note:** This pool can ONLY be used for contacts, not other karma expenditures.

### Limits

- **Per Contact:** 2-7 Karma (min 1 Connection + 1 Loyalty)
- **No limit** on number of contacts

### Contact Cost Matrix

| Connection | Loy 1 | Loy 2 | Loy 3 | Loy 4 | Loy 5 | Loy 6 |
| ---------- | ----- | ----- | ----- | ----- | ----- | ----- |
| 1          | 2     | 3     | 4     | 5     | 6     | 7     |
| 2          | 3     | 4     | 5     | 6     | 7     | —     |
| 3          | 4     | 5     | 6     | 7     | —     | —     |
| 4          | 5     | 6     | 7     | —     | —     | —     |
| 5          | 6     | 7     | —     | —     | —     | —     |
| 6          | 7     | —     | —     | —     | —     | —     |

### Output Format

```markdown
### Contact Pool Validation

**Free Contact Karma:** CHA 3 × 3 = **9 Karma**

| Contact             | Connection | Loyalty | Cost  |
| ------------------- | ---------- | ------- | ----- |
| Fixer (Mr. Johnson) | 3          | 2       | 5     |
| Street Doc (Patch)  | 2          | 1       | 3     |
| **Total**           |            |         | **8** |

**Validation:** ✓ 8 Karma spent ≤ 9 available
**Excess to General Pool:** 1 Karma (can be used for other purchases)
```

---

## Magic Purchase Limits (Awakened Characters)

### Spells, Rituals, and Preparations

| Category     | Karma Cost | Creation Limit |
| ------------ | ---------- | -------------- |
| Spells       | 5 each     | ≤ Magic × 2    |
| Rituals      | 5 each     | ≤ Magic × 2    |
| Preparations | 5 each     | ≤ Magic × 2    |

**Example:** Magic 4 character can have up to 8 spells, 8 rituals, and 8 preparations.

### Focus Bonding Limits at Creation

| Limit            | Formula   |
| ---------------- | --------- |
| Max bonded count | ≤ Magic   |
| Max total Force  | ≤ Magic×2 |
| Force per test   | Only 1    |

**Example:** Magic 4 can bond up to 4 foci with total Force ≤ 8.

### Mystic Adept Power Points

- **Cost:** 5 Karma per Power Point
- **Limit:** Cannot exceed Magic rating
- **Note:** Adepts get Power Points free (= Magic rating)

### Output Format

```markdown
### Magic Validation

**Magic Rating:** 4 (Magician)
**Tradition:** Hermetic

**Spells (6/8 limit):**

- Stunbolt, Manabolt, Armor, Heal, Improved Invisibility, Levitate

**Foci (2 foci, Force 5/8 limit):**
| Focus | Force | Bonding Cost |
| -------------- | ----- | ------------ |
| Spell Focus | 3 | 6 Karma |
| Power Focus | 2 | 12 Karma |
| **Total** | 5 | **18 Karma** |

**Validation:**

- ✓ Spells (6) ≤ Magic×2 (8)
- ✓ Foci count (2) ≤ Magic (4)
- ✓ Total Force (5) ≤ Magic×2 (8)
```

---

## Creation Limits Summary

### Hard Limits (All Levels)

| Category               | Limit                |
| ---------------------- | -------------------- |
| Karma carryover        | ≤7                   |
| Nuyen carryover        | ≤5,000¥              |
| Positive qualities     | ≤25 Karma            |
| Negative qualities     | ≤25 Karma bonus      |
| Attribute augmentation | +4 max per attribute |
| Physical at max        | Only 1               |
| Mental at max          | Only 1               |
| Skill rating           | ≤6 (7 with Aptitude) |
| Bonded foci count      | ≤Magic               |
| Bonded foci Force      | ≤Magic × 2           |
| Spells per category    | ≤Magic × 2           |
| Complex forms          | ≤Logic               |
| Bound spirits          | ≤Charisma            |
| Registered sprites     | ≤Charisma            |

### Level-Dependent Limits

| Limit          | Street | Standard | Prime |
| -------------- | ------ | -------- | ----- |
| Starting Karma | 13     | 25       | 35    |
| Availability   | ≤10    | ≤12      | ≤15   |
| Device Rating  | ≤4     | ≤6       | —     |
| Karma-to-Nuyen | 5      | 10       | 25    |

### Output Format

```markdown
### Creation Limits Validation

| Limit                 | Value | Max   | Status |
| --------------------- | ----- | ----- | ------ |
| Karma carryover       | 4     | 7     | ✓      |
| Nuyen carryover       | 2,500 | 5,000 | ✓      |
| Positive qualities    | 13    | 25    | ✓      |
| Negative qualities    | 25    | 25    | ✓      |
| Physical at max       | 1     | 1     | ✓      |
| Mental at max         | 0     | 1     | ✓      |
| Max skill rating      | 6     | 6     | ✓      |
| Max availability      | 12R   | 12    | ✓      |
| Max device rating     | 5     | 6     | ✓      |
| Foci count            | 2     | 4     | ✓      |
| Foci total Force      | 5     | 8     | ✓      |
| Spells (per category) | 6     | 8     | ✓      |
```

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
2. **Check naming consistency** - Match exact names from catalog (see Fuzzy Matching below)
3. **Check availability limits** - Items must be ≤12 availability at creation (without qualities)

### Default Rating Rule

**CRITICAL:** When a stat block lists an item that has ratings in the database but does NOT specify a rating, **default to Rating 1**.

**Example:**

- Stat block shows: "Bug Scanner — 100¥"
- Database has: Bug Scanner (Rating 1-6, costs 100¥-600¥)
- Correct interpretation: Bug Scanner Rating 1 at 100¥

**Common rated items that often omit ratings:**
| Item | Rating Range | R1 Cost | R6 Cost |
|------|--------------|---------|---------|
| Bug Scanner | 1-6 | 100¥ | 600¥ |
| White Noise Generator | 1-6 | 50¥ | 300¥ |
| Jammer (Area) | 1-6 | 200¥ | — |
| Medkit | 1-6 | 250¥ | 1,500¥ |
| Fake SIN | 1-6 | 2,500¥ | 15,000¥ |
| Autopicker | 1-6 | 50¥ | 300¥ |

**Validation:** If the stat block price doesn't match Rating 1, check if it matches another rating and document accordingly.

### Fuzzy Matching for Item Names

**CRITICAL:** Sourcebook stat blocks often use slightly different names than the database. Before marking an item as "missing," perform fuzzy matching to find close matches.

#### Name Normalization Steps

When an exact match fails, normalize both the stat block name and database names:

1. **Remove/normalize hyphens and spaces:**
   - `Ultra Power` → `ultrapower`
   - `Ultra-Power` → `ultrapower`
   - Match: ✓

2. **Normalize Roman numerals vs digits:**
   - `Predator V` → `predator5`
   - `Predator 5` → `predator5`
   - Match: ✓

3. **Handle parenthetical variations:**
   - `Smartgun System (Internal)` → `smartgunsysteminternal`
   - `Internal Smartgun System` → search for "smartgun" + "internal"

4. **Case-insensitive comparison:**
   - `APDS` = `apds` = `Apds`

5. **Handle common abbreviations:**
   - `E-War` ↔ `Electronic Warfare`
   - `AR` ↔ `Assault Rifle`
   - `SMG` ↔ `Submachine Gun`

#### Fuzzy Search Algorithm

```
1. Exact match → Use database name
2. Normalized match (remove hyphens/spaces, lowercase) → Use database name
3. Substring match (stat block name contained in database name) → Flag as "close match"
4. Token overlap (≥80% of words match) → Flag as "close match"
5. No match → Mark as "missing"
```

#### Common Name Variations

| Stat Block Name      | Database Name         | Variation Type |
| -------------------- | --------------------- | -------------- |
| Browning Ultra Power | Browning Ultra-Power  | Hyphen         |
| Ares Predator 5      | Ares Predator V       | Roman numeral  |
| Ingram Smartgun X    | Ingram Smartgun XI    | Numeral typo   |
| Fichetti Sec 600     | Fichetti Security 600 | Abbreviation   |
| Earbuds              | Ear Buds              | Word split     |
| Hardware kit         | Hardware Toolkit      | Synonym        |
| Jammer (area)        | Area Jammer           | Word order     |
| Silencer             | Silencer/Suppressor   | Partial name   |
| Concealed holster    | Concealable Holster   | Adjective form |
| Regular ammunition   | Regular Rounds        | Synonym        |
| Wired Reflexes 2     | Wired Reflexes        | Rating in name |

#### Updated Validation Output Format

```markdown
### Matched Items (45/50)

**Exact matches:** 42 items found in `/data/editions/sr5/core-rulebook.json`

**Close matches (auto-corrected):**
| Stat Block Name | Database Name | Correction Applied |
| -------------------- | -------------------- | ------------------ |
| Browning Ultra Power | Browning Ultra-Power | Added hyphen |
| Earbuds | Ear Buds | Split words |
| Silencer | Silencer/Suppressor | Full name |

### Missing from Database (3 items)

| Item                     | Type     | Fuzzy Search Results               |
| ------------------------ | -------- | ---------------------------------- |
| Electrochromatic T-shirt | Clothing | No close matches found             |
| Custom Grip Mod          | Weapon   | Partial: "Grip" in 3 items         |
| Ares Roto-Drone MkII     | Drone    | Close: "Ares Roto-Drone" (no MkII) |
```

#### Implementation: grep Commands for Fuzzy Search

When validating items, use these grep patterns:

```bash
# Exact match
grep -i '"name": "Browning Ultra Power"' /data/editions/sr5/core-rulebook.json

# Normalized search (ignore hyphens/spaces)
grep -i '"name":.*browning.*ultra.*power' /data/editions/sr5/core-rulebook.json

# Partial/substring search
grep -i '"name":.*browning' /data/editions/sr5/core-rulebook.json | head -20

# Find all weapons to manually review
grep -i '"name":' /data/editions/sr5/core-rulebook.json | grep -i pistol
```

### Calculation Validation

1. **Essence tracking** - Sum all cyberware/bioware essence costs, verify matches stated essence
2. **Capacity tracking** - Verify enhancements don't exceed container capacity
3. **Cost verification** - Verify category subtotals and grand total
4. **Grade multipliers** - Verify cyberware costs include grade multipliers

### Hierarchy Validation

1. **Parent-child relationships** - Every enhancement must have a parent
2. **Capacity bounds** - No container can exceed its rated capacity
3. **License-SIN binding** - Licenses must match their parent SIN rating

### Karma & Budget Validation

1. **Karma budget** - Verify starting karma matches gameplay level (13/25/35)
2. **Positive qualities** - Total ≤25 Karma
3. **Negative qualities** - Total bonus ≤25 Karma
4. **Karma-to-Nuyen** - Verify conversion within level limit
5. **Karma carryover** - Remaining ≤7 Karma
6. **Nuyen carryover** - Remaining ≤5,000¥

### Knowledge & Contact Validation

1. **Knowledge points** - Verify total ≤ (INT + LOG) × 2
2. **Contact pool** - Verify total ≤ CHA × 3 (contacts only)
3. **Contact limits** - Each contact 2-7 Karma (min 1 Con + 1 Loy)

### Magic/Resonance Validation (if applicable)

1. **Spell limits** - Each category ≤ Magic × 2
2. **Focus count** - Bonded foci ≤ Magic
3. **Focus Force** - Total Force ≤ Magic × 2
4. **Complex forms** - Total ≤ Logic
5. **Bound spirits** - Count ≤ Charisma
6. **Registered sprites** - Count ≤ Charisma

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
