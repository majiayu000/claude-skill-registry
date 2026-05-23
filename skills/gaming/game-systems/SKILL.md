---
name: game-systems
description: Implements common game systems including inventory, shops, trading, quests, achievements, pets, crafting, and leveling. Use when building RPG mechanics, progression systems, or monetization features.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Roblox Game Systems

When implementing game systems, follow these patterns for robust and exploiter-resistant mechanics.

## Inventory System

### Slot-Based Inventory
```lua
local InventoryService = {}

local DEFAULT_SLOTS = 20
local MAX_STACK = 99

function InventoryService.create(maxSlots)
    return {
        slots = {},
        maxSlots = maxSlots or DEFAULT_SLOTS
    }
end

function InventoryService.addItem(inventory, itemId, quantity)
    quantity = quantity or 1

    -- Try to stack with existing
    for slotIndex, slot in pairs(inventory.slots) do
        if slot.itemId == itemId and slot.quantity < MAX_STACK then
            local canAdd = math.min(quantity, MAX_STACK - slot.quantity)
            slot.quantity = slot.quantity + canAdd
            quantity = quantity - canAdd

            if quantity <= 0 then
                return true, slotIndex
            end
        end
    end

    -- Find empty slots for remaining
    while quantity > 0 do
        local emptySlot = InventoryService.findEmptySlot(inventory)
        if not emptySlot then
            return false, "Inventory full"
        end

        local stackSize = math.min(quantity, MAX_STACK)
        inventory.slots[emptySlot] = {
            itemId = itemId,
            quantity = stackSize
        }
        quantity = quantity - stackSize
    end

    return true
end

function InventoryService.removeItem(inventory, itemId, quantity)
    quantity = quantity or 1
    local removed = 0

    -- Remove from slots (prefer partial stacks first)
    local slots = {}
    for slotIndex, slot in pairs(inventory.slots) do
        if slot.itemId == itemId then
            table.insert(slots, {index = slotIndex, quantity = slot.quantity})
        end
    end

    table.sort(slots, function(a, b) return a.quantity < b.quantity end)

    for _, slotInfo in ipairs(slots) do
        local slot = inventory.slots[slotInfo.index]
        local toRemove = math.min(quantity - removed, slot.quantity)

        slot.quantity = slot.quantity - toRemove
        removed = removed + toRemove

        if slot.quantity <= 0 then
            inventory.slots[slotInfo.index] = nil
        end

        if removed >= quantity then
            break
        end
    end

    return removed >= quantity, removed
end

function InventoryService.hasItem(inventory, itemId, quantity)
    quantity = quantity or 1
    local total = 0

    for _, slot in pairs(inventory.slots) do
        if slot.itemId == itemId then
            total = total + slot.quantity
            if total >= quantity then
                return true
            end
        end
    end

    return false
end

function InventoryService.getItemCount(inventory, itemId)
    local total = 0
    for _, slot in pairs(inventory.slots) do
        if slot.itemId == itemId then
            total = total + slot.quantity
        end
    end
    return total
end

function InventoryService.findEmptySlot(inventory)
    for i = 1, inventory.maxSlots do
        if not inventory.slots[i] then
            return i
        end
    end
    return nil
end
```

## Shop System

