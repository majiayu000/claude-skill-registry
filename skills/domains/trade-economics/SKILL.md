---
name: trade-economics
description: 'name: trade-economics'
---

# Trade Economics

name: trade-economics
description: International trade — comparative advantage, trade policy. Cover Ricardo, H-O, tariffs, WTO, GVCs.

## When to Activate

- Analyzing comparative advantage and trade patterns between countries
- Evaluating the impact of tariffs, quotas, and trade barriers
- Assessing trade agreements and WTO dispute implications
- Understanding global value chains (GVCs) and supply chain economics
- Modeling the welfare effects of trade liberalization or protectionism
- Analyzing terms of trade, trade balances, and current account dynamics
- Evaluating trade policy options (FTAs, customs unions, MFN treatment)
- Assessing the impact of trade on labor markets, wages, and inequality

## Core Concepts

### Classical Trade Theory

**Ricardian Model — Comparative Advantage:**
```
A country should specialize in and export goods where it has the
LOWEST OPPORTUNITY COST, not the lowest absolute cost.

Example:
                    Wine (hours/unit)    Cloth (hours/unit)
  Portugal               80                   90
  England               120                  100

  Portugal: Opportunity cost of wine = 80/90 = 0.89 cloth
  England:  Opportunity cost of wine = 120/100 = 1.20 cloth

  Portugal has comparative advantage in wine (lower opportunity cost)
  England has comparative advantage in cloth

  Both countries gain from trade even though Portugal is more
  efficient at producing BOTH goods (absolute advantage in both)
```

**Key insight:** Trade is driven by relative (not absolute) productivity differences. Even the least productive country has a comparative advantage in something.

### Heckscher-Ohlin (H-O) Model

**Factor proportions theory:**
- Countries export goods that use their abundant factor intensively
- Capital-abundant countries export capital-intensive goods
- Labor-abundant countries export labor-intensive goods

**Key predictions:**
- **H-O theorem:** Trade pattern determined by relative factor endowments
- **Stolper-Samuelson theorem:** Trade liberalization benefits the abundant factor and hurts the scarce factor. In developed countries, trade with developing countries raises returns to capital and skilled labor but reduces unskilled wages
- **Factor price equalization theorem:** Free trade tends to equalize factor prices across countries (wages converge, returns to capital converge)
- **Rybczynski theorem:** Growth in one factor increases output of the good using that factor intensively and decreases output of the other good

**Leontief Paradox:** The US (capital-abundant) exported labor-intensive goods in the 1950s — contradicting H-O predictions. Explanations: human capital, technology differences, natural resources.

### New Trade Theory

**Economies of scale and imperfect competition:**
- Intra-industry trade: Countries trade similar goods (German cars for Japanese cars) — driven by product differentiation and increasing returns to scale
- First-mover advantages: Countries that establish industries early can maintain dominance through learning curves and scale economies
- Home market effect: Industries locate in countries with large domestic demand for the product, then export surplus
- Strategic trade policy: Government support (subsidies, R&D funding) can help domestic firms capture rents in imperfectly competitive global industries

### Trade Policy Instruments

**Tariffs:**
```
Effects of an import tariff:
  - Consumer surplus:   Decreases (higher prices)
  - Producer surplus:   Increases (domestic producers benefit from protection)
  - Government revenue: Increases (tariff revenue = t x M)
  - Net welfare effect: Negative for small countries (deadweight loss)
                        Potentially positive for large countries
                        (terms of trade improvement may exceed deadweight loss)

Effective rate of protection:
  ERP = (VA_t - VA_f) / VA_f x 100%

  VA_t = Value added under tariff protection
  VA_f = Value added under free trade

  Tariff escalation: Higher tariffs on processed goods than raw materials
  → ERP on processing can be much higher than nominal tariff rate
```

**Non-tariff barriers:**
| Instrument | Mechanism | WTO Status |
|------------|-----------|------------|
| Import quota | Quantity restriction on imports | Generally prohibited |
| Voluntary export restraint | Exporter limits own exports | Prohibited since Uruguay Round |
| Anti-dumping duty | Duty on imports sold below "normal value" | Permitted under WTO rules |
| Countervailing duty | Duty to offset foreign subsidies | Permitted with investigation |
| Technical barriers (TBT) | Product standards, labeling | Permitted if non-discriminatory |
| Sanitary/phytosanitary (SPS) | Health and safety standards | Permitted if science-based |
| Local content requirements | Minimum domestic input share | Prohibited under TRIMs |
| Government procurement | Preferences for domestic suppliers | Covered by GPA (plurilateral) |

### WTO Framework

**Core principles:**
- **Most Favored Nation (MFN):** Treat all WTO members equally — best tariff rate given to one must be given to all (exceptions: FTAs, customs unions, GSP for developing countries)
- **National treatment:** Imported goods treated no less favorably than domestic goods once inside the border
- **Bound tariffs:** Tariff ceilings committed in negotiations — actual applied rates can be lower
- **Transparency:** Publish trade regulations, notify changes
- **Dispute settlement:** Binding dispute resolution mechanism (panels, Appellate Body)

