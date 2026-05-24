---
name: monetization
description: Implements monetization systems including GamePasses, Developer Products, Premium benefits, and ethical monetization patterns. Use when adding in-game purchases, premium features, or any Robux-based transactions.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Roblox Monetization Systems

When implementing monetization, follow these patterns for secure and player-friendly purchases.

## MarketplaceService Basics

```lua
local MarketplaceService = game:GetService("MarketplaceService")
local Players = game:GetService("Players")

-- IDs from your game's monetization page
local GAME_PASSES = {
    VIP = 123456789,
    DoubleCash = 234567890,
    SpeedBoost = 345678901
}

local DEV_PRODUCTS = {
    Cash_100 = 111111111,
    Cash_500 = 222222222,
    Cash_1000 = 333333333,
    Revive = 444444444
}
```

## Game Passes

### Checking Ownership

```lua
local function ownsGamePass(player, passId)
    local success, owns = pcall(function()
        return MarketplaceService:UserOwnsGamePassAsync(player.UserId, passId)
    end)

    if success then
        return owns
    else
        warn("Failed to check game pass ownership:", owns)
        return false
    end
end

-- Cache ownership to reduce API calls
local gamePassCache = {}

local function getGamePassOwnership(player, passId)
    local key = player.UserId .. "_" .. passId

    if gamePassCache[key] ~= nil then
        return gamePassCache[key]
    end

    local owns = ownsGamePass(player, passId)
    gamePassCache[key] = owns

    return owns
end

-- Clear cache when player leaves
Players.PlayerRemoving:Connect(function(player)
    for key in pairs(gamePassCache) do
        if key:find(tostring(player.UserId)) then
            gamePassCache[key] = nil
        end
    end
end)
```

### Prompting Purchase

```lua
local function promptGamePass(player, passId)
    local success, err = pcall(function()
        MarketplaceService:PromptGamePassPurchase(player, passId)
    end)

    if not success then
        warn("Failed to prompt game pass:", err)
    end
end

-- Handle purchase completion
MarketplaceService.PromptGamePassPurchaseFinished:Connect(function(player, passId, wasPurchased)
    if wasPurchased then
        -- Update cache
        local key = player.UserId .. "_" .. passId
        gamePassCache[key] = true

        -- Grant benefits immediately
        applyGamePassBenefits(player, passId)

        print(player.Name, "purchased game pass:", passId)
    end
end)
```

### Applying Benefits

```lua
local function applyGamePassBenefits(player, passId)
    if passId == GAME_PASSES.VIP then
        -- VIP tag
        player:SetAttribute("VIP", true)

        -- VIP chat tag
        local tags = player:GetAttribute("ChatTags") or ""
        player:SetAttribute("ChatTags", "[VIP] " .. tags)

        -- Daily bonus multiplier
        player:SetAttribute("DailyBonusMultiplier", 2)

    elseif passId == GAME_PASSES.DoubleCash then
        player:SetAttribute("CashMultiplier", 2)

    elseif passId == GAME_PASSES.SpeedBoost then
        player:SetAttribute("SpeedBoost", 1.5)

        -- Apply to character
        local character = player.Character
        if character then
            local humanoid = character:FindFirstChildOfClass("Humanoid")
            if humanoid then
                humanoid.WalkSpeed = 16 * 1.5
            end
        end
    end
end

-- Apply on join (for returning players)
Players.PlayerAdded:Connect(function(player)
    player.CharacterAdded:Connect(function()
        for name, passId in pairs(GAME_PASSES) do
            if getGamePassOwnership(player, passId) then
                applyGamePassBenefits(player, passId)
            end
        end
    end)
end)
```

## Developer Products (Consumables)

### Processing Receipts (CRITICAL)

