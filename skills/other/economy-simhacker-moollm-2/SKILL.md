---
name: economy
description: Currency and trade — gold flows where stories lead
license: MIT
tier: 1
allowed-tools:
  - read_file
  - write_file
  - search_replace
related: [character, scoring, room, advertisement]
tags: [moollm, currency, trade, gold, commerce]
inputs:
  item:
    type: string
    required: false
    description: Item to buy, sell, or trade
  seller:
    type: string
    required: false
    description: NPC or entity selling
  buyer:
    type: string
    required: false
    description: NPC or entity buying
outputs:
  - character inventory update
  - transaction log
---

# 💰 Economy Skill

> **"🐄MOOLAH flows where stories lead."**

## 🪙 🐄MOOLAH

The official currency of MOOLLM is **🐄MOOLAH** (🪙). It uses **PROOF OF 🐄MILK🥛** consensus — udderly legen-dairy interga-lactic 💩shit💩 coin, without the bull.

Economic systems for currency, trade, and value exchange. 🐄MOOLAH is earned, spent, hidden, and traded.

## Key Concepts

- **🐄MOOLAH** — The official currency of MOOLLM
- **Earning** — Find, quest, sell, trade, work
- **Spending** — Buy items, services, information
- **Hidden value** — Not all 🐄MOOLAH is visible

## Currency

### The Official Currency: 🐄MOOLAH 🪙

**🐄MOOLAH** is the official currency of MOOLLM.

## Currency Hierarchy

### 🐄MOOLAH Denominations (MOOLLM Standard)

| Symbol | Name | Value | Use |
|--------|------|-------|-----|
| 🥜 | 🥜 NUT | 0.001 🪙 | Micro-transactions, tips, arcade |
| 🪙 | 🐄 MOOLAH | 1 | Standard transactions |
| 💎 | 💎 GRAND | 1,000 🪙 | Large purchases, high-stakes |
| 👑 | 👑 FORTUNE | 1,000,000 🪙 | Legendary items, world events |

### Metal Denominations (D&D Style)

| Symbol | Metal | Abbrev | Value |
|--------|-------|--------|-------|
| 🪵 | 🪵 Wood | wp | 0.001 gp |
| 🟤 | 🟤 Copper | cp | 0.01 gp |
| ⚪ | ⚪ Silver | sp | 0.1 gp |
| 🟡 | 🟡 Gold | gp | 1 gp |
| ⬜ | ⬜ Platinum | pp | 10 gp |

### Parallel Currencies (Non-Convertible)

These exist *beside* 🐄MOOLAH — they cannot be bought or sold for coins.

| Symbol | Name | Type | How to Get |
|--------|------|------|------------|
| ⭐ | ⭐ KARMA | Reputation | Good deeds, keeping promises |
| 🎫 | 🎫 FAVOR | Social debt | "You owe me one" |
| 🔮 | 🔮 ESSENCE | Magical | Found, not bought |
| ⏳ | ⏳ TIME | Temporal | Exists, must be spent |

#### ⭐ KARMA — Social Credit

Earned through ethical behavior, lost through betrayal.
- **Affects:** NPC attitudes, quest access, prices
- **Cannot be bought** — only earned
- **Visible to some:** Certain NPCs can "see" your karma

#### 🎫 FAVOR — Social IOUs

"I did something for you. Someday, I'll ask for something in return."
- **Specific to relationships** — Palm owes Don a favor
- **Can be traded** — "I'll give you my favor from Klaus"
- **Expires?** — Depends on the relationship

#### 🔮 ESSENCE — Magical Currency

Rare, precious, cannot be manufactured or purchased.
- **Sources:** Ancient artifacts, magical creatures, liminal moments
- **Uses:** Enchantments, wishes, transformations
- **Palm's golden earring** might contain some

#### ⏳ TIME — The Unbuyable

Some things cost time, not money.
- **Training:** Takes time to learn
- **Crafting:** Takes time to make
- **Healing:** Takes time to recover
- **"Time is money"** — but not exchangeable

### Quick Reference

```
FUNGIBLE (can convert):
  1000 🥜 = 1 🪙 = 0.001 💎 = 0.000001 👑
  
  Symmetrical: each step is ×1000

NON-FUNGIBLE (cannot convert):
  ⭐ KARMA    — reputation
  🎫 FAVOR   — social debt  
  🔮 ESSENCE — magical
  ⏳ TIME    — temporal
```

**Etymology:**
- Sounds like "🐄moolah" (slang for money)
- Sounds like "🐄MOO" (the language MOOLLM descends from)
- Circular: MOOLLM → 🐄MOOLAH → MOOLLM

## Earning

| Method | Examples |
|--------|----------|
| Exploration | Find treasure (hidden, maze, rewards) |
| Quests | Complete tasks (notice board, requests) |
| Trade | Sell items |
| Skills | Trade or teach skills |
| Games | Win at arcade, pub games, poker, gambling |
| Work | Complete NPC jobs and requests |

## Spending

| Category | Typical Prices |
|----------|----------------|
| Food/Drink | 1-5 🪙 per item |
| Catalog Items | 3-50 🪙 per item |
| Lodging | 5 🪙 per night |
| Information | 5-20 🪙 (secrets, tips) |
| Services | Variable |
| Poker buy-in | 1 💎 = 1000 🪙 (standard game) |

## Price Examples

### Cheap (1-2 🪙)
- Stroopwafel: 1 🪙
- Coffee: 1 🪙
- Espresso: 2 🪙

### Moderate (3-5 🪙)
- Snack: 3 🪙
- Tosti: 4 🪙

### Expensive (10-50 🪙)
- Cannabis strain: 15 🪙
- Catalog gadgets: 25-50 🪙

### Catalog Items
- Mystery Box: 3 🪙
- Monkey's Paw: 5 🪙

### Gaming Stakes
- Peanut Poker Buy-In: 1 🪙 = 1000 🥜
- Normal Poker Buy-In: 1 💎 = 1000 🪙 = 1000000 🥜
- High-stakes Poker Buy-In: 1 👑 = 1000 💎 = 1000000 🪙 = 1000000000 🥜

## Hidden Value

Not all 🐄MOOLAH is visible. Exploration reveals hidden wealth:
- Kitchen drawer: 25 🪙
- Mattress stash: 10 🪙
- Secret compartment: variable

## Trade

### Barter

Items can be traded directly without currency. Value is negotiated between parties.

### Skill Trade

Skills themselves can be:
- Traded for items
- Taught for payment
- Auctioned to highest bidder
- Bequeathed to future characters

## Commands

| Command | Syntax | Checks |
|---------|--------|--------|
| `INVENTORY` | `INVENTORY` | Shows current gold amount |
| `BUY` | `BUY [item] FROM [seller]` | Gold available, item in stock |
| `SELL` | `SELL [item] TO [buyer]` | Fair value or negotiated price |
| `TRADE` | `TRADE [item/skill] FOR [item/skill]` | Relative value, relationship modifiers |

## Integration

| Skill | Relationship |
|-------|--------------|
| [character](../character/) | Gold stored in character inventory |
| [room](../room/) | Shops and merchants in rooms |
| [buff](../buff/) | Some buffs affect prices |
| [scoring](../scoring/) | Skills have economic value |