### Server-Side Shop with Validation
```lua
local ShopService = {}

local ShopItems = {
    sword_basic = {price = 100, currency = "coins", category = "weapons"},
    potion_health = {price = 50, currency = "coins", category = "consumables"},
    vip_pass = {price = 499, currency = "robux", productId = 123456789}
}

function ShopService.canPurchase(player, itemId, quantity)
    quantity = quantity or 1
    local item = ShopItems[itemId]

    if not item then
        return false, "Item not found"
    end

    if item.currency == "robux" then
        -- Robux purchases handled differently
        return true, "Use promptPurchase"
    end

    local playerCurrency = DataManager.get(player, item.currency) or 0
    local totalCost = item.price * quantity

    if playerCurrency < totalCost then
        return false, "Not enough " .. item.currency
    end

    -- Check inventory space
    local inventory = DataManager.get(player, "inventory")
    local emptySlots = InventoryService.countEmptySlots(inventory)

    if emptySlots < math.ceil(quantity / MAX_STACK) then
        return false, "Inventory full"
    end

    return true, totalCost
end

function ShopService.purchase(player, itemId, quantity)
    quantity = quantity or 1

    local canBuy, result = ShopService.canPurchase(player, itemId, quantity)
    if not canBuy then
        return false, result
    end

    local item = ShopItems[itemId]

    if item.currency == "robux" then
        -- Prompt Robux purchase
        MarketplaceService:PromptProductPurchase(player, item.productId)
        return true, "Purchase prompted"
    end

    -- Deduct currency (atomic operation)
    local success = DataManager.removeCurrency(player, item.currency, result)
    if not success then
        return false, "Transaction failed"
    end

    -- Add item
    local inventory = DataManager.get(player, "inventory")
    local added = InventoryService.addItem(inventory, itemId, quantity)

    if not added then
        -- Rollback currency
        DataManager.addCurrency(player, item.currency, result)
        return false, "Failed to add item"
    end

    return true, "Purchase successful"
end

-- Handle Robux purchases
MarketplaceService.ProcessReceipt = function(receiptInfo)
    local player = Players:GetPlayerByUserId(receiptInfo.PlayerId)
    if not player then
        return Enum.ProductPurchaseDecision.NotProcessedYet
    end

    local productId = receiptInfo.ProductId
    local itemId = getItemByProductId(productId)

    if not itemId then
        return Enum.ProductPurchaseDecision.NotProcessedYet
    end

    local inventory = DataManager.get(player, "inventory")
    local added = InventoryService.addItem(inventory, itemId, 1)

    if added then
        DataManager.save(player)
        return Enum.ProductPurchaseDecision.PurchaseGranted
    end

    return Enum.ProductPurchaseDecision.NotProcessedYet
end
```

## Trading System

### Secure Trading
```lua
local TradingService = {}
TradingService.activeTrades = {}

function TradingService.requestTrade(player1, player2)
    local tradeId = HttpService:GenerateGUID()

    TradingService.activeTrades[tradeId] = {
        player1 = {
            player = player1,
            items = {},
            confirmed = false
        },
        player2 = {
            player = player2,
            items = {},
            confirmed = false
        },
        status = "pending",
        createdAt = os.clock()
    }

    -- Notify player2
    TradeRequestRemote:FireClient(player2, player1.Name, tradeId)

    return tradeId
end

function TradingService.addItem(tradeId, player, itemSlot)
    local trade = TradingService.activeTrades[tradeId]
    if not trade or trade.status ~= "active" then
        return false, "Invalid trade"
    end

    local side = trade.player1.player == player and trade.player1 or
                 trade.player2.player == player and trade.player2

    if not side then
        return false, "Not in this trade"
    end

    -- Reset confirmations when items change
    trade.player1.confirmed = false
    trade.player2.confirmed = false

    -- Validate player owns the item
    local inventory = DataManager.get(player, "inventory")
    local item = inventory.slots[itemSlot]

    if not item then
        return false, "Item not found"
    end

    -- Check item isn't already in trade
    for _, existingSlot in ipairs(side.items) do
        if existingSlot == itemSlot then
            return false, "Item already in trade"
        end
    end

    table.insert(side.items, itemSlot)

    -- Update both players' UI
    TradeUpdateRemote:FireClient(trade.player1.player, tradeId, trade)
    TradeUpdateRemote:FireClient(trade.player2.player, tradeId, trade)

    return true
end

function TradingService.confirmTrade(tradeId, player)
    local trade = TradingService.activeTrades[tradeId]
    if not trade or trade.status ~= "active" then
        return false
    end

    local side = trade.player1.player == player and trade.player1 or
                 trade.player2.player == player and trade.player2

    if not side then return false end

    side.confirmed = true

    -- Check if both confirmed
    if trade.player1.confirmed and trade.player2.confirmed then
        return TradingService.executeTrade(tradeId)
    end

    -- Update UI
    TradeUpdateRemote:FireClient(trade.player1.player, tradeId, trade)
    TradeUpdateRemote:FireClient(trade.player2.player, tradeId, trade)

    return true
end

function TradingService.executeTrade(tradeId)
    local trade = TradingService.activeTrades[tradeId]
    trade.status = "executing"

    local p1 = trade.player1.player
    local p2 = trade.player2.player
    local inv1 = DataManager.get(p1, "inventory")
    local inv2 = DataManager.get(p2, "inventory")

    -- Validate both players still have the items
    for _, slot in ipairs(trade.player1.items) do
        if not inv1.slots[slot] then
            TradingService.cancelTrade(tradeId, "Item no longer available")
            return false
        end
    end

    for _, slot in ipairs(trade.player2.items) do
        if not inv2.slots[slot] then
            TradingService.cancelTrade(tradeId, "Item no longer available")
            return false
        end
    end

    -- Execute swap atomically
    local p1Items = {}
    local p2Items = {}

    -- Remove items from player 1
    for _, slot in ipairs(trade.player1.items) do
        table.insert(p1Items, inv1.slots[slot])
        inv1.slots[slot] = nil
    end

    -- Remove items from player 2
    for _, slot in ipairs(trade.player2.items) do
        table.insert(p2Items, inv2.slots[slot])
        inv2.slots[slot] = nil
    end

    -- Add player 1's items to player 2
    for _, item in ipairs(p1Items) do
        InventoryService.addItem(inv2, item.itemId, item.quantity)
    end

    -- Add player 2's items to player 1
    for _, item in ipairs(p2Items) do
        InventoryService.addItem(inv1, item.itemId, item.quantity)
    end

    -- Save both players
    DataManager.save(p1)
    DataManager.save(p2)

    -- Complete trade
    trade.status = "completed"
    TradingService.activeTrades[tradeId] = nil

    TradeCompleteRemote:FireClient(p1, tradeId, true)
    TradeCompleteRemote:FireClient(p2, tradeId, true)

    return true
end
```