```lua
-- This MUST be set and handle ALL purchases
local purchaseHistory = {}  -- In production, use DataStore

MarketplaceService.ProcessReceipt = function(receiptInfo)
    -- Prevent duplicate processing
    local purchaseKey = receiptInfo.PlayerId .. "_" .. receiptInfo.PurchaseId

    if purchaseHistory[purchaseKey] then
        return Enum.ProductPurchaseDecision.PurchaseGranted
    end

    local player = Players:GetPlayerByUserId(receiptInfo.PlayerId)
    if not player then
        -- Player left, try again later
        return Enum.ProductPurchaseDecision.NotProcessedYet
    end

    local productId = receiptInfo.ProductId
    local success = false

    -- Grant the product
    if productId == DEV_PRODUCTS.Cash_100 then
        success = grantCash(player, 100)
    elseif productId == DEV_PRODUCTS.Cash_500 then
        success = grantCash(player, 500)
    elseif productId == DEV_PRODUCTS.Cash_1000 then
        success = grantCash(player, 1000)
    elseif productId == DEV_PRODUCTS.Revive then
        success = revivePlayer(player)
    else
        warn("Unknown product:", productId)
        return Enum.ProductPurchaseDecision.NotProcessedYet
    end

    if success then
        -- Record purchase
        purchaseHistory[purchaseKey] = true

        -- In production: save to DataStore
        savePurchaseRecord(player, receiptInfo)

        return Enum.ProductPurchaseDecision.PurchaseGranted
    else
        return Enum.ProductPurchaseDecision.NotProcessedYet
    end
end

local function grantCash(player, amount)
    local currentCash = DataManager.get(player, "cash") or 0
    DataManager.set(player, "cash", currentCash + amount)

    -- Apply multipliers from game passes
    local multiplier = player:GetAttribute("CashMultiplier") or 1
    if multiplier > 1 then
        local bonus = amount * (multiplier - 1)
        DataManager.set(player, "cash", currentCash + amount + bonus)

        -- Notify about bonus
        CashNotificationRemote:FireClient(player, amount, bonus)
    else
        CashNotificationRemote:FireClient(player, amount, 0)
    end

    -- Save immediately after purchase
    DataManager.save(player)

    return true
end

local function revivePlayer(player)
    local character = player.Character
    if not character then return false end

    local humanoid = character:FindFirstChildOfClass("Humanoid")
    if not humanoid then return false end

    if humanoid.Health > 0 then
        return false  -- Not dead, don't charge
    end

    -- Revive
    humanoid.Health = humanoid.MaxHealth

    -- Clear ragdoll/death state if applicable
    player:SetAttribute("IsDead", false)

    ReviveEffectRemote:FireAllClients(character)

    return true
end
```

### Prompting Products

```lua
local function promptProduct(player, productId)
    local success, err = pcall(function()
        MarketplaceService:PromptProductPurchase(player, productId)
    end)

    if not success then
        warn("Failed to prompt product:", err)
    end
end

-- Example: Revive prompt on death
local function onPlayerDied(player)
    task.delay(2, function()
        -- Show revive option
        RevivePromptRemote:FireClient(player, DEV_PRODUCTS.Revive)
    end)
end
```

### Product Info Display

```lua
local function getProductInfo(productId)
    local success, info = pcall(function()
        return MarketplaceService:GetProductInfo(productId, Enum.InfoType.Product)
    end)

    if success then
        return {
            name = info.Name,
            description = info.Description,
            price = info.PriceInRobux,
            icon = "rbxassetid://" .. info.IconImageAssetId
        }
    end

    return nil
end

-- Cache product info
local productInfoCache = {}

local function getCachedProductInfo(productId)
    if not productInfoCache[productId] then
        productInfoCache[productId] = getProductInfo(productId)
    end
    return productInfoCache[productId]
end
```

## Premium Benefits

