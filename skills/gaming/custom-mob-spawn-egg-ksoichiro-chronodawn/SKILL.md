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

Content (identical for all versions):
```json
{
  "parent": "item/template_spawn_egg"
}
```

No custom texture file is needed - Minecraft generates the spawn egg texture procedurally from the two color values.

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

---

## Why NeoForge Needs Explicit Color Registration

Minecraft spawn eggs use `tintIndex` (0 = background, 1 = spots) to colorize the template texture at runtime. Fabric integrates with vanilla's `ColorProviderRegistry` automatically through `DeferredSpawnEggItem`, but NeoForge uses its own event system (`RegisterColorHandlersEvent.Item`) which requires manual registration. The alpha channel (`0xFF000000 |`) must also be added explicitly on NeoForge.
