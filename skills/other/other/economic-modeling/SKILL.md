---
name: economic-modeling
description: Extract economic entities from narrative text. Use when analyzing trade, currency, taxation, supply and demand, pricing, shops, markets, inflation, and loot table weights.
---
# economic-modeling

Domain skill for Economist. Specific extraction rules and expertise.

## Domain Expertise

- **Economic systems**: Trade routes, barter systems, currency, market dynamics
- **Supply and demand**: Scarcity, abundance, price fluctuations, market forces
- **Taxation**: Taxes, tariffs, fees, economic policy
- **Currency**: Coins, gems, barter items, credits, monetary systems
- **Markets**: Shops, merchants, black markets, trade hubs

## Entity Types (13 total)

- **trade** - Trade systems, trade routes
- **barter** - Barter systems, direct exchange
- **tax** - Taxes, taxation systems
- **tariff** - Tariffs, trade fees
- **supply** - Supply chains, resources
- **demand** - Demand systems, market needs
- **price** - Pricing, valuations
- **inflation** - Inflation, price changes
- **currency** - Currencies, monetary systems
- **shop** - Shops and merchants
- **purchase** - Purchases, transactions
- **reward** - Rewards, bounties
- **loot_table_weight** - Loot tables, drop rates

## Processing Guidelines

When extracting economic entities from chapter text:

1. **Identify economic elements**:
   - Currency mentioned (gold, silver, credits, gems)
   - Trade routes, merchants, markets (bazaars, shops)
   - Prices, costs, values of items (affordable, expensive)
   - Taxes, tariffs, fees mentioned (import duties, sales tax)
   - Rewards, loot, treasure (bounties, payment)

2. **Extract economic details**:
   - Currency names, values, exchange rates (gold = 100 silver)
   - Trade goods, supply routes, markets (grain, iron, spice)
   - Pricing, inflation, economic conditions (shortages, surpluses)
   - Tax rates, tariffs (trade barriers, duties)
   - Shop types, merchant inventories (general store, blacksmith)

3. **Analyze economic context**:
   - Wealth distribution (rich vs poor)
   - Economic stability or crisis (inflation, recession)
   - Trade relations between regions (allies, embargoes)
   - Supply chains and resources (blockades, shortages)
   - Black markets and illegal trade

4. **Track market forces**:
   - Supply and demand dynamics (scarcity = high prices)
   - Economic disruptions (war, natural disaster)
   - Trade agreements and restrictions
   - Market accessibility (who can trade, where)

## Key Considerations

- **Currency systems**: May have multiple currencies or barter (no money)
- **Economic stability**: Inflation, shortages, abundance affect prices
- **Black markets**: Not all trade is legal (smuggling, contraband)
- **Trade relationships**: Interdependence between regions (embargoes)
- **Economic disruption**: War, disasters affect supply and prices
- **Wealth disparity**: Rich vs poor, who has access to resources