## Quest System

### Quest Manager
```lua
local QuestService = {}

local QuestDefinitions = {
    kill_enemies_1 = {
        title = "Enemy Slayer",
        description = "Defeat 10 enemies",
        objectives = {
            {type = "kill", target = "enemy", count = 10}
        },
        rewards = {
            {type = "currency", currency = "coins", amount = 100},
            {type = "experience", amount = 50}
        }
    },
    collect_items_1 = {
        title = "Collector",
        description = "Collect 5 gems",
        objectives = {
            {type = "collect", item = "gem", count = 5}
        },
        rewards = {
            {type = "currency", currency = "coins", amount = 200}
        }
    }
}

function QuestService.startQuest(player, questId)
    local quest = QuestDefinitions[questId]
    if not quest then return false end

    local playerQuests = DataManager.get(player, "activeQuests") or {}

    -- Check not already active
    if playerQuests[questId] then
        return false, "Quest already active"
    end

    -- Initialize progress
    playerQuests[questId] = {
        startedAt = os.time(),
        progress = {}
    }

    for i, objective in ipairs(quest.objectives) do
        playerQuests[questId].progress[i] = 0
    end

    DataManager.set(player, "activeQuests", playerQuests)
    return true
end

function QuestService.updateProgress(player, eventType, eventData)
    local playerQuests = DataManager.get(player, "activeQuests") or {}
    local updated = false

    for questId, questProgress in pairs(playerQuests) do
        local quest = QuestDefinitions[questId]
        if not quest then continue end

        for i, objective in ipairs(quest.objectives) do
            if objective.type == eventType then
                local matches = true

                -- Check target matches
                if objective.target and eventData.target ~= objective.target then
                    matches = false
                end
                if objective.item and eventData.item ~= objective.item then
                    matches = false
                end

                if matches and questProgress.progress[i] < objective.count then
                    questProgress.progress[i] = questProgress.progress[i] + (eventData.amount or 1)
                    updated = true

                    -- Check if quest completed
                    if QuestService.isQuestComplete(questId, questProgress) then
                        QuestService.completeQuest(player, questId)
                    end
                end
            end
        end
    end

    if updated then
        DataManager.set(player, "activeQuests", playerQuests)
    end
end

function QuestService.isQuestComplete(questId, progress)
    local quest = QuestDefinitions[questId]

    for i, objective in ipairs(quest.objectives) do
        if progress.progress[i] < objective.count then
            return false
        end
    end

    return true
end

function QuestService.completeQuest(player, questId)
    local quest = QuestDefinitions[questId]
    local playerQuests = DataManager.get(player, "activeQuests")

    -- Remove from active
    playerQuests[questId] = nil
    DataManager.set(player, "activeQuests", playerQuests)

    -- Add to completed
    local completedQuests = DataManager.get(player, "completedQuests") or {}
    completedQuests[questId] = os.time()
    DataManager.set(player, "completedQuests", completedQuests)

    -- Grant rewards
    for _, reward in ipairs(quest.rewards) do
        if reward.type == "currency" then
            DataManager.addCurrency(player, reward.currency, reward.amount)
        elseif reward.type == "experience" then
            LevelingService.addExperience(player, reward.amount)
        elseif reward.type == "item" then
            local inventory = DataManager.get(player, "inventory")
            InventoryService.addItem(inventory, reward.item, reward.quantity or 1)
        end
    end

    QuestCompleteRemote:FireClient(player, questId, quest.rewards)
end
```

