---
name: multiversion-support
description: Guide for multi-version development and version-specific API differences
---

# Multi-Version Support

**Purpose**: Guide for multi-version Minecraft mod development supporting 1.20.1 + 1.21.1 in a single codebase.

**How it works**: This skill is automatically activated when you mention tasks related to:
- Building for specific Minecraft versions
- Running the client for version testing
- Handling version-specific API differences
- Managing version-specific data packs
- Troubleshooting multi-version compatibility issues

Simply describe what you want to do, and Claude will reference the appropriate guidance from this skill.

---

## Overview

**Documentation**: Detailed migration plan is available in `docs/multiversion_migration_plan.md`.

**Supported Versions**: Minecraft 1.20.1 + 1.21.1 (single codebase)

**Strategy**:
- Custom Gradle scripts + abstraction layer approach (no external preprocessor dependencies)
- All code consolidated in one place (prioritizing AI development efficiency, avoiding Git branch separation)
- **Status**: ✅ Phase 1-6 completed (integration testing complete, 2026-01-11)

---

## Key Components

### 1. Data Pack Version Switching

Version-specific directories (`resources-1.20.1/`, `resources-1.21.1/`) switched via Gradle:

**1.20.1**:
- Plural folders: `advancements/`, `loot_tables/`, `recipes/`
- pack_format: 18

**1.21.1**:
- Singular folders: `advancement/`, `loot_table/`, `recipe/`
- pack_format: 48

### 2. Java Code Compatibility Layer

`compat/` package absorbs API differences:

**ItemStack**:
- 1.20.1: NBT-based data storage
- 1.21.1: DataComponents system

**SavedData**:
- 1.20.1: No `HolderLookup.Provider` parameter
- 1.21.1: Requires `HolderLookup.Provider` parameter

**ArmorMaterial**:
- 1.20.1: Interface implementation
- 1.21.1: Record class

**Tier**:
- 1.20.1: `getLevel()` method available
- 1.21.1: `getLevel()` method removed

---

## Build Commands

### Build for Specific Versions

```bash
# Build for Minecraft 1.20.1
./gradlew build1_20_1

# Build for Minecraft 1.21.1 (default)
./gradlew build1_21_1

# Build all versions sequentially
./gradlew buildAll

# Explicit version build
./gradlew build -Ptarget_mc_version=1.20.1
```

---

## Run Client Commands

Auto-generated from `gradle/subproject-run-tasks.gradle`:

### Fabric

```bash
# Run Fabric client for 1.20.1
./gradlew fabric:runClient1_20_1

# Run Fabric client for 1.21.1
./gradlew fabric:runClient1_21_1
```

### NeoForge/Forge

```bash
# Run NeoForge/Forge client for 1.20.1
./gradlew neoforge:runClient1_20_1

# Run NeoForge client for 1.21.1
./gradlew neoforge:runClient1_21_1
```

### Alternative Method (Explicit Version)

```bash
# Fabric with explicit version
./gradlew :fabric:runClient -Ptarget_mc_version=1.20.1

# NeoForge with explicit version
./gradlew :neoforge:runClient -Ptarget_mc_version=1.21.1
```

### Adding New Versions

Edit `supportedVersions` list in `gradle/subproject-run-tasks.gradle`

---

## Output JARs

**Naming Convention**:
- Fabric: `chronodawn-{version}+{mc_version}-fabric.jar`
- NeoForge: `chronodawn-{version}+{mc_version}-neoforge.jar`
- Example: `chronodawn-0.3.0-beta+1.21.1-fabric.jar`

**Important Note**:
- 1.20.1 is Fabric-only (NeoForge only supports 1.20.5+)

---

## Development Guidelines

### When Writing Version-Specific Code

1. **Check API Compatibility**: Always verify if the API exists in both versions
2. **Use Compat Layer**: Add version-specific logic to `compat/` package
3. **Avoid Direct Version Checks**: Use abstraction instead of `if (version == "1.20.1")`
4. **Test Both Versions**: Run `./gradlew buildAll` before committing

### Common Pitfalls

1. **Hardcoding Data Pack Paths**: Use Gradle-switched directories
2. **Assuming API Availability**: Check Minecraft version before using new APIs
3. **Forgetting Compat Implementations**: Always implement both version variants
4. **Not Testing Both Versions**: Always test both 1.20.1 and 1.21.1 builds

---

## Troubleshooting

### Build Fails for Specific Version

**Symptom**: Build succeeds for one version but fails for another

**Common Causes**:
1. Using API that doesn't exist in older version
2. Missing compat layer implementation
3. Incorrect data pack structure for version

**Solution**: Check error message for missing class/method, add compat layer

### Wrong Data Pack Format

**Symptom**: Resources not loading in-game

**Checklist**:
1. Verify `pack_format` matches Minecraft version (18 for 1.20.1, 48 for 1.21.1)
2. Check folder names (plural vs singular)
3. Confirm Gradle switched correct resource directory

### Compat Layer Not Working

**Symptom**: Version-specific code fails at runtime

**Solution**:
1. Verify compat interface is properly implemented for both versions
2. Check factory method returns correct implementation
3. Confirm build includes correct compat classes

---

**Last Updated**: 2026-01-16
**Maintained by**: Chrono Dawn Development Team
