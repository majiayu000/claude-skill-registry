# HGB Standards (German GAAP)

name: hgb-standards
description: German GAAP (HGB) — Bilanzierung, GoB, Maßgeblichkeitsprinzip

## When to Activate

- User asks about German accounting standards (HGB) or Handelsrecht
- Applying Grundsätze ordnungsmäßiger Buchführung (GoB)
- Evaluating the Maßgeblichkeitsprinzip (authoritative principle linking tax and commercial accounting)
- Accounting for Rückstellungen, Abschreibungen, or Herstellungskosten under HGB
- Comparing HGB treatment with IFRS for German companies

## Core Concepts

### HGB Framework

The Handelsgesetzbuch (HGB) is the German Commercial Code governing financial reporting for all German commercial entities. It applies to:
- Einzelkaufleute (sole traders)
- Personengesellschaften (partnerships: OHG, KG, GmbH & Co. KG)
- Kapitalgesellschaften (corporations: GmbH, AG, KGaA)

**Key legislation hierarchy:**
```
HGB (Handelsgesetzbuch) — primary source
  §§ 238-263: Allgemeine Vorschriften (general provisions)
  §§ 264-335: Kapitalgesellschaften (corporations)
  §§ 336-339: Genossenschaften (cooperatives)
  §§ 340-341: Kreditinstitute, Versicherungen (banks, insurers)
  §§ 342-342e: Rechnungslegungsgremium (accounting standards body)

DRS (Deutsche Rechnungslegungs Standards) — interpretive guidance from DRSC
EStG (Einkommensteuergesetz) — tax law, linked via Maßgeblichkeitsprinzip
```

**Who must apply HGB:**
- All Kapitalgesellschaften must prepare HGB financial statements
- Listed companies must additionally prepare IFRS consolidated statements (EU IAS Regulation)
- Non-listed groups may voluntarily apply IFRS for consolidated statements (§ 315e HGB)
- Individual (statutory) financial statements must always follow HGB (basis for tax and profit distribution)

### Grundsätze ordnungsmäßiger Buchführung (GoB)

GoB are the fundamental accounting principles underlying HGB. They are partly codified and partly derived from legal practice and academic doctrine.

**Core principles:**

| Principle | German | HGB Reference | Meaning |
|-----------|--------|---------------|---------|
| Completeness | Vollständigkeit | § 246 Abs. 1 | All assets, liabilities, income, expenses must be recorded |
| Clarity | Klarheit | § 243 Abs. 2 | Financial statements must be clear and comprehensible |
| Going concern | Fortführung | § 252 Abs. 1 Nr. 2 | Assume continuation of business activity |
| Individual valuation | Einzelbewertung | § 252 Abs. 1 Nr. 3 | Assets and liabilities valued individually |
| Prudence | Vorsichtsprinzip | § 252 Abs. 1 Nr. 4 | Cautious valuation; anticipate losses, not gains |
| Realization | Realisationsprinzip | § 252 Abs. 1 Nr. 4 | Revenue only when realized (delivery, performance) |
| Imparity | Imparitätsprinzip | § 252 Abs. 1 Nr. 4 | Unrealized losses must be recognized; unrealized gains must not |
| Accrual | Periodenabgrenzung | § 252 Abs. 1 Nr. 5 | Income/expenses allocated to the correct period |
| Consistency | Stetigkeit | § 252 Abs. 1 Nr. 6 | Consistent application of valuation methods |

**The Vorsichtsprinzip (prudence principle) is the dominant principle in HGB, unlike IFRS where neutrality/faithful representation takes precedence. This leads to systematically more conservative HGB balance sheets.**

### Maßgeblichkeitsprinzip (Authoritative Principle)

The Maßgeblichkeitsprinzip (§ 5 Abs. 1 EStG) establishes that the commercial balance sheet (Handelsbilanz) is authoritative for the tax balance sheet (Steuerbilanz).

```
Grundsatz:
Handelsbilanz → Steuerbilanz (was in der Handelsbilanz steht, gilt auch steuerlich)

Ausnahmen:
- Steuerliche Sondervorschriften gehen vor (z.B. § 6 EStG Bewertung)
- Steuerliche Wahlrechte können unabhängig von der Handelsbilanz ausgeübt werden
  (seit BilMoG 2009 — Durchbrechung der umgekehrten Maßgeblichkeit)
```

