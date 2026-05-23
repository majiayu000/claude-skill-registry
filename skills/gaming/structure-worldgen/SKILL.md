---
name: structure-worldgen
description: Comprehensive guidance for implementing complex structure generation in Minecraft mods
---

# Structure Worldgen Guide

**Purpose**: Guide for implementing complex structure generation with waterlogging prevention, Jigsaw techniques, and boss spawning.

**How it works**: This skill is automatically activated when you mention tasks related to:
- Creating underground or multi-chunk structures
- Implementing waterlogging prevention systems
- Using Jigsaw structures with programmatic boss room placement
- Configuring terrain adaptation for structures
- Implementing boss spawning systems

Simply describe what you want to do, and Claude will reference the appropriate guidance from this skill.

---

## Underground Structure Waterlogging (2025-11-11)

**Problem**: In Minecraft 1.18+, underground structures face waterlogging issues due to the Aquifer system:
- Aquifers generate water sources throughout underground areas
- When structures generate where water exists, waterloggable blocks (stairs, lanterns, slabs, fences, etc.) automatically become `waterlogged=true`
- Water flows out from these blocks inside the structure

**Standard Solution**: **Avoid waterloggable blocks in underground structures**
- Use full blocks instead of stairs for elevation changes
- Use torches, glowstone, or sea lanterns instead of hanging lanterns
- Avoid slabs, fences, and other non-full blocks in deep underground structures

**Alternative Approaches** (less reliable):
- Processor to remove water (`remove_water.json`) - only removes water blocks, not waterlogged state
- Generate at shallower depths (Y > 40) - reduces aquifer exposure
- 2-block thick walls - does NOT solve waterlogging issue

**Vanilla Examples**:
- Ancient City: Uses waterloggable blocks but generates at Y < -30 (below most aquifers)
- Mineshaft: Allows water flooding (intentional design)
- Stronghold: Generates at Y 40-60 (minimal aquifer exposure)

**Best Practice**: For structures with significant underground portions (Y < 40), use only full blocks for decoration and avoid waterloggable blocks entirely.

**Reference**: See `specs/chrono-dawn-mod/research.md` → "Structure Waterlogging Research" for detailed analysis

---

## Advanced Solution: Complete Waterlogging Prevention System (2025-11-24)

**Use Case**: When you need to:
1. Use waterloggable blocks in underground structures (stairs, lanterns, slabs, etc.)
2. Include decorative water features (waterfalls, pools) in the same structures
3. Support intentional waterlogging (waterlogged slabs for decorative pools)

**Problem**: Simple Mixin-based water removal cannot distinguish between:
- Aquifer water (unwanted) vs Decorative water (wanted)
- Aquifer-induced waterlogging (unwanted) vs Intentional waterlogging (wanted)

**Complete Solution: Three-Component System**

### 1. Custom Decorative Water Fluid

**Files**: `DecorativeWaterFluid.java`, `ModFluids.java`

**Purpose**:
- Create `chronodawn:decorative_water` fluid that looks identical to vanilla water
- Use in NBT structures for decorative water features (waterfalls, pools)
- Distinguishable from Aquifer water (`minecraft:water`) during generation
- Preserves flow state (level=0-15) for waterfalls

### 2. Structure Processor

**File**: `CopyFluidLevelProcessor.java`

```java
@Override
public StructureBlockInfo processBlock(...) {
    // Phase 1: During structure placement (per-block processing)

    // A. Convert decorative water → vanilla water (preserve flow)
    if (state.is(ModBlocks.DECORATIVE_WATER.get())) {
        int level = state.getValue(BlockStateProperties.LEVEL);
        return new StructureBlockInfo(pos, Blocks.WATER.defaultBlockState()
            .setValue(BlockStateProperties.LEVEL, level), nbt);
    }

    // B. Record intentional waterlogging positions
    BlockPos worldPos = currentBlockInfo.pos();  // IMPORTANT: use currentBlockInfo.pos()!
    if (originalBlockInfo.state().getValue(WATERLOGGED) == true) {
        INTENTIONAL_WATERLOGGING.add(worldPos.immutable());
    }

    // C. Remove ALL waterlogging temporarily (prevents water spread)
    if (currentBlockInfo.state().getValue(WATERLOGGED) == true) {
        return new StructureBlockInfo(pos, state.setValue(WATERLOGGED, false), nbt);
    }
}
```

