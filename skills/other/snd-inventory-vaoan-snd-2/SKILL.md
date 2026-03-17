---
name: SND Inventory Functions
description: Use this skill when working with player inventory, item management, and container operations in SND macros. Covers inventory queries, item counts, container types, and item manipulation.
---

# Inventory Functions for SND

This skill covers inventory management and item operations in SND macros.

> **Source Status:** Unverified - documented from screenshots and testing. These are SND built-in functions.

## Inventory Types

SND provides access to various inventory containers:

```lua
-- Main inventory types (InventoryType enum)
local InventoryType = {
    Inventory1 = 0,
    Inventory2 = 1,
    Inventory3 = 2,
    Inventory4 = 3,
    EquippedItems = 1000,
    Currency = 2000,
    Crystals = 2001,
    -- Retainer inventories
    RetainerPage1 = 10000,
    RetainerPage2 = 10001,
    RetainerPage3 = 10002,
    RetainerPage4 = 10003,
    RetainerPage5 = 10004,
    RetainerPage6 = 10005,
    RetainerPage7 = 10006,
    RetainerEquipped = 10007,
    RetainerGil = 10008,
    RetainerCrystals = 10009,
    RetainerMarket = 10010,
    -- Saddlebag
    SaddleBag1 = 4000,
    SaddleBag2 = 4001,
    PremiumSaddleBag1 = 4100,
    PremiumSaddleBag2 = 4101,
    -- Glamour dresser
    GlamourChest = 20000,
    -- Armoire
    Armoire = 2500,
}
```

## Core Inventory Functions

### Checking Item Counts
```lua
-- Get count of item in all inventories
GetItemCount(number itemId) → number

-- Get count of item in specific inventory type
GetItemCountInContainer(number itemId, number inventoryType) → number

-- Check if player has item
HasItem(number itemId) → boolean

-- Get count including HQ items separately
GetItemCountHQ(number itemId) → number
```

### Inventory Space
```lua
-- Get free inventory slots
GetFreeInventorySlots() → number

-- Check if inventory is full
IsInventoryFull() → boolean
```

### Container Access
```lua
-- Get inventory container
GetInventoryContainer(number inventoryType) → InventoryContainer

-- Container properties
container.Size → number
container[slotIndex] → InventoryItem
```

### Item Properties
```lua
-- InventoryItem properties
item.ItemId → number
item.Quantity → number
item.IsHQ → boolean
item.Spiritbond → number
item.Condition → number
item.Slot → number
item.Container → number
```

## Usage Patterns

### Count Items in Inventory
```lua
function CountItem(itemId)
    local count = GetItemCount(itemId)
    return count or 0
end

-- Example: Count Gil
local gilCount = CountItem(1)  -- Gil item ID is 1
```

### Check for Required Items
```lua
function HasRequiredItems(requirements)
    for itemId, requiredCount in pairs(requirements) do
        local count = GetItemCount(itemId)
        if count < requiredCount then
            return false, itemId
        end
    end
    return true
end

-- Usage
local requirements = {
    [5111] = 10,  -- Earth Shard x10
    [5112] = 10,  -- Ice Shard x10
}
local hasAll, missingId = HasRequiredItems(requirements)
```

### Check Inventory Space
```lua
function EnsureInventorySpace(minSlots)
    local freeSlots = GetFreeInventorySlots()
    if freeSlots < minSlots then
        yield("/echo [Script] Need " .. minSlots .. " free slots, have " .. freeSlots)
        return false
    end
    return true
end
```

### Iterate Through Inventory
```lua
function FindItemSlot(itemId)
    for containerType = 0, 3 do  -- Inventory1-4
        local container = GetInventoryContainer(containerType)
        if container then
            for i = 0, container.Size - 1 do
                local item = container[i]
                if item and item.ItemId == itemId then
                    return containerType, i, item
                end
            end
        end
    end
    return nil
end
```

### Check Equipped Item
```lua
function GetEquippedItem(slot)
    local container = GetInventoryContainer(1000)  -- EquippedItems
    if container then
        return container[slot]
    end
    return nil
end

-- Equipment slots
local EquipSlot = {
    MainHand = 0,
    OffHand = 1,
    Head = 2,
    Body = 3,
    Hands = 4,
    Waist = 5,
    Legs = 6,
    Feet = 7,
    Ears = 8,
    Neck = 9,
    Wrists = 10,
    Ring1 = 11,
    Ring2 = 12,
    SoulCrystal = 13,
}
```

## Item Manipulation

### Use Item
```lua
-- Use item from inventory (food, potions, etc.)
yield("/item <itemname>")

-- Use item on target
yield("/item <itemname> <t>")
```

### Discard Item
```lua
-- Discard requires interacting with the inventory UI
-- Use with caution - this is destructive!
function DiscardItem(itemId)
    -- Implementation depends on addon interaction
    -- See snd-addons skill for UI automation
end
```

## Common Item IDs

```lua
local CommonItems = {
    -- Currency
    Gil = 1,

    -- Crystals (Shards)
    FireShard = 2,
    IceShard = 3,
    WindShard = 4,
    EarthShard = 5,
    LightningShard = 6,
    WaterShard = 7,

    -- Crystals
    FireCrystal = 8,
    IceCrystal = 9,
    WindCrystal = 10,
    EarthCrystal = 11,
    LightningCrystal = 12,
    WaterCrystal = 13,

    -- Clusters
    FireCluster = 14,
    IceCluster = 15,
    WindCluster = 16,
    EarthCluster = 17,
    LightningCluster = 18,
    WaterCluster = 19,

    -- Ventures (for retainers)
    Venture = 21072,
}
```

## Best Practices

1. **Always check item existence** before assuming count is valid
2. **Use container iteration** for complex inventory operations
3. **Check inventory space** before automated gathering/crafting
4. **Cache item counts** if checking repeatedly in a loop
5. **Prefer GetItemCount** over manual iteration for simple counts
