---
name: doc-maintenance
description: Guide documentation updates when changing versions, adding content, or preparing releases
---

# Documentation Maintenance

**Purpose**: Guide documentation updates when changing versions, adding content, or preparing releases.

**How it works**: This skill is automatically activated when you mention tasks related to:
- Updating Minecraft or dependency versions
- Adding new bosses, structures, or items
- Preparing for a release
- Adding new mod dependencies

Simply describe what you want to do, and Claude will reference the appropriate checklist from this skill.

---

## Version Update Checklist

**When to use**: Updating Minecraft version, mod loader versions, or dependency versions

### Files to Update

1. **gradle.properties**
   - Update version properties
   - Example: `minecraft_version=1.21.1`

2. **README.md** (lines ~47-50)
   - Section: "Requirements" → "Dependencies"
   - Update all version numbers

3. **docs/player_guide.md** (lines ~25-56)
   - Sections: "Prerequisites" and "Required Dependencies"
   - Update version numbers and download links

4. **docs/developer_guide.md** (lines ~32-45)
   - Section: "Key Technologies"
   - Update version specifications

5. **docs/curseforge_description.md** (lines ~125-128)
   - Section: "Technical Details" → "Requirements" → "Dependencies"
   - Update version numbers

6. **docs/modrinth_description.md** (lines ~30-39)
   - Sections: "Requirements" (both Fabric and NeoForge)
   - Update version numbers

7. **fabric/src/main/resources/fabric.mod.json**
   - Update `depends` section version ranges
   - Update `recommends` section if applicable

8. **neoforge/src/main/resources/META-INF/neoforge.mods.toml**
   - Update `[[dependencies.chronodawn]]` entries
   - Update `versionRange` fields

9. **THIRD_PARTY_LICENSES.md**
   - Update version numbers in "Runtime Dependencies" section
   - Update: Minecraft, Fabric Loader, Fabric API, NeoForge, Architectury API
   - Update "Last updated" date at the bottom

### Current Versions (Reference)

```
Minecraft: 1.21.1
Fabric Loader: 0.17.3+
Fabric API: 0.116.7+
NeoForge: 21.1.209+
Architectury API: 13.0.8+
```

**After updating**, update this reference list in this skill file.

---

## Adding a New Boss

**When to use**: Adding a new boss enemy to the mod

### Files to Update

1. **README.md** (lines ~25-31)
   - Section: "Boss Enemies" list
   - Add: `- Boss Name (description, drops Item Name)`

2. **docs/player_guide.md**
   - Section: "Boss Battles"
   - Add full entry with:
     - Stats (Health, Attack, Defense)
     - Abilities (list special attacks)
     - Strategy (combat tips)
     - Drops (items dropped)

3. **docs/curseforge_description.md** (lines ~28-35)
   - Section: "Powerful Boss Battles"
   - Add boss to appropriate category (mini-boss, mid-boss, final boss)

4. **docs/modrinth_description.md** (lines ~105-140)
   - Section: "Boss Battles"
   - Add boss entry with stats and abilities

5. **specs/chrono-dawn-mod/spec.md**
   - Add to User Stories if boss is critical to progression
   - Add to Requirements section

6. **specs/chrono-dawn-mod/data-model.md**
   - Add boss entity definition with complete specifications

7. **specs/chrono-dawn-mod/tasks.md**
   - Add implementation tasks for the boss

### Template

```markdown
### Boss Name (Category)

**Location**: Structure Name

**Stats**:
- Health: XXX HP
- Attack: XX damage
- Defense: XX armor points

**Abilities**:
- Ability 1: Description
- Ability 2: Description

**Strategy**:
- Tip 1
- Tip 2

**Drops**:
- **Item Name**: Description
- Experience points
```

---

## Adding a New Structure

**When to use**: Adding a new structure to the mod

### Files to Update

1. **README.md** (lines ~17-24)
   - Section: "Major Structures" list
   - Add: `- Structure Name (location, description)`

2. **docs/player_guide.md**
   - Section: "Exploring the Chrono Dawn" or appropriate section
   - Add structure description and how to find it

3. **docs/curseforge_description.md** (lines ~22-29)
   - Section: "Epic Structures"
   - Add structure to the list

