---
name: consolidation
description: 'description: Group consolidation — IFRS 10, intercompany elimination,
  minority interests'
---

# Group Consolidation

name: consolidation
description: Group consolidation — IFRS 10, intercompany elimination, minority interests

## When to Activate

- User needs to prepare or understand consolidated financial statements
- Determining consolidation scope under IFRS 10 (control assessment)
- Performing intercompany eliminations (sales, loans, dividends)
- Calculating goodwill and non-controlling interests
- Applying the equity method for associates or proportional consolidation for joint ventures
- Handling currency translation for foreign subsidiaries (IAS 21)

## Core Concepts

### Consolidation Scope — IFRS 10 Control Model

An investor controls an investee when it has all three:
1. **Power** over the investee (ability to direct relevant activities)
2. **Exposure to variable returns** from the investee
3. **Ability to use power to affect returns**

**Assessment indicators:**

| Factor | Suggests Control | Does Not Suggest Control |
|--------|-----------------|------------------------|
| Voting rights | > 50% voting rights | < 20% with no other indicators |
| Board composition | Majority of board appointed | Minority representation only |
| Contractual arrangements | Power to direct key decisions | Advisory role only |
| De facto control | Largest shareholder with dispersed remainder | Multiple large shareholders with blocking rights |
| Potential voting rights | Currently exercisable options | Out-of-the-money or restricted options |
| Special purpose entities | Bears majority of risks/rewards | Merely a service provider |

**Consolidation thresholds:**
```
> 50% voting rights (or control)  → Full consolidation (IFRS 10)
20-50% significant influence       → Equity method (IAS 28)
Joint control (shared equally)     → Equity method for joint ventures (IFRS 11)
                                     or proportional consolidation (permitted under some GAAPs)
< 20% no significant influence     → Financial instrument (IFRS 9)
```

### Full Consolidation — Step-by-Step

**Step 1: Uniform accounting policies**
- All group entities must apply the same accounting policies
- Adjust subsidiary accounts to group policies before consolidation
- Align reporting dates (maximum 3-month difference allowed under IFRS 10)

**Step 2: Aggregate financial statements**
- Line-by-line addition of all assets, liabilities, income, and expenses
- Parent + Subsidiary A + Subsidiary B + ... = Aggregated total

**Step 3: Eliminate the parent's investment**
```
At acquisition (initial consolidation):
  Dr. Net identifiable assets at fair value (FV adjustments)
  Dr. Goodwill (residual)
  Dr. Non-controlling interest (NCI)
    Cr. Investment in subsidiary (parent's books)
    Cr. Subsidiary's equity (pre-acquisition)
```

**Step 4: Eliminate intercompany balances and transactions** (see detailed section below)

**Step 5: Recognize non-controlling interests**
- NCI share of subsidiary's post-acquisition equity
- Presented within equity but separately from parent's equity
- NCI share of profit/loss presented separately on the income statement

**Step 6: Eliminate pre-acquisition equity of subsidiaries**
- Subsidiary's equity at acquisition date is replaced by PPA and goodwill
- Only post-acquisition retained earnings flow through consolidated reserves

### Intercompany Eliminations

**IC Revenue and COGS:**
```
Subsidiary A sells goods to Subsidiary B for $1,000
A recorded: Revenue $1,000
B recorded: Inventory/COGS $1,000 (if sold through) or Inventory $1,000 (if still held)

Elimination entry:
  Dr. Revenue $1,000
    Cr. COGS $1,000 (if goods sold through to external customer)

If goods still in B's inventory with unrealized profit:
  Dr. Revenue $1,000
    Cr. COGS $800 (A's cost)
    Cr. Inventory $200 (unrealized profit margin)
```

**IC Loans and Interest:**
```
Parent lends $5,000 to subsidiary at 5% interest

Elimination:
  Dr. Intercompany payable (subsidiary) $5,000
    Cr. Intercompany receivable (parent) $5,000

  Dr. Interest income (parent) $250
    Cr. Interest expense (subsidiary) $250
```

**IC Dividends:**
```
Subsidiary declares dividend to parent

Elimination:
  Dr. Dividend income (parent) $____
    Cr. Dividends declared (subsidiary) $____

Note: NCI share of dividends is NOT eliminated (represents cash outflow to external parties)
```

**IC Fixed Asset Transfers:**
```
Subsidiary A sells equipment to Subsidiary B:
  A's carrying amount: $800
  Transfer price: $1,200
  A's gain: $400

Elimination at transfer:
  Dr. Gain on sale $400
    Cr. Property, plant & equipment $400

Subsequent periods: adjust depreciation for the unrealized gain
  Dr. Accumulated depreciation (excess depreciation)
    Cr. Depreciation expense
```

### Goodwill Calculation

```
=== GOODWILL AT ACQUISITION ===

Consideration transferred (FV):                    $____
+ NCI at acquisition (full goodwill or partial):    $____
+ FV of previously held interest (step acq.):      $____
= Total                                            $____

Less: Net identifiable assets at FV:
  Assets at FV                                      $____
  - Liabilities at FV                              ($____)
  - Contingent liabilities at FV                   ($____)
  = Net identifiable assets                         $____

Goodwill                                            $____
```

