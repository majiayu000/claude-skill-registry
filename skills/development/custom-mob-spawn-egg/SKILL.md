---
name: custom-mob-spawn-egg
description: Use when adding spawn eggs or fixing spawn egg visual bugs (black square, grayscale, invisible).
---

# Custom Mob Spawn Egg Implementation Guide

**Purpose**: Ensure all required steps are completed when adding a spawn egg for a custom mob. Spawn eggs require multiple registration points across Fabric, NeoForge, and multi-version resource files. Missing any step causes visual bugs (grayscale, invisible texture).

---

## Spawn Egg Implementation Checklist

When adding a spawn egg for a new custom mob, **all** of the following steps must be completed:

### 1. Item Registration (ModItems.java)

Register the spawn egg item in `ModItems.java` for each version.

**1.21.2** (requires `.setId()`):
```java
public static final RegistrySupplier<Item> MOB_NAME_SPAWN_EGG = ITEMS.register(
    "mob_name_spawn_egg",
    () -> new com.chronodawn.items.DeferredSpawnEggItem(
        ModEntities.MOB_NAME,
        0xAABBCC, // Background color
        0xDDEEFF, // Spots color
        new Item.Properties()
                .setId(ResourceKey.create(Registries.ITEM,
                    ResourceLocation.fromNamespaceAndPath(ChronoDawn.MOD_ID, "mob_name_spawn_egg")))
    )
);
```

**1.21.1 / 1.20.1** (simpler, no `.setId()`):
```java
public static final RegistrySupplier<Item> MOB_NAME_SPAWN_EGG = ITEMS.register(
    "mob_name_spawn_egg",
    () -> new com.chronodawn.items.DeferredSpawnEggItem(
        ModEntities.MOB_NAME,
        0xAABBCC, // Background color
        0xDDEEFF, // Spots color
        new Item.Properties()
    )
);
```

### 2. Initialize Spawn Egg (ModItems.java)

Add the `initializeSpawnEgg()` call inside the `initializeSpawnEggs()` method:

```java
if (MOB_NAME_SPAWN_EGG.get() instanceof com.chronodawn.items.DeferredSpawnEggItem) {
    ((com.chronodawn.items.DeferredSpawnEggItem) MOB_NAME_SPAWN_EGG.get()).initializeSpawnEgg();
}
```

### 3. Creative Tab Entry (ModItems.java)

Add to the `populateCreativeTab()` method:

```java
if (MOB_NAME_SPAWN_EGG.isPresent()) {
    output.accept(MOB_NAME_SPAWN_EGG.get());
}
```

### 4. Item Model File (CRITICAL)

**Without this file, the spawn egg will be completely invisible in the inventory.**

Create `models/item/mob_name_spawn_egg.json` in all version resource directories:
- `common-1.20.1/src/main/resources/assets/chronodawn/models/item/`
- `common-1.21.1/src/main/resources/assets/chronodawn/models/item/`
- `common-1.21.2/src/main/resources/assets/chronodawn/models/item/`
- `common-1.21.4/src/main/resources/assets/chronodawn/models/item/`

Content (identical for all versions):
```json
{
  "parent": "item/template_spawn_egg"
}
```

No custom texture file is needed - Minecraft generates the spawn egg texture procedurally from the two color values.

### 4a. Item Definition File (1.21.4 ONLY - CRITICAL)

**1.21.4 introduced a new item definition system.** Without this file, spawn egg colors will not display correctly.

Create `items/mob_name_spawn_egg.json` in the 1.21.4 resource directory:
- `common-1.21.4/src/main/resources/assets/chronodawn/items/`

**Note**: This is a separate directory from `models/item/` - both files are required for 1.21.4.

Content:
```json
{
  "model": {
    "type": "minecraft:model",
    "model": "minecraft:item/template_spawn_egg",
    "tints": [
      {
        "type": "minecraft:constant",
        "value": 10194798
      },
      {
        "type": "minecraft:constant",
        "value": 14329120
      }
    ]
  }
}
```

**Color Value Conversion**: The `tints` array uses **decimal** values, not hex:
- First tint (index 0): Background color
- Second tint (index 1): Spots color
- Convert hex to decimal: `0x9B8B6E` → `10194798`, `0xDAA520` → `14329120`
- JavaScript conversion: `parseInt("9B8B6E", 16)` → `10194798`

**IMPORTANT**: Colors must be specified in BOTH:
1. Java code (hex): `0x9B8B6E, 0xDAA520` in ModItems.java
2. JSON file (decimal): `10194798, 14329120` in items/*.json

### 5. NeoForge Color Handler Registration (CRITICAL)

**Without this, the spawn egg will appear grayscale on NeoForge.** Fabric handles this automatically via vanilla mechanisms, but NeoForge requires explicit registration.

File: `neoforge-base/src/main/java/com/chronodawn/neoforge/client/ChronoDawnClientNeoForge.java`

Add `ModItems.MOB_NAME_SPAWN_EGG.get()` to the item list in the `onRegisterItemColors` method:

```java
@SubscribeEvent
public static void onRegisterItemColors(RegisterColorHandlersEvent.Item event) {
    event.register(
        (stack, tintIndex) -> {
            if (stack.getItem() instanceof com.chronodawn.items.DeferredSpawnEggItem egg) {
                int color = egg.getColor(tintIndex);
                return 0xFF000000 | color;
            }
            return 0xFFFFFFFF;
        },
        // ... existing spawn eggs ...
        ModItems.MOB_NAME_SPAWN_EGG.get()  // <-- Add here
    );
}
```

### 6. Language Files

Add entries to both `en_us.json` and `ja_jp.json` for all 3 versions:

```json
"item.chronodawn.mob_name_spawn_egg": "Mob Name Spawn Egg"
```

---

## Common Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| Spawn egg invisible, or black square (dark purple on hover) | Missing item model JSON | Add `models/item/xxx_spawn_egg.json` with `"parent": "item/template_spawn_egg"` |
| Grayscale on NeoForge only | Missing NeoForge color handler | Add to `onRegisterItemColors` in `ChronoDawnClientNeoForge.java` |
| Correct on NeoForge, broken on Fabric | Missing `initializeSpawnEgg()` call | Add to `initializeSpawnEggs()` |
| No name displayed | Missing lang entry | Add to `en_us.json` / `ja_jp.json` |
| Not in creative tab | Missing creative tab entry | Add to `populateCreativeTab()` |
| **Colors wrong on 1.21.4 only** | **Missing items/*.json with tints** | **Add `items/xxx_spawn_egg.json` with tints array (1.21.4 only)** |
| **Colors mismatch between versions** | **Hex/decimal mismatch** | **Ensure Java (hex) and JSON (decimal) colors match** |

---

## Why NeoForge Needs Explicit Color Registration

Minecraft spawn eggs use `tintIndex` (0 = background, 1 = spots) to colorize the template texture at runtime. Fabric integrates with vanilla's `ColorProviderRegistry` automatically through `DeferredSpawnEggItem`, but NeoForge uses its own event system (`RegisterColorHandlersEvent.Item`) which requires manual registration. The alpha channel (`0xFF000000 |`) must also be added explicitly on NeoForge.