4. **docs/modrinth_description.md** (lines ~89-97)
   - Section: "Structures"
   - Add structure entry

5. **specs/chrono-dawn-mod/spec.md**
   - Add to User Stories if structure is critical
   - Add to Requirements if needed

6. **specs/chrono-dawn-mod/data-model.md**
   - Add structure definition (generation rules, loot, etc.)

---

## Adding a New Ultimate Artifact

**When to use**: Adding a new ultimate artifact item

### Files to Update

1. **README.md** (line ~32)
   - Section: "Ultimate Artifacts" list
   - Add: `Item Name (type), Description`

2. **docs/player_guide.md**
   - Section: "Ultimate Artifacts"
   - Add full entry with:
     - Stats (damage, armor, durability)
     - Special Ability (detailed description)
     - Recipe (crafting requirements)

3. **docs/curseforge_description.md** (lines ~41-46)
   - Section: "Ultimate Artifacts"
   - Add brief description

4. **docs/modrinth_description.md** (lines ~143-167)
   - Section: "Ultimate Artifacts"
   - Add item entry with ability description

5. **specs/chrono-dawn-mod/data-model.md**
   - Add item definition with complete specifications

### Template

```markdown
### Item Name (Type)

**Stats**:
- Stat 1: Value
- Stat 2: Value

**Special Ability**: **Ability Name**
- Effect description
- Usage notes

**Recipe**:
\`\`\`
- Ingredient 1
- Ingredient 2
- Ingredient 3
\`\`\`
```

---

## Updating Content Counts and Lists

**When to use**: Adding or removing biomes, bosses, structures, wood types, or other countable content

**Purpose**: Ensure numeric descriptions (e.g., "8 unique biomes", "4 mid-bosses", "three wood types") remain accurate across all documentation

### Files to Check

1. **README.md**
   - Check: Biome count, boss count, structure count, wood type count
   - Look for: "8 unique biomes", "Boss Enemies" list length, "Major Structures" list length

2. **docs/player_guide.md**
   - Check: Biome count, boss count (categorized: mini-boss, mid-bosses, final boss), structure count, wood type count
   - Look for: "8 unique biomes", "three wood types", mid-boss descriptions ("4 mid-bosses")

3. **docs/curseforge_description.md**
   - Check: Biome count, boss count, structure count, artifact count
   - Look for: "8 Unique Biomes", boss list lengths, structure list

4. **docs/modrinth_description.md**
   - Check: Biome count, boss count, structure count, wood type count
   - Look for: "8 unique biomes", boss list, structure list

5. **CLAUDE.md**
   - Check: Current versions list if content affects version compatibility
   - Look for: "8 unique biomes" in Recent Changes or Active Technologies

### Verification Method

When adding/removing content:
1. Search for numeric descriptions (e.g., "8", "four", "4 mid-bosses")
2. Verify counts match actual implementation
3. Update Table of Contents if section counts change
4. Check for phrases like "all X", "both", "each of the Y"

**Tip**: Use `grep -r "8 unique biomes" docs/` to find all occurrences quickly

---

## Adding a New Dependency

**When to use**: Adding a new mod dependency (required or optional)

### Files to Update

1. **gradle.properties**
   - Add version property if needed
   - Example: `new_mod_version=1.0.0`

2. **fabric/build.gradle**
   - Add to `dependencies` section
   - Use `modImplementation`, `modApi`, or `modCompileOnly` as appropriate

3. **neoforge/build.gradle**
   - Add to `dependencies` section
   - Use `modImplementation`, `modApi`, or `modCompileOnly` as appropriate

4. **fabric/src/main/resources/fabric.mod.json**
   - Add to `depends` (required) or `recommends` (optional)
   - Specify version range

5. **neoforge/src/main/resources/META-INF/neoforge.mods.toml**
   - Add `[[dependencies.chronodawn]]` entry
   - Set `type` to "required" or "optional"
   - Specify `versionRange`

6. **README.md** (lines ~47-50)
   - Section: "Requirements" → "Dependencies"
   - Add dependency with version and description

7. **docs/player_guide.md** (lines ~41-56)
   - Section: "Required Dependencies"
   - Add numbered entry with links to CurseForge and Modrinth