**Before BilMoG (2009):** Umgekehrte Maßgeblichkeit required that tax-only options had to be mirrored in the commercial accounts. This is largely abolished.

**After BilMoG:** Tax choices no longer need to be reflected in the Handelsbilanz. This means HGB and tax balance sheets can now diverge more significantly, creating more latente Steuern (deferred taxes).

### Bewertungsvorschriften (Valuation Rules)

**Anschaffungskosten (acquisition cost) — § 255 Abs. 1 HGB:**
```
Purchase price
+ Incidental acquisition costs (transport, customs, notary)
- Reductions in purchase price (rebates, discounts)
= Anschaffungskosten
```

**Herstellungskosten (production cost) — § 255 Abs. 2-3 HGB:**
```
Mandatory inclusion (Untergrenze):
  Material costs (Materialeinzelkosten)
  + Manufacturing labor (Fertigungseinzelkosten)
  + Special direct costs (Sondereinzelkosten)
  + Material overhead (Materialgemeinkosten) — mandatory since BilMoG
  + Manufacturing overhead (Fertigungsgemeinkosten) — mandatory since BilMoG

Optional inclusion (Wahlrecht):
  + General administrative overhead (Verwaltungsgemeinkosten)
  + Social facility costs (Aufwendungen für soziale Einrichtungen)

Prohibited inclusion:
  - Research costs (Forschungskosten)
  - Selling costs (Vertriebskosten)

Development costs: Wahlrecht to capitalize (§ 248 Abs. 2 HGB) with distribution restriction (§ 268 Abs. 8 HGB)
```

### Abschreibungen (Depreciation / Amortization)

**Planmäßige Abschreibungen (scheduled depreciation) — § 253 Abs. 3 HGB:**
- Applied to fixed assets with limited useful life
- Methods: straight-line (linear), declining balance (degressiv), units of production
- Useful lives based on AfA-Tabellen (tax depreciation tables) as practical guidance

**Außerplanmäßige Abschreibungen (unscheduled write-downs) — § 253 Abs. 3-4 HGB:**
- Financial fixed assets: only if impairment is expected to be permanent (dauerhaft)
- Other fixed assets: write-down if impairment is expected to be permanent (Wahlrecht for temporary impairment abolished for Kapitalgesellschaften since BilMoG)
- Current assets: strict lower-of-cost-or-market (strenges Niederstwertprinzip) — must write down to lower fair value

**Wertaufholung (reversal of write-down) — § 253 Abs. 5 HGB:**
- Mandatory reversal if reasons for write-down no longer exist (Zuschreibungspflicht)
- Exception: goodwill write-downs cannot be reversed

### Rückstellungen (Provisions)

**Mandatory provisions (Passivierungspflicht) — § 249 Abs. 1 HGB:**
- Ungewisse Verbindlichkeiten (uncertain liabilities)
- Drohende Verluste aus schwebenden Geschäften (onerous contracts)
- Unterlassene Aufwendungen für Instandhaltung (deferred maintenance, if within 3 months of year-end)
- Gewährleistungen ohne rechtliche Verpflichtung (warranties without legal obligation, based on past practice)

**Measurement — § 253 Abs. 1-2 HGB:**
```
Rückstellungen = best estimate of settlement amount (Erfüllungsbetrag)

Long-term provisions (> 1 year):
  Must be discounted using the average market interest rate
  of the past 7 years for the corresponding maturity
  (Published monthly by Deutsche Bundesbank)
```

### Latente Steuern (Deferred Taxes)

**§ 274 HGB (Kapitalgesellschaften):**
- Temporary differences between Handelsbilanz and Steuerbilanz
- Active latente Steuern (DTA): Wahlrecht to capitalize (optional)
- Passive latente Steuern (DTL): Passivierungspflicht (mandatory)
- If net DTA: activation is optional; if activated, distribution restriction applies (§ 268 Abs. 8 HGB)
- If net DTL: must be recognized