```lua
local function isPremium(player)
    return player.MembershipType == Enum.MembershipType.Premium
end

local function applyPremiumBenefits(player)
    if isPremium(player) then
        -- Premium badge
        player:SetAttribute("IsPremium", true)

        -- Premium-only benefits
        player:SetAttribute("CashMultiplier",
            (player:GetAttribute("CashMultiplier") or 1) * 1.5)

        player:SetAttribute("XPMultiplier",
            (player:GetAttribute("XPMultiplier") or 1) * 1.5)

        -- Premium daily bonus
        player:SetAttribute("DailyBonusMultiplier",
            (player:GetAttribute("DailyBonusMultiplier") or 1) * 2)

        -- Premium-only items unlocked
        player:SetAttribute("PremiumItemsUnlocked", true)
    end
end

-- Handle subscription changes mid-game
Players.PlayerMembershipChanged:Connect(function(player)
    if isPremium(player) then
        applyPremiumBenefits(player)
        PremiumWelcomeRemote:FireClient(player)
    end
end)

-- Prompt to upgrade to Premium
local function promptPremium(player)
    local success, err = pcall(function()
        MarketplaceService:PromptPremiumPurchase(player)
    end)

    if not success then
        warn("Failed to prompt premium:", err)
    end
end
```

## Shop UI Patterns

### Shop Item Template

```lua
-- Server: Shop configuration
local ShopItems = {
    cash = {
        {id = DEV_PRODUCTS.Cash_100, amount = 100, icon = "rbxassetid://123"},
        {id = DEV_PRODUCTS.Cash_500, amount = 500, icon = "rbxassetid://124", bonus = 50},
        {id = DEV_PRODUCTS.Cash_1000, amount = 1000, icon = "rbxassetid://125", bonus = 200}
    },
    gamePasses = {
        {id = GAME_PASSES.VIP, name = "VIP", description = "VIP tag + 2x daily bonus"},
        {id = GAME_PASSES.DoubleCash, name = "2x Cash", description = "Double all cash earnings"},
        {id = GAME_PASSES.SpeedBoost, name = "Speed Boost", description = "50% faster movement"}
    }
}

-- Client: Fetch and display
GetShopItemsRemote.OnClientEvent:Connect(function(items)
    for _, item in ipairs(items.cash) do
        local info = MarketplaceService:GetProductInfo(item.id, Enum.InfoType.Product)

        local button = createShopButton()
        button.Icon.Image = item.icon
        button.Amount.Text = item.amount .. (item.bonus and " +" .. item.bonus or "")
        button.Price.Text = info.PriceInRobux .. " R$"

        button.MouseButton1Click:Connect(function()
            MarketplaceService:PromptProductPurchase(Players.LocalPlayer, item.id)
        end)
    end
end)
```

### Purchase Confirmation UI

```lua
-- Client: Confirm before expensive purchases
local function confirmPurchase(productName, robuxCost)
    local result = showConfirmDialog(
        "Confirm Purchase",
        "Buy " .. productName .. " for " .. robuxCost .. " Robux?",
        {"Yes", "No"}
    )

    return result == "Yes"
end

-- Modified purchase flow
PurchaseButton.MouseButton1Click:Connect(function()
    local info = getCachedProductInfo(selectedProductId)

    if info.price >= 100 then  -- Confirm expensive purchases
        if not confirmPurchase(info.name, info.price) then
            return
        end
    end

    MarketplaceService:PromptProductPurchase(LocalPlayer, selectedProductId)
end)
```

## Purchase Persistence

### Save Purchase Records

```lua
local PurchaseStore = DataStoreService:GetDataStore("Purchases_v1")

local function savePurchaseRecord(player, receiptInfo)
    local key = "Player_" .. player.UserId

    pcall(function()
        PurchaseStore:UpdateAsync(key, function(data)
            data = data or {purchases = {}}

            table.insert(data.purchases, {
                productId = receiptInfo.ProductId,
                purchaseId = receiptInfo.PurchaseId,
                time = os.time(),
                robuxSpent = receiptInfo.CurrencySpent
            })

            -- Keep last 100 purchases
            while #data.purchases > 100 do
                table.remove(data.purchases, 1)
            end

            return data
        end)
    end)
end

local function getPurchaseHistory(player)
    local key = "Player_" .. player.UserId

    local success, data = pcall(function()
        return PurchaseStore:GetAsync(key)
    end)

    if success and data then
        return data.purchases or {}
    end

    return {}
end
```