8. **docs/curseforge_description.md** (lines ~125-128)
   - Section: "Requirements" → "Dependencies"
   - Add dependency to the list

9. **docs/modrinth_description.md** (lines ~30-39)
   - Sections: "Requirements" (both Fabric and NeoForge)
   - Add dependency to both loader sections

10. **THIRD_PARTY_LICENSES.md**
    - Add new dependency entry to "Runtime Dependencies" or "Development Dependencies" section
    - Include: Project name, version, developer/organization, license, URL, license URL
    - Add license summary if it's a new license type
    - Update "Last updated" date at the bottom
    - Research license information from project's GitHub repository or official page

### Dependency Type Guidelines

- **Required (`depends` / `required`)**: Mod cannot function without it
- **Optional (`recommends` / `optional`)**: Adds features but not essential
- **Include in JAR**: Use `include` in Fabric for bundling

---

## Pre-Release Verification

**When to use**: Before creating a release or publishing to CurseForge/Modrinth

### Checklist

- [ ] **Version Consistency**
  - All documentation files show consistent version numbers
  - gradle.properties matches documentation
  - fabric.mod.json and neoforge.mods.toml dependencies match gradle files

- [ ] **Documentation Accuracy**
  - README.md is accurate and up-to-date
  - player_guide.md is complete with all features
  - developer_guide.md reflects current architecture
  - curseforge_description.md ready for publication
  - modrinth_description.md ready for publication

- [ ] **Configuration Files**
  - fabric.mod.json has correct dependencies
  - neoforge.mods.toml has correct dependencies
  - All dependency versions are tested and working

- [ ] **Build Verification**
  - `./gradlew clean build` succeeds for both loaders
  - JAR files are generated correctly
  - No build warnings or errors

- [ ] **Testing**
  - All unit tests pass (`./gradlew test`)
  - Manual testing completed (see quickstart.md checklist)
  - Both Fabric and NeoForge builds tested in-game

- [ ] **CHANGELOG** (if using)
  - CHANGELOG.md exists and is current
  - All user-facing changes documented

- [ ] **GitHub Repository**
  - All changes committed and pushed
  - Branch is up-to-date with main/develop
  - Tags are ready for release version

---

## Quick Reference

### Documentation Files by Purpose

**User-Facing**:
- `README.md` - Project overview, installation, build instructions
- `docs/player_guide.md` - Complete gameplay guide
- `docs/curseforge_description.md` - CurseForge mod page content
- `docs/modrinth_description.md` - Modrinth mod page content

**Legal**:
- `LICENSE` - Project license (MIT)
- `THIRD_PARTY_LICENSES.md` - Dependency licenses and version information

**Developer**:
- `docs/developer_guide.md` - Development setup and architecture
- `specs/chrono-dawn-mod/spec.md` - Feature specification
- `specs/chrono-dawn-mod/data-model.md` - Data models
- `specs/chrono-dawn-mod/tasks.md` - Implementation tasks

**Configuration**:
- `gradle.properties` - Version definitions
- `fabric/src/main/resources/fabric.mod.json` - Fabric metadata
- `neoforge/src/main/resources/META-INF/neoforge.mods.toml` - NeoForge metadata

### Common Line Number References

- README.md Dependencies: ~47-50
- player_guide.md Prerequisites: ~25-56
- developer_guide.md Technologies: ~32-45
- curseforge_description.md Requirements: ~125-128
- modrinth_description.md Requirements: ~30-39
- README.md Boss List: ~25-31
- README.md Structure List: ~17-24

---

## Tips

1. **Always update in pairs**: When updating Fabric configs, update NeoForge configs too
2. **Test both loaders**: Changes to dependencies affect both Fabric and NeoForge differently
3. **Use search**: Use `grep` or IDE search to find all occurrences of version numbers
4. **Keep CLAUDE.md current**: Update the current versions list after major updates
5. **Commit frequently**: Commit documentation changes separately from code changes

---

**Last Updated**: 2025-12-08 (Added THIRD_PARTY_LICENSES.md to maintenance checklists)
**Maintained by**: Chrono Dawn Development Team
