---
name: mixin-guide
description: Guide for configuring Mixins in Architectury multi-loader projects
---

# Mixin Configuration Guide

**Purpose**: Guide for configuring Mixins in Architectury multi-loader projects.

**How it works**: This skill is automatically activated when you mention tasks related to:
- Adding new Mixin classes
- Configuring Mixin files for Fabric or NeoForge
- Debugging Mixin-related errors (InvalidInjectionException, refMap issues)
- Setting up build configuration for Mixins

Simply describe what you want to do, and Claude will reference the appropriate guidance from this skill.

---

## Critical: Loader-Specific Mixin Configurations (2025-12-02)

**Problem**: Fabric and NeoForge require **different** Mixin configurations due to mapping differences.

### Loader-Specific Mixin Files

- **Fabric**: `fabric/src/main/resources/chronodawn-fabric.mixins.json`
  - **Must include** `"refmap": "common-common-refmap.json"`
  - Required for Mojang → Intermediary mapping conversion in production
  - Referenced in `fabric.mod.json`

- **NeoForge**: `neoforge/src/main/resources/chronodawn-neoforge.mixins.json`
  - **Must NOT include** refMap property
  - Uses Mojang mappings directly in development environment
  - Referenced in `META-INF/neoforge.mods.toml`

- **Common**: `common/src/main/resources/chronodawn.mixins.json`
  - No refMap property
  - **Excluded from both JARs** via build.gradle exclude rules
  - Kept for reference only

### Adding New Mixins

When adding new Mixin classes:

1. Create Mixin class in `common/src/main/java/com/chronodawn/mixin/`
2. Update **both** loader-specific configs:
   - Add to `chronodawn-fabric.mixins.json` (with refMap)
   - Add to `chronodawn-neoforge.mixins.json` (without refMap)
3. Do NOT modify `chronodawn.mixins.json` (excluded from builds)

### Build Configuration

**Fabric** (`fabric/build.gradle`):
```groovy
processResources {
    from(project(':common').sourceSets.main.resources) {
        exclude 'chronodawn.mixins.json'  // Exclude common config
    }
}
shadowJar {
    exclude 'chronodawn.mixins.json'  // Also exclude from shadow JAR
}
```

**NeoForge** (`neoforge/build.gradle`):
```groovy
from(project(":common").sourceSets.main.resources) {
    exclude "chronodawn.mixins.json"  // Already configured
}
```

### Why This Separation is Necessary

- **Fabric (Production)**: Runs with Intermediary mappings → needs refMap to translate method names
- **NeoForge (Development)**: Runs with Mojang mappings → refMap causes InvalidInjectionException
- **Root Cause**: Architectury Loom generates refMap using Intermediary mappings, incompatible with NeoForge's Mojang mappings

**Reference**: Commit 77958c0 (fix: separate loader-specific Mixin configs)

---

## Troubleshooting

### InvalidInjectionException in NeoForge

**Symptom**: Mixin injection fails in NeoForge but works in Fabric.

**Cause**: NeoForge Mixin config includes refMap property.

**Solution**: Remove `"refmap"` from `chronodawn-neoforge.mixins.json`.

### Mixin Not Applied

**Symptom**: Mixin class exists but doesn't apply at runtime.

**Checklist**:
1. Verify Mixin class is in `chronodawn-fabric.mixins.json` (for Fabric)
2. Verify Mixin class is in `chronodawn-neoforge.mixins.json` (for NeoForge)
3. Check Mixin config is referenced in `fabric.mod.json` / `neoforge.mods.toml`
4. Verify build excludes `chronodawn.mixins.json` from JARs

### RefMap Missing in Production

**Symptom**: Fabric mod works in dev but crashes in production with refMap errors.

**Cause**: Missing `"refmap": "common-common-refmap.json"` in `chronodawn-fabric.mixins.json`.

**Solution**: Add refMap property to Fabric Mixin config.

---

**Last Updated**: 2025-12-08
**Maintained by**: Chrono Dawn Development Team