## Pet System

### Pet Manager
```lua
local PetService = {}

local PetDefinitions = {
    cat_basic = {name = "Cat", rarity = "common", bonuses = {luck = 5}},
    dog_basic = {name = "Dog", rarity = "common", bonuses = {speed = 5}},
    dragon_epic = {name = "Dragon", rarity = "epic", bonuses = {damage = 20, luck = 10}}
}

function PetService.createPet(petType)
    local def = PetDefinitions[petType]
    if not def then return nil end

    return {
        id = HttpService:GenerateGUID(),
        type = petType,
        name = def.name,
        level = 1,
        experience = 0,
        equipped = false
    }
end

function PetService.equipPet(player, petId)
    local pets = DataManager.get(player, "pets") or {}

    -- Find the pet
    local targetPet
    for _, pet in ipairs(pets) do
        if pet.id == petId then
            targetPet = pet
        else
            pet.equipped = false  -- Unequip others
        end
    end

    if not targetPet then
        return false, "Pet not found"
    end

    targetPet.equipped = true
    DataManager.set(player, "pets", pets)

    -- Apply bonuses
    PetService.applyBonuses(player, targetPet)

    -- Spawn visual pet
    PetService.spawnPetVisual(player, targetPet)

    return true
end

function PetService.applyBonuses(player, pet)
    local def = PetDefinitions[pet.type]
    if not def then return end

    local levelMultiplier = 1 + (pet.level - 1) * 0.1  -- 10% per level

    for stat, value in pairs(def.bonuses) do
        local bonus = math.floor(value * levelMultiplier)
        player:SetAttribute("PetBonus_" .. stat, bonus)
    end
end

function PetService.spawnPetVisual(player, pet)
    local character = player.Character
    if not character then return end

    -- Remove existing pet visual
    local existing = character:FindFirstChild("PetModel")
    if existing then existing:Destroy() end

    local def = PetDefinitions[pet.type]
    local petModel = ReplicatedStorage.Pets[pet.type]:Clone()
    petModel.Name = "PetModel"
    petModel.Parent = character

    -- Pet following behavior
    task.spawn(function()
        local hrp = character:FindFirstChild("HumanoidRootPart")
        while petModel.Parent and hrp do
            local targetPos = hrp.Position + hrp.CFrame.RightVector * 3 + Vector3.new(0, 2, 0)
            local currentPos = petModel.PrimaryPart.Position

            local direction = (targetPos - currentPos)
            if direction.Magnitude > 0.5 then
                local newPos = currentPos + direction.Unit * math.min(direction.Magnitude, 0.5)
                petModel:PivotTo(CFrame.lookAt(newPos, hrp.Position))
            end

            task.wait()
        end
    end)
end
```