**Key difference from IFRS/US GAAP:** HGB uses the balance sheet liability method like IFRS but with the option (not obligation) to recognize net DTAs.

## Methodology

### HGB vs IFRS Key Differences

| Topic | HGB | IFRS |
|-------|-----|------|
| Dominant principle | Vorsichtsprinzip (prudence) | Faithful representation / neutrality |
| Revenue recognition | Realisationsprinzip (simpler) | IFRS 15 five-step model |
| Leases (lessee) | Economic ownership test | IFRS 16 — all on balance sheet |
| Development costs | Wahlrecht to capitalize | Capitalize if IAS 38 criteria met |
| Goodwill | Amortize over useful life (max 10 yr, §253 HGB) | No amortization, annual impairment |
| Provisions | Erfüllungsbetrag, 7-year avg discount rate | Best estimate, current market rate |
| Fair value measurement | Limited (primarily cost model) | Extensive fair value (IFRS 13) |
| Deferred taxes | Net DTA: Wahlrecht; Net DTL: Pflicht | IAS 12: recognize all (probable DTAs) |
| Inventory LIFO | Permitted | Prohibited |
| Revaluation of assets | Not permitted above cost | Permitted (IAS 16 revaluation model) |
| Consolidation scope | Stimmrechtsmehrheit or control | IFRS 10: control model |

### Practical Impact on Financial Statements

HGB financials typically show:
- **Lower equity** — due to prudence principle, limited asset recognition
- **Lower total assets** — no ROU assets for operating leases, limited capitalization
- **More provisions** — onerous contract provisions (drohende Verluste) mandatory
- **Goodwill amortized** — reduces intangible assets over time
- **Lower but more stable earnings** — less mark-to-market volatility

## Templates

### HGB Bilanzgliederung (Balance Sheet Structure per § 266 HGB)

```
AKTIVA (Assets)
A. Anlagevermögen (Non-current assets)
   I.   Immaterielle Vermögensgegenstände
   II.  Sachanlagen
   III. Finanzanlagen
B. Umlaufvermögen (Current assets)
   I.   Vorräte
   II.  Forderungen und sonstige Vermögensgegenstände
   III. Wertpapiere
   IV.  Kassenbestand, Guthaben bei Kreditinstituten
C. Rechnungsabgrenzungsposten (Prepaid expenses)
D. Aktive latente Steuern
E. Aktiver Unterschiedsbetrag aus Vermögensverrechnung

PASSIVA (Equity & Liabilities)
A. Eigenkapital
   I.   Gezeichnetes Kapital
   II.  Kapitalrücklage
   III. Gewinnrücklagen
   IV.  Gewinnvortrag / Verlustvortrag
   V.   Jahresüberschuss / Jahresfehlbetrag
B. Rückstellungen
C. Verbindlichkeiten
D. Rechnungsabgrenzungsposten (Deferred income)
E. Passive latente Steuern
```

## Quality Gate

Before finalizing HGB accounting, verify:

- [ ] GoB principles are consistently applied (especially Vorsichtsprinzip)
- [ ] Herstellungskosten include mandatory components (material + manufacturing overhead since BilMoG)
- [ ] Abschreibungen follow appropriate useful lives (AfA-Tabellen as guidance)
- [ ] Rückstellungen are measured at Erfüllungsbetrag (settlement amount, not historical cost)
- [ ] Long-term provisions are discounted using the Bundesbank 7-year average rate
- [ ] Latente Steuern are correctly computed (net DTA: Wahlrecht; net DTL: Pflicht)
- [ ] Maßgeblichkeitsprinzip is correctly applied (deviations documented)
- [ ] Goodwill is amortized over estimated useful life (maximum 10 years)
- [ ] Bilanzgliederung follows § 266 HGB structure
- [ ] GuV follows either Gesamtkostenverfahren or Umsatzkostenverfahren (§ 275 HGB)
- [ ] Größenklassen (size classes per § 267 HGB) are determined for disclosure requirements
- [ ] Anhang (notes) includes all mandatory disclosures for Kapitalgesellschaften
- [ ] Lagebericht (management report) is prepared if required (§ 289 HGB)