### 3. Mixin

**File**: `StructureStartMixin.java`

```java
@Inject(method = "placeInChunk", at = @At("HEAD"))
private void removeWaterBeforePlacement(...) {
    // Phase 2a: Before structure placement
    // Remove ONLY minecraft:water (Aquifer), preserve chronodawn:decorative_water
    for (BlockPos pos : structurePieceBoundingBox) {
        if (state.is(Blocks.WATER) && !state.is(ModBlocks.DECORATIVE_WATER)) {
            level.setBlock(pos, Blocks.AIR.defaultBlockState(), 2);
        }
    }
}

@Inject(method = "placeInChunk", at = @At("RETURN"))
private void finalizeWaterlogging(...) {
    // Phase 2b: After structure placement
    // Process current chunk + 1-block border (fixes multi-chunk timing issues)
    for (BlockPos pos : chunkBox.expanded(1, 0, 1)) {
        BlockPos immutablePos = pos.immutable();

        if (state.hasProperty(WATERLOGGED)) {
            boolean shouldBeWaterlogged = INTENTIONAL_WATERLOGGING.contains(immutablePos);

            // Restore intentional, remove unintentional
            if (state.getValue(WATERLOGGED) != shouldBeWaterlogged) {
                level.setBlock(pos, state.setValue(WATERLOGGED, shouldBeWaterlogged), 2);
            }

            // Cleanup: remove from set after processing
            if (shouldBeWaterlogged) {
                INTENTIONAL_WATERLOGGING.remove(immutablePos);
            }
        }
    }
}
```

### Processing Flow

```
1. Mixin HEAD: Remove Aquifer water (minecraft:water only)
2. Structure Placement:
   - NBT blocks placed
   - Processor runs for each block:
     * Records intentional waterlogging positions
     * Removes all waterlogging (prevents spread during placement)
     * Converts decorative_water → minecraft:water
3. Mixin RETURN:
   - Restores intentional waterlogging (from recorded positions)
   - Removes unintentional waterlogging (Aquifer or water spread)
   - Processes chunk + 1-block border (fixes multi-chunk structures)
```

### Critical Implementation Details

1. **Correct World Position** (Most Common Bug):
   ```java
   // WRONG: blockPos parameter is structure origin (same for all blocks!)
   BlockPos worldPos = blockPos;

   // CORRECT: Get actual position from currentBlockInfo
   BlockPos worldPos = currentBlockInfo.pos();
   ```

2. **Immutable BlockPos for Set Storage**:
   ```java
   INTENTIONAL_WATERLOGGING.add(worldPos.immutable());  // Store immutable
   INTENTIONAL_WATERLOGGING.contains(pos.immutable());   // Check immutable
   ```

3. **Multi-Chunk Structures** (Timing Issue):
   - Each chunk processes separately via `placeInChunk()`
   - Later chunks can waterlog blocks in earlier (already processed) chunks
   - Solution: Expand processing area by 1 block: `chunkBox.expanded(1, 0, 1)`
   - Don't clear `INTENTIONAL_WATERLOGGING` set until all chunks processed

4. **Set Cleanup**:
   ```java
   // WRONG: Clear entire set after each chunk
   INTENTIONAL_WATERLOGGING.clear();

   // CORRECT: Remove individual positions after restoration
   if (shouldBeWaterlogged) {
       INTENTIONAL_WATERLOGGING.remove(immutablePos);
   }
   ```

### Capabilities

- ✅ Prevents Aquifer water from waterlogging stairs, lanterns, slabs, etc.
- ✅ Supports decorative water features (waterfalls with flow)
- ✅ Supports intentional waterlogging (waterlogged slabs for pools)
- ✅ Works with multi-chunk structures
- ✅ Compatible with Jigsaw structures

### Files