## Leveling System

### Experience & Leveling
```lua
local LevelingService = {}

-- XP required for each level: level^2 * 100
local function getRequiredXP(level)
    return level * level * 100
end

function LevelingService.addExperience(player, amount)
    local currentLevel = DataManager.get(player, "level") or 1
    local currentXP = DataManager.get(player, "experience") or 0

    currentXP = currentXP + amount

    -- Check for level ups
    local levelsGained = 0
    while currentXP >= getRequiredXP(currentLevel) do
        currentXP = currentXP - getRequiredXP(currentLevel)
        currentLevel = currentLevel + 1
        levelsGained = levelsGained + 1
    end

    DataManager.set(player, "level", currentLevel)
    DataManager.set(player, "experience", currentXP)

    if levelsGained > 0 then
        LevelingService.onLevelUp(player, currentLevel, levelsGained)
    end

    return currentLevel, currentXP, levelsGained
end

function LevelingService.onLevelUp(player, newLevel, levelsGained)
    -- Heal to full
    local character = player.Character
    if character then
        local humanoid = character:FindFirstChildOfClass("Humanoid")
        if humanoid then
            humanoid.Health = humanoid.MaxHealth
        end
    end

    -- Grant stat points
    local statPoints = DataManager.get(player, "statPoints") or 0
    DataManager.set(player, "statPoints", statPoints + levelsGained * 3)

    -- Unlock abilities
    local unlocks = AbilityUnlocks[newLevel]
    if unlocks then
        for _, abilityId in ipairs(unlocks) do
            AbilityService.unlock(player, abilityId)
        end
    end

    -- Visual/audio feedback
    LevelUpRemote:FireClient(player, newLevel)
end

function LevelingService.getProgress(player)
    local level = DataManager.get(player, "level") or 1
    local xp = DataManager.get(player, "experience") or 0
    local required = getRequiredXP(level)

    return {
        level = level,
        currentXP = xp,
        requiredXP = required,
        progress = xp / required
    }
end
```

## Daily Rewards

### Daily Login System
```lua
local DailyRewardService = {}

local DAILY_REWARDS = {
    {type = "coins", amount = 100},
    {type = "coins", amount = 150},
    {type = "coins", amount = 200},
    {type = "gems", amount = 5},
    {type = "coins", amount = 300},
    {type = "gems", amount = 10},
    {type = "item", itemId = "rare_chest", amount = 1}
}

function DailyRewardService.checkDailyReward(player)
    local lastLogin = DataManager.get(player, "lastLoginTime") or 0
    local loginStreak = DataManager.get(player, "loginStreak") or 0

    local now = os.time()
    local lastLoginDate = os.date("*t", lastLogin)
    local currentDate = os.date("*t", now)

    -- Check if it's a new day
    local isNewDay = lastLoginDate.yday ~= currentDate.yday or
                     lastLoginDate.year ~= currentDate.year

    if not isNewDay then
        return nil, "Already claimed today"
    end

    -- Check if streak continues or resets
    local hoursSinceLastLogin = (now - lastLogin) / 3600
    if hoursSinceLastLogin > 48 then
        loginStreak = 0  -- Reset streak
    end

    loginStreak = loginStreak + 1
    local rewardIndex = ((loginStreak - 1) % #DAILY_REWARDS) + 1
    local reward = DAILY_REWARDS[rewardIndex]

    -- Update data
    DataManager.set(player, "lastLoginTime", now)
    DataManager.set(player, "loginStreak", loginStreak)

    -- Grant reward
    if reward.type == "coins" or reward.type == "gems" then
        DataManager.addCurrency(player, reward.type, reward.amount)
    elseif reward.type == "item" then
        local inventory = DataManager.get(player, "inventory")
        InventoryService.addItem(inventory, reward.itemId, reward.amount)
    end

    return {
        day = loginStreak,
        reward = reward
    }
end
```
