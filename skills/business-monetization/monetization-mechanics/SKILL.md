---
name: monetization-mechanics
description: Roblox-specific monetization strategies and game mechanics that drive engagement and revenue. Use when designing game economies, implementing purchase systems, or planning retention features.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Roblox Monetization & Game Mechanics

## Quick Reference Links

**Official Documentation:**
- [Monetization Overview](https://create.roblox.com/docs/production/monetization)
- [Passes](https://create.roblox.com/docs/production/monetization/game-passes)
- [Developer Products](https://create.roblox.com/docs/production/monetization/developer-products)
- [Subscriptions](https://create.roblox.com/docs/production/monetization/subscriptions)
- [Creator Rewards](https://create.roblox.com/docs/creator-rewards)
- [Live Ops Essentials](https://create.roblox.com/docs/production/promotion/live-ops-essentials)

**Wiki References:**
- [Game Pass (Wiki)](https://roblox.fandom.com/wiki/Pass)
- [Developer Product (Wiki)](https://roblox.fandom.com/wiki/Developer_product)
- [Creator Rewards (Wiki)](https://roblox.fandom.com/wiki/Creator_Rewards)
- [Private Servers (Wiki)](https://roblox.fandom.com/wiki/Private_server)
- [Tycoon Genre](https://roblox.fandom.com/wiki/Tycoon)
- [Simulator Genre](https://roblox.fandom.com/wiki/Simulator)
- [Obby Genre](https://roblox.fandom.com/wiki/Obby)

---

## Monetization Products

### 1. Game Passes (One-Time Purchases)
**Best for:** Permanent unlocks, VIP benefits, cosmetics

```lua
-- Check if player owns a pass
local MarketplaceService = game:GetService("MarketplaceService")
local Players = game:GetService("Players")

local PASS_ID = 123456789

local function hasPass(player)
    local success, hasPass = pcall(function()
        return MarketplaceService:UserOwnsGamePassAsync(player.UserId, PASS_ID)
    end)
    return success and hasPass
end

-- Prompt purchase
MarketplaceService:PromptGamePassPurchase(player, PASS_ID)

-- Handle purchase completion
MarketplaceService.PromptGamePassPurchaseFinished:Connect(function(player, passId, purchased)
    if purchased and passId == PASS_ID then
        -- Grant benefits
    end
end)
```

**Common Pass Types:**
- VIP/Premium access (2x coins, special areas)
- Permanent boosts (speed, damage, luck)
- Cosmetic unlocks (trails, effects, skins)
- Skip stages (obbies)
- Extra inventory slots
- Radio/boombox access

**Pricing Guidelines:**
- Small perks: 50-100 Robux
- Medium benefits: 100-400 Robux
- Major features: 400-1000 Robux
- Premium VIP: 1000+ Robux

### 2. Developer Products (Consumables)
**Best for:** Currency, consumables, repeatable purchases

```lua
local MarketplaceService = game:GetService("MarketplaceService")
local DataStoreService = game:GetService("DataStoreService")

local PRODUCTS = {
    [123456] = {name = "100 Coins", coins = 100},
    [123457] = {name = "500 Coins", coins = 500},
    [123458] = {name = "Revive", type = "revive"},
}

-- IMPORTANT: Must save purchase data - Roblox doesn't track this
MarketplaceService.ProcessReceipt = function(receiptInfo)
    local player = Players:GetPlayerByUserId(receiptInfo.PlayerId)
    if not player then return Enum.ProductPurchaseDecision.NotProcessedYet end

    local product = PRODUCTS[receiptInfo.ProductId]
    if not product then return Enum.ProductPurchaseDecision.NotProcessedYet end

    -- Grant the product
    local success = pcall(function()
        if product.coins then
            -- Add coins to player data
            addCoins(player, product.coins)
        elseif product.type == "revive" then
            revivePlayer(player)
        end
    end)

    if success then
        return Enum.ProductPurchaseDecision.PurchaseGranted
    end
    return Enum.ProductPurchaseDecision.NotProcessedYet
end

-- Prompt purchase
MarketplaceService:PromptProductPurchase(player, productId)
```

**Common Developer Products:**
- In-game currency bundles
- Revives/extra lives
- Temporary boosts (2x XP for 30 min)
- Loot boxes/crates (be transparent about odds!)
- Rebirths/prestiges
- Instant unlocks

### 3. Subscriptions (Recurring Monthly)
**Best for:** Battle passes, VIP memberships, premium tiers

```lua
local MarketplaceService = game:GetService("MarketplaceService")

local SUBSCRIPTION_ID = "EXP-123456"

-- Check active subscription
local function hasSubscription(player)
    local success, result = pcall(function()
        return MarketplaceService:GetUserSubscriptionStatusAsync(player, SUBSCRIPTION_ID)
    end)
    return success and result and result.IsSubscribed
end

-- Prompt subscription
MarketplaceService:PromptSubscriptionPurchase(player, SUBSCRIPTION_ID)
```

**Subscription Ideas:**
- Monthly VIP with exclusive rewards
- Battle pass with tiered rewards
- Premium server access
- Exclusive cosmetic rotations

### 4. Private Servers
**Best for:** Farming, content creation, privacy

```lua
-- Detect private server
local privateServerId = game.PrivateServerId
local privateServerOwnerId = game.PrivateServerOwnerId

local isPrivateServer = privateServerId ~= "" and privateServerId ~= nil
```

- Can be free or paid (monthly subscription)
- Developers earn 70% of paid server revenue
- Players can own up to 100 free private servers total
- Popular for: farming, content creation, testing, privacy

### 5. Creator Rewards (NEW - July 2025)
Replaced Premium Payouts. Two reward systems:

**Daily Engagement Rewards:**
- 5 Robux per qualified user
- User must visit your experience as one of first 3 that day
- User must spend 10+ minutes in your experience
- User must be "Active Spender" ($9.99+ USD spent in past 60 days)

**Audience Expansion Rewards:**
- 35% revenue share on user's first $100 USD purchases (platform-wide)
- For new users or reactivated users you bring
- Requirements:
  - User plays 10+ minutes on first day
  - Experience maintains 100+ DAU for 60 days
  - Attribution via share link, direct link, or search

### 6. Immersive Ads
Insert ad units into your experience for passive revenue:
- Image ad format (billboards, posters)
- Portal ad format (teleport to advertiser experience)

## Game Mechanics by Genre

### Tycoon Mechanics
Core loop: Collect → Upgrade → Expand → Rebirth

```lua
-- Dropper system
local function createDropper(tycoon, dropperData)
    local dropper = Instance.new("Part")
    -- Dropper creates "bricks" that fall onto conveyor

    local function drop()
        local brick = Instance.new("Part")
        brick.Size = Vector3.new(1, 1, 1)
        brick.Position = dropper.Position - Vector3.new(0, 2, 0)
        brick.Parent = workspace.Drops

        -- Brick value (can be upgraded)
        brick:SetAttribute("Value", dropperData.baseValue * tycoon.multiplier)
    end

    -- Auto-drop or click-to-drop
    if dropperData.auto then
        task.spawn(function()
            while true do
                drop()
                task.wait(dropperData.interval)
            end
        end)
    end
end

-- Rebirth system (prestige)
local function rebirth(player)
    local data = getPlayerData(player)
    if data.money >= getRebirthCost(data.rebirths) then
        data.rebirths = data.rebirths + 1
        data.multiplier = 1 + (data.rebirths * 0.5)  -- 50% boost per rebirth
        data.money = 0
        -- Reset tycoon but keep multiplier
        resetTycoon(player)
    end
end
```

**Key Mechanics:**
- Droppers (manual click or auto)
- Conveyor belts
- Upgraders (increase brick value)
- Collectors (convert bricks to cash)
- Rebirth/prestige system
- Multi-user tycoons (collaboration)

**Monetization:**
- 2x money pass
- Auto-collect pass
- Extra droppers
- Skip rebirth requirements
- Exclusive upgraders

### Simulator Mechanics
Core loop: Grind → Upgrade → Unlock areas → Rebirth

```lua
-- Click/tap to collect
local function collectResource(player, amount)
    local data = getPlayerData(player)
    local collected = math.min(amount * data.multiplier, data.maxCapacity - data.current)
    data.current = data.current + collected
end

-- Sell resources for currency
local function sell(player)
    local data = getPlayerData(player)
    local earnings = data.current * data.sellMultiplier
    data.coins = data.coins + earnings
    data.current = 0
end

-- Pet system with multipliers
local function equipPet(player, petId)
    local pet = getPetData(petId)
    local data = getPlayerData(player)
    data.multiplier = data.baseMultiplier * pet.boostMultiplier
end

-- Area unlock system
local function canAccessArea(player, area)
    local data = getPlayerData(player)
    return data.rebirths >= area.requiredRebirths
        or data.coins >= area.coinCost
        or hasPass(player, area.passId)
end
```

**Key Mechanics:**
- Click/tap collection
- Backpack capacity upgrades
- Sell stations
- Multiple areas/worlds (gated by level/currency/passes)
- Pet system with multipliers and trading
- Rebirth/prestige
- Leaderboards

**Monetization:**
- Capacity upgrades
- Multiplier boosts
- Area unlock passes
- Pet crates/eggs
- Auto-collect
- Lucky boosts (better pet odds)

### Obby Mechanics
Core loop: Attempt → Checkpoint → Progress → Complete

```lua
-- Checkpoint system
local function setupCheckpoint(checkpoint, stageNumber)
    checkpoint.Touched:Connect(function(hit)
        local player = Players:GetPlayerFromCharacter(hit.Parent)
        if player then
            local data = getPlayerData(player)
            if stageNumber > data.currentStage then
                data.currentStage = stageNumber
                -- Respawn point
                player.RespawnLocation = checkpoint
            end
        end
    end)
end

-- Skip stage (monetization)
local function skipStage(player)
    local data = getPlayerData(player)
    data.currentStage = data.currentStage + 1
    respawnAtStage(player, data.currentStage)
end

-- Kill brick
local killBrick = Instance.new("Part")
killBrick.Touched:Connect(function(hit)
    local humanoid = hit.Parent:FindFirstChild("Humanoid")
    if humanoid then
        humanoid.Health = 0
    end
end)
```

**Obby Varieties:**
- Classic obbies (simple platforming)
- Story-based obbies
- Escape obbies (escape the ___!)
- Tower obbies (climb to top)
- Difficulty chart obbies (progressive difficulty)

**Monetization:**
- Skip stage (per stage or bulk)
- Checkpoint saves (resume progress)
- Speed boost
- Gravity coil
- Winner area rewards

## Engagement & Retention Strategies

### Tourists vs Locals Framework
**Tourists:**
- Hop between experiences
- Prefer immediate effects
- Want variety and novelty
- Like standing out (cosmetics)
- Target with: instant unlocks, flashy items

**Locals:**
- Focus on fewer experiences
- Engage deeply over time
- Form the core community
- Prefer long-term benefits
- Target with: battle passes, subscriptions, progression systems

### Live Ops Best Practices
```lua
-- Daily login rewards
local function checkDailyReward(player)
    local data = getPlayerData(player)
    local today = os.date("%Y-%m-%d")

    if data.lastLogin ~= today then
        data.loginStreak = (data.lastLoginDate == yesterday())
            and data.loginStreak + 1
            or 1
        data.lastLogin = today

        -- Grant daily reward based on streak
        local reward = DAILY_REWARDS[math.min(data.loginStreak, #DAILY_REWARDS)]
        grantReward(player, reward)
    end
end

-- Limited time events
local function isEventActive(eventId)
    local event = EVENTS[eventId]
    local now = os.time()
    return now >= event.startTime and now <= event.endTime
end
```

**Key Principles:**
1. **Weekly update cadence** - Ideal for keeping users engaged
2. **Monthly minimum** - Roblox users expect regular updates
3. **Themed updates** - All new content connects to a theme
4. **Earn access** - Make users achieve something to access new content
5. **Don't use timers/energy** - Unpopular on Roblox (unlike mobile F2P)

### Social Features
```lua
-- Trading system
local function initiateTrade(player1, player2, offer1, offer2)
    -- Verify both players have items
    -- Show trade UI to both
    -- Require confirmation from both
    -- Execute swap atomically
end

-- Limited time items create urgency
local function isItemAvailable(itemId)
    local item = ITEMS[itemId]
    if item.limitedTime then
        return os.time() <= item.endTime
    end
    return true
end
```

**Social Monetization:**
- Trading systems (drive pet/item value)
- Limited time items (FOMO)
- Gifting system
- Party/friend bonuses
- Leaderboards (competitive spending)

## Anti-Patterns to Avoid

1. **Energy/Timer Systems** - Unpopular on Roblox
2. **Forced Ads** - Users will downvote
3. **Pay-to-Win without alternatives** - Provide free paths
4. **Hidden odds** - Be transparent with loot boxes
5. **Predatory pricing** - Users will leave bad reviews
6. **No free progression** - Always allow F2P advancement

## Revenue Split

| Source | Developer Share |
|--------|-----------------|
| Game Passes | 70% |
| Developer Products | 70% |
| Private Servers | 70% |
| Subscriptions | 70% |
| Creator Rewards | Varies |
| Immersive Ads | Varies |

## Data Persistence Warning

**CRITICAL:** Roblox does NOT automatically save purchase data for Developer Products. You MUST use DataStoreService to track purchases:

```lua
local DataStoreService = game:GetService("DataStoreService")
local purchaseStore = DataStoreService:GetDataStore("Purchases")

-- Always save after granting product
local function recordPurchase(player, receiptId, productId)
    local key = "user_" .. player.UserId
    local success, err = pcall(function()
        purchaseStore:UpdateAsync(key, function(oldData)
            oldData = oldData or {purchases = {}}
            table.insert(oldData.purchases, {
                receiptId = receiptId,
                productId = productId,
                timestamp = os.time()
            })
            return oldData
        end)
    end)
    return success
end
```

## Checklist for Monetization Design

- [ ] Clear value proposition for each purchase
- [ ] Free progression path exists
- [ ] Transparent odds for randomized items
- [ ] No forced wait timers
- [ ] Social/trading features to add value
- [ ] Regular content updates planned
- [ ] Data persistence for all purchases
- [ ] Price testing across tiers
- [ ] Both tourist and local appeal
- [ ] Rebirth/prestige for long-term engagement
