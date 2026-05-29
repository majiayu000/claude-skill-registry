---
name: versioning
description: Versioning strategy and Semantic Versioning guide
---

# Versioning Guide

**Purpose**: Document versioning strategy and provide guidance for version updates in Chrono Dawn mod.

**When to use**: When updating mod version, preparing for release, or understanding version numbering.

---

## Semantic Versioning Overview

Chrono Dawn follows **Semantic Versioning 2.0.0** (https://semver.org/).

### Version Format

```
<major>.<minor>.<patch>-<prerelease>+<buildmetadata>
```

**Examples**:
- `0.2.0-beta+1.21.1-fabric` - Beta version for Minecraft 1.21.1 (Fabric)
- `1.0.0+1.21.1-neoforge` - Stable release for Minecraft 1.21.1 (NeoForge)
- `1.2.3-rc.1+1.21.2-fabric` - Release Candidate 1 for Minecraft 1.21.2 (Fabric)

### Components

1. **Version Number** (`major.minor.patch`):
   - `major`: Incompatible API changes (e.g., 0.x.x → 1.0.0)
   - `minor`: New features, backward-compatible (e.g., 1.0.0 → 1.1.0)
   - `patch`: Bug fixes, backward-compatible (e.g., 1.1.0 → 1.1.1)

2. **Prerelease Identifier** (optional, `-<identifier>`):
   - Separated by hyphen `-`
   - Examples: `-alpha`, `-beta`, `-rc.1`
   - Indicates unstable/pre-release version
   - Removed for stable releases

3. **Build Metadata** (`+<minecraft-version>-<loader>`):
   - Separated by plus `+`
   - Format: `+<minecraft_version>-<fabric|neoforge>`
   - Example: `+1.21.1-fabric`
   - Automatically appended by build system

---

## Chrono Dawn Versioning Strategy

### Development vs. Release Versions

**Development** (during feature implementation):
```
mod_version=0.2.0-beta
```
Builds to: `chronodawn-0.2.0-beta+1.21.1-fabric.jar`

**Release** (when publishing):
```
mod_version=0.2.0
```
Builds to: `chronodawn-0.2.0+1.21.1-fabric.jar`

### Prerelease Identifiers

Use appropriate identifiers based on development stage:

- **`-alpha`**: Early development, major features incomplete
  - Example: `0.2.0-alpha`
  - Use case: Initial implementation of new dimension

- **`-beta`**: Feature-complete, testing in progress
  - Example: `0.2.0-beta`
  - Use case: All bosses implemented, playtesting phase

- **`-rc.1`, `-rc.2`, etc.**: Release Candidate
  - Example: `1.0.0-rc.1`
  - Use case: Final testing before stable release, no new features

- **No identifier**: Stable release
  - Example: `1.0.0`
  - Use case: Production-ready, fully tested

### Version Increment Guide

| Change Type | Example | When to Use |
|------------|---------|-------------|
| `0.1.0` → `0.2.0` | New major features (new dimension area, new boss system) |
| `0.2.0` → `0.2.1` | Bug fixes only |
| `0.9.0` → `1.0.0` | First stable release |
| `1.0.0` → `2.0.0` | Breaking changes (incompatible with old saves) |

---

## Build System Integration

### gradle.properties

Define **only** the version number and prerelease identifier:

```properties
mod_version=0.2.0-beta
```

**Do NOT include** Minecraft version or loader name here.

### Build Scripts

**fabric/build.gradle** (line 86):
```groovy
archiveVersion = "${rootProject.mod_version}+${rootProject.minecraft_version}-fabric"
```

**neoforge/build.gradle** (line 98):
```groovy
archiveVersion = "${rootProject.mod_version}+${rootProject.minecraft_version}-neoforge"
```

These scripts **automatically append** `+1.21.1-fabric` or `+1.21.1-neoforge`.

### Resulting JAR Names

From `mod_version=0.2.0-beta`:
- Fabric: `chronodawn-0.2.0-beta+1.21.1-fabric.jar`
- NeoForge: `chronodawn-0.2.0-beta+1.21.1-neoforge.jar`
- Common: `common-0.2.0-beta.jar`

---

## Version Update Procedure

### Files to Update

When changing `mod_version` in `gradle.properties`, also update:

1. **gradle.properties** (line 6)
   ```properties
   mod_version=X.Y.Z-prerelease
   ```

2. **README.md** (lines 81-83, 209, 220)
   - Build output file names
   - Installation instructions

3. **docs/player_guide.md** (lines 78-79)
   - Download file names

4. **docs/developer_guide.md** (lines 235, 274-276)
   - gradle.properties example
   - Build output file names

5. **fabric.mod.json** and **neoforge.mods.toml**
   - Use `${version}` placeholder (no manual update needed)

### Version Update Checklist

- [ ] Update `gradle.properties` with new version
- [ ] Update all documentation with correct JAR names (include `+1.21.1`)
- [ ] Verify version format follows Semantic Versioning
- [ ] For release: Remove prerelease identifier (e.g., `-beta`)
- [ ] Test build: `./gradlew clean build`
- [ ] Verify JAR names match documentation

---

## Common Patterns

### Preparing Next Version (Development)

```bash
# Start development on 0.3.0
mod_version=0.3.0-alpha
```

### Pre-Release Testing

```bash
# Feature-complete, ready for testing
mod_version=0.3.0-beta
```

### Release Candidate

```bash
# Final testing before release
mod_version=0.3.0-rc.1
```

### Stable Release

```bash
# Production release
mod_version=0.3.0
```

### Hotfix Release

```bash
# Critical bug fix for 0.3.0
mod_version=0.3.1
```

---

## Examples by Scenario

### Scenario 1: Starting Development on 0.2.0
```
Current: 0.1.0 (stable)
Change to: 0.2.0-alpha
Reason: Beginning work on new features
```

### Scenario 2: Entering Beta Phase
```
Current: 0.2.0-alpha
Change to: 0.2.0-beta
Reason: All features implemented, testing phase
```

### Scenario 3: Preparing Release
```
Current: 0.2.0-beta
Change to: 0.2.0-rc.1
Reason: Final testing before release
```

### Scenario 4: Stable Release
```
Current: 0.2.0-rc.1
Change to: 0.2.0
Reason: Release candidate passed testing
```

### Scenario 5: Bug Fix Release
```
Current: 0.2.0 (stable)
Change to: 0.2.1
Reason: Critical bug found, needs hotfix
```

---

## Automated Version Update

Use the `update-version` command to automate version updates:

```bash
/update-version 0.3.0-beta
```

This will:
1. Update `gradle.properties`
2. Update all documentation files with correct JAR names
3. Verify version format

---

## Reference

- **Semantic Versioning Spec**: https://semver.org/
- **Current Version**: Check `gradle.properties` line 6
- **Version History**: See git tags and CHANGELOG.md (if exists)

---

**Last Updated**: 2026-01-01
**Maintained by**: Chrono Dawn Development Team