### Grant Missed Purchases

```lua
-- On player join, check for ungranted purchases
local function checkPendingPurchases(player)
    local history = getPurchaseHistory(player)
    local grantedIds = DataManager.get(player, "grantedPurchases") or {}

    for _, purchase in ipairs(history) do
        if not grantedIds[purchase.purchaseId] then
            -- Grant this purchase
            local granted = grantProduct(player, purchase.productId)

            if granted then
                grantedIds[purchase.purchaseId] = true
            end
        end
    end

    DataManager.set(player, "grantedPurchases", grantedIds)
end
```

## Ethical Monetization Guidelines

### DO:
- Clearly display prices before purchase
- Allow players to earn most things through gameplay
- Make premium items cosmetic or time-saving, not power-increasing
- Provide value at every price point
- Respect player's time and money

### DON'T:
- Create artificial scarcity or FOMO
- Hide true costs behind multiple currencies
- Require purchases to progress or compete
- Target children with manipulative dark patterns
- Make gameplay frustrating to encourage purchases

### Fair Pricing Examples

```lua
-- GOOD: Clear value proposition
local SHOP_CONFIG = {
    -- Currency packs with bonus for larger purchases
    cashPacks = {
        {robux = 25, cash = 100, bonus = 0},     -- Base rate
        {robux = 50, cash = 250, bonus = 50},    -- 20% bonus
        {robux = 100, cash = 600, bonus = 100},  -- 40% bonus
        {robux = 200, cash = 1500, bonus = 300}  -- 50% bonus
    },

    -- Game passes are permanent, one-time purchases
    gamePasses = {
        vip = {robux = 199, benefits = "Permanent VIP status + 2x daily bonus"},
        doubleCash = {robux = 149, benefits = "Permanent 2x cash multiplier"}
    }
}

-- BAD: Don't do this
-- local PREDATORY_PATTERNS = {
--     limitedTimeOffer = true,  -- Creates FOMO
--     spinToWin = true,         -- Gambling mechanics
--     payToProgress = true,     -- Gameplay gating
--     obscurePricing = true     -- Multiple currencies
-- }
```

### Spending Limits (Self-Regulation)

```lua
-- Track spending for responsible monetization
local function trackSpending(player, robuxSpent)
    local today = os.date("%Y-%m-%d")
    local spendingKey = "Spending_" .. today

    local todaySpent = player:GetAttribute(spendingKey) or 0
    todaySpent = todaySpent + robuxSpent
    player:SetAttribute(spendingKey, todaySpent)

    -- Optional: Warn at spending thresholds
    if todaySpent >= 1000 then
        SpendingWarningRemote:FireClient(player,
            "You've spent " .. todaySpent .. " Robux today. Consider taking a break!")
    end
end

-- In ProcessReceipt
MarketplaceService.ProcessReceipt = function(receiptInfo)
    -- ... existing code ...

    if success then
        trackSpending(player, receiptInfo.CurrencySpent)
    end

    -- ... existing code ...
end
```

## Complete Shop Implementation

