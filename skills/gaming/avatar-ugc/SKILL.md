---
name: avatar-ugc
description: Programmatically apply UGC (User-Generated Content) to characters including clothing, accessories, and avatar customization. Use when dressing NPCs, building avatar editors, or creating character customization systems.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Avatar & UGC Customization

## Quick Reference Links

**Official Documentation:**
- [Character Appearance](https://create.roblox.com/docs/characters/appearance) - Overview of avatar customization
- [HumanoidDescription API](https://create.roblox.com/docs/reference/engine/classes/HumanoidDescription) - Core avatar properties
- [Shirt API](https://create.roblox.com/docs/reference/engine/classes/Shirt) - Classic shirt clothing
- [Pants API](https://create.roblox.com/docs/reference/engine/classes/Pants) - Classic pants clothing
- [ShirtGraphic API](https://create.roblox.com/docs/reference/engine/classes/ShirtGraphic) - T-shirts
- [Accessory API](https://create.roblox.com/docs/reference/engine/classes/Accessory) - Accessories/hats
- [InsertService API](https://create.roblox.com/docs/reference/engine/classes/InsertService) - Loading assets
- [AvatarEditorService API](https://create.roblox.com/docs/reference/engine/classes/AvatarEditorService) - Avatar editor support

**Wiki References:**
- [User-generated content (Wiki)](https://roblox.fandom.com/wiki/User-generated_content) - UGC overview
- [Accessory (Wiki)](https://roblox.fandom.com/wiki/Accessory) - Accessory system
- [Clothing (Wiki)](https://roblox.fandom.com/wiki/Clothing) - Clothing system

---

## Two Approaches to Avatar Customization

### 1. HumanoidDescription (Recommended)
Best for: Comprehensive avatar changes, player characters, loading from asset IDs

### 2. Direct Clothing Instances
Best for: NPCs, simple clothing changes, runtime modifications

---

## HumanoidDescription Approach

### Key Properties

| Property | Type | Description |
|----------|------|-------------|
| `Shirt` | number | Shirt asset ID |
| `Pants` | number | Pants asset ID |
| `GraphicTShirt` | number | T-shirt asset ID |
| `Face` | number | Face asset ID |
| `Head` | number | Head mesh asset ID |
| `Torso` | number | Torso mesh asset ID |
| `LeftArm`, `RightArm` | number | Arm mesh asset IDs |
| `LeftLeg`, `RightLeg` | number | Leg mesh asset IDs |
| `HatAccessory` | string | Comma-separated hat asset IDs |
| `HairAccessory` | string | Comma-separated hair asset IDs |
| `FaceAccessory` | string | Comma-separated face accessory IDs |
| `NeckAccessory` | string | Comma-separated neck accessory IDs |
| `ShouldersAccessory` | string | Comma-separated shoulder accessory IDs |
| `FrontAccessory` | string | Comma-separated front accessory IDs |
| `BackAccessory` | string | Comma-separated back accessory IDs |
| `WaistAccessory` | string | Comma-separated waist accessory IDs |

### Creating HumanoidDescription

```lua
-- Method 1: Create new empty description
local humanoidDescription = Instance.new("HumanoidDescription")

-- Method 2: Get from existing character
local function getDescriptionFromCharacter(character)
    local humanoid = character:FindFirstChildOfClass("Humanoid")
    if humanoid then
        return humanoid:GetAppliedDescription()
    end
    return nil
end

-- Method 3: Get from player's avatar
local Players = game:GetService("Players")
local function getDescriptionFromUserId(userId)
    local success, description = pcall(function()
        return Players:GetHumanoidDescriptionFromUserId(userId)
    end)
    return success and description or nil
end

-- Method 4: Get from outfit ID
local function getDescriptionFromOutfit(outfitId)
    local success, description = pcall(function()
        return Players:GetHumanoidDescriptionFromOutfitId(outfitId)
    end)
    return success and description or nil
end
```

### Modifying HumanoidDescription

```lua
local function customizeDescription(humanoidDescription)
    -- Set clothing (use asset IDs, not content URLs)
    humanoidDescription.Shirt = 6536023867        -- Shirt asset ID
    humanoidDescription.Pants = 6536027646        -- Pants asset ID
    humanoidDescription.GraphicTShirt = 1711661   -- T-shirt asset ID

    -- Set accessories (comma-separated strings for multiple)
    humanoidDescription.HatAccessory = "2551510151,2535600138"
    humanoidDescription.HairAccessory = "4819740796"
    humanoidDescription.FaceAccessory = ""
    humanoidDescription.BackAccessory = "4447084948"

    -- Set body parts
    humanoidDescription.Face = 86487700
    humanoidDescription.Head = 0  -- 0 = default

    -- Set body colors
    humanoidDescription.HeadColor = Color3.fromRGB(234, 184, 146)
    humanoidDescription.TorsoColor = Color3.fromRGB(234, 184, 146)
    humanoidDescription.LeftArmColor = Color3.fromRGB(234, 184, 146)
    humanoidDescription.RightArmColor = Color3.fromRGB(234, 184, 146)
    humanoidDescription.LeftLegColor = Color3.fromRGB(234, 184, 146)
    humanoidDescription.RightLegColor = Color3.fromRGB(234, 184, 146)

    -- Set scale
    humanoidDescription.HeightScale = 1.0
    humanoidDescription.WidthScale = 1.0
    humanoidDescription.HeadScale = 1.0
    humanoidDescription.BodyTypeScale = 0.0  -- 0 = blocky, 1 = realistic
    humanoidDescription.ProportionScale = 0.0

    return humanoidDescription
end
```

### Setting Multiple Accessories with SetAccessories

```lua
local function setMultipleAccessories(humanoidDescription)
    local accessories = {
        {
            Order = 1,
            AssetId = 6984769289,
            AccessoryType = Enum.AccessoryType.Hat
        },
        {
            Order = 2,
            AssetId = 6984767443,
            AccessoryType = Enum.AccessoryType.Hair
        },
        {
            Order = 3,
            AssetId = 4447084948,
            AccessoryType = Enum.AccessoryType.Back
        }
    }

    humanoidDescription:SetAccessories(accessories, false)  -- false = don't include rigid accessories
end
```

### Applying HumanoidDescription

```lua
-- Apply to existing character
local function applyToCharacter(character, humanoidDescription)
    local humanoid = character:FindFirstChildOfClass("Humanoid")
    if humanoid then
        humanoid:ApplyDescription(humanoidDescription)
    end
end

-- Apply to NPC
local function dressNPC(npc, shirtId, pantsId, hatIds)
    local humanoid = npc:FindFirstChildOfClass("Humanoid")
    if not humanoid then return end

    local description = humanoid:GetAppliedDescription()
    description.Shirt = shirtId or description.Shirt
    description.Pants = pantsId or description.Pants
    description.HatAccessory = hatIds or description.HatAccessory

    humanoid:ApplyDescription(description)
end

-- Load character with description (for spawning)
local function spawnWithDescription(player, humanoidDescription)
    player:LoadCharacterWithHumanoidDescription(humanoidDescription)
end
```

---

## Direct Clothing Instances (Classic Method)

### Apply Shirt to Character/NPC

```lua
local function applyShirt(character, shirtAssetId)
    -- Find or create Shirt instance
    local shirt = character:FindFirstChildOfClass("Shirt")
    if not shirt then
        shirt = Instance.new("Shirt")
        shirt.Parent = character
    end

    -- Set template (use rbxassetid:// format)
    shirt.ShirtTemplate = "rbxassetid://" .. shirtAssetId
end
```

### Apply Pants to Character/NPC

```lua
local function applyPants(character, pantsAssetId)
    local pants = character:FindFirstChildOfClass("Pants")
    if not pants then
        pants = Instance.new("Pants")
        pants.Parent = character
    end

    pants.PantsTemplate = "rbxassetid://" .. pantsAssetId
end
```

### Apply T-Shirt to Character/NPC

```lua
local function applyTShirt(character, tshirtAssetId)
    local tshirt = character:FindFirstChildOfClass("ShirtGraphic")
    if not tshirt then
        tshirt = Instance.new("ShirtGraphic")
        tshirt.Parent = character
    end

    tshirt.Graphic = "rbxassetid://" .. tshirtAssetId
end
```

### Apply Complete Outfit

```lua
local function applyOutfit(character, outfit)
    -- outfit = { shirt = id, pants = id, tshirt = id }

    if outfit.shirt then
        applyShirt(character, outfit.shirt)
    end

    if outfit.pants then
        applyPants(character, outfit.pants)
    end

    if outfit.tshirt then
        applyTShirt(character, outfit.tshirt)
    end
end

-- Usage
applyOutfit(npc, {
    shirt = 6536023867,
    pants = 6536027646,
    tshirt = 1711661
})
```

---

## Loading Accessories with InsertService

```lua
local InsertService = game:GetService("InsertService")

-- IMPORTANT: Can only load assets accessible to experience creator
local function loadAccessory(accessoryAssetId)
    local success, model = pcall(function()
        return InsertService:LoadAsset(accessoryAssetId)
    end)

    if success and model then
        local accessory = model:FindFirstChildOfClass("Accessory")
        if accessory then
            accessory.Parent = nil  -- Remove from model container
            model:Destroy()
            return accessory
        end
        model:Destroy()
    end

    return nil
end

-- Apply loaded accessory to character
local function giveAccessory(character, accessoryAssetId)
    local accessory = loadAccessory(accessoryAssetId)
    if accessory then
        local humanoid = character:FindFirstChildOfClass("Humanoid")
        if humanoid then
            humanoid:AddAccessory(accessory)
        end
    end
end
```

---

## AvatarEditorService (Catalog Integration)

### Get Item Details

```lua
local AvatarEditorService = game:GetService("AvatarEditorService")

local function getItemDetails(assetId)
    local success, details = pcall(function()
        return AvatarEditorService:GetItemDetails(assetId, Enum.AvatarItemType.Asset)
    end)

    if success then
        return {
            name = details.Name,
            assetType = details.AssetType,
            price = details.Price,
            isOwned = details.IsOwned,
            isFavorited = details.IsFavorited,
            creatorId = details.CreatorTargetId,
            creatorName = details.CreatorName
        }
    end

    return nil
end
```

### Get Player's Inventory

```lua
local function getPlayerInventory(player, assetTypes)
    -- assetTypes = array of Enum.AvatarAssetType
    local success, inventory = pcall(function()
        return AvatarEditorService:GetInventory(assetTypes)
    end)

    if success then
        return inventory:GetCurrentPage()
    end

    return {}
end

-- Example: Get player's hats
local hatTypes = {Enum.AvatarAssetType.Hat}
local playerHats = getPlayerInventory(player, hatTypes)
```

### Get Outfit Details

```lua
local function getOutfitDetails(outfitId)
    local success, details = pcall(function()
        return AvatarEditorService:GetOutfitDetails(outfitId)
    end)

    return success and details or nil
end
```

---

## Complete NPC Dressing System

```lua
local Players = game:GetService("Players")

local NPCOutfits = {
    Guard = {
        shirt = 6536023867,
        pants = 6536027646,
        hats = "2551510151",
        bodyColors = {
            head = Color3.fromRGB(234, 184, 146),
            torso = Color3.fromRGB(234, 184, 146)
        }
    },
    Merchant = {
        shirt = 398633610,
        pants = 398635927,
        tshirt = 0,
        hats = "4819740796"
    }
}

local function createDressedNPC(npcModel, outfitName)
    local outfit = NPCOutfits[outfitName]
    if not outfit then return end

    local humanoid = npcModel:FindFirstChildOfClass("Humanoid")
    if not humanoid then return end

    -- Get current description or create new one
    local description = humanoid:GetAppliedDescription()

    -- Apply outfit
    if outfit.shirt then
        description.Shirt = outfit.shirt
    end
    if outfit.pants then
        description.Pants = outfit.pants
    end
    if outfit.tshirt then
        description.GraphicTShirt = outfit.tshirt
    end
    if outfit.hats then
        description.HatAccessory = outfit.hats
    end

    -- Apply body colors
    if outfit.bodyColors then
        if outfit.bodyColors.head then
            description.HeadColor = outfit.bodyColors.head
        end
        if outfit.bodyColors.torso then
            description.TorsoColor = outfit.bodyColors.torso
        end
        -- ... etc for other body parts
    end

    -- Apply the description
    humanoid:ApplyDescription(description)
end
```

---

## UGC Catalog Search (Server-Side)

```lua
local AvatarEditorService = game:GetService("AvatarEditorService")

-- Search catalog for items
local function searchCatalog(keyword, assetType, sortType)
    local searchParams = CatalogSearchParams.new()
    searchParams.SearchKeyword = keyword
    searchParams.AssetTypes = {assetType}
    searchParams.SortType = sortType or Enum.CatalogSortType.Relevance

    local success, results = pcall(function()
        return AvatarEditorService:SearchCatalog(searchParams)
    end)

    if success then
        return results:GetCurrentPage()
    end

    return {}
end

-- Example: Search for hats
local hats = searchCatalog("crown", Enum.AvatarAssetType.Hat)
for _, hat in ipairs(hats) do
    print(hat.Name, hat.Id)
end
```

---

## AccessoryType Enum Reference

| Enum Value | Description |
|------------|-------------|
| `Enum.AccessoryType.Hat` | Hats, helmets |
| `Enum.AccessoryType.Hair` | Hair styles |
| `Enum.AccessoryType.Face` | Glasses, masks |
| `Enum.AccessoryType.Neck` | Necklaces, scarves |
| `Enum.AccessoryType.Shoulder` | Shoulder pads |
| `Enum.AccessoryType.Front` | Front accessories |
| `Enum.AccessoryType.Back` | Backpacks, wings |
| `Enum.AccessoryType.Waist` | Belts, tails |
| `Enum.AccessoryType.TShirt` | Layered t-shirts |
| `Enum.AccessoryType.Shirt` | Layered shirts |
| `Enum.AccessoryType.Pants` | Layered pants |
| `Enum.AccessoryType.Jacket` | Layered jackets |
| `Enum.AccessoryType.Sweater` | Layered sweaters |
| `Enum.AccessoryType.Shorts` | Layered shorts |
| `Enum.AccessoryType.LeftShoe` | Left shoe |
| `Enum.AccessoryType.RightShoe` | Right shoe |
| `Enum.AccessoryType.DressSkirt` | Dresses/skirts |

---

## Important Considerations

### Asset ID vs Content ID
- **Asset ID**: The numeric ID (e.g., `6536023867`)
- **Content ID**: The full URL format (e.g., `rbxassetid://6536023867`)
- HumanoidDescription properties use **Asset IDs** (numbers)
- Shirt/Pants/ShirtGraphic templates use **Content IDs** (strings)

### Security & Permissions
- `InsertService:LoadAsset()` only works with assets accessible to the experience creator
- For UGC items from other creators, use HumanoidDescription with asset IDs instead
- Player inventory access requires appropriate permissions

### Classic vs Layered Clothing
- **Classic Clothing**: Shirt, Pants, ShirtGraphic (2D textures)
- **Layered Clothing**: 3D clothing that deforms with the avatar body
- Layered clothing uses AccessoryType values like TShirt, Jacket, Sweater

### Best Practices
1. Always wrap asset loading in `pcall()` for error handling
2. Cache HumanoidDescriptions when making multiple changes
3. Use `GetAppliedDescription()` to preserve existing appearance when making partial changes
4. For NPCs, apply description once after all changes rather than multiple times

## Checklist for Avatar Customization

- [ ] Determine approach (HumanoidDescription vs Direct Instances)
- [ ] Collect asset IDs for clothing/accessories
- [ ] Handle pcall for all async operations
- [ ] Test with R6 and R15 rigs
- [ ] Consider body colors and scale
- [ ] Verify asset permissions for InsertService usage
- [ ] Cache descriptions for performance