- `DecorativeWaterFluid.java` - Custom fluid (Source + Flowing)
- `ModFluids.java` - Fluid registration
- `CopyFluidLevelProcessor.java` - Structure processor
- `ModStructureProcessorTypes.java` - Processor type registration
- `StructureStartMixin.java` - Mixin for water removal and waterlogging finalization
- `convert_decorative_water.json` - Processor list (applied to template pools)

**Reference**: Master Clock (T234-238) - uses stairs, decorative water, intentional waterlogging

---

## Structure Generation Priority (2025-11-11)

**Generation Order**: Structures generate in phases determined by the `step` parameter:
1. `raw_generation` - Immediately after terrain generation
2. `lakes` - Lake generation
3. `local_modifications` - Local terrain modifications
4. `underground_structures` - Underground structures (early)
5. `surface_structures` - Surface structures (late)
6. `strongholds` - Strongholds
7. `underground_ores` - Ore generation
8. ... (vegetation, decoration, etc.)

**Priority Rule**: Earlier steps have priority over later steps. Later structures avoid overwriting earlier structures.

**Use Case**: For unique/important structures (like Master Clock), use `underground_structures` step even if they have surface components. This prevents common structures (using `surface_structures`) from overwriting them.

**Limitation**: Structures in different `structure_set` definitions have weak collision detection. Overlaps can still occur but are less likely when using earlier generation steps.

---

## Advanced Jigsaw Structure Techniques (2025-11-27)

**Use Case**: When you need to combine Jigsaw system (random generation) with programmatic placement (guaranteed single boss room).

**Example**: Phantom Catacombs - Jigsaw maze with exactly one boss room connected to a random dead-end

### Problem: Jigsaw Limitations for Boss Rooms

Jigsaw system cannot guarantee:
1. Exactly one boss room (might generate 0 or multiple)
2. Boss room connects to maze in specific way
3. Boss room avoids collision with existing maze rooms

### Solution: Hybrid Jigsaw + Programmatic Approach

**Architecture**:
1. **Jigsaw Phase**: Generate maze structure (entrance → corridors → rooms → dead-ends)
2. **Marker Phase**: Place markers (Crying Obsidian) in dead-end rooms during Jigsaw generation
3. **Programmatic Phase**: Replace one marker with boss room using custom placer logic
4. **Cleanup Phase**: Remove remaining markers

**Implementation Pattern** (Phantom Catacombs example):

```java
// 1. Jigsaw generates maze with dead-end markers
// dead_end.nbt contains Crying Obsidian marker at specific position

// 2. PhantomCatacombsBossRoomPlacer periodic check (every 30 seconds)
public static void checkAndPlaceRooms(ServerLevel level) {
    // Find dead-end markers in structure bounding box
    List<BlockPos> deadEndMarkers = findDeadEndMarkers(level, structureOrigin, boundingBox);

    // Require minimum markers (ensures maze generated sufficiently)
    if (deadEndMarkers.size() < 3) return;

    // Evaluate all placements (dead_ends × rotations)
    List<PlacementCandidate> candidates = evaluateAllPlacements(level, deadEndMarkers, ...);

    // 3-stage fallback:
    // Phase 1: Collision-free placement (0 room collisions)
    // Phase 2: Minimal collision (1 room collision, acceptable)
    // Phase 3: Independent placement (hidden chamber, no maze connection)

    PlacementCandidate selected = selectBestCandidate(candidates);

    // Place room_7 (transition) + boss_room
    placeRoom7(level, selected.deadEndPos, selected.rotation);
    placeBossRoom(level, room7ConnectorPos);

    // Remove all remaining dead-end markers
    cleanupMarkers(level, deadEndMarkers);
}
```

### Marker Strategy

**Dead-End Marker** (Crying Obsidian):
- Placed in dead-end room NBT at specific position
- Indicates potential boss room connection point
- Removed after boss room placement (or if not selected)

**Connector Marker** (Amethyst Block):
- Placed in room_7 NBT (exit to boss room)
- Placed in boss_room NBT (entrance from room_7)
- Used for Jigsaw-like connection alignment (both markers align to same world position)

**Why Two Markers**:
- Crying Obsidian: Replacement target (dead-end → room_7)
- Amethyst Block: Connection point (room_7 ↔ boss_room)

### Rotation Handling