**Trade agreements hierarchy:**
```
Depth of integration (ascending):
  1. Preferential trade agreement (PTA): Reduced tariffs on selected goods
  2. Free trade agreement (FTA): Zero tariffs on substantially all trade between members
  3. Customs union: FTA + common external tariff (e.g., EU, Mercosur)
  4. Common market: Customs union + free movement of factors (labor, capital)
  5. Economic union: Common market + harmonized economic policies
  6. Monetary union: Economic union + single currency (Eurozone)
```

### Global Value Chains (GVCs)

**Concept:** Production fragmented across countries — each country performs specific tasks/stages rather than producing complete goods.

**GVC metrics:**
- **Foreign value added (FVA) in exports:** Share of a country's gross exports that consists of imported intermediate inputs. Higher FVA = deeper GVC integration
- **Backward participation:** Using foreign inputs in exports (importing to export)
- **Forward participation:** Supplying inputs that other countries use in their exports
- **GVC position index:** Forward participation / backward participation. >1 indicates upstream position (raw materials, components); <1 indicates downstream (assembly, final goods)

**Trade in value added (TiVA):**
```
Gross exports overstate bilateral trade imbalances when GVCs are involved.

Example: iPhone assembled in China using components from Japan, Korea, US
  Gross export value (China → US): $300
  Chinese value added:             $10 (assembly labor and margin)
  Actual bilateral value added:    Much smaller than gross trade data suggests

TiVA adjusts for this by tracking where value is actually created.
```

**GVC risks:**
- Supply chain disruptions (pandemics, geopolitical tensions, natural disasters)
- Reshoring and nearshoring trends reducing GVC length
- Trade policy uncertainty (tariffs on intermediate goods amplified through GVC)
- Concentration risk (single-source dependencies for critical inputs)

### Terms of Trade

```
Terms of Trade (ToT) = Price of Exports / Price of Imports x 100

ToT improvement: Export prices rise relative to import prices
  → Country can buy more imports for each unit of exports
  → Real income gain

ToT deterioration: Import prices rise relative to export prices
  → Country needs to export more to buy same imports
  → Real income loss

Commodity exporters: ToT highly volatile, driven by commodity price cycles
Manufacturing exporters: ToT more stable, but subject to competitive pressure
```

## Methodology

1. **Trade pattern analysis**: Identify revealed comparative advantage (RCA) using Balassa index. RCA > 1 indicates comparative advantage in that product category
2. **Tariff impact modeling**: Estimate consumer surplus loss, producer surplus gain, government revenue, and deadweight loss. For large countries, include terms of trade effects
3. **GVC mapping**: Trace value chain stages across countries using TiVA data. Identify concentration risks and vulnerability to disruption
4. **Trade agreement assessment**: Evaluate trade creation vs trade diversion effects. Estimate tariff revenue losses and market access gains
5. **Labor market impact**: Apply Stolper-Samuelson framework. Estimate sectoral employment effects and adjustment costs

## Templates

### Trade Policy Impact Assessment

```
Policy measure: __________    Country: __________

                            Before      After       Change
Applied tariff rate          ____%       ____%       ____%
Import volume               _________   _________   ____%
Import value                _________   _________   ____%
Domestic production          _________   _________   ____%
Consumer price               _________   _________   ____%

Welfare effects (annual):
  Consumer surplus change:             _________
  Producer surplus change:             _________
  Government revenue change:           _________
  Net welfare effect:                  _________

Employment impact:
  Protected sector:                    +/- _________ jobs
  Downstream industries:               +/- _________ jobs
  Export sectors (retaliation risk):    +/- _________ jobs
```

### Trade Balance Decomposition

```
Country: __________    Period: __________    Currency: __________

                                Amount          % of GDP
Goods exports                   _________       ____%
Goods imports                   (_________)      ____%
Trade balance (goods)           _________       ____%

Services exports                _________       ____%
Services imports                (_________)      ____%
Trade balance (services)        _________       ____%

Current account balance         _________       ____%

Top export destinations:    1. __________  2. __________  3. __________
Top import sources:         1. __________  2. __________  3. __________
Export concentration (HHI):     _________
```

## Quality Gate

- [ ] Comparative advantage analysis uses relative (not absolute) productivity or cost measures
- [ ] Tariff analysis distinguishes nominal tariff rate from effective rate of protection
- [ ] Welfare analysis includes all components (consumer, producer, government, deadweight loss)
- [ ] GVC analysis uses trade-in-value-added data rather than gross trade flows where appropriate
- [ ] WTO consistency of proposed trade measures assessed (MFN, national treatment, bound rates)
- [ ] Distributional effects identified (winners and losers from trade policy changes)
- [ ] Retaliation risk and trade war escalation scenarios considered
- [ ] Terms of trade effects included for large-country analysis
- [ ] Adjustment costs and transition periods acknowledged for trade liberalization
- [ ] Data sources specified (WTO, UNCTAD, OECD TiVA, World Bank WITS)