```lua
-- Server: MonetizationService.lua
local MonetizationService = {}

-- Configuration
MonetizationService.GAME_PASSES = {
    VIP = {id = 123456789, benefits = {"VIPTag", "DoubleDailyBonus"}},
    DoubleCash = {id = 234567890, benefits = {"CashMultiplier"}},
    PetSlots = {id = 345678901, benefits = {"ExtraPetSlots"}}
}

MonetizationService.DEV_PRODUCTS = {
    Cash_100 = {id = 111111111, grant = {"cash", 100}},
    Cash_500 = {id = 222222222, grant = {"cash", 500}},
    Gems_10 = {id = 333333333, grant = {"gems", 10}},
    Revive = {id = 444444444, action = "revive"}
}

-- Ownership cache
local ownershipCache = {}

function MonetizationService.init()
    -- Set up ProcessReceipt
    MarketplaceService.ProcessReceipt = function(receiptInfo)
        return MonetizationService.processReceipt(receiptInfo)
    end

    -- Handle game pass purchases
    MarketplaceService.PromptGamePassPurchaseFinished:Connect(function(player, passId, purchased)
        if purchased then
            MonetizationService.onGamePassPurchased(player, passId)
        end
    end)

    -- Apply benefits on join
    Players.PlayerAdded:Connect(function(player)
        player.CharacterAdded:Connect(function()
            MonetizationService.applyAllBenefits(player)
        end)
    end)
end

function MonetizationService.ownsGamePass(player, passName)
    local passConfig = MonetizationService.GAME_PASSES[passName]
    if not passConfig then return false end

    local cacheKey = player.UserId .. "_" .. passConfig.id
    if ownershipCache[cacheKey] ~= nil then
        return ownershipCache[cacheKey]
    end

    local success, owns = pcall(function()
        return MarketplaceService:UserOwnsGamePassAsync(player.UserId, passConfig.id)
    end)

    if success then
        ownershipCache[cacheKey] = owns
        return owns
    end

    return false
end

function MonetizationService.applyAllBenefits(player)
    -- Game passes
    for passName, config in pairs(MonetizationService.GAME_PASSES) do
        if MonetizationService.ownsGamePass(player, passName) then
            for _, benefit in ipairs(config.benefits) do
                MonetizationService.applyBenefit(player, benefit)
            end
        end
    end

    -- Premium
    if player.MembershipType == Enum.MembershipType.Premium then
        MonetizationService.applyBenefit(player, "Premium")
    end
end

function MonetizationService.applyBenefit(player, benefit)
    if benefit == "VIPTag" then
        player:SetAttribute("VIP", true)
    elseif benefit == "DoubleDailyBonus" then
        player:SetAttribute("DailyBonusMultiplier", 2)
    elseif benefit == "CashMultiplier" then
        player:SetAttribute("CashMultiplier", 2)
    elseif benefit == "ExtraPetSlots" then
        player:SetAttribute("MaxPets", 10)  -- Default is 5
    elseif benefit == "Premium" then
        player:SetAttribute("IsPremium", true)
        player:SetAttribute("XPMultiplier", 1.5)
    end
end

function MonetizationService.processReceipt(receiptInfo)
    local player = Players:GetPlayerByUserId(receiptInfo.PlayerId)
    if not player then
        return Enum.ProductPurchaseDecision.NotProcessedYet
    end

    local productId = receiptInfo.ProductId
    local granted = false

    -- Find matching product
    for productName, config in pairs(MonetizationService.DEV_PRODUCTS) do
        if config.id == productId then
            if config.grant then
                local currency, amount = config.grant[1], config.grant[2]
                granted = MonetizationService.grantCurrency(player, currency, amount)
            elseif config.action == "revive" then
                granted = MonetizationService.revivePlayer(player)
            end
            break
        end
    end

    if granted then
        DataManager.save(player)
        return Enum.ProductPurchaseDecision.PurchaseGranted
    end

    return Enum.ProductPurchaseDecision.NotProcessedYet
end

function MonetizationService.grantCurrency(player, currency, amount)
    local current = DataManager.get(player, currency) or 0

    -- Apply multipliers
    local multiplier = player:GetAttribute(currency:sub(1,1):upper() .. currency:sub(2) .. "Multiplier") or 1
    local finalAmount = math.floor(amount * multiplier)

    DataManager.set(player, currency, current + finalAmount)

    CurrencyGrantedRemote:FireClient(player, currency, amount, finalAmount - amount)

    return true
end

function MonetizationService.revivePlayer(player)
    local character = player.Character
    if not character then return false end

    local humanoid = character:FindFirstChildOfClass("Humanoid")
    if not humanoid or humanoid.Health > 0 then
        return false
    end

    humanoid.Health = humanoid.MaxHealth
    return true
end

return MonetizationService
```