**Challenge**: Structures can rotate (NONE, 90°, 180°, 270°), affecting:
- Marker positions
- Entrance/exit directions
- Boss spawn center position

**Solution Pattern**:

```java
// 1. Detect entrance direction from existing blocks (air = corridor)
Direction entranceDir = detectEntranceDirection(level, markerPos);
Rotation rotation = getRotationFromDirection(entranceDir);

// 2. Calculate rotated marker positions
StructurePlaceSettings settings = new StructurePlaceSettings().setRotation(rotation);
BlockPos rotatedMarker = StructureTemplate.calculateRelativePosition(settings, templateMarker);

// 3. Align markers: worldPos = placementPos + rotatedMarker
BlockPos placementPos = worldMarkerPos.subtract(rotatedMarker);

// 4. Calculate exit direction from rotation
Direction exitDir = getExitDirectionFromRotation(rotation);

// 5. Calculate boss room center from connector (rotation-aware)
BlockPos centerOffset = switch (exitDir) {
    case EAST -> new BlockPos(10, 4, 0);   // Room extends east
    case WEST -> new BlockPos(-10, 4, 0);  // Room extends west
    case NORTH -> new BlockPos(0, 4, -10); // Room extends north
    case SOUTH -> new BlockPos(0, 4, 10);  // Room extends south
};
BlockPos bossRoomCenter = connectorPos.offset(centerOffset);
```

**Critical**: Always use rotation-aware calculations, never assume NONE rotation.

### Collision Detection for Boss Room Placement

**Problem**: Boss room might overlap with existing maze rooms.

**Solution**: Evaluate all candidates and select best option.

```java
// 1. Generate candidates: all dead_ends × valid rotations
for (BlockPos deadEnd : deadEndMarkers) {
    Direction mazeEntranceDir = detectEntranceDirection(level, deadEnd);

    for (Rotation rotation : Rotation.values()) {
        Direction bossRoomDir = getExitDirectionFromRotation(rotation);

        // Skip if boss room would block maze entrance
        if (bossRoomDir == mazeEntranceDir) continue;

        // Calculate placement positions
        BlockPos bossRoomPlacementPos = calculatePlacementPos(...);
        BoundingBox bossRoomBox = calculateBoundingBox(...);

        // Count colliding maze rooms
        int collidingRooms = countCollidingRooms(level, bossRoomBox);

        candidates.add(new PlacementCandidate(deadEnd, rotation, collidingRooms));
    }
}

// 2. Select best candidate
// Phase 1: Prefer collision-free (0 collisions)
List<PlacementCandidate> collisionFree = candidates.stream()
    .filter(c -> c.collidingRoomCount == 0)
    .toList();

if (!collisionFree.isEmpty()) {
    return collisionFree.get(random.nextInt(collisionFree.size()));
}

// Phase 2: Accept minimal collision (1 collision)
List<PlacementCandidate> minimalCollision = candidates.stream()
    .filter(c -> c.collidingRoomCount == 1)
    .toList();

if (!minimalCollision.isEmpty()) {
    return minimalCollision.get(random.nextInt(minimalCollision.size()));
}

// Phase 3: Independent placement (hidden chamber)
return placeBossRoomIndependently(level, structureOrigin);
```

**Room Collision Detection**:
```java
private static int countCollidingRooms(ServerLevel level, BoundingBox bossRoomBox) {
    Set<BlockPos> collidingRooms = new HashSet<>();

    for (BlockPos pos : BlockPos.betweenClosed(box.minX(), box.minY(), box.minZ(),
                                                box.maxX(), box.maxY(), box.maxZ())) {
        BlockState state = level.getBlockState(pos);

        // Check for maze structure blocks
        if (state.is(Blocks.DEEPSLATE_BRICKS) || state.is(Blocks.CHEST) || ...) {
            // Estimate room origin (rooms are 7x7, align to grid)
            BlockPos roomOrigin = new BlockPos(
                Math.floorDiv(pos.getX(), 7) * 7,
                pos.getY(),
                Math.floorDiv(pos.getZ(), 7) * 7
            );
            collidingRooms.add(roomOrigin);
        }
    }

    return collidingRooms.size();
}
```