**NCI measurement options (IFRS 3 — election per transaction):**
- **Full goodwill method:** NCI at fair value (includes NCI's share of goodwill)
- **Partial goodwill method:** NCI at proportionate share of net identifiable assets (goodwill attributable to parent only)

### Non-Controlling Interests (NCI)

**Initial recognition:** At acquisition date (full FV or proportionate share — see above)

**Subsequent measurement:**
```
NCI at period end = NCI at acquisition
                  + NCI share of post-acquisition profits
                  - NCI share of dividends
                  +/- NCI share of OCI
                  +/- Changes in ownership without loss of control
```

**Transactions with NCI (no loss of control):**
- Changes in parent's ownership that do not result in loss of control are equity transactions
- No gain/loss in P&L; difference between consideration and NCI adjustment goes to parent's equity

**Loss of control:**
- Deconsolidate subsidiary on the date control is lost
- Recognize gain/loss in P&L
- Remeasure any retained interest at fair value

### Equity Method (IAS 28)

For associates (significant influence, typically 20-50%) and joint ventures (IFRS 11):

```
Investment at acquisition:          $____ (cost = consideration paid)
+ Share of post-acquisition profit: $____
- Share of dividends received:     ($____)
- Impairment (if any):             ($____)
+/- Share of OCI:                   $____
= Carrying amount of investment:    $____
```

**P&L impact:** Single line — "Share of profit of associates" (after tax)
**Balance sheet:** Single line — "Investments in associates" within non-current assets

**Upstream/downstream transactions:** Eliminate unrealized profit to the extent of the investor's interest.

### Currency Translation (IAS 21)

**Step 1: Determine functional currency** of each entity (currency of primary economic environment)

**Step 2: Translate to presentation currency (if different):**
```
Assets and liabilities:    Closing rate (balance sheet date)
Income and expenses:       Average rate for the period (or transaction date rate)
Equity:                    Historical rate

Translation difference → Other Comprehensive Income (OCI) — recycled to P&L on disposal
```

**Goodwill:** Treated as an asset of the foreign operation → translated at closing rate. Exchange differences on goodwill go to OCI.

**Hyperinflationary economies (IAS 29):**
- Restate financial statements for inflation before translating
- All items at closing rate (no average rate for P&L)

## Methodology

### Consolidation Process Workflow

1. **Collect reporting packages** from all subsidiaries (standardized template)
2. **Review and adjust** for group policy alignment, cut-off differences
3. **Convert currencies** for foreign subsidiaries (functional → presentation)
4. **Aggregate** all entity financial statements line by line
5. **Eliminate investment** in subsidiaries (replace with PPA, goodwill, NCI)
6. **Eliminate IC balances** (receivables/payables, loans)
7. **Eliminate IC transactions** (revenue/COGS, interest, dividends, management fees)
8. **Eliminate unrealized IC profits** (inventory, fixed assets)
9. **Calculate NCI** share of post-acquisition results
10. **Test goodwill** for impairment (annual or triggering event)
11. **Prepare consolidated statements** (BS, P&L, OCI, equity, cash flow)
12. **Reconcile** — verify elimination entries balance, NCI ties, goodwill rolls forward

### IC Reconciliation

Before consolidation, ensure IC balances match across entities:

```
=== INTERCOMPANY RECONCILIATION ===

Entity Pair    | Type       | Entity A Balance | Entity B Balance | Difference | Resolution
Parent / Sub A | Loan       | Receivable $5M   | Payable $5M      | $0         | Matched
Parent / Sub B | Trade      | Receivable $1.2M | Payable $1.1M    | $0.1M      | Timing — invoice in transit
Sub A / Sub B  | Mgmt fee   | Receivable $0.3M | Payable $0.3M    | $0         | Matched
```

**Common causes of IC mismatches:**
- Timing differences (invoices in transit, payments not yet received)
- FX differences (entities recording at different rates)
- Classification differences (one entity in trade AP, other in accruals)
- Genuine errors (missed postings)

## Templates

### Goodwill and NCI Roll-Forward

```
=== GOODWILL ROLL-FORWARD ===

                          | Sub A  | Sub B  | Sub C  | Total
Opening Balance           | ____   | ____   | ____   | ____
+ Acquisitions            | ____   |   —    | ____   | ____
- Impairment              |   —    | (____)  |   —    | (____)
+/- FX translation        | ____   | ____   | ____   | ____
+/- Measurement period adj| ____   |   —    |   —    | ____
Closing Balance           | ____   | ____   | ____   | ____

=== NCI ROLL-FORWARD ===

                          | Sub A  | Sub B  | Total
Opening Balance           | ____   | ____   | ____
+ NCI share of profit     | ____   | ____   | ____
- NCI share of dividends  | (____)  | (____)  | (____)
+/- NCI share of OCI      | ____   | ____   | ____
+/- Ownership changes     | ____   |   —    | ____
Closing Balance           | ____   | ____   | ____
```

## Quality Gate

Before finalizing consolidated financial statements, verify:

- [ ] Control assessment under IFRS 10 is documented for all significant investments
- [ ] All subsidiaries use uniform accounting policies (adjusted if different)
- [ ] Reporting dates are aligned (maximum 3-month gap, with adjustment for significant events)
- [ ] IC balances are reconciled with differences resolved or explained
- [ ] All IC revenue, costs, dividends, and interest are fully eliminated
- [ ] Unrealized IC profits in inventory and fixed assets are eliminated
- [ ] Goodwill is correctly calculated and allocated to CGUs for impairment testing
- [ ] NCI is presented separately in equity and in the income statement
- [ ] Currency translation uses correct rates (closing for BS, average for P&L)
- [ ] Translation differences are recognized in OCI (not P&L)
- [ ] Equity method investments show single-line P&L and BS treatment
- [ ] Consolidation adjustments are documented and auditable
- [ ] Cash flow statement eliminates IC cash flows (dividends, loan repayments)
- [ ] Segment reporting (IFRS 8) reflects management's internal reporting structure