### Terrain Adaptation for Underground + Surface Structures

**Problem**: Structures with both underground (maze) and surface (entrance) components can cause terrain deletion.

**Symptom**: Surface terrain (hills, mountains) flattened above underground portions when using `terrain_adaptation: "beard_thin"`.

**Solution**:
```json
{
  "terrain_adaptation": "none",              // Disable terrain deletion
  "start_height": {"absolute": 0},           // Y=0 start
  "project_start_to_heightmap": "WORLD_SURFACE_WG"  // Entrance projects to surface
}
```

**Effect**:
- Surface terrain preserved (no flattening)
- Entrance still accessible from surface
- Minimal visual disruption

**Alternative Options** (if terrain integration needed):
- `"terrain_adaptation": "bury"` - Minimal terrain modification
- `"terrain_adaptation": "encapsulate"` - Structure enclosed in terrain

### Boss Spawning System

**Pattern**: Proximity-based spawning when player enters boss room.

```java
public class BossSpawner {
    // Track boss_room positions (per dimension)
    private static final Map<ResourceLocation, Set<BlockPos>> bossRoomPositions = new HashMap<>();

    // Track spawned boss_rooms (prevent duplicates)
    private static final Map<ResourceLocation, Set<BlockPos>> spawnedBossRooms = new HashMap<>();

    // Boss room placer registers positions after placement
    public static void registerBossRoom(ServerLevel level, BlockPos bossRoomCenter) {
        ResourceLocation dimensionId = level.dimension().location();
        bossRoomPositions.putIfAbsent(dimensionId, new HashSet<>());
        bossRoomPositions.get(dimensionId).add(bossRoomCenter.immutable());
    }

    // Server tick event: check player proximity (every 1 second)
    public static void checkAndSpawnBoss(ServerLevel level) {
        // Check every 20 ticks (1 second)
        if (tickCounter++ < 20) return;
        tickCounter = 0;

        for (BlockPos bossRoomCenter : bossRoomPositions.get(dimensionId)) {
            if (spawnedBossRooms.contains(bossRoomCenter)) continue;

            // Check player proximity (AABB bounds)
            AABB bossRoomBounds = new AABB(bossRoomCenter).inflate(12, 6, 12);

            for (ServerPlayer player : level.players()) {
                if (bossRoomBounds.contains(player.position())) {
                    spawnBoss(level, bossRoomCenter);
                    spawnedBossRooms.add(bossRoomCenter);
                    break;
                }
            }
        }
    }
}
```

**Center Position Calculation** (rotation-aware):
```java
// From connector position (entrance Amethyst Block)
BlockPos centerOffset = switch (exitDir) {
    case EAST -> new BlockPos(10, 4, 0);   // Room extends 10 blocks east, 4 blocks up
    case WEST -> new BlockPos(-10, 4, 0);
    case NORTH -> new BlockPos(0, 4, -10);
    case SOUTH -> new BlockPos(0, 4, 10);
};
BlockPos bossRoomCenter = connectorPos.offset(centerOffset);
```

### Integration with Waterlogging Prevention

When combining programmatic placement with waterlogging prevention:

1. **Boss Room Placement**: Apply `convert_decorative_water` processor list
   ```java
   StructurePlaceSettings settings = new StructurePlaceSettings()
       .setRotation(rotation);

   // Load processor list from registry
   var processorList = level.registryAccess()
       .registryOrThrow(Registries.PROCESSOR_LIST)
       .get(ResourceLocation.fromNamespaceAndPath(MOD_ID, "convert_decorative_water"));

   if (processorList != null) {
       for (var processor : processorList.list()) {
           settings.addProcessor(processor);
       }
   }

   template.placeInWorld(level, placementPos, placementPos, settings, random, 2);
   ```

2. **Mixin Coordination**: StructureStartMixin processes both Jigsaw pieces and programmatic placements
   - HEAD injection: Remove Aquifer water before all placements
   - RETURN injection: Finalize waterlogging after all placements

**Reference**: Phantom Catacombs (T236m-r) - complete implementation example

---

**Last Updated**: 2025-12-08
**Maintained by**: Chrono Dawn Development Team
